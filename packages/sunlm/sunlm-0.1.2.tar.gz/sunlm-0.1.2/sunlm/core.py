import pandas as pd
import numpy as np
import statsmodels.api as sm
from patsy import dmatrices  # formula parsing

# Note: Users will need to install patsy: pip install patsy


class SunLM_Model:
    """
    Simple, social-science–friendly OLS wrapper using formula syntax.

    - Uses patsy to parse formulas
    - Fits OLS via statsmodels
    - Provides unstandardized B, standardized Beta, semi-partial R² (sr²), etc.
    """

    def __init__(self, formula: str, data: pd.DataFrame):
        self.formula = formula
        self.data = data
        self.fit_result = None
        self.X = None
        self.y = None

        # 1. Parse formula and create design matrices using patsy
        self.y, self.X = dmatrices(formula, data, return_type="dataframe")

        # 2. Run OLS Regression
        model = sm.OLS(self.y, self.X)
        self.fit_result = model.fit()

    def summary(self):
        """
        Prints a regression summary in a social-science style table.
        """
        if self.fit_result is None:
            print("Model has not been fitted.")
            return

        df_result, model_stats = self._calculate_sslm_metrics()

        print("## 📊 SSLM Regression Summary")
        print("---------------------------------------------------------")
        print(df_result[['Unstd. B', 'Std. Err.', 'Std. β', 't-value', 'p-print', 'sr^2']])
        print("\n## 📈 Model Fit Statistics")
        print("---------------------------------------------------------")
        print(pd.Series(model_stats).to_string(header=False))
        print("---------------------------------------------------------")

    def as_dataframe(self):
        """
        Returns the coefficient table as a pandas DataFrame
        (for further formatting/export).
        """
        df_result, _ = self._calculate_sslm_metrics()
        return df_result

    def _calculate_sslm_metrics(self):
        """
        Internal method to calculate standardized coefficients and sr².
        """
        model_results = self.fit_result
        X = self.X
        y = self.y.iloc[:, 0]  # y is a 1-column DataFrame from patsy

        # Identify intercept-like column (patsy usually names it 'Intercept')
        exog_names = list(model_results.params.index)
        intercept_candidates = [name for name in exog_names if "Intercept" in name]
        intercept_name = intercept_candidates[0] if intercept_candidates else None

        if intercept_name is not None:
            X_vars = X.drop(columns=[intercept_name], errors='ignore')
        else:
            X_vars = X.copy()

        sd_y = y.std(ddof=1)
        R2_full = model_results.rsquared

        results_df = pd.DataFrame({
            'Unstd. B': model_results.params,
            'Std. Err.': model_results.bse,
            't-value': model_results.tvalues,
            'p-value': model_results.pvalues
        })

        beta_list = []
        sr2_list = []

        for var_name, B in model_results.params.items():
            # Skip intercept for Std. β and sr²
            if var_name == intercept_name:
                beta_list.append(np.nan)
                sr2_list.append(np.nan)
                continue

            # Standardized Beta
            sd_x = X_vars[var_name].std(ddof=1)
            beta = B * (sd_x / sd_y)
            beta_list.append(beta)

            # Semi-partial R² (ΔR²): R²_full - R²_reduced_without_var
            X_reduced = X.drop(columns=[var_name], errors='ignore')
            model_reduced = sm.OLS(y, X_reduced).fit()
            sr2 = R2_full - model_reduced.rsquared
            sr2_list.append(sr2)

        results_df['Std. β'] = beta_list
        results_df['sr^2'] = sr2_list

        # p-value formatting
        results_df['p-print'] = results_df['p-value'].apply(
            lambda x: f"{x:.3f}" if x >= .001 else "< .001"
        )

        # Model fit stats
        model_fit_stats = {
            'Dependent variable': self.y.columns[0],
            'N': int(model_results.nobs),
            'R-squared': model_results.rsquared,
            'Adjusted R-squared': model_results.rsquared_adj,
            'F-statistic': model_results.fvalue,
            'Prob (F-statistic)': model_results.f_pvalue,
        }

        return results_df, model_fit_stats


def ols(formula: str, data: pd.DataFrame) -> SunLM_Model:
    """
    High-level user function:
    Runs OLS regression using formula notation and returns an SSLM_Model object.

    Example
    -------
    model = ols("y ~ x1 + x2 + x3", data=df)
    model.summary()
    """
    return SunLM_Model(formula, data)