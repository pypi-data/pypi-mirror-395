import sys
from pathlib import Path
from typing import List, Optional, Tuple

import dask
import numba
import numpy as np
import pandas as pd
import sourcefinder.image
import sqlalchemy
from astropy.io import fits
from astropy.wcs import WCS

from trap.associate import associate
from trap.io import open_db
from trap.log import logger
from trap.source_extraction import (
    force_fit,
    read_pyse_image,
    sources_from_fits_pyse,
)


def _force_single_threaded_numba():
    """Monkey-patch all numba functions that could invoke a parallel runtime and
    make sure that no parallel runtime is spawned. This can reduce performance
    of the compiled numba function inquestion but this is sometimes nesecary
    if no threadsafe numba runtime is available on the system.
    """
    _real_guvectorize = numba.guvectorize
    _real_vectorize = numba.vectorize
    _real_jit = numba.jit
    _real_njit = numba.njit

    def guvectorize_cpu(*args, **kwargs):
        kwargs["target"] = "cpu"
        return _real_guvectorize(*args, **kwargs)

    def vectorize_cpu(*args, **kwargs):
        kwargs["target"] = "cpu"
        return _real_vectorize(*args, **kwargs)

    def jit_cpu(*args, **kwargs):
        kwargs.pop("parallel", None)
        return _real_jit(*args, **kwargs)

    def njit_cpu(*args, **kwargs):
        kwargs.pop("parallel", None)
        return _real_njit(*args, **kwargs)

    numba.guvectorize = guvectorize_cpu
    numba.vectorize = vectorize_cpu
    numba.jit = jit_cpu
    numba.njit = njit_cpu


# Ceck if numba can find a threadsafe runtime.
# See: https://numba.pydata.org/numba-doc/dev/user/threading-layer.html#selecting-a-threading-layer-for-safe-parallel-execution
# We cannot use the 'workqueue' threading layer in combination with the
# multithreading invoked by Dask. To check the numba runtyime we first
# have to compile a function, otherwise numba will report that no runtime
# has been initialized.
@numba.njit(parallel=True)
def _force_numba_runtime_init(vals):
    """Dummy function that does just enough work for numba
    to not optimize the function away but initialize a threading
    runtime instead."""
    return 2 * vals


_force_numba_runtime_init(np.arange(2))
if numba.threading_layer() == "workqueue":
    logger.warn(
        """Numba was unable to find a threadsafe runtime. Falling back to single threaded execution of numba functions.
        For more information, see:
        https://numba.pydata.org/numba-doc/dev/user/threading-layer.html#selecting-a-threading-layer-for-safe-parallel-execution
    """
    )
    _force_single_threaded_numba()


def force_fit_null_detections(
    im_id: int,
    pyse_im: sourcefinder.image.ImageData,
    source_list: pd.DataFrame,
    null_detection_ids: np.ndarray,
    extracted_sources: pd.DataFrame,
):
    """Force fit locations of known sources that were not found in the ``pyse_im`` corresponding to image index ``im_id``.

    Parameters
    ----------
    im_id: int
        The index of the image in which the sources are to be force-fitted
    pyse_im: sourcefinder.image.ImageData
        The PySE image in which to fit the sources
    source_list: pandas.DataFrame
        DataFrame with the known sources
        Columns used in this function:
            - "ra": The Right Ascension of the source (most recent detection, barring force fits)
            - "dec": The Declination of the source (most recent detection, barring force fits)
            - "latest_extracted_source_id": The index of the last source in the lightcurve, matching the
              extracted sources database.
              # TODO: point to table in database description (yet to be documented)
    null_detection_ids: list
        A list of indices matching the source_list indicating which known sources should be fitted in
        the supplied ``pyse_im``.
    extracted_sources: pandas.DataFrame
        A DataFrame containing the sources already extracted from the ``pyse_im`` that is to be updated
        with the sources fitted in this function (new fits are added to this DataFrame).
        # TODO: point to table in database description (yet to be documented)

    Returns
    -------
    pandas.DataFrame
        An updated ``extracted_sources`` where the sources fitted in this function have been added.

    """
    if null_detection_ids is None or len(null_detection_ids) == 0:
        return extracted_sources

    null_detection_coords = source_list.loc[
        null_detection_ids, ["ra", "dec"]
    ].to_numpy()
    logger.info(f"Forcing {len(null_detection_ids)} detections")

    # TODO: The following method adds empty rows for sources that were not found.
    #          This keeps the lightcurve easy to reconstruct, without any gaps in the parent
    #          ids. This only works if reasonable locations are force-fitted. If we have
    #          a lot of force fits outside of the AOI we get a lot of nan-entries in the database.
    #          Therefore we need to make sure to only force-fit on sources in the AOI, which
    #          becomes a concern when the input fits files do not all overlap.
    #            ---> I.E. we need a spatial index when selecting sources from the source list
    #                 to force-fit or or even to associate with (which comes before force-fitting).

    # First create empty dataframe with correnct number of rows
    null_detection_fluxes = pd.DataFrame(
        np.nan,
        index=np.arange(len(null_detection_ids)),
        columns=extracted_sources.columns,
    )
    null_detection_flux_results, fit_ids = force_fit(
        pyse_im, positions=null_detection_coords
    )
    null_detection_flux_results = null_detection_flux_results.set_index(
        np.array(fit_ids)
    )
    # Now add all found fluxes to the dataframe. Rows related to sources that could not be force fitted will remain nan.
    null_detection_fluxes = null_detection_fluxes.assign(**null_detection_flux_results)
    # For sources that could not be force-fitted, set the coordinates to that of the sample location
    if len(fit_ids) != len(null_detection_ids):
        failed_fit_np_ids = np.setdiff1d(np.arange(len(null_detection_ids)), fit_ids)
        null_detection_fluxes.loc[failed_fit_np_ids, ["ra", "dec"]] = (
            null_detection_coords[failed_fit_np_ids]
        )

    source_list.loc[null_detection_ids, "peak_flux"] = (
        null_detection_fluxes.peak_flux.values
    )
    null_detection_fluxes["im_id"] = im_id
    null_detection_fluxes["src_id"] = null_detection_ids
    null_detection_fluxes["is_force_fit"] = True
    null_detection_fluxes["is_duplicate"] = False
    null_detection_fluxes = null_detection_fluxes.set_index(
        extracted_sources.index.max() + 1 + np.arange(len(null_detection_ids))
    )
    null_detection_fluxes["parent"] = source_list.loc[
        null_detection_ids, "latest_extracted_source_id"
    ].values

    extracted_sources = pd.concat([extracted_sources, null_detection_fluxes])

    return extracted_sources  # End force_fit_null_detections()


def update_source_list(
    nr_extracted_sources: int,
    im_id: int,
    source_list: pd.DataFrame,
    new_sources: pd.DataFrame,
    rejected: bool,
    max_nr_consecutive_force_fits: int,
    **association_kwargs,
) -> Tuple[
    pd.DataFrame,
    np.ndarray,
    pd.DataFrame,
    int,
]:
    """Compare the ``new_sources`` with the ``source_list`` containing the known sources and update
    the list of known sources accordingly.

    Also updates the source list to include the sources that will be force-fit.
    This is a promise in some sense that we will force fit these and in the meantime we continue associating
    while we are force fitting in a separate task. We do this because the force fit can take a long time we cannot afford to wait on it.

    .. Note ::

        It is possible for PySE to fail on a force fit. The association could therefore match sources with a parent that
        does not exist because PySE did not find a fit. To prevent this we create a dummy row in the database that has the
        id of the failed source and it's coordinates, but nan values for other source parameters. This way the lightcurve
        parent chain remains complete. The reconstructed lightcurves will then have nans at the locations where the force
        fit failed.

    ..

    Parameters
    ----------
    nr_extracted_sources
        The total number of extracted sources, which will be added to in this function
        and is used to determine the indices that are to be assigned to the new sources.
    im_id: int
        The index of the image corresponding the the ``new_sources``
    source_list
        A DataFrame containing the known sources before extracting the ``new_sources``.
        A copy of this dataframe will be modified to include the new sources and returned.
    new_sources: pd.DataFrame
        The sources extracted from the image with index ``im_id``
    **association_kwargs
        The keyword arguments passed to :func:`trap.association.associate`

    Returns
    -------
    pd.DataFrame
        The updated ``source_list``
    list
        A list containing source indices matching the updated ``source_list`` of sources that
        were already known but not found in the supplied ``new_sources``
    extracted_sources
        An updated version of ``new_sources`` where the following columns were added:
            - im_id
            - src_id
            - is_force_fit
            - is_duplicate
            - parent
    int
        The updated total number of extracted sources, needed to determine the index of new extracted sources
        in the following iteration.
    """
    if rejected:
        return (
            source_list,
            np.array([]),
            new_sources.copy(),
            nr_extracted_sources,
        )

    # For the first image, there is no need to associate.
    # Initialize the source list here.
    if source_list.empty:
        extracted_sources = new_sources.copy()
        extracted_sources = extracted_sources.set_index(np.arange(len(new_sources)))
        extracted_sources.index.name = "id"
        extracted_sources["im_id"] = im_id
        extracted_sources["src_id"] = new_sources.index
        extracted_sources["is_force_fit"] = False
        extracted_sources["is_duplicate"] = False
        extracted_sources["parent"] = -1

        null_detection_ids = np.array([])
        persistings_mapping = pd.DataFrame(
            [], columns=["original_id", "new_id", "de_ruiter"]
        )
        duplicate_mapping = pd.DataFrame(
            {"new_id": [], "original_id": [], "de_ruiter": []}
        )
        nr_extracted_sources += len(new_sources)
        source_list = new_sources[
            ["ra", "dec", "uncertainty_ns", "uncertainty_ew"]
        ].copy()
        source_list["nr_consecutive_force_fits"] = 0
        source_list["latest_extracted_source_id"] = np.arange(len(source_list))
        return (
            source_list,
            null_detection_ids,
            extracted_sources,
            nr_extracted_sources,
        )

    # Call the association, which matches up the sources in `new_sources` with the already known
    # sources in `source_list`. It returns a veriety of mappings that relate the IDs of the
    # new sources with those of the known sources.
    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        source_list, new_sources, **association_kwargs
    )

    # Trim the null_detection_ids to not include any source that has not naturally been found
    # for `max_nr_consecutive_force_fits` number of images in a row.
    null_detection_ids = null_detection_ids[
        source_list.loc[null_detection_ids, "nr_consecutive_force_fits"]
        <= max_nr_consecutive_force_fits
    ]

    # Update the source list by adding any new sources found
    extracted_sources = new_sources.copy()
    new_source_ids = [*new_ids, *duplicate_mapping.new_id]
    new_sources_slice = new_sources.loc[new_source_ids]
    new_source_ids = source_list.index.max() + np.arange(len(new_sources_slice)) + 1
    new_sources_slice = new_sources_slice.set_index(new_source_ids)
    # Initialize `latest_extracted_source_id` as -1, otherwise pandas will insert NaN on concat and
    # turns the series into a float instead of int.
    new_sources_slice["latest_extracted_source_id"] = -1
    new_sources_slice["nr_consecutive_force_fits"] = 0
    source_list = pd.concat([source_list, new_sources_slice])

    # Format extracted_sources table for later export.
    # Will allso be appended to if any force fitting is done in a later step.
    extracted_sources["im_id"] = im_id
    extracted_sources["src_id"] = np.nan
    extracted_sources["is_force_fit"] = False
    extracted_sources["is_duplicate"] = False
    extracted_sources["parent"] = -1
    # Update the src_id for persistant sources
    extracted_sources.loc[persistings_mapping["new_id"].values, "src_id"] = (
        persistings_mapping.original_id.values
    )
    if not duplicate_mapping.empty:
        # Update the src_id for duplicate sources
        extracted_sources.loc[duplicate_mapping["new_id"].values, "src_id"] = (
            new_source_ids[-len(duplicate_mapping) :]
        )  # <- I need the ID of the new source_list row, not original id
    # slice new_source_ids as to not include the duplicates
    extracted_sources.loc[new_ids, "src_id"] = new_source_ids[: len(new_ids)]
    # Update parent reference for persistant sources
    extracted_sources.loc[persistings_mapping["new_id"].values, "parent"] = (
        source_list.loc[
            persistings_mapping["original_id"].values, "latest_extracted_source_id"
        ].values
    )
    # Update parent reference for duplicate sources (i.e. excess sources in a one-to-many scenario)
    extracted_sources.loc[duplicate_mapping["new_id"].values, "parent"] = (
        source_list.loc[
            duplicate_mapping["original_id"].values, "latest_extracted_source_id"
        ].values
    )
    # Label the duplicate sources as such
    extracted_sources.loc[duplicate_mapping["new_id"].values, "is_duplicate"] = True
    # Update the index after adding the new sources
    extracted_sources = extracted_sources.set_index(
        nr_extracted_sources + np.arange(len(new_sources))
    )
    extracted_sources.index.name = "id"
    assert not np.any(
        np.isnan(extracted_sources["src_id"])
    ), "All new ids should be assigned something, nan is not allowed"

    # Update the source list
    update_cols = [
        "ra",
        "dec",
        "uncertainty_ns",
        "uncertainty_ew",
    ]
    source_list.loc[extracted_sources["src_id"].values, update_cols] = (
        extracted_sources[update_cols].set_index(
            source_list.loc[extracted_sources["src_id"].values].index
        )
    )
    source_list.loc[
        extracted_sources["src_id"].values, "latest_extracted_source_id"
    ] = extracted_sources.index.values

    # Update the latest_extracted_source_id here as a promise that we will fit these ids before export in a separate task
    null_detection_extracted_source_id = (
        extracted_sources.index.max() + 1
    ) + np.arange(len(null_detection_ids))
    source_list.loc[null_detection_ids, "latest_extracted_source_id"] = (
        null_detection_extracted_source_id
    )
    source_list.loc[null_detection_ids, "nr_consecutive_force_fits"] += 1
    source_list.loc[extracted_sources["src_id"].values, "nr_consecutive_force_fits"] = 0
    assert (
        not -1 in source_list.latest_extracted_source_id
    ), "Source list contains sources of which the latest_extracted_source_id was not set."

    return (
        source_list,
        null_detection_ids,
        extracted_sources,
        nr_extracted_sources + len(new_sources) + len(null_detection_ids),
    )  # end update_source_list()


def export_to_database(db_kwargs, im_id, im_meta, extracted_sources):
    """Write the data for time step ``im_id`` to the database.

    Parameters
    ----------
    db_kwargs: dict
        A dictionary containing the arguments for :func:`trap.io.open_db`
    im_id: int
        The index corresponding to the image
    im_meta: dict
        A dictionary containing the metadata corresponding to the image that is to be written to the database.
        # TODO: point to table in database description (yet to be documented)
    extracted_sources: dict
        A dictionary containing the information of each source that was fitted in the image (corresponding to the
        supplied ``im_id`` and ``im_meta``). These sources will be written to the database.
        # TODO: point to table in database description (yet to be documented)

    returns
    -------
    db_kwargs: dict
        Return the same database arguments, unaltered.
        This is exported such that this can be fed into the next call to export_database to enable the creation
        of a sequential Dask chain, which would prevent simultaneous execution of multiple `export_to_database`
        calls at once.
        # TODO: investigate if we can have parallel writes to the same table (I believe postgres supports this but sqlite less so)

    """
    db_engine = open_db(**db_kwargs)
    # Write image metadta table
    image_db = pd.DataFrame(
        {
            "id": [im_id],
            "rejected": [0],
            **im_meta,
        }
    )
    images_dtypes = {
        "id": sqlalchemy.Integer,
        "url": sqlalchemy.Text,
        "acquisition_date": sqlalchemy.Text,
        "rejected": sqlalchemy.Integer,  # sqlite does not support boolean but uses integers
    }
    image_db.to_sql(
        "images", db_engine, if_exists="append", index=False, dtype=images_dtypes
    )
    # Write extracted sources table
    extracted_sources.index.name = "id"
    extracted_sources.to_sql(
        "extracted_sources", db_engine, if_exists="append", index=True
    )
    return db_kwargs


def main(
    image_paths: List[Path],
    db_kwargs: dict,
    max_nr_consecutive_force_fits: int,
    pyse_config: Optional[dict] = None,
    association_kwargs: Optional[dict] = None,
):
    # These will be used as input to export_to_database_delayed and will become a delayed
    # object after the first pass through that function.
    db_kwargs_delayed = db_kwargs.copy()

    # Do not use mutable objects like dictionaries as default function arguments
    # because they can lead to unexpected behaviour on repeated function calls.
    # Use None as default and initialize here to work around this.
    pyse_config = {} if pyse_config is None else pyse_config
    association_kwargs = {} if association_kwargs is None else association_kwargs

    nr_extracted_sources = 0

    # Turn functions representing the core steps into delayed functions
    read_pyse_image_delayed = dask.delayed(read_pyse_image, nout=3)
    sources_from_fits_pyse_delayed = dask.delayed(sources_from_fits_pyse)
    update_source_list_delayed = dask.delayed(update_source_list, nout=4)
    force_fit_null_detections_delayed = dask.delayed(force_fit_null_detections)
    export_to_database_delayed = dask.delayed(export_to_database)

    # Start with first image to initiate, then loop over all other images to process
    source_list = pd.DataFrame({})
    for im_id, path in enumerate(image_paths):
        pyse_im, im_meta, rejected = read_pyse_image_delayed(str(path), **pyse_config)
        new_sources = sources_from_fits_pyse_delayed(pyse_im, rejected=rejected)
        source_list, null_detection_ids, extracted_sources, nr_extracted_sources = (
            update_source_list_delayed(
                nr_extracted_sources,
                im_id,
                source_list,
                new_sources,
                rejected,
                max_nr_consecutive_force_fits,
                **association_kwargs,
            )
        )
        extracted_sources_for_export = force_fit_null_detections_delayed(
            im_id, pyse_im, source_list, null_detection_ids, extracted_sources
        )
        db_kwargs_delayed = export_to_database_delayed(
            db_kwargs_delayed, im_id, im_meta, extracted_sources_for_export
        )

    dask.compute(db_kwargs_delayed, traverse=False)
    logger.info(
        f"TraP run completed, results stored in '{db_kwargs['db_backend']}' database '{db_kwargs['db_name']}'"
    )
    return  # End of main
