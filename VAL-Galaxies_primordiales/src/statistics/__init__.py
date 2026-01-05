"""Statistical analysis and model fitting"""

from .fitting import *

__all__ = ['log_likelihood', 'log_prior', 'log_posterior',
           'run_mcmc', 'compute_aic', 'compute_bic', 'compute_dic',
           'gelman_rubin_diagnostic', 'autocorrelation_time']
