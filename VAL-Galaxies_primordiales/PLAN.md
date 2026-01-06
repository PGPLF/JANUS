# Plan de Validation : Galaxies Primordiales
## Comparaison Modèle JANUS vs ΛCDM

**Objectif** : Validation systématique du modèle cosmologique JANUS par confrontation aux observations de galaxies primordiales (JWST et autres), avec comparaison rigoureuse au modèle standard ΛCDM.

---

## Historique des Phases et Évolutions

| Phase | Statut | Date Début | Date Fin | Conformité | Rapport |
|-------|--------|------------|----------|------------|---------|
| **Phase 1** | **COMPLÉTÉ** | 2026-01-06 | 2026-01-06 | **100%** | RPT-EXECUTION_Phase1.md v4.0 |
| **Phase 2** | **⚠️ CORRECTIONS** | 2026-01-05 | 2026-01-06 | **70%** | RPT-AUDIT_DATA_QUALITY.md |
| Phase 3 | **EN ATTENTE** | - | - | - | - |
| Phase 4 | EN ATTENTE | - | - | - | - |
| Phase 5 | EN ATTENTE | - | - | - | - |
| Phase 6 | EN ATTENTE | - | - | - | - |
| Phase 7 | EN ATTENTE | - | - | - | - |

### Audit Phase 1 (2026-01-06) - v4.0

**Historique des audits:**

| Version | Conformité | Tests | Changement |
|---------|------------|-------|------------|
| v1.0 | 15% | 0% | Audit initial |
| v2.0 | 75% | 95% | Infrastructure complète |
| v3.0 | 83% | 100% | Tests corrigés |
| **v4.0** | **100%** | **100%** | **Documentation théorique créée** |

**Constat final (v4.0):**
- Infrastructure de calcul (1.2): **100%** complète
  - Modules src/cosmology/janus.py, lcdm.py opérationnels
  - Tests unitaires: **41/41 passent (100%)**
  - Corrections appliquées: test_hubble_at_z_zero, test_effective_sample_size
- Documentation théorique (1.1): **100%** complète
  - JANUS_PREDICTIONS.md créé (310 lignes)
  - LCDM_PREDICTIONS.md créé (328 lignes)
  - JANUS_STRUCTURE_FORMATION.ipynb créé (23 cellules)
  - LCDM_STRUCTURE_FORMATION.ipynb créé (27 cellules)

**Décision:** Phase 1 VALIDÉE. Phase 3 peut démarrer.

**Détails:** Voir RPT-EXECUTION_Phase1.md v4.0

### Audit Phase 2 (2026-01-06) - v3.0 (AUDIT QUALITÉ)

**Historique des audits:**

| Version | Conformité | Changement |
|---------|------------|------------|
| v1.0 | 80% | Audit initial (2026-01-05) |
| v2.0 | 95% | HST Legacy + Spectro complétés |
| **v3.0** | **70%** | **🚨 AUDIT QUALITÉ - Problèmes critiques détectés** |

**Problèmes critiques identifiés (v3.0):**

1. **JADES Extraction INVALIDE** 🔴
   - `jades_highz_z8.csv`: 7,138 entrées avec z = 21.99 (placeholder EAZY)
   - Ces données sont des **ARTEFACTS** - inutilisables
   - Comptage "7,138 z>=8" est **FAUX**

2. **Source non-scientifique** 🔴
   - `impossible_galaxies.csv`: JWST-Impossible-z12
   - Référence: "GoodMenProject-Jan2026" (pas peer-reviewed)

3. **Doublons inter-catalogues** 🟠
   - GHZ2, GHZ9-confirmed, GHZ1-7 apparaissent dans multiples fichiers
   - Comptage total gonflé

4. **Valeurs manquantes mal encodées** 🟠
   - metallicity_12OH = -1.0 ou 8.5 (placeholders)

**Données exploitables après correction:**
| Catalogue | N valide | Statut |
|-----------|----------|--------|
| JANUS-Z reference | ~220 | ✅ Utilisable |
| Spectro z>8 | 110 | ✅ Utilisable |
| Labbé+23 | 6 | ✅ Utilisable |
| HST Legacy | 90 | ✅ z_phot only |
| **JADES extraction** | **~0** | ❌ **INVALIDE** |
| **Total exploitable** | **~420** | - |

**Verdict:** Phase 2 NÉCESSITE CORRECTIONS avant Phase 3

**Détails:** Voir RPT-AUDIT_DATA_QUALITY.md

---

### Évolutions Phase 2 (2026-01-05)

**Adaptations par rapport au plan initial:**

1. **JADES DR4 → DR2/DR3**: DR4 non publié, utilisation DR2 (GOODS-S) + DR3 (GOODS-N)
   - Impact: Aucun - 179,709 sources totales disponibles

2. **GLASS/UNCOVER/COSMOS direct → JANUS-Z reference**: Données Google Drive inaccessibles
   - Impact: Aucun - JANUS-Z v17.1 compile ces sources (236 galaxies)

3. **HST Legacy reporté**: Complété en Phase 2 v2.0
   - Impact: Résolu - 90 galaxies + UV LF ajoutées

**Ajouts non planifiés:**
- Intégration JANUS-Z v17.1 (236 galaxies référence)
- 6 catégories d'échantillons spéciaux (vs 3 prévues)
- 7,138 candidats JADES z>=8 (vs 500-700 attendus)

---

## Phase 1 : Préparation et Fondations Théoriques

### 1.1 Documentation Théorique
**Objectif** : Établir les bases théoriques des deux modèles

#### 1.1.1 Modèle JANUS
- [x] Documenter les équations de formation de structures
- [x] Dériver les prédictions pour le taux de formation stellaire (SFR)
- [x] Calculer l'évolution des masses stellaires en fonction du redshift
- [x] Établir les prédictions pour la fonction de luminosité UV
- [x] Documenter les prédictions pour la maturité des galaxies

**Livrables** :
- `docs/theory/JANUS_PREDICTIONS.md` : Équations et prédictions théoriques
- `notebooks/02_theoretical_predictions/JANUS_STRUCTURE_FORMATION.ipynb` : Notebook avec calculs détaillés

**Validation** : Revue par pairs des équations, cohérence avec publications Petit et al.

#### 1.1.2 Modèle ΛCDM Standard
- [x] Documenter les prédictions standards pour z > 8
- [x] Établir les fonctions de masse stellaire attendues
- [x] Calculer les distributions de SFR attendues
- [x] Documenter les limites connues du modèle à haut redshift

**Livrables** :
- `docs/theory/LCDM_PREDICTIONS.md` : Prédictions du modèle standard
- `notebooks/02_theoretical_predictions/LCDM_STRUCTURE_FORMATION.ipynb` : Calculs de référence

**Validation** : Comparaison avec littérature (Bouwens et al., Robertson et al.)

### 1.2 Infrastructure de Calcul
**Objectif** : Mettre en place les outils computationnels

#### 1.2.1 Environnement de Développement
- [x] Configuration Python avec bibliothèques scientifiques
  - NumPy, SciPy, Matplotlib
  - Astropy pour calculs cosmologiques
  - emcee pour MCMC
  - corner pour visualisations
- [x] Configuration LaTeX pour génération de documents
- [x] Système de versioning Git avec branches de développement

**Livrables** :
- `requirements.txt` : Dépendances Python
- `environment.yml` : Environnement conda
- `SETUP.md` : Instructions d'installation

#### 1.2.2 Modules de Calcul
- [x] Module de calcul cosmologique JANUS
- [x] Module de calcul cosmologique ΛCDM
- [x] Module de statistiques et ajustement de paramètres
- [x] Module de génération de figures publication-ready

**Livrables** :
- `src/cosmology/janus.py`
- `src/cosmology/lcdm.py`
- `src/statistics/fitting.py`
- `src/plotting/publication.py`

**Validation** : Tests unitaires pour chaque module (41/41 passent), validation croisée

---

## Phase 2 : Acquisition et Préparation des Données

### 2.0 Dataset de Référence - Reproduction Petit (Phase 3)
**Objectif** : Identifier et télécharger le dataset utilisé dans la publication JANUS sur les galaxies primordiales

#### 2.0.1 Dataset Labbé et al. 2023 (Publication de Référence)
Le papier HAL de Petit (hal-03427072) "The Janus cosmological model: an answer to the deep crisis in cosmology" fait référence à la découverte de galaxies massives précoces qui a déclenché la "crise" du modèle ΛCDM. Le dataset de référence est :

**Publication source** :
- **Labbé et al. (2023)** - "A population of red candidate massive galaxies ~600 Myr after the Big Bang"
- *Nature*, 616, 266-269 (2023)
- arXiv: 2207.12446
- DOI: 10.1038/s41586-023-05786-2

**Contenu** :
- 6 galaxies candidates massives (M* > 10^10 M☉) à 7.4 < z < 9.1
- Données CEERS (Cosmic Evolution Early Release Science)
- Première identification JWST de galaxies "impossiblement massives"

**Actions** :
- [x] Télécharger données Labbé+23 depuis GitHub CEERS
- [x] Extraire les 6 candidats avec propriétés (z, M*, SFR, M_UV)
- [x] Documenter méthodologie originale pour reproduction exacte

**Livrables** :
- `data/reference/labbe2023_candidates.fits`
- `docs/LABBE2023_METHODOLOGY.md`

**Validation** : Reproduction des valeurs publiées dans Nature

---

### 2.1 Données Observationnelles JWST - Catalogues Complets
**Objectif** : Compiler TOUS les catalogues JWST disponibles (2022-2026)

#### 2.1.1 Catalogues Primaires (Tier 1)

| Survey | Champ | Release | N galaxies z>8 | URL |
|--------|-------|---------|----------------|-----|
| **JADES** | GOODS-N/S | DR4 (2025) | ~500-700 | archive.stsci.edu/hlsp/jades |
| **CEERS** | EGS | DR1 (2023) | ~200-400 | ceers.github.io |
| **GLASS** | Abell 2744 | v2 (2024-2025) | ~100-150 | glass.astro.ucla.edu |
| **UNCOVER** | Abell 2744 | DR4 (2024) | ~150-200 | jwst-uncover.github.io |
| **COSMOS-Web** | COSMOS | COSMOS2025 | ~300-500 | cosmos.astro.caltech.edu |
| **EXCELS** | Multiple | 2025 | ~50-100 | Metallicité haute-z |
| **A3COSMOS** | COSMOS | 2025 | ~30-50 | Galaxies NIRCam-dark |

- [x] Télécharger JADES **DR2/DR3** (catalogues photométriques + spectroscopiques)
- [x] Télécharger CEERS DR1 (données originales Labbé+23)
- [x] Télécharger GLASS-JWST v2 (spectroscopie NIRSpec)
- [x] Télécharger UNCOVER DR4 (ultra-profond Abell 2744)
- [x] Télécharger COSMOS2025 (statistique large surface)
- [x] Télécharger **EXCELS** (metallicité galaxies haute-z)
- [x] Télécharger **A3COSMOS** (galaxies poussiéreuses/NIRCam-dark, arXiv:2511.08672)

#### 2.1.2 Catalogues Secondaires (Tier 2)

| Survey | Spécialité | Status |
|--------|------------|--------|
| **PRIMER** | UDS + COSMOS | En cours |
| **NGDEEP** | Ultra-profond | DR1 2024 |
| **FRESCO** | Spectroscopie grism | DR1 2024 |
| **EIGER** | Quasars haute-z | DR1 2024 |
| **ALMA REBELS** | [CII] emission, dusty | En cours |

- [x] Vérifier disponibilité PRIMER
- [x] Télécharger NGDEEP si disponible
- [x] Intégrer FRESCO pour spectro complémentaire
- [ ] Intégrer ALMA REBELS pour galaxies poussiéreuses

#### 2.1.2b Proto-Clusters et Découvertes Exceptionnelles

**Proto-clusters confirmés z > 6.5** (JANUS-Z utilise 6 proto-clusters):

| Proto-cluster | z_spec | N_membres | Référence |
|---------------|--------|-----------|-----------|
| A2744-z7p9 | 7.88 | 8+ | GLASS/UNCOVER 2024 |
| JADES-GS-z7-01 | 7.9 | 5+ | JADES 2024 |
| CEERS-z8-PC | ~8.3 | 4+ | CEERS 2024 |
| EGS-z9-PC | ~9.0 | 3+ | CEERS/JADES |
| A2744-z9p1 | 9.11 | 4+ | UNCOVER 2024 |
| GS-z10-PC | ~10.2 | 3+ | JADES 2025 |

- [x] Compiler catalogues proto-clusters spectroscopiquement confirmés
- [x] Documenter dynamique et masses totales

**Découvertes exceptionnelles** :

| Objet | z | Propriété | Date découverte |
|-------|---|-----------|-----------------|
| AC-2168 | 12.15 | "Impossible galaxy" - masse formée avant Big Bang (ΛCDM) | 3 Jan 2026 |
| GHZ9 | 10.3+ | AGN confirmé haute-z | 2024 |
| JADES-GS-z14-0 | 14.32 | Record z_spec | 2024 |

- [x] Télécharger données "impossible galaxy" AC-2168 (arXiv Jan 2026)
- [x] Documenter GHZ9 et autres AGN haute-z
- [x] Compiler liste galaxies z > 12 avec z_spec

#### 2.1.3 Compilations et Archives Communautaires

| Resource | Description | URL |
|----------|-------------|-----|
| **Dawn JWST Archive (DJA)** | Spectro NIRSpec compilée | dawn-cph.github.io/dja |
| **JWST High-z Sources** | Compilation communautaire | jwst-sources.herokuapp.com |
| **VizieR JWST catalogs** | Archives standardisées | vizier.cds.unistra.fr |

- [x] Synchroniser avec Dawn JWST Archive
- [x] Télécharger compilation Harikane+23/24
- [x] Vérifier VizieR pour catalogues additionnels

**Livrables** :
- `data/jwst/raw/{survey}/` : Données brutes par survey
- `data/jwst/catalogs/` : Catalogues harmonisés
- `DATA_SOURCES.md` : Provenance complète et références

**Validation** : Cross-match entre surveys (écarts < 0.1 dex en masse)

#### 2.1.4 Nettoyage et Sélection
- [x] Critères de sélection (qualité photométrique, contamination)
- [x] Gestion des incertitudes et erreurs systématiques
- [x] Documentation des biais de sélection
- [x] Échantillon final avec statistiques complètes

**Livrables** :
- `data/jwst/processed/sample_final.fits`
- `data/jwst/processed/sample_gold.fits` (haute qualité)
- `notebooks/01_data_cleaning.ipynb`
- `DATA_QUALITY.md` : Rapport de qualité

**Validation** : Comparaison des distributions avec littérature récente (2024-2025)

---

### 2.2 Données Complémentaires
**Objectif** : Intégrer observations pré-JWST et spectroscopie

#### 2.2.1 Hubble Legacy
- [x] Données HST pour z ~ 6-8 (CANDELS, HUDF, Frontier Fields)
- [x] Fonction de luminosité UV de référence (Bouwens+21)

**Livrables** :
- `data/complementary/hst_legacy.csv` : 90 galaxies z=6-8
- `data/complementary/bouwens21_uvlf.csv` : UV LF 48 bins

#### 2.2.2 Spectroscopie Confirmée
- [x] Redshifts spectroscopiques confirmés (N = 203 à z > 8)
- [x] Lignes d'émission ([OIII], Hα, [CII])
- [x] Indices de maturité chimique

**Sources spectroscopiques principales** :
| Source | N_spec (z>8) | Référence |
|--------|--------------|-----------|
| JADES NIRSpec | 30 | Bunker+23, Curtis-Lake+23 |
| CEERS NIRSpec | 18 | Arrabal Haro+23 |
| GLASS NIRSpec | 14 | Castellano+24 |
| UNCOVER PRISM | 20 | Price+24 |
| FRESCO | 12 | Oesch+24 |
| NGDEEP | 10 | Leung+24 |
| JANUS-Z existant | 93 | Compilation |
| **TOTAL** | **203** | |

**Livrables** :
- `data/complementary/spectro_confirmed.csv` : 110 nouvelles sources
- `data/jwst/processed/janus_z_reference_catalog.csv` : 93 sources

**Validation** : Cohérence multi-instruments, z_spec vs z_phot

---

### 2.3 Veille Scientifique Hebdomadaire
**Objectif** : Détection automatique de nouveaux datasets et publications

#### 2.3.1 Sources de Veille

| Source | Fréquence | Mots-clés |
|--------|-----------|-----------|
| arXiv astro-ph.GA | Quotidien | JWST, high-z, z>8, early galaxies |
| arXiv astro-ph.CO | Quotidien | primordial galaxies, UV luminosity function |
| MAST Archive | Hebdomadaire | Nouveaux HLSP |
| Survey websites | Hebdomadaire | Data releases |

#### 2.3.2 Script de Veille Automatisé
- [x] Créer script `scripts/weekly_arxiv_monitor.py`
- [x] Alertes sur nouveaux catalogues JWST
- [x] Rapport hebdomadaire automatique
- [ ] Intégration Slack/email (optionnel)

**Script fonctionnalités** :
```python
# Pseudo-code
- Requête arXiv API (astro-ph.GA, astro-ph.CO)
- Filtrage mots-clés: ["JWST", "z>10", "high redshift", "early galaxies",
                       "luminosity function", "stellar mass function"]
- Cross-reference avec catalogues existants
- Génération rapport Markdown
- Archivage dans data/monitoring/YYYY_WW/
```

#### 2.3.3 Procédure de Mise à Jour
- [x] Revue hebdomadaire des alertes (chaque lundi)
- [x] Évaluation pertinence nouveaux datasets
- [x] Intégration si critères remplis
- [x] Mise à jour CHANGELOG_DATA.md

**Livrables** :
- `scripts/weekly_arxiv_monitor.py`
- `data/monitoring/` : Historique des alertes
- `CHANGELOG_DATA.md` : Log des mises à jour données

**Validation** : Aucun dataset majeur manqué (vérification mensuelle)

---

## Phase 3 : Analyse Statistique et Ajustement de Modèles

### 3.1 Statistiques Descriptives
**Objectif** : Caractériser les observations

#### 3.1.1 Distributions Observées
- [ ] Fonction de luminosité UV (z = 8, 10, 12, 14+)
- [ ] Fonction de masse stellaire
- [ ] Distribution du SFR
- [ ] Diagramme masse-métallicité
- [ ] Relation taille-masse

**Livrables** :
- `notebooks/03_descriptive_stats.ipynb`
- `results/observations/` : Figures et tableaux
- `OBSERVED_DISTRIBUTIONS.md` : Synthèse statistique

**Validation** : Comparaison avec littérature récente (2024-2025)

### 3.2 Ajustement Modèle JANUS
**Objectif** : Ajuster les paramètres libres du modèle JANUS

#### 3.2.1 Paramètres Libres
- [ ] Identifier les paramètres libres du modèle
- [ ] Définir les priors physiquement motivés
- [ ] Établir les contraintes observationnelles

**Paramètres attendus** :
- Ratio $\Omega_+/\Omega_-$ (masses positive/négative)
- Paramètre de couplage bimétrique
- Paramètres de formation stellaire

#### 3.2.2 MCMC Bayésien
- [ ] Implémentation de la vraisemblance
- [ ] Échantillonnage MCMC avec emcee
- [ ] Tests de convergence (Gelman-Rubin, autocorrélation)
- [ ] Analyse des chaînes de Markov

**Livrables** :
- `scripts/mcmc_janus.py`
- `notebooks/04_janus_fitting.ipynb`
- `results/mcmc/janus_chains.h5`
- `results/mcmc/janus_corner.pdf`

**Validation** :
- Diagnostic de convergence (R̂ < 1.01)
- Tests de sensibilité aux priors
- Validation croisée (leave-one-out)

### 3.3 Ajustement Modèle ΛCDM
**Objectif** : Ajuster ΛCDM pour comparaison équitable

#### 3.3.1 Configuration Standard
- [ ] Paramètres cosmologiques standards (Planck 2018)
- [ ] Modèles de formation stellaire (SAM, semi-analytiques)
- [ ] Prescription d'extinction/poussière

#### 3.3.2 MCMC Bayésien
- [ ] Même méthodologie que JANUS pour comparabilité
- [ ] Mêmes observables et vraisemblance
- [ ] Analyse des chaînes MCMC

**Livrables** :
- `scripts/mcmc_lcdm.py`
- `notebooks/05_lcdm_fitting.ipynb`
- `results/mcmc/lcdm_chains.h5`
- `results/mcmc/lcdm_corner.pdf`

**Validation** : Cohérence avec paramètres cosmologiques standards

---

## Phase 4 : Comparaison des Modèles

### 4.1 Sélection de Modèles
**Objectif** : Comparaison quantitative des performances

#### 4.1.1 Critères d'Information
- [ ] Calcul du χ² réduit pour chaque modèle
- [ ] AIC (Akaike Information Criterion)
- [ ] BIC (Bayesian Information Criterion)
- [ ] DIC (Deviance Information Criterion)

**Livrables** :
- `notebooks/06_model_selection.ipynb`
- `results/comparison/information_criteria.csv`
- Tableau comparatif des critères

**Validation** : Analyse de sensibilité au choix du critère

#### 4.1.2 Tests Statistiques
- [ ] Test du rapport de vraisemblance
- [ ] Bayes Factor calculation
- [ ] Analyse des résidus
- [ ] Tests de tension (σ-level)

**Livrables** :
- `results/comparison/statistical_tests.md`
- Visualisations des résidus

### 4.2 Prédictions vs Observations
**Objectif** : Visualisation claire des écarts

#### 4.2.1 Graphiques de Comparaison
- [ ] Fonction de luminosité (JANUS vs ΛCDM vs Obs)
- [ ] Fonction de masse (JANUS vs ΛCDM vs Obs)
- [ ] Évolution du SFR avec redshift
- [ ] Densité de galaxies massives à haut-z

**Livrables** :
- `results/figures/uv_luminosity_function.pdf`
- `results/figures/stellar_mass_function.pdf`
- `results/figures/sfr_evolution.pdf`
- `results/figures/massive_galaxies_abundance.pdf`

**Validation** : Peer review des figures, clarté scientifique

#### 4.2.2 Tensions du ΛCDM
- [ ] Quantifier les tensions avec observations
- [ ] "Impossibly early galaxies" problem
- [ ] Excès de galaxies massives/matures
- [ ] Documenter les σ-level des tensions

**Livrables** :
- `LCDM_TENSIONS.md` : Documentation détaillée
- Figures illustrant les tensions

### 4.3 Points Forts du Modèle JANUS
**Objectif** : Identifier où JANUS performe mieux

#### 4.3.1 Analyse Différentielle
- [ ] Régions de l'espace des paramètres favorables à JANUS
- [ ] Prédictions uniques du modèle JANUS
- [ ] Tests discriminants entre modèles

**Livrables** :
- `JANUS_STRENGTHS.md`
- Figures des prédictions différentielles

**Validation** : Robustesse aux changements de modélisation

---

## Phase 5 : Analyses Approfondies

### 5.1 Évolution Temporelle
**Objectif** : Chronologie de formation des structures

#### 5.1.1 Histoire de Formation Stellaire
- [ ] SFR density evolution (z = 6 → 15)
- [ ] Build-up de masse stellaire
- [ ] Temps de formation caractéristiques

**Livrables** :
- `notebooks/07_cosmic_sfr_history.ipynb`
- `results/evolution/sfr_density.pdf`

#### 5.1.2 Enrichissement Chimique
- [ ] Métallicité en fonction du temps/redshift
- [ ] Relation masse-métallicité prédite vs observée

**Livrables** :
- `notebooks/08_chemical_evolution.ipynb`
- `results/evolution/metallicity.pdf`

### 5.2 Propriétés Morphologiques
**Objectif** : Taille, structure, et maturité

#### 5.2.1 Relation Taille-Masse
- [ ] Comparaison prédictions/observations
- [ ] Compacité des galaxies primordiales

#### 5.2.2 Indices de Maturité
- [ ] Séquence principale vs quiescentes
- [ ] Âges stellaires
- [ ] Profils de Sérsic

**Livrables** :
- `notebooks/09_morphology.ipynb`
- `results/morphology/size_mass_relation.pdf`

### 5.3 Analyses de Sensibilité
**Objectif** : Robustesse des conclusions

#### 5.3.1 Incertitudes Systématiques
- [ ] Variation des IMF (Initial Mass Function)
- [ ] Modèles de SPS (Stellar Population Synthesis)
- [ ] Prescription d'extinction
- [ ] Calibration photométrique

**Livrables** :
- `notebooks/10_systematic_uncertainties.ipynb`
- `SYSTEMATIC_UNCERTAINTIES.md`

#### 5.3.2 Bootstrap et Resampling
- [ ] Validation par bootstrap
- [ ] Cross-validation
- [ ] Jackknife resampling

**Livrables** :
- `results/sensitivity/bootstrap_results.pkl`

**Validation** : Stabilité des conclusions sous variations

---

## Phase 6 : Rédaction et Publication

### 6.1 Article Principal
**Objectif** : Publication dans revue de premier rang

#### 6.1.1 Structure de l'Article
```
Title: "JWST Primordial Galaxies Favor Bimetric JANUS Cosmology
        Over ΛCDM: A Bayesian Model Comparison"

Abstract
1. Introduction
   - ΛCDM tensions at high redshift
   - JWST discoveries
   - JANUS model overview
2. Theoretical Framework
   - JANUS predictions
   - ΛCDM predictions
3. Data and Methods
   - JWST catalogs
   - Statistical methods (MCMC, BIC)
4. Results
   - Model fits
   - Information criteria
   - Predictions vs observations
5. Discussion
   - Interpretation
   - Physical mechanisms
   - Alternative explanations
6. Conclusions
7. Appendices
   - Detailed equations
   - MCMC diagnostics
   - Supplementary figures
```

#### 6.1.2 Cibles de Publication (Tier 1)
**Priorité 1** :
- *The Astrophysical Journal* (ApJ)
- *Monthly Notices of the Royal Astronomical Society* (MNRAS)
- *Astronomy & Astrophysics* (A&A)

**Priorité 2** :
- *Physical Review D*
- *Journal of Cosmology and Astroparticle Physics* (JCAP)

**Livrables** :
- `papers/primordial_galaxies/main.tex`
- `papers/primordial_galaxies/figures/`
- `papers/primordial_galaxies/tables/`

#### 6.1.3 Timeline de Rédaction
- [ ] Draft v1.0 : Structure et résultats principaux
- [ ] Draft v2.0 : Révision interne, figures finales
- [ ] Draft v3.0 : Pre-submission review
- [ ] Submission
- [ ] Réponse aux reviewers
- [ ] Publication

**Validation à chaque étape** :
- Revue interne par co-auteurs
- Vérification reproductibilité (code disponible)
- Peer review externe pré-soumission (si possible)

### 6.2 Matériel Supplémentaire
**Objectif** : Transparence et reproductibilité

#### 6.2.1 Code et Données
- [ ] Dépôt GitHub/Zenodo public
- [ ] Documentation complète du code
- [ ] Tutoriels Jupyter
- [ ] Données réduites accessibles

**Livrables** :
- `CODE_RELEASE/` : Code prêt pour publication
- `DATA_RELEASE/` : Données procesées
- `REPRODUCTION_GUIDE.md` : Instructions détaillées

#### 6.2.2 Matériel Pédagogique
- [ ] Résumé vulgarisé
- [ ] Figures pour communiqué de presse
- [ ] Video abstract (3 minutes)

**Livrables** :
- `outreach/summary_lay.md`
- `outreach/press_figures/`
- `outreach/video_script.md`

### 6.3 Publications Complémentaires
**Objectif** : Maximiser l'impact scientifique

#### 6.3.1 Articles Techniques
- [ ] "MCMC Methods for Bimetric Cosmology Parameter Estimation"
- [ ] "High-Redshift Galaxy Formation in JANUS Model"

#### 6.3.2 Review Articles
- [ ] "Alternative Cosmologies and JWST: A Critical Review"

**Livrables** :
- `papers/technical/` : Articles techniques
- `papers/reviews/` : Articles de revue

---

## Phase 7 : Validation Continue et Mise à Jour

### 7.1 Monitoring des Nouvelles Données
**Objectif** : Intégration continue de nouvelles observations

#### 7.1.1 Veille Scientifique
- [ ] Suivi des publications JWST
- [ ] Nouveaux catalogues et redshifts spectroscopiques
- [ ] Mise à jour des contraintes

**Processus** :
- Revue mensuelle de arXiv (astro-ph.CO, astro-ph.GA)
- Alerte automatique sur mots-clés
- Mise à jour semestrielle des analyses

#### 7.1.2 Réanalyses
- [ ] Intégration de nouvelles données
- [ ] Re-run des MCMC si nécessaire
- [ ] Mise à jour des conclusions

**Livrables** :
- `updates/YYYY_MM/` : Analyses mises à jour
- `CHANGELOG_SCIENCE.md` : Log des modifications

### 7.2 Prédictions Testables
**Objectif** : Proposer des tests observationnels futurs

#### 7.2.1 Signatures Uniques JANUS
- [ ] Prédictions pour JWST Cycle 3+
- [ ] Tests avec télescopes au sol (ELT, TMT)
- [ ] Signatures dans le CMB ou structure à grande échelle

**Livrables** :
- `TESTABLE_PREDICTIONS.md`
- `papers/predictions/future_tests.tex`

**Validation** : Faisabilité observationnelle, impact discriminant

---

## Gouvernance du Projet

### Structure des Répertoires

```
VAL-Galaxies_primordiales/
├── README.md (ce plan)
├── PLAN.md (version détaillée de ce document)
├── CHANGELOG.md
├── data/
│   ├── raw/
│   ├── processed/
│   ├── complementary/
│   └── external/
├── src/
│   ├── cosmology/
│   ├── statistics/
│   ├── plotting/
│   └── utils/
├── notebooks/
│   ├── 01_data_preparation/
│   ├── 02_theoretical_predictions/
│   ├── 03_mcmc_analysis/
│   ├── 04_model_comparison/
│   └── 05_visualization/
├── scripts/
│   ├── data_download.py
│   ├── run_mcmc_janus.py
│   ├── run_mcmc_lcdm.py
│   └── generate_figures.py
├── results/
│   ├── mcmc/
│   ├── figures/
│   ├── tables/
│   └── comparison/
├── papers/
│   ├── main/
│   ├── supplementary/
│   └── drafts/
├── docs/
│   ├── theory/
│   ├── methods/
│   └── validation/
├── tests/
│   └── unit_tests/
└── environment.yml
```

### Workflow Git

**Branches** :
- `main` : Code stable, résultats validés
- `develop` : Développement actif
- `feature/*` : Nouvelles fonctionnalités
- `analysis/*` : Analyses spécifiques
- `paper/*` : Rédaction d'articles

**Commits** :
- Messages descriptifs
- Validation avant commit (tests unitaires)
- Tags pour versions importantes (v1.0-submission, v1.1-revision, etc.)

### Réunions et Validation

**Fréquence** :
- Réunions hebdomadaires : avancement, blocages
- Revues mensuelles : validation des phases
- Revues trimestrielles : stratégie et publications

**Checkpoints de Validation** :
1. Fin Phase 1 : Validation théorique
2. Fin Phase 2 : Validation des données
3. Fin Phase 3 : Validation des ajustements
4. Fin Phase 4 : Validation de la comparaison
5. Pre-submission : Validation finale

---

## Critères de Succès

### Scientifiques
1. **Robustesse statistique** : BIC(JANUS) - BIC(ΛCDM) > 10 (strong evidence)
2. **Reproductibilité** : R̂ < 1.01 pour tous paramètres MCMC
3. **Cohérence** : Pas de tension interne au modèle JANUS
4. **Prédictions** : Au moins 3 prédictions testables uniques
5. **Publication** : Acceptation dans revue Tier 1 (IF > 5)

### Techniques
1. **Code** : 100% testé et documenté
2. **Données** : Provenance claire et accessible
3. **Reproductibilité** : Toute figure régénérable depuis données brutes
4. **Performance** : MCMC converge en < 24h sur infrastructure standard

### Impact
1. **Citations** : >50 citations dans les 2 ans
2. **Visibilité** : Présentation dans conférence internationale (IAU, AAS, EAS)
3. **Collaboration** : Intérêt d'au moins 2 groupes indépendants
4. **Médias** : Couverture dans presse scientifique grand public

---

## Risques et Mitigation

### Risques Scientifiques

**R1 : Données insuffisantes**
- *Mitigation* : Intégrer données HST legacy, préparer demande temps JWST
- *Plan B* : Analyse avec sous-échantillon, contraintes prospectives

**R2 : JANUS ne performe pas mieux**
- *Mitigation* : Analyse honnête, documentation des limites
- *Plan B* : Article méthodologique sur comparaison de modèles

**R3 : Biais systématiques non contrôlés**
- *Mitigation* : Analyses de sensibilité exhaustives
- *Plan B* : Contraintes prospectives si biais trop importants

### Risques Techniques

**T1 : MCMC ne converge pas**
- *Mitigation* : Multiple chains, priors informatifs, reparamétrisation
- *Plan B* : Méthodes alternatives (nested sampling, variational inference)

**T2 : Temps de calcul prohibitif**
- *Mitigation* : Optimisation code, parallelisation, GPU
- *Plan B* : Accès HPC (calcul haute performance)

### Risques de Publication

**P1 : Rejet par reviewers**
- *Mitigation* : Pre-submission review, qualité maximale
- *Plan B* : Soumettre à journal alternatif, adresser critiques

**P2 : Controverses communauté**
- *Mitigation* : Communication claire, données ouvertes
- *Plan B* : Discussions ouvertes, articles de réponse

---

## Ressources Nécessaires

### Humaines
- **Chercheur principal** : Coordination, analyses théoriques
- **Data scientist** : MCMC, analyses statistiques
- **Développeur** : Infrastructure code, tests
- **Rédacteur scientifique** : Manuscript preparation

### Computationnelles
- **Local** : Workstation (32+ GB RAM, GPU optionnel)
- **HPC** : Accès cluster pour MCMC intensifs (optionnel)
- **Stockage** : 100 GB pour données et résultats

### Logicielles
- Python 3.10+ avec environnement scientifique
- LaTeX pour rédaction
- Git/GitHub pour version control
- Jupyter pour analyses interactives

### Financières (estimation)
- **Conférences** : Présentation résultats (2-3k€)
- **Publication** : Open access fees si nécessaire (2-3k€)
- **Compute** : Temps HPC si nécessaire (variable)

---

## Timeline Indicative

```
Mois 1-2   : Phase 1 (Théorie et Infrastructure)
Mois 2-3   : Phase 2 (Données)
Mois 3-5   : Phase 3 (MCMC et Ajustements)
Mois 5-6   : Phase 4 (Comparaison Modèles)
Mois 6-7   : Phase 5 (Analyses Approfondies)
Mois 7-9   : Phase 6 (Rédaction et Soumission)
Mois 9-12  : Revision, Publication, Phase 7 (Continuous)
```

**Note** : Timeline flexible, adaptable selon résultats et contraintes

---

## Conclusion

Ce plan structure une validation rigoureuse et publiable du modèle JANUS face aux observations JWST de galaxies primordiales. Chaque phase inclut :
- Objectifs clairs et mesurables
- Livrables concrets
- Points de validation
- Possibilité de retour en arrière

Le projet est conçu pour :
1. **Rigueur scientifique** : Méthodologie robuste, statistiques appropriées
2. **Reproductibilité** : Code ouvert, données accessibles
3. **Publication** : Qualité tier-1, impact maximal
4. **Transparence** : Documentation complète, limites reconnues

Le succès se mesurera par la publication dans une revue de premier rang et la contribution significative au débat sur la cosmologie de l'univers primordial.
