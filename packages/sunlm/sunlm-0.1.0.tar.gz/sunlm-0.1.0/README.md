# sunlm

**sunlm** is a lightweight, social-science–friendly Python package that provides an intuitive OLS regression wrapper using formula syntax (similar to R's `lm()`), with standardized coefficients, semi-partial R² (sr²), and APA-style output.  
It is designed for researchers in communication, psychology, marketing, and the social sciences who want simple but informative regression summaries without complex statistical coding.

---

## 🔧 Features

- ✔️ Formula interface via **patsy** (`y ~ x1 + x2`)
- ✔️ OLS estimation via **statsmodels**
- ✔️ Unstandardized coefficients (B)  
- ✔️ Standardized coefficients (Beta, β)
- ✔️ Semi-partial R² (sr²) for effect size
- ✔️ Clean social-science–style regression summary
- ✔️ Return results as a DataFrame for further formatting/export
- ✔️ Easy to extend (robust SE, interactions, PROCESS-style mediation planned)

---

## 📥 Installation

### From PyPI (once officially released)
```bash
pip install pysslm


# Quick Start Example
import pandas as pd
import sslm

# Example dataset
df = pd.DataFrame({
    "y":  [1, 2, 3, 4, 5],
    "x1": [2, 1, 4, 3, 5]
})

# Run regression
model = sslm.ols("y ~ x1", data=df)

# Print summary
model.summary()

# Sample Output
## 📊 SSLM Regression Summary
---------------------------------------------------------
           Unstd. B  Std. Err.  Std. β   t-value p-print  sr^2
Intercept       0.6   1.148913     NaN  0.522233   0.638   NaN
x1              0.8   0.346410     0.8  2.309401   0.104  0.64

## 📈 Model Fit Statistics
---------------------------------------------------------
Dependent variable           y
N                            5
R-squared                 0.64
Adjusted R-squared        0.52
F-statistic           5.333333
Prob (F-statistic)    0.104088
---------------------------------------------------------


# API Overview

sslm.ols(formula, data)

Runs OLS regression using formula syntax.

Parameters
	•	formula — string, e.g., "y ~ x1 + x2"
	•	data — pandas DataFrame

Returns
	•	SSLM_Model object

⸻

model.summary()

Prints APA-style regression output including:
	•	unstandardized coefficients (B)
	•	standard errors
	•	standardized beta (β)
	•	t-values & p-values
	•	semi-partial R² (sr²)
	•	model-level fit stats (R², Adj. R², F, etc.)

⸻

model.as_dataframe()

Returns the full coefficient table as a pandas DataFrame
(ideal for exporting to Excel, LaTeX, or APA tables).

# Project Structure
sslm/
 ├─ sslm/
 │   ├─ __init__.py
 │   └─ core.py        # main implementation
 ├─ pyproject.toml
 └─ README.md

# Contributing
Pull requests, feature suggestions, and bug reports are welcome once the GitHub repository is available.

# License
MIT License

# Author
Seonwoo Kim
Northern Arizona University
Designed for students, researchers, and anyone needing a clean statistical pipeline in Python.
