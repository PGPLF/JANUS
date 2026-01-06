#!/usr/bin/env python3
"""
Phase 3.1: Statistiques Descriptives pour Publication
======================================================

Génère les distributions observationnelles pour la validation JANUS vs ΛCDM:
1. UV Luminosity Function (z = 8, 10, 12, 14)
2. Stellar Mass Function
3. SFR Distribution
4. Mass-Metallicity Relation
5. Size-Mass Relation

Output: Figures publication-quality + tables LaTeX

Usage:
    python3 phase31_descriptive_stats.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration publication
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.figsize': (8, 6),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.linewidth': 1.2,
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'xtick.minor.width': 0.6,
    'ytick.minor.width': 0.6,
})

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results" / "observations"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Colors for redshift bins
COLORS_Z = {
    '6-8': '#1f77b4',
    '8-10': '#ff7f0e',
    '10-12': '#2ca02c',
    '12-14': '#d62728',
    '14+': '#9467bd'
}

def load_data():
    """Load all processed data"""
    print("Loading data...")

    # JANUS-Z complete (236 galaxies with all parameters)
    janus_z = pd.read_csv(DATA_DIR / "jwst" / "processed" / "janus_z_complete.csv")
    print(f"  JANUS-Z: {len(janus_z)} galaxies")

    # JADES high-z (large sample for statistics)
    jades = pd.read_csv(DATA_DIR / "jwst" / "processed" / "jades_highz_muv_reff.csv")
    print(f"  JADES high-z: {len(jades)} galaxies")

    return janus_z, jades

# =============================================================================
# 1. UV LUMINOSITY FUNCTION
# =============================================================================

def compute_uv_lf(data, z_bins, M_UV_bins, volume_Mpc3=1e6):
    """
    Compute UV luminosity function Φ(M_UV)

    Returns number density per magnitude bin [Mpc^-3 mag^-1]
    Note: Volume approximation - for publication, use proper Vmax method
    """
    results = {}

    for z_label, (z_lo, z_hi) in z_bins.items():
        mask = (data['z'] >= z_lo) & (data['z'] < z_hi) & data['M_UV'].notna()
        sample = data[mask]['M_UV'].values

        if len(sample) < 5:
            continue

        # Histogram
        counts, edges = np.histogram(sample, bins=M_UV_bins)
        bin_centers = 0.5 * (edges[:-1] + edges[1:])
        bin_width = edges[1] - edges[0]

        # Number density (simplified - no completeness correction)
        phi = counts / (volume_Mpc3 * bin_width)
        phi_err = np.sqrt(counts) / (volume_Mpc3 * bin_width)

        # Store
        results[z_label] = {
            'M_UV': bin_centers,
            'phi': phi,
            'phi_err': phi_err,
            'N': len(sample),
            'z_range': (z_lo, z_hi)
        }

    return results

def plot_uv_lf(lf_results, output_file):
    """Plot UV luminosity function - publication quality"""
    fig, ax = plt.subplots(figsize=(8, 6))

    for z_label, data in lf_results.items():
        if data['N'] < 10:
            continue

        mask = data['phi'] > 0
        ax.errorbar(
            data['M_UV'][mask],
            np.log10(data['phi'][mask]),
            yerr=0.434 * data['phi_err'][mask] / data['phi'][mask],
            fmt='o-',
            color=COLORS_Z.get(z_label, 'gray'),
            label=f"z ~ {z_label} (N={data['N']})",
            markersize=6,
            capsize=2,
            linewidth=1.5
        )

    ax.set_xlabel(r'$M_{\rm UV}$ [mag]')
    ax.set_ylabel(r'$\log_{10}(\Phi)$ [Mpc$^{-3}$ mag$^{-1}$]')
    ax.set_title('UV Luminosity Function - JWST High-z Galaxies')
    ax.set_xlim(-24, -16)
    ax.set_ylim(-7, -2)
    ax.invert_xaxis()
    ax.legend(loc='upper left', frameon=True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.savefig(output_file)
    plt.savefig(output_file.with_suffix('.png'))
    print(f"  Saved: {output_file}")
    plt.close()

# =============================================================================
# 2. STELLAR MASS FUNCTION
# =============================================================================

def compute_smf(data, z_bins, mass_bins, volume_Mpc3=1e6):
    """Compute Stellar Mass Function Φ(M*)"""
    results = {}

    for z_label, (z_lo, z_hi) in z_bins.items():
        mask = (data['z'] >= z_lo) & (data['z'] < z_hi) & data['log_Mstar'].notna()
        sample = data[mask]['log_Mstar'].values

        if len(sample) < 5:
            continue

        counts, edges = np.histogram(sample, bins=mass_bins)
        bin_centers = 0.5 * (edges[:-1] + edges[1:])
        bin_width = edges[1] - edges[0]

        phi = counts / (volume_Mpc3 * bin_width)
        phi_err = np.sqrt(counts) / (volume_Mpc3 * bin_width)

        results[z_label] = {
            'log_Mstar': bin_centers,
            'phi': phi,
            'phi_err': phi_err,
            'N': len(sample),
            'z_range': (z_lo, z_hi)
        }

    return results

def plot_smf(smf_results, output_file):
    """Plot Stellar Mass Function"""
    fig, ax = plt.subplots(figsize=(8, 6))

    for z_label, data in smf_results.items():
        if data['N'] < 5:
            continue

        mask = data['phi'] > 0
        ax.errorbar(
            data['log_Mstar'][mask],
            np.log10(data['phi'][mask]),
            yerr=0.434 * data['phi_err'][mask] / data['phi'][mask],
            fmt='s-',
            color=COLORS_Z.get(z_label, 'gray'),
            label=f"z ~ {z_label} (N={data['N']})",
            markersize=6,
            capsize=2,
            linewidth=1.5
        )

    ax.set_xlabel(r'$\log_{10}(M_*/M_\odot)$')
    ax.set_ylabel(r'$\log_{10}(\Phi)$ [Mpc$^{-3}$ dex$^{-1}$]')
    ax.set_title('Stellar Mass Function - JWST High-z Galaxies')
    ax.set_xlim(7.5, 11.5)
    ax.set_ylim(-7, -2)
    ax.legend(loc='upper right', frameon=True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.savefig(output_file)
    plt.savefig(output_file.with_suffix('.png'))
    print(f"  Saved: {output_file}")
    plt.close()

# =============================================================================
# 3. SFR DISTRIBUTION
# =============================================================================

def plot_sfr_distribution(data, output_file):
    """Plot SFR distribution by redshift"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    z_bins = {'6-8': (6, 8), '8-10': (8, 10), '10-12': (10, 12), '12+': (12, 20)}

    # Left: SFR histogram
    ax = axes[0]
    for z_label, (z_lo, z_hi) in z_bins.items():
        mask = (data['z'] >= z_lo) & (data['z'] < z_hi) & data['log_SFR'].notna()
        sample = data[mask]['log_SFR'].values
        if len(sample) > 3:
            ax.hist(sample, bins=15, alpha=0.5, label=f'z ~ {z_label} (N={len(sample)})',
                   color=COLORS_Z.get(z_label, 'gray'), density=True, histtype='stepfilled')

    ax.set_xlabel(r'$\log_{10}({\rm SFR} / M_\odot\,{\rm yr}^{-1})$')
    ax.set_ylabel('Probability Density')
    ax.set_title('SFR Distribution')
    ax.legend(loc='upper left', frameon=True)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Right: SFR vs redshift
    ax = axes[1]
    mask = data['log_SFR'].notna()
    sc = ax.scatter(data[mask]['z'], data[mask]['log_SFR'],
                   c=data[mask]['log_Mstar'], cmap='viridis',
                   alpha=0.7, s=20, edgecolor='none')
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label(r'$\log_{10}(M_*/M_\odot)$')

    ax.set_xlabel('Redshift z')
    ax.set_ylabel(r'$\log_{10}({\rm SFR} / M_\odot\,{\rm yr}^{-1})$')
    ax.set_title('SFR vs Redshift')
    ax.set_xlim(6, 15)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(output_file)
    plt.savefig(output_file.with_suffix('.png'))
    print(f"  Saved: {output_file}")
    plt.close()

# =============================================================================
# 4. MASS-METALLICITY RELATION
# =============================================================================

def plot_mass_metallicity(data, output_file):
    """Plot Mass-Metallicity Relation"""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Filter valid metallicity
    mask = (data['metallicity_12OH'] > 6) & (data['metallicity_12OH'] < 10) & data['log_Mstar'].notna()
    sample = data[mask]

    if len(sample) < 5:
        print("  WARNING: Not enough metallicity data for MZR plot")
        plt.close()
        return

    # Color by redshift
    sc = ax.scatter(sample['log_Mstar'], sample['metallicity_12OH'],
                   c=sample['z'], cmap='plasma', s=50, alpha=0.8,
                   edgecolor='k', linewidth=0.5)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Redshift z')

    # Fit linear relation
    valid = sample['metallicity_12OH'].notna() & sample['log_Mstar'].notna()
    if valid.sum() > 10:
        slope, intercept, r, p, se = stats.linregress(
            sample[valid]['log_Mstar'],
            sample[valid]['metallicity_12OH']
        )
        x_fit = np.linspace(8, 11, 100)
        y_fit = slope * x_fit + intercept
        ax.plot(x_fit, y_fit, 'k--', linewidth=2,
               label=f'Fit: 12+log(O/H) = {slope:.2f}×log(M*) + {intercept:.2f}')

    # Local MZR reference (Tremonti+04)
    x_local = np.linspace(8, 11, 100)
    y_local = -1.492 + 1.847*x_local - 0.08026*x_local**2  # simplified Tremonti+04
    ax.plot(x_local, y_local, 'b:', linewidth=2, alpha=0.7, label='Local MZR (z~0)')

    ax.set_xlabel(r'$\log_{10}(M_*/M_\odot)$')
    ax.set_ylabel(r'$12 + \log({\rm O/H})$')
    ax.set_title(f'Mass-Metallicity Relation (N={len(sample)})')
    ax.set_xlim(7.5, 11.5)
    ax.set_ylim(6.5, 9.5)
    ax.legend(loc='lower right', frameon=True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.savefig(output_file)
    plt.savefig(output_file.with_suffix('.png'))
    print(f"  Saved: {output_file}")
    plt.close()

# =============================================================================
# 5. SIZE-MASS RELATION
# =============================================================================

def plot_size_mass(data, output_file):
    """Plot Size-Mass Relation"""
    fig, ax = plt.subplots(figsize=(8, 6))

    mask = data['r_eff_kpc'].notna() & data['log_Mstar'].notna() & (data['r_eff_kpc'] > 0)
    sample = data[mask]

    if len(sample) < 5:
        print("  WARNING: Not enough size data")
        plt.close()
        return

    # Color by redshift
    sc = ax.scatter(sample['log_Mstar'], np.log10(sample['r_eff_kpc']),
                   c=sample['z'], cmap='plasma', s=50, alpha=0.8,
                   edgecolor='k', linewidth=0.5)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Redshift z')

    # Fit relation
    valid = (sample['r_eff_kpc'] > 0) & sample['log_Mstar'].notna()
    if valid.sum() > 10:
        slope, intercept, r, p, se = stats.linregress(
            sample[valid]['log_Mstar'],
            np.log10(sample[valid]['r_eff_kpc'])
        )
        x_fit = np.linspace(8, 11, 100)
        y_fit = slope * x_fit + intercept
        ax.plot(x_fit, y_fit, 'k--', linewidth=2,
               label=f'Fit: log(r_eff) = {slope:.2f}×log(M*) + {intercept:.2f}')

    # Local relation reference (van der Wel+14)
    x_local = np.linspace(8, 11, 100)
    y_local = 0.22 * (x_local - 10) + np.log10(2.5)  # z~0 reference
    ax.plot(x_local, y_local, 'b:', linewidth=2, alpha=0.7, label='Local (z~0)')

    ax.set_xlabel(r'$\log_{10}(M_*/M_\odot)$')
    ax.set_ylabel(r'$\log_{10}(r_{\rm eff}$ / kpc)')
    ax.set_title(f'Size-Mass Relation (N={len(sample)})')
    ax.set_xlim(7.5, 11.5)
    ax.set_ylim(-1.5, 1.5)
    ax.legend(loc='lower right', frameon=True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.savefig(output_file)
    plt.savefig(output_file.with_suffix('.png'))
    print(f"  Saved: {output_file}")
    plt.close()

# =============================================================================
# SUMMARY TABLE
# =============================================================================

def create_summary_table(janus_z, output_file):
    """Create LaTeX summary table"""

    z_bins = [(6.5, 8), (8, 10), (10, 12), (12, 14), (14, 20)]

    rows = []
    for z_lo, z_hi in z_bins:
        mask = (janus_z['z'] >= z_lo) & (janus_z['z'] < z_hi)
        sample = janus_z[mask]
        n = len(sample)

        if n == 0:
            continue

        row = {
            'z_range': f'{z_lo:.1f}-{z_hi:.1f}',
            'N': n,
            'M_UV_med': f"{sample['M_UV'].median():.1f}",
            'M_UV_std': f"{sample['M_UV'].std():.1f}",
            'logM_med': f"{sample['log_Mstar'].median():.2f}",
            'logM_std': f"{sample['log_Mstar'].std():.2f}",
            'logSFR_med': f"{sample['log_SFR'].median():.2f}",
            'logSFR_std': f"{sample['log_SFR'].std():.2f}",
            'r_eff_med': f"{sample['r_eff_kpc'].median():.2f}",
            'r_eff_std': f"{sample['r_eff_kpc'].std():.2f}",
        }
        rows.append(row)

    # Write LaTeX
    with open(output_file, 'w') as f:
        f.write("% Table 1: Sample Statistics by Redshift Bin\n")
        f.write("\\begin{table*}\n")
        f.write("\\centering\n")
        f.write("\\caption{Sample statistics for JWST high-z galaxies by redshift bin.}\n")
        f.write("\\label{tab:sample_stats}\n")
        f.write("\\begin{tabular}{lccccccccc}\n")
        f.write("\\hline\\hline\n")
        f.write("z range & N & $M_{\\rm UV}$ & $\\sigma$ & $\\log M_*$ & $\\sigma$ & $\\log$ SFR & $\\sigma$ & $r_{\\rm eff}$ & $\\sigma$ \\\\\n")
        f.write(" & & [mag] & & [$M_\\odot$] & & [$M_\\odot$/yr] & & [kpc] & \\\\\n")
        f.write("\\hline\n")

        for row in rows:
            f.write(f"{row['z_range']} & {row['N']} & {row['M_UV_med']} & {row['M_UV_std']} & ")
            f.write(f"{row['logM_med']} & {row['logM_std']} & {row['logSFR_med']} & {row['logSFR_std']} & ")
            f.write(f"{row['r_eff_med']} & {row['r_eff_std']} \\\\\n")

        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")

    print(f"  Saved: {output_file}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*60)
    print("PHASE 3.1: STATISTIQUES DESCRIPTIVES")
    print("="*60)

    # Load data
    janus_z, jades = load_data()

    # Define bins
    z_bins = {
        '6-8': (6.5, 8),
        '8-10': (8, 10),
        '10-12': (10, 12),
        '12-14': (12, 14),
        '14+': (14, 20)
    }
    M_UV_bins = np.arange(-24, -14, 1)
    mass_bins = np.arange(7.5, 12, 0.5)

    # 1. UV Luminosity Function
    print("\n1. UV Luminosity Function...")
    lf_results = compute_uv_lf(janus_z, z_bins, M_UV_bins)
    plot_uv_lf(lf_results, RESULTS_DIR / "fig1_uv_luminosity_function.pdf")

    # 2. Stellar Mass Function
    print("\n2. Stellar Mass Function...")
    smf_results = compute_smf(janus_z, z_bins, mass_bins)
    plot_smf(smf_results, RESULTS_DIR / "fig2_stellar_mass_function.pdf")

    # 3. SFR Distribution
    print("\n3. SFR Distribution...")
    plot_sfr_distribution(janus_z, RESULTS_DIR / "fig3_sfr_distribution.pdf")

    # 4. Mass-Metallicity Relation
    print("\n4. Mass-Metallicity Relation...")
    plot_mass_metallicity(janus_z, RESULTS_DIR / "fig4_mass_metallicity.pdf")

    # 5. Size-Mass Relation
    print("\n5. Size-Mass Relation...")
    plot_size_mass(janus_z, RESULTS_DIR / "fig5_size_mass_relation.pdf")

    # Summary table
    print("\n6. Summary Table...")
    create_summary_table(janus_z, RESULTS_DIR / "table1_sample_statistics.tex")

    # Create markdown summary
    print("\n7. Documentation...")
    with open(RESULTS_DIR.parent.parent / "OBSERVED_DISTRIBUTIONS.md", 'w') as f:
        f.write("# Distributions Observées - Phase 3.1\n\n")
        f.write(f"**Date**: 2026-01-06\n")
        f.write(f"**Échantillon**: JANUS-Z (N={len(janus_z)})\n\n")
        f.write("## Figures Générées\n\n")
        f.write("| Figure | Description | Fichier |\n")
        f.write("|--------|-------------|--------|\n")
        f.write("| Fig. 1 | UV Luminosity Function | `fig1_uv_luminosity_function.pdf` |\n")
        f.write("| Fig. 2 | Stellar Mass Function | `fig2_stellar_mass_function.pdf` |\n")
        f.write("| Fig. 3 | SFR Distribution | `fig3_sfr_distribution.pdf` |\n")
        f.write("| Fig. 4 | Mass-Metallicity Relation | `fig4_mass_metallicity.pdf` |\n")
        f.write("| Fig. 5 | Size-Mass Relation | `fig5_size_mass_relation.pdf` |\n")
        f.write("\n## Table\n\n")
        f.write("| Table | Description | Fichier |\n")
        f.write("|-------|-------------|--------|\n")
        f.write("| Table 1 | Sample Statistics | `table1_sample_statistics.tex` |\n")

    print("\n" + "="*60)
    print("PHASE 3.1 TERMINÉE")
    print("="*60)
    print(f"\nFigures: {RESULTS_DIR}")

if __name__ == "__main__":
    main()
