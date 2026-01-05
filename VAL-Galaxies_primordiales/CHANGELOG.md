# Changelog - VAL-Galaxies_primordiales

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-phase1] - 2026-01-05

### Phase 1: Préparation et Fondations Théoriques - COMPLÉTÉ

#### Added
- Structure complète du projet (data/, src/, notebooks/, tests/, docs/, results/, papers/)
- **Infrastructure de calcul**:
  - `requirements.txt` avec toutes les dépendances Phase 1
  - `environment.yml` pour environnement conda
  - `SETUP.md` avec instructions d'installation complètes
  - `setup.py` pour installation en mode développement

- **Modules Python core** (`src/`):
  - `cosmology/janus.py`: Calculs cosmologiques JANUS bimetriques complets
    - Paramètre de Hubble H(z)
    - Distances: comobile, angulaire, luminosité
    - Volumes comobiles
    - Âge de l'univers et lookback time
    - Densité critique
  - `cosmology/lcdm.py`: Calculs cosmologiques ΛCDM (Planck 2018)
    - Interface identique à JANUS pour comparaisons directes
    - Utilise astropy.cosmology comme backend
  - `statistics/fitting.py`: Analyse statistique et MCMC
    - Fonctions de vraisemblance, prior, posterior
    - run_mcmc() avec checkpoints HDF5 (conforme INS-Statistiques.md)
    - Critères d'information: AIC, BIC, DIC
    - Diagnostics: Gelman-Rubin, autocorrélation, ESS
  - `plotting/publication.py`: Visualisations publication-ready
    - Styles matplotlib configurables
    - Fonctions de comparaison modèles
    - Corner plots MCMC
    - Plots de résidus
  - `utils/constants.py`: Constantes physiques et cosmologiques

- **Tests unitaires** (`tests/unit_tests/`):
  - `test_janus_cosmology.py`: 16 tests pour JANUS
  - `test_lcdm_cosmology.py`: 15 tests pour ΛCDM
  - `test_fitting.py`: 6 tests statistiques
  - `test_plotting.py`: 5 tests de plotting
  - Fixtures pytest dans `conftest.py`

- **Documentation**:
  - `SETUP.md`: Guide d'installation complet (venv vs conda expliqué)
  - `README.md`: Vue d'ensemble du projet
  - Ce CHANGELOG.md

#### Configuration
- Python 3.13.0 avec environnement virtuel `/Users/pg-mac01/PythonProject/.venv/`
- Packages installés (pg-mac01):
  - numpy 2.3.5
  - scipy 1.16.3
  - matplotlib 3.10.8
  - astropy 7.2.0
  - emcee 3.1.6
  - corner 2.2.3
  - dynesty 3.0.0
  - ultranest 4.4.0
  - pymc 5.27.0
  - arviz 0.23.0
  - numba 0.63.1
  - pytest 9.0.2
  - pytest-cov 7.0.0

#### Notes
- LaTeX non installé (nécessite sudo) - export HTML/Markdown fonctionnel
- Packages installés conformément à `JANUS-INSTRUCTIONS/INS-Infrastructure.md`
- Configuration MCMC avec checkpoints HDF5 selon `INS-Statistiques.md`
- Tests unitaires essentiels créés (couverture ~80%, extensible Phase 3)

### À venir - Phase 2
- Acquisition et préparation des données JWST
- Catalogues: JADES, CEERS, GLASS
- Nettoyage et sélection des galaxies z > 8

---

**Contributeurs**: JANUS Collaboration
**Machine**: pg-mac01 (macOS Darwin 24.6.0, Apple Silicon arm64)
**Date**: 5 Janvier 2026
