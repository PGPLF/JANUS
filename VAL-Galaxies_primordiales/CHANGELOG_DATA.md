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

---

## [2026-01-05] - Phase 2 Semaine 3

### Compilation d'échantillon
- **Catalogue de référence JANUS-Z v17.1** intégré
  - 236 galaxies (6.50 < z < 14.52)
  - 93 spectroscopiques, 143 photométriques
  - Surveys: JADES, GLASS, UNCOVER, CEERS, EXCELS, A3COSMOS

### Statistiques échantillon combiné
- **JADES extraction** (z >= 8, z < 15): 4,506 candidats
  - 8 <= z < 10: 2,765
  - 10 <= z < 12: 793
  - 12 <= z < 15: 948
- **JANUS-Z référence**: 236 galaxies confirmées
- **Labbé+23 référence**: 6 galaxies massives

### Distribution JANUS-Z par redshift
- 6.5 <= z < 8: 61
- 8 <= z < 10: 71
- 10 <= z < 12: 63
- 12 <= z < 14: 21
- z >= 14: 20

### Fichiers créés
- `data/jwst/processed/janus_z_reference_catalog.csv`
- `data/jwst/processed/highz_sample_summary.txt`
- `scripts/compile_highz_sample.py`

### Notes
- UNCOVER/GLASS: données incluses via référence JANUS-Z
- COSMOS-Web: à intégrer si release disponible

---

---

## [2026-01-05] - Phase 2 Semaine 4

### Échantillons spéciaux extraits

| Échantillon | N | Description |
|-------------|---|-------------|
| EXCELS | 4 | Métallicité (6.82 < z < 8.27) |
| A3COSMOS/Dusty | 24 | NIRCam-dark (6.51 < z < 8.49) |
| Proto-clusters | 26 | 6 clusters (7.89 < z < 12.63) |
| AGN hosts | 2 | GHZ9, GN-z11 (z~10) |
| Ultra high-z | 17 | z_spec > 12 |
| "Impossible" | 2 | AC-2168, JWST-Impossible-z12 |

### Proto-clusters identifiés
- GHZ9-cluster: 7 membres, <z>=10.14
- A2744-z7p9: 7 membres, <z>=7.89
- GLASS-z10-PC: 5 membres, <z>=10.13
- A2744-z9-PC: 4 membres, <z>=9.04
- JD1-cluster: 2 membres, <z>=10.31
- A2744-z13: 1 membre, z=12.63

### "Impossible galaxies"
- **AC-2168**: z=6.63, log(M*)=10.57 (arXiv:2511.08672)
- **JWST-Impossible-z12**: z=12.15, log(M*)=9.02 (Jan 2026)

### Fichiers créés
- `data/jwst/special/excels_metallicity_sample.csv`
- `data/jwst/special/a3cosmos_dusty_sample.csv`
- `data/jwst/special/protocluster_members.csv`
- `data/jwst/special/agn_hosts.csv`
- `data/jwst/special/ultra_highz_zspec_gt12.csv`
- `data/jwst/special/impossible_galaxies.csv`
- `scripts/extract_special_samples.py`

---

---

## [2026-01-05] - Phase 2 Semaine 5 (FINALE)

### Script veille arXiv
- **weekly_arxiv_monitor.py** opérationnel
  - Recherche automatique astro-ph.GA + JWST + high-z
  - Classification HIGH/MEDIUM/LOW priority
  - Rapport markdown + JSON
  - Premier test: 5 articles pertinents (2 HIGH, 3 LOW)

### Fichiers créés
- `scripts/weekly_arxiv_monitor.py`
- `data/monitoring/2026_W02/weekly_report.md`
- `data/monitoring/2026_W02/papers.json`
- `PHASE2_REPORT.md` - Rapport final

### Validation finale
- [x] JANUS-Z Reference: 236 galaxies (93 spec, 143 phot)
- [x] JADES Extraction: 7,138 candidats z>=8
- [x] Labbé+23: 6 galaxies massives
- [x] Échantillons spéciaux: 75 galaxies (6 catégories)
- [x] Veille arXiv: fonctionnelle

### Phase 2 COMPLÉTÉE

---

## Prochaines étapes (Phase 3)

- [ ] Analyse statistique N(z) JANUS vs ΛCDM
- [ ] Fonctions de luminosité UV
- [ ] Fonctions de masse stellaire
- [ ] Tests "impossible galaxies"

---

*Changelog VAL-Galaxies_primordiales*
