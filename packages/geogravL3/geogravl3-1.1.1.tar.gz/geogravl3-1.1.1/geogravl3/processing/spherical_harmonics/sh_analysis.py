# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Module to do Spherical Harmonic (SH) analysis."""
from logging import Logger

import numpy as np

from ...utils.utils import get_constant, ellipsoid_radius
from ...datamodels.grids import Grid3DObject
from ...datamodels.shc import SHObject
from .legendre import legendre


def sh_analysis(
        logger: Logger,
        grid: Grid3DObject,
        *,
        love_numbers: dict,
        case: str = "ewh",
        n_max: int = None) -> list[SHObject]:
    """
    Do the spherical harmonic analysis of the gridded input data.

    Parameters
    ----------
    logger (Logger): Logger object
    grid (Grid3DObject): Input grid of ewh to be converted to sh coefficients
    love_numbers (dict): Dictionary of Love number series, where 'k' corresponds to the
    relevant series of Love numbers up to degree l_max.
    n_max (int): Maximum spherical harmonic degree to consider. If None, max degree is set to 90.
    Raises ValueError if negative or zero
    case (str): {"ewh","one","geo","pre", "pot"}
    ewh = equivalent water heights,
    geo = geoid heights,
    pre = pressure
    Interprets the physical meaning of `grid` and applies the corresponding inverse
    of the synthesis scaling before the SH integral.

    Returns
    -------
    object spherical harmonic coefficients stored in a list of SHObjects

    """
    # # read orography file
    # orography_nc = read_nc(orography_file)
    # orthometric_height = orography_nc['reference_geopotential']['value']
    #
    # # geometric distance from Center_of_Earth to reference ellipsoid
    # rad = get_constant('deg_2_rad')
    # ellips_radius_lat = np.array([ellipsoid_radius(lat * rad) for lat in grid.lat])
    #
    # ellips_radius = ellipsoid_radius(45 * rad)
    #
    # # normal gravity at geometric height above ellipsoid
    # normal_gravity_lat = np.array([normal_gravity(grid.lat[i] * rad,
    #                                               orthometric_height[i,j])
    #                                for i in range(grid.nlat)
    #                                for j in range(grid.nlon)])
    #
    # # scaling factor
    # matrix_quotient = (ellips_radius_lat[:, np.newaxis] + orthometric_height) / ellips_radius
    #
    # powers = 2 + np.arange(n_max + 1)[:, np.newaxis, np.newaxis]  # shape (n_max+1, 1, 1)
    # factor_degree = matrix_quotient[np.newaxis, :, :] ** powers
    if n_max is None:
        n_max = 90
    if not isinstance(n_max, int) or n_max <= 0:
        msg = f"n_max has to be a positive integer, but is {n_max}."
        logger.error(msg)
        raise ValueError(msg)

    # convert units of input grid to unit less grid
    rho_water = get_constant('water_density')
    rho_earth = get_constant('earths_density')
    rad = get_constant('deg_2_rad')
    gravity_earth = get_constant('standard_gravity_acceleration')
    gm_earth = get_constant("geocentric_gravitational_constant_iers")
    ellips_radius = ellipsoid_radius(45 * rad)

    # --- degree-independent grid scaling (inverse of synthesis' degree-independent factor)
    case_key = (case or "ewh").lower().strip()
    degree_scale = None
    if case_key == "one":
        case = 1.0
    elif case_key == "geo":
        case = 1.0 / ellips_radius
    elif case_key == "ewh":
        case = (3.0 * rho_water) / (ellips_radius * rho_earth)
        degree_scale = "norm"  # use (1+k_l)/(2l+1)
    elif case_key == "pot":
        case = ellips_radius / gm_earth
    elif case_key == "pre":
        case = 3.0 / (ellips_radius * rho_earth * gravity_earth)
        degree_scale = "norm"  # use (1+k_l)/(2l+1)
    else:
        raise ValueError(f'Unknown case "{case}". Use one of: "ewh", "one", "geo", "pre", "pot".')

    # work on a copy (avoid mutating caller's object)
    field = grid.grid.astype(np.float64, copy=True)
    field *= case

    # Get area for each grid cell
    area = grid.get_grid_area(ellips_radius)
    # area_globe = 4 * np.pi * get_constant('earths_radius_iers') ** 2
    area_globe = 4 * np.pi * ellips_radius ** 2

    # trigonometric functions
    rad = get_constant('deg_2_rad')
    sinj = np.sin(grid.lat * rad).astype(np.float64)
    lon_rad = grid.lon * rad

    # Precompute trigonometric matrices (vectorized) ---
    m = np.arange(n_max + 1)[:, None]  # (n_max+1, 1)
    mat_cosm = np.cos(m * lon_rad)  # (n_max+1, nlon)
    mat_sinm = np.sin(m * lon_rad)  # (n_max+1, nlon)

    # Legendre polynomials
    polynomials = legendre(logger=logger, lmax=n_max, lat_rows=grid.nlat, sin_lat=sinj)

    # --- degree-dependent normalization (inverse of synthesis' (2l+1)/(1+k_l))
    k_arr = np.asarray(love_numbers["k"], dtype=np.float64)
    deg = np.arange(n_max + 1, dtype=np.float64)
    if degree_scale == "norm":
        l_scale = (1.0 + k_arr[:n_max + 1]) / (2.0 * deg + 1.0)  # (l)
    else:
        l_scale = np.ones(n_max + 1, dtype=np.float64)

    # --- main loop over time
    results: list[SHObject] = []
    for t_idx in range(grid.ntime):
        # area-weighted field normalized by total area
        grid_t = field[t_idx, :, :] * area / area_globe

        # --- Step 1: integrate over longitude (fastest dimension)
        lon_cos = mat_cosm @ grid_t.T
        lon_sin = mat_sinm @ grid_t.T

        # --- Step 2: apply polynomials and integrate over latitude

        # Broadcast correctly: lon_cos[m, nlat] -> (l, m, nlat)
        lon_cos_exp = lon_cos[None, :, :]
        lon_sin_exp = lon_sin[None, :, :]

        # Multiply and sum over latitude (axis=2)
        cnm = l_scale[:, None] * np.sum(polynomials[:n_max + 1, :n_max + 1, :] * lon_cos_exp[:, :n_max + 1, :], axis=2)
        snm = l_scale[:, None] * np.sum(polynomials[:n_max + 1, :n_max + 1, :] * lon_sin_exp[:, :n_max + 1, :], axis=2)

        # above is vectorized from of:
        # cnm = np.zeros((n_max + 1, n_max + 1))
        # snm = np.zeros((n_max + 1, n_max + 1))
        #
        # for n in range(n_max+1):
        #     for m in range(n+1):
        #         c = 0
        #         s = 0
        #         for i in range(grid.nlat):
        #             for j in range(grid.nlon):
        #                 c += scale[n] * grid_t[i,j] * polynomials[n, m, i] * mat_cosm[m,j]
        #                 s += scale[n] * grid_t[i, j] * polynomials[n, m, i] * mat_sinm[m,j]
        #         cnm[n, m] = c
        #         snm[n, m] = s

        # Mask out invalid (i_ord > i_deg) entries if needed
        cnm = np.tril(cnm)
        snm = np.tril(snm)

        results.append(SHObject(logger=logger, date=grid.dates[t_idx], cnm=cnm, snm=snm))

    return results
