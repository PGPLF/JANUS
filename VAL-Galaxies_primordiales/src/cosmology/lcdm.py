"""
ΛCDM Standard Cosmology Module

Implements standard ΛCDM cosmology using Planck 2018 parameters
Interface compatible with JANUSCosmology for direct comparison

References:
- Planck Collaboration (2018) - A&A 641, A6
- Uses astropy.cosmology as computational backend
"""

import numpy as np
from astropy.cosmology import FlatLambdaCDM, LambdaCDM
from astropy import units as u

try:
    from ..utils.constants import (
        H0_PLANCK2018, OMEGA_M_PLANCK, OMEGA_LAMBDA_PLANCK,
        C_LIGHT, MPC_TO_KM, GYR_TO_S
    )
except ImportError:
    from utils.constants import (
        H0_PLANCK2018, OMEGA_M_PLANCK, OMEGA_LAMBDA_PLANCK,
        C_LIGHT, MPC_TO_KM, GYR_TO_S
    )


class LCDMCosmology:
    """
    ΛCDM Standard Cosmology Model

    Parameters
    ----------
    H0 : float, optional
        Hubble constant at z=0 [km/s/Mpc]. Default: 67.4 (Planck 2018)
    Omega_m : float, optional
        Matter density parameter. Default: 0.315 (Planck 2018)
    Omega_Lambda : float, optional
        Dark energy density parameter. Default: 0.685 (Planck 2018)
    """

    def __init__(self, H0=H0_PLANCK2018, Omega_m=OMEGA_M_PLANCK,
                 Omega_Lambda=OMEGA_LAMBDA_PLANCK):
        self.H0 = H0
        self.Omega_m = Omega_m
        self.Omega_Lambda = Omega_Lambda
        self.Omega_k = 1.0 - Omega_m - Omega_Lambda

        # Create astropy cosmology object
        if abs(self.Omega_k) < 1e-5:  # Flat universe
            self._cosmo = FlatLambdaCDM(H0=H0 * u.km / u.s / u.Mpc,
                                         Om0=Omega_m,
                                         Tcmb0=2.7255 * u.K)
        else:
            self._cosmo = LambdaCDM(H0=H0 * u.km / u.s / u.Mpc,
                                     Om0=Omega_m,
                                     Ode0=Omega_Lambda,
                                     Tcmb0=2.7255 * u.K)

    def hubble_parameter(self, z):
        """
        Hubble parameter H(z) for ΛCDM model

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
        H = self._cosmo.H(z).to(u.km / u.s / u.Mpc).value
        return H if H.shape != () else float(H)

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
        return self._cosmo.comoving_distance(z).to(u.Mpc).value

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
        if z <= 0:
            return 0.0
        return self._cosmo.angular_diameter_distance(z).to(u.Mpc).value

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
        if z <= 0:
            return 0.0
        return self._cosmo.luminosity_distance(z).to(u.Mpc).value

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
        if z <= 0:
            return 0.0
        return self._cosmo.comoving_volume(z).to(u.Mpc**3).value

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
        return self._cosmo.age(z).to(u.Gyr).value

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
        if z <= 0:
            return 0.0
        return self._cosmo.lookback_time(z).to(u.Gyr).value

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
        rho_crit_astropy = self._cosmo.critical_density(z)
        # Convert to M_sun/Mpc^3
        rho_crit = rho_crit_astropy.to(u.Msun / u.Mpc**3).value
        return rho_crit

    def distmod(self, z):
        """
        Distance modulus

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        mu : float
            Distance modulus [mag]
        """
        if z <= 0:
            return -np.inf
        return self._cosmo.distmod(z).value

    def comoving_transverse_distance(self, z):
        """
        Comoving transverse distance

        Parameters
        ----------
        z : float
            Redshift

        Returns
        -------
        d_M : float
            Comoving transverse distance [Mpc]
        """
        if z <= 0:
            return 0.0
        d_c = self.comoving_distance(z)

        if abs(self.Omega_k) < 1e-5:  # Flat
            return d_c
        elif self.Omega_k > 0:  # Open
            DH = C_LIGHT / self.H0
            return DH * np.sinh(np.sqrt(self.Omega_k) * d_c / DH) / np.sqrt(self.Omega_k)
        else:  # Closed
            DH = C_LIGHT / self.H0
            return DH * np.sin(np.sqrt(abs(self.Omega_k)) * d_c / DH) / np.sqrt(abs(self.Omega_k))

    def __repr__(self):
        return (f"LCDMCosmology(H0={self.H0:.2f}, Omega_m={self.Omega_m:.3f}, "
                f"Omega_Lambda={self.Omega_Lambda:.3f})")
