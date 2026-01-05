# Équations Fondamentales du Modèle Cosmologique JANUS

## Introduction

Le modèle cosmologique JANUS est une théorie bimétrique développée par Jean-Pierre Petit, basée sur l'idée originale d'Andrei Sakharov d'un "univers jumeau". Ce modèle propose l'existence de deux métriques couplées, l'une décrivant la matière à masse positive, l'autre la matière à masse négative.

Ce document compile les équations fondamentales du modèle JANUS, extraites des publications scientifiques du projet.

---

## 1. Équations de Champ Bimetriques

### 1.1 Équations d'Einstein Gémellaires

Le modèle JANUS repose sur deux métriques couplées :

- **Métrique de l'espace positif** : $g_{\mu\nu}$ → matière à masse positive
- **Métrique de l'espace négatif** : $h_{\mu\nu}$ (également notée $\bar{g}_{\mu\nu}$) → matière à masse négative

#### 1.1.1 Équation pour la métrique positive

$$
R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = \chi \left( T_{\mu\nu} + \sqrt{\frac{|\bar{g}|}{|g|}} T'_{\mu\nu} \right)
$$

où :
- $R_{\mu\nu}$ : tenseur de Ricci
- $R$ : courbure scalaire
- $T_{\mu\nu}$ : tenseur énergie-impulsion de la matière positive
- $T'_{\mu\nu}$ : terme d'interaction avec l'univers négatif
- $\chi$ : constante de couplage ($\chi = 8\pi G/c^4$)

#### 1.1.2 Équation pour la métrique négative

$$
\bar{R}_{\mu\nu} - \frac{1}{2} \bar{g}_{\mu\nu} \bar{R} = \kappa \chi \left( \bar{T}_{\mu\nu} + \sqrt{\frac{|g|}{|\bar{g}|}} \bar{T}'_{\mu\nu} \right)
$$

où :
- $\kappa = -1$ : paramètre assurant une attraction mutuelle entre masses négatives
- $\bar{R}_{\mu\nu}$, $\bar{R}$ : tenseur de Ricci et courbure scalaire dans l'espace négatif
- $\bar{T}_{\mu\nu}$ : tenseur énergie-impulsion de la matière négative

### 1.2 Contraintes de Couplage

Les tenseurs d'interaction doivent satisfaire :

$$
\nabla^\mu T'_{\mu\nu} = 0
$$

$$
\nabla^\mu \bar{T}'_{\mu\nu} = 0
$$

ce qui assure la conservation de l'énergie-impulsion dans chaque secteur.

---

## 2. Métrique de Schwarzschild Gémellaire

### 2.1 Métrique de Schwarzschild Positive

Pour un objet de masse positive $m$ :

$$
ds^2 = -\left(1 - \frac{2r_s}{r}\right) c^2 dt^2 + \left(1 - \frac{2r_s}{r}\right)^{-1} dr^2 + r^2 d\Omega^2
$$

où $r_s = 2Gm/c^2$ est le rayon de Schwarzschild.

### 2.2 Métrique de Schwarzschild Négative

Pour un objet de masse négative $-m$ :

$$
d\bar{s}^2 = -\left(1 + \frac{2r_s}{r}\right) c^2 dt^2 + \left(1 + \frac{2r_s}{r}\right)^{-1} dr^2 + r^2 d\Omega^2
$$

**Caractéristique clé :** Le signe change devant $2r_s/r$, éliminant la singularité de Schwarzschild. Les masses négatives n'ont pas d'horizon des événements.

---

## 3. Équations Cosmologiques

### 3.1 Métriques de Friedmann-Lemaître-Robertson-Walker (FLRW)

Le modèle JANUS utilise deux métriques FLRW couplées :

**Métrique positive :**
$$
ds^2 = -c^2 dt^2 + a^2(t) \left[ \frac{dr^2}{1-kr^2} + r^2(d\theta^2 + \sin^2\theta d\phi^2) \right]
$$

**Métrique négative :**
$$
d\bar{s}^2 = -\bar{c}^2 dt^2 + \bar{a}^2(t) \left[ \frac{dr^2}{1-\bar{k}r^2} + r^2(d\theta^2 + \sin^2\theta d\phi^2) \right]
$$

où :
- $a(t)$ et $\bar{a}(t)$ : facteurs d'échelle (expansion de l'univers)
- $k$ et $\bar{k}$ : courbures spatiales (-1, 0, ou +1)
- **Contrainte JANUS :** $k = \bar{k} = -1$ (courbure négative obligatoire)

### 3.2 Équations de Friedmann Gémellaires

Les équations d'Einstein appliquées à un univers FLRW donnent :

**Pour l'univers positif :**
$$
a^2 \frac{d^2a}{dx^2} = \frac{\chi}{2} E
$$

**Pour l'univers négatif :**
$$
\bar{a}^2 \frac{d^2\bar{a}}{dx^2} = -\frac{\chi}{2} E
$$

où $E$ est l'énergie totale du système couplé : 

$$
E = \rho c^2 a^3 + \bar{\rho} \bar{c}^2 \bar{a}^3
$$

**Point clé :** Si $E < 0$ (matière négative dominante), l'accélération cosmique émerge **sans constante cosmologique** (sans énergie sombre).

### 3.3 Paramètre de Hubble

$$
H(t) = \frac{\dot{a}}{a}
$$

$$
\bar{H}(t) = \frac{\dot{\bar{a}}}{\bar{a}}
$$

### 3.4 Paramètres de Densité

$$
\Omega(t) = \frac{\rho}{\rho_{crit}}
$$

$$
\bar{\Omega}(t) = \frac{\bar{\rho}}{\rho_{crit}}
$$

où $\rho_{crit} = \frac{3H^2}{8\pi G}$.

---

## 4. Équations pour les Observations

### 4.1 Supernovæ de Type Ia (SNIa)

#### 4.1.1 Module de Distance

Le module de distance apparent :

$$
\mu = 5 \log_{10}(d_L) + 25
$$

où $d_L$ est la distance lumineuse en Megaparsecs (Mpc).

#### 4.1.2 Distance Lumineuse

$$
d_L(z) = (1+z) \int_0^z \frac{c \, dz'}{H(z')}
$$

Le modèle JANUS calcule $d_L$ numériquement à partir des équations de champ couplées.

### 4.2 Oscillations Acoustiques Baryoniques (BAO)

La distance acoustique aux drag epoch et oscillations :

$$
r_s = \int_0^{z_{drag}} \frac{c_s}{H(z')} dz'
$$

### 4.3 Fond Diffus Cosmologique (CMB)

#### 4.3.1 Redshift du Découplage

$$
z_{dec} = \frac{T_{cmb}}{T_{0}} - 1
$$

où $T_{cmb}$ est la température du CMB aujourd'hui (~2.725 K).

#### 4.3.2 Spectre de Puissance

Le modèle JANUS prédit un spectre de puissance du CMB différent des modèles ΛCDM.

### 4.4 Lentilles Gravitationnelles

La métrique de Schwarzschild négative prédit des motifs de déviation légèrement différents de la déflexion classique :

$$
\alpha = \frac{4GM}{c^2} \frac{D_{ls}D_s}{D_l}
$$

Prédiction spécifique au modèle JANUS : **motifs en anneau** pour les objets derrière les grands vides cosmiques (voids).

### 4.5 Courbes de Rotation des Galaxies

$$
v(r) = \sqrt{\frac{GM(r)}{r}}
$$

Le modèle JANUS explique les courbes plates sans matière noire, par l'interaction avec la matière à masse négative.

---

## 5. Récapitulatif des Équations Clés

| Domaine | Équation Clé | Apport du Modèle JANUS |
|---------|-------------|------------------------|
| Bimétrie | $R_{\mu\nu} - \frac{1}{2} g_{\mu\nu} R = \chi [T_{\mu\nu} + \sqrt{\|\bar{g}\|/\|g\|} T'_{\mu\nu}]$ | Couplage de deux métriques Lorentziennes |
| Schwarzschild | $ds^2 = -(1 \pm \frac{2r_s}{r}) c^2 dt^2 \dots$ | Signe + ou - selon la masse, élimine l'horizon événementiel |
| Friedmann | $a^2 d^2a/dx^2 = \chi/2 \cdot E$ | Accélération en $E < 0$ |
| Luminosité SNIa | $d_L(z) = (1+z) \int_0^z cdz/H(z')$ | Calcul basé des équations différentielles couplées |
| Lentilles | $\alpha \sim M/D$ | Motifs "en anneau" pour vides cosmiques |

---

## 6. Références Bibliographiques

1. Petit, J.-P. (2024). "A bimetric model for variational dark energy and dark matter based on the Janus cosmological model". European Physical Journal C.
2. D'Agostini, G. & Petit, J.-P. (2018). "Constraints from recent observations of supernovae type Ia". Astrophysics and Space Science.
3. Petit, J.-P. (2021). "The Schwarzschild-Scheen ergosphere in Janus cosmology".
4. Petit, J.-P. (2014). "Negative mass hypothesis in cosmology and the nature of dark energy".
5. Henry-Couannier, F. (2005). "Dark gravity and bimetric theory".
6. Sakharov, A.D. (1967). "Violation of CP-invariance, C asymmetry, and baryon asymmetry of the Universe". Pisma Zh. Eksp. Teor. Fiz.
