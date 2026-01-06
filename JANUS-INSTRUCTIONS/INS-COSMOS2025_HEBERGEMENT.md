# INS-COSMOS2025_HEBERGEMENT - Plan Hébergement Complet COSMOS2025

**Projet**: VAL-Galaxies_primordiales - Phase 3
**Date**: 6 Janvier 2026
**Objectif**: Téléchargement complet COSMOS2025 + Upload Zenodo professionnel
**Référence**: INS-ZENODO.md pour infrastructure Zenodo

---

## Vue d'Ensemble

### Stratégie d'Hébergement Complète

**Nouvelle approche**: **Téléchargement INTÉGRAL** + **Hébergement Zenodo professionnel**

**Raisons du changement**:
1. ✅ **Réutilisation future**: Données brutes pour d'autres études JANUS
2. ✅ **Pérennité**: Stockage Zenodo avec DOI citable
3. ✅ **Reconnaissance scientifique**: Publication dataset avec citation
4. ✅ **Collaboration**: Données accessibles à la communauté
5. ✅ **Versioning**: Zenodo gère les versions automatiquement

### Workflow Complet

```
Local (pg-mac01)              →         Zenodo (pérenne)
─────────────────                       ─────────────────
1. Télécharger COSMOS2025 complet       4. Créer archives optimisées
   (~100-130 GB)                           (< 50 GB chacune)

2. Valider intégrité                    5. Upload vers Zenodo
   (checksums, colonnes)                   (API ou interface)

3. Extraction z>8 locale                6. Publication avec DOI
   (pour Phase 3 immédiate)                (citable dans papier)
```

**Tailles estimées**:
- Local temporaire: **100-130 GB** (peut être nettoyé après upload)
- Zenodo permanent: **100-130 GB** (6-7 archives)
- Extraction z>8: **~500 MB** (conservé local)

---

## Inventaire Complet COSMOS2025

### Tous les Fichiers à Télécharger

| Catégorie | Fichier | Taille | Usage |
|-----------|---------|--------|-------|
| **Catalogue Master** | | | |
| | `COSMOS-Web_master_v2.0.fits` | ~8-10 GB | Toutes les 6 extensions ensemble |
| **Extensions Séparées** | | | |
| | `cosmos_web_phot_v2.0.fits` | ~2-3 GB | Photométrie multi-bandes |
| | `cosmos_web_lephare_v2.0.fits` | ~1-2 GB | Photo-z + masses stellaires |
| | `cosmos_web_cigale_v2.0.fits` | ~1-2 GB | SED fitting complet |
| | `cosmos_web_morph_v2.0.fits` | ~1 GB | Morphologie (Sérsic, etc.) |
| | `cosmos_web_specz_v2.0.fits` | ~100 MB | Redshifts spectroscopiques |
| | `cosmos_web_flags_v2.0.fits` | ~100 MB | Flags qualité |
| **Detection Images** | | | |
| | 20 tiles (~1.8 GB chacune) | ~36 GB | Images détection NIRCam |
| **Segmentation Maps** | | | |
| | 20 tiles (~8 MB chacune) | ~160 MB | Cartes segmentation |
| **LePhare Produits** | | | |
| | `lephare_pdfz_v2.0.pkl` | ~5-10 GB | Distributions P(z) |
| | `lephare_seds_v2.0.tar.gz` | ~20-40 GB | SEDs 784k sources |
| **CIGALE Produits** | | | |
| | `cigale_seds_v2.0.tar.gz` | ~20-40 GB | SEDs 784k sources |

**Total COSMOS2025 complet**: **~100-130 GB**

### Décision Catalogue Master vs Extensions

**Recommandation**: **Télécharger les DEUX** pour Zenodo
- Master (~8-10 GB): Pour utilisateurs voulant tout d'un coup
- Extensions séparées (~6-7 GB): Pour utilisateurs ciblés
- Coût espace: +8-10 GB mais meilleure accessibilité

---

## Plan d'Implémentation - 7 Phases

### Phase 1: Préparation Infrastructure Locale (15 min)

**Objectif**: Créer structure complète + vérifier ressources

**Actions**:
```bash
# Vérifier espace disque (besoin 150 GB disponible: 130 GB données + 20 GB travail)
df -h /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/data/

# Créer structure locale
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
mkdir -p data/jwst/raw/cosmos2025/{catalog,detection_images,segmentation_maps,lephare,cigale}
mkdir -p data/jwst/processed/cosmos2025/
mkdir -p data/zenodo_upload/COSMOS2025_JANUS/

# Vérifier structure
tree data/ -L 4
```

**Validation**:
- [ ] Espace disque >= 150 GB libre
- [ ] Structure répertoires créée
- [ ] Permissions OK

---

### Phase 2: Téléchargement Complet COSMOS2025 (2-4 heures)

**Objectif**: Télécharger TOUTES les données COSMOS2025

**Ordre de téléchargement** (par priorité pour Phase 3):

#### 2.1 Catalogue Complet (30-60 min)

```bash
cd data/jwst/raw/cosmos2025/catalog/

# Master catalog (toutes extensions)
wget https://cosmos2025.iap.fr/data/COSMOS-Web_master_v2.0.fits

# Extensions séparées (pour flexibilité Zenodo)
wget https://cosmos2025.iap.fr/data/cosmos_web_phot_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_lephare_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_cigale_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_morph_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_specz_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_flags_v2.0.fits
```

**Validation**:
```bash
# Vérifier tailles
ls -lh data/jwst/raw/cosmos2025/catalog/
```

#### 2.2 Detection Images (1-2 heures)

```bash
cd data/jwst/raw/cosmos2025/detection_images/

# Télécharger tarball complet ou tiles individuelles
# Option A: Tarball (si disponible)
wget https://cosmos2025.iap.fr/data/detection_images_all.tar.gz
tar -xzf detection_images_all.tar.gz

# Option B: Tiles individuelles (ajuster URLs selon site)
for i in {01..20}; do
  wget https://cosmos2025.iap.fr/data/detection_tile_${i}.fits
done
```

#### 2.3 Segmentation Maps (5 min)

```bash
cd data/jwst/raw/cosmos2025/segmentation_maps/

# Tarball ou tiles individuelles
wget https://cosmos2025.iap.fr/data/segmentation_maps_all.tar.gz
tar -xzf segmentation_maps_all.tar.gz
```

#### 2.4 LePhare Produits (1-2 heures)

```bash
cd data/jwst/raw/cosmos2025/lephare/

# PDFz (distributions redshift)
wget https://cosmos2025.iap.fr/data/lephare_pdfz_v2.0.pkl

# SEDs (peut être très gros)
wget https://cosmos2025.iap.fr/data/lephare_seds_v2.0.tar.gz
# Ne PAS extraire (garder tar.gz pour Zenodo)
```

#### 2.5 CIGALE Produits (1-2 heures)

```bash
cd data/jwst/raw/cosmos2025/cigale/

# SEDs CIGALE
wget https://cosmos2025.iap.fr/data/cigale_seds_v2.0.tar.gz
# Ne PAS extraire (garder tar.gz pour Zenodo)
```

**Validation Phase 2**:
```bash
# Vérifier tous les fichiers téléchargés
find data/jwst/raw/cosmos2025/ -type f -exec ls -lh {} \;

# Compter total
du -sh data/jwst/raw/cosmos2025/
# Attendu: ~100-130 GB
```

**Checklist**:
- [ ] Master catalog téléchargé
- [ ] 6 extensions séparées téléchargées
- [ ] 20 detection images téléchargées
- [ ] 20 segmentation maps téléchargées
- [ ] LePhare PDFz téléchargé
- [ ] LePhare SEDs tar.gz téléchargé
- [ ] CIGALE SEDs tar.gz téléchargé

---

### Phase 3: Validation Intégrité (30 min)

**Objectif**: Vérifier que tous les fichiers sont complets et utilisables

**Script validation**: `scripts/validate_cosmos2025_complete.py`

```python
"""
Validation intégrité complète COSMOS2025
"""
import os
from astropy.io import fits
import pickle

def validate_fits_file(filepath, expected_min_size_gb=0.1):
    """Valider fichier FITS"""
    if not os.path.exists(filepath):
        return False, f"Fichier manquant: {filepath}"

    # Vérifier taille
    size_gb = os.path.getsize(filepath) / (1024**3)
    if size_gb < expected_min_size_gb:
        return False, f"Fichier trop petit: {size_gb:.2f} GB < {expected_min_size_gb} GB"

    # Vérifier que FITS est lisible
    try:
        with fits.open(filepath) as hdul:
            n_sources = len(hdul[1].data)
            if n_sources < 700000:  # Attendu: ~784k
                return False, f"Trop peu de sources: {n_sources}"
        return True, f"OK ({n_sources} sources, {size_gb:.2f} GB)"
    except Exception as e:
        return False, f"Erreur lecture: {e}"

def validate_cosmos2025_download(base_dir='data/jwst/raw/cosmos2025/'):
    """Validation complète"""
    print("=" * 60)
    print("VALIDATION COSMOS2025 TÉLÉCHARGEMENT COMPLET")
    print("=" * 60)

    results = {}

    # 1. Catalogue master
    print("\n1. MASTER CATALOG")
    master_path = os.path.join(base_dir, 'catalog/COSMOS-Web_master_v2.0.fits')
    ok, msg = validate_fits_file(master_path, expected_min_size_gb=5.0)
    results['master'] = ok
    print(f"   Master: {'✓' if ok else '✗'} {msg}")

    # 2. Extensions séparées
    print("\n2. EXTENSIONS SÉPARÉES")
    extensions = {
        'phot': 2.0,
        'lephare': 1.0,
        'cigale': 1.0,
        'morph': 0.5,
        'specz': 0.05,
        'flags': 0.05
    }

    for ext, min_size in extensions.items():
        ext_path = os.path.join(base_dir, f'catalog/cosmos_web_{ext}_v2.0.fits')
        ok, msg = validate_fits_file(ext_path, expected_min_size_gb=min_size)
        results[f'ext_{ext}'] = ok
        print(f"   {ext.upper()}: {'✓' if ok else '✗'} {msg}")

    # 3. Detection images
    print("\n3. DETECTION IMAGES")
    det_dir = os.path.join(base_dir, 'detection_images/')
    if os.path.exists(det_dir):
        n_tiles = len([f for f in os.listdir(det_dir) if f.endswith('.fits')])
        results['detection'] = (n_tiles == 20)
        print(f"   Tiles: {'✓' if n_tiles == 20 else '✗'} {n_tiles}/20 trouvées")
    else:
        results['detection'] = False
        print(f"   Tiles: ✗ Dossier manquant")

    # 4. Segmentation maps
    print("\n4. SEGMENTATION MAPS")
    seg_dir = os.path.join(base_dir, 'segmentation_maps/')
    if os.path.exists(seg_dir):
        n_segmaps = len([f for f in os.listdir(seg_dir) if f.endswith('.fits')])
        results['segmentation'] = (n_segmaps == 20)
        print(f"   Segmaps: {'✓' if n_segmaps == 20 else '✗'} {n_segmaps}/20 trouvées")
    else:
        results['segmentation'] = False
        print(f"   Segmaps: ✗ Dossier manquant")

    # 5. LePhare
    print("\n5. LEPHARE PRODUITS")
    lp_pdfz = os.path.join(base_dir, 'lephare/lephare_pdfz_v2.0.pkl')
    lp_seds = os.path.join(base_dir, 'lephare/lephare_seds_v2.0.tar.gz')

    if os.path.exists(lp_pdfz):
        size_gb = os.path.getsize(lp_pdfz) / (1024**3)
        results['lp_pdfz'] = (size_gb > 0.5)
        print(f"   PDFz: {'✓' if size_gb > 0.5 else '✗'} {size_gb:.2f} GB")
    else:
        results['lp_pdfz'] = False
        print(f"   PDFz: ✗ Manquant")

    if os.path.exists(lp_seds):
        size_gb = os.path.getsize(lp_seds) / (1024**3)
        results['lp_seds'] = (size_gb > 10.0)
        print(f"   SEDs: {'✓' if size_gb > 10.0 else '✗'} {size_gb:.2f} GB")
    else:
        results['lp_seds'] = False
        print(f"   SEDs: ✗ Manquant")

    # 6. CIGALE
    print("\n6. CIGALE PRODUITS")
    cig_seds = os.path.join(base_dir, 'cigale/cigale_seds_v2.0.tar.gz')

    if os.path.exists(cig_seds):
        size_gb = os.path.getsize(cig_seds) / (1024**3)
        results['cig_seds'] = (size_gb > 10.0)
        print(f"   SEDs: {'✓' if size_gb > 10.0 else '✗'} {size_gb:.2f} GB")
    else:
        results['cig_seds'] = False
        print(f"   SEDs: ✗ Manquant")

    # Résumé
    print("\n" + "=" * 60)
    n_ok = sum(results.values())
    n_total = len(results)
    pct = 100 * n_ok / n_total
    print(f"RÉSULTAT: {n_ok}/{n_total} validations réussies ({pct:.1f}%)")

    if n_ok == n_total:
        print("✅ Téléchargement complet VALIDÉ")
        return True
    else:
        print("❌ Téléchargement INCOMPLET - voir détails ci-dessus")
        return False

if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    base = 'data/jwst/raw/cosmos2025/'
    validate_cosmos2025_download(base)
```

**Exécution**:
```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
source /Users/pg-mac01/PythonProject/.venv/bin/activate
python scripts/validate_cosmos2025_complete.py
```

**Validation Phase 3**:
- [ ] Master catalog lisible (784k sources)
- [ ] 6 extensions lisibles
- [ ] 20 detection images présentes
- [ ] 20 segmentation maps présentes
- [ ] LePhare PDFz + SEDs présents
- [ ] CIGALE SEDs présent
- [ ] Taille totale ~100-130 GB

---

### Phase 4: Extraction z>8 Locale (30 min)

**Objectif**: Extraire échantillon haute-z pour Phase 3 immédiate

**Script**: `scripts/extract_cosmos2025_highz.py` (déjà dans INS-COSMOS2025.md)

```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
source /Users/pg-mac01/PythonProject/.venv/bin/activate

# Extraction z>8 depuis master catalog
python scripts/extract_cosmos2025_highz.py \
  --catalog data/jwst/raw/cosmos2025/catalog/COSMOS-Web_master_v2.0.fits \
  --zmin 8.0 \
  --zmax 15.0 \
  --output data/jwst/processed/cosmos2025/

# Résultat attendu: cosmos2025_highz_z8.fits (~5-10k galaxies, ~500 MB)
```

**Validation**:
- [ ] Fichier `cosmos2025_highz_z8.fits` créé
- [ ] N sources 5000-10000 galaxies
- [ ] z_phot range 8.0-15.0
- [ ] Colonnes essentielles présentes (ID, RA, DEC, z_phot, log_mstar, log_sfr, mag_UV)

---

### Phase 5: Préparation Archives Zenodo (1-2 heures)

**Objectif**: Créer archives optimisées < 50 GB pour upload Zenodo

**Structure cible** (voir INS-ZENODO.md):
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

**Script préparation**: `scripts/prepare_zenodo_archives.sh`

```bash
#!/bin/bash
# Préparation archives Zenodo COSMOS2025_JANUS

BASE_RAW="data/jwst/raw/cosmos2025"
BASE_PROCESSED="data/jwst/processed/cosmos2025"
ZENODO_DIR="data/zenodo_upload/COSMOS2025_JANUS"

echo "Préparation archives Zenodo..."

# Créer structure
mkdir -p $ZENODO_DIR/{00_catalog/extensions_separate,01_detection_images,02_segmentation_maps,03_lephare,04_cigale,05_janus_analysis/{mcmc_chains,jwst_highz_selection,comparative_fits},scripts}

# Copier README et métadonnées (à créer manuellement)
cp templates/ZENODO_README.md $ZENODO_DIR/README.md
cp templates/CITATION.cff $ZENODO_DIR/CITATION.cff
cp templates/LICENSE $ZENODO_DIR/LICENSE

# 1. Catalogue (master + extensions)
echo "Archive 1: Catalogue..."
cp $BASE_RAW/catalog/COSMOS-Web_master_v2.0.fits $ZENODO_DIR/00_catalog/
cp $BASE_RAW/catalog/cosmos_web_*.fits $ZENODO_DIR/00_catalog/extensions_separate/

# 2. Detection images (split en 2 archives)
echo "Archive 2-3: Detection images..."
cd $BASE_RAW/detection_images/
ls *.fits | head -10 | tar -czf $ZENODO_DIR/01_detection_images/detection_part1.tar.gz -T -
ls *.fits | tail -10 | tar -czf $ZENODO_DIR/01_detection_images/detection_part2.tar.gz -T -
cd -

# 3. Segmentation maps
echo "Archive 3: Segmentation..."
cd $BASE_RAW/segmentation_maps/
tar -czf $ZENODO_DIR/02_segmentation_maps/segmentation_all.tar.gz *.fits
cd -

# 4. LePhare
echo "Archive 4: LePhare..."
cp $BASE_RAW/lephare/lephare_pdfz_v2.0.pkl $ZENODO_DIR/03_lephare/
cp $BASE_RAW/lephare/lephare_seds_v2.0.tar.gz $ZENODO_DIR/03_lephare/

# 5. CIGALE
echo "Archive 5: CIGALE..."
cp $BASE_RAW/cigale/cigale_seds_v2.0.tar.gz $ZENODO_DIR/04_cigale/

# 6. JANUS analysis
echo "Archive 6: JANUS analysis..."
cp $BASE_PROCESSED/cosmos2025_highz_z8.fits $ZENODO_DIR/05_janus_analysis/jwst_highz_selection/
# MCMC chains à ajouter quand disponibles
# cp results/mcmc/*.h5 $ZENODO_DIR/05_janus_analysis/mcmc_chains/

# Scripts reproduction
cp scripts/extract_cosmos2025_highz.py $ZENODO_DIR/scripts/
cp scripts/validate_cosmos2025_complete.py $ZENODO_DIR/scripts/
cp requirements.txt $ZENODO_DIR/scripts/
cp environment.yml $ZENODO_DIR/scripts/

echo "✓ Structure Zenodo préparée: $ZENODO_DIR"
du -sh $ZENODO_DIR
```

**Exécution**:
```bash
chmod +x scripts/prepare_zenodo_archives.sh
./scripts/prepare_zenodo_archives.sh
```

**Création archives finales** (< 50 GB chacune):

```bash
cd data/zenodo_upload/

# Archive 1: Catalogue + segmentation (~8 GB)
zip -r COSMOS2025_catalog_segmaps.zip \
  COSMOS2025_JANUS/00_catalog/ \
  COSMOS2025_JANUS/02_segmentation_maps/ \
  COSMOS2025_JANUS/README.md \
  COSMOS2025_JANUS/CITATION.cff \
  COSMOS2025_JANUS/LICENSE

# Archive 2: Detection part 1 (~18 GB)
# Déjà tar.gz dans 01_detection_images/detection_part1.tar.gz

# Archive 3: Detection part 2 (~18 GB)
# Déjà tar.gz dans 01_detection_images/detection_part2.tar.gz

# Archive 4: LePhare (~30-40 GB)
# Déjà tar.gz pour SEDs, copier PDFz aussi
cd COSMOS2025_JANUS/03_lephare/
tar -czf COSMOS2025_lephare.tar.gz *.pkl *.tar.gz
cd ../..

# Archive 5: CIGALE (~30-40 GB)
# Déjà tar.gz

# Archive 6: JANUS analysis (~variable)
tar -czf COSMOS2025_JANUS_analysis.tar.gz \
  COSMOS2025_JANUS/05_janus_analysis/ \
  COSMOS2025_JANUS/scripts/
```

**Vérification tailles**:
```bash
ls -lh *.zip *.tar.gz
# Toutes archives doivent être < 50 GB
```

**Validation Phase 5**:
- [ ] 6-7 archives créées
- [ ] Toutes < 50 GB
- [ ] README.md, CITATION.cff, LICENSE inclus
- [ ] Structure conforme INS-ZENODO.md

---

### Phase 6: Upload Zenodo (2-4 heures)

**Objectif**: Uploader toutes les archives vers Zenodo avec métadonnées

**Prérequis**:
- Compte Zenodo créé (https://zenodo.org)
- ORCID ID obtenu (recommandé)
- Personal Access Token généré

**Méthode recommandée**: **API Zenodo** (pour gros fichiers)

**Script upload**: `scripts/zenodo_upload.py`

```python
"""
Upload COSMOS2025_JANUS vers Zenodo
Voir INS-ZENODO.md pour détails complets
"""
import requests
import os
from tqdm import tqdm

ACCESS_TOKEN = os.environ.get('ZENODO_TOKEN')  # Définir dans .bashrc
BASE_URL = "https://zenodo.org/api"

def create_deposition():
    """Créer nouveau dépôt"""
    metadata = {
        "upload_type": "dataset",
        "title": "COSMOS2025_JANUS: Complete dataset for JANUS bimetric cosmology validation",
        "creators": [
            {"name": "[Votre Nom]", "orcid": "[Votre ORCID]"}
        ],
        "description": "Complete COSMOS-Web DR1 catalog (~784k galaxies) and JANUS bimetric cosmology analysis for primordial galaxies validation.",
        "access_right": "open",
        "license": "CC-BY-4.0",
        "keywords": ["cosmology", "JANUS model", "bimetric gravity", "JWST", "COSMOS-Web", "high-redshift galaxies", "MCMC"],
        "related_identifiers": [
            {"identifier": "https://cosmos2025.iap.fr/", "relation": "isSupplementTo"},
            {"identifier": "https://github.com/PGPLF/JANUS", "relation": "isDocumentedBy"}
        ]
    }

    r = requests.post(
        f"{BASE_URL}/deposit/depositions",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={"metadata": metadata}
    )
    return r.json()

def upload_large_file(bucket_url, filepath):
    """Upload fichier avec barre de progression"""
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    print(f"\nUploading {filename} ({filesize / (1024**3):.2f} GB)...")

    with open(filepath, 'rb') as f:
        with tqdm(total=filesize, unit='B', unit_scale=True) as pbar:
            def read_callback(chunk_size=8192):
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    pbar.update(len(chunk))
                    yield chunk

            r = requests.put(
                f"{bucket_url}/{filename}",
                headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                data=read_callback()
            )

    if r.status_code == 201:
        print(f"✓ {filename} uploaded successfully")
        return True
    else:
        print(f"✗ {filename} upload failed: {r.text}")
        return False

def main():
    """Pipeline complet upload Zenodo"""

    # 1. Créer dépôt
    print("Creating Zenodo deposition...")
    dep = create_deposition()
    deposition_id = dep['id']
    bucket_url = dep['links']['bucket']

    print(f"✓ Deposition created: ID {deposition_id}")

    # 2. Upload tous les fichiers
    archives = [
        "data/zenodo_upload/COSMOS2025_catalog_segmaps.zip",
        "data/zenodo_upload/COSMOS2025_JANUS/01_detection_images/detection_part1.tar.gz",
        "data/zenodo_upload/COSMOS2025_JANUS/01_detection_images/detection_part2.tar.gz",
        "data/zenodo_upload/COSMOS2025_JANUS/03_lephare/COSMOS2025_lephare.tar.gz",
        "data/zenodo_upload/COSMOS2025_JANUS/04_cigale/cigale_seds_v2.0.tar.gz",
        "data/zenodo_upload/COSMOS2025_JANUS_analysis.tar.gz"
    ]

    success = []
    for archive in archives:
        if os.path.exists(archive):
            if upload_large_file(bucket_url, archive):
                success.append(archive)
        else:
            print(f"⚠ File not found: {archive}")

    # 3. Publier (optionnel - commenter pour rester en brouillon)
    # publish_url = f"{BASE_URL}/deposit/depositions/{deposition_id}/actions/publish"
    # r = requests.post(publish_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
    # doi = r.json()['doi']
    # print(f"\n✓ Published! DOI: {doi}")

    print(f"\n✓ Upload complete: {len(success)}/{len(archives)} archives")
    print(f"   Deposition ID: {deposition_id}")
    print(f"   URL: https://zenodo.org/deposit/{deposition_id}")
    print("\n⚠ Don't forget to PUBLISH on Zenodo web interface to get DOI!")

if __name__ == '__main__':
    if not ACCESS_TOKEN:
        print("Error: Set ZENODO_TOKEN environment variable")
        print("  export ZENODO_TOKEN='your_token_here'")
        exit(1)

    main()
```

**Exécution**:
```bash
# 1. Définir token Zenodo
export ZENODO_TOKEN='your_personal_access_token'

# 2. Lancer upload
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
source /Users/pg-mac01/PythonProject/.venv/bin/activate
pip install requests tqdm

python scripts/zenodo_upload.py
```

**Validation Phase 6**:
- [ ] Deposition créée sur Zenodo
- [ ] 6-7 archives uploadées
- [ ] Métadonnées complètes
- [ ] Brouillon sauvegardé (ne PAS publier immédiatement)

---

### Phase 7: Publication et Documentation (30 min)

**Objectif**: Publier sur Zenodo + mettre à jour documentation projet

#### 7.1 Publication Zenodo

**Actions sur interface Zenodo**:
1. Aller sur https://zenodo.org/deposit/[DEPOSITION_ID]
2. Vérifier métadonnées
3. Vérifier que README.md est visible
4. Cliquer **"Publish"**
5. **Copier le DOI généré** (ex: `10.5281/zenodo.1234567`)

#### 7.2 Mise à Jour Documentation

**Mettre à jour README.md Zenodo avec DOI final**:
- Remplacer `[10.5281/zenodo.XXXXXXX]` par DOI réel
- Mettre à jour date de release

**Mettre à jour CITATION.cff avec DOI**:
```yaml
doi: 10.5281/zenodo.1234567  # DOI réel
date-released: 2026-01-XX     # Date réelle
```

**Mettre à jour DATA_SOURCES.md local**:
```markdown
### COSMOS2025 (COSMOS-Web DR1)

**Source**: Institut d'Astrophysique de Paris (IAP)
**URL originale**: https://cosmos2025.iap.fr/
**Zenodo DOI**: https://doi.org/10.5281/zenodo.1234567
**Date d'accès**: 6-XX Janvier 2026

**Téléchargement complet**: 100-130 GB
- Catalogue master + 6 extensions
- 20 detection images + segmentation maps
- LePhare + CIGALE SEDs complets

**Hébergement**: Zenodo (pérenne, citable)
**Extraction locale z>8**: `cosmos2025_highz_z8.fits` (~5-10k galaxies)
```

**Mettre à jour CHANGELOG_DATA.md**:
```markdown
## [2026-01-XX] - Phase 3 Hébergement Complet

### Téléchargé
- **COSMOS2025 complet**: ~100-130 GB
  - Catalogue master COSMOS-Web_master_v2.0.fits (784k galaxies)
  - 6 extensions séparées (PHOT, LEPHARE, CIGALE, MORPH, SPEC-Z, FLAGS)
  - 20 detection images NIRCam (~36 GB)
  - 20 segmentation maps (~160 MB)
  - LePhare produits (PDFz + SEDs, ~30-50 GB)
  - CIGALE produits (SEDs, ~30-40 GB)

### Hébergé sur Zenodo
- **DOI**: https://doi.org/10.5281/zenodo.1234567
- **Dataset**: COSMOS2025_JANUS v1.0
- **6 archives** (~100-130 GB total)
- **Citable** dans publications scientifiques

### Extraction locale
- **cosmos2025_highz_z8.fits**: ~5-10k galaxies z>8
- Prêt pour analyses Phase 3
```

**Validation Phase 7**:
- [ ] Dataset publié sur Zenodo
- [ ] DOI obtenu et copié
- [ ] README.md et CITATION.cff mis à jour avec DOI
- [ ] DATA_SOURCES.md et CHANGELOG_DATA.md mis à jour
- [ ] Announcement (optionnel): Twitter/X, blog, etc.

---

## Checklist Complète

### Phase 1: Préparation (15 min)
- [ ] Espace disque >= 150 GB vérifié
- [ ] Structure répertoires créée
- [ ] Permissions OK

### Phase 2: Téléchargement (2-4h)
- [ ] Master catalog (~8-10 GB)
- [ ] 6 extensions séparées (~6-7 GB)
- [ ] 20 detection images (~36 GB)
- [ ] 20 segmentation maps (~160 MB)
- [ ] LePhare PDFz + SEDs (~30-50 GB)
- [ ] CIGALE SEDs (~30-40 GB)
- [ ] **Total: ~100-130 GB**

### Phase 3: Validation (30 min)
- [ ] Script validation exécuté
- [ ] Master catalog lisible (784k sources)
- [ ] Extensions lisibles
- [ ] Detection/segmentation complètes
- [ ] LePhare/CIGALE complets

### Phase 4: Extraction z>8 (30 min)
- [ ] Script extraction exécuté
- [ ] `cosmos2025_highz_z8.fits` créé (~5-10k sources)
- [ ] Validation colonnes et redshifts

### Phase 5: Archives Zenodo (1-2h)
- [ ] Structure COSMOS2025_JANUS créée
- [ ] README.md, CITATION.cff, LICENSE créés
- [ ] 6-7 archives créées (< 50 GB chacune)
- [ ] Vérification tailles

### Phase 6: Upload Zenodo (2-4h)
- [ ] Compte Zenodo créé
- [ ] Access token obtenu
- [ ] Deposition créée
- [ ] 6-7 archives uploadées
- [ ] Métadonnées complètes
- [ ] Brouillon sauvegardé

### Phase 7: Publication (30 min)
- [ ] Dataset publié sur Zenodo
- [ ] DOI obtenu
- [ ] README/CITATION.cff Zenodo mis à jour
- [ ] DATA_SOURCES.md local mis à jour
- [ ] CHANGELOG_DATA.md local mis à jour

---

## Résumé Temporel

| Phase | Durée | Tâche Principale |
|-------|-------|------------------|
| Phase 1 | 15 min | Préparation infrastructure |
| Phase 2 | 2-4h | Téléchargement complet (100-130 GB) |
| Phase 3 | 30 min | Validation intégrité |
| Phase 4 | 30 min | Extraction z>8 locale |
| Phase 5 | 1-2h | Préparation archives Zenodo |
| Phase 6 | 2-4h | Upload vers Zenodo |
| Phase 7 | 30 min | Publication + documentation |
| **TOTAL** | **~7-11h** | Infrastructure complète professionnelle |

---

## Ressources Requises

### Espace Disque

| Localisation | Usage | Taille |
|--------------|-------|--------|
| `data/jwst/raw/cosmos2025/` | Données brutes téléchargées | 100-130 GB |
| `data/jwst/processed/cosmos2025/` | Extraction z>8 | ~500 MB |
| `data/zenodo_upload/COSMOS2025_JANUS/` | Archives Zenodo (temporaire) | 100-130 GB |
| **TOTAL temporaire** | (peut être nettoyé après upload) | **~200-260 GB** |
| **Permanent local** | Extraction z>8 uniquement | **~500 MB** |
| **Zenodo** | Hébergement pérenne | **100-130 GB** |

### Bande Passante

- **Download**: 100-130 GB (2-4h selon connexion)
- **Upload Zenodo**: 100-130 GB (2-4h selon connexion)
- **Total**: ~200-260 GB transfert

### Compute

- CPU: validation, archivage (1-2h)
- RAM: < 16 GB (lecture FITS)
- Python: numpy, astropy, requests, tqdm

---

## Nettoyage Post-Upload

**Une fois upload Zenodo validé**, libérer espace disque:

```bash
# Option 1: Supprimer données brutes (tout sur Zenodo)
rm -rf data/jwst/raw/cosmos2025/
rm -rf data/zenodo_upload/
# Économie: ~200-260 GB

# Option 2: Garder uniquement master catalog
rm -rf data/jwst/raw/cosmos2025/{detection_images,segmentation_maps,lephare,cigale}
rm -rf data/zenodo_upload/
# Économie: ~180-240 GB, garde ~10 GB catalogue

# Option 3: Tout garder localement
# Pas de nettoyage
# Total: ~200-260 GB permanent
```

**Recommandation**: Option 1 (tout supprimer) car:
- Données pérennes sur Zenodo
- Extraction z>8 locale conservée (~500 MB)
- Ré-téléchargement depuis Zenodo possible si besoin

---

## Troubleshooting

Voir **INS-ZENODO.md** section Troubleshooting pour:
- Problèmes upload Zenodo
- Fichiers corrompus
- Archives trop volumineuses
- DOI non généré

---

## Références

- **INS-COSMOS2025.md**: Description catalogue, script extraction z>8
- **INS-ZENODO.md**: Infrastructure Zenodo complète, templates, API
- **COSMOS2025 Official**: https://cosmos2025.iap.fr/
- **Zenodo**: https://zenodo.org

---

**Document**: INS-COSMOS2025_HEBERGEMENT.md
**Version**: 2.0 (Hébergement complet + Zenodo)
**Date**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales - Phase 3
**Référence**: INS-ZENODO.md
