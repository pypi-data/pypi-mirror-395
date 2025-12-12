#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Reader functions for geogravL3 package."""

import datetime as dt
import os
import re
from dataclasses import dataclass
from logging import Logger
from typing import Union, Tuple, List, Any, Dict
import json
from pathlib import Path

import numpy as np
from netCDF4 import Dataset
import pandas as pd

from ..datamodels.grids import Grid2DObject
from ..datamodels.shc import SHObject


def read_input_folder(logger: Logger, file_list: Union[list[str], str], max_degree: int = None) \
        -> Tuple[List, Dict[dt.datetime, str]]:
    """
    Read all data in the input folder depending on if gfc or sinex files.

    Parameters
    ----------
    logger (Logger): logger object to log the error messages
    file_list (Union[list of str, str])
    List of filenames or a string representing the folder name. If a folder is provided,
    all files in the folder will be read.
    max_degree: maximum degree and order to be read

    Returns
    -------
    sh_objects (list): Read data in SHObjects
    dict_date_filename (dict): Only needed for sinex files linking the date to the file name for later repeated reading
    """
    from ..processing.shc_processing.vdk_filter_functions import _build_CS_matrices

    if isinstance(file_list, str):
        # Treat as folder
        file_list = [os.path.join(file_list, f) for f in sorted(os.listdir(file_list))
                     if f.endswith(".gfc") or f.endswith('snx')]
    if file_list[0].endswith(".gfc"):
        if max_degree is not None:
            sh_objects = read_folder_gfc(logger=logger, file_list=file_list, max_degree=max_degree)
        else:
            sh_objects = read_folder_gfc(logger=logger, file_list=file_list)
        dict_date_filename = {}
    elif file_list[0].endswith(".snx"):
        sections = parse_sinex_sections(file_list[0])
        keys_to_keep = ['nou', 'estimate', 'total_lines', 'date', 'max_degree']
        sections_subset = {k: sections[k] for k in keys_to_keep if k in sections}
        sh_objects = []
        dict_date_filename = {}
        for filepath in file_list:
            if filepath.endswith(".snx"):
                data = read_sinex_data(logger=logger, path=filepath, sections=sections_subset)
                cnm, snm = _build_CS_matrices(df=data['estimate'], n_max=data['max_degree'])
                sh_objects.append(SHObject(logger=logger, date=data['date'], cnm=cnm, snm=snm))
                dict_date_filename[data['date']] = filepath
    else:
        message = 'Neither .gfc nor .snx files found the be read.'
        logger.error(message)
        raise ValueError(message)
    return sh_objects, dict_date_filename


def read_folder_gfc(logger: Logger, file_list: Union[list[str], str], max_degree: int = 96) -> list[SHObject]:
    """
    Read all SH coefficient files in the format gfc (Standard of ICGEM) in folder or list.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    file_list: Union[list of str, str]
        List of filenames or a string representing the folder name. If a folder is provided,
        all files in the folder will be read.
    max_degree: int, optional
        Maximum degree for the spherical harmonic coefficients (default is 96).

    Returns
    -------
    sh_objects: list[SHObject]
        A list of SHObject instances, one for each file. Uses the lowest max_degree found across all files.
    """
    sh_objects = []

    if isinstance(file_list, str):
        # Treat as folder
        file_list = [os.path.join(file_list, f) for f in sorted(os.listdir(file_list)) if f.endswith(".gfc")]

    min_max_degree = max_degree

    # First pass to determine the lowest max_degree
    for filepath in file_list:
        if filepath.endswith(".gfc"):
            with open(filepath) as file:
                lines = file.readlines()
                for line in lines:
                    if "max_degree" in line:
                        max_degree_line = line.split()
                        max_from_file = int(max_degree_line[1])
                    if "end_of head" in line:
                        break  # pragma: no cover
                min_max_degree = min(min_max_degree, int(max_from_file))

    # Notify user if min_max_degree differs from initial max_degree
    if min_max_degree < max_degree:
        logger.warning(  # pragma: no cover
            f"Warning: The minimum max_degree found across all files ({min_max_degree}) is lower "
            f"than the specified max_degree ({max_degree}). Using {min_max_degree}."
        )
    if min_max_degree > max_degree:
        logger.warning(  # pragma: no cover
            f"Warning: The minimum max_degree found across all files ({min_max_degree}) is higher "
            f"than the specified max_degree ({max_degree}). Using {max_degree}."
        )

    # Second pass to read files using the lowest max_degree
    for filepath in file_list:
        if filepath.endswith(".gfc"):
            try:
                sh_objects.append(read_gfc(logger=logger, file_name=filepath, max_degree=min_max_degree))
            except (IndexError, ValueError) as e:  # pragma: no cover
                logger.error(f"Error reading file {filepath}: {e}")  # pragma: no cover

    return sh_objects


def read_gfc(logger: Logger, file_name: str, max_degree: int = None) -> SHObject:
    """
    Read single gfc file.

    Parameters
    ----------
    logger: Logger, Logger object to log the error messages
    file_name: str, name of gfc file
    max_degree: int, optional Maximum degree for the spherical harmonic coefficients (default is 96).
    If None read from file

    Returns
    -------
    SHObject: SHObject: an instance of the SHObject class containing the date, cnm, and snm.
    """
    with open(file_name) as file:
        lines = file.readlines()
        date = dt.datetime(2010, 1, 1, 0, 0)  # dummy date, if no date is found in file
        data_line_index = 0
        for i, line in enumerate(lines):
            if "time_period" in line:  # this only handles gfc files of the SDS and COST-G
                if "time_period_of_data" in line:
                    date_line = re.findall(r"\d{8}", line)
                    date_start = dt.datetime.strptime(date_line[0], "%Y%m%d")
                    date_end = dt.datetime.strptime(date_line[1], "%Y%m%d")
                    date = date_start + (date_end - date_start) / 2
                else:
                    match = re.search(r'(\d{7})-(\d{7})', line)
                    start_str, end_str = match.groups()
                    start_date = dt.datetime.strptime(start_str, "%Y%j")
                    end_date = dt.datetime.strptime(end_str, "%Y%j")
                    date = start_date + (end_date - start_date) / 2

            if "max_degree" in line:
                max_degree_line = line.split()
                max_degree_file = int(max_degree_line[1])
            if "end_of_head" in line:
                data_line_index = i
                break

        if max_degree is None:
            max_degree = max_degree_file

        data_lines = lines[data_line_index + 1:]
        cnm = np.zeros((max_degree + 1, max_degree + 1))
        snm = np.zeros((max_degree + 1, max_degree + 1))
        for line in data_lines:
            parts = line.split()
            var_l = int(parts[1])
            var_m = int(parts[2])
            if var_l <= max_degree and var_m <= max_degree:
                var_c = float(parts[3])
                var_s = float(parts[4])
                cnm[var_l, var_m] = var_c
                snm[var_l, var_m] = var_s
        # Return an instance of SHObject
        return SHObject(logger=logger, date=date, cnm=cnm, snm=snm)


def read_lowdegree_coefficients(file_name: str) \
        -> Tuple[List[dt.date], List[float], List[float], List[float], List[float]]:
    """
    Read low-degree coefficients from a GRACE/GRACE-FO data file.

    Parameters
    ----------
    file_name (str): Path to the data file

    Returns
    -------
    tuple: Containing lists/arrays of:
    - dates (MJD)
    - c20 coefficients
    - c21 coefficients
    - s21 coefficients
    - c30 coefficients
    """
    dates = []
    c20 = []
    c21 = []
    s21 = []
    c30 = []
    # Skip header lines
    with open(file_name) as f:
        lines = f.readlines()
        data_lines = lines[lines.index("PRODUCT:\n") + 1:]
        for line in data_lines:
            # Extract columns based on the format description
            parts = line.split()
            # convert MJD from column 0 to datetime object
            mjd_epoch = dt.datetime(year=1858, month=11, day=17)
            mjd_date = mjd_epoch + dt.timedelta(days=np.float64(parts[0]))
            # fill lists
            dates.append(mjd_date)  # MJD (Column 1)
            c20.append(np.float64(parts[2]))  # C(2,0) coefficient (Column 3)
            c30.append(np.float64(parts[5]))  # C(3,0) coefficient (Column 6)
            c21.append(np.float64(parts[8]))  # C(2,1) coefficient (Column 9)
            s21.append(np.float64(parts[11]))  # S(2,1) coefficient (Column 12)

    return dates, c20, c21, s21, c30


def read_nc(file_name: str) -> dict:
    """
    Read the contents of a NetCDF file and extracts variable data along with its attributes.

    Args:
        file_name (str): Path to the NetCDF file to be read.

    Returns:
        dict: A dictionary containing the variables from the NetCDF file.
              Each variable is represented as a key, and its value is a dictionary with:
              - `"value"`: The variable's data (as a NumPy array or similar structure).
              - `"attributes"`: A dictionary of the variable's attributes.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        OSError: If there is an issue opening or reading the NetCDF file.

    Example Usage:
        ```
        data = read_nc("data_file.nc")
        units = data["temperature"]["attributes"]["units"]  # Access temperature units
        ```
    """
    file_content = {}

    # Open the NetCDF file
    with Dataset(file_name, mode="r") as nc_file:
        # Loop through all variables in the file
        for var_name in nc_file.variables:
            var_data = nc_file.variables[var_name]

            # Read variable data and attributes
            value = var_data[:].filled(np.nan)
            attributes = {attr_name: getattr(var_data, attr_name) for attr_name in var_data.ncattrs()}

            # Store data in the output dictionary
            file_content[var_name] = {"value": value, "attributes": attributes}

    return file_content


def read_mask(logger: Logger, file_name: str) -> Grid2DObject:
    """
    Read a netcdf file containing a mask.

    Parameters
    ----------
    logger: Logger, Logger object to log the error messages
    file_name: str, name of netcdf file

    Returns
    -------
    mask: Grid2DObject: an instance of the Grid2DObject class containing the mask, lon, and lat.

    Raises
    -------
        ValueError: If there is an issue opening or reading the NetCDF file.
    """
    ncdata = read_nc(file_name)

    lon = next(
        (ncdata[key]["value"] for key in ncdata if key in {"lon", "longitude"}),
        None)
    if lon is None:
        message = "No lon or longitude definition found in NetCDF file {}".format(file_name)
        logger.error(message)
        raise ValueError(message)

    lat = next(
        (ncdata[key]["value"] for key in ncdata if key in {"lat", "latitude"}),
        None)
    if lat is None:
        message = "No lat or latitude definition found in NetCDF file {}".format(file_name)
        logger.error(message)
        raise ValueError(message)

    # Takes the first variable in the nc file that contains mask in the variable name.
    # If no variable name contains grid, take the first variable of the nc file but not lon, lat, or time
    mask = next(
        (ncdata[key]["value"] for key in ncdata if "mask" in key),
        next(
            (ncdata[key]["value"] for key in ncdata if key not in {"lon", "lat", "time"}),
            None))
    if mask is None:
        message = "No mask or variable that could be understood as mask found in NetCDF file {}".format(file_name)
        logger.error(message)
        raise ValueError(message)
    # Convert the dtype to bool
    bool_masked_array = mask.astype(bool)

    return Grid2DObject(logger=logger, grid=bool_masked_array, lon=lon, lat=lat)


def read_load_love_numbers(logger: Logger, file_name: str) -> dict:
    """
    Read the load love numbers from file.

    Parameters
    ----------
    logger: Logger, Logger object to log the error messages
    file_name: str, name of load love numbers file, column 1: degrees, column 2: h, column 3: l, column 4: k

    Returns
    -------
    lln: dict, keys are 'degree', 'h', 'l', 'k', values each np.ndarray containing the resp. columns of the file
    """
    degree = []
    h = []
    var_l = []  # noqa
    k = []
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            # Extract columns based on the format description
            parts = line.split()
            if len(parts) < 4:
                message = (f"Load love numbers file {file_name} contain less then 4 columns. "
                           f"Required columns are degree, h, l, and k")
                logger.error(message)
                raise ValueError(message)
            degree.append(int(parts[0]))  # (Column 1)
            h.append(np.float64(parts[1].replace("D", "E")))  # (Column 2)
            var_l.append(np.float64(parts[2].replace("D", "E")))  # (Column 3)
            k.append(np.float64(parts[3].replace("D", "E")))  # (Column 4)

    return dict(degree=np.array(degree), h=np.array(h), l=np.array(var_l), k=np.array(k))


def read_grid_definition(file_name: str) -> dict:
    """
    Read and parses a grid definition file to extract grid-related parameters.

    Args:
        file_name (str): Path to the grid definition file.

    Returns:
        dict: A dictionary containing grid parameters extracted from the file.
              The keys include:
              - "xsize", "ysize" (grid dimensions)
              - "xfirst", "xinc", "yfirst", "yinc" (coordinate and increment values)

    The function processes each line in the file, extracting key-value pairs where:
    - Keys are specific parameters such as "xsize" or "xinc".
    - Values are converted to `numpy.float64` for precision.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file contains improperly formatted lines.

    """
    grid_information = {}

    with open(file_name) as file:
        for line in file:
            # Remove whitespace and split at '='
            parts = line.strip().split("=")
            if len(parts) == 2:
                key, value = parts[0].strip(), parts[1].strip().removesuffix(",")

                # Add relevant keys to the dictionary
                if key in ["xsize", "ysize"] or key in ["xfirst", "xinc", "yfirst", "yinc"]:
                    grid_information[key] = np.float64(value)

    return grid_information


def read_shnc_coeff_2_SHObject(logger: Logger, filename: str, variable_name: str) -> list[SHObject]:
    """
    Read sh coefficients stored in netcdf in the SHNC tool format.

    Parameters
    ----------
    logger (Logger): logger object to log the error messages
    filename (str): path to file to be read
    variable_name (str): Variable name in netcdf file

    Returns
    -------
    list_SHObjects (list[SHObjects]): List of the SHObjects read from file. One object per time slice
    """
    from ..utils.date_utils import datetime_from_nc_time
    data_nc = read_nc(filename)
    coefficients_shnc = data_nc[variable_name]['value']
    degrees = data_nc['Degree']['value']
    orders = data_nc['Order']['value']
    time = datetime_from_nc_time(logger=logger,
                                 time_values=data_nc['time']['value'],
                                 time_attributes=data_nc['time']['attributes'])
    if not isinstance(time, (list, np.ndarray)):
        time = [time]  # pragma: no cover
    max_degree = np.max(data_nc['Degree']['value'])

    list_SHObjects = []
    for i in range(len(time)):
        date = time[i]
        cnm = np.zeros((max_degree + 1, max_degree + 1))
        snm = np.zeros((max_degree + 1, max_degree + 1))
        coeff = coefficients_shnc[i, :, :]
        for i in range(max_degree + 1):
            for j in range(max_degree + 1):
                d = degrees[i, j]
                o = orders[i, j]
                if j >= i:
                    cnm[d, o] = coeff[i, j]
                else:
                    snm[d, o] = coeff[i, j]

        list_SHObjects.append(SHObject(logger=logger, date=date, cnm=cnm, snm=snm))

    return list_SHObjects


@dataclass
class EQDef:
    """
    Store definitions related to an earthquake event.

    This class holds various attributes to define an earthquake's date, its
    epicenter's coordinates, and associated spatial deltas for latitude and
    longitude. It is intended to encapsulate essential earthquake event
    information for use in further computational or analytical processes.

    Attributes:
        eve_year: int
            Year of the earthquake event.
        eve_month: int
            Month of the earthquake event.
        eve_day: int
            Day of the earthquake event.
        pre_year: int
            Year of the preceding event or related data.
        pre_month: int
            Month of the preceding event or related data.
        aft_year: int
            Year of the subsequent event or related data.
        aft_month: int
            Month of the subsequent event or related data.
        epi_lat: float
            Latitude coordinate of the earthquake's epicenter.
        epi_lon: float
            Longitude coordinate of the earthquake's epicenter.
        del_lat: float
            Delta or offset value for latitude associated with the event.
        del_lon: float
            Delta or offset value for longitude associated with the event.
    """

    eve_year: int
    eve_month: int
    eve_day: int
    pre_year: int
    pre_month: int
    aft_year: int
    aft_month: int
    epi_lat: float
    epi_lon: float
    del_lat: float
    del_lon: float


def parse_eqfile(logger: Logger, eqfile: str) -> EQDef:
    """
    Parse earthquake ASCII file with the same semantics as the original csh script.

    Expected numeric tokens:
      line 1: event  <year> <month> <day>     -> first three numeric tokens
      line 3: pre    <year> <month>           -> first two numeric tokens
      line 4: post   <year> <month>           -> first two numeric tokens
      line 5: epi_lat                           first numeric token
      line 6: del_lat                           first numeric token
      line 7: epi_lon                           first numeric token
      line 8: del_lon                           first numeric token
    """
    with open(eqfile, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()
    if len(lines) < 8:
        message = "eqfile has fewer than 8 lines."
        logger.error(message)
        raise ValueError(message)

    l1 = grab(lines[0])
    assert len(l1) >= 3
    eve_year, eve_month, eve_day = map(int, l1[:3])

    l3 = grab(lines[2])
    assert len(l3) >= 2
    pre_year, pre_month = map(int, l3[:2])

    l4 = grab(lines[3])
    assert len(l4) >= 2
    aft_year, aft_month = map(int, l4[:2])

    epi_lat = float(grab(lines[4])[0])
    del_lat = float(grab(lines[5])[0])
    epi_lon = float(grab(lines[6])[0])
    del_lon = float(grab(lines[7])[0])

    return EQDef(eve_year, eve_month, eve_day,
                 pre_year, pre_month, aft_year, aft_month,
                 epi_lat, epi_lon, del_lat, del_lon)


def grab(s: str):
    """
    Extract numerical values from a string.

    This function scans a string and extracts all substrings that represent
    numerical values. It returns a list of all extracted numerical values in
    string format.

    Args:
        s (str): The input string to search for numerical values.

    Returns:
        list: A list of numeric values found in the input string as strings.
    """
    return re.findall(r"[+-]?\d+(?:\.\d+)?", s)


def read_region_geojson(logger: Logger, file_path: str) -> list[dict[str, Any]]:
    """
    Read predefined regions (e.g., river basins, ocean regions) from a GeoJSON file.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    file_path : str
        Path to the GeoJSON file containing polygonal regions.

    Returns
    -------
    list of dict
        A list of dictionaries with keys:
        - 'name': region name (string)
        - 'geometry': geometry coordinates from the GeoJSON

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file content is invalid or contains no features.
    """
    path = Path(file_path)
    if not path.exists():
        message = f"GeoJSON file not found: {file_path}"
        logger.error(message)
        raise FileNotFoundError(message)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        message = f"Invalid JSON structure: {file_path}"
        logger.error(message)
        raise ValueError(message)

    if "features" not in data or not isinstance(data["features"], list) or len(data["features"]) == 0:
        message = f"Invalid GeoJSON file (no features): {file_path}"
        logger.error(message)
        raise ValueError(message)

    regions = []
    for i, feature in enumerate(data["features"]):
        geom = feature.get("geometry")
        props = feature.get("properties", {})
        if geom is None:
            continue
        name = props.get("name", f"region_{i}")
        regions.append({"name": name, "geometry": geom})

    if not regions:
        message = f"No valid geometries found in GeoJSON: {file_path}"
        logger.error(message)
        raise ValueError(message)
    return regions


def read_ice_basins_from_kernel(logger: Logger, file_path: str) -> dict[int, dict[str, np.ndarray]]:
    """
    Read basin masks and associated area information from a sensitivity kernel NetCDF file.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    file_path : str
        Path to the NetCDF file containing 'Mask_basinnumbers' and 'area' variables.

    Returns
    -------
    dict[int, dict[str, np.ndarray]]
        Mapping of basin_number → {'mask': 2D boolean array, 'area': 2D float array}

    Raises
    ------
    FileNotFoundError
        If the kernel file does not exist.
    KeyError
        If required variables ('Mask_basinnumbers', 'area') are missing.
    """
    data = read_nc(file_path)

    if "Mask_basinnumbers" not in data or "area" not in data:
        message = "Kernel file must contain 'Mask_basinnumbers' and 'area' fields."
        logger.error(message)
        raise KeyError(message)

    basins = data["Mask_basinnumbers"]["value"]
    area = data["area"]["value"]

    if basins.shape != area.shape:
        message = "Mismatch between 'Mask_basinnumbers' and 'area' dimensions."
        logger.error(message)
        raise ValueError(message)

    unique_basins = np.unique(basins[~np.isnan(basins)])
    unique_basins = unique_basins[unique_basins > 0]

    basin_dict = {}
    for basin_num in unique_basins.astype(int):
        mask = basins == basin_num
        basin_dict[basin_num] = {"mask": mask, "area": area}

    return basin_dict


def parse_sinex_sections(path):
    """
    Parse SINEX file and identifies line indices of important sections.

    Args:
        path (str): Path to the SINEX file.

    Returns:
        dict: Dictionary of section names and their starting line numbers.
    """
    section_lines = {}
    with open(path, "r") as fi:
        for i, line in enumerate(fi):
            if "NUMBER OF UNKNOWNS" in line:
                section_lines['nou'] = int(float(line.strip().split()[-1]))
            if "+SOLUTION/APRIORI" in line:
                section_lines['apriori'] = i
            if "+SOLUTION/ESTIMATE" in line:
                section_lines['estimate'] = i
            if "+SOLUTION/NORMAL_EQUATION_VECTOR" in line:
                section_lines['neq_vector'] = i
            if "+SOLUTION/NORMAL_EQUATION_MATRIX" in line:
                section_lines['neq_matrix'] = i
        section_lines['total_lines'] = i + 1
    return section_lines


def read_sinex_data(logger: Logger, path: str, sections: dict):
    """
    Read relevant sections of a SINEX file into DataFrames.

    Args:
        path (str): Path to the SINEX file.
        sections (dict): Dictionary of section line indices. Mandatory keys: nou, total_lines

    Returns:
        data: dict containing DataFrames for all sections in sections
        (possible apriori, estimate, NEQM, mandatory nou=number of unknowns).
    """
    # Output dict
    data = {}
    # Read header
    header = read_sinex_header(path)
    try:
        line_dates = header['FILE/COMMENT']['time_period']
        start_str, end_str = line_dates.split('-')
        # Parse using year + day of year format
        start_date = dt.datetime.strptime(start_str, "%Y%j")
        end_date = dt.datetime.strptime(end_str, "%Y%j")
        date = start_date + (end_date - start_date) / 2
        data['date'] = date
    except ValueError:
        message = f'Sinex file {path} does not contain the date in the header.'
        logger.error(message)
        raise ValueError(message)

    try:
        data['max_degree'] = int(header['FILE/COMMENT']['max_degree'])
    except ValueError:
        message = f'Sinex file {path} does not contain the max Degree in the header.'
        logger.error(message)
        raise ValueError(message)

    nou = sections['nou']

    for section in sections:
        if section == 'neq_matrix':
            indices_to_skip = np.concatenate((
                np.arange(0, sections['neq_matrix'] + 2),
                [sections['total_lines'] - 3, sections['total_lines'] - 2, sections['total_lines'] - 1]
            ))
            data[section] = pd.read_csv(path,
                                        header=None,
                                        names=["PARA1", "PARA2", "PARA2+0", "PARA2+1", "PARA2+2"],
                                        delim_whitespace=True,
                                        skiprows=indices_to_skip)
        elif section == 'nou':
            data['nou'] = sections['nou']
        elif section == 'total_lines':
            continue
        else:
            data[section] = pd.read_csv(path,
                                        header=None,
                                        names=["index", "type", "degree", "pt", "order", "ref_epoch",
                                               "unit", "C", "value", "weight"],
                                        delim_whitespace=True,
                                        skiprows=sections[section] + 2,
                                        nrows=nou)

    logger.info("Finished reading SINEX file")
    return data


def read_sinex_header(filepath):
    """Read the Sinex File header."""
    header_data = {}
    current_section = None
    collecting = False
    buffer = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')

            # detect SINEX version line
            if line.startswith('%=SNX'):
                header_data['SNX_HEADER'] = line
                continue

            if line.startswith('+SOLUTION/ESTIMATE'):
                break

            # start of a section
            if line.startswith('+'):
                current_section = line[1:].strip()  # remove '+'
                collecting = True
                buffer = []
                continue

            # end of a section
            if line.startswith('-') and current_section:
                section_name = current_section
                header_data[section_name] = parse_sinex_header_section(section_name, buffer)
                current_section = None
                collecting = False
                continue

            # collect lines in section
            if collecting:
                # skip comment/header lines starting with '*'
                if not line.startswith('*'):
                    buffer.append(line.strip())

    return header_data


def parse_sinex_header_section(name, lines):
    """Parse key-value pairs or free-text sections."""
    section_data = {}

    # For FILE/REFERENCE → parse as key–value pairs
    if name == 'FILE/REFERENCE':
        for line in lines:
            # Expect "KEY   VALUE"
            parts = re.split(r'\s{2,}', line.strip(), maxsplit=1)
            if len(parts) == 2:
                key, val = parts
                section_data[key.strip()] = val.strip()

    # For FILE/COMMENT → store as text and key-values
    elif name == 'FILE/COMMENT':
        key_val_pattern = re.compile(r'(\w+)\s+(.+)')
        for line in lines:
            match = key_val_pattern.match(line)
            if match:
                section_data[match.group(1)] = match.group(2)
            else:
                section_data.setdefault('comments', []).append(line)
        if 'comments' in section_data:
            section_data['comments'] = '\n'.join(section_data['comments'])

    # For SOLUTION/STATISTICS → parse numeric values
    elif name == 'SOLUTION/STATISTICS':
        for line in lines:
            parts = re.split(r'\s{2,}', line.strip(), maxsplit=1)
            if len(parts) == 2:
                key, val = parts
                try:
                    section_data[key.strip()] = float(val.strip())
                except ValueError:
                    section_data[key.strip()] = val.strip()

    # Otherwise, just return as raw lines
    else:
        section_data['raw'] = lines

    return section_data
