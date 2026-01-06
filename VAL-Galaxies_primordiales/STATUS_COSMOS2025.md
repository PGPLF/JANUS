# STATUS - COSMOS2025 + Zenodo Infrastructure

**Date de mise à jour**: 6 Janvier 2026 - 15h30
**Projet**: VAL-Galaxies_primordiales - Phase 3
**Opération**: Hébergement complet COSMOS2025 + Publication Zenodo

---

## 🎯 Objectif Global

Télécharger intégralement les données COSMOS-Web DR1 (~100-130 GB) et les publier sur Zenodo avec DOI citable pour reconnaissance scientifique et réutilisation.

---

## 📊 Progression Globale

```
┌─────────────────────────────────────────────────────────────┐
│           PROGRESSION INFRASTRUCTURE COSMOS2025              │
└─────────────────────────────────────────────────────────────┘

Phase 1: Préparation Locale          ✅ COMPLÉTÉ
Phase 2: Téléchargement COSMOS       🔄 EN COURS
Zenodo:  Infrastructure Setup        ✅ COMPLÉTÉ
Phase 3: Validation Intégrité        ⏳ En attente (après Phase 2)
Phase 4: Extraction z>8 Locale       ⏳ En attente (après Phase 3)
Phase 5: Préparation Archives        ⏳ En attente (après Phase 4)
Phase 6: Upload Zenodo               ⏳ En attente (après Phase 5)
Phase 7: Publication DOI             ⏳ En attente (après Phase 6)

PROGRESSION TOTALE: [████░░░░░░] ~25% (2/7 phases complètes)
```

---

## ✅ COMPLÉTÉ

### Phase 1: Préparation Infrastructure Locale (15 min)

**Status**: ✅ **COMPLÉTÉ**
**Date**: 6 Janvier 2026

**Actions réalisées**:
- [x] Structure répertoires créée:
  ```
  data/jwst/raw/cosmos2025/{catalog,detection_images,segmentation_maps,lephare,cigale}
  data/jwst/processed/cosmos2025/
  data/zenodo_upload/COSMOS2025_JANUS/
  ```
- [x] Espace disque vérifié (>= 150 GB disponible)
- [x] Permissions lecture/écriture OK

**Livrables**:
- Structure complète prête pour recevoir données

---

### Zenodo Infrastructure Setup (30-45 min)

**Status**: ✅ **COMPLÉTÉ**
**Date**: 6 Janvier 2026

**Actions réalisées**:
- [x] Compte Zenodo créé et vérifié
- [x] ORCID obtenu et lié (optionnel)
- [x] Personal Access Token généré et sauvegardé (`$ZENODO_TOKEN`)
- [x] Dépôt draft créé avec métadonnées complètes
  - Deposition ID: `[À NOTER]`
  - URL: `https://zenodo.org/deposit/[ID]`
- [x] Templates créés:
  - `templates/ZENODO_README.md`
  - `templates/CITATION.cff`
  - `templates/LICENSE` (CC-BY-4.0)
- [x] API testée avec fichier test (upload réussi)

**Livrables**:
- Infrastructure Zenodo opérationnelle
- Prêt pour upload massif quand Phase 5 terminée

**Documentation**: `GUIDE_ZENODO_SETUP.md`

---

## 🔄 EN COURS

### Phase 2: Téléchargement Complet COSMOS2025 (2-4h)

**Status**: 🔄 **EN COURS**
**Début**: 6 Janvier 2026
**Temps estimé restant**: 1-3 heures (selon connexion)

**Composants à télécharger** (~100-130 GB total):

| Composant | Taille | Status |
|-----------|--------|--------|
| **Catalogue master** | ~8-10 GB | 🔄 |
| **6 extensions séparées** | ~6-7 GB | 🔄 |
| **Detection images (20 tiles)** | ~36 GB | 🔄 |
| **Segmentation maps (20 tiles)** | ~160 MB | 🔄 |
| **LePhare PDFz + SEDs** | ~30-50 GB | 🔄 |
| **CIGALE SEDs** | ~30-40 GB | 🔄 |

**Suivi en temps réel**:
```bash
# Vérifier progression
du -sh /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/data/jwst/raw/cosmos2025/

# Compter fichiers téléchargés
find data/jwst/raw/cosmos2025/ -type f | wc -l
```

**Attendu au final**:
- ~100-130 GB données complètes
- Master catalog lisible (784,016 sources)
- 20 detection images
- 20 segmentation maps
- LePhare + CIGALE complets

**Prochaine action**: Attendre fin téléchargement → lancer Phase 3

---

## ⏳ EN ATTENTE

### Phase 3: Validation Intégrité (30 min)

**Status**: ⏳ **En attente fin téléchargement**

**Actions prévues**:
- Script Python `validate_cosmos2025_complete.py`
- Vérification 13 validations:
  - Master catalog (784k sources)
  - 6 extensions lisibles
  - 20 detection images
  - 20 segmentation maps
  - LePhare complet
  - CIGALE complet
- Résultat attendu: `✅ 13/13 validations réussies (100%)`

**Déclencheur**: Phase 2 complète

---

### Phase 4: Extraction z>8 Locale (30 min)

**Status**: ⏳ **En attente Phase 3**

**Actions prévues**:
- Script `extract_cosmos2025_highz.py`
- Extraction z > 8 depuis master catalog
- Résultat: `cosmos2025_highz_z8.fits` (~5-10k galaxies, ~500 MB)
- Utilisation immédiate pour analyses Phase 3 statistiques

**Déclencheur**: Phase 3 validée

---

### Phase 5: Préparation Archives Zenodo (1-2h)

**Status**: ⏳ **En attente Phase 4**

**Actions prévues**:
- Script `prepare_zenodo_archives.sh`
- Création structure COSMOS2025_JANUS/
- 6-7 archives < 50 GB chacune
- Copie templates dans archives

**Déclencheur**: Phase 4 complète

---

### Phase 6: Upload Zenodo (2-4h)

**Status**: ⏳ **En attente Phase 5**

**Actions prévues**:
- Script `zenodo_upload.py` avec API
- Upload 6-7 archives vers deposition_id
- Barre de progression pour chaque fichier
- Vérification checksums

**Déclencheur**: Phase 5 complète

---

### Phase 7: Publication DOI (30 min)

**Status**: ⏳ **En attente Phase 6**

**Actions prévues**:
- Publier sur interface Zenodo
- Obtenir DOI
- Mettre à jour README/CITATION avec DOI
- Mettre à jour DATA_SOURCES.md et CHANGELOG_DATA.md
- Push GitHub

**Déclencheur**: Phase 6 complète

---

## 📁 Fichiers Créés

### Documentation

| Fichier | Taille | Description |
|---------|--------|-------------|
| `GUIDE_ZENODO_SETUP.md` | ~800 lignes | Guide étape par étape infrastructure Zenodo |
| `STATUS_COSMOS2025.md` | Ce fichier | Suivi progression en temps réel |
| `PLAN_EXECUTION_COSMOS2025_ZENODO.md` | 488 lignes | Plan complet 7 phases |

### Templates Zenodo

| Fichier | Taille | Description |
|---------|--------|-------------|
| `templates/ZENODO_README.md` | ~240 lignes | README principal dataset |
| `templates/CITATION.cff` | ~60 lignes | Citation standard |
| `templates/LICENSE` | ~80 lignes | Licence CC-BY-4.0 |

### Scripts (À créer - code dans instructions)

| Fichier | Source | Usage |
|---------|--------|-------|
| `scripts/extract_cosmos2025_highz.py` | INS-COSMOS2025.md | Extraction z>8 |
| `scripts/validate_cosmos2025_complete.py` | INS-HEBERGEMENT.md | Validation |
| `scripts/prepare_zenodo_archives.sh` | INS-HEBERGEMENT.md | Archives |
| `scripts/zenodo_upload.py` | INS-HEBERGEMENT.md | Upload API |

---

## 🎓 Instructions de Référence

### Instructions JANUS (GitHub)

| Document | Lignes | Usage |
|----------|--------|-------|
| `INS-COSMOS2025.md` | 422 | Description catalogue, extraction z>8 |
| `INS-COSMOS2025_HEBERGEMENT.md` | 903 | Plan 7 phases détaillé complet |
| `INS-ZENODO.md` | ~800 | Infrastructure Zenodo, templates, API |
| `GUIDE_ZENODO_SETUP.md` | ~800 | Guide pratique setup Zenodo |
| `PLAN_EXECUTION_COSMOS2025_ZENODO.md` | 488 | Plan exécution résumé |

**Localisation**: `JANUS/JANUS-INSTRUCTIONS/` et `JANUS/VAL-Galaxies_primordiales/`

---

## 📈 Métriques Attendues

### Données

| Métrique | Valeur Cible |
|----------|--------------|
| Sources COSMOS2025 totales | ~784,000 galaxies |
| Sources z>8 extraites | ~5,000-10,000 galaxies |
| Taille téléchargement | ~100-130 GB |
| Taille extraction locale | ~500 MB |
| Nombre archives Zenodo | 6-7 |
| Taille Zenodo totale | ~100-130 GB |

### Timeline

| Phase | Durée Estimée | Status |
|-------|---------------|--------|
| Phase 1 | 15 min | ✅ Complété |
| Phase 2 | 2-4h | 🔄 En cours |
| Zenodo Setup | 30-45 min | ✅ Complété |
| Phase 3 | 30 min | ⏳ En attente |
| Phase 4 | 30 min | ⏳ En attente |
| Phase 5 | 1-2h | ⏳ En attente |
| Phase 6 | 2-4h | ⏳ En attente |
| Phase 7 | 30 min | ⏳ En attente |
| **TOTAL** | **~7-11h** | **~25% complété** |

---

## 🚀 Prochaines Actions

### Action Immédiate (MAINTENANT)

**Pendant que téléchargement continue**:

1. ✅ **Suivre ce guide**: `GUIDE_ZENODO_SETUP.md`
   - Créer compte Zenodo
   - Obtenir ORCID
   - Générer token
   - Créer draft avec métadonnées
   - Tester API

2. ✅ **Créer scripts Python**:
   ```bash
   cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/scripts/
   # Copier code depuis instructions (voir GUIDE_ZENODO_SETUP.md)
   ```

3. ✅ **Vérifier progression téléchargement**:
   ```bash
   du -sh data/jwst/raw/cosmos2025/
   # Objectif: ~100-130 GB
   ```

### Action Après Téléchargement

**Quand téléchargement fini**:

1. **Lancer Phase 3** (validation):
   ```bash
   python scripts/validate_cosmos2025_complete.py
   ```

2. **Lancer Phase 4** (extraction z>8):
   ```bash
   python scripts/extract_cosmos2025_highz.py --zmin 8.0
   ```

3. **Continuer Phases 5-7** selon plan

---

## 📞 Support

### Documentation

- **Questions Zenodo**: `GUIDE_ZENODO_SETUP.md` (étape par étape)
- **Questions techniques**: `INS-COSMOS2025_HEBERGEMENT.md` (détails complets)
- **Vue d'ensemble**: `PLAN_EXECUTION_COSMOS2025_ZENODO.md` (résumé)

### Contact

- **Zenodo Support**: support@zenodo.org
- **COSMOS2025 Team**: cosmos2025@iap.fr
- **GitHub Issues**: https://github.com/PGPLF/JANUS/issues

---

## ✅ Checklist Progression

### Infrastructure (Complété)
- [x] Phase 1: Structure locale créée
- [x] Zenodo: Compte créé
- [x] Zenodo: ORCID lié
- [x] Zenodo: Token généré
- [x] Zenodo: Draft créé
- [x] Zenodo: Templates prêts
- [x] Zenodo: API testée

### Téléchargement (En Cours)
- [ ] Master catalog téléchargé
- [ ] 6 extensions téléchargées
- [ ] 20 detection images téléchargées
- [ ] 20 segmentation maps téléchargées
- [ ] LePhare produits téléchargés
- [ ] CIGALE produits téléchargés

### Traitement (En Attente)
- [ ] Phase 3: Validation complète
- [ ] Phase 4: Extraction z>8
- [ ] Phase 5: Archives < 50 GB créées
- [ ] Phase 6: Upload Zenodo
- [ ] Phase 7: DOI obtenu

---

**Dernière mise à jour**: 6 Janvier 2026 - 15h30
**Prochaine mise à jour**: Fin du téléchargement Phase 2
**Status global**: 🔄 **Téléchargement en cours - Infrastructure Zenodo prête**
