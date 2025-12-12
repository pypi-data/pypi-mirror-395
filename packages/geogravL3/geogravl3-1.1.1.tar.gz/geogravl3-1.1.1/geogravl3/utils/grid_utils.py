# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Grid utils module."""

from logging import Logger
from typing import Union

import numpy as np
from scipy.spatial import cKDTree

from .utils import get_constant
from ..datamodels.grids import Grid2DObject, Grid3DObject


def standardize_lat_lon_grid(logger=Logger,
                             longitudes=None,
                             latitudes=None,
                             grid: Union[Grid2DObject, Grid3DObject, None] = None,
                             target_lon_format: str = "[-180, 180]",
                             target_lat_order: str = "ascending"
                             ):
    """
    Check and reformat longitude, latitude, and optionally associated grids.

    This function supports Grid2DObject (lat, lon) and Grid3DObject (time, lat, lon) and ensures their
    longitude and latitude definitions follow the desired conventions.

    Parameters
    ----------
    logger: Logger, logger object to log the error messages
    longitudes : array-like
    1D array of longitude values (can be in 0–360 or -180–180 format)
    latitudes : array-like
    1D array of latitude values (can be in 90 to -90 or -90 to 90 format)
    grid : Grid2DObject or Grid3DObject, optional
    The grid of values aligned with lat/lon. If None, only coordinates are standardized.
    target_lon_format : str, optional
    Desired longitude format: "[-180, 180]" (default) or "[0, 360]"
    target_lat_order : str, optional
    Desired latitude order:
    - "ascending" → from -90 to 90 (default)
    - "descending" → from 90 to -90

    Returns
    -------
    tuple
        If grid is None:
            (longitudes_fixed, latitudes_fixed)
        If grid is Grid2DObject:
            Grid2DObject with updated coords and grid
        If grid is Grid3DObject:
            Grid3DObject with updated coords and grid

    Notes
    -----
    - Longitude values are wrapped if needed to match the target format.
    - Grid is rearranged accordingly along longitude and/or latitude axes.
    - Latitude arrays are flipped if their order does not match the target.

    """
    longitudes = np.array(longitudes)
    latitudes = np.array(latitudes)

    grid_fixed = None
    dates = None
    if isinstance(grid, Grid2DObject):
        grid_fixed = np.array(grid.grid)
    elif isinstance(grid, Grid3DObject):
        grid_fixed = np.array(grid.grid)
        dates = grid.dates

    # --- Fix longitude range ---
    if target_lon_format == "[0, 360]":
        longitudes_fixed = np.mod(longitudes, 360)
    elif target_lon_format == "[-180, 180]":
        longitudes_fixed = ((longitudes + 180) % 360) - 180
    else:
        message = "Invalid target_lon_format. Use '[0, 360]' or '[-180, 180]'."
        logger.error(message)
        raise ValueError(message)

    # Sort longitudes and rearrange grid accordingly
    sort_idx = np.argsort(longitudes_fixed)
    longitudes_fixed = longitudes_fixed[sort_idx]
    if grid_fixed is not None:
        if grid_fixed.ndim == 2:
            grid_fixed = grid_fixed[:, sort_idx]
        elif grid_fixed.ndim == 3:
            grid_fixed = grid_fixed[:, :, sort_idx]

    # --- Fix latitude order ---
    lat_is_descending = latitudes[0] > latitudes[-1]
    if target_lat_order == "ascending" and lat_is_descending:
        latitudes_fixed = np.flip(latitudes, axis=0)
        if grid_fixed is not None:
            grid_fixed = np.flip(grid_fixed, axis=1 if grid_fixed.ndim == 3 else 0)
    elif target_lat_order == "descending" and not lat_is_descending:
        latitudes_fixed = np.flip(latitudes, axis=0)
        if grid_fixed is not None:
            grid_fixed = np.flip(grid_fixed, axis=1 if grid_fixed.ndim == 3 else 0)
    else:
        latitudes_fixed = latitudes

    # --- Return result ---
    if grid is None:
        return longitudes_fixed, latitudes_fixed
    if isinstance(grid, Grid2DObject):
        return Grid2DObject(logger, grid_fixed, longitudes_fixed, latitudes_fixed)
    if isinstance(grid, Grid3DObject):
        return Grid3DObject(logger, grid_fixed, dates, longitudes_fixed, latitudes_fixed)
    message = "grid must be Grid2DObject, Grid3DObject, or None"
    logger.error(message)
    raise TypeError(message)


def land_ocean_mask_buffer(logger: Logger, lo_mask: Grid2DObject, buffer: float) -> Grid2DObject:
    """
    Produce buffered land-ocean mask.

    Parameters
    ----------
    logger: Logger, logger object to log the error messages
    lo_mask (Grid2DObject): Mask of the land (1 or True) and ocean (0 or False)
    buffer (float): Buffer (in km) around the coast, >=0

    Returns
    -------
    lo_masked_buffered (Grid2DObject): Land ocean mask with extended land of buffer size,
                                       land (1 or True) and ocean (0 or False)

    """
    if buffer < 0:
        message = f'Buffer set to {buffer}, but needs to be >=0.'
        logger.error(message)
        raise ValueError(message)

    # --- Prepare coordinate mesh ---
    lon2d, lat2d = np.meshgrid(lo_mask.lon, lo_mask.lat)

    # --- Extract land and ocean coordinates ---
    land_idx = np.where(lo_mask.grid == 1)
    ocean_idx = np.where(lo_mask.grid == 0)
    land_points = np.column_stack((lat2d[land_idx], lon2d[land_idx]))
    ocean_points = np.column_stack((lat2d[ocean_idx], lon2d[ocean_idx]))

    # --- Convert to 3D Cartesian coordinates (for great-circle distance) ---
    R = get_constant('earths_radius_iers') / 1000  # Earth radius in km

    def _sph2xyz(lat, lon):
        deg2rad = get_constant('deg_2_rad')
        lat, lon = lat * deg2rad, lon * deg2rad
        x = R * np.cos(lat) * np.cos(lon)
        y = R * np.cos(lat) * np.sin(lon)
        z = R * np.sin(lat)
        return np.column_stack((x, y, z))

    land_xyz = _sph2xyz(land_points[:, 0], land_points[:, 1])
    ocean_xyz = _sph2xyz(ocean_points[:, 0], ocean_points[:, 1])

    # --- Build KD-tree for land points in 3D space ---
    tree = cKDTree(land_xyz)

    # --- Query nearest land distance for each ocean point ---
    distances, _ = tree.query(ocean_xyz, k=1)

    # Convert chord distance (in km) to surface distance
    # (Great-circle distance = 2 * R * asin(chord/(2R)))
    great_circle_km = 2 * R * np.arcsin(np.clip(distances / (2 * R), 0, 1))

    # --- Define buffer width ---
    ocean_near_land = great_circle_km <= buffer

    # --- Create buffered mask ---
    lo_masked_buffered = lo_mask.copy(deep=True)
    lo_masked_buffered.grid[ocean_idx[0][ocean_near_land], ocean_idx[1][ocean_near_land]] = 1

    return lo_masked_buffered


def global_weighted_sum(grid: Grid2DObject,
                        radius: float = None) -> float:
    """
    Compute the global area weighted sum of input grid.

    Parameters
    ----------
    grid (Grid2DObject: Grid which is summed up weighted by area
    radius (float): Reference radius to use with the area function. Default set to earths_radius from constants

    Returns
    -------
    weighted sum (float)
    """
    if radius is None:
        radius = get_constant('earths_radius_iers')
    area = grid.get_grid_area(radius)
    weighted_sum = np.nansum(area * grid.grid)
    return weighted_sum
