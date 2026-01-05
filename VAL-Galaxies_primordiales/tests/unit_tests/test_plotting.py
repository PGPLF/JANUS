"""
Unit tests for plotting module
"""

import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / 'src'
sys.path.insert(0, str(src_path))

from plotting import publication


class TestPlotting:
    """Test plotting functions"""

    def test_setup_plot_style(self):
        """Test plot style setup"""
        # Should not raise an error
        publication.setup_plot_style('publication')
        publication.setup_plot_style('presentation')
        publication.setup_plot_style('notebook')

        # Check that style was applied
        assert matplotlib.rcParams['figure.figsize'] is not None

    def test_plot_comparison(self, mock_data):
        """Test comparison plot creation"""
        z, data, errors = mock_data
        janus_pred = 10.2 + 0.5 * z
        lcdm_pred = 10.0 + 0.48 * z

        fig, ax = publication.plot_comparison(z, data, errors, janus_pred, lcdm_pred)

        assert fig is not None
        assert ax is not None
        plt.close(fig)

    def test_plot_residuals(self, mock_data):
        """Test residuals plot creation"""
        z, data, errors = mock_data
        model_pred = 10.1 + 0.49 * z

        fig, (ax1, ax2) = publication.plot_residuals(z, data, model_pred, errors)

        assert fig is not None
        assert ax1 is not None
        assert ax2 is not None
        plt.close(fig)

    def test_plot_corner_mcmc(self):
        """Test corner plot creation"""
        np.random.seed(42)
        samples = np.random.normal(0, 1, (1000, 3))
        labels = ['param1', 'param2', 'param3']

        fig = publication.plot_corner_mcmc(samples, labels)

        assert fig is not None
        plt.close(fig)

    def test_format_axis_scientific(self):
        """Test scientific notation formatting"""
        fig, ax = plt.subplots()
        publication.format_axis_scientific(ax, axis='both')

        # Should not raise an error
        assert ax is not None
        plt.close(fig)
