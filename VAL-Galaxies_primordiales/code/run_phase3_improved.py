#!/usr/bin/env python3
"""
Phase 3.2 Improved - MCMC with Better Convergence
==================================================
Run MCMC with improved parameters for better convergence:
- 128 walkers (vs 64)
- 5000 steps (vs 2000)
- Burn-in: 2500 steps

Author: VAL-Galaxies_primordiales
Date: 2026-01-10
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import json

# Add paths
BASE_DIR = Path('/Users/patrickguerin/Desktop/JANUS/VAL-Galaxies_primordiales')
sys.path.insert(0, str(BASE_DIR / 'src'))

from cosmology.janus import JANUSCosmology
from cosmology.lcdm import LCDMCosmology

# Import from phase3_complete_v2.py
sys.path.insert(0, str(BASE_DIR / 'code'))
from phase3_complete_v2 import (
    compute_uv_lf_bins, schechter_function,
    log_prior_janus, log_prior_lcdm,
    log_posterior_janus, log_posterior_lcdm,
    calculate_rhat
)

import emcee
import corner
import h5py

# Setup paths
DATA_DIR = BASE_DIR / 'data/jwst/processed'
RESULTS_DIR = BASE_DIR / 'results/v3_improved'
FIGURES_DIR = RESULTS_DIR / 'figures'
MCMC_DIR = RESULTS_DIR / 'mcmc'

# Create directories
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
MCMC_DIR.mkdir(parents=True, exist_ok=True)

# IMPROVED PARAMETERS
N_WALKERS = 128  # Was 64
N_STEPS = 5000   # Was 2000
BURN_IN = 2500   # 50% of steps

# Plot settings
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'figure.figsize': (10, 8),
    'figure.dpi': 150,
    'savefig.dpi': 300
})


def run_mcmc_janus_improved(uv_lf_data):
    """Run JANUS MCMC with improved parameters"""
    ndim = 6

    # Fresh run - remove old backend
    backend_file = str(MCMC_DIR / 'janus_improved.h5')
    if os.path.exists(backend_file):
        os.remove(backend_file)

    # Initial positions (spread around expected values)
    p0 = np.zeros((N_WALKERS, ndim))
    p0[:, 0] = np.random.uniform(65, 80, N_WALKERS)      # H0
    p0[:, 1] = np.random.uniform(0.20, 0.40, N_WALKERS)  # Omega_plus
    p0[:, 2] = np.random.uniform(0.01, 0.10, N_WALKERS)  # Omega_minus
    p0[:, 3] = np.random.uniform(-4.8, -4.2, N_WALKERS)  # log_phi_star
    p0[:, 4] = np.random.uniform(-23.5, -22.0, N_WALKERS)# M_star
    p0[:, 5] = np.random.uniform(-1.8, -1.4, N_WALKERS)  # alpha

    # Setup backend
    backend = emcee.backends.HDFBackend(backend_file)
    backend.reset(N_WALKERS, ndim)

    # Create sampler
    sampler = emcee.EnsembleSampler(
        N_WALKERS, ndim,
        lambda p: log_posterior_janus(p, uv_lf_data),
        backend=backend
    )

    # Run
    print(f"Running JANUS MCMC ({N_WALKERS} walkers, {N_STEPS} steps)...")
    print(f"This will take approximately 3-5 minutes...")
    sampler.run_mcmc(p0, N_STEPS, progress=True)

    return sampler


def run_mcmc_lcdm_improved(uv_lf_data):
    """Run LCDM MCMC with improved parameters"""
    ndim = 5

    # Fresh run - remove old backend
    backend_file = str(MCMC_DIR / 'lcdm_improved.h5')
    if os.path.exists(backend_file):
        os.remove(backend_file)

    # Initial positions
    p0 = np.zeros((N_WALKERS, ndim))
    p0[:, 0] = np.random.uniform(62, 75, N_WALKERS)      # H0
    p0[:, 1] = np.random.uniform(0.25, 0.40, N_WALKERS)  # Omega_m
    p0[:, 2] = np.random.uniform(-4.8, -4.2, N_WALKERS)  # log_phi_star
    p0[:, 3] = np.random.uniform(-23.5, -22.0, N_WALKERS)# M_star
    p0[:, 4] = np.random.uniform(-1.8, -1.4, N_WALKERS)  # alpha

    # Setup backend
    backend = emcee.backends.HDFBackend(backend_file)
    backend.reset(N_WALKERS, ndim)

    # Create sampler
    sampler = emcee.EnsembleSampler(
        N_WALKERS, ndim,
        lambda p: log_posterior_lcdm(p, uv_lf_data),
        backend=backend
    )

    # Run
    print(f"Running LCDM MCMC ({N_WALKERS} walkers, {N_STEPS} steps)...")
    print(f"This will take approximately 3-5 minutes...")
    sampler.run_mcmc(p0, N_STEPS, progress=True)

    return sampler


def analyze_results(sampler, param_names, model_name, uv_lf_data):
    """Analyze MCMC results and compute diagnostics"""
    chain = sampler.get_chain()

    # Convergence diagnostics
    acc_rate = np.mean(sampler.acceptance_fraction)

    rhat = calculate_rhat(chain[BURN_IN:].transpose(1, 0, 2))

    print(f"\n{model_name} Convergence Diagnostics:")
    print(f"  Acceptance rate: {acc_rate:.3f} (target: 0.2-0.5)")
    print(f"  R-hat max: {np.max(rhat):.4f} (target: < 1.1)")
    for name, r in zip(param_names, rhat):
        status = "OK" if r < 1.1 else "WARNING"
        print(f"    {name}: {r:.4f} [{status}]")

    # Best-fit parameters
    flat_chain = sampler.get_chain(flat=True, discard=BURN_IN)

    results = {}
    print(f"\n{model_name} Best-Fit Parameters:")
    for i, name in enumerate(param_names):
        q16, q50, q84 = np.percentile(flat_chain[:, i], [16, 50, 84])
        results[name] = {
            'median': q50,
            'lower': q50 - q16,
            'upper': q84 - q50,
            'std': (q84 - q16) / 2
        }
        print(f"  {name}: {q50:.4f} +{q84-q50:.4f}/-{q50-q16:.4f}")

    # Compute chi-squared
    if 'log_phi*' in param_names:
        phi_idx = param_names.index('log_phi*')
        M_idx = param_names.index('M*')
        alpha_idx = param_names.index('alpha')
    else:
        return results

    phi_star = 10**results['log_phi*']['median']
    M_star = results['M*']['median']
    alpha = results['alpha']['median']

    chi2 = 0
    n_data = 0
    for _, row in uv_lf_data.iterrows():
        M = row['M_mid']
        phi_obs = row['phi']
        phi_err = row['phi_err']

        if phi_err <= 0 or phi_obs <= 0:
            continue

        phi_model = schechter_function(M, phi_star, M_star, alpha)
        if phi_model > 0:
            log_phi_obs = np.log10(phi_obs)
            log_phi_model = np.log10(phi_model)
            log_err = 0.434 * phi_err / phi_obs
            chi2 += ((log_phi_obs - log_phi_model) / log_err)**2
            n_data += 1

    n_params = len(param_names)
    results['chi2'] = chi2
    results['n_data'] = n_data
    results['n_params'] = n_params
    results['BIC'] = chi2 + n_params * np.log(n_data)
    results['AIC'] = chi2 + 2 * n_params
    results['rhat_max'] = float(np.max(rhat))
    results['rhat_all'] = {name: float(r) for name, r in zip(param_names, rhat)}
    results['acceptance'] = float(acc_rate)
    results['n_walkers'] = N_WALKERS
    results['n_steps'] = N_STEPS
    results['burn_in'] = BURN_IN

    print(f"\nGoodness of fit:")
    print(f"  chi2 = {chi2:.2f}")
    print(f"  Reduced chi2 = {chi2/(n_data-n_params):.2f}")
    print(f"  BIC = {results['BIC']:.2f}")
    print(f"  AIC = {results['AIC']:.2f}")

    return results


def plot_trace(sampler, param_names, model_name):
    """Plot trace plots for convergence check"""
    chain = sampler.get_chain()
    n_params = len(param_names)

    fig, axes = plt.subplots(n_params, 1, figsize=(12, 2*n_params), sharex=True)

    for i, (ax, name) in enumerate(zip(axes, param_names)):
        for j in range(min(20, N_WALKERS)):  # Plot 20 walkers
            ax.plot(chain[:, j, i], alpha=0.3, lw=0.5)
        ax.axvline(BURN_IN, color='r', linestyle='--', label='Burn-in')
        ax.set_ylabel(name)

    axes[-1].set_xlabel('Step')
    axes[0].set_title(f'{model_name} - Trace Plot ({N_WALKERS} walkers, {N_STEPS} steps)')

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / f'{model_name.lower()}_trace_improved.pdf')
    fig.savefig(FIGURES_DIR / f'{model_name.lower()}_trace_improved.png')
    plt.close()
    print(f"Saved: {model_name.lower()}_trace_improved.pdf/png")


def main():
    print("="*70)
    print("PHASE 3.2 IMPROVED - MCMC WITH BETTER CONVERGENCE")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    print(f"IMPROVED PARAMETERS:")
    print(f"  N walkers: {N_WALKERS} (was 64)")
    print(f"  N steps: {N_STEPS} (was 2000)")
    print(f"  Burn-in: {BURN_IN} (was 1000)")
    print()

    # Verify cosmology modules
    print("Testing cosmology modules...")
    janus_test = JANUSCosmology(H0=70.0, Omega_plus=0.30, Omega_minus=0.05)
    lcdm_test = LCDMCosmology(H0=67.4, Omega_m=0.315)

    print(f"JANUS t(z=0) = {janus_test.age_of_universe(0):.3f} Gyr")
    print(f"LCDM t(z=0) = {lcdm_test.age_of_universe(0):.3f} Gyr")
    print()

    # Load catalog
    catalog_file = DATA_DIR / 'highz_catalog_VERIFIED_v2.csv'
    print(f"Loading: {catalog_file}")
    catalog = pd.read_csv(catalog_file)
    print(f"Loaded: {len(catalog)} sources")

    # Compute UV LF data
    uv_lf_data = compute_uv_lf_bins(catalog)
    print(f"UV LF bins computed: {len(uv_lf_data)} data points")
    print()

    # Run JANUS MCMC
    print("="*70)
    print("JANUS MODEL")
    print("="*70)
    sampler_janus = run_mcmc_janus_improved(uv_lf_data)

    janus_params = ['H0', 'Omega_+', 'Omega_-', 'log_phi*', 'M*', 'alpha']
    janus_results = analyze_results(sampler_janus, janus_params, "JANUS", uv_lf_data)

    # Trace plot
    plot_trace(sampler_janus, janus_params, "JANUS")

    # Corner plot
    flat_chain = sampler_janus.get_chain(flat=True, discard=BURN_IN)
    fig = corner.corner(flat_chain, labels=janus_params,
                       quantiles=[0.16, 0.5, 0.84],
                       show_titles=True, title_fmt='.3f')
    fig.suptitle(f'JANUS MCMC ({N_WALKERS} walkers, {N_STEPS} steps)', y=1.02)
    fig.savefig(FIGURES_DIR / 'janus_corner_improved.pdf')
    fig.savefig(FIGURES_DIR / 'janus_corner_improved.png')
    plt.close()
    print("\nSaved: janus_corner_improved.pdf/png")

    # Run LCDM MCMC
    print()
    print("="*70)
    print("LCDM MODEL")
    print("="*70)
    sampler_lcdm = run_mcmc_lcdm_improved(uv_lf_data)

    lcdm_params = ['H0', 'Omega_m', 'log_phi*', 'M*', 'alpha']
    lcdm_results = analyze_results(sampler_lcdm, lcdm_params, "LCDM", uv_lf_data)

    # Trace plot
    plot_trace(sampler_lcdm, lcdm_params, "LCDM")

    # Corner plot
    flat_chain = sampler_lcdm.get_chain(flat=True, discard=BURN_IN)
    fig = corner.corner(flat_chain, labels=lcdm_params,
                       quantiles=[0.16, 0.5, 0.84],
                       show_titles=True, title_fmt='.3f')
    fig.suptitle(f'LCDM MCMC ({N_WALKERS} walkers, {N_STEPS} steps)', y=1.02)
    fig.savefig(FIGURES_DIR / 'lcdm_corner_improved.pdf')
    fig.savefig(FIGURES_DIR / 'lcdm_corner_improved.png')
    plt.close()
    print("\nSaved: lcdm_corner_improved.pdf/png")

    # Model comparison
    print()
    print("="*70)
    print("MODEL COMPARISON")
    print("="*70)

    delta_bic = janus_results['BIC'] - lcdm_results['BIC']
    delta_aic = janus_results['AIC'] - lcdm_results['AIC']
    delta_chi2 = janus_results['chi2'] - lcdm_results['chi2']

    print(f"Δchi² (JANUS - LCDM) = {delta_chi2:.2f}")
    print(f"ΔBIC (JANUS - LCDM) = {delta_bic:.2f}")
    print(f"ΔAIC (JANUS - LCDM) = {delta_aic:.2f}")

    if delta_bic < -10:
        verdict = "Strong evidence for JANUS"
    elif delta_bic < -6:
        verdict = "Positive evidence for JANUS"
    elif delta_bic < 6:
        verdict = "Inconclusive"
    elif delta_bic < 10:
        verdict = "Positive evidence for LCDM"
    else:
        verdict = "Strong evidence for LCDM"

    print(f"Verdict: {verdict}")

    # Convergence comparison
    print()
    print("CONVERGENCE COMPARISON (R-hat):")
    print(f"  JANUS R-hat max: {janus_results['rhat_max']:.4f} {'OK' if janus_results['rhat_max'] < 1.1 else 'WARNING'}")
    print(f"  LCDM R-hat max: {lcdm_results['rhat_max']:.4f} {'OK' if lcdm_results['rhat_max'] < 1.1 else 'WARNING'}")

    # Age comparison
    print()
    print("Age of Universe Comparison:")
    print("| z  | JANUS (Gyr) | LCDM (Gyr) | Δt (Myr) |")
    print("|----|-------------|------------|----------|")

    janus = JANUSCosmology(
        H0=janus_results['H0']['median'],
        Omega_plus=janus_results['Omega_+']['median'],
        Omega_minus=janus_results['Omega_-']['median']
    )
    lcdm = LCDMCosmology(
        H0=lcdm_results['H0']['median'],
        Omega_m=lcdm_results['Omega_m']['median']
    )

    age_data = []
    for z in [0, 8, 10, 12, 14]:
        t_j = janus.age_of_universe(z)
        t_l = lcdm.age_of_universe(z)
        delta = (t_j - t_l) * 1000
        print(f"| {z:2d} | {t_j:11.3f} | {t_l:10.3f} | {delta:+8.1f} |")
        age_data.append({'z': z, 'janus': t_j, 'lcdm': t_l, 'delta_myr': delta})

    # Save results
    all_results = {
        'date': datetime.now().isoformat(),
        'mcmc_config': {
            'n_walkers': N_WALKERS,
            'n_steps': N_STEPS,
            'burn_in': BURN_IN,
            'algorithm': 'emcee.EnsembleSampler'
        },
        'janus': janus_results,
        'lcdm': lcdm_results,
        'comparison': {
            'delta_chi2': delta_chi2,
            'delta_bic': delta_bic,
            'delta_aic': delta_aic,
            'verdict': verdict
        },
        'ages': age_data,
        'note': "Improved MCMC with 128 walkers and 5000 steps for better convergence"
    }

    # Convert numpy types for JSON serialization
    def convert_types(obj):
        if isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_types(v) for v in obj]
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        else:
            return obj

    results_file = RESULTS_DIR / 'phase3_improved_results.json'
    with open(results_file, 'w') as f:
        json.dump(convert_types(all_results), f, indent=2)
    print(f"\nSaved: {results_file}")

    print()
    print("="*70)
    print("PHASE 3.2 IMPROVED - COMPLETE")
    print("="*70)

    return all_results


if __name__ == '__main__':
    results = main()
