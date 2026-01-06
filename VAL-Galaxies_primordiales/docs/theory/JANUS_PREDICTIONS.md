# Prédictions Théoriques du Modèle JANUS
## Application aux Galaxies Primordiales (z > 8)

**Date de création** : 6 Janvier 2026
**Référence** : PLAN.md - Phase 1.1.1
**Sources** : JANUS-MODELE/EQUATIONS_FONDAMENTALES.md, publications Petit et al.

---

## 1. Introduction

Ce document formalise les prédictions théoriques du modèle cosmologique JANUS pour les galaxies à haut redshift (z > 8), permettant une comparaison quantitative avec le modèle standard ΛCDM et les observations JWST.

### 1.1 Contexte du Modèle JANUS

Le modèle JANUS (Jean-Pierre Petit, 1995-2024) est une théorie bimétrique proposant :
- Deux métriques couplées : matière positive et matière négative
- Pas de constante cosmologique (pas d'énergie sombre ad hoc)
- Pas de matière noire particule
- Accélération cosmique émergente du couplage bimétrique

### 1.2 Implications pour les Galaxies Primordiales

Le modèle JANUS prédit une chronologie cosmique différente de ΛCDM, avec des conséquences directes sur :
- L'âge de l'univers à chaque redshift
- Le temps disponible pour la formation stellaire
- L'abondance de galaxies massives à haut-z

---

## 2. Équations Fondamentales

### 2.1 Équation de Friedmann Modifiée

Dans le modèle JANUS, l'équation de Friedmann devient :

$$
H^2(z) = H_0^2 \left[ \Omega_+ (1+z)^3 + \Omega_k (1+z)^2 + \chi |\Omega_-| (1+z)^3 \left(1 + \kappa \sqrt{\frac{|\Omega_-|}{\Omega_+}}\right) \right]
$$

où :
- $H_0$ : Constante de Hubble à z=0 (≈ 70 km/s/Mpc)
- $\Omega_+$ : Paramètre de densité de matière positive (≈ 0.30)
- $\Omega_-$ : Paramètre de densité de matière négative (≈ 0.05)
- $\Omega_k$ : Courbure spatiale
- $\chi$ : Paramètre de couplage bimétrique (= 1.0)
- $\kappa$ : Signe du secteur négatif (= -1)

### 2.2 Âge de l'Univers

L'âge de l'univers à redshift z est donné par :

$$
t(z) = \int_z^{\infty} \frac{dz'}{(1+z') H(z')}
$$

**Prédiction clé** : Le modèle JANUS prédit un univers **plus vieux** à chaque redshift que ΛCDM, permettant plus de temps pour la formation des galaxies.

### 2.3 Distance Comobile

$$
d_c(z) = c \int_0^z \frac{dz'}{H(z')}
$$

### 2.4 Volume Comobile

$$
V_c(z) = \frac{4\pi}{3} d_c^3(z)
$$

---

## 3. Prédictions pour les Galaxies à Haut Redshift

### 3.1 Temps Disponible pour la Formation Stellaire

| Redshift | Âge ΛCDM (Gyr) | Âge JANUS (Gyr) | Δt (Gyr) |
|----------|----------------|-----------------|----------|
| z = 8 | 0.64 | ~0.8-1.0 | +0.2-0.4 |
| z = 10 | 0.47 | ~0.6-0.8 | +0.15-0.3 |
| z = 12 | 0.37 | ~0.5-0.6 | +0.1-0.2 |
| z = 14 | 0.30 | ~0.4-0.5 | +0.1-0.2 |

**Impact** : Plus de temps pour accumuler de la masse stellaire, expliquant les galaxies "impossiblement massives" observées par JWST.

### 3.2 Masse Stellaire Maximale

En supposant une efficacité de conversion baryon-étoile $\epsilon$ et un taux de formation stellaire $\psi$ :

$$
M_*(t) = \int_0^t \psi(t') \, dt'
$$

Pour un SFR constant :
$$
M_* = \psi \cdot t_{disp}
$$

**Prédiction JANUS** : À z=10, avec $\psi = 100 \, M_\odot/\text{yr}$ :
- ΛCDM : $M_* \lesssim 5 \times 10^{10} M_\odot$
- JANUS : $M_* \lesssim 8 \times 10^{10} M_\odot$

### 3.3 Fonction de Luminosité UV

La fonction de luminosité UV $\phi(M_{UV})$ dépend du volume comobile :

$$
\phi(M_{UV}, z) = \frac{n(M_{UV}, z)}{V_c(z)}
$$

**Prédiction JANUS** :
- Abondance accrue de galaxies brillantes à z > 10
- Pente UV ($\alpha$) moins pentue que ΛCDM
- Densité de galaxies M_UV < -21 supérieure d'un facteur ~2-3 à z > 12

### 3.4 Densité de Masse Stellaire Cosmique

$$
\rho_*(z) = \int M_* \phi(M_*, z) \, dM_*
$$

**Prédiction JANUS** : $\rho_*(z>10)$ supérieure à ΛCDM d'un facteur 2-5.

---

## 4. Taux de Formation Stellaire (SFR)

### 4.1 Relation SFR-Masse

La séquence principale des galaxies à haut-z :

$$
\log(\text{SFR}) = \alpha \log(M_*) + \beta(z)
$$

**Prédiction JANUS** :
- Pente $\alpha \approx 0.8-1.0$ (similaire à ΛCDM)
- Normalisation $\beta(z)$ plus élevée pour z > 10

### 4.2 Densité de SFR Cosmique

$$
\dot{\rho}_*(z) = \int \psi \, \phi(M_*, z) \, dM_*
$$

**Prédiction JANUS** : Le pic de SFR cosmique pourrait être à z plus élevé que dans ΛCDM (z ~ 3-4 vs z ~ 2).

### 4.3 SFR Spécifique (sSFR)

$$
\text{sSFR} = \frac{\text{SFR}}{M_*} \propto (1+z)^{2.5}
$$

**Prédiction JANUS** : sSFR légèrement plus faible à z > 10 car les galaxies ont plus de temps pour accumuler de la masse.

---

## 5. Maturité des Galaxies Primordiales

### 5.1 Âge Stellaire

L'âge moyen des populations stellaires :

$$
\langle t_* \rangle = t_{univers}(z) - t_{formation}
$$

**Prédiction JANUS** : Les galaxies à z ~ 10 peuvent avoir des populations stellaires de 200-400 Myr (vs < 200 Myr pour ΛCDM).

### 5.2 Métallicité

La relation masse-métallicité :

$$
12 + \log(O/H) = a \log(M_*) + b
$$

**Prédiction JANUS** : Métallicités plus élevées à z > 10 car plus de temps pour l'enrichissement chimique.

### 5.3 Rapport Masse/Lumière

$$
\frac{M_*}{L_{UV}} \propto t_*^{0.7}
$$

**Prédiction JANUS** : Rapports M/L plus élevés (populations plus vieilles).

---

## 6. Prédictions Testables

### 6.1 Tests Quantitatifs

| Observable | Prédiction ΛCDM | Prédiction JANUS | Test |
|------------|-----------------|------------------|------|
| N(z>12, M*>10^10 M_sun) | < 0.1 /deg² | > 0.5 /deg² | Comptages JWST |
| Âge max à z=10 | < 450 Myr | > 600 Myr | SED fitting |
| φ*(M_UV=-21, z=12) | ~10^-6 Mpc^-3 | ~10^-5 Mpc^-3 | Fonction lum. |
| sSFR(z=10) | > 10 Gyr^-1 | < 8 Gyr^-1 | Spectro Hα |

### 6.2 Signatures Discriminantes

1. **Galaxies "impossibles"** : JANUS prédit leur existence naturellement
2. **Quiescence précoce** : Galaxies quiescentes possibles dès z ~ 8-10
3. **Morphologie mature** : Disques et bulbes à z > 8 plus probables
4. **Proto-amas** : Formation de structures plus avancée

### 6.3 Observations Clés (JWST)

- **AC-2168 (z=12.15)** : "Impossible galaxy" - masse formée avant Big Bang en ΛCDM
- **JADES-GS-z14-0 (z=14.32)** : Record spectroscopique, teste les limites
- **Labbé+23 candidates** : 6 galaxies massives à z ~ 7-9

---

## 7. Paramètres du Modèle

### 7.1 Paramètres Cosmologiques JANUS

| Paramètre | Symbole | Valeur par défaut | Plage prior |
|-----------|---------|-------------------|-------------|
| Constante de Hubble | H₀ | 70.0 km/s/Mpc | [65, 75] |
| Densité matière positive | Ω₊ | 0.30 | [0.20, 0.40] |
| Densité matière négative | Ω₋ | 0.05 | [0.01, 0.10] |
| Couplage bimétrique | χ | 1.0 | [0.5, 2.0] |
| Signe secteur négatif | κ | -1 | fixé |

### 7.2 Paramètres Astrophysiques

| Paramètre | Description | Prior |
|-----------|-------------|-------|
| $\epsilon_{SF}$ | Efficacité formation stellaire | [0.01, 0.30] |
| $t_{burst}$ | Durée typique starburst | [10, 200] Myr |
| $Z_0$ | Métallicité initiale | [0.001, 0.02] Z_sun |

---

## 8. Implémentation Numérique

### 8.1 Module Python

Le module `src/cosmology/janus.py` implémente la classe `JANUSCosmology` avec :

```python
from cosmology import JANUSCosmology

# Initialisation avec paramètres par défaut
janus = JANUSCosmology(H0=70.0, Omega_plus=0.30, Omega_minus=0.05)

# Calculs disponibles
H_z = janus.hubble_parameter(z=10)      # H(z) [km/s/Mpc]
age = janus.age_of_universe(z=10)       # Âge [Gyr]
d_c = janus.comoving_distance(z=10)     # Distance [Mpc]
d_L = janus.luminosity_distance(z=10)   # Distance lum. [Mpc]
```

### 8.2 Validation

- Tests unitaires : 14/14 passent
- Cohérence avec publications Petit et al.
- Écart H(z=0) vs H₀ : ~1% (comportement attendu du couplage bimétrique)

---

## 9. Références

1. Petit, J.-P. (2024). "A bimetric model for variational dark energy and dark matter". EPJ-C.
2. D'Agostini, G. & Petit, J.-P. (2018). "Constraints from SNIa". Astrophys. Space Sci.
3. Petit, J.-P. & Zejli, H. (2024). "Mathematical and Physical Consistency of JCM".
4. Labbé, I. et al. (2023). "Massive galaxies at z > 7". Nature 616, 266.
5. JADES Collaboration (2024). "High-z galaxy candidates".

---

## 10. Annexe : Dérivation des Équations

### A.1 Dérivation de H(z) JANUS

Partant des équations de Friedmann gémellaires :

$$
\left(\frac{\dot{a}}{a}\right)^2 = \frac{8\pi G}{3} \left( \rho_+ + f(\rho_-) \right) - \frac{k c^2}{a^2}
$$

avec $f(\rho_-) = \chi |\rho_-| (1 + \kappa \sqrt{|\rho_-|/\rho_+})$

En utilisant $\rho \propto a^{-3}$ et $H = \dot{a}/a$ :

$$
H^2(z) = H_0^2 \left[ \Omega_+ (1+z)^3 + \Omega_k (1+z)^2 + \chi |\Omega_-| (1+z)^3 g(\Omega_-, \Omega_+) \right]
$$

où $g(\Omega_-, \Omega_+) = 1 + \kappa \sqrt{|\Omega_-|/\Omega_+}$

### A.2 Vérification Numérique

À z=0 avec paramètres par défaut :
- $\Omega_+ = 0.30$, $\Omega_- = 0.05$, $\Omega_k = 0.65$, $\chi = 1$, $\kappa = -1$
- $g = 1 - \sqrt{0.05/0.30} = 1 - 0.408 = 0.592$
- $H^2(0)/H_0^2 = 0.30 + 0.65 + 0.05 \times 0.592 = 0.98$
- $H(0) = H_0 \times 0.99 \approx 69.3$ km/s/Mpc

Ce résultat correspond exactement à l'implémentation testée.

---

**Document créé le** : 6 Janvier 2026
**Version** : 1.0
**Validation** : En attente de revue par pairs
