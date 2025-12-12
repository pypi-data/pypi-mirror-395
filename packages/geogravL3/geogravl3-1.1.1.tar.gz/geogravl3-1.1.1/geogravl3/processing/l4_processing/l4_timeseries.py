#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam

"""Timeseries utilities: regional IO and aggregation functions."""
from logging import Logger
from typing import Any, Union

import numpy as np
from shapely.geometry import Point, shape

from geogravl3.datamodels.grids import Grid2DObject, Grid3DObject, Grid3DIceObject
from geogravl3.processing.timeseries import (
    apply_harmonic_components_grid,
    FitConfig,
    gaussian_filter_grid
)


def compute_regional_timeseries(
    grid: Grid3DObject,
    regions: list[dict[str, Any]],
    precomputed_masks: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    """
    Compute area-weighted mean time series for each region.

    This function calculates the mean value of a 3D field (time × lat × lon)
    within each given region, weighted by the grid-cell area.

    Parameters
    ----------
    grid : Grid3DObject
        3D grid object with attributes:
        - grid (np.ndarray): data array with shape (ntime × nlat × nlon)
        - lat (np.ndarray): latitude array
        - lon (np.ndarray): longitude array
        - get_grid_area(): method returning the area of each grid cell
    regions : list[dict[str, Any]]
        List of region definitions, each containing:
        - "name": region identifier
        - "geometry": shapely Polygon or MultiPolygon defining the region.

    Returns
    -------
    dict[str, np.ndarray]
        Mapping of region name → time series of mean values.
    """
    ntime, nlat, nlon = grid.grid.shape
    areas = grid.get_grid_area()

    # ✅ Use precomputed masks if available, otherwise compute them here
    if precomputed_masks is not None:
        region_masks = precomputed_masks
    else:
        region_masks = precompute_region_masks(grid=grid, regions=regions)

    results = {}
    for region in regions:
        name = region["name"]
        mask = region_masks[name]  # Shapely geometry (Polygon or MultiPolygon)
        if not mask.any():
            results[name] = np.full(ntime, np.nan)
            continue

        masked_area = np.where(mask, areas, 0.0)
        wsum = np.nansum(masked_area)
        ts_mean = np.empty(ntime)

        for t in range(ntime):
            arr = np.where(mask, grid.grid[t], np.nan)
            ts_mean[t] = np.nansum(arr * masked_area) / wsum
        results[name] = ts_mean

    return results


def compute_regional_timeseries_std(
    grid: Grid3DObject,
    regions: list[dict[str, Any]],
    precomputed_masks: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    """
    Compute area-weighted propagated standard deviation time series for each region.

    For each region, this function computes the propagated uncertainty (standard deviation)
    over time using area weighting based on the grid-cell area.

    Parameters
    ----------
    grid : Grid3DObject
        3D grid object with attributes:
        - grid (np.ndarray): data array with shape (ntime × nlat × nlon)
        - lat (np.ndarray): latitude array
        - lon (np.ndarray): longitude array
        - get_grid_area(): method returning the area of each grid cell
    regions : list[dict[str, Any]]
        List of region definitions, each containing:
        - "name": region identifier
        - "geometry": shapely Polygon or MultiPolygon defining the region.
    precomputed_masks :  dict[str, np.ndarray] | None
        If provided, the region mask is not newly computed

    Returns
    -------
    dict[str, np.ndarray]
        Mapping of region name → time series of propagated standard deviation.
    """
    ntime, nlat, nlon = grid.grid.shape
    areas = grid.get_grid_area()

    # ✅ Use precomputed masks if available, otherwise compute them here
    if precomputed_masks is not None:
        region_masks = precomputed_masks
    else:
        region_masks = precompute_region_masks(grid=grid, regions=regions)

    results = {}

    for region in regions:
        name = region["name"]
        mask = region_masks[name]  # Shapely geometry
        if not mask.any():
            results[name] = np.full(ntime, np.nan)
            continue

        masked_area = np.where(mask, areas, 0.0)
        wsum = np.nansum(masked_area)
        ts_std = np.empty(ntime)
        for t in range(ntime):
            arr = np.where(mask, grid.grid[t], np.nan)
            var = np.nanvar(arr)
            ts_std[t] = np.sqrt(np.nansum((masked_area ** 2) * var) / (wsum ** 2))

        results[name] = ts_std

    return results


def compute_regional_ice_timeseries(
    grid: Grid3DIceObject,
    basin_dict: dict[int, dict[str, np.ndarray]],
) -> dict[int, np.ndarray]:
    """
    Compute area-weighted mean ice-mass time series for each basin.

    Parameters
    ----------
    grid : Grid3DIceObject
        3D ice grid object with:
        - grid (np.ndarray): data array (ntime × nlat × nlon)
        - dates (np.ndarray): corresponding time stamps
    basin_dict : dict[int, dict[str, np.ndarray]]
        Basin information returned by `read_ice_basins_from_kernel()`.
        Each entry must contain:
        - "mask": boolean 2D array defining the basins
        - "area": 2D array of cell areas.

    Returns
    -------
    dict[int, np.ndarray]
        Mapping of basin_number → mean time series (1D array of length ntime).

    """
    ntime = grid.grid.shape[0]
    results = {}

    for basin_id, info in basin_dict.items():
        mask = info["mask"]
        area = info["area"]

        if mask.shape != grid.grid.shape[1:]:
            raise ValueError(f"Mask for basin {basin_id} does not match grid dimensions.")

        masked_area = np.where(mask, area, 0.0)
        wsum = np.nansum(masked_area)
        if wsum == 0:
            results[basin_id] = np.full(ntime, np.nan)
            continue

        ts_mean = np.empty(ntime)
        for t in range(ntime):
            arr = np.where(mask, grid.grid[t], np.nan)
            ts_mean[t] = np.nansum(arr * masked_area) / wsum

        results[basin_id] = ts_mean

    return results


def compute_regional_ice_timeseries_std(
    logger: Logger,
    grid: Grid3DObject,
    basin_dict: dict[int, dict[str, np.ndarray]],
) -> dict[int, np.ndarray]:
    """
    Compute time-dependent standard deviations of the ice-mass field for each basin.

    This function removes deterministic temporal components (trend, annual, semiannual, etc.),
    applies Gaussian smoothing, and computes the time-dependent spatial standard deviation
    within each basin.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    grid : Grid3DObject
        Input 3D ice grid (ntime × nlat × nlon).
    basin_dict : dict[int, dict[str, np.ndarray]]
        Basin information from `read_ice_basins_from_kernel()`,
        containing "mask" (boolean 2D array) and "area" (2D array of grid-cell areas).

    Returns
    -------
    dict[int, np.ndarray]
        Mapping of basin_number → 1D array of std values per time step.
    """
    # 1. Remove deterministic components
    cfg = FitConfig(include_mean=True, trend=True, annual=True, semiannual=True, quadratic=True)
    residual_dict = apply_harmonic_components_grid(logger=logger, grid3d=grid, components=cfg)
    residual_grid = residual_dict["output"]

    # 2. Gaussian smoothing
    smoothed_grid = gaussian_filter_grid(logger=logger, grid3d=residual_grid, sigma=0.25, cutdist=0.75)

    ntime = smoothed_grid.grid.shape[0]
    results = {}

    for basin_id, info in basin_dict.items():
        mask = info["mask"]

        if mask.shape != smoothed_grid.grid.shape[1:]:
            raise ValueError(f"Mask for basin {basin_id} does not match grid dimensions.")

        ts_std = np.empty(ntime)
        for t in range(ntime):
            arr = np.where(mask, smoothed_grid.grid[t], np.nan)
            ts_std[t] = np.nanstd(arr)

        results[basin_id] = ts_std

    return results


def precompute_region_masks(
    grid: Union[Grid2DObject, Grid3DObject],
    regions: list[dict[str, Any]]
) -> dict[str, np.ndarray]:
    """
    Precompute boolean masks for each region.

    This function creates 2D boolean masks indicating which grid cells fall within
    each given region geometry. The masks can be used to accelerate subsequent
    computations (e.g., area-weighted means or standard deviations).

    Parameters
    ----------
    grid : Union[Grid2DObject, Grid3DObject]
        Grid object providing `.lat` and `.lon` arrays.
        Can be a 2D or 3D grid; only spatial coordinates are used.
    regions : list[dict[str, Any]]
        List of region definitions, each containing:
        - "name": region identifier
        - "geometry": shapely Polygon or MultiPolygon defining the region boundary.


    Returns
    -------
    dict[str, np.ndarray]
        Mapping of region name → boolean mask (nlat×nlon).
    """
    nlat, nlon = len(grid.lat), len(grid.lon)
    lon_grid, lat_grid = np.meshgrid(grid.lon, grid.lat)
    region_masks = {}

    for region in regions:
        geom = shape(region["geometry"])
        name = region["name"]

        mask = np.zeros((nlat, nlon), dtype=bool)
        for i in range(nlat):
            for j in range(nlon):
                if geom.contains(Point(lon_grid[i, j], lat_grid[i, j])):
                    mask[i, j] = True

        region_masks[name] = mask

    return region_masks
