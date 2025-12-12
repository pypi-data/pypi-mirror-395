import re
import subprocess

import numpy as np
import pandas as pd
import pytest
from db_verification import verify_database

import trap


def run_trap_cli(input_files, output_db, extra_args):
    """Use subprocess to call TraP through the CLI. The stdout is captured for later validation"""
    extra_args = [str(arg) for arg in extra_args]
    cli_args = ["trap-run", "--config_file", "trap_config.toml"]
    if isinstance(input_files, str):
        cli_args.append("-i")
        cli_args.append(input_files)
    else:
        # Explode file paths and give each a -i flag
        try:
            for path in input_files:
                cli_args.append("-i")
                cli_args.append(path)
        except TypeError as e:
            raise TypeError(
                f"Expected a string or an iterable of strings, got {type(input_files)}"
            ) from e
    cli_args.extend(extra_args)
    cli_args.extend(["--db_name", str(output_db)])

    result = subprocess.run(cli_args, stdout=subprocess.PIPE)
    return result.stdout.decode("utf8").split("\n")


@pytest.mark.parametrize(
    "extra_args",
    [
        ["--detection_threshold", 5],
        ["--analysis_threshold", 3],
        ["--im_radius", 700],
        ["--scheduler", "threads"],
        ["--scheduler", "distributed"],
    ],
)
def test_trap_run(tmp_path, extra_args):
    if not "-n" in extra_args:
        # Use two threads if not otherwise specified
        extra_args.append("-n")
        extra_args.append(2)

    input_files = "tests/data/lofar1/"
    output_db = tmp_path / "trap_test_output.db"
    stdout = run_trap_cli(input_files, output_db, extra_args)

    db_handle = trap.io.open_db("sqlite", str(output_db))
    verify_database(
        db_handle
    )  # Perform sanity checks of the images table with respect to the extracted_sources table

    # Check if the numbers reported in the logs match the sources found in the database
    nr_sources_per_image_from_logs = []
    nr_attempted_force_fits_per_image_from_logs = [
        0
    ]  # First image does not call force fit and hence is not mentioned in stdout
    nr_succesful_force_fits_per_image_from_logs = [
        0
    ]  # First image does not call force fit and hence is not mentioned in stdout
    for line in stdout:
        pattern_nr_sources = re.compile(r"Found (\d+) sources \(source_extraction\.py")
        match_nr_sources = pattern_nr_sources.search(line)
        if match_nr_sources:
            # Expected format of line of interest:
            # 2025-09-17 14:25:13,510 - TraP - INFO - Found 221 sources (source_extraction.py:382)
            nr_sources = int(match_nr_sources.group(1))
            nr_sources_per_image_from_logs.append(nr_sources)
            continue

        pattern_nr_force_fit_attempts = re.compile(
            r"Forcing (\d+) detections \(run\.py"
        )
        match_nr_force_fit_attempts = pattern_nr_force_fit_attempts.search(line)
        if match_nr_force_fit_attempts:
            # Expected format of line of interest:
            # 2025-09-17 15:04:11,636 - TraP - INFO - Forcing 73 detections (run.py:66)
            nr_attempted_force_fits = int(match_nr_force_fit_attempts.group(1))
            nr_attempted_force_fits_per_image_from_logs.append(nr_attempted_force_fits)
            continue

        pattern_nr_force_fit_successes = re.compile(
            r"Forced fit for (\d+) sources \(source_extraction\.py"
        )
        match_nr_force_fit_successes = pattern_nr_force_fit_successes.search(line)
        if match_nr_force_fit_successes:
            # Expected format of line of interest:
            # 2025-09-17 14:25:14,104 - TraP - INFO - Forced fit for 22 sources (source_extraction.py:446)
            nr_force_fits = int(match_nr_force_fit_successes.group(1))
            nr_succesful_force_fits_per_image_from_logs.append(nr_force_fits)

    extracted_sources = pd.read_sql_table("extracted_sources", db_handle)
    extracted_sources["is_not_force_fit"] = ~extracted_sources["is_force_fit"]
    grouped_im_id = extracted_sources.groupby("im_id")

    # Check if the reported number of force fits in the logs matches the database, including failed fits
    nr_force_fits_per_image_from_db = grouped_im_id["is_force_fit"].sum()
    np.testing.assert_array_equal(
        # Note: sort the values because the logs report image info based on order
        #       of execution which is handled by Dask and is not deterministic.
        np.sort(nr_force_fits_per_image_from_db.values),
        np.sort(nr_attempted_force_fits_per_image_from_logs),
    )

    # Check if the reported number of force fits in the logs matches the database, excluding failed fits
    failed_force_fits = extracted_sources[~np.isfinite(extracted_sources["peak_flux"])]
    nr_failed_force_fits_per_image_db = (
        failed_force_fits.groupby("im_id")["is_force_fit"]
        .count()
        .reindex(extracted_sources["im_id"].unique(), fill_value=0)
    )
    nr_succesful_force_fits_per_image_from_db = (
        nr_force_fits_per_image_from_db - nr_failed_force_fits_per_image_db
    )
    np.testing.assert_array_equal(
        # Note: sort the values because the logs report image info based on order
        #       of execution which is handled by Dask and is not deterministic.
        np.sort(nr_succesful_force_fits_per_image_from_db.values),
        np.sort(nr_succesful_force_fits_per_image_from_logs),
    )

    # Check if the reported number of found sources in the logs matches the database
    nr_sources_per_image_from_db = grouped_im_id["is_not_force_fit"].sum().values
    np.testing.assert_array_equal(
        # Note: sort the values because the logs report image info based on order
        #       of execution which is handled by Dask and is not deterministic.
        np.sort(nr_sources_per_image_from_db),
        np.sort(nr_sources_per_image_from_logs),
    )
