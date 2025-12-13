"""
Ultra Statistical Analysis

Goes far beyond basic scipy with:
- ANOVA/MANOVA
- Time-series statistical tests
- Bayesian statistics
- Non-parametric tests
- Multivariate analysis
- Power analysis
- Bootstrap methods
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from scipy import stats
from scipy.stats import (
    f_oneway,
    kruskal,
    friedmanchisquare,
    chi2_contingency,
    fisher_exact,
    mcnemar,
    cochran_q,
    mannwhitneyu,
    wilcoxon,
    kendalltau,
    spearmanr,
    pearsonr,
)
import warnings

try:
    from scipy.stats import manova

    MANOVA_AVAILABLE = True
except ImportError:
    MANOVA_AVAILABLE = False
    warnings.warn("MANOVA not available. Some multivariate tests will be limited.")


class UltraStatisticalAnalyzer:
    """
    Ultra statistical analysis that goes far beyond basic scipy.
    Includes ANOVA, MANOVA, time-series tests, Bayesian methods, and more.
    """

    def __init__(self, alpha: float = 0.05):
        """
        Initialize ultra statistical analyzer.

        Args:
            alpha: Significance level for hypothesis tests
        """
        self.alpha = alpha

    def anova_analysis(
        self,
        groups: List[pd.Series],
        post_hoc: bool = True,
    ) -> Dict[str, Any]:
        """
        ANOVA analysis with post-hoc tests and effect sizes.

        Args:
            groups: List of groups (Series) to compare
            post_hoc: Whether to perform post-hoc tests

        Returns:
            Dictionary with ANOVA results, post-hoc tests, and effect sizes
        """
        # Clean groups
        groups_clean = [g.dropna() for g in groups if len(g.dropna()) > 0]

        if len(groups_clean) < 2:
            return {"error": "Need at least 2 groups for ANOVA"}

        results: Dict[str, Any] = {
            "anova": {},
            "post_hoc": {},
            "effect_sizes": {},
            "interpretation": "",
            "recommendations": [],
        }
        # Type annotations for nested dicts
        anova_dict: Dict[str, Any] = results["anova"]  # type: ignore
        effect_sizes_dict: Dict[str, Any] = results["effect_sizes"]  # type: ignore

        # One-way ANOVA
        try:
            f_stat, p_value = f_oneway(*groups_clean)
            results["anova"]["one_way"] = {
                "f_statistic": f_stat,
                "p_value": p_value,
                "significant": p_value < self.alpha,
                "df_between": len(groups_clean) - 1,
                "df_within": sum(len(g) for g in groups_clean) - len(groups_clean),
            }

            # Calculate effect size: Eta-squared
            all_data = np.concatenate(groups_clean)
            grand_mean = np.mean(all_data)
            ss_between = sum(
                len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups_clean
            )
            ss_total = sum((x - grand_mean) ** 2 for x in all_data)
            eta_squared = ss_between / ss_total if ss_total > 0 else 0

            effect_sizes_dict["eta_squared"] = eta_squared

            # Interpret eta-squared
            if eta_squared < 0.01:
                effect_interpretation = "negligible"
            elif eta_squared < 0.06:
                effect_interpretation = "small"
            elif eta_squared < 0.14:
                effect_interpretation = "medium"
            else:
                effect_interpretation = "large"

            effect_sizes_dict["eta_squared_interpretation"] = effect_interpretation

        except Exception as e:
            anova_dict["one_way"] = {"error": str(e)}

        # Kruskal-Wallis (non-parametric alternative)
        try:
            h_stat, p_value = kruskal(*groups_clean)
            results["anova"]["kruskal_wallis"] = {
                "h_statistic": h_stat,
                "p_value": p_value,
                "significant": p_value < self.alpha,
            }
        except Exception as e:
            anova_dict["kruskal_wallis"] = {"error": str(e)}

        # Post-hoc tests
        if post_hoc and len(groups_clean) > 2:
            post_hoc_results = {}
            for i in range(len(groups_clean)):
                for j in range(i + 1, len(groups_clean)):
                    try:
                        # Bonferroni correction
                        t_stat, p_value = stats.ttest_ind(
                            groups_clean[i], groups_clean[j]
                        )
                        p_corrected = min(
                            p_value * (len(groups_clean) * (len(groups_clean) - 1) / 2),
                            1.0,
                        )

                        post_hoc_results[f"group_{i}_vs_group_{j}"] = {
                            "t_statistic": t_stat,
                            "p_value": p_value,
                            "p_corrected": p_corrected,
                            "significant": p_corrected < self.alpha,
                        }
                    except Exception as e:
                        post_hoc_results[f"group_{i}_vs_group_{j}"] = {"error": str(e)}

            results["post_hoc"] = post_hoc_results

        # Interpretation
        anova_sig = anova_dict.get("one_way", {}).get("significant", False)
        if anova_sig:
            results["interpretation"] = "Groups are significantly different"
            results["recommendations"].append(
                "Reject null hypothesis - groups differ significantly"
            )
        else:
            results["interpretation"] = "No significant difference between groups"
            results["recommendations"].append(
                "Fail to reject null hypothesis - groups are similar"
            )

        return results

    def manova_analysis(
        self,
        groups: List[pd.DataFrame],
        group_labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Multivariate Analysis of Variance (MANOVA).

        Args:
            groups: List of DataFrames (each group has multiple variables)
            group_labels: Optional labels for groups

        Returns:
            Dictionary with MANOVA results
        """
        if not MANOVA_AVAILABLE:
            return {"error": "MANOVA not available. Install required dependencies."}

        results: Dict[str, Any] = {
            "manova": {},
            "interpretation": "",
            "recommendations": [],
        }
        # Type annotation for manova dict
        manova_dict: Dict[str, Any] = results["manova"]  # type: ignore

        # Prepare data
        all_data = []
        group_indices = []
        for i, group_df in enumerate(groups):
            group_clean = group_df.dropna()
            if len(group_clean) > 0:
                all_data.append(group_clean.values)
                group_indices.extend([i] * len(group_clean))

        if len(all_data) < 2:
            return {"error": "Need at least 2 groups for MANOVA"}

        # Combine all data
        X = np.vstack(all_data)
        y = np.array(group_indices)

        try:
            # Perform MANOVA
            manova_result = manova(X, y)
            manova_dict["statistic"] = manova_result.statistic
            manova_dict["p_value"] = manova_result.pvalue
            manova_dict["significant"] = manova_result.pvalue < self.alpha

            if manova_dict["significant"]:
                results["interpretation"] = (
                    "Groups differ significantly on multivariate measures"
                )
                results["recommendations"].append(
                    "Perform univariate ANOVAs to identify which variables differ"
                )
            else:
                results["interpretation"] = (
                    "No significant multivariate difference between groups"
                )

        except Exception as e:
            manova_dict["error"] = str(e)

        return results

    def time_series_statistical_tests(
        self,
        series: pd.Series,
        test_stationarity: bool = True,
        test_trend: bool = True,
    ) -> Dict[str, Any]:
        """
        Time-series statistical tests.

        Args:
            series: Time series data
            test_stationarity: Whether to test for stationarity
            test_trend: Whether to test for trends

        Returns:
            Dictionary with time-series test results
        """
        series_clean = series.dropna()

        if len(series_clean) < 10:
            return {"error": "Insufficient data for time-series tests"}

        results: Dict[str, Any] = {
            "stationarity": {},
            "trend": {},
            "autocorrelation": {},
            "interpretation": "",
            "recommendations": [],
        }
        # Type annotations for nested dicts
        stationarity_dict: Dict[str, Any] = results["stationarity"]  # type: ignore
        trend_dict: Dict[str, Any] = results["trend"]  # type: ignore
        autocorrelation_dict: Dict[str, Any] = results["autocorrelation"]  # type: ignore

        # Augmented Dickey-Fuller test (stationarity)
        if test_stationarity:
            try:
                from statsmodels.tsa.stattools import adfuller

                adf_stat, adf_p, _, _, adf_critical, _ = adfuller(series_clean)
                stationarity_dict["adf"] = {
                    "statistic": adf_stat,
                    "p_value": adf_p,
                    "critical_values": adf_critical,
                    "stationary": adf_p < self.alpha,
                }

                if stationarity_dict["adf"]["stationary"]:
                    results["interpretation"] += "Series is stationary. "
                else:
                    results["interpretation"] += "Series is non-stationary. "
                    results["recommendations"].append(
                        "Consider differencing or transformation"
                    )

            except ImportError:
                stationarity_dict["adf"] = {
                    "error": "statsmodels not available. Install: pip install statsmodels"
                }
            except Exception as e:
                stationarity_dict["adf"] = {"error": str(e)}

        # Trend test (Mann-Kendall)
        if test_trend:
            try:
                # Simple trend test using linear regression
                x = np.arange(len(series_clean))
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    x, series_clean
                )

                trend_dict["linear"] = {
                    "slope": slope,
                    "p_value": p_value,
                    "r_squared": r_value**2,
                    "has_trend": p_value < self.alpha,
                }

                if trend_dict["linear"]["has_trend"]:
                    trend_direction = "increasing" if slope > 0 else "decreasing"
                    results["interpretation"] += f"Series has {trend_direction} trend. "
                    results["recommendations"].append("Consider detrending if needed")

            except Exception as e:
                trend_dict["linear"] = {"error": str(e)}

        # Autocorrelation
        try:
            autocorr_lag1 = series_clean.autocorr(lag=1)
            autocorr_lag5 = (
                series_clean.autocorr(lag=5) if len(series_clean) > 5 else None
            )

            results["autocorrelation"] = {
                "lag_1": autocorr_lag1,
                "lag_5": autocorr_lag5,
                "has_autocorrelation": (
                    abs(autocorr_lag1) > 0.3 if not np.isnan(autocorr_lag1) else False
                ),
            }

            if autocorrelation_dict["has_autocorrelation"]:
                results["recommendations"].append(
                    "Series shows autocorrelation - consider ARIMA models"
                )

        except Exception as e:
            results["autocorrelation"] = {"error": str(e)}

        return results

    def bayesian_analysis(
        self,
        group1: pd.Series,
        group2: pd.Series,
        prior_mean: float = 0.0,
        prior_std: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Bayesian statistical analysis for group comparison.

        Args:
            group1: First group
            group2: Second group
            prior_mean: Prior mean for Bayesian analysis
            prior_std: Prior standard deviation

        Returns:
            Dictionary with Bayesian analysis results
        """
        group1_clean = group1.dropna()
        group2_clean = group2.dropna()

        if len(group1_clean) < 3 or len(group2_clean) < 3:
            return {"error": "Insufficient data for Bayesian analysis"}

        results = {
            "posterior": {},
            "bayes_factor": {},
            "interpretation": "",
            "recommendations": [],
        }

        # Simple Bayesian analysis
        mean1, std1 = group1_clean.mean(), group1_clean.std()
        mean2, std2 = group2_clean.mean(), group2_clean.std()
        n1, n2 = len(group1_clean), len(group2_clean)

        # Posterior distribution parameters
        # Using conjugate prior (normal-normal)
        posterior_mean = (
            prior_mean / prior_std**2 + (mean1 - mean2) / (std1**2 / n1 + std2**2 / n2)
        ) / (1 / prior_std**2 + 1 / (std1**2 / n1 + std2**2 / n2))
        posterior_std = np.sqrt(
            1 / (1 / prior_std**2 + 1 / (std1**2 / n1 + std2**2 / n2))
        )

        results["posterior"] = {
            "mean": posterior_mean,
            "std": posterior_std,
            "credible_interval_95": [
                posterior_mean - 1.96 * posterior_std,
                posterior_mean + 1.96 * posterior_std,
            ],
        }

        # Bayes factor (simplified)
        # Compare models: H0 (no difference) vs H1 (difference)
        likelihood_h0 = stats.norm.pdf(0, loc=0, scale=posterior_std)
        likelihood_h1 = stats.norm.pdf(posterior_mean, loc=0, scale=posterior_std)
        bayes_factor = likelihood_h1 / likelihood_h0 if likelihood_h0 > 0 else np.inf

        results["bayes_factor"] = {
            "value": bayes_factor,
            "interpretation": self._interpret_bayes_factor(bayes_factor),
        }

        # Interpretation
        if abs(posterior_mean) > 2 * posterior_std:
            results["interpretation"] = "Strong evidence for difference between groups"
        else:
            results["interpretation"] = "Weak evidence for difference between groups"

        return results

    def _interpret_bayes_factor(self, bf: float) -> str:
        """Interpret Bayes factor."""
        if bf < 1:
            return "Evidence for H0"
        elif bf < 3:
            return "Anecdotal evidence for H1"
        elif bf < 10:
            return "Moderate evidence for H1"
        elif bf < 30:
            return "Strong evidence for H1"
        elif bf < 100:
            return "Very strong evidence for H1"
        else:
            return "Extreme evidence for H1"

    def power_analysis(
        self,
        effect_size: float,
        alpha: Optional[float] = None,
        power: Optional[float] = None,
        n: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Statistical power analysis.

        Args:
            effect_size: Expected effect size (Cohen's d)
            alpha: Significance level (default: self.alpha)
            power: Desired power (default: 0.8)
            n: Sample size

        Returns:
            Dictionary with power analysis results
        """
        alpha = alpha or self.alpha
        power = power or 0.8

        results: Dict[str, Any] = {
            "parameters": {
                "effect_size": effect_size,
                "alpha": alpha,
                "power": power,
            },
            "sample_size": {},
            "interpretation": "",
        }
        # Type annotation for nested dicts
        sample_size_dict: Dict[str, Any] = results["sample_size"]  # type: ignore
        power_dict: Dict[str, Any] = results.get("power", {})  # type: ignore

        # Calculate required sample size if not provided
        if n is None:
            from scipy.stats import norm

            z_alpha = norm.ppf(1 - alpha / 2)
            z_power = norm.ppf(power)

            n_required = 2 * ((z_alpha + z_power) / effect_size) ** 2
            sample_size_dict["required"] = int(np.ceil(n_required))
            results["interpretation"] = (
                f"Required sample size: {sample_size_dict['required']} per group"
            )

        # Calculate achieved power if sample size provided
        else:
            from scipy.stats import norm

            z_alpha = norm.ppf(1 - alpha / 2)
            z_effect = effect_size * np.sqrt(n / 2)
            achieved_power = norm.cdf(z_effect - z_alpha) + norm.cdf(
                -z_effect - z_alpha
            )

            sample_size_dict["provided"] = n
            results["power"] = {
                "achieved": achieved_power,
                "adequate": achieved_power >= power,
            }
            results["interpretation"] = f"Achieved power: {achieved_power:.3f}"

        return results

    def bootstrap_analysis(
        self,
        data: pd.Series,
        statistic: str = "mean",
        n_bootstrap: int = 1000,
        confidence_level: float = 0.95,
    ) -> Dict[str, Any]:
        """
        Bootstrap statistical analysis.

        Args:
            data: Input data
            statistic: Statistic to bootstrap ('mean', 'median', 'std')
            n_bootstrap: Number of bootstrap samples
            confidence_level: Confidence level for intervals

        Returns:
            Dictionary with bootstrap results
        """
        data_clean = data.dropna()

        if len(data_clean) < 10:
            return {"error": "Insufficient data for bootstrap analysis"}

        results: Dict[str, Any] = {
            "bootstrap": {},
            "confidence_interval": {},
            "interpretation": "",
        }
        # Type annotation for bootstrap dict to help mypy
        bootstrap_dict: Dict[str, Any] = results["bootstrap"]  # type: ignore

        # Bootstrap samples
        bootstrap_stats: List[Union[float, np.floating[Any]]] = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(data_clean, size=len(data_clean), replace=True)
            if statistic == "mean":
                bootstrap_stats.append(float(np.mean(sample)))
            elif statistic == "median":
                bootstrap_stats.append(float(np.median(sample)))
            elif statistic == "std":
                bootstrap_stats.append(float(np.std(sample)))
            else:
                bootstrap_stats.append(float(np.mean(sample)))

        bootstrap_stats_array: np.ndarray = np.array(bootstrap_stats)

        # Calculate statistics
        bootstrap_dict["mean"] = np.mean(bootstrap_stats_array)
        bootstrap_dict["std"] = np.std(bootstrap_stats_array)
        bootstrap_dict["bias"] = np.mean(bootstrap_stats_array) - (
            np.mean(data_clean) if statistic == "mean" else np.median(data_clean)
        )

        # Confidence interval
        alpha_ci = 1 - confidence_level
        lower = np.percentile(bootstrap_stats_array, 100 * alpha_ci / 2)
        upper = np.percentile(bootstrap_stats_array, 100 * (1 - alpha_ci / 2))

        results["confidence_interval"] = {
            "lower": lower,
            "upper": upper,
            "level": confidence_level,
        }

        results["interpretation"] = (
            f"Bootstrap {statistic}: {bootstrap_dict['mean']:.3f} [{lower:.3f}, {upper:.3f}]"
        )

        return results
