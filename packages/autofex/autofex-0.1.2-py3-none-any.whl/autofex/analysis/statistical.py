"""
Statistical Analysis

Goes beyond basic scipy to provide integrated statistical insights
with automated hypothesis testing and effect size calculations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from scipy import stats
from scipy.stats import (
    shapiro,
    normaltest,
    kstest,
    anderson,
    jarque_bera,
    levene,
    bartlett,
    mannwhitneyu,
    kruskal,
    chi2_contingency,
)
import warnings


class StatisticalAnalyzer:
    """
    Statistical analysis that goes beyond basic scipy functions.
    Provides integrated insights, effect sizes, and automated interpretations.
    """

    def __init__(self, alpha: float = 0.05):
        """
        Initialize statistical analyzer.

        Args:
            alpha: Significance level for hypothesis tests
        """
        self.alpha = alpha

    def comprehensive_normality_test(self, series: pd.Series) -> Dict[str, Any]:
        """
        Comprehensive normality testing with multiple tests and effect sizes.

        Args:
            series: Input data series

        Returns:
            Dictionary with test results and interpretations
        """
        series_clean = series.dropna()

        if len(series_clean) < 3:
            return {"error": "Insufficient data for normality testing"}

        results: Dict[str, Any] = {
            "tests": {},
            "interpretation": "",
            "recommendation": "",
        }
        # Type annotation for tests dict to help mypy
        tests_dict: Dict[str, Any] = results["tests"]  # type: ignore

        # Shapiro-Wilk test (best for small samples)
        if 3 <= len(series_clean) <= 5000:
            try:
                stat, p_value = shapiro(series_clean)
                tests_dict["shapiro_wilk"] = {
                    "statistic": stat,
                    "p_value": p_value,
                    "significant": p_value < self.alpha,
                }
            except Exception as e:
                tests_dict["shapiro_wilk"] = {"error": str(e)}

        # D'Agostino's normality test (good for larger samples)
        if len(series_clean) >= 8:
            try:
                stat, p_value = normaltest(series_clean)
                tests_dict["dagostino"] = {
                    "statistic": stat,
                    "p_value": p_value,
                    "significant": p_value < self.alpha,
                }
            except Exception as e:
                tests_dict["dagostino"] = {"error": str(e)}

        # Kolmogorov-Smirnov test
        if len(series_clean) >= 4:
            try:
                mean, std = series_clean.mean(), series_clean.std()
                stat, p_value = kstest(
                    series_clean, lambda x: stats.norm.cdf(x, mean, std)
                )
                tests_dict["kolmogorov_smirnov"] = {
                    "statistic": stat,
                    "p_value": p_value,
                    "significant": p_value < self.alpha,
                }
            except Exception as e:
                tests_dict["kolmogorov_smirnov"] = {"error": str(e)}

        # Jarque-Bera test (tests skewness and kurtosis)
        if len(series_clean) >= 4:
            try:
                stat, p_value = jarque_bera(series_clean)
                tests_dict["jarque_bera"] = {
                    "statistic": stat,
                    "p_value": p_value,
                    "significant": p_value < self.alpha,
                }
            except Exception as e:
                tests_dict["jarque_bera"] = {"error": str(e)}

        # Calculate skewness and kurtosis
        skewness = series_clean.skew()
        kurtosis = series_clean.kurtosis()

        results["descriptive"] = {
            "skewness": skewness,
            "kurtosis": kurtosis,
            "mean": series_clean.mean(),
            "std": series_clean.std(),
            "median": series_clean.median(),
        }

        # Interpretation
        significant_tests = sum(
            1
            for test in results["tests"].values()
            if isinstance(test, dict) and test.get("significant", False)
        )
        total_tests = len(
            [
                t
                for t in results["tests"].values()
                if isinstance(t, dict) and "p_value" in t
            ]
        )

        if significant_tests == 0 and total_tests > 0:
            results["interpretation"] = "Data appears to be normally distributed"
            results["recommendation"] = "Parametric tests are appropriate"
        elif significant_tests > total_tests / 2:
            results["interpretation"] = "Data is NOT normally distributed"
            results["recommendation"] = "Use non-parametric tests or transformations"
        else:
            results["interpretation"] = (
                "Mixed results - use caution with parametric tests"
            )
            results["recommendation"] = (
                "Consider transformations or non-parametric alternatives"
            )

        return results

    def comprehensive_comparison_test(
        self,
        group1: pd.Series,
        group2: pd.Series,
        test_type: str = "auto",
    ) -> Dict[str, Any]:
        """
        Comprehensive comparison between two groups with multiple tests and effect sizes.

        Args:
            group1: First group data
            group2: Second group data
            test_type: Test type ('auto', 'parametric', 'nonparametric')

        Returns:
            Dictionary with test results, effect sizes, and interpretations
        """
        group1_clean = group1.dropna()
        group2_clean = group2.dropna()

        if len(group1_clean) < 3 or len(group2_clean) < 3:
            return {"error": "Insufficient data for comparison"}

        results: Dict[str, Any] = {
            "tests": {},
            "effect_sizes": {},
            "interpretation": "",
            "recommendation": "",
        }
        # Type annotation for tests dict to help mypy
        tests_dict: Dict[str, Any] = results["tests"]  # type: ignore

        # Check normality for both groups
        norm1 = self.comprehensive_normality_test(group1_clean)
        norm2 = self.comprehensive_normality_test(group2_clean)

        is_normal = (
            norm1.get("interpretation", "").find("normally distributed") >= 0
            and norm2.get("interpretation", "").find("normally distributed") >= 0
        )

        # Check variance homogeneity
        try:
            levene_stat, levene_p = levene(group1_clean, group2_clean)
            equal_var = levene_p > self.alpha
        except:
            equal_var = True  # Assume equal variance if test fails

        # Choose appropriate test
        if test_type == "auto":
            use_parametric = is_normal and equal_var
        else:
            use_parametric = test_type == "parametric"

        # Parametric tests
        if use_parametric:
            try:
                t_stat, t_p = stats.ttest_ind(
                    group1_clean, group2_clean, equal_var=equal_var
                )
                tests_dict["t_test"] = {
                    "statistic": t_stat,
                    "p_value": t_p,
                    "significant": t_p < self.alpha,
                    "equal_variance": equal_var,
                }

                # Effect size: Cohen's d
                pooled_std = np.sqrt(
                    (
                        (len(group1_clean) - 1) * group1_clean.var()
                        + (len(group2_clean) - 1) * group2_clean.var()
                    )
                    / (len(group1_clean) + len(group2_clean) - 2)
                )
                cohens_d = (group1_clean.mean() - group2_clean.mean()) / pooled_std
                results["effect_sizes"]["cohens_d"] = cohens_d

                # Interpret Cohen's d
                if abs(cohens_d) < 0.2:
                    effect_interpretation = "negligible"
                elif abs(cohens_d) < 0.5:
                    effect_interpretation = "small"
                elif abs(cohens_d) < 0.8:
                    effect_interpretation = "medium"
                else:
                    effect_interpretation = "large"

                results["effect_sizes"][
                    "cohens_d_interpretation"
                ] = effect_interpretation

            except Exception as e:
                tests_dict["t_test"] = {"error": str(e)}

        # Non-parametric tests
        if not use_parametric or test_type == "nonparametric":
            try:
                u_stat, u_p = mannwhitneyu(
                    group1_clean, group2_clean, alternative="two-sided"
                )
                tests_dict["mann_whitney_u"] = {
                    "statistic": u_stat,
                    "p_value": u_p,
                    "significant": u_p < self.alpha,
                }

                # Effect size: Rank-biserial correlation
                n1, n2 = len(group1_clean), len(group2_clean)
                r_biserial = 1 - (2 * u_stat) / (n1 * n2)
                results["effect_sizes"]["rank_biserial"] = r_biserial

            except Exception as e:
                tests_dict["mann_whitney_u"] = {"error": str(e)}

        # Descriptive statistics
        results["descriptive"] = {
            "group1": {
                "mean": group1_clean.mean(),
                "median": group1_clean.median(),
                "std": group1_clean.std(),
                "n": len(group1_clean),
            },
            "group2": {
                "mean": group2_clean.mean(),
                "median": group2_clean.median(),
                "std": group2_clean.std(),
                "n": len(group2_clean),
            },
        }

        # Interpretation
        significant = any(
            test.get("significant", False)
            for test in results["tests"].values()
            if isinstance(test, dict)
        )

        if significant:
            results["interpretation"] = "Groups are significantly different"
            effect_size = results["effect_sizes"].get("cohens_d") or results[
                "effect_sizes"
            ].get("rank_biserial", 0)
            if abs(effect_size) > 0.5:
                results["recommendation"] = "Large effect size - practical significance"
            else:
                results["recommendation"] = "Statistically significant but small effect"
        else:
            results["interpretation"] = "No significant difference between groups"
            results["recommendation"] = "Groups are statistically similar"

        return results

    def correlation_analysis(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        Correlation analysis with multiple methods and interpretations.

        Args:
            X: Feature DataFrame
            y: Target variable (optional)

        Returns:
            Dictionary with correlation analysis results
        """
        results: Dict[str, Any] = {
            "feature_correlations": {},
            "target_correlations": {},
            "multicollinearity": {},
            "recommendations": [],
        }
        # Type annotations for nested dicts
        multicollinearity_dict: Dict[str, Any] = results["multicollinearity"]  # type: ignore
        recommendations_list: List[str] = results["recommendations"]  # type: ignore

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return results

        # Feature-feature correlations
        corr_matrix = X[numeric_cols].corr()

        # Find highly correlated pairs
        high_corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.9:
                    high_corr_pairs.append(
                        {
                            "feature1": corr_matrix.columns[i],
                            "feature2": corr_matrix.columns[j],
                            "correlation": corr_val,
                        }
                    )

        multicollinearity_dict["high_correlation_pairs"] = high_corr_pairs
        multicollinearity_dict["count"] = len(high_corr_pairs)

        if len(high_corr_pairs) > 0:
            recommendations_list.append(
                f"Found {len(high_corr_pairs)} highly correlated pairs (>0.9). Consider removing redundant features."
            )

        # Target correlations (if available)
        if y is not None:
            target_corrs = {}
            for col in numeric_cols:
                try:
                    if y.dtype in ["object", "category"] or y.nunique() < 20:
                        # Categorical target - use point-biserial or Cramér's V
                        if y.nunique() == 2:
                            corr, p_val = stats.pointbiserialr(
                                X[col].fillna(X[col].mean()), y
                            )
                        else:
                            # Use ANOVA F-statistic as correlation proxy
                            groups = [X[col][y == cls].dropna() for cls in y.unique()]
                            if len(groups) > 1:
                                f_stat, p_val = stats.f_oneway(*groups)
                                corr = (
                                    np.sqrt(f_stat / (f_stat + len(X)))
                                    if f_stat > 0
                                    else 0
                                )
                            else:
                                continue
                    else:
                        # Continuous target - Pearson correlation
                        corr, p_val = stats.pearsonr(X[col].fillna(X[col].mean()), y)

                    target_corrs[col] = {
                        "correlation": corr,
                        "p_value": p_val,
                        "significant": p_val < self.alpha,
                        "abs_correlation": abs(corr),
                    }
                except Exception as e:
                    continue

            results["target_correlations"] = target_corrs

            # Top correlated features
            top_corr = sorted(
                target_corrs.items(),
                key=lambda x: abs(x[1]["correlation"]),
                reverse=True,
            )[:10]

            results["target_correlations"]["top_features"] = [
                {"feature": k, **v} for k, v in top_corr
            ]

            if top_corr:
                results["recommendations"].append(
                    f"Top feature: {top_corr[0][0]} (correlation: {top_corr[0][1]['correlation']:.3f})"
                )

        return results

    def automated_insights(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        Generate automated statistical insights and recommendations.

        Args:
            X: Feature DataFrame
            y: Target variable (optional)

        Returns:
            Dictionary with automated insights
        """
        insights: Dict[str, Any] = {
            "data_characteristics": {},
            "statistical_tests": {},
            "recommendations": [],
            "warnings": [],
        }
        # Type annotations for nested structures
        insights_statistical_tests: Dict[str, Any] = insights["statistical_tests"]  # type: ignore
        insights_recommendations: List[str] = insights["recommendations"]  # type: ignore
        insights_warnings: List[str] = insights["warnings"]  # type: ignore

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        # Analyze each numeric feature
        for col in numeric_cols[:10]:  # Limit to first 10 for performance
            series = X[col].dropna()

            if len(series) < 3:
                continue

            # Normality test
            norm_result = self.comprehensive_normality_test(series)
            insights_statistical_tests[col] = {
                "normality": norm_result,
                "skewness": series.skew(),
                "kurtosis": series.kurtosis(),
            }

            # Recommendations based on distribution
            if abs(series.skew()) > 2:
                insights_recommendations.append(
                    f"Feature '{col}' is highly skewed (skew={series.skew():.2f}). Consider log/sqrt transformation."
                )

            if abs(series.kurtosis()) > 3:
                insights_warnings.append(
                    f"Feature '{col}' has high kurtosis (kurt={series.kurtosis():.2f}). May have outliers."
                )

        # Correlation analysis
        if len(numeric_cols) >= 2:
            corr_analysis = self.correlation_analysis(X, y)
            insights["correlation_analysis"] = corr_analysis
            insights_recommendations.extend(corr_analysis.get("recommendations", []))

        return insights
