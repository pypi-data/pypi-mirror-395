from typing import Tuple

import astropy
import numpy as np
import pandas as pd
from astropy import coordinates


def de_ruiter_radius(
    *,
    p1_ra: np.ndarray,
    p1_dec: np.ndarray,
    p2_ra: np.ndarray,
    p2_dec: np.ndarray,
    p1_err_ns: np.ndarray,
    p1_err_ew: np.ndarray,
    p2_err_ns: np.ndarray,
    p2_err_ew: np.ndarray,
):
    r"""Find the 'de Ruiter radius' of two points, which is a weighted distance that takes the positional
    uncertainties of both points into account.

    This calculation is based on section 4.4.1 in the TraP paper[1].

    The equation is:

    .. math::

        r_{i,j} = \sqrt{
            \frac{
                ( \alpha_i - \alpha_j)^2 \cos^2( (\delta_i + \delta_j) / 2 )
            }{
                \sigma_{\alpha_i}^2 + \sigma_{\alpha_j}^2
            }
            +
            \frac{
                (\delta_i - \delta_j)^2
            }{
                \sigma_{\delta_i}^2 + \sigma_{\delta_j}^2
            }
        }

    Here the subscript `i` refers to a specific source and `j` refers to a potential new source.
    :math:`\alpha` is the right ascension of the source and :math:`\delta` the declination.
    :math:`\sigma_{\alpha}` and :math:`\sigma_{\delta}` refer to the uncertainty in right ascending and declination, respectively.

    [1] Swinbank, John D., et al. "The LOFAR transients pipeline." Astronomy and Computing 11 (2015): 25-48.

    Parameters
    ----------
    p1_ra: :class:`np.ndarray`
        The right ascension of the first point
    p1_dec: :class:`np.ndarray`
        The declination of the first point
    p2_ra: :class:`np.ndarray`
        The right ascension of the second point
    p2_dec: :class:`np.ndarray`
        The declination of the second point
    p1_err_ns: :class:`np.ndarray`
        The uncertainty in the right ascension coordinate of the first point in degrees
    p1_err_ew: :class:`np.ndarray`
        The uncertainty in the declination coordinate of the first point in degrees
    p2_err_ns: :class:`np.ndarray`
        The uncertainty in the right ascension coordinate of the second point in degrees
    p2_err_ew: :class:`np.ndarray`
        The uncertainty in the declination coordinate of the second point in degrees

    Returns
    -------
    :class:`np.ndarray`
        The de Ruiter radius as defined in the TraP paper[1]
    """
    return np.sqrt(
        ((p1_ra - p2_ra) ** 2 * np.cos(np.deg2rad((p1_dec + p2_dec) / 2)) ** 2)
        / (p1_err_ew**2 + p2_err_ew**2)
        + (p2_dec - p1_dec) ** 2 / (p2_err_ns**2 + p1_err_ns**2)
    )


def associate(
    sources: pd.DataFrame,
    new_sources: pd.DataFrame,
    de_ruiter_r_max: float = 5.68,
    surpress_duplications: bool = False,
) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame, pd.DataFrame]:
    """Relates new sources with existing sources.

    Start with a DataFrame that contains known sources and one that contains new sources.
    The new sources are then matched to the known sources.
    The sources can be obtained using :func:`trap.source_extraction.sources_from_fits_pyse`.

    Parameters
    ----------
    sources: :class:`pd.DataFrame`
        The list of know sources with at least the following columns:

            - "id" (index of source)
            - "ra" (right-ascension coordinate of source)
            - "dec" (declination coordinate of source))
            - "uncertainty_ns" (sqare root of quadratic sum of systematic error in north-south direction and the error_radius)
            - "uncertainty_ew" (sqare root of quadratic sum of systematic error in east-west direction and the error_radius)

    new_sources: :class:`pd.DataFrame`
        The list of new sources with at least the following columns:

            - "id" (index of source)
            - "ra" (right-ascension coordinate of source)
            - "dec" (declination coordinate of source))
            - "uncertainty_ns" (square root of quadratic sum of the systematic error in north-south direction and error_radius)
            - "uncertainty_ew" (square root of quadratic sum of the systematic error in east-west direction and error_radius)

    de_ruiter_r_max: float
        If the de Ruiter radius is larger than this value for a given source pair,
        the sources are considered to be different sources. If the radius is smaller than
        de_ruiter_r_max, the sources are elligable to be considered the same source.

    surpress_duplications: bool
        In the many-to-many case, prefer a connection to a source that is not connected yet over the nearest source if True.
        When False, always connect to the nearest source even if there are other, even closer, connections to that source already.
        False is the way both the vast pipeline and the original TraP operated and is the default here.

    Returns
    -------
    null_detection_ids: the ids corresponding to `new_sources.index` that were not found in sources
    new_source_ids: the ids corresponding to `sources.index` that were in new_sources but not in the original sources
    persistings_mapping: :class:`pd.DataFrame`:
        A dataframe containing the columns `[original_id, new_id, de_ruiter]` that map the indices
        from sources to new_sources of those that are identified as being a persistant source,
        meaning it is a source that occurs in both sourcse lists.
    duplicate_mapping: A dataframe containing the columns `[original_id, new_id, de_ruiter]` that map the indices
        of any access sources in new_sources to the nearest source in the original sources DataFrame.
    """
    # Find the nearby sources using astropy's kdtree method.
    # We get a correlation where we select the known sources that match new sources and vice versa.
    # One source may match several new sources and vice versa.
    # Therefore there are likely more matches than either sources or new soruces.
    # This is a first pass. Further down the nearby sources will be matched more carefully.
    source_coords = astropy.coordinates.SkyCoord(
        ra=sources["ra"], dec=sources["dec"], unit=astropy.units.deg
    )
    new_coords = astropy.coordinates.SkyCoord(
        ra=new_sources["ra"], dec=new_sources["dec"], unit=astropy.units.deg
    )
    bw_max = astropy.coordinates.Angle(
        420 * astropy.units.arcsec
    )  # FIXME: don't hardcode value, handle when configuration support is added
    new_coord_ids, source_coord_ids, sep2d, dist3d = source_coords.search_around_sky(
        new_coords, bw_max
    )
    source_selection = sources.iloc[source_coord_ids].reset_index()
    new_selection = new_sources.iloc[new_coord_ids].reset_index()

    # Calculate the 'de Ruiter radius' which we use to select the nearest source
    de_ruiter = de_ruiter_radius(
        p1_ra=source_selection.ra,
        p1_dec=source_selection.dec,
        p1_err_ew=source_selection.uncertainty_ew,
        p1_err_ns=source_selection.uncertainty_ns,
        p2_ra=new_selection.ra,
        p2_dec=new_selection.dec,
        p2_err_ew=new_selection.uncertainty_ew,
        p2_err_ns=new_selection.uncertainty_ns,
    )

    # Apply de_ruiter_mask, removing every source that is too far to be considered the same source
    de_ruiter_mask = de_ruiter < de_ruiter_r_max
    cross_index = pd.DataFrame(
        {
            "original_id": source_selection[sources.index.name or "index"],
            "new_id": new_selection[new_sources.index.name or "index"],
            "de_ruiter": de_ruiter,
        }
    )[de_ruiter_mask]

    if surpress_duplications:
        # Prune
        def prune(df, id):
            """If a source is present in multiple relations, say it is present in a
            many-to-one and a ont-to-many and connected to different sources,
            it should only be matched to one source, the one with the lowest de Ruiter radius.
            Here we assume the data is sorted by the de Ruiter radius.
            We also take in an id where we assume all rows that come before this ID are already pruned.
            Any row after this ID is removed if it contains a source that is in the row that matches the given id.
            """
            df_subset = df.iloc[id + 1 :]

            original_id = df.iloc[id]["original_id"]
            new_id = df.iloc[id]["new_id"]
            mask = ~(
                (df_subset["original_id"] == original_id)
                | (df_subset["new_id"] == new_id)
            )
            return pd.concat([df.iloc[: id + 1], df_subset.loc[mask]])

        cross_index_full = cross_index.copy()
        cross_index = cross_index.sort_values("de_ruiter")
        row_id = 0
        while row_id < (
            len(cross_index) - 1
        ):  # subtract 1 from length to account for 0-index
            cross_index = prune(cross_index, row_id)
            row_id += 1

    # One-to-one: Select those where only one new id and one old id align.
    original_id, original_id_count = np.unique(
        cross_index["original_id"], return_counts=True
    )
    original_one_match_mask = original_id_count == 1
    one_to_one_original_id = original_id[original_one_match_mask]
    one_to_one_original_id = cross_index.index[
        cross_index.original_id.isin(one_to_one_original_id)
    ]
    new_id, new_id_count = np.unique(cross_index["new_id"], return_counts=True)
    new_one_match_mask = new_id_count == 1
    one_to_one_new_id2 = new_id[new_one_match_mask]
    one_to_one_new_id2 = cross_index.index[cross_index.new_id.isin(one_to_one_new_id2)]
    one_to_one_ids = np.intersect1d(one_to_one_original_id, one_to_one_new_id2)
    one_to_one_index = cross_index.loc[one_to_one_ids]

    # One-to-many: Select those where one soruce matches several new sources. Duplicate the extra sources.
    candidates = cross_index[
        cross_index.original_id.isin(original_id[~original_one_match_mask])
    ]
    de_ruiter_min = candidates.groupby("original_id")["de_ruiter"].transform("min")
    one_to_many_matched = candidates[candidates["de_ruiter"] == de_ruiter_min]
    if not surpress_duplications:
        duplicate_mapping = candidates[candidates["de_ruiter"] != de_ruiter_min]
        duplicate_mapping = duplicate_mapping[
            ~duplicate_mapping["new_id"].isin(one_to_many_matched["new_id"])
        ]
        # Prevent the same new_id from having multiple `original_id` values assigned.
        # It is possible in the many-to-many case that a new_id is regarded as the duplicate
        # of multiple original sources. In such a case, pick only the pair with the smallest de_ruiter_r
        de_ruiter_min_2 = duplicate_mapping.groupby("new_id")["de_ruiter"].transform(
            "min"
        )
        duplicate_mapping = duplicate_mapping[
            duplicate_mapping["de_ruiter"] == de_ruiter_min_2
        ]

    # Many-to-one: Select those where we start with a group of sources but only one nearby source is found.
    #              The extra sources that are not matched will be considered null-detections.
    candidates = cross_index[cross_index.new_id.isin(new_id[~new_one_match_mask])]
    de_ruiter_min = candidates.groupby("new_id")["de_ruiter"].transform("min")
    to_drop_sources = candidates[candidates["de_ruiter"] != de_ruiter_min]
    many_to_one_matched = candidates[candidates["de_ruiter"] == de_ruiter_min]

    persistings_mapping = pd.concat(
        [one_to_one_index, one_to_many_matched, many_to_one_matched]
    )
    # A match in a many-to-many situation will show up in both one_to_many_matched and many_to_one_matched.
    # To prevent this, remove the duplicates
    persistings_mapping = persistings_mapping[
        ~persistings_mapping.index.duplicated(keep="first")
    ]  # FIXME: make more rigorous in many to many case

    # Make sure no one-to-one mapping contains multiple original_ids
    persistings_mapping = persistings_mapping[
        ~persistings_mapping["original_id"].duplicated(keep="first")
    ]  # FIXME: make more rigorous in many to many case

    # Make sure no one-to-one mapping contains multiple new_ids
    persistings_mapping = persistings_mapping[
        ~persistings_mapping["new_id"].duplicated(keep="first")
    ]  # FIXME: make more rigorous in many to many case

    new_ids = np.setdiff1d(new_sources.index, cross_index.new_id)
    null_detection_ids = np.setdiff1d(sources.index, persistings_mapping.original_id)

    if surpress_duplications:
        duplicates = []
        for id in new_ids:
            duplicate_rows = np.where(cross_index_full.new_id == id)[0]
            if len(duplicate_rows) > 0:
                candidates = cross_index_full.iloc[duplicate_rows]
                duplicates.append(
                    candidates[candidates["de_ruiter"] == candidates["de_ruiter"].min()]
                )
        if len(duplicates) > 0:
            duplicate_mapping = pd.concat(duplicates)
        else:
            duplicate_mapping = cross_index[:0]

    return (
        null_detection_ids,
        np.setdiff1d(new_ids, duplicate_mapping.new_id),
        persistings_mapping,
        duplicate_mapping,
    )
