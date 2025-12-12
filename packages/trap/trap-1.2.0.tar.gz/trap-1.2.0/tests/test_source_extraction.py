import numpy
import pytest

from trap import source_extraction


@pytest.mark.parametrize(
    "path, force_beam, expected_nr_sources",
    [
        (
            "tests/data/lofar1/GRB201006A_final_2min_srcs-t0000-image-pb.fits",
            False,
            218,
        ),
        (
            "tests/data/lofar1/GRB201006A_final_2min_srcs-t0001-image-pb.fits",
            False,
            215,
        ),
        (
            "tests/data/lofar1/GRB201006A_final_2min_srcs-t0002-image-pb.fits",
            False,
            216,
        ),
        ("tests/data/lofar1/GRB201006A_final_2min_srcs-t0000-image-pb.fits", True, 218),
        ("tests/data/lofar1/GRB201006A_final_2min_srcs-t0001-image-pb.fits", True, 215),
        ("tests/data/lofar1/GRB201006A_final_2min_srcs-t0002-image-pb.fits", True, 216),
    ],
)
def test_sources_from_fits_pyse(path, force_beam, expected_nr_sources):

    pyse_im, im_meta, rejected = source_extraction.read_pyse_image(
        path,
        force_beam=force_beam,
        detection_thr=8,
        analysis_thr=3,
        deblend_nthresh=0,
    )

    expected_meta_colums = {
        "rms",
        "rms_min",
        "rms_max",
        "freq_eff",
        "freq_bw",
        "taustart_ts",
        "url",
        "rb_smaj",
        "rb_smin",
        "rb_pa",
        "centre_ra",
        "centre_dec",
        "xtr_radius",
        "rejected",
    }
    for key in expected_meta_colums:
        assert key in im_meta, f"Expected '{key}' in image metadata but was not found"

    meta_key_diff = set(im_meta.keys()).difference(expected_meta_colums)
    if any(meta_key_diff):
        raise KeyError(f"Found unexpected keys in image meta: {meta_key_diff} ")

    sources = source_extraction.sources_from_fits_pyse(pyse_im)

    expected_columns = [
        "ra",
        "dec",
        "ra_fit_err",
        "dec_fit_err",
        "peak_flux",
        "peak_flux_err",
        "int_flux",
        "int_flux_err",
        "significance_detection_level",
        "semimajor_axis",
        "semiminor_axis",
        "parallactic_angle",
        "ew_sys_err",
        "ns_sys_err",
        "error_radius",
        "gaussian_fit",
        "chisq",
        "reduced_chisq",
        "uncertainty_ew",
        "uncertainty_ns",
    ]

    assert len(sources) == expected_nr_sources

    for col in expected_columns:
        assert col in sources
