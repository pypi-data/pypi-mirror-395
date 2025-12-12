from pathlib import Path

import pytest

from trap import io


@pytest.mark.parametrize(
    "path, expected_nr_files",
    [
        ("tests/data/lofar1", 3),
        ("tests/data/lofar1/*", 3),
        ("tests/data/lofar1/GRB201006A_final_2min_srcs-t000*-image-pb.fits", 3),
        ("tests/data/lofar1/GRB201006A_final_2min_srcs-t0001-image-pb.fits", 1),
        ("tests/data*/lofar*/GRB201006A_*.fits", 3),
    ],
)
def test_find_fits(path, expected_nr_files):
    fits_files = io.find_fits(path)

    assert len(fits_files) == expected_nr_files
    for f in fits_files:
        assert isinstance(f, Path)
        assert f.exists()
