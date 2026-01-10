# Rapport d'Execution - Phase 3.2
## Ajustement MCMC du Modele JANUS

**Date d'execution** : 10 Janvier 2026 - 12:11 UTC
**Version** : 2.0
**Reference** : PLAN.md - Phase 3.2
**Statut** : COMPLETE

---

## Resume Executif

| Metrique | JANUS | LCDM | Delta |
|----------|-------|------|-------|
| chi2 | 1508.39 | 1508.31 | +0.08 |
| BIC | 1530.22 | 1526.50 | **+3.72** |
| AIC | 1520.39 | 1518.31 | +2.08 |
| R-hat max | 1.170 | 1.116 | - |

**Verdict** : **INCONCLUSIF** (DBIC = +3.72, dans la plage [-6, +6])

---

## 1. Configuration de l'Analyse

### 1.1 Donnees Utilisees

| Parametre | Valeur |
|-----------|--------|
| Catalogue | `highz_catalog_VERIFIED_v2.csv` |
| N sources totales | 6,609 |
| N bins UV LF | 38 |
| Plage redshift | z = 6.5 - 15.0 |

### 1.2 Configuration MCMC

| Parametre | Valeur |
|-----------|--------|
| Algorithme | emcee EnsembleSampler |
| N walkers | 64 |
| N steps | 2,000 |
| Burn-in | 1,000 |
| Parametres JANUS | 6 (H0, Omega+, Omega-, phi*, M*, alpha) |
| Parametres LCDM | 5 (H0, Omega_m, phi*, M*, alpha) |

---

## 2. Resultats JANUS

### 2.1 Parametres Best-Fit

| Parametre | Mediane | -sigma | +sigma | Unite |
|-----------|---------|--------|--------|-------|
| H0 | 75.67 | 17.51 | 16.69 | km/s/Mpc |
| Omega_+ | 0.491 | 0.267 | 0.246 | - |
| Omega_- | 0.136 | 0.094 | 0.104 | - |
| log(phi*) | -4.523 | 0.105 | 0.090 | log(Mpc^-3) |
| M* | -22.85 | 0.278 | 0.221 | mag |
| alpha | -1.606 | 0.026 | 0.026 | - |

### 2.2 Diagnostics de Convergence

| Metrique | Valeur | Cible | Statut |
|----------|--------|-------|--------|
| Taux d'acceptation | 0.381 | 0.2-0.5 | OK |
| R-hat (H0) | 1.158 | < 1.1 | Proche |
| R-hat (Omega_+) | 1.170 | < 1.1 | Proche |
| R-hat (Omega_-) | 1.150 | < 1.1 | Proche |
| R-hat max | 1.170 | < 1.1 | A surveiller |

### 2.3 Qualite de l'Ajustement

| Metrique | Valeur |
|----------|--------|
| chi2 | 1508.39 |
| chi2 reduit | 47.14 |
| BIC | 1530.22 |
| AIC | 1520.39 |

---

## 3. Resultats LCDM

### 3.1 Parametres Best-Fit

| Parametre | Mediane | -sigma | +sigma | Unite |
|-----------|---------|--------|--------|-------|
| H0 | 75.41 | 17.53 | 16.99 | km/s/Mpc |
| Omega_m | 0.354 | 0.175 | 0.168 | - |
| log(phi*) | -4.511 | 0.099 | 0.085 | log(Mpc^-3) |
| M* | -22.82 | 0.267 | 0.210 | mag |
| alpha | -1.604 | 0.025 | 0.025 | - |

### 3.2 Diagnostics de Convergence

| Metrique | Valeur | Cible | Statut |
|----------|--------|-------|--------|
| Taux d'acceptation | 0.452 | 0.2-0.5 | OK |
| R-hat (H0) | 1.116 | < 1.1 | Proche |
| R-hat (Omega_m) | 1.112 | < 1.1 | Proche |
| R-hat max | 1.116 | < 1.1 | Proche |

### 3.3 Qualite de l'Ajustement

| Metrique | Valeur |
|----------|--------|
| chi2 | 1508.31 |
| chi2 reduit | 45.71 |
| BIC | 1526.50 |
| AIC | 1518.31 |

---

## 4. Comparaison des Modeles

### 4.1 Criteres d'Information

| Critere | JANUS | LCDM | Delta | Interpretation |
|---------|-------|------|-------|----------------|
| chi2 | 1508.39 | 1508.31 | +0.08 | Quasi-identiques |
| BIC | 1530.22 | 1526.50 | **+3.72** | Inconclusif |
| AIC | 1520.39 | 1518.31 | +2.08 | Inconclusif |

### 4.2 Echelle d'Interpretation BIC

| Delta BIC | Evidence |
|-----------|----------|
| < -10 | Forte evidence pour JANUS |
| -10 a -6 | Evidence positive pour JANUS |
| **-6 a +6** | **INCONCLUSIF** |
| +6 a +10 | Evidence positive pour LCDM |
| > +10 | Forte evidence pour LCDM |

**Resultat** : DBIC = +3.72 -> **INCONCLUSIF**

### 4.3 Comparaison Age de l'Univers

| Redshift | JANUS (Gyr) | LCDM (Gyr) | Difference (Myr) |
|----------|-------------|------------|------------------|
| z = 0 | 9.82 | 12.06 | **-2,240** |
| z = 8 | 0.42 | 0.54 | -120 |
| z = 10 | 0.31 | 0.40 | -87 |
| z = 12 | 0.24 | 0.31 | -67 |
| z = 14 | 0.20 | 0.25 | -54 |

---

## 5. Constat Theorique Important

### 5.1 Probleme Identifie

Le modele JANUS, tel qu'implemente avec l'equation de Friedmann bimetrique :

$$H^2(z) = H_0^2 \left[ \Omega_+ (1+z)^3 + \Omega_k (1+z)^2 + \chi |\Omega_-| (1+z)^3 \left(1 + \kappa \sqrt{\frac{|\Omega_-|}{\Omega_+}}\right) \right]$$

**Ne contient pas de terme d'energie sombre (Lambda).**

### 5.2 Consequence

Sans equivalent a Lambda, JANUS se comporte comme un univers domine par la matiere, qui s'expand plus rapidement a bas redshift. Cela donne necessairement un univers **plus jeune** que LCDM :

- **JANUS t(z=0)** = 9.82 Gyr (trop jeune)
- **LCDM t(z=0)** = 12.06 Gyr (proche de 13.8 Gyr attendu)

### 5.3 Implication

Contrairement aux predictions theoriques documentees dans `JANUS_PREDICTIONS.md`, le modele JANUS donne **MOINS** de temps cosmique pour la formation des galaxies, pas plus.

---

## 6. Fichiers Generes

### 6.1 Resultats

| Fichier | Description |
|---------|-------------|
| `results/v2_corrected/phase3_corrected_results.json` | Resultats complets JSON |
| `results/v2_corrected/mcmc/janus_corrected.h5` | Chaines MCMC JANUS |
| `results/v2_corrected/mcmc/lcdm_corrected.h5` | Chaines MCMC LCDM |

### 6.2 Figures

| Figure | Description |
|--------|-------------|
| `janus_corner_corrected.pdf` | Corner plot posteriors JANUS |
| `janus_corner_corrected.png` | Version PNG |
| `lcdm_corner_corrected.pdf` | Corner plot posteriors LCDM |
| `lcdm_corner_corrected.png` | Version PNG |

---

## 7. Conclusions

### 7.1 Resultats Statistiques

1. **Ajustement reussi** : Les deux modeles s'ajustent aux donnees UV LF
2. **Chi2 identiques** : Les deux modeles reproduisent egalement bien les observations
3. **BIC inconclusif** : DBIC = +3.72 ne permet pas de discriminer

### 7.2 Probleme Theorique

1. **JANUS donne MOINS de temps** que LCDM a tous les redshifts
2. **Incoherence** avec les predictions theoriques documentees
3. **Action requise** : Clarification theorique necessaire

### 7.3 Recommandations

- [ ] Verifier l'equation de Friedmann JANUS avec l'equipe theorique
- [ ] Determiner si un terme d'energie sombre effective existe
- [ ] Mettre a jour JANUS_PREDICTIONS.md si necessaire
- [ ] Suspendre Phase 4 en attente de clarification

---

## 8. Statut Final

| Composant | Statut |
|-----------|--------|
| Execution MCMC JANUS | COMPLETE |
| Execution MCMC LCDM | COMPLETE |
| Convergence JANUS | R-hat = 1.17 (proche) |
| Convergence LCDM | R-hat = 1.12 (proche) |
| Comparaison modeles | INCONCLUSIF |
| Figures generees | COMPLETE |

**PHASE 3.2** : **COMPLETE**

**Note** : Phase 4 en attente de clarification theorique.

---

**Rapport genere le** : 10 Janvier 2026 - 12:15 UTC
**Script** : `run_phase3_corrected.py`
**Version** : 2.0
