#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Functions for replacing the low degree harmonics (c20, c30) in the geogravL3 package."""
from logging import Logger
from typing import List
import datetime as dt

import numpy as np

from ...datamodels.shc import SHObject
import geogravl3.io.readers as rd


def replace_low_degrees(logger: Logger,
                        shc: List[SHObject],
                        filename_replacements: str) -> List[SHObject]:
    """
    Replace the low degree harmonics.

    C20 and C30 (only between 2016/11 and 2017/6) are taken from auxiliary file

    Parameters
    ----------
    logger (Logger): logger object
    shc List[SHObject]: List of spherical harmonic objects.
    filename_replacements (str): path and filename to the file containing the replacements for the low degree harmonics

    Returns
    -------
    List[SHObject]
    """
    dates_replacement, c20, c21, s21, c30 = rd.read_lowdegree_coefficients(file_name=filename_replacements)
    dates_replacement_dt = [_to_datetime(d) for d in dates_replacement]
    dates = np.array([s.date for s in shc])
    dates_dt = [_to_datetime(d) for d in dates]

    shc_replaced = shc.copy()

    for i in range(len(dates)):
        index_dates = _get_nearest_date(logger, dates_dt[i], dates_replacement_dt)
        shc_replaced[i].cnm[2, 0] = c20[index_dates]

        if dt.datetime(2016, 11, 1) <= dates_dt[i] <= dt.datetime(2017, 6, 30):
            shc_replaced[i].cnm[3, 0] = c30[index_dates]

    return shc_replaced


def _get_nearest_date(logger: Logger,
                      d_target: dt.date | dt.datetime,
                      dates: np.ndarray[dt.date] | np.ndarray[dt.datetime]) -> int:
    """
    Return the index of the date closest to `d_target`.

    Raises a warning if multiple dates are equally close.
    """
    target_dt = _to_datetime(d_target)
    dates_dt = [_to_datetime(d) for d in dates]

    # Compute absolute differences (timedelta)
    diffs = [abs(d - target_dt) for d in dates_dt]

    # Find the minimum difference
    min_diff = min(diffs)

    if min_diff > dt.timedelta(days=17):
        message = f"Closest date is {min_diff.days} days away from target ({target_dt})."
        logger.error(message)
        raise ValueError(message)

    # Find all indices that have this minimum difference
    closest_indices = [i for i, diff in enumerate(diffs) if diff == min_diff]

    # Warn if there's a tie
    if len(closest_indices) > 1:
        message = (f"In replacement of low degree harmonics: Multiple dates are equally close to {target_dt}. "
                   f"Using the first (index {closest_indices[0]}).")
        logger.warning(message)

    return closest_indices[0]


def _to_datetime(d):
    """Convert date to datetime if necessary."""
    return dt.datetime.combine(d, dt.datetime.min.time()) if (isinstance(d, dt.date)
                                                              and not isinstance(d, dt.datetime)) else d
