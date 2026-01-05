"""
Unit tests for statistics/fitting module
"""

import pytest
import numpy as np
from numpy.testing import assert_allclose
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from statistics import fitting


class TestFitting:
    """Test statistical fitting functions"""

    def test_log_likelihood(self):
        """Test log-likelihood calculation"""
        data = np.array([1.0, 2.0, 3.0])
        errors = np.array([0.1, 0.1, 0.1])
        model_fn = lambda params: params[0] * np.ones(3)

        params = [2.0]
        log_L = fitting.log_likelihood(params, model_fn, data, errors)
        assert np.isfinite(log_L)
        assert log_L < 0  # Log-likelihood should be negative

    def test_log_prior(self):
        """Test log-prior calculation"""
        params = [1.0, 2.0]
        bounds = [(0.0, 2.0), (1.0, 3.0)]

        log_p = fitting.log_prior(params, bounds)
        assert log_p == 0.0  # Within bounds

        params_out = [3.0, 2.0]
        log_p_out = fitting.log_prior(params_out, bounds)
        assert log_p_out == -np.inf  # Outside bounds

    def test_compute_aic(self):
        """Test AIC computation"""
        log_L = -10.0
        n_params = 3
        n_data = 20

        aic = fitting.compute_aic(log_L, n_params, n_data)
        # AIC = 2k - 2ln(L) = 6 + 20 = 26
        # AICc correction applies for small samples
        assert aic > 0
        assert np.isfinite(aic)

    def test_compute_bic(self):
        """Test BIC computation"""
        log_L = -10.0
        n_params = 3
        n_data = 100

        bic = fitting.compute_bic(log_L, n_params, n_data)
        # BIC = k*ln(n) - 2ln(L) = 3*ln(100) + 20
        expected = n_params * np.log(n_data) - 2 * log_L
        assert_allclose(bic, expected)

    def test_gelman_rubin_diagnostic(self):
        """Test Gelman-Rubin R-hat calculation"""
        # Create mock converged chains
        np.random.seed(42)
        n_chains, n_steps, n_params = 4, 1000, 2

        # Converged chains (same distribution)
        chains = np.random.normal(0, 1, (n_chains, n_steps, n_params))

        R_hat = fitting.gelman_rubin_diagnostic(chains)
        assert len(R_hat) == n_params
        # R_hat should be close to 1 for converged chains
        assert np.all(R_hat < 1.2)

    def test_effective_sample_size(self):
        """Test effective sample size calculation"""
        np.random.seed(42)
        n_steps, n_params = 1000, 2
        chain = np.random.normal(0, 1, (n_steps, n_params))

        ess = fitting.effective_sample_size(chain)
        assert len(ess) == n_params
        # ESS should be positive and <= n_steps
        assert np.all(ess > 0)
        assert np.all(ess <= n_steps)
