# Plan Étapes 3.0.a et 3.1.a - Reconstruction sur Données Vérifiées

**Date**: 2026-01-06
**Contexte**: Audit révèle 66% de données contaminées dans le catalogue JANUS-Z
**Objectif**: Reconstruire l'analyse sur bases fiables uniquement

---

## Résumé Audit

### Sources FIABLES (à utiliser)

| Source | N | Type | Provenance | Status |
|--------|---|------|------------|--------|
| JADES DR2/DR3 photométrie | 179,709 | Brut | STScI Archive | ✅ Vérifié |
| jades_highz_muv_reff.csv | 16,766 | Dérivé | Calculé des FITS | ✅ Vérifié |
| JADES DR4 spectroscopie | 5,190 (145 z>8) | Brut | jades-survey.github.io | ✅ Vérifié |
| COSMOS-Web | 784,016 (2,827 z>8) | Brut | cosmos2025.iap.fr | ✅ Vérifié |
| Labbé+23 | 6 | Référence | Nature/arXiv | ✅ Vérifié |
| CEERS NIRSpec DR0.7 | 1,325 | Brut | CEERS official | ✅ Vérifié |

### Sources CONTAMINÉES (à NE PAS utiliser)

| Source | Problème | Action |
|--------|----------|--------|
| janus_z_reference_catalog.csv | 66% fictif (preview/2026) | SUPPRIMER |
| janus_z_complete.csv | Dérivé du précédent | SUPPRIMER |
| Échantillons spéciaux | Extraits du catalogue contaminé | RECONSTRUIRE |

---

## Étape 3.0.a - Préparation Données Propres

### Objectif
Créer un catalogue consolidé UNIQUEMENT à partir de sources vérifiées.

### 3.0.a.1 - Échantillon Photométrique JADES (VALIDE)

**Source**: `jades_highz_muv_reff.csv` (déjà calculé depuis FITS bruts)

**Actions**:
1. Filtrer outliers M_UV (garder -25 < M_UV < -12)
2. Filtrer outliers r_eff (garder 0.05 < r_eff < 5 kpc)
3. Appliquer cut qualité photo-z (z_hi - z_lo < 1.0)

**Résultat attendu**: ~14,000 galaxies z ≥ 6.5

### 3.0.a.2 - Échantillon Spectroscopique JADES DR4

**Source**: `Combined_DR4_external_v1.2.1.fits`

**Actions**:
1. Extraire galaxies avec z_Spec > 0 et z_Spec_flag = 'secure'
2. Sélectionner z_spec > 6.5
3. Extraire paramètres: ID, RA, Dec, z_spec, z_err

**Résultat attendu**: ~200-300 galaxies z_spec > 6.5

### 3.0.a.3 - Paramètres Physiques COSMOS-Web

**Source**: `COSMOSWeb_mastercatalog_v1.fits`

**Actions**:
1. Extraire extension CIGALE (masses stellaires, SFR)
2. Sélectionner zfinal > 6.5
3. Filtrer sur qualité χ²

**Colonnes à extraire**:
- `mass_best`, `mass_err` (log M*)
- `sfr_best`, `sfr_err` (SFR)
- `zfinal`, `zpdf_l68`, `zpdf_u68`

**Résultat attendu**: ~15,000 galaxies z > 6.5 avec M* et SFR

### 3.0.a.4 - Consolidation

**Actions**:
1. Cross-match JADES + COSMOS par position (1" radius)
2. Prioriser z_spec sur z_phot
3. Créer catalogue unifié avec flag qualité (Gold/Silver/Bronze)

**Format catalogue final**:
```
ID, RA, DEC, z, z_err, z_type (spec/phot),
M_UV, M_UV_err, log_Mstar, log_Mstar_err,
log_SFR, log_SFR_err, r_eff_kpc, r_eff_err,
Survey, Quality_flag, Reference
```

### Livrables 3.0.a

| Fichier | Description |
|---------|-------------|
| `highz_catalog_VERIFIED_v1.csv` | Catalogue consolidé propre |
| `highz_spectro_GOLD.csv` | Sous-échantillon z_spec uniquement |
| `AUDIT_REPORT_3.0a.md` | Rapport d'audit détaillé |

---

## Étape 3.1.a - Statistiques Descriptives (Données Vérifiées)

### Objectif
Recalculer toutes les distributions avec le catalogue propre.

### 3.1.a.1 - UV Luminosity Function

**Données**: JADES photométrique filtré
**Bins z**: 6.5-8, 8-10, 10-12, 12-14, 14+
**Méthode**: 1/Vmax avec corrections de complétude

**Output**: `fig1a_uv_luminosity_function.pdf`

### 3.1.a.2 - Stellar Mass Function

**Données**: COSMOS-Web CIGALE masses
**Bins z**: 6.5-8, 8-10, 10-12
**Méthode**: 1/Vmax

**Output**: `fig2a_stellar_mass_function.pdf`

### 3.1.a.3 - SFR Distribution

**Données**: COSMOS-Web CIGALE SFR
**Bins z**: par bin de redshift

**Output**: `fig3a_sfr_distribution.pdf`

### 3.1.a.4 - Size-Mass Relation

**Données**: JADES r_eff + COSMOS M*
**Cross-match**: Position 1"

**Output**: `fig4a_size_mass_relation.pdf`

### 3.1.a.5 - Redshift Distribution (NOUVEAU)

**Données**: Tous échantillons
**Comparaison**: z_spec vs z_phot

**Output**: `fig5a_redshift_distribution.pdf`

### Livrables 3.1.a

| Fichier | Description |
|---------|-------------|
| `fig1a_uv_luminosity_function.pdf` | UV LF par bin z |
| `fig2a_stellar_mass_function.pdf` | SMF par bin z |
| `fig3a_sfr_distribution.pdf` | Distribution SFR |
| `fig4a_size_mass_relation.pdf` | Relation r_eff - M* |
| `fig5a_redshift_distribution.pdf` | N(z) spec vs phot |
| `table1a_sample_statistics.tex` | Table statistiques |
| `OBSERVED_DISTRIBUTIONS_v2.md` | Documentation |

---

## Validation

### Critères de Qualité

| Critère | Seuil | Vérification |
|---------|-------|--------------|
| N galaxies z>8 | > 1000 | Distribution statistique |
| N z_spec confirmés | > 100 | Cross-match littérature |
| M_UV cohérent | -25 < M_UV < -12 | Comparaison Harikane+24 |
| M* cohérent | 7 < log(M*) < 12 | Comparaison Stefanon+21 |
| r_eff cohérent | 0.05 < r < 5 kpc | Comparaison Ono+24 |

### Comparaisons Littérature

- UV LF: Harikane+2024, Bouwens+2021
- SMF: Stefanon+2021, Song+2016
- Sizes: Ono+2024, Shibuya+2015

---

## Timeline

| Étape | Durée | Dépendances |
|-------|-------|-------------|
| 3.0.a.1 Filtre JADES | 1h | - |
| 3.0.a.2 Extract DR4 | 2h | - |
| 3.0.a.3 Extract COSMOS | 2h | - |
| 3.0.a.4 Consolidation | 2h | 3.0.a.1-3 |
| 3.1.a Figures | 3h | 3.0.a.4 |
| Validation | 2h | 3.1.a |

**Total estimé**: 1 session de travail

---

## Risques et Mitigations

| Risque | Impact | Mitigation |
|--------|--------|------------|
| COSMOS M* systématiquement biaisé | Moyen | Comparaison avec JADES SED fitting |
| Peu de z_spec z>12 | Faible | Combiner avec photo-z haute confiance |
| Cross-match ambigu | Faible | Utiliser matching radius strict (0.5") |

---

## Prochaines Étapes (après 3.1.a)

1. **Phase 3.2.a**: Prédictions théoriques JANUS
2. **Phase 3.3.a**: Prédictions théoriques ΛCDM
3. **Phase 4.a**: Comparaison modèles (χ², BIC)
4. **Phase 5.a**: Tests "impossible galaxies" avec Labbé+23

---

*Plan 3.0.a/3.1.a - VAL-Galaxies_primordiales*
*Basé sur audit 2026-01-06*
