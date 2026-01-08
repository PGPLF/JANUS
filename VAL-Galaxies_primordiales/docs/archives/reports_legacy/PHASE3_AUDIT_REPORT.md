# Rapport d'Audit Phase 3 - Analyse Statistique

**Projet**: VAL-Galaxies_primordiales
**Date**: 2026-01-07
**Auditeur**: Claude Code
**Version**: 1.0

---

## Résumé Exécutif

| Composant | Status | Conformité |
|-----------|--------|------------|
| Phase 3.1 Statistiques Descriptives | ✅ COMPLÉTÉ | 100% |
| Phase 3.2 JANUS MCMC | ⚠️ CONVERGENCE INSUFFISANTE | 70% |
| Phase 3.3 ΛCDM MCMC | ⚠️ CONVERGENCE MARGINALE | 80% |
| **PHASE 3 GLOBALE** | ⚠️ **À CORRIGER** | **75%** |

**Problème critique**: Les chaînes MCMC n'ont pas convergé (R-hat > 1.1)

---

## 1. Phase 3.1 - Statistiques Descriptives

### 1.1 Status: ✅ COMPLÉTÉ (100%)

| Livrable | Fichier | Status |
|----------|---------|--------|
| UV Luminosity Function | fig1a_uv_luminosity_function.pdf | ✅ |
| Stellar Mass Function | fig2a_stellar_mass_function.pdf | ✅ |
| SFR Distribution | fig3a_sfr_distribution.pdf | ✅ |
| Size-Mass Relation | fig4a_size_mass_relation.pdf | ✅ |
| Redshift Distribution | fig5a_redshift_distribution.pdf | ✅ |
| Statistics Table | table1a_sample_statistics.tex | ✅ |

### 1.2 Catalogue Utilisé

| Version | Sources | z Range | Status |
|---------|---------|---------|--------|
| v1 | 6,672 | 6.50-21.99 | ⚠️ Contient z invalides |
| **v2** | **6,609** | **3.20-15.00** | ✅ **RECOMMANDÉ** |

**Distribution v2 par redshift**:
- z > 8: 1,384 sources
- z > 10: 400 sources
- z > 12: 79 sources
- z > 14: 20 sources (dont MoM-z14 spectro)

### 1.3 Verdict Phase 3.1

✅ **VALIDÉ** - Statistiques descriptives complètes sur données vérifiées

---

## 2. Phase 3.2 - Ajustement JANUS

### 2.1 Configuration MCMC

| Paramètre | Valeur |
|-----------|--------|
| Sampler | emcee |
| Walkers | 32 |
| Steps | 500 |
| Burn-in | 250 |
| Paramètres | 6 (H0, Ω+, Ω-, φ*, M*, α) |

### 2.2 Résultats Best-Fit

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| H0 | 78.8 ± 1.2 km/s/Mpc | Constante de Hubble |
| Ω+ | 0.47 ± 0.02 | Densité matière positive |
| Ω- | 0.03 ± 0.02 | Densité matière négative |
| φ*_0 | 3.56×10⁻⁴ Mpc⁻³ | Normalisation UV LF |
| M*_0 | -21.37 | Magnitude caractéristique |
| α_0 | -2.43 | Pente faint-end |

### 2.3 Diagnostics de Convergence

| Critère | Valeur | Seuil | Status |
|---------|--------|-------|--------|
| R-hat max | **1.341** | < 1.1 | ❌ **ÉCHEC** |
| R-hat param 0 | 1.234 | < 1.1 | ❌ |
| R-hat param 1 | 1.326 | < 1.1 | ❌ |
| R-hat param 2 | 1.259 | < 1.1 | ❌ |
| R-hat param 3 | 1.268 | < 1.1 | ❌ |
| R-hat param 4 | 1.197 | < 1.1 | ⚠️ |
| R-hat param 5 | 1.341 | < 1.1 | ❌ |
| ESS min | 4000 | > 100 | ✅ |
| Acceptance | 0.392 | 0.2-0.5 | ✅ |

### 2.4 Verdict Phase 3.2

❌ **NON CONVERGÉ** - R-hat > 1.1 pour 5/6 paramètres

**Action requise**: Augmenter n_steps à 2000+ ou améliorer les priors

---

## 3. Phase 3.3 - Ajustement ΛCDM

### 3.1 Configuration MCMC

| Paramètre | Valeur |
|-----------|--------|
| Sampler | emcee |
| Walkers | 32 |
| Steps | 500 |
| Burn-in | 250 |
| Paramètres | 5 (H0, Ωm, φ*, M*, α) |

### 3.2 Résultats Best-Fit

| Paramètre | Valeur | Planck 2018 |
|-----------|--------|-------------|
| H0 | 71.35 km/s/Mpc | 67.4 |
| Ωm | 0.405 | 0.315 |
| φ*_0 | 8.74×10⁻⁴ Mpc⁻³ | - |
| M*_0 | -23.80 | - |
| α_0 | -1.99 | - |

### 3.3 Diagnostics de Convergence

| Critère | Valeur | Seuil | Status |
|---------|--------|-------|--------|
| R-hat max | **1.204** | < 1.1 | ⚠️ **MARGINAL** |
| R-hat param 0 | 1.184 | < 1.1 | ⚠️ |
| R-hat param 1 | 1.204 | < 1.1 | ❌ |
| R-hat param 2 | 1.108 | < 1.1 | ⚠️ |
| R-hat param 3 | 1.139 | < 1.1 | ⚠️ |
| R-hat param 4 | 1.137 | < 1.1 | ⚠️ |
| ESS min | 2000 | > 100 | ✅ |
| Acceptance | 0.447 | 0.2-0.5 | ✅ |

### 3.4 Verdict Phase 3.3

⚠️ **MARGINALEMENT CONVERGÉ** - R-hat proche du seuil

---

## 4. Comparaison des Modèles

### 4.1 Chi-squared (du rapport existant)

| Modèle | χ² | χ²/dof | AIC | BIC |
|--------|-----|--------|-----|-----|
| JANUS | 2603 | 86.8 | 2615 | 2624 |
| LCDM | 4445 | 148.2 | 4451 | 4455 |
| **Δ** | **-1842** | | **-1836** | **-1831** |

### 4.2 Interprétation

Selon les résultats existants:
- ΔBIC = -1831 → "Strong evidence for JANUS"

**ATTENTION**: Ces résultats doivent être interprétés avec prudence car:
1. Les chaînes MCMC n'ont pas convergé
2. Les incertitudes sur les paramètres peuvent être sous-estimées
3. Une ré-analyse avec convergence appropriée est nécessaire

---

## 5. Fichiers Phase 3

### 5.1 Scripts

| Script | Description | Status |
|--------|-------------|--------|
| phase30a_31a_verified.py | Préparation données | ✅ |
| phase32_janus_fitting.py | MCMC JANUS | ✅ |
| phase33_lcdm_fitting.py | MCMC LCDM | ✅ |
| phase3_complete_v2.py | Pipeline complet v2 | ✅ |

### 5.2 Résultats MCMC

| Fichier | Contenu | Size |
|---------|---------|------|
| janus_v2.h5 | Chaînes JANUS | 2.9 MB |
| lcdm_v2.h5 | Chaînes LCDM | 2.9 MB |

### 5.3 Figures

| Figure | Description |
|--------|-------------|
| fig1_redshift_distribution_v2.pdf | N(z) |
| fig2_uv_lf_distribution_v2.pdf | UV LF |
| fig3_stellar_mass_function_v2.pdf | SMF |
| fig6_janus_corner_v2.pdf | Corner plot JANUS |
| uv_lf_comparison.pdf | Comparaison modèles |
| age_comparison.pdf | Âge univers |
| chi2_comparison.pdf | χ² par bin z |

---

## 6. Anomalies Détectées

### 6.1 Critique: Convergence MCMC

| Problème | Impact | Solution |
|----------|--------|----------|
| R-hat JANUS > 1.3 | Paramètres non fiables | Augmenter steps à 2000+ |
| R-hat LCDM > 1.1 | Incertitudes sous-estimées | Augmenter steps à 1000+ |

### 6.2 Moyenne: Catalogue v1 vs v2

| Problème | Impact | Solution |
|----------|--------|----------|
| v1 contient z=21.99 | Analyse biaisée | Utiliser exclusivement v2 |

### 6.3 Mineure: Documentation

| Problème | Impact | Solution |
|----------|--------|----------|
| Rapport contradictoires | Confusion | Consolider RPT_PHASE3*.md |

---

## 7. Recommandations

### 7.1 Actions Prioritaires (HAUTE)

1. **Relancer MCMC JANUS** avec:
   - n_steps = 2000 minimum
   - Vérifier convergence R-hat < 1.05
   - Sauvegarder diagnostic plots

2. **Relancer MCMC LCDM** avec:
   - n_steps = 1000 minimum
   - Même critères de convergence

3. **Utiliser exclusivement catalogue v2** pour toutes analyses

### 7.2 Actions Secondaires (MOYENNE)

4. Consolider les rapports Phase 3 en un seul document
5. Mettre à jour PLAN.md avec status réel

### 7.3 Validation Post-Correction

Critères pour valider Phase 3:
- [ ] R-hat < 1.05 pour tous paramètres
- [ ] ESS > 200 pour tous paramètres
- [ ] Acceptance rate 0.2-0.5
- [ ] Corner plots sans multimodalité

---

## 8. Conclusion

### Phase 3 Status Actuel

| Composant | Conformité | Bloquant? |
|-----------|------------|-----------|
| 3.1 Stats descriptives | 100% | Non |
| 3.2 JANUS MCMC | 70% | **OUI** |
| 3.3 LCDM MCMC | 80% | **OUI** |

### Verdict

⚠️ **PHASE 3 INCOMPLÈTE**

Les résultats actuels (ΔBIC favoring JANUS) sont **préliminaires** et nécessitent validation avec MCMC correctement convergés.

**Ne pas publier** ces résultats sans correction de la convergence MCMC.

---

## Annexe: Commande pour Relancer MCMC

```python
# Paramètres recommandés pour convergence
n_walkers = 64  # Augmenter
n_steps = 2000  # Minimum
burn_in = 500   # 25% du total

# Critères de convergence
target_rhat = 1.05
min_ess = 200
```

---

*Rapport d'Audit Phase 3 - VAL-Galaxies_primordiales*
*Généré le 2026-01-07*
