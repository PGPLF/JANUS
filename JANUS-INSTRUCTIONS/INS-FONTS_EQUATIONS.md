# Guide des Polices et Affichage des Équations - Projet JANUS

## Problème Identifié

Les équations mathématiques s'affichent avec des caractères chinois ou incorrects dans les fichiers Markdown (.md) sur GitHub.

## Cause

Utilisation de syntaxe LaTeX brute (`\command`) dans Markdown sans délimiteurs appropriés.

## Solutions

### 1. Pour les Fichiers Markdown (.md) sur GitHub

GitHub supporte maintenant nativement les équations mathématiques via MathJax. Utiliser :

**Équations en ligne** :
```markdown
La constante de Hubble $H_0$ est mesurée en km/s/Mpc.
```

**Équations en bloc** :
```markdown
$$
E = mc^2
$$
```

**Exemple pour équations complexes** :
```markdown
$$
R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = 8\pi G T_{\mu\nu}
$$
```

### 2. Syntaxe Correcte pour JANUS

#### Métriques Bimetriques

**Version LaTeX incorrecte** (affiche caractères chinois) :
```
`R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = \chi T_{\mu\nu}`
```

**Version Markdown correcte** (affichage correct) :
```markdown
$$R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = \chi T_{\mu\nu}$$
```

### 3. Règles d'Affichage

| Contexte | Syntaxe à Utiliser | Rendu |
|----------|-------------------|-------|
| Markdown GitHub | `$equation$` ou `$$equation$$` | ✅ Correct |
| Fichier LaTeX .tex | `\begin{equation}...\end{equation}` | ✅ Correct |
| Code inline Markdown | Backticks simples | ❌ Affiche le code |
| Notebook Jupyter | `$equation$` dans cell Markdown | ✅ Correct |

### 4. Exemples Corrigés pour JANUS

#### Équations d'Einstein Gémellaires

**Équation positive** :
```markdown
$$
R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = \chi \left( T_{\mu\nu} + \sqrt{\frac{|\bar{g}|}{|g|}} T'_{\mu\nu} \right)
$$
```

**Équation négative** :
```markdown
$$
\bar{R}_{\mu\nu} - \frac{1}{2} \bar{g}_{\mu\nu} \bar{R} = \kappa \chi \left( \bar{T}_{\mu\nu} + \sqrt{\frac{|g|}{|\bar{g}|}} \bar{T}'_{\mu\nu} \right)
$$
```

où $\kappa = -1$.

#### Métrique de Schwarzschild

**Positive** :
```markdown
$$
ds^2 = -\left(1 - \frac{2r_s}{r}\right) c^2 dt^2 + \left(1 - \frac{2r_s}{r}\right)^{-1} dr^2 + r^2 d\Omega^2
$$
```

**Négative** (masse négative) :
```markdown
$$
d\bar{s}^2 = -\left(1 + \frac{2r_s}{r}\right) c^2 dt^2 + \left(1 + \frac{2r_s}{r}\right)^{-1} dr^2 + r^2 d\Omega^2
$$
```

### 5. Pour les PDF via LaTeX

Dans les fichiers .tex, utiliser la syntaxe LaTeX standard :

```latex
\begin{equation}
R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = \chi T_{\mu\nu}
\label{eq:einstein}
\end{equation}
```

### 6. Pour Jupyter Notebooks

Les cellules Markdown dans Jupyter supportent la même syntaxe que GitHub :

```markdown
La constante cosmologique $\Lambda$ peut être exprimée comme :

$$
\Lambda = \frac{3H_0^2}{c^2} \Omega_\Lambda
$$
```

### 7. Polices et Rendu

#### Sur GitHub
- Utilise MathJax automatiquement
- Pas de configuration nécessaire
- Fonctionne dans README.md et tous fichiers .md

#### En Local (VSCode, etc.)
Installer une extension Markdown avec support Math :
- **Markdown Preview Enhanced**
- **Markdown All in One**

#### Pour PDF
- LaTeX gère automatiquement les polices mathématiques
- Packages recommandés :
  ```latex
  \usepackage{amsmath,amssymb,amsfonts}
  \usepackage{mathtools}
  ```

## Vérification

Pour tester si l'affichage est correct :

1. Sur GitHub : Les équations doivent s'afficher en notation mathématique professionnelle
2. Si vous voyez des caractères chinois ou étranges : la syntaxe est incorrecte
3. Solution : Remplacer les backticks par `$...$` ou `$$...$$`

## Actions de Correction

- [ ] Corriger EQUATIONS_FONDAMENTALES.md
- [ ] Vérifier tous les fichiers .md du projet
- [ ] Tester l'affichage sur GitHub
- [ ] Mettre à jour le guide PDF_COMPILATION.md

## Références

- [GitHub Math Support](https://github.blog/2022-05-19-math-support-in-markdown/)
- [MathJax Documentation](https://docs.mathjax.org/)
- [LaTeX Math Symbols](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)


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

