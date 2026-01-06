# Instructions JANUS

**Dernière mise à jour** : 6 Janvier 2026

Ce dossier contient les instructions pour le projet JANUS.

---

## Liste des Instructions

| Fichier | Description | Dernière MAJ |
|---------|-------------|--------------|
| **INS-Infrastructure.md** | Configuration machines, packages Python, requirements | 2026-01-05 |
| **INS-Statistiques.md** | Calculs MCMC intensifs, checkpoints, optimisations | 2026-01-05 |
| **INS-CLAUDE.md** | Bonnes pratiques assistant IA, accélération traitements | 2026-01-05 |
| **INS-PDF_COMPILATION.md** | Compilation PDF avec LaTeX et Jupyter | 2026-01-05 |
| **INS-FONTS_EQUATIONS.md** | Polices et affichage des équations | 2026-01-05 |

---

## Sous-Projets

| Projet | Description | Status |
|--------|-------------|--------|
| **JANUS-S** | Supernovae Ia (Pantheon+, DES-SN5YR) - Contraintes JANUS vs ΛCDM | V2 Complete |
| **JANUS-Z** | Galaxies primordiales JWST (CEERS, JADES, UNCOVER) | En cours |

---

## Convention de Nommage

- Préfixe `INS-` pour tous les fichiers d'instructions
- Format : `INS-{Domaine}.md`

---

## Résumé par Domaine

### Infrastructure (INS-Infrastructure.md)
- Configuration matérielle des machines
- Packages Python et versions minimales
- État d'installation par machine
- Historique des modifications avec réversibilité

### Statistiques (INS-Statistiques.md)
- Contraintes calculs longs (mémoire, interruptions)
- Système de checkpoints (emcee, dynesty)
- Optimisations Apple Silicon M4
- Reprise de calculs interrompus

### Assistant IA (INS-CLAUDE.md)
- Stratégies d'accélération (background, parallèle)
- Workflow recommandé pour MCMC
- Script `run_mcmc_optimized.py`
- Commandes utiles et monitoring

### Compilation (INS-PDF_COMPILATION.md)
- Export PDF depuis Jupyter
- Configuration LaTeX
- Résolution problèmes courants

### Équations (INS-FONTS_EQUATIONS.md)
- Polices mathématiques
- Rendu LaTeX dans notebooks
- Symboles cosmologiques

---

## Mise à Jour

Lors de la modification d'une INS :
1. Mettre à jour l'horodatage dans l'INS
2. Ajouter une entrée dans l'historique de l'INS
3. Mettre à jour ce README (tableau "Liste des Instructions")
