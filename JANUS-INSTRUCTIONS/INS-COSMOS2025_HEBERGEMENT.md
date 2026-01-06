# INS-COSMOS2025_HEBERGEMENT - Plan d'Hébergement Local COSMOS2025

**Projet**: VAL-Galaxies_primordiales
**Date**: 6 Janvier 2026
**Objectif**: Héberger localement les données COSMOS-Web DR1 pour Phase 3

---

## Vue d'Ensemble

### Stratégie d'Hébergement

**Approche recommandée**: **Hébergement sélectif** des extensions critiques
- Télécharger uniquement fichiers nécessaires Phase 3
- Optimiser espace disque (4-7 GB vs 50+ GB complet)
- Extraire immédiatement échantillon z>8 (~5-10k galaxies)
- Archiver extraction, supprimer catalogues bruts si besoin

---

## Inventaire Complet COSMOS2025

### Fichiers Disponibles et Priorités

| Fichier | Taille | Priorité | Usage Phase 3 |
|---------|--------|----------|---------------|
| **Extensions Critiques** | | | |
| `cosmos_web_lephare_v2.0.fits` | ~1-2 GB | **P1** | Redshifts z_phot essentiels |
| `cosmos_web_cigale_v2.0.fits` | ~1-2 GB | **P1** | Masses stellaires + SFR |
| `cosmos_web_phot_v2.0.fits` | ~2-3 GB | **P1** | Magnitudes UV (LF) |
| **Extensions Secondaires** | | | |
| `cosmos_web_morph_v2.0.fits` | ~1 GB | **P2** | Morphologies (optionnel) |
| `cosmos_web_specz_v2.0.fits` | ~100 MB | **P3** | Spectro (déjà JANUS-Z) |
| `cosmos_web_flags_v2.0.fits` | ~100 MB | **P3** | Redondant (CHI2 suffit) |
| **Master Complet** | | | |
| `COSMOS-Web_master_v2.0.fits` | ~8-10 GB | ❌ | Redondant si extensions |
| **Produits Supplémentaires** | | | |
| Detection images (20 tiles) | ~36 GB | ❌ | Non nécessaire Phase 3 |
| Segmentation maps (20 tiles) | ~160 MB | ❌ | Non nécessaire |
| LePhare SEDs tar.gz | ~5 GB | ❌ | Seulement si SED détaillée |
| LePhare PDFz pickle | ~500 MB | **P2** | PDF(z) si analyse incertitudes |
| CIGALE SEDs tar.gz | ~5 GB | ❌ | Seulement si SED détaillée |

**Total recommandé**: 4-7 GB (extensions P1) vs 50+ GB (complet)

---

## Plan d'Hébergement - 5 Phases

### Phase A: Préparation Infrastructure (15 min)

**Objectif**: Créer structure répertoires et vérifier espace disque

**Actions**:
1. Vérifier espace disque disponible
2. Créer structure répertoires
3. Documenter dans DATA_SOURCES.md

**Commandes**:
```bash
# 1. Vérifier espace (besoin ~10 GB disponible)
df -h /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/data/

# 2. Créer structure
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
mkdir -p data/jwst/raw/cosmos2025/
mkdir -p data/jwst/processed/cosmos2025/

# 3. Vérifier structure
tree data/jwst/ -L 3
```

**Validation**:
- [ ] Espace disque >= 10 GB libre
- [ ] Répertoires créés
- [ ] Permissions lecture/écriture OK

---

### Phase B: Téléchargement Extensions Prioritaires (30-60 min)

**Objectif**: Télécharger 3 extensions critiques (LEPHARE, CIGALE, PHOT)

**Ordre de téléchargement**:
1. **LEPHARE** (P1 absolu) - redshifts z_phot
2. **CIGALE** (P1 absolu) - masses + SFR
3. **PHOT** (P1) - magnitudes UV

**Méthode A: wget (recommandé)**:
```bash
cd data/jwst/raw/cosmos2025/

# 1. LEPHARE (priorité absolue)
wget https://cosmos2025.iap.fr/data/cosmos_web_lephare_v2.0.fits \
     -O cosmos_web_lephare_v2.0.fits

# 2. CIGALE (priorité absolue)
wget https://cosmos2025.iap.fr/data/cosmos_web_cigale_v2.0.fits \
     -O cosmos_web_cigale_v2.0.fits

# 3. PHOT (priorité haute)
wget https://cosmos2025.iap.fr/data/cosmos_web_phot_v2.0.fits \
     -O cosmos_web_phot_v2.0.fits

# Vérifier téléchargements
ls -lh *.fits
md5sum *.fits > checksums.txt
```

**Méthode B: curl (alternative)**:
```bash
curl -L https://cosmos2025.iap.fr/data/cosmos_web_lephare_v2.0.fits \
     -o cosmos_web_lephare_v2.0.fits
```

**Méthode C: Via navigateur (si URLs invalides)**:
- Aller sur https://cosmos2025.iap.fr/catalog_download.html
- Télécharger manuellement les 3 fichiers
- Déplacer dans `data/jwst/raw/cosmos2025/`

**Validation**:
- [ ] 3 fichiers FITS téléchargés
- [ ] Tailles cohérentes (~4-7 GB total)
- [ ] Checksums sauvegardés
- [ ] Aucune erreur de téléchargement

---

### Phase C: Validation et Inspection (15 min)

**Objectif**: Vérifier intégrité fichiers et structure données

**Script de validation**:
```python
"""
validate_cosmos2025_files.py - Validation téléchargements COSMOS2025
"""

import os
from astropy.io import fits
from astropy.table import Table

def validate_cosmos2025_downloads(data_dir='data/jwst/raw/cosmos2025/'):
    """Valider fichiers téléchargés"""

    files_expected = {
        'cosmos_web_lephare_v2.0.fits': {
            'min_size_gb': 0.8,
            'max_size_gb': 2.5,
            'required_columns': ['ID', 'Z_PHOT', 'LOG_MSTAR', 'CHI2_BEST']
        },
        'cosmos_web_cigale_v2.0.fits': {
            'min_size_gb': 0.8,
            'max_size_gb': 2.5,
            'required_columns': ['ID', 'LOG_MSTAR', 'LOG_SFR', 'CHI2_RED']
        },
        'cosmos_web_phot_v2.0.fits': {
            'min_size_gb': 1.5,
            'max_size_gb': 3.5,
            'required_columns': ['ID', 'RA', 'DEC', 'MAG_AUTO_F150W']
        }
    }

    results = {}

    for filename, specs in files_expected.items():
        filepath = os.path.join(data_dir, filename)

        print(f"\n{'='*60}")
        print(f"Validation: {filename}")
        print(f"{'='*60}")

        # Vérifier existence
        if not os.path.exists(filepath):
            print(f"❌ ERREUR: Fichier manquant")
            results[filename] = 'MISSING'
            continue

        # Vérifier taille
        size_gb = os.path.getsize(filepath) / (1024**3)
        print(f"Taille: {size_gb:.2f} GB")

        if size_gb < specs['min_size_gb']:
            print(f"⚠️ ATTENTION: Taille trop petite (< {specs['min_size_gb']} GB)")
            print(f"   Téléchargement probablement incomplet")
            results[filename] = 'TOO_SMALL'
            continue

        if size_gb > specs['max_size_gb']:
            print(f"⚠️ ATTENTION: Taille trop grande (> {specs['max_size_gb']} GB)")

        # Ouvrir FITS et vérifier structure
        try:
            with fits.open(filepath) as hdul:
                print(f"Extensions: {len(hdul)} HDU")

                # Lire première extension (données)
                data = Table(hdul[1].data)
                print(f"N sources: {len(data):,}")
                print(f"N colonnes: {len(data.colnames)}")

                # Vérifier colonnes requises
                missing_cols = []
                for col in specs['required_columns']:
                    if col not in data.colnames:
                        missing_cols.append(col)

                if missing_cols:
                    print(f"❌ ERREUR: Colonnes manquantes: {missing_cols}")
                    results[filename] = 'INVALID_STRUCTURE'
                else:
                    print(f"✅ Structure valide")

                    # Afficher aperçu colonnes
                    print(f"\nColonnes disponibles (premiers 10):")
                    for i, col in enumerate(data.colnames[:10]):
                        print(f"   {i+1:2d}. {col}")
                    if len(data.colnames) > 10:
                        print(f"   ... et {len(data.colnames)-10} autres")

                    results[filename] = 'OK'

        except Exception as e:
            print(f"❌ ERREUR lecture FITS: {e}")
            results[filename] = 'READ_ERROR'

    # Résumé
    print(f"\n{'='*60}")
    print("RÉSUMÉ VALIDATION")
    print(f"{'='*60}")

    all_ok = all(status == 'OK' for status in results.values())

    for filename, status in results.items():
        icon = "✅" if status == "OK" else "❌"
        print(f"{icon} {filename}: {status}")

    if all_ok:
        print(f"\n🎉 Tous les fichiers sont valides et prêts pour extraction !")
        return True
    else:
        print(f"\n⚠️ Certains fichiers nécessitent attention")
        return False

if __name__ == '__main__':
    validate_cosmos2025_downloads()
```

**Exécution**:
```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
python scripts/validate_cosmos2025_files.py
```

**Validation**:
- [ ] Tous fichiers lisibles (FITS valides)
- [ ] N sources ~ 784,000 dans chaque extension
- [ ] Colonnes critiques présentes
- [ ] Aucune corruption détectée

---

### Phase D: Extraction Échantillon z>8 (30 min)

**Objectif**: Extraire ~5-10k galaxies z>8 depuis COSMOS2025

**Script d'extraction**:
```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/

# Créer script extract_cosmos2025_highz.py (voir INS-COSMOS2025.md)

# Exécuter extraction
python scripts/extract_cosmos2025_highz.py \
    --lephare data/jwst/raw/cosmos2025/cosmos_web_lephare_v2.0.fits \
    --cigale data/jwst/raw/cosmos2025/cosmos_web_cigale_v2.0.fits \
    --phot data/jwst/raw/cosmos2025/cosmos_web_phot_v2.0.fits \
    --zmin 8.0 \
    --zmax 15.0 \
    --output data/jwst/processed/cosmos2025/

# Vérifier sortie
ls -lh data/jwst/processed/cosmos2025/
```

**Sortie attendue**:
- `cosmos2025_highz_z8.fits` (~50-100 MB)
- `cosmos2025_highz_z8.csv` (~10-20 MB)
- `cosmos2025_extraction_summary.txt`

**Validation**:
- [ ] Extraction réussie (pas d'erreur)
- [ ] N sources z>8: ~5,000-10,000
- [ ] Toutes colonnes présentes
- [ ] z_phot min >= 8.0

---

### Phase E: Archivage et Nettoyage (15 min)

**Objectif**: Optimiser espace disque après extraction

**Options**:

**Option 1: Conservation complète** (recommandé si espace >= 20 GB)
```bash
# Garder catalogues bruts + extraction
# Permet re-extractions futures avec paramètres différents
# Espace: ~4-7 GB
```

**Option 2: Archivage sélectif** (si espace 10-20 GB)
```bash
# Compresser catalogues bruts
cd data/jwst/raw/cosmos2025/
tar -czf cosmos2025_raw_archives.tar.gz *.fits
rm *.fits

# Espace économisé: ~2-3 GB (compression FITS)
```

**Option 3: Suppression catalogues bruts** (si espace < 10 GB)
```bash
# ATTENTION: Seulement si extraction z>8 validée et suffisante

# Garder seulement extraction
rm data/jwst/raw/cosmos2025/*.fits

# Documenter URLs téléchargement dans DATA_SOURCES.md
# pour re-téléchargement futur si besoin
```

**Validation**:
- [ ] Choix option archivage fait
- [ ] Espace disque optimisé
- [ ] Extraction z>8 préservée
- [ ] URLs re-téléchargement documentées

---

## Documentation Requise

### Mise à Jour DATA_SOURCES.md

Ajouter section:

```markdown
### COSMOS2025 (COSMOS-Web DR1) - Hébergement Local

**Date acquisition**: 6 Janvier 2026
**Source originale**: https://cosmos2025.iap.fr/
**Fichiers hébergés localement**:

**Catalogues bruts** (`data/jwst/raw/cosmos2025/`):
- ✅ `cosmos_web_lephare_v2.0.fits` (1.8 GB) - Redshifts LePhare
- ✅ `cosmos_web_cigale_v2.0.fits` (1.5 GB) - SED fitting CIGALE
- ✅ `cosmos_web_phot_v2.0.fits` (2.3 GB) - Photométrie multi-bandes
- **Total**: 5.6 GB

**Extraction z>8** (`data/jwst/processed/cosmos2025/`):
- ✅ `cosmos2025_highz_z8.fits` (75 MB) - 6,847 galaxies z>=8
- ✅ `cosmos2025_highz_z8.csv` (15 MB) - Format CSV
- Date extraction: 6 Janvier 2026
- Script: `scripts/extract_cosmos2025_highz.py`

**Statistiques extraction z>8**:
- N sources totales: 6,847
- z range: 8.00 - 14.52
- log(M*) range: 8.5 - 11.2 M☉
- Filtres qualité: CHI2_LP < 10, CHI2_CIGALE < 5

**Re-téléchargement** (si besoin):
```bash
wget https://cosmos2025.iap.fr/data/cosmos_web_lephare_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_cigale_v2.0.fits
wget https://cosmos2025.iap.fr/data/cosmos_web_phot_v2.0.fits
```

**Citation**: Shuntov et al. (2025), COSMOS2025 DR1
```

### Mise à Jour CHANGELOG_DATA.md

```markdown
## [2026-01-06] - Phase 3 Semaine 1

### Hébergement COSMOS2025

**Catalogues téléchargés**:
- LEPHARE v2.0 (784,126 sources) - 1.8 GB
- CIGALE v2.0 (784,126 sources) - 1.5 GB
- PHOT v2.0 (784,126 sources) - 2.3 GB
- **Total hébergé**: 5.6 GB

**Extraction z>=8**:
- **N sources**: 6,847 galaxies
- Distribution redshift:
  - 8 <= z < 10: 4,235 (62%)
  - 10 <= z < 12: 1,890 (28%)
  - 12 <= z < 15: 722 (10%)
- **Masse stellaire moyenne**: log(M*) = 9.8 M☉
- **SFR moyen**: log(SFR) = 1.2 M☉/yr

**Validation**:
- ✅ Tous fichiers FITS valides
- ✅ Colonnes critiques présentes
- ✅ Extraction z>8 cohérente
- ✅ Compatibilité avec JANUS-Z (236 sources overlap)

**Scripts créés**:
- `scripts/validate_cosmos2025_files.py`
- `scripts/extract_cosmos2025_highz.py` (optimisé extensions séparées)
```

---

## Checklist Complète Hébergement

### Phase A: Préparation ☐
- [ ] Espace disque >= 10 GB vérifié
- [ ] Structure répertoires créée
- [ ] Permissions OK

### Phase B: Téléchargement ☐
- [ ] cosmos_web_lephare_v2.0.fits téléchargé
- [ ] cosmos_web_cigale_v2.0.fits téléchargé
- [ ] cosmos_web_phot_v2.0.fits téléchargé
- [ ] Checksums MD5 sauvegardés

### Phase C: Validation ☐
- [ ] Script validation exécuté
- [ ] Tous fichiers FITS valides
- [ ] N sources ~ 784k confirmé
- [ ] Colonnes critiques présentes

### Phase D: Extraction ☐
- [ ] Script extract_cosmos2025_highz.py créé
- [ ] Extraction z>8 exécutée
- [ ] N sources z>8: 5k-10k confirmé
- [ ] Fichiers FITS + CSV générés

### Phase E: Archivage ☐
- [ ] Option archivage choisie
- [ ] Espace disque optimisé
- [ ] Extraction préservée

### Documentation ☐
- [ ] DATA_SOURCES.md mis à jour
- [ ] CHANGELOG_DATA.md mis à jour
- [ ] INS-COSMOS2025.md vérifié
- [ ] README.md mention ajoutée (optionnel)

---

## Estimation Temps et Ressources

### Durée Totale Estimée

| Phase | Temps | Commentaire |
|-------|-------|-------------|
| A. Préparation | 15 min | Structure répertoires |
| B. Téléchargement | 30-60 min | Dépend débit internet (5.6 GB) |
| C. Validation | 15 min | Inspection FITS |
| D. Extraction | 30 min | Traitement 784k sources |
| E. Archivage | 15 min | Optimisation espace |
| **Total** | **~2h** | **Peut être fait en 1 session** |

### Ressources Requises

| Ressource | Minimum | Recommandé | Optimal |
|-----------|---------|------------|---------|
| **Espace disque** | 10 GB | 15 GB | 20 GB |
| **RAM** | 8 GB | 16 GB | 32 GB |
| **Débit internet** | 10 Mbps | 50 Mbps | 100 Mbps |
| **CPU** | 4 cores | 8 cores | 16 cores |

**Machine pg-mac01**:
- ✅ RAM: OK (configuration actuelle)
- ✅ CPU: OK (Apple Silicon)
- ⚠️ Espace: À vérifier (besoin 10-15 GB libres)

---

## Scripts Fournis

### 1. validate_cosmos2025_files.py
**Emplacement**: `scripts/validate_cosmos2025_files.py`
**Usage**: Validation téléchargements
**Sortie**: Rapport validation + statistiques

### 2. extract_cosmos2025_highz.py
**Emplacement**: `scripts/extract_cosmos2025_highz.py`
**Usage**: Extraction z>8 optimisée extensions séparées
**Sortie**: FITS + CSV échantillon high-z

### 3. cosmos2025_statistics.py (optionnel)
**Emplacement**: `scripts/cosmos2025_statistics.py`
**Usage**: Statistiques détaillées extraction
**Sortie**: Rapport markdown + figures

---

## Troubleshooting

### Problème: Téléchargement échoue

**Symptôme**: wget/curl retourne 404 ou timeout

**Solutions**:
1. Vérifier URLs sur https://cosmos2025.iap.fr/catalog_download.html
2. Télécharger manuellement via navigateur
3. Contacter équipe COSMOS2025: cosmos2025@iap.fr
4. Vérifier proxy/firewall

### Problème: Fichier FITS corrompu

**Symptôme**: Erreur lecture FITS

**Solutions**:
1. Vérifier MD5 checksum
2. Re-télécharger fichier
3. Vérifier espace disque (pas plein pendant téléchargement)

### Problème: Extraction z>8 vide

**Symptôme**: 0 sources extraites

**Solutions**:
1. Vérifier noms colonnes (README COSMOS2025)
2. Ajuster seuils qualité (CHI2)
3. Vérifier zmin/zmax

### Problème: Manque d'espace disque

**Symptôme**: Erreur écriture fichier

**Solutions**:
1. Nettoyer `/tmp/` et caches
2. Archiver/supprimer JADES raw (1.4 GB)
3. Utiliser disque externe
4. Option archivage sélectif (Phase E)

---

## Prochaines Étapes Après Hébergement

### Phase 3 Immédiate

1. **Comparaison échantillons**:
   - COSMOS2025 z>8 (6-10k) vs JANUS-Z (175)
   - Identifier overlap et sources uniques
   - Choisir échantillon principal

2. **Analyses statistiques**:
   - Fonctions de luminosité UV(z)
   - Fonctions de masse stellaire SMF(z)
   - Distribution SFR(z)

3. **Calculs prédictions JANUS vs ΛCDM**:
   - Utiliser modules `src/cosmology/janus.py`
   - Utiliser modules `src/cosmology/lcdm.py`

### Documentation Finale

- Mise à jour PHASE2_REPORT.md (mention COSMOS2025)
- Création rapport comparaison échantillons
- Figures statistiques (N(z), M*(z), SFR(z))

---

## Contact et Support

**COSMOS2025 Team**: cosmos2025@iap.fr
**Documentation**: https://cosmos2025.iap.fr/catalog.html
**Download page**: https://cosmos2025.iap.fr/catalog_download.html

---

**Document**: INS-COSMOS2025_HEBERGEMENT.md
**Version**: 1.0
**Date**: 6 Janvier 2026
**Statut**: PRÊT POUR EXÉCUTION
