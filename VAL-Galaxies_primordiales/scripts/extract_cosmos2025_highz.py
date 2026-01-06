#!/usr/bin/env python3
"""
Extraction galaxies z > 8 du catalogue COSMOS2025 DR1

Usage:
    python extract_cosmos2025_highz.py --zmin 8.0 --output data/jwst/processed/

Extrait échantillon haute-z pour analyses JANUS.
"""
import numpy as np
from astropy.io import fits
from astropy.table import Table
import argparse
import sys
import os

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

    # Vérifier que fichier existe
    if not os.path.exists(catalog_path):
        print(f"❌ Erreur: Fichier non trouvé: {catalog_path}")
        sys.exit(1)

    # Lire catalogue master (ou extension LEPHARE)
    try:
        with fits.open(catalog_path) as hdul:
            print(f"Extensions disponibles: {[h.name for h in hdul]}")

            # Extension LEPHARE contient z_phot
            lephare = Table(hdul['LEPHARE'].data)
            phot = Table(hdul['PHOT'].data)
            cigale = Table(hdul['CIGALE'].data)
            flags = Table(hdul['FLAGS'].data)
    except Exception as e:
        print(f"❌ Erreur lecture FITS: {e}")
        sys.exit(1)

    print(f"Catalogue: {len(lephare)} sources totales")

    # Sélection redshift
    z_phot = lephare['Z_PHOT']  # Redshift photométrique LePhare

    # Vérifier que colonne existe
    if 'Z_PHOT' not in lephare.colnames:
        print(f"❌ Erreur: Colonne Z_PHOT non trouvée")
        print(f"Colonnes disponibles: {lephare.colnames[:10]}...")
        sys.exit(1)

    mask_z = (z_phot >= zmin) & (z_phot < zmax)

    if quality_cuts:
        # Filtres qualité (ajuster selon README)
        print("Application filtres qualité...")

        # Vérifier colonnes disponibles
        has_chi2 = 'CHI2_BEST' in lephare.colnames
        has_use_phot = 'USE_PHOT' in flags.colnames
        has_star_flag = 'STAR_FLAG' in flags.colnames

        mask_quality = np.ones(len(lephare), dtype=bool)

        if has_chi2:
            mask_quality &= (lephare['CHI2_BEST'] < 10)
            print(f"  - Chi2 < 10: {mask_quality.sum()} sources")

        if has_use_phot:
            mask_quality &= (flags['USE_PHOT'] == 1)
            print(f"  - USE_PHOT=1: {mask_quality.sum()} sources")

        if has_star_flag:
            mask_quality &= (flags['STAR_FLAG'] == 0)
            print(f"  - STAR_FLAG=0: {mask_quality.sum()} sources")

        mask = mask_z & mask_quality
    else:
        mask = mask_z

    print(f"\nGalaxies {zmin} < z < {zmax}: {mask.sum()}")

    if mask.sum() == 0:
        print("⚠️ Aucune galaxie trouvée dans cet intervalle!")
        print(f"   z_phot range: {z_phot.min():.2f} - {z_phot.max():.2f}")
        sys.exit(1)

    # Créer table de sortie avec colonnes pertinentes
    highz = Table()

    # ID et coordonnées
    highz['ID'] = lephare['ID'][mask] if 'ID' in lephare.colnames else np.arange(mask.sum())
    highz['RA'] = phot['RA'][mask] if 'RA' in phot.colnames else phot['ALPHA_J2000'][mask]
    highz['DEC'] = phot['DEC'][mask] if 'DEC' in phot.colnames else phot['DELTA_J2000'][mask]

    # Redshift
    highz['z_phot'] = z_phot[mask]

    if 'Z_PHOT_68_LOW' in lephare.colnames:
        highz['z_phot_68_low'] = lephare['Z_PHOT_68_LOW'][mask]
        highz['z_phot_68_high'] = lephare['Z_PHOT_68_HIGH'][mask]

    # Masses stellaires (LePhare et CIGALE)
    if 'LOG_MSTAR' in lephare.colnames:
        highz['log_mstar_lp'] = lephare['LOG_MSTAR'][mask]
    if 'LOG_MSTAR' in cigale.colnames:
        highz['log_mstar_cigale'] = cigale['LOG_MSTAR'][mask]

    # SFR (CIGALE)
    if 'LOG_SFR' in cigale.colnames:
        highz['log_sfr_cigale'] = cigale['LOG_SFR'][mask]

    # Magnitudes UV (ajuster bandes selon README)
    for band in ['F150W', 'F277W', 'F444W']:
        mag_col = f'MAG_AUTO_{band}'
        if mag_col in phot.colnames:
            highz[f'mag_{band.lower()}'] = phot[mag_col][mask]

    # Flags qualité
    if 'CHI2_BEST' in lephare.colnames:
        highz['chi2_lp'] = lephare['CHI2_BEST'][mask]
    if 'CHI2_RED' in cigale.colnames:
        highz['chi2_cigale'] = cigale['CHI2_RED'][mask]

    return highz

def main():
    parser = argparse.ArgumentParser(
        description='Extraire z>8 COSMOS2025',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python extract_cosmos2025_highz.py --zmin 8.0
  python extract_cosmos2025_highz.py --zmin 10.0 --zmax 12.0 --no-quality-cuts
        """
    )

    parser.add_argument('--catalog', type=str,
                        default='data/jwst/raw/cosmos2025/catalog/COSMOS-Web_master_v2.0.fits',
                        help='Chemin catalogue COSMOS2025')
    parser.add_argument('--zmin', type=float, default=8.0,
                        help='Redshift minimum (défaut: 8.0)')
    parser.add_argument('--zmax', type=float, default=15.0,
                        help='Redshift maximum (défaut: 15.0)')
    parser.add_argument('--output', type=str,
                        default='data/jwst/processed/cosmos2025/',
                        help='Dossier de sortie')
    parser.add_argument('--no-quality-cuts', action='store_true',
                        help='Désactiver filtres qualité')

    args = parser.parse_args()

    # Créer dossier output si nécessaire
    os.makedirs(args.output, exist_ok=True)

    # Extraction
    print("=" * 60)
    print("EXTRACTION COSMOS2025 HIGH-Z")
    print("=" * 60)

    highz = extract_cosmos2025_highz(
        args.catalog,
        zmin=args.zmin,
        zmax=args.zmax,
        quality_cuts=not args.no_quality_cuts
    )

    # Sauvegardes
    out_fits = os.path.join(args.output, f"cosmos2025_highz_z{int(args.zmin)}.fits")
    out_csv = os.path.join(args.output, f"cosmos2025_highz_z{int(args.zmin)}.csv")

    print(f"\nSauvegarde résultats...")
    highz.write(out_fits, format='fits', overwrite=True)
    highz.write(out_csv, format='csv', overwrite=True)

    print("\n" + "=" * 60)
    print("✅ EXTRACTION COMPLÈTE")
    print("=" * 60)
    print(f"\nFichiers créés:")
    print(f"   FITS: {out_fits}")
    print(f"   CSV:  {out_csv}")

    print(f"\nStatistiques:")
    print(f"   N sources: {len(highz)}")
    print(f"   z range: {highz['z_phot'].min():.2f} - {highz['z_phot'].max():.2f}")

    if 'log_mstar_cigale' in highz.colnames:
        valid_mass = ~np.isnan(highz['log_mstar_cigale'])
        if valid_mass.sum() > 0:
            print(f"   log(M*) range: {highz['log_mstar_cigale'][valid_mass].min():.2f} - {highz['log_mstar_cigale'][valid_mass].max():.2f}")

    print("\nProchaine étape: Phase 5 - Préparation archives Zenodo")
    print("  bash scripts/prepare_zenodo_archives.sh")

if __name__ == '__main__':
    main()
