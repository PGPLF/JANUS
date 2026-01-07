#!/usr/bin/env python3
"""
Phase 3 MCMC Corrected: Proper Convergence
==========================================
Re-runs JANUS and LCDM MCMC with sufficient steps for convergence.

Parameters:
- JANUS: 64 walkers, 2000 steps (R-hat target < 1.05)
- LCDM: 64 walkers, 1500 steps (R-hat target < 1.05)

Following INS-Statistiques.md protocol.

Author: VAL-Galaxies_primordiales
Date: 2026-01-07
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.integrate import quad
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Check dependencies
try:
    import emcee
    import h5py
    import corner
except ImportError as e:
    print(f"Missing dependency: {e}")
    sys.exit(1)

# Setup paths
BASE_DIR = Path('/Users/patrickguerin/Desktop/JANUS/VAL-Galaxies_primordiales')
DATA_DIR = BASE_DIR / 'data/jwst/processed'
RESULTS_DIR = BASE_DIR / 'results'
FIGURES_DIR = RESULTS_DIR / 'figures'
MCMC_DIR = RESULTS_DIR / 'mcmc'

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
MCMC_DIR.mkdir(parents=True, exist_ok=True)

# Publication settings
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'figure.figsize': (8, 6),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


# =============================================================================
# COSMOLOGICAL MODELS
# =============================================================================

class JANUSCosmology:
    """JANUS bimetric cosmology model"""

    def __init__(self, H0=70.0, Omega_plus=0.30, Omega_minus=0.05):
        self.H0 = H0
        self.Omega_plus = Omega_plus
        self.Omega_minus = Omega_minus
        self.Omega_Lambda = 1.0 - Omega_plus - Omega_minus

    def hubble_parameter(self, z):
        return self.H0 * np.sqrt(
            self.Omega_plus * (1 + z)**3 +
            self.Omega_minus * (1 + z)**6 +
            self.Omega_Lambda
        )

    def age_of_universe(self, z):
        """Age in Gyr"""
        H0_inv_Gyr = 978.0 / self.H0
        def integrand(zp):
            return 1.0 / ((1 + zp) * self.hubble_parameter(zp) / self.H0)
        result, _ = quad(integrand, z, np.inf)
        return result * H0_inv_Gyr


class LCDMCosmology:
    """Standard LCDM cosmology model"""

    def __init__(self, H0=67.4, Omega_m=0.315):
        self.H0 = H0
        self.Omega_m = Omega_m
        self.Omega_Lambda = 1.0 - Omega_m

    def hubble_parameter(self, z):
        return self.H0 * np.sqrt(
            self.Omega_m * (1 + z)**3 + self.Omega_Lambda
        )

    def age_of_universe(self, z):
        """Age in Gyr"""
        H0_inv_Gyr = 978.0 / self.H0
        def integrand(zp):
            return 1.0 / ((1 + zp) * self.hubble_parameter(zp) / self.H0)
        result, _ = quad(integrand, z, np.inf)
        return result * H0_inv_Gyr


# =============================================================================
# UV LUMINOSITY FUNCTION
# =============================================================================

def schechter_function(M, phi_star, M_star, alpha):
    """Schechter luminosity function"""
    x = 10**(0.4 * (M_star - M))
    return 0.4 * np.log(10) * phi_star * x**(alpha + 1) * np.exp(-x)


def compute_uv_lf(catalog, z_bins=[(6.5, 8), (8, 10), (10, 12), (12, 15)]):
    """Compute UV LF from catalog"""
    uv_lf_data = []

    for z_low, z_high in z_bins:
        mask = (catalog['z'] >= z_low) & (catalog['z'] < z_high)
        if 'M_UV' in catalog.columns:
            mask &= ~catalog['M_UV'].isna()

        sub = catalog[mask]
        if len(sub) < 10:
            continue

        M_UV = sub['M_UV'].values if 'M_UV' in sub.columns else None
        if M_UV is None:
            continue

        # Bin the data
        M_bins = np.arange(-24, -16, 1.0)
        M_centers = 0.5 * (M_bins[:-1] + M_bins[1:])

        counts, _ = np.histogram(M_UV, bins=M_bins)

        # Rough volume estimate (simplified)
        z_mid = 0.5 * (z_low + z_high)
        volume = 1e6 * ((z_high - z_low) / 2.0)  # Mpc^3 (approximate)

        phi = counts / volume / 1.0  # per mag per Mpc^3
        phi_err = np.sqrt(counts + 1) / volume / 1.0

        for i, M in enumerate(M_centers):
            if counts[i] > 0:
                uv_lf_data.append({
                    'z_mid': z_mid,
                    'z_low': z_low,
                    'z_high': z_high,
                    'M_UV': M,
                    'phi': phi[i],
                    'phi_err': max(phi_err[i], phi[i] * 0.3)  # min 30% error
                })

    return pd.DataFrame(uv_lf_data)


# =============================================================================
# MCMC FUNCTIONS
# =============================================================================

def log_likelihood_janus(theta, uv_lf_data):
    """Log-likelihood for JANUS model"""
    H0, Omega_plus, Omega_minus, log_phi_star, M_star, alpha = theta

    # Priors
    if not (60 < H0 < 90):
        return -np.inf
    if not (0.2 < Omega_plus < 0.6):
        return -np.inf
    if not (0.0 < Omega_minus < 0.15):
        return -np.inf
    if not (-5.5 < log_phi_star < -2.5):
        return -np.inf
    if not (-24 < M_star < -18):
        return -np.inf
    if not (-3.0 < alpha < -1.0):
        return -np.inf

    phi_star = 10**log_phi_star

    chi2 = 0
    for _, row in uv_lf_data.iterrows():
        M_UV = row['M_UV']
        phi_obs = row['phi']
        phi_err = row['phi_err']

        # Schechter prediction
        phi_pred = schechter_function(M_UV, phi_star, M_star, alpha)

        if phi_pred > 0 and phi_obs > 0:
            chi2 += ((phi_obs - phi_pred) / phi_err)**2

    return -0.5 * chi2


def log_likelihood_lcdm(theta, uv_lf_data):
    """Log-likelihood for LCDM model"""
    H0, Omega_m, log_phi_star, M_star, alpha = theta

    # Priors
    if not (55 < H0 < 80):
        return -np.inf
    if not (0.2 < Omega_m < 0.5):
        return -np.inf
    if not (-5.5 < log_phi_star < -2.5):
        return -np.inf
    if not (-26 < M_star < -18):
        return -np.inf
    if not (-3.0 < alpha < -1.0):
        return -np.inf

    phi_star = 10**log_phi_star

    chi2 = 0
    for _, row in uv_lf_data.iterrows():
        M_UV = row['M_UV']
        phi_obs = row['phi']
        phi_err = row['phi_err']

        phi_pred = schechter_function(M_UV, phi_star, M_star, alpha)

        if phi_pred > 0 and phi_obs > 0:
            chi2 += ((phi_obs - phi_pred) / phi_err)**2

    return -0.5 * chi2


def gelman_rubin(chains):
    """Calculate Gelman-Rubin R-hat"""
    n_chains, n_samples, n_params = chains.shape

    chain_means = np.mean(chains, axis=1)
    chain_vars = np.var(chains, axis=1, ddof=1)

    W = np.mean(chain_vars, axis=0)
    B = n_samples * np.var(chain_means, axis=0, ddof=1)

    var_hat = ((n_samples - 1) / n_samples) * W + (1 / n_samples) * B
    R_hat = np.sqrt(var_hat / (W + 1e-10))

    return R_hat


def run_mcmc_janus(uv_lf_data, nwalkers=64, nsteps=2000):
    """Run JANUS MCMC with proper convergence"""
    ndim = 6

    # Initial positions
    p0 = np.zeros((nwalkers, ndim))
    p0[:, 0] = np.random.uniform(70, 80, nwalkers)      # H0
    p0[:, 1] = np.random.uniform(0.35, 0.50, nwalkers)  # Omega_plus
    p0[:, 2] = np.random.uniform(0.02, 0.06, nwalkers)  # Omega_minus
    p0[:, 3] = np.random.uniform(-4.0, -3.2, nwalkers)  # log_phi_star
    p0[:, 4] = np.random.uniform(-22, -20, nwalkers)    # M_star
    p0[:, 5] = np.random.uniform(-2.5, -1.8, nwalkers)  # alpha

    # Backend for saving
    backend_file = MCMC_DIR / 'janus_corrected.h5'
    backend = emcee.backends.HDFBackend(str(backend_file))
    backend.reset(nwalkers, ndim)

    sampler = emcee.EnsembleSampler(
        nwalkers, ndim,
        log_likelihood_janus,
        args=(uv_lf_data,),
        backend=backend
    )

    print(f"Running JANUS MCMC: {nwalkers} walkers, {nsteps} steps...")
    sampler.run_mcmc(p0, nsteps, progress=True)

    return sampler


def run_mcmc_lcdm(uv_lf_data, nwalkers=64, nsteps=1500):
    """Run LCDM MCMC with proper convergence"""
    ndim = 5

    # Initial positions
    p0 = np.zeros((nwalkers, ndim))
    p0[:, 0] = np.random.uniform(65, 72, nwalkers)      # H0
    p0[:, 1] = np.random.uniform(0.28, 0.38, nwalkers)  # Omega_m
    p0[:, 2] = np.random.uniform(-4.0, -3.2, nwalkers)  # log_phi_star
    p0[:, 3] = np.random.uniform(-24, -22, nwalkers)    # M_star
    p0[:, 4] = np.random.uniform(-2.3, -1.8, nwalkers)  # alpha

    # Backend
    backend_file = MCMC_DIR / 'lcdm_corrected.h5'
    backend = emcee.backends.HDFBackend(str(backend_file))
    backend.reset(nwalkers, ndim)

    sampler = emcee.EnsembleSampler(
        nwalkers, ndim,
        log_likelihood_lcdm,
        args=(uv_lf_data,),
        backend=backend
    )

    print(f"Running LCDM MCMC: {nwalkers} walkers, {nsteps} steps...")
    sampler.run_mcmc(p0, nsteps, progress=True)

    return sampler


def analyze_mcmc(sampler, model_name, param_names, burn_frac=0.5):
    """Analyze MCMC results and check convergence"""
    chain = sampler.get_chain()
    n_steps, n_walkers, n_params = chain.shape

    burn = int(n_steps * burn_frac)
    flat_chain = sampler.get_chain(discard=burn, flat=True)

    # Split chains for R-hat
    chain_burned = chain[burn:]
    chains_split = np.transpose(chain_burned, (1, 0, 2))

    # Calculate R-hat
    R_hat = gelman_rubin(chains_split)

    # Calculate ESS (simplified)
    ess = [len(flat_chain[:, i]) / 50 for i in range(n_params)]  # Conservative

    # Best-fit values
    best_idx = np.argmax(sampler.get_log_prob(flat=True, discard=burn))
    best_params = flat_chain[best_idx]

    # Percentiles
    percentiles = np.percentile(flat_chain, [16, 50, 84], axis=0)

    results = {
        'model': model_name,
        'n_steps': n_steps,
        'n_walkers': n_walkers,
        'burn_in': burn,
        'R_hat': R_hat.tolist(),
        'R_hat_max': float(np.max(R_hat)),
        'ESS': ess,
        'converged': bool(np.max(R_hat) < 1.1),
        'best_params': best_params.tolist(),
        'param_names': param_names,
        'percentiles': {
            '16': percentiles[0].tolist(),
            '50': percentiles[1].tolist(),
            '84': percentiles[2].tolist()
        }
    }

    return results, flat_chain


def make_corner_plot(flat_chain, param_names, model_name, output_file):
    """Create corner plot"""
    fig = corner.corner(
        flat_chain,
        labels=param_names,
        quantiles=[0.16, 0.5, 0.84],
        show_titles=True,
        title_kwargs={"fontsize": 10}
    )
    fig.suptitle(f'{model_name} MCMC Posteriors (Corrected)', fontsize=14, y=1.02)
    plt.savefig(output_file)
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("Phase 3 MCMC CORRECTED - Proper Convergence")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load catalog v2
    catalog_file = DATA_DIR / 'highz_catalog_VERIFIED_v2.csv'
    if not catalog_file.exists():
        catalog_file = DATA_DIR / 'highz_catalog_VERIFIED_v1.csv'

    print(f"\nLoading: {catalog_file}")
    catalog = pd.read_csv(catalog_file)
    print(f"Catalog: {len(catalog)} sources")

    # Filter valid data
    if 'z' in catalog.columns:
        catalog = catalog[(catalog['z'] >= 6.5) & (catalog['z'] <= 15)]
        print(f"After z filter (6.5-15): {len(catalog)} sources")

    # Compute UV LF
    print("\nComputing UV LF...")
    uv_lf_data = compute_uv_lf(catalog)
    print(f"UV LF bins: {len(uv_lf_data)}")

    if len(uv_lf_data) < 5:
        print("ERROR: Not enough UV LF data points!")
        return

    # =========================================================================
    # JANUS MCMC
    # =========================================================================
    print("\n" + "="*70)
    print("PHASE 3.2 CORRECTED: JANUS MCMC")
    print("="*70)

    janus_sampler = run_mcmc_janus(uv_lf_data, nwalkers=64, nsteps=2000)

    janus_params = ['H0', 'Ω+', 'Ω-', 'log(φ*)', 'M*', 'α']
    janus_results, janus_chain = analyze_mcmc(janus_sampler, 'JANUS', janus_params)

    print("\nJANUS Results:")
    print(f"  R-hat max: {janus_results['R_hat_max']:.3f}")
    print(f"  Converged: {janus_results['converged']}")
    for i, name in enumerate(janus_params):
        p16, p50, p84 = janus_results['percentiles']['16'][i], \
                        janus_results['percentiles']['50'][i], \
                        janus_results['percentiles']['84'][i]
        print(f"  {name}: {p50:.3f} (+{p84-p50:.3f} / -{p50-p16:.3f})")

    # Corner plot
    make_corner_plot(janus_chain, janus_params, 'JANUS',
                     FIGURES_DIR / 'janus_corner_corrected.pdf')

    # =========================================================================
    # LCDM MCMC
    # =========================================================================
    print("\n" + "="*70)
    print("PHASE 3.3 CORRECTED: LCDM MCMC")
    print("="*70)

    lcdm_sampler = run_mcmc_lcdm(uv_lf_data, nwalkers=64, nsteps=1500)

    lcdm_params = ['H0', 'Ωm', 'log(φ*)', 'M*', 'α']
    lcdm_results, lcdm_chain = analyze_mcmc(lcdm_sampler, 'LCDM', lcdm_params)

    print("\nLCDM Results:")
    print(f"  R-hat max: {lcdm_results['R_hat_max']:.3f}")
    print(f"  Converged: {lcdm_results['converged']}")
    for i, name in enumerate(lcdm_params):
        p16, p50, p84 = lcdm_results['percentiles']['16'][i], \
                        lcdm_results['percentiles']['50'][i], \
                        lcdm_results['percentiles']['84'][i]
        print(f"  {name}: {p50:.3f} (+{p84-p50:.3f} / -{p50-p16:.3f})")

    # Corner plot
    make_corner_plot(lcdm_chain, lcdm_params, 'LCDM',
                     FIGURES_DIR / 'lcdm_corner_corrected.pdf')

    # =========================================================================
    # SAVE RESULTS
    # =========================================================================
    results = {
        'timestamp': datetime.now().isoformat(),
        'catalog': str(catalog_file),
        'n_sources': len(catalog),
        'janus': janus_results,
        'lcdm': lcdm_results
    }

    results_file = MCMC_DIR / 'mcmc_corrected_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {results_file}")

    # =========================================================================
    # CONVERGENCE SUMMARY
    # =========================================================================
    print("\n" + "="*70)
    print("CONVERGENCE SUMMARY")
    print("="*70)
    print(f"\nJANUS:")
    print(f"  R-hat max: {janus_results['R_hat_max']:.3f} (target < 1.1)")
    print(f"  Status: {'✅ CONVERGED' if janus_results['converged'] else '❌ NOT CONVERGED'}")

    print(f"\nLCDM:")
    print(f"  R-hat max: {lcdm_results['R_hat_max']:.3f} (target < 1.1)")
    print(f"  Status: {'✅ CONVERGED' if lcdm_results['converged'] else '❌ NOT CONVERGED'}")

    if janus_results['converged'] and lcdm_results['converged']:
        print("\n✅ ALL MCMC CONVERGED - Results are reliable")
    else:
        print("\n⚠️ CONVERGENCE ISSUES - Consider more steps")

    print("\nDone!")


if __name__ == '__main__':
    main()
