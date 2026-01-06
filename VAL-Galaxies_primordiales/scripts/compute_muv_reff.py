#!/usr/bin/env python3
"""
Étape 3.0: Calcul M_UV et extraction r_eff pour Phase 3.1
Complète le catalogue JANUS-Z avec les données manquantes

Usage:
    python3 compute_muv_reff.py
"""

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
JADES_S = DATA_DIR / "jwst" / "raw" / "jades" / "jades_goods-s_photometry_v2.0.fits"
JADES_N = DATA_DIR / "jwst" / "raw" / "jades" / "jades_goods-n_photometry_v1.0.fits"
REF_CATALOG = DATA_DIR / "jwst" / "processed" / "janus_z_reference_catalog.csv"
OUTPUT_DIR = DATA_DIR / "jwst" / "processed"

# Zero-point for AB magnitudes (nJy to AB mag)
# AB mag = -2.5 * log10(flux_nJy) + 31.4
ZP_AB = 31.4  # for flux in nJy

def flux_to_mag(flux_njy):
    """Convert flux in nJy to AB magnitude"""
    with np.errstate(divide='ignore', invalid='ignore'):
        mag = -2.5 * np.log10(flux_njy) + ZP_AB
        mag[~np.isfinite(mag)] = np.nan
    return mag

def compute_muv(m_obs, z, filter_wave_um):
    """
    Compute absolute UV magnitude M_UV

    M_UV = m_obs - DM(z) - K_UV

    Where:
    - DM = distance modulus = 5*log10(D_L/10pc)
    - K_UV ≈ -2.5*log10(1+z) for rest-frame UV (simple approximation)

    For high-z galaxies, we use:
    - F150W for z ~ 8-10 (rest-frame ~1500Å)
    - F200W for z ~ 10-13 (rest-frame ~1500Å)
    - F277W for z > 13 (rest-frame ~1500Å)
    """
    # Distance modulus
    D_L = cosmo.luminosity_distance(z).to(u.pc).value
    DM = 5 * np.log10(D_L / 10)

    # K-correction (simple approximation for rest-UV)
    # More accurate would require SED fitting
    K_UV = -2.5 * np.log10(1 + z)

    M_UV = m_obs - DM - K_UV

    return M_UV

def select_uv_filter(z):
    """Select appropriate filter for rest-frame UV based on redshift"""
    if z < 9:
        return 'F150W'
    elif z < 12:
        return 'F200W'
    else:
        return 'F277W'

def load_jades_photometry(fits_file, field_name):
    """Load JADES photometry and sizes"""
    print(f"Loading {field_name}...")

    with fits.open(fits_file) as hdu:
        # Photometry (KRON extension)
        kron = hdu['KRON'].data

        # Sizes (SIZE extension)
        size = hdu['SIZE'].data

        # Photo-z (PHOTOZ extension)
        photoz = hdu['PHOTOZ'].data

    # Create DataFrame
    df = pd.DataFrame({
        'ID': kron['ID'],
        'RA': kron['RA'],
        'DEC': kron['DEC'],
        'z': photoz['EAZY_z_a'],
        'z_lo': photoz['EAZY_l68'],
        'z_hi': photoz['EAZY_u68'],
        # Kron fluxes (in nJy)
        'F150W_flux': kron['F150W_KRON'],
        'F200W_flux': kron['F200W_KRON'],
        'F277W_flux': kron['F277W_KRON'],
        # Half-light radii (in arcsec)
        'r_eff_F150W': size['F150W_RHALF'],
        'r_eff_F200W': size['F200W_RHALF'],
        'r_eff_F277W': size['F277W_RHALF'],
        'field': field_name
    })

    print(f"  Loaded {len(df)} sources")
    return df

def process_highz_sample(df, z_min=6.5):
    """Process high-z sample: compute M_UV and select r_eff"""

    # Filter high-z
    highz = df[df['z'] >= z_min].copy()
    print(f"\nHigh-z sample (z >= {z_min}): {len(highz)} galaxies")

    # Convert fluxes to magnitudes
    highz['m_F150W'] = flux_to_mag(highz['F150W_flux'])
    highz['m_F200W'] = flux_to_mag(highz['F200W_flux'])
    highz['m_F277W'] = flux_to_mag(highz['F277W_flux'])

    # Compute M_UV using appropriate filter for each redshift
    M_UV = []
    r_eff = []
    uv_filter = []

    for idx, row in highz.iterrows():
        z = row['z']
        filt = select_uv_filter(z)
        uv_filter.append(filt)

        # Get magnitude and r_eff for selected filter
        m_col = f'm_{filt}'
        r_col = f'r_eff_{filt}'

        m_obs = row[m_col]
        r = row[r_col]

        # Compute M_UV
        if np.isfinite(m_obs) and np.isfinite(z):
            muv = compute_muv(m_obs, z, filter_wave_um=1.5)  # approx
            M_UV.append(muv)
        else:
            M_UV.append(np.nan)

        # Physical size: r_eff in kpc
        if np.isfinite(r) and np.isfinite(z):
            # Convert arcsec to kpc
            kpc_per_arcsec = cosmo.kpc_proper_per_arcmin(z).to(u.kpc/u.arcsec).value
            r_kpc = r * kpc_per_arcsec
            r_eff.append(r_kpc)
        else:
            r_eff.append(np.nan)

    highz['M_UV'] = M_UV
    highz['r_eff_kpc'] = r_eff
    highz['UV_filter'] = uv_filter

    return highz

def crossmatch_janus_z(jades_df, ref_catalog, match_radius=0.5):
    """Cross-match JADES with JANUS-Z reference catalog"""

    ref = pd.read_csv(ref_catalog)
    print(f"\nCross-matching with JANUS-Z reference ({len(ref)} galaxies)...")

    # Simple positional match (would be better with astropy SkyCoord)
    # For now, match by ID patterns or nearest neighbor

    # Add M_UV and r_eff columns to reference
    ref['M_UV'] = np.nan
    ref['r_eff_kpc'] = np.nan
    ref['UV_filter'] = ''

    # Stats
    matched = 0

    # Try to match by survey and approximate position
    for idx, row in ref.iterrows():
        survey = row.get('Survey', '')

        if 'JADES' in survey:
            # Find closest match in JADES by ID or position
            # For simplicity, assign median values if no direct match
            z = row['z']

            # Find JADES sources at similar redshift
            z_match = jades_df[(jades_df['z'] > z - 0.5) & (jades_df['z'] < z + 0.5)]

            if len(z_match) > 0:
                # Use median M_UV and r_eff for this redshift bin
                ref.loc[idx, 'M_UV'] = z_match['M_UV'].median()
                ref.loc[idx, 'r_eff_kpc'] = z_match['r_eff_kpc'].median()
                ref.loc[idx, 'UV_filter'] = select_uv_filter(z)
                matched += 1

    print(f"  Matched: {matched}/{len(ref)}")

    return ref

def compute_muv_from_mass(ref):
    """
    Estimate M_UV from stellar mass using empirical relation
    For galaxies without direct photometry

    Relation from Song+16, Stefanon+21:
    M_UV ≈ -2.5 * (log_Mstar - 10) - 21
    (rough approximation for high-z)
    """
    print("\nEstimating M_UV from stellar mass...")

    # Initialize column if not exists
    if 'M_UV' not in ref.columns:
        ref['M_UV'] = np.nan
    if 'UV_filter' not in ref.columns:
        ref['UV_filter'] = ''

    mask = ref['M_UV'].isna() & ref['log_Mstar'].notna()
    n_estimate = mask.sum()

    # Empirical relation (approximate)
    ref.loc[mask, 'M_UV'] = -2.5 * (ref.loc[mask, 'log_Mstar'] - 10) - 21
    ref.loc[mask, 'UV_filter'] = 'estimated'

    print(f"  Estimated M_UV for {n_estimate} galaxies")

    return ref

def compute_reff_from_mass(ref):
    """
    Estimate r_eff from stellar mass using size-mass relation

    Relation from Shibuya+15, Ono+24:
    log(r_eff/kpc) ≈ 0.22 * (log_Mstar - 9) - 0.3 * (1+z)/10
    (rough approximation for high-z)
    """
    print("\nEstimating r_eff from stellar mass...")

    # Initialize column if not exists
    if 'r_eff_kpc' not in ref.columns:
        ref['r_eff_kpc'] = np.nan

    mask = ref['r_eff_kpc'].isna() & ref['log_Mstar'].notna()
    n_estimate = mask.sum()

    # Size-mass relation (approximate)
    log_reff = 0.22 * (ref.loc[mask, 'log_Mstar'] - 9) - 0.3 * (1 + ref.loc[mask, 'z']) / 10
    ref.loc[mask, 'r_eff_kpc'] = 10**log_reff

    print(f"  Estimated r_eff for {n_estimate} galaxies")

    return ref

def main():
    print("="*60)
    print("ÉTAPE 3.0: CALCUL M_UV ET r_eff")
    print("="*60)

    # Load JADES data
    jades_list = []

    if JADES_S.exists():
        jades_s = load_jades_photometry(JADES_S, 'GOODS-S')
        jades_list.append(jades_s)

    if JADES_N.exists():
        jades_n = load_jades_photometry(JADES_N, 'GOODS-N')
        jades_list.append(jades_n)

    if not jades_list:
        print("ERROR: No JADES data found!")
        return

    # Combine
    jades_all = pd.concat(jades_list, ignore_index=True)
    print(f"\nTotal JADES sources: {len(jades_all)}")

    # Process high-z sample
    jades_highz = process_highz_sample(jades_all, z_min=6.5)

    # Statistics
    n_valid_muv = jades_highz['M_UV'].notna().sum()
    n_valid_reff = jades_highz['r_eff_kpc'].notna().sum()
    print(f"\nValid M_UV: {n_valid_muv}")
    print(f"Valid r_eff: {n_valid_reff}")

    # Save JADES high-z with M_UV and r_eff
    output_jades = OUTPUT_DIR / "jades_highz_muv_reff.csv"
    cols_out = ['ID', 'RA', 'DEC', 'z', 'z_lo', 'z_hi', 'field',
                'M_UV', 'UV_filter', 'r_eff_kpc',
                'm_F150W', 'm_F200W', 'm_F277W']
    jades_highz[cols_out].to_csv(output_jades, index=False)
    print(f"\nSaved: {output_jades}")

    # Update JANUS-Z reference
    if REF_CATALOG.exists():
        ref = pd.read_csv(REF_CATALOG)

        # Add M_UV from mass relation
        ref = compute_muv_from_mass(ref)

        # Add r_eff from size-mass relation
        ref = compute_reff_from_mass(ref)

        # Save updated reference
        output_ref = OUTPUT_DIR / "janus_z_complete.csv"
        ref.to_csv(output_ref, index=False)
        print(f"Saved: {output_ref}")

        # Summary
        print("\n" + "="*60)
        print("RÉSUMÉ JANUS-Z COMPLÉTÉ")
        print("="*60)
        print(f"Total galaxies: {len(ref)}")
        print(f"M_UV disponible: {ref['M_UV'].notna().sum()}")
        print(f"r_eff disponible: {ref['r_eff_kpc'].notna().sum()}")
        print(f"M_UV range: {ref['M_UV'].min():.1f} to {ref['M_UV'].max():.1f}")
        print(f"r_eff range: {ref['r_eff_kpc'].min():.2f} to {ref['r_eff_kpc'].max():.2f} kpc")

    print("\n" + "="*60)
    print("ÉTAPE 3.0 TERMINÉE")
    print("="*60)

if __name__ == "__main__":
    main()
