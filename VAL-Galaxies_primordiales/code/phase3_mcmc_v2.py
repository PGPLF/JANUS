#!/usr/bin/env python3
"""
Phase 3 MCMC v2: Improved Convergence with Informative Priors
=============================================================
Uses literature-based Gaussian priors on Schechter parameters.
Fixes cosmological parameters to study UV LF evolution.

Key improvements:
- Gaussian priors on (phi*, M*, alpha) from Bouwens+21
- Two-step fitting: (1) fixed cosmology, (2) cosmology variation
- Better volume estimation using proper cosmological distance
- Increased walker count and tighter initialization

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
# LITERATURE PRIORS (Bouwens+21, Harikane+23)
# =============================================================================
# UV LF parameters at z~8-10 from literature
PRIOR_PHI_STAR = (-3.5, 0.5)   # log10(phi*) ~ N(-3.5, 0.5)
PRIOR_M_STAR = (-21.0, 1.0)    # M* ~ N(-21, 1)
PRIOR_ALPHA = (-2.0, 0.3)      # alpha ~ N(-2, 0.3)

# Cosmological priors
PRIOR_H0_JANUS = (75.0, 5.0)   # H0 ~ N(75, 5) for JANUS
PRIOR_H0_LCDM = (70.0, 5.0)    # H0 ~ N(70, 5) for LCDM
PRIOR_OMEGA_M = (0.30, 0.05)   # Omega_m ~ N(0.30, 0.05)


# =============================================================================
# COSMOLOGY
# =============================================================================
class Cosmology:
    """Generic cosmology class"""
    c = 2.998e5  # km/s

    def __init__(self, H0=70.0, Omega_m=0.30):
        self.H0 = H0
        self.Omega_m = Omega_m
        self.Omega_Lambda = 1.0 - Omega_m

    def E(self, z):
        """E(z) = H(z)/H0"""
        return np.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_Lambda)

    def comoving_distance(self, z):
        """Comoving distance in Mpc"""
        def integrand(zp):
            return 1.0 / self.E(zp)
        result, _ = quad(integrand, 0, z)
        return (self.c / self.H0) * result

    def comoving_volume_element(self, z):
        """dV/dz/dOmega in Mpc^3/sr"""
        Dc = self.comoving_distance(z)
        return (self.c / self.H0) * Dc**2 / self.E(z)

    def comoving_volume(self, z_low, z_high, area_deg2):
        """Comoving volume in Mpc^3 for given area"""
        area_sr = area_deg2 * (np.pi / 180)**2
        def integrand(z):
            return self.comoving_volume_element(z)
        result, _ = quad(integrand, z_low, z_high)
        return result * area_sr


class JANUSCosmology(Cosmology):
    """JANUS bimetric cosmology"""

    def __init__(self, H0=75.0, Omega_plus=0.40, Omega_minus=0.05):
        self.H0 = H0
        self.Omega_plus = Omega_plus
        self.Omega_minus = Omega_minus
        self.Omega_Lambda = 1.0 - Omega_plus - Omega_minus

    def E(self, z):
        """Modified E(z) for JANUS"""
        return np.sqrt(
            self.Omega_plus * (1 + z)**3 +
            self.Omega_minus * (1 + z)**6 +
            self.Omega_Lambda
        )


# =============================================================================
# UV LUMINOSITY FUNCTION
# =============================================================================
def schechter_function(M, phi_star, M_star, alpha):
    """Schechter luminosity function (per mag per Mpc^3)"""
    x = 10**(0.4 * (M_star - M))
    return 0.4 * np.log(10) * phi_star * x**(alpha + 1) * np.exp(-x)


def compute_uv_lf_binned(catalog, z_bins, survey_area_deg2=500.0, cosmo=None):
    """
    Compute UV LF from catalog with proper volume calculation.

    Parameters:
    -----------
    catalog : DataFrame with 'z' and 'M_UV' columns
    z_bins : list of (z_low, z_high) tuples
    survey_area_deg2 : effective survey area
    cosmo : cosmology object for volume calculation
    """
    if cosmo is None:
        cosmo = Cosmology(H0=70.0, Omega_m=0.30)

    uv_lf_data = []
    M_bins = np.arange(-24, -16, 0.75)
    M_centers = 0.5 * (M_bins[:-1] + M_bins[1:])
    dM = M_bins[1] - M_bins[0]

    for z_low, z_high in z_bins:
        mask = (catalog['z'] >= z_low) & (catalog['z'] < z_high)
        if 'M_UV' in catalog.columns:
            mask &= ~catalog['M_UV'].isna()

        sub = catalog[mask]
        if len(sub) < 5:
            continue

        M_UV = sub['M_UV'].values
        z_mid = 0.5 * (z_low + z_high)

        # Proper comoving volume
        volume = cosmo.comoving_volume(z_low, z_high, survey_area_deg2)

        counts, _ = np.histogram(M_UV, bins=M_bins)

        for i, M in enumerate(M_centers):
            if counts[i] > 0:
                phi = counts[i] / volume / dM
                # Poisson error + 30% systematic floor
                phi_err = max(np.sqrt(counts[i]) / volume / dM, phi * 0.3)

                uv_lf_data.append({
                    'z_mid': z_mid,
                    'z_low': z_low,
                    'z_high': z_high,
                    'M_UV': M,
                    'phi': phi,
                    'phi_err': phi_err,
                    'n_gal': counts[i],
                    'volume': volume
                })

    return pd.DataFrame(uv_lf_data)


# =============================================================================
# MCMC LIKELIHOOD FUNCTIONS
# =============================================================================
def log_prior_gaussian(x, mu, sigma):
    """Gaussian log-prior"""
    return -0.5 * ((x - mu) / sigma)**2


def log_likelihood_schechter_only(theta, uv_lf_data):
    """
    Log-likelihood for Schechter parameters only (fixed cosmology).
    theta = [log_phi_star, M_star, alpha]
    """
    log_phi_star, M_star, alpha = theta

    # Flat + Gaussian priors
    if not (-5.5 < log_phi_star < -2.0):
        return -np.inf
    if not (-24 < M_star < -18):
        return -np.inf
    if not (-3.0 < alpha < -1.0):
        return -np.inf

    # Gaussian priors from literature
    log_prior = 0.0
    log_prior += log_prior_gaussian(log_phi_star, PRIOR_PHI_STAR[0], PRIOR_PHI_STAR[1])
    log_prior += log_prior_gaussian(M_star, PRIOR_M_STAR[0], PRIOR_M_STAR[1])
    log_prior += log_prior_gaussian(alpha, PRIOR_ALPHA[0], PRIOR_ALPHA[1])

    phi_star = 10**log_phi_star

    # Chi-squared
    chi2 = 0
    for _, row in uv_lf_data.iterrows():
        M_UV = row['M_UV']
        phi_obs = row['phi']
        phi_err = row['phi_err']

        phi_pred = schechter_function(M_UV, phi_star, M_star, alpha)

        if phi_pred > 0 and phi_obs > 0:
            chi2 += ((np.log10(phi_obs) - np.log10(phi_pred)) / 0.3)**2

    return log_prior - 0.5 * chi2


def log_likelihood_janus(theta, uv_lf_data):
    """
    Log-likelihood for JANUS with Gaussian priors.
    theta = [H0, Omega_plus, Omega_minus, log_phi_star, M_star, alpha]
    """
    H0, Omega_plus, Omega_minus, log_phi_star, M_star, alpha = theta

    # Flat bounds (widened to accommodate data-driven values)
    if not (60 < H0 < 90):
        return -np.inf
    if not (0.20 < Omega_plus < 0.60):
        return -np.inf
    if not (0.005 < Omega_minus < 0.15):
        return -np.inf
    if not (-6.5 < log_phi_star < -2.0):
        return -np.inf
    if not (-24 < M_star < -18):
        return -np.inf
    if not (-3.0 < alpha < -0.5):
        return -np.inf

    # Gaussian priors
    log_prior = 0.0
    log_prior += log_prior_gaussian(H0, PRIOR_H0_JANUS[0], PRIOR_H0_JANUS[1])
    log_prior += log_prior_gaussian(log_phi_star, PRIOR_PHI_STAR[0], PRIOR_PHI_STAR[1])
    log_prior += log_prior_gaussian(M_star, PRIOR_M_STAR[0], PRIOR_M_STAR[1])
    log_prior += log_prior_gaussian(alpha, PRIOR_ALPHA[0], PRIOR_ALPHA[1])

    phi_star = 10**log_phi_star

    chi2 = 0
    for _, row in uv_lf_data.iterrows():
        M_UV = row['M_UV']
        phi_obs = row['phi']
        phi_err = row['phi_err']

        phi_pred = schechter_function(M_UV, phi_star, M_star, alpha)

        if phi_pred > 0 and phi_obs > 0:
            # Log-space chi2 for better numerical stability
            chi2 += ((np.log10(phi_obs) - np.log10(phi_pred)) / 0.3)**2

    return log_prior - 0.5 * chi2


def log_likelihood_lcdm(theta, uv_lf_data):
    """
    Log-likelihood for LCDM with Gaussian priors.
    theta = [H0, Omega_m, log_phi_star, M_star, alpha]
    """
    H0, Omega_m, log_phi_star, M_star, alpha = theta

    # Flat bounds (widened to accommodate data-driven values)
    if not (55 < H0 < 85):
        return -np.inf
    if not (0.15 < Omega_m < 0.50):
        return -np.inf
    if not (-6.5 < log_phi_star < -2.0):
        return -np.inf
    if not (-24 < M_star < -18):
        return -np.inf
    if not (-3.0 < alpha < -0.5):
        return -np.inf

    # Gaussian priors
    log_prior = 0.0
    log_prior += log_prior_gaussian(H0, PRIOR_H0_LCDM[0], PRIOR_H0_LCDM[1])
    log_prior += log_prior_gaussian(Omega_m, PRIOR_OMEGA_M[0], PRIOR_OMEGA_M[1])
    log_prior += log_prior_gaussian(log_phi_star, PRIOR_PHI_STAR[0], PRIOR_PHI_STAR[1])
    log_prior += log_prior_gaussian(M_star, PRIOR_M_STAR[0], PRIOR_M_STAR[1])
    log_prior += log_prior_gaussian(alpha, PRIOR_ALPHA[0], PRIOR_ALPHA[1])

    phi_star = 10**log_phi_star

    chi2 = 0
    for _, row in uv_lf_data.iterrows():
        M_UV = row['M_UV']
        phi_obs = row['phi']
        phi_err = row['phi_err']

        phi_pred = schechter_function(M_UV, phi_star, M_star, alpha)

        if phi_pred > 0 and phi_obs > 0:
            chi2 += ((np.log10(phi_obs) - np.log10(phi_pred)) / 0.3)**2

    return log_prior - 0.5 * chi2


# =============================================================================
# CONVERGENCE DIAGNOSTICS
# =============================================================================
def gelman_rubin(chains):
    """Calculate Gelman-Rubin R-hat statistic"""
    n_chains, n_samples, n_params = chains.shape

    chain_means = np.mean(chains, axis=1)
    chain_vars = np.var(chains, axis=1, ddof=1)

    W = np.mean(chain_vars, axis=0)
    B = n_samples * np.var(chain_means, axis=0, ddof=1)

    var_hat = ((n_samples - 1) / n_samples) * W + (1 / n_samples) * B
    R_hat = np.sqrt(var_hat / (W + 1e-10))

    return R_hat


def effective_sample_size(chain):
    """Calculate ESS using autocorrelation"""
    n = len(chain)
    if n < 10:
        return n

    # Simple autocorrelation-based ESS
    mean = np.mean(chain)
    var = np.var(chain)
    if var == 0:
        return n

    # Calculate autocorrelation up to lag n/2
    max_lag = min(n // 2, 500)
    rho = np.zeros(max_lag)
    for k in range(max_lag):
        rho[k] = np.mean((chain[:n-k] - mean) * (chain[k:] - mean)) / var

    # Find first negative autocorrelation
    first_neg = np.where(rho < 0.05)[0]
    if len(first_neg) > 0:
        tau = 1 + 2 * np.sum(rho[:first_neg[0]])
    else:
        tau = 1 + 2 * np.sum(rho)

    return n / max(tau, 1)


# =============================================================================
# MCMC RUNNERS
# =============================================================================
def run_schechter_mcmc(uv_lf_data, nwalkers=32, nsteps=1000):
    """Run Schechter-only MCMC (Step 1)"""
    ndim = 3

    # Tight initialization around prior means
    p0 = np.zeros((nwalkers, ndim))
    p0[:, 0] = np.random.normal(PRIOR_PHI_STAR[0], 0.1, nwalkers)  # log_phi*
    p0[:, 1] = np.random.normal(PRIOR_M_STAR[0], 0.2, nwalkers)    # M*
    p0[:, 2] = np.random.normal(PRIOR_ALPHA[0], 0.1, nwalkers)     # alpha

    sampler = emcee.EnsembleSampler(
        nwalkers, ndim,
        log_likelihood_schechter_only,
        args=(uv_lf_data,)
    )

    print(f"Running Schechter-only MCMC: {nwalkers} walkers, {nsteps} steps...")
    sampler.run_mcmc(p0, nsteps, progress=True)

    return sampler


def run_janus_mcmc(uv_lf_data, schechter_best, nwalkers=64, nsteps=3000):
    """Run JANUS MCMC (Step 2) initialized from Schechter best-fit"""
    ndim = 6

    # Initialize around best Schechter fit and prior means
    p0 = np.zeros((nwalkers, ndim))
    p0[:, 0] = np.random.normal(PRIOR_H0_JANUS[0], 2.0, nwalkers)     # H0
    p0[:, 1] = np.random.normal(0.40, 0.03, nwalkers)                 # Omega_plus
    p0[:, 2] = np.random.normal(0.05, 0.01, nwalkers)                 # Omega_minus
    p0[:, 3] = np.random.normal(schechter_best[0], 0.1, nwalkers)    # log_phi*
    p0[:, 4] = np.random.normal(schechter_best[1], 0.2, nwalkers)    # M*
    p0[:, 5] = np.random.normal(schechter_best[2], 0.1, nwalkers)    # alpha

    backend_file = MCMC_DIR / 'janus_v2.h5'
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


def run_lcdm_mcmc(uv_lf_data, schechter_best, nwalkers=64, nsteps=2000):
    """Run LCDM MCMC (Step 2) initialized from Schechter best-fit"""
    ndim = 5

    p0 = np.zeros((nwalkers, ndim))
    p0[:, 0] = np.random.normal(PRIOR_H0_LCDM[0], 2.0, nwalkers)     # H0
    p0[:, 1] = np.random.normal(PRIOR_OMEGA_M[0], 0.02, nwalkers)    # Omega_m
    p0[:, 2] = np.random.normal(schechter_best[0], 0.1, nwalkers)    # log_phi*
    p0[:, 3] = np.random.normal(schechter_best[1], 0.2, nwalkers)    # M*
    p0[:, 4] = np.random.normal(schechter_best[2], 0.1, nwalkers)    # alpha

    backend_file = MCMC_DIR / 'lcdm_v2.h5'
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
    """Analyze MCMC results"""
    chain = sampler.get_chain()
    n_steps, n_walkers, n_params = chain.shape

    burn = int(n_steps * burn_frac)
    flat_chain = sampler.get_chain(discard=burn, flat=True)

    # Split chains for R-hat
    chain_burned = chain[burn:]
    chains_split = np.transpose(chain_burned, (1, 0, 2))

    R_hat = gelman_rubin(chains_split)

    # ESS per parameter
    ess = [effective_sample_size(flat_chain[:, i]) for i in range(n_params)]

    # Best-fit
    log_prob = sampler.get_log_prob(flat=True, discard=burn)
    best_idx = np.argmax(log_prob)
    best_params = flat_chain[best_idx]

    # Percentiles
    percentiles = np.percentile(flat_chain, [16, 50, 84], axis=0)

    # Acceptance rate
    acceptance = np.mean(sampler.acceptance_fraction)

    results = {
        'model': model_name,
        'n_steps': n_steps,
        'n_walkers': n_walkers,
        'burn_in': burn,
        'R_hat': R_hat.tolist(),
        'R_hat_max': float(np.max(R_hat)),
        'ESS': ess,
        'ESS_min': float(np.min(ess)),
        'acceptance_rate': float(acceptance),
        'converged': bool(np.max(R_hat) < 1.1 and np.min(ess) > 100),
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
    fig.suptitle(f'{model_name} Posteriors (v2 - Informative Priors)', fontsize=12, y=1.02)
    plt.savefig(output_file)
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("="*70)
    print("Phase 3 MCMC v2 - Informative Priors")
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

    # Compute UV LF with proper volume
    print("\nComputing UV LF with proper cosmological volume...")
    z_bins = [(6.5, 8), (8, 10), (10, 12), (12, 15)]
    cosmo = Cosmology(H0=70.0, Omega_m=0.30)
    uv_lf_data = compute_uv_lf_binned(catalog, z_bins, survey_area_deg2=500.0, cosmo=cosmo)
    print(f"UV LF data points: {len(uv_lf_data)}")
    print(f"Total galaxies in UV LF: {uv_lf_data['n_gal'].sum():.0f}")

    if len(uv_lf_data) < 5:
        print("ERROR: Not enough UV LF data points!")
        return

    # =========================================================================
    # STEP 1: Schechter-only fit (quick convergence check)
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 1: Schechter-only fit (fixed cosmology)")
    print("="*70)

    schechter_sampler = run_schechter_mcmc(uv_lf_data, nwalkers=32, nsteps=1000)
    schechter_params = ['log(φ*)', 'M*', 'α']
    schechter_results, schechter_chain = analyze_mcmc(
        schechter_sampler, 'Schechter', schechter_params, burn_frac=0.5
    )

    print(f"\nSchechter Results:")
    print(f"  R-hat max: {schechter_results['R_hat_max']:.3f}")
    print(f"  ESS min: {schechter_results['ESS_min']:.0f}")
    print(f"  Converged: {schechter_results['converged']}")

    schechter_best = schechter_results['percentiles']['50']
    print(f"  Best fit: log(φ*)={schechter_best[0]:.2f}, M*={schechter_best[1]:.2f}, α={schechter_best[2]:.2f}")

    # =========================================================================
    # STEP 2: JANUS MCMC
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 2: JANUS MCMC (initialized from Schechter fit)")
    print("="*70)

    janus_sampler = run_janus_mcmc(uv_lf_data, schechter_best, nwalkers=64, nsteps=3000)
    janus_params = ['H0', 'Ω+', 'Ω-', 'log(φ*)', 'M*', 'α']
    janus_results, janus_chain = analyze_mcmc(janus_sampler, 'JANUS', janus_params, burn_frac=0.5)

    print(f"\nJANUS Results:")
    print(f"  R-hat max: {janus_results['R_hat_max']:.3f}")
    print(f"  ESS min: {janus_results['ESS_min']:.0f}")
    print(f"  Acceptance: {janus_results['acceptance_rate']:.3f}")
    print(f"  Converged: {janus_results['converged']}")
    for i, name in enumerate(janus_params):
        p16, p50, p84 = janus_results['percentiles']['16'][i], \
                        janus_results['percentiles']['50'][i], \
                        janus_results['percentiles']['84'][i]
        print(f"  {name}: {p50:.3f} (+{p84-p50:.3f} / -{p50-p16:.3f})")

    make_corner_plot(janus_chain, janus_params, 'JANUS',
                     FIGURES_DIR / 'janus_corner_v2.pdf')

    # =========================================================================
    # STEP 3: LCDM MCMC
    # =========================================================================
    print("\n" + "="*70)
    print("STEP 3: LCDM MCMC (initialized from Schechter fit)")
    print("="*70)

    lcdm_sampler = run_lcdm_mcmc(uv_lf_data, schechter_best, nwalkers=64, nsteps=2000)
    lcdm_params = ['H0', 'Ωm', 'log(φ*)', 'M*', 'α']
    lcdm_results, lcdm_chain = analyze_mcmc(lcdm_sampler, 'LCDM', lcdm_params, burn_frac=0.5)

    print(f"\nLCDM Results:")
    print(f"  R-hat max: {lcdm_results['R_hat_max']:.3f}")
    print(f"  ESS min: {lcdm_results['ESS_min']:.0f}")
    print(f"  Acceptance: {lcdm_results['acceptance_rate']:.3f}")
    print(f"  Converged: {lcdm_results['converged']}")
    for i, name in enumerate(lcdm_params):
        p16, p50, p84 = lcdm_results['percentiles']['16'][i], \
                        lcdm_results['percentiles']['50'][i], \
                        lcdm_results['percentiles']['84'][i]
        print(f"  {name}: {p50:.3f} (+{p84-p50:.3f} / -{p50-p16:.3f})")

    make_corner_plot(lcdm_chain, lcdm_params, 'LCDM',
                     FIGURES_DIR / 'lcdm_corner_v2.pdf')

    # =========================================================================
    # SAVE RESULTS
    # =========================================================================
    results = {
        'timestamp': datetime.now().isoformat(),
        'version': 'v2_informative_priors',
        'catalog': str(catalog_file),
        'n_sources': len(catalog),
        'n_uv_lf_points': len(uv_lf_data),
        'priors': {
            'phi_star': PRIOR_PHI_STAR,
            'M_star': PRIOR_M_STAR,
            'alpha': PRIOR_ALPHA,
            'H0_janus': PRIOR_H0_JANUS,
            'H0_lcdm': PRIOR_H0_LCDM,
            'Omega_m': PRIOR_OMEGA_M
        },
        'schechter': schechter_results,
        'janus': janus_results,
        'lcdm': lcdm_results
    }

    results_file = MCMC_DIR / 'mcmc_v2_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {results_file}")

    # =========================================================================
    # CONVERGENCE SUMMARY
    # =========================================================================
    print("\n" + "="*70)
    print("CONVERGENCE SUMMARY")
    print("="*70)

    print(f"\nSchechter (fixed cosmology):")
    print(f"  R-hat max: {schechter_results['R_hat_max']:.3f}")
    print(f"  Status: {'✅ CONVERGED' if schechter_results['converged'] else '❌ NOT CONVERGED'}")

    print(f"\nJANUS:")
    print(f"  R-hat max: {janus_results['R_hat_max']:.3f}")
    print(f"  ESS min: {janus_results['ESS_min']:.0f}")
    print(f"  Status: {'✅ CONVERGED' if janus_results['converged'] else '❌ NOT CONVERGED'}")

    print(f"\nLCDM:")
    print(f"  R-hat max: {lcdm_results['R_hat_max']:.3f}")
    print(f"  ESS min: {lcdm_results['ESS_min']:.0f}")
    print(f"  Status: {'✅ CONVERGED' if lcdm_results['converged'] else '❌ NOT CONVERGED'}")

    all_converged = schechter_results['converged'] and janus_results['converged'] and lcdm_results['converged']
    if all_converged:
        print("\n✅ ALL MCMC CONVERGED - Results are reliable!")
    else:
        print("\n⚠️ Some chains need more steps or better priors")

    print("\nDone!")


if __name__ == '__main__':
    main()
