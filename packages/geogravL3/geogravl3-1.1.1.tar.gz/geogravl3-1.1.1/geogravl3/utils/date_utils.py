# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Date Utils module."""

import calendar
import datetime as dt
from logging import Logger
from typing import Dict, Union
import re

import numpy as np


def datetime_to_date_float(date_input):
    """
    Convert a date or datetime object (or list/array of them) to a float representing the decimal year format.

    Parameters:
    -----------
    date_input : datetime.date, datetime.datetime, list, or numpy.ndarray
        A single datetime object or a list/array of datetime.date or datetime.datetime objects.

    Returns:
    --------
    float or numpy.ndarray
        A float or NumPy array of floats representing the date(s) in decimal year format.
        Example: 2025-07-01 → 2025.4986
    """

    def to_float(d):
        year = d.year
        day_of_year = d.timetuple().tm_yday
        days_in_year = 366 if calendar.isleap(year) else 365
        return year + (day_of_year - 1) / days_in_year

    if isinstance(date_input, (list, np.ndarray)):
        return np.array([to_float(d) for d in date_input])
    else:
        return to_float(date_input)


def date_float_to_datetime(float_input):
    """
    Convert a float or list/array of floats in decimal year format back to a datetime.date object.

    Parameters:
    -----------
    float_input : float, list, or numpy.ndarray
        A single float or a list/array of floats representing the fractional year.
        Example: 2025.4986 → ~2025-07-01

    Returns:
    --------
    dat.date or numpy.ndarray
        A dt.date object (or NumPy array of them) corresponding to the float input.
        The result is rounded to the nearest calendar day.
    """

    def from_float(f):
        year = int(f)
        fraction = f - year
        days_in_year = 366 if calendar.isleap(year) else 365
        day_of_year = int(round(fraction * days_in_year)) + 1
        return dt.date(year, 1, 1) + dt.timedelta(days=day_of_year - 1)

    if isinstance(float_input, (list, np.ndarray)):
        return np.array([from_float(f) for f in float_input])
    else:
        return from_float(float_input)


def datetime_from_nc_time(logger: Logger, time_values: Union[np.ndarray, list, float], time_attributes: Dict) \
        -> Union[np.ndarray, dt.date]:
    """
    Return the time variable read from a netcdf file in common datetime format.

    Parameters
    ----------
    logger (Logger): logger object to log the error messages
    time_values(Union[np.ndarray, list, float]): Either array, list, or float of the time value(s)
    time_attributes (Dict): Attribute list returned by read_nc function of the time variable

    Returns
    -------
    array of or single datetime object

    """

    def transform(time_value: float, time_attributes: Dict) -> dt.date:
        if 'days since' in time_attributes['units']:
            time_units_split = re.split(r' |-|T', time_attributes['units'])
            start_date = dt.date(int(time_units_split[2]), int(time_units_split[3]), int(time_units_split[4]))
            date = start_date + dt.timedelta(int(time_value))
        elif 'day as %Y%m%d.%f' in time_attributes['units']:
            year_t = int(np.floor(time_value / 10000))
            month_t = int(np.floor((time_value - year_t * 10000) / 100))
            day_t = int(np.floor((time_value - year_t * 10000 - month_t * 100)))
            date = dt.date(year_t, month_t, day_t)
        else:
            message = ('Unknown time definition in netcdf file. '
                       'Only "days since refdate" and "day as %Y%m%d.%f" covered')
            logger.error(message)
            raise ValueError(message)
        return date

    if isinstance(time_values, (list, np.ndarray)):
        return np.array([transform(f, time_attributes) for f in time_values])
    else:
        return transform(time_values, time_attributes)


def dates_to_days_since_ref(dates, ref: str = "2002-04-18") -> np.ndarray:
    """Convert a sequence of dates into days since a reference date.

    Parameters
    ----------
    dates : sequence of datetime.date or datetime.datetime
        The dates to convert.
    ref : str, optional
        Reference date in ISO format (YYYY-MM-DD). Default is "2002-04-18".

    Returns
    -------
    np.ndarray
        Array of days since the reference date.
    """
    ref_date = dt.datetime.strptime(ref, "%Y-%m-%d").date()
    return np.array([(d.date() - ref_date if isinstance(d, dt.datetime) else d - ref_date).days
                     if isinstance(d, (dt.datetime, dt.date)) else None
                     for d in dates])


def reference_period_2_datetime(ref_period: str) -> np.ndarray[dt.date]:
    """
    Convert string to datetime for reference period.

    Parameters
    ----------
    ref_period (str): as provided from the config file

    Returns
    -------
    np.ndarray: reference period given as array of datetime objects

    """
    # Pattern for a single month: "YYYY/MM"
    single_pattern = re.compile(r"^(\d{4})/(\d{2})$")
    # Pattern for a range: "YYYY/MM-YYYY/MM"
    range_pattern = re.compile(r"^(\d{4})/(\d{2})-(\d{4})/(\d{2})$")

    m_single = single_pattern.fullmatch(ref_period)
    if m_single:
        year = int(m_single.group(1))
        month = int(m_single.group(2))
        return np.array([dt.date(year, month, 15)])

    m_range = range_pattern.fullmatch(ref_period)
    if m_range:
        year1 = int(m_range.group(1))
        month1 = int(m_range.group(2))
        year2 = int(m_range.group(3))
        month2 = int(m_range.group(4))
        return np.array([dt.date(year1, month1, 15), dt.date(year2, month2, 15)])
    return None
