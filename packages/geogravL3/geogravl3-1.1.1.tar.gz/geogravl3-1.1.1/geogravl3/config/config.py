# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Configuration checks."""

import os
import re
import datetime as dt
from pathlib import Path
from typing import Any, ClassVar, List, Optional

import numpy as np
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator, model_validator

from ..io.readers import read_mask, read_grid_definition, read_gfc, read_lowdegree_coefficients, \
    read_input_folder
from .json_config import load_json_configuration  # import here to avoid circular import
from .xml_config import load_xml_configuration  # import here to avoid circular import
from ..utils.utils import get_resource_dir

path_resources = get_resource_dir()
path_testdata = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "tests", "data"))


class MandatorySettings(BaseModel, extra="forbid"):
    """Template for necessary settings in config file."""

    input_folder: str = Field(title="Location of the input folder.", description="The Folder of the SH coefficients.")

    output_folder: str = Field(
        title="Location of the output directory.", description="Define folder where all output data should be stored."
    )

    @field_validator("input_folder")
    def check_input_folder(cls, v: str) -> str:  # noqa: N805
        """
        Validate that a folder path is defined and is not an empty string and contains data files.

        If the folder path is relative, it will be converted to an absolute path.

        Parameters
        ----------
        v : str
            The folder path to validate.

        Returns
        -------
        str
            The validated folder path, converted to an absolute path if it was relative.

        Raises
        ------
        ValueError
            If the folder path is an empty string.
        """
        if v == "":
            raise ValueError("Empty string is not allowed.")
        if not os.path.isabs(v) and v.startswith("tests"):
            v = os.path.abspath(os.path.join(path_testdata, '..', '..', v))
        if os.path.isdir(v):
            # check files in the directory
            gfc_files = [file for file in os.listdir(v) if file.endswith(".gfc")]
            snx_files = [file for file in os.listdir(v) if file.endswith(".snx")]
            if not gfc_files and not snx_files:
                raise ValueError("The directory does not contain valid data files.")

        return v

    @field_validator("output_folder")
    def check_output_folder(cls, v: str) -> str:  # noqa: N805
        """
        Validate that a folder path is defined and is not an empty string.

        If the folder path is relative, it will be converted to an absolute path.

        Parameters
        ----------
        v : str
            The folder path to validate.

        Returns
        -------
        str
            The validated folder path, converted to an absolute path if it was relative.

        Raises
        ------
        ValueError
            If the folder path is an empty string.
        """
        if v == "":
            raise ValueError("Empty string is not allowed.")
        if not os.path.isabs(v) and v.startswith("tests"):
            v = os.path.abspath(os.path.join(path_testdata, '..', '..', v))
        return v


class OptionalSettings(BaseModel, extra="forbid"):
    """Template for optional settings in config file."""

    GRID_KEYS: ClassVar[list[str]] = ["xsize", "ysize", "xfirst", "yfirst", "xinc", "yinc"]

    time_mean: str = Field(
        title="Time mean in format YYYY/MM or YYYY/MM-YYYY-MM.",
        description="Anything between 2002/04 to today is possible. Either one month or a time range. "
                    "If empty, None, or setting is omitted, the default (2002/04-2020/03) is used."
                    "If single date or date range are outside the range 2002/04 - today, default is used.",
        default="2002/04-2020/03",
    )

    filter: Optional[List[str]] = Field(
        title="Filter. Possible values: None, DDK1-8, VDK1-8, GaussXXX or any combination.",
        description="If None is provided (or list is empty or setting is omitted), no filter is used. "
                    "GaussXXX: XXX = any positive Integer.",
        default=None,
    )

    lowdegree_coefficients: Optional[str] = Field(title="Path to lowdegree coefficients file.",
                                                  description="If None is provided or setting is omitted, "
                                                              "no lowdegree coefficients are replaced.",
                                                  default=None)

    gia_model: Optional[str] = Field(title="Path to GIA Model",
                                     description="If None is provided or setting is omitted, no GIA model is corrected",
                                     default=None)

    insert_geocenter_motion: bool = Field(title="Flag for estimation and insertion of geocentre motion",
                                          description="Degree 1 coefficients. If 'True' signal is "
                                                      "estimated and inserted",
                                          default=False)

    remove_s2_aliased_signal: bool = Field(title="Flag for s2 aliased signal removal",
                                           description="If 'True' signal is estimated and removed",
                                           default=False)

    grid: str = Field(title="Grid definition.",
                      description="Must contain parameters: xsize, ysize, xfirst, yfirst, xinc "
                                  "and yinc. E.g. grid description provided by CDO griddes of an"
                                  "existing netcdf file.",
                      default=os.path.join(path_resources, "grid", "grid_parameters_360x180.dat"))

    max_degree: int = Field(
        title="Max degree.",
        description="Positive Integer. If files with lower max_degree exists, the minimum will be used. If setting is"
                    "omitted, set to 96.",
        default=96,
    )

    love_numbers: str = Field(title="File path for love numbers file.",
                              default=os.path.join(path_resources, "love", "Load_Love2_CF.dat"))

    earthquake: Optional[List[str]] = Field(
        title="List of earthquakes to be considered.",
        description="Can be 2004, 2010, 2011, any combination, or None. If None is selected, "
                    "no earthquakes are considered.",
        default=None,
    )

    domain: List[str] = Field(
        title="Domain",
        description="Can be either all, or any selection of: land, ocean, ice, greenland, antarctica. 'ice' equals to "
                    "greenland and antarctica together. In the case all, the land processing is applied globally "
                    "without any ocean and ice masking. If setting is omitted, set to default 'all'",
        default=["all"],
    )

    sensitivity_kernel_greenland: Optional[str] = Field(
        title="Path to greenland sensitivity kernel file.",
        description="If None is provided or setting is omitted, no sensitivity kernel is applied",
        default=None,
    )

    sensitivity_kernel_antarctica: Optional[str] = Field(
        title="Path to antarctica sensitivity kernel file.",
        description="If None is provided or setting is omitted, no sensitivity kernel is applied",
        default=None,
    )

    land_ocean_mask: Optional[str] = Field(
        title="Path to land_ocean_mask file.",
        description="Land-ocean mask for the differentiation between the domains land and ocean. If setting is omitted "
                    "land-ocean mask is set to default "
                    "resources/masks/Land_Ocean_mask_fraction_1deg_based_on_ESA_150m_land_ocean_mask_w_ice.nc",
        default=os.path.join(path_resources, "masks",
                             "Land_Ocean_mask_fraction_1deg_based_on_ESA_150m_land_ocean_mask_w_ice.nc"),
    )

    land_ice_mask: Optional[str] = Field(
        title="Path to land_ice_mask file.",
        description="Only needed for land domain, to mask out the ice covered land regions in Greenland and Antarctica."
                    "If set to None or setting is omitted, these regions are not masked out",
        default=None,
    )

    reference_surface: str = Field(
        title="Reference surface.", description="Can be either ellipsoidal or spherical.", default="ellipsoidal"
    )

    logging_level: Optional[str] = Field(
        title="Logging level.",
        description="Logging level, it should be one of: DEBUG, INFO, WARN, or ERROR.",
        default="INFO",
    )

    region_land_geojson: Optional[str] = Field(
        title='Path to geojson file with land regions for mean timeseries.',
        description='Has to be set if mean time series should be computed. If omited or set to None, no mean '
                    'time series over land are computed.',
        default=None,
    )

    region_ocean_geojson: Optional[str] = Field(
        title='Path to geojson file with ocean regions for mean timeseries.',
        description='Has to be set if mean time series should be computed. If omitted or set to None, no mean '
                    'time series over land are computed.',
        default=None,
    )

    @field_validator("grid")
    def check_grid(cls, v: str):
        """
        Validate the grid definition file by checking its existence, format, and required keys.

        Args:
            v (str): The file path to the grid definition file, expected to be a string.

        Returns:
            str: The validated grid definition file path if all checks pass.

        Raises:
            ValueError: If the grid definition file is not found, if it does not contain the required gridtype
                        or keys, or if the gridtype is not "lonlat".

        Validation Steps:
            1. The method checks if the provided file path exists and is readable.
            2. It reads the file line by line, expecting key-value pairs in the format 'key = value'.
            3. If any required keys are missing, a `ValueError` is raised, indicating which keys are absent.
            4. The method ensures that the gridtype is "lonlat". If it is not, a `ValueError` is raised.
            5. If no gridtype is provided, "lonlat" is assumed and a Warning issued to the user.
            6. The validated file path is returned if all checks pass.
        """
        if not os.path.isabs(v) and v.startswith("resources"):
            v = os.path.abspath(os.path.join(path_resources, '..', v))
        grid_information = {}
        # check that the file exists and read key-value pairs
        try:
            with open(v) as file:
                for line in file:
                    parts = line.strip().split("=")
                    if len(parts) == 2:
                        key, value = parts[0].strip(), parts[1].strip().removesuffix(",")
                        grid_information[key] = value  # Populate grid_information
        except FileNotFoundError:
            raise ValueError(f"Grid definition file '{v}' not found.") from FileNotFoundError
        # Ensure only supported gridtype is processed
        if "gridtype" in grid_information and grid_information["gridtype"] != "lonlat":
            raise ValueError("Only 'lonlat' grids are supported.")

        if "gridtype" not in grid_information:
            print("Warning: No explicit gridtype provided, assuming 'lonlat'.")
        # Validate that all required keys are present
        missing_keys = [key for key in cls.GRID_KEYS if key not in grid_information]
        if missing_keys:
            raise ValueError(f"Missing required keys in grid definition file: {', '.join(missing_keys)}")
        return v

    @field_validator("love_numbers", mode="before")
    def validate_love_numbers(cls, value: Any, info: FieldValidationInfo) -> str:
        """
        Validate the `love_numbers` field for valid file paths to '.dat' files.

        Args:
            value (Any): The input value to be validated, which should be a string representing a file path.
            info  (FieldValidationInfo): The field that is currently checked.

        Returns:
            str: The validated file path, which must be a non-empty string pointing to a `.dat` file.

        Raises:
            ValueError: If the value is not a string, if it is empty, if the file path does not end with '.dat',
                        or if the file does not exist at the specified location.

        Validation Steps:
            1. The method checks that the value is a string.
            2. It trims any leading or trailing whitespace from the string.
            3. It checks that the file path ends with the `.dat` extension.
            4. It optionally verifies that the file exists at the given path.
            5. If any of these checks fail, a `ValueError` is raised with an appropriate error message.
        """
        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError("love_numbers must be a string representing the file path.")
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError("love_numbers cannot be an empty string.")
        # Check that the file path ends with '.dat'
        if not value.endswith(".dat"):
            raise ValueError("love_numbers must point to a file with a '.dat' extension.")
        if not os.path.isabs(value) and value.startswith("resources"):
            value = os.path.abspath(os.path.join(path_resources, '..', value))
        # Optionally, check if the file exists.
        path = Path(value)
        if not path.exists():
            raise ValueError(f"love_numbers file does not exist at the provided path: {value}")
        return value

    @field_validator("lowdegree_coefficients", mode="before")
    def validate_lowdegree_coefficients(cls, value: Any, info: FieldValidationInfo) -> Optional[str]:
        """
        Validate the `lowdegree_coefficients` field for valid file paths to '.dat' files.

        Args:
            value (Any): The input value to be validated, which should be a string representing a file path.
            info  (FieldValidationInfo): The field that is currently checked.

        Returns:
            str: The validated file path, which must be a non-empty string pointing to a `.dat` file.

        Raises:
            ValueError: If the value is not a string, if it is empty, if the file path does not end with '.dat',
                        or if the file does not exist at the specified location.

        Validation Steps:
            1. The method checks that the value is a string.
            2. It trims any leading or trailing whitespace from the string.
            3. It checks that the file path ends with the `.dat` extension.
            4. It optionally verifies that the file exists at the given path.
            5. If any of these checks fail, a `ValueError` is raised with an appropriate error message.
        """
        if value is None:
            return None
        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError("lowdegree_coefficients must be a string representing the file path.")
        # Normalize the input.
        normalized = value.strip().lower()
        if normalized == "none":
            # Return actual None if the input is "None"
            return None
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError("lowdegree_coefficients cannot be an empty string.")
        # Check that the file path ends with '.dat'
        if not value.endswith(".dat"):
            raise ValueError("lowdegree_coefficients must point to a file with a '.dat' extension.")
        if not os.path.isabs(value) and value.startswith("tests"):
            value = os.path.abspath(os.path.join(path_testdata, '..', '..', value))
        # Optionally, check if the file exists.
        path = Path(value)
        if not path.exists():
            raise ValueError(f"lowdegree_coefficients file does not exist at the provided path: {value}")
        return value

    @field_validator("filter", mode="before")
    def validate_filter(cls, value: Any) -> Optional[List[str]]:
        """
        Validate the `filter` field to ensure the following.

        - The value is provided as a list of strings.
        - An empty list results in no filter (i.e., None).
        - If the list contains only the string "None" (case-insensitive), the filter is considered not applied.
        - If "None" is present together with other values, an error is raised.
        - Each filter item must match one of the allowed patterns:
            * "DDK" followed by a digit between 1 and 8.
            * "VDK" followed by a digit between 1 and 8.
            * "Gauss" followed by a positive integer.

        Args:
            value (Any): The raw input value for the filter field.

        Returns:
            Optional[List[str]]: A list of validated filter items, or None if no filter is applied.

        Raises:
            ValueError: If the input is not a list of strings or if any filter item does not meet the required format.
        """
        if value is None:
            return None
        # Ensure the value is a list.
        if not isinstance(value, list):
            raise ValueError(
                f"filter must be provided as a list of strings, but is {type(value).__name__}."
            )
        # Clean and filter empty strings
        items = [str(item).strip() for item in value if isinstance(item, str) and item.strip()]
        if not items or (len(items) == 1 and items[0].lower() == "none"):
            return None
        if any(item.lower() == "none" for item in items):
            raise ValueError("'None' cannot be combined with other filter selections.")
        # Define regex patterns for allowed filter items.
        valid_patterns = [
            re.compile(r"^DDK[1-8]$"),
            re.compile(r"^VDK[1-8]$"),
            re.compile(r"^Gauss[1-9]\d*$"),
        ]

        def is_valid(item: str) -> bool:
            return any(p.fullmatch(item) for p in valid_patterns)

        invalid_items = [item for item in items if not is_valid(item)]
        if invalid_items:
            raise ValueError(
                f"Invalid filter value(s): {', '.join(invalid_items)}. "
                "Expected 'DDK1-8', 'VDK1-8', 'Gauss<positive integer>', or 'None'."
            )
        return items

    @field_validator("gia_model", mode="before")
    def validate_gia_model(cls, value: Any) -> Optional[str]:
        """
        Validate the `gia_model` field, ensuring it is either a valid file path, or `None`.

        Args:
            value (Any): The input value to be validated, which can be a string or `None`.

        Returns:
            Optional[str]: The file path to `gia_model`. Returns `None` if the input is `"None"`
                           Returns `None` if no value is provided.

        Raises:
            ValueError: If the value is neither a string nor 'None'.

        Validation Steps:
            1. If the value is `None`, it passes through and returns `None`.
            2. If the value is a string, it is normalized (leading/trailing whitespace
                removed and converted to lowercase).
            3. If the normalized value is `"none"`, it returns `None`.
            4. If the normalized value is `"ice6g"`, it returns the canonical string `"Ice6G"`.
            5. If the value does not match either `"none"` or `"ice6g"`, a `ValueError` is raised.
        """
        # Allow None to pass through.
        if value is None:
            return None
        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError("gia_model must be provided as a string.")
        # Normalize the input.
        normalized = value.strip().lower()
        if normalized == "none":
            # Return actual None if the input is "None"
            return None
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError("gia_model cannot be an empty string.")
        # Check that the file path ends with '.gfc'
        if not value.endswith(".gfc"):
            raise ValueError("gia_model must point to a file with a '.gfc' extension.")
        if not os.path.isabs(value) and value.startswith("resources"):
            value = os.path.abspath(os.path.join(path_resources, '..', value))
        # Optionally, check if the file exists.
        path = Path(value)
        if not path.exists():
            raise ValueError(f"gia_model file does not exist at the provided path: {value}")
        return value

    @field_validator("earthquake")
    def validate_earthquake(cls, v: Any) -> Optional[List[str]]:
        """
        Validate the `earthquake` field, ensuring it is a list of allowed years.

        Args:
            v (Any): The input value to be validated, which can be a string (comma-separated list), a list, or `None`.

        Returns:
            Optional[List[str]]: A list of valid earthquake years as strings. If the value is `None` or an empty input,
            returns `None`.

        Raises:
            ValueError: If the value is neither `None`, a list, nor a valid comma-separated string, or if any
            year in the list is not allowed.

        Validation Steps:
            1. If the value is `None` or an empty string, it returns `None`.
            2. If the value is a string, it is split into a list by commas, and any extra whitespace is removed.
            3. If the value is a list, it is used as-is.
            4. The method checks that each year in the list is one of the allowed years: `"2004"`, `"2010"`, `"2011"`.
            5. If an invalid year is found, a `ValueError` is raised.
        """
        # If the value is the string "None", convert it to a Python None.
        if not v:
            return None
        # If the value is a string, assume it is a comma-separated list of years.
        if isinstance(v, str):
            tokens = [token.strip() for token in v.split(",") if token.strip()]  # pragma: no cover
        elif isinstance(v, list):
            tokens = v
        else:
            raise ValueError("earthquake must be provided as a list, a comma-separated string, or 'None'.")
        # Define the set of allowed earthquake years.
        allowed_years = {"2004", "2010", "2011"}
        for token in tokens:
            if token not in allowed_years:
                raise ValueError(f"Invalid earthquake value: {token}. Allowed values are {allowed_years}.")
        return tokens

    @field_validator("time_mean", mode="before")
    def validate_time_mean(cls, value: Optional[str]) -> Optional[str]:
        """
        Validate the `time_mean` field to ensure it is in a valid format and range.

        Args:
            value (Optional[str]): The input value to be validated, expected to be a string representing a date in
            the `YYYY/MM` or `YYYY/MM-YYYY/MM` format.

        Returns:
            str: A normalized date string in the `YYYY/MM` or `YYYY/MM-YYYY/MM` format, or the default
            value `"2002/04-2020/03"` if the input is `None`, empty, or equals `"2002/04-2020/0"`.

        Raises:
            ValueError: If the value is not in the valid `YYYY-MM` or `YYYY/MM-YYYY/MM` format, the month is not
            between `01` and `12`, values outside range 2002/04 and today

        Validation Steps:
            1. If the value is `None`, empty, or the default string `"2002/04-2020/03"`, set to `"2002/04-2020/03"`.
            2. The value is checked against the `YYYY-MM` or `YYYY/MM-YYYY/MM` format using a regular expression.
            3. The month is validated to be between `01` and `12`.
            4. The year-month is checked to fall within the range of `2002/04` and today.
            5. If valid, the string is returned in the normalized `YYYY-MM` or `YYYY/MM-YYYY/MM`
               format with a two-digit month.
        """
        # If value is None, empty, or the default descriptive string, set it to the default valid value "2002-04".
        if value is None or value.strip() == "" or value == "2002/04-2020/03":
            return "2002/04-2020/03"
        value = value.strip()
        # Define allowed period as tuples (year, month).
        allowed_start = (2002, 4)
        today = dt.date.today()
        allowed_end = (today.year, today.month)
        # Pattern for a single month: "YYYY/MM"
        single_pattern = re.compile(r"^(\d{4})/(\d{2})$")
        # Pattern for a range: "YYYY/MM-YYYY/MM"
        range_pattern = re.compile(r"^(\d{4})/(\d{2})-(\d{4})/(\d{2})$")
        m_single = single_pattern.fullmatch(value)
        if m_single:
            year = int(m_single.group(1))
            month = int(m_single.group(2))
            if not (allowed_start <= (year, month) <= allowed_end):
                raise ValueError("The date of time_mean must be between 2002/04 and today.")
            else:
                # Return a normalized value.
                return f"{year:04d}/{month:02d}"
        m_range = range_pattern.fullmatch(value)
        if m_range:
            year1 = int(m_range.group(1))
            month1 = int(m_range.group(2))
            year2 = int(m_range.group(3))
            month2 = int(m_range.group(4))
            if not (allowed_start <= (year1, month1) <= allowed_end and
                    allowed_start <= (year2, month2) <= allowed_end):
                raise ValueError("The start and end of the time range must be between 2002/04 and today.")
            if (year1, month1) > (year2, month2):
                raise ValueError(
                    "The start of the time range must be earlier than or equal to the end."
                )
            return f"{year1:04d}/{month1:02d}-{year2:04d}/{month2:02d}"
        # If the input doesn't match either pattern.
        raise ValueError("time_mean must be in format YYYY/MM for a single month or YYYY/MM-YYYY/MM for a range.")

    @field_validator("max_degree", mode="before")
    def validate_max_degree(cls, value: Any) -> int:
        """
        Validate the `max_degree` field to ensure it is a positive integer, with special handling for default values.

        Args:
            value (Any): The input value to be validated, expected to be a positive
            integer or a string that can be interpreted as one.

        Returns:
            int: The validated positive integer for `max_degree`. Defaults to 96 if the value is
                 `None`, an empty string, or the string "None" (case-insensitive).

        Raises:
            ValueError: If the value cannot be converted to a positive integer, or if the integer is not
            greater than zero.

        Validation Steps:
            1. If the value is `None`, an empty string, or the string "None" (case-insensitive), it defaults to `96`.
            2. If the value is a valid integer string, it is converted to an integer.
            3. If the value is not a valid integer or if the integer is less than or equal to zero,
                a `ValueError` is raised.
        """
        # return the default value of 96.
        if value is None or (isinstance(value, str) and value.strip().lower() in ("", "none")):
            return 96
        try:
            # Convert the value to an integer.
            int_value = int(value)
        except (TypeError, ValueError):
            raise ValueError("max_degree must be a positive integer") from ValueError
        # Check that the integer is positive.
        if int_value <= 0:
            raise ValueError("max_degree must be a positive integer greater than zero")
        return int_value

    @field_validator("domain", mode="before")
    def validate_domain(cls, value: Any) -> Optional[List[str]]:
        """
        Validate the `domain` field to ensure it is a valid list of strings or a single string.

        Args:
            value (Any): The input value to be validated, which can be a string or a list of strings.

        Returns:
            Optional[List[str]]: A list of valid domain values. If the value is empty or contains invalid values,
                                  it returns `["all"]`. If valid, returns the list of domains.

        Raises:
            ValueError: If the value is not a string or a list of strings, or if any list item is invalid.

        Validation Steps:
            1. If the value is a list:

                - Each item must be a string.
                - Allowed domains: "all", "land", "ocean", "ice", "greenland", "antarctica".
                - If "all" is present with other values, the list is replaced with ["all"].

            2. If the value is empty:

                - Defaults to ["all"].

            3. If the value is a string (not a list):

                - A ValueError is raised.

        """
        allowed = {"land", "ocean", "ice", "greenland", "antarctica"}
        if isinstance(value, list):
            if not value:
                return ["all"]
            items = []
            for item in value:
                if not isinstance(item, str):
                    raise ValueError("Each domain value must be a string.")
                item = item.strip()
                if item != "all" and item not in allowed:
                    raise ValueError(f"Invalid domain value: '{item}'. Allowed values are 'all' or {allowed}.")
                items.append(item)
            return items
        else:
            raise ValueError("domain must be provided as a list of strings.")

    @field_validator("sensitivity_kernel_greenland", "sensitivity_kernel_antarctica", mode="before")
    def validate_sensitivity_kernel(cls, value: Any, info) -> str:
        """
        Validate the "sensitivity_kernel_greenland/antarctica" field to ensure it meets the required criteria.

        The validation ensures that the value is a string, trims extra whitespace, checks that
        the string ends with '.nc', and optionally verifies if the file exists at the provided
        path.

        Parameters:
            value: Any
                The value provided for the "sensitivity_kernel_x" field.

        Returns:
            str:
                The validated and potentially modified string value.

        Raises:
            ValueError:
                If the value is not a string, is empty, does not end with '.nc', or if the file
                does not exist on the provided path.

        """
        field_name = info.field_name

        # Allow None to pass through.
        if value is None:
            return None

        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string representing the file path.")
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError(f"{field_name} cannot be an empty string.")
        # Check that the file path ends with '.nc'
        if not value.endswith(".nc"):
            raise ValueError(f"{field_name} must point to a file with a '.nc' extension.")
        # Optionally, check if the file exists.
        if not os.path.isabs(value) and value.startswith("resources"):
            value = os.path.abspath(os.path.join(path_resources, '..', value))
        path = Path(value)
        if not path.exists():
            raise ValueError(f"{field_name} file does not exist at the provided path: {value}")
        return value

    @field_validator("reference_surface", mode="before")
    def validate_reference_surface(cls, value: Any) -> str:
        """
        Validate and normalizes the `reference_surface` field, ensuring it is a valid string.

        Args:
            value (Any): The input value to be validated, expected to be a string.

        Returns:
            str: The validated and normalized `reference_surface` value.
            Defaults to `"ellipsoidal"` if no value is provided.

        Raises:
            ValueError: If the value is not a string or is not one of the allowed options.

        Validation Steps:
            1. If the value is `None` or an empty string, it defaults to `"ellipsoidal"`.
            2. Ensures the value is a string.
            3. Trims whitespace and converts the string to lowercase.
            4. Checks that the value is one of the allowed options: `"ellipsoidal"` or `"spherical"`.
        """
        # If the value is None or an empty string, default to "ellipsoidal".
        if value is None or (isinstance(value, str) and not value.strip()):
            return "ellipsoidal"
        if not isinstance(value, str):
            raise ValueError("reference_surface must be provided as a string.")
        # Normalize the string (trim whitespace and convert to lowercase).
        value = value.strip().lower()
        allowed = {"ellipsoidal", "spherical"}
        if value not in allowed:
            raise ValueError(
                f"Invalid reference_surface value: '{value}'. "
                f"Allowed values are: {allowed}."
            )
        return value

    @field_validator("land_ocean_mask", mode="before")
    def validate_land_ocean_mask(cls, value: Any) -> str:
        """
        Validate the `land_ocean_mask` field to ensure it meets required criteria.

        Args:
            value (Any): The input value to be validated, expected to be a file path string.

        Returns:
            str: The validated and cleaned file path.

        Raises:
            ValueError: If any of the following conditions are not met:
                - The value is not a string.
                - The string is empty or contains only whitespace.
                - The file path does not have a `.nc` extension.
                - The file path does not point to an existing file.
        """
        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError("land_ocean_mask must be a string representing the file path.")
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError("land_ocean_mask cannot be an empty string.")
        # Check that the file path ends with '.nc'
        if not value.endswith(".nc"):
            raise ValueError("land_ocean_mask must point to a file with a '.nc' extension.")
        if not os.path.isabs(value) and value.startswith("resources"):
            value = os.path.abspath(os.path.join(path_resources, '..', value))
        # Optionally, check if the file exists.
        path = Path(value)
        if not path.exists():
            raise ValueError(f"land_ocean_mask file does not exist at the provided path: {value}")
        return value

    @field_validator("land_ice_mask", mode="before")
    def validate_ice_mask(cls, value: Any) -> str:
        """
        Validate the `ice_mask` field to ensure it meets required criteria.

        Args:
            value (Any): The input value to be validated, expected to be a file path string.

        Returns:
            str: The validated and cleaned file path.

        Raises:
            ValueError: If any of the following conditions are not met:
                - The value is neither a string nor None.
                - The string is empty or contains only whitespace.
                - The file path does not have a `.nc` extension.
                - The file path does not point to an existing file.

        Validation Steps:
            1. If the value is `None` or an empty string, it returns `None`.
            2. If the value is a string, it is split into a list by commas, and any extra whitespace is removed.
            3. If the value is a list, it is used as-is.
            4. The method checks that each year in the list is one of the allowed years: `"2004"`, `"2010"`, `"2011"`.
            5. If an invalid year is found, a `ValueError` is raised.
        """
        # If the value is the string "None", convert it to a Python None.
        if value is None:
            return None
        # Normalize the input.
        normalized = value.strip().lower()
        if normalized == "none":
            # Return actual None if the input is "None"
            return None
        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError("ice_mask must be a string representing the file path or None.")
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError("ice_mask cannot be an empty string.")
        # Check that the file path ends with '.nc'
        if not value.endswith(".nc"):
            raise ValueError("ice_mask must point to a file with a '.nc' extension.")
        if not os.path.isabs(value) and value.startswith("resources"):
            value = os.path.abspath(os.path.join(path_resources, '..', value))
        # Optionally, check if the file exists.
        path = Path(value)
        if not path.exists():
            raise ValueError(f"ice_mask file does not exist at the provided path: {value}")
        return value

    @field_validator("logging_level")
    def validate_logging_level(cls, v: str) -> str:  # noqa: N805
        """
        Validate that the logging level is correct.

        The logging level must be one of the following:
        - "DEBUG"
        - "INFO"
        - "WARN"
        - "ERROR"

        Parameters
        ----------
        v : str
            The logging level to validate.

        Returns
        -------
        str
            The validated logging level.

        Raises
        ------
        ValueError
            If the logging level is not one of the allowed values.
        """
        if v not in ["DEBUG", "INFO", "WARN", "ERROR"]:
            raise ValueError("Logging level, it should be one of: DEBUG, INFO, WARN, or ERROR.")
        return v

    @field_validator("insert_geocenter_motion", mode="before")
    def validate_insert_geocenter_motion(cls, value: Any) -> bool:
        """
        Validate and normalizes the `insert_geocenter_motion` field, ensuring it is a valid string.

        Args:
            value (Any): The input value to be validated, expected to be a string.

        Returns:
            Bool: The validated and normalized `insert_geocenter_motion` value.
            Defaults to `True` if no value is provided.

        Raises:
            ValueError: If the value is not a string or is not one of the allowed options (True False.

        Validation Steps:
            1. If the value is `None` or an empty string, it defaults to `True`.
            2. Ensures the value is a string.
            3. Trims whitespace and converts the string to lowercase.
            4. Checks that the value is one of the allowed options: {"true", "True", "false", "False", "y", "n"}
            5. Returns true or false as bool
        """
        # If the value is None or an empty string, default to "ellipsoidal".
        if value is None or (isinstance(value, str) and not value.strip()):
            return True
        if not (isinstance(value, str) or isinstance(value, bool)):
            raise ValueError("insert_geocenter_motion must be provided as a string or bool.")
        if isinstance(value, bool):
            return value
        else:
            # Normalize the string (trim whitespace and convert to lowercase).
            value = value.strip().lower()
            allowed = {"true", "True", "false", "False", "y", "n"}
            if value not in allowed:
                raise ValueError(
                    f"Invalid insert_geocenter_motion value: '{value}'. "
                    f"Allowed values are: {allowed}."
                )
            if value in {"true", "True", "y"}:
                return True
            else:
                return False

    @field_validator("remove_s2_aliased_signal", mode="before")
    def validate_remove_s2_aliased_signal(cls, value: Any) -> bool:
        """
        Validate and normalizes the `remove_s2_aliased_signal` field, ensuring it is a valid string.

        Args:
            value (Any): The input value to be validated, expected to be a string.

        Returns:
            Bool: The validated and normalized `remove_s2_aliased_signal` value.
            Defaults to `True` if no value is provided.

        Raises:
            ValueError: If the value is not a string or is not one of the allowed options (True False.

        Validation Steps:
            1. If the value is `None` or an empty string, it defaults to `True`.
            2. Ensures the value is a string.
            3. Trims whitespace and converts the string to lowercase.
            4. Checks that the value is one of the allowed options: {"true", "True", "false", "False", "y", "n"}
            5. Returns true or false as bool
        """
        # If the value is None or an empty string, default to True.
        if value is None or (isinstance(value, str) and not value.strip()):
            return True
        if not (isinstance(value, str) or isinstance(value, bool)):
            raise ValueError("remove_s2_aliased_signal must be provided as a string.")
        if isinstance(value, bool):
            return value
        else:
            # Normalize the string (trim whitespace and convert to lowercase).
            value = value.strip().lower()
            allowed = {"true", "True", "false", "False", "y", "n"}
            if value not in allowed:
                raise ValueError(
                    f"Invalid remove_s2_aliased_signal value: '{value}'. "
                    f"Allowed values are: {allowed}."
                )
            if value in {"true", "True", "y"}:
                return True
            else:
                return False

    @field_validator("region_land_geojson", mode="before")
    def validate_region_land_geojson(cls, value: Any) -> str:
        """
        Validate the `region_land_geojson` field to ensure it meets required criteria.

        Args:
            value (Any): The input value to be validated, expected to be a file path string.

        Returns:
            str: The validated and cleaned file path.

        """
        # If the value is the string "None", convert it to a Python None.
        if value is None:
            return None
        # Normalize the input.
        normalized = value.strip().lower()
        if normalized == "none":
            # Return actual None if the input is "None"
            return None
        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError("region_land_geojson must be a string representing the file path or None.")
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError("region_land_geojson cannot be an empty string.")
        # Check that the file path ends with '.nc'
        if not value.endswith(".geojson"):
            raise ValueError("region_land_geojson must point to a file with a '.geojson' extension.")
        if not os.path.isabs(value) and value.startswith("resources"):
            value = os.path.abspath(os.path.join(path_resources, '..', value))
        # Optionally, check if the file exists.
        path = Path(value)
        if not path.exists():
            raise ValueError(f"region_land_geojson file does not exist at the provided path: {value}")
        return value

    @field_validator("region_ocean_geojson", mode="before")
    def validate_region_ocean_geojson(cls, value: Any) -> str:
        """
        Validate the `region_ocean_geojson` field to ensure it meets required criteria.

        Args:
            value (Any): The input value to be validated, expected to be a file path string.

        Returns:
            str: The validated and cleaned file path.

        """
        # If the value is the string "None", convert it to a Python None.
        if value is None:
            return None
        # Normalize the input.
        normalized = value.strip().lower()
        if normalized == "none":
            # Return actual None if the input is "None"
            return None
        # Ensure the value is a string.
        if not isinstance(value, str):
            raise ValueError("region_ocean_geojson must be a string representing the file path or None.")
        # Trim any extra whitespace.
        value = value.strip()
        if not value:
            raise ValueError("region_ocean_geojson cannot be an empty string.")
        # Check that the file path ends with '.nc'
        if not value.endswith(".geojson"):
            raise ValueError("region_ocean_geojson must point to a file with a '.geojson' extension.")
        if not os.path.isabs(value) and value.startswith("resources"):
            value = os.path.abspath(os.path.join(path_resources, '..', value))
        # Optionally, check if the file exists.
        path = Path(value)
        if not path.exists():
            raise ValueError(f"region_ocean_geojson file does not exist at the provided path: {value}")
        return value


class Config(BaseModel):
    """Template for the configuration file."""

    mandatory_settings: MandatorySettings = Field(title="Mandatory settings.", description="")
    optional_settings: OptionalSettings = Field(title="Optional settings.", description="")

    @model_validator(mode="after")
    def check_dependency_ice_kernel(cls, v):
        """
        Validate the model configuration for specific dependencies related to ice domains.

        This function checks if sensitivity kernel settings are provided whenever the domain
        includes ice-related identifiers.
        This validation ensures the configuration adheres to necessary requirements for ice
        domain scenarios.

        Parameters:
            v: Input configuration containing optional settings,
            including 'domain' and 'sensitivity_kernel_greenland'/'sensitivity_kernel_antarctica'.

        Returns:
            The validated configuration.

        Raises:
            ValueError: If the domain contains ice-related identifiers (e.g., "ice",
            "greenland", "antarctica") and no sensitivity kernel is provided.
        """
        domain = v.optional_settings.domain
        sensitivity_kernel_greenland = v.optional_settings.sensitivity_kernel_greenland
        sensitivity_kernel_antarctica = v.optional_settings.sensitivity_kernel_antarctica
        if "greenland" in domain and sensitivity_kernel_greenland is None:
            raise ValueError("For greenland domain, sensitivity kernel greenland must be provided")
        if "antarctica" in domain and sensitivity_kernel_antarctica is None:
            raise ValueError("For antarctica domain, sensitivity kernel antarctica must be provided")
        if "ice" in domain and sensitivity_kernel_antarctica is None and sensitivity_kernel_greenland is None:
            raise ValueError("For ice domain, sensitivity kernel antarctica and greenland must be provided")
        return v

    @model_validator(mode="after")
    def check_dependency_spatial_resolution(cls, v):
        """
        Check if spatial resolution of grid, lo mask and ice mask fit.

        Parameters
        ----------
            v: Input configuration containing optional settings,
            including 'domain' and 'sensitivity_kernel_greenland'/'sensitivity_kernel_antarctica'.

        Returns:
        ---------
            The validated configuration.

        Raises:
        ----------
            ValueError: grid definition and grid of lo mask do not fit.
            ValueError: grid of ice mask and grid of lo mask do not fit.
        """
        from geogravl3.utils.utils import create_test_logger
        test_logger = create_test_logger()
        grid_file = v.optional_settings.grid
        grid = read_grid_definition(grid_file)
        lo_mask_file = v.optional_settings.land_ocean_mask
        lo_mask = read_mask(logger=test_logger, file_name=lo_mask_file)
        lon_mask = lo_mask.lon
        lat_mask = lo_mask.lat
        if (lon_mask[0] != grid['xfirst'] or (lon_mask[1] - lon_mask[0]) != grid['xinc'] or
                lat_mask[0] != grid['yfirst'] or (lat_mask[1] - lat_mask[0]) != grid['yinc']):
            raise ValueError(f"Grid definition between grid and land-ocean mask do not match with: "
                             f"mask lon_0={lon_mask[0]}, lat_0={lat_mask[0]}, "
                             f"delta_lon={lon_mask[1] - lon_mask[0]}, delta_lat={lat_mask[1] - lat_mask[0]} "
                             f"and grid definition lon_0={grid['xfirst']}, lat_0={grid['xfirst']}, "
                             f"delta_lon={grid['xinc']}, delta_lat={grid['yinc']}")
        if v.optional_settings.land_ice_mask is not None:
            ice_mask_file = v.optional_settings.land_ice_mask
            ice_mask = read_mask(logger=test_logger, file_name=ice_mask_file)
            if not ice_mask.same_coords(lo_mask):
                raise ValueError("Grid definition ofLand-ocean and ice mask do not match")
        return v

    @model_validator(mode="after")
    def check_gia_model_max_degree(cls, v):
        """
        Check if max degree of configuration is smaller than max degree of GIA model.

        Parameters
        ----------
            v: Input configuration containing optional settings, including 'gia_model'.

        Returns:
        ---------
            The validated configuration.

        Raises:
        ----------
            ValueError: If max degree of gia model is smaller than max degree of configuration.
        """
        if v.optional_settings.gia_model is not None:
            from geogravl3.utils.utils import create_test_logger
            test_logger = create_test_logger()
            gia_model_file = v.optional_settings.gia_model
            gia_model_shc = read_gfc(logger=test_logger, file_name=gia_model_file, max_degree=None)
            n_max_gia = gia_model_shc.get_max_degree()
            n_max_config = v.optional_settings.max_degree
            if n_max_gia < n_max_config:
                raise ValueError(f"max degree of gia model {n_max_gia} is smaller than max degree set in config for "
                                 f"SH synthesis {n_max_config}")
        return v

    @model_validator(mode="after")
    def check_lengths_of_low_degree_file(cls, v):
        """
        Check if provided low degree harmonics file matches lengths of data.

        Parameters
        ----------
            v: Input configuration containing optional settings, including 'lowdegree_coefficients'.

        Returns:
        ---------
            The validated configuration.

        Raises:
        ----------
            ValueError: If 'lowdegree_coefficients' is shorter than the input data.
        """
        if v.optional_settings.lowdegree_coefficients is not None:
            low_degree_file = v.optional_settings.lowdegree_coefficients
            dates, c20, c21, s21, c30 = read_lowdegree_coefficients(low_degree_file)
            inputfolder = v.mandatory_settings.input_folder
            from ..utils.utils import create_test_logger
            test_logger = create_test_logger()
            shc_input, _ = read_input_folder(logger=test_logger, file_list=inputfolder)
            dates_shc = np.array([s.date for s in shc_input])
            if (dates_shc[0] < (dates[0] - dt.timedelta(days=5))
                    or dates_shc[-1] > (dates[-1] + dt.timedelta(days=5))):
                raise ValueError(f"First time step of the input data {dates_shc[0]} is before the first time step "
                                 f" in the low degree harmonics file with {dates[0]}. "
                                 f"Or last time step of the input data {dates_shc[-1]} is after the last time step "
                                 f" in the low degree harmonics file with {dates[-1]}. Considering a date mismatch "
                                 f"of up to five days.")
        return v

    @model_validator(mode="after")
    def check_sinex_vdk(cls, v):
        """
        Check if sinex files are provided with input if VDK filter is chosen.

        Parameters
        ----------
            v: Input configuration containing optional settings, including 'filter' set to vdk.

        Returns:
        ---------
            The validated configuration.

        Raises:
        ----------
            ValueError: If 'filter'=vdk is set but no sinex files provided in input folder.
        """
        if v.optional_settings.filter is not None:
            if any([re.compile(r"^VDK[1-8]$").fullmatch(item) for item in v.optional_settings.filter]):
                snx_files = [file for file in os.listdir(v.mandatory_settings.input_folder)
                             if file.endswith(".snx")]
                if not snx_files:
                    raise ValueError("VDK Filter has been set but no SINEX file is provided in the input folder")
        return v


def load_configuration(path_config: str) -> dict:
    """
    Load configuration file in json or xml format.

    Parameters
    ----------
    path_config : str
        Path to the configuration file (JSON or XML format).

    Returns
    -------
    : dict
        A dictionary containing configurations.

    Raises
    ------
    OSError
        Failed to load the configuration file.
    ValueError
        If the configuration file is neither a json nor an xml file.
    """
    if path_config.endswith(".json"):
        return load_json_configuration(path_config)
    elif path_config.endswith(".xml"):
        return load_xml_configuration(path_config)
    else:
        raise ValueError(f"Config file {path_config} is neither a json nor an xml file.")
