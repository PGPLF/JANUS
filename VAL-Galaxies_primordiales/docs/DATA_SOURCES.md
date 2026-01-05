# Sources de Données - VAL-Galaxies_primordiales

**Date de création**: 5 Janvier 2026
**Dernière mise à jour**: 5 Janvier 2026 22:20 (Post-Phase 2)

---

## 1. Dataset de Référence

### Labbé et al. (2023)
| Attribut | Valeur |
|----------|--------|
| **Publication** | Nature 616, 266-269 |
| **arXiv** | 2207.12446 |
| **DOI** | 10.1038/s41586-023-05786-2 |
| **Source données** | github.com/ivolabbe/red-massive-candidates |
| **Fichier** | sample_revision3_2207.12446.ecsv |
| **Date téléchargement** | 5 Jan 2026 20:30 |
| **N sources** | 13 (6 massives sélectionnées) |
| **Status** | ✅ Complet |

**Fichiers locaux**:
```
data/reference/
├── labbe2023_sample.ecsv      # Original (13 sources)
├── labbe2023_candidates.fits  # Sélection (6 massives)
└── labbe2023_candidates.csv   # Format CSV
```

---

## 2. Catalogues JWST

### 2.1 JADES DR2/DR3
| Attribut | Valeur |
|----------|--------|
| **URL** | archive.stsci.edu/hlsp/jades |
| **Status** | ✅ Téléchargé (S2) |
| **Date** | 2026-01-05 21:00 |
| **Fichiers** | GOODS-S DR2 (642 MB), GOODS-N DR3 (780 MB) |
| **N sources** | 179,709 totales |
| **N z>=8** | **7,138 candidats extraits** |

**Fichiers locaux**:
```
data/jwst/raw/jades/
├── jades_goods-s_photometry_v2.0.fits  # 94,000 sources
└── jades_goods-n_photometry_v1.0.fits  # 85,709 sources

data/jwst/processed/
├── jades_highz_z8.fits                  # 7,138 z>=8
└── jades_highz_z8.csv                   # Format CSV
```

### 2.2 CEERS NIRSpec DR0.7
| Attribut | Valeur |
|----------|--------|
| **URL** | web.corral.tacc.utexas.edu/ceersdata/DR07 |
| **Status** | ✅ Téléchargé (S2) |
| **Date** | 2026-01-05 21:00 |
| **Fichier** | ceers_nirspec_master_dr0.7.csv (145 KB) |
| **Note** | Master spectro catalog |

### 2.3 GLASS-JWST v2
| Attribut | Valeur |
|----------|--------|
| **URL** | glass.astro.ucla.edu |
| **Status** | ✅ Via JANUS-Z reference |
| **Date** | 2026-01-05 21:30 |
| **N inclus** | Intégré dans JANUS-Z (236 gal.) |

### 2.4 UNCOVER DR4
| Attribut | Valeur |
|----------|--------|
| **URL** | jwst-uncover.github.io/DR4.html |
| **Status** | ✅ Via JANUS-Z reference |
| **Date** | 2026-01-05 21:30 |
| **N inclus** | Intégré dans JANUS-Z (236 gal.) |

### 2.5 COSMOS-Web
| Attribut | Valeur |
|----------|--------|
| **URL** | cosmos.astro.caltech.edu |
| **Status** | ⚠️ Via JANUS-Z (COSMOS2025 non publié) |
| **Date** | 2026-01-05 21:30 |
| **N inclus** | Partiel via JANUS-Z |

### 2.6 EXCELS
| Attribut | Valeur |
|----------|--------|
| **Spécialité** | Métallicité haute-z |
| **Status** | ✅ Via JANUS-Z reference |
| **Date** | 2026-01-05 21:45 |
| **N inclus** | 4 galaxies (metallicity_12OH mesuré) |

**Fichier**: `data/jwst/special/excels_metallicity_sample.csv`

### 2.7 A3COSMOS
| Attribut | Valeur |
|----------|--------|
| **arXiv** | 2511.08672 |
| **Spécialité** | Galaxies NIRCam-dark |
| **Status** | ✅ Via JANUS-Z reference |
| **Date** | 2026-01-05 21:45 |
| **N inclus** | 24 galaxies dusty |

**Fichier**: `data/jwst/special/a3cosmos_dusty_sample.csv`

---

## 3. JANUS-Z Reference Catalog

### JANUS-Z v17.1 (Source principale Phase 2)
| Attribut | Valeur |
|----------|--------|
| **Source** | Projet JANUS-Z |
| **Version** | v17.1 |
| **Status** | ✅ Intégré |
| **Date** | 2026-01-05 21:30 |
| **N total** | 236 galaxies |
| **z range** | 6.50 - 14.52 |
| **z_spec** | 93 (39%) |
| **z_phot** | 143 (61%) |

**Surveys inclus**: JADES, GLASS, UNCOVER, CEERS, EXCELS, A3COSMOS

**Fichier**: `data/jwst/processed/janus_z_reference_catalog.csv`

---

## 4. Découvertes Exceptionnelles

### 4.1 "Impossible Galaxies"
| Objet | z | log(M*) | Status |
|-------|---|---------|--------|
| AC-2168 | 6.63 | 10.57 | ✅ Inclus |
| JWST-Impossible-z12 | 12.15 | 9.02 | ✅ Inclus |

**Fichier**: `data/jwst/special/impossible_galaxies.csv`
**Date**: 2026-01-05 21:45

### 4.2 AGN Haute-z
| Objet | z | Status |
|-------|---|--------|
| GHZ9 | 10.38 | ✅ Inclus |
| GN-z11 | 10.60 | ✅ Inclus |

**Fichier**: `data/jwst/special/agn_hosts.csv`
**Date**: 2026-01-05 21:45

### 4.3 Ultra High-z (z_spec > 12)
| Attribut | Valeur |
|----------|--------|
| **N galaxies** | 17 |
| **z range** | 12.01 - 14.52 |
| **Status** | ✅ Complet |

**Fichier**: `data/jwst/special/ultra_highz_zspec_gt12.csv`

---

## 5. Proto-clusters

| Proto-cluster | z_spec | N membres | Status |
|---------------|--------|-----------|--------|
| GHZ9-cluster | 10.14 | 7 | ✅ |
| A2744-z7p9 | 7.89 | 7 | ✅ |
| GLASS-z10-PC | 10.13 | 5 | ✅ |
| A2744-z9-PC | 9.04 | 4 | ✅ |
| JD1-cluster | 10.31 | 2 | ✅ |
| A2744-z13 | 12.63 | 1 | ✅ |
| **Total** | | **26** | ✅ |

**Fichier**: `data/jwst/special/protocluster_members.csv`
**Date**: 2026-01-05 21:45

---

## 6. Données Complémentaires

### HST Legacy
| Attribut | Valeur |
|----------|--------|
| **Source** | CANDELS, HUDF |
| **Status** | ⬜ Reporté Phase 3 |
| **Priorité** | Basse (si nécessaire) |

### Dawn JWST Archive
| Attribut | Valeur |
|----------|--------|
| **URL** | dawn-cph.github.io/dja |
| **Status** | ⬜ Non téléchargé |
| **Note** | JANUS-Z inclut spectro équivalente |

---

## 7. Résumé Phase 2

| Source | N | Status | Fichier |
|--------|---|--------|---------|
| Labbé+23 | 6 | ✅ | reference/labbe2023_candidates.csv |
| JADES extraction | 7,138 | ✅ | processed/jades_highz_z8.csv |
| JANUS-Z reference | 236 | ✅ | processed/janus_z_reference_catalog.csv |
| EXCELS | 4 | ✅ | special/excels_metallicity_sample.csv |
| A3COSMOS | 24 | ✅ | special/a3cosmos_dusty_sample.csv |
| Proto-clusters | 26 | ✅ | special/protocluster_members.csv |
| AGN hosts | 2 | ✅ | special/agn_hosts.csv |
| Ultra high-z | 17 | ✅ | special/ultra_highz_zspec_gt12.csv |
| Impossible | 2 | ✅ | special/impossible_galaxies.csv |

**Total unique estimé**: ~7,400 galaxies z >= 8

---

## Légende Status
- ✅ Téléchargé et validé
- ⚠️ Partiel ou adaptation
- ⬜ Non téléchargé / Reporté

---

*DATA_SOURCES.md - VAL-Galaxies_primordiales*
*Mise à jour: 2026-01-05 22:20 (Post-Phase 2)*
