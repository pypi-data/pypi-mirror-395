# Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import sys
import warnings
from datetime import datetime
from functools import wraps
from pathlib import Path
from time import monotonic

# Create a timestamp string
start_time = datetime.now().strftime("%Y-%m-%dT%H.%M.%S%z")


# Log warnings raised using the warnings package
def handle_warning(message, category, filename, lineno, file=None, line=None):
    logger.warning(f"{category.__name__}: {message} ({filename}:{lineno})")


warnings.showwarning = handle_warning


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("TraP")
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


def add_log_file_handler(log_dir: os.PathLike) -> logging.Logger:
    """Add a file handler for all logging and a separete one for only errors and warnings.
    This makes the logger write both to the terminal and to a file in the specified `log_dir` location.

    Parameters
    ----------
    :class:`os.PathLike`
        The location where the logs will be stored. Must be a directory.

    Returns
    -------
    :class:`logging.Logger`
        The updated logger that now also writes to log files
    """
    log_file = Path(f"{log_dir}/trap_{start_time}.log")
    error_file = Path(f"{log_dir}/trap_error_{start_time}.log")

    try:
        # Make sure the location exists and that we are able to write to it
        os.makedirs(log_dir, exist_ok=True)
        log_file.touch()
        error_file.touch()
    except PermissionError:
        # Warn about being unable to create (error) logs. Ironic, no?
        logger.warning(
            f"Unable to store logs in location: {log_dir}. Check permissions."
        )
        return logger  # Return pre-maturely before adding the file loggers

    # File handler for all logs
    std_handler = logging.FileHandler(log_file)
    std_handler.setLevel(logging.DEBUG)  # logs everything
    std_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )
    )
    logger.addHandler(std_handler)

    # File handler for errors only
    error_handler = logging.FileHandler(error_file)
    error_handler.setLevel(logging.WARNING)  # only warnings and above
    error_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )
    )
    logger.addHandler(error_handler)

    return logger


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log keyboard interrupts (Ctrl+C)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


# Install the custom exception handler
sys.excepthook = handle_exception


def log_time(log_level="info"):
    def decorator(func):
        @wraps(
            func
        )  # This preserves the original function's metadata, which is required for sphinx autodoc
        def wrapper(*args, **kwargs):
            start_time = monotonic()
            result = func(*args, **kwargs)
            end_time = monotonic()
            getattr(logger, log_level)(
                f"Function `{func.__name__}` took {end_time - start_time} seconds"
            )
            return result

        return wrapper

    return decorator
