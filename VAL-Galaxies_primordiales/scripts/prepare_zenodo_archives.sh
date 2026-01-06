#!/bin/bash
# Préparation archives Zenodo COSMOS2025_JANUS
#
# Usage:
#   bash scripts/prepare_zenodo_archives.sh
#
# Crée structure COSMOS2025_JANUS/ et archives < 50 GB pour upload Zenodo

set -e  # Exit on error

echo "=========================================="
echo "PRÉPARATION ARCHIVES ZENODO"
echo "=========================================="

# Chemins
BASE_RAW="data/jwst/raw/cosmos2025"
BASE_PROCESSED="data/jwst/processed/cosmos2025"
ZENODO_DIR="data/zenodo_upload/COSMOS2025_JANUS"

# Vérifier que données existent
if [ ! -d "$BASE_RAW" ]; then
    echo "❌ Erreur: $BASE_RAW n'existe pas"
    echo "   Lancer Phase 2 (téléchargement) d'abord"
    exit 1
fi

echo ""
echo "Création structure Zenodo..."
mkdir -p "$ZENODO_DIR"/{00_catalog/extensions_separate,01_detection_images,02_segmentation_maps,03_lephare,04_cigale,05_janus_analysis/{mcmc_chains,jwst_highz_selection,comparative_fits},scripts}

# Copier README et métadonnées
echo "Copie templates..."
if [ -f "templates/ZENODO_README.md" ]; then
    cp templates/ZENODO_README.md "$ZENODO_DIR/README.md"
    echo "  ✓ README.md"
else
    echo "  ⚠ templates/ZENODO_README.md non trouvé"
fi

if [ -f "templates/CITATION.cff" ]; then
    cp templates/CITATION.cff "$ZENODO_DIR/CITATION.cff"
    echo "  ✓ CITATION.cff"
else
    echo "  ⚠ templates/CITATION.cff non trouvé"
fi

if [ -f "templates/LICENSE" ]; then
    cp templates/LICENSE "$ZENODO_DIR/LICENSE"
    echo "  ✓ LICENSE"
else
    echo "  ⚠ templates/LICENSE non trouvé"
fi

# 1. Catalogue (master + extensions)
echo ""
echo "Archive 1: Catalogue..."
if [ -f "$BASE_RAW/catalog/COSMOS-Web_master_v2.0.fits" ]; then
    cp "$BASE_RAW/catalog/COSMOS-Web_master_v2.0.fits" "$ZENODO_DIR/00_catalog/"
    echo "  ✓ Master catalog copié"
else
    echo "  ⚠ Master catalog non trouvé"
fi

if [ -d "$BASE_RAW/catalog" ]; then
    cp "$BASE_RAW/catalog"/cosmos_web_*.fits "$ZENODO_DIR/00_catalog/extensions_separate/" 2>/dev/null || echo "  ⚠ Extensions non trouvées"
    echo "  ✓ Extensions copiées"
fi

# 2. Detection images (split en 2 archives)
echo ""
echo "Archive 2-3: Detection images..."
if [ -d "$BASE_RAW/detection_images" ]; then
    cd "$BASE_RAW/detection_images"

    # Compter fichiers
    n_tiles=$(ls *.fits 2>/dev/null | wc -l | tr -d ' ')
    echo "  Trouvé $n_tiles tiles"

    if [ "$n_tiles" -gt 0 ]; then
        # Split en 2 archives
        ls *.fits | head -10 | tar -czf "../../zenodo_upload/COSMOS2025_JANUS/01_detection_images/detection_part1.tar.gz" -T - 2>/dev/null && echo "  ✓ Part 1 créée" || echo "  ⚠ Erreur part 1"
        ls *.fits | tail -10 | tar -czf "../../zenodo_upload/COSMOS2025_JANUS/01_detection_images/detection_part2.tar.gz" -T - 2>/dev/null && echo "  ✓ Part 2 créée" || echo "  ⚠ Erreur part 2"
    fi

    cd - > /dev/null
else
    echo "  ⚠ Detection images non trouvées"
fi

# 3. Segmentation maps
echo ""
echo "Archive 3: Segmentation..."
if [ -d "$BASE_RAW/segmentation_maps" ]; then
    cd "$BASE_RAW/segmentation_maps"
    tar -czf "../../zenodo_upload/COSMOS2025_JANUS/02_segmentation_maps/segmentation_all.tar.gz" *.fits 2>/dev/null && echo "  ✓ Segmentation archive créée" || echo "  ⚠ Erreur segmentation"
    cd - > /dev/null
else
    echo "  ⚠ Segmentation maps non trouvées"
fi

# 4. LePhare
echo ""
echo "Archive 4: LePhare..."
if [ -d "$BASE_RAW/lephare" ]; then
    [ -f "$BASE_RAW/lephare/lephare_pdfz_v2.0.pkl" ] && cp "$BASE_RAW/lephare/lephare_pdfz_v2.0.pkl" "$ZENODO_DIR/03_lephare/" && echo "  ✓ PDFz copié"
    [ -f "$BASE_RAW/lephare/lephare_seds_v2.0.tar.gz" ] && cp "$BASE_RAW/lephare/lephare_seds_v2.0.tar.gz" "$ZENODO_DIR/03_lephare/" && echo "  ✓ SEDs copié"
else
    echo "  ⚠ LePhare non trouvé"
fi

# 5. CIGALE
echo ""
echo "Archive 5: CIGALE..."
if [ -f "$BASE_RAW/cigale/cigale_seds_v2.0.tar.gz" ]; then
    cp "$BASE_RAW/cigale/cigale_seds_v2.0.tar.gz" "$ZENODO_DIR/04_cigale/"
    echo "  ✓ CIGALE SEDs copié"
else
    echo "  ⚠ CIGALE SEDs non trouvé"
fi

# 6. JANUS analysis
echo ""
echo "Archive 6: JANUS analysis..."
if [ -f "$BASE_PROCESSED/cosmos2025_highz_z8.fits" ]; then
    cp "$BASE_PROCESSED/cosmos2025_highz_z8.fits" "$ZENODO_DIR/05_janus_analysis/jwst_highz_selection/"
    echo "  ✓ High-z selection copié"
else
    echo "  ⚠ High-z selection non trouvé (exécuter extract_cosmos2025_highz.py d'abord)"
fi

# MCMC chains (si disponibles)
if [ -d "results/mcmc" ]; then
    cp results/mcmc/*.h5 "$ZENODO_DIR/05_janus_analysis/mcmc_chains/" 2>/dev/null && echo "  ✓ MCMC chains copiés" || echo "  ⚠ MCMC chains non trouvés"
fi

# Scripts reproduction
echo ""
echo "Copie scripts reproduction..."
[ -f "scripts/extract_cosmos2025_highz.py" ] && cp scripts/extract_cosmos2025_highz.py "$ZENODO_DIR/scripts/" && echo "  ✓ extract_cosmos2025_highz.py"
[ -f "scripts/validate_cosmos2025_complete.py" ] && cp scripts/validate_cosmos2025_complete.py "$ZENODO_DIR/scripts/" && echo "  ✓ validate_cosmos2025_complete.py"
[ -f "requirements.txt" ] && cp requirements.txt "$ZENODO_DIR/scripts/" && echo "  ✓ requirements.txt"
[ -f "environment.yml" ] && cp environment.yml "$ZENODO_DIR/scripts/" && echo "  ✓ environment.yml"

# Créer archives finales
echo ""
echo "=========================================="
echo "CRÉATION ARCHIVES FINALES"
echo "=========================================="

cd data/zenodo_upload/

echo ""
echo "Archive 1: Catalogue + Segmentation..."
zip -r COSMOS2025_catalog_segmaps.zip \
    COSMOS2025_JANUS/00_catalog/ \
    COSMOS2025_JANUS/02_segmentation_maps/ \
    COSMOS2025_JANUS/README.md \
    COSMOS2025_JANUS/CITATION.cff \
    COSMOS2025_JANUS/LICENSE \
    > /dev/null 2>&1 && echo "  ✓ COSMOS2025_catalog_segmaps.zip créé" || echo "  ⚠ Erreur création zip"

echo ""
echo "Archive 4: LePhare complet..."
if [ -d "COSMOS2025_JANUS/03_lephare" ]; then
    cd COSMOS2025_JANUS/03_lephare
    tar -czf ../../../COSMOS2025_lephare.tar.gz * > /dev/null 2>&1 && echo "  ✓ COSMOS2025_lephare.tar.gz créé" || echo "  ⚠ Erreur LePhare"
    cd ../..
fi

echo ""
echo "Archive 6: JANUS analysis..."
tar -czf COSMOS2025_JANUS_analysis.tar.gz \
    COSMOS2025_JANUS/05_janus_analysis/ \
    COSMOS2025_JANUS/scripts/ \
    > /dev/null 2>&1 && echo "  ✓ COSMOS2025_JANUS_analysis.tar.gz créé" || echo "  ⚠ Erreur analysis"

cd ../..

# Vérifier tailles
echo ""
echo "=========================================="
echo "VÉRIFICATION TAILLES"
echo "=========================================="

cd data/zenodo_upload/
echo ""
ls -lh *.zip *.tar.gz 2>/dev/null || true
ls -lh COSMOS2025_JANUS/01_detection_images/*.tar.gz 2>/dev/null || true
ls -lh COSMOS2025_JANUS/04_cigale/*.tar.gz 2>/dev/null || true

echo ""
echo "⚠ IMPORTANT: Vérifier que toutes archives < 50 GB"
echo ""

cd ../..

# Résumé
echo ""
echo "=========================================="
echo "✅ PRÉPARATION TERMINÉE"
echo "=========================================="
echo ""
echo "Structure Zenodo préparée: $ZENODO_DIR"
echo ""
du -sh "$ZENODO_DIR" 2>/dev/null || true
echo ""
echo "Archives créées:"
echo "  1. COSMOS2025_catalog_segmaps.zip"
echo "  2. detection_part1.tar.gz"
echo "  3. detection_part2.tar.gz"
echo "  4. COSMOS2025_lephare.tar.gz"
echo "  5. cigale_seds_v2.0.tar.gz"
echo "  6. COSMOS2025_JANUS_analysis.tar.gz"
echo ""
echo "Prochaine étape: Phase 6 - Upload Zenodo"
echo "  python scripts/zenodo_upload.py"
