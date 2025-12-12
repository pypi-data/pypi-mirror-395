import argparse
import os
import pdb
import sys
from pathlib import Path

tomllib_present = False
try:
    import tomllib  # Build-in from python 3.11

    tomllib_present = True
except ImportError:
    import toml


def parse_bool(value):
    if value is None:
        return None

    truthy = {"1", "true", "yes", "on", "t"}
    falsy = {"0", "false", "no", "off", "f"}

    if not isinstance(value, str):
        raise TypeError(f"Expected string, got {type(value).__name__}: {value}")

    value = value.strip().lower()
    if value in truthy:
        return True
    elif value in falsy:
        return False
    else:
        raise ValueError(f"Cannot convert string to boolean: '{value}'")


def filter_none_values_from_dict(dict_to_filter: dict):
    return {k: v for (k, v) in dict_to_filter.items() if v is not None}


def update_params_from_config_file(config_file, params):
    """Update the parameters that were not found on the command line with those in the config file.

    Parameters
    ----------
    config_file: :class:`str`
        The path to the configuration file. Must be a .toml format.
    params: :class:`dict`
        The parameters as parsed by argparse from the command line.
        This dictionary is updated in-place

    Returns
    -------
    None
    """

    def overwrite_params_from_nested_dict(mapping: dict):
        for key, value in mapping.items():
            if isinstance(value, dict):
                overwrite_params_from_nested_dict(value)
            else:
                if params.get(key) is None:
                    params[key] = value

    if config_file is not None:
        if tomllib_present:
            # >= python3.11
            with open(config_file, "rb") as f:
                config_data = tomllib.load(f)
        else:
            # < python3.11
            config_data = toml.load(config_file)
        overwrite_params_from_nested_dict(config_data)


def construct_argument_parser(require_command=False, require_processing_args=True):

    parser = argparse.ArgumentParser(
        description="Transients Pipeline. Extract sources in radio astronomy data to find transients. Source: https://git.astron.nl/RD/trap"
    )

    if require_command:
        parser.add_argument(
            "command",
            choices=["run", "view"],
            help="""Command to execute: 'run' or 'view'.
            'run' will process the images and store the results in a database.
            'view' will visualize the sources in the database created by the 'run' command.
            For 'view' only the variables that create a database connection are used.
            """,
        )

    # General arguments
    general_group = parser.add_argument_group("General")
    if not require_processing_args:
        parser.add_argument(
            "--view_command",
            "--view-command",
            "-v",
            choices=["all_sources", "interactive", "lightcurves"],
            default="all_sources",
            help="""View command to execute: 'all_sources' or 'interactive', 'lightcurves'.
            'all_sources' will show all locations of each source.
            'interactive' will run an interactive viewer where you can navigate
            through the images and see what sources were found, also showing new and missed sources.
            'lightcurves' will plot all lightcurves as intensity over time.
            """,
        )
    general_group.add_argument(
        "--version",
        action="store_true",
        help="""
        Display the version of the currently installed TraP.
    """,
    )
    general_group.add_argument(
        "--pyse_version",
        "--pyse-version",
        action="store_true",
        help="""
        Display the version of the currently installed radio-pyse.
    """,
    )
    general_group.add_argument(
        "--config_file",
        "--config-file",
        help="""
        TOML file containing default input arguments to TraP.
        Default file name: trap_config.toml
        This is especially convenient when swapping between configurations for the same project.
    """,
    )
    general_group.add_argument(
        "--log_dir",
        "--log-dir",
        help="""
        The directory in which to write the log and the error log file.
        The same information is also printed to the terminal standard output.
    """,
    )
    general_group.add_argument(
        "--nr_threads",
        "--nr-threads",
        "-n",
        type=int,
        help="""Number of threads to spawn. With multiple threads, images can be read and processed in parallel.
        If None, use as many theads as there are cores.
        Using multiple threads speeds up computation significantly. Note that there is a point where the
        association becomes the bottleneck, since it is fundamentally a sequential operation.
        That means that adding more processes to pre-load the images has diminishing returns.
        Warning: there is a known bug where the RAM of your device might blow up if you use
        many processes but either have little RAM or very many images to process.
        It can happen that all of the images get loaded in before the program is near completion.
        To work around this, use a low number of processes. This bug will be addressed in the future.
        When the distributed scheduler is used, the nr_threads will be divided over the
        processes and threads. For example, if nr_threads=12, we might get 3 processes with
        4 workers each. If a prime number is chosen this might result in a skewed distribution.
        When nr_threads is set to 13, we might for example get one process with 13 threads,
        which will run fine but is often non-optimal in terms of performance.
        Also see argument: scheduler
        """,
    )
    general_group.add_argument(
        "--scheduler",
        type=str,
        help="""The Dask scheduler to use.
        Options are: ['threads', 'distributed'].
        Default: 'threads'. The 'threads' scheduler uses multithreading to process in parallel.
        This has the least overhead but is limited by Python's GIL.
        The 'distributed' scheduler uses a balance of both processes and threads which allows for
        more versitile parallel computing but can carry more overhead, especially when data between processes
        needs to be communicated. The distributed scheduler also provides a real-time diagnostics dashboard and
        allows for running accross multiple nodes. In general I recommend using the threads scheduler when running
        on a smaller machine like a laptop and use the distributed scheduler when running on a compute node
        with lots of RAM and many CPU cores.
        See also the argument: nr_threads.
        """,
    )
    general_group.add_argument(
        "--pdb",
        action="store_true",
        help="""
        Enter debug mode when the application crashes. Meant to be used for more comprehensive debugging.
        This argument is not exported to the database.
    """,
    )

    # Database parameters
    db_group = parser.add_argument_group("Database parameters")
    db_group.add_argument(
        "--db_backend",
        "--db-backend",
        help="""
        The database solution to use.
        Options are: ['sqlite', 'postgres'].
        Default: 'sqlite'. If set to 'postgres', the following parameters
        also need to be provided:
        'db_user', 'db_password', 'db_host', 'db_port'.
    """,
    )
    db_group.add_argument(
        "--db_name",
        "--db-name",
        help="""
        When 'db_backend' is sqlite, 'db_name' represents the path to the file.
        When 'db_backend' is 'postgres', 'db_name' represents the name of the database.
    """,
    )
    db_group.add_argument(
        "--db_host",
        "--db-host",
        help="The name of the host where the database is located (used for 'postgres').",
    )
    db_group.add_argument(
        "--db_port",
        "--db-port",
        help="The port number to go along with 'db_host' (used for 'postgres').",
    )
    db_group.add_argument(
        "--db_user",
        "--db-user",
        help="The username used for accessing the database (used for 'postgres').",
    )
    db_group.add_argument(
        "--db_password",
        "--db-password",
        help="""
            The password used for accessing the database (used for 'postgres').
            This argument is not exported to the database.
        """,
    )
    db_group.add_argument(
        "--db_overwrite",
        "--db-overwrite",
        action="store_true",
        default=None,
        help="""
        If supplied, clears the database and starts fresh. Only use this if you are OK losing the
        existing database with the supplied 'db_name'. When not supplied, the program will error
        if the database already exists, preventing deletion of existing data.
    """,
    )

    if require_processing_args:
        # Image parameters
        image_group = parser.add_argument_group("Input image parameters")
        image_group.add_argument(
            "--input_images",
            "--input-images",
            "-i",
            action="append",
            help="""
            The input images in which to find the sources.
            Only .fits images are supported.
            This can refer to either a file, directory or glob pattern (e.g. 'images/my_image_*.fits').
            When using a glob pattern, remember to wrap the line in quotes or the terminal might get confused.
            If a directory or glob pattern is used, all fits images found there will be used.
            If a nested directory is supplied, the subdirectories will also be searched for fits files.
            These arguments can be supplied multiple times to refer to multiple files or locations.
        """,
        )
        image_group.add_argument(
            "--rms_min",
            "--rms-min",
            type=float,
            help="Lower bound for the RMS quality check. If an image has a lower RMS value than 'rms_min', it is 'rejected' and not processed.",
        )
        image_group.add_argument(
            "--rms_max",
            "--rms-max",
            type=float,
            help="Upper bound for the RMS quality check. If an image has a larger RMS value than 'rms_max', it is 'rejected' and not processed.",
        )
        image_group.add_argument(
            "--reduction_factor_for_rms",
            type=float,
            help="""
            Only the region around the center of the image is used to determine the RMS of the image on which the rejection is based.
            The 'reduction_factor_for_rms' determines the size of this region around the center, where 'reduction_factor_for_rms'
            is the fraction of each axis to use. To illustrate: if an image is 100x100 pixels, a `reduction_factor_for_rms=2` results
            in a 50x50 slice around the center that is used to calculate the RMS of the image.
        """,
        )

        # Extraction parameters
        extraction_group = parser.add_argument_group("Extraction parameters")
        extraction_group.add_argument(
            "--ew_sys_err",
            "--ew-sys-err",
            type=float,
            help="Systematic error in arcseconds along the east-west axis.",
        )
        extraction_group.add_argument(
            "--ns_sys_err",
            "--ns-sys-err",
            type=float,
            help="Systematic error in arcseconds along the north-south axis.",
        )
        extraction_group.add_argument(
            "--detection_threshold",
            "--detection-threshold",
            type=float,
            help="The detection threshold, as a multiple of the RMS noise.",
        )
        extraction_group.add_argument(
            "--analysis_threshold",
            "--analysis-threshold",
            type=float,
            help="Analysis threshold, as a multiple of the RMS noise.",
        )
        extraction_group.add_argument(
            "--deblend_nthresh",
            "--deblend-nthresh",
            type=int,
            help="Number of subthresholds to use for deblending. Set to 0 to disable.",
        )
        extraction_group.add_argument(
            "--max_nr_consecutive_force_fits",
            "--max-nr-consecutive-force-fits",
            type=int,
            help="""Stop force fitting if the source has not naturally been found after a specified number of images.
            If the source has been found naturally again this is reset and we will again force fit for the specified number of images.
            If the source is naturally detected at a regular interval that is smaller than max_nr_consecutive_force_fits,
            the lightcurve will be continuous. If there are periods where the source is not naturally found within the specified number
            of images, there will be gaps in the time axis of the lightcurve.
            """,
        )
        extraction_group.add_argument(
            "--force_beam",
            "--force-beam",
            action="store_true",
            default=None,
            help="Force all extractions to have major/minor axes equal to the restoring beam.",
        )
        extraction_group.add_argument(
            "--im_margin",
            "--im-margin",
            type=int,
            help="The number of pixels from the edge of the image within which sources are ignored.",
        )
        extraction_group.add_argument(
            "--im_radius",
            "--im-radius",
            type=int,
            help="The radius in pixels around the center of the image, outside of which sources are ignored.",
        )
        extraction_group.add_argument(
            "--im_back_size_x",
            "--im-back-size-x",
            type=int,
            help="Width of the background boxes as used in SEP.",
        )
        extraction_group.add_argument(
            "--im_back_size_y",
            "--im-back-size-y",
            type=int,
            help="Height of the background boxes as used in SEP.",
        )

        # Association parameters
        association_group = parser.add_argument_group("Association parameters")
        association_group.add_argument(
            "--de_ruiter_r_max",
            "--de-ruiter-r-max",
            type=float,
            help="If the de Ruiter radius is larger than this value, sources are considered different.",
        )
    return parser


def parse_arguments(require_command=False, require_processing_args=True):
    parser = construct_argument_parser(
        require_command=require_command, require_processing_args=require_processing_args
    )
    args = parser.parse_args()
    params = vars(args)

    update_params_from_config_file(params["config_file"], params)
    return params


def run_batch(params=None):
    if params is None:
        params = parse_arguments()

    # Handle the case where version information is requested.
    # The program is meant to exist after printing the information,
    # similar to the --help argument.
    version_info = []
    if params["version"]:
        import trap

        version_info.append(f"TraP version: v{trap.__version__}")

    if params["pyse_version"]:
        import sourcefinder

        version_info.append(f"Radio-PySE version: v{sourcefinder.__version__}")

    if version_info:
        sys.exit("\n".join(version_info))

    if params["pdb"]:
        # Automatically start the debugger on an unhandled exception
        def excepthook(type, value, traceback):
            pdb.post_mortem(traceback)

        sys.excepthook = excepthook

    # Prepare trap for running
    from pathlib import Path

    import dask
    import numpy as np
    import pandas as pd
    from dask.distributed import Client
    from dask.distributed.deploy.utils import nprocesses_nthreads

    from trap import run
    from trap.io import find_fits, init_db, order_fits_by_time
    from trap.log import add_log_file_handler, logger

    logger = add_log_file_handler(params["log_dir"] or "./logs")

    if params["input_images"] is None:
        raise Exception(
            "No images were specified. Use '--input_images' or '-i' to specify the location of input images."
        )

    nr_threads = params["nr_threads"]
    if isinstance(nr_threads, str):
        # Parse "None" as None such that Dask can use it's own defaults,
        # which is related to to total number of CPU cores on the machine.
        if nr_threads.lower() == "none":
            nr_threads = None
    if params["scheduler"] is None or params["scheduler"].lower() == "threads":
        dask.config.set(scheduler="threads")
        dask.config.set(num_workers=nr_threads)
        dask.config.set(pool=None)  # Ensure it respects num_workers
    elif params["scheduler"].lower() == "distributed":
        if nr_threads is None:
            # Let Dask use defaults
            client = Client()
            thread_info = client.nthreads()
            n_workers = len(thread_info)
            n_threads = int(np.median(list(thread_info.values())))
        else:
            n_threads, n_workers = nprocesses_nthreads(nr_threads)
            client = Client(n_workers=n_workers, threads_per_worker=n_threads)
        logger.info(
            f"Processing with {n_workers} processes with {n_threads} threads each."
        )
        logger.info("View progress dashboard at: " + str(client.dashboard_link))
    elif (
        params["scheduler"].lower() == "processes"
        or params["scheduler"].lower() == "multiprocessing"
    ):
        raise NotImplementedError(
            """
            Note: we deliberately don't support using only processes, because that results in a lot of data
            communication between workers which is very inefficient. This communication happens especially when
            copying the image object for force-fitting after association. Re-reading is also not performant, unless
            maybe if the file is still kept hot by the OS but in practice this rarely seems to happen during TraP processing.
            Consider using a distributed scheduler with a combination of processes and threads instead.
        """
        )

    else:
        raise ValueError(
            f"Unrecognized 'scheduler' argument provided. Expected 'threads' or 'distributed', got: {params['scheduler']}"
        )

    if params["db_name"] is None:
        raise ValueError(
            "No '--db_name' was supplied. Please specify the name of the database the TraP data is to be exported to."
        )

    db_kwargs = filter_none_values_from_dict(
        dict(
            db_backend=params["db_backend"] or "sqlite",
            db_name=params["db_name"],
            db_user=params["db_user"],
            db_password=params["db_password"],
            db_host=params["db_host"],
            db_port=params["db_port"],
        )
    )

    # Init db, cleaning if needed
    db_engine = init_db(**db_kwargs, db_overwrite=params["db_overwrite"])

    # Turn relative paths into absolute paths.
    for i in range(len(params["input_images"])):
        params["input_images"][i] = str(Path(params["input_images"][i]).absolute())

    logger.info(f"Gathering .fits files in: {', '.join(params['input_images'])}")
    fits_paths = []
    for path in params["input_images"]:
        fits_paths.extend(find_fits(path))
    fits_paths = np.unique(fits_paths)
    fits_paths, datetimes = order_fits_by_time(fits_paths)

    if len(fits_paths) == 0:
        raise Exception(
            "No input images were found in any of: \n - "
            + "\n - ".join(params["input_images"])
        )
    elif len(fits_paths) == 1:
        logger.info("Found exactly one input image")
    else:
        logger.info(f"Found {len(fits_paths)} input images")

    for path, time in zip(fits_paths, datetimes):
        logger.debug(f"Found image: [{time}] {path}")

    # Save the configuration in the database.
    # Make sure any list is turned into a single string.
    # This happens when multiple inputs are allowed in the CLI such as with --input_images
    # If we keep this a list there will be multiple rows in the table. Any non-list values are then duplicated.
    params_for_db = params.copy()
    for key, val in params_for_db.items():
        if hasattr(val, "__len__") and not isinstance(val, str):
            params_for_db[key] = "; ".join(params_for_db[key])
    params_for_db.pop("pdb")  # Uninteresting for export
    params_for_db.pop("db_password")  # Not safe to export
    pd.DataFrame(params_for_db, index=[0]).to_sql("config", db_engine, index=False)
    return run.main(
        fits_paths,
        db_kwargs=db_kwargs,
        max_nr_consecutive_force_fits=params["max_nr_consecutive_force_fits"],
        pyse_config=filter_none_values_from_dict(
            dict(
                margin=params["im_margin"],
                radius=params["im_radius"],
                back_size_x=params["im_back_size_x"],
                back_size_y=params["im_back_size_y"],
                force_beam=params["force_beam"],
                ew_sys_err=params["ew_sys_err"],
                ns_sys_err=params["ns_sys_err"],
                detection_thr=params["detection_threshold"],
                analysis_thr=params["analysis_threshold"],
                deblend_nthresh=params["deblend_nthresh"],
            )
        ),
        association_kwargs=filter_none_values_from_dict(
            dict(
                de_ruiter_r_max=params["de_ruiter_r_max"],
            )
        ),
    )


def view(params=None):
    if params is None:
        params = parse_arguments(require_processing_args=False)

    if params["pdb"]:
        # Automatically start the debugger on an unhandled exception
        def excepthook(type, value, traceback):
            pdb.post_mortem(traceback)

        sys.excepthook = excepthook

    from trap.io import open_db
    from trap.log import logger
    from trap.visualize import plot_all_sources, plot_lightcurves, visualize

    db_engine = open_db(
        db_backend=params["db_backend"],
        db_name=params["db_name"],
        db_user=params["db_user"],
        db_password=params["db_password"],
        db_host=params["db_host"],
        db_port=params["db_port"],
    )
    match params["view_command"]:
        case "all_sources":
            plot_all_sources(db_engine)
        case "interactive":
            visualize(db_engine)
        case "lightcurves":
            plot_lightcurves(db_engine)
        case _:
            raise ValueError(f"Unrecognized view_command '{params['view_command']}'")


def main():
    params = parse_arguments(require_command=True)
    if params["command"] == "run":
        return run_batch(params)
    elif params["command"] == "view":
        return view(params)


if __name__ == "__main__":
    sys.exit(main())
