# Plan de Validation : Galaxies Primordiales
## Comparaison Modèle JANUS vs ΛCDM

**Objectif** : Validation systématique du modèle cosmologique JANUS par confrontation aux observations de galaxies primordiales (JWST et autres), avec comparaison rigoureuse au modèle standard ΛCDM.

---

## Phase 1 : Préparation et Fondations Théoriques

### 1.1 Documentation Théorique
**Objectif** : Établir les bases théoriques des deux modèles

#### 1.1.1 Modèle JANUS
- [ ] Documenter les équations de formation de structures
- [ ] Dériver les prédictions pour le taux de formation stellaire (SFR)
- [ ] Calculer l'évolution des masses stellaires en fonction du redshift
- [ ] Établir les prédictions pour la fonction de luminosité UV
- [ ] Documenter les prédictions pour la maturité des galaxies

**Livrables** :
- `JANUS_PREDICTIONS.md` : Équations et prédictions théoriques
- `JANUS_STRUCTURE_FORMATION.ipynb` : Notebook avec calculs détaillés

**Validation** : Revue par pairs des équations, cohérence avec publications Petit et al.

#### 1.1.2 Modèle ΛCDM Standard
- [ ] Documenter les prédictions standards pour z > 8
- [ ] Établir les fonctions de masse stellaire attendues
- [ ] Calculer les distributions de SFR attendues
- [ ] Documenter les limites connues du modèle à haut redshift

**Livrables** :
- `LCDM_PREDICTIONS.md` : Prédictions du modèle standard
- `LCDM_STRUCTURE_FORMATION.ipynb` : Calculs de référence

**Validation** : Comparaison avec littérature (Bouwens et al., Robertson et al.)

### 1.2 Infrastructure de Calcul
**Objectif** : Mettre en place les outils computationnels

#### 1.2.1 Environnement de Développement
- [ ] Configuration Python avec bibliothèques scientifiques
  - NumPy, SciPy, Matplotlib
  - Astropy pour calculs cosmologiques
  - emcee pour MCMC
  - corner pour visualisations
- [ ] Configuration LaTeX pour génération de documents
- [ ] Système de versioning Git avec branches de développement

**Livrables** :
- `requirements.txt` : Dépendances Python
- `environment.yml` : Environnement conda
- `SETUP.md` : Instructions d'installation

#### 1.2.2 Modules de Calcul
- [ ] Module de calcul cosmologique JANUS
- [ ] Module de calcul cosmologique ΛCDM
- [ ] Module de statistiques et ajustement de paramètres
- [ ] Module de génération de figures publication-ready

**Livrables** :
- `src/cosmology/janus.py`
- `src/cosmology/lcdm.py`
- `src/statistics/fitting.py`
- `src/plotting/publication.py`

**Validation** : Tests unitaires pour chaque module, validation croisée

---

## Phase 2 : Acquisition et Préparation des Données

### 2.1 Données Observationnelles JWST
**Objectif** : Compiler et nettoyer les observations JWST

#### 2.1.1 Catalogues de Galaxies
- [ ] Télécharger catalogues JWST officiels
  - JADES (JWST Advanced Deep Extragalactic Survey)
  - CEERS (Cosmic Evolution Early Release Science)
  - GLASS (Grism Lens-Amplified Survey from Space)
- [ ] Compiler les galaxies à z > 8
- [ ] Extraire : masses stellaires, SFR, magnitudes UV, redshifts

**Livrables** :
- `data/jwst/raw/` : Données brutes
- `data/jwst/catalogs/` : Catalogues compilés
- `DATA_SOURCES.md` : Provenance et références

**Validation** : Vérification croisée avec publications sources

#### 2.1.2 Nettoyage et Sélection
- [ ] Critères de sélection (qualité photométrique, contamination)
- [ ] Gestion des incertitudes et erreurs systématiques
- [ ] Documentation des biais de sélection
- [ ] Échantillon final avec statistiques complètes

**Livrables** :
- `data/jwst/processed/sample_final.csv`
- `notebooks/01_data_cleaning.ipynb`
- `DATA_QUALITY.md` : Rapport de qualité

**Validation** : Comparaison des distributions avec littérature

### 2.2 Données Complémentaires
**Objectif** : Intégrer d'autres observations pertinentes

#### 2.2.1 Hubble Legacy
- [ ] Données HST pour z ~ 6-8 (overlap avec JWST)
- [ ] Fonction de luminosité UV de référence

#### 2.2.2 Spectroscopie
- [ ] Redshifts spectroscopiques confirmés
- [ ] Lignes d'émission ([OIII], Hα, [CII])
- [ ] Indices de maturité chimique

**Livrables** :
- `data/complementary/` : Données additionnelles
- `notebooks/02_complementary_data.ipynb`

**Validation** : Cohérence multi-instruments

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
