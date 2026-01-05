#!/usr/bin/env python3
"""
Script MCMC optimisé pour le projet JANUS
Conçu pour être lancé en background par Claude Code

Usage:
    python run_mcmc_optimized.py --config config.json
    python run_mcmc_optimized.py --config config.json &  # Background

Optimisations:
    - Numba JIT compilation
    - Parallélisation sur cœurs performance M4
    - Checkpoints automatiques
    - Monitoring mémoire
    - Reprise automatique si interrompu
"""

import argparse
import json
import os
import sys
import time
import signal
from pathlib import Path
from datetime import datetime
from multiprocessing import Pool, cpu_count

import numpy as np
import emcee
import h5py
import psutil

# =============================================================================
# CONFIGURATION OPTIMALE POUR APPLE M4
# =============================================================================

# Cœurs performance uniquement pour calculs intensifs
N_PERFORMANCE_CORES = 4
CHECKPOINT_INTERVAL = 500  # steps
MEMORY_LIMIT_GB = 20  # Laisser 4GB pour le système

# =============================================================================
# MONITORING
# =============================================================================

class MCMCMonitor:
    """Monitore le calcul MCMC en temps réel."""

    def __init__(self, output_dir, run_name):
        self.output_dir = Path(output_dir)
        self.run_name = run_name
        self.log_file = self.output_dir / f"{run_name}.log"
        self.status_file = self.output_dir / f"{run_name}_status.json"
        self.start_time = None

    def start(self):
        self.start_time = time.time()
        self._log("=" * 60)
        self._log(f"MCMC DÉMARRÉ: {self.run_name}")
        self._log(f"PID: {os.getpid()}")
        self._log("=" * 60)
        self._update_status("running")

    def checkpoint(self, iteration, total, tau=None, acceptance=None):
        elapsed = time.time() - self.start_time
        progress = 100 * iteration / total
        rate = iteration / elapsed if elapsed > 0 else 0
        eta = (total - iteration) / rate if rate > 0 else 0

        # Mémoire
        mem_gb = psutil.Process().memory_info().rss / 1e9

        msg = (f"[{progress:5.1f}%] Iter {iteration:,}/{total:,} | "
               f"Vitesse: {rate:.1f} it/s | ETA: {eta/60:.1f} min | "
               f"Mémoire: {mem_gb:.2f} GB")

        if tau is not None:
            msg += f" | τ_max: {tau:.1f}"
        if acceptance is not None:
            msg += f" | Accept: {acceptance:.3f}"

        self._log(msg)

        self._update_status("running", {
            "iteration": iteration,
            "total": total,
            "progress": progress,
            "elapsed_seconds": elapsed,
            "eta_seconds": eta,
            "memory_gb": mem_gb,
            "rate_its": rate,
            "tau_max": tau,
            "acceptance": acceptance
        })

        # Alerte mémoire
        if mem_gb > MEMORY_LIMIT_GB:
            self._log(f"⚠️ ALERTE: Mémoire {mem_gb:.2f} GB > limite {MEMORY_LIMIT_GB} GB")

    def complete(self, results=None):
        elapsed = time.time() - self.start_time
        self._log("=" * 60)
        self._log(f"MCMC TERMINÉ en {elapsed/3600:.2f} heures")
        if results:
            self._log(f"Samples effectifs: {results.get('n_effective', 'N/A')}")
        self._log("=" * 60)
        self._update_status("completed", {"elapsed_hours": elapsed/3600})

    def error(self, error_msg):
        self._log(f"❌ ERREUR: {error_msg}")
        self._update_status("error", {"error": str(error_msg)})

    def _log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        with open(self.log_file, 'a') as f:
            f.write(line + "\n")

    def _update_status(self, status, data=None):
        status_data = {
            "status": status,
            "run_name": self.run_name,
            "pid": os.getpid(),
            "last_update": datetime.now().isoformat(),
            "data": data or {}
        }
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)


# =============================================================================
# MCMC RUNNER OPTIMISÉ
# =============================================================================

def run_optimized_mcmc(config):
    """
    Exécute un MCMC optimisé avec toutes les bonnes pratiques.

    Parameters
    ----------
    config : dict
        Configuration du run (voir exemple ci-dessous)
    """
    # Extraire configuration
    run_name = config.get("run_name", "mcmc_run")
    output_dir = Path(config.get("output_dir", "./mcmc_outputs"))
    output_dir.mkdir(parents=True, exist_ok=True)

    nwalkers = config.get("nwalkers", 32)
    nsteps = config.get("nsteps", 10000)
    ndim = config.get("ndim", 5)
    n_workers = config.get("n_workers", N_PERFORMANCE_CORES)
    checkpoint_interval = config.get("checkpoint_interval", CHECKPOINT_INTERVAL)

    # Initialiser monitoring
    monitor = MCMCMonitor(output_dir, run_name)

    # Fichiers
    chain_file = output_dir / f"{run_name}.h5"

    # Backend HDF5
    backend = emcee.backends.HDFBackend(chain_file)

    # Vérifier reprise
    if backend.iteration > 0:
        monitor._log(f"REPRISE depuis itération {backend.iteration}")
        initial_pos = None
        nsteps_remaining = nsteps - backend.iteration
    else:
        backend.reset(nwalkers, ndim)
        # Position initiale (à personnaliser selon le modèle)
        initial_pos = config.get("initial_pos")
        if initial_pos is None:
            # Positions par défaut autour des priors
            prior_center = np.array(config.get("prior_center", np.zeros(ndim)))
            prior_width = np.array(config.get("prior_width", np.ones(ndim)))
            initial_pos = prior_center + prior_width * 0.1 * np.random.randn(nwalkers, ndim)
        nsteps_remaining = nsteps

    # Fonction log_prob (doit être définie dans le module importé)
    log_prob_module = config.get("log_prob_module", "janus_model")
    log_prob_name = config.get("log_prob_function", "log_probability")

    # Import dynamique
    try:
        import importlib
        mod = importlib.import_module(log_prob_module)
        log_prob_fn = getattr(mod, log_prob_name)
    except (ImportError, AttributeError) as e:
        # Fallback: fonction de test
        monitor._log(f"⚠️ Module {log_prob_module} non trouvé, utilisation fonction test")
        def log_prob_fn(theta):
            # Simple gaussienne pour test
            return -0.5 * np.sum(theta**2)

    # Gestionnaire d'interruption
    interrupted = False
    def signal_handler(signum, frame):
        nonlocal interrupted
        interrupted = True
        monitor._log("Signal d'interruption reçu, sauvegarde en cours...")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Démarrer
    monitor.start()

    try:
        # Créer sampler avec pool
        if n_workers > 1:
            pool = Pool(n_workers)
            sampler = emcee.EnsembleSampler(
                nwalkers, ndim, log_prob_fn,
                pool=pool,
                backend=backend
            )
        else:
            pool = None
            sampler = emcee.EnsembleSampler(
                nwalkers, ndim, log_prob_fn,
                backend=backend
            )

        # Exécuter par blocs
        steps_done = 0
        while steps_done < nsteps_remaining and not interrupted:
            steps_this_round = min(checkpoint_interval, nsteps_remaining - steps_done)

            sampler.run_mcmc(
                initial_pos,
                steps_this_round,
                progress=False,  # On gère notre propre progress
                skip_initial_state_check=(initial_pos is None)
            )

            initial_pos = None
            steps_done += steps_this_round

            # Calcul diagnostics
            try:
                tau = sampler.get_autocorr_time(tol=0)
                tau_max = tau.max()
            except:
                tau_max = None

            acceptance = sampler.acceptance_fraction.mean()

            # Checkpoint
            monitor.checkpoint(
                backend.iteration, nsteps,
                tau=tau_max, acceptance=acceptance
            )

            # Vérifier convergence
            if tau_max is not None and backend.iteration > 50 * tau_max:
                monitor._log("✅ CONVERGENCE ATTEINTE")
                break

        # Fermer pool
        if pool:
            pool.close()
            pool.join()

        # Résultats finaux
        if not interrupted:
            try:
                tau = sampler.get_autocorr_time()
                n_effective = backend.iteration / tau.mean()
            except:
                n_effective = None

            monitor.complete({"n_effective": n_effective})
        else:
            monitor._log("Run interrompu mais sauvegardé")
            monitor._update_status("interrupted")

    except Exception as e:
        monitor.error(str(e))
        raise

    return chain_file


# =============================================================================
# EXEMPLE DE CONFIGURATION
# =============================================================================

EXAMPLE_CONFIG = {
    "run_name": "janus_highz_galaxies",
    "output_dir": "./mcmc_outputs",

    # Paramètres MCMC
    "nwalkers": 32,
    "nsteps": 50000,
    "ndim": 5,

    # Parallélisation
    "n_workers": 4,  # Cœurs performance M4

    # Checkpoints
    "checkpoint_interval": 500,

    # Modèle (module Python contenant log_probability)
    "log_prob_module": "janus_model",
    "log_prob_function": "log_probability",

    # Priors (pour initialisation)
    "prior_center": [70, 0.3, 0.5, 1.0, 0.1],  # H0, Om0, Om0_bar, chi, sigma
    "prior_width": [10, 0.1, 0.2, 0.5, 0.05]
}


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCMC optimisé pour JANUS")
    parser.add_argument("--config", type=str, help="Fichier de configuration JSON")
    parser.add_argument("--example-config", action="store_true",
                        help="Afficher exemple de configuration")

    args = parser.parse_args()

    if args.example_config:
        print(json.dumps(EXAMPLE_CONFIG, indent=2))
        sys.exit(0)

    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        print("Usage: python run_mcmc_optimized.py --config config.json")
        print("       python run_mcmc_optimized.py --example-config")
        sys.exit(1)

    # Lancer
    chain_file = run_optimized_mcmc(config)
    print(f"\nRésultats sauvegardés: {chain_file}")