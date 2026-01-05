# Rapport Phase 2 - Acquisition Données JWST

**Projet**: VAL-Galaxies_primordiales
**Date**: 2026-01-05
**Statut**: COMPLÉTÉ

---

## Résumé Exécutif

La Phase 2 a permis l'acquisition et la structuration d'un échantillon complet de galaxies à haut redshift pour la validation du modèle JANUS.

### Statistiques Globales

| Source | N galaxies | Description |
|--------|------------|-------------|
| JANUS-Z Reference | 236 | Catalogue de référence (z=6.5-14.5) |
| JADES Extraction | 7,138 | Candidats photométriques z>=8 |
| Labbé+23 | 6 | Galaxies massives impossibles |
| **Total unique** | ~7,380 | Échantillon combiné |

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

### 1.3 Labbé+23 Reference
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

- [x] JADES: 7,138 candidats z>=8
- [x] JANUS-Z: 236 galaxies référence
- [x] Labbé+23: 6 candidats massifs
- [x] Échantillons spéciaux: 75 galaxies
- [x] Veille arXiv: opérationnelle

**Phase 2 COMPLÉTÉE avec succès.**

---
*Rapport généré automatiquement - VAL-Galaxies_primordiales*
