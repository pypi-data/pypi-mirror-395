# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Module to handle Legendre polynomials."""
import math
from logging import Logger

import numpy as np


def legendre(logger: Logger, lmax: int, lat_rows: int, sin_lat: np.ndarray) -> np.ndarray:
    """
    Compute fully normalized associated Legendre polynomials.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    lmax : int
        Maximum spherical harmonic degree.
    lat_rows : int
        Number of nodal rows in latitude.
    sin_lat : np.ndarray
        Array of sin(latitude) values, shape (lat_rows,).

    Returns
    -------
    np.ndarray
        Fully normalized associated Legendre functions with shape
        (lmax+1, lmax+1, lat_rows), where result[l, m, j] = P̄_lm(sin_lat[j]).
    """
    polynomials = np.zeros((lmax + 1, lmax + 1, lat_rows), dtype=np.float64)

    for j, s in enumerate(sin_lat):
        pp = legendre_normalized(logger=logger, lmax=lmax, z=s)
        for n in range(lmax + 1):
            for m in range(n + 1):
                idx = n * (n + 1) // 2 + m
                polynomials[n, m, j] = pp[idx]

    return polynomials


def legendre_normalized(logger: Logger, lmax: int, z: float) -> np.ndarray:
    """
    Calculate and returns legendre functions not polynomials.

    Fully normalized associated Legendre functions P̄_lm(z) up to degree lmax
    (geophysical convention, no rescaling) based on Holmes & Featherstone
    (2002, 10.1007/s00190-002-0216-2) (Eqs. 11 & 12).

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    lmax : int
        Maximum degree.
    z : float
        Argument, cos(colatitude) or sin(latitude), must be in [-1, 1].

    Returns
    -------
    np.ndarray
        Shape (lmax+1, lmax+1), where result[l_var, m] = P̄_l^m(z).
        Entries with m > l_var are zero.
    """
    if not -1.0 <= z <= 1.0:
        message = "z must be in [-1, 1]"
        logger.error(message)
        raise ValueError(message)

    phase = 1.0
    # scaling factors to prevent over- / underflow. See Holmes & Featherstone Sec. 2.7. Allows computation up to 2700.
    tiny_scale = 1.0e-280

    # Precompute square roots, with zero-indexing there is a shift between index and the associated sqr by one!
    sqr = np.sqrt(np.arange(1, 2 * lmax + 2, dtype=np.float64))

    # Precompute recursion coefficients, index of the array corresponds to l*(l+1)/2 + m
    f1 = np.zeros((lmax + 1) * (lmax + 2) // 2, dtype=np.float64)
    f2 = np.zeros_like(f1)

    k = 3
    for n in range(2, lmax + 1):
        k += 1
        f1[k - 1] = sqr[2 * n - 2] * sqr[2 * n] / n
        f2[k - 1] = (n - 1) * sqr[2 * n] / (sqr[2 * n - 4] * n)
        for m in range(1, n - 1):
            k += 1
            dbl_l = 2 * n
            m_plus, m_minus = n + m - 1, n - m - 1
            f1[k - 1] = sqr[dbl_l] * sqr[dbl_l - 2] / (sqr[m_plus] * sqr[m_minus])
            f2[k - 1] = (
                sqr[dbl_l]
                * sqr[m_minus - 1]
                * sqr[m_plus - 1]
                / (sqr[dbl_l - 4] * sqr[m_plus] * sqr[m_minus])
            )
        k += 2

    # Allocate results
    p = np.full((lmax + 1) * (lmax + 2) // 2, np.nan, dtype=np.float64)

    # Base cases P(0,0), P(1,0)
    p[0] = 1.0
    p[1] = sqr[2] * z

    # Recursion for P(l,0)
    k = 1
    for n in range(2, lmax + 1):
        k += n
        p[k] = f1[k] * z * p[k - n] - f2[k] * p[k - 2 * n + 1]

    # General case: P(m,m), P(m+1,m), and P(l,m)
    u = math.sqrt(1.0 - z * z)  # z=cos(colat) -> u=sqrt(1-z**2)=sin(colat)
    pmm = sqr[1] * tiny_scale
    rescale = 1.0 / tiny_scale
    kstart = 0

    for m in range(1, lmax):
        rescale *= u
        kstart += m + 1
        # P(m,m), this value is used unscaled in the for loop below and then gets modified with the
        # scaling factor and sin(colat) below as well.
        pmm = phase * pmm * sqr[2 * m] / sqr[2 * m - 1]
        p[kstart] = pmm

        # P(m+1,m)
        k = kstart + m + 1
        p[k] = z * sqr[2 * m + 2] * pmm

        # P(l,m), l >= m+2
        for n in range(m + 2, lmax + 1):
            k += n
            p[k] = z * f1[k] * p[k - n] - f2[k] * p[k - 2 * n + 1]
            p[k - 2 * n + 1] *= rescale

        p[k] *= rescale
        p[k - lmax] *= rescale

    # Final case P(lmax,lmax)
    rescale *= u
    kstart += lmax + 1

    p[kstart] = phase * pmm * sqr[2 * lmax] / sqr[2 * lmax - 1] * rescale

    return p
