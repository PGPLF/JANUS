#!/usr/bin/env python3
"""
Phase 3 Corrected Execution
============================
Run MCMC with corrected cosmology modules (validated janus.py and lcdm.py)
Uses 2000 steps for better convergence (R-hat < 1.1)

Author: VAL-Galaxies_primordiales
Date: 2026-01-08
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
RESULTS_DIR = BASE_DIR / 'results/v2_corrected'
FIGURES_DIR = RESULTS_DIR / 'figures'
MCMC_DIR = RESULTS_DIR / 'mcmc'

# Create directories
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
MCMC_DIR.mkdir(parents=True, exist_ok=True)

# Plot settings
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'figure.figsize': (8, 6),
    'figure.dpi': 150,
    'savefig.dpi': 300
})


def run_mcmc_janus_corrected(uv_lf_data, nwalkers=64, nsteps=2000):
    """Run JANUS MCMC with more iterations for convergence"""
    ndim = 6

    # Fresh run - remove old backend
    backend_file = str(MCMC_DIR / 'janus_corrected.h5')
    if os.path.exists(backend_file):
        os.remove(backend_file)

    # Initial positions (tighter around expected values)
    p0 = np.zeros((nwalkers, ndim))
    p0[:, 0] = np.random.uniform(68, 75, nwalkers)      # H0
    p0[:, 1] = np.random.uniform(0.25, 0.35, nwalkers)  # Omega_plus
    p0[:, 2] = np.random.uniform(0.02, 0.08, nwalkers)  # Omega_minus
    p0[:, 3] = np.random.uniform(-4.0, -3.5, nwalkers)  # log_phi_star
    p0[:, 4] = np.random.uniform(-21.5, -20.5, nwalkers)# M_star
    p0[:, 5] = np.random.uniform(-2.2, -1.8, nwalkers)  # alpha

    # Setup backend
    backend = emcee.backends.HDFBackend(backend_file)
    backend.reset(nwalkers, ndim)

    # Create sampler
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim,
        lambda p: log_posterior_janus(p, uv_lf_data),
        backend=backend
    )

    # Run
    print(f"Running JANUS MCMC ({nwalkers} walkers, {nsteps} steps)...")
    sampler.run_mcmc(p0, nsteps, progress=True)

    return sampler


def run_mcmc_lcdm_corrected(uv_lf_data, nwalkers=64, nsteps=2000):
    """Run LCDM MCMC with more iterations for convergence"""
    ndim = 5

    # Fresh run - remove old backend
    backend_file = str(MCMC_DIR / 'lcdm_corrected.h5')
    if os.path.exists(backend_file):
        os.remove(backend_file)

    # Initial positions
    p0 = np.zeros((nwalkers, ndim))
    p0[:, 0] = np.random.uniform(65, 70, nwalkers)      # H0
    p0[:, 1] = np.random.uniform(0.28, 0.35, nwalkers)  # Omega_m
    p0[:, 2] = np.random.uniform(-4.0, -3.5, nwalkers)  # log_phi_star
    p0[:, 3] = np.random.uniform(-21.5, -20.5, nwalkers)# M_star
    p0[:, 4] = np.random.uniform(-2.2, -1.8, nwalkers)  # alpha

    # Setup backend
    backend = emcee.backends.HDFBackend(backend_file)
    backend.reset(nwalkers, ndim)

    # Create sampler
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim,
        lambda p: log_posterior_lcdm(p, uv_lf_data),
        backend=backend
    )

    # Run
    print(f"Running LCDM MCMC ({nwalkers} walkers, {nsteps} steps)...")
    sampler.run_mcmc(p0, nsteps, progress=True)

    return sampler


def analyze_results(sampler, param_names, model_name, uv_lf_data):
    """Analyze MCMC results and compute diagnostics"""
    chain = sampler.get_chain()

    # Convergence diagnostics
    acc_rate = np.mean(sampler.acceptance_fraction)

    burnin = chain.shape[0] // 2
    rhat = calculate_rhat(chain[burnin:].transpose(1, 0, 2))

    print(f"\n{model_name} Convergence Diagnostics:")
    print(f"  Acceptance rate: {acc_rate:.3f} (target: 0.2-0.5)")
    print(f"  R-hat max: {np.max(rhat):.4f} (target: < 1.1)")
    for name, r in zip(param_names, rhat):
        print(f"    {name}: {r:.4f}")

    # Best-fit parameters
    flat_chain = sampler.get_chain(flat=True, discard=burnin)

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
    results['acceptance'] = float(acc_rate)

    print(f"\nGoodness of fit:")
    print(f"  chi2 = {chi2:.2f}")
    print(f"  Reduced chi2 = {chi2/(n_data-n_params):.2f}")
    print(f"  BIC = {results['BIC']:.2f}")
    print(f"  AIC = {results['AIC']:.2f}")

    return results


def main():
    print("="*70)
    print("PHASE 3 CORRECTED - MCMC EXECUTION")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Verify cosmology modules
    print("Testing corrected cosmology modules...")
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
    sampler_janus = run_mcmc_janus_corrected(uv_lf_data, nwalkers=64, nsteps=2000)

    janus_params = ['H0', 'Omega_+', 'Omega_-', 'log_phi*', 'M*', 'alpha']
    janus_results = analyze_results(sampler_janus, janus_params, "JANUS", uv_lf_data)

    # Corner plot
    flat_chain = sampler_janus.get_chain(flat=True, discard=1000)
    fig = corner.corner(flat_chain, labels=janus_params,
                       quantiles=[0.16, 0.5, 0.84],
                       show_titles=True, title_fmt='.3f')
    fig.savefig(FIGURES_DIR / 'janus_corner_corrected.pdf')
    fig.savefig(FIGURES_DIR / 'janus_corner_corrected.png')
    plt.close()
    print("\nSaved: janus_corner_corrected.pdf/png")

    # Run LCDM MCMC
    print()
    print("="*70)
    print("LCDM MODEL")
    print("="*70)
    sampler_lcdm = run_mcmc_lcdm_corrected(uv_lf_data, nwalkers=64, nsteps=2000)

    lcdm_params = ['H0', 'Omega_m', 'log_phi*', 'M*', 'alpha']
    lcdm_results = analyze_results(sampler_lcdm, lcdm_params, "LCDM", uv_lf_data)

    # Corner plot
    flat_chain = sampler_lcdm.get_chain(flat=True, discard=1000)
    fig = corner.corner(flat_chain, labels=lcdm_params,
                       quantiles=[0.16, 0.5, 0.84],
                       show_titles=True, title_fmt='.3f')
    fig.savefig(FIGURES_DIR / 'lcdm_corner_corrected.pdf')
    fig.savefig(FIGURES_DIR / 'lcdm_corner_corrected.png')
    plt.close()
    print("\nSaved: lcdm_corner_corrected.pdf/png")

    # Model comparison
    print()
    print("="*70)
    print("MODEL COMPARISON")
    print("="*70)

    delta_bic = janus_results['BIC'] - lcdm_results['BIC']
    delta_aic = janus_results['AIC'] - lcdm_results['AIC']

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
        'janus': janus_results,
        'lcdm': lcdm_results,
        'comparison': {
            'delta_bic': delta_bic,
            'delta_aic': delta_aic,
            'verdict': verdict
        },
        'ages': age_data,
        'note': "JANUS gives LESS time than LCDM (no dark energy equivalent in bimetric equation)"
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

    results_file = RESULTS_DIR / 'phase3_corrected_results.json'
    with open(results_file, 'w') as f:
        json.dump(convert_types(all_results), f, indent=2)
    print(f"\nSaved: {results_file}")

    print()
    print("="*70)
    print("PHASE 3 CORRECTED - COMPLETE")
    print("="*70)

    return all_results


if __name__ == '__main__':
    results = main()
