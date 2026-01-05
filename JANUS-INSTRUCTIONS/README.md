# README - Instructions JANUS

Ce dossier contient les instructions pour le projet JANUS.

## Objectif

Documenter les instructions de travail, les procédures et les guidelines pour le développement du projet JANUS.

## Liste des Instructions

- **INS-PDF_COMPILATION.md** : Guide de compilation PDF avec LaTeX et Jupyter
- **INS-FONTS_EQUATIONS.md** : Guide des polices et affichage correct des équations
- **README.md** : Ce fichier (vue d'ensemble des instructions)

## Convention de Nommage

Tous les fichiers d'instructions portent le préfixe `INS-` pour faciliter leur identification et gestion.

---

## État d'Installation / Configuration

### Session du 5 Janvier 2026 - 15:20 UTC

#### Machine: pg-mac01 (macOS Darwin 24.6.0, Apple Silicon arm64)

**✅ Outils Installés et Fonctionnels** :
- Python 3.13.0 (environnement virtuel: `/Users/pg-mac01/PythonProject/.venv/`)
- pip 25.3
- Jupyter Notebook 7.5.1
- JupyterLab 4.5.1
- nbconvert 7.16.6
- Git (via Homebrew)

**⚠️ Installation Manuelle Requise** :
- **LaTeX** (pdflatex, bibtex) : Nécessite privilèges administrateur
  - Commande: `brew install --cask basictex` (avec sudo)
  - Alternative: Télécharger MacTeX depuis https://www.tug.org/mactex/

**Environnement** :
- Répertoire de travail: `/`
- Homebrew: `/opt/homebrew/bin/brew`

---

### Instructions pour Nouvelles Machines

Lors de l'ajout d'une nouvelle machine de travail, ajouter une section ci-dessous:

#### Machine: [NOM] - [DATE]

**Système** : [OS, Version, Architecture]

**Outils Installés** :
- [ ] Python 3.10+
- [ ] Jupyter
- [ ] LaTeX
- [ ] Git

**Configuration** :
```bash
git clone https://github.com/PGPLF/JANUS.git
cd JANUS
# ... commandes spécifiques
```

**Notes** : [Notes spécifiques à cette machine]

---

## Mise à Jour des Instructions

Pour mettre à jour cet état d'installation:
1. Ajouter une nouvelle section datée
2. Conserver l'historique des sessions précédentes
3. Mettre à jour la liste des outils

