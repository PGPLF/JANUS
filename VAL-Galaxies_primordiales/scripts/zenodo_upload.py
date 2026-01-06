#!/usr/bin/env python3
"""
Upload COSMOS2025_JANUS vers Zenodo via API

Usage:
    export ZENODO_TOKEN='votre_token'
    export DEPOSITION_ID='votre_deposition_id'
    python zenodo_upload.py

Ou spécifier dans le code (non recommandé pour sécurité).

Upload avec barre de progression pour gros fichiers.
"""
import requests
import os
import sys
from pathlib import Path

def upload_large_file(bucket_url, filepath, token):
    """
    Upload fichier avec barre de progression

    Parameters
    ----------
    bucket_url : str
        URL du bucket Zenodo
    filepath : str
        Chemin fichier à uploader
    token : str
        Personal Access Token Zenodo

    Returns
    -------
    success : bool
        True si upload réussi
    """
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    print(f"\n{'='*60}")
    print(f"Upload: {filename}")
    print(f"Taille: {filesize / (1024**3):.2f} GB")
    print(f"{'='*60}")

    # Essayer d'importer tqdm, sinon upload sans progress bar
    try:
        from tqdm import tqdm
        use_tqdm = True
    except ImportError:
        print("⚠ tqdm non installé, upload sans progress bar")
        print("  Installer: pip install tqdm")
        use_tqdm = False

    with open(filepath, 'rb') as f:
        if use_tqdm:
            # Avec barre de progression
            with tqdm(total=filesize, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                def read_callback(chunk_size=8192*1024):  # 8 MB chunks
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        pbar.update(len(chunk))
                        yield chunk

                # Convertir generator en bytes pour requests
                data = b''.join(read_callback())

            # Upload (après lecture complète avec progress)
            print("\nEnvoi vers Zenodo...")
            r = requests.put(
                f'{bucket_url}/{filename}',
                headers={'Authorization': f'Bearer {token}'},
                data=data
            )
        else:
            # Sans barre de progression
            print("Upload en cours...")
            r = requests.put(
                f'{bucket_url}/{filename}',
                headers={'Authorization': f'Bearer {token}'},
                data=f
            )

    if r.status_code == 201:
        print(f"✅ {filename} uploadé avec succès!")
        return True
    else:
        print(f"❌ {filename} upload échoué!")
        print(f"   Status: {r.status_code}")
        print(f"   Erreur: {r.text[:200]}")
        return False

def get_bucket_url(deposition_id, token):
    """Obtenir bucket URL pour deposition"""
    r = requests.get(
        f'https://zenodo.org/api/deposit/depositions/{deposition_id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    if r.status_code != 200:
        print(f"❌ Erreur accès deposition {deposition_id}")
        print(f"   Status: {r.status_code}")
        print(f"   Erreur: {r.text[:200]}")
        return None

    return r.json()['links']['bucket']

def main():
    """Pipeline complet upload Zenodo"""

    print("="*60)
    print("UPLOAD COSMOS2025_JANUS VERS ZENODO")
    print("="*60)

    # 1. Récupérer token et deposition_id
    token = os.environ.get('ZENODO_TOKEN')
    deposition_id = os.environ.get('DEPOSITION_ID')

    # Si pas dans environment, demander
    if not token:
        print("\n❌ ZENODO_TOKEN non défini")
        print("   Définir: export ZENODO_TOKEN='votre_token'")
        print("   Ou éditer ce script ligne ~150")
        sys.exit(1)

    if not deposition_id:
        deposition_id = input("\nEntrer votre DEPOSITION_ID (depuis URL Zenodo): ")
        if not deposition_id:
            print("❌ DEPOSITION_ID requis")
            sys.exit(1)

    print(f"\nDeposition ID: {deposition_id}")
    print(f"Token: {token[:15]}...{token[-5:]}")

    # 2. Obtenir bucket URL
    print("\nObtention bucket URL...")
    bucket_url = get_bucket_url(deposition_id, token)

    if not bucket_url:
        sys.exit(1)

    print(f"✓ Bucket URL obtenu")

    # 3. Lister fichiers à uploader
    archives = [
        "data/zenodo_upload/COSMOS2025_catalog_segmaps.zip",
        "data/zenodo_upload/COSMOS2025_JANUS/01_detection_images/detection_part1.tar.gz",
        "data/zenodo_upload/COSMOS2025_JANUS/01_detection_images/detection_part2.tar.gz",
        "data/zenodo_upload/COSMOS2025_lephare.tar.gz",
        "data/zenodo_upload/COSMOS2025_JANUS/04_cigale/cigale_seds_v2.0.tar.gz",
        "data/zenodo_upload/COSMOS2025_JANUS_analysis.tar.gz"
    ]

    # Vérifier quels fichiers existent
    existing_files = []
    missing_files = []

    for archive in archives:
        if os.path.exists(archive):
            existing_files.append(archive)
        else:
            missing_files.append(archive)

    print(f"\n{'='*60}")
    print(f"FICHIERS À UPLOADER: {len(existing_files)}/{len(archives)}")
    print(f"{'='*60}")

    for f in existing_files:
        size_gb = os.path.getsize(f) / (1024**3)
        print(f"  ✓ {os.path.basename(f):<50} {size_gb:>8.2f} GB")

    if missing_files:
        print(f"\n⚠ Fichiers manquants ({len(missing_files)}):")
        for f in missing_files:
            print(f"  ✗ {f}")
        print("\n⚠ Exécuter prepare_zenodo_archives.sh d'abord?")

    if not existing_files:
        print("\n❌ Aucun fichier à uploader!")
        sys.exit(1)

    # Demander confirmation
    print(f"\n{'='*60}")
    total_size = sum(os.path.getsize(f) for f in existing_files) / (1024**3)
    print(f"Taille totale: {total_size:.2f} GB")
    print(f"Temps estimé: {total_size / 10:.0f}-{total_size / 5:.0f} min (selon connexion)")
    print(f"{'='*60}")

    response = input("\nContinuer upload? (oui/non): ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("Upload annulé")
        sys.exit(0)

    # 4. Upload tous les fichiers
    success = []
    failed = []

    for i, archive in enumerate(existing_files, 1):
        print(f"\n{'='*60}")
        print(f"Archive {i}/{len(existing_files)}")
        print(f"{'='*60}")

        if upload_large_file(bucket_url, archive, token):
            success.append(archive)
        else:
            failed.append(archive)
            # Demander si continuer
            if i < len(existing_files):
                response = input("\nErreur upload. Continuer avec fichier suivant? (oui/non): ")
                if response.lower() not in ['oui', 'o', 'yes', 'y']:
                    break

    # 5. Résumé
    print(f"\n{'='*60}")
    print("RÉSUMÉ UPLOAD")
    print(f"{'='*60}")
    print(f"\n✅ Réussi: {len(success)}/{len(existing_files)}")
    for f in success:
        print(f"   ✓ {os.path.basename(f)}")

    if failed:
        print(f"\n❌ Échoué: {len(failed)}")
        for f in failed:
            print(f"   ✗ {os.path.basename(f)}")

    print(f"\nDeposition ID: {deposition_id}")
    print(f"URL: https://zenodo.org/deposit/{deposition_id}")

    if len(success) == len(existing_files):
        print("\n✅ TOUS LES FICHIERS UPLOADÉS AVEC SUCCÈS!")
        print("\n⚠ NE PAS OUBLIER:")
        print("   1. Vérifier fichiers sur Zenodo")
        print("   2. PUBLIER sur interface Zenodo pour obtenir DOI")
        print("   3. Mettre à jour README/CITATION avec DOI")
        print("\nProchaine étape: Phase 7 - Publication DOI")
    else:
        print("\n⚠ Certains fichiers n'ont pas été uploadés")
        print("   Relancer le script pour retry")

if __name__ == '__main__':
    main()
