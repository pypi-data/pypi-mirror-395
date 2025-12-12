# asteroid-spinprops

## Overview
**asteroid-spinprops** is a Python package providing tools to fit SHG1G2 and SOCCA photometric models to sparse asteroid photometry.  
It supports multiband modeling, residual analysis and shape, period and pole orientation estimation for small solar system objects.

---

## Installation
Install the package via pip:

```bash
pip install asteroid_spinprops
```

## Input column requirements and preprocessing

`asteroid_spinprops` expects photometric measurements to follow the **Fink alert schema**.  
If your DataFrame uses different column names, they must be renamed to the standard format before analysis.

The package maps common input columns to Fink-style fields:

| Expected name | Description | 
|---------------|-------------|
| `cjd`         | Observation time (JD) |
| `cmagpsf`     | PSF magnitude |
| `csigmapsf`   | Magnitude uncertainty | 
| `cfid`        | Filter identifier | 
| `ra`          | Right ascension (deg) | 
| `dec`         | Declination (deg) |
| `Phase`       | Solar phase angle (deg) | 

### Additional columns created during preprocessing

The preprocessing step also adds the following fields:

- **`cmred` — Reduced magnitude**

  Computed from the heliocentric and observer-centric distances:


$$
\mathrm{cmred} = \mathrm{cmagpsf} - 5\log_{10}\!\left(\frac{r\,\Delta}{\mathrm{AU}^2}\right)
$$  
where `Obj_Sun_LTC_km` = \(r\) and `Range_LTC_km` = \(\Delta\).

- **`jd_ltc` — Light-time–corrected Julian Date**

  First converts MJD → JD (`+ 2400000.5`), then applies the correction

  $$
  JD_\mathrm{ltc} = JD - \frac{\Delta}{c},
  $$    

  using the one-way light-travel time in days.

```python
pdf.rename(
    columns={
        "Your_JD_column": "cjd",
        "Your_magnitudes_column": "cmagpsf",
        "Your_phase_angle_column": "Phase",
        "Your_RA_column": "ra",
        "Your_Dec_column": "dec",
        "Your_magnitude_uncertainty_column": "csigmapsf",
        "Your_filter_column": "cfid",
    },
    inplace=True,
)

# Add missing columns
pdf["cmred"] = pdf["cmagpsf"] - 5 * np.log10(
    pdf["Observer_SSO_distance_column"] * pdf["Sun_SSO_distance_column"] / (au**2)
)

# LT correction
pdf["cjd"] = pdf["cjd"] + 2400000.5  # MJD to JD
pdf["jd_ltc"] = pdf["cjd"] - pdf["Observer_SSO_distance_column"] / c_kmday  # light time correction

```

### Required inputs

Your input DataFrame must therefore include:

- time of observation                               (JD)
- PSF magnitude and uncertainty         
- filter ID         
- RA, Dec                                           (Degrees)                
- phase angle                       
- heliocentric distance                             (AU)
- observer-centric distance                         (AU)

The preprocessing step renames these fields to the Fink schema, computes reduced magnitudes, and applies the light-time correction to the observation timestamps.


## Quick Start
```python
import numpy as np
import pandas as pd
from asteroid_spinprops.ssolib import dataprep, periodest, modelfit

# Suppose `pdf` is your initial asteroid DataFrame 
# Ensure all columns are converted to the required single row format.
pdf_s = pd.DataFrame({col: [np.array(pdf[col])] for col in pdf.columns})

# Convert filter IDs to numeric
unique_vals, inv = np.unique(pdf_s["cfid"].values[0], return_inverse=True)
numeric_filter = inv + 1
pdf_s["cfid"].values[0] = numeric_filter

# --- Data cleaning and filtering ---
clean_data, errorbar_rejects = dataprep.errorbar_filtering(data=pdf_s, mlimit=0.7928) # mag limit from the LCDB
clean_data, projection_rejects = dataprep.projection_filtering(data=clean_data)
clean_data, iterative_rejects = dataprep.iterative_filtering(data=clean_data)

# --- Fit SOCCA ---
SOCCA_params = modelfit.get_fit_params(
        data=clean_data,
        flavor="SOCCA",
        shg1g2_constrained=True,
        pole_blind=False,
        period_blind=True,
        period_in=None,
        period_quality_flag=True
    )


## --- Or step-by-step --- ##
# --- Fit SHG1G2 model ---
shg1g2_params = modelfit.get_fit_params(
    data=clean_data,
    flavor="SHG1G2",
)

# Compute residuals for period analysis
residuals_dataframe = modelfit.make_residuals_df(
    clean_data, model_parameters=shg1g2_params
)

# --- Estimate rotation period ---
p_in, k_val, p_rms, signal_peak, window_peak = periodest.get_multiband_period_estimate(
    residuals_dataframe,
    k_free=True,
)

# Assess period robustness via bootstrap resampling
_, Nbs = periodest.perform_residual_resampling(
    resid_df=residuals_dataframe,
    p_min=0.03,
    p_max=2,
    k=int(k_val)
)

# --- Fit SOCCA model ---
SOCCA_params = modelfit.get_fit_params(
    data=clean_data,
    flavor="SSHG1G2",
    shg1g2_constrained=True,
    period_blind=False,
    pole_blind=False,
    period_in=p_in,
    period_quality_flag=False
)
```

## Models
Photometric models from Carry et al.(2024) {2024A&A...687A..38C}
and https://github.com/astrolabsoftware

## Project status
Under development
