import numba as nb
import numpy as np
import pandas as pd
import sqlalchemy


def construct_lightcurves(
    db_engine: sqlalchemy.engine.base.Engine = None,
    attribute: str = "int_flux",
    sources: pd.DataFrame = None,
):
    """Reconstruct a dataframe with lightcurves from the source relations defined in the standard database.

    Parameters
    ----------
    db_engine
        A sqlalchemy database engine.
    attribute: str
        The name of the attribute to use as value for the lightcurve.
        This can be any column name of the extraced_sources table.
    sources: pandas.DataFrame
        A DataFrame containing the extracted sources. By providing the sources
        there is no need to read the extracted_sources from the database. If the
        sources are already in memory, providing them like this is more performant
        than having to read the data from the database every time this function
        is called. This is especially relevant when this function is called several
        times with a different attribute on the same DataFrame with extracted sources.

    Returns
    -------
    A pandas DataFrame where each row is a lightcurve and each column is correlated to each image.
    """
    if sources is None:
        if db_engine is None:
            raise ValueError(
                "Either the argument 'db_engine' or 'sources' must be provided."
            )
        with db_engine.connect() as conn:
            query = "SELECT * FROM extracted_sources"
            sources = pd.read_sql_query(query, conn)

    lightcurves = pd.DataFrame(
        {
            "id": [],
        }
    ).set_index("id")
    total_nr_sources = sources.src_id.max() + 1
    for im_id in range(sources.im_id.max() + 1):
        fluxes = np.full(total_nr_sources, np.nan)
        im_slice = sources[sources.im_id == im_id]
        fluxes[im_slice.src_id.values] = im_slice[attribute].values
        lightcurves[f"im_{im_id}"] = fluxes
        # Update duplicate's history
        duplicate_slice = im_slice[im_slice.is_duplicate.astype("bool")]
        to_copy_slice = sources.loc[duplicate_slice["parent"]]
        lightcurves.loc[duplicate_slice["src_id"], lightcurves.columns[:-1]] = (
            lightcurves.loc[to_copy_slice["src_id"], lightcurves.columns[:-1]].values
        )

    return lightcurves


@nb.njit()
def _weighted_sum(ra, ra_err, dec, dec_err):
    """Private function used to calculate the weighted sums for ra and dec."""
    nr_sources = ra.shape[0]
    nr_images = ra.shape[1]
    weighted_sum_ra = np.zeros(nr_sources)
    sum_weight_ra = np.zeros(nr_sources)
    weighted_sum_dec = np.zeros(nr_sources)
    sum_weight_dec = np.zeros(nr_sources)
    for i in range(nr_images):

        mask = np.isfinite(ra[:, i])
        w_ra = 1 / ra_err[mask, i] ** 2
        w_dec = 1 / dec_err[mask, i] ** 2

        weighted_sum_ra[mask] += w_ra * ra[mask, i]
        sum_weight_ra[mask] += w_ra

        weighted_sum_dec[mask] += w_dec * dec[mask, i]
        sum_weight_dec[mask] += w_dec
    return weighted_sum_ra, sum_weight_ra, weighted_sum_dec, sum_weight_dec


@nb.njit()
def _first_image_of_detection(lightcurve):
    """Private function used to determine the first image each source was found in"""
    nr_sources = lightcurve.shape[0]
    nr_images = lightcurve.shape[1]
    first_image = np.full(nr_sources, fill_value=-1, dtype="int")
    already_found = np.full(nr_sources, False, dtype="bool")
    for i in range(nr_images):
        mask = np.isfinite(lightcurve[:, i])
        mask &= ~already_found
        first_image[mask] = i
        already_found[mask] = True
    return first_image


def construct_varmetric(db_engine: sqlalchemy.engine.base.Engine) -> pd.DataFrame:
    r"""Calculate lightcurve properties which can be used for filtering and isolating potential transients.

    The properties are based on the extracted_sources table.
    These properties are:
        - newsource
            Reference to the id of the first extracted source in the lightcurve.
        - v_int
            The flux coefficient of variation (V_ν), based on the integrated flux values.
        - eta_int
            The ‘reduced chi-squared’ variability index (η_ν), based on the integrated flux values.
        - sigma_rms_min
            Integrated flux from the from the extracted source that triggered an new source entry, divided by the minimum value of the estimated-RMS-map within the source-extraction region.
        - sigma_rms_max
            Integrated flux from the from the extracted source that triggered an new source entry, divided by the maximum value of the estimated-RMS-map within the source-extraction region.
        - lightcurve_max
            The maximum flux value of the lightcurve based on the integrated flux.
        - lightcurve_avg
            The average flux value of the lightcurve based on the integrated flux.
        - lightcurve_median
            The median flux value of the lightcurve based on the integrated flux.
        - wm_ra
            The weighted mean right ascension of the source, computed across all detections
            using inverse-squared positional uncertainties (1/ra_err²) as weights. This represents
            the best-estimate sky position in right ascension.
        - wm_dec
            The weighted mean declination of the source, computed across all detections
            using inverse-squared positional uncertainties (1/dec_err²) as weights. This represents
            the best-estimate sky position in declination.
        - avg_ra_err
            The average or mean of the right ascension uncertainties (ra_fir_err) across all detections
            contributing to the lightcurve. Represents the average measurement uncertainty in RA.
        - avg_dec_err
            The average or mean of the declination uncertainties (dec_fit_err) across all detections
            contributing to the lightcurve. Represents the average measurement uncertainty in Dec.
        - nr_datapoints
            The number of images that were used to calculate the variablility metrics per source.
            If a source was not naturally detected in a specific image the flux value is NaN.
            Such values are not used in the calculation of the variability metrics and do not
            count towards the total nr_datapoints for that source.
        - first_image
            The id of the first image in which a source was detected
        - first_detection_time
            The acquisition time of the first image in which a source was detected

    Parameters
    ----------
    db_engine
        A sqlalchemy database engine.

    Returns
    -------
    dict
        A dictionary with the lightcurve properties mentioned above.
    """
    with db_engine.connect() as conn:
        images = pd.read_sql_query("SELECT * FROM images", conn)
        sources = pd.read_sql_query("SELECT * FROM extracted_sources", conn)

    src_ids = np.unique(sources.src_id)
    first_extracted_source_id = np.zeros(len(src_ids), dtype=int)

    # Remove force fits as these are not suitable to variability metrics: https://git.astron.nl/RD/trap/-/issues/32#note_134250
    sources = sources[~sources.is_force_fit.astype(bool)]

    grouped = sources.groupby("src_id")
    im_ids = grouped["im_id"].min()
    first_extracted_source_id = grouped.id.min().values
    int_flux_first_src = sources.loc[first_extracted_source_id].int_flux

    lightcurves_int = construct_lightcurves(
        db_engine, attribute="int_flux", sources=sources
    )
    lightcurve_integrated_flux = lightcurves_int.to_numpy()
    lightcurves_int_err = construct_lightcurves(
        db_engine, attribute="int_flux_err", sources=sources
    )
    lightcurve_integrated_flux_error = lightcurves_int_err.to_numpy()

    nr_images_per_source = np.isfinite(lightcurve_integrated_flux).sum(axis=1)
    multiple_sources_mask = nr_images_per_source > 1
    lightcurve_integrated_flux_subset = lightcurve_integrated_flux[
        multiple_sources_mask
    ]
    lightcurve_integrated_flux_error = lightcurve_integrated_flux_error[
        multiple_sources_mask
    ]
    nr_images_per_source_masked = nr_images_per_source[multiple_sources_mask]

    integrated_flux_mean = (
        np.nansum(lightcurve_integrated_flux_subset, axis=1)
        / nr_images_per_source_masked
    )
    integrated_flux_mean_sq = (
        np.nansum(lightcurve_integrated_flux_subset**2, axis=1)
        / nr_images_per_source_masked
    )
    integrated_flux_mean_weighted = (
        np.nansum(
            lightcurve_integrated_flux_subset / lightcurve_integrated_flux_error**2,
            axis=1,
        )
        / nr_images_per_source_masked
    )
    integrated_flux_mean_weighted_sq = (
        np.nansum(
            lightcurve_integrated_flux_subset**2 / lightcurve_integrated_flux_error**2,
            axis=1,
        )
        / nr_images_per_source_masked
    )
    normalized_integrated_flux_weighted = (
        np.nansum(1.0 / lightcurve_integrated_flux_error**2, axis=1)
        / nr_images_per_source_masked
    )

    v_int = np.full(len(src_ids), np.nan)
    v_int[multiple_sources_mask] = (
        np.sqrt(
            nr_images_per_source_masked
            * (integrated_flux_mean_sq - integrated_flux_mean**2)
            / (nr_images_per_source_masked - 1.0)
        )
        / integrated_flux_mean
    )
    eta = np.full(len(src_ids), np.nan)
    eta[multiple_sources_mask] = (
        nr_images_per_source_masked
        * (
            integrated_flux_mean_weighted_sq
            - integrated_flux_mean_weighted**2 / normalized_integrated_flux_weighted
        )
        / (nr_images_per_source_masked - 1.0)
    )

    # Varmetric caluclations based on: https://github.com/transientskp/tkp/blob/b34582712b82b888a5a7b51b3ee371e682b8c349/tkp/testutil/db_subs.py#L188
    varmetric = pd.DataFrame(
        {
            "newsource": first_extracted_source_id,
            "v_int": v_int,
            "eta_int": eta,
        }
    )
    # The following are added separately such that the gaps are filled with nans and the lengths match the rest
    varmetric["lightcurve_max"] = np.nan
    varmetric["lightcurve_avg"] = np.nan
    varmetric["lightcurve_median"] = np.nan
    varmetric["lightcurve_max"] = np.nanmax(lightcurve_integrated_flux, axis=1)
    varmetric["lightcurve_avg"] = np.nanmean(lightcurve_integrated_flux, axis=1)
    varmetric["lightcurve_median"] = np.nanmedian(lightcurve_integrated_flux, axis=1)

    # Add weighted ra and dec metrics
    ra = construct_lightcurves(db_engine, attribute="ra")
    ra_err = construct_lightcurves(db_engine, attribute="ra_fit_err")
    dec = construct_lightcurves(db_engine, attribute="dec")
    dec_err = construct_lightcurves(db_engine, attribute="dec_fit_err")

    src_ids = ra.index.to_numpy()
    ra = ra.to_numpy()
    ra_err = ra_err.to_numpy()
    dec = dec.to_numpy()
    dec_err = dec_err.to_numpy()

    weighted_sum_ra, sum_weight_ra, weighted_sum_dec, sum_weight_dec = _weighted_sum(
        ra, ra_err, dec, dec_err
    )

    varmetric["wm_ra"] = weighted_sum_ra / sum_weight_ra
    varmetric["wm_dec"] = weighted_sum_dec / sum_weight_dec
    varmetric["av_ra_err"] = np.nanmean(ra_err, axis=1)
    varmetric["av_dec_err"] = np.nanmean(dec_err, axis=1)

    varmetric["nr_datapoints"] = nr_images_per_source

    first_image_detected_src = _first_image_of_detection(ra)
    assert (
        not -1 in first_image_detected_src
    ), "Sources were all values are NaN. This is not supposed to happen, please raise a github issue."
    varmetric["first_image"] = first_image_detected_src
    varmetric["first_detection_time"] = images.taustart_ts.get(
        first_image_detected_src
    ).values

    return varmetric.set_index(src_ids)
