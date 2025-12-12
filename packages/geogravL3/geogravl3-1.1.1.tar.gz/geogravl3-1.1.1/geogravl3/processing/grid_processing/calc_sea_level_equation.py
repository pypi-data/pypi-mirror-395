# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Module to solve the sea level equation."""
import copy
from logging import Logger
import datetime as dt

import numpy as np

from geogravl3.datamodels.shc import SHObject
from geogravl3.datamodels.grids import Grid3DObject, Grid2DObject
from geogravl3.processing.spherical_harmonics.sh_analysis import sh_analysis
from geogravl3.processing.spherical_harmonics.sh_synthesis import sh_synthesis
from geogravl3.utils.utils import get_constant, ellipsoid_radius
from geogravl3.utils.grid_utils import global_weighted_sum


def calc_sle(logger: Logger,
             ewh_grid: Grid3DObject,
             *,
             n_iterations: int = 2,
             n_max: int = 180,
             love_numbers: dict,
             rotational_feedback: bool = False,
             only_ocean: bool = False,
             lo_mask: Grid2DObject) -> Grid3DObject:
    """
    Calculate Sea-Level Pattern for Surface Load on grid.

    Parameters
    ----------
    logger: Logger, logger object to log the error messages
    grid_ocean (Grid3DObject): grid storing the mass anomaly in ewh over land
    n_iterations (int): Number of iterations, positive int, default=2
    n_max (int): maximum degree and order for SHA and SHS, positive int, default 180
    rotational_feedback (bool): Flag if rotational feedback should be considered, default True
    only_ocean (bool): Flag if output should be masked to ocean, default True
    lo_mask (Grid2DObject): land ocean mask

    Returns
    -------
    sea_level_pattern_out_grid (Grid3DObject): calculated sea level pattern

    """
    if n_iterations < 0:
        message = f"Number of iterations has to be larger or equal to 0, n_iterations={n_iterations}"
        logger.error(message)
        raise ValueError(message)
    if n_max < 1:
        message = f"Maximum degree has to be larger than 0, n_max={n_max}"
        logger.error(message)
        raise ValueError(message)

    # Reference ellipsoidal radius
    ellips_radius = ellipsoid_radius(45.0 * get_constant('deg_2_rad'))

    # Load love numbers
    # l_lovenumber = np.asarray(love_numbers["l"])
    k_lovenumber = np.asarray(love_numbers["k"])

    # --- Rotational feedback correction ---
    rotational_corr_cnm, rotational_corr_snm = _init_rotational_correction(
        rotational_feedback=rotational_feedback,
        n_max=n_max,
        k_love=k_lovenumber)

    # compute the area of the oceans
    ocean_area = global_weighted_sum(lo_mask, ellips_radius)

    # transform to shc for initial values
    ewh_shc = sh_analysis(logger=logger, grid=copy.deepcopy(ewh_grid), love_numbers=love_numbers, n_max=n_max)

    # Get grid infos of the input grid
    grid_info = ewh_grid.get_grid_info_dict()

    # loop over all time steps
    sea_level_pattern_out_grid = ewh_grid.copy()
    sea_level_pattern_out_grid.grid = np.zeros(ewh_grid.shape)

    for t in range(ewh_grid.ntime):
        # Global sum of loading grid pf the current month
        sum_load = global_weighted_sum(ewh_grid.to_Grid2DObject(logger=logger, index=t), ellips_radius)
        grid_sle_t = _compute_single_timestep(logger=logger,
                                              ewh_shc=ewh_shc[t],
                                              sum_load=sum_load,
                                              lo_mask=lo_mask,
                                              ellips_radius=ellips_radius,
                                              love_numbers=love_numbers,
                                              rotational_corr_cnm=rotational_corr_cnm,
                                              rotational_corr_snm=rotational_corr_snm,
                                              n_max=n_max,
                                              n_iterations=n_iterations,
                                              ocean_area=ocean_area,
                                              only_ocean=only_ocean,
                                              grid_info=grid_info)

        sea_level_pattern_out_grid.grid[t, :, :] = grid_sle_t
    return sea_level_pattern_out_grid


def _compute_single_timestep(logger: Logger,
                             ewh_shc: SHObject,
                             sum_load: float,
                             lo_mask: Grid2DObject,
                             ellips_radius: float,
                             love_numbers: dict,
                             rotational_corr_cnm: np.ndarray,
                             rotational_corr_snm: np.ndarray,
                             n_max: int,
                             n_iterations: int,
                             ocean_area: float,
                             only_ocean: bool,
                             grid_info: dict) -> np.ndarray:
    """
    Compute sea level pattern for one time step.

    Parameters
    ----------
    ewh_shc: shc of this time steps
    sum_load: sum of the mass loading of this time step
    lo_mask: Land ocean mask
    ellips_radius: reference radius
    love_numbers: dict containing the load love numbers
    rotational_corr_cnm: rotational correction for cnm
    rotational_corr_snm: rotational correction for snm
    n_max: max degree
    n_iterations: number of iterations
    ocean_area: area of the ocean according to land ocean mask
    only_ocean: flag for return if only ocean shall be computed
    grid_info: dict storing the grid information

    Returns
    ------------
    sea level pattern of this timestep
    """
    # Constants
    rho_water = get_constant('water_density')
    rho_earth = get_constant('earths_density')

    # Love numbers
    k_lovenumber = np.asarray(love_numbers["k"])
    h_lovenumber = np.asarray(love_numbers["h"])

    # initialising all grids for save handling if n_iterations=0
    nlat = grid_info['ysize']
    lat = np.array([grid_info['yfirst'] + i * grid_info['yinc'] for i in range(nlat)])
    nlon = grid_info['xsize']
    lon = np.array([grid_info['xfirst'] + i * grid_info['xinc'] for i in range(nlon)])

    grid_crust_ocean = np.zeros((nlat, nlon))
    grid_sea_level = np.zeros((nlat, nlon))
    grid_height_ocean = np.zeros((nlat, nlon))

    # Iteration adapted from Tamisiea et al. (2010, 10.1029/2009JC005687) but applying
    # Eq. 12 in the spatial domain instead.
    #
    #          equ. 11 <------------------------
    #             |                            |
    #             v                            |
    #  in --->  equ. 14 -> equa. 13 -> equ. 12 -
    #
    # In iteration 0 Eq. 11 is not applied.
    # set grid_sea_level:=0 -> global uniform ocean layer balancing the applied load 'gridLoad'
    # -> grid_crust_ocean = 0 (equ. 14)
    #          sea_level_shc   <------------- height_ocean_shc
    #           |                                   ^
    #           SYN                                 |
    #           |                                  SHA
    #           v                                   |
    # in --->  grid_crust_ocean  ->  dphi  ->   grid_height_ocean  ----> out

    # Using n_iterations + 1 since the first iteration is used as initialization
    # and does not count towards number of iterations.
    for iteration in range(0, n_iterations + 1):
        # Corresponds to variable RO_j in Tamisiea et al.
        grid_crust_ocean[:, :] = 0
        if iteration > 0:
            # Convert grid-Height_ocean (Delta S of Tamisiea et al.) to SHs for Eq. 11
            height_ocean_shc = sh_analysis(logger=logger,
                                           grid=Grid3DObject(logger=logger,
                                                             grid=grid_height_ocean[None, :, :],
                                                             # Arbitrary date not used in the following
                                                             dates=np.array([dt.date(2000, 1, 1)]),
                                                             lon=lon, lat=lat),
                                           love_numbers=love_numbers, n_max=n_max)

            # equation 11: relative sea-level (sea-level equation)
            sea_level_shc = SHObject(logger=logger,
                                     date=dt.date(2000, 1, 1),
                                     cnm=ewh_shc.cnm + height_ocean_shc[0].cnm,
                                     snm=ewh_shc.snm + height_ocean_shc[0].snm)

            # loading / self-attraction / rotational deformation

            # Degree-dependent scaling factor: shape (n_max+1, 1)
            n = np.arange(n_max + 1)[:, None]
            scaling_factor = (1 + k_lovenumber[:n_max + 1] - h_lovenumber[:n_max + 1]) / (2 * n + 1)
            factor_rho = (3 * rho_water / rho_earth)

            # Apply rotational correction and scaling (which considers effects of gravitation and deformation)
            sea_level_shc.cnm[:n_max + 1, :] *= (scaling_factor + rotational_corr_cnm[:n_max + 1, :]) * factor_rho
            sea_level_shc.snm[:n_max + 1, :] *= (scaling_factor + rotational_corr_snm[:n_max + 1, :]) * factor_rho

            # Transform back to grid
            shs_out = sh_synthesis(logger=logger,
                                   shc=[sea_level_shc],
                                   gridinfo=grid_info,
                                   love_numbers=love_numbers,
                                   n_max=n_max,
                                   ref_surface="spherical")
            grid_sea_level = shs_out.grid[0]

            # equation 14: apply ocean function in spatial domain for new ocean surface
            grid_crust_ocean = grid_sea_level * lo_mask.grid

        # equation 13: mass conservation in spatial domain
        sum_crust_ocean = global_weighted_sum(Grid2DObject(logger=logger,
                                                           grid=grid_crust_ocean,
                                                           lon=lon, lat=lat),
                                              ellips_radius)

        dphi = - (sum_load + sum_crust_ocean) / ocean_area

        # Updating water column via Eq. 12 of Tamisiea et al. but in spatial domain.
        grid_height_ocean = grid_crust_ocean + dphi * lo_mask.grid
        # iteration end

    # only ocean or ocean and land part (gridSL-gridRO-gridLoad) from last iteration
    if only_ocean:
        grid_sea_level_pattern_out = grid_height_ocean
    else:
        grid_sea_level_pattern_out = grid_height_ocean + grid_sea_level - grid_crust_ocean

    return grid_sea_level_pattern_out


def _init_rotational_correction(rotational_feedback: bool, n_max: int, k_love: np.ndarray) \
        -> (np.ndarray, np.ndarray):
    """
    Initialize rotational correction arrays.

    Calculates the rotational correction and tidal deformation factor based on Martinec & Hagedoorn
    (2014, 10.1093/gji/ggu369) Eq. 123: (1+k_e^L)/(k^s^T-k_e^T)[1 + k_e^T - h_e^T]
    The correction is applied in Eq. 11 of Tamisiea et al.
    by kffSL = kffSL + 3*rhoW/5/rhoE*rotcorr*kffSL

    Parameters
    ----------
    rotational_feedback (Bool): if correction should be applied or not
    n_max (int): max degree
    k_love (np.ndarray): k Load love numbers

    Returns
    -------
    corr_cnm (np.ndarray): Correction for cnm [n_max+1, n_max+1]
    corr_snm (np.ndarray): Correction for snm [n_max+1, n_max+1]
    """
    corr_cnm = np.zeros((n_max + 1, n_max + 1))
    corr_snm = np.zeros((n_max + 1, n_max + 1))

    if rotational_feedback:
        # only for C21, S21
        coeff = (1.0 + k_love[2]) / (0.9667 - 0.2955) * (1.0 + 0.2955 - 0.5984)
        corr_cnm[2, 1] = coeff
        corr_snm[2, 1] = coeff
    return corr_cnm, corr_snm
