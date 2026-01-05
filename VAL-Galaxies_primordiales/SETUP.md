# Guide d'Installation - VAL-Galaxies_primordiales

## Vue d'Ensemble

Ce document décrit l'installation et la configuration de l'environnement de développement pour le projet **VAL-Galaxies_primordiales**, Phase 1 du plan de validation du modèle cosmologique JANUS.

## Prérequis Système

### Configuration Minimale
- **CPU**: 4 cœurs
- **RAM**: 16 GB
- **Stockage**: 100 GB SSD disponibles
- **OS**: macOS 10.14+, Linux (Ubuntu 20.04+), Windows 10+ (avec WSL2)

### Configuration Recommandée
- **CPU**: 8+ cœurs (Apple Silicon M1/M2/M3 ou Intel/AMD récent)
- **RAM**: 32+ GB
- **Stockage**: 500 GB SSD
- **GPU** (optionnel): NVIDIA pour accélération calculs PyMC

## Installation

### Option 1: Environnement Virtuel Python (venv) - Recommandé

#### Étape 1: Cloner le Repository

```bash
cd ~
git clone https://github.com/PGPLF/JANUS.git
cd JANUS/VAL-Galaxies_primordiales
```

#### Étape 2: Créer l'Environnement Virtuel

```bash
# Créer l'environnement
python3 -m venv venv

# Activer l'environnement (macOS/Linux)
source venv/bin/activate

# Activer l'environnement (Windows WSL)
source venv/bin/activate

# Activer l'environnement (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

#### Étape 3: Installer les Dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer toutes les dépendances
pip install -r requirements.txt
```

#### Étape 4: Vérifier l'Installation

```bash
python -c "import numpy, scipy, matplotlib, astropy, emcee, corner, pymc; print('✓ Installation réussie!')"
```

### Option 2: Environnement Conda

#### Étape 1: Installer Miniconda

Si conda n'est pas installé:

```bash
# macOS (Apple Silicon)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh

# macOS (Intel)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh

# Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

#### Étape 2: Créer l'Environnement depuis environment.yml

```bash
cd ~/JANUS/VAL-Galaxies_primordiales
conda env create -f environment.yml
conda activate janus-val
```

#### Étape 3: Vérifier l'Installation

```bash
python -c "import numpy, scipy, matplotlib, astropy, emcee, corner, pymc; print('✓ Installation réussie!')"
```

## Configuration Jupyter

### Installation du Kernel

```bash
# Activer l'environnement
source venv/bin/activate  # ou: conda activate janus-val

# Installer le kernel Jupyter
python -m ipykernel install --user --name=janus-val --display-name="JANUS Validation"
```

### Lancer JupyterLab

```bash
jupyter lab
```

Le navigateur s'ouvrira automatiquement sur `http://localhost:8888`.

## Installation LaTeX (Optionnel - Pour Compilation PDF)

### macOS

```bash
# Option 1: BasicTeX (léger, ~100 MB)
brew install --cask basictex

# Option 2: MacTeX (complet, ~4 GB)
brew install --cask mactex

# Ajouter au PATH
eval "$(/usr/libexec/path_helper)"

# Installer packages LaTeX additionnels
sudo tlmgr update --self
sudo tlmgr install amsmath amssymb natbib
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install texlive-full texlive-lang-french bibtex
```

### Vérification

```bash
pdflatex --version
bibtex --version
```

## Tests de Validation

### Tests Unitaires

```bash
# Depuis la racine du projet
pytest tests/unit_tests/ -v
```

### Tests de Couverture

```bash
pytest tests/unit_tests/ --cov=src --cov-report=html
# Ouvrir htmlcov/index.html dans un navigateur
```

### Test des Imports

```bash
python -c "
import numpy as np
import scipy
import matplotlib.pyplot as plt
import astropy
import emcee
import corner
import pymc
import arviz
print('NumPy:', np.__version__)
print('SciPy:', scipy.__version__)
print('Matplotlib:', plt.matplotlib.__version__)
print('Astropy:', astropy.__version__)
print('emcee:', emcee.__version__)
print('PyMC:', pymc.__version__)
print('\\n✓ Tous les packages installés correctement!')
"
```

## Structure du Projet

```
VAL-Galaxies_primordiales/
├── README.md                   # Vue d'ensemble du projet
├── PLAN.md                     # Plan complet de validation (7 phases)
├── SETUP.md                    # Ce fichier
├── CHANGELOG.md                # Historique des versions
├── requirements.txt            # Dépendances Python (pip)
├── environment.yml             # Environnement conda
│
├── data/                       # Données observationnelles
│   ├── raw/                    # Données brutes
│   ├── processed/              # Données traitées
│   └── external/               # Références externes
│
├── src/                        # Code source
│   ├── cosmology/              # Modules cosmologie (JANUS, ΛCDM)
│   ├── statistics/             # Statistiques et MCMC
│   ├── plotting/               # Visualisations
│   └── utils/                  # Utilitaires
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01_data_preparation/
│   ├── 02_theoretical_predictions/
│   ├── 03_mcmc_analysis/
│   ├── 04_model_comparison/
│   └── 05_visualization/
│
├── scripts/                    # Scripts exécutables
├── results/                    # Résultats d'analyses
│   ├── mcmc/                   # Chaînes MCMC
│   ├── figures/                # Figures publication
│   ├── tables/                 # Tableaux de données
│   └── comparison/             # Comparaisons de modèles
│
├── papers/                     # Articles scientifiques
│   ├── main/                   # Article principal
│   ├── supplementary/          # Matériel supplémentaire
│   └── drafts/                 # Brouillons
│
├── docs/                       # Documentation
│   ├── theory/                 # Fondements théoriques
│   ├── methods/                # Méthodologie
│   └── validation/             # Protocoles de validation
│
└── tests/                      # Tests unitaires
    └── unit_tests/
```

## Dépannage

### Erreur: Module Not Found

Si un module n'est pas trouvé:

```bash
# Réinstaller les dépendances
pip install --force-reinstall -r requirements.txt
```

### Erreur: Permission Denied (macOS/Linux)

Si vous rencontrez des erreurs de permissions:

```bash
# N'utilisez PAS sudo avec pip dans un venv
# À la place, vérifiez que vous êtes dans l'environnement virtuel
which python  # Devrait afficher .../venv/bin/python
```

### Erreur: LaTeX Not Found

Si LaTeX n'est pas trouvé après installation:

```bash
# macOS: Ajouter au PATH
export PATH="/Library/TeX/texbin:$PATH"
echo 'export PATH="/Library/TeX/texbin:$PATH"' >> ~/.zshrc  # ou ~/.bashrc

# Relancer le terminal
```

### Problèmes de Mémoire (MCMC)

Pour les calculs MCMC intensifs, consultez `JANUS-INSTRUCTIONS/INS-Statistiques.md` pour:
- Configuration des checkpoints HDF5
- Optimisation du nombre de workers
- Monitoring de la mémoire

## Mises à Jour

### Mettre à Jour les Dépendances

```bash
# venv
pip install --upgrade -r requirements.txt

# conda
conda env update -f environment.yml --prune
```

### Mettre à Jour le Code

```bash
cd ~/JANUS/VAL-Galaxies_primordiales
git pull origin main
```

## Ressources Supplémentaires

- **Documentation JANUS**: `../JANUS-INSTRUCTIONS/`
- **Infrastructure**: `../JANUS-INSTRUCTIONS/INS-Infrastructure.md`
- **Statistiques MCMC**: `../JANUS-INSTRUCTIONS/INS-Statistiques.md`
- **Compilation PDF**: `../JANUS-INSTRUCTIONS/INS-PDF_COMPILATION.md`

## Support

Pour toute question ou problème:
1. Consulter les `JANUS-INSTRUCTIONS/`
2. Vérifier les issues GitHub: https://github.com/PGPLF/JANUS/issues
3. Créer une nouvelle issue avec le tag `[VAL-Galaxies_primordiales]`

---

**Date de dernière mise à jour**: 5 Janvier 2026
**Version**: Phase 1.0
