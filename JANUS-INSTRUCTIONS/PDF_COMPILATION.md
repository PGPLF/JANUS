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

## 10. Alternatives – également robustes

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

## 11. Résumé

Pour le projet JANUS, nous recommandons: 

**LaTeX** comme solution principale pour :
- Sa robustesse éprouvée
- Son standard dans la communaué scientifique
- Sa gestion excellente des équations et références
- Sa portabilité et sa réproductibilité

Le schéma LaTeX modulaire proposé permettra une gestion efficace des équations du modèle JANUS et leur compilation en documents PDF de haute qualité.
