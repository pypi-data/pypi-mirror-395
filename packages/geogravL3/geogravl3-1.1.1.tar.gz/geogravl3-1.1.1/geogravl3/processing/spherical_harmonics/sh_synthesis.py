# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Module to do Spherical Harmonic (SH) synthesis."""
from logging import Logger

import numpy as np

from ...datamodels.grids import Grid3DObject
from ...datamodels.shc import SHObject
from ...utils.utils import get_constant, ellipsoid_radius
from .legendre import legendre


def sh_synthesis(
        logger: Logger,
        shc: list[SHObject],
        gridinfo: dict,
        love_numbers: dict,
        n_max: int = None,
        case: str = "ewh",
        ref_surface="spherical") -> Grid3DObject:
    """
    Perform Spherical Harmonic (SH) synthesis.

    Compute a global grid of values based on the
    provided SH coefficients, grid information, and additional parameters.

    This function calculates the geographical distribution of a spherical harmonic field using
    the SH coefficients for sine and cosine terms, grid configuration, and Love numbers. It
    supports spherical or ellipsoidal reference surfaces for the final computations.

    Parameters:
        logger (Logger): Logger object
        shc : spherical harmonic coefficients stored in a list of SHObjects
        gridinfo (dict): Information regarding the geographical grid, containing keys like
        'xfirst', 'xsize', 'xinc', 'yfirst', 'ysize', 'yinc'.
        love_numbers (dict): Dictionary of Love number series, where 'k' corresponds to the
        relevant series of Love numbers up to degree l_max.
        n_max (int): Maximum spherical harmonic degree to consider. If None, max degree is read from data.
        case : {"ewh","one","geo","pre"}
        Controls the physical scaling:
        - "one": geoid heights, mat_fact(l) = 1
        - "geo": mat_fact(l) = ellipsoid radius at 45°
        - "ewh": equivalent water heights,
        mat_fact(l) = ((2.0 * n + 1.0) / lln) * (ellips_radius * mean_earth_density / (3.0 * water_density))
        - "pre": pressure,
        mat_fact(l) = ((2.0 * n + 1.0) / lln) * (ellips_radius * mean_earth_density / 3.0 * gravity_earth)

        Default is "ewh".
        ref_surface (str): Reference surface for computations, either "spherical" or
        "ellipsoidal". Defaults to "spherical".

    Returns:
        grid (Grid3DObject): (global) grid containing the synthesized geographical values.

    """
    # max Degree, n_max
    if n_max is None:
        n_max = shc[0].get_max_degree()

    # number of time steps
    n_time = len(shc)

    # constants
    mean_earth_density = get_constant("earths_density")
    water_density = get_constant("water_density")
    rad = get_constant("deg_2_rad")
    gravity_earth = get_constant("standard_gravity_acceleration")

    # grid axes
    lon = gridinfo["xfirst"] + np.arange(gridinfo["xsize"]) * gridinfo["xinc"]
    lat = gridinfo["yfirst"] + np.arange(gridinfo["ysize"]) * gridinfo["yinc"]
    num_longitudes = len(lon)
    num_latitudes = len(lat)

    # trigonometric functions
    sinj = np.sin(lat * rad).astype(np.float64)
    lon_rad = lon * rad
    m = np.arange(n_max + 1)[:, None]  # (n_max+1, 1)
    mat_cosm = np.cos(m * lon_rad)  # (n_max+1, nlon)
    mat_sinm = np.sin(m * lon_rad)  # (n_max+1, nlon)

    # Legendre polynomials
    polynomials = legendre(logger=logger, lmax=n_max, lat_rows=num_latitudes, sin_lat=sinj)

    # ellips_radius: ellipsoid radius at reference latitude (45°)
    reflat = 45 * rad
    ellips_radius = ellipsoid_radius(reflat)

    # mat_fact per select case
    n = np.arange(n_max + 1, dtype=np.float64)
    lln = np.array(love_numbers["k"][:n_max + 1]) + 1

    case = (case or "ewh").lower().strip()
    if case == "one":
        mat_fact = np.ones(n_max + 1, dtype=np.float64)
    elif case == "geo":
        mat_fact = np.full(n_max + 1, ellips_radius, dtype=np.float64)
    elif case == "ewh":
        mat_fact = ((2.0 * n + 1.0) / lln) * (ellips_radius * mean_earth_density / (3.0 * water_density))
    elif case == "pre":
        mat_fact = ((2.0 * n + 1.0) / lln) * (ellips_radius * mean_earth_density / 3.0 * gravity_earth)
    else:
        message = f'Unknown case "{case}". Use one of: "ewh", "one", "geo", "pre".'
        logger.error(message)
        raise ValueError(message)

    # approximation
    mat_appr = np.ones((n_max + 1, num_latitudes))

    if ref_surface == "ellipsoidal":
        lat_rad = lat * rad  # shape (num_latitudes,)
        ellip = ellipsoid_radius(lat_rad)  # shape (num_latitudes,)

        n = np.arange(n_max + 1).reshape(-1, 1)  # shape (n_max+1, 1)
        mat_appr = (ellips_radius / ellip) ** (n + 2)

    # Time loop
    grid = np.zeros((n_time, num_latitudes, num_longitudes))
    for t, shc_t in enumerate(shc):
        cnm = shc_t.cnm[:n_max+1, :n_max+1]
        snm = shc_t.snm[:n_max+1, :n_max+1]

        # mat_PNMdC and mat_PNMdS: shape (n_max+1, n_max+1, num_latitudes)
        mat_PNMdC = cnm[:, :, np.newaxis] * polynomials  # broadcast over latitudes
        mat_PNMdS = snm[:, :, np.newaxis] * polynomials

        # geographical loop
        for j in range(num_latitudes):
            mat_term1 = mat_PNMdC[:, :, j] @ mat_cosm
            mat_term2 = mat_PNMdS[:, :, j] @ mat_sinm

            a = mat_fact * mat_appr[:, j]
            b = mat_term1 + mat_term2

            grid[t, j, :] = a @ b
    output_grid = Grid3DObject(logger=logger,
                               grid=grid,
                               dates=np.array([shc_t.date for shc_t in shc]),
                               lon=lon,
                               lat=lat)
    return output_grid
