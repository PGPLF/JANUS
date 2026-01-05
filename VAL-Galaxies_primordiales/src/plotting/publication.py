"""
Publication-Quality Plotting Functions

Utilities for creating high-quality figures for scientific publications.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams
import corner


def setup_plot_style(style='publication'):
    """
    Setup matplotlib style for publication-quality figures

    Parameters
    ----------
    style : str, optional
        Style preset: 'publication', 'presentation', 'notebook'
    """
    if style == 'publication':
        # Publication style (2-column format)
        rcParams['figure.figsize'] = (7, 5)
        rcParams['font.size'] = 11
        rcParams['axes.labelsize'] = 12
        rcParams['axes.titlesize'] = 12
        rcParams['xtick.labelsize'] = 10
        rcParams['ytick.labelsize'] = 10
        rcParams['legend.fontsize'] = 10
        rcParams['font.family'] = 'serif'
        rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
        rcParams['mathtext.fontset'] = 'dejavuserif'
        rcParams['lines.linewidth'] = 1.5
        rcParams['axes.linewidth'] = 1.0
        rcParams['xtick.major.width'] = 1.0
        rcParams['ytick.major.width'] = 1.0
        rcParams['xtick.minor.width'] = 0.5
        rcParams['ytick.minor.width'] = 0.5
        rcParams['legend.frameon'] = False
        rcParams['savefig.dpi'] = 300
        rcParams['savefig.bbox'] = 'tight'
        rcParams['savefig.pad_inches'] = 0.05

    elif style == 'presentation':
        # Presentation style (larger fonts)
        rcParams['figure.figsize'] = (10, 7)
        rcParams['font.size'] = 16
        rcParams['axes.labelsize'] = 18
        rcParams['axes.titlesize'] = 20
        rcParams['xtick.labelsize'] = 14
        rcParams['ytick.labelsize'] = 14
        rcParams['legend.fontsize'] = 14
        rcParams['lines.linewidth'] = 2.5
        rcParams['savefig.dpi'] = 150

    elif style == 'notebook':
        # Jupyter notebook style
        rcParams['figure.figsize'] = (8, 6)
        rcParams['font.size'] = 12
        rcParams['lines.linewidth'] = 2.0
        rcParams['savefig.dpi'] = 100

    # Common settings
    rcParams['axes.grid'] = True
    rcParams['grid.alpha'] = 0.3
    rcParams['grid.linestyle'] = '--'


def plot_comparison(z, obs_data, obs_errors, janus_pred, lcdm_pred,
                    xlabel='Redshift', ylabel='Observable', title='',
                    save_path=None):
    """
    Plot model comparison with observations

    Parameters
    ----------
    z : array
        Redshift values
    obs_data : array
        Observed data
    obs_errors : array
        Observational errors
    janus_pred : array
        JANUS model predictions
    lcdm_pred : array
        ΛCDM model predictions
    xlabel, ylabel, title : str, optional
        Axis labels and title
    save_path : str, optional
        Path to save figure

    Returns
    -------
    fig, ax : matplotlib figure and axis
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot observations with error bars
    ax.errorbar(z, obs_data, yerr=obs_errors, fmt='o', color='black',
                markersize=5, capsize=3, label='JWST Observations',
                alpha=0.7, zorder=3)

    # Plot model predictions
    ax.plot(z, janus_pred, '-', color='#d62728', linewidth=2,
            label='JANUS Model', zorder=2)
    ax.plot(z, lcdm_pred, '--', color='#1f77b4', linewidth=2,
            label='ΛCDM Model', zorder=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

    if save_path:
        save_figure(fig, save_path)

    return fig, ax


def plot_corner_mcmc(samples, labels, truths=None, save_path=None):
    """
    Create corner plot for MCMC samples

    Parameters
    ----------
    samples : array
        MCMC samples (n_samples, n_params)
    labels : list of str
        Parameter names
    truths : array, optional
        True parameter values to overplot
    save_path : str, optional
        Path to save figure

    Returns
    -------
    fig : matplotlib figure
    """
    fig = corner.corner(samples, labels=labels, truths=truths,
                        quantiles=[0.16, 0.5, 0.84],
                        show_titles=True, title_fmt='.3f',
                        title_kwargs={"fontsize": 12},
                        label_kwargs={"fontsize": 14})

    if save_path:
        save_figure(fig, save_path)

    return fig


def plot_residuals(z, obs_data, model_pred, obs_errors,
                   model_name='Model', save_path=None):
    """
    Plot residuals (data - model) with error bars

    Parameters
    ----------
    z : array
        Redshift values
    obs_data : array
        Observed data
    model_pred : array
        Model predictions
    obs_errors : array
        Observational errors
    model_name : str, optional
        Name of model for title
    save_path : str, optional
        Path to save figure

    Returns
    -------
    fig, (ax1, ax2) : matplotlib figure and axes
    """
    residuals = obs_data - model_pred
    chi = residuals / obs_errors

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8),
                                     gridspec_kw={'height_ratios': [2, 1]},
                                     sharex=True)

    # Top panel: data and model
    ax1.errorbar(z, obs_data, yerr=obs_errors, fmt='o', color='black',
                 markersize=5, capsize=3, label='Data', alpha=0.7)
    ax1.plot(z, model_pred, '-', color='#d62728', linewidth=2,
             label=model_name)
    ax1.set_ylabel('Observable')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)

    # Bottom panel: residuals
    ax2.errorbar(z, residuals, yerr=obs_errors, fmt='o', color='black',
                 markersize=5, capsize=3, alpha=0.7)
    ax2.axhline(0, color='red', linestyle='--', linewidth=1.5)
    ax2.set_xlabel('Redshift')
    ax2.set_ylabel('Residuals')
    ax2.grid(True, alpha=0.3)

    # Add chi-squared statistic
    chi2 = np.sum(chi**2)
    dof = len(z) - 1  # Degrees of freedom (minus model parameters)
    chi2_red = chi2 / dof
    ax2.text(0.05, 0.95, f'χ²/dof = {chi2_red:.2f}',
             transform=ax2.transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    if save_path:
        save_figure(fig, save_path)

    return fig, (ax1, ax2)


def save_figure(fig, path, dpi=300, formats=['pdf', 'png']):
    """
    Save figure in multiple formats

    Parameters
    ----------
    fig : matplotlib figure
        Figure to save
    path : str
        Base path (without extension)
    dpi : int, optional
        Resolution for raster formats. Default: 300
    formats : list of str, optional
        File formats to save. Default: ['pdf', 'png']
    """
    from pathlib import Path

    base_path = Path(path).with_suffix('')

    for fmt in formats:
        output_path = base_path.with_suffix(f'.{fmt}')
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        print(f"Saved: {output_path}")


def format_axis_scientific(ax, axis='both'):
    """
    Format axis with scientific notation

    Parameters
    ----------
    ax : matplotlib axis
        Axis to format
    axis : str, optional
        Which axis to format: 'x', 'y', or 'both'
    """
    from matplotlib.ticker import ScalarFormatter

    formatter = ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2, 3))

    if axis in ['x', 'both']:
        ax.xaxis.set_major_formatter(formatter)
    if axis in ['y', 'both']:
        ax.yaxis.set_major_formatter(formatter)


# Setup default publication style on import
setup_plot_style('publication')
