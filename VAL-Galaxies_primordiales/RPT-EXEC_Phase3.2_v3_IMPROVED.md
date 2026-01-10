# Rapport d'Execution - Phase 3.2 AMELIOREE
## Ajustement MCMC avec Convergence Optimisee

**Date d'execution** : 10 Janvier 2026 - 12:32 UTC
**Version** : 3.0 (Improved)
**Reference** : PLAN.md - Phase 3.2
**Statut** : COMPLETE - CONVERGENCE ATTEINTE

---

## Resume Executif

### Amelioration de la Convergence

| Metrique | Version 2.0 | Version 3.0 | Amelioration |
|----------|-------------|-------------|--------------|
| N walkers | 64 | **128** | x2 |
| N steps | 2,000 | **5,000** | x2.5 |
| Burn-in | 1,000 | **2,500** | x2.5 |
| R-hat JANUS | 1.170 | **1.059** | OK |
| R-hat LCDM | 1.116 | **1.040** | OK |

### Resultats Principaux

| Metrique | JANUS | LCDM | Delta |
|----------|-------|------|-------|
| chi2 | 1508.33 | 1508.35 | -0.01 |
| BIC | 1530.16 | 1526.53 | **+3.62** |
| AIC | 1520.33 | 1518.35 | +1.99 |
| R-hat max | **1.059** | **1.040** | - |

**Verdict** : **INCONCLUSIF** (ΔBIC = +3.62)

**Convergence** : **ATTEINTE** (R-hat < 1.1 pour les deux modeles)

---

## 1. Configuration MCMC Amelioree

### 1.1 Parametres

| Parametre | Avant | Apres | Justification |
|-----------|-------|-------|---------------|
| N walkers | 64 | **128** | Meilleure exploration de l'espace |
| N steps | 2,000 | **5,000** | Plus de temps pour converger |
| Burn-in | 1,000 | **2,500** | 50% des steps |
| Algorithme | emcee | emcee | Inchange |

### 1.2 Temps d'Execution

| Modele | Temps |
|--------|-------|
| JANUS (6 params) | ~3 minutes |
| LCDM (5 params) | ~3 minutes |
| **Total** | **~6 minutes** |

---

## 2. Resultats JANUS

### 2.1 Parametres Best-Fit

| Parametre | Mediane | sigma | Unite |
|-----------|---------|-------|-------|
| H0 | 75.30 | 17.10 | km/s/Mpc |
| Omega_+ | 0.465 | 0.249 | - |
| Omega_- | 0.137 | 0.100 | - |
| log(phi*) | -4.515 | 0.098 | log(Mpc^-3) |
| M* | -22.84 | 0.250 | mag |
| alpha | -1.604 | 0.026 | - |

### 2.2 Diagnostics de Convergence

| Parametre | R-hat | Statut |
|-----------|-------|--------|
| H0 | 1.056 | OK |
| Omega_+ | 1.053 | OK |
| Omega_- | 1.059 | OK |
| log(phi*) | 1.056 | OK |
| M* | 1.055 | OK |
| alpha | 1.052 | OK |
| **Maximum** | **1.059** | **OK** |

- **Taux d'acceptation** : 0.381 (cible: 0.2-0.5) OK

### 2.3 Qualite de l'Ajustement

| Metrique | Valeur |
|----------|--------|
| chi2 | 1508.33 |
| chi2 reduit | 47.14 |
| BIC | 1530.16 |
| AIC | 1520.33 |

---

## 3. Resultats LCDM

### 3.1 Parametres Best-Fit

| Parametre | Mediane | sigma | Unite |
|-----------|---------|-------|-------|
| H0 | 75.47 | 17.07 | km/s/Mpc |
| Omega_m | 0.356 | 0.169 | - |
| log(phi*) | -4.519 | 0.097 | log(Mpc^-3) |
| M* | -22.84 | 0.248 | mag |
| alpha | -1.605 | 0.026 | - |

### 3.2 Diagnostics de Convergence

| Parametre | R-hat | Statut |
|-----------|-------|--------|
| H0 | 1.037 | OK |
| Omega_m | 1.040 | OK |
| log(phi*) | 1.034 | OK |
| M* | 1.037 | OK |
| alpha | 1.033 | OK |
| **Maximum** | **1.040** | **OK** |

- **Taux d'acceptation** : 0.454 (cible: 0.2-0.5) OK

### 3.3 Qualite de l'Ajustement

| Metrique | Valeur |
|----------|--------|
| chi2 | 1508.35 |
| chi2 reduit | 45.71 |
| BIC | 1526.53 |
| AIC | 1518.35 |

---

## 4. Comparaison des Modeles

### 4.1 Criteres d'Information

| Critere | JANUS | LCDM | Delta | Interpretation |
|---------|-------|------|-------|----------------|
| chi2 | 1508.33 | 1508.35 | -0.01 | Identiques |
| BIC | 1530.16 | 1526.53 | **+3.62** | Inconclusif |
| AIC | 1520.33 | 1518.35 | +1.99 | Inconclusif |

### 4.2 Interpretation

| Delta BIC | Evidence |
|-----------|----------|
| < -10 | Forte evidence pour JANUS |
| -10 a -6 | Evidence positive pour JANUS |
| **-6 a +6** | **INCONCLUSIF** (cas actuel) |
| +6 a +10 | Evidence positive pour LCDM |
| > +10 | Forte evidence pour LCDM |

### 4.3 Comparaison Age de l'Univers

| Redshift | JANUS (Gyr) | LCDM (Gyr) | Delta (Myr) |
|----------|-------------|------------|-------------|
| z = 0 | 9.96 | 12.04 | **-2,075** |
| z = 8 | 0.43 | 0.54 | -106 |
| z = 10 | 0.32 | 0.40 | -77 |
| z = 12 | 0.25 | 0.31 | -59 |
| z = 14 | 0.20 | 0.25 | -47 |

---

## 5. Comparaison v2.0 vs v3.0

### 5.1 Amelioration Convergence

| Modele | R-hat v2.0 | R-hat v3.0 | Amelioration |
|--------|------------|------------|--------------|
| JANUS | 1.170 | **1.059** | -9.5% |
| LCDM | 1.116 | **1.040** | -6.8% |

### 5.2 Stabilite des Resultats

| Parametre | v2.0 | v3.0 | Ecart |
|-----------|------|------|-------|
| JANUS H0 | 75.67 | 75.30 | -0.5% |
| JANUS Omega_+ | 0.491 | 0.465 | -5.3% |
| LCDM H0 | 75.41 | 75.47 | +0.1% |
| LCDM Omega_m | 0.354 | 0.356 | +0.6% |
| ΔBIC | +3.72 | +3.62 | -2.7% |

**Conclusion** : Les resultats sont stables entre v2.0 et v3.0, confirmant la robustesse des conclusions.

---

## 6. Fichiers Generes

### 6.1 Resultats

| Fichier | Description |
|---------|-------------|
| `results/v3_improved/phase3_improved_results.json` | Resultats JSON complets |
| `results/v3_improved/mcmc/janus_improved.h5` | Chaines MCMC JANUS (128x5000) |
| `results/v3_improved/mcmc/lcdm_improved.h5` | Chaines MCMC LCDM (128x5000) |

### 6.2 Figures

| Figure | Description |
|--------|-------------|
| `janus_corner_improved.pdf` | Corner plot JANUS |
| `janus_trace_improved.pdf` | Trace plot convergence JANUS |
| `lcdm_corner_improved.pdf` | Corner plot LCDM |
| `lcdm_trace_improved.pdf` | Trace plot convergence LCDM |

---

## 7. Conclusions

### 7.1 Convergence

**OBJECTIF ATTEINT** : R-hat < 1.1 pour tous les parametres des deux modeles.

| Critere | JANUS | LCDM | Statut |
|---------|-------|------|--------|
| R-hat < 1.1 | 1.059 | 1.040 | OK |
| Acceptance 0.2-0.5 | 0.381 | 0.454 | OK |

### 7.2 Resultats Scientifiques

1. **Chi2 identiques** : Les deux modeles reproduisent egalement les observations UV LF
2. **BIC inconclusif** : ΔBIC = +3.62 ne permet pas de discriminer
3. **Resultats stables** : Coherence entre v2.0 et v3.0

### 7.3 Probleme Theorique (Inchange)

JANUS predit toujours **MOINS de temps cosmique** que LCDM :
- Age JANUS (z=0) : 9.96 Gyr vs LCDM : 12.04 Gyr
- Incoherence avec les predictions theoriques documentees

### 7.4 Recommandations

- [x] Convergence MCMC atteinte (R-hat < 1.1)
- [ ] Clarification theorique toujours requise
- [ ] Phase 4 en attente

---

## 8. Statut Final

| Composant | Statut |
|-----------|--------|
| MCMC JANUS (128 walkers, 5000 steps) | COMPLETE |
| MCMC LCDM (128 walkers, 5000 steps) | COMPLETE |
| Convergence JANUS (R-hat = 1.059) | **OK** |
| Convergence LCDM (R-hat = 1.040) | **OK** |
| Comparaison modeles | INCONCLUSIF |
| Figures et rapports | COMPLETE |

**PHASE 3.2 AMELIOREE** : **COMPLETE - CONVERGENCE ATTEINTE**

---

**Rapport genere le** : 10 Janvier 2026 - 12:35 UTC
**Script** : `run_phase3_improved.py`
**Version** : 3.0 (Improved)
