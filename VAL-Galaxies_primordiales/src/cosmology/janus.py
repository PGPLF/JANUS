"""
JANUS Bimetric Cosmology Module

Implements cosmological calculations for the JANUS bimetric model
with positive and negative mass sectors.

References:
- Petit, J.-P. & D'Agostini, G. (2014-2024) - JANUS cosmological model papers
- Based on bimetric relativity with matter-antimatter asymmetry
"""

import numpy as np
from scipy.integrate import quad, odeint
from scipy.interpolate import interp1d
import warnings

try:
    from ..utils.constants import (
        C_LIGHT, H0_JANUS_DEFAULT,
        OMEGA_PLUS_DEFAULT, OMEGA_MINUS_DEFAULT, CHI_DEFAULT, KAPPA,
        INTEGRATION_RTOL, INTEGRATION_ATOL, MPC_TO_KM, GYR_TO_S
    )
except ImportError:
    from utils.constants import (
        C_LIGHT, H0_JANUS_DEFAULT,
        OMEGA_PLUS_DEFAULT, OMEGA_MINUS_DEFAULT, CHI_DEFAULT, KAPPA,
        INTEGRATION_RTOL, INTEGRATION_ATOL, MPC_TO_KM, GYR_TO_S
    )


class JANUSCosmology:
    """
    JANUS Bimetric Cosmology Model

    Parameters
    ----------
    H0 : float, optional
        Hubble constant at z=0 [km/s/Mpc]. Default: 70.0
    Omega_plus : float, optional
        Positive mass density parameter. Default: 0.30
    Omega_minus : float, optional
        Negative mass density parameter. Default: 0.05
    chi : float, optional
        Bimetric coupling parameter. Default: 1.0
    kappa : float, optional
        Sign for negative sector. Default: -1
    """

    def __init__(self, H0=H0_JANUS_DEFAULT, Omega_plus=OMEGA_PLUS_DEFAULT,
                 Omega_minus=OMEGA_MINUS_DEFAULT, chi=CHI_DEFAULT, kappa=KAPPA):
        self.H0 = H0
        self.Omega_plus = Omega_plus
        self.Omega_minus = Omega_minus
        self.chi = chi
        self.kappa = kappa

        # Derived parameters
        self.Omega_k = 1.0 - Omega_plus - abs(Omega_minus)  # Curvature

        # Precompute age of universe for inverse lookups
        self._setup_age_interpolator()

    def hubble_parameter(self, z):
        """
        Hubble parameter H(z) for JANUS model

        Parameters
        ----------
        z : float or array-like
            Redshift

        Returns
        -------
        H : float or array
            Hubble parameter [km/s/Mpc]
        """
        z = np.atleast_1d(z)
        a = 1.0 / (1.0 + z)  # Scale factor

        # JANUS modification to Friedmann equation
        # Includes coupling between positive and negative sectors
        H_squared = self.H0**2 * (
            self.Omega_plus * a**(-3) +
            self.Omega_k * a**(-2) +
            self.chi * abs(self.Omega_minus) * a**(-3) *
            (1.0 + self.kappa * np.sqrt(abs(self.Omega_minus) / self.Omega_plus))
        )

        return np.sqrt(np.maximum(H_squared, 0))

    def comoving_distance(self, z):
        """
        Comoving distance to redshift z

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        d_c : float
            Comoving distance [Mpc]
        """
        if z <= 0:
            return 0.0

        integrand = lambda zp: C_LIGHT / self.hubble_parameter(zp)
        d_c, _ = quad(integrand, 0, z, epsrel=INTEGRATION_RTOL, epsabs=INTEGRATION_ATOL)

        return d_c

    def angular_diameter_distance(self, z):
        """
        Angular diameter distance

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        d_A : float
            Angular diameter distance [Mpc]
        """
        d_c = self.comoving_distance(z)
        return d_c / (1.0 + z)

    def luminosity_distance(self, z):
        """
        Luminosity distance

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        d_L : float
            Luminosity distance [Mpc]
        """
        d_c = self.comoving_distance(z)
        return d_c * (1.0 + z)

    def comoving_volume(self, z):
        """
        Comoving volume out to redshift z

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        V_c : float
            Comoving volume [Mpc^3]
        """
        d_c = self.comoving_distance(z)

        if abs(self.Omega_k) < 1e-5:  # Flat universe
            return (4.0 / 3.0) * np.pi * d_c**3
        elif self.Omega_k > 0:  # Open universe
            return (4.0 * np.pi / (2.0 * self.Omega_k)) * (
                d_c * np.sqrt(1.0 + self.Omega_k * (d_c / C_LIGHT * self.H0)**2) -
                np.arcsinh(np.sqrt(self.Omega_k) * d_c / C_LIGHT * self.H0) / np.sqrt(self.Omega_k)
            )
        else:  # Closed universe
            Om_k_abs = abs(self.Omega_k)
            return (4.0 * np.pi / (2.0 * Om_k_abs)) * (
                np.arcsin(np.sqrt(Om_k_abs) * d_c / C_LIGHT * self.H0) / np.sqrt(Om_k_abs) -
                d_c * np.sqrt(1.0 - Om_k_abs * (d_c / C_LIGHT * self.H0)**2)
            )

    def age_of_universe(self, z):
        """
        Age of the universe at redshift z

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        t : float
            Age of universe [Gyr]
        """
        if z < 0:
            raise ValueError("Redshift must be non-negative")

        # Integrate dt/dz from infinity (z_max) to z
        z_max = 1000.0  # Approximate "infinity"

        integrand = lambda zp: 1.0 / ((1.0 + zp) * self.hubble_parameter(zp))
        t_Mpc, _ = quad(integrand, z, z_max, epsrel=INTEGRATION_RTOL, epsabs=INTEGRATION_ATOL)

        # Convert from Mpc to Gyr
        t_Gyr = t_Mpc * MPC_TO_KM / (C_LIGHT * GYR_TO_S * 1e9)

        return t_Gyr

    def _setup_age_interpolator(self):
        """Setup interpolator for age(z) for faster lookups"""
        z_grid = np.logspace(-3, np.log10(1000), 100)
        age_grid = np.array([self.age_of_universe(z) for z in z_grid])
        self._age_interpolator = interp1d(z_grid, age_grid, kind='cubic',
                                          bounds_error=False, fill_value='extrapolate')

    def lookback_time(self, z):
        """
        Lookback time to redshift z

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        t_lb : float
            Lookback time [Gyr]
        """
        t0 = self.age_of_universe(0)
        t_z = self.age_of_universe(z)
        return t0 - t_z

    def critical_density(self, z):
        """
        Critical density at redshift z

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        rho_crit : float
            Critical density [M_sun/Mpc^3]
        """
        H_z = self.hubble_parameter(z)  # km/s/Mpc
        # Convert to M_sun/Mpc^3
        # rho_c = 3 H^2 / (8 pi G)
        rho_crit = 2.77536627e11 * (H_z / 100.0)**2  # M_sun/Mpc^3
        return rho_crit

    def __repr__(self):
        return (f"JANUSCosmology(H0={self.H0:.2f}, Omega_plus={self.Omega_plus:.3f}, "
                f"Omega_minus={self.Omega_minus:.3f}, chi={self.chi:.2f})")
