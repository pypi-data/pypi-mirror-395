# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Load JSON configuration module."""

import json
from json import JSONDecodeError


def load_json_configuration(path: str) -> dict:
    """
    Load configuration json file.

    Parameters
    ----------
    path : str
        Path to the configuration json file.

    Returns
    -------
    : dict
        A dictionary containing configurations.

    Raises
    ------
    OSError
        Failed to load the configuration json file.
    """
    from .config import Config  # import here to avoid circular import

    try:
        with open(path) as config_fp:
            config = json.load(config_fp)
            config = Config(**config).model_dump(by_alias=True)
    except JSONDecodeError as e:        # pragma: no cover
        raise OSError(f"Failed to load the configuration json file => {e}") from e      # pragma: no cover
    return config
