# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Load XML configuration module."""

from pathlib import Path
import xmltodict


def load_xml_configuration(path: str) -> dict:
    """
    Load configuration from an XML file and validate using the existing Pydantic Config model.

    Parameters
    ----------
    path : str
        Path to the XML configuration file.

    Returns
    -------
    dict
        A validated configuration dictionary.

    Raises
    ------
    OSError
        If the XML file cannot be read or parsed.
    ValueError
        If the configuration does not conform to the Pydantic schema.
    """
    from .config import Config  # import here to avoid circular import

    xml_path = Path(path)
    if not xml_path.exists():
        raise OSError(f"XML configuration file '{path}' does not exist.")

    # Parse XML into an ordered dictionary
    try:
        with open(xml_path, "r", encoding="utf-8") as f:
            xml_dict = xmltodict.parse(f.read())
    except Exception as e:
        raise OSError(f"Failed to parse XML file '{path}': {e}") from e

    # xmltodict wraps everything under the root tag, e.g., <config>
    # Convert OrderedDict to a regular dict
    config_dict = dict(xml_dict.get("config", {}))

    # xmltodict converts single elements as strings and arrays as OrderedDict/list
    # Ensure that lists (like filter, earthquake, domain) are always lists
    def ensure_list(value):
        if value is None:
            return None
        if isinstance(value, list):
            return value
        return [value]

    optional_settings = config_dict.get("optional_settings", {})
    for key in ["filter", "earthquake", "domain"]:
        if key in optional_settings:
            # Check if it contains 'item' list or single string
            items = optional_settings[key].get("item") if isinstance(optional_settings[key], dict) \
                else optional_settings[key]
            optional_settings[key] = ensure_list(items)

    config_dict["optional_settings"] = optional_settings

    # Validate using Pydantic
    validated_config = Config(**config_dict).model_dump(by_alias=True)
    return validated_config
