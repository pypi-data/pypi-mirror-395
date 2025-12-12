#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""L3 functions for geogravL3 package."""
from logging import Logger
from typing import Union, Tuple, Optional, List

import numpy as np

from .calc_sea_level_equation import calc_sle
from .remove_coseismic import remove_coseismic_signal
from ...processing.timeseries import apply_harmonic_components_grid, FitConfig, gaussian_filter_grid
from ...datamodels.grids import Grid2DObject, Grid3DObject, Grid3DIceObject
from ...utils.utils import get_constant
from ...utils.grid_utils import land_ocean_mask_buffer, standardize_lat_lon_grid
from ...io.readers import read_mask, read_nc
from ...datamodels.shc import SHObject


def prepare_land_ocean_masks(logger: Logger,
                             file_land_ocean_mask: str,
                             file_ice_mask: Optional[str] = None
                             ) \
        -> Union[Grid2DObject, Tuple[Grid2DObject, Grid2DObject]]:
    """
    Prepare land-ocean (and ice) mask.

    If an ice mask is provided, the ice regions are also masked out.

    Parameters
    ----------
    logger: Logger, logger object to log the error messages
    file_land_ocean_mask: str, file name from config file
    file_ice_mask: str, file name from config file

    Returns
    -------
    land_ocean_mask: np.ndarray(bool), containing the land-ocean mask
    no_ice_mask: np.ndarray(bool), containing the land-ocean mask,
    excluding the ice covered regions Greenland and Antarctica

    """
    land_ocean_mask = read_mask(logger=logger, file_name=file_land_ocean_mask)

    if file_ice_mask is not None:
        ice_mask = read_mask(logger=logger, file_name=file_ice_mask)
        if land_ocean_mask.same_coords(ice_mask):
            no_ice_mask = Grid2DObject(logger=logger,
                                       grid=land_ocean_mask.grid ^ ice_mask.grid,
                                       lon=land_ocean_mask.lon,
                                       lat=land_ocean_mask.lat)
            return land_ocean_mask, no_ice_mask
        else:
            if land_ocean_mask.shape == ice_mask.shape:
                land_ocean_mask = standardize_lat_lon_grid(logger=logger,
                                                           longitudes=land_ocean_mask.lon,
                                                           latitudes=land_ocean_mask.lat,
                                                           grid=land_ocean_mask,
                                                           target_lat_order='descending',
                                                           target_lon_format="[0, 360]")

                ice_mask = standardize_lat_lon_grid(logger=logger,
                                                    longitudes=ice_mask.lon,
                                                    latitudes=ice_mask.lat,
                                                    grid=ice_mask,
                                                    target_lat_order='descending',
                                                    target_lon_format="[0, 360]")
                no_ice_mask = Grid2DObject(logger=logger,
                                           grid=land_ocean_mask.grid ^ ice_mask.grid,
                                           lon=land_ocean_mask.lon,
                                           lat=land_ocean_mask.lat)
                return land_ocean_mask, no_ice_mask
            else:
                logger.warning(f"WARNING: {file_land_ocean_mask} and {file_ice_mask} do not have the same dimensions!"
                               f" {file_ice_mask} is ignored")
                return land_ocean_mask, land_ocean_mask
    else:
        return land_ocean_mask


def tws_processing(logger: Logger,
                   input_ewh_grid: Grid3DObject,
                   file_land_ocean_mask: str,
                   domain: str,
                   list_earthquakes: List[str],
                   file_ice_mask: Optional[str] = None) \
        -> Tuple[Grid3DObject, Grid3DObject]:
    """
    Process TWS and TWS uncertainties.

    - Removal of earthquake signal
    - Estimating uncertainties
    - Masking out the ocean and possibly ice covered regions

    Parameters
    ----------
    logger: Logger, logger object to log the error messages
    input_ewh_grid: Grid3DObject, filtered global ewh grid in the unit meter, [t x n x m]
    file_land_ocean_mask: str, path to file of land-mask [n x m] 1 for the land grid points, 0 everywhere else
    domain: either "all" - no land-mask applied, or "land" - land-mask applied
    list_earthquakes: List[str] list of filenames for earthquake definitions
    file_ice_mask: Optional, str, path to file of ice mask

    Returns
    -------
    tws: Grid3DObject, Masked out tws field
    std_tws: Grid3DObject, tws standard deviation
    """
    # Prepare land_ocean_ice masks
    if file_ice_mask is not None:
        lo_mask_all, lo_mask = prepare_land_ocean_masks(logger=logger,
                                                        file_land_ocean_mask=file_land_ocean_mask,
                                                        file_ice_mask=file_ice_mask)
        open_ocean_mask = land_ocean_mask_buffer(logger=logger,
                                                 lo_mask=lo_mask_all,
                                                 buffer=1000)
        open_ocean_mask.grid = ~open_ocean_mask.grid
    else:
        lo_mask = prepare_land_ocean_masks(logger=logger, file_land_ocean_mask=file_land_ocean_mask)
        open_ocean_mask = land_ocean_mask_buffer(logger=logger,
                                                 lo_mask=lo_mask,
                                                 buffer=1000)
        open_ocean_mask.grid = ~open_ocean_mask.grid

    if not lo_mask.same_coords(input_ewh_grid) and lo_mask.shape == input_ewh_grid.shape[1::]:
        if np.min(input_ewh_grid.lon) < 0:
            target_lon = '[-180, 180]'
        else:
            target_lon = '[0, 360]'
        if input_ewh_grid.lat[0] > input_ewh_grid.lat[-1]:
            target_lat = 'descending'
        else:
            target_lat = 'ascending'

        open_ocean_mask = standardize_lat_lon_grid(logger=logger,
                                                   longitudes=open_ocean_mask.lon,
                                                   latitudes=open_ocean_mask.lat,
                                                   grid=open_ocean_mask,
                                                   target_lat_order=target_lat,
                                                   target_lon_format=target_lon)
        lo_mask = standardize_lat_lon_grid(logger=logger,
                                           longitudes=lo_mask.lon,
                                           latitudes=lo_mask.lat,
                                           grid=lo_mask,
                                           target_lat_order=target_lat,
                                           target_lon_format=target_lon)
    elif not lo_mask.same_coords(input_ewh_grid):
        message = (f'Size of the land ocean mask with {lo_mask.shape} does not fit the size of the '
                   f'data grid with {input_ewh_grid.shape[1::]}')
        logger.error(message)
        raise ValueError(message)

    # Removal of earthquakes
    ewh_eq_grid = input_ewh_grid.copy()
    for eq_file in list_earthquakes:
        ewh_eq_grid = remove_coseismic_signal(logger=logger,
                                              grid=ewh_eq_grid.copy(),
                                              eqfile=eq_file)

    # estimate uncertainty in the form of ocean std
    masked_ewh_ocean = np.where(open_ocean_mask.grid, input_ewh_grid.grid, np.nan)
    ewh_grid_ocean = Grid3DObject(logger=logger,
                                  grid=masked_ewh_ocean,
                                  dates=input_ewh_grid.dates,
                                  lon=input_ewh_grid.lon, lat=input_ewh_grid.lat)

    cfg = FitConfig(include_mean=False, trend=True, annual=True, semiannual=True)
    ewh_grid_ocean_reduced_dict = apply_harmonic_components_grid(logger=logger, grid3d=ewh_grid_ocean, components=cfg)
    ewh_grid_ocean_reduced = ewh_grid_ocean_reduced_dict['output'].grid
    std_per_timestep = np.nanstd(ewh_grid_ocean_reduced, axis=(1, 2))
    std_tws = np.broadcast_to(std_per_timestep[:, np.newaxis, np.newaxis], input_ewh_grid.shape)

    if domain == 'land':
        # mask out ocean and possible ice
        masked_ewh = np.where(lo_mask.grid, ewh_eq_grid.grid, np.nan)
        tws = input_ewh_grid.copy()
        tws.grid = masked_ewh * 1000  # units mm

        masked_std_tws = np.where(lo_mask.grid, std_tws, np.nan)
        std_tws_grid = input_ewh_grid.copy()
        std_tws_grid.grid = masked_std_tws * 1000  # units mm
    else:
        tws = input_ewh_grid.copy()
        tws.grid = ewh_eq_grid.grid * 1000  # units mm

        std_tws_grid = input_ewh_grid.copy()
        std_tws_grid.grid = std_tws * 1000  # units mm

    return tws, std_tws_grid


def obp_processing(logger: Logger,
                   input_ewh_grid: Grid3DObject,
                   file_land_ocean_mask: str,
                   love_numbers: dict,
                   list_earthquakes: List[str],
                   num_iterations_sle: int = 2,
                   n_max_sle: int = 180) \
        -> Tuple[Grid3DObject, Grid3DObject, Grid3DObject, Grid3DObject]:
    """
    Process SLE and residual OBP and their uncertainties.

    - Solving sea level equation
        - SLE uncertainty
    - Residual OBP = Input - SLE
        - Remove earthquake signals
        - Residual OBP uncertainty
    - Masking out land

    Parameters
    ----------
    logger: Logger, logger object to log the error messages
    input_ewh_grid: Grid3DObject, filtered global ewh grid in the unit meter, [t x n x m]
    file_land_ocean_mask: str, path to file of land-mask [n x m] 1 for the land grid points, 0 everywhere else
    love_numbers: dict, Dictionary of Love number series, where 'k', 'h', and 'l' corresponds to the
    relevant series of Love numbers up to degree l_max.
    list_earthquakes: List[str] list of filenames for earthquake definitions
    num_iterations_sle: int, number of iterations done for solving the sea level equation
    n_max_sle: int, maximum degree and order used in solving the sea level equation

    Returns
    -------
    sle_grid: Grid3DObject, Masked out sle field
    sle_std_grid: Grid3DObject, sle standard deviation
    residual_obp_grid: Grid3DObject, Masked out residual obp field
    residual_obp_std_grid: Grid3DObject, residual obp standard deviation

    """
    # check input
    if num_iterations_sle < 0 or not isinstance(num_iterations_sle, int):
        message = (f'Number of iterations for SLE needs to be a integer >= 0, '
                   f'num_iteration_sle provided {num_iterations_sle}')
        logger.error(message)
        raise ValueError(message)
    if n_max_sle <= 0 or not isinstance(n_max_sle, int):
        message = f'Max degree for SLE needs to be a integer > 0, n_max_sle provided {n_max_sle}'
        logger.error(message)
        raise ValueError(message)

    # read land_ocean_mask
    lo_mask = prepare_land_ocean_masks(logger=logger, file_land_ocean_mask=file_land_ocean_mask)
    if not lo_mask.same_coords(input_ewh_grid) and lo_mask.shape == input_ewh_grid.shape[1::]:
        if np.min(input_ewh_grid.lon) < 0:
            target_lon = '[-180, 180]'
        else:
            target_lon = '[0, 360]'
        if input_ewh_grid.lat[0] > input_ewh_grid.lat[-1]:
            target_lat = 'descending'
        else:
            target_lat = 'ascending'

        lo_mask = standardize_lat_lon_grid(logger=logger,
                                           longitudes=lo_mask.lon,
                                           latitudes=lo_mask.lat,
                                           grid=lo_mask,
                                           target_lat_order=target_lat,
                                           target_lon_format=target_lon)
    elif not lo_mask.same_coords(input_ewh_grid):
        message = (f'Size of the land ocean mask with {lo_mask.shape} does not fit the size of the '
                   f'data grid with {input_ewh_grid.shape[1::]}')
        logger.error(message)
        raise ValueError(message)

    # factor m -> hPa
    water_density = get_constant('water_density')
    standard_gravity = get_constant('standard_gravity_acceleration_pole')
    factor = water_density * standard_gravity / 100

    # --- Estimate sea level pattern - SLE ---
    sle_in = input_ewh_grid.copy()
    sle_in.grid = sle_in.grid * lo_mask.grid

    sle_grid = calc_sle(logger=logger,
                        ewh_grid=sle_in,
                        n_iterations=num_iterations_sle,
                        n_max=n_max_sle,
                        love_numbers=love_numbers,
                        lo_mask=lo_mask)
    sle_grid.grid = sle_grid.grid * factor

    # SLE uncertainties
    fsle = 0.1  # factor for sle
    # Temporal standard deviation
    sle_std = np.tile(np.nanstd(sle_grid.grid, axis=0), (sle_grid.ntime, 1, 1))
    # Multiply by constant
    sle_std_scaled = fsle * sle_std
    sle_std_grid = sle_grid.copy()
    sle_std_grid.grid = sle_std_scaled * factor

    # --- residual circulation ---
    residual_obp_grid = input_ewh_grid.copy()
    residual_obp_grid.grid = input_ewh_grid.grid * factor - sle_grid.grid

    # Earthquakes
    for eq_file in list_earthquakes:
        residual_obp_grid = remove_coseismic_signal(logger=logger,
                                                    grid=residual_obp_grid.copy(),
                                                    eqfile=eq_file)

    # estimate uncertainty for residual circulation in the form of ocean std
    cfg = FitConfig(include_mean=False, trend=True, annual=True, semiannual=True)
    input_ewh_grid_reduced_dict = apply_harmonic_components_grid(logger=logger,
                                                                 grid3d=input_ewh_grid,
                                                                 components=cfg)
    ewh_grid_ocean_reduced = input_ewh_grid_reduced_dict['output'].grid
    std_per_timestep = np.nanstd(ewh_grid_ocean_reduced, axis=(1, 2))
    std_residobp_grid = np.broadcast_to(std_per_timestep[:, np.newaxis, np.newaxis], input_ewh_grid.shape)
    residual_obp_std_grid = input_ewh_grid.copy()
    residual_obp_std_grid.grid = std_residobp_grid * factor

    # --- masking ---
    sle_grid.grid = sle_grid.grid * ~lo_mask.grid
    sle_std_grid.grid = sle_std_grid.grid * ~lo_mask.grid
    residual_obp_grid.grid = residual_obp_grid.grid * ~lo_mask.grid
    residual_obp_std_grid.grid = residual_obp_std_grid.grid * ~lo_mask.grid

    return sle_grid, sle_std_grid, residual_obp_grid, residual_obp_std_grid


def im_processing(logger: Logger,
                  shc: list[SHObject],
                  file_name_sensitivity_kernel: str,
                  love_numbers: dict) -> Tuple[Grid3DIceObject, Grid3DIceObject]:
    """
    Process ice mass IM.

    Parameters
    ----------
    logger (Logger): logger object
    shc (list[SHObjects]): list SHObjects
    file_name_sensitivity_kernel (str): name to sensitivity kernel file
    love_numbers (dict): dictionary containing load love numbers


    Returns
    -------
    Grid3DIceObject of im results
    """
    # read sensitivity kernel
    sensitivity_kernel_nc = read_nc(file_name=file_name_sensitivity_kernel)
    sens_kernel = sensitivity_kernel_nc['Eta']['value']

    # Check for max degrees of coefficients and sensitivity kernel
    n_max_sens_kernel = int(np.sqrt(sens_kernel.shape[0]) - 1)
    n_max = shc[0].get_max_degree()
    if n_max < n_max_sens_kernel:  # Reduce max degree of sensitivity kernels
        sens_kernel = sens_kernel[sensitivity_kernel_nc['degrees']['value'] <= n_max, :]
    elif n_max > n_max_sens_kernel:
        logger.warning(""f'WARNING: maximum degree of data {n_max} is larger than maximum degree {n_max_sens_kernel} '
                       f'of sensitivity kernels! Reduced to  {n_max_sens_kernel}')
        shc_reduced = reduce_max_degree_SHObject(logger=logger, shc=shc, n_max=n_max_sens_kernel)
        shc = shc_reduced
        n_max = n_max_sens_kernel

    # Factor for conversion to surface mass density
    M = get_constant('geocentric_gravitational_constant_iers') / get_constant('gravitational_constant_iers')
    r = get_constant('earths_radius_iers')
    factor_smd = np.array([M / (4 * np.pi * r ** 2) * (2 * n + 1) / (1 + love_numbers["k"][n])
                           for n in range(0, n_max + 1)])
    shc_surface_mass_density = [SHObject(logger=logger,
                                         date=s.date,
                                         cnm=s.cnm * factor_smd[:, None],
                                         snm=s.snm * factor_smd[:, None])
                                for s in shc]

    vectorized_shc = reformat_shc(shc=shc_surface_mass_density)

    # Apply sensitivity kernel
    im_mass_vectorized = (4 * np.pi * r ** 2) * sens_kernel.T @ vectorized_shc

    # reformat to grid
    dates = np.array([s.date for s in shc])
    im_grid_object = reformat_im_grid(logger=logger,
                                      im=im_mass_vectorized,
                                      mask_grid_number=sensitivity_kernel_nc["Mask_masconnumbers"]['value'],
                                      area=sensitivity_kernel_nc["area"]['value'],
                                      dates=dates,
                                      x=sensitivity_kernel_nc["x"]['value'],
                                      y=sensitivity_kernel_nc["y"]['value'],
                                      lon=sensitivity_kernel_nc["lon"]['value'],
                                      lat=sensitivity_kernel_nc["lat"]['value'],
                                      projection=sensitivity_kernel_nc["crs"]['attributes'])
    # estimate uncertainty
    cfg = FitConfig(include_mean=True, trend=True, annual=True, semiannual=True, quadratic=True,
                    period161_cos=True, period161_sin=True)
    im_grid_object_deterministic_reduced = apply_harmonic_components_grid(logger=logger,
                                                                          grid3d=im_grid_object,
                                                                          components=cfg)['output']
    im_grid_object_gauss_smoothed = gaussian_filter_grid(logger=logger,
                                                         grid3d=im_grid_object_deterministic_reduced,
                                                         sigma=0.25,
                                                         cutdist=0.75)

    im_grid_gauss_smoothed = im_grid_object_gauss_smoothed.grid
    im_grid_std_per_grid = np.std(im_grid_gauss_smoothed, axis=0)
    std_im = np.broadcast_to(im_grid_std_per_grid[np.newaxis, :, :], im_grid_gauss_smoothed.shape)
    im_std_grid_object = Grid3DIceObject(logger=logger,
                                         grid=std_im,
                                         dates=im_grid_object.dates,
                                         lon=im_grid_object.lon,
                                         lat=im_grid_object.lat,
                                         x=im_grid_object.x,
                                         y=im_grid_object.y,
                                         projection=im_grid_object.projection,
                                         area=im_grid_object.area
                                         )
    return im_grid_object, im_std_grid_object


def reduce_max_degree_SHObject(logger: Logger, shc: list[SHObject], n_max: int):
    """
    Reduce the maximum degree and order of all SHObjects in the list to n_max.

    Parameters
    ----------
    logger (Logger): Logger object to log the error messages
    shc (list[SHObjects]): list SHObjects
    n_max (int): Max degree

    Returns
    -------
    list[SHObjects]
    """
    shc_reduced = [SHObject(logger=logger,
                            date=s.date,
                            cnm=s.cnm[0:n_max + 1, 0:n_max + 1],
                            snm=s.snm[0:n_max + 1, 0:n_max + 1]) for s in shc]
    return shc_reduced


def reformat_shc(shc: list[SHObject]) -> np.ndarray:
    """
    Reformate/vectorizes sh coefficients for matrix multiplication order wise.

    Example:
    c = np.array([[1,0,0], [2,3,0], [4,5,6]])

    s = np.array([[0,0,0], [0,7,0], [0,8,9]])

    coefficients_vector = [1 2 4 3 7 5 8 6 9]

    Parameters
    ----------
    shc (list[SHObjects]): the list of all SHObjects in which the cnm and snm are stored to be reformated

    Returns
    -------
    np.ndarray size [(n_max+1)**2, t]

    """
    n_max = shc[0].get_max_degree()
    coefficients_vector = np.zeros(((n_max + 1) ** 2, len(shc)))
    for ii, s in enumerate(shc):
        k = 0  # position index
        cnm = s.cnm
        snm = s.snm
        # first column of c
        for i in range(n_max + 1):
            coefficients_vector[k, ii] = cnm[i, 0]
            k += 1

        # remaining columns
        for j in range(1, n_max + 1):
            # diagonal pair
            coefficients_vector[k, ii] = cnm[j, j]
            k += 1
            coefficients_vector[k, ii] = snm[j, j]
            k += 1

            # sub-diagonal pairs
            for i in range(j + 1, n_max + 1):
                coefficients_vector[k, ii] = cnm[i, j]
                k += 1
                coefficients_vector[k, ii] = snm[i, j]
                k += 1
    return coefficients_vector


def reformat_im_grid(logger: Logger,
                     im: np.ndarray,
                     mask_grid_number: np.ndarray,
                     area: np.ndarray,
                     dates: np.ndarray,
                     x: np.ndarray,
                     y: np.ndarray,
                     lon: np.ndarray,
                     lat: np.ndarray,
                     projection: dict) -> Grid3DIceObject:
    """
    Reformats the vectorized results into grid.

    Parameters
    ----------
    logger: Logger, Logger object to log the error messages
    im (np.array): Vectorized results, each column one solution, each row one grid cell
    mask_grid_number (np.array): A 2D array containing the grid numbers to lines of im [n x m].
    area (np.array): A 2D array containing the grid areas of the grid [n x m].
    dates (np.array): dates of the solutions, in datetime.date
    x (np.array): A 1D array containing the x coordinates [m].
    y (np.array): A 1D array containing the y coordinates [n].
    lon (np.array): A 2D array containing the longitude coordinates of the grid [n x m].
    lat (np.array): A 2D array containing the latitude coordinates of the grid [n x m]
    projection (dict): Dictionary storing projection parameters

    Returns
    -------
    Grid3DIceObject
    """
    im_grid = np.zeros((im.shape[1], len(y), len(x))) * np.nan
    grid_numbers = np.unique(mask_grid_number[mask_grid_number > 0])
    for num in grid_numbers:
        id_grid = np.nonzero(mask_grid_number == num)
        im_gridcell = im[num - 1, :] / area[id_grid[0], id_grid[1]]
        im_grid[:, id_grid[0], id_grid[1]] = im_gridcell[:, None]

    im_grid_output = Grid3DIceObject(logger=logger,
                                     grid=im_grid,
                                     dates=dates,
                                     x=x,
                                     y=y,
                                     lat=lat,
                                     lon=lon,
                                     projection=projection,
                                     area=area)

    return im_grid_output
