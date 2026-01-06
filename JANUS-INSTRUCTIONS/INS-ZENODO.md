# INS-ZENODO - Infrastructure Professionnelle Zenodo

**Source**: Zenodo (https://zenodo.org)
**Date de création**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales - Phase 3
**Objectif**: Hébergement pérenne données COSMOS2025 avec DOI citable

---

## Vue d'Ensemble

**Zenodo** est un dépôt de données scientifiques open-access hébergé par le CERN, offrant:
- ✅ **Stockage pérenne** (50 Go/fichier, illimité en nombre)
- ✅ **DOI citable** pour chaque dépôt
- ✅ **Versioning** automatique
- ✅ **Intégration GitHub** (releases automatiques)
- ✅ **Licence libre** (CC0, CC-BY, etc.)
- ✅ **Reconnaissance scientifique** internationale

### Cas d'Usage JANUS

**Dépôt prévu**: `COSMOS2025_JANUS_Dataset`

**Contenu** (~80-130 GB total):
1. **Données brutes COSMOS2025** complètes (~80-130 GB)
   - Catalogue maître 784k galaxies
   - Detection images (20 tiles)
   - Segmentation maps
   - LePhare SEDs + PDFz
   - CIGALE SEDs

2. **Analyses JANUS** (taille variable)
   - MCMC chains (JANUS vs ΛCDM)
   - Sélections haute-z
   - Résultats comparatifs
   - Scripts reproduction

---

## Structure du Dépôt Zenodo

### Architecture Complète

```
COSMOS2025_JANUS/
│
├── README.md                           # Description générale (template ci-dessous)
├── CITATION.cff                        # Citation standard (template ci-dessous)
├── LICENSE                             # CC-BY-4.0 recommandée
│
├── 00_catalog/
│   ├── COSMOS-Web_master_v2.0.fits               # Catalogue complet 6 extensions (~5 GB)
│   ├── extensions_separate/                       # Extensions individuelles
│   │   ├── cosmos_web_phot_v2.0.fits             # Photométrie
│   │   ├── cosmos_web_lephare_v2.0.fits          # Photo-z
│   │   ├── cosmos_web_cigale_v2.0.fits           # SED fitting
│   │   ├── cosmos_web_morph_v2.0.fits            # Morphologie
│   │   ├── cosmos_web_specz_v2.0.fits            # Spectro-z
│   │   └── cosmos_web_flags_v2.0.fits            # Flags qualité
│   └── catalog_README.md                         # Description colonnes
│
├── 01_detection_images/
│   ├── detection_images_tiles_01-10.tar.gz       # Tiles 1-10 (~18 GB)
│   └── detection_images_tiles_11-20.tar.gz       # Tiles 11-20 (~18 GB)
│
├── 02_segmentation_maps/
│   └── segmentation_maps_all_tiles.tar.gz        # Toutes les segmaps (~160 MB)
│
├── 03_lephare/
│   ├── lephare_pdfz_v2.0.pkl                     # Distributions redshift (~5-10 GB)
│   └── lephare_seds_v2.0.tar.gz                  # Best-fit SEDs 784k sources (~20-40 GB)
│
├── 04_cigale/
│   └── cigale_seds_v2.0.tar.gz                   # Best-fit SEDs 784k sources (~20-40 GB)
│
├── 05_janus_analysis/                            # Analyses spécifiques JANUS
│   ├── mcmc_chains/
│   │   ├── LCDM_baseline.h5                      # MCMC ΛCDM
│   │   ├── JANUS_bimetric.h5                     # MCMC JANUS
│   │   └── chains_README.md
│   ├── bootstrap/
│   │   └── bootstrap_results.tar.gz              # Résultats bootstrap
│   ├── jwst_highz_selection/
│   │   ├── cosmos2025_highz_z8.fits              # Sélection z>8
│   │   ├── impossible_galaxies.fits              # Galaxies "impossibles"
│   │   └── selection_criteria.md
│   └── comparative_fits/
│       ├── LCDM_vs_JANUS_stats.csv
│       └── figures/
│
├── 06_mp_gadget_simulations/                     # Simulations (si applicable)
│   ├── snapshots/
│   ├── ics/
│   └── param_files/
│
└── scripts/
    ├── reproduction_pipeline.py                  # Pipeline complet
    ├── mcmc_analysis.py
    ├── extract_highz.py
    ├── requirements.txt
    └── environment.yml
```

### Découpage Archives (limite 50 GB/fichier Zenodo)

| Archive | Contenu | Taille estimée |
|---------|---------|----------------|
| `COSMOS2025_catalog_segmaps.zip` | Catalogue + segmentation | ~5 GB |
| `COSMOS2025_detection_part1.tar.gz` | Detection images tiles 1-10 | ~18 GB |
| `COSMOS2025_detection_part2.tar.gz` | Detection images tiles 11-20 | ~18 GB |
| `COSMOS2025_lephare.tar.gz` | PDFz + SEDs LePhare | ~30-40 GB |
| `COSMOS2025_cigale.tar.gz` | SEDs CIGALE | ~30-40 GB |
| `COSMOS2025_JANUS_analysis.tar.gz` | Analyses JANUS complètes | Variable |

**Total**: 6-7 archives (~100-130 GB)

---

## Template README.md Principal

```markdown
# COSMOS2025_JANUS Dataset

**DOI**: [10.5281/zenodo.XXXXXXX] (généré automatiquement par Zenodo)

## Description

Complete dataset for the JANUS bimetric cosmology validation project using COSMOS-Web DR1 (Data Release 1) primordial galaxies observations from JWST.

**Project**: VAL-Galaxies_primordiales
**Model**: JANUS Bimetric Cosmology
**Comparison**: ΛCDM Standard Model
**Date**: January 2026

### Contents

This dataset includes:

1. **COSMOS-Web DR1 Complete Catalog** (~784,000 galaxies)
   - JWST NIRCam + HST + ground-based photometry
   - LePhare photometric redshifts and stellar masses
   - CIGALE SED fitting (masses, SFR, attenuation)
   - Morphological parameters
   - Spectroscopic redshifts (when available)

2. **Detection Images and Segmentation Maps** (20 tiles)
   - JWST NIRCam detection images (0.03"/pixel)
   - Source segmentation maps

3. **SED Fitting Products**
   - LePhare: redshift probability distributions (PDFz) + best-fit SEDs
   - CIGALE: best-fit SEDs for all sources

4. **JANUS Specific Analyses**
   - MCMC chains (JANUS vs ΛCDM comparison)
   - High-z galaxy selections (z > 8)
   - "Impossible galaxies" sample
   - Bootstrap analysis results
   - Comparative statistics

5. **Reproduction Scripts**
   - Complete Python pipeline
   - Environment configuration
   - Documentation

## COSMOS-Web DR1 Source

**Original Data**: Institut d'Astrophysique de Paris (IAP)
**URL**: https://cosmos2025.iap.fr/
**Paper**: Shuntov, M., Akins, H. B., Paquereau, L., Casey, C. M., Ilbert, O., et al. (2025). "COSMOS2025: The COSMOS-Web galaxy catalog of photometry, morphology, and physical parameters from JWST, HST and ground-based imaging", ApJ (submitted).

## JANUS Model References

**JANUS Cosmology**:
- Petit, J.-P., d'Agostini, G. (2014). "Cosmological bimetric model with interacting positive and negative masses and two different speeds of light", Astrophysics and Space Science, 354, 611-615.
- Petit, J.-P., d'Agostini, G. (2015). "Negative mass hypothesis and the nature of dark energy and dark matter", Astrophysics and Space Science, 357, 67.

## Data Structure

See individual `README.md` files in each subdirectory for detailed descriptions:
- `00_catalog/catalog_README.md` - Column descriptions
- `05_janus_analysis/chains_README.md` - MCMC methodology
- `05_janus_analysis/jwst_highz_selection/selection_criteria.md` - High-z selection

## Usage

### Requirements

```bash
# Python 3.10+
pip install -r scripts/requirements.txt

# Or conda
conda env create -f scripts/environment.yml
```

### Quick Start

```python
from astropy.io import fits
import h5py

# Load catalog
hdul = fits.open('00_catalog/COSMOS-Web_master_v2.0.fits')
lephare = hdul['LEPHARE'].data  # Photo-z
cigale = hdul['CIGALE'].data    # SED fitting

# Load MCMC chains
with h5py.File('05_janus_analysis/mcmc_chains/JANUS_bimetric.h5', 'r') as f:
    chains = f['mcmc/chain'][:]
    lnprob = f['mcmc/lnprobability'][:]
```

See `scripts/reproduction_pipeline.py` for complete analysis workflow.

## Citation

If you use this dataset in your research, please cite:

### COSMOS-Web DR1 Catalog
```bibtex
@article{Shuntov2025,
  author = {Shuntov, M. and Akins, H. B. and Paquereau, L. and Casey, C. M. and Ilbert, O. and others},
  title = {COSMOS2025: The COSMOS-Web galaxy catalog of photometry, morphology, and physical parameters from JWST, HST and ground-based imaging},
  journal = {ApJ},
  year = {2025},
  note = {submitted},
  url = {https://cosmos2025.iap.fr/}
}
```

### This Dataset
```bibtex
@dataset{COSMOS2025_JANUS,
  author = {[Your Name/Team]},
  title = {COSMOS2025_JANUS: Complete dataset for JANUS bimetric cosmology validation},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

### JANUS Model
```bibtex
@article{Petit2014,
  author = {Petit, J.-P. and d'Agostini, G.},
  title = {Cosmological bimetric model with interacting positive and negative masses and two different speeds of light},
  journal = {Astrophysics and Space Science},
  volume = {354},
  pages = {611--615},
  year = {2014},
  doi = {10.1007/s10509-014-2106-5}
}
```

## License

**COSMOS-Web DR1 Data**: Please refer to original COSMOS2025 data policy at https://cosmos2025.iap.fr/

**JANUS Analysis Scripts and Results**: CC-BY-4.0

You are free to:
- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

## Contact

**Project**: VAL-Galaxies_primordiales
**Repository**: https://github.com/PGPLF/JANUS
**Issues**: https://github.com/PGPLF/JANUS/issues

## Version History

- **v1.0** (2026-01-XX): Initial release
  - Complete COSMOS-Web DR1 catalog
  - JANUS vs ΛCDM MCMC analysis
  - High-z galaxy selections

## Acknowledgments

This work uses data from the COSMOS-Web JWST program (PI: Casey, PID: 1727) and the COSMOS survey. We thank the IAP COSMOS team for making the DR1 catalog publicly available.

---

**Last updated**: 2026-01-XX
```

---

## Template CITATION.cff

```yaml
cff-version: 1.2.0
message: "If you use this dataset, please cite it as below."
authors:
  - family-names: "[Your Last Name]"
    given-names: "[Your First Name]"
    orcid: "https://orcid.org/XXXX-XXXX-XXXX-XXXX"
title: "COSMOS2025_JANUS: Complete dataset for JANUS bimetric cosmology validation"
version: 1.0
doi: 10.5281/zenodo.XXXXXXX
date-released: 2026-01-XX
url: "https://github.com/PGPLF/JANUS"
repository-code: "https://github.com/PGPLF/JANUS/tree/master/VAL-Galaxies_primordiales"
keywords:
  - cosmology
  - JANUS model
  - bimetric gravity
  - JWST
  - primordial galaxies
  - COSMOS-Web
  - high-redshift galaxies
  - MCMC
  - Bayesian inference
license: CC-BY-4.0
```

---

## Template catalog_README.md

```markdown
# COSMOS-Web DR1 Catalog Description

## Master Catalog: COSMOS-Web_master_v2.0.fits

**Total sources**: 784,016 galaxies
**Area**: ~0.54 deg² (COSMOS field)
**Redshift range**: z ~ 0-14 (photometric)

### HDU Extensions (6 total)

1. **PHOT** - Photométrie multi-bandes
   - JWST NIRCam: F115W, F150W, F277W, F444W
   - HST ACS: F814W
   - HST WFC3: F125W, F160W
   - Ground-based: u, g, r, i, z, Y (Subaru, CFHT, VLT)

2. **MORPH** - Paramètres morphologiques
   - Sérsic profiles
   - Effective radius
   - Axis ratio
   - Position angle

3. **LEPHARE** - Photo-z et masses stellaires
   - `Z_PHOT`: Redshift photométrique
   - `Z_PHOT_68_LOW`, `Z_PHOT_68_HIGH`: Intervalle confiance 68%
   - `LOG_MSTAR`: log10(M*/M☉) masse stellaire
   - `CHI2_BEST`: χ² du meilleur fit

4. **CIGALE** - SED fitting complet
   - `LOG_MSTAR`: log10(M*/M☉) masse stellaire
   - `LOG_SFR`: log10(SFR/M☉/yr) star formation rate
   - `AV`: Atténuation visuelle (magnitudes)
   - `CHI2_RED`: χ² réduit

5. **SPEC-Z** - Redshifts spectroscopiques
   - Sous-échantillon avec spectroscopie confirmée
   - Qualité et source du redshift

6. **FLAGS** - Flags qualité et sélection
   - `USE_PHOT`: Photométrie utilisable (0/1)
   - `STAR_FLAG`: Étoile identifiée (0/1)
   - Flags contamination, saturation, etc.

### Key Columns for JANUS Analysis

**Redshift**:
- `LEPHARE['Z_PHOT']` - Primary photo-z
- `LEPHARE['Z_PHOT_68_LOW/HIGH']` - Uncertainties
- `SPEC-Z['Z_SPEC']` - Spectroscopic (when available)

**Stellar Mass**:
- `LEPHARE['LOG_MSTAR']` - From template fitting
- `CIGALE['LOG_MSTAR']` - From full SED fitting (preferred)

**Star Formation Rate**:
- `CIGALE['LOG_SFR']` - Primary SFR estimate

**UV Magnitudes** (for luminosity functions):
- `PHOT['MAG_AUTO_F150W']` - Rest-frame UV proxy at z~8
- `PHOT['MAG_AUTO_F277W']` - Rest-frame UV proxy at z~10

**Quality Control**:
- `FLAGS['USE_PHOT'] == 1` - Good photometry
- `FLAGS['STAR_FLAG'] == 0` - Not a star
- `LEPHARE['CHI2_BEST'] < 10` - Reasonable fit
- `CIGALE['CHI2_RED'] < 5` - Acceptable SED fit

## Separate Extensions

Alternatively available as individual files:
- `cosmos_web_phot_v2.0.fits` (~2-3 GB)
- `cosmos_web_lephare_v2.0.fits` (~1-2 GB)
- `cosmos_web_cigale_v2.0.fits` (~1-2 GB)
- `cosmos_web_morph_v2.0.fits` (~500 MB)
- `cosmos_web_specz_v2.0.fits` (~50 MB)
- `cosmos_web_flags_v2.0.fits` (~100 MB)

## Detection Images

**Format**: FITS
**Resolution**: 0.03"/pixel (JWST NIRCam)
**Size**: ~1.8 GB per tile
**Tiles**: 20 total covering COSMOS-Web footprint

## Segmentation Maps

**Format**: FITS (integer IDs)
**Size**: ~8 MB per tile
**Usage**: Source IDs match catalog `ID` column

## LePhare Products

**PDFz** (`lephare_pdfz_v2.0.pkl`):
- Python pickle file
- Redshift probability distributions for all sources
- Load with: `import pickle; pdfz = pickle.load(open(file, 'rb'))`

**SEDs** (`lephare_seds_v2.0.tar.gz`):
- Best-fit spectral energy distributions
- One file per source (784k files)
- Format: ASCII columns (wavelength, flux)

## CIGALE Products

**SEDs** (`cigale_seds_v2.0.tar.gz`):
- Best-fit SEDs from full SED fitting
- One file per source (784k files)
- Format: ASCII columns (wavelength, flux, model components)

---

**For detailed column descriptions**: See official COSMOS2025 README at https://cosmos2025.iap.fr/catalog.html
```

---

## Métadonnées Zenodo

### Champs Obligatoires

**Lors de l'upload sur Zenodo**, remplir:

| Champ | Valeur |
|-------|--------|
| **Upload type** | Dataset |
| **Title** | COSMOS2025_JANUS: Complete dataset for JANUS bimetric cosmology validation |
| **Authors** | [Votre nom] (+ ORCID si disponible) |
| **Description** | Complete COSMOS-Web DR1 catalog (~784k galaxies) and JANUS bimetric cosmology analysis for primordial galaxies validation. Includes photometry, photo-z, SED fitting, MCMC chains, and high-z selections. |
| **Version** | 1.0 |
| **License** | Creative Commons Attribution 4.0 International (CC-BY-4.0) |
| **Keywords** | cosmology, JANUS model, bimetric gravity, JWST, COSMOS-Web, high-redshift galaxies, primordial galaxies, MCMC, Bayesian inference, dark matter, dark energy |
| **Related identifiers** | https://cosmos2025.iap.fr/ (isSupplementTo)<br>https://github.com/PGPLF/JANUS (isDocumentedBy) |
| **Contributors** | COSMOS-Web Team (DataCollector)<br>IAP CANDIDE (HostingInstitution) |
| **Subjects** | Astronomy (FOS: Physical sciences)<br>Cosmology and Nongalactic Astrophysics |
| **Funding** | [Si applicable] |

---

## Workflow Upload Zenodo

### Étape 1: Création Compte Zenodo

1. Aller sur https://zenodo.org
2. Créer compte (connexion via ORCID ou GitHub recommandée)
3. Vérifier email

### Étape 2: Nouveau Dépôt

1. Cliquer **"New upload"**
2. Remplir métadonnées (voir tableau ci-dessus)
3. **Ne pas publier immédiatement** (sauvegarder comme brouillon)

### Étape 3: Upload Fichiers

**Limite Zenodo**: 50 GB/fichier, illimité en nombre

**Méthodes d'upload**:

#### A. Interface Web (< 10 GB)
- Drag & drop dans l'interface
- Attendre fin upload avant de publier

#### B. API Zenodo (> 10 GB, recommandé)

```bash
# Obtenir ACCESS_TOKEN depuis Zenodo → Applications → Personal access tokens

# Créer nouveau dépôt
curl -X POST \
  https://zenodo.org/api/deposit/depositions \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"upload_type": "dataset", "title": "COSMOS2025_JANUS"}}'

# Récupérer DEPOSITION_ID de la réponse

# Upload fichier
BUCKET_URL="https://zenodo.org/api/files/BUCKET_ID"
curl -X PUT \
  "$BUCKET_URL/COSMOS2025_catalog_segmaps.zip" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  --data-binary "@COSMOS2025_catalog_segmaps.zip"

# Publier quand tous les fichiers sont uploadés
curl -X POST \
  https://zenodo.org/api/deposit/depositions/DEPOSITION_ID/actions/publish \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

#### C. Script Python (zenodo_upload.py)

```python
import requests
import os

ACCESS_TOKEN = "YOUR_TOKEN"
BASE_URL = "https://zenodo.org/api"

def create_deposition(metadata):
    """Créer nouveau dépôt"""
    r = requests.post(
        f"{BASE_URL}/deposit/depositions",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={"metadata": metadata}
    )
    return r.json()

def upload_file(deposition_id, filepath):
    """Upload fichier vers dépôt"""
    bucket_url = f"{BASE_URL}/deposit/depositions/{deposition_id}/files"
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as f:
        r = requests.put(
            f"{bucket_url}/{filename}",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            data=f
        )
    return r.json()

def publish_deposition(deposition_id):
    """Publier dépôt (génère DOI)"""
    r = requests.post(
        f"{BASE_URL}/deposit/depositions/{deposition_id}/actions/publish",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
    )
    return r.json()

# Usage
metadata = {
    "upload_type": "dataset",
    "title": "COSMOS2025_JANUS Dataset",
    "creators": [{"name": "Your Name", "orcid": "0000-0000-0000-0000"}],
    "description": "Complete COSMOS-Web DR1 for JANUS validation",
    "access_right": "open",
    "license": "CC-BY-4.0",
    "keywords": ["cosmology", "JANUS", "JWST", "COSMOS-Web"]
}

dep = create_deposition(metadata)
deposition_id = dep['id']

files = [
    "COSMOS2025_catalog_segmaps.zip",
    "COSMOS2025_detection_part1.tar.gz",
    # ... etc
]

for filepath in files:
    print(f"Uploading {filepath}...")
    upload_file(deposition_id, filepath)
    print(f"✓ {filepath} uploaded")

# Publier (génère DOI)
result = publish_deposition(deposition_id)
print(f"Published! DOI: {result['doi']}")
```

### Étape 4: Versioning

Pour mettre à jour le dataset:
1. Aller sur votre dépôt Zenodo
2. Cliquer **"New version"**
3. Modifier fichiers/métadonnées
4. Publier → nouveau DOI lié à l'ancien

---

## Intégration GitHub-Zenodo

### Activation GitHub Integration

1. Zenodo → Settings → GitHub
2. Synchroniser compte GitHub
3. Activer repo `PGPLF/JANUS`
4. **Effet**: Chaque release GitHub → archive Zenodo automatique avec DOI

### Workflow Recommandé

```bash
# Créer release GitHub
git tag -a v1.0-cosmos2025 -m "COSMOS2025 dataset v1.0"
git push origin v1.0-cosmos2025

# Sur GitHub: Create Release from tag
# → Zenodo détecte automatiquement et crée archive
```

**Avantage**: DOI automatique pour chaque version du code

---

## Checklist Upload Zenodo

### Préparation

- [ ] Compte Zenodo créé et vérifié
- [ ] ORCID ID obtenu (recommandé)
- [ ] ACCESS_TOKEN Zenodo généré (si API)
- [ ] Toutes les données téléchargées localement
- [ ] Archives créées (< 50 GB chacune)
- [ ] README.md principal rédigé
- [ ] CITATION.cff créé
- [ ] LICENSE file créé
- [ ] catalog_README.md rédigé

### Upload

- [ ] Nouveau dépôt créé sur Zenodo (brouillon)
- [ ] Métadonnées remplies (titre, auteurs, description, keywords)
- [ ] Licence sélectionnée (CC-BY-4.0)
- [ ] Related identifiers ajoutés (COSMOS2025, GitHub)
- [ ] Archive 1 uploadée: `COSMOS2025_catalog_segmaps.zip`
- [ ] Archive 2 uploadée: `COSMOS2025_detection_part1.tar.gz`
- [ ] Archive 3 uploadée: `COSMOS2025_detection_part2.tar.gz`
- [ ] Archive 4 uploadée: `COSMOS2025_lephare.tar.gz`
- [ ] Archive 5 uploadée: `COSMOS2025_cigale.tar.gz`
- [ ] Archive 6 uploadée: `COSMOS2025_JANUS_analysis.tar.gz`
- [ ] Vérification intégrité fichiers (checksums)

### Publication

- [ ] Revue finale métadonnées
- [ ] README visible dans preview
- [ ] Cliquer **"Publish"**
- [ ] DOI généré et copié
- [ ] Mise à jour README.md avec DOI final
- [ ] Mise à jour CITATION.cff avec DOI final
- [ ] Création release GitHub (optionnel)
- [ ] Annonce dépôt (Twitter/X, blog, etc.)

---

## Maintenance et Versioning

### Mise à Jour Dataset

**Quand créer nouvelle version?**
- Ajout de nouvelles analyses JANUS
- Mise à jour MCMC chains (convergence améliorée)
- Ajout de nouvelles sélections haute-z
- Corrections d'erreurs dans analyses

**Processus**:
1. Zenodo → Dépôt existant → **"New version"**
2. Modifier fichiers nécessaires
3. Mettre à jour README.md avec changelog
4. Publier → nouveau DOI (lié à l'ancien)

### Changelog Format

```markdown
## Version History

### v1.1 (2026-03-XX)
- Added MP-Gadget simulations snapshots
- Updated MCMC chains with extended burn-in
- Fixed typo in catalog_README.md

### v1.0 (2026-01-XX)
- Initial release
- Complete COSMOS-Web DR1 catalog
- JANUS vs ΛCDM MCMC analysis
```

---

## Troubleshooting

### Problème 1: Upload échoue (timeout)

**Cause**: Fichier trop gros ou connexion instable

**Solutions**:
- Utiliser API Zenodo plutôt qu'interface web
- Découper archive en parties plus petites (< 50 GB)
- Uploader en dehors heures de pointe
- Vérifier connexion internet stable

### Problème 2: DOI non généré après publication

**Cause**: Métadonnées incomplètes

**Solution**:
- Vérifier tous les champs obligatoires remplis
- Titre non vide
- Au moins un auteur avec nom complet
- Description > 20 caractères
- Licence sélectionnée

### Problème 3: Archive trop volumineuse (> 50 GB)

**Cause**: Limite Zenodo 50 GB/fichier

**Solution**:
- Découper avec `split`:
```bash
# Découper en parties de 45 GB
split -b 45G COSMOS2025_lephare.tar.gz COSMOS2025_lephare.tar.gz.part_

# Reconstruire (instructions dans README):
cat COSMOS2025_lephare.tar.gz.part_* > COSMOS2025_lephare.tar.gz
```

### Problème 4: Fichiers corrompus après upload

**Cause**: Upload interrompu ou erreur transfert

**Solution**:
- Vérifier checksums MD5/SHA256:
```bash
# Générer checksum local
md5sum COSMOS2025_catalog_segmaps.zip > checksums.txt

# Comparer avec checksum Zenodo (affiché après upload)
```
- Re-uploader fichier si nécessaire

---

## Ressources

### Documentation Officielle
- **Zenodo Help**: https://help.zenodo.org/
- **API Documentation**: https://developers.zenodo.org/
- **GitHub Integration**: https://docs.zenodo.org/deposit/integrations/github/

### Citation Standards
- **CITATION.cff Format**: https://citation-file-format.github.io/
- **DOI Handbook**: https://www.doi.org/the-identifier/resources/handbook

### Best Practices
- **FAIR Data Principles**: https://www.go-fair.org/fair-principles/
- **Research Data Management**: https://zenodo.org/communities/rdm/

---

## Contact et Support

**Zenodo Support**: support@zenodo.org
**COSMOS2025 Team**: cosmos2025@iap.fr
**JANUS Project**: https://github.com/PGPLF/JANUS/issues

---

**Document**: INS-ZENODO.md
**Version**: 1.0
**Date**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales
**Phase**: 3 (Hébergement Données)
