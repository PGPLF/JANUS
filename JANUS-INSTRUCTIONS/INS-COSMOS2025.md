# INS-COSMOS2025 - Catalogue COSMOS-Web DR1

**Source**: https://cosmos2025.iap.fr/
**Date d'accès**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales - Phase 3

---

## Vue d'Ensemble

**COSMOS2025** est le catalogue officiel Data Release 1 (DR1) du programme COSMOS-Web JWST, contenant **~784,000 galaxies** avec photométrie, morphologie et paramètres physiques.

### Publication
- **Titre**: "COSMOS2025: The COSMOS-Web galaxy catalog of photometry, morphology, and physical parameters from JWST, HST and ground-based imaging"
- **Auteurs**: M. Shuntov, H. B. Akins, L. Paquereau, C. M. Casey, O. Ilbert, R. C. Arango-Toro, H. J. McCracken, M. Franco, S. Harish, J. S. Kartaltepe, A. M. Koekemoer, L. Yang, M. Huertas-Company et al.
- **URL catalogue**: https://cosmos2025.iap.fr/catalog_download.html
- **URL README**: https://cosmos2025.iap.fr/catalog.html

---

## Contenu du Catalogue

### Catalogue Photométrique Principal

**Fichier master**: `COSMOS-Web_master_v2.0.fits` (~784k sources)

**6 Extensions HDU**:
1. **PHOT**: Photométrie multi-bandes (JWST + HST + ground)
2. **MORPH**: Paramètres morphologiques
3. **LEPHARE**: Redshifts photométriques et masses stellaires
4. **CIGALE**: SED fitting (masses, SFR, atténuation)
5. **SPEC-Z**: Redshifts spectroscopiques (quand disponibles)
6. **FLAGS**: Flags qualité et sélection

**Extensions séparées disponibles**:
- `cosmos_web_phot_v2.0.fits`
- `cosmos_web_morph_v2.0.fits`
- `cosmos_web_lephare_v2.0.fits`
- `cosmos_web_cigale_v2.0.fits`
- `cosmos_web_specz_v2.0.fits`
- `cosmos_web_flags_v2.0.fits`

### Produits Supplémentaires

**Detection images** (20 tiles, ~1.8 GB chacune):
- Format: FITS
- Résolution: JWST NIRCam (0.03"/pixel)
- Tarballs disponibles

**Segmentation maps** (20 tiles, ~8 MB chacune):
- Cartes de segmentation pour extraction photométrie
- ID sources correspondant au catalogue

**LePhare SEDs**:
- Distributions redshift (PDFz) : fichier pickle
- Best-fit SEDs : tar.gz (~784k sources)

**CIGALE SEDs**:
- Best-fit SEDs : tar.gz (~784k sources)

---

## Couverture et Statistiques

### Couverture Spatiale
- Champ: **COSMOS** (RA ~ 150°, Dec ~ +2°)
- Aire: **~0.54 deg²** (COSMOS-Web area)
- Profondeur: Ultra-deep JWST imaging

### Couverture en Redshift
- **z ~ 0 - 14** (photométrique)
- Forte densité z > 1
- Échantillon z > 8: **À extraire du catalogue**

### Filtres Photométriques
**JWST NIRCam**:
- F115W, F150W, F277W, F444W (imaging)
- Autres bandes selon tiles

**HST**:
- ACS: F814W
- WFC3: F125W, F160W

**Ground-based**:
- Subaru, CFHT, VLT (u, g, r, i, z, Y)

---

## Utilité pour VAL-Galaxies_primordiales

### Phase 3: Analyses Statistiques

**1. Complément JANUS-Z (236 galaxies)**
- COSMOS2025 contient **784k galaxies** vs JANUS-Z 236
- Extraction z > 8 attendue: **plusieurs milliers de sources**
- Améliore statistiques pour fonctions de luminosité UV

**2. Données disponibles pertinentes**
- ✅ Redshifts photométriques (LePhare PDFz)
- ✅ Masses stellaires (CIGALE + LePhare)
- ✅ Star Formation Rates (CIGALE)
- ✅ Magnitudes UV (photométrie multi-bandes)
- ✅ Morphologies (Sérsic profiles, etc.)
- ✅ Spectroscopie (sous-échantillon)

**3. Overlap avec Phase 2**
- JANUS-Z v17.1 inclut déjà des sources COSMOS-Web
- COSMOS2025 DR1 = **version complète plus récente**
- Peut remplacer/compléter données JANUS-Z partielles

### Analyses Possibles

**A. Fonctions de Luminosité UV**
- Grande statistique z > 8
- Comparaison JANUS vs ΛCDM
- Bins en redshift: z=8-10, 10-12, 12-14

**B. Fonctions de Masse Stellaire**
- SED fitting CIGALE (plus robuste que JANUS-Z partiel)
- Masses stellaires homogènes pour 784k sources
- Test "impossible galaxies" à z > 8

**C. Star Formation Rates**
- SFR(z) du SED fitting CIGALE
- Comparaison prédictions JANUS pour formation rapide

**D. Statistiques de Maturité**
- Morphologies (compacité, profils Sérsic)
- Test maturité précoce prédite par JANUS

---

## Téléchargement

### URLs Directes

**Catalogue master**:
```
https://cosmos2025.iap.fr/data/COSMOS-Web_master_v2.0.fits
```

**Extensions séparées**:
```
https://cosmos2025.iap.fr/data/cosmos_web_phot_v2.0.fits
https://cosmos2025.iap.fr/data/cosmos_web_lephare_v2.0.fits
https://cosmos2025.iap.fr/data/cosmos_web_cigale_v2.0.fits
```

**LePhare produits**:
```
https://cosmos2025.iap.fr/data/lephare_pdfz_v2.0.pkl  (redshift PDFs)
https://cosmos2025.iap.fr/data/lephare_seds_v2.0.tar.gz  (SEDs)
```

**CIGALE SEDs**:
```
https://cosmos2025.iap.fr/data/cigale_seds_v2.0.tar.gz
```

### Taille des Fichiers (estimée)

| Fichier | Taille estimée |
|---------|----------------|
| Master catalog | ~5-10 GB |
| Extension PHOT | ~2-3 GB |
| Extension LEPHARE | ~1-2 GB |
| Extension CIGALE | ~1-2 GB |
| LePhare PDFz | ~500 MB |
| Detection images (all) | ~36 GB (20×1.8GB) |
| Segmentation maps (all) | ~160 MB (20×8MB) |

---

## Script d'Extraction z > 8

### Extraction COSMOS2025 High-z

**Script**: `scripts/extract_cosmos2025_highz.py`

```python
"""
Extraction galaxies z > 8 du catalogue COSMOS2025 DR1

Usage:
    python scripts/extract_cosmos2025_highz.py --zmin 8.0 --output data/jwst/processed/
"""

import numpy as np
from astropy.io import fits
from astropy.table import Table
import argparse

def extract_cosmos2025_highz(catalog_path, zmin=8.0, zmax=15.0, quality_cuts=True):
    """
    Extrait galaxies z > zmin du catalogue COSMOS2025

    Parameters
    ----------
    catalog_path : str
        Chemin vers COSMOS-Web_master_v2.0.fits
    zmin : float
        Redshift minimum (défaut: 8.0)
    zmax : float
        Redshift maximum (défaut: 15.0)
    quality_cuts : bool
        Appliquer filtres qualité (défaut: True)

    Returns
    -------
    highz_sample : astropy.table.Table
        Échantillon z > zmin avec colonnes pertinentes
    """

    print(f"Lecture catalogue COSMOS2025: {catalog_path}")

    # Lire catalogue master (ou extension LEPHARE)
    with fits.open(catalog_path) as hdul:
        # Extension LEPHARE contient z_phot
        lephare = Table(hdul['LEPHARE'].data)
        phot = Table(hdul['PHOT'].data)
        cigale = Table(hdul['CIGALE'].data)
        flags = Table(hdul['FLAGS'].data)

    print(f"Catalogue: {len(lephare)} sources totales")

    # Sélection redshift
    z_phot = lephare['Z_PHOT']  # Redshift photométrique LePhare
    z_phot_68 = lephare['Z_PHOT_68']  # Intervalle confiance 68%

    mask_z = (z_phot >= zmin) & (z_phot < zmax)

    if quality_cuts:
        # Filtres qualité (ajuster selon README)
        mask_quality = (
            (lephare['CHI2_BEST'] < 10) &  # Chi2 raisonnable
            (flags['USE_PHOT'] == 1) &  # Photométrie utilisable
            (flags['STAR_FLAG'] == 0)  # Pas une étoile
        )
        mask = mask_z & mask_quality
    else:
        mask = mask_z

    print(f"Galaxies {zmin} < z < {zmax}: {mask.sum()}")

    # Créer table de sortie avec colonnes pertinentes
    highz = Table()
    highz['ID'] = lephare['ID'][mask]
    highz['RA'] = phot['RA'][mask]
    highz['DEC'] = phot['DEC'][mask]
    highz['z_phot'] = z_phot[mask]
    highz['z_phot_68_low'] = lephare['Z_PHOT_68_LOW'][mask]
    highz['z_phot_68_high'] = lephare['Z_PHOT_68_HIGH'][mask]

    # Masses stellaires (LePhare et CIGALE)
    highz['log_mstar_lp'] = lephare['LOG_MSTAR'][mask]
    highz['log_mstar_cigale'] = cigale['LOG_MSTAR'][mask]

    # SFR (CIGALE)
    highz['log_sfr_cigale'] = cigale['LOG_SFR'][mask]

    # Magnitudes UV (ajuster bandes selon README)
    highz['mag_f150w'] = phot['MAG_AUTO_F150W'][mask]
    highz['mag_f277w'] = phot['MAG_AUTO_F277W'][mask]
    highz['mag_f444w'] = phot['MAG_AUTO_F444W'][mask]

    # Flags qualité
    highz['chi2_lp'] = lephare['CHI2_BEST'][mask]
    highz['chi2_cigale'] = cigale['CHI2_RED'][mask]

    return highz

def main():
    parser = argparse.ArgumentParser(description='Extraire z>8 COSMOS2025')
    parser.add_argument('--catalog', type=str,
                        default='data/jwst/raw/cosmos2025/COSMOS-Web_master_v2.0.fits',
                        help='Chemin catalogue COSMOS2025')
    parser.add_argument('--zmin', type=float, default=8.0,
                        help='Redshift minimum')
    parser.add_argument('--zmax', type=float, default=15.0,
                        help='Redshift maximum')
    parser.add_argument('--output', type=str,
                        default='data/jwst/processed/',
                        help='Dossier de sortie')
    parser.add_argument('--no-quality-cuts', action='store_true',
                        help='Désactiver filtres qualité')

    args = parser.parse_args()

    # Extraction
    highz = extract_cosmos2025_highz(
        args.catalog,
        zmin=args.zmin,
        zmax=args.zmax,
        quality_cuts=not args.no_quality_cuts
    )

    # Sauvegardes
    out_fits = f"{args.output}/cosmos2025_highz_z{int(args.zmin)}.fits"
    out_csv = f"{args.output}/cosmos2025_highz_z{int(args.zmin)}.csv"

    highz.write(out_fits, format='fits', overwrite=True)
    highz.write(out_csv, format='csv', overwrite=True)

    print(f"\n✅ Sauvegardé:")
    print(f"   FITS: {out_fits}")
    print(f"   CSV:  {out_csv}")
    print(f"\nStatistiques:")
    print(f"   N sources: {len(highz)}")
    print(f"   z range: {highz['z_phot'].min():.2f} - {highz['z_phot'].max():.2f}")
    print(f"   log(M*) range: {highz['log_mstar_cigale'].min():.2f} - {highz['log_mstar_cigale'].max():.2f}")

if __name__ == '__main__':
    main()
```

---

## Intégration Phase 3

### Mise à Jour DATA_SOURCES.md

Ajouter section:

```markdown
### COSMOS2025 (COSMOS-Web DR1)

**Source**: Institut d'Astrophysique de Paris (IAP)
**URL**: https://cosmos2025.iap.fr/
**Date d'accès**: 6 Janvier 2026
**Fichier**: `COSMOS-Web_master_v2.0.fits`

**Description**: Catalogue photométrique complet COSMOS-Web (~784k galaxies)
- Photométrie JWST NIRCam + HST + ground-based
- SED fitting LePhare et CIGALE
- Redshifts photométriques + spectroscopiques

**Extraction z > 8**: `cosmos2025_highz_z8.fits`
- Script: `scripts/extract_cosmos2025_highz.py`
- N sources attendu: ~5,000-10,000 galaxies
```

### Mise à Jour CHANGELOG_DATA.md

```markdown
## [2026-01-06] - Phase 3 Semaine 1

### Ajouté
- **Catalogue COSMOS2025 DR1**
  - Source: https://cosmos2025.iap.fr/
  - ~784,000 galaxies avec photométrie JWST+HST
  - SED fitting LePhare + CIGALE complet

### Extraction haute-z
- **COSMOS2025 z >= 8**: N sources (à déterminer après extraction)
- Complément JANUS-Z pour statistiques
- Masses stellaires et SFR homogènes

### Fichiers créés
- `data/jwst/raw/cosmos2025/COSMOS-Web_master_v2.0.fits`
- `data/jwst/processed/cosmos2025_highz_z8.fits`
- `data/jwst/processed/cosmos2025_highz_z8.csv`
- `scripts/extract_cosmos2025_highz.py`
```

---

## Citation

Lors de publication, citer:

```
Shuntov, M., Akins, H. B., Paquereau, L., Casey, C. M., Ilbert, O., et al. (2025).
"COSMOS2025: The COSMOS-Web galaxy catalog of photometry, morphology,
and physical parameters from JWST, HST and ground-based imaging",
ApJ (submitted). https://cosmos2025.iap.fr/
```

---

## Recommandations Phase 3

### Priorité 1: Téléchargement Immédiat
1. **Catalogue master** ou **Extension LEPHARE** (redshifts + masses)
2. **Extension CIGALE** (SED fitting complet)

### Priorité 2: Extraction High-z
- Exécuter `extract_cosmos2025_highz.py`
- Sélection z > 8 avec filtres qualité
- Documenter statistiques (N, z range, masses)

### Priorité 3: Comparaison JANUS-Z
- Vérifier overlap sources entre JANUS-Z et COSMOS2025
- Identifier sources uniques dans chaque catalogue
- Décider échantillon principal Phase 3

### Avantages COSMOS2025 vs JANUS-Z

| Aspect | COSMOS2025 | JANUS-Z v17.1 |
|--------|------------|---------------|
| N sources totales | ~784,000 | 236 |
| N sources z>8 | ~5k-10k (estimé) | 175 |
| SED fitting | Homogène (LePhare+CIGALE) | Hétérogène |
| Redshift quality | PDFz disponibles | Mix spectro/photo |
| Morphologies | Oui (complet) | Non |
| Couverture | COSMOS field | Multi-fields |

**Recommandation**: Utiliser COSMOS2025 comme échantillon principal z>8 pour statistiques, conserver JANUS-Z pour validation croisée.

---

## Contact et Support

**COSMOS2025 Team**: cosmos2025@iap.fr
**IAP CANDIDE Cluster**: https://www.iap.fr/

---

**Document**: INS-COSMOS2025.md
**Version**: 1.0
**Date**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales
**Phase**: 3 (Analyses Statistiques)
