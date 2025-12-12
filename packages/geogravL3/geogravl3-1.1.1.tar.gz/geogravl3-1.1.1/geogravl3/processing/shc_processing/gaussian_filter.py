#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Gaussian filtering functions for geogravL3 package."""
import numpy as np

from ...utils.utils import get_constant


def filt_gaussian(lmax: int, radius: float):
    """
    Compute Gaussian smoothing weights.

    Parameters
    ----------
    lmax : int
        Maximum spherical harmonic degree.
    radius : float
        Gaussian radius (km).

    Returns
    -------
    gaussian_weights : np.ndarray
        Gaussian weights for degrees 0..Lmax.
    """
    gaussian_weights = np.zeros(lmax + 1)
    if radius == 0:
        gaussian_weights[:] = 1.0 / (2.0 * np.pi)
        return gaussian_weights

    gb = 0.693147181 / (1 - np.cos(radius * 1000.0 / get_constant("earths_radius_iers")))  # ln(2)
    gaussian_weights[0] = 1.0 / (2.0 * np.pi)
    gaussian_weights[1] = (1.0 / (2.0 * np.pi)) * (((1 + np.exp(-2 * gb)) / (1 - np.exp(-2 * gb))) - 1.0 / gb)

    for n in range(1, lmax):
        gaussian_weights[n + 1] = gaussian_weights[n - 1] - ((2 * n + 1) / gb) * gaussian_weights[n]
        if gaussian_weights[n + 1] < 0:
            gaussian_weights[n + 1] = 0.0
            break

    return gaussian_weights
