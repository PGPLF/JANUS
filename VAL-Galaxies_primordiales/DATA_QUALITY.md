# Data Quality Assessment - Phase 2

**Project**: VAL-Galaxies_primordiales
**Date**: 2026-01-06
**Version**: 1.0

---

## 1. Datasets Inventory

### 1.1 Primary Datasets (Tier 1)

| Dataset | Status | Size | Location | Quality |
|---------|--------|------|----------|---------|
| JADES DR4 | ✅ Downloaded | 90 MB | `data/jwst/jades_dr4/` | A |
| COSMOS2025 | ⚠️ Manual | ~2 GB | Pending | - |
| JANUS-Z Reference | ✅ Integrated | 236 entries | `data/jwst/processed/` | A |
| JADES DR2/DR3 | ✅ Integrated | 1.4 GB | `data/jwst/raw/jades/` | A |

### 1.2 Complementary Datasets

| Dataset | Status | Size | Location | Quality |
|---------|--------|------|----------|---------|
| DJA Spectro | ✅ Documented | 8.4 GB | External | A |
| Labbé+23 | ✅ Integrated | 6 entries | `data/reference/` | A |
| Bouwens+21 UV LF | ⚠️ Manual | ~10 MB | Pending | - |

---

## 2. Quality Grades

| Grade | Definition |
|-------|------------|
| A | Verified, complete, ready for analysis |
| B | Minor issues, usable with caveats |
| C | Significant gaps, limited use |
| - | Not yet assessed |

---

## 3. Validation Criteria

### 3.1 Spectroscopic Data
- [ ] Redshift precision: σ_z/(1+z) < 0.01
- [ ] S/N ratio: median > 5 per resolution element
- [ ] Wavelength calibration: < 1 Å systematic
- [ ] Flux calibration: < 10% uncertainty

### 3.2 Photometric Data
- [ ] Filter coverage: minimum 4 bands (optical + NIR)
- [ ] Depth: 5σ limiting magnitude documented
- [ ] Photo-z quality: |Δz|/(1+z) < 0.15 for 80% sample
- [ ] Stellar mass uncertainty: < 0.3 dex

### 3.3 Catalog Completeness
- [ ] Selection function documented
- [ ] Contamination rate estimated
- [ ] Overlap regions cross-matched

---

## 4. JADES DR4 Validation

**File**: `Combined_DR4_external_v1.2.1.fits`
**Downloaded**: 2026-01-06
**Source**: https://jades-survey.github.io/scientists/data.html

### Contents
- 5,190 NIRSpec spectra
- 396 galaxies at z > 5.7
- Includes GS-z14-0 (z=14.32), GS-z14-1 (z=13.90)
- Prism + gratings (G140M/G235M/G395M/G395H)

### Quality Assessment
- [x] File integrity verified (90 MB)
- [ ] Column structure documented
- [ ] Redshift distribution analyzed
- [ ] Cross-match with JANUS-Z reference

---

## 5. Manual Download Instructions

### 5.1 COSMOS2025

**URL**: https://cosmos2025.iap.fr/

**Steps**:
1. Visit https://cosmos2025.iap.fr/
2. Navigate to "Data Products" or "Download"
3. Select "Master Catalog" (COSMOSWeb_mastercatalog_v1.fits)
4. Download to `data/jwst/cosmos2025/`

**Expected file**: `COSMOSWeb_mastercatalog_v1.fits` (~2 GB)

### 5.2 Bouwens+21 UV LF (HST Legacy)

**URL**: https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/AJ/162/47

**Steps**:
1. Visit VizieR catalog page
2. Select tables: `table1.dat`, `table2.dat`
3. Export as FITS or CSV
4. Save to `data/hst/bouwens21/`

**Note**: This dataset is OPTIONAL for Phase 2 completion.

---

## 6. Data Pipeline Status

```
Raw Data → Extraction → Cross-match → Quality Check → Analysis Ready
   ↓           ↓            ↓             ↓              ↓
 JADES      extract_     compile_     [This file]    PHASE 3
 COSMOS     highz.py     sample.py    validation
```

---

## 7. Known Issues

1. **COSMOS2025**: Direct URL download returns 404; requires web interface
2. **Bouwens+21**: VizieR requires authentication for bulk download
3. **DJA**: 8.4 GB total size - download on-demand recommended

---

## 8. Recommendations

1. **Priority**: Complete JADES DR4 column analysis
2. **Optional**: Manual download of COSMOS2025 if large statistics needed
3. **Defer**: Bouwens+21 to Phase 3 (HST comparison is secondary objective)

---

*DATA_QUALITY.md - VAL-Galaxies_primordiales - 2026-01-06*
