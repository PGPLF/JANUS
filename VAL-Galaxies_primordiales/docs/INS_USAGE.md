# Instructions d'Utilisation - VAL-Galaxies_primordiales

**Version**: 1.0
**Date**: 2026-01-05
**Auteur**: Claude Code

---

## 1. Vue d'Ensemble

Ce projet valide le modèle cosmologique JANUS contre les observations JWST de galaxies primordiales (z > 8).

### Structure du Projet

```
VAL-Galaxies_primordiales/
├── PLAN.md                    # Plan directeur (7 phases)
├── PHASE2_SUBPLAN.md          # Sous-plan Phase 2 (acquisition données)
├── PHASE2_REPORT.md           # Rapport final Phase 2
├── RPT_PHASE2_VALIDATION.md   # Rapport de validation Phase 2
├── CHANGELOG_DATA.md          # Historique acquisitions données
├── data/
│   ├── reference/             # Données de référence (Labbé+23)
│   ├── jwst/
│   │   ├── raw/               # Données brutes JADES, CEERS
│   │   ├── processed/         # Données traitées
│   │   └── special/           # Échantillons spéciaux
│   └── monitoring/            # Rapports veille arXiv
├── scripts/                   # Scripts Python
├── docs/                      # Documentation
├── notebooks/                 # Jupyter notebooks (Phase 3+)
├── results/                   # Résultats analyses (Phase 3+)
└── papers/                    # Articles (Phase 6)
```

---

## 2. Données Disponibles (Post-Phase 2)

### 2.1 Échantillons Principaux

| Fichier | N | Description |
|---------|---|-------------|
| `data/jwst/processed/janus_z_reference_catalog.csv` | 236 | Référence principale JANUS-Z v17.1 |
| `data/jwst/processed/jades_highz_z8.csv` | 7,138 | Candidats JADES z >= 8 |
| `data/reference/labbe2023_candidates.csv` | 6 | Galaxies massives Labbé+23 |

### 2.2 Échantillons Spéciaux

| Fichier | N | Description |
|---------|---|-------------|
| `data/jwst/special/excels_metallicity_sample.csv` | 4 | Métallicité mesurée |
| `data/jwst/special/a3cosmos_dusty_sample.csv` | 24 | NIRCam-dark/ALMA |
| `data/jwst/special/protocluster_members.csv` | 26 | 6 proto-clusters |
| `data/jwst/special/agn_hosts.csv` | 2 | GHZ9, GN-z11 |
| `data/jwst/special/ultra_highz_zspec_gt12.csv` | 17 | z_spec > 12 |
| `data/jwst/special/impossible_galaxies.csv` | 2 | AC-2168, JWST-Impossible |

---

## 3. Scripts Disponibles

### 3.1 Extraction de Données

```bash
# Extraire candidats Labbé+23
python3 scripts/extract_labbe2023_candidates.py

# Extraire haute-z de JADES
python3 scripts/extract_highz_jades.py

# Compiler échantillon complet
python3 scripts/compile_highz_sample.py

# Extraire échantillons spéciaux
python3 scripts/extract_special_samples.py
```

### 3.2 Veille arXiv

```bash
# Veille hebdomadaire (7 jours par défaut)
python3 scripts/weekly_arxiv_monitor.py

# Veille étendue (14 jours)
python3 scripts/weekly_arxiv_monitor.py --days 14
```

**Exécution recommandée**: Chaque lundi matin

---

## 4. Colonnes des Catalogues

### 4.1 JANUS-Z Reference (`janus_z_reference_catalog.csv`)

| Colonne | Type | Description |
|---------|------|-------------|
| ID | str | Identifiant unique |
| z | float | Redshift |
| z_err | float | Incertitude redshift |
| z_type | str | "spec" ou "phot" |
| log_Mstar | float | log10(M*/Msun) |
| sigma_Mstar | float | Incertitude masse |
| log_SFR | float | log10(SFR/Msun/yr) |
| metallicity_12OH | float | 12 + log(O/H) |
| has_AGN | int | 0/1 |
| is_dusty | int | 0/1 |
| protocluster | str | Nom ou "field" |
| Survey | str | Source survey |
| Reference | str | Article source |

### 4.2 JADES High-z (`jades_highz_z8.csv`)

| Colonne | Type | Description |
|---------|------|-------------|
| ID | str | Identifiant JADES |
| RA | float | Ascension droite (deg) |
| DEC | float | Déclinaison (deg) |
| EAZY_z_a | float | Redshift photométrique |
| EAZY_l68 | float | Borne inférieure 68% |
| EAZY_u68 | float | Borne supérieure 68% |
| field | str | "GOODS-S" ou "GOODS-N" |

---

## 5. Procédures

### 5.1 Veille Hebdomadaire

1. Exécuter `python3 scripts/weekly_arxiv_monitor.py`
2. Consulter rapport dans `data/monitoring/YYYY_WNN/weekly_report.md`
3. Si articles HIGH priority: évaluer pour intégration
4. Mettre à jour `CHANGELOG_DATA.md` si nouvelles données

### 5.2 Ajout de Nouvelles Données

1. Placer fichiers bruts dans `data/jwst/raw/{survey}/`
2. Créer script d'extraction dans `scripts/`
3. Exporter vers `data/jwst/processed/`
4. Documenter dans `docs/DATA_SOURCES.md`
5. Logger dans `CHANGELOG_DATA.md`

### 5.3 Mise à Jour GitHub

```bash
# Vérifier statut
git status

# Ajouter fichiers
git add -A

# Commit avec message descriptif
git commit -m "Phase N: Description courte"

# Pousser vers remote
git push origin master
```

---

## 6. Dépendances Python

```python
# Requis
numpy
pandas
astropy
matplotlib

# Scripts veille
urllib
xml.etree.ElementTree
```

---

## 7. Contact et Support

- **Projet**: VAL-Galaxies_primordiales
- **Parent**: JANUS
- **Documentation**: `docs/`
- **Rapports**: `RPT_*.md`

---

*INS_USAGE.md - Instructions d'Utilisation*
*VAL-Galaxies_primordiales v1.0*
