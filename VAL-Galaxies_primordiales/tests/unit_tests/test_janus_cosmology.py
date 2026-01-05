"""
Unit tests for JANUS cosmology module
"""

import pytest
import numpy as np
from numpy.testing import assert_allclose
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from cosmology import JANUSCosmology


class TestJANUSCosmology:
    """Test JANUS cosmology calculations"""

    def test_initialization(self):
        """Test JANUS cosmology initialization"""
        cosmo = JANUSCosmology(H0=70.0, Omega_plus=0.30, Omega_minus=0.05)
        assert cosmo.H0 == 70.0
        assert cosmo.Omega_plus == 0.30
        assert cosmo.Omega_minus == 0.05
        assert cosmo.chi == 1.0

    def test_hubble_at_z_zero(self, janus_cosmo):
        """Test H(z=0) = H0"""
        H_z0 = janus_cosmo.hubble_parameter(0.0)
        assert_allclose(H_z0, janus_cosmo.H0, rtol=1e-6)

    def test_hubble_increases_with_z(self, janus_cosmo, sample_redshifts):
        """Test that H(z) increases monotonically with z"""
        H_z = janus_cosmo.hubble_parameter(sample_redshifts)
        assert np.all(np.diff(H_z) > 0), "H(z) should increase with z"

    def test_comoving_distance_positive(self, janus_cosmo):
        """Test that comoving distances are positive"""
        z_values = [0.5, 1.0, 2.0, 5.0, 10.0]
        for z in z_values:
            d_c = janus_cosmo.comoving_distance(z)
            assert d_c > 0, f"Comoving distance at z={z} should be positive"

    def test_comoving_distance_zero_at_z_zero(self, janus_cosmo):
        """Test d_c(z=0) = 0"""
        d_c = janus_cosmo.comoving_distance(0.0)
        assert_allclose(d_c, 0.0, atol=1e-10)

    def test_angular_diameter_distance(self, janus_cosmo):
        """Test angular diameter distance"""
        z = 1.0
        d_c = janus_cosmo.comoving_distance(z)
        d_A = janus_cosmo.angular_diameter_distance(z)
        # d_A = d_c / (1+z)
        assert_allclose(d_A, d_c / (1.0 + z), rtol=1e-6)

    def test_luminosity_distance(self, janus_cosmo):
        """Test luminosity distance"""
        z = 1.0
        d_c = janus_cosmo.comoving_distance(z)
        d_L = janus_cosmo.luminosity_distance(z)
        # d_L = d_c * (1+z)
        assert_allclose(d_L, d_c * (1.0 + z), rtol=1e-6)

    def test_distance_duality(self, janus_cosmo):
        """Test distance duality: d_L = d_A * (1+z)^2"""
        z = 2.0
        d_A = janus_cosmo.angular_diameter_distance(z)
        d_L = janus_cosmo.luminosity_distance(z)
        assert_allclose(d_L, d_A * (1.0 + z)**2, rtol=1e-6)

    def test_comoving_volume_positive(self, janus_cosmo):
        """Test that comoving volume is positive"""
        z_values = [0.5, 1.0, 2.0, 5.0]
        for z in z_values:
            V_c = janus_cosmo.comoving_volume(z)
            assert V_c > 0, f"Comoving volume at z={z} should be positive"

    def test_age_positive(self, janus_cosmo):
        """Test that age of universe is positive"""
        z_values = [0.0, 1.0, 5.0, 10.0]
        for z in z_values:
            age = janus_cosmo.age_of_universe(z)
            assert age > 0, f"Age at z={z} should be positive"

    def test_age_decreases_with_z(self, janus_cosmo):
        """Test that age decreases with increasing z"""
        z_values = np.array([0.0, 1.0, 2.0, 5.0, 10.0])
        ages = np.array([janus_cosmo.age_of_universe(z) for z in z_values])
        assert np.all(np.diff(ages) < 0), "Age should decrease with increasing z"

    def test_lookback_time(self, janus_cosmo):
        """Test lookback time"""
        z = 1.0
        t0 = janus_cosmo.age_of_universe(0)
        t_z = janus_cosmo.age_of_universe(z)
        t_lb = janus_cosmo.lookback_time(z)
        assert_allclose(t_lb, t0 - t_z, rtol=1e-6)

    def test_critical_density_positive(self, janus_cosmo):
        """Test that critical density is positive"""
        z_values = [0.0, 1.0, 5.0]
        for z in z_values:
            rho_crit = janus_cosmo.critical_density(z)
            assert rho_crit > 0, f"Critical density at z={z} should be positive"

    def test_repr(self, janus_cosmo):
        """Test string representation"""
        repr_str = repr(janus_cosmo)
        assert 'JANUSCosmology' in repr_str
        assert 'H0' in repr_str
