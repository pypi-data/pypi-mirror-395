#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""DDK filtering functions for geogravL3 package."""
from logging import Logger
from typing import List, Dict, Any
import numpy as np

from ...datamodels.shc import SHObject


# --- Helper: extract a weight block from file data ---
def _extract_block(dat, block_idx: int, block_sizes: List[int], nstart: List[int], nend: List[int],
                   lmax: int, order: int = 0) -> np.ndarray:
    """Extract one filter block and truncate to valid range for given order."""
    block = np.reshape(dat["pack1"][nstart[block_idx] - 1: nend[block_idx]],
                       (block_sizes[block_idx], block_sizes[block_idx])).T
    # truncate size depending on order
    if order == 0:
        return block[: lmax - 1, : lmax - 1]
    max_dim = min(lmax - 1, lmax - order + 1)
    return block[:max_dim, :max_dim]


def filt_ddk(logger: Logger, input_shc: List[SHObject],  filename_filter: str, lmax: int) -> List[SHObject]:
    """
    Apply DDK filtering to spherical harmonic coefficients.

    Parameters
    ----------
    logger: Logger
        Logger object to log the error messages
    input_shc : List[SHObject]
        List of spherical harmonic objects. Each has attributes:
        - date
        - cnm: cosine coefficients (array of shape (lmax+1, lmax+1))
        - snm: sine coefficients (same shape)
    filename_filter : str
        Path to binary DDK weight file.
    lmax : int
        Maximum spherical harmonic degree.

    Returns
    -------
    output_shc : List[SHObject]
        Filtered coefficients, same length as input_shc.
    """
    # Read binary file:
    dat = read_BIN(logger=logger, ifile=filename_filter)
    dat = unpack_blocks(dat, dat["type"])

    # --- Precompute block sizes and index ranges ---
    block_sizes = []
    nstart, nend = [], []
    prev_end = 0
    for blk_end in dat["blockind"]:
        sz = blk_end - prev_end
        block_sizes.append(sz)
        start_idx = 1 if not nstart else nend[-1] + 1
        end_idx = start_idx + sz ** 2 - 1
        nstart.append(start_idx)
        nend.append(end_idx)
        prev_end = blk_end

    # --- Initialize output SHObjects ---
    dummy_cnm = np.zeros((lmax+1, lmax+1))
    dummy_snm = np.zeros((lmax+1, lmax+1))
    output_shc = [SHObject(logger=logger, date=sh.date, cnm=dummy_cnm.copy(), snm=dummy_snm.copy()) for sh in input_shc]

    # --- Case m = 0 ---
    block_idx = 0  # first block
    block = np.reshape(
        dat["pack1"][nstart[block_idx] - 1: nend[block_idx]],
        (block_sizes[block_idx], block_sizes[block_idx]),
    ).T
    block = block[: lmax - 1, : lmax - 1]  # truncate to lmax

    for t, sh in enumerate(input_shc):
        coef = sh.cnm[2: lmax + 1, 0]  # m=0 coefficients, degree >= 2
        output_shc[t].cnm[2:, 0] = block @ coef

    # --- Case m > 0 ---
    for order in range(1, lmax + 1):
        blockC = _extract_block(dat=dat, block_idx=2 * order - 1, block_sizes=block_sizes,
                                nstart=nstart, nend=nend, lmax=lmax, order=order)
        blockS = _extract_block(dat=dat, block_idx=2 * order, block_sizes=block_sizes,
                                nstart=nstart, nend=nend, lmax=lmax, order=order)

        degree_start = max(3, order + 1)
        for t, sh in enumerate(input_shc):
            coefC = sh.cnm[degree_start - 1: lmax + 1, order]
            coefS = sh.snm[degree_start - 1: lmax + 1, order]
            output_shc[t].cnm[degree_start - 1:, order] = blockC @ coefC
            output_shc[t].snm[degree_start - 1:, order] = blockS @ coefS

    return output_shc


def _decode_str(fid, n: int) -> str:
    """Read and decode a fixed-length string from binary file."""
    return np.fromfile(fid, dtype="uint8", count=n).tobytes().decode("utf-8", errors="ignore").strip()


def read_BIN(logger: Logger, ifile: str) -> Dict[str, Any]:
    """
    Read a binary file containing symmetric, full, block-diagonal matrices.

    logger: Logger, Logger object to log the error messages
    ifile: str, path to binary file

    Returns
    -------
    dat (Dict[str, Any]): dictionary of parsed contents
    """
    dat: Dict[str, Any] = {}

    try:
        with open(ifile, "rb") as fid:
            # File header
            dat["version"] = _decode_str(fid, 8)
            dat["type"] = _decode_str(fid, 8)
            dat["descr"] = _decode_str(fid, 80)

            # Index metadata
            metaint = np.fromfile(fid, dtype="int32", count=6)
            dat["nval1"], dat["nval2"], dat["pval1"], dat["pval2"] = metaint[2:]

            # Number of blocks for block types
            if dat["type"] in {"BDSYMV0_", "BDFULLV0"}:
                dat["nblocks"] = int(np.fromfile(fid, dtype="int32", count=1))

            n_ints, n_dbls = int(metaint[0]), int(metaint[1])

            if n_ints > 0:
                dat["ints_d"] = np.fromfile(fid, dtype="uint8", count=n_ints * 24).reshape((n_ints, 24))
                dat["ints"] = np.fromfile(fid, dtype="int32", count=n_ints)
            if n_dbls > 0:
                dat["dbls_d"] = np.fromfile(fid, dtype="uint8", count=n_dbls * 24).reshape((n_dbls, 24))
                dat["dbls"] = np.fromfile(fid, dtype="float64", count=n_dbls)

            # side1 data
            dat["side1_d"] = np.fromfile(fid, dtype="uint8", count=dat["nval1"] * 24).reshape((dat["nval1"], 24))

            # block indices
            if dat["type"] in {"BDSYMV0_", "BDFULLV0"}:
                dat["blockind"] = np.fromfile(fid, dtype="int32", count=dat["nblocks"])

            # Main data: always read pack1 (and vec1/vec2 for some types)
            t = dat["type"]
            if t == "SYMV0___":
                dat["pack1"] = np.fromfile(fid, dtype="float64", count=dat["pval1"])
            elif t == "SYMV1___":
                dat["vec1"] = np.fromfile(fid, dtype="float64", count=dat["nval1"])
                dat["pack1"] = np.fromfile(fid, dtype="float64", count=dat["pval1"])
            elif t == "SYMV2___":
                dat["vec1"] = np.fromfile(fid, dtype="float64", count=dat["nval1"])
                dat["vec2"] = np.fromfile(fid, dtype="float64", count=dat["nval1"])
                dat["pack1"] = np.fromfile(fid, dtype="float64", count=dat["pval1"])
            elif t in {"BDSYMV0_", "BDFULLV0", "FULLSQV0"}:
                dat["pack1"] = np.fromfile(fid, dtype="float64", count=dat["pval1"])

    except Exception as e:
        message = f"Error reading file {ifile}: {e}"
        logger.error(message)
        raise RuntimeError(message)

    return dat


def _unpack_symmetric(pack: np.ndarray, n: int) -> np.ndarray:
    """Convert packed upper-triangle storage to full symmetric matrix."""
    mat = np.zeros((n, n), dtype=float)
    ind = np.triu_indices(n)
    mat[ind] = pack
    mat += mat.T - np.diag(np.diag(mat))
    return mat


def unpack_blocks(dat: dict, unpack_type: str, unpack: bool = False) -> dict:
    """
    Unpack the pack1 data to mat1 depending on type.

    Works for ``SYMV0___``, ``SYMV1___``, ``SYMV2___``, ``BDSYMV0_``, ``BDFULLV0``, ``FULLSQV0``.
    """
    t = unpack_type

    if t in ["SYMV0___", "SYMV1___", "SYMV1___"]:
        if unpack:
            dat["mat1"] = _unpack_symmetric(dat["pack1"], dat["nval1"])
            del dat["pack1"]

    elif t == "BDSYMV0_":
        if unpack:
            mat = np.zeros((0, 0))
            skip = skipentries = 0
            for sz_end in dat["blockind"]:
                sz = sz_end - skip
                ind = np.triu_indices(sz)
                blk = np.zeros((sz, sz))
                blk[ind] = dat["pack1"][skipentries:skipentries + sz * (sz + 1) // 2]
                blk += blk.T - np.diag(np.diag(blk))
                mat = np.block([
                    [mat, np.zeros((mat.shape[0], sz))],
                    [np.zeros((sz, mat.shape[1])), blk]
                ])
                skip = sz_end
                skipentries += sz * (sz + 1) // 2
            dat["mat1"] = mat
            del dat["pack1"]

    elif t == "BDFULLV0":
        if unpack:
            mat = np.zeros((0, 0))
            skip = skipentries = 0
            for sz_end in dat["blockind"]:
                sz = sz_end - skip
                blk = np.reshape(dat["pack1"][skipentries:skipentries + sz ** 2], (sz, sz))
                mat = np.block([
                    [mat, np.zeros((mat.shape[0], sz))],
                    [np.zeros((sz, mat.shape[1])), blk]
                ])
                skip = sz_end
                skipentries += sz ** 2
            dat["mat1"] = mat
            del dat["pack1"]

    elif t == "FULLSQV0":
        if unpack:
            dat["mat1"] = dat["pack1"].reshape((dat["nval1"], dat["nval1"]))
            del dat["pack1"]

    return dat
