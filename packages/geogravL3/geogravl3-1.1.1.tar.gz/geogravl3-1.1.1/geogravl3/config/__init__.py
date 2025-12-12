# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Config module for geogravL3 containing configuration classes, functions, and templates."""

from .config import Config, load_configuration, path_testdata, path_resources

__all__ = ["Config", "load_configuration", "path_testdata", "path_resources"]
