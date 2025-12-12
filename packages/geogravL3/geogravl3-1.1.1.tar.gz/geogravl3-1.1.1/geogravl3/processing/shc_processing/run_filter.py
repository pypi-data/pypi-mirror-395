#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Filtering functions for geogravL3 package."""

import os
import copy
import re
from pathlib import Path
from typing import List, Dict
import datetime as dt
from logging import Logger

from .vdk_filter_functions import vdk
from ...datamodels.shc import SHObject
from ...config import path_resources
from .ddk_filter import filt_ddk
from .gaussian_filter import filt_gaussian


def run_filter(logger: Logger,
               filter_name: str,
               input_shc: List[SHObject],
               lmax: int,
               dict_date_to_filename: Dict[dt.datetime, str] = None) \
        -> List[SHObject]:
    """
    Run the filter given in filter_name to a list of SHObjects.

    Parameters
    ----------
    logger (Logger): logger object
    filter_name (str): name of the filter
    input_shc (List[SHObject]): List of the SHObjects to be filtered
    lmax (int=None): Maximum degree and order of  the filter, if None, max Degree of input is used
    dict_date_to_filename (dict): Dictionary linking the date of the data to the sinex file, only needed for vdk filter

    Returns
    -------
    filtered_output_shc (List[SHObject]): List of the filtered SHObjects
    """
    if 'DDK' in filter_name:
        logger.info(f"Apply the {filter_name} filter")
        filtered_output_shc = run_ddk_filter(input_shc=input_shc, ddk_name=filter_name, lmax=lmax, logger=logger)

    elif 'Gauss' in filter_name:
        filter_width = int(re.fullmatch(r"(Gauss)(\d+)", filter_name).groups()[1])
        logger.info(f"Apply the Gaussian filter with filter width of {filter_width} km")
        filtered_output_shc = run_gauss_filter(input_shc=input_shc, radius_km=filter_width, logger=logger, lmax=lmax)
    elif 'VDK' in filter_name:
        logger.info(f"Apply the {filter_name} filter")
        filtered_output_shc = run_vdk_filter(logger=logger,
                                             input_shc=input_shc,
                                             vdk_name=filter_name,
                                             lmax=lmax,
                                             dict_date_to_filename=dict_date_to_filename)
    else:
        message = f"Filter '{filter_name}' not supported"
        logger.error(message)
        raise ValueError(message)

    return filtered_output_shc


def run_gauss_filter(logger: Logger, input_shc: List[SHObject], radius_km: float, lmax: int = None) -> List[SHObject]:
    """
    Run the Gaussian filter on list of SHObjects.

    Parameters
    ----------
    logger (Logger): logger object
    input_shc (List[SHObject]): List of the SHObjects to be filtered
    radius_km (float): Positive float of the filter width
    lmax (int=None): Maximum degree and order of  the filter, if None, max Degree of input is used

    Returns
    -------
    filtered_output_shc (List[SHObject]): List of the filtered SHObjects
    """
    if lmax is None:
        lmax = input_shc[0].get_max_degree()
    else:
        if lmax > input_shc[0].get_max_degree():
            logger.warning(f'WARNING: provided max Degree {lmax} larger than max degree of input SH coefficients '
                           f'{input_shc[0].get_max_degree()}. Set to {input_shc[0].get_max_degree()}')
            lmax = input_shc[0].get_max_degree()

    if radius_km <= 0:
        message = f"Filter radius 'radius_km' must be positive, but is {radius_km}"
        logger.error(message)
        raise ValueError(message)

    # Generate Gaussian weights
    gw = filt_gaussian(lmax=lmax, radius=radius_km)

    # loop over all SHObjects in input
    filtered_output_shc = []
    for in_shc in input_shc:
        cnm_filt = in_shc.cnm.copy()[:lmax + 1, :lmax + 1]
        snm_filt = in_shc.snm.copy()[:lmax + 1, :lmax + 1]
        # Apply filter: multiply each degree's coefficients by its weight
        for n in range(lmax + 1):
            cnm_filt[n, :n + 1] *= gw[n]
            snm_filt[n, :n + 1] *= gw[n]
        filtered_output_shc.append(SHObject(logger=logger, date=in_shc.date, cnm=cnm_filt, snm=snm_filt))

    return filtered_output_shc


def run_ddk_filter(logger: Logger, input_shc: List[SHObject], ddk_name: str, lmax: int) -> List[SHObject]:
    """
    Run the DDK filter on list of SHObjects.

    Parameters
    ----------
    logger (Logger): logger object
    input_shc (List[SHObject]): List of the SHObjects to be filtered
    ddk_name (float): Name of the DDK filter to be used. Possible names DDK[1-8]
    lmax (int=None): Maximum degree and order of  the filter, if None, max Degree of input is used

    Returns
    -------
    filtered_output_shc (List[SHObject]): List of the filtered SHObjects
    """
    if lmax is None:
        lmax = input_shc[0].get_max_degree()
    else:
        if lmax > input_shc[0].get_max_degree():
            logger.warning(f'WARNING: provided max Degree {lmax} larger than max degree of input SH coefficients '
                           f'{input_shc[0].get_max_degree()}. Set to {input_shc[0].get_max_degree()}')
            lmax = input_shc[0].get_max_degree()

    input_copy_shc = copy.deepcopy(input_shc)

    # reduce input to max degree
    for sh in input_copy_shc:
        sh.cnm = sh.cnm[:lmax + 1, :lmax + 1]
        sh.snm = sh.snm[:lmax + 1, :lmax + 1]

    # Filter with given DDK filter
    ddk_file = Path(os.path.join(path_resources, 'DDKfilter')) / ddk_name
    filtered_output_shc = filt_ddk(logger=logger, input_shc=input_copy_shc, filename_filter=ddk_file, lmax=lmax)

    return filtered_output_shc


def run_vdk_filter(logger: Logger,
                   input_shc: List[SHObject],
                   vdk_name: str,
                   lmax: int,
                   dict_date_to_filename: Dict[dt.datetime, str]) -> List[SHObject]:
    """
    Run the VDK filter on list of SHObjects.

    Parameters
    ----------
    logger (Logger): logger object
    input_shc (List[SHObject]): List of the SHObjects to be filtered
    vdk_name (float): Name of the DDK filter to be used. Possible names VDK[1-8]
    lmax (int=None): Maximum degree and order of  the filter, if None, max Degree of input is used
    dict_date_to_filename (dict): Dictionary linking the date of the data to the sinex file

    Returns
    -------
    filtered_output_shc (List[SHObject]): List of the filtered SHObjects
    """
    if lmax is None:
        lmax = input_shc[0].get_max_degree()
    else:
        if lmax > input_shc[0].get_max_degree():
            logger.warning(f'WARNING: provided max Degree {lmax} larger than max degree of input SH coefficients '
                           f'{input_shc[0].get_max_degree()}. Set to {input_shc[0].get_max_degree()}')
            lmax = input_shc[0].get_max_degree()

    def _vdkname_to_alpha(name: str) -> float:
        name_to_alpha = {'VDK1': 10 ** 20,
                         'VDK2': 10 ** 19,
                         'VDK3': 10 ** 18,
                         'VDK4': 5 * 10 ** 17,
                         'VDK5': 10 ** 17,
                         'VDK6': 5 * 10 ** 16,
                         'VDK7': 10 ** 16,
                         'VDK8': 5 * 10 ** 15}
        return name_to_alpha[name]

    input_copy_shc = copy.deepcopy(input_shc)
    output_shc = []
    for sh in input_copy_shc:
        out_shc = vdk(logger=logger,
                      shc=sh,
                      path_snx=dict_date_to_filename[sh.date],
                      alpha=_vdkname_to_alpha(vdk_name))
        out_shc.cnm = out_shc.cnm[:lmax + 1, :lmax + 1]
        out_shc.snm = out_shc.snm[:lmax + 1, :lmax + 1]
        output_shc.append(out_shc)
    return output_shc
