"""
Statistical Fitting and Model Comparison

Implements MCMC sampling, likelihood functions, and information criteria
for comparing JANUS vs ΛCDM models.

Conforme à INS-Statistiques.md pour checkpoints et monitoring.
"""

import numpy as np
import emcee
import h5py
from scipy.stats import norm
import warnings


def log_likelihood(params, model, data, errors):
    """
    Log-likelihood function (chi-squared)

    Parameters
    ----------
    params : array-like
        Model parameters
    model : callable
        Model function that takes params and returns predictions
    data : array
        Observed data
    errors : array
        Observational errors

    Returns
    -------
    log_L : float
        Log-likelihood value
    """
    predictions = model(params)

    # Chi-squared
    chi2 = np.sum(((data - predictions) / errors)**2)

    # Log-likelihood (assuming Gaussian errors)
    log_L = -0.5 * chi2

    return log_L


def log_prior(params, bounds):
    """
    Log-prior function (uniform priors within bounds)

    Parameters
    ----------
    params : array-like
        Model parameters
    bounds : list of tuples
        [(min1, max1), (min2, max2), ...] for each parameter

    Returns
    -------
    log_P : float
        Log-prior value
    """
    for param, (pmin, pmax) in zip(params, bounds):
        if not (pmin < param < pmax):
            return -np.inf  # Outside prior bounds

    return 0.0  # Flat prior within bounds


def log_posterior(params, model, data, errors, bounds):
    """
    Log-posterior function

    Parameters
    ----------
    params : array-like
        Model parameters
    model : callable
        Model function
    data : array
        Observed data
    errors : array
        Observational errors
    bounds : list of tuples
        Parameter bounds for priors

    Returns
    -------
    log_post : float
        Log-posterior value
    """
    lp = log_prior(params, bounds)
    if not np.isfinite(lp):
        return -np.inf

    ll = log_likelihood(params, model, data, errors)

    return lp + ll


def run_mcmc(log_prob_fn, initial_params, nwalkers=32, nsteps=5000,
             burn_in=500, backend_file=None, progress=True):
    """
    Run MCMC sampling with emcee

    Parameters
    ----------
    log_prob_fn : callable
        Log-probability function (posterior)
    initial_params : array
        Initial parameter values
    nwalkers : int, optional
        Number of MCMC walkers. Default: 32
    nsteps : int, optional
        Number of steps per walker. Default: 5000
    burn_in : int, optional
        Number of burn-in steps to discard. Default: 500
    backend_file : str, optional
        HDF5 file for checkpointing. If None, no checkpointing.
    progress : bool, optional
        Show progress bar. Default: True

    Returns
    -------
    sampler : emcee.EnsembleSampler
        MCMC sampler object with results
    samples : array
        Flattened MCMC samples (post burn-in)
    """
    ndim = len(initial_params)

    # Initialize walkers in a small ball around initial params
    pos = initial_params + 1e-4 * np.random.randn(nwalkers, ndim)

    # Setup backend for checkpointing (conforme INS-Statistiques.md)
    backend = None
    if backend_file is not None:
        backend = emcee.backends.HDFBackend(backend_file)
        backend.reset(nwalkers, ndim)

    # Create sampler
    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob_fn, backend=backend)

    # Run MCMC
    print(f"Running MCMC with {nwalkers} walkers for {nsteps} steps...")
    sampler.run_mcmc(pos, nsteps, progress=progress)

    # Get samples (discard burn-in)
    samples = sampler.get_chain(discard=burn_in, flat=True)

    print(f"MCMC complete. Final chain shape: {samples.shape}")
    print(f"Mean acceptance fraction: {np.mean(sampler.acceptance_fraction):.3f}")

    # Check convergence
    try:
        tau = sampler.get_autocorr_time(quiet=True)
        print(f"Autocorrelation time: {tau}")
    except emcee.autocorr.AutocorrError:
        warnings.warn("Autocorrelation time could not be reliably estimated. "
                      "Chain may not be converged.")

    return sampler, samples


def compute_aic(log_likelihood, n_params, n_data):
    """
    Compute Akaike Information Criterion

    AIC = 2k - 2ln(L)

    Parameters
    ----------
    log_likelihood : float
        Maximum log-likelihood
    n_params : int
        Number of model parameters
    n_data : int
        Number of data points

    Returns
    -------
    aic : float
        AIC value (lower is better)
    """
    aic = 2 * n_params - 2 * log_likelihood

    # Corrected AIC for small sample sizes
    if n_data / n_params < 40:
        aicc = aic + (2 * n_params**2 + 2 * n_params) / (n_data - n_params - 1)
        return aicc

    return aic


def compute_bic(log_likelihood, n_params, n_data):
    """
    Compute Bayesian Information Criterion

    BIC = k*ln(n) - 2ln(L)

    Parameters
    ----------
    log_likelihood : float
        Maximum log-likelihood
    n_params : int
        Number of model parameters
    n_data : int
        Number of data points

    Returns
    -------
    bic : float
        BIC value (lower is better)
    """
    bic = n_params * np.log(n_data) - 2 * log_likelihood
    return bic


def compute_dic(samples, log_likelihood_fn):
    """
    Compute Deviance Information Criterion

    DIC = p_D + D_bar
    where p_D = D_bar - D(theta_bar)

    Parameters
    ----------
    samples : array
        MCMC samples (n_samples, n_params)
    log_likelihood_fn : callable
        Log-likelihood function

    Returns
    -------
    dic : float
        DIC value (lower is better)
    p_d : float
        Effective number of parameters
    """
    # Deviance = -2 * log_likelihood
    deviances = np.array([-2 * log_likelihood_fn(sample) for sample in samples])

    D_bar = np.mean(deviances)  # Mean deviance

    # Deviance at posterior mean
    theta_bar = np.mean(samples, axis=0)
    D_theta_bar = -2 * log_likelihood_fn(theta_bar)

    p_d = D_bar - D_theta_bar  # Effective number of parameters
    dic = p_d + D_bar

    return dic, p_d


def gelman_rubin_diagnostic(chains):
    """
    Compute Gelman-Rubin convergence diagnostic (R-hat)

    Parameters
    ----------
    chains : array
        MCMC chains (n_chains, n_steps, n_params)

    Returns
    -------
    R_hat : array
        R-hat value for each parameter (should be < 1.1)
    """
    n_chains, n_steps, n_params = chains.shape

    # Within-chain variance
    W = np.mean(np.var(chains, axis=1, ddof=1), axis=0)

    # Between-chain variance
    chain_means = np.mean(chains, axis=1)
    B = n_steps * np.var(chain_means, axis=0, ddof=1)

    # Pooled variance estimate
    var_plus = ((n_steps - 1) / n_steps) * W + (1 / n_steps) * B

    # R-hat statistic
    R_hat = np.sqrt(var_plus / W)

    return R_hat


def autocorrelation_time(chain):
    """
    Estimate autocorrelation time using emcee

    Parameters
    ----------
    chain : array
        MCMC chain (n_steps, n_params)

    Returns
    -------
    tau : array
        Autocorrelation time for each parameter
    """
    chain = np.atleast_2d(chain)
    n_steps, n_params = chain.shape

    try:
        # Use emcee's integrated autocorrelation time estimator
        from emcee.autocorr import integrated_time

        # Compute tau for each parameter separately to ensure array output
        tau = np.zeros(n_params)
        for i in range(n_params):
            try:
                tau_val = integrated_time(chain[:, i], quiet=True)
                # Handle both scalar and array returns
                tau[i] = float(np.atleast_1d(tau_val)[0])
            except Exception:
                # If estimation fails for a parameter, use heuristic
                tau[i] = n_steps / 10.0  # Conservative estimate

        return tau

    except Exception as e:
        warnings.warn(f"Could not compute autocorrelation time: {e}")
        return np.full(n_params, np.nan)


def effective_sample_size(chain):
    """
    Compute effective sample size

    ESS = N / tau

    Parameters
    ----------
    chain : array
        MCMC chain (n_steps, n_params)

    Returns
    -------
    ess : array
        Effective sample size for each parameter
    """
    chain = np.atleast_2d(chain)
    n_steps, n_params = chain.shape
    tau = autocorrelation_time(chain)

    # Ensure tau is an array with correct shape
    tau = np.atleast_1d(tau)
    if len(tau) != n_params:
        warnings.warn(f"tau shape mismatch: expected {n_params}, got {len(tau)}")
        tau = np.full(n_params, tau[0] if len(tau) > 0 else 1.0)

    ess = n_steps / tau
    return ess
