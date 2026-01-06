# GUIDE PRATIQUE - Setup Infrastructure Zenodo

**Date**: 6 Janvier 2026
**Projet**: VAL-Galaxies_primordiales - Phase 3
**Objectif**: Créer infrastructure Zenodo pendant téléchargement COSMOS2025
**Durée**: ~30-45 minutes

---

## 📌 Phase 1 Expliquée

### Qu'est-ce que la Phase 1 ?

**Phase 1: Préparation Infrastructure Locale (15 min)**

C'était la création de la structure de répertoires pour recevoir les données:

```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/

# Créer dossiers pour données brutes
mkdir -p data/jwst/raw/cosmos2025/catalog/
mkdir -p data/jwst/raw/cosmos2025/detection_images/
mkdir -p data/jwst/raw/cosmos2025/segmentation_maps/
mkdir -p data/jwst/raw/cosmos2025/lephare/
mkdir -p data/jwst/raw/cosmos2025/cigale/

# Créer dossiers pour traitement
mkdir -p data/jwst/processed/cosmos2025/

# Créer dossiers pour upload Zenodo
mkdir -p data/zenodo_upload/COSMOS2025_JANUS/
```

**Status actuel**: ✅ **Probablement déjà fait** puisque vous avez lancé le téléchargement

**Vérification**:
```bash
tree data/jwst/raw/cosmos2025/ -L 2
```

Si les dossiers existent et que le téléchargement est en cours → Phase 1 complétée ✅

---

## 🚀 Setup Zenodo MAINTENANT (Pendant Téléchargement)

### Pourquoi Créer Infrastructure Zenodo Maintenant ?

✅ **Parallélisation**: Téléchargement COSMOS2025 = 2-4 heures → utiliser ce temps!
✅ **Préparation**: Compte, token, templates prêts quand téléchargement fini
✅ **Test**: Vérifier que tout fonctionne avant upload massif
✅ **Optimisation**: Pas de temps perdu à attendre

---

## 📋 ÉTAPE PAR ÉTAPE - Infrastructure Zenodo

### Étape 1: Créer Compte Zenodo (5 min)

#### 1.1 Aller sur Zenodo

🌐 Ouvrir navigateur: **https://zenodo.org**

#### 1.2 S'inscrire

**Méthode recommandée: GitHub** (connexion rapide)

1. Cliquer **"Sign up"** (en haut à droite)
2. Choisir **"Sign up with GitHub"**
3. Autoriser Zenodo à accéder à votre compte GitHub
4. Vérifier email reçu de Zenodo
5. Cliquer lien de confirmation dans l'email

**Méthode alternative: ORCID** (recommandé pour chercheurs)

1. Si vous avez un ORCID → **"Sign up with ORCID"**
2. Sinon, créer ORCID d'abord: https://orcid.org/register
3. Autoriser Zenodo
4. Vérifier email

**Méthode alternative: Email direct**

1. Entrer email + mot de passe
2. Vérifier email
3. Confirmer compte

#### 1.3 Vérification

✅ Vous êtes connecté si vous voyez votre nom en haut à droite
✅ Cliquer sur votre nom → **"Settings"** pour accéder aux paramètres

**Résultat**: Compte Zenodo créé et vérifié ✅

---

### Étape 2: Obtenir ORCID (Optionnel mais Recommandé) (10 min)

#### 2.1 Qu'est-ce que ORCID ?

**ORCID** = Open Researcher and Contributor ID
- Identifiant unique chercheur (comme DOI pour publications)
- Format: `0000-0001-2345-6789`
- Utilisé dans toutes publications scientifiques
- **Gratuit** et permanent

#### 2.2 Créer ORCID (si vous n'en avez pas)

1. 🌐 Aller sur: **https://orcid.org/register**
2. Remplir formulaire:
   - Prénom
   - Nom
   - Email principal
   - Mot de passe
3. Vérifier email
4. Confirmer compte
5. **Copier votre ORCID** (format: `0000-0001-2345-6789`)

#### 2.3 Lier ORCID à Zenodo

1. Sur Zenodo → **Settings** (cliquer votre nom en haut à droite)
2. Onglet **"Linked accounts"**
3. Cliquer **"Connect"** à côté de ORCID
4. Autoriser connexion
5. Vérifier que ORCID apparaît dans votre profil

**Résultat**: ORCID créé et lié à Zenodo ✅

**À Noter**: Votre ORCID sera inclus automatiquement dans les métadonnées du dataset

---

### Étape 3: Générer Personal Access Token (5 min)

#### 3.1 Pourquoi un Token ?

Le **Personal Access Token** permet:
- Upload via API (nécessaire pour fichiers > 10 GB)
- Upload avec barre de progression
- Automatisation scripts Python
- **Sécurisé**: peut être révoqué à tout moment

#### 3.2 Créer Token

1. Sur Zenodo → **Settings** (votre nom en haut à droite)
2. Onglet **"Applications"** (menu gauche)
3. Section **"Personal access tokens"**
4. Cliquer **"New token"**
5. Donner un nom: `COSMOS2025_Upload`
6. Cocher les permissions:
   - ✅ **`deposit:write`** (obligatoire pour upload)
   - ✅ **`deposit:actions`** (obligatoire pour publier)
7. Cliquer **"Create"**
8. **⚠️ IMPORTANT**: Copier le token immédiatement (il ne sera plus affiché!)

**Format du token**: `ghsecret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` (environ 40 caractères)

#### 3.3 Sauvegarder Token Localement

**Option 1: Fichier .bashrc (recommandé)**

```bash
# Ouvrir .bashrc
nano ~/.bashrc

# Ajouter à la fin
export ZENODO_TOKEN='votre_token_ici'

# Sauvegarder (Ctrl+O, Enter, Ctrl+X)

# Recharger
source ~/.bashrc

# Vérifier
echo $ZENODO_TOKEN
```

**Option 2: Fichier .env (sécurisé)**

```bash
# Créer fichier .env
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
echo "ZENODO_TOKEN='votre_token_ici'" > .env

# Ajouter au .gitignore (ne JAMAIS commit token!)
echo ".env" >> .gitignore
```

**Résultat**: Token créé et sauvegardé en sécurité ✅

---

### Étape 4: Créer Dépôt Zenodo Draft (10 min)

#### 4.1 Pourquoi Créer Draft Maintenant ?

- **Réserver ID**: Obtenir deposition_id dès maintenant
- **Tester**: Vérifier que tout fonctionne
- **Préparer métadonnées**: Les remplir tranquillement
- **Upload progressif**: Ajouter fichiers au fur et à mesure

#### 4.2 Créer Draft via Interface Web

1. Sur Zenodo, cliquer **"Upload"** (en haut)
2. Cliquer **"New upload"**
3. Vous êtes sur la page de création

#### 4.3 Remplir Métadonnées Principales

**Section 1: Basic information**

| Champ | Valeur |
|-------|--------|
| **Upload type** | Dataset |
| **Publication date** | 2026-01-06 (aujourd'hui) |
| **Title** | `COSMOS2025_JANUS: Complete dataset for JANUS bimetric cosmology validation` |
| **Authors** | Cliquer "Add author"<br>- Name: `[Votre Nom]`<br>- ORCID: `[Votre ORCID si disponible]`<br>- Affiliation: `[Votre institution]` |
| **Description** | Copier texte ci-dessous ↓ |

**Description (copier-coller)**:
```
Complete COSMOS-Web Data Release 1 catalog (~784,000 galaxies) and JANUS bimetric cosmology analysis for primordial galaxies validation using JWST observations.

This dataset includes:
- COSMOS-Web DR1 complete catalog with photometry, photo-z, SED fitting, and morphology
- Detection images and segmentation maps (20 tiles)
- LePhare and CIGALE SED fitting products
- JANUS high-z galaxy selections (z > 8)
- MCMC analysis results (JANUS vs ΛCDM comparison)
- Reproduction scripts and documentation

Data source: Institut d'Astrophysique de Paris (IAP) - https://cosmos2025.iap.fr/
Project: VAL-Galaxies_primordiales
Model: JANUS Bimetric Cosmology
```

**Section 2: License**

- Sélectionner: **Creative Commons Attribution 4.0 International** (CC-BY-4.0)

**Section 3: Recommended information**

| Champ | Valeur |
|-------|--------|
| **Keywords** | `cosmology`, `JANUS model`, `bimetric gravity`, `JWST`, `COSMOS-Web`, `high-redshift galaxies`, `primordial galaxies`, `MCMC`, `Bayesian inference`, `dark matter`, `dark energy` |
| **Additional notes** | `Complete dataset for JANUS bimetric cosmology validation. All data from COSMOS-Web DR1 (Shuntov et al. 2025).` |

**Section 4: Related identifiers**

Cliquer **"Add related identifier"**:

1. **Relation type**: `is supplemented by`
   - **Identifier**: `https://cosmos2025.iap.fr/`
   - **Identifier type**: URL
   - **Resource type**: Dataset

2. **Relation type**: `is documented by`
   - **Identifier**: `https://github.com/PGPLF/JANUS`
   - **Identifier type**: URL
   - **Resource type**: Software

**Section 5: Contributors**

Cliquer **"Add contributor"**:

1. **Name**: `COSMOS-Web Team`
   - **Type**: Data collector
   - **Affiliation**: Institut d'Astrophysique de Paris

2. **Name**: `IAP CANDIDE Cluster`
   - **Type**: Hosting institution
   - **Affiliation**: Institut d'Astrophysique de Paris

#### 4.4 Sauvegarder Draft (NE PAS PUBLIER!)

1. En bas de page, cliquer **"Save"** (ne PAS cliquer "Publish"!)
2. ⚠️ **IMPORTANT**: Le dépôt reste en **brouillon**
3. Vous verrez: `This upload is in draft mode`

#### 4.5 Noter le Deposition ID

En haut de page, noter l'URL:
```
https://zenodo.org/deposit/1234567
                              ^^^^^^^ = deposition_id
```

**Copier ce deposition_id** → vous en aurez besoin pour l'upload API

**Résultat**: Draft Zenodo créé avec métadonnées ✅

---

### Étape 5: Créer Templates Locaux (10 min)

Pendant que le téléchargement continue, créer les templates pour Zenodo.

#### 5.1 Créer Structure Templates

```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
mkdir -p templates
cd templates/
```

#### 5.2 Créer README.md Principal

**Fichier**: `templates/ZENODO_README.md`

```bash
# Copier depuis INS-ZENODO.md lignes 26-246
# Ou utiliser commande Write ci-dessous
```

**Contenu**: Voir document séparé `templates/ZENODO_README.md` (sera créé par script)

#### 5.3 Créer CITATION.cff

**Fichier**: `templates/CITATION.cff`

```bash
# Copier depuis INS-ZENODO.md lignes 253-277
# Ou utiliser commande Write ci-dessous
```

**Contenu**: Voir document séparé `templates/CITATION.cff` (sera créé par script)

#### 5.4 Créer LICENSE

**Fichier**: `templates/LICENSE`

```bash
# Licence CC-BY-4.0 standard
# Sera créé par script
```

**Résultat**: Templates prêts pour upload Zenodo ✅

---

### Étape 6: Tester Token API (5 min)

#### 6.1 Vérifier Token Fonctionne

```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/
source /Users/pg-mac01/PythonProject/.venv/bin/activate

# Test simple API
curl -H "Authorization: Bearer $ZENODO_TOKEN" \
     https://zenodo.org/api/deposit/depositions
```

**Sortie attendue**: Liste de vos dépôts (JSON)
```json
[
  {
    "id": 1234567,
    "title": "COSMOS2025_JANUS: Complete dataset...",
    "state": "unsubmitted",
    ...
  }
]
```

Si vous voyez votre dépôt → ✅ Token fonctionne!

#### 6.2 Tester Upload Petit Fichier

```bash
# Créer fichier test
echo "Test Zenodo Upload" > test_zenodo.txt

# Upload via API
python3 << 'EOF'
import requests
import os

token = os.environ.get('ZENODO_TOKEN')
deposition_id = 1234567  # Remplacer par votre ID

# Obtenir bucket URL
r = requests.get(
    f'https://zenodo.org/api/deposit/depositions/{deposition_id}',
    headers={'Authorization': f'Bearer {token}'}
)
bucket_url = r.json()['links']['bucket']

# Upload fichier test
with open('test_zenodo.txt', 'rb') as f:
    r = requests.put(
        f'{bucket_url}/test_zenodo.txt',
        headers={'Authorization': f'Bearer {token}'},
        data=f
    )

print(f"Status: {r.status_code}")
print("✅ Upload test réussi!" if r.status_code == 201 else "❌ Erreur")
EOF
```

**Résultat attendu**:
```
Status: 201
✅ Upload test réussi!
```

**Vérifier sur Zenodo**:
1. Aller sur https://zenodo.org/deposit/[votre_deposition_id]
2. Vous devriez voir `test_zenodo.txt` dans la liste des fichiers
3. Supprimer ce fichier test (croix rouge à droite)

**Résultat**: API Zenodo fonctionnelle ✅

---

## 📊 Récapitulatif Setup Zenodo

### Checklist Complète

- [ ] **Étape 1**: Compte Zenodo créé et vérifié
- [ ] **Étape 2**: ORCID obtenu et lié (optionnel)
- [ ] **Étape 3**: Personal Access Token généré et sauvegardé
- [ ] **Étape 4**: Dépôt draft créé avec métadonnées
- [ ] **Étape 5**: Templates créés localement
- [ ] **Étape 6**: API testée avec petit fichier

### Informations à Noter

| Info | Valeur | Où la trouver |
|------|--------|---------------|
| **ZENODO_TOKEN** | `ghsecret_XXX...` | Settings → Applications → Personal access tokens |
| **Deposition ID** | `1234567` | URL du draft: https://zenodo.org/deposit/1234567 |
| **ORCID** | `0000-0001-2345-6789` | https://orcid.org/ (si créé) |
| **Bucket URL** | `https://zenodo.org/api/files/...` | Obtenu via API (sera dans deposition JSON) |

---

## ⏭️ Prochaines Étapes (Après Téléchargement)

### Quand Téléchargement COSMOS2025 Terminé

1. ✅ **Phase 3**: Valider intégrité (script Python)
2. ✅ **Phase 4**: Extraire z>8 locale
3. ✅ **Phase 5**: Préparer archives Zenodo (< 50 GB chacune)
4. ✅ **Phase 6**: Upload vers deposition_id (API Python)
5. ✅ **Phase 7**: Publier sur Zenodo → obtenir DOI

### Infrastructure Zenodo Ready

✅ **Compte** créé
✅ **Token** configuré
✅ **Draft** préparé avec métadonnées
✅ **Templates** prêts
✅ **API** testée

**Temps gagné**: ~30-45 min (fait en parallèle du téléchargement!)

---

## 🔧 Scripts à Créer Pendant Téléchargement

Profiter du temps de téléchargement pour créer les scripts:

### Script 1: validate_cosmos2025_complete.py

```bash
cd /Users/pg-mac01/JANUS/VAL-Galaxies_primordiales/scripts/
# Copier code depuis INS-COSMOS2025_HEBERGEMENT.md lignes 214-349
```

### Script 2: extract_cosmos2025_highz.py

```bash
# Copier code depuis INS-COSMOS2025.md lignes 178-314
```

### Script 3: prepare_zenodo_archives.sh

```bash
# Copier code depuis INS-COSMOS2025_HEBERGEMENT.md lignes 419-477
chmod +x prepare_zenodo_archives.sh
```

### Script 4: zenodo_upload.py

```bash
# Copier code depuis INS-COSMOS2025_HEBERGEMENT.md lignes 546-660
# IMPORTANT: Remplacer deposition_id par le vôtre!
```

---

## 📞 Support

### Problèmes Token

**Erreur**: `401 Unauthorized`
→ Vérifier que token est bien dans `$ZENODO_TOKEN`
→ Re-générer token si perdu

**Erreur**: `403 Forbidden`
→ Vérifier permissions token (deposit:write, deposit:actions)

### Problèmes Upload

**Erreur**: `Request Entity Too Large`
→ Fichier > 50 GB, découper avec `split`

**Erreur**: `Connection timeout`
→ Upload gros fichier en dehors heures de pointe

### Contact Zenodo

**Support**: support@zenodo.org
**Documentation**: https://help.zenodo.org/

---

## 📈 Progression Totale

```
Phase 1: Préparation Locale       ✅ COMPLÉTÉ (structure créée)
Phase 2: Téléchargement COSMOS    🔄 EN COURS (100-130 GB)
Zenodo Setup: Infrastructure      ✅ COMPLÉTÉ (ce guide)
Phase 3-7: À venir après téléchargement
```

**Estimation temps restant**:
- Téléchargement: 1-3 heures (selon connexion)
- Validation + extraction: 1 heure
- Archives + upload: 3-6 heures
- **Total restant**: ~5-10 heures

---

**Document**: GUIDE_ZENODO_SETUP.md
**Version**: 1.0
**Date**: 6 Janvier 2026
**Status**: Infrastructure Zenodo prête pour upload
**Prochaine action**: Attendre fin téléchargement → Phase 3 validation
