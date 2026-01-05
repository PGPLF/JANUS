"""Pytest configuration and fixtures"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_redshifts():
    """Sample redshift array for testing"""
    return np.array([0.0, 0.5, 1.0, 2.0, 5.0, 10.0])


@pytest.fixture
def janus_cosmo():
    """JANUS cosmology instance with default parameters"""
    from cosmology import JANUSCosmology
    return JANUSCosmology()


@pytest.fixture
def lcdm_cosmo():
    """ΛCDM cosmology instance with Planck 2018 parameters"""
    from cosmology import LCDMCosmology
    return LCDMCosmology()


@pytest.fixture
def mock_data():
    """Mock observational data for testing"""
    np.random.seed(42)
    z = np.linspace(8, 14, 10)
    data = 10.0 + 0.5 * z + np.random.normal(0, 0.1, len(z))
    errors = np.full_like(data, 0.15)
    return z, data, errors
