# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Top-level package for geogravL3."""

__author__ = """ "Eva Boergens" """
__email__ = "boergens@gfz.de"

from .version import __version__
from .pipeline import run_pipeline
from .data_downloads.downloads import download_resources
from .config import load_configuration

__all__ = [
    "__version__",
    "run_pipeline",
    "download_resources",
    "load_configuration"
]
