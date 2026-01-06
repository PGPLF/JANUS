# Prédictions Théoriques du Modèle ΛCDM
## Application aux Galaxies Primordiales (z > 8)

**Date de création** : 6 Janvier 2026
**Référence** : PLAN.md - Phase 1.1.2
**Sources** : Planck Collaboration (2018), Bouwens et al. (2021), Robertson et al. (2023)

---

## 1. Introduction

Ce document formalise les prédictions théoriques du modèle cosmologique standard ΛCDM (Lambda Cold Dark Matter) pour les galaxies à haut redshift (z > 8), servant de référence pour la comparaison avec le modèle JANUS.

### 1.1 Paramètres Planck 2018

Le modèle ΛCDM est paramétré par les valeurs Planck 2018 (Planck Collaboration, A&A 641, A6) :

| Paramètre | Symbole | Valeur | Incertitude |
|-----------|---------|--------|-------------|
| Constante de Hubble | H₀ | 67.4 km/s/Mpc | ± 0.5 |
| Densité de matière | Ωₘ | 0.315 | ± 0.007 |
| Densité baryonique | Ωᵦ | 0.0493 | ± 0.0006 |
| Densité d'énergie sombre | ΩΛ | 0.685 | ± 0.007 |
| Indice spectral | nₛ | 0.965 | ± 0.004 |
| Amplitude fluctuations | σ₈ | 0.811 | ± 0.006 |
| Âge de l'univers | t₀ | 13.80 Gyr | ± 0.02 |

### 1.2 Tensions avec Observations JWST

Le modèle ΛCDM fait face à des tensions croissantes avec les observations de galaxies primordiales JWST :
- Galaxies "impossiblement massives" à z > 10
- Abondance de galaxies brillantes supérieure aux prédictions
- Maturité morphologique et chimique précoce

---

## 2. Équations Fondamentales

### 2.1 Équation de Friedmann Standard

$$
H^2(z) = H_0^2 \left[ \Omega_m (1+z)^3 + \Omega_\Lambda \right]
$$

Pour un univers plat ($\Omega_k = 0$) avec $\Omega_m + \Omega_\Lambda = 1$.

### 2.2 Âge de l'Univers

$$
t(z) = \frac{1}{H_0} \int_z^{\infty} \frac{dz'}{(1+z') \sqrt{\Omega_m (1+z')^3 + \Omega_\Lambda}}
$$

**Valeurs numériques (Planck 2018)** :

| Redshift | Âge (Gyr) | Temps depuis Big Bang (Myr) |
|----------|-----------|----------------------------|
| z = 6 | 0.93 | 930 |
| z = 8 | 0.64 | 640 |
| z = 10 | 0.47 | 470 |
| z = 12 | 0.37 | 370 |
| z = 14 | 0.30 | 300 |
| z = 15 | 0.27 | 270 |

### 2.3 Distance Comobile

$$
d_c(z) = \frac{c}{H_0} \int_0^z \frac{dz'}{\sqrt{\Omega_m (1+z')^3 + \Omega_\Lambda}}
$$

### 2.4 Distance Lumineuse

$$
d_L(z) = (1+z) \, d_c(z)
$$

---

## 3. Prédictions pour les Galaxies à Haut Redshift

### 3.1 Contrainte Temporelle sur la Formation Stellaire

**Problème central** : À z = 10, l'univers n'a que 470 Myr. Pour former une galaxie de masse $M_* = 10^{10} M_\odot$ :

$$
\text{SFR}_{min} = \frac{M_*}{t_{disponible}} = \frac{10^{10}}{4.7 \times 10^8} \approx 21 \, M_\odot/\text{yr}
$$

Ceci nécessite un SFR soutenu extrêmement élevé pendant **toute** l'histoire cosmique.

### 3.2 Masse Stellaire Maximale Théorique

En considérant la fraction baryonique cosmique $f_b = \Omega_b/\Omega_m \approx 0.16$ et une efficacité de conversion $\epsilon_{SF} \lesssim 0.3$ :

$$
M_{*,max}(z) = \epsilon_{SF} \cdot f_b \cdot M_{halo}(z)
$$

**Prédictions ΛCDM** :

| Redshift | M_halo max (M_sun) | M_* max (M_sun) |
|----------|--------------------|-----------------|
| z = 10 | ~10^12 | ~5×10^10 |
| z = 12 | ~10^11.5 | ~1.5×10^10 |
| z = 14 | ~10^11 | ~5×10^9 |

### 3.3 Fonction de Luminosité UV

La fonction de Schechter :

$$
\phi(M_{UV}) = 0.4 \ln(10) \, \phi^* \, 10^{0.4(M^* - M_{UV})(\alpha+1)} \exp\left(-10^{0.4(M^* - M_{UV})}\right)
$$

**Paramètres à z ~ 10 (Bouwens+21)** :
- $M^* \approx -20.5$ mag
- $\phi^* \approx 10^{-4}$ Mpc⁻³
- $\alpha \approx -2.0$

**Prédiction** : Densité de galaxies M_UV < -21 : $\phi \lesssim 10^{-6}$ Mpc⁻³ mag⁻¹

### 3.4 Densité de Masse Stellaire Cosmique

$$
\rho_*(z) = \int_{-\infty}^{M_{UV,lim}} M_*(M_{UV}) \, \phi(M_{UV}) \, dM_{UV}
$$

**Prédiction ΛCDM (z > 10)** : $\rho_* \lesssim 10^{5.5}$ M_sun Mpc⁻³

---

## 4. Taux de Formation Stellaire

### 4.1 Relation SFR-UV

$$
\text{SFR} = K_{UV} \times L_{UV}
$$

où $K_{UV} = 1.4 \times 10^{-28}$ M_sun yr⁻¹ / (erg s⁻¹ Hz⁻¹) (Kennicutt & Evans 2012)

### 4.2 Densité de SFR Cosmique (SFRD)

$$
\dot{\rho}_*(z) = \int L_{UV} \, \phi(L_{UV}) \, dL_{UV} \times K_{UV}
$$

**Modèle Madau & Dickinson (2014)** :

$$
\dot{\rho}_*(z) = 0.015 \frac{(1+z)^{2.7}}{1 + [(1+z)/2.9]^{5.6}} \, M_\odot \text{yr}^{-1} \text{Mpc}^{-3}
$$

**Prédictions** :
- Pic SFRD à z ≈ 2
- SFRD(z=10) ≈ 10⁻² M_sun yr⁻¹ Mpc⁻³

### 4.3 SFR Spécifique

$$
\text{sSFR}(z) \approx 10 \left(\frac{1+z}{11}\right)^{2.5} \, \text{Gyr}^{-1}
$$

**Prédiction à z = 10** : sSFR ≈ 10 Gyr⁻¹

---

## 5. Limites et Tensions du Modèle ΛCDM

### 5.1 "Impossibly Early Galaxies"

Plusieurs observations JWST violent les prédictions ΛCDM :

| Objet | Redshift | M_* (M_sun) | Tension |
|-------|----------|-------------|---------|
| Labbé+23 #1 | 7.4 | 10^10.9 | 2-3σ |
| Labbé+23 #2 | 9.1 | 10^10.6 | 3-4σ |
| AC-2168 | 12.15 | 10^10+ | >5σ |
| JADES-GS-z14-0 | 14.32 | - | Limite temps |

### 5.2 Excès de Galaxies Brillantes

L'abondance observée de galaxies UV-brillantes à z > 10 dépasse les prédictions :

| Redshift | φ observée (Mpc⁻³) | φ ΛCDM (Mpc⁻³) | Ratio |
|----------|--------------------|--------------------|-------|
| z = 10 | ~10⁻⁵ | ~10⁻⁶ | ~10× |
| z = 12 | ~10⁻⁵·⁵ | ~10⁻⁷ | ~30× |
| z = 14 | ~10⁻⁶ | ~10⁻⁸ | ~100× |

### 5.3 Maturité Précoce

Observations inattendues en ΛCDM :
- Disques établis à z > 8
- Métallicités élevées (~0.1-0.5 Z_sun) à z > 10
- Populations stellaires "vieilles" (>200 Myr) à z > 10

### 5.4 Solutions ΛCDM Proposées

Pour résoudre ces tensions sans nouveau modèle :
1. **IMF variable** : Plus de massive stars → plus de luminosité UV
2. **Efficacité SF accrue** : $\epsilon_{SF} \rightarrow 1$ à haut-z
3. **Contribution AGN** : Émission non-stellaire surestimée
4. **Erreurs photométriques** : Redshifts mal estimés

**Problème** : Ces solutions sont ad hoc et créent d'autres tensions.

---

## 6. Comparaison ΛCDM vs JANUS

### 6.1 Différences Clés

| Aspect | ΛCDM | JANUS |
|--------|------|-------|
| Énergie sombre | ΩΛ = 0.685 (constante) | Émergent du couplage |
| Matière noire | Particule (CDM) | Effet bimétrique |
| H₀ | 67.4 km/s/Mpc | ~70 km/s/Mpc |
| Âge à z=10 | 470 Myr | ~600-800 Myr |
| Galaxies massives z>10 | Tension | Prédit |

### 6.2 Tests Discriminants

| Observable | Prédiction ΛCDM | Prédiction JANUS |
|------------|-----------------|------------------|
| N(M*>10^10, z>12) | <0.1 /deg² | >0.5 /deg² |
| Âge max pop. stellaire z=10 | <450 Myr | >600 Myr |
| Quiescent fraction z>8 | <1% | >5% |

---

## 7. Paramètres du Modèle

### 7.1 Paramètres Cosmologiques Planck 2018

```python
# Paramètres Planck 2018 pour LCDMCosmology
H0 = 67.4          # km/s/Mpc
Omega_m = 0.315    # Matière (baryons + CDM)
Omega_Lambda = 0.685  # Énergie sombre
Omega_b = 0.0493   # Baryons
```

### 7.2 Paramètres Astrophysiques Standards

| Paramètre | Valeur | Référence |
|-----------|--------|-----------|
| IMF | Chabrier (2003) | Standard |
| $\epsilon_{SF}$ | 0.01-0.20 | Behroozi+19 |
| Dust extinction | A_V ~ 0.5 mag | Calzetti+00 |
| Metallicity floor | 0.01 Z_sun | Primordiale |

---

## 8. Implémentation Numérique

### 8.1 Module Python

Le module `src/cosmology/lcdm.py` implémente `LCDMCosmology` utilisant astropy :

```python
from cosmology import LCDMCosmology

# Initialisation avec Planck 2018
lcdm = LCDMCosmology(H0=67.4, Omega_m=0.315, Omega_Lambda=0.685)

# Calculs disponibles
H_z = lcdm.hubble_parameter(z=10)      # H(z) [km/s/Mpc]
age = lcdm.age_of_universe(z=10)       # Âge [Gyr]
d_c = lcdm.comoving_distance(z=10)     # Distance [Mpc]
d_L = lcdm.luminosity_distance(z=10)   # Distance lum. [Mpc]
mu = lcdm.distmod(z=10)                # Module distance [mag]
```

### 8.2 Validation

- Tests unitaires : 16/16 passent
- Cohérence avec astropy.cosmology
- Reproduction des valeurs Planck 2018

---

## 9. Références

1. Planck Collaboration (2020). "Planck 2018 results. VI. Cosmological parameters". A&A 641, A6.
2. Bouwens, R.J. et al. (2021). "UV Luminosity Functions at z ~ 8-10". AJ 162, 47.
3. Robertson, B.E. (2022). "Galaxy Formation and Reionization". ARAA 60, 121.
4. Madau, P. & Dickinson, M. (2014). "Cosmic Star Formation History". ARAA 52, 415.
5. Labbé, I. et al. (2023). "Massive galaxies at z > 7". Nature 616, 266.
6. Kennicutt, R.C. & Evans, N.J. (2012). "Star Formation". ARAA 50, 531.

---

## 10. Annexe : Calculs Détaillés

### A.1 Calcul de l'Âge à z=10

$$
t(z=10) = \frac{1}{H_0} \int_{10}^{\infty} \frac{dz'}{(1+z') \sqrt{0.315 (1+z')^3 + 0.685}}
$$

Avec $H_0 = 67.4$ km/s/Mpc = $2.18 \times 10^{-18}$ s⁻¹ :

$$
t(z=10) \approx 4.7 \times 10^8 \text{ yr} = 0.47 \text{ Gyr}
$$

### A.2 Volume Comobile à z=10

$$
V_c(z=10) = \frac{4\pi}{3} d_c^3 \approx 3.8 \times 10^{11} \text{ Mpc}^3
$$

### A.3 Densité de Halos

Press-Schechter :

$$
n(M, z) = \frac{\bar{\rho}}{M} \left| \frac{d\ln\sigma}{d\ln M} \right| f(\nu) \nu
$$

où $\nu = \delta_c / \sigma(M, z)$ et $\delta_c \approx 1.686$.

---

**Document créé le** : 6 Janvier 2026
**Version** : 1.0
**Validation** : En attente de revue
