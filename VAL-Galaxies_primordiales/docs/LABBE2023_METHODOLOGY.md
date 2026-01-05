# Méthodologie Labbé et al. (2023)
## Dataset de Référence pour Reproduction Phase 3

**Date**: 5 Janvier 2026
**Version**: 1.0

---

## 1. Publication Source

### Référence Complète
```
Labbé, I., van Dokkum, P., Nelson, E., et al. (2023)
"A population of red candidate massive galaxies ~600 Myr after the Big Bang"
Nature, 616, 266-269
DOI: 10.1038/s41586-023-05786-2
arXiv: 2207.12446
```

### Impact Scientifique
- **Citations**: >500 (Jan 2026)
- **Significance**: Première détection JWST de galaxies "impossiblement massives"
- **Implication**: Déclencheur de la "crise" du modèle ΛCDM à haut redshift

---

## 2. Données Utilisées

### 2.1 Observations
- **Instrument**: JWST NIRCam
- **Programme**: CEERS (Cosmic Evolution Early Release Science)
- **Champ**: Extended Groth Strip (EGS)
- **Bandes NIRCam**: F115W, F150W, F200W, F277W, F356W, F410M, F444W
- **Bandes HST**: F435W, F606W, F814W (archivées)

### 2.2 Fichier Source
```
Repository: github.com/ivolabbe/red-massive-candidates
Fichier: sample_revision3_2207.12446.ecsv
Format: ECSV (Enhanced CSV with metadata)
```

### 2.3 Contenu
| Colonne | Description | Unité |
|---------|-------------|-------|
| id | Identifiant CEERS | - |
| ra, dec | Coordonnées J2000 | deg |
| z | Redshift photométrique | - |
| zlo, zhi | Intervalle 68% | - |
| zxlo, zxhi | Intervalle 95% | - |
| mass | log(M*/Msun) | log Msun |
| masslo, masshi | Intervalle 68% masse | log Msun |
| chi2 | Qualité ajustement | - |
| fXXXw | Flux dans bande XXX | nJy |
| eXXXw | Erreur flux | nJy |

---

## 3. Méthodologie SED Fitting

### 3.1 Code Utilisé
- **EAZY**: Redshifts photométriques (Brammer+08)
- **Prospector**: Masses stellaires (Johnson+21)

### 3.2 Paramètres Prospector
```python
# Configuration SED fitting
IMF = 'Chabrier (2003)'
SFH = 'non-parametric'  # Flexible star formation history
Dust = 'Calzetti (2000)'
Metallicity = 'variable'  # 0.2 - 2.0 Zsun
Age_prior = 'uniform in log(age)'
```

### 3.3 Priors
| Paramètre | Prior | Plage |
|-----------|-------|-------|
| log(M*/Msun) | Uniform | 6 - 13 |
| log(Z/Zsun) | Uniform | -2 - 0.2 |
| log(age/yr) | Uniform | 6 - age_universe(z) |
| A_V | Uniform | 0 - 4 |
| z | P(z) from EAZY | - |

---

## 4. Critères de Sélection

### 4.1 Sélection Couleur
```
Critère "red": F277W - F444W > 0.7 mag
Critère "break": F150W - F200W < 0.5 mag  (Lyman break)
SNR > 5 dans F277W, F356W, F444W
```

### 4.2 Sélection Masse
```
log(M*/Msun) > 10.0
z_phot > 7.0
chi2 < 100 (bon ajustement)
```

### 4.3 Exclusions
- Sources avec solution AGN probable
- Sources avec contamination voisin
- Sources avec artefacts photométriques

---

## 5. Les 6 Candidats Massifs

### 5.1 Tableau Récapitulatif

| ID | z_phot | σ_z | log(M*/Msun) | σ_M | Note |
|----|--------|-----|--------------|-----|------|
| 11184 | 7.32 | +0.28/-0.35 | 10.18 | ±0.10 | - |
| 38094 | 7.48 | +0.04/-0.04 | 10.89 | ±0.09 | Plus massif |
| 2859 | 8.11 | +0.49/-1.50 | 10.03 | ±0.24 | Large incertitude z |
| 13050 | 8.14 | +0.45/-1.71 | 10.14 | ±0.29 | Large incertitude z |
| 14924 | 8.83 | +0.17/-0.09 | 10.02 | ±0.14 | z bien contraint |
| 35300 | 9.08 | +0.31/-0.38 | 10.40 | ±0.21 | Plus haut z |

### 5.2 Propriétés Dérivées

**Masses stellaires**:
- Plage: 10^10.0 - 10^10.9 Msun
- Moyenne: 10^10.3 Msun
- Ces masses sont 10-100x supérieures aux prédictions ΛCDM

**Redshifts**:
- Plage: 7.3 - 9.1
- Époque: 500-700 Myr après le Big Bang
- Confirmations spectro partielles (suivi 2023-2024)

---

## 6. Tension avec ΛCDM

### 6.1 Le Problème
Dans le modèle ΛCDM standard:
```
Masse halo max (z~8) ~ 10^11 Msun
Fraction baryonique ~ 0.16
Efficacité SF typique ~ 0.1-0.3
=> M* max théorique ~ 10^9 Msun
```

**Observé**: M* ~ 10^10-11 Msun
**Tension**: Facteur 10-100x

### 6.2 Explications Proposées (ΛCDM)
1. **Biais photométrique**: Surestimation des masses
2. **AGN cachés**: Contribution non-stellaire
3. **Poussière**: Extinction mal modélisée
4. **IMF différente**: Top-heavy à haute-z

### 6.3 Solution JANUS
Le modèle bimétrique JANUS prédit naturellement:
- Formation plus précoce des structures
- Masses stellaires plus élevées à haut-z
- Pas besoin de physique exotique

---

## 7. Suivi Spectroscopique

### 7.1 Confirmations (2023-2024)
| ID | z_spec | Instrument | Référence |
|----|--------|------------|-----------|
| 35300 | 9.08 | NIRSpec PRISM | Arrabal Haro+23 |
| 14924 | 8.88 | NIRSpec G395M | CEERS Team 2024 |

### 7.2 Révisions
Certaines sources ont été révisées à des z plus bas après spectroscopie.
L'échantillon "revision 3" intègre ces mises à jour.

---

## 8. Reproduction Phase 3

### 8.1 Objectif
Reproduire l'analyse Labbé+23 avec:
1. Mêmes données photométriques
2. Même méthodologie SED fitting
3. Comparer résultats ΛCDM vs JANUS

### 8.2 Étapes
1. ✅ Télécharger données GitHub
2. ✅ Extraire 6 candidats massifs
3. ⬜ Configurer Prospector avec paramètres originaux
4. ⬜ Calculer masses avec cosmologie ΛCDM
5. ⬜ Calculer masses avec cosmologie JANUS
6. ⬜ Comparer et quantifier différences

### 8.3 Fichiers Produits
```
data/reference/
├── labbe2023_sample.ecsv      # Échantillon complet (13 sources)
├── labbe2023_candidates.fits  # 6 candidats massifs
└── labbe2023_candidates.csv   # Format CSV
```

---

## 9. Références

1. Labbé, I., et al. (2023), Nature 616, 266
2. Brammer, G. B., et al. (2008), ApJ 686, 1503 (EAZY)
3. Johnson, B. D., et al. (2021), ApJS 254, 22 (Prospector)
4. Chabrier, G. (2003), PASP 115, 763 (IMF)
5. Calzetti, D., et al. (2000), ApJ 533, 682 (Dust)
6. Arrabal Haro, P., et al. (2023), Nature 622, 707

---

*Document VAL-Galaxies_primordiales - Méthodologie Labbé+23*
*5 Janvier 2026*
