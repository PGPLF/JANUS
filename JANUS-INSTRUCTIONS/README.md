# Instructions JANUS

**Dernière mise à jour** : 6 Janvier 2026

Ce dossier contient les instructions pour le projet JANUS.

---

## Liste des Instructions

| Fichier | Description | Dernière MAJ |
|---------|-------------|--------------|
| **INS-Infrastructure.md** | Configuration machines, packages Python, requirements | 2026-01-06 |
| **INS-Statistiques.md** | Calculs MCMC intensifs, checkpoints, optimisations | 2026-01-05 |
| **INS-CLAUDE.md** | Bonnes pratiques assistant IA, accélération traitements | 2026-01-05 |
| **INS-PDF_COMPILATION.md** | Compilation PDF avec LaTeX et Jupyter | 2026-01-05 |
| **INS-FONTS_EQUATIONS.md** | Polices et affichage des équations | 2026-01-05 |
| **INS-COSMOS2025.md** | Catalogue COSMOS-Web DR1 (~784k galaxies), extraction z>8 | 2026-01-06 |
| **INS-COSMOS2025_HEBERGEMENT.md** | Plan hébergement complet COSMOS2025 + Zenodo (7 phases) | 2026-01-06 |
| **INS-ZENODO.md** | Infrastructure professionnelle Zenodo, templates, API | 2026-01-06 |

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

### Données COSMOS2025 (INS-COSMOS2025.md)
- Catalogue COSMOS-Web DR1 (~784,000 galaxies)
- 6 extensions HDU (PHOT, LEPHARE, CIGALE, MORPH, SPEC-Z, FLAGS)
- URLs de téléchargement
- Script extraction z>8
- Utilité pour Phase 3 (statistiques haute-z)

### Hébergement COSMOS2025 (INS-COSMOS2025_HEBERGEMENT.md)
- Plan 7 phases (~7-11h total)
- Stratégie: téléchargement complet + upload Zenodo
- ~100-130 GB données complètes
- Scripts validation, extraction, upload Python
- Checklist complète 49 items
- Préparation archives < 50 GB

### Infrastructure Zenodo (INS-ZENODO.md)
- Hébergement professionnel datasets scientifiques
- DOI citable pour publications
- Structure COSMOS2025_JANUS complète
- Templates: README.md, CITATION.cff, LICENSE
- API Zenodo pour upload gros fichiers (> 10 GB)
- Métadonnées FAIR et versioning
- Workflow GitHub-Zenodo integration

---

## Mise à Jour

Lors de la modification d'une INS :
1. Mettre à jour l'horodatage dans l'INS
2. Ajouter une entrée dans l'historique de l'INS
3. Mettre à jour ce README (tableau "Liste des Instructions")
