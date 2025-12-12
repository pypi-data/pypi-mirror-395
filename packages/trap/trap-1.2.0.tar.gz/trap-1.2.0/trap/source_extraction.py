# Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0
import dataclasses
from typing import Tuple

import numpy as np
import pandas as pd
from sourcefinder import image
from sourcefinder.accessors import open as pyse_open
from sourcefinder.accessors import sourcefinder_image_from_accessor
from sourcefinder.config import Conf

from trap.log import log_time, logger

PYSE_OUT_COLUMNS = {
    "ra": "ra",
    "dec": "dec",
    "ra_fit_err": "ra_err",
    "dec_fit_err": "dec_err",
    "peak_flux": "peak",
    "peak_flux_err": "peak_err",
    "int_flux": "flux",
    "int_flux_err": "flux_err",
    "significance_detection_level": "sig",
    "semimajor_axis": "smaj_asec",
    "semiminor_axis": "smin_asec",
    "parallactic_angle": "theta_celes",
    "error_radius": "error_radius",
    "chisq": "chisq",
    "reduced_chisq": "reduced_chisq",
}

# Currently, PySE has two different ways of returning results based on the configuration.
# Where possible it returns a Pandas DataFrame as of v0.5.0, but this is not yet
# always the case. This should always be an Pandas DataFrame after the following
# issue has been completed: https://github.com/transientskp/pyse/issues/90
PYSE_OUT_COLUMNS_LEGACY = {
    **PYSE_OUT_COLUMNS,
    "ew_sys_err": "ew_sys_err",
    "ns_sys_err": "ns_sys_err",
    "gaussian_fit": "gaussian",
}


def rms(data: np.ndarray) -> np.ndarray:
    """Returns the RMS of the data about the median.
    Args:
        data: a numpy array
    """
    data -= np.median(data)
    return np.sqrt((data**2).sum() / data.size)


def subregion(data: np.ndarray, reduction_factor: float = 2) -> np.ndarray:
    """Take the center region of the data where the size of the center region is defined by reduction_factor.

    Parameters
    ----------
    data: np.ndarray
        The image data to clip.
    reduction_factor: float
        The factor by which to decrease the image. This applies to each axis, so if ``reduction_factor=2`` and
        the image is of shape 100x100, then the shape of the clipped center region is 50x50. This effectively
        reduces the image size by a factor 4 (10.000 pixels to 2500 pixels).
        If ``reduction_factor=1``, the original 100x100 pixels are returned.
        It is also possibly to supply a floating point number. For the same 100x100 image, if a
        ``reduction_factor=1.5`` is supplied, the resulting slice is of shape (67,67).
        The way to make sense of this is that `100/1.5=66.6667`.

    Examples
    --------

    >>> import numpy as np
    >>> data = np.array([
    ...     [0, 1, 2, 1, 0],
    ...     [1, 2, 3, 2, 1],
    ...     [2, 3, 4, 3, 2],
    ...     [1, 2, 3, 2, 1],
    ...     [0, 1, 2, 1, 0]
    ... ])
    >>> subregion(data, 2)
    array([[2, 3, 2],
           [3, 4, 3],
           [2, 3, 2]])

    ..

    Returns
    -------
    numpy.ndarray: A slice of the original data at the center of the data.
    """
    height, width = data.shape
    center_x = width / 2
    center_y = height / 2
    offset_x = center_x / reduction_factor
    offset_y = center_y / reduction_factor
    # Make sure the slice is centered around the origin
    if center_x % 2 == 0:
        slice_x = slice(int(center_x - offset_x), int(center_x + offset_x))
    else:
        slice_x = slice(int(center_x - offset_x), int(center_x + offset_y + 1))

    if center_y % 2 == 0:
        slice_y = slice(int(center_y - offset_y), int(center_y + offset_y))
    else:
        slice_y = slice(int(center_y - offset_y), int(center_y + offset_y + 1))
    return data[slice_y, slice_x]  # Note that numpy indexing is in order (y,x)


def clip(data: np.ndarray, sigma: float = 3) -> np.ndarray:
    """Remove all values above a threshold from the array.
    Uses iterative clipping at sigma value until nothing more is getting clipped.

    Parameters
    ----------
    data: numpy.ndarray
        The data to clip
    sigma: float
        The amount of standard deviations that determine the threshold for clipping

    returns
    -------
    np.ndarray
        The data with the high values removed
    """
    raveled = data.ravel()
    median = np.median(raveled)
    std = np.std(raveled)
    newdata = raveled[np.abs(raveled - median) <= sigma * std]
    if len(newdata) and len(newdata) != len(raveled):
        return clip(newdata, sigma)
    else:
        return newdata


@log_time()
def read_pyse_image(
    path: str,
    margin=0,
    radius=1500,
    back_size_x=50,
    back_size_y=50,
    reduction_factor_for_rms=4,
    rms_min=0,
    rms_max=1,
    force_beam=True,
    ew_sys_err=0,
    ns_sys_err=0,
    **pyse_conf,
) -> Tuple[image.ImageData, dict, bool]:
    """
    Read an image with PySE that can be used in functions like :func:`sources_from_fits_pyse` and :func:`force_fit`.
    Some basic image metadata is also read and calculated. The metadata fields are:
     - rms
        The rms of the inner region of the image. The size of this inner region is determined by ``reduction_factor_for_rms``.
     - rms_min
        Lowest value of the RMS background map. Note that this is different from ``rms`` which uses the center region of the image rather than a RMS background map.
     - rms_max
        Largest value of the RMS background map. Note that this is different from ``rms`` which uses the center region of the image rather than a RMS background map.
     - freq_eff
        Effective frequency of the image in Hz.
        That is, the mean frequency of all the visibility data which comprises this image.
     - freq_bw
        The frequency bandwidth of this image in Hz.
     - taustart_ts
        Timestamp of the start of the observaion.
     - url
        Location of the image
     - rb_smaj
        The semi-major axis of the restoring beam, in degrees.
     - rb_smin
        The semi-minor axis of the restoring beam, in degrees.
     - rb_pa
        The position angle of the restoring beam (from north to east to the major axis), in degrees.
     - centre_ra
        The central right-ascention coordinate (J2000) (or pointing centre) of the region, in degrees.
     - centre_dec
        The central declination coordinate (J2000) (or pointing centre) of the region, in degrees.
     - xtr_radius
        The radius of the circular mask used for source extraction, in degrees.

    The image is also checked for quality. The quality check involves a check for the values where
    the image is rejected if it has all nodta values (nan, inf, -inf) or if the ``rms`` is below
    the ``rms_min`` or above the ``rms_max`` values. These min and max values are set in the :ref:`input arguments <input_arguments>`.

    Parameters
    ----------
        fits_path: str
            The path to the .fits file containing the image of which the sources are to be extracted.
        margin: int
            The margin in pixels from the edge of the image within which sources are ignored.
            This exclusion area combines with radius.
        radius: int,
            The radius in pixels around the center of the image, outside of which sources are ignored.
            This exclusion area combines with margin.
        back_size_x: int
            Widht of the background boxes as uses in SEP.
            See https://sep.readthedocs.io/en/v1.1.x/api/sep.Background.html#sep.Background
        back_size_y: int
            Height of the background boxes as used in SEP.
            See https://sep.readthedocs.io/en/v1.1.x/api/sep.Background.html#sep.Background
        reduction_factor_for_rms: float
            The reduction_factor passed to :func:`subregion` used to slice the data at the center
            before calculating the rms.
        ew_sys_err: float
            Systematic errors in units of arcseconds which augment the sourcefinder-measured errors on source positions when performing source association. These variables refer to an absolute angular error along an east-west and north-south axis respectively. (NB Although these values are stored during the source-extraction process, they affect the source-association process.)
        ns_sys_err: float
            Same as ew_sys_err but in perpendicular direction

    Returns: (sourcefinder.image.ImageData, dict, bool)
        A tuple containing:
         - A PySE image that can be used for source extraction
         - Metadata of the image
         - Whether the image is rejected or not
    """
    im = pyse_open(path)

    source_params = set(PYSE_OUT_COLUMNS.values())
    conf = Conf(
        image=dict(
            margin=margin,
            radius=radius,
            back_size_x=back_size_x,
            back_size_y=back_size_y,
            vectorized=True,
            force_beam=force_beam,
            ew_sys_err=ew_sys_err,
            ns_sys_err=ns_sys_err,
            **pyse_conf,
        ),
        export=dict(
            pandas_df=True,
            source_params=list(source_params),
        ),
    )
    pyse_im = sourcefinder_image_from_accessor(
        im,
        conf=conf,
    )

    # Extract metadata from image
    pyse_im_meta = im.extract_metadata()
    try:
        # Note: If pyse_im.data is empty, pyse_im.rmsmap errors on an assert, see:
        #       https://github.com/transientskp/pyse/blob/a43b64d684775605051adf9f754bb0ce6eda3493/sourcefinder/image.py#L246
        #       7 April 2025, Timo Millenaar
        rmsmap = pyse_im.rmsmap
        rms_min = rmsmap.min()
        rms_max = rmsmap.max()
    except AssertionError:
        rms_min = float("nan")
        rms_max = float("nan")
    im_meta = dict(
        rms=rms(clip(subregion(pyse_im.data.data, reduction_factor_for_rms))),
        rms_min=rms_min,
        rms_max=rms_max,
        freq_eff=pyse_im_meta["freq_eff"],
        freq_bw=pyse_im_meta["freq_bw"],
        taustart_ts=pyse_im_meta["taustart_ts"],
        url=pyse_im_meta["url"],
        rb_smaj=pyse_im_meta["beam_smaj_pix"] * np.abs(pyse_im_meta["deltax"]),
        rb_smin=pyse_im_meta["beam_smin_pix"] * np.abs(pyse_im_meta["deltay"]),
        rb_pa=np.rad2deg(pyse_im_meta["beam_pa_rad"]),
        centre_ra=pyse_im_meta["centre_ra"],
        centre_dec=pyse_im_meta["centre_decl"],
        xtr_radius=radius,
    )

    # Reject image if all data is nan or inf or when the rms value is not within the supplied bounds
    rejected = False
    if np.all(~np.isfinite(pyse_im.data)):
        rejected = True
        logger.info(f"Image rejected because it contains no data: {im_meta['url']}")
    if not rms_min < im_meta["rms"] < rms_max:
        rejected = True
        logger.info(
            f"Image rejected because the rms ({im_meta['rms']}) is not within the supplied thresholds: rms_min: {rms_min}, rms_max: {rms_max}. Image path: {im_meta['url']}"
        )
    im_meta["rejected"] = int(rejected)

    return pyse_im, im_meta, rejected


@log_time()
def sources_from_fits_pyse(
    pyse_im: image.ImageData,
    *,
    rejected: bool = False,
    detection_threshold: float = 8,
    analysis_threshold: float = 3,
    deblend_nthresh: float = 0,
) -> pd.DataFrame:
    """Extract sources from an image using PySE.

    Parameters
    ----------
    pyse_im: sourcefinder.image.ImageData
        The pyse image as read using :func:`read_pyse_image`
    detection_threshold: float
        The detection threshold, as a multiple of the RMS
        noise. At least one pixel in a source must exceed this value
        for it to be regarded as significant.
    analysis_threshold: float
        Analysis threshold, as a multiple of the RMS
        noise. All the pixels within the island that exceed
        this will be used when fitting the source.
    deblend_nthresh: int
        Number of subthresholds to use for
        deblending. Set to 0 to disable.

    Returns
    -------
    `pandas.DataFrame`
        A dataframe where each row is an obtained source.
        The columns contain the attributes of the corces.

        Column names with explenation:

            ra [deg]: float
                Right ascension coordinate of the source
            dec [deg]: float
                Declination coordinate of the source
            ra_fit_err [deg]: float
                1-sigma error from the gaussian fit in right ascension.
                Note that for a source located towards the poles the ra_fit_err
                increases with absolute declination.
            dec_fit_err [deg]: float
                1-sigma error from the gaussian fit in declination
            peak_flux [Jy]: float
            peak_flux_err [Jy]: float
            int_flux [Jy]: float
            int_flux_err [Jy]: float
            significance_detection_level: float
            semimajor_axis [arcsec]: float
            semiminor_axis [arcsec]: float
            parallactic_angle [deg]: float
            ew_sys_err [arcsec]: float
                Telescope dependent systematic error in east-west direction.
            ns_sys_err [arcsec]: float
                Telescope dependent systematic error in north-south direction.
            error_radius [arcsec]: float
                A pessimistic on-sky position error estimate in arcsec.
            gaussian_fit: bool
            chisq: float
            reduced_chisq: float
    """
    if rejected:
        sources = pd.DataFrame({}, columns=PYSE_OUT_COLUMNS.keys())
        sources.index.name = "id"
        return sources

    # Note: for explanation of variables see tkp/db/general.py::insert_extracted_sources:
    #       https://github.com/transientskp/tkp/blob/b34582712b82b888a5a7b51b3ee371e682b8c349/tkp/db/general.py#L106
    extraction_results = pyse_im.extract()

    if isinstance(extraction_results, pd.DataFrame):
        extraction_results.rename(
            lambda name: name.split(".")[-1].lower(), axis="columns", inplace=True
        )
        extraction_results = extraction_results[PYSE_OUT_COLUMNS.values()]
        sources = extraction_results.rename(
            columns={v: k for k, v in PYSE_OUT_COLUMNS.items()}
        )
        sources["ns_sys_err"] = pyse_im.conf.image.ns_sys_err
        sources["ew_sys_err"] = pyse_im.conf.image.ew_sys_err
        sources["gaussian_fit"] = True
    else:
        extraction_results = [r.serialize(pyse_im.conf) for r in extraction_results]
        sources = pd.DataFrame(
            extraction_results, columns=PYSE_OUT_COLUMNS_LEGACY.keys()
        )
    # uncertainty_ew: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    sources["uncertainty_ew"] = (
        np.sqrt(sources["ew_sys_err"] ** 2 + sources["error_radius"] ** 2) / 3600.0
    )
    # uncertainty_ns: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    sources["uncertainty_ns"] = (
        np.sqrt(sources["ns_sys_err"] ** 2 + sources["error_radius"] ** 2) / 3600.0
    )

    logger.info(f"Found {len(sources)} sources")

    sources.index.name = "id"
    return sources


def force_fit(
    pyse_im: image.ImageData,
    positions: np.ndarray,
    ew_sys_err: float = 10,
    ns_sys_err: float = 10,
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Fit the specified locations using PySE.

    Parameters
    ----------
    pyse_im: sourcefinder.image.ImageData
        The pyse image as read using :func:`read_pyse_image`
    positions: np.ndarray
        A numpy array with the positions of the sources to be force fitted in the form [[ra_1, dec_1], [ra_2, dec_2]]
    ew_sys_err [arcsec]: float
        Telescope dependent systematic error in east-west direction.
    ns_sys_err [arcsec]: float
        Telescope dependent systematic error in north-south direction.
    Returns
    -------
    pd.DataFrame
        A dataframe with the force-fitted sources
    """
    box_in_beampix = 10
    boxsize = box_in_beampix * max(pyse_im.beam[0], pyse_im.beam[1])
    ids = np.arange(len(positions))
    # Some fits could have been dropped by PySE. Also return the fit_ids so the caller can know what ids were dropped
    forced_fits, fit_ids = pyse_im.fit_fixed_positions(
        positions, boxsize, ids=range(len(positions))
    )

    conf = Conf(
        image=pyse_im.conf.image,
        export=dataclasses.replace(
            pyse_im.conf.export, source_params=list(PYSE_OUT_COLUMNS_LEGACY.values())
        ),
    )
    force_fit_results = [r.serialize(conf, every_parm=True) for r in forced_fits]
    forced_sources = pd.DataFrame(
        force_fit_results, columns=PYSE_OUT_COLUMNS_LEGACY.keys()
    )

    # uncertainty_ew: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    forced_sources["uncertainty_ew"] = (
        np.sqrt(forced_sources["ew_sys_err"] ** 2 + forced_sources["error_radius"] ** 2)
        / 3600.0
    )
    # uncertainty_ns: sqrt of quadratic sum of systematic error and error_radius
    # divided by 3600 because uncertainty in degrees and others in arcsec.
    forced_sources["uncertainty_ns"] = (
        np.sqrt(forced_sources["ns_sys_err"] ** 2 + forced_sources["error_radius"] ** 2)
        / 3600.0
    )

    logger.info(f"Forced fit for {len(forced_sources)} sources")

    return forced_sources, fit_ids
