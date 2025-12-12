#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""GIA correction module for geogravL3 package."""

import datetime as dt
from logging import Logger
from typing import Union

import numpy as np

from ...io.readers import read_gfc
from ...datamodels.shc import SHObject
from ...utils.date_utils import datetime_to_date_float


def get_gia_model(logger: Logger, filename: str, max_degree: int,
                  dates: Union[np.ndarray[dt.datetime], list[dt.datetime],
                               np.ndarray[dt.date], list[dt.date]]) -> list[SHObject]:
    """
    Load GIA model given in trends [m/year] and expand to accumulated GIA rates.

    Parameters
    ----------
    logger (Logger): Logger object to log the error messages
    filename (str): Filename to the gfc file storing the gia rates
    max_degree (int): Maximum degree and order needed of the GIA model
    dates (list[dt.datetime]): List of the dates to which the GIA should be expanded

    Returns
    -------
    accumulated_gia_rates_shc (list[SHObject]): list of accumulated GIA rates ([m])
    """
    gia_model_shc = read_gfc(logger=logger, file_name=filename, max_degree=max_degree)
    gia_rate_cnm = gia_model_shc.cnm
    gia_rate_snm = gia_model_shc.snm

    # compute elapsed time for the data
    dates_float = datetime_to_date_float(dates)
    elapsed_years = dates_float - dates_float[0]

    # Multiply rate (m/yr) × elapsed time (yr)
    trend_cnm = np.multiply.outer(elapsed_years, gia_rate_cnm)
    trend_snm = np.multiply.outer(elapsed_years, gia_rate_snm)

    accumulated_gia_rates_shc = [SHObject(logger=logger, date=dates[i],
                                          cnm=trend_cnm[i, :, :], snm=trend_snm[i, :, :]) for i in range(len(dates))]

    return accumulated_gia_rates_shc


def reduce_gia_model(logger: Logger, filename_gia_model: str, shc: list[SHObject]) -> list[SHObject]:
    """
    Reduce the GIA effect from the SH coefficients.

    Parameters
    ----------
    logger (Logger): Logger object to log the error messages
    filename_gia_model (str): Filename to the gfc file storing the gia rates
    shc (list[SHObjects]): list SHObjects to be corrected

    Returns
    -------
    shc_gia_reduced (list[SHObjects]): list SHObjects to with GIA correction applied

    """
    # get GIA signal
    dates_shc = [s.date for s in shc]
    accumulated_gia_rates_shc = get_gia_model(logger=logger, filename=filename_gia_model,
                                              max_degree=shc[0].get_max_degree(), dates=dates_shc)

    # reduce GIA from the shc
    shc_gia_reduced = [SHObject(logger=logger,
                                date=dates_shc[i],
                                cnm=shc[i].cnm - accumulated_gia_rates_shc[i].cnm,
                                snm=shc[i].snm - accumulated_gia_rates_shc[i].snm)
                       for i in range(len(dates_shc))]

    return shc_gia_reduced
