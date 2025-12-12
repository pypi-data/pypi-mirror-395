# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Writers for specific NetCDF products (TWS, OBP, ICE)."""

from __future__ import annotations
import csv
from datetime import date
from typing import Any, Sequence
from logging import Logger

import numpy as np
from netCDF4 import Dataset

from ..datamodels.grids import Grid3DObject, Grid3DIceObject
from ..utils.date_utils import dates_to_days_since_ref


def write_nc(
    filename: str,
    dimensions: list[np.ndarray],
    dimension_names: list[str],
    dimension_units: list[str],
    variables: list[np.ndarray],
    variable_names: list[str],
    variable_units: list[str],
    variable_dimensions: list[list[str]],
) -> None:
    """
    Save any generic netcdf file.

    Parameters
    ----------
    filename: str, filename of netcdf file
    dimensions: [np.ndarray], list of np.ndarray, each containing the values of the dimensions
    dimension_names: [str], list of dimension names
    dimension_units: [str], list of dimension units
    variables: [np.ndarray], list of np.ndarray, each containing the values of the variables
    variable_names: [str], list of variable names
    variable_units: [str], list of variable units
    variable_dimensions: [[str]], list containing a list for each variable, which contains the names of the dimensions
    """
    # Open a new NetCDF file for writing
    with Dataset(filename, "w", format="NETCDF4") as nc_file:
        # Define dimensions
        dim_map = {}
        for dim_name, dim_data, dim_unit in zip(dimension_names, dimensions, dimension_units):
            dim_length = len(dim_data)
            nc_file.createDimension(dim_name, dim_length)
            dim_var = nc_file.createVariable(dim_name, dim_data.dtype, (dim_name,))
            dim_var[:] = dim_data
            dim_var.units = dim_unit
            dim_map[dim_name] = dim_var

        # Define variables
        for var_name, var_data, var_unit, var_dims in zip(
            variable_names, variables, variable_units, variable_dimensions
        ):
            var_dims_tuple = tuple(var_dims)
            var = nc_file.createVariable(var_name, var_data.dtype, var_dims_tuple)
            var[:] = var_data
            var.units = var_unit
    return


def write_tws_nc(logger: Logger, filename: str, tws: Grid3DObject, std_tws: Grid3DObject) -> None:
    """
    Write Terrestrial Water Storage (TWS) anomalies NetCDF file.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    filename : str
        Path for output NetCDF file.
    tws : Grid3DObject
        Grid3DObject containing terrestrial water storage anomalies.
    std_tws : Grid3DObject
        Grid3DObject containing standard deviations.

    Raises
    ------
    ValueError
        If tws and std_tws do not have the same shape.
    """
    if tws.grid.shape != std_tws.grid.shape:
        message = "tws and std_tws must have the same shape."
        logger.error(message)
        raise ValueError(message)

    time_days = dates_to_days_since_ref(tws.dates)

    with Dataset(filename, "w", format="NETCDF4") as nc:
        # ----------------
        # Dimensions
        # ----------------
        nc.createDimension("time", tws.ntime)
        nc.createDimension("lon", tws.nlon)
        nc.createDimension("lat", tws.nlat)

        # ----------------
        # Time variable
        # ----------------
        time_var = nc.createVariable("time", "f8", ("time",))
        time_var[:] = time_days
        time_var.standard_name = "time"
        time_var.units = "days since 2002-4-18 00:00:00"
        time_var.calendar = "proleptic_gregorian"
        time_var.axis = "T"

        # ----------------
        # Lon / Lat
        # ----------------
        lon_var = nc.createVariable("lon", "f4", ("lon",))
        lon_var[:] = tws.lon
        lon_var.standard_name = "longitude"
        lon_var.long_name = "longitude"
        lon_var.units = "degrees_east"
        lon_var.axis = "X"

        lat_var = nc.createVariable("lat", "f4", ("lat",))
        lat_var[:] = tws.lat
        lat_var.standard_name = "latitude"
        lat_var.long_name = "latitude"
        lat_var.units = "degrees_north"
        lat_var.axis = "Y"

        # ----------------
        # Data variables
        # ----------------
        v1 = nc.createVariable("tws", "f8", ("time", "lat", "lon"), fill_value=-9e33)
        v1[:] = tws.grid
        v1.standard_name = "terrestrial_water_storage"
        v1.long_name = "gravity-based terrestrial water storage"
        v1.units = "mm"
        v1.missing_value = -9e33

        v2 = nc.createVariable("std_tws", "f8", ("time", "lat", "lon"), fill_value=-9e33)
        v2[:] = std_tws.grid
        v2.standard_name = "std_terrestrial_water_storage"
        v2.long_name = "gravity-based terrestrial water storage standard deviations"
        v2.units = "mm"
        v2.missing_value = -9e33

        # ----------------
        # Global attributes
        # ----------------
        nc.title = "Globally Gridded Terrestrial Water Storage Anomalies"
        nc.institution = (
            "GFZ Helmholtz Centre for Geosciences, Potsdam, Germany, "
            "Section 1.3: Earth System Modelling"
        )


def write_obp_nc(
    logger: Logger,
    filename: str,
    barslv: Grid3DObject,
    std_barslv: Grid3DObject,
    resobp: Grid3DObject,
    std_resobp: Grid3DObject,
) -> None:
    """
    Write Ocean Bottom Pressure (OBP) anomalies NetCDF file.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    filename : str
        Path to output NetCDF file.
    barslv : Grid3DObject
        Barystatic sea-level pressure.
    std_barslv : Grid3DObject
        Uncertainties of barystatic sea-level pressure.
    resobp : Grid3DObject
        Residual ocean circulation bottom pressure.
    std_resobp : Grid3DObject
        Uncertainties of residual ocean circulation bottom pressure.

    Raises
    ------
    ValueError
        If any of the input objects do not have the same shape.
    """
    # ----------------
    # Validation
    # ----------------
    shapes = [barslv.grid.shape, std_barslv.grid.shape, resobp.grid.shape, std_resobp.grid.shape]
    if not all(s == shapes[0] for s in shapes):
        message = "barslv, std_barslv, resobp, and std_resobp must have the same shape."
        logger.error(message)
        raise ValueError(message)

    time_days = dates_to_days_since_ref(barslv.dates)

    with Dataset(filename, "w", format="NETCDF4") as nc:
        # Dimensions
        nc.createDimension("time", barslv.ntime)
        nc.createDimension("lon", barslv.nlon)
        nc.createDimension("lat", barslv.nlat)

        # Time
        time_var = nc.createVariable("time", "f8", ("time",))
        time_var[:] = time_days
        time_var.standard_name = "time"
        time_var.units = "days since 2002-4-18 00:00:00"
        time_var.calendar = "proleptic_gregorian"
        time_var.axis = "T"

        # Lon
        lon_var = nc.createVariable("lon", "f8", ("lon",))
        lon_var[:] = barslv.lon
        lon_var.standard_name = "longitude"
        lon_var.long_name = "Longitude"
        lon_var.units = "degrees_east"
        lon_var.axis = "X"

        # Lat
        lat_var = nc.createVariable("lat", "f8", ("lat",))
        lat_var[:] = barslv.lat
        lat_var.standard_name = "latitude"
        lat_var.long_name = "Latitude"
        lat_var.units = "degrees_north"
        lat_var.axis = "Y"

        # Barslv
        v1 = nc.createVariable("barslv", "f8", ("time", "lat", "lon"), fill_value=-9e33)
        v1[:] = barslv.grid
        v1.standard_name = "barystatic_sealevel_pressure"
        v1.long_name = "gravity-based barystatic sea-level pressure"
        v1.units = "hPa"
        v1.missing_value = -9e33

        # Std Barslv
        v2 = nc.createVariable("std_barslv", "f8", ("time", "lat", "lon"), fill_value=-9e33)
        v2[:] = std_barslv.grid
        v2.standard_name = "std_barystatic_sealevel_pressure"
        v2.long_name = "gravity-based barystatic sea-level pressure uncertainties"
        v2.units = "hPa"
        v2.missing_value = -9e33

        # ResOBP
        v3 = nc.createVariable("resobp", "f8", ("time", "lat", "lon"), fill_value=-9e33)
        v3[:] = resobp.grid
        v3.standard_name = "residual_ocean_circulation_pressure"
        v3.long_name = "gravity-based residual ocean circulation bottom pressure"
        v3.units = "hPa"
        v3.missing_value = -9e33

        # Std ResOBP
        v4 = nc.createVariable("std_resobp", "f8", ("time", "lat", "lon"), fill_value=-9e33)
        v4[:] = std_resobp.grid
        v4.standard_name = "std_residual_ocean_circulation_pressure"
        v4.long_name = "gravity-based ocean circulation residual bottom pressure uncertainties"
        v4.units = "hPa"
        v4.missing_value = -9e33

        # Global attributes
        nc.title = "Globally Gridded Ocean Bottom Pressure Anomalies"
        nc.institution = (
            "GFZ Helmholtz Centre for Geosciences, Potsdam, Germany, "
            "Section 1.3: Earth System Modelling"
        )


def write_ice_nc(filename: str, dm: Grid3DIceObject, std_dm: Grid3DIceObject) -> None:
    """
    Write Gridded GIS Mass Changes (Ice) NetCDF file.

    Parameters
    ----------
    filename : str
        Path to output NetCDF file.
    dm : Grid3DIceObject
        Grid3DIceObject containing change in ice mass, coordinates, and projection info.
    std_dm : Grid3DIceObject
        Grid3DIceObject containing std of change in ice mass, coordinates, and projection info.

    """
    time_days = dates_to_days_since_ref(dm.dates)

    with Dataset(filename, "w", format="NETCDF4") as nc:
        # ----------------
        # Dimensions
        # ----------------
        nc.createDimension("time", dm.ntime)
        nc.createDimension("x", dm.nx)
        nc.createDimension("y", dm.ny)

        # ----------------
        # Coordinates
        # ----------------
        x_var = nc.createVariable("x", "f8", ("x",))
        x_var[:] = dm.x
        x_var.long_name = "x-coordinate"
        x_var.standard_name = "projection_x_coordinate"
        x_var.units = "m"
        x_var.axis = "X"

        y_var = nc.createVariable("y", "f8", ("y",))
        y_var[:] = dm.y
        y_var.long_name = "y-coordinate"
        y_var.standard_name = "projection_y_coordinate"
        y_var.units = "m"
        y_var.axis = "Y"

        time_var = nc.createVariable("time", "f8", ("time",))
        time_var[:] = time_days
        time_var.long_name = "modified julian date"
        time_var.standard_name = "time"
        time_var.units = "days since 2002-04-18"
        time_var.axis = "T"

        lon_var = nc.createVariable("lon", "f8", ("y", "x"))
        lon_var[:] = dm.lon
        lon_var.long_name = "longitude"
        lon_var.units = "degrees_east"

        lat_var = nc.createVariable("lat", "f8", ("y", "x"))
        lat_var[:] = dm.lat
        lat_var.long_name = "latitude"
        lat_var.units = "degrees_north"

        # ----------------
        # Data variables
        # ----------------
        dm_var = nc.createVariable("dm", "f8", ("time", "y", "x"), fill_value=-9e33)
        dm_var[:] = dm.grid
        dm_var.long_name = "change in ice mass"
        dm_var.units = "kg/m^2"

        area_var = nc.createVariable("area", "f8", ("time", "y", "x"), fill_value=-9e33)
        area_var[:] = dm.area
        area_var.long_name = "grid cell area on the ellipsoid"
        area_var.units = "m^2"

        std_dm_var = nc.createVariable("std_dm", "f8", ("time", "y", "x"), fill_value=-9e33)
        std_dm_var[:] = std_dm.grid
        std_dm_var.long_name = "change in ice mass"
        std_dm_var.units = "kg/m^2"

        # ----------------
        # CRS (from dm.projection dict)
        # ----------------
        crs = nc.createVariable("crs", "c")
        for key, value in dm.projection.items():
            setattr(crs, key, value)

        # ----------------
        # Global attributes
        # ----------------
        nc.title = "Gridded GIS Mass Changes"
        nc.institution = (
            "TU Dresden, Chair of Geodetic Earth System Research and "
            "GFZ Helmholtz Centre for Geosciences, Potsdam, Germany, "
            "Section 1.3: Earth System Modelling"
        )


def save_timeseries_to_csv(
    means_dict: dict[str, np.ndarray],
    stds_dict: dict[str, np.ndarray],
    dates: Sequence[Any],
    file_path: str,
) -> None:
    """
    Save mean and standard deviation time series of multiple regions to a CSV file.

    Parameters
    ----------
    means_dict : dict[str, np.ndarray]
        Regional mean values keyed by region name.
    stds_dict : dict[str, np.ndarray]
        Regional std values keyed by region name.
    dates : sequence of datetime.date or datetime64
        Dates corresponding to time steps.
    file_path : str
        Output CSV file path.

    Returns
    -------
    None
    """
    # Collect all region names
    mean_regions = list(means_dict.keys())
    std_regions = list(stds_dict.keys())

    header = ["date"]
    header += [f"{r}_mean" for r in mean_regions]
    header += [f"{r}_std" for r in std_regions]

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for idx, d in enumerate(dates):
            # Convert datetime/date to ISO string
            date_str = d.isoformat() if isinstance(d, date) else str(d)
            row = [date_str]
            row += [means_dict[r][idx] for r in mean_regions]
            row += [stds_dict[r][idx] for r in std_regions]
            writer.writerow(row)


def save_ice_timeseries_to_csv(
    mean_dict: dict[int, np.ndarray],
    std_dict: dict[int, np.ndarray],
    dates: Sequence[Any],
    file_path: str,
) -> None:
    """
    Save basin-wise ice mean and standard deviation time series to a CSV file.

    Parameters
    ----------
    mean_dict : dict[int, np.ndarray]
        Basin mean values keyed by basin number.
    std_dict : dict[int, np.ndarray]
        Basin standard deviation values keyed by basin number.
    dates : Sequence[Any]
        List or array of datetime.date or string date objects.
    file_path : str
        Path where the CSV file should be written.

    Returns
    -------
    None
    """
    mean_basins = sorted(mean_dict.keys())
    std_basins = sorted(std_dict.keys())

    header = ["date"]
    header += [f"basin_{b}_mean" for b in mean_basins]
    header += [f"basin_{b}_std" for b in std_basins]

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for i, d in enumerate(dates):
            date_str = d.isoformat() if hasattr(d, "isoformat") else str(d)
            row = [date_str]
            row += [mean_dict[b][i] for b in mean_basins]
            row += [std_dict[b][i] for b in std_basins]
            writer.writerow(row)
