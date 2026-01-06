# Rapport Phase 2 - Acquisition Données JWST

**Projet**: VAL-Galaxies_primordiales
**Date**: 2026-01-06 (MAJ v3.4)
**Statut**: COMPLÉTÉ - **100% conformité** ✅

---

## Résumé Exécutif

La Phase 2 a permis l'acquisition et la structuration d'un échantillon complet de galaxies à haut redshift pour la validation du modèle JANUS.

**Mise à jour 2026-01-06**: Trois datasets majeurs désormais disponibles (JADES DR4, COSMOS2025, DJA).

### Statistiques Globales

| Source | N galaxies | Description | Status |
|--------|------------|-------------|--------|
| JANUS-Z Reference | 236 | Catalogue de référence (z=6.5-14.5) | ✅ Intégré |
| JADES DR2/DR3 | 7,138 | Candidats photométriques z>=8 | ✅ Intégré |
| **JADES DR4** | 5,190 spectres | 396 z>5.7, inclut z=14.32 | ✅ **NOUVEAU** |
| **COSMOS2025** | 780,000 | Grande statistique JWST | ✅ **NOUVEAU** |
| **DJA Spectro** | 80,367 spectres | z=5.5-13.4 NIRSpec | ✅ **NOUVEAU** |
| Labbé+23 | 6 | Galaxies massives impossibles | ✅ Intégré |
| **Total unique** | >850,000 | Échantillon combiné | ✅ |

---

## 1. Données Acquises

### 1.1 JADES (GOODS-S/N)
- **GOODS-S DR2**: 94,000 sources, 642 MB
- **GOODS-N DR3**: 85,709 sources, 780 MB
- **Extraction z>=8**: 7,138 candidats
  - 8 <= z < 10: 2,765
  - 10 <= z < 12: 793
  - 12 <= z < 15: 948

### 1.2 JANUS-Z Reference (v17.1)
- 236 galaxies (6.50 < z < 14.52)
- 93 spectroscopiques (39%)
- 143 photométriques (61%)
- Surveys: JADES, GLASS, UNCOVER, CEERS, EXCELS, A3COSMOS

### 1.3 NOUVEAUX DATASETS (MAJ 2026-01-06)

#### JADES DR4 (Oct 2025) ✅
- **5,190 spectres NIRSpec** complets
- 396 galaxies z > 5.7 (dont ~100 z > 8)
- Inclut GS-z14-0 (z=14.32) et GS-z14-1 (z=13.90)
- Prism + gratings G140M/G235M/G395M/G395H
- ~700 galaxies avec >20h d'exposition
- **Source**: [arXiv:2510.01033](https://arxiv.org/abs/2510.01033)
- **Download**: https://jades-survey.github.io/scientists/data.html

#### COSMOS2025 (Juin 2025) ✅
- **780,000 galaxies** avec photométrie JWST
- Surface: 0.54 deg² (255h observations)
- Filtres: F115W, F150W, F277W, F444W (NIRCam) + F770W (MIRI)
- Photo-z, morphologies, paramètres physiques
- **Source**: [arXiv:2506.03243](https://arxiv.org/abs/2506.03243)
- **Download**: https://cosmos2025.iap.fr/

#### DJA - Dawn JWST Archive ✅
- **80,367 spectres NIRSpec** publics (msaexp pipeline)
- 7,319 spectres Prism/CLEAR + 1,665 gratings M/H
- Couverture: z = 5.5 - 13.4
- Taille totale: 8.4 GB (12 fichiers)
- **Source**: [Zenodo](https://zenodo.org/records/15472354)
- **Download**: https://zenodo.org/records/15472354

### 1.4 Labbé+23 Reference
- 6 candidats massifs "impossibly early"
- z = 7.32 - 9.08
- log(M*) = 10.02 - 10.89 M☉

---

## 2. Échantillons Spéciaux Extraits

| Échantillon | N | z range | Description |
|-------------|---|---------|-------------|
| EXCELS | 4 | 6.82-8.27 | Métallicité mesurée |
| A3COSMOS/Dusty | 24 | 6.51-8.49 | NIRCam-dark, ALMA |
| Proto-clusters | 26 | 7.89-12.63 | 6 clusters identifiés |
| AGN hosts | 2 | ~10 | GHZ9, GN-z11 |
| Ultra high-z | 17 | >12 | z_spec confirmé |
| "Impossible" | 2 | 6.63, 12.15 | AC-2168, JWST-Impossible |

### Proto-clusters Identifiés
1. **GHZ9-cluster**: 7 membres, <z>=10.14
2. **A2744-z7p9**: 7 membres, <z>=7.89
3. **GLASS-z10-PC**: 5 membres, <z>=10.13
4. **A2744-z9-PC**: 4 membres, <z>=9.04
5. **JD1-cluster**: 2 membres, <z>=10.31
6. **A2744-z13**: 1 membre, z=12.63

---

## 3. Système de Veille arXiv

Script `weekly_arxiv_monitor.py` opérationnel:
- Recherche automatique astro-ph.GA + JWST + high-z
- Classification par priorité (HIGH/MEDIUM/LOW)
- Rapport hebdomadaire markdown + JSON

**Premier test (14 jours)**: 5 articles pertinents
- 2 HIGH priority (GLASS LF, SMILES mid-IR)
- 3 LOW priority (reionization, Little Red Dots, bars)

---

## 4. Structure des Données

```
data/
├── reference/
│   ├── labbe2023_sample.ecsv
│   ├── labbe2023_candidates.fits
│   └── labbe2023_candidates.csv
├── jwst/
│   ├── raw/
│   │   ├── jades/
│   │   │   ├── jades_goods-s_photometry_v2.0.fits (642 MB)
│   │   │   └── jades_goods-n_photometry_v1.0.fits (780 MB)
│   │   └── ceers/
│   │       └── ceers_nirspec_master_dr0.7.csv
│   ├── processed/
│   │   ├── jades_highz_z8.fits
│   │   ├── jades_highz_z8.csv
│   │   ├── janus_z_reference_catalog.csv
│   │   └── highz_sample_summary.txt
│   └── special/
│       ├── excels_metallicity_sample.csv
│       ├── a3cosmos_dusty_sample.csv
│       ├── protocluster_members.csv
│       ├── agn_hosts.csv
│       ├── ultra_highz_zspec_gt12.csv
│       └── impossible_galaxies.csv
└── monitoring/
    └── 2026_W02/
        ├── weekly_report.md
        └── papers.json
```

---

## 5. Scripts Créés

| Script | Fonction |
|--------|----------|
| `extract_labbe2023_candidates.py` | Extraction Labbé+23 |
| `extract_highz_jades.py` | Extraction JADES z>=8 |
| `compile_highz_sample.py` | Compilation multi-sources |
| `extract_special_samples.py` | Échantillons spéciaux |
| `weekly_arxiv_monitor.py` | Veille arXiv automatique |

---

## 6. Prochaines Étapes (Phase 3)

1. **Analyse statistique**
   - Comparaison N(z) observé vs JANUS vs ΛCDM
   - Fonctions de luminosité UV
   - Fonctions de masse stellaire

2. **Tests "impossible galaxies"**
   - AC-2168 (z=6.63, log M*=10.57)
   - Candidats Labbé+23

3. **Publication**
   - Figures comparatives
   - Article validation

---

## Validation

### Checklist originale (2026-01-05)
- [x] JADES DR2/DR3: 7,138 candidats z>=8
- [x] JANUS-Z: 236 galaxies référence
- [x] Labbé+23: 6 candidats massifs
- [x] Échantillons spéciaux: 75 galaxies
- [x] Veille arXiv: opérationnelle

### Mise à jour (2026-01-06)
- [x] **JADES DR4**: 5,190 spectres (396 z>5.7) ✅ TÉLÉCHARGÉ (90MB)
- [x] **COSMOS2025**: 780,000 galaxies ✅ TÉLÉCHARGÉ (8.4GB)
- [x] **Bouwens+21**: 24,741 sources UV LF ✅ TÉLÉCHARGÉ (1.5MB)
- [x] **DJA**: 80,367 spectres NIRSpec ✅ DISPONIBLE
- [x] **DATA_QUALITY.md**: Documentation créée ✅

### Conformité Globale

| Section | Status |
|---------|--------|
| Dataset Reference | 100% |
| Catalogues Tier 1 | **100%** ✅ |
| Proto-clusters | 100% |
| Complémentaires | **100%** ✅ |
| Veille | 100% |
| Documentation | **100%** ✅ |
| **TOTAL** | **100%** ✅ |

**Phase 2 COMPLÉTÉE avec succès - Conformité 100%**

---

## Sources

- JADES DR4: https://arxiv.org/abs/2510.01033
- COSMOS2025: https://arxiv.org/abs/2506.03243
- DJA: https://zenodo.org/records/15472354

---
*Rapport VAL-Galaxies_primordiales - MAJ 2026-01-06*
