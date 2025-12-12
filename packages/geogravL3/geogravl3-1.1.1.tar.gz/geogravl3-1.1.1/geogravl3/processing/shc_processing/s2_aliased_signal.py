#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Remove s2 aliased signal functions for geogravL3 package."""
from logging import Logger
from typing import List, Optional, Union
import datetime as dt

import numpy as np

from ..timeseries import fit_161d_with_phaseoffset_sh
from ...datamodels.shc import SHObject


def remove_s2_aliased_signal(logger: Logger,
                             shc: List[SHObject],
                             start_idx: Optional[Union[int, dt.date]] = None,
                             end_idx: Optional[Union[int, dt.date]] = None) -> List[SHObject]:
    """
    Wraper function to remove the s2 aliased signal from the SH coefficients.

    Parameters
    ----------
    shc (List[SHObjects]):  List of the SHObjects from which the s2 signal shall be removed
    start_idx (Union[int, dt.date]): Start date or index of the reference epoch on which the signal is estimated
    end_idx (Union[int, dt.date]): End date or index of the reference epoch on which the signal is estimated

    Returns
    -------
    List[SHObjects] from which the signal is removed

    """
    times = np.array([s.date for s in shc])
    phase_offset = np.where(times >= dt.datetime(2018, 1, 1), 100, 0)

    shc_fit, shc_parameter = fit_161d_with_phaseoffset_sh(logger=logger,
                                                          sh_list=shc,
                                                          phaseoffset=phase_offset,
                                                          start_idx=start_idx,
                                                          end_idx=end_idx)

    shc_s2_removed = [SHObject(logger=logger,
                               date=shc[k].date,
                               cnm=(shc[k].cnm-shc_fit[k].cnm),
                               snm=(shc[k].snm-shc_fit[k].snm))
                      for k in range(len(shc))]

    return shc_s2_removed
