#!/usr/bin/env python3
"""
Validation intégrité complète COSMOS2025

Usage:
    python validate_cosmos2025_complete.py

Vérifie que tous les fichiers COSMOS2025 sont téléchargés et lisibles.
"""
import os
import sys
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
        print("\nProchaine étape: Phase 4 - Extraction z>8")
        print("  python scripts/extract_cosmos2025_highz.py --zmin 8.0")
        return True
    else:
        print("❌ Téléchargement INCOMPLET - voir détails ci-dessus")
        print("\nFichiers manquants ou invalides:")
        for key, value in results.items():
            if not value:
                print(f"  - {key}")
        return False

if __name__ == '__main__':
    # Déterminer chemin base
    if len(sys.argv) > 1:
        base = sys.argv[1]
    else:
        base = 'data/jwst/raw/cosmos2025/'

    success = validate_cosmos2025_download(base)
    sys.exit(0 if success else 1)
