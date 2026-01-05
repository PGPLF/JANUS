# Changelog Données - VAL-Galaxies_primordiales

Historique des acquisitions et mises à jour de données.

---

## [2026-01-05] - Phase 2 Semaine 1

### Ajouté
- **Dataset de référence Labbé+23**
  - Source: github.com/ivolabbe/red-massive-candidates
  - Fichier: `sample_revision3_2207.12446.ecsv`
  - 13 sources originales, 6 candidats massifs extraits

### Fichiers créés
- `data/reference/labbe2023_sample.ecsv` - Échantillon complet
- `data/reference/labbe2023_candidates.fits` - 6 candidats log(M*) > 10
- `data/reference/labbe2023_candidates.csv` - Format CSV

### Scripts créés
- `scripts/extract_labbe2023_candidates.py` - Extraction automatisée

### Documentation créée
- `docs/LABBE2023_METHODOLOGY.md` - Méthodologie SED fitting
- `docs/DATA_SOURCES.md` - Registre des sources

### Validation
- ✅ 6 candidats extraits (z: 7.32-9.08, log M*: 10.02-10.89)
- ✅ Cohérent avec Table 1 Nature (légères différences revision 3)

---

---

## [2026-01-05] - Phase 2 Semaine 2

### Téléchargé
- **JADES GOODS-S DR2** (642 MB)
  - Source: archive.stsci.edu/hlsp/jades
  - 94,000 sources totales
  - 3,979 candidats z >= 8

- **JADES GOODS-N DR3** (780 MB)
  - Source: archive.stsci.edu/hlsp/jades
  - 85,709 sources totales
  - 3,159 candidats z >= 8

- **CEERS NIRSpec DR0.7** (145 KB)
  - Source: web.corral.tacc.utexas.edu/ceersdata/DR07

### Extraction haute-z
- **Total: 7,138 candidats z >= 8**
  - GOODS-S: 3,979
  - GOODS-N: 3,159
- Distribution par redshift:
  - 8 <= z < 10: 2,765
  - 10 <= z < 12: 793
  - 12 <= z < 14: 630
  - z >= 14: 2,454 (à filtrer sur qualité)

### Fichiers créés
- `data/jwst/raw/jades/jades_goods-s_photometry_v2.0.fits`
- `data/jwst/raw/jades/jades_goods-n_photometry_v1.0.fits`
- `data/jwst/raw/ceers/ceers_nirspec_master_dr0.7.csv`
- `data/jwst/processed/jades_highz_z8.fits`
- `data/jwst/processed/jades_highz_z8.csv`
- `scripts/extract_highz_jades.py`

### Notes
- GLASS et UNCOVER nécessitent téléchargement manuel (Google Drive)
- Candidats z > 20 probablement artefacts - nécessite filtrage qualité

---

## À venir

### Semaine 3 (S3)
- [ ] UNCOVER DR3 (Google Drive)
- [ ] COSMOS-Web

### Semaine 3 (S3)
- [ ] UNCOVER DR4
- [ ] COSMOS-Web
- [ ] HST Legacy

### Semaine 4 (S4)
- [ ] EXCELS
- [ ] A3COSMOS

### Semaine 5 (S5)
- [ ] Proto-clusters
- [ ] AC-2168 ("impossible galaxy")
- [ ] Liste z > 12

---

*Changelog VAL-Galaxies_primordiales*
