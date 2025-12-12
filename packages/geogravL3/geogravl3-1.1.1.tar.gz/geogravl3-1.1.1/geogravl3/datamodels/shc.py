#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Data representations for spherical harmonic coefficients."""

import datetime as dt
from logging import Logger

import numpy as np


class SHObject:
    """
    Represents spherical harmonic coefficients and associated metadata.

    Attributes
    ----------
    date : dt.date
        The date corresponding to the data, derived from the file header.
    cnm : np.ndarray
        A 2D array containing the C_nm coefficients (cosine terms).
    snm : np.ndarray
        A 2D array containing the S_nm coefficients (sine terms).
    """

    def __init__(self, logger: Logger, date: dt.date, cnm: np.ndarray, snm: np.ndarray):
        """
        Initialize an SHObject instance with spherical harmonic coefficients and metadata.

        Args:
            logger (Logger): Logger instance for logging information and debugging messages.
            date (dt.date): The date corresponding to the data, typically derived from the file header.
            cnm (np.ndarray): A 2D array containing the C_nm coefficients (cosine terms).
            snm (np.ndarray): A 2D array containing the S_nm coefficients (sine terms).

        Attributes:
            date (dt.date): The date of the data.
            cnm (np.ndarray): The cosine terms of the spherical harmonic coefficients.
            snm (np.ndarray): The sine terms of the spherical harmonic coefficients.

        Raises:
            ValueError: If the dimensions are not fitting together
        """
        if cnm.shape != snm.shape:
            message = "cnm and snm do not have the same dimensions"
            logger.error(message)
            raise ValueError(message)

        self.date = date
        self.cnm = cnm
        self.snm = snm

    def get_max_degree(self) -> int:
        """
        Return the maximum degree and order of the stored cnm/snm.

        Returns
        -------
        max_degree (int): taken from shape of cnm
        """
        return int(self.cnm.shape[0] - 1)
