# Rapport d'Audit Qualité des Données Brutes

**Date**: 6 Janvier 2026
**Version**: v1.0
**Auteur**: Audit automatisé VAL-Galaxies_primordiales
**Référence**: Phase 2 - Contrôle qualité post-acquisition

---

## 🚨 RÉSUMÉ EXÉCUTIF

| Sévérité | Nombre | Description |
|----------|--------|-------------|
| **CRITIQUE** | 2 | Données inutilisables en l'état |
| **MAJEUR** | 3 | Corrections nécessaires avant analyse |
| **MINEUR** | 4 | Améliorations recommandées |

**Statut global**: ⚠️ **CORRECTIONS REQUISES**

---

## 1. PROBLÈMES CRITIQUES 🔴

### 1.1 JADES High-z Extraction - DONNÉES INVALIDES

**Fichier**: `data/jwst/processed/jades_highz_z8.csv`
**Lignes affectées**: 7,138 (100%)

**Description du problème**:
```
TOUTES les entrées ont z = 21.99
```

**Exemple**:
```csv
ID,RA,DEC,EAZY_z_a,EAZY_l68,EAZY_u68,field
291868,53.202,-27.747,21.99,6.225,21.563,GOODS-S
1152942,189.111,62.221,21.99,5.534,21.259,GOODS-N
```

**Analyse**:
- `EAZY_z_a = 21.99` est une valeur par défaut/placeholder du code EAZY
- Cela indique que le fit photométrique a échoué ou n'a pas convergé
- Les vraies valeurs z sont probablement dans `EAZY_l68` (borne basse 68%)
- **Les 7,138 "candidats z>=8" sont en fait des artefacts de pipeline**

**Impact**:
- Le comptage "7,138 sources z>=8" est **FAUX**
- Ces données ne peuvent PAS être utilisées pour l'analyse JANUS vs ΛCDM

**Action requise**:
1. Re-extraire depuis les catalogues JADES originaux avec critères corrects
2. Filtrer sur `EAZY_l68 >= 8` au lieu de `EAZY_z_a >= 8`
3. Ou télécharger le catalogue high-z officiel JADES

---

### 1.2 Source Non-Scientifique dans Données

**Fichier**: `data/jwst/special/impossible_galaxies.csv`
**Entrée**: JWST-Impossible-z12

**Problème**:
```csv
JWST-Impossible-z12,12.15,0.25,phot,9.02,0.3,1.15,6.8,0,0,field,-1,JWST-Press,GoodMenProject-Jan2026,-1.0
```

**Analyse**:
- Référence "GoodMenProject-Jan2026" n'est **PAS** une publication scientifique peer-reviewed
- Incertitude z_err = 0.25 (20%) trop élevée pour une confirmation
- z_type = "phot" (photométrique) sans confirmation spectroscopique

**Impact**:
- Introduit un biais dans les statistiques "impossible galaxies"
- Compromet la crédibilité scientifique du dataset

**Action requise**:
1. Supprimer cette entrée ou la marquer comme "non-confirmée"
2. Ne conserver que AC-2168 qui a une référence arXiv valide

---

## 2. PROBLÈMES MAJEURS 🟠

### 2.1 Doublons Inter-Catalogues

**Sources dupliquées identifiées**:

| Source | Fichier 1 | Fichier 2 | Fichier 3 |
|--------|-----------|-----------|-----------|
| GHZ2 | ultra_highz_zspec_gt12.csv | protocluster_members.csv | janus_z_reference_catalog.csv |
| GHZ9-confirmed | agn_hosts.csv | protocluster_members.csv | janus_z_reference_catalog.csv |
| GHZ1-confirmed | protocluster_members.csv | janus_z_reference_catalog.csv | - |
| GHZ7-confirmed | protocluster_members.csv | janus_z_reference_catalog.csv | - |
| GHZ8-confirmed | protocluster_members.csv | janus_z_reference_catalog.csv | - |
| JD1-member1/2 | protocluster_members.csv | janus_z_reference_catalog.csv | - |
| A2744-z7p9OD-* | protocluster_members.csv | janus_z_reference_catalog.csv | - |

**Impact**:
- Comptage total gonflé artificiellement
- Statistiques biaisées sur N(z), SMF

**Action requise**:
1. Créer une table de correspondance ID unique
2. Marquer les entrées comme "alias" dans les catalogues spéciaux
3. Recalculer les statistiques sans doublons

---

### 2.2 Valeurs Manquantes Encodées Incorrectement

**Fichier**: `data/jwst/processed/janus_z_reference_catalog.csv`

**Problème**:
```
metallicity_12OH = -1.0  (devrait être NaN ou vide)
metallicity_12OH = 8.5   (valeur par défaut suspecte - répétée 40+ fois)
log_Mvir = -1.0          (pour galaxies field - OK mais inconsistant)
```

**Entrées avec metallicity_12OH = 8.5 (valeur placeholder)**:
- JADES-DR5-preview-001 à -100 (nombreuses)
- COSMOS-Web-DR2-* (nombreuses)

**Impact**:
- Analyses de métallicité biaisées
- Valeurs placeholder peuvent être prises pour vraies mesures

**Action requise**:
1. Remplacer -1.0 et 8.5 par NaN ou chaîne vide
2. Documenter explicitement les valeurs manquantes

---

### 2.3 CEERS NIRSpec - Catalogue Incomplet

**Fichier**: `data/jwst/raw/ceers/ceers_nirspec_master_dr0.7.csv`

**Contenu actuel**:
```csv
MSA_ID,ra,dec,prism_4,Mgrat_4,prism_5,...
```

**Problème**:
- Ce fichier est un **catalogue de pointage MSA**, PAS un catalogue de redshifts
- Aucune colonne z_spec, log_Mstar, SFR
- Inutilisable pour l'analyse scientifique

**Action requise**:
1. Télécharger le catalogue spectroscopique CEERS (avec redshifts)
2. URL: https://web.corral.tacc.utexas.edu/ceersdata/DR07/
3. Fichier nécessaire: `ceers_spectroscopic_catalog_dr0.7.fits`

---

## 3. PROBLÈMES MINEURS 🟡

### 3.1 Labbé+23 - Valeurs Vides

**Fichier**: `data/reference/labbe2023_sample.ecsv`

**Lignes concernées**: 44, 45, 49 (sources 14924, 16624, 35300)
```
f435w = ""  e435w = ""  (chaînes vides au lieu de NaN)
```

**Action**: Remplacer "" par NaN dans les valeurs photométriques

---

### 3.2 HST Legacy - Aucune Spectroscopie

**Fichier**: `data/complementary/hst_legacy.csv`

**Observation**: Toutes les 90 sources ont `z_spec = -1`

**Impact**: Limité - c'est cohérent avec les données HST pré-JWST
**Recommandation**: Documenter cette limitation dans l'analyse

---

### 3.3 Redshifts z = 14.5 Multiples

**Fichier**: `data/jwst/processed/janus_z_reference_catalog.csv`

**Entrées avec z = 14.5 exactement**:
- JADES-DR5-preview-014, -020, -021, -024, -047, -048, -067, -082, -085, -096

**Suspicion**: z = 14.5 pourrait être une limite supérieure du fit, pas une mesure

**Recommandation**: Vérifier avec sources JADES DR5 originales

---

### 3.4 Incohérence Format ID

**Observation**:
- Labbé+23: IDs numériques (2859, 7274, ...)
- JANUS-Z: IDs alphanumériques (JADES-GS-z14-0, GHZ9-confirmed, ...)
- JADES extraction: IDs numériques longs (291868, 1152942, ...)

**Recommandation**: Créer table de mapping ID unifié

---

## 4. STATISTIQUES CORRIGÉES

### Avant correction:
| Catalogue | N déclaré |
|-----------|-----------|
| JADES z>=8 | 7,138 |
| JANUS-Z | 236 |
| Total unique | ~7,600 |

### Après analyse:
| Catalogue | N valide | N problématique |
|-----------|----------|-----------------|
| JADES z>=8 | **~0** | 7,138 (z=21.99) |
| JANUS-Z | ~220 | ~16 doublons |
| Labbé+23 | 6 | 0 |
| Spectro z>8 | 110 | 0 |
| HST Legacy | 90 | 0 (z_phot only) |
| **Total exploitable** | **~420** | - |

---

## 5. PLAN DE CORRECTION

### Priorité 1 (Immédiate):
- [ ] Re-extraire JADES avec filtrage correct sur z_phot
- [ ] Supprimer JWST-Impossible-z12 des données

### Priorité 2 (Court terme):
- [ ] Dédupliquer les catalogues
- [ ] Télécharger catalogue spectro CEERS correct
- [ ] Normaliser valeurs manquantes (NaN)

### Priorité 3 (Amélioration):
- [ ] Créer table de mapping ID unique
- [ ] Documenter limitations HST
- [ ] Vérifier sources z=14.5

---

## 6. IMPACT SUR LES PHASES

### Phase 2 (Acquisition):
- **Conformité révisée**: 95% → **70%** (JADES invalide)
- Données exploitables réduites de 7,600 à ~420 sources

### Phase 3 (Analyse):
- Analyse ΛCDM vs JANUS: **POSSIBLE** avec ~420 sources
- Fonction de masse: Limitée par échantillon réduit
- UV LF z>10: Seulement ~50 sources spectro confirmées

---

## 7. RECOMMANDATIONS

1. **NE PAS UTILISER** `jades_highz_z8.csv` en l'état
2. **Prioriser** le catalogue JANUS-Z (236 sources, qualité validée)
3. **Complémenter** avec spectro_confirmed.csv (110 sources)
4. **Vérifier** chaque source z>12 individuellement

---

*RPT-AUDIT_DATA_QUALITY.md - VAL-Galaxies_primordiales*
*Généré le 2026-01-06*
