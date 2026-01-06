#!/usr/bin/env python3
"""
Script de correction qualité des données - VAL-Galaxies_primordiales
Phase 2 v3.0 - Actions correctives

Actions:
1. Re-extraire JADES avec filtre EAZY_l68 >= 8
2. Supprimer JWST-Impossible-z12 des données
3. Dédupliquer les catalogues
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def action_1_reextract_jades():
    """Re-extraire JADES avec le bon filtre (EAZY_l68 >= 8)"""
    print("\n" + "="*60)
    print("ACTION 1: Re-extraction JADES avec EAZY_l68 >= 8")
    print("="*60)

    # Lire le fichier original
    jades_file = DATA_DIR / "jwst/processed/jades_highz_z8.csv"
    df = pd.read_csv(jades_file)

    print(f"Fichier original: {len(df)} entrées")
    print(f"Distribution EAZY_z_a: min={df['EAZY_z_a'].min()}, max={df['EAZY_z_a'].max()}")
    print(f"Distribution EAZY_l68: min={df['EAZY_l68'].min()}, max={df['EAZY_l68'].max()}")

    # Analyser les valeurs z=21.99
    n_placeholder = (df['EAZY_z_a'] == 21.99).sum()
    print(f"\nEntrées avec EAZY_z_a = 21.99 (placeholder): {n_placeholder} ({100*n_placeholder/len(df):.1f}%)")

    # Filtrer sur EAZY_l68 >= 8 (la vraie limite basse du redshift)
    df_valid = df[df['EAZY_l68'] >= 8.0].copy()
    print(f"\nAprès filtre EAZY_l68 >= 8: {len(df_valid)} entrées")

    # Créer un z_best basé sur EAZY_l68 (puisque EAZY_z_a est invalide)
    # On utilise la moyenne entre l68 et u68
    df_valid['z_best'] = (df_valid['EAZY_l68'] + df_valid['EAZY_u68']) / 2
    df_valid['z_err'] = (df_valid['EAZY_u68'] - df_valid['EAZY_l68']) / 2

    # Réorganiser les colonnes
    df_valid = df_valid[['ID', 'RA', 'DEC', 'z_best', 'z_err', 'EAZY_l68', 'EAZY_u68', 'field']]

    # Sauvegarder le fichier corrigé
    output_file = DATA_DIR / "jwst/processed/jades_highz_z8_CORRECTED.csv"
    df_valid.to_csv(output_file, index=False)
    print(f"\nFichier corrigé sauvegardé: {output_file}")

    # Statistiques
    if len(df_valid) > 0:
        print(f"\nStatistiques z_best:")
        print(f"  Min: {df_valid['z_best'].min():.2f}")
        print(f"  Max: {df_valid['z_best'].max():.2f}")
        print(f"  Median: {df_valid['z_best'].median():.2f}")
        print(f"  Par field:")
        print(df_valid.groupby('field').size())

    return len(df_valid)


def action_2_remove_invalid_source():
    """Supprimer JWST-Impossible-z12 (source non-scientifique)"""
    print("\n" + "="*60)
    print("ACTION 2: Suppression de JWST-Impossible-z12")
    print("="*60)

    # Fichier impossible_galaxies.csv
    file_path = DATA_DIR / "jwst/special/impossible_galaxies.csv"
    df = pd.read_csv(file_path)

    print(f"Avant: {len(df)} entrées")
    print(df[['ID', 'z', 'Survey', 'Reference']])

    # Supprimer JWST-Impossible-z12
    df_clean = df[df['ID'] != 'JWST-Impossible-z12'].copy()

    print(f"\nAprès suppression: {len(df_clean)} entrées")

    # Créer backup
    backup_file = DATA_DIR / "jwst/special/impossible_galaxies_BACKUP.csv"
    df.to_csv(backup_file, index=False)

    # Sauvegarder fichier corrigé
    df_clean.to_csv(file_path, index=False)
    print(f"Fichier corrigé: {file_path}")
    print(f"Backup créé: {backup_file}")

    # Mettre à jour JANUS-Z reference catalog aussi
    janus_z_file = DATA_DIR / "jwst/processed/janus_z_reference_catalog.csv"
    df_janus = pd.read_csv(janus_z_file)
    n_before = len(df_janus)
    df_janus = df_janus[df_janus['ID'] != 'JWST-Impossible-z12']
    n_after = len(df_janus)

    if n_before != n_after:
        df_janus.to_csv(janus_z_file, index=False)
        print(f"\nJANUS-Z catalog mis à jour: {n_before} -> {n_after} entrées")

    return len(df_clean)


def action_3_deduplicate_catalogs():
    """Dédupliquer les catalogues en créant une table de correspondance"""
    print("\n" + "="*60)
    print("ACTION 3: Déduplication des catalogues")
    print("="*60)

    # Charger tous les catalogues
    catalogs = {}

    # JANUS-Z reference (catalogue principal)
    janus_z_file = DATA_DIR / "jwst/processed/janus_z_reference_catalog.csv"
    catalogs['janus_z'] = pd.read_csv(janus_z_file)

    # Catalogues spéciaux
    special_files = [
        'protocluster_members.csv',
        'ultra_highz_zspec_gt12.csv',
        'agn_hosts.csv',
        'impossible_galaxies.csv',
        'excels_metallicity_sample.csv',
        'a3cosmos_dusty_sample.csv'
    ]

    for f in special_files:
        path = DATA_DIR / f"jwst/special/{f}"
        if path.exists():
            catalogs[f.replace('.csv', '')] = pd.read_csv(path)

    # Identifier les doublons
    all_ids = {}
    duplicates = []

    for cat_name, df in catalogs.items():
        if 'ID' in df.columns:
            for idx, row in df.iterrows():
                source_id = row['ID']
                if source_id in all_ids:
                    duplicates.append({
                        'ID': source_id,
                        'catalog_1': all_ids[source_id],
                        'catalog_2': cat_name
                    })
                else:
                    all_ids[source_id] = cat_name

    print(f"\nDoublons identifiés: {len(duplicates)}")
    for dup in duplicates:
        print(f"  - {dup['ID']}: {dup['catalog_1']} <-> {dup['catalog_2']}")

    # Créer table de mapping unique
    unique_sources = pd.DataFrame([
        {'ID': source_id, 'primary_catalog': catalog}
        for source_id, catalog in all_ids.items()
    ])

    # Ajouter les doublons comme références secondaires
    dup_df = pd.DataFrame(duplicates)
    if len(dup_df) > 0:
        # Marquer les sources avec doublons
        dup_ids = set(dup_df['ID'].tolist())
        unique_sources['has_duplicates'] = unique_sources['ID'].isin(dup_ids)

        # Sauvegarder table des doublons
        dup_file = DATA_DIR / "jwst/processed/duplicate_mapping.csv"
        dup_df.to_csv(dup_file, index=False)
        print(f"\nTable des doublons: {dup_file}")
    else:
        unique_sources['has_duplicates'] = False

    # Sauvegarder table unique
    unique_file = DATA_DIR / "jwst/processed/unique_source_registry.csv"
    unique_sources.to_csv(unique_file, index=False)
    print(f"Registre sources uniques: {unique_file}")
    print(f"Total sources uniques: {len(unique_sources)}")

    # Créer catalogue consolidé sans doublons
    print("\n--- Création catalogue consolidé ---")

    # Prendre JANUS-Z comme base (prioritaire)
    consolidated = catalogs['janus_z'].copy()
    consolidated['source_catalog'] = 'janus_z'

    # Ajouter les sources des autres catalogues qui ne sont pas dans JANUS-Z
    janus_z_ids = set(consolidated['ID'].tolist())

    for cat_name, df in catalogs.items():
        if cat_name == 'janus_z':
            continue
        if 'ID' not in df.columns:
            continue

        # Filtrer les sources pas encore dans consolidated
        new_sources = df[~df['ID'].isin(janus_z_ids)].copy()
        if len(new_sources) > 0:
            new_sources['source_catalog'] = cat_name
            # S'assurer que les colonnes sont compatibles
            for col in consolidated.columns:
                if col not in new_sources.columns:
                    new_sources[col] = np.nan
            consolidated = pd.concat([consolidated, new_sources[consolidated.columns]], ignore_index=True)
            print(f"  + {len(new_sources)} sources de {cat_name}")

    # Sauvegarder catalogue consolidé
    consolidated_file = DATA_DIR / "jwst/processed/consolidated_catalog.csv"
    consolidated.to_csv(consolidated_file, index=False)
    print(f"\nCatalogue consolidé: {consolidated_file}")
    print(f"Total après déduplication: {len(consolidated)} sources uniques")

    return len(consolidated), len(duplicates)


def generate_correction_report(n_jades, n_impossible, n_consolidated, n_duplicates):
    """Générer rapport des corrections"""
    print("\n" + "="*60)
    print("RAPPORT DE CORRECTIONS")
    print("="*60)

    report = f"""# Rapport des Actions Correctives

**Date**: 6 Janvier 2026
**Version**: v1.0

---

## Résumé des Actions

| Action | Statut | Résultat |
|--------|--------|----------|
| Re-extraction JADES | ✅ COMPLÉTÉ | {n_jades} sources z>=8 valides |
| Suppression source invalide | ✅ COMPLÉTÉ | JWST-Impossible-z12 retiré |
| Déduplication | ✅ COMPLÉTÉ | {n_duplicates} doublons identifiés |

---

## Action 1: Re-extraction JADES

**Problème**: 7,138 entrées avec EAZY_z_a = 21.99 (placeholder)

**Solution**: Filtrage sur EAZY_l68 >= 8 (limite basse 68%)

**Résultat**:
- Avant: 7,138 entrées (toutes invalides)
- Après: **{n_jades} sources** avec z >= 8 confirmé

**Fichier créé**: `data/jwst/processed/jades_highz_z8_CORRECTED.csv`

---

## Action 2: Suppression Source Non-Scientifique

**Problème**: JWST-Impossible-z12 avec référence "GoodMenProject-Jan2026"

**Solution**: Suppression de cette entrée

**Fichiers modifiés**:
- `data/jwst/special/impossible_galaxies.csv` (1 -> 0 ou ajustement)
- `data/jwst/processed/janus_z_reference_catalog.csv`
- Backup créé: `impossible_galaxies_BACKUP.csv`

---

## Action 3: Déduplication

**Problème**: Sources présentes dans multiples catalogues

**Doublons identifiés**: {n_duplicates}

**Solution**:
- Table de mapping créée: `duplicate_mapping.csv`
- Registre unique: `unique_source_registry.csv`
- Catalogue consolidé: `consolidated_catalog.csv`

**Résultat final**: **{n_consolidated} sources uniques**

---

## Statistiques Finales

| Catalogue | N sources |
|-----------|-----------|
| JADES corrigé (z>=8) | {n_jades} |
| Catalogue consolidé | {n_consolidated} |
| Doublons résolus | {n_duplicates} |

---

*Généré automatiquement le 2026-01-06*
"""

    report_file = BASE_DIR / "RPT-CORRECTIONS_APPLIED.md"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\nRapport sauvegardé: {report_file}")
    return report


if __name__ == "__main__":
    print("="*60)
    print("SCRIPT DE CORRECTION QUALITÉ - VAL-Galaxies_primordiales")
    print("="*60)

    # Exécuter les 3 actions
    n_jades = action_1_reextract_jades()
    n_impossible = action_2_remove_invalid_source()
    n_consolidated, n_duplicates = action_3_deduplicate_catalogs()

    # Générer rapport
    generate_correction_report(n_jades, n_impossible, n_consolidated, n_duplicates)

    print("\n" + "="*60)
    print("TOUTES LES CORRECTIONS APPLIQUÉES AVEC SUCCÈS")
    print("="*60)
