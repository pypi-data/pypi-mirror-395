# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam

"""Provide all-in-one time-series deseasoning utilities.

This module fits and removes mean, trend, annual, and semiannual components from 1-D time
series, and applies the same logic to grids and spherical-harmonic (SH) coefficient arrays.
It supports both windowed fits (populate results only inside the fit window) and subset-fit
full-apply behavior (fit on a window and evaluate over the full time axis).
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from logging import Logger
from typing import Any, Dict, Optional, Tuple, Union
import datetime as dt

import numpy as np

from ..datamodels.grids import Grid3DObject, Grid3DIceObject
from ..datamodels.shc import SHObject
from ..utils.utils import get_constant
from ..utils.date_utils import datetime_to_date_float

__all__ = [
    "year_days",
    "twopi",
    "FitConfig",
    "fit_harmonics",
    "remove_harmonic_components_windowed",
    "deseason_series_windowed",
    "remove_harmonic_components_extrapolate",
    "apply_harmonic_components_grid",
    "apply_harmonic_components_sh",
    "remove_mean",
    "remove_mean_grid",
    "remove_mean_sh",
    "gaussian_filter_series",
    "gaussian_filter_grid",
    "gaussian_filter_sh",
]

year_days = 365.2422
twopi = 2.0 * np.pi


# -------------------------------
# Config and design matrix helpers
# -------------------------------


@dataclass
class FitConfig:
    """Flags to include or exclude deterministic components.

    Parameters
    ----------
    include_mean : bool, default=True
        Constant offset term.
    trend : bool, default=True
        Linear trend term.
    annual : bool, default=True
        Annual cosine and sine harmonics.
    semiannual : bool, default=True
        Semiannual cosine and sine harmonics.
    quadratic : bool, default=False
        Quadratic trend term (years²/2).
    period161_cos : bool, default=False
        Cosine harmonic with 161-day period.
    period161_sin : bool, default=False
        Sine harmonic with 161-day period.
    """

    include_mean: bool = True
    trend: bool = True
    annual: bool = True
    semiannual: bool = True
    quadratic: bool = False
    period161_cos: bool = False
    period161_sin: bool = False


def _num_params(cfg: FitConfig) -> int:
    p = 0
    if cfg.include_mean:
        p += 1
    if cfg.trend:
        p += 1
    if cfg.annual:
        p += 2
    if cfg.semiannual:
        p += 2
    if cfg.quadratic:
        p += 1
    if cfg.period161_cos:
        p += 1
    if cfg.period161_sin:
        p += 1
    return p


def _design_matrix(
    logger: Logger,
    t: np.ndarray,
    cfg: FitConfig,
    *,
    t_center: Optional[float] = None,
) -> np.ndarray:
    """Build the design matrix for the selected components.

    Parameters
    ----------
    logger (Logger): Logger instance for logging information and debugging messages.
    t
        Time in date float (shape (N,)).
    cfg
        Component selection flags.
    t_center
        Reference time (days) used to center the trend term for numerical conditioning.

    Returns
    -------
    np.ndarray
        Design matrix with shape (N, P), where:
        - N is the number of time samples (len(t)).
        - P is the number of model components included according to `cfg`.
    """
    t = np.asarray(t, dtype=float)
    cols = []

    if cfg.include_mean:
        cols.append(np.ones_like(t))

    if cfg.trend:
        if t_center is None or not np.isfinite(t_center):
            t_center = float(np.nanmean(t))
        cols.append(t - t_center)

    if cfg.quadratic:
        if t_center is None or not np.isfinite(t_center):
            t_center = float(np.nanmean(t))
        cols.append(0.5 * (t - t_center) ** 2)

    if cfg.annual:
        w1 = twopi
        cols.append(np.cos(w1 * t))
        cols.append(np.sin(w1 * t))

    if cfg.semiannual:
        w2 = twopi * 2.0
        cols.append(np.cos(w2 * t))
        cols.append(np.sin(w2 * t))

    if cfg.period161_cos or cfg.period161_sin:
        w161 = twopi * (year_days / 161.0)
        if cfg.period161_cos:
            cols.append(np.cos(w161 * t))
        if cfg.period161_sin:
            cols.append(np.sin(w161 * t))

    if not cols:
        message = "'_design_matrix': Design matrix would be empty (no components selected)."
        logger.error(message)
        raise ValueError(message)

    return np.column_stack(cols)


def _solve_lstsq(
    logger: Logger,
    X: np.ndarray,
    y: np.ndarray,
    w: Optional[np.ndarray] = None,
    C: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Solve an ordinary, weighted, or generalized least squares problem.

    Parameters
    ----------
    logger (Logger): Logger instance for logging information and debugging messages.
    X : np.ndarray
        Design matrix with shape (Nv, P).
    y : np.ndarray
        Observation vector with shape (Nv,).
    w : np.ndarray, optional
        Weights applied to the observations (shape (Nv,)). Interpreted as the
        inverse of the standard deviation for each observation. Mutually
        exclusive with `C`.
    C : np.ndarray, optional
        Full covariance matrix of the observations with shape (Nv, Nv).
        If provided, generalized least squares is solved. Mutually exclusive
        with `w`.

    Returns
    -------
    np.ndarray
        Estimated model parameters with shape (P,).
    """
    if w is not None and C is not None:
        message = "'_solve_lstsq': Provide either weights `w` or covariance `C`, not both."
        logger.error(message)
        raise ValueError(message)

    if C is not None:
        # Generalized least squares: solve (X^T C^-1 X) beta = X^T C^-1 y
        Cinv = np.linalg.inv(C)
        Xt_Cinv = X.T @ Cinv
        beta = np.linalg.solve(Xt_Cinv @ X, Xt_Cinv @ y)
    elif w is not None:
        if np.any(~np.isfinite(w)):
            message = "'_solve_lstsq': Weights contain non-finite values after masking."
            logger.error(message)
            raise ValueError(message)

        if np.any(w < 0):
            message = "'_solve_lstsq': Weights must be non-negative."
            logger.error(message)
            raise ValueError(message)
        sw = np.sqrt(w)
        beta, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    else:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def _amplitude_phase_from_beta(
    beta: np.ndarray,
    cfg: FitConfig,
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """Extract amplitude and phase for present harmonics from the coefficient vector.

    The phase convention is: if the harmonic term is ``A*cos(w t) + B*sin(w t)``, then we
    report ``R = hypot(A, B)`` and ``phi = atan2(-B, A)`` so the term may be written as
    ``R * cos(w t + phi)``.
    """
    amp: Dict[str, float] = {}
    ph: Dict[str, float] = {}

    k = 0
    if cfg.include_mean:
        k += 1
    if cfg.trend:
        k += 1

    if cfg.annual:
        if k + 1 < beta.size:
            A1, B1 = float(beta[k]), float(beta[k + 1])
            amp["annual"] = float(np.hypot(A1, B1))
            ph["annual"] = float(np.arctan2(-B1, A1))
        k += 2

    if cfg.semiannual:
        if k + 1 < beta.size:
            A2, B2 = float(beta[k]), float(beta[k + 1])
            amp["semiannual"] = float(np.hypot(A2, B2))
            ph["semiannual"] = float(np.arctan2(-B2, A2))
        k += 2

    return amp, ph


def _date_to_index(logger: Logger, times: np.ndarray, d: Union[int, dt.date]) -> int:
    """Convert either an integer index or a datetime.date into an index for times."""
    if isinstance(d, int):
        return d
    elif isinstance(d, dt.date):
        tval = datetime_to_date_float(d)
        return int(np.argmin(np.abs(times - tval)))
    else:
        message = f"Expected int or datetime.date in '_date_to_index', got {type(d)}"
        logger.error(message)
        raise ValueError(message)


# -----------------
# Core 1-D routines
# -----------------


def fit_harmonics(
    logger: Logger,
    t: np.ndarray,
    y: np.ndarray,
    cfg: Optional[FitConfig] = None,
    weights: Optional[np.ndarray] = None,
) -> Dict[str, np.ndarray]:
    """Fit mean, trend, harmonic and quadratic components by (weighted) least squares."""
    cfg = cfg or FitConfig()

    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)

    mask_valid = np.isfinite(t) & np.isfinite(y)
    w_valid = None
    if weights is not None:
        weights = np.asarray(weights, dtype=float)
        mask_valid &= np.isfinite(weights)
        w_valid = weights[mask_valid]

    t_valid = t[mask_valid]
    y_valid = y[mask_valid]

    Nv = t_valid.size
    P = _num_params(cfg)

    if Nv < P:
        message = (f"Insufficient observations for fitting the harmonic signals: Nv={Nv} < P={P}. "
                   "At least as many observations as parameters are required.")
        logger.error(message)
        raise ValueError(message)

    if Nv == 0:
        n = y.size
        return {
            "beta": np.array([]),
            "y_fit": np.full(n, np.nan, float),
            "y_resid": np.full(n, np.nan, float),
            "X": np.empty((0, 0)),
            "cfg": cfg,
            "mask_valid": mask_valid,
            "amplitude": {},
            "phase": {}, f"Insufficient observations: Nv={Nv} < P={P}. "
                         "At least as many observations as parameters are required."
                         "t_center": np.nan,
            "coefficients": {},
        }

    t_center = float(np.nanmean(t_valid))
    X = _design_matrix(logger=logger, t=t_valid, cfg=cfg, t_center=t_center)
    beta = _solve_lstsq(logger=logger, X=X, y=y_valid, w=w_valid)

    y_fit_valid = X @ beta
    y_resid_valid = y_valid - y_fit_valid

    y_fit = np.full_like(y, np.nan, dtype=float)
    y_resid = np.full_like(y, np.nan, dtype=float)
    y_fit[mask_valid] = y_fit_valid
    y_resid[mask_valid] = y_resid_valid

    amplitude, phase = _amplitude_phase_from_beta(beta, cfg)

    # Build dictionary of named coefficients
    coeffs: Dict[str, float] = {}
    k = 0
    if cfg.include_mean:
        coeffs["mean"] = float(beta[k])
        k += 1
    if cfg.trend:
        coeffs["trend"] = float(beta[k])
        k += 1
    if cfg.annual:
        coeffs["annual_cos"] = float(beta[k])
        coeffs["annual_sin"] = float(beta[k + 1])
        k += 2
    if cfg.semiannual:
        coeffs["semiannual_cos"] = float(beta[k])
        coeffs["semiannual_sin"] = float(beta[k + 1])
        k += 2
    if cfg.quadratic:
        coeffs["quadratic"] = float(beta[k])
        k += 1
    if cfg.period161_cos:
        coeffs["period161_cos"] = float(beta[k])
        k += 1
    if cfg.period161_sin:
        coeffs["period161_sin"] = float(beta[k])
        k += 1

    return {
        "beta": beta,
        "y_fit": y_fit,
        "y_resid": y_resid,
        "X": X,
        "cfg": cfg,
        "mask_valid": mask_valid,
        "amplitude": amplitude,
        "phase": phase,
        "t_center": t_center,
        "coefficients": coeffs,
    }


def remove_harmonic_components_windowed(
    logger: Logger,
    t: np.ndarray,
    y: np.ndarray,
    cfg: Optional[FitConfig] = None,
    weights: Optional[np.ndarray] = None,
    mode: str = "remove",
) -> Dict[str, Union[np.ndarray, Dict[str, np.ndarray]]]:
    """Wrap ``fit_harmonics`` and return output based on the selected mode."""
    res = fit_harmonics(logger=logger, t=t, y=y, cfg=cfg, weights=weights)
    if mode == "remove":
        res["output"] = res["y_resid"]
    elif mode == "fit":
        res["output"] = res["y_fit"]
    elif mode == "harmonics":
        res["output"] = {
            "beta": res["beta"],
            "amplitude": res["amplitude"],
            "phase": res["phase"],
        }
    else:
        message = (
            f"Weights in 'remove_harmonic_components_windowed' must match the shape of data for "
            f"extrapolate mode (same length as data). "
            f"Length of weights: {weights.shape}, length data: {y.shape}"
        )
        logger.error(message)
        raise ValueError(message)
    return res


def deseason_series_windowed(
    logger: Logger,
    times: np.ndarray,
    data: np.ndarray,
    *,
    components: Optional[FitConfig] = None,
    start_idx: Optional[Union[int, dt.date]] = None,
    end_idx: Optional[Union[int, dt.date]] = None,
    mode: str = "remove",
    weights: Optional[np.ndarray] = None,
) -> Dict[str, Union[np.ndarray, Dict[str, np.ndarray], Tuple[int, int]]]:
    """Fit and remove components only inside the window and leave NaN elsewhere."""
    t = np.asarray(times, dtype=float)
    y = np.asarray(data, dtype=float)
    n = y.size

    s = 0 if start_idx is None else _date_to_index(logger=logger, times=times, d=start_idx)
    e = n if end_idx is None else _date_to_index(logger=logger, times=times, d=end_idx)
    if not (0 <= s <= e <= n):
        message = (f"Invalid bounds for deseasoning on subset of time series "
                   f"with start: {start_idx}, end: {end_idx} and length timeseries: {n}")
        logger.error(message)
        raise ValueError(message)

    cfg = components or FitConfig()
    w_sub = None
    if weights is not None:
        weights = np.asarray(weights, dtype=float)
        if weights.shape != y.shape:
            message = (
                f"Weights in 'deseason_series_windowed' must match the shape of data for "
                f"extrapolate mode (same length as data). "
                f"Length of weights: {weights.shape}, length data: {y.shape}"
            )
        w_sub = weights[s:e + 1]

    sub = remove_harmonic_components_windowed(logger=logger,
                                              t=t[s:e + 1],
                                              y=y[s:e + 1],
                                              cfg=cfg,
                                              weights=w_sub,
                                              mode=mode)

    y_fit_full = np.full(n, np.nan, float)
    y_resid_full = np.full(n, np.nan, float)
    if isinstance(sub.get("y_fit"), np.ndarray):
        y_fit_full[s:e + 1] = sub["y_fit"]
    if isinstance(sub.get("y_resid"), np.ndarray):
        y_resid_full[s:e + 1] = sub["y_resid"]

    if mode == "remove":
        output_full: Union[np.ndarray, Dict[str, np.ndarray]] = y_resid_full
    elif mode == "fit":
        output_full = y_fit_full
    elif mode == "harmonics":
        output_full = sub["output"]
    else:
        message = (
            f"Weights in 'deseason_series_windowed' must match the shape of data for "
            f"extrapolate mode (same length as data). "
            f"Length of weights: {weights.shape}, length data: {y.shape}"
        )
        logger.error(message)
        raise ValueError(message)
    sub.update(
        {
            "y_fit_full": y_fit_full,
            "y_resid_full": y_resid_full,
            "output_full": output_full,
            "fit_window": (s, e),
        }
    )
    return sub


def remove_harmonic_components_extrapolate(
    logger: Logger,
    times: np.ndarray,
    data: np.ndarray,
    *,
    components: Optional[FitConfig] = None,
    start_idx: Optional[Union[int, dt.date]] = None,
    end_idx: Optional[Union[int, dt.date]] = None,
    mode: str = "remove",
    weights: Optional[np.ndarray] = None
) -> Dict[str, Union[np.ndarray, Dict[str, np.ndarray], Tuple[int, int]]]:
    """Fit on a window and then evaluate across the full time span."""
    t = np.asarray(times, dtype=float)
    y = np.asarray(data, dtype=float)
    n = y.size

    s = 0 if start_idx is None else _date_to_index(logger=logger, times=times, d=start_idx)
    e = n if end_idx is None else _date_to_index(logger=logger, times=times, d=end_idx)
    if not (0 <= s <= e <= n):
        message = (f"Invalid bounds for estimation of harmonic components on subset of time series "
                   f"with start: {start_idx}, end: {end_idx} and length timeseries: {n}")
        logger.error(message)
        raise ValueError(message)

    cfg = components or FitConfig()
    w_sub = None
    if weights is not None:
        weights = np.asarray(weights, dtype=float)
        if weights.shape != y.shape:
            message = (
                f"Weights in 'remove_harmonic_components_extrapolate' must match the shape of data for "
                f"extrapolate mode (same length as data). "
                f"Length of weights: {weights.shape}, length data: {y.shape}"
            )
            logger.error(message)
            raise ValueError(message)
        w_sub = weights[s:e + 1]

    fit = fit_harmonics(logger=logger, t=t[s:e + 1], y=y[s:e + 1], cfg=cfg, weights=w_sub)
    beta = fit["beta"]
    t_center = fit["t_center"]
    mask_valid_window = fit["mask_valid"]

    if beta.size:
        fin_t = np.isfinite(t)
        y_fit_full = np.full(n, np.nan, float)
        X_full = _design_matrix(logger=logger, t=t[fin_t], cfg=cfg, t_center=t_center)
        y_fit_full[fin_t] = X_full @ beta
    else:
        y_fit_full = np.full(n, np.nan, float)

    y_resid_full = y - y_fit_full

    if mode == "remove":
        output_full: Union[np.ndarray, Dict[str, np.ndarray]] = y_resid_full
    elif mode == "fit":
        output_full = y_fit_full
    elif mode == "harmonics":
        amp, ph = fit["amplitude"], fit["phase"]
        output_full = {"beta": beta, "amplitude": amp, "phase": ph}
    else:
        message = (f"mode provided in 'remove_harmonic_components_extrapolate' must be one of: "
                   f"'remove', 'fit', 'harmonics'. "
                   f"Provided: {mode}")
        logger.error(message)
        raise ValueError(message)

    return {
        "beta": beta,
        "amplitude": fit["amplitude"],
        "phase": fit["phase"],
        "t_center": t_center,
        "mask_valid_window": mask_valid_window,
        "y_fit_full": y_fit_full,
        "y_resid_full": y_resid_full,
        "output_full": output_full,
        "fit_window": (s, e),
    }


def apply_harmonic_components_grid(
    logger: Logger,
    grid3d: Union[Grid3DObject, Grid3DIceObject],
    *,
    components: Optional[FitConfig] = None,
    start_idx: Optional[Union[int, dt.date]] = None,
    end_idx: Optional[Union[int, dt.date]] = None,
    mode: str = "remove",
    weights: Optional[Union[np.ndarray, float]] = None,
) -> Dict[str, Union[Grid3DObject, Grid3DIceObject]]:
    """
    Apply subset-fit/full-apply deseasoning directly to a Grid3DObject or Grid3DIceObject.

    Arguments:
        logger (Logger): Logger instance for logging information and debugging messages.
        grid3d (Union[Grid3DObject, Grid3DIceObject]): A 3D grid object containing time-series
        data, as well as associated metadata such as dates, longitude, latitude,
        and projection parameters.
        components (Optional[FitConfig]): Configuration for harmonic components fitting,
        or None to use a default configuration.
        start_idx (Optional[Union[int, dt.date]]): Optional index or date specifying
        the start of the analysis period.
        end_idx (Optional[Union[int, dt.date]]): Optional index or date specifying
        the end of the analysis period.
        mode (str): A string specifying the mode of operation. Valid options include
        'remove', 'update', or other compatible operation modes. Default is 'remove'.
        weights (Optional[Union[np.ndarray, float]]): Weights to apply to the grid points
        during harmonic component fitting. It can be either a 1D array (over time), a
        3D array (matching grid shape), or a scalar value.

    Returns:
        Dict[str, Union[Grid3DObject, Grid3DIceObject]]: A dictionary containing the
        modified grid object under the key "output".

    Raises:
        ValueError: If the shape of the weights does not match the required dimensions,
        or other incompatible configurations are provided.

    """
    t_days = datetime_to_date_float(grid3d.dates)

    T, Ny, Nx = grid3d.grid.shape
    out = np.full((T, Ny, Nx), np.nan, float)
    cfg = components or FitConfig()

    def _weights_for_cell(j: int, i: int) -> Optional[np.ndarray]:
        if weights is None:
            return None
        w = np.asarray(weights)
        if w.ndim == 1:
            if w.shape[0] != T:
                message = "weights 1-D length must match time dimension"
                logger.error(message)
                raise ValueError(message)
            return w
        if w.shape != grid3d.grid.shape:
            message = "weights (T, Ny, Nx) must match grid shape"
            logger.error(message)
            raise ValueError(message)
        return w[:, j, i]

    for j in range(Ny):
        for i in range(Nx):
            ts = grid3d.grid[:, j, i]
            if not np.isfinite(ts).any():
                continue
            w_ts = _weights_for_cell(j, i)
            res = remove_harmonic_components_extrapolate(
                logger=logger,
                times=t_days,
                data=ts,
                components=cfg,
                start_idx=start_idx,
                end_idx=end_idx,
                mode=mode,
                weights=w_ts,
            )
            r = res["output_full"]
            if isinstance(r, np.ndarray):
                out[:, j, i] = r

    if isinstance(grid3d, Grid3DIceObject):
        out_obj = Grid3DIceObject(
            logger=logger,
            grid=out,
            dates=grid3d.dates,
            lon=grid3d.lon,
            lat=grid3d.lat,
            x=grid3d.x,
            y=grid3d.y,
            projection=grid3d.projection
        )
    else:
        out_obj = Grid3DObject(
            logger=logger,
            grid=out,
            dates=grid3d.dates,
            lon=grid3d.lon,
            lat=grid3d.lat
        )

    return {"output": out_obj}


def apply_harmonic_components_sh(
    logger: Logger,
    sh_list: list[object],
    *,
    components: FitConfig | None = None,
    start_idx: Optional[Union[int, dt.date]] = None,
    end_idx: Optional[Union[int, dt.date]] = None,
    mode: str = "remove",
    triangular: bool = True
) -> dict[str, list[object]]:
    """Apply subset-fit/full-apply deseasoning to a time series of SHObjects.

    Each element of `sh_list` must have:
      - .cnm: np.ndarray of shape (L+1, L+1)
      - .snm: np.ndarray of shape (L+1, L+1)
      - .date: datetime-like (numpy.datetime64 or datetime.date)
    """
    if not sh_list:
        return {"output": []}

    C0 = np.asarray(sh_list[0].cnm, dtype=float)
    Lp1 = C0.shape[0]

    dates = np.array([obj.date for obj in sh_list])
    t_days = datetime_to_date_float(dates)

    C = np.stack([np.asarray(obj.cnm, dtype=float) for obj in sh_list], axis=0)  # (T, L+1, L+1)
    S = np.stack([np.asarray(obj.snm, dtype=float) for obj in sh_list], axis=0)
    T = C.shape[0]

    C_out = np.full_like(C, np.nan, dtype=float)
    S_out = np.full_like(S, np.nan, dtype=float)

    cfg = components or FitConfig()

    for ell in range(Lp1):
        mmax = ell if triangular else Lp1 - 1
        for m in range(mmax + 1):
            resC = remove_harmonic_components_extrapolate(logger=logger,
                                                          times=t_days, data=C[:, ell, m], components=cfg,
                                                          start_idx=start_idx, end_idx=end_idx, mode=mode
                                                          )
            resS = remove_harmonic_components_extrapolate(logger=logger,
                                                          times=t_days, data=S[:, ell, m], components=cfg,
                                                          start_idx=start_idx, end_idx=end_idx, mode=mode
                                                          )
            outC = resC["output_full"]
            outS = resS["output_full"]
            if isinstance(outC, np.ndarray):
                C_out[:, ell, m] = outC
            if isinstance(outS, np.ndarray):
                S_out[:, ell, m] = outS

    out_list = copy.deepcopy(sh_list)
    for k in range(T):
        out_list[k].cnm = C_out[k]
        out_list[k].snm = S_out[k]
    return {"output": out_list}


def remove_mean(
    logger: Logger,
    times: np.ndarray,
    data: np.ndarray,
    *,
    start_idx: Optional[Union[int, dt.date]] = None,
    end_idx: Optional[Union[int, dt.date]] = None,
) -> dict[str, np.ndarray]:
    """Remove the mean from a time series.

    Parameters
    ----------
    logger (Logger): Logger instance for logging information and debugging messages.
    times : np.ndarray
    Time axis (decimal years or days).
    data : np.ndarray
    Data array (1D, length N).
    start_idx : int, optional
    Start index for mean computation.
    end_idx : int, optional
    End index for mean computation (exclusive).

    Returns
    -------
    dict
        Dictionary containing:
        - "mean_value": float
        - "data_demeaned": np.ndarray
        - "fit_window": (s, e)

    """
    y = np.asarray(data, dtype=float)
    n = y.size

    s = 0 if start_idx is None else _date_to_index(logger=logger, times=times, d=start_idx)
    e = n if end_idx is None else _date_to_index(logger=logger, times=times, d=end_idx)
    if not (0 <= s <= e <= n):
        message = (f"Invalid bounds for estimation of mean signal on subset of time series with start: {start_idx}, "
                   f"end: {end_idx} and length timeseries: {n}")
        logger.error(message)
        raise ValueError(message)

    # Use only finite values
    window_vals = y[s:e + 1]
    mask = np.isfinite(window_vals)

    if not mask.any():
        mean_val = np.nan
    else:
        mean_val = float(np.nanmean(window_vals))

    data_demeaned = y - mean_val

    return {
        "mean_value": mean_val,
        "data_demeaned": data_demeaned,
        "fit_window": (s, e),
    }


def remove_mean_grid(
    logger: Logger,
    times: np.ndarray,
    grid_obj: Union[Grid3DObject, Grid3DIceObject],
    *,
    start_idx: Optional[Union[int, dt.date]] = None,
    end_idx: Optional[Union[int, dt.date]] = None,
) -> dict[str, Any]:
    """Remove the temporal mean from each grid cell of a 3-D gridded time series.

    Applies mean removal independently at each (lat, lon) location across time,
    returning the grid of mean values and a new Grid3DObject or Grid3DIceObject with demeaned values.
    """
    data = np.asarray(grid_obj.grid, dtype=float)  # (T, Ny, Nx)
    T, Ny, Nx = data.shape

    mean_values = np.full((Ny, Nx), np.nan, dtype=float)
    demeaned = np.empty_like(data)

    for j in range(Ny):
        for i in range(Nx):
            res = remove_mean(logger=logger, times=times, data=data[:, j, i], start_idx=start_idx, end_idx=end_idx)
            mean_values[j, i] = res["mean_value"]
            demeaned[:, j, i] = res["data_demeaned"]

    if isinstance(grid_obj, Grid3DIceObject):
        grid_demeaned = Grid3DIceObject(
            logger=logger,
            grid=demeaned,
            dates=grid_obj.dates,
            lon=grid_obj.lon,
            lat=grid_obj.lat,
            x=grid_obj.x,
            y=grid_obj.y,
            projection=grid_obj.projection
        )
    else:
        grid_demeaned = Grid3DObject(
            logger=logger,
            grid=demeaned,
            dates=grid_obj.dates,
            lon=grid_obj.lon,
            lat=grid_obj.lat,
        )

    return {
        "mean_values": mean_values,
        "grid_demeaned": grid_demeaned,
        "fit_window": (0 if start_idx is None else _date_to_index(logger=logger, times=times, d=start_idx),
                       T if end_idx is None else _date_to_index(logger=logger, times=times, d=end_idx)),
    }


def remove_mean_sh(
    logger: Logger,
    times: np.ndarray,
    sh_list: list[SHObject],
    *,
    start_idx: Optional[Union[int, dt.date]] = None,
    end_idx: Optional[Union[int, dt.date]] = None,
) -> dict[str, Any]:
    """Remove the temporal mean from spherical harmonic coefficients.

    Computes and subtracts the mean Cnm and Snm values over the selected
    time window for each (degree, order), returning the mean coefficients
    and a new list of SHObjects with demeaned coefficients.
    """
    if not sh_list:
        return {"mean_values": None, "sh_demeaned": [], "fit_window": (0, 0)}

    Lp1 = sh_list[0].cnm.shape[0]
    T = len(sh_list)

    # Stack coefficients across time
    C_all = np.stack([sh.cnm for sh in sh_list], axis=0)  # (T, L+1, L+1)
    S_all = np.stack([sh.snm for sh in sh_list], axis=0)

    mean_values = np.full((Lp1, Lp1, 2), np.nan)
    demeaned_C = np.empty_like(C_all)
    demeaned_S = np.empty_like(S_all)

    for ell in range(Lp1):
        for m in range(Lp1):
            res_C = remove_mean(logger=logger, times=times, data=C_all[:, ell, m], start_idx=start_idx, end_idx=end_idx)
            res_S = remove_mean(logger=logger, times=times, data=S_all[:, ell, m], start_idx=start_idx, end_idx=end_idx)

            mean_values[ell, m, 0] = res_C["mean_value"]
            mean_values[ell, m, 1] = res_S["mean_value"]

            demeaned_C[:, ell, m] = res_C["data_demeaned"]
            demeaned_S[:, ell, m] = res_S["data_demeaned"]

    sh_demeaned = [
        SHObject(logger=logger, date=sh_list[k].date, cnm=demeaned_C[k], snm=demeaned_S[k])
        for k in range(T)
    ]
    sh_mean_values = SHObject(logger=logger, date=sh_list[0].date, cnm=mean_values[:, :, 0], snm=mean_values[:, :, 1])

    return {
        "mean_values": sh_mean_values,
        "sh_demeaned": sh_demeaned,
        "fit_window": (0 if start_idx is None else _date_to_index(logger=logger, times=times, d=start_idx),
                       T if end_idx is None else _date_to_index(logger=logger, times=times, d=end_idx)),
    }


def gaussian_filter_series(t: np.ndarray, y: np.ndarray, sigma: float, cutdist: float) -> np.ndarray:
    """Apply Gaussian temporal filter to a 1D series.

    Parameters
    ----------
    t [np.ndarray]: time vector of the time series
    y [np.ndarray]: vector of the time series
    sigma [float]: 1 sigma filter radius
    cutdist [float]: distance at which the Gaussian filter hat is cut of
    """
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(t)
    out = np.full_like(y, np.nan, dtype=float)

    for i in range(n):
        mask = (t >= t[i] - cutdist) & (t <= t[i] + cutdist) & np.isfinite(y)
        if not mask.any():
            continue
        g = np.exp(-0.5 * ((t[mask] - t[i]) / sigma) ** 2)
        den = np.sum(g)
        g = g / den
        out[i] = np.sum(y[mask] * g)
    return out


def gaussian_filter_grid(logger: Logger, grid3d: Union[Grid3DObject, Grid3DIceObject],
                         sigma: float, cutdist: float) -> Union[Grid3DObject, Grid3DIceObject]:
    """Apply a Gaussian temporal filter to each cell in a 3-D gridded time series.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    grid3d : Union[Grid3DObject, Grid3DIceObject]
        Input gridded time series with shape (T, Ny, Nx).
    sigma : float
        1-sigma filter radius, in the same units as the time axis (typically days).
    cutdist : float
        Radius at which the Gaussian kernel is truncated.

    Returns
    -------
    Union[Grid3DObject, Grid3DIceObject]
        New Grid3DObject or Grid3DIceObject with the same metadata as the input, but with
        each time series filtered in time using the Gaussian kernel.
    """
    t = datetime_to_date_float(grid3d.dates)
    T, Ny, Nx = grid3d.grid.shape
    out = np.full_like(grid3d.grid, np.nan, dtype=float)
    for j in range(Ny):
        for i in range(Nx):
            out[:, j, i] = gaussian_filter_series(t, grid3d.grid[:, j, i], sigma, cutdist)

    if isinstance(grid3d, Grid3DIceObject):
        out_grid = Grid3DIceObject(
            logger=logger,
            grid=out,
            dates=grid3d.dates,
            lon=grid3d.lon,
            lat=grid3d.lat,
            x=grid3d.x,
            y=grid3d.y,
            projection=grid3d.projection
        )
    else:
        out_grid = Grid3DObject(
            logger=logger,
            grid=out,
            dates=grid3d.dates,
            lon=grid3d.lon,
            lat=grid3d.lat,
        )

    return out_grid


def gaussian_filter_sh(logger: Logger, sh_list: list[SHObject], sigma: float, cutdist: float) -> list[SHObject]:
    """Apply a Gaussian temporal filter to a list of spherical harmonic objects.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    sh_list : list[SHObject]
        Sequence of SHObjects, each with .cnm, .snm arrays of shape (L+1, L+1).
    sigma : float
        1-sigma filter radius, in the same units as the time axis (typically days).
    cutdist : float
        Radius at which the Gaussian kernel is truncated.

    Returns
    -------
    list[SHObject]
        New list of SHObjects with the same dates as the input, but with
        each coefficient time series filtered in time using the Gaussian kernel.
    """
    dates = np.array([obj.date for obj in sh_list])
    t = datetime_to_date_float(dates)

    # Correct shape: each cnm is (L+1, L+1)
    Lp1 = sh_list[0].cnm.shape[0]
    T = len(sh_list)

    # Stack into arrays (T, L+1, L+1)
    C = np.stack([obj.cnm for obj in sh_list], axis=0)
    S = np.stack([obj.snm for obj in sh_list], axis=0)

    C_out = np.empty_like(C)
    S_out = np.empty_like(S)

    for ell in range(Lp1):
        for m in range(Lp1):
            C_out[:, ell, m] = gaussian_filter_series(t, C[:, ell, m], sigma, cutdist)
            S_out[:, ell, m] = gaussian_filter_series(t, S[:, ell, m], sigma, cutdist)
    return [SHObject(logger=logger, date=sh_list[k].date, cnm=C_out[k], snm=S_out[k]) for k in range(T)]


def fit_161d_with_phaseoffset_sh(logger: Logger,
                                 sh_list: list[SHObject],
                                 phaseoffset: np.ndarray,
                                 start_idx: Optional[Union[int, dt.date]] = None,
                                 end_idx: Optional[Union[int, dt.date]] = None) \
        -> Tuple[list[SHObject], list[SHObject]]:
    """
    Wrap the fit_161d_with_phaseoffset for shcs.

    Parameters
    ----------
    logger (Logger): Logger instance for logging information and debugging messages.
    sh_list: list[SHObject]
        Sequence of SHObjects, each with .cnm, .snm arrays of shape (n_max+1, n_max+1).
    phaseoffset: np.ndarray
        Array containing the phase offsets applied in the estimation
    start_idx: Union[int, dt.date]
        If estimation is done on part of the timeseries, start index or start date
    end_idx: Union[int, dt.date]
        If estimation is done on part of the timeseries, end index or end date

    Returns
    -------
    sh_list_fit: list[SHObject] List of fitted signal
    sh_parameter: list[SHObject] len 2 fitted parameter

    """
    dates = np.array([obj.date for obj in sh_list])
    t = datetime_to_date_float(dates)
    n_max, _ = sh_list[0].cnm.shape
    T = len(t)

    C = np.stack([obj.cnm for obj in sh_list], axis=0)
    S = np.stack([obj.snm for obj in sh_list], axis=0)
    C_fit161 = np.zeros(C.shape)
    para_c = np.zeros((2, n_max + 1, n_max + 1))
    S_fit161 = np.zeros(S.shape)
    para_s = np.zeros((2, n_max + 1, n_max + 1))
    for n in range(n_max):
        for m in range(n + 1):
            para_c[:, n, m], C_fit161[:, n, m] = fit_161d_with_phaseoffset(logger=logger,
                                                                           time=t,
                                                                           timeseries=C[:, n, m],
                                                                           phase_offset=phaseoffset,
                                                                           start_idx=start_idx,
                                                                           end_idx=end_idx)
            para_s[:, n, m], S_fit161[:, n, m] = fit_161d_with_phaseoffset(logger=logger,
                                                                           time=t,
                                                                           timeseries=S[:, n, m],
                                                                           phase_offset=phaseoffset,
                                                                           start_idx=start_idx,
                                                                           end_idx=end_idx)

    sh_list_fit = [SHObject(logger=logger, date=sh_list[k].date, cnm=C_fit161[k], snm=S_fit161[k]) for k in range(T)]
    # date is arbitrary no longer needed
    sh_parameter = [SHObject(logger=logger,
                             date=dt.date(2000, 1, 1 + k),
                             cnm=para_c[k],
                             snm=para_s[k]) for k in range(2)]

    return sh_list_fit, sh_parameter


def fit_161d_with_phaseoffset(logger: Logger,
                              time: np.ndarray,
                              timeseries: np.ndarray,
                              phase_offset: np.ndarray,
                              start_idx: Optional[Union[int, dt.date]] = None,
                              end_idx: Optional[Union[int, dt.date]] = None) \
        -> Tuple[np.ndarray, np.ndarray]:
    """
    Fit the 161d signal (or s2 signal) to a time series with potentially included phase shifts.

    Parameters
    ----------
    logger (Logger): Logger instance for logging information and debugging messages.
    time (np.ndarray): time vector as date float yyyy.ffff
    timeseries (np.ndarray): Observation vector
    phase_offset (np.ndarray): phase offset vector in degree
    start_idx (int or datetime.date): start index if estimation is only done on part of the time series
    end_idx (int or datetime.date): end index if estimation is only done on part of the time series

    Returns
    -------
    parameters (np.ndarray): estimated parameters [a, b] of functional model
                            f(x) = a*cos(2pi*year_days/161.0)+b*sin(2pi*year_days/161.0) + e
    timeseries_estimated (np.ndarray): estimated time series of function model
                            f(x) = a*cos(2pi*year_days/161.0)+b*sin(2pi*year_days/161.0)

    """
    n = len(time)
    s = 0 if start_idx is None else _date_to_index(logger=logger, times=time, d=start_idx)
    e = n if end_idx is None else _date_to_index(logger=logger, times=time, d=end_idx)
    if not (0 <= s <= e <= n):
        message = (f"Invalid bounds for estimation of 161d signal on subset of time series with start: {start_idx}, "
                   f"end: {end_idx} and length timeseries: {n}")
        logger.error(message)
        raise ValueError(message)

    deg_2_rad = get_constant('deg_2_rad')
    time_part = time[s:e + 1]
    timeseries_part = timeseries[s:e + 1]
    design_matrix = np.zeros((len(time_part), 2))
    w161 = twopi * (year_days / 161.0)
    design_matrix[:, 0] = np.cos(w161 * time_part + deg_2_rad * phase_offset[s:e + 1])
    design_matrix[:, 1] = np.sin(w161 * time_part + deg_2_rad * phase_offset[s:e + 1])
    parameter = _solve_lstsq(logger=logger,
                             X=design_matrix,
                             y=timeseries_part)

    if len(time_part) < n:
        design_matrix_extrapolate = np.zeros((len(time), 2))
        w161 = twopi * (year_days / 161.0)
        design_matrix_extrapolate[:, 0] = np.cos(w161 * time_part + deg_2_rad * phase_offset)
        design_matrix_extrapolate[:, 1] = np.sin(w161 * time_part + deg_2_rad * phase_offset)
        timeseries_estimated = design_matrix_extrapolate @ parameter
    else:
        timeseries_estimated = design_matrix @ parameter

    return parameter, timeseries_estimated
