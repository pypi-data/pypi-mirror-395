from os import PathLike
from pathlib import Path
from typing import List, Literal, Optional, Tuple, Union

import numpy as np
import sqlalchemy
from astropy.io import fits

from trap.log import logger


def is_fits(file: Path):
    """Check if the supplied file exists and is a .fits image.

    Parameters
    ----------
    file: :class:`Path`
        The path to the file of which we want to know if it is a valid fits file

    Returns
    -------
    bool
        Whether the file is a fits file or not
    """
    if not file.is_file():
        return False

    if file.suffix.lower() != ".fits":
        return False

    return True


def find_fits(path: Union[str, Path]) -> List[Path]:
    """Find the .fits files in the supplied directories.
    Only .fits images are supported.
    Both absolute and relative paths are allowed.
    Supported input style: \n
        - File (/data/im0.fits) \n
        - Directory (/data/im0.fits) \n
        - Glob (/data/*/im_*) \n
    In the case of a directory all fits files in the given directory are used. Any non-fits files are ignored.
    Same with the glob pattern.

    Parameters
    ----------
    fits_path: list
        A list of directories, glob patterns or file locations.

    Returns
    -------
    fits_path: numpy.ndarray
        A list of file paths for each .fits file found
    """

    def _expand_glob_path(path: Path):
        # Expand each * in the path.
        # E.g. /data/dummy_*/files would be turned into [/data/dummy_aaa/files, /data/dummy_bbb/files, ...]
        parent_dir = path.parent
        if "*" in str(parent_dir):
            matches = _expand_glob_path(parent_dir)
            return [match / path.name for match in matches]
        else:
            return parent_dir.glob(path.name)

    # The workflow below is as follows:
    # 1. If path is a fits file, add it to the list
    # 2. If path is a directory, call this function again for each item (file or sub-directory) in the given directory
    # 3. If there is a glob pattern (*) in the filename, find each file using that pattern
    # 4. If there is a glob pattern (*) in the directory, expand it into a list of directories using _expand_glob_path
    #    and call find_fits again for each directory found by expanding the glob patterns.
    search_path: Path = Path(path)
    fits_files = []
    if search_path.is_file():  # Step 1. add fits file to the list
        if not search_path.exists():
            raise FileNotFoundError(f"Cannot read {search_path}: file does not exist.")
        if is_fits(search_path):
            fits_files.append(search_path)
    elif search_path.is_dir():  # Step 2. find all fits files in directory
        for p in search_path.iterdir():
            fits_files.extend(find_fits(p))
    else:
        if "*" in str(
            search_path.parent
        ):  # Step 3. expand directories with '*' in the path
            paths = _expand_glob_path(search_path)
            for p in paths:
                fits_files.extend(find_fits(p))
        elif "*" in str(search_path):  # Step 4. find files with '*' in filename
            found_files_or_dirs = list(search_path.parent.glob(search_path.name))
            for p in found_files_or_dirs:
                if is_fits(p):
                    fits_files.append(p)
                elif p.is_dir():
                    fits_files.extend(find_fits(p))
        else:
            raise ValueError(
                f"Cannot interpret supplied path as directory or file: {search_path}. Does this location exist?"
            )
    return fits_files


def order_fits_by_time(fits_paths: List[Path]) -> Tuple[np.ndarray, np.ndarray]:
    """Order a list of paths to fits images by their acquisition time, as read from the metadata.

    Parameters
    ----------
    fits_path: list
        A list of .fits files.

    Returns
    -------
    fits_path: numpy.ndarray
        The ordered array of fits image paths
    datetimes: numpy.ndarray
        An array containing the datetimes to go along with the paths in fits_path
    """
    datetimes = np.empty(len(fits_paths), dtype="datetime64[ms]")
    for i, path in enumerate(fits_paths):
        with fits.open(path) as im:
            header = im[0].header
            date_time = header.get("DATE-OBS", None)
            datetimes[i] = np.datetime64(date_time, "s")

    order = np.argsort(datetimes)
    fits_paths = np.asarray(fits_paths)
    fits_paths = fits_paths[order]
    datetimes = datetimes[order]
    return fits_paths, datetimes


def init_db(
    db_backend: Literal["sqlite", "postgres"],
    db_name: str,
    db_user: Optional[str] = None,
    db_password: Optional[str] = None,
    db_host: Optional[str] = None,
    db_port: Optional[str] = None,
    db_overwrite: bool = False,
) -> sqlalchemy.engine.base.Engine:
    """Create a new database. An error is raised if the database already exists, except if ``db_overwrite`` is provided.
    In that case the original database will be removed before the new database is created.

    Parameters
    ----------
    db_backend: Literal["sqlite", "postgres"] (default: "sqlite")
        The database implementation to use.
    db_name: str
        If ``db_backend`` is "sqlite" this is the path to the database.
        If ``db_backend`` is "postgres" this is the name of database.
    db_user: str
        The username with which to log in to the database.
        Only used if ``db_backend`` is "postgres".
    db_password: str
        The password to go along with db_user.
        Only used if ``db_backend`` is "postgres".
    db_host: str
        The name of the host where the database is located.
        Only used if ``db_backend`` is "postgres".
    db_port: str
        The port at which to connect to the host. Goes along wht ``db_host``.
        Only used if ``db_backend`` is "postgres".
    db_overwrite: bool (default: False)
        Allow overwriting of an existing database.
        If `db_overwrite` is False, an error is raised if the database ``db_name`` already exists.
        If `db_overwrite` is True, the database ``db_name`` will be removed if it already exists.

    Returns
    -------
        A sqlalchemy database engine.
    """
    logger.info(f"Establishing {db_backend} database connection for '{db_name}'")
    match db_backend:
        case "sqlite":
            db_path: Path = Path(db_name)
            if db_path.exists():
                if db_overwrite:
                    db_path.unlink()
                else:
                    raise Exception(
                        f"SQLite database {db_name} already exists. Either run TraP with a different 'db_name' or supply '--db_overwrite'."
                    )

            db_engine = sqlalchemy.create_engine(f"sqlite:///{db_name}")
        case "postgres":
            # First connect to the default database to create the new database
            admin_engine = sqlalchemy.create_engine(
                f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/postgres",
                isolation_level="AUTOCOMMIT",
            )
            with admin_engine.connect() as conn:
                if db_overwrite:
                    try:
                        logger.warning(f"Dropping existing database '{db_name}'")
                        conn.execute(
                            sqlalchemy.text(f"DROP DATABASE IF EXISTS {db_name}")
                        )
                    except Exception as e:
                        raise Exception(
                            f"Problem dropping Postgres database '{db_name}', see above for original error"
                        ) from e
                try:
                    conn.execute(sqlalchemy.text(f"CREATE DATABASE {db_name}"))
                except sqlalchemy.exc.ProgrammingError as e:
                    if "already exists" in str(e):
                        raise Exception(
                            f"Postgres database '{db_name}' already exists. Either run TraP with a different 'db_name' or supply '--db_overwrite'."
                        ) from e
                    else:
                        raise Exception(
                            f"Problem connecting to Postgres database '{db_name}', see above for original error"
                        ) from e

            db_engine = sqlalchemy.create_engine(
                f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )
        case _:
            raise ValueError(
                f"Unsupported database backend: {db_backend}. Supported backends: ['sqlite', 'postgres']"
            )
    return db_engine


def open_db(
    db_backend: Literal["sqlite", "postgres"],
    db_name: str,
    db_user: Optional[str] = None,
    db_password: Optional[str] = None,
    db_host: Optional[str] = None,
    db_port: Optional[str] = None,
) -> sqlalchemy.engine.base.Engine:
    """Open a handle to a database for reading or appending to.

    Parameters
    ----------
    db_backend: Literal["sqlite", "postgres"] (default: "sqlite")
        The database implementation to use.
    db_name: str
        If ``db_backend`` is "sqlite" this is the path to the database.
        If ``db_backend`` is "postgres" this is the name of database.
    db_user: str
        The username with which to log in to the database.
        Only used if ``db_backend`` is "postgres".
    db_password: str
        The password to go along with db_user.
        Only used if ``db_backend`` is "postgres".
    db_host: str
        The name of the host where the database is located.
        Only used if ``db_backend`` is "postgres".
    db_port: str
        The port at which to connect to the host. Goes along wht ``db_host``.
        Only used if ``db_backend`` is "postgres".

    Returns
    -------
        A sqlalchemy database engine.
    """
    logger.info(f"Establishing {db_backend} database connection for '{db_name}'")
    match db_backend:
        case "sqlite":
            db_path: Path = Path(db_name)
            if not db_path.exists():
                raise Exception(f"SQLite database {db_name} not found.")

            db_engine = sqlalchemy.create_engine(f"sqlite:///{db_name}")
        case "postgres":
            try:
                db_engine = sqlalchemy.create_engine(
                    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
                )
            except Exception as e:
                raise Exception(
                    f"Unable to connect to postgres database {db_host}:{db_port}/{db_name} as {db_user}."
                ) from e
        case _:
            raise ValueError(
                f"Unsupported database backend: {db_backend}. Supported backends: ['sqlite', 'postgres']"
            )
    return db_engine
