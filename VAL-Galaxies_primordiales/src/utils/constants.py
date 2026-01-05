"""
Physical and Cosmological Constants
Conforme aux valeurs standards et JANUS model specifications
"""

import numpy as np
from astropy import constants as const
from astropy import units as u

# Physical Constants (from astropy)
C_LIGHT = const.c.to(u.km / u.s).value  # Speed of light [km/s]
G_NEWTON = const.G.value  # Gravitational constant [m^3 kg^-1 s^-2]
H_PLANCK = const.h.value  # Planck constant [J s]
K_BOLTZMANN = const.k_B.value  # Boltzmann constant [J/K]

# Cosmological Constants
H0_PLANCK2018 = 67.4  # Hubble constant [km/s/Mpc] - Planck 2018
H0_JANUS_DEFAULT = 70.0  # Default H0 for JANUS model [km/s/Mpc]

# ΛCDM Parameters (Planck 2018)
OMEGA_M_PLANCK = 0.315  # Matter density parameter
OMEGA_LAMBDA_PLANCK = 0.685  # Dark energy density parameter
OMEGA_B_PLANCK = 0.049  # Baryon density parameter
OMEGA_CDM_PLANCK = OMEGA_M_PLANCK - OMEGA_B_PLANCK  # Cold dark matter

# JANUS Model Parameters (default values)
OMEGA_PLUS_DEFAULT = 0.30  # Positive mass density
OMEGA_MINUS_DEFAULT = 0.05  # Negative mass density
CHI_DEFAULT = 1.0  # Bimetric coupling parameter
KAPPA = -1  # Sign for negative sector

# Redshift ranges for high-z galaxies
Z_MIN_JWST = 8.0  # Minimum redshift for JWST primordial galaxies
Z_MAX_JWST = 20.0  # Maximum observed redshift

# Conversion factors
MPC_TO_KM = 3.08567758149137e19  # Megaparsec to kilometers
GYR_TO_S = 3.15576e16  # Gigayear to seconds

# Age of universe at z=0 (Planck 2018)
T0_PLANCK = 13.787  # Gyr

# Solar values
M_SUN = const.M_sun.value  # Solar mass [kg]
L_SUN = const.L_sun.value  # Solar luminosity [W]

# Astrophysical constants
AB_MAGNITUDE_ZERO_POINT = -48.6  # AB magnitude zero point

# Numerical precision
INTEGRATION_RTOL = 1e-8  # Relative tolerance for integrations
INTEGRATION_ATOL = 1e-10  # Absolute tolerance for integrations
