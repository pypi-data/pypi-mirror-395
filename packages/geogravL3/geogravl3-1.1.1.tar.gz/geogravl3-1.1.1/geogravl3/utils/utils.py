# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Utils module."""

import logging
import os
import sys
from pathlib import Path

import numpy as np

from ..processing.global_constants import constants


def get_constant(name: str):
    """
    Return the value of a global constant by name.

    Parameters:
        name (str): The name of the constant.

    Returns:
        The value of the constant if it exists, otherwise raises AttributeError.
    """
    if hasattr(constants, name):
        return getattr(constants, name)
    else:
        raise AttributeError(f"Constant '{name}' not found.")


def create_logger(logging_dir: str, logging_level: str = 'INFO') -> logging.Logger:
    """
    Create and configure a logger based on the provided configuration.

    Parameters:
        logging_dir (str): Directory where to create the log file.
        logging_level (str): logging level to use

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging_level = logging.getLevelName(logging_level)
    log_formatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(__name__)
    logger.handlers.clear()  # Avoid duplicate logs if this is called multiple times

    os.makedirs(logging_dir, exist_ok=True)
    file_handler = logging.FileHandler(f"{logging_dir}/geogravl3_logfile.log", mode="w")
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging_level)

    return logger


def create_test_logger() -> logging.Logger:
    """
    Create and configure a logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging_level = logging.getLevelName("DEBUG")

    log_formatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger('test_logger')
    logger.handlers.clear()  # Avoid duplicate logs if this is called multiple times

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging_level)

    return logger


def ellipsoid_radius(lat: float) -> float:
    """
    Compute distance to the center of the ellipsoid for a given geocentric latitude.

    Parameters
    ----------
    lat : float
        Geocentric latitude [radians].

    Returns
    -------
    r : float
        Distance from ellipsoid center [m]
    """
    radius = get_constant("earths_radius_iers")
    flattening = get_constant("earths_flattening_iers")

    a = radius * np.cos(lat)
    b = (radius - radius * flattening) * np.sin(lat)

    r = np.sqrt(a ** 2 + b ** 2)

    return r


def get_resource_dir() -> Path:
    """Return the directory where resources should be loaded from.

    If running inside a source checkout (detected via `.git`), use the
    repository's resource directory. Otherwise, use the cache directory
    ($HOME/.cache/geogravl3/resources).
    """
    # check the environment variable
    GEOGRAVL3_DATA = os.environ.get('GEOGRAVL3_DATA')
    if GEOGRAVL3_DATA:
        return Path(GEOGRAVL3_DATA)

    # geogravl3/utils/__file__
    package_root = Path(__file__).resolve().parents[2]

    if (package_root / ".git").exists() and (package_root / "geogravl3" / "resources").exists():
        # Running from a repo clone
        return package_root / "geogravl3" / "resources"

    # Running from an installed package
    return Path.home() / ".cache" / "geogravl3" / "resources"
