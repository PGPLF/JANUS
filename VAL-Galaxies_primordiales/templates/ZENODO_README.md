# COSMOS2025_JANUS Dataset

**DOI**: [10.5281/zenodo.XXXXXXX] (à mettre à jour après publication)

## Description

Complete dataset for the JANUS bimetric cosmology validation project using COSMOS-Web DR1 (Data Release 1) primordial galaxies observations from JWST.

**Project**: VAL-Galaxies_primordiales
**Model**: JANUS Bimetric Cosmology
**Comparison**: ΛCDM Standard Model
**Date**: January 2026

### Contents

This dataset includes:

1. **COSMOS-Web DR1 Complete Catalog** (~784,000 galaxies)
   - JWST NIRCam + HST + ground-based photometry
   - LePhare photometric redshifts and stellar masses
   - CIGALE SED fitting (masses, SFR, attenuation)
   - Morphological parameters
   - Spectroscopic redshifts (when available)

2. **Detection Images and Segmentation Maps** (20 tiles)
   - JWST NIRCam detection images (0.03"/pixel)
   - Source segmentation maps

3. **SED Fitting Products**
   - LePhare: redshift probability distributions (PDFz) + best-fit SEDs
   - CIGALE: best-fit SEDs for all sources

4. **JANUS Specific Analyses**
   - MCMC chains (JANUS vs ΛCDM comparison)
   - High-z galaxy selections (z > 8)
   - "Impossible galaxies" sample
   - Bootstrap analysis results
   - Comparative statistics

5. **Reproduction Scripts**
   - Complete Python pipeline
   - Environment configuration
   - Documentation

## COSMOS-Web DR1 Source

**Original Data**: Institut d'Astrophysique de Paris (IAP)
**URL**: https://cosmos2025.iap.fr/
**Paper**: Shuntov, M., Akins, H. B., Paquereau, L., Casey, C. M., Ilbert, O., et al. (2025). "COSMOS2025: The COSMOS-Web galaxy catalog of photometry, morphology, and physical parameters from JWST, HST and ground-based imaging", ApJ (submitted).

## JANUS Model References

**JANUS Cosmology**:
- Petit, J.-P., d'Agostini, G. (2014). "Cosmological bimetric model with interacting positive and negative masses and two different speeds of light", Astrophysics and Space Science, 354, 611-615.
- Petit, J.-P., d'Agostini, G. (2015). "Negative mass hypothesis and the nature of dark energy and dark matter", Astrophysics and Space Science, 357, 67.

## Data Structure

See individual `README.md` files in each subdirectory for detailed descriptions:
- `00_catalog/catalog_README.md` - Column descriptions
- `05_janus_analysis/chains_README.md` - MCMC methodology
- `05_janus_analysis/jwst_highz_selection/selection_criteria.md` - High-z selection

## Archive Contents

This dataset is divided into 6 archives due to Zenodo's 50 GB file limit:

1. **COSMOS2025_catalog_segmaps.zip** (~8 GB)
   - Complete master catalog (784k sources, 6 HDU extensions)
   - Separate extension files
   - Segmentation maps (20 tiles)
   - README, CITATION, LICENSE

2. **detection_part1.tar.gz** (~18 GB)
   - Detection images tiles 1-10

3. **detection_part2.tar.gz** (~18 GB)
   - Detection images tiles 11-20

4. **COSMOS2025_lephare.tar.gz** (~30-40 GB)
   - LePhare PDFz (redshift probability distributions)
   - LePhare best-fit SEDs (784k sources)

5. **cigale_seds_v2.0.tar.gz** (~30-40 GB)
   - CIGALE best-fit SEDs (784k sources)

6. **COSMOS2025_JANUS_analysis.tar.gz** (variable)
   - JANUS MCMC chains (JANUS vs ΛCDM)
   - High-z selections (z > 8)
   - Comparative statistics
   - Reproduction scripts

## Usage

### Requirements

```bash
# Python 3.10+
pip install -r scripts/requirements.txt

# Or conda
conda env create -f scripts/environment.yml
```

### Quick Start

```python
from astropy.io import fits
import h5py

# Load catalog
hdul = fits.open('00_catalog/COSMOS-Web_master_v2.0.fits')
lephare = hdul['LEPHARE'].data  # Photo-z
cigale = hdul['CIGALE'].data    # SED fitting

# Load MCMC chains
with h5py.File('05_janus_analysis/mcmc_chains/JANUS_bimetric.h5', 'r') as f:
    chains = f['mcmc/chain'][:]
    lnprob = f['mcmc/lnprobability'][:]
```

See `scripts/reproduction_pipeline.py` for complete analysis workflow.

## Citation

If you use this dataset in your research, please cite:

### COSMOS-Web DR1 Catalog
```bibtex
@article{Shuntov2025,
  author = {Shuntov, M. and Akins, H. B. and Paquereau, L. and Casey, C. M. and Ilbert, O. and others},
  title = {COSMOS2025: The COSMOS-Web galaxy catalog of photometry, morphology, and physical parameters from JWST, HST and ground-based imaging},
  journal = {ApJ},
  year = {2025},
  note = {submitted},
  url = {https://cosmos2025.iap.fr/}
}
```

### This Dataset
```bibtex
@dataset{COSMOS2025_JANUS,
  author = {[Your Name/Team]},
  title = {COSMOS2025_JANUS: Complete dataset for JANUS bimetric cosmology validation},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

### JANUS Model
```bibtex
@article{Petit2014,
  author = {Petit, J.-P. and d'Agostini, G.},
  title = {Cosmological bimetric model with interacting positive and negative masses and two different speeds of light},
  journal = {Astrophysics and Space Science},
  volume = {354},
  pages = {611--615},
  year = {2014},
  doi = {10.1007/s10509-014-2106-5}
}
```

## License

**COSMOS-Web DR1 Data**: Please refer to original COSMOS2025 data policy at https://cosmos2025.iap.fr/

**JANUS Analysis Scripts and Results**: CC-BY-4.0

You are free to:
- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

## Contact

**Project**: VAL-Galaxies_primordiales
**Repository**: https://github.com/PGPLF/JANUS
**Issues**: https://github.com/PGPLF/JANUS/issues

## Version History

- **v1.0** (2026-01-XX): Initial release
  - Complete COSMOS-Web DR1 catalog
  - JANUS vs ΛCDM MCMC analysis
  - High-z galaxy selections

## Acknowledgments

This work uses data from the COSMOS-Web JWST program (PI: Casey, PID: 1727) and the COSMOS survey. We thank the IAP COSMOS team for making the DR1 catalog publicly available.

---

**Last updated**: 2026-01-06
**Status**: Version 1.0 - Initial Release
