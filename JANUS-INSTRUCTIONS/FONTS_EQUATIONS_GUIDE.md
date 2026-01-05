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
