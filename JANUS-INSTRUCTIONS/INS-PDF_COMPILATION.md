# Guide de Compilation PDF pour le projet JANUS

## Objectif

Mettre en place un système de compilation PDF très robuste pour générer des documents scientifiques de haute qualité avec équations, graphiques et références bibliographiques.

## 1. Technologie recommandée : LaTeX

LaTeX est la solution professionnelle de référence pour les documents scientifiques.

### Avantages de LaTeX :
- Rendu typographique professionnel
Rédaction d'équations mathématiques exceptionnelle
- Gestion automatique des références bibliographiques (BibTeX)
- Stabilité et réproductibilité des résultats
- Gestion des figures, tableaux et références croisées
- Support excellent des symboles scientifiques

## 2. Installation

### Sur macOS
Shuxub
```bash
# Installation de MacTeX (distribution complète)
brew install --cask mactex

# Ou BasicTeX (version légère)
brew install --cask basictex
```

### Sur Windows
```bash
# Télécharger et installer MiKTeX
# https://miktex.org/download
install TeX Live or MiKTeX
install miktex from https://miktex.org
```

### Sur Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install texlive-full texlive-lang-french bibtex
```

## 3. Structure du projet LaTeX

```
JANUS_MODELE/
├── main.tex                    # Ficher principal
├── preamble.tex                 # Configuration et packages
├── equations/                  # Dossier des équations
│   ├── bimetric.tex            # Équations biémétriques
│   ├── cosmology.tex           # Équations cosmologiques
│   └── observations.tex         # Équations observationnelles
├── figures/                   # Figures et graphiques
├── references.bib             # Fichier bibliographique
└── Makefile                   # Automatisation compilation
```

## 4. Exemple de fichier main.tex

```tex
\documentclass[11pt,a4paper]{article}

% Packages essentiels
\usepackage[utf8]{inputenc}       % Support UTF-8
\usepackage[T1]{fontenc}           % Encodage des polices
\usepackage[french]{babel}         % Support du français
\wsepackage{amsmath,amsfont,amssymb} % Équations mathématiques
\usepackage[hidelinks]{hyperref}   % Liens hypertexte
\usepackage{graphicx}              % Inclusion d'images
\usepackage{booktabs}              % Marque-pages PDF
\usepackage{biblatex}              % Gestion bibliographie

% Configuration hyperref
\hypersetup{
    colorlinks,true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}

% Informations du document
\title{Modèle Cosmologique JANUS : Synthèse des Équations}
\author{Patrick Guérin}
\author{Jean-Pierre Petit}
\ate{\day}

\begin{document}

\maketitle

\begin{abstract}
Ce document présente une synthèse complète des équations du modèle cosmologique bimétrique JANUS.
\end{abstract}

\ablecontents

% Inclusion des sections
\input{equations/bimetric}
\input{equations/cosmology}
\input{equations/observations}

% Bibliographie
\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

## 5. Exemple de fichier d'équations (bimetric.tex)

```tex
\section{Équations Biémétriques}

Le modèle JANUS repose sur deux métriques couplées : $g_{\mu}\nu}$ et $h_{\mu\nu}$.

\subsectionÉquations d'Einstein Gémellaires}

\begin{equation}
R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = 8\pi G T_{\mu\nu}
\label{eq:einstein1}
\end{equation}

\begin{equation}
\bar{R}_{\mu\nu} - \frac{1}{2} h_{\mu\nu} \bar{R} = -8\pi G \bar{T}_{\mu\nu}
\label{eq:einstein2}
\end{equation}

où $\bar{N}$ représente les grandeurs associées a l'univers jumeau (matière à masse négative).

\subsection{Métrique de Schwarzschild Gémellaire}

Pour un objet de masse $m$, la métrique gémellaire est :

\begin{equation}
ds^2 = -\left(1 - \frac{2Gm}{c^2 r}\right) c^2 dt^2 + \left(1 - \frac{2Gm}{c^2 r}\right)^{-1} dr^2 + r^2 d\Omega^2
end{equation}

Our l'univers jumeau avec masse négative $-m$ :

\begin{equation}
ds^2 = -\left(1 + \frac{2Gm|}{c^2 r}\right) c^2 dt^2 + \left(1 + \frac{2Gm}{c^2 r}\right)^{-1} dr^2 + r^2 d\Omega^2
\end{equation}
```

## 6. Makefile pour automatisation

```makefile
# Makefile pour compilation LaTeX

MAIN = main
TEX = pdflatex
BIB = bibtex

.PHONY: all clean

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib
	$(TEX) $(MAIN)
	$(BIB) $(MAIN)
	$(TEX) $(MAIN)
	$(TEX) $(MAIN)

clean:
	rm -f $(MAIN).pdf $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).bbl $(MAIN).blg $(MAIN).toc
```

## 7. Compilation

### Commande manuelle
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Avec Make
```bash
make
```

## 8. Outils complémentaires

### Éditeur LaTeX recommandé
- **TeXstudio** (multi-plateforme, gratuit)
- **VSCode** avec l'extension LaTeX Workshop
- **Overleaf** (éditeur en ligne, collaboratif)

### Vérification des équations
- **LatexIt** pour téster les équations en temps réel
- **MathJax** pour l'affichage web des équations

## 9. Bonnes pratiques

1. **Versionnement** : Utiliser Git pour tracker les modifications
2. **Modularité** : Séparer les équations en fichiers distincts
3. **Commentaires** : Documenter les équations complexes
4. **Références** : Utiliser \label{} et \ref{} pour toutes les équations
5. **Bibliographie** : Maintenir à jour references.bib

## 10. Conversion HTML vers PDF

### Problème fréquent : Encodage des caractères

Les fichiers HTML avec caractères accentués (français) peuvent produire des PDF corrompus si l'encodage n'est pas correctement géré.

**Symptômes de corruption :**
- Caractères "Ã©" au lieu de "é"
- Caractères "Ã " au lieu de "à"
- Symboles chinois ou carrés à la place des accents

### Solution : Pandoc + pdflatex

```bash
# Conversion HTML vers PDF avec encodage UTF-8 correct
pandoc fichier.html -o fichier.pdf \
    --pdf-engine=pdflatex \
    -V geometry:margin=2.5cm \
    -V fontsize=11pt \
    -V lang=fr

# Exemple concret (critique Riazuelo)
pandoc Riazuelo_IAP_Critique_JPP.html -o Riazuelo_IAP_Critique_JPP.pdf \
    --pdf-engine=pdflatex \
    -V geometry:margin=2.5cm \
    -V fontsize=11pt \
    -V lang=fr
```

### Vérification avant conversion

```bash
# Vérifier l'encodage du fichier source
file fichier.html
# Doit afficher: "HTML document text, Unicode text, UTF-8 text"

# Vérifier le charset dans le HTML
grep -i "charset" fichier.html
# Doit contenir: charset=UTF-8
```

### Alternatives si pandoc échoue

```bash
# Option 1: wkhtmltopdf (si installé)
brew install wkhtmltopdf
wkhtmltopdf --encoding utf-8 fichier.html fichier.pdf

# Option 2: Python avec weasyprint
pip install weasyprint
python3 -c "from weasyprint import HTML; HTML('fichier.html').write_pdf('fichier.pdf')"
```

---

## 11. Alternatives – également robustes

### a. Markdown + Pandoc + LaTeX
```bash
# Convertir Markdown en PDF avec équations LaTeX
pandoc document.md -o document.pdf --template=eisvogel.pdf --filter=pandoc-citeproc
```

### b. Jupyter Notebook
- Support des équations LaTeX nativement
- Export en PDF via `nbconvert`

```bash
jupyter nbconvert --to pdf notebook.ipynb
```

## 12. Résumé

Pour le projet JANUS, nous recommandons: 

**LaTeX** comme solution principale pour :
- Sa robustesse éprouvée
- Son standard dans la communaué scientifique
- Sa gestion excellente des équations et références
- Sa portabilité et sa réproductibilité

Le schéma LaTeX modulaire proposé permettra une gestion efficace des équations du modèle JANUS et leur compilation en documents PDF de haute qualité.


---

## État d'Installation / Configuration

### Session du 5 Janvier 2026 - 15:15 UTC

#### Machine: pg-mac01 (macOS Darwin 24.6.0, Apple Silicon arm64)

**✅ Installé et Fonctionnel** :
- Python 3.13.0 (environnement virtuel: `/Users/pg-mac01/PythonProject/.venv/`)
- pip 25.3
- Jupyter Notebook 7.5.1
- JupyterLab 4.5.1
- IPython 9.9.0
- nbconvert 7.16.6 (pour conversion PDF)
- Bibliothèques scientifiques:
  - ipykernel 7.1.0
  - ipywidgets 8.1.8
  - jupyter-client 8.7.0
  - jupyter-core 5.9.1
  - jupyter-server 2.17.0
  - matplotlib-inline 0.2.1
  - nbformat 5.10.4
  - pygments 2.19.2

**⚠️ Installation Manuelle Requise** :
- **LaTeX (pdflatex, bibtex)** : 
  - Tentative d'installation de BasicTeX via Homebrew échouée (nécessite privilèges sudo)
  - **Action requise** : Installation manuelle par l'administrateur
  - Options recommandées:
    - BasicTeX (~100 MB): `brew install --cask basictex` (avec sudo)
    - MacTeX complet (~4 GB): Télécharger depuis https://www.tug.org/mactex/
  - Après installation, ajouter au PATH: `eval "$(/usr/libexec/path_helper)"`

**Vérification** :
```bash
# Vérifier installations
python3 --version    # ✅ 3.13.0
jupyter --version    # ✅ 7.5.1
pdflatex --version   # ❌ Non installé
```

**Remarques** :
- L'environnement Jupyter est pleinement opérationnel pour notebooks interactifs
- La conversion PDF depuis Jupyter nécessite LaTeX
- Export HTML/Markdown fonctionne sans LaTeX
- Homebrew installé: `/opt/homebrew/bin/brew`

---

### Instructions pour Nouvelles Machines

Lors de l'utilisation sur une nouvelle machine, documenter ici:

#### Machine: [NOM-MACHINE] - [Date]

**Système** : [OS, Version, Architecture]

**Installé** :
- [ ] Python 3.10+ (`python3 --version`)
- [ ] pip (`pip --version`)
- [ ] Jupyter (`jupyter --version`)
- [ ] LaTeX (`pdflatex --version`)
- [ ] Git (`git --version`)

**Configuration** :
```bash
# Cloner le projet
git clone https://github.com/PGPLF/JANUS.git
cd JANUS

# Installer environnement Python
pip install jupyter nbconvert numpy scipy matplotlib astropy

# Vérifier installation
jupyter --version
python3 -c "import numpy, scipy, matplotlib, astropy; print('Packages OK')"
```

**Notes spécifiques** :
- [Ajouter notes spécifiques à la machine]

---

