# Calculs Statistiques Intensifs - Projet JANUS

## Objectif

Ce document établit les bonnes pratiques pour les calculs statistiques intensifs (MCMC, nested sampling, ajustements bayésiens) dans le cadre du projet JANUS. Il couvre la gestion de la mémoire, les checkpoints, la reprise de calculs interrompus, et les optimisations spécifiques à notre infrastructure Apple Silicon.

---

## 1. Contraintes et Risques des Calculs Longs

### 1.1 Risques Identifiés

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| **Saturation mémoire** | Crash système, perte données | Élevée pour >10⁶ points | Chunking, backends HDF5 |
| **Interruption imprévue** | Perte heures/jours de calcul | Moyenne | Checkpoints réguliers |
| **Non-convergence** | Résultats invalides | Variable | Monitoring autocorrélation |
| **Surchauffe CPU** | Throttling, ralentissement | Sur calculs >1h | Pauses, ventilation |
| **Corruption données** | Résultats inutilisables | Faible | Checksums, sauvegardes |

### 1.2 Estimation des Ressources

**Formule approximative pour MCMC** :
```
Mémoire ≈ nwalkers × nsteps × ndim × 8 bytes × facteur_overhead
```

**Exemples pour notre infrastructure (24 GB RAM)** :

| Configuration | Mémoire estimée | Faisabilité |
|---------------|-----------------|-------------|
| 32 walkers × 10,000 steps × 5 params | ~13 MB | ✅ Aucun problème |
| 64 walkers × 100,000 steps × 10 params | ~512 MB | ✅ OK |
| 128 walkers × 1,000,000 steps × 20 params | ~20 GB | ⚠️ Limite, utiliser backend |
| 256 walkers × 10,000,000 steps × 50 params | ~1 TB | ❌ Impossible sans chunking |

---

## 2. Système de Checkpoints

### 2.1 emcee avec Backend HDF5

Le backend HDF5 permet de sauvegarder la chaîne MCMC sur disque au fur et à mesure, évitant la perte de données en cas de crash.

**Configuration standard** :
```python
import emcee
import numpy as np
from pathlib import Path

def run_mcmc_with_checkpoints(
    log_prob_fn,
    initial_pos,
    nwalkers,
    ndim,
    nsteps,
    output_dir="./mcmc_outputs",
    run_name="janus_mcmc",
    checkpoint_interval=100
):
    """
    Exécute MCMC avec checkpoints automatiques.

    Parameters
    ----------
    checkpoint_interval : int
        Sauvegarde tous les N steps (défaut: 100)
    """
    # Créer répertoire de sortie
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Fichier HDF5 pour les résultats
    backend_file = output_path / f"{run_name}.h5"

    # Initialiser le backend
    backend = emcee.backends.HDFBackend(backend_file)

    # Vérifier si on reprend un calcul existant
    if backend.iteration > 0:
        print(f"Reprise depuis l'itération {backend.iteration}")
        initial_pos = None  # Reprendre depuis la dernière position
        nsteps_remaining = nsteps - backend.iteration
    else:
        backend.reset(nwalkers, ndim)
        nsteps_remaining = nsteps

    # Créer le sampler avec backend
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim, log_prob_fn,
        backend=backend
    )

    # Exécuter par blocs pour permettre le monitoring
    steps_done = 0
    while steps_done < nsteps_remaining:
        steps_this_round = min(checkpoint_interval, nsteps_remaining - steps_done)

        sampler.run_mcmc(
            initial_pos,
            steps_this_round,
            progress=True,
            skip_initial_state_check=(initial_pos is None)
        )

        initial_pos = None  # Continuer depuis la dernière position
        steps_done += steps_this_round

        # Log de progression
        print(f"Checkpoint: {backend.iteration}/{nsteps} steps "
              f"({100*backend.iteration/nsteps:.1f}%)")

        # Vérifier convergence (optionnel)
        if backend.iteration > 500:
            try:
                tau = sampler.get_autocorr_time(tol=0)
                converged = np.all(backend.iteration > 50 * tau)
                if converged:
                    print(f"Convergence atteinte à l'itération {backend.iteration}")
                    break
            except emcee.autocorr.AutocorrError:
                pass  # Pas assez de samples pour estimer tau

    return sampler, backend_file
```

### 2.2 dynesty avec Checkpoints

dynesty offre un système de checkpoint natif depuis la version 2.0.

**Configuration standard** :
```python
import dynesty
from dynesty import NestedSampler, DynamicNestedSampler
import pickle
from pathlib import Path

def run_nested_with_checkpoints(
    log_likelihood,
    prior_transform,
    ndim,
    output_dir="./nested_outputs",
    run_name="janus_nested",
    checkpoint_every=60,  # secondes
    nlive=500,
    dynamic=False
):
    """
    Exécute nested sampling avec checkpoints réguliers.

    Parameters
    ----------
    checkpoint_every : int
        Intervalle de checkpoint en secondes (défaut: 60)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    checkpoint_file = output_path / f"{run_name}.save"
    results_file = output_path / f"{run_name}_results.pkl"

    # Vérifier si on reprend un calcul
    if checkpoint_file.exists():
        print(f"Reprise depuis {checkpoint_file}")
        if dynamic:
            sampler = DynamicNestedSampler.restore(str(checkpoint_file))
        else:
            sampler = NestedSampler.restore(str(checkpoint_file))

        sampler.run_nested(
            resume=True,
            checkpoint_file=str(checkpoint_file),
            checkpoint_every=checkpoint_every
        )
    else:
        # Nouveau calcul
        if dynamic:
            sampler = DynamicNestedSampler(
                log_likelihood, prior_transform, ndim,
                nlive=nlive
            )
        else:
            sampler = NestedSampler(
                log_likelihood, prior_transform, ndim,
                nlive=nlive
            )

        sampler.run_nested(
            checkpoint_file=str(checkpoint_file),
            checkpoint_every=checkpoint_every
        )

    # Sauvegarder les résultats finaux
    results = sampler.results
    with open(results_file, 'wb') as f:
        pickle.dump(results, f)

    print(f"Résultats sauvegardés: {results_file}")
    print(f"log(Z) = {results.logz[-1]:.2f} ± {results.logzerr[-1]:.2f}")

    return sampler, results

# Utilitaire pour reprendre un calcul interrompu
def resume_nested_sampling(checkpoint_file, pool=None):
    """
    Reprend un calcul nested sampling interrompu.
    """
    checkpoint_path = Path(checkpoint_file)

    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint non trouvé: {checkpoint_file}")

    # Détecter le type de sampler
    sampler = NestedSampler.restore(str(checkpoint_path), pool=pool)

    print(f"Reprise depuis iteration {sampler.it}")
    sampler.run_nested(resume=True)

    return sampler
```

---

## 3. Gestion de la Mémoire

### 3.1 Stratégies de Réduction Mémoire

**1. Utiliser des backends disque plutôt que mémoire** :
```python
# ❌ MAUVAIS: tout en mémoire
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
sampler.run_mcmc(pos, 1000000)  # Peut saturer la RAM

# ✅ BON: backend HDF5
backend = emcee.backends.HDFBackend("chain.h5")
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob, backend=backend)
sampler.run_mcmc(pos, 1000000)  # Sauvé sur disque progressivement
```

**2. Traitement par chunks pour grandes données** :
```python
import numpy as np
from functools import lru_cache

class ChunkedDataHandler:
    """Gestionnaire de données volumineuses par chunks."""

    def __init__(self, data_file, chunk_size=10000):
        self.data_file = data_file
        self.chunk_size = chunk_size
        self._cache = {}

    def get_chunk(self, start_idx):
        """Charge un chunk de données à la demande."""
        if start_idx not in self._cache:
            # Limiter la taille du cache
            if len(self._cache) > 10:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]

            # Charger le chunk
            with h5py.File(self.data_file, 'r') as f:
                end_idx = min(start_idx + self.chunk_size, f['data'].shape[0])
                self._cache[start_idx] = f['data'][start_idx:end_idx]

        return self._cache[start_idx]
```

**3. Garbage collection explicite** :
```python
import gc

def memory_efficient_mcmc(sampler, nsteps, checkpoint_every=1000):
    """MCMC avec nettoyage mémoire périodique."""
    for i in range(0, nsteps, checkpoint_every):
        steps = min(checkpoint_every, nsteps - i)
        sampler.run_mcmc(None, steps, progress=True)

        # Forcer le garbage collection
        gc.collect()

        # Log utilisation mémoire
        import psutil
        process = psutil.Process()
        mem_gb = process.memory_info().rss / 1e9
        print(f"Mémoire utilisée: {mem_gb:.2f} GB")
```

### 3.2 Monitoring de la Mémoire

```python
import psutil
import time
from threading import Thread
import matplotlib.pyplot as plt

class MemoryMonitor:
    """Monitore l'utilisation mémoire pendant les calculs."""

    def __init__(self, interval=5):
        self.interval = interval
        self.running = False
        self.memory_log = []
        self.time_log = []
        self._thread = None

    def _monitor(self):
        start_time = time.time()
        while self.running:
            process = psutil.Process()
            mem_gb = process.memory_info().rss / 1e9
            self.memory_log.append(mem_gb)
            self.time_log.append(time.time() - start_time)
            time.sleep(self.interval)

    def start(self):
        self.running = True
        self.memory_log = []
        self.time_log = []
        self._thread = Thread(target=self._monitor)
        self._thread.start()

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()

    def plot(self, save_path=None):
        """Génère un graphique de l'utilisation mémoire."""
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(self.time_log, self.memory_log, 'b-', linewidth=1)
        ax.fill_between(self.time_log, self.memory_log, alpha=0.3)
        ax.set_xlabel('Temps (s)')
        ax.set_ylabel('Mémoire (GB)')
        ax.set_title('Utilisation mémoire pendant le calcul')
        ax.axhline(y=24, color='r', linestyle='--', label='Limite (24 GB)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches='tight')

        return fig

    def get_peak(self):
        """Retourne le pic de mémoire utilisée."""
        return max(self.memory_log) if self.memory_log else 0

# Utilisation
monitor = MemoryMonitor(interval=10)
monitor.start()

# ... calculs MCMC ...

monitor.stop()
print(f"Pic mémoire: {monitor.get_peak():.2f} GB")
monitor.plot("memory_usage.png")
```

---

## 4. Optimisations pour Apple Silicon (M4)

### 4.1 Configuration Optimale pour M4

Notre iMac M4 dispose de 10 cœurs (4 performance + 6 efficiency). Voici les configurations optimales :

```python
import multiprocessing as mp
import os

# Nombre optimal de workers pour M4
N_PERFORMANCE_CORES = 4
N_EFFICIENCY_CORES = 6
N_TOTAL_CORES = N_PERFORMANCE_CORES + N_EFFICIENCY_CORES

def get_optimal_workers(task_type="heavy"):
    """
    Retourne le nombre optimal de workers selon le type de tâche.

    Parameters
    ----------
    task_type : str
        "heavy" : calculs intensifs (utiliser cœurs performance)
        "light" : tâches légères (utiliser tous les cœurs)
        "balanced" : mix optimal
    """
    if task_type == "heavy":
        # Calculs intensifs: utiliser principalement les cœurs performance
        return N_PERFORMANCE_CORES
    elif task_type == "light":
        # Tâches légères: utiliser tous les cœurs
        return N_TOTAL_CORES
    else:  # balanced
        # Mix: cœurs performance + quelques efficiency
        return N_PERFORMANCE_CORES + 2

# Configuration recommandée pour emcee sur M4
OPTIMAL_NWALKERS = 32  # Multiple du nombre de cœurs performance
```

### 4.2 Parallélisation avec Pool

```python
import emcee
import multiprocessing as mp

def run_parallel_mcmc(log_prob, pos, nwalkers, ndim, nsteps, backend=None):
    """
    MCMC parallélisé optimisé pour Apple Silicon.
    """
    # Nombre de workers optimal pour M4
    n_workers = get_optimal_workers("heavy")

    # Note: Sur macOS, utiliser 'spawn' pour éviter les problèmes de fork
    ctx = mp.get_context('spawn')

    with ctx.Pool(n_workers) as pool:
        sampler = emcee.EnsembleSampler(
            nwalkers, ndim, log_prob,
            pool=pool,
            backend=backend
        )
        sampler.run_mcmc(pos, nsteps, progress=True)

    return sampler
```

### 4.3 Accélération avec Numba

Numba fonctionne très bien sur Apple Silicon. Voici comment optimiser les fonctions critiques :

```python
from numba import jit, prange
import numpy as np

@jit(nopython=True, cache=True, fastmath=True)
def fast_chi2(observed, model, errors):
    """
    Calcul chi² optimisé avec Numba.
    ~10-100x plus rapide que NumPy pur.
    """
    chi2 = 0.0
    for i in range(len(observed)):
        residual = (observed[i] - model[i]) / errors[i]
        chi2 += residual * residual
    return chi2

@jit(nopython=True, cache=True, parallel=True)
def fast_log_likelihood_batch(theta_batch, data, errors):
    """
    Log-likelihood parallélisée pour plusieurs paramètres.
    Utilise tous les cœurs disponibles.
    """
    n_samples = theta_batch.shape[0]
    results = np.empty(n_samples)

    for i in prange(n_samples):
        theta = theta_batch[i]
        model = compute_model(theta)  # Doit aussi être @jit
        results[i] = -0.5 * fast_chi2(data, model, errors)

    return results

@jit(nopython=True, cache=True)
def compute_model(theta):
    """
    Exemple de modèle cosmologique simple optimisé.
    À adapter selon votre modèle JANUS.
    """
    H0, Om0 = theta[0], theta[1]
    # ... calculs du modèle ...
    return model_values
```

### 4.4 Optimisations Vectorielles (SIMD)

Apple M4 supporte NEON SIMD. NumPy et SciPy en bénéficient automatiquement via Accelerate :

```python
import numpy as np

# Vérifier que NumPy utilise Accelerate
np.show_config()  # Doit montrer "accelerate" ou "vecLib"

# Opérations vectorielles optimisées automatiquement
def vectorized_distance_modulus(z, H0, Om0, Ode0):
    """
    Calcul vectorisé du module de distance.
    Exploite automatiquement SIMD sur M4.
    """
    from scipy.integrate import cumulative_trapezoid

    # Intégration vectorisée
    z_array = np.atleast_1d(z)
    z_grid = np.linspace(0, z_array.max(), 1000)

    E_z = np.sqrt(Om0 * (1 + z_grid)**3 + Ode0)

    # Calcul vectorisé
    integral = cumulative_trapezoid(1/E_z, z_grid, initial=0)

    # Interpolation pour les z demandés
    d_L = np.interp(z_array, z_grid, integral) * (1 + z_array)

    c = 299792.458  # km/s
    mu = 5 * np.log10(c / H0 * d_L) + 25

    return mu
```

---

## 5. Reprise de Calculs Interrompus

### 5.1 Architecture Robuste

```python
import json
from pathlib import Path
from datetime import datetime
import hashlib

class RobustMCMCRunner:
    """
    Gestionnaire de calculs MCMC robuste avec reprise automatique.
    """

    def __init__(self, output_dir, run_name):
        self.output_dir = Path(output_dir)
        self.run_name = run_name
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Fichiers de gestion
        self.chain_file = self.output_dir / f"{run_name}.h5"
        self.metadata_file = self.output_dir / f"{run_name}_metadata.json"
        self.log_file = self.output_dir / f"{run_name}.log"

    def _save_metadata(self, config, status="running"):
        """Sauvegarde les métadonnées du run."""
        metadata = {
            "run_name": self.run_name,
            "status": status,
            "config": config,
            "last_update": datetime.now().isoformat(),
            "config_hash": hashlib.md5(
                json.dumps(config, sort_keys=True).encode()
            ).hexdigest()
        }
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _load_metadata(self):
        """Charge les métadonnées existantes."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return None

    def _log(self, message):
        """Ajoute un message au log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")

    def run(self, log_prob_fn, nwalkers, ndim, nsteps, initial_pos=None,
            checkpoint_interval=500):
        """
        Exécute ou reprend un calcul MCMC.
        """
        import emcee

        config = {
            "nwalkers": nwalkers,
            "ndim": ndim,
            "nsteps": nsteps,
            "checkpoint_interval": checkpoint_interval
        }

        # Vérifier si on reprend un calcul
        backend = emcee.backends.HDFBackend(self.chain_file)
        existing_metadata = self._load_metadata()

        if backend.iteration > 0 and existing_metadata:
            # Vérifier la cohérence de configuration
            if existing_metadata.get("config_hash") != hashlib.md5(
                json.dumps(config, sort_keys=True).encode()
            ).hexdigest():
                raise ValueError(
                    "Configuration différente du run existant. "
                    "Utilisez un nouveau run_name ou supprimez les fichiers."
                )

            self._log(f"Reprise depuis l'itération {backend.iteration}")
            initial_pos = None
            nsteps_remaining = nsteps - backend.iteration
        else:
            backend.reset(nwalkers, ndim)
            nsteps_remaining = nsteps

            if initial_pos is None:
                raise ValueError("initial_pos requis pour un nouveau run")

            self._log(f"Nouveau run: {nsteps} steps avec {nwalkers} walkers")

        self._save_metadata(config, status="running")

        # Créer le sampler
        sampler = emcee.EnsembleSampler(
            nwalkers, ndim, log_prob_fn,
            backend=backend
        )

        # Exécuter par blocs
        try:
            steps_done = 0
            while steps_done < nsteps_remaining:
                steps_this_round = min(checkpoint_interval,
                                       nsteps_remaining - steps_done)

                sampler.run_mcmc(
                    initial_pos,
                    steps_this_round,
                    progress=True,
                    skip_initial_state_check=(initial_pos is None)
                )

                initial_pos = None
                steps_done += steps_this_round

                # Log progression
                progress = 100 * backend.iteration / nsteps
                self._log(f"Progression: {backend.iteration}/{nsteps} "
                         f"({progress:.1f}%)")

                # Vérifier convergence
                if backend.iteration >= 1000:
                    try:
                        tau = sampler.get_autocorr_time(tol=0)
                        self._log(f"Temps d'autocorrélation: {tau.mean():.1f}")

                        if np.all(backend.iteration > 50 * tau):
                            self._log("CONVERGENCE ATTEINTE")
                            break
                    except:
                        pass

            self._save_metadata(config, status="completed")
            self._log("Run terminé avec succès")

        except KeyboardInterrupt:
            self._save_metadata(config, status="interrupted")
            self._log("Run interrompu par l'utilisateur")
            raise

        except Exception as e:
            self._save_metadata(config, status="error")
            self._log(f"Erreur: {str(e)}")
            raise

        return sampler

    def get_results(self, discard=None, thin=None):
        """
        Récupère les résultats du run.

        Parameters
        ----------
        discard : int
            Nombre de steps à écarter (burn-in)
        thin : int
            Facteur de thin (prendre 1 sample sur N)
        """
        import emcee

        backend = emcee.backends.HDFBackend(self.chain_file)

        if discard is None:
            # Estimer le burn-in automatiquement
            try:
                tau = backend.get_autocorr_time()
                discard = int(2 * tau.max())
            except:
                discard = backend.iteration // 5

        if thin is None:
            try:
                tau = backend.get_autocorr_time()
                thin = max(1, int(tau.max() / 2))
            except:
                thin = 1

        samples = backend.get_chain(discard=discard, thin=thin, flat=True)
        log_prob = backend.get_log_prob(discard=discard, thin=thin, flat=True)

        return {
            "samples": samples,
            "log_prob": log_prob,
            "discard": discard,
            "thin": thin,
            "n_samples": len(samples)
        }
```

### 5.2 Script de Reprise Automatique

```python
#!/usr/bin/env python3
"""
Script de reprise automatique des calculs MCMC interrompus.
Utilisation: python resume_mcmc.py <output_dir>
"""

import sys
from pathlib import Path
import json

def find_interrupted_runs(output_dir):
    """Trouve tous les runs interrompus."""
    output_path = Path(output_dir)
    interrupted = []

    for metadata_file in output_path.glob("*_metadata.json"):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        if metadata.get("status") in ["running", "interrupted"]:
            interrupted.append({
                "run_name": metadata["run_name"],
                "status": metadata["status"],
                "last_update": metadata["last_update"],
                "metadata_file": metadata_file
            })

    return interrupted

def resume_run(metadata_file, log_prob_fn):
    """Reprend un run interrompu."""
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    output_dir = metadata_file.parent
    run_name = metadata["run_name"]
    config = metadata["config"]

    runner = RobustMCMCRunner(output_dir, run_name)
    sampler = runner.run(
        log_prob_fn,
        config["nwalkers"],
        config["ndim"],
        config["nsteps"],
        checkpoint_interval=config["checkpoint_interval"]
    )

    return sampler

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resume_mcmc.py <output_dir>")
        sys.exit(1)

    interrupted = find_interrupted_runs(sys.argv[1])

    if not interrupted:
        print("Aucun run interrompu trouvé.")
    else:
        print(f"Runs interrompus trouvés: {len(interrupted)}")
        for run in interrupted:
            print(f"  - {run['run_name']}: {run['status']} "
                  f"(dernière MAJ: {run['last_update']})")
```

---

## 6. Monitoring de Convergence

### 6.1 Critères de Convergence

```python
import numpy as np
import emcee

def check_convergence(sampler, verbose=True):
    """
    Vérifie la convergence d'une chaîne MCMC.

    Returns
    -------
    dict
        Dictionnaire avec les métriques de convergence
    """
    results = {
        "converged": False,
        "n_iterations": sampler.iteration,
        "checks": {}
    }

    # 1. Temps d'autocorrélation
    try:
        tau = sampler.get_autocorr_time(tol=0)
        tau_mean = tau.mean()
        tau_max = tau.max()

        # Critère: N > 50 * tau
        tau_check = sampler.iteration > 50 * tau_max

        results["checks"]["autocorr"] = {
            "tau_mean": tau_mean,
            "tau_max": tau_max,
            "n_effective": sampler.iteration / tau_mean,
            "passed": bool(tau_check)
        }

        if verbose:
            print(f"Autocorrélation: τ_mean={tau_mean:.1f}, τ_max={tau_max:.1f}")
            print(f"  N_eff = {sampler.iteration / tau_mean:.0f} "
                  f"(objectif > 50×τ = {50*tau_max:.0f})")
            print(f"  Status: {'✅' if tau_check else '❌'}")

    except emcee.autocorr.AutocorrError:
        results["checks"]["autocorr"] = {"passed": False, "error": "Pas assez de samples"}
        if verbose:
            print("Autocorrélation: ❌ Pas assez de samples")

    # 2. Acceptation rate
    acceptance = sampler.acceptance_fraction.mean()
    acceptance_check = 0.2 < acceptance < 0.5

    results["checks"]["acceptance"] = {
        "rate": acceptance,
        "passed": acceptance_check
    }

    if verbose:
        print(f"Taux d'acceptation: {acceptance:.3f} "
              f"(objectif: 0.2-0.5) {'✅' if acceptance_check else '⚠️'}")

    # 3. Gelman-Rubin (R-hat) si plusieurs walkers
    try:
        chain = sampler.get_chain()  # (nsteps, nwalkers, ndim)

        # Calculer R-hat pour chaque paramètre
        rhat = calculate_rhat(chain)
        rhat_check = np.all(rhat < 1.1)

        results["checks"]["rhat"] = {
            "values": rhat.tolist(),
            "max": rhat.max(),
            "passed": rhat_check
        }

        if verbose:
            print(f"R-hat max: {rhat.max():.3f} (objectif < 1.1) "
                  f"{'✅' if rhat_check else '❌'}")

    except Exception as e:
        results["checks"]["rhat"] = {"passed": False, "error": str(e)}

    # Convergence globale
    all_passed = all(
        check.get("passed", False)
        for check in results["checks"].values()
    )
    results["converged"] = all_passed

    if verbose:
        print(f"\nConvergence globale: {'✅ OUI' if all_passed else '❌ NON'}")

    return results

def calculate_rhat(chain):
    """
    Calcule le R-hat (Gelman-Rubin) pour chaque paramètre.

    Parameters
    ----------
    chain : array (nsteps, nwalkers, ndim)
    """
    nsteps, nwalkers, ndim = chain.shape

    # Diviser chaque walker en 2 chaînes
    half = nsteps // 2
    split_chain = np.concatenate([
        chain[:half],
        chain[half:2*half]
    ], axis=1)  # (half_steps, 2*nwalkers, ndim)

    m = split_chain.shape[1]  # nombre de chaînes
    n = split_chain.shape[0]  # longueur des chaînes

    # Moyennes par chaîne
    chain_means = split_chain.mean(axis=0)  # (m, ndim)

    # Moyenne globale
    global_mean = chain_means.mean(axis=0)  # (ndim,)

    # Variance inter-chaînes (B)
    B = n / (m - 1) * np.sum((chain_means - global_mean)**2, axis=0)

    # Variance intra-chaînes (W)
    chain_vars = split_chain.var(axis=0, ddof=1)  # (m, ndim)
    W = chain_vars.mean(axis=0)

    # Estimation de la variance
    var_est = (n - 1) / n * W + B / n

    # R-hat
    rhat = np.sqrt(var_est / W)

    return rhat
```

### 6.2 Visualisation en Temps Réel

```python
import matplotlib.pyplot as plt
from IPython.display import clear_output
import time

def live_monitoring(sampler, update_interval=100, max_time=None):
    """
    Monitoring en temps réel pour Jupyter notebooks.
    """
    start_time = time.time()
    last_iteration = 0

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    while True:
        current_iteration = sampler.iteration

        if current_iteration > last_iteration:
            clear_output(wait=True)

            chain = sampler.get_chain()
            log_prob = sampler.get_log_prob()

            # Plot 1: Trace des paramètres
            axes[0, 0].clear()
            for i in range(min(3, chain.shape[2])):
                axes[0, 0].plot(chain[:, :, i], alpha=0.3)
            axes[0, 0].set_xlabel('Iteration')
            axes[0, 0].set_ylabel('Valeur paramètre')
            axes[0, 0].set_title('Trace des paramètres')

            # Plot 2: Log-probabilité
            axes[0, 1].clear()
            axes[0, 1].plot(log_prob, alpha=0.3)
            axes[0, 1].set_xlabel('Iteration')
            axes[0, 1].set_ylabel('Log-probabilité')
            axes[0, 1].set_title('Log-probabilité')

            # Plot 3: Autocorrélation
            axes[1, 0].clear()
            try:
                tau = sampler.get_autocorr_time(tol=0)
                axes[1, 0].bar(range(len(tau)), tau)
                axes[1, 0].axhline(current_iteration/50, color='r',
                                  linestyle='--', label='Seuil convergence')
                axes[1, 0].set_xlabel('Paramètre')
                axes[1, 0].set_ylabel('τ')
                axes[1, 0].set_title(f'Autocorrélation (τ_max={tau.max():.1f})')
                axes[1, 0].legend()
            except:
                axes[1, 0].text(0.5, 0.5, 'Pas assez de samples',
                               ha='center', va='center')

            # Plot 4: Statistiques
            axes[1, 1].clear()
            axes[1, 1].axis('off')
            stats_text = f"""
            Iteration: {current_iteration}
            Temps écoulé: {time.time() - start_time:.0f}s
            Taux acceptation: {sampler.acceptance_fraction.mean():.3f}
            """
            axes[1, 1].text(0.1, 0.5, stats_text, fontsize=12,
                           family='monospace', va='center')

            plt.tight_layout()
            plt.show()

            last_iteration = current_iteration

        # Vérifier limite de temps
        if max_time and (time.time() - start_time) > max_time:
            break

        time.sleep(1)
```

---

## 7. Bonnes Pratiques Générales

### 7.1 Checklist Avant un Long Calcul

```markdown
## Checklist Pré-Calcul MCMC/Nested Sampling

### Préparation
- [ ] Données validées et nettoyées
- [ ] Modèle testé sur un sous-ensemble
- [ ] Prior bien défini et justifié
- [ ] Log-likelihood testée (pas de NaN/Inf)

### Configuration
- [ ] nwalkers ≥ 2 × ndim (recommandé: 4 × ndim)
- [ ] nsteps estimé selon temps disponible
- [ ] Backend HDF5 configuré
- [ ] Checkpoint interval défini (recommandé: 100-500)

### Infrastructure
- [ ] Espace disque suffisant (estimer: nwalkers × nsteps × ndim × 8 bytes)
- [ ] Mémoire RAM suffisante (vérifier estimation section 1.2)
- [ ] Machine branchée sur secteur
- [ ] Ventilation correcte

### Sécurité
- [ ] Répertoire de sortie créé
- [ ] Droits d'écriture vérifiés
- [ ] Aucun autre calcul intensif en parallèle
- [ ] Notifications activées (email/Slack) si disponibles

### Post-Run
- [ ] Vérifier convergence (τ, R-hat, acceptance)
- [ ] Sauvegarder les résultats finaux
- [ ] Documenter les paramètres utilisés
```

### 7.2 Structure de Répertoire Recommandée

```
JANUS-ANALYSES/
├── data/
│   ├── raw/                    # Données brutes
│   └── processed/              # Données prétraitées
├── models/
│   ├── janus_model.py          # Modèle JANUS
│   └── lcdm_model.py           # Modèle ΛCDM
├── mcmc_runs/
│   ├── run_20260105_janus/
│   │   ├── chain.h5            # Chaîne MCMC
│   │   ├── metadata.json       # Métadonnées
│   │   ├── run.log             # Logs
│   │   └── results/            # Résultats analysés
│   └── run_20260105_lcdm/
├── notebooks/
│   ├── 01_data_prep.ipynb
│   ├── 02_mcmc_janus.ipynb
│   └── 03_analysis.ipynb
└── scripts/
    ├── run_mcmc.py
    └── analyze_results.py
```

### 7.3 Estimation du Temps de Calcul

```python
import time
import numpy as np

def estimate_runtime(log_prob_fn, pos_sample, nwalkers, nsteps, n_test=100):
    """
    Estime le temps total de calcul.

    Parameters
    ----------
    log_prob_fn : callable
        Fonction de log-probabilité
    pos_sample : array
        Position d'exemple (ndim,)
    nwalkers : int
        Nombre de walkers
    nsteps : int
        Nombre de steps prévus
    n_test : int
        Nombre d'évaluations pour le test

    Returns
    -------
    dict
        Estimations de temps
    """
    # Mesurer le temps d'une évaluation
    times = []
    for _ in range(n_test):
        t0 = time.perf_counter()
        log_prob_fn(pos_sample)
        times.append(time.perf_counter() - t0)

    t_eval = np.median(times)

    # Estimation totale
    # Chaque step = nwalkers évaluations (en série sans parallélisation)
    total_evals = nwalkers * nsteps
    t_total_serial = total_evals * t_eval

    # Avec parallélisation (4 cœurs performance sur M4)
    n_cores = 4
    t_total_parallel = t_total_serial / n_cores

    # Overhead emcee (~20%)
    overhead_factor = 1.2

    results = {
        "t_eval_ms": t_eval * 1000,
        "total_evaluations": total_evals,
        "estimated_serial_hours": t_total_serial * overhead_factor / 3600,
        "estimated_parallel_hours": t_total_parallel * overhead_factor / 3600,
        "n_cores_parallel": n_cores
    }

    print(f"Temps par évaluation: {results['t_eval_ms']:.2f} ms")
    print(f"Évaluations totales: {results['total_evaluations']:,}")
    print(f"Temps estimé (série): {results['estimated_serial_hours']:.1f} heures")
    print(f"Temps estimé ({n_cores} cœurs): {results['estimated_parallel_hours']:.1f} heures")

    return results
```

### 7.4 Template de Configuration

```python
"""
Configuration standard pour calculs MCMC - Projet JANUS
"""

# =============================================================================
# CONFIGURATION GÉNÉRALE
# =============================================================================

RUN_CONFIG = {
    "run_name": "janus_galaxies_highz_v1",
    "description": "Ajustement MCMC du modèle JANUS sur galaxies z>10",
    "date": "2026-01-05",
    "author": "PGPLF"
}

# =============================================================================
# PARAMÈTRES MCMC
# =============================================================================

MCMC_CONFIG = {
    # Sampler
    "nwalkers": 32,           # Recommandé: 2-4 × ndim
    "nsteps": 50000,          # Ajuster selon convergence
    "ndim": 5,                # Nombre de paramètres

    # Checkpoints
    "checkpoint_interval": 500,
    "output_dir": "./mcmc_outputs",

    # Convergence
    "min_autocorr_times": 50,  # N > min_autocorr_times × τ
    "target_acceptance": (0.2, 0.5),  # Fourchette acceptable

    # Parallélisation
    "n_workers": 4,           # Cœurs performance sur M4
    "use_pool": True
}

# =============================================================================
# PARAMÈTRES DU MODÈLE
# =============================================================================

MODEL_PARAMS = {
    "names": ["H0", "Om0", "Om0_bar", "chi", "sigma_int"],
    "labels": [r"$H_0$", r"$\Omega_{m,0}$", r"$\bar{\Omega}_{m,0}$",
               r"$\chi$", r"$\sigma_{int}$"],
    "units": ["km/s/Mpc", "", "", "", "mag"],

    # Priors (uniform)
    "prior_bounds": {
        "H0": (60, 80),
        "Om0": (0.1, 0.5),
        "Om0_bar": (0.1, 0.9),
        "chi": (0, 2),
        "sigma_int": (0.01, 0.5)
    }
}

# =============================================================================
# RESSOURCES
# =============================================================================

RESOURCE_LIMITS = {
    "max_memory_gb": 20,      # Limite à 20 GB sur 24 disponibles
    "max_runtime_hours": 48,  # Limite de temps
    "disk_space_gb": 10       # Espace disque requis
}
```

---

## 8. Dépannage

### 8.1 Problèmes Courants

| Problème | Cause Probable | Solution |
|----------|---------------|----------|
| `MemoryError` | Chaîne trop grande en RAM | Utiliser backend HDF5 |
| Convergence lente | Priors trop larges / mal choisis | Affiner priors, utiliser MAP comme départ |
| `NaN` dans log_prob | Paramètres hors domaine | Ajouter vérifications dans prior |
| Acceptance rate < 0.1 | Problème d'échelle | Rescaler paramètres |
| Acceptance rate > 0.5 | Exploration insuffisante | Augmenter nwalkers |
| Calcul très lent | Likelihood non optimisée | Utiliser Numba, vectoriser |

### 8.2 Récupération d'Urgence

```python
def emergency_save(sampler, output_path):
    """
    Sauvegarde d'urgence en cas de problème.
    À appeler dans un bloc try/except.
    """
    import pickle
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    emergency_file = f"{output_path}/emergency_save_{timestamp}.pkl"

    try:
        # Tenter de récupérer ce qui est possible
        data = {
            "chain": sampler.get_chain() if hasattr(sampler, 'get_chain') else None,
            "log_prob": sampler.get_log_prob() if hasattr(sampler, 'get_log_prob') else None,
            "iteration": getattr(sampler, 'iteration', None),
            "acceptance_fraction": getattr(sampler, 'acceptance_fraction', None)
        }

        with open(emergency_file, 'wb') as f:
            pickle.dump(data, f)

        print(f"Sauvegarde d'urgence: {emergency_file}")
        return emergency_file

    except Exception as e:
        print(f"Échec sauvegarde d'urgence: {e}")
        return None

# Utilisation
try:
    sampler.run_mcmc(pos, nsteps)
except Exception as e:
    emergency_save(sampler, "./mcmc_outputs")
    raise
```

---

## 9. Références

### Documentation Officielle
- [emcee - Saving & Monitoring Progress](https://emcee.readthedocs.io/en/stable/tutorials/monitor/)
- [dynesty - Checkpointing](https://dynesty.readthedocs.io/en/latest/quickstart.html)
- [PyMC Documentation](https://www.pymc.io/)

### Articles et Tutoriels
- [MCMC for big datasets with JAX](https://martiningram.github.io/mcmc-comparison/)
- [Computational Statistics in Python - MCMC](https://people.duke.edu/~ccc14/sta-663/MCMC.html)

### Packages Complémentaires
- [arviz](https://python.arviz.org/) - Diagnostics et visualisation
- [corner](https://corner.readthedocs.io/) - Corner plots
- [ChainConsumer](https://samreay.github.io/ChainConsumer/) - Analyse de chaînes

---

## Historique des Modifications

| Date | Auteur | Modification |
|------|--------|--------------|
| 2026-01-05 | Claude/PGPLF | Création initiale |
