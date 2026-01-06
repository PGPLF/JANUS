# PLAN D'EXÉCUTION - Infrastructure COSMOS2025 + Zenodo

**Projet**: VAL-Galaxies_primordiales - Phase 3
**Date**: 6 Janvier 2026
**Objectif**: Hébergement professionnel complet des données COSMOS2025 avec DOI citable

---

## 🎯 Résumé Exécutif

### Stratégie Globale

**Téléchargement COMPLET** des données COSMOS-Web DR1 (~100-130 GB) + **Publication Zenodo professionnelle** avec DOI citable.

### Raisons

1. ✅ **Réutilisation scientifique**: Données brutes disponibles pour d'autres études JANUS
2. ✅ **Pérennité**: Stockage Zenodo (CERN) avec garantie long-terme
3. ✅ **Citation**: DOI dans publications scientifiques
4. ✅ **Collaboration**: Données ouvertes pour la communauté
5. ✅ **Reconnaissance**: Dataset publié comme contribution scientifique

### Ressources Requises

| Ressource | Quantité | Usage |
|-----------|----------|-------|
| **Espace disque** | 150-200 GB | Temporaire (nettoyable après upload) |
| **Bande passante** | 200-260 GB | Download (100-130 GB) + Upload (100-130 GB) |
| **Temps total** | 7-11 heures | Automatisable en grande partie |
| **Compte Zenodo** | 1 | Gratuit, avec ORCID recommandé |

### Livrables Finaux

1. **Données locales**: Extraction z>8 (~500 MB) pour Phase 3 immédiate
2. **Zenodo**: Dataset complet (~100-130 GB) avec DOI
3. **Documentation**: README, CITATION.cff, scripts reproduction
4. **Tracabilité**: DATA_SOURCES.md, CHANGELOG_DATA.md mis à jour

---

## 📋 Plan Complet - 7 Phases

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                      WORKFLOW COMPLET                           │
└─────────────────────────────────────────────────────────────────┘

Phase 1: Préparation Infrastructure Locale (15 min)
   ↓
   └─→ Vérifier espace disque (150 GB)
   └─→ Créer structure répertoires

Phase 2: Téléchargement Complet COSMOS2025 (2-4h)
   ↓
   ├─→ Catalogue master + extensions (~15 GB)
   ├─→ Detection images 20 tiles (~36 GB)
   ├─→ Segmentation maps (~160 MB)
   ├─→ LePhare SEDs + PDFz (~30-50 GB)
   └─→ CIGALE SEDs (~30-40 GB)

Phase 3: Validation Intégrité (30 min)
   ↓
   └─→ Script Python validation automatique
   └─→ Vérification 784k sources

Phase 4: Extraction z>8 Locale (30 min)
   ↓
   └─→ cosmos2025_highz_z8.fits (~5-10k galaxies)
   └─→ Prêt pour Phase 3 analyses

Phase 5: Préparation Archives Zenodo (1-2h)
   ↓
   ├─→ Structure COSMOS2025_JANUS/
   ├─→ 6-7 archives < 50 GB chacune
   ├─→ README.md, CITATION.cff, LICENSE
   └─→ Scripts reproduction

Phase 6: Upload Zenodo (2-4h)
   ↓
   └─→ API Zenodo avec barre progression
   └─→ 6-7 archives uploadées
   └─→ Métadonnées complètes

Phase 7: Publication et Documentation (30 min)
   ↓
   ├─→ Publication Zenodo → DOI
   ├─→ Mise à jour DOI dans README/CITATION
   └─→ DATA_SOURCES.md et CHANGELOG_DATA.md

┌─────────────────────────────────────────────────────────────────┐
│  RÉSULTAT: Dataset COSMOS2025_JANUS v1.0 avec DOI citable      │
│  Local: 500 MB (z>8)  |  Zenodo: 100-130 GB (complet)         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Instructions de Référence

### Documents Créés

| Fichier | Taille | Contenu |
|---------|--------|---------|
| **INS-COSMOS2025.md** | 422 lignes | Description catalogue COSMOS2025, extraction z>8 |
| **INS-COSMOS2025_HEBERGEMENT.md** | 903 lignes | Plan 7 phases complet, scripts Python |
| **INS-ZENODO.md** | ~800 lignes | Infrastructure Zenodo, templates, API |

### Localisation

```
JANUS/
├── JANUS-INSTRUCTIONS/
│   ├── INS-COSMOS2025.md                    ← Description catalogue
│   ├── INS-COSMOS2025_HEBERGEMENT.md        ← Plan 7 phases
│   ├── INS-ZENODO.md                        ← Infrastructure Zenodo
│   └── README.md                            ← Index instructions (mis à jour)
│
└── VAL-Galaxies_primordiales/
    ├── PLAN_EXECUTION_COSMOS2025_ZENODO.md  ← CE DOCUMENT
    ├── scripts/
    │   ├── extract_cosmos2025_highz.py      ← À créer (dans INS-COSMOS2025.md)
    │   ├── validate_cosmos2025_complete.py  ← À créer (dans INS-HEBERGEMENT.md)
    │   ├── prepare_zenodo_archives.sh       ← À créer (dans INS-HEBERGEMENT.md)
    │   └── zenodo_upload.py                 ← À créer (dans INS-HEBERGEMENT.md)
    │
    ├── templates/                           ← À créer
    │   ├── ZENODO_README.md                 ← Template dans INS-ZENODO.md
    │   ├── CITATION.cff                     ← Template dans INS-ZENODO.md
    │   └── LICENSE                          ← CC-BY-4.0
    │
    └── data/
        ├── jwst/raw/cosmos2025/             ← Données téléchargées
        ├── jwst/processed/cosmos2025/       ← Extraction z>8
        └── zenodo_upload/COSMOS2025_JANUS/  ← Archives Zenodo
```

---

## ⏱️ Timeline Détaillée

### Phase 1: Préparation (15 min)

**Actions**:
```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/

# Vérifier espace disque
df -h data/

# Créer structure
mkdir -p data/jwst/raw/cosmos2025/{catalog,detection_images,segmentation_maps,lephare,cigale}
mkdir -p data/jwst/processed/cosmos2025/
mkdir -p data/zenodo_upload/COSMOS2025_JANUS/
```

**Validation**:
- [ ] >= 150 GB disponible
- [ ] Structure créée

---

### Phase 2: Téléchargement (2-4h)

**Référence**: INS-COSMOS2025_HEBERGEMENT.md Phase 2

**Ordre de priorité**:
1. **Catalogue** (30-60 min): Master + 6 extensions
2. **Detection images** (1-2h): 20 tiles
3. **Segmentation maps** (5 min): 20 tiles
4. **LePhare** (1-2h): PDFz + SEDs
5. **CIGALE** (1-2h): SEDs

**Commandes**:
```bash
cd data/jwst/raw/cosmos2025/catalog/

# Master catalog
wget https://cosmos2025.iap.fr/data/COSMOS-Web_master_v2.0.fits

# Extensions séparées
wget https://cosmos2025.iap.fr/data/cosmos_web_phot_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_lephare_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_cigale_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_morph_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_specz_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_flags_v2.0.fits

# Detection images, segmentation, LePhare, CIGALE
# (voir INS-COSMOS2025_HEBERGEMENT.md sections 2.2-2.5)
```

**Validation**:
```bash
du -sh data/jwst/raw/cosmos2025/
# Attendu: ~100-130 GB
```

---

### Phase 3: Validation (30 min)

**Référence**: INS-COSMOS2025_HEBERGEMENT.md Phase 3

**Script**: `scripts/validate_cosmos2025_complete.py`

```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
source /Users/pg-mac01/PythonProject/.venv/bin/activate
python scripts/validate_cosmos2025_complete.py
```

**Attendu**:
```
============================================================
VALIDATION COSMOS2025 TÉLÉCHARGEMENT COMPLET
============================================================

1. MASTER CATALOG
   Master: ✓ OK (784016 sources, 8.53 GB)

2. EXTENSIONS SÉPARÉES
   PHOT: ✓ OK (784016 sources, 2.31 GB)
   LEPHARE: ✓ OK (784016 sources, 1.42 GB)
   CIGALE: ✓ OK (784016 sources, 1.38 GB)
   MORPH: ✓ OK (784016 sources, 0.87 GB)
   SPECZ: ✓ OK (45231 sources, 0.09 GB)
   FLAGS: ✓ OK (784016 sources, 0.12 GB)

3. DETECTION IMAGES
   Tiles: ✓ 20/20 trouvées

4. SEGMENTATION MAPS
   Segmaps: ✓ 20/20 trouvées

5. LEPHARE PRODUITS
   PDFz: ✓ 8.32 GB
   SEDs: ✓ 35.12 GB

6. CIGALE PRODUITS
   SEDs: ✓ 32.87 GB

============================================================
RÉSULTAT: 13/13 validations réussies (100.0%)
✅ Téléchargement complet VALIDÉ
```

---

### Phase 4: Extraction z>8 (30 min)

**Référence**: INS-COSMOS2025.md lignes 174-313

**Script**: `scripts/extract_cosmos2025_highz.py`

```bash
python scripts/extract_cosmos2025_highz.py \
  --catalog data/jwst/raw/cosmos2025/catalog/COSMOS-Web_master_v2.0.fits \
  --zmin 8.0 \
  --zmax 15.0 \
  --output data/jwst/processed/cosmos2025/
```

**Résultat attendu**:
```
Lecture catalogue COSMOS2025: data/jwst/raw/cosmos2025/catalog/COSMOS-Web_master_v2.0.fits
Catalogue: 784016 sources totales
Galaxies 8.0 < z < 15.0: 8742

✅ Sauvegardé:
   FITS: data/jwst/processed/cosmos2025/cosmos2025_highz_z8.fits
   CSV:  data/jwst/processed/cosmos2025/cosmos2025_highz_z8.csv

Statistiques:
   N sources: 8742
   z range: 8.01 - 14.32
   log(M*) range: 7.89 - 11.34
```

---

### Phase 5: Préparation Archives Zenodo (1-2h)

**Référence**: INS-COSMOS2025_HEBERGEMENT.md Phase 5 + INS-ZENODO.md

**Actions**:

#### 5.1 Créer Templates

```bash
# Copier templates depuis INS-ZENODO.md
mkdir -p templates/

# README.md principal (lignes 26-246 de INS-ZENODO.md)
# CITATION.cff (lignes 253-277)
# LICENSE (CC-BY-4.0 standard)
```

#### 5.2 Préparer Structure

**Script**: `scripts/prepare_zenodo_archives.sh`

```bash
chmod +x scripts/prepare_zenodo_archives.sh
./scripts/prepare_zenodo_archives.sh
```

**Validation**:
```bash
cd data/zenodo_upload/
tree COSMOS2025_JANUS/ -L 2

# Attendu:
# COSMOS2025_JANUS/
# ├── README.md
# ├── CITATION.cff
# ├── LICENSE
# ├── 00_catalog/
# ├── 01_detection_images/
# ├── 02_segmentation_maps/
# ├── 03_lephare/
# ├── 04_cigale/
# ├── 05_janus_analysis/
# └── scripts/
```

#### 5.3 Créer Archives Finales

```bash
# Archive 1: Catalogue + segmentation (~8 GB)
zip -r COSMOS2025_catalog_segmaps.zip \
  COSMOS2025_JANUS/00_catalog/ \
  COSMOS2025_JANUS/02_segmentation_maps/ \
  COSMOS2025_JANUS/README.md \
  COSMOS2025_JANUS/CITATION.cff \
  COSMOS2025_JANUS/LICENSE

# Archives 2-6: Detection, LePhare, CIGALE, JANUS analysis
# (voir INS-COSMOS2025_HEBERGEMENT.md lignes 486-517)
```

**Vérification**:
```bash
ls -lh *.zip *.tar.gz
# Toutes < 50 GB
```

---

### Phase 6: Upload Zenodo (2-4h)

**Référence**: INS-ZENODO.md section "Workflow Upload Zenodo"

#### 6.1 Créer Compte Zenodo

1. Aller sur https://zenodo.org
2. Sign up avec ORCID ou GitHub
3. Vérifier email
4. Générer **Personal Access Token**:
   - Settings → Applications → Personal access tokens
   - New token → Sélectionner "deposit:write"
   - Copier token (sera utilisé comme `ZENODO_TOKEN`)

#### 6.2 Upload via API

**Script**: `scripts/zenodo_upload.py`

```bash
# Définir token
export ZENODO_TOKEN='votre_token_ici'

# Installer dépendances
pip install requests tqdm

# Lancer upload
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
source /Users/pg-mac01/PythonProject/.venv/bin/activate
python scripts/zenodo_upload.py
```

**Sortie attendue**:
```
Creating Zenodo deposition...
✓ Deposition created: ID 1234567

Uploading COSMOS2025_catalog_segmaps.zip (8.23 GB)...
████████████████████████████████████████ 100% 8.23GB/8.23GB
✓ COSMOS2025_catalog_segmaps.zip uploaded successfully

Uploading detection_part1.tar.gz (17.89 GB)...
████████████████████████████████████████ 100% 17.89GB/17.89GB
✓ detection_part1.tar.gz uploaded successfully

[... 4 autres archives ...]

✓ Upload complete: 6/6 archives
   Deposition ID: 1234567
   URL: https://zenodo.org/deposit/1234567

⚠ Don't forget to PUBLISH on Zenodo web interface to get DOI!
```

---

### Phase 7: Publication (30 min)

**Référence**: INS-COSMOS2025_HEBERGEMENT.md Phase 7

#### 7.1 Publier sur Zenodo

1. Aller sur https://zenodo.org/deposit/[DEPOSITION_ID]
2. Vérifier métadonnées
3. Vérifier que README.md est affiché
4. Cliquer **"Publish"**
5. **Copier DOI** (ex: `10.5281/zenodo.1234567`)

#### 7.2 Mettre à Jour Documentation Locale

**DATA_SOURCES.md**:
```markdown
### COSMOS2025 (COSMOS-Web DR1)

**Source**: Institut d'Astrophysique de Paris (IAP)
**URL originale**: https://cosmos2025.iap.fr/
**Zenodo DOI**: https://doi.org/10.5281/zenodo.1234567
**Date d'accès**: 6 Janvier 2026

**Hébergement**: Zenodo (pérenne, citable)
**Téléchargement complet**: 100-130 GB (6 archives)
**Extraction locale z>8**: cosmos2025_highz_z8.fits (~8,742 galaxies)
```

**CHANGELOG_DATA.md**:
```markdown
## [2026-01-06] - Infrastructure COSMOS2025 + Zenodo

### Téléchargé
- **COSMOS2025 complet**: ~120 GB
  - Master catalog + 6 extensions (784k galaxies)
  - 20 detection images + segmentation maps
  - LePhare + CIGALE SEDs complets

### Publié sur Zenodo
- **DOI**: https://doi.org/10.5281/zenodo.1234567
- **Dataset**: COSMOS2025_JANUS v1.0
- **Citable** dans publications

### Extraction locale
- **cosmos2025_highz_z8.fits**: 8,742 galaxies z>8
- Prêt pour Phase 3 analyses statistiques
```

---

## 📊 Checklist Complète

### Phase 1: Préparation
- [ ] Espace disque >= 150 GB vérifié
- [ ] Structure répertoires créée

### Phase 2: Téléchargement
- [ ] Master catalog (~8-10 GB)
- [ ] 6 extensions (~6-7 GB)
- [ ] 20 detection images (~36 GB)
- [ ] 20 segmentation maps (~160 MB)
- [ ] LePhare PDFz + SEDs (~30-50 GB)
- [ ] CIGALE SEDs (~30-40 GB)

### Phase 3: Validation
- [ ] Script validation exécuté
- [ ] 13/13 validations réussies

### Phase 4: Extraction z>8
- [ ] cosmos2025_highz_z8.fits créé
- [ ] ~5-10k galaxies extraites

### Phase 5: Archives Zenodo
- [ ] Templates créés (README, CITATION, LICENSE)
- [ ] Structure COSMOS2025_JANUS préparée
- [ ] 6-7 archives créées (< 50 GB chacune)

### Phase 6: Upload Zenodo
- [ ] Compte Zenodo créé
- [ ] ORCID ID obtenu
- [ ] Personal Access Token généré
- [ ] 6-7 archives uploadées
- [ ] Deposition sauvegardée

### Phase 7: Publication
- [ ] Dataset publié sur Zenodo
- [ ] DOI copié
- [ ] README/CITATION Zenodo mis à jour avec DOI
- [ ] DATA_SOURCES.md mis à jour
- [ ] CHANGELOG_DATA.md mis à jour

---

## 🎓 Scripts Python à Créer

Tous les scripts sont documentés en détail dans les instructions. Copier le code depuis:

1. **extract_cosmos2025_highz.py**
   → INS-COSMOS2025.md lignes 178-314

2. **validate_cosmos2025_complete.py**
   → INS-COSMOS2025_HEBERGEMENT.md lignes 214-349

3. **prepare_zenodo_archives.sh**
   → INS-COSMOS2025_HEBERGEMENT.md lignes 419-477

4. **zenodo_upload.py**
   → INS-COSMOS2025_HEBERGEMENT.md lignes 546-660

---

## 🔍 Résolution de Problèmes

### Problème: Téléchargement échoue (timeout)

**Solution**:
```bash
# Utiliser wget avec reprise automatique
wget -c https://cosmos2025.iap.fr/data/[fichier]
```

### Problème: Fichier FITS corrompu

**Solution**:
```bash
# Vérifier intégrité
python -c "from astropy.io import fits; hdul = fits.open('fichier.fits'); print(len(hdul[1].data))"

# Re-télécharger si nécessaire
rm fichier.fits
wget https://cosmos2025.iap.fr/data/fichier.fits
```

### Problème: Upload Zenodo échoue

**Solution**: Voir INS-ZENODO.md section "Troubleshooting"

### Problème: Espace disque insuffisant

**Option 1**: Supprimer fichiers temporaires après validation
```bash
# Après Phase 3 validation OK
rm -rf data/jwst/raw/cosmos2025/detection_images/
rm -rf data/jwst/raw/cosmos2025/segmentation_maps/
# Économie: ~36 GB
```

**Option 2**: Upload par étapes
- Préparer + uploader archives 1-3
- Supprimer fichiers sources
- Préparer + uploader archives 4-6

---

## 📚 Références Complètes

### Instructions JANUS

| Document | Lignes | Contenu Principal |
|----------|--------|-------------------|
| **INS-COSMOS2025.md** | 422 | Catalogue COSMOS2025, extraction z>8 |
| **INS-COSMOS2025_HEBERGEMENT.md** | 903 | Plan 7 phases complet, tous scripts |
| **INS-ZENODO.md** | ~800 | Infrastructure Zenodo, templates, API |

### Liens Externes

- **COSMOS2025 Official**: https://cosmos2025.iap.fr/
- **Zenodo**: https://zenodo.org
- **Zenodo API Docs**: https://developers.zenodo.org/
- **ORCID**: https://orcid.org/
- **CC-BY-4.0 License**: https://creativecommons.org/licenses/by/4.0/

---

## 🚀 Démarrage Rapide

### Pour Lancer Maintenant

```bash
# 1. Vérifier espace
df -h /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/data/

# 2. Si >= 150 GB disponible, lancer Phase 1
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
mkdir -p data/jwst/raw/cosmos2025/{catalog,detection_images,segmentation_maps,lephare,cigale}
mkdir -p data/jwst/processed/cosmos2025/
mkdir -p data/zenodo_upload/COSMOS2025_JANUS/

# 3. Commencer Phase 2 (téléchargement)
cd data/jwst/raw/cosmos2025/catalog/
wget https://cosmos2025.iap.fr/data/COSMOS-Web_master_v2.0.fits

# ... continuer selon INS-COSMOS2025_HEBERGEMENT.md Phase 2
```

### Pour Lire d'Abord

1. **INS-COSMOS2025.md** - Comprendre le catalogue
2. **INS-COSMOS2025_HEBERGEMENT.md** - Plan détaillé phase par phase
3. **INS-ZENODO.md** - Infrastructure Zenodo professionnelle

---

## 📈 Métriques Finales Attendues

### Données

| Métrique | Valeur |
|----------|--------|
| **Sources COSMOS2025 totales** | ~784,000 galaxies |
| **Sources z>8 extraites** | ~5,000-10,000 galaxies |
| **Taille téléchargement** | ~100-130 GB |
| **Taille extraction locale** | ~500 MB |
| **Nombre d'archives Zenodo** | 6-7 |
| **Taille Zenodo totale** | ~100-130 GB |

### Timeline

| Phase | Temps Estimé | Temps Cumulé |
|-------|--------------|--------------|
| Phase 1 | 15 min | 15 min |
| Phase 2 | 2-4h | 2h-4h15 |
| Phase 3 | 30 min | 2h30-4h45 |
| Phase 4 | 30 min | 3h-5h15 |
| Phase 5 | 1-2h | 4h-7h15 |
| Phase 6 | 2-4h | 6h-11h15 |
| Phase 7 | 30 min | 6h30-11h45 |
| **TOTAL** | **~7-11h** | - |

**Note**: Temps réel dépend de la connexion internet pour Phases 2 et 6.

---

## ✅ Validation Finale

Une fois Phase 7 complétée, vérifier:

- [ ] DOI Zenodo obtenu et fonctionnel
- [ ] Dataset accessible sur https://doi.org/[votre-doi]
- [ ] README.md Zenodo affiche correctement
- [ ] Extraction locale cosmos2025_highz_z8.fits utilisable
- [ ] DATA_SOURCES.md et CHANGELOG_DATA.md à jour
- [ ] Instructions GitHub à jour (README instructions)
- [ ] Nettoyage espace disque effectué (optionnel)

---

**Document**: PLAN_EXECUTION_COSMOS2025_ZENODO.md
**Version**: 1.0
**Date**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales - Phase 3
**Auteur**: Infrastructure setup avec Claude Sonnet 4.5

**Instructions complètes**:
- JANUS-INSTRUCTIONS/INS-COSMOS2025.md
- JANUS-INSTRUCTIONS/INS-COSMOS2025_HEBERGEMENT.md
- JANUS-INSTRUCTIONS/INS-ZENODO.md
