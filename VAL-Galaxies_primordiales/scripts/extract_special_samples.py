#!/usr/bin/env python3
"""
Extract special galaxy samples from JANUS-Z reference catalog:
1. EXCELS - Metallicity measurements
2. A3COSMOS - Dusty/NIRCam-dark galaxies
3. Proto-clusters
4. AGN hosts
5. Spectroscopically confirmed z > 12
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "jwst" / "processed"
SPECIAL_DIR = DATA_DIR / "jwst" / "special"
SPECIAL_DIR.mkdir(parents=True, exist_ok=True)

def load_reference_catalog():
    """Load JANUS-Z reference catalog"""
    ref_file = PROCESSED_DIR / "janus_z_reference_catalog.csv"
    df = pd.read_csv(ref_file)
    print(f"Loaded {len(df)} galaxies from reference catalog")
    return df

def extract_excels(df):
    """Extract EXCELS metallicity sample"""
    excels = df[df['Survey'] == 'EXCELS'].copy()
    print(f"\nEXCELS sample: {len(excels)} galaxies")

    if len(excels) > 0:
        print(f"  z range: {excels['z'].min():.2f} - {excels['z'].max():.2f}")
        print(f"  Metallicity range: {excels['metallicity_12OH'].min():.2f} - {excels['metallicity_12OH'].max():.2f}")

        # Save
        output = SPECIAL_DIR / "excels_metallicity_sample.csv"
        excels.to_csv(output, index=False)
        print(f"  Saved to: {output}")

    return excels

def extract_a3cosmos(df):
    """Extract A3COSMOS dusty/NIRCam-dark sample"""
    # Dusty galaxies flagged
    dusty = df[df['is_dusty'] == 1].copy()
    print(f"\nA3COSMOS/Dusty sample: {len(dusty)} galaxies")

    if len(dusty) > 0:
        print(f"  z range: {dusty['z'].min():.2f} - {dusty['z'].max():.2f}")

        # Check for AC-2168 specifically
        ac2168 = dusty[dusty['ID'].str.contains('AC-2168', na=False)]
        if len(ac2168) > 0:
            print(f"  Includes AC-2168 (NIRCam-dark, z=6.63)")

        # Save
        output = SPECIAL_DIR / "a3cosmos_dusty_sample.csv"
        dusty.to_csv(output, index=False)
        print(f"  Saved to: {output}")

    return dusty

def extract_protoclusters(df):
    """Extract proto-cluster members"""
    # Non-field galaxies
    pc = df[df['protocluster'] != 'field'].copy()
    print(f"\nProto-cluster members: {len(pc)} galaxies")

    if len(pc) > 0:
        clusters = pc['protocluster'].unique()
        print(f"  Clusters: {len(clusters)}")
        for cl in clusters:
            n = len(pc[pc['protocluster'] == cl])
            z_mean = pc[pc['protocluster'] == cl]['z'].mean()
            print(f"    {cl}: {n} members, <z>={z_mean:.2f}")

        # Save
        output = SPECIAL_DIR / "protocluster_members.csv"
        pc.to_csv(output, index=False)
        print(f"  Saved to: {output}")

    return pc

def extract_agn(df):
    """Extract AGN hosts"""
    agn = df[df['has_AGN'] == 1].copy()
    print(f"\nAGN hosts: {len(agn)} galaxies")

    if len(agn) > 0:
        print(f"  z range: {agn['z'].min():.2f} - {agn['z'].max():.2f}")
        for _, row in agn.iterrows():
            print(f"    {row['ID']}: z={row['z']:.2f}")

        # Save
        output = SPECIAL_DIR / "agn_hosts.csv"
        agn.to_csv(output, index=False)
        print(f"  Saved to: {output}")

    return agn

def extract_ultra_highz(df):
    """Extract spectroscopically confirmed z > 12"""
    # Spectroscopic z > 12
    uhz = df[(df['z'] > 12) & (df['z_type'] == 'spec')].copy()
    print(f"\nUltra high-z (z_spec > 12): {len(uhz)} galaxies")

    if len(uhz) > 0:
        uhz_sorted = uhz.sort_values('z', ascending=False)
        print(f"  Top 5:")
        for _, row in uhz_sorted.head(5).iterrows():
            print(f"    {row['ID']}: z={row['z']:.2f}")

        # Save
        output = SPECIAL_DIR / "ultra_highz_zspec_gt12.csv"
        uhz.to_csv(output, index=False)
        print(f"  Saved to: {output}")

    return uhz

def extract_impossible_galaxy(df):
    """Extract the 'impossible galaxy' AC-2168 / JWST-Impossible-z12"""
    impossible = df[df['ID'].str.contains('Impossible|AC-2168', na=False, case=False)].copy()
    print(f"\n'Impossible galaxies': {len(impossible)}")

    if len(impossible) > 0:
        for _, row in impossible.iterrows():
            print(f"  {row['ID']}: z={row['z']:.2f}, log(M*)={row['log_Mstar']:.2f}")

        # Save
        output = SPECIAL_DIR / "impossible_galaxies.csv"
        impossible.to_csv(output, index=False)
        print(f"  Saved to: {output}")

    return impossible

def create_summary(df, excels, dusty, pc, agn, uhz, impossible):
    """Create summary file"""
    summary = SPECIAL_DIR / "special_samples_summary.txt"

    with open(summary, 'w') as f:
        f.write("SPECIAL GALAXY SAMPLES - Phase 2 Semaine 4\n")
        f.write("="*50 + "\n\n")

        f.write(f"Source: JANUS-Z reference catalog v17.1\n")
        f.write(f"Total galaxies: {len(df)}\n\n")

        f.write("EXTRACTED SAMPLES:\n")
        f.write("-"*50 + "\n")
        f.write(f"1. EXCELS (metallicity):     {len(excels):3d} galaxies\n")
        f.write(f"2. A3COSMOS (dusty):         {len(dusty):3d} galaxies\n")
        f.write(f"3. Proto-cluster members:    {len(pc):3d} galaxies\n")
        f.write(f"4. AGN hosts:                {len(agn):3d} galaxies\n")
        f.write(f"5. Ultra high-z (z_spec>12): {len(uhz):3d} galaxies\n")
        f.write(f"6. 'Impossible' galaxies:    {len(impossible):3d} galaxies\n")
        f.write("-"*50 + "\n")

        f.write("\nFILES CREATED:\n")
        f.write("- excels_metallicity_sample.csv\n")
        f.write("- a3cosmos_dusty_sample.csv\n")
        f.write("- protocluster_members.csv\n")
        f.write("- agn_hosts.csv\n")
        f.write("- ultra_highz_zspec_gt12.csv\n")
        f.write("- impossible_galaxies.csv\n")

    print(f"\nSummary saved to: {summary}")

def main():
    print("="*60)
    print("SPECIAL SAMPLES EXTRACTION - Phase 2 S4")
    print("="*60)

    # Load data
    df = load_reference_catalog()

    # Extract samples
    excels = extract_excels(df)
    dusty = extract_a3cosmos(df)
    pc = extract_protoclusters(df)
    agn = extract_agn(df)
    uhz = extract_ultra_highz(df)
    impossible = extract_impossible_galaxy(df)

    # Summary
    create_summary(df, excels, dusty, pc, agn, uhz, impossible)

    print("\n" + "="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
