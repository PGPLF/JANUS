# Rapport d'Audit - Phase 3 v2.0
**Date**: 2026-01-07
**Version**: 1.0
**Statut**: AUDIT COMPLET - PROBLÈMES CRITIQUES IDENTIFIÉS

---

## Résumé Exécutif

L'audit de la Phase 3 v2.0 a révélé **plusieurs problèmes critiques** qui doivent être corrigés avant de passer à la Phase 4. Les résultats publiés dans RPT_PHASE3_v2.md contiennent des erreurs significatives.

| Composant | Statut | Sévérité |
|-----------|--------|----------|
| Phase 3.0 - Vérification données | PASS | - |
| Phase 3.1 - Statistiques descriptives | PASS | - |
| Phase 3.2 - MCMC JANUS | **FAIL** | **CRITIQUE** |
| Phase 3.3 - MCMC ΛCDM | WARNING | Modéré |
| Rapport RPT_PHASE3_v2.md | **FAIL** | **CRITIQUE** |
| Publication v2.0 | **FAIL** | **CRITIQUE** |

---

## 1. Audit Phase 3.0 - Vérification Données

### Résultat: PASS

**Points positifs:**
- Catalogue v2 correctement vérifié (6,609 sources)
- Purge des 66 entrées invalides (z > 15, z = 21.99)
- Sources clés présentes (MoM-z14, JADES-GS-z14-0/1)
- Aucun placeholder détecté

**Recommandations mineures:**
- Documenter les sources z >= 14 spectroscopiques dans le rapport (actuellement listées uniquement les photométriques z=15.00)

---

## 2. Audit Phase 3.1 - Statistiques Descriptives

### Résultat: PASS

**Points positifs:**
- 5 figures générées correctement
- Distribution redshift claire (spec vs phot)
- UV LF et SMF par bin de redshift

**Recommandations:**
- Ajouter incertitudes sur les distributions
- Inclure ligne ΛCDM théorique dans fig5 (déjà fait)

---

## 3. Audit Phase 3.2 - MCMC JANUS

### Résultat: FAIL - CRITIQUE

#### Problème 1: Équation JANUS incorrecte

**Constat:** Le script `phase3_complete_v2.py` implémente une équation JANUS **INCORRECTE**:

```python
# CODE ACTUEL (FAUX)
H(z) = H0 * sqrt(Omega_+ * (1+z)^3 + Omega_- * (1+z)^6 + Omega_Lambda)
```

**Équation théorique correcte** (JANUS_PREDICTIONS.md, ligne 37-39):
```
H²(z) = H0² [ Ω+ (1+z)³ + Ωk (1+z)² + χ|Ω-| (1+z)³ (1 + κ√(|Ω-|/Ω+)) ]
```

**Impact:**
- Le terme `(1+z)^6` fait diverger H(z) à haut redshift
- Les âges calculés sont **5763 Myr trop courts** à z=0
- Les paramètres best-fit (Ω- = 0.128) sont physiquement irréalistes

#### Problème 2: Module validé non utilisé

**Constat:** Le script `phase3_complete_v2.py` définit sa propre classe `JANUSCosmology` au lieu d'utiliser le module validé `src/cosmology/janus.py`.

**Preuve:**
```bash
# phase3_complete_v2.py - Ligne 54-69
class JANUSCosmology:
    def hubble_parameter(self, z):
        return self.H0 * np.sqrt(
            self.Omega_plus * (1 + z)**3 +
            self.Omega_minus * (1 + z)**6 +  # FAUX!
            self.Omega_Lambda
        )
```

#### Problème 3: Bug dans module validé

**Constat:** Le module `src/cosmology/janus.py` a aussi un bug dans la conversion d'unités:

```python
# Ligne 201 - FAUX
t_Gyr = t_Mpc * MPC_TO_KM / (C_LIGHT * GYR_TO_S * 1e9)
                                              ^^^^
# Facteur 1e9 en trop!
```

**Impact:** Ages 1 milliard de fois trop petits (retourne 0.000 Gyr)

#### Problème 4: Convergence MCMC insuffisante

| Diagnostic | Valeur | Seuil | Statut |
|------------|--------|-------|--------|
| Acceptance rate | 0.39 | 0.2-0.5 | OK |
| R-hat max | 1.61 | < 1.1 | **FAIL** |
| N_eff | ~250 | > 1000 | **FAIL** |

**Impact:** Paramètres best-fit non fiables, incertitudes sous-estimées.

---

## 4. Audit Phase 3.3 - MCMC ΛCDM

### Résultat: WARNING

**Points positifs:**
- Équation ΛCDM correcte
- Acceptance rate bon (0.45)

**Problèmes:**
- R-hat = 1.41 (> 1.1) - convergence insuffisante
- Incertitudes très larges (H0 ± 15 km/s/Mpc)

---

## 5. Audit Rapport RPT_PHASE3_v2.md

### Résultat: FAIL - CRITIQUE

#### Erreur 1: Âges de l'univers incorrects

**Valeurs dans le rapport:**
| z | JANUS (Gyr) | LCDM (Gyr) |
|---|-------------|------------|
| z=8 | **0.017** | 0.574 |
| z=10 | **0.009** | 0.425 |

**Problème:** JANUS devrait donner PLUS de temps que ΛCDM, pas moins!

**Valeurs attendues (doc théorique):**
| z | JANUS (Gyr) | LCDM (Gyr) |
|---|-------------|------------|
| z=8 | ~0.8-1.0 | 0.64 |
| z=10 | ~0.6-0.8 | 0.47 |

#### Erreur 2: Verdict incohérent

Le rapport conclut "JANUS predicts 80-110 Myr more cosmic time" mais les données montrent le contraire (-557 Myr à z=8).

---

## 6. Audit Publication v2.0

### Résultat: FAIL - CRITIQUE

La publication `JWST_HighZ_v2.0.pdf` hérite des mêmes erreurs:
- Âges JANUS incorrects dans Table 5
- Best-fit parameters non fiables
- Conclusions invalides

**Action requise:** Ne pas diffuser cette publication.

---

## 7. Corrections Requises Avant Phase 4

### Priorité CRITIQUE (bloquer Phase 4)

1. **Corriger équation JANUS dans phase3_complete_v2.py**
   - Utiliser le module validé `src/cosmology/janus.py`
   - Ou corriger l'équation inline

2. **Corriger bug unités dans src/cosmology/janus.py**
   - Ligne 201: supprimer le facteur `1e9`

3. **Re-exécuter MCMC avec plus d'itérations**
   - Minimum 2000 steps (actuellement 500)
   - Vérifier R-hat < 1.1

4. **Régénérer rapport et publication**
   - Avec valeurs correctes

### Priorité HAUTE

5. **Ajouter contrainte sur âge t(z=0)**
   - Prior ou likelihood penalty si t(z=0) ≠ 13.8 ± 0.5 Gyr

6. **Resserrer priors JANUS**
   - Ω- < 0.1 (actuellement 0.0-0.3)

### Priorité MOYENNE

7. **Utiliser nested sampling (dynesty)**
   - Meilleure exploration de l'espace des paramètres
   - Evidence ratio pour comparaison de modèles

---

## 8. Recommandation

**BLOQUER LE PASSAGE À LA PHASE 4** jusqu'à correction des problèmes critiques.

Temps estimé pour corrections: 2-3 heures de calcul + validation

---

## 9. Annexe: Tests de Validation

### Test âge univers avec paramètres par défaut

```
JANUS (H0=70, Ω+=0.30, Ω-=0.05):
  t(z=0) = 11.25 Gyr  (attendu: ~13.8 Gyr)
  t(z=8) = 0.565 Gyr  (attendu: 0.8-1.0 Gyr)

ΛCDM (H0=67.4, Ω_m=0.315):
  t(z=0) = 13.79 Gyr  ✓
  t(z=8) = 0.636 Gyr  ✓
```

### Diagnostic du problème

Le modèle JANUS avec l'équation documentée (couplage bimétrique) donne des âges **INFÉRIEURS** à ΛCDM, contrairement aux prédictions attendues.

**Hypothèse:** L'équation dans JANUS_PREDICTIONS.md ne correspond peut-être pas au modèle JANUS publié par Petit et al.

**Action recommandée:** Vérifier avec les équations originales des publications Petit (EPJ-C 2024, hal-03427072).

---

*Rapport généré par audit automatique*
*VAL-Galaxies_primordiales - Phase 3 Audit*
