# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Module to handle degree one terms."""

from logging import Logger
from typing import Any, List, Tuple

import numpy as np

from ..spherical_harmonics.legendre import legendre
from ..spherical_harmonics.sh_analysis import sh_analysis
from ...datamodels.grids import Grid2DObject
from ...datamodels.shc import SHObject
from ...processing.spherical_harmonics.sh_synthesis import sh_synthesis
from ...utils.grid_utils import land_ocean_mask_buffer
from ...utils.utils import get_constant


def estimate_degree1_sh(
    logger: Logger,
    sh_objects: list[SHObject],
    lomask: Grid2DObject,
    lmax: int,
    love_numbers: dict[str, float],
    n_it: int = 5,
    buf: int = 200,
) -> Tuple[List[SHObject], np.ndarray[tuple[int, float], np.dtype[Any]]]:
    """
    Estimates degree-1 spherical harmonics expansion for solid Earth geophysics applications.

    This function computes the degree-1 spherical harmonics expansion coefficients
    using the input spherical harmonic coefficients, love number information, and
    land-ocean mask data. It performs several matrix operations and iterative computations
    to arrive at the degree-1 coefficients. The output coefficients are used to model the
    Earth's water mass distribution and related geophysical parameters.

    Parameters:
        logger (Logger): A logging object used to record computation progress and debug information.
        sh_objects (SHObject): Input spherical harmonic coefficient matrix containing both
        cosine (C) and sine (S) terms for expansion up to a certain degree.
        lomask (Grid2DObject): A 2D grid object representing the land-ocean mask data, 1 for land, 0 for ocean.
        lmax (int): The maximum spherical harmonic degree included in the calculation.
        love_numbers (dict[str, float]): Dictionary containing Love numbers (e.g., 'k')
        instrumental in scaling spherical harmonic coefficients.
        n_it (int): Number of iterations for sequential refinement during computation
        Defaults to 5.
        buf (int): Buffer size used for calculating the land-ocean mask. Defaults to 200.

    Returns:
        np.ndarray: A NumPy array containing the refined degree-1 coefficients after
        all iterations. The coefficients are returned in terms of equivalent water height (EWH).

    """
    # constants:
    radius = get_constant("earths_radius_iers")
    density = get_constant("earths_density")
    density_water = get_constant("water_density")
    four_pi_rr = 4.0 * np.pi * radius ** 2

    k_lovenumber = np.asarray(love_numbers["k"])
    l_arr = np.arange(lmax + 1)
    f_ewh = (radius * density / 3.0) * (2 * l_arr + 1) / (1.0 + k_lovenumber[: lmax + 1])

    # Ocean mask selection and prep
    ocean_mask = land_ocean_mask_buffer(logger=logger, lo_mask=lomask, buffer=buf)
    ocean_mask.grid = np.where(ocean_mask.grid == 0, 1.0, 0.0)

    # Build oc_mask_coefficients
    oc_mask_shc = sh_analysis(logger=logger,
                              grid=ocean_mask.to_Grid3DObject(logger=logger, date=sh_objects[0].date),
                              n_max=lmax,
                              case='one',
                              love_numbers=love_numbers)
    oc_mask_shc = oc_mask_shc[0]

    # Ocean area
    oc_area = float(int_sphere(logger=logger, grid=ocean_mask, radius=radius))

    # Call synthesis (returns Grid3DObject)
    # Set deg 0 and deg 1 sh coefficients to 0
    sh_objects_deg1_to_0 = [
        SHObject(
            logger=logger,
            date=s.date,
            cnm=np.where(np.indices(s.cnm.shape)[0] < 2, 0, s.cnm),
            snm=np.where(np.indices(s.snm.shape)[0] < 2, 0, s.snm),
        )
        for s in sh_objects
    ]

    grid_obj = sh_synthesis(
        logger=logger,
        shc=sh_objects_deg1_to_0,
        gridinfo=ocean_mask.get_grid_info_dict(),
        love_numbers=love_numbers,
        n_max=lmax,
        case='ewh',
        ref_surface="spherical",
    )

    # Iterations
    cs1_ewh_eust = np.zeros((3, n_it), dtype=float)
    cs1_eust = np.zeros((3, n_it), dtype=float)

    corrected_shc = []
    cs1_eust_out = np.zeros((3, len(sh_objects)), dtype=float)

    # looping over time steps
    for timestep in range(len(grid_obj.dates)):

        cnm_data = sh_objects[timestep].cnm[:lmax + 1, :lmax + 1].copy()
        snm_data = sh_objects[timestep].snm[:lmax + 1, :lmax + 1].copy()

        l2b_cs2_ewh_cnm = f_ewh[:, None] * cnm_data
        l2b_cs2_ewh_snm = f_ewh[:, None] * snm_data
        temp_cnm = l2b_cs2_ewh_cnm.copy()
        temp_snm = l2b_cs2_ewh_snm.copy()

        # iterations
        for it in range(n_it):
            if it > 0:
                c10, c11, s11 = cs1_ewh_eust[:, it - 1]
                temp_cnm[1, 0] = float(c10)
                temp_cnm[1, 1] = float(c11)
                temp_snm[1, 1] = float(s11)

            oc_mass = four_pi_rr * float(
                np.sum(temp_cnm * oc_mask_shc.cnm[:lmax + 1, :lmax + 1]) +
                np.sum(temp_snm * oc_mask_shc.snm[:lmax + 1, :lmax + 1])
            )

            row = 1  # 0-based for MATLAB row 2
            c10_val = oc_mask_shc.cnm[row, 0] * oc_mass / oc_area
            c11_val = oc_mask_shc.cnm[row, 1] * oc_mass / oc_area
            s11_val = oc_mask_shc.snm[row, 1] * oc_mass / oc_area
            cs1_oc_eust_row = np.array([c10_val, c11_val, s11_val], dtype=float)

            d1 = degree_one_sw06(
                logger=logger,
                ocean_grid=ocean_mask,
                kappa=grid_obj.grid[timestep] * density_water,
                oc_n1=cs1_oc_eust_row,
            )

            cs1_ewh_eust[:, it] = np.asarray(d1, dtype=float).ravel()
            cs1_eust[:, it] = cs1_ewh_eust[:, it] / f_ewh[1]
        cs1_eust_out[:, timestep] = cs1_eust[:, -1]
        cnm = sh_objects[timestep].cnm
        cnm[1, 0] = cs1_eust[0, -1]
        cnm[1, 1] = cs1_eust[1, -1]
        snm = sh_objects[timestep].snm
        snm[1, 1] = cs1_eust[2, -1]
        corrected_shc.append(SHObject(logger=logger,
                                      date=sh_objects[timestep].date,
                                      cnm=cnm,
                                      snm=snm))
    return corrected_shc, cs1_eust_out


def int_sphere(logger: Logger, grid: Grid2DObject, radius: float) -> float:
    """
    Numerical integration on a sphere over a regular lon/lat grid.

    Parameters
    ----------
    logger: Logger
        Logger object
    grid : Grid2DObject
        Object containing grid, lat, lon information
    radius : float
        Sphere radius (same units as desired for area, e.g. meters or 1 for unit sphere)

    Returns
    -------
    float
        Integral over the sphere of `grid`.

    """
    lat = grid.lat
    lon = grid.lon
    area = grid.get_grid_area(radius=radius)
    grid = grid.grid

    nlat = lat.size
    nlon = lon.size

    if grid.shape != (nlat, nlon):
        message = "int_sphere: Func must be of size lat x lon!"
        logger.error(message)
        raise ValueError(message)

    # equally spaced checks (tolerant to tiny float noise)
    def _equally_spaced(x: np.ndarray) -> bool:
        if x.size < 2:
            return True
        d = np.diff(x)
        return np.allclose(d, d[0], rtol=0, atol=max(1e-12, 1e-9 * max(1.0, float(np.abs(d[0])))))

    message = "int_sphere: latitude vector must be equally spaced!"
    if not _equally_spaced(lat):
        logger.error(message)
        raise ValueError(message)
    message = "int_sphere: longitude vector must be equally spaced!"
    if not _equally_spaced(lon):
        logger.error(message)
        raise ValueError(message)

    # set NaNs to zero (MATLAB: grid(isnan)=0)
    grid = np.nan_to_num(grid, copy=False)

    # grid resolution (degrees)
    dlat = (lat.max() - lat.min()) / (nlat - 1) if nlat > 1 else 0.0

    # handle global grid wrap (0..360 or -180..180) -> drop the first column to avoid duplicate meridian
    int_cap = 0.0
    if nlon >= 2 and np.isclose(abs(lon[0] - lon[-1]), 360.0):
        grid = grid[:, 1:]
        area = area[:, 1:]
        lon = lon[1:]
        nlon = lon.size

    # polar cap handling (gridline registration: pole exactly present)
    if nlat >= 1 and (np.isclose(abs(lat[0]), 90.0) or np.isclose(abs(lat[-1]), 90.0)):
        # warn if pole row values differ
        if np.isclose(abs(lat[0]), 90.0) and not np.allclose(grid[0, :], grid[0, 0]):
            logger.warning(
                "int_sphere: Grid seems to include the pole, but the grid values at the pole differ!"
            )
        if np.isclose(abs(lat[-1]), 90.0) and not np.allclose(grid[-1, :], grid[-1, 0]):
            logger.warning(
                "int_sphere: Grid seems to include the pole, but the grid values at the pole differ!"
            )

        # spherical cap area using cap height for half-lat spacing
        h = radius * (1.0 - np.cos(np.deg2rad(dlat / 2.0)))
        area_cap = 2.0 * np.pi * radius * h  # 2πR h

        if np.isclose(abs(lat[0]), 90.0):
            int_cap += grid[0, 0] * area_cap
            grid = grid[1:, :]
            area = area[1:, :]
            lat = lat[1:]
            nlat = lat.size

        if nlat > 0 and np.isclose(abs(lat[-1]), 90.0):
            int_cap += grid[-1, 0] * area_cap
            grid = grid[:-1, :]
            area = area[:-1, :]
            lat = lat[:-1]
            nlat = lat.size

    if nlat == 0 or nlon == 0:
        # nothing left but possibly caps
        return float(int_cap)

    integral = np.sum(grid * area) + int_cap
    return float(integral)


def degree_one_sw06(logger: Logger, ocean_grid: Grid2DObject, kappa: np.ndarray, oc_n1: np.ndarray) \
        -> np.ndarray:
    """
    Swenson & Wahr (2006) degree-1 solution using a grid and an ocean mask.

    Parameters
    ----------
    logger : Logger
    ocean_grid : Grid2DObject
    Must provide attributes:
    - grid: (nlat, nlon) array-like, ocean mask (0/1 or weights)
    - lat: latitudes in degrees, equally spaced
    - lon: longitudes in degrees, equally spaced
    kappa: (nlat, nlon) np.ndarray
    Surface mass change field [kg/m^2]. (Degree-1 must be excluded in its synthesis.)
    oc_n1: np.ndarray
    Degree-1 surface mass coefficients of the ocean [kg/m^2], ordered
    [g_deg1_order0_cos, g_deg1_order1_cos, g_deg1_order1_sin].

    Returns
    -------
    degree1_coefficients: np.ndarray
        Estimated degree-1 surface mass coefficients [kg/m^2] (g_deg1_order0_cos, g_deg1_order1_cos, g_deg1_order1_sin).

    """
    oc_mask = ocean_grid.grid
    lat = ocean_grid.lat
    lon = ocean_grid.lon

    nlat, nlon = oc_mask.shape
    if kappa.shape != (nlat, nlon):
        message = "degree_one_sw06: kappa must match oc_mask (lat x lon)."
        logger.error(message)
        raise ValueError(message)

    oc_n1 = np.asarray(oc_n1, dtype=float).reshape(-1)
    if oc_n1.size != 3:
        message = "degree_one_sw06: oc_n1 must be length 3 (g_deg1_order0_cos, g_deg1_order1_cos, g_deg1_order1_sin)."
        logger.error(message)
        raise ValueError(message)

    # --- Legendre functions (fully normalized) for l=1
    # legendre() expects sin(latitude) values:
    sin_lat = np.sin(np.deg2rad(lat))  # shape (nlat,)
    polynomials = legendre(logger=logger, lmax=1, lat_rows=nlat, sin_lat=sin_lat)  # shape (2,2,nlat)
    # Extract degree-1, m=0 and m=1 rows over latitude:
    p_deg1_order0_lat = polynomials[1, 0, :]  # shape (nlat,)
    p_deg1_order1_lat = polynomials[1, 1, :]  # shape (nlat,)

    # Expand to (nlat, nlon) for grid operations
    p_deg1_order0 = p_deg1_order0_lat[:, None] * np.ones((1, nlon))
    p_deg1_order1 = p_deg1_order1_lat[:, None] * np.ones((1, nlon))

    # cos(m*lambda), sin(m*lambda) for m=1, expanded to (nlat, nlon)
    cos_ml_row = np.cos(np.deg2rad(lon))  # (nlon,)
    sin_ml_row = np.sin(np.deg2rad(lon))  # (nlon,)
    cos_ml = np.broadcast_to(cos_ml_row, (nlat, nlon))  # (nlat, nlon)
    sin_ml = np.broadcast_to(sin_ml_row, (nlat, nlon))  # (nlat, nlon)

    # --- Build fields and integrate (unit sphere radius=1)
    # g_vector vector
    func = p_deg1_order0 * oc_mask * kappa
    grid_obj_tmp = Grid2DObject(logger=logger, grid=func, lat=lat, lon=lon)
    g_deg1_order0_cos = (1.0 / (4.0 * np.pi)) * int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0)

    func = p_deg1_order1 * cos_ml * oc_mask * kappa
    grid_obj_tmp.grid = func
    g_deg1_order1_cos = (1.0 / (4.0 * np.pi)) * int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0)

    func = p_deg1_order1 * sin_ml * oc_mask * kappa
    grid_obj_tmp.grid = func
    g_deg1_order1_sin = (1.0 / (4.0 * np.pi)) * int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0)

    g_vector = np.array([g_deg1_order0_cos, g_deg1_order1_cos, g_deg1_order1_sin], dtype=float)

    # influence_matrix matrix
    func = p_deg1_order0 * oc_mask * p_deg1_order0
    grid_obj_tmp.grid = func
    i_deg1_order0_cos__deg1_order0_cos = ((1.0 / (4.0 * np.pi)) *
                                          int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0))

    func = p_deg1_order0 * oc_mask * p_deg1_order1 * cos_ml
    grid_obj_tmp.grid = func
    i_deg1_order0_cos__deg1_order1_cos = ((1.0 / (4.0 * np.pi)) *
                                          int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0))
    i_deg1_order1_cos__deg1_order0_cos = i_deg1_order0_cos__deg1_order1_cos

    func = p_deg1_order0 * oc_mask * p_deg1_order1 * sin_ml
    grid_obj_tmp.grid = func
    i_deg1_order0_cos__deg1_order1_sin = ((1.0 / (4.0 * np.pi)) *
                                          int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0))
    i_deg1_order1_sin__deg1_order0_cos = i_deg1_order0_cos__deg1_order1_sin

    func = p_deg1_order1 * cos_ml * oc_mask * p_deg1_order1 * cos_ml
    grid_obj_tmp.grid = func
    i_deg1_order1_cos__deg1_order1_cos = ((1.0 / (4.0 * np.pi)) *
                                          int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0))

    func = p_deg1_order1 * cos_ml * oc_mask * p_deg1_order1 * sin_ml
    grid_obj_tmp.grid = func
    i_deg1_order1_cos__deg1_order1_sin = ((1.0 / (4.0 * np.pi)) *
                                          int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0))
    i_deg1_order1_sin__deg1_order1_cos = i_deg1_order1_cos__deg1_order1_sin

    func = p_deg1_order1 * sin_ml * oc_mask * p_deg1_order1 * sin_ml
    grid_obj_tmp.grid = func
    i_deg1_order1_sin__deg1_order1_sin = ((1.0 / (4.0 * np.pi)) *
                                          int_sphere(logger=logger, grid=grid_obj_tmp, radius=1.0))

    influence_matrix = np.array([
        [i_deg1_order0_cos__deg1_order0_cos, i_deg1_order0_cos__deg1_order1_cos, i_deg1_order0_cos__deg1_order1_sin],
        [i_deg1_order1_cos__deg1_order0_cos, i_deg1_order1_cos__deg1_order1_cos, i_deg1_order1_cos__deg1_order1_sin],
        [i_deg1_order1_sin__deg1_order0_cos, i_deg1_order1_sin__deg1_order1_cos, i_deg1_order1_sin__deg1_order1_sin], ],
        dtype=float,
    )

    # --- Solve for degree-1 coefficients
    # degree1_coefficients = influence_matrix^{-1} * (oc_n1 - g_vector)
    rhs = oc_n1 - g_vector
    degree1_coefficients = np.linalg.solve(influence_matrix, rhs)

    return degree1_coefficients
