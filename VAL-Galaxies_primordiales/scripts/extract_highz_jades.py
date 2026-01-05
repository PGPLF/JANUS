#!/usr/bin/env python3
"""
Extract high-z galaxy candidates from JADES catalogs
GOODS-S DR2 + GOODS-N DR3
"""

import numpy as np
from astropy.table import Table, vstack, join
from astropy.io import fits
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
JADES_DIR = DATA_DIR / "jwst" / "raw" / "jades"
OUTPUT_DIR = DATA_DIR / "jwst" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_jades_with_photoz(filepath, field_name):
    """Load JADES catalog with photometric redshifts"""
    print(f"\nLoading {field_name} from {filepath.name}...")

    with fits.open(filepath) as hdul:
        # Load position data from FLAG or SIZE
        if 'FLAG' in [h.name for h in hdul]:
            pos_data = Table.read(hdul['FLAG'])
        else:
            pos_data = Table.read(hdul['SIZE'])

        # Load photoz data
        if 'PHOTOZ' in [h.name for h in hdul]:
            photoz = Table.read(hdul['PHOTOZ'])
        else:
            print("  WARNING: No PHOTOZ extension found")
            return None

        # Load photometry (KRON or CIRC)
        if 'KRON' in [h.name for h in hdul]:
            phot = Table.read(hdul['KRON'])
        elif 'CIRC' in [h.name for h in hdul]:
            phot = Table.read(hdul['CIRC'])
        else:
            phot = None

    # Merge tables on ID
    data = join(pos_data, photoz, keys='ID', join_type='inner')
    if phot is not None:
        # Only join key columns to avoid duplicates
        phot_cols = ['ID'] + [c for c in phot.colnames if c not in data.colnames]
        data = join(data, phot[phot_cols], keys='ID', join_type='left')

    print(f"  Total sources: {len(data)}")

    return data

def extract_highz(data, field_name, z_col='EAZY_z_a', z_min=8.0):
    """Extract high-z candidates"""

    if z_col not in data.colnames:
        print(f"  ERROR: Column {z_col} not found")
        return None

    z_values = np.array(data[z_col])

    # Valid redshifts above threshold
    valid = np.isfinite(z_values) & (z_values >= z_min)
    highz = data[valid]

    print(f"  High-z candidates (z >= {z_min}): {len(highz)}")

    if len(highz) > 0:
        z_arr = np.array(highz[z_col])
        print(f"  Redshift range: {z_arr.min():.2f} - {z_arr.max():.2f}")

        # Breakdown by redshift bins
        for z_low, z_high in [(8, 10), (10, 12), (12, 14), (14, 20)]:
            n = np.sum((z_arr >= z_low) & (z_arr < z_high))
            if n > 0:
                print(f"    {z_low} <= z < {z_high}: {n}")

    return highz

def create_output_catalog(highz_list, output_file):
    """Create combined output catalog"""

    # Select key columns
    key_cols = ['ID', 'RA', 'DEC', 'EAZY_z_a', 'EAZY_l68', 'EAZY_u68', 'field']

    combined = []
    for highz in highz_list:
        if highz is None or len(highz) == 0:
            continue

        # Select available columns
        available = [c for c in key_cols if c in highz.colnames]
        subset = highz[available]
        combined.append(subset)

    if not combined:
        print("No high-z candidates found!")
        return None

    catalog = vstack(combined)
    catalog.sort('EAZY_z_a', reverse=True)

    # Save
    catalog.write(output_file, overwrite=True)
    print(f"\nSaved {len(catalog)} candidates to {output_file}")

    return catalog

def main():
    print("="*60)
    print("JADES HIGH-Z EXTRACTION")
    print("="*60)

    # Files
    goods_s_file = JADES_DIR / "jades_goods-s_photometry_v2.0.fits"
    goods_n_file = JADES_DIR / "jades_goods-n_photometry_v1.0.fits"

    # Load and extract
    results = []

    if goods_s_file.exists():
        goods_s = load_jades_with_photoz(goods_s_file, "GOODS-S")
        if goods_s is not None:
            highz_s = extract_highz(goods_s, "GOODS-S")
            if highz_s is not None and len(highz_s) > 0:
                highz_s['field'] = 'GOODS-S'
                results.append(highz_s)

    if goods_n_file.exists():
        goods_n = load_jades_with_photoz(goods_n_file, "GOODS-N")
        if goods_n is not None:
            highz_n = extract_highz(goods_n, "GOODS-N")
            if highz_n is not None and len(highz_n) > 0:
                highz_n['field'] = 'GOODS-N'
                results.append(highz_n)

    # Create output
    if results:
        output_fits = OUTPUT_DIR / "jades_highz_z8.fits"
        output_csv = OUTPUT_DIR / "jades_highz_z8.csv"

        catalog = create_output_catalog(results, output_fits)
        if catalog is not None:
            # Also save CSV
            catalog.write(output_csv, overwrite=True, format='csv')
            print(f"Saved CSV to {output_csv}")

            # Summary stats
            print("\n" + "="*60)
            print("SUMMARY")
            print("="*60)
            z = np.array(catalog['EAZY_z_a'])
            print(f"Total candidates z >= 8: {len(catalog)}")
            print(f"  GOODS-S: {np.sum(np.array(catalog['field']) == 'GOODS-S')}")
            print(f"  GOODS-N: {np.sum(np.array(catalog['field']) == 'GOODS-N')}")
            print(f"Highest redshift: z = {z.max():.2f}")

            # Top 10 highest z
            print("\nTop 10 highest redshift candidates:")
            print(f"{'ID':<15} {'z_phot':<8} {'z_lo':<8} {'z_hi':<8} {'Field':<10}")
            print("-"*50)
            for row in catalog[:10]:
                print(f"{row['ID']:<15} {row['EAZY_z_a']:<8.2f} {row['EAZY_l68']:<8.2f} {row['EAZY_u68']:<8.2f} {row['field']:<10}")

    return results

if __name__ == "__main__":
    main()
