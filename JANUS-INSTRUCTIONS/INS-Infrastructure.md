# Infrastructure de Calcul pour l'Astrophysique et la Cosmologie - Projet JANUS

## Objectif

Mettre en place une infrastructure complète de calcul scientifique pour les analyses astrophysiques, cosmologiques et statistiques du projet JANUS, incluant les analyses MCMC (Markov Chain Monte Carlo), l'ajustement bayésien, et la comparaison de modèles.

---

## 1. Environnement Python Scientifique

### 1.1 Python et Gestion d'Environnements

**Version recommandée** : Python 3.10+ (testé avec 3.13.0)

**Création d'environnement virtuel** :
```bash
# Créer un environnement virtuel dédié
python3 -m venv janus_env

# Activer l'environnement
# Sur macOS/Linux:
source janus_env/bin/activate
# Sur Windows:
janus_env\Scripts\activate

# Mettre à jour pip
pip install --upgrade pip
```

### 1.2 Bibliothèques Scientifiques de Base

```bash
# Calcul numérique et algèbre linéaire
pip install numpy scipy

# Visualisation
pip install matplotlib seaborn

# Analyse de données
pip install pandas

# Astronomie et cosmologie
pip install astropy astroquery
```

**Détail des packages** :
- **NumPy** : Calcul vectoriel, matrices, algèbre linéaire
- **SciPy** : Intégration numérique, optimisation, interpolation, statistiques
- **Matplotlib** : Visualisation 2D/3D, graphiques scientifiques
- **Seaborn** : Visualisations statistiques avancées
- **Pandas** : Manipulation de données tabulaires
- **Astropy** : Constantes astronomiques, unités, cosmologie, coordonnées
- **Astroquery** : Accès aux bases de données astronomiques (SDSS, Gaia, etc.)

---

## 2. Analyse Statistique et MCMC

### 2.1 emcee - MCMC Affine-Invariant

**Installation** :
```bash
pip install emcee corner
```

**Utilisation** :
```python
import emcee
import numpy as np

# Définir la log-probabilité
def log_probability(theta, x, y, yerr):
    # Modèle : y = m*x + b
    m, b, log_f = theta
    model = m * x + b
    sigma2 = yerr**2 + model**2 * np.exp(2 * log_f)
    return -0.5 * np.sum((y - model)**2 / sigma2 + np.log(sigma2))

# Configuration MCMC
ndim = 3  # Nombre de paramètres
nwalkers = 32  # Nombre de marcheurs
nsteps = 5000  # Nombre d'itérations

# Position initiale
pos = np.random.randn(nwalkers, ndim)

# Initialiser le sampler
sampler = emcee.EnsembleSampler(
    nwalkers, ndim, log_probability,
    args=(x_data, y_data, yerr_data)
)

# Exécuter MCMC
sampler.run_mcmc(pos, nsteps, progress=True)
```

### 2.2 PyMC - Modélisation Bayésienne Probabiliste

**Installation** :
```bash
pip install pymc arviz
```

**Caractéristiques** :
- Modélisation bayésienne de haut niveau
- Samplers MCMC modernes (NUTS, HMC)
- Diagnostic et visualisation intégrés
- Excellent pour modèles hiérarchiques

### 2.3 Corner.py - Visualisation des Distributions Postérieures

```python
import corner

# Créer un corner plot
fig = corner.corner(
    samples,
    labels=["$m$", "$b$", "$\ln f$"],
    truths=[m_true, b_true, np.log(f_true)],
    quantiles=[0.16, 0.5, 0.84],
    show_titles=True
)
```

---

## 3. Cosmologie et Astrophysique

### 3.1 Astropy Cosmology

```bash
pip install astropy
```

**Exemple - Calcul de distances cosmologiques** :
```python
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

# Définir cosmologie ΛCDM
cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Om0=0.3)

# Calculer distance luminosité
z = 1.5
d_L = cosmo.luminosity_distance(z)

# Âge de l'univers
age = cosmo.age(z)

# Module de distance
mu = cosmo.distmod(z)
```

### 3.2 Cosmologie Personnalisée pour JANUS

Pour implémenter le modèle JANUS avec métriques bimétriques :

```python
from astropy.cosmology import FLRW
import astropy.units as u
import numpy as np

class JANUSCosmology(FLRW):
    """
    Modèle cosmologique JANUS avec univers jumeaux
    """
    def __init__(self, H0, Om0, Om0_bar, chi, kappa=-1):
        """
        H0: Constante de Hubble
        Om0: Densité de matière (univers positif)
        Om0_bar: Densité de matière (univers négatif)
        chi: Constante de couplage
        kappa: Signature métrique (-1 pour masse négative)
        """
        super().__init__(H0=H0, Om0=Om0, Ode0=1-Om0, Tcmb0=2.725)
        self.Om0_bar = Om0_bar
        self.chi = chi
        self.kappa = kappa

    def H(self, z):
        """Fonction de Hubble modifiée pour JANUS"""
        # Implémenter équations de Friedmann bimétriques
        # (À compléter selon modèle théorique)
        pass
```

### 3.3 CCL - Core Cosmology Library

```bash
pip install pyccl
```

**Caractéristiques** :
- Calculs cosmologiques rapides
- Spectre de puissance de matière
- Fonctions de corrélation angulaire
- Optimisé pour analyses de grands relevés

---

## 4. Analyse de Données Observationnelles

### 4.1 Accès aux Données JWST

```bash
pip install astroquery jwst
```

**Exemple - Télécharger données JWST** :
```python
from astroquery.mast import Observations

# Rechercher observations
obs_table = Observations.query_criteria(
    obs_collection="JWST",
    instrument_name="NIRCAM",
    target_name="SMACS0723"
)

# Télécharger produits
data_products = Observations.get_product_list(obs_table)
Observations.download_products(data_products)
```

### 4.2 Photométrie et Analyse d'Images

```bash
pip install photutils sep
```

- **Photutils** : Photométrie d'ouverture, PSF fitting, détection de sources
- **SEP** : Source Extractor en Python (rapide)

### 4.3 Ajustement de SED (Spectral Energy Distribution)

```bash
pip install prospector sedpy fsps
```

- **Prospector** : Ajustement bayésien de SED
- **FSPS** : Modèles de synthèse de populations stellaires

---

## 5. Comparaison de Modèles Statistiques

### 5.1 Critères d'Information

**Installation** :
```bash
pip install scipy statsmodels
```

**Calcul BIC et AIC** :
```python
import numpy as np

def calculate_bic(log_likelihood, n_params, n_data):
    """
    Calcule le Bayesian Information Criterion
    """
    return n_params * np.log(n_data) - 2 * log_likelihood

def calculate_aic(log_likelihood, n_params):
    """
    Calcule le Akaike Information Criterion
    """
    return 2 * n_params - 2 * log_likelihood

def calculate_bayes_factor(log_evidence1, log_evidence2):
    """
    Calcule le facteur de Bayes
    log_evidence = log(P(D|M))
    """
    return np.exp(log_evidence1 - log_evidence2)
```

### 5.2 Nested Sampling

**Installation** :
```bash
pip install dynesty ultranest
```

- **Dynesty** : Nested sampling pour calcul d'évidence bayésienne
- **UltraNest** : Nested sampling pour hautes dimensions

**Exemple Dynesty** :
```python
import dynesty

# Définir prior transform et likelihood
def prior_transform(u):
    # Transform unit cube to prior
    return u  # (à adapter)

def log_likelihood(theta):
    # Calculate log-likelihood
    return -0.5 * np.sum((data - model(theta))**2 / errors**2)

# Run nested sampling
sampler = dynesty.NestedSampler(
    log_likelihood, prior_transform, ndim=3
)
sampler.run_nested()
results = sampler.results

# Evidence bayésienne
log_evidence = results.logz
log_evidence_err = results.logzerr
```

---

## 6. Calcul Parallèle et Haute Performance

### 6.1 Multiprocessing

```python
import multiprocessing as mp
from functools import partial

def parallel_mcmc(nwalkers, ndim, nsteps):
    """MCMC avec parallélisation"""
    with mp.Pool() as pool:
        sampler = emcee.EnsembleSampler(
            nwalkers, ndim, log_probability,
            args=(x, y, yerr),
            pool=pool
        )
        sampler.run_mcmc(pos, nsteps)
    return sampler
```

### 6.2 Numba - JIT Compilation

```bash
pip install numba
```

**Exemple** :
```python
from numba import jit

@jit(nopython=True)
def fast_calculation(x):
    """Fonction accélérée par JIT compilation"""
    result = 0.0
    for i in range(len(x)):
        result += np.exp(-x[i]**2)
    return result
```

### 6.3 JAX - Différentiation Automatique et GPU

```bash
pip install jax jaxlib
```

**Caractéristiques** :
- Différentiation automatique
- Compilation XLA
- Support GPU/TPU
- Idéal pour optimisation de modèles complexes

---

## 7. Jupyter Notebooks et Documentation Interactive

### 7.1 Installation Jupyter

```bash
pip install jupyter jupyterlab ipywidgets
```

### 7.2 Extensions Utiles

```bash
# Extension pour exportation PDF
pip install nbconvert

# Widgets interactifs
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Support LaTeX
pip install jupyter-latex-envs
```

### 7.3 Notebooks Recommandés pour JANUS

Structure suggérée :
```
notebooks/
├── 01_data_preparation.ipynb       # Préparation données JWST
├── 02_janus_model.ipynb            # Implémentation modèle JANUS
├── 03_lcdm_model.ipynb             # Modèle ΛCDM de référence
├── 04_mcmc_janus.ipynb             # Ajustement MCMC JANUS
├── 05_mcmc_lcdm.ipynb              # Ajustement MCMC ΛCDM
├── 06_model_comparison.ipynb       # Comparaison statistique
└── 07_results_visualization.ipynb   # Visualisation résultats
```

---

## 8. Gestion des Données et Stockage

### 8.1 HDF5 pour Données Volumineuses

```bash
pip install h5py
```

**Exemple** :
```python
import h5py

# Sauvegarder chaînes MCMC
with h5py.File('mcmc_results.h5', 'w') as f:
    f.create_dataset('samples', data=sampler.chain)
    f.create_dataset('log_prob', data=sampler.lnprobability)
    f.attrs['nwalkers'] = nwalkers
    f.attrs['nsteps'] = nsteps
```

### 8.2 Pickle pour Objets Python

```python
import pickle

# Sauvegarder sampler complet
with open('sampler.pkl', 'wb') as f:
    pickle.dump(sampler, f)

# Charger
with open('sampler.pkl', 'rb') as f:
    sampler_loaded = pickle.load(f)
```

---

## 9. Contrôle de Version et Reproductibilité

### 9.1 Requirements.txt

Créer un fichier `requirements.txt` :
```text
# Core scientifique
numpy>=2.0.0
scipy>=1.10.0
pandas>=2.0.0

# Visualisation
matplotlib>=3.8.0
seaborn>=0.13.0
corner>=2.2.0

# Astronomie et cosmologie
astropy>=7.0.0
astroquery>=0.4.11
photutils>=1.9.0

# MCMC et statistiques bayésiennes
emcee>=3.1.0
dynesty>=2.1.0
arviz>=0.15.0
chainconsumer>=1.0.0

# Performance
numba>=0.57.0
h5py>=3.9.0

# Notebooks
jupyter>=1.0.0
jupyterlab>=4.0.0

# Tests
pytest>=7.0.0
```

Installer :
```bash
pip install -r requirements.txt
```

### 9.2 Freeze de l'Environnement

```bash
# Exporter environnement exact
pip freeze > requirements_frozen.txt

# Ou avec conda
conda env export > environment.yml
```

---

## 10. Configuration Matérielle Recommandée

### 10.1 Pour Analyses MCMC Standard

**Minimum** :
- CPU : 4 cœurs (8 threads)
- RAM : 16 GB
- Stockage : 100 GB SSD

**Recommandé** :
- CPU : 8+ cœurs (16+ threads)
- RAM : 32+ GB
- Stockage : 500 GB+ SSD
- GPU : Optionnel (pour JAX/TensorFlow)

### 10.2 Pour Analyses Intensives (High-Z galaxies, nested sampling)

**Optimal** :
- CPU : 16+ cœurs (32+ threads) ou accès cluster HPC
- RAM : 64-128 GB
- Stockage : 1+ TB NVMe SSD
- GPU : NVIDIA avec CUDA (V100, A100 pour deep learning)

---

## 11. Tests et Validation

### 11.1 Tests Unitaires

```bash
pip install pytest
```

**Exemple de test** :
```python
# test_janus_cosmology.py
import pytest
from janus_model import JANUSCosmology

def test_hubble_parameter():
    cosmo = JANUSCosmology(H0=70, Om0=0.3, Om0_bar=0.7)
    H_z0 = cosmo.H(0)
    assert abs(H_z0.value - 70) < 1e-6
```

### 11.2 Validation Croisée

```python
from sklearn.model_selection import KFold

# K-fold cross-validation pour robustesse
kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, test_idx in kf.split(data):
    train_data = data[train_idx]
    test_data = data[test_idx]
    # Ajuster modèle et valider
```

---

## 12. Ressources et Documentation

### 12.1 Documentation Officielle

- **emcee** : https://emcee.readthedocs.io/
- **Astropy** : https://docs.astropy.org/
- **PyMC** : https://www.pymc.io/
- **Dynesty** : https://dynesty.readthedocs.io/
- **Matplotlib** : https://matplotlib.org/

### 12.2 Tutoriels Recommandés

- **MCMC avec emcee** : https://emcee.readthedocs.io/en/stable/tutorials/line/
- **Cosmologie Astropy** : https://docs.astropy.org/en/stable/cosmology/
- **Nested Sampling** : https://dynesty.readthedocs.io/en/stable/quickstart.html

### 12.3 Livres de Référence

- **"Data Analysis: A Bayesian Tutorial"** - D.S. Sivia
- **"Information Theory, Inference, and Learning Algorithms"** - David MacKay
- **"Modern Statistical Methods for Astronomy"** - Feigelson & Babu
- **"Cosmology"** - Steven Weinberg

---

## 13. Checklist d'Installation Complète

### Environnement de Base
- [ ] Python 3.10+ installé
- [ ] Environnement virtuel créé
- [ ] pip mis à jour

### Packages Scientifiques
- [ ] NumPy, SciPy installés
- [ ] Matplotlib, Seaborn installés
- [ ] Pandas installé
- [ ] Astropy installé

### MCMC et Statistiques
- [ ] emcee installé
- [ ] corner installé
- [ ] dynesty ou ultranest installé
- [ ] PyMC (optionnel)

### Cosmologie
- [ ] Astropy cosmology testé
- [ ] CCL installé (optionnel)
- [ ] Classe cosmologie JANUS implémentée

### Données Observationnelles
- [ ] astroquery installé
- [ ] photutils installé
- [ ] Accès API MAST configuré

### Notebooks
- [ ] Jupyter Lab installé
- [ ] Extensions installées
- [ ] Structure notebooks créée

### Performance
- [ ] Numba installé et testé
- [ ] Multiprocessing testé
- [ ] JAX installé (si GPU disponible)

### Reproductibilité
- [ ] requirements.txt créé
- [ ] Git configuré
- [ ] Tests unitaires mis en place

---

## 14. Scripts d'Installation Automatisés

### 14.1 Installation Complète (macOS/Linux)

```bash
#!/bin/bash
# install_janus_env.sh

# Créer environnement
python3 -m venv janus_env
source janus_env/bin/activate

# Mise à jour pip
pip install --upgrade pip

# Packages de base
pip install numpy scipy matplotlib seaborn pandas

# Astronomie
pip install astropy astroquery photutils

# MCMC et statistiques
pip install emcee corner dynesty arviz

# Cosmologie
pip install pyccl

# Notebooks
pip install jupyter jupyterlab ipywidgets nbconvert

# Performance
pip install numba

# Tests
pip install pytest

# Sauvegarder configuration
pip freeze > requirements.txt

echo "Installation terminée! Activer avec: source janus_env/bin/activate"
```

### 14.2 Vérification de l'Installation

```python
# verify_installation.py
import sys

packages = {
    'numpy': '1.24.0',
    'scipy': '1.10.0',
    'matplotlib': '3.7.0',
    'astropy': '5.3.0',
    'emcee': '3.1.0',
    'corner': '2.2.0',
    'dynesty': '2.0.0',
    'jupyter': '1.0.0'
}

print("Vérification des packages installés:\n")
for package, min_version in packages.items():
    try:
        module = __import__(package)
        version = getattr(module, '__version__', 'unknown')
        status = '✅' if version >= min_version else '⚠️'
        print(f"{status} {package}: {version} (minimum: {min_version})")
    except ImportError:
        print(f"❌ {package}: NON INSTALLÉ")

print("\n" + "="*50)
print("Python:", sys.version)
```

---

## 15. Workflow Type pour Analyse JANUS

### Pipeline Complet

```python
# janus_analysis_pipeline.py

import numpy as np
import emcee
import corner
from astropy.cosmology import FlatLambdaCDM
from astroquery.mast import Observations

# 1. Télécharger données JWST
def download_jwst_data(target):
    obs = Observations.query_criteria(
        obs_collection="JWST",
        target_name=target
    )
    return obs

# 2. Préparer données
def prepare_data(obs):
    # Extraire magnitudes, redshifts, erreurs
    pass

# 3. Définir modèles
class JANUSModel:
    def predict_magnitude(self, z, params):
        # Prédiction JANUS
        pass

class LCDMModel:
    def predict_magnitude(self, z, params):
        # Prédiction ΛCDM
        pass

# 4. MCMC fitting
def run_mcmc(model, data, nwalkers=32, nsteps=5000):
    def log_prob(theta):
        return model.log_likelihood(theta, data)

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob)
    sampler.run_mcmc(initial_pos, nsteps, progress=True)
    return sampler

# 5. Comparaison modèles
def compare_models(samples_janus, samples_lcdm, data):
    bic_janus = calculate_bic(...)
    bic_lcdm = calculate_bic(...)
    delta_bic = bic_lcdm - bic_janus

    print(f"ΔBIC (ΛCDM - JANUS): {delta_bic}")
    if delta_bic > 10:
        print("Évidence très forte pour JANUS")

    return delta_bic

# 6. Visualisation
def plot_results(samples_janus, samples_lcdm):
    fig = corner.corner(samples_janus, labels=["H0", "Om0", "chi"])
    fig.savefig("janus_corner.pdf")

# Exécution pipeline
if __name__ == "__main__":
    data = download_jwst_data("SMACS0723")
    data_clean = prepare_data(data)

    janus = JANUSModel()
    lcdm = LCDMModel()

    samples_janus = run_mcmc(janus, data_clean)
    samples_lcdm = run_mcmc(lcdm, data_clean)

    delta_bic = compare_models(samples_janus, samples_lcdm, data_clean)
    plot_results(samples_janus, samples_lcdm)
```

---

## État d'Installation / Configuration

### Session du 5 Janvier 2026 - 15:30 UTC

#### Machine: pg-mac01 (macOS Darwin 24.6.0, Apple Silicon arm64)

**✅ Installé et Fonctionnel** :
- Python 3.13.0 (environnement virtuel: `/Users/pg-mac01/PythonProject/.venv/`)
- pip 25.3
- Jupyter Notebook 7.5.1
- JupyterLab 4.5.1
- IPython 9.9.0
- nbconvert 7.16.6
- Bibliothèques de base Jupyter:
  - ipykernel 7.1.0
  - ipywidgets 8.1.8
  - jupyter-client 8.7.0
  - jupyter-core 5.9.1
  - jupyter-server 2.17.0
  - matplotlib-inline 0.2.1
  - nbformat 5.10.4
  - pygments 2.19.2
- Git (via Homebrew)
- Homebrew: `/opt/homebrew/bin/brew`

**⚠️ À Installer** :
- **Packages scientifiques Python** :
  ```bash
  pip install numpy scipy matplotlib astropy emcee corner dynesty pandas seaborn photutils astroquery numba
  ```
- **LaTeX** (pdflatex, bibtex) :
  - Nécessite privilèges administrateur
  - Options recommandées:
    - BasicTeX (~100 MB): `brew install --cask basictex` (avec sudo)
    - MacTeX complet (~4 GB): https://www.tug.org/mactex/
  - Après installation: `eval "$(/usr/libexec/path_helper)"`

**Vérification** :
```bash
# Vérifier installations actuelles
python3 --version      # ✅ 3.13.0
jupyter --version      # ✅ 7.5.1
pip --version          # ✅ 25.3

# À vérifier après installation packages scientifiques
python3 -c "import numpy; print(numpy.__version__)"
python3 -c "import emcee; print(emcee.__version__)"
python3 -c "import astropy; print(astropy.__version__)"

# LaTeX
pdflatex --version     # ❌ Non installé
```

**Remarques** :
- Environnement Jupyter pleinement opérationnel
- Installation packages scientifiques possible immédiatement (pas besoin sudo)
- Conversion PDF depuis Jupyter nécessite LaTeX
- Export HTML/Markdown fonctionne sans LaTeX

---

### Machine: patrickguerin-imac (iMac M4 24")

**Dernière mise à jour** : 5 Janvier 2026 - 21:00 UTC

**Configuration Matérielle** :
| Composant | Spécification |
|-----------|---------------|
| Modèle | iMac (Mac16,3) |
| Processeur | Apple M4 (10 cœurs: 4 performance + 6 efficiency) |
| Mémoire | 24 GB RAM unifié |
| Stockage | 228 GB SSD (75 GB disponibles) |
| OS | macOS Darwin 24.5.0 |
| Architecture | Apple Silicon arm64 |

**✅ Infrastructure Complète et Opérationnelle** :

*Environnement de Base* :
- Python 3.13.5
- pip 25.1.1
- Git 2.50.1
- Homebrew 5.0.8
- LaTeX (TeX Live 2025) - pdflatex disponible

*Jupyter Ecosystem* :
- JupyterLab 4.5.1
- Notebook 7.5.1
- IPython 9.9.0
- ipykernel 7.1.0
- ipywidgets 8.1.8
- nbconvert 7.16.6

*Packages Scientifiques Python* :
- numpy 2.3.5
- scipy 1.16.3
- matplotlib 3.10.8
- pandas 2.3.3
- seaborn 0.13.2
- astropy 7.2.0
- astroquery 0.4.11
- photutils 2.3.0

*MCMC et Statistiques* :
- emcee 3.1.6
- corner 2.2.3
- dynesty 3.0.0
- arviz 0.23.0
- chainconsumer 1.3.0 (visualisation avancée des chaînes)
- statsmodels 0.14.6 (modèles statistiques)

*Performance et Tests* :
- numba 0.63.1 (JIT compilation)
- pytest 9.0.2
- h5py 3.15.1
- psutil 7.2.1 (monitoring système/mémoire)

**Capacité de Calcul** :
- ✅ MCMC standard (emcee) : Opérationnel
- ✅ Nested sampling (dynesty) : Opérationnel
- ✅ Compilation PDF LaTeX : Opérationnel
- ✅ Notebooks Jupyter interactifs : Opérationnel
- ✅ Accès données JWST (astroquery) : Opérationnel
- ✅ Accélération Numba : Opérationnel
- ✅ Visualisation chaînes (chainconsumer) : Opérationnel
- ✅ Monitoring mémoire (psutil) : Opérationnel

**Remarques** :
- Machine configurée pour analyses MCMC de complexité moyenne
- 24 GB RAM suffisant pour la plupart des analyses cosmologiques
- Puce M4 offre excellentes performances mono/multi-thread
- Pas de GPU dédié (utilisation CPU pour calculs)

**Historique des Modifications** :

| Date | Heure UTC | Modification | Réversibilité |
|------|-----------|--------------|---------------|
| 2026-01-05 | 19:00 | Installation initiale: Python, Jupyter, packages scientifiques de base | Commit `3aa4199` |
| 2026-01-05 | 19:30 | Ajout packages MCMC: emcee, corner, dynesty, arviz | Commit `19ea2c1` |
| 2026-01-05 | 19:45 | Ajout INS-Statistiques.md (bonnes pratiques calculs intensifs) | Commit `19ea2c1` |
| 2026-01-05 | 20:00 | Ajout chainconsumer, statsmodels, psutil | Commit `903bc17` |
| 2026-01-05 | 20:15 | Mise en place historique des modifications | Commit `d09b974` |
| 2026-01-05 | 21:00 | Mise à jour requirements.txt avec versions minimales correctes | Commit `ffd2503` |

**Commandes de Réversibilité** :
```bash
# Voir l'état à un commit spécifique
git show <commit_hash>:JANUS-INSTRUCTIONS/INS-Infrastructure.md

# Revenir à un état précédent (créer une branche)
git checkout <commit_hash> -- JANUS-INSTRUCTIONS/INS-Infrastructure.md

# Lister tous les commits de ce fichier
git log --oneline JANUS-INSTRUCTIONS/INS-Infrastructure.md
```

---

### Instructions pour Nouvelles Machines

Lors de l'utilisation sur une nouvelle machine, documenter ici:

#### Machine: [NOM-MACHINE] - [Date]

**Système** : [OS, Version, Architecture]

**Installé** :
- [ ] Python 3.10+ (`python3 --version`)
- [ ] pip (`pip --version`)
- [ ] Environnement virtuel créé
- [ ] Jupyter (`jupyter --version`)
- [ ] Packages scientifiques (numpy, scipy, matplotlib, astropy)
- [ ] MCMC packages (emcee, corner, dynesty)
- [ ] LaTeX (`pdflatex --version`)
- [ ] Git (`git --version`)

**Configuration** :
```bash
# Cloner le projet
git clone https://github.com/PGPLF/JANUS.git
cd JANUS

# Créer environnement
python3 -m venv janus_env
source janus_env/bin/activate  # ou janus_env\Scripts\activate sur Windows

# Installer packages
pip install -r requirements.txt

# Vérifier installation
python3 verify_installation.py
```

**Notes spécifiques** :
- [Ajouter notes spécifiques à la machine]

---
