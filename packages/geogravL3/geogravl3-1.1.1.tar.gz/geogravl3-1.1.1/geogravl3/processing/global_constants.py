# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Global constants module."""

import numpy as np

# Earth and physical constants based on IERS Conventions 2010
# ---------------------------------------------------------------


class constants:
    """
    Definition of constants (IERS conventions 2010).

     Originally from ATM3DGRAV.
    """

    # Earth radius (meters)
    earths_radius_iers = 6378136.6  # IERS Table 1.1
    # Alternative : PPAIERS = 6378137.0  # (GRS80)

    # GM - Gravitational Constant × Earth's Mass (m^3/s^2)
    geocentric_gravitational_constant_iers = 0.3986004418e+15  # IERS Table 1.1
    # Alternative: PPGMIERS = 0.3986005000e+15  # (GRS80)

    # Earth's flattening
    earths_flattening_iers = 1.0 / 298.25642  # IERS Table 1.1
    # Alternative: PPFIERS = 1.0 / 298.25722101  # (GRS80)

    # Earth's rotation rate (rad/s)
    earths_rotation_rate_grs80 = 0.7292115e-4  # IERS Table 1.2 (GRS80)

    """
    Nature Constants
    ------------------
    """
    # Mean Earth density (kg/m^3)
    earths_density = 5517.0

    # Water density (kg/m^3)
    water_density = 1000.0

    # Standard gravity (m/s^2)
    standard_gravity_acceleration = 9.80665

    # Standard gravity at the equator (m/s^2)
    standard_gravity_acceleration_equator = 9.7803267715

    # Standard gravity at the pole (m/s^2)
    standard_gravity_acceleration_pole = 9.8321863685

    # Gravitational constant G (m^3/kg/s^2)
    gravitational_constant_iers = 6.67428e-11  # IERS Table 1.1

    """
    Mathematical Constants
    -----------------------
    """
    # Degrees to radians conversion factor
    deg_2_rad = np.pi / 180.0

    # Radians to degrees  conversion factor
    rad_2_deg = 180.0 / np.pi
