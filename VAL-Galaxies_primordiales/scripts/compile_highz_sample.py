#!/usr/bin/env python3
"""
Compile comprehensive high-z galaxy sample for VAL-Galaxies_primordiales
Combines: JADES extraction + JANUS-Z reference + Labbé+23 reference
"""

import numpy as np
import pandas as pd
from astropy.table import Table
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "jwst" / "processed"
REFERENCE_DIR = DATA_DIR / "reference"
OUTPUT_DIR = PROCESSED_DIR

def load_jades_highz():
    """Load JADES high-z extraction"""
    jades_file = PROCESSED_DIR / "jades_highz_z8.csv"
    if jades_file.exists():
        df = pd.read_csv(jades_file)
        df['source'] = 'JADES'
        df['z_type'] = 'phot'
        # Rename columns
        df = df.rename(columns={
            'EAZY_z_a': 'z',
            'EAZY_l68': 'z_lo',
            'EAZY_u68': 'z_hi'
        })
        print(f"JADES: {len(df)} sources")
        return df
    return None

def load_janus_z_reference():
    """Load JANUS-Z reference catalog"""
    ref_file = PROCESSED_DIR / "janus_z_reference_catalog.csv"
    if ref_file.exists():
        df = pd.read_csv(ref_file)
        df['source'] = 'JANUS-Z-ref'
        # Standardize columns
        df = df.rename(columns={
            'log_Mstar': 'log_mass',
            'sigma_Mstar': 'log_mass_err'
        })
        print(f"JANUS-Z reference: {len(df)} sources")
        return df
    return None

def load_labbe_reference():
    """Load Labbé+23 reference candidates"""
    ref_file = REFERENCE_DIR / "labbe2023_candidates.csv"
    if ref_file.exists():
        df = pd.read_csv(ref_file)
        df['source'] = 'Labbe+23'
        df['z_type'] = 'phot'
        df = df.rename(columns={
            'z_phot': 'z',
            'log_mass': 'log_mass'
        })
        print(f"Labbé+23 reference: {len(df)} sources")
        return df
    return None

def create_summary_statistics(combined):
    """Generate summary statistics"""
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)

    # By source
    print("\nBy source:")
    for src in combined['source'].unique():
        n = len(combined[combined['source'] == src])
        print(f"  {src}: {n}")

    # By redshift bin
    print("\nBy redshift bin:")
    z = combined['z'].values
    for z_lo, z_hi in [(6.5, 8), (8, 10), (10, 12), (12, 14), (14, 20)]:
        n = np.sum((z >= z_lo) & (z < z_hi))
        print(f"  {z_lo} <= z < {z_hi}: {n}")

    # Spectroscopic vs photometric
    if 'z_type' in combined.columns:
        print("\nBy z type:")
        print(f"  spec: {len(combined[combined['z_type'] == 'spec'])}")
        print(f"  phot: {len(combined[combined['z_type'] == 'phot'])}")

    # Top 10 highest z
    print("\nTop 10 highest redshift galaxies:")
    top10 = combined.nlargest(10, 'z')
    for _, row in top10.iterrows():
        z_type = row.get('z_type', 'unknown')
        print(f"  {row.get('ID', 'N/A'):<25} z={row['z']:.2f} ({z_type}) [{row['source']}]")

def main():
    print("="*60)
    print("HIGH-Z SAMPLE COMPILATION")
    print("="*60)

    # Load all sources
    dfs = []

    jades = load_jades_highz()
    if jades is not None:
        # Filter to high-quality (z < 15 for sanity)
        jades_clean = jades[jades['z'] < 15].copy()
        print(f"  -> After quality cut (z<15): {len(jades_clean)}")
        dfs.append(jades_clean[['ID', 'RA', 'DEC', 'z', 'source', 'z_type', 'field']])

    janus_ref = load_janus_z_reference()
    if janus_ref is not None:
        # Select key columns
        cols = ['ID', 'z', 'z_err', 'z_type', 'log_mass', 'log_mass_err',
                'log_SFR', 'metallicity_12OH', 'has_AGN', 'is_dusty',
                'protocluster', 'Survey', 'Reference', 'source']
        available_cols = [c for c in cols if c in janus_ref.columns]
        dfs.append(janus_ref[available_cols])

    labbe = load_labbe_reference()
    if labbe is not None:
        cols = ['id', 'ra', 'dec', 'z', 'log_mass', 'source', 'z_type']
        available_cols = [c for c in cols if c in labbe.columns]
        df_labbe = labbe[available_cols].copy()
        df_labbe = df_labbe.rename(columns={'id': 'ID', 'ra': 'RA', 'dec': 'DEC'})
        dfs.append(df_labbe)

    # Summary of individual catalogs
    print("\n" + "="*60)
    print("INDIVIDUAL CATALOG STATISTICS")
    print("="*60)

    if jades is not None:
        z = jades['z'].values
        print(f"\nJADES (all z>=8):")
        print(f"  8 <= z < 10: {np.sum((z >= 8) & (z < 10))}")
        print(f"  10 <= z < 12: {np.sum((z >= 10) & (z < 12))}")
        print(f"  12 <= z < 15: {np.sum((z >= 12) & (z < 15))}")
        print(f"  z >= 15 (excluded): {np.sum(z >= 15)}")

    if janus_ref is not None:
        z = janus_ref['z'].values
        print(f"\nJANUS-Z reference:")
        print(f"  z range: {z.min():.2f} - {z.max():.2f}")
        print(f"  spec: {len(janus_ref[janus_ref['z_type'] == 'spec'])}")
        print(f"  phot: {len(janus_ref[janus_ref['z_type'] == 'phot'])}")

    # Save comprehensive catalog info
    output_info = OUTPUT_DIR / "highz_sample_summary.txt"
    with open(output_info, 'w') as f:
        f.write("HIGH-Z GALAXY SAMPLE COMPILATION\n")
        f.write("="*50 + "\n\n")
        f.write("Sources:\n")
        f.write(f"  1. JADES DR2/DR3 extraction (z>=8, z<15): ~{len(jades_clean) if jades is not None else 0}\n")
        f.write(f"  2. JANUS-Z reference catalog: {len(janus_ref) if janus_ref is not None else 0}\n")
        f.write(f"  3. Labbé+23 reference: {len(labbe) if labbe is not None else 0}\n")
        f.write("\nNote: JANUS-Z reference includes spectroscopic confirmations\n")
        f.write("from JADES, GLASS, UNCOVER, CEERS, EXCELS, A3COSMOS\n")

    print(f"\nSummary saved to: {output_info}")

    # Create combined statistics
    if janus_ref is not None:
        create_summary_statistics(janus_ref)

    return dfs

if __name__ == "__main__":
    main()
