# VAL-Galaxies Primordiales

**Validation du modèle cosmologique JANUS par confrontation aux observations de galaxies primordiales**

## Vue d'Ensemble

Ce projet vise à valider systématiquement le modèle cosmologique JANUS bimétrique par confrontation rigoureuse aux observations récentes de galaxies primordiales (z > 8), notamment celles du James Webb Space Telescope (JWST), en comparaison directe avec le modèle standard ΛCDM.

### Objectifs

- **Validation scientifique**: Tester les prédictions du modèle JANUS pour la formation des premières structures cosmiques
- **Comparaison quantitative**: Analyse bayésienne (MCMC) avec critères d'information (AIC, BIC, DIC)
- **Publication**: Article dans revue Tier 1 (ApJ, MNRAS, A&A)
- **Reproductibilité**: Code ouvert, données accessibles, méthodologie transparente

### Observations Clés JWST

Les galaxies primordiales observées par JWST présentent des caractéristiques surprenantes pour ΛCDM:
- **Masses stellaires importantes** à très haut redshift (z > 10)
- **Maturité structurelle précoce** (galaxies déjà évoluées à z ~ 12-14)
- **Abondance élevée** de galaxies massives peu après le Big Bang
- **Vitesses de formation stellaire** (SFR) plus rapides que prédit par ΛCDM

Le modèle JANUS prédit naturellement une formation plus rapide des structures grâce au secteur de masse négative.

## État d'Avancement

### ✅ Phase 1 Complétée (5 Janvier 2026)

**Préparation et Fondations Théoriques**

Infrastructure de calcul et modules Python opérationnels:

| Composant | Status | Description |
|-----------|--------|-------------|
| Structure projet | ✅ | 8 dossiers organisés (data/, src/, notebooks/, tests/, etc.) |
| Environnement Python | ✅ | venv avec 15+ packages scientifiques |
| Module JANUS | ✅ | Cosmologie bimétrique complète (H(z), distances, âges) |
| Module ΛCDM | ✅ | Cosmologie standard (Planck 2018, via astropy) |
| Statistiques MCMC | ✅ | emcee, checkpoints HDF5, diagnostics convergence |
| Plotting | ✅ | Figures publication-ready, corner plots |
| Tests unitaires | ✅ | 42 tests (cosmology, statistics, plotting) |
| Documentation | ✅ | SETUP.md, CHANGELOG.md, ce README |

**Packages installés** (pg-mac01): numpy 2.3.5, scipy 1.16.3, matplotlib 3.10.8, astropy 7.2.0, emcee 3.1.6, corner 2.2.3, dynesty 3.0.0, pymc 5.27.0, arviz 0.23.0, numba 0.63.1, pytest 9.0.2

### 📋 Phase 2 À venir

**Acquisition et Préparation des Données**

- Téléchargement catalogues JWST (JADES, CEERS, GLASS)
- Compilation galaxies z > 8 avec masses stellaires, SFR, magnitudes UV
- Nettoyage et sélection (qualité photométrique, biais)
- Documentation provenance et qualité

### 🔮 Phases 3-7

Voir [`PLAN.md`](PLAN.md) pour le plan complet en 7 phases.

## Installation Rapide

### Prérequis
- Python 3.10+ (testé avec 3.13.0)
- 16+ GB RAM recommandé
- Git

### Installation

```bash
# Cloner le repository
git clone https://github.com/PGPLF/JANUS.git
cd JANUS/VAL-Galaxies_primordiales

# Créer et activer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou: .\venv\Scripts\activate  # Windows

# Installer dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Installer en mode développement
pip install -e .

# Vérifier installation
python -c "import sys; sys.path.insert(0, 'src'); from cosmology import JANUSCosmology, LCDMCosmology; print('✓ Installation réussie!')"
```

### Tests

```bash
# Lancer tous les tests
pytest tests/unit_tests/ -v

# Tests avec couverture
pytest tests/unit_tests/ --cov=src --cov-report=html
```

Voir [`SETUP.md`](SETUP.md) pour instructions détaillées.

## Utilisation

### Calculs Cosmologiques

```python
import sys
sys.path.insert(0, 'src')
from cosmology import JANUSCosmology, LCDMCosmology

# Modèle JANUS
janus = JANUSCosmology(H0=70.0, Omega_plus=0.30, Omega_minus=0.05)
print(f"H(z=10) = {janus.hubble_parameter(10):.2f} km/s/Mpc")
print(f"Age(z=10) = {janus.age_of_universe(10):.3f} Gyr")
print(f"d_L(z=10) = {janus.luminosity_distance(10):.2f} Mpc")

# Modèle ΛCDM (Planck 2018)
lcdm = LCDMCosmology()
print(f"H(z=10) = {lcdm.hubble_parameter(10):.2f} km/s/Mpc")
print(f"Age(z=10) = {lcdm.age_of_universe(10):.3f} Gyr")
```

### Analyse MCMC

```python
from statistics import run_mcmc, compute_bic

# Définir modèle et données
def model(params):
    # Votre modèle ici
    pass

# Lancer MCMC
sampler, samples = run_mcmc(
    log_prob_fn=lambda p: log_posterior(p, model, data, errors, bounds),
    initial_params=[70.0, 0.30, 0.05],
    nwalkers=32,
    nsteps=5000,
    backend_file='results/mcmc/janus_chains.h5'  # Checkpoints HDF5
)

# Calculer BIC
bic = compute_bic(log_likelihood_max, n_params=3, n_data=len(data))
print(f"BIC = {bic:.2f}")
```

### Visualisations

```python
from plotting import plot_comparison, plot_corner_mcmc, setup_plot_style

# Style publication
setup_plot_style('publication')

# Comparaison modèles
fig, ax = plot_comparison(
    z=redshifts,
    obs_data=observations,
    obs_errors=errors,
    janus_pred=janus_predictions,
    lcdm_pred=lcdm_predictions,
    xlabel='Redshift z',
    ylabel='Stellar Mass [$M_\\odot$]',
    save_path='results/figures/comparison'
)

# Corner plot MCMC
fig = plot_corner_mcmc(
    samples,
    labels=['$H_0$', '$\\Omega_+$', '$\\Omega_-$'],
    save_path='results/figures/corner_janus'
)
```

## Structure du Projet

```
VAL-Galaxies_primordiales/
├── README.md                 # Ce fichier
├── PLAN.md                   # Plan complet 7 phases
├── SETUP.md                  # Installation détaillée
├── CHANGELOG.md              # Historique versions
├── requirements.txt          # Dépendances pip
├── environment.yml           # Environnement conda
├── setup.py                  # Installation package
│
├── data/                     # Données observationnelles
│   ├── raw/                  # Catalogues bruts JWST
│   ├── processed/            # Données nettoyées
│   └── external/             # Références
│
├── src/                      # Code source
│   ├── cosmology/            # JANUS & ΛCDM
│   ├── statistics/           # MCMC, fitting
│   ├── plotting/             # Visualisations
│   └── utils/                # Constantes, helpers
│
├── notebooks/                # Jupyter notebooks
│   ├── 02_theoretical_predictions/
│   ├── 03_mcmc_analysis/
│   └── 04_model_comparison/
│
├── scripts/                  # Scripts exécutables
├── results/                  # Résultats analyses
│   ├── mcmc/                 # Chaînes MCMC
│   ├── figures/              # Figures publication
│   └── comparison/           # Comparaisons modèles
│
├── papers/                   # Articles scientifiques
├── docs/                     # Documentation théorique
└── tests/                    # Tests unitaires
    └── unit_tests/
```

## Références

### Modèle JANUS
- Petit, J.-P. & D'Agostini, G. (2014-2024) - Publications sur le modèle cosmologique JANUS bimétrique

### Observations JWST
- Robertson et al. (2023) - Identification of Four Extremely Red Objects at z > 10
- Bouwens et al. (2023) - JWST NIRCam + NIRSpec: Interstellar Medium and Stellar Populations at z > 8
- Labbé et al. (2023) - A population of red candidate massive galaxies at z > 10

### Cosmologie Standard
- Planck Collaboration (2018) - Planck 2018 results. VI. Cosmological parameters

## Contributions

Ce projet fait partie du travail de validation scientifique du modèle JANUS.

**Contributeurs**: JANUS Collaboration

## License

À déterminer (en discussion)

## Contact

Pour questions ou collaborations: voir issues GitHub https://github.com/PGPLF/JANUS/issues

---

**Status**: Phase 1 complétée ✅ | **Version**: 0.1.0-phase1 | **Date**: 5 Janvier 2026
