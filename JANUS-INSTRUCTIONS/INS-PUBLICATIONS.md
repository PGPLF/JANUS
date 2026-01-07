# INS-PUBLICATIONS : Guide des Bonnes Pratiques de Publication Scientifique

**Version** : 1.0
**Date** : Janvier 2026
**Projet** : JANUS Cosmology Validation

---

## Table des matières

1. [Structure d'un article scientifique](#1-structure-dun-article-scientifique)
2. [Références bibliographiques](#2-références-bibliographiques)
3. [Équations et formules](#3-équations-et-formules)
4. [Tableaux](#4-tableaux)
5. [Figures](#5-figures)
6. [Sections obligatoires](#6-sections-obligatoires)
7. [Template LaTeX](#7-template-latex)
8. [Checklist avant soumission](#8-checklist-avant-soumission)

---

## 1. Structure d'un article scientifique

### 1.1 Ordre des sections (standard A&A/ApJ/MNRAS)

```
1. Title
2. Author(s) + Affiliations
3. Abstract (150-300 mots)
4. Keywords (5-8 termes)
5. Introduction
6. Data / Observations
7. Methods / Analysis
8. Results
9. Discussion
10. Conclusions
11. Acknowledgments
12. Data Availability Statement
13. References
14. Appendices (optionnel)
```

### 1.2 Header auteur complet

```latex
\author{Prénom Nom\thanks{Corresponding author: email@domain.com}\\
\small Affiliation\\
\small Ville, Pays\\
\\
\small \textit{Author contributions}: Description des contributions.\\
\small \textit{Funding}: Sources de financement ou "No specific funding".\\
\small \textit{Conflicts of interest}: Déclaration ou "None declared".\\
\small \textit{Data availability}: URL du dépôt de données.}
```

---

## 2. Références bibliographiques

### 2.1 Style recommandé : Auteur-année (natbib)

Le style **auteur-année** est le standard pour les journaux d'astrophysique (A&A, ApJ, MNRAS, Nature Astronomy).

```latex
\usepackage{natbib}
\bibliographystyle{aasjournal}  % ou aa, mnras, apalike
```

### 2.2 Règles de formatage

| Règle | Exemple correct | Exemple incorrect |
|-------|-----------------|-------------------|
| Ordre alphabétique | Bunker... Casey... Petit... | Petit... Bunker... Casey... |
| Noms complets | Petit, J.-P. | Petit, JP ou J.P. Petit |
| Année entre parenthèses | (2024) | 2024 |
| Journal abrégé standard | ApJ, A&A, MNRAS | Astrophysical Journal |
| Volume en gras | **84**, 879 | 84, 879 |
| Pages ou article ID | 879 ou L14 | p. 879 |

### 2.3 Format des entrées bibliographiques

#### Article de journal
```latex
\bibitem[Petit et al.(2024)]{petit2024}
Petit, J.-P., Esculier, T., \& d'Agostini, G.\ 2024,
European Physical Journal C, \textbf{84}, 879
```

#### Preprint arXiv
```latex
\bibitem[Bunker et al.(2025)]{bunker2025}
Bunker, A.~J., Cameron, A.~J., Curtis-Lake, E., et al.\ 2025,
arXiv:2510.01033
```

#### Livre
```latex
\bibitem[Weinberg(1972)]{weinberg1972}
Weinberg, S.\ 1972, Gravitation and Cosmology
(New York: Wiley)
```

### 2.4 Tri alphabétique obligatoire

Les références DOIVENT être triées par :
1. **Nom du premier auteur** (alphabétique)
2. **Année** (croissante si même auteur)
3. **Lettre suffixe** (a, b, c) si même auteur et année

```latex
% CORRECT
\bibitem[Astropy Collaboration(2022)]{astropy2022}
\bibitem[Boylan-Kolchin(2023)]{boylan2023}
\bibitem[Bunker et al.(2024)]{bunker2024}
\bibitem[Petit \& d'Agostini(2014)]{petit2014}
\bibitem[Petit et al.(2024a)]{petit2024a}
\bibitem[Petit et al.(2024b)]{petit2024b}
```

### 2.5 Citations dans le texte

| Type | Commande | Résultat |
|------|----------|----------|
| Parenthétique | `\citep{petit2024}` | (Petit et al. 2024) |
| Textuelle | `\citet{petit2024}` | Petit et al. (2024) |
| Multiple | `\citep{petit2024,bunker2025}` | (Petit et al. 2024; Bunker et al. 2025) |
| Avec page | `\citep[p.~15]{petit2024}` | (Petit et al. 2024, p. 15) |
| Année seule | `\citeyear{petit2024}` | 2024 |

### 2.6 Nombre minimum de références

| Type de publication | Minimum recommandé |
|---------------------|-------------------|
| Letter (ApJL, A&A Letters) | 15-25 |
| Article standard | 30-50 |
| Review | 100+ |

---

## 3. Équations et formules

### 3.1 Éviter les débordements en deux colonnes

```latex
% PROBLÈME : équation trop longue
\begin{equation}
\phi(M) = 0.4 \ln(10) \phi^* 10^{0.4(M^*-M)(\alpha+1)} \exp[-10^{0.4(M^*-M)}]
\end{equation}

% SOLUTION 1 : Fractions
\begin{equation}
\phi(M) = \frac{2}{5} \ln(10) \, \phi^* \, 10^{0.4(M^*-M)(\alpha+1)}
e^{-10^{0.4(M^*-M)}}
\end{equation}

% SOLUTION 2 : Multiligne
\begin{align}
\phi(M) &= 0.4 \ln(10) \, \phi^* \nonumber \\
&\quad \times 10^{0.4(M^*-M)(\alpha+1)} e^{-10^{0.4(M^*-M)}}
\end{align}
```

### 3.2 Numérotation

- Toutes les équations référencées doivent être numérotées
- Utiliser `\nonumber` pour les lignes intermédiaires
- Référencer avec `Eq.~\eqref{eq:schechter}` ou `Equation~(\ref{eq:schechter})`

---

## 4. Tableaux

### 4.1 Format standard avec booktabs

```latex
\usepackage{booktabs}

\begin{table}[h]
\centering
\caption{Titre descriptif du tableau}
\label{tab:example}
\begin{tabular}{lcc}
\toprule
Colonne 1 & Colonne 2 & Colonne 3 \\
\midrule
Données & $1.23 \pm 0.05$ & Unité \\
Données & $4.56 \pm 0.10$ & Unité \\
\midrule
\textbf{Total} & \textbf{5.79} & \\
\bottomrule
\end{tabular}
\tablefoot{Notes de bas de tableau si nécessaire.}
\end{table}
```

### 4.2 Règles

- **Jamais** de lignes verticales (`|`)
- Utiliser `\toprule`, `\midrule`, `\bottomrule` uniquement
- Caption AU-DESSUS du tableau
- Incertitudes avec `$\pm$` ou asymétriques `$^{+0.1}_{-0.2}$`

---

## 5. Figures

### 5.1 Format et résolution

| Type | Format | Résolution |
|------|--------|------------|
| Graphiques vectoriels | PDF | N/A (vectoriel) |
| Images bitmap | PNG/TIFF | 300 dpi minimum |
| Photographies | JPEG | 300 dpi |

### 5.2 Structure

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\columnwidth]{figures/fig1.pdf}
\caption{Description complète de la figure. Les axes doivent être
clairement étiquetés. Source des données si applicable.}
\label{fig:example}
\end{figure}
```

### 5.3 Règles

- Caption EN-DESSOUS de la figure
- Légende lisible (font size >= 8pt)
- Couleurs accessibles (éviter rouge-vert seul)
- Référencer toutes les figures dans le texte

---

## 6. Sections obligatoires

### 6.1 Abstract

- 150-300 mots
- Structure : Contexte → Méthode → Résultats → Conclusion
- Pas de citations ni d'acronymes non définis
- Chiffres clés avec incertitudes

### 6.2 Keywords

```latex
\textbf{Keywords:} cosmology -- galaxies: high-redshift --
methods: statistical -- surveys: JWST
```

Utiliser le vocabulaire contrôlé du journal cible (ex: A&A keywords).

### 6.3 Acknowledgments

Structure recommandée :
```latex
\section*{Acknowledgments}

% 1. Personnes (mentors, collaborateurs)
We thank [Name] for valuable discussions...

% 2. Données et télescopes
This research is based on observations made with [telescope]...
Data obtained from [archive]...

% 3. Logiciels
This work made use of Astropy \citep{astropy2022}, NumPy...

% 4. Financements
This work was supported by [grant number]...

% 5. Facilities & Software (format AAS)
\textbf{Facilities:} JWST (NIRCam, NIRSpec), HST (ACS).
\textbf{Software:} Astropy, NumPy, SciPy, Matplotlib, emcee.
```

### 6.4 Data Availability Statement

**Obligatoire** pour la plupart des journaux depuis 2020.

```latex
\section*{Data Availability}

% Option 1 : Données publiques
The data underlying this article are available in [Repository Name],
at \url{https://doi.org/10.xxxx/xxxxx}.

% Option 2 : Sur demande
The data underlying this article will be shared on reasonable
request to the corresponding author.

% Option 3 : Mixte
Observational data are available from [Archive]. Derived data and
analysis code are available at \url{https://github.com/...}.
```

---

## 7. Template LaTeX

### 7.1 Préambule standard JANUS

```latex
\documentclass[twocolumn,10pt]{article}

% Encodage
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}

% Mathématiques
\usepackage{amsmath,amssymb}

% Tableaux et figures
\usepackage{graphicx}
\usepackage{booktabs}

% Hyperliens
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}

% Bibliographie
\usepackage{natbib}

% Mise en page
\usepackage{geometry}
\geometry{margin=2cm}

% Commandes personnalisées
\newcommand{\LCDM}{$\Lambda$CDM}
\newcommand{\Msun}{M$_{\odot}$}
\newcommand{\kms}{km\,s$^{-1}$}
```

### 7.2 Structure du document

```latex
\begin{document}

\title{Titre}
\author{Auteur}
\date{Mois Année (vX.X)}

\maketitle

\begin{abstract}
...
\end{abstract}

\textbf{Keywords:} ...

\section{Introduction}
...

\section*{Acknowledgments}
...

\section*{Data Availability}
...

\begin{thebibliography}{99}
% Références en ordre ALPHABÉTIQUE
\bibitem[Author(Year)]{key} ...
\end{thebibliography}

\end{document}
```

---

## 8. Checklist avant soumission

### 8.1 Contenu

- [ ] Abstract complet (contexte, méthode, résultats, conclusion)
- [ ] Toutes les figures/tableaux référencés dans le texte
- [ ] Toutes les équations numérotées si référencées
- [ ] Incertitudes sur tous les résultats quantitatifs
- [ ] Comparaison avec travaux antérieurs

### 8.2 Références

- [ ] Tri alphabétique par premier auteur
- [ ] Format cohérent (journal abrégé, volume en gras)
- [ ] Toutes les citations dans le texte présentes dans la bibliographie
- [ ] Pas de références orphelines (non citées)
- [ ] DOI ou arXiv ID pour chaque référence récente

### 8.3 Formatage

- [ ] Pas d'overfull/underfull hbox significatifs
- [ ] Figures en haute résolution (300 dpi minimum)
- [ ] Tableaux sans lignes verticales
- [ ] Compilation LaTeX sans erreurs

### 8.4 Sections obligatoires

- [ ] Acknowledgments (personnes, données, logiciels, financement)
- [ ] Data Availability Statement
- [ ] Conflicts of Interest declaration
- [ ] Author contributions (si multi-auteurs)

### 8.5 Soumission

- [ ] Vérifier les guidelines du journal cible
- [ ] Lettre de couverture (cover letter)
- [ ] Suggestions de reviewers (si demandé)
- [ ] Fichiers source (.tex) + figures séparées

---

## Ressources

- **A&A Author Guide** : https://www.aanda.org/for-authors
- **ApJ/AAS Style Guide** : https://journals.aas.org/authors/
- **MNRAS Instructions** : https://academic.oup.com/mnras/pages/General_Instructions
- **arXiv Submission** : https://arxiv.org/help/submit
- **ADS Abstract Service** : https://ui.adsabs.harvard.edu/

---

*Document maintenu par le projet JANUS. Dernière mise à jour : Janvier 2026.*
