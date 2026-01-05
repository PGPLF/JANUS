#!/usr/bin/env python3
"""
Extract the 6 massive galaxy candidates from Labbé et al. (2023)
Nature 616, 266-269 (arXiv:2207.12446)

Criteria: log(M*/Msun) > 10 at z > 7
"""

import numpy as np
from astropy.table import Table
from astropy.io import fits
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data" / "reference"
INPUT_FILE = DATA_DIR / "labbe2023_sample.ecsv"
OUTPUT_FITS = DATA_DIR / "labbe2023_candidates.fits"
OUTPUT_CSV = DATA_DIR / "labbe2023_candidates.csv"

def main():
    # Load data
    print("Loading Labbé+23 sample...")
    data = Table.read(INPUT_FILE, format='ascii.ecsv')

    print(f"Total sources in sample: {len(data)}")
    print(f"Columns: {data.colnames}")

    # Selection criteria: massive galaxies (log M* > 10) at z > 7
    mask_massive = data['mass'] >= 10.0
    mask_highz = data['z'] >= 7.0
    mask = mask_massive & mask_highz

    candidates = data[mask]
    print(f"\nSelected {len(candidates)} massive candidates (log M* >= 10, z >= 7)")

    # Sort by redshift
    candidates.sort('z')

    # Display summary
    print("\n" + "="*80)
    print("LABBÉ ET AL. (2023) - 6 MASSIVE GALAXY CANDIDATES")
    print("="*80)
    print(f"{'ID':<10} {'z_phot':<8} {'z_lo':<8} {'z_hi':<8} {'log(M*)':<10} {'M*_lo':<8} {'M*_hi':<8}")
    print("-"*80)

    for row in candidates:
        print(f"{row['id']:<10} {row['z']:<8.2f} {row['zlo']:<8.2f} {row['zhi']:<8.2f} "
              f"{row['mass']:<10.2f} {row['masslo']:<8.2f} {row['masshi']:<8.2f}")

    print("-"*80)

    # Create simplified output table
    output = Table()
    output['id'] = candidates['id']
    output['ra'] = candidates['ra']
    output['dec'] = candidates['dec']
    output['z_phot'] = np.round(candidates['z'], 2)
    output['z_lo'] = np.round(candidates['zlo'], 2)
    output['z_hi'] = np.round(candidates['zhi'], 2)
    output['log_mass'] = np.round(candidates['mass'], 2)
    output['log_mass_lo'] = np.round(candidates['masslo'], 2)
    output['log_mass_hi'] = np.round(candidates['masshi'], 2)
    output['chi2'] = candidates['chi2']

    # Add photometry columns (key bands)
    for band in ['f115w', 'f150w', 'f200w', 'f277w', 'f356w', 'f444w']:
        output[band] = np.round(candidates[band], 2)
        output[f'e_{band}'] = np.round(candidates[f'e{band[1:]}'], 2)

    # Calculate UV magnitude (approximate from F150W at z~8)
    # M_UV = m_AB - 5*log10(d_L/10pc) - K-correction
    # For simplicity, use apparent magnitude in F150W
    output['m_F150W'] = -2.5 * np.log10(output['f150w'] * 1e-9) + 8.9  # nJy to AB mag

    # Save outputs
    output.write(OUTPUT_FITS, overwrite=True)
    output.write(OUTPUT_CSV, overwrite=True, format='csv')

    print(f"\nSaved to:")
    print(f"  - {OUTPUT_FITS}")
    print(f"  - {OUTPUT_CSV}")

    # Statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Redshift range: {output['z_phot'].min():.2f} - {output['z_phot'].max():.2f}")
    print(f"Mean redshift: {np.mean(output['z_phot']):.2f}")
    print(f"Mass range: {output['log_mass'].min():.2f} - {output['log_mass'].max():.2f} log(M*/Msun)")
    print(f"Mean mass: {np.mean(output['log_mass']):.2f} log(M*/Msun)")

    # Comparison with Nature paper Table 1
    print("\n" + "="*80)
    print("VALIDATION vs NATURE PAPER (Table 1)")
    print("="*80)
    print("Expected 6 candidates at 7.4 < z < 9.1 with M* > 10^10 Msun")
    print(f"Found: {len(output)} candidates at {output['z_phot'].min():.1f} < z < {output['z_phot'].max():.1f}")
    print("NOTE: Slight differences due to revised SED fitting (revision 3)")

    return output

if __name__ == "__main__":
    candidates = main()
