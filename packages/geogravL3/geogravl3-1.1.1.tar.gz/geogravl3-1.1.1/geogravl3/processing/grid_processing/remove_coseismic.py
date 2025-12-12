#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Remove coseismic functions for geogravL3 package."""
import os
from datetime import datetime, timedelta
from logging import Logger
from typing import Tuple, List

import numpy as np
from scipy.ndimage import convolve

from geogravl3.config import path_resources
from geogravl3.datamodels.grids import Grid3DObject
from geogravl3.io.readers import parse_eqfile


def remove_coseismic_signal(
        logger: Logger,
        grid: Grid3DObject,
        eqfile: str,
        addzone: float = 3.0,
) -> Grid3DObject:
    """
    Empirically estimate and remove the co-seismic signal from a TWS time series.

    Inputs
    ------
    grid : Grid3DObject
        Input grid; 'grid.grid' is interpreted as TWS with shape (time, lat, lon).
        'grid.dates' are the timestamps (datetime.date / datetime / np.datetime64 / str).
        'grid.lat' (lat), 'grid.lon' (lon) are 1D coordinates.
    eqfile : str
        Path to earthquake ASCII file (same structure as the original script).
    addzone : float, default=3.0
        Extend the event box by this many degrees.

    Output
    ------
    Grid3DObject
        A copy of the input with 'grid' replaced by the adjusted TWS.

    Raises
    ------
    ValueError
        If addzone is negative.
    """
    if addzone < 0:
        message = "addzone must be positive."
        logger.error(message)
        raise ValueError(message)
    # --- Resolve earthquake definition
    eqdef = parse_eqfile(logger=logger, eqfile=eqfile)

    # --- Extract arrays
    grid_data = grid.grid
    lat = grid.lat
    lon = grid.lon
    if isinstance(grid.dates[0], datetime):
        time = np.array([d.date() for d in grid.dates])
    else:
        time = grid.dates

    # --- Time-mean removal (anomaly)
    grid_data_mean = np.nanmean(grid_data, axis=0, keepdims=True)  # (1, lat, lon)
    gsma = grid_data - grid_data_mean  # (time, lat, lon)

    # --- Event box (+ padding)
    lat1 = eqdef.epi_lat - eqdef.del_lat - addzone
    lat2 = eqdef.epi_lat + eqdef.del_lat + addzone
    lon1 = eqdef.epi_lon - eqdef.del_lon - addzone
    lon2 = eqdef.epi_lon + eqdef.del_lon + addzone
    mask_box = box_mask(lat=lat, lon=lon, lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2)

    # --- Daily vs monthly detection (same logic as original)
    pre_y, pre_m = eqdef.pre_year, eqdef.pre_month
    aft_y, aft_m = eqdef.aft_year, eqdef.aft_month
    # Get last day of the pre-event month and first day of the post-event month
    py, pm, pd = last_of_month(y=pre_y, m=pre_m)
    pre_last_day = datetime(year=py, month=pm, day=pd).date()
    aft_first_day = datetime(year=aft_y, month=aft_m, day=1).date()
    # Count how many timestamps fall between those two dates
    num_points_in_range = np.sum((time >= pre_last_day) & (time <= aft_first_day))

    # If more than one date fits in that range → daily data, otherwise monthly
    if num_points_in_range > 1:
        sampling = "daily"
    else:
        sampling = "monthly"

    # Event-adjacent bounds
    eve = datetime(year=eqdef.eve_year, month=eqdef.eve_month, day=eqdef.eve_day).date()
    if sampling == "daily":
        pre_dt = eve - np.timedelta64(1, "D")
        aft_dt = eve + np.timedelta64(1, "D")
    else:
        # monthly: previous month's last day, next month's first day
        pm_y, pm_m = (eqdef.eve_year, eqdef.eve_month - 1) if eqdef.eve_month > 1 else (eqdef.eve_year - 1, 12)
        y2, m2, d2 = last_of_month(y=pm_y, m=pm_m)
        pre_dt = datetime(year=y2, month=m2, day=d2).date()
        y3, m3, d3 = first_of_next_month(y=eqdef.eve_year, m=eqdef.eve_month)
        aft_dt = datetime(year=y3, month=m3, day=d3).date()

    # --- Pre/Post spatial means (anomalies) in wide windows like the script
    pre_sel = (time >= datetime(year=2000, month=1, day=1).date()) & (time <= pre_dt)
    pst_sel = (time >= aft_dt) & (time <= datetime(year=2100, month=12, day=31).date())
    if not pre_sel.any():
        message = f"No time steps found before the event window. Earthquake {eqfile} not corrected."
        logger.warning(message)
        return grid
    if not pst_sel.any():
        message = f"No time steps found after the event window. Earthquake {eqfile} not corrected."
        logger.warning(message)
        return grid

    preco = np.nanmean(gsma[pre_sel, :, :], axis=0)  # (lat, lon)
    pstco = np.nanmean(gsma[pst_sel, :, :], axis=0)  # (lat, lon)

    # Apply geographic box (outside -> 0) and smooth edges
    prebox = preco * mask_box
    pstbox = pstco * mask_box
    presig = smooth(field_2d=prebox, passes=2)
    pstsig = smooth(field_2d=pstbox, passes=2)

    # Build adjusted series
    out = grid_data.copy()

    # subtract presig before event
    pre_mask = time < pre_dt
    out[pre_mask] -= presig

    # subtract partial signal at the event epoch(s)
    if sampling == "daily":
        parsig = 0.5 * (presig + pstsig)
        event_mask = (time == eve)
    else:
        facpre = eqdef.eve_day  # fixed 31-day logic as in the script
        facpst = 31 - eqdef.eve_day
        parsig = (facpre * presig + facpst * pstsig) / 31.0
        event_mask = (time >= pre_dt) & (time <= aft_dt)

    out[event_mask] -= parsig

    # subtract pstsig after event
    post_mask = time > aft_dt
    out[post_mask] -= pstsig

    # --- Return a new Grid3DObject with the adjusted grid
    adjusted = Grid3DObject(
        logger=logger,
        grid=out,
        dates=np.array(grid.dates, copy=True),
        lon=np.array(grid.lon, copy=True),
        lat=np.array(grid.lat, copy=True),
    )

    return adjusted


def box_mask(lat: np.ndarray, lon: np.ndarray, lat1: float, lat2: float, lon1: float, lon2: float) -> np.ndarray:
    """
    Create a geographical mask for a defined latitude and longitude box.

    This function generates a mask array where the specific region defined by latitude
    and longitude boundaries is marked, combining latitude and longitude masks.
    The output mask can be useful for extracting or filtering data within a
    certain spatial boundary.

    Args:
        lat (np.ndarray): Latitude values as a NumPy array.
        lon (np.ndarray): Longitude values as a NumPy array.
        lat1 (float): Lower latitude bound in degrees.
        lat2 (float): Upper latitude bound in degrees.
        lon1 (float): Lower longitude bound in degrees.
        lon2 (float): Upper longitude bound in degrees.

    Returns:
        np.ndarray: A 2D NumPy array where elements represent the geographical mask
                    for the given latitude and longitude box.
    """
    lat = np.asarray(lat, dtype=float)
    lo, hi = sorted([lat1, lat2])
    mlat = (lat >= lo) & (lat <= hi)
    lon = np.asarray(lon, dtype=float)
    mlon = in_lon_box(lon_vals=lon, lon1=lon1, lon2=lon2)

    return mlat[:, None].astype(float) * mlon[None, :].astype(float)


def in_lon_box(lon_vals: np.ndarray, lon1: float, lon2: float) -> np.ndarray:
    """
    Determine whether longitudes are inside a specified range, wrapping of longitude values within the range [0, 360).

    Parameters:
        lon_vals (np.ndarray): Array of longitude values to be checked.
        lon1 (float): Start of the longitude range (inclusive).
        lon2 (float): End of the longitude range (inclusive).

    Returns:
        np.ndarray: A boolean array where True indicates that the corresponding longitude value
        is within the specified range. Handles wrapping around the 0 to 360 longitude boundary.
    """
    x = (lon_vals % 360.0 + 360.0) % 360.0
    a = (lon1 % 360 + 360) % 360
    b = (lon2 % 360 + 360) % 360
    if a <= b:
        return (x >= a) & (x <= b)
    else:
        return (x >= a) | (x <= b)


def smooth(field_2d: np.ndarray, passes: int = 2) -> np.ndarray:
    """
    Smooth a 2D field by applying a 3x3 averaging filter for a specific number of passes.

    The function uses periodic boundary conditions
    along the longitudinal direction and ensures the input is converted
    to a float array before smoothing.

    Parameters:
    -----------
    field_2d: np.ndarray
    The 2D array to be smoothed.
    passes: int, default=2
    The number of smoothing passes to apply. If less than one, it is treated as one pass at a minimum.

    Returns:
    --------
    np.ndarray
    The smoothed 2D array after applying the specified number of passes.

    """
    g = np.asarray(field_2d, dtype=float)
    for _ in range(max(1, passes)):
        g = smooth9(g)
    return g


def smooth9(field_2d: np.ndarray) -> np.ndarray:
    """
    Smooth a 2D numerical field using a defined 3x3 kernel with NaN-aware processing.

    This function applies convolution to smooth the input data,
    while handling missing values (NaNs) sensibly to retain accuracy in the
    processed data.

    Parameters:
    field_2d: np.ndarray
    A 2D NumPy array containing numerical data. Missing values should be represented as NaN.

    Returns:
    np.ndarray
    A 2D NumPy array of the same shape as the input, with smoothed values after applying the kernel.
    Missing values are preserved as NaN.

    """
    mask = np.isfinite(field_2d)

    # Define the 3×3 kernel used by smooth9
    kernel = np.array([[0.3, 0.5, 0.3],
                       [0.5, 1, 0.5],
                       [0.3, 0.5, 0.3]], dtype=float)
    kernel /= kernel.sum()  # normalize to sum = 1

    # Apply convolution along lat/lon dimensions
    if field_2d.ndim == 3:
        kernel = kernel[None, :, :]

    # NaN aware smoothing
    numerator = convolve(np.nan_to_num(field_2d), kernel, mode="nearest")
    denominator = convolve(mask.astype(float), kernel, mode="nearest")

    smoothed = np.where(denominator > 0, numerator / denominator, np.nan)

    return smoothed


def last_of_month(y: int, m: int) -> Tuple[int, int, int]:
    """
    Calculate the last day of a given month and year.

    This function determines the last day of the specified month in the given year.
    It handles the transition between months and years, correctly computing the
    final day of the current month.

    Parameters:
    y: int
    The year for which the last day of the month is to be calculated.
    m: int
    The month (1-12) for which the last day is to be calculated.

    Returns:
    Tuple[int, int, int]
    A tuple containing the year, month, and the last day of the provided month.

    Raises:
    ValueError
    If the provided month is not in the valid range of 1 to 12.

    """
    if m not in range(1, 13):
        raise ValueError(f"Invalid month: {m}")
    if m == 12:
        return y, m, 31
    first_next = datetime(year=y + (m // 12), month=(m % 12) + 1, day=1)
    last = first_next - timedelta(days=1)
    return last.year, last.month, last.day


def first_of_next_month(y: int, m: int) -> Tuple[int, int, int]:
    """
    Calculate the date of the first day of the next month based on the given year and month.

    The function determines the next month and adjusts the year if the current month
    is December. It raises an exception if the provided month is not within the valid
    range of 1 to 12.

    Parameters:
    y (int): The year.
    m (int): The month (1-12).

    Returns:
    Tuple[int, int, int]: A tuple containing the following:
    - The year of the first day of the next month.
    - The month of the first day of the next month.
    - The day of the first day of the next month (always 1).

    Raises:
    ValueError: If the input month (m) is not in the range 1 to 12.

    """
    if m not in range(1, 13):
        raise ValueError(f"Invalid month: {m}")
    if m == 12:
        return y + 1, 1, 1
    return y, m + 1, 1


def get_eq_filenames(eq_years: List[str]) -> List[str]:
    """
    Return the filenames for the earthquakes specified by their year.

    Parameters
    ----------
    eq_years (List[str]): List collection the years of the earthquakes

    """
    if eq_years is None:
        return []
    folder_resources_eq = os.path.join(path_resources, 'earthquakes')
    year_to_filename = {'2004': os.path.join(folder_resources_eq, 'Sumatra-Andaman_2004.dat'),
                        '2010': os.path.join(folder_resources_eq, 'Maule-Chile_2010.dat'),
                        '2011': os.path.join(folder_resources_eq, 'Tohoku-Oki_2011.dat')}
    return [year_to_filename[year] for year in eq_years]
