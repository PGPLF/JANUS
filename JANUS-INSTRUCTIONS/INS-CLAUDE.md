# Instructions pour l'Assistant IA - Projet JANUS

**Dernière mise à jour** : 5 Janvier 2026 - 20:45 UTC

## Objectif

Ce document définit les bonnes pratiques pour l'utilisation de l'assistant IA dans le cadre du projet JANUS, notamment pour les traitements intensifs (MCMC, nested sampling, analyses de données).

---

## 1. Stratégies d'Accélération des Traitements

### 1.1 Exécution en Background

Pour les calculs longs (>10 minutes), toujours lancer en background :

```bash
# Lancer et continuer à travailler
python scripts/run_mcmc_optimized.py --config config.json &

# Avec nohup pour les runs très longs (>1 heure)
nohup python scripts/run_mcmc_optimized.py --config config.json > /dev/null 2>&1 &

# Suivre la progression
tail -f mcmc_outputs/run_name.log

# Vérifier le statut
cat mcmc_outputs/run_name_status.json
```

### 1.2 Agents en Parallèle

L'assistant peut lancer **plusieurs agents simultanément** pour des tâches indépendantes :

```
Exemple : Lancer 3 analyses en parallèle
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Agent 1         │  │ Agent 2         │  │ Agent 3         │
│ MCMC modèle A   │  │ MCMC modèle B   │  │ Analyse données │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                    Résultats consolidés
```

**Cas d'usage** :
- Comparaisons de modèles (JANUS vs ΛCDM)
- Analyses sur différents datasets
- Tests de sensibilité aux paramètres

### 1.3 Architecture de Travail Efficace

```
┌─────────────────────────────────────────────────────────┐
│                    SESSION DE TRAVAIL                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Terminal 1 - Background]     [Terminal 2 - Actif]    │
│  ┌───────────────────────┐     ┌───────────────────┐   │
│  │ MCMC en cours...      │     │ Préparation       │   │
│  │ Progress: 45%         │     │ prochaine analyse │   │
│  │ ETA: 2h 30min         │     │                   │   │
│  └───────────────────────┘     └───────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Optimisations de Performance

### 2.1 Gains Estimés par Stratégie

| Stratégie | Gain Estimé | Implémentation |
|-----------|-------------|----------------|
| **Pool multiprocessing** | ~4x | 4 cœurs performance M4 |
| **Numba JIT** | ~10-100x | `@jit(nopython=True, cache=True)` |
| **Vectorisation NumPy** | ~5-20x | Éviter boucles Python |
| **Backend HDF5** | Illimité | Pas de limite mémoire |
| **Cache Numba** | ~2-5x | `cache=True` (évite recompilation) |

### 2.2 Configuration Optimale M4

```python
# Nombre de workers optimal pour Apple M4
N_PERFORMANCE_CORES = 4   # Cœurs performance uniquement
N_EFFICIENCY_CORES = 6    # Cœurs efficiency (tâches légères)
N_TOTAL_CORES = 10

# Pour calculs MCMC intensifs
n_workers = 4  # Utiliser uniquement les cœurs performance

# Pour tâches parallèles légères
n_workers = 10  # Utiliser tous les cœurs
```

### 2.3 Parallélisation emcee

```python
from multiprocessing import Pool
import emcee

# Créer pool avec cœurs performance
with Pool(4) as pool:
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim, log_prob,
        pool=pool,
        backend=backend  # HDF5 pour sauvegardes progressives
    )
    sampler.run_mcmc(pos, nsteps, progress=True)
```

### 2.4 Accélération Numba

```python
from numba import jit, prange
import numpy as np

@jit(nopython=True, cache=True, fastmath=True)
def fast_chi2(observed, model, errors):
    """
    Calcul chi² optimisé - ~100x plus rapide.
    """
    chi2 = 0.0
    for i in range(len(observed)):
        residual = (observed[i] - model[i]) / errors[i]
        chi2 += residual * residual
    return chi2

@jit(nopython=True, cache=True, parallel=True)
def fast_likelihood_batch(theta_batch, data, errors):
    """
    Calcul parallélisé sur tous les cœurs.
    """
    n_samples = theta_batch.shape[0]
    results = np.empty(n_samples)

    for i in prange(n_samples):
        theta = theta_batch[i]
        model = compute_model(theta)
        results[i] = -0.5 * fast_chi2(data, model, errors)

    return results
```

---

## 3. Estimation des Temps de Calcul

### 3.1 Temps Typiques sur M4 (24GB RAM)

| Configuration | Temps Estimé | Mémoire |
|---------------|--------------|---------|
| 32 walkers × 10,000 steps | ~10-30 min | ~50 MB |
| 32 walkers × 50,000 steps | ~1-2 heures | ~250 MB |
| 64 walkers × 100,000 steps | ~4-8 heures | ~1 GB |
| 128 walkers × 500,000 steps | ~24-48 heures | ~5 GB |

### 3.2 Script d'Estimation

```python
import time
import numpy as np

def estimate_runtime(log_prob_fn, pos_sample, nwalkers, nsteps, n_test=100):
    """
    Estime le temps total de calcul MCMC.
    """
    # Mesurer temps d'une évaluation
    times = []
    for _ in range(n_test):
        t0 = time.perf_counter()
        log_prob_fn(pos_sample)
        times.append(time.perf_counter() - t0)

    t_eval = np.median(times)

    # Estimation totale
    total_evals = nwalkers * nsteps
    t_serial = total_evals * t_eval
    t_parallel = t_serial / 4  # 4 cœurs performance

    # Overhead emcee (~20%)
    t_parallel *= 1.2

    print(f"Temps par évaluation: {t_eval*1000:.2f} ms")
    print(f"Temps estimé (4 cœurs): {t_parallel/3600:.1f} heures")

    return t_parallel
```

---

## 4. Workflow Recommandé

### 4.1 Phase 1 : Préparation (Assistant Actif)

```markdown
1. [ ] Générer/optimiser le code MCMC
2. [ ] Configurer les checkpoints (intervalle 500 steps)
3. [ ] Tester sur petit échantillon (100-500 steps)
4. [ ] Estimer temps total et mémoire
5. [ ] Créer fichier config.json
```

### 4.2 Phase 2 : Exécution (Background)

```markdown
1. [ ] Lancer MCMC en background avec nohup
2. [ ] Vérifier démarrage correct (log + status)
3. [ ] Assistant libre pour autres tâches
4. [ ] Monitoring périodique (optionnel)
```

### 4.3 Phase 3 : Analyse (Assistant Actif)

```markdown
1. [ ] Charger résultats depuis HDF5
2. [ ] Diagnostics convergence (τ, R-hat, acceptance)
3. [ ] Visualisations (corner plots, traces)
4. [ ] Génération rapport
```

---

## 5. Script MCMC Optimisé

Le projet inclut un script prêt à l'emploi : `scripts/run_mcmc_optimized.py`

### 5.1 Fonctionnalités

- Parallélisation sur 4 cœurs performance M4
- Checkpoints automatiques (configurable)
- Monitoring temps réel (mémoire, vitesse, ETA)
- Reprise automatique si interrompu
- Backend HDF5 (pas de limite mémoire)
- Gestion signaux (SIGINT/SIGTERM)
- Configuration par fichier JSON
- Fichier status JSON pour suivi externe

### 5.2 Usage

```bash
# Afficher exemple de configuration
python scripts/run_mcmc_optimized.py --example-config

# Créer votre config
python scripts/run_mcmc_optimized.py --example-config > my_config.json
# Éditer my_config.json

# Lancer en background
nohup python scripts/run_mcmc_optimized.py --config my_config.json > /dev/null 2>&1 &

# Suivre progression
tail -f mcmc_outputs/run_name.log
watch -n 10 cat mcmc_outputs/run_name_status.json
```

### 5.3 Exemple de Configuration

```json
{
    "run_name": "janus_highz_galaxies",
    "output_dir": "./mcmc_outputs",

    "nwalkers": 32,
    "nsteps": 50000,
    "ndim": 5,

    "n_workers": 4,
    "checkpoint_interval": 500,

    "log_prob_module": "janus_model",
    "log_prob_function": "log_probability",

    "prior_center": [70, 0.3, 0.5, 1.0, 0.1],
    "prior_width": [10, 0.1, 0.2, 0.5, 0.05]
}
```

---

## 6. Commandes Utiles

### 6.1 Gestion des Processus Background

```bash
# Lister processus Python
ps aux | grep python

# Trouver PID d'un run spécifique
cat mcmc_outputs/run_name_status.json | grep pid

# Arrêter proprement (sauvegarde checkpoint)
kill -TERM <PID>

# Arrêter forcé (pas de sauvegarde)
kill -9 <PID>
```

### 6.2 Monitoring Système

```bash
# Utilisation CPU en temps réel
top -pid <PID>

# Mémoire utilisée
ps -o pid,rss,command -p <PID>

# Utilisation disque
du -sh mcmc_outputs/
```

### 6.3 Analyse Rapide des Résultats

```python
import emcee
import corner

# Charger résultats
backend = emcee.backends.HDFBackend("mcmc_outputs/run_name.h5")

# Vérifier convergence
tau = backend.get_autocorr_time(tol=0)
print(f"Temps autocorrélation: {tau}")

# Extraire samples (après burn-in)
samples = backend.get_chain(discard=1000, thin=15, flat=True)

# Corner plot
fig = corner.corner(samples, labels=["H0", "Om0", "Om0_bar", "chi", "sigma"])
fig.savefig("corner_plot.pdf")
```

---

## 7. Bonnes Pratiques

### 7.1 Avant un Long Calcul

| Vérification | Commande |
|--------------|----------|
| Espace disque | `df -h .` |
| Mémoire disponible | `vm_stat` |
| Processus existants | `ps aux \| grep python` |
| Config valide | `python -c "import json; json.load(open('config.json'))"` |

### 7.2 Règles Générales

1. **Toujours tester d'abord** avec 100-500 steps
2. **Utiliser backend HDF5** pour runs >1000 steps
3. **Limiter mémoire à 20 GB** (garder 4 GB pour système)
4. **Sauvegarder configs** dans le repo pour reproductibilité
5. **Lancer en `nohup`** pour runs >1 heure
6. **Documenter chaque run** dans un log

### 7.3 En Cas de Problème

| Problème | Solution |
|----------|----------|
| Calcul bloqué | `kill -TERM <PID>` puis reprendre |
| Mémoire saturée | Réduire nwalkers ou utiliser chunking |
| Convergence lente | Vérifier priors, initialisation |
| Erreur au démarrage | Tester log_prob manuellement |

---

## 8. Communication avec l'Assistant

### 8.1 Demandes Efficaces

**Bon** :
```
"Lance un MCMC JANUS avec 32 walkers, 50000 steps, en background.
Paramètres: H0, Om0, Om0_bar, chi, sigma_int.
Config dans mcmc_outputs/janus_v1/"
```

**Moins bon** :
```
"Fais un MCMC"
```

### 8.2 Informations à Fournir

Pour un nouveau calcul MCMC, préciser :
- Modèle (JANUS, ΛCDM, autre)
- Nombre de paramètres et leurs noms
- Priors (bornes ou distributions)
- Données (fichier ou dataset)
- Objectif (exploration, comparaison, publication)

### 8.3 Suivi de Progression

L'assistant peut :
- Vérifier le statut d'un run background
- Analyser les logs en temps réel
- Estimer le temps restant
- Détecter les problèmes de convergence

---

## 9. Intégration avec le Projet JANUS

### 9.1 Structure des Fichiers

```
JANUS/
├── scripts/
│   └── run_mcmc_optimized.py    # Script MCMC principal
├── mcmc_outputs/                 # Résultats (ignoré par git)
│   ├── run_name.h5              # Chaîne MCMC
│   ├── run_name.log             # Logs
│   └── run_name_status.json     # Statut temps réel
├── configs/                      # Configurations (versionné)
│   └── janus_highz_v1.json
└── JANUS-INSTRUCTIONS/
    ├── INS-Statistiques.md      # Détails techniques MCMC
    └── INS-CLAUDE.md            # Ce fichier
```

### 9.2 Conventions de Nommage

```
Format: {modele}_{dataset}_{version}

Exemples:
- janus_highz_v1
- lcdm_snia_v2
- comparison_jwst_v1
```

---

## Historique des Modifications

| Date | Heure UTC | Modification |
|------|-----------|--------------|
| 2026-01-05 | 20:45 | Création initiale |

