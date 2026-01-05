"""
Unit tests for ΛCDM cosmology module
"""

import pytest
import numpy as np
from numpy.testing import assert_allclose
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from cosmology import LCDMCosmology


class TestLCDMCosmology:
    """Test ΛCDM cosmology calculations"""

    def test_initialization(self):
        """Test ΛCDM cosmology initialization"""
        cosmo = LCDMCosmology(H0=67.4, Omega_m=0.315, Omega_Lambda=0.685)
        assert cosmo.H0 == 67.4
        assert cosmo.Omega_m == 0.315
        assert cosmo.Omega_Lambda == 0.685

    def test_hubble_at_z_zero(self, lcdm_cosmo):
        """Test H(z=0) = H0"""
        H_z0 = lcdm_cosmo.hubble_parameter(0.0)
        assert_allclose(H_z0, lcdm_cosmo.H0, rtol=1e-6)

    def test_hubble_increases_with_z(self, lcdm_cosmo, sample_redshifts):
        """Test that H(z) increases with z"""
        H_z = lcdm_cosmo.hubble_parameter(sample_redshifts)
        # For ΛCDM at low z, H(z) should increase
        assert np.all(H_z[1:] > H_z[:-1]), "H(z) should increase with z"

    def test_comoving_distance_positive(self, lcdm_cosmo):
        """Test that comoving distances are positive"""
        z_values = [0.5, 1.0, 2.0, 5.0, 10.0]
        for z in z_values:
            d_c = lcdm_cosmo.comoving_distance(z)
            assert d_c > 0, f"Comoving distance at z={z} should be positive"

    def test_comoving_distance_zero_at_z_zero(self, lcdm_cosmo):
        """Test d_c(z=0) = 0"""
        d_c = lcdm_cosmo.comoving_distance(0.0)
        assert_allclose(d_c, 0.0, atol=1e-10)

    def test_angular_diameter_distance(self, lcdm_cosmo):
        """Test angular diameter distance"""
        z = 1.0
        d_c = lcdm_cosmo.comoving_distance(z)
        d_A = lcdm_cosmo.angular_diameter_distance(z)
        # For flat universe: d_A = d_c / (1+z)
        assert_allclose(d_A, d_c / (1.0 + z), rtol=1e-6)

    def test_luminosity_distance(self, lcdm_cosmo):
        """Test luminosity distance"""
        z = 1.0
        d_c = lcdm_cosmo.comoving_distance(z)
        d_L = lcdm_cosmo.luminosity_distance(z)
        # For flat universe: d_L = d_c * (1+z)
        assert_allclose(d_L, d_c * (1.0 + z), rtol=1e-6)

    def test_distance_duality(self, lcdm_cosmo):
        """Test distance duality: d_L = d_A * (1+z)^2"""
        z = 2.0
        d_A = lcdm_cosmo.angular_diameter_distance(z)
        d_L = lcdm_cosmo.luminosity_distance(z)
        assert_allclose(d_L, d_A * (1.0 + z)**2, rtol=1e-5)

    def test_comoving_volume_positive(self, lcdm_cosmo):
        """Test that comoving volume is positive"""
        z_values = [0.5, 1.0, 2.0, 5.0]
        for z in z_values:
            V_c = lcdm_cosmo.comoving_volume(z)
            assert V_c > 0, f"Comoving volume at z={z} should be positive"

    def test_age_positive(self, lcdm_cosmo):
        """Test that age of universe is positive"""
        z_values = [0.0, 1.0, 5.0, 10.0]
        for z in z_values:
            age = lcdm_cosmo.age_of_universe(z)
            assert age > 0, f"Age at z={z} should be positive"

    def test_age_at_z_zero(self, lcdm_cosmo):
        """Test age at z=0 is close to Planck value (13.787 Gyr)"""
        age_z0 = lcdm_cosmo.age_of_universe(0)
        assert 13.0 < age_z0 < 14.5, f"Age at z=0 ({age_z0:.2f} Gyr) should be ~13.8 Gyr"

    def test_lookback_time(self, lcdm_cosmo):
        """Test lookback time"""
        z = 1.0
        t_lb = lcdm_cosmo.lookback_time(z)
        assert 5.0 < t_lb < 10.0, "Lookback time to z=1 should be ~7-8 Gyr"

    def test_lookback_time_zero_at_z_zero(self, lcdm_cosmo):
        """Test lookback time is zero at z=0"""
        t_lb = lcdm_cosmo.lookback_time(0.0)
        assert_allclose(t_lb, 0.0, atol=1e-10)

    def test_critical_density_positive(self, lcdm_cosmo):
        """Test that critical density is positive"""
        z_values = [0.0, 1.0, 5.0]
        for z in z_values:
            rho_crit = lcdm_cosmo.critical_density(z)
            assert rho_crit > 0, f"Critical density at z={z} should be positive"

    def test_distmod(self, lcdm_cosmo):
        """Test distance modulus"""
        z = 1.0
        mu = lcdm_cosmo.distmod(z)
        # Distance modulus should be positive and reasonable
        assert 40 < mu < 50, f"Distance modulus at z=1 ({mu:.2f}) should be ~44"

    def test_repr(self, lcdm_cosmo):
        """Test string representation"""
        repr_str = repr(lcdm_cosmo)
        assert 'LCDMCosmology' in repr_str
        assert 'H0' in repr_str
