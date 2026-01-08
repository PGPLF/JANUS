# Rapport d'Exécution - Phase 3 Corrigée
**Date**: 2026-01-08
**Version**: 2.1 (Corrigée)
**Statut**: COMPLÉTÉ - ANALYSE CORRIGÉE

---

## Résumé Exécutif

Phase 3 v2.1 a été ré-exécutée avec les corrections suivantes:
1. Bug de conversion d'unités corrigé dans `src/cosmology/janus.py`
2. Module JANUS validé importé dans `phase3_complete_v2.py` (remplace l'équation incorrecte)
3. MCMC exécuté avec 2000 steps (64 walkers) pour meilleure convergence

### Résultats Principaux

| Modèle | chi² | BIC | AIC | R-hat max |
|--------|------|-----|-----|-----------|
| JANUS | 1508.3 | 1530.2 | 1520.3 | 1.163 |
| ΛCDM | 1508.4 | 1526.6 | 1518.4 | 1.125 |
| **Δ** | -0.03 | +3.60 | +1.96 | - |

**Verdict**: Inconclusive (ΔBIC = +3.60)

---

## 1. Corrections Apportées

### 1.1 Bug d'Unités dans janus.py

**Avant** (ligne 209):
```python
t_Gyr = t_Mpc * MPC_TO_KM / C_LIGHT / GYR_TO_S
```

**Après** (corrigé):
```python
t_Gyr = t_Mpc * MPC_TO_KM / GYR_TO_S
```

**Impact**: La division par `C_LIGHT` (~300,000 km/s) rendait les âges 300,000× trop petits.

### 1.2 Équation JANUS Incorrecte

**Avant** (phase3_complete_v2.py ligne 92-96):
```python
H(z) = H0 * sqrt(Omega_plus * (1+z)^3 + Omega_minus * (1+z)^6 + Omega_Lambda)
```

**Après** (import du module validé):
```python
from cosmology.janus import JANUSCosmology  # Équation bimétrique correcte
```

### 1.3 MCMC Amélioré

| Paramètre | Avant | Après |
|-----------|-------|-------|
| Walkers | 32 | 64 |
| Steps | 500 | 2000 |
| Burn-in | 250 | 1000 |

---

## 2. Résultats JANUS

### 2.1 Paramètres Best-Fit

| Paramètre | Médiane | -σ | +σ |
|-----------|---------|-----|-----|
| H0 [km/s/Mpc] | 74.18 | 16.09 | 17.31 |
| Ω+ | 0.510 | 0.272 | 0.222 |
| Ω- | 0.149 | 0.102 | 0.101 |
| log(φ*) | -4.52 | 0.11 | 0.09 |
| M* [mag] | -22.84 | 0.29 | 0.22 |
| α | -1.60 | 0.03 | 0.03 |

### 2.2 Diagnostics de Convergence

- **Taux d'acceptation**: 0.383 (cible: 0.2-0.5) ✓
- **R-hat max**: 1.163 (cible: < 1.1) ⚠️
- **Chi²**: 1508.34
- **BIC**: 1530.17
- **AIC**: 1520.34

---

## 3. Résultats ΛCDM

### 3.1 Paramètres Best-Fit

| Paramètre | Médiane | -σ | +σ |
|-----------|---------|-----|-----|
| H0 [km/s/Mpc] | 75.86 | 17.34 | 16.31 |
| Ωm | 0.348 | 0.171 | 0.168 |
| log(φ*) | -4.52 | 0.11 | 0.09 |
| M* [mag] | -22.86 | 0.28 | 0.23 |
| α | -1.61 | 0.03 | 0.03 |

### 3.2 Diagnostics de Convergence

- **Taux d'acceptation**: 0.457 (cible: 0.2-0.5) ✓
- **R-hat max**: 1.125 (cible: < 1.1) ⚠️
- **Chi²**: 1508.38
- **BIC**: 1526.57
- **AIC**: 1518.38

---

## 4. Comparaison des Modèles

### 4.1 Critères d'Information

| Critère | Valeur | Interprétation |
|---------|--------|----------------|
| ΔBIC | +3.60 | Inconclusive (|Δ| < 6) |
| ΔAIC | +1.96 | Inconclusive |
| Δchi² | -0.03 | Quasiment identiques |

### 4.2 Âge de l'Univers

| z | JANUS (Gyr) | ΛCDM (Gyr) | Δt (Myr) |
|---|-------------|------------|----------|
| 0 | 9.98 | 12.03 | **-2049** |
| 8 | 0.42 | 0.54 | -120 |
| 10 | 0.31 | 0.40 | -88 |
| 12 | 0.24 | 0.31 | -68 |
| 14 | 0.20 | 0.25 | -54 |

---

## 5. Constat Critique: Incohérence Théorique

### 5.1 Problème Identifié

Le document `JANUS_PREDICTIONS.md` prédit que JANUS donne **PLUS** de temps cosmique que ΛCDM à chaque redshift. Cependant, l'équation de Friedmann JANUS documentée:

$$H^2(z) = H_0^2 \left[ \Omega_+ (1+z)^3 + \Omega_k (1+z)^2 + \chi |\Omega_-| (1+z)^3 \left(1 + \kappa \sqrt{\frac{|\Omega_-|}{\Omega_+}}\right) \right]$$

**Ne contient pas de terme d'énergie sombre (Λ)**.

### 5.2 Conséquence

Sans équivalent à Λ, le modèle JANUS se comporte comme un univers dominé par la matière, qui s'expand plus vite à bas redshift, donnant nécessairement un univers **plus jeune** qu'un modèle avec énergie sombre (ΛCDM).

### 5.3 Vérification Numérique

Avec paramètres par défaut (H0=70, Ω+=0.30, Ω-=0.05):
- JANUS t(z=0) = 11.25 Gyr (**pas 13.8 Gyr**)
- ΛCDM t(z=0) = 13.79 Gyr ✓

### 5.4 Recommandation

**Réviser le document théorique JANUS_PREDICTIONS.md** ou **ajouter un mécanisme d'énergie sombre effective** au modèle JANUS si les prédictions de "plus de temps cosmique" doivent être maintenues.

---

## 6. Fichiers Générés

### 6.1 Résultats

| Fichier | Description |
|---------|-------------|
| `results/v2_corrected/phase3_corrected_results.json` | Résultats complets JSON |
| `results/v2_corrected/mcmc/janus_corrected.h5` | Chaînes MCMC JANUS |
| `results/v2_corrected/mcmc/lcdm_corrected.h5` | Chaînes MCMC ΛCDM |

### 6.2 Figures

| Figure | Description |
|--------|-------------|
| `janus_corner_corrected.pdf` | Corner plot JANUS |
| `lcdm_corner_corrected.pdf` | Corner plot ΛCDM |

---

## 7. Conclusions

1. **Code corrigé**: Les bugs d'unités et d'équation ont été corrigés
2. **MCMC amélioré**: Convergence meilleure (R-hat proche de 1.1)
3. **Modèles équivalents**: ΔBIC ≈ 3.6 → pas de préférence statistique claire
4. **Problème théorique**: JANUS donne MOINS de temps que ΛCDM, contrairement aux prédictions

### Actions Requises

- [ ] Clarifier les prédictions théoriques JANUS avec l'équipe
- [ ] Vérifier si un terme d'énergie sombre effective existe dans le modèle JANUS complet
- [ ] Mettre à jour JANUS_PREDICTIONS.md si nécessaire

---

*Rapport généré par run_phase3_corrected.py*
*VAL-Galaxies_primordiales - Phase 3 Corrigée*
