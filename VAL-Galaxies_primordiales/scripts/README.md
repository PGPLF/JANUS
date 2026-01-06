# Scripts COSMOS2025 + Zenodo

Scripts Python et Bash pour le workflow complet COSMOS2025 → Zenodo.

---

## Scripts Disponibles

### 1. validate_cosmos2025_complete.py

**Usage**: Phase 3 - Validation téléchargement

```bash
python scripts/validate_cosmos2025_complete.py
```

**Fonction**:
- Valide que tous les fichiers COSMOS2025 sont téléchargés
- Vérifie tailles et lisibilité FITS
- 13 validations:
  - Master catalog (784k sources)
  - 6 extensions (PHOT, LEPHARE, CIGALE, MORPH, SPEC-Z, FLAGS)
  - 20 detection images
  - 20 segmentation maps
  - LePhare produits
  - CIGALE produits

**Sortie attendue**:
```
✅ Téléchargement complet VALIDÉ
13/13 validations réussies (100%)
```

---

### 2. extract_cosmos2025_highz.py

**Usage**: Phase 4 - Extraction galaxies z>8

```bash
# Extraction standard (z >= 8)
python scripts/extract_cosmos2025_highz.py --zmin 8.0

# Extraction personnalisée
python scripts/extract_cosmos2025_highz.py --zmin 10.0 --zmax 12.0

# Sans filtres qualité
python scripts/extract_cosmos2025_highz.py --zmin 8.0 --no-quality-cuts
```

**Arguments**:
- `--catalog`: Chemin catalogue (défaut: `data/jwst/raw/cosmos2025/catalog/COSMOS-Web_master_v2.0.fits`)
- `--zmin`: Redshift minimum (défaut: 8.0)
- `--zmax`: Redshift maximum (défaut: 15.0)
- `--output`: Dossier sortie (défaut: `data/jwst/processed/cosmos2025/`)
- `--no-quality-cuts`: Désactiver filtres qualité

**Sortie**:
- `cosmos2025_highz_z8.fits` (FITS)
- `cosmos2025_highz_z8.csv` (CSV)

**Colonnes extraites**:
- `ID`, `RA`, `DEC`
- `z_phot`, `z_phot_68_low`, `z_phot_68_high`
- `log_mstar_lp`, `log_mstar_cigale`
- `log_sfr_cigale`
- `mag_f150w`, `mag_f277w`, `mag_f444w`
- `chi2_lp`, `chi2_cigale`

**Résultat attendu**: ~5,000-10,000 galaxies z>8

---

### 3. prepare_zenodo_archives.sh

**Usage**: Phase 5 - Préparation archives Zenodo

```bash
bash scripts/prepare_zenodo_archives.sh
```

**Fonction**:
- Crée structure `COSMOS2025_JANUS/`
- Copie templates (README, CITATION, LICENSE)
- Organise données par catégorie
- Crée 6-7 archives < 50 GB chacune

**Archives créées**:
1. `COSMOS2025_catalog_segmaps.zip` (~8 GB)
2. `detection_part1.tar.gz` (~18 GB)
3. `detection_part2.tar.gz` (~18 GB)
4. `COSMOS2025_lephare.tar.gz` (~30-40 GB)
5. `cigale_seds_v2.0.tar.gz` (~30-40 GB)
6. `COSMOS2025_JANUS_analysis.tar.gz` (variable)

**Structure créée**:
```
data/zenodo_upload/COSMOS2025_JANUS/
├── README.md
├── CITATION.cff
├── LICENSE
├── 00_catalog/
├── 01_detection_images/
├── 02_segmentation_maps/
├── 03_lephare/
├── 04_cigale/
├── 05_janus_analysis/
└── scripts/
```

---

### 4. zenodo_upload.py

**Usage**: Phase 6 - Upload vers Zenodo

```bash
# Définir token et deposition_id
export ZENODO_TOKEN='votre_token'
export DEPOSITION_ID='votre_deposition_id'

# Installer tqdm pour progress bar (optionnel)
pip install tqdm

# Lancer upload
python scripts/zenodo_upload.py
```

**Prérequis**:
- Token Zenodo (`$ZENODO_TOKEN`)
- Deposition ID (`$DEPOSITION_ID`)
- Archives préparées (Phase 5)

**Fonction**:
- Upload 6-7 archives via API Zenodo
- Barre de progression pour chaque fichier
- Gestion erreurs avec retry possible
- Vérification tailles < 50 GB

**Temps estimé**: 2-4 heures (selon connexion)

---

## Workflow Complet

### Phase 3: Validation (30 min)

```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
source /Users/pg-mac01/PythonProject/.venv/bin/activate

python scripts/validate_cosmos2025_complete.py
```

**Attendu**: ✅ 13/13 validations réussies

---

### Phase 4: Extraction z>8 (30 min)

```bash
python scripts/extract_cosmos2025_highz.py --zmin 8.0
```

**Résultat**: `data/jwst/processed/cosmos2025/cosmos2025_highz_z8.fits`

**Utilisation**:
```python
from astropy.table import Table

# Charger extraction
highz = Table.read('data/jwst/processed/cosmos2025/cosmos2025_highz_z8.fits')

print(f"N sources: {len(highz)}")
print(f"z range: {highz['z_phot'].min():.2f} - {highz['z_phot'].max():.2f}")
```

---

### Phase 5: Archives Zenodo (1-2h)

```bash
bash scripts/prepare_zenodo_archives.sh
```

**Vérification**:
```bash
# Voir archives créées
ls -lh data/zenodo_upload/*.zip data/zenodo_upload/*.tar.gz

# Vérifier tailles (toutes < 50 GB)
du -h data/zenodo_upload/*.zip data/zenodo_upload/*.tar.gz
```

---

### Phase 6: Upload Zenodo (2-4h)

```bash
# Configuration
export ZENODO_TOKEN='votre_token_depuis_zenodo'
export DEPOSITION_ID='1234567'  # Depuis URL draft

# Upload
python scripts/zenodo_upload.py
```

**Confirmation demandée avant upload**:
```
Taille totale: 120.45 GB
Temps estimé: 12-24 min (selon connexion)

Continuer upload? (oui/non):
```

---

## Dépendances

### Python Packages

```bash
pip install numpy astropy requests

# Optionnel mais recommandé (progress bar)
pip install tqdm
```

### Packages Déjà Installés

Si environnement configuré selon `requirements.txt`:
- ✅ numpy
- ✅ scipy
- ✅ astropy
- ✅ matplotlib
- ✅ h5py
- ✅ pandas

**Vérification**:
```bash
python -c "import numpy, astropy, requests; print('✓ OK')"
```

---

## Troubleshooting

### Erreur: "Module 'astropy' not found"

```bash
source /Users/pg-mac01/PythonProject/.venv/bin/activate
pip install astropy
```

### Erreur: "Fichier non trouvé"

Vérifier chemins:
```bash
# Téléchargement complet?
du -sh data/jwst/raw/cosmos2025/

# Structure OK?
tree data/ -L 3
```

### Erreur Upload Zenodo: "401 Unauthorized"

Token invalide:
```bash
# Vérifier token
echo $ZENODO_TOKEN

# Redéfinir
export ZENODO_TOKEN='nouveau_token'
```

### Erreur Upload: "Request Entity Too Large"

Fichier > 50 GB:
```bash
# Découper avec split
split -b 45G fichier.tar.gz fichier.tar.gz.part_
```

---

## Références

### Documentation Complète

| Document | Description |
|----------|-------------|
| `INS-COSMOS2025.md` | Description catalogue COSMOS2025 |
| `INS-COSMOS2025_HEBERGEMENT.md` | Plan 7 phases détaillé |
| `INS-ZENODO.md` | Infrastructure Zenodo complète |
| `GUIDE_ZENODO_SETUP.md` | Guide setup étape par étape |
| `PLAN_EXECUTION_COSMOS2025_ZENODO.md` | Plan exécution résumé |

**Localisation**: `JANUS/JANUS-INSTRUCTIONS/` et `JANUS/VAL-Galaxies_primordiales/`

---

## Support

**Issues**: https://github.com/PGPLF/JANUS/issues
**Documentation**: Voir fichiers `INS-*.md` dans `JANUS-INSTRUCTIONS/`

---

**Dernière mise à jour**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales - Phase 3
