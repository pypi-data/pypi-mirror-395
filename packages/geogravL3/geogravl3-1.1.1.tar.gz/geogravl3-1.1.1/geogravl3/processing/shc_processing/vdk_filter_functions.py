#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""VDK filter module for geogravL3 package."""

from logging import Logger

import pandas as pd
import numpy as np

from geogravl3.datamodels.shc import SHObject
from geogravl3.io.readers import parse_sinex_sections, read_sinex_data


def _build_CS_matrices(df: pd.DataFrame, n_max: int):
    """
    Build the filtered cnm and snm spherical harmonic coefficient matrices.

    Args:
        df_filt (pd.DataFrame): DataFrame with columns ['type', 'degree', 'order', 'filtered_value'].
        n_max (int): Maximum spherical harmonic degree/order.

    Returns:
        tuple: (cnm, snm) as NumPy arrays of shape (DO+1, DO+1).
    """
    cnm = np.zeros((n_max + 1, n_max + 1))
    snm = np.zeros((n_max + 1, n_max + 1))

    # Convert to numpy arrays
    deg = df["degree"].to_numpy(int)
    ord_ = df["order"].to_numpy(int)
    typ = df["type"].to_numpy(str)
    val = df["value"].to_numpy(float)

    # Masks for CN and SN
    mask_cn = typ == "CN"
    mask_sn = ~mask_cn

    # Vectorized assignment
    cnm[deg[mask_cn], ord_[mask_cn]] = val[mask_cn]
    snm[deg[mask_sn], ord_[mask_sn]] = val[mask_sn]

    return cnm, snm


def _shObject_vector(shc: SHObject, degree: pd.Series, order: pd.Series, type_: pd.Series) -> np.ndarray:
    """
    Vectorized the sh coefficients to be filtered.

    Parameters
    ----------
    shc (SHObject): Object storing the SH coefficients
    degree (pd.Series): containing the degrees of each element of the vectorized SH coefficients
    order (pd.Series): containing the orders of each element of the vectorized SH coefficients
    type_ (pd.Series): containing the type of each element of the vectorized SH coefficients

    Returns
    -------
    shc_vectorized (np.ndarray): vectorized sh coefficients

    """
    degree = np.asarray(degree, int)
    order = np.asarray(order, int)
    type_ = np.asarray(type_, str)

    shc_vectorized = np.empty_like(degree, dtype=float)
    mask_cn = type_ == 'CN'
    mask_sn = ~mask_cn

    shc_vectorized[mask_cn] = shc.cnm[degree[mask_cn], order[mask_cn]]
    shc_vectorized[mask_sn] = shc.snm[degree[mask_sn], order[mask_sn]]
    return shc_vectorized


def _build_normal_matrix(df_NEQM, nou):
    """
    Construct the full normal equation matrix from SINEX NEQM section.

    Args:
        df_NEQM (pd.DataFrame): DataFrame of the NEQM section.
        nou (int): Number of unknowns.

    Returns:
        np.ndarray: Full symmetric normal equation matrix.
    """
    N = np.zeros((nou, nou))
    snx_array = df_NEQM.iloc[:, 2:].to_numpy()

    for snx_i, (i, j) in enumerate(zip(df_NEQM["PARA1"] - 1, df_NEQM["PARA2"] - 1)):
        slice_end = min(j + 3, nou)
        N[i, j:slice_end] = snx_array[snx_i, :slice_end - j]

    np.nan_to_num(N, copy=False)
    N_full = N.T + N
    np.fill_diagonal(N_full, np.diag(N))
    return N_full


def _generate_kaula_matrix(degrees, a, b):
    """
    Generate a diagonal Kaula rule-based signal variance matrix.

    Args:
        degrees (np.ndarray): Degrees of spherical harmonics.
        a (float): Kaula coefficient.
        b (float): Kaula exponent.

    Returns:
        np.ndarray: Diagonal matrix with Kaula variances.
    """
    M_vector = a * degrees ** -b
    return M_vector  # np.diag(M_vector)


def vdk(logger: Logger,
        shc: SHObject,
        path_snx: str,
        alpha: float,
        variance_method: str = "Kaula",
        a: float = 1.0,
        b: float = -4.0,
        M: np.ndarray = None) -> SHObject:
    """
    Apply the VDK filter to SINEX normal equation data and returns filtered C and S coefficients.

    Args:
        logger (Logger): logger object to log the error messages
        shc (SHObject): spherical harmonic object. With attributes:
                        - date
                        - cnm: cosine coefficients (array of shape (lmax+1, lmax+1))
                        - snm: sine coefficients (same shape)
        path_snx (str): Path to the SINEX normal equation file.
        alpha (float): Regularization parameter for the VDK filter. Higher values apply stronger filtering.
        variance_method (str): Method for computing signal variance. Defaults to "Kaula".
        a (float): Coefficient "a" in the Kaula rule (used when varianceMethod="Kaula").
        b (float): Exponent "b" in the Kaula rule (used when varianceMethod="Kaula").
        M (np.ndarray, optional): Pre-defined signal variance matrix.
                                If None and varianceMethod is "Kaula", it is calculated.

    Returns:
        SHObject: Representing the filtered sh coefficients

    Example:
        C, S = vdk("path/to/sinex.snx", alpha=1e5)
    """
    section_lines = parse_sinex_sections(path_snx)

    sinex_data = read_sinex_data(logger=logger,
                                 path=path_snx,
                                 sections=section_lines)

    df_apriori = sinex_data['apriori']
    df_estimate = sinex_data['estimate']
    nou = sinex_data['nou']
    df_NEQM = sinex_data['neq_matrix']
    date = sinex_data['date']
    max_deg = sinex_data['max_degree']
    x_raw = _shObject_vector(shc=shc,
                             degree=df_estimate["degree"],
                             order=df_estimate["order"],
                             type_=df_estimate["type"])

    if variance_method == "Kaula" and M is None:
        mdiag = _generate_kaula_matrix(df_apriori["degree"].values, a, b)
        M = np.diag(mdiag)

    N_full = _build_normal_matrix(df_NEQM=df_NEQM, nou=nou)

    logger.info("Calculating filter matrix")
    reg_matrix = N_full + alpha * M
    reg_matrix_inv = np.linalg.inv(reg_matrix)
    W = reg_matrix_inv @ N_full
    x_filt = W @ x_raw

    df_filt = pd.DataFrame({
        "type": df_estimate["type"],
        "degree": df_estimate["degree"],
        "order": df_estimate["order"],
        "value": x_filt
    })

    C, S = _build_CS_matrices(df_filt, max_deg)
    return SHObject(logger=logger, cnm=C, snm=S, date=date)
