"""
Scipy Operations

Leverages scipy for scientific computing features.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from scipy import stats, signal, optimize, special, interpolate
from scipy.spatial.distance import pdist, squareform
import warnings


class ScipyOperations:
    """
    Scipy-based feature engineering operations.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize scipy operations.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

    def create_special_function_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using scipy.special functions.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with special function features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col].fillna(X[col].mean())
            col_features = pd.DataFrame(index=X.index)

            # Gamma function
            try:
                col_features[f"{col}_gamma"] = special.gamma(np.clip(series, 0.1, 100))
            except Exception:
                pass

            # Error functions
            try:
                col_features[f"{col}_erf"] = special.erf(series)
                col_features[f"{col}_erfc"] = special.erfc(series)
            except Exception:
                pass

            # Bessel functions
            try:
                col_features[f"{col}_bessel_i0"] = special.i0(np.clip(series, -10, 10))
                col_features[f"{col}_bessel_j0"] = special.j0(series)
            except Exception:
                pass

            # Exponential integrals
            try:
                col_features[f"{col}_exp1"] = special.exp1(np.clip(series, 1e-10, 100))
            except Exception:
                pass

            if not col_features.empty:
                features.append(col_features)

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_distance_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using scipy distance metrics.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with distance features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        features = pd.DataFrame(index=X.index)

        # Distance to mean vector
        mean_vector = X_numeric.mean().values
        for i, row in enumerate(X_numeric.values):
            try:
                # Euclidean distance
                euclidean = np.linalg.norm(row - mean_vector)
                features.loc[X.index[i], "distance_to_mean_euclidean"] = euclidean

                # Manhattan distance
                manhattan: float = float(np.sum(np.abs(row - mean_vector)))
                features.loc[X.index[i], "distance_to_mean_manhattan"] = manhattan

                # Cosine distance
                dot_product = np.dot(row, mean_vector)
                norm_row = np.linalg.norm(row)
                norm_mean = np.linalg.norm(mean_vector)
                if norm_row > 0 and norm_mean > 0:
                    cosine = 1 - (dot_product / (norm_row * norm_mean))
                    features.loc[X.index[i], "distance_to_mean_cosine"] = cosine
            except Exception:
                pass

        return features

    def create_optimization_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using scipy optimization.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with optimization features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = pd.DataFrame(index=X.index)

        # Fit polynomial to each row (if enough columns)
        if len(numeric_cols) >= 3:
            X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean()).values
            x = np.arange(len(numeric_cols))

            for i, row in enumerate(X_numeric):
                try:
                    # Fit polynomial
                    coeffs = np.polyfit(x, row, deg=min(2, len(row) - 1))
                    features.loc[X.index[i], "polyfit_coeff0"] = (
                        coeffs[0] if len(coeffs) > 0 else 0
                    )
                    features.loc[X.index[i], "polyfit_coeff1"] = (
                        coeffs[1] if len(coeffs) > 1 else 0
                    )

                    # Fit exponential
                    def exp_func(x, a, b, c):
                        return a * np.exp(b * x) + c

                    popt, _ = optimize.curve_fit(
                        exp_func, x, row, maxfev=1000, p0=[1, 0.1, 0]
                    )
                    features.loc[X.index[i], "expfit_a"] = popt[0]
                    features.loc[X.index[i], "expfit_b"] = popt[1]
                except Exception:
                    pass

        return features

    def create_signal_processing_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create signal processing features.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with signal processing features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col].dropna().values

            if len(series) < 10:
                continue

            col_features = pd.DataFrame(index=[X.index[0]])

            # FFT features
            try:
                fft = np.fft.fft(series)
                fft_magnitude = np.abs(fft)
                col_features[f"{col}_fft_peak_freq"] = (
                    np.argmax(fft_magnitude[1 : len(series) // 2]) + 1
                )
                col_features[f"{col}_fft_peak_magnitude"] = np.max(fft_magnitude)
            except Exception:
                pass

            # Spectral features
            try:
                freqs, psd = signal.welch(series, nperseg=min(256, len(series)))
                col_features[f"{col}_spectral_centroid"] = np.sum(freqs * psd) / (
                    np.sum(psd) + 1e-10
                )
                col_features[f"{col}_spectral_bandwidth"] = np.sqrt(
                    np.sum(
                        (
                            (freqs - col_features[f"{col}_spectral_centroid"].iloc[0])
                            ** 2
                        )
                        * psd
                    )
                    / (np.sum(psd) + 1e-10)
                )
            except Exception:
                pass

            # Autocorrelation
            try:
                autocorr = signal.correlate(series, series, mode="full")
                autocorr = autocorr[len(autocorr) // 2 :]
                autocorr = autocorr / autocorr[0] if autocorr[0] != 0 else autocorr
                col_features[f"{col}_autocorr_lag1"] = (
                    autocorr[1] if len(autocorr) > 1 else 0
                )
            except Exception:
                pass

            if not col_features.empty:
                features.append(col_features)

        if features:
            result = pd.concat(features, axis=1)
            if len(result) == 1:
                result = result.reindex(X.index, method="ffill")
            return result
        return pd.DataFrame(index=X.index)

    def create_integration_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create features using scipy integration.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with integration features
        """
        from scipy import integrate

        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = pd.DataFrame(index=[X.index[0]])

        for col in numeric_cols:
            series = X[col].dropna().values

            if len(series) < 5:
                continue

            try:
                x = np.arange(len(series))
                # Trapezoidal integration
                integral = integrate.trapz(series, x)
                features[f"{col}_integral"] = integral

                # Simpson's rule
                if len(series) % 2 == 1:  # Simpson requires odd number of points
                    integral_simpson = integrate.simpson(series, x)
                    features[f"{col}_integral_simpson"] = integral_simpson
            except Exception:
                pass

        if len(features) == 1:
            features = features.reindex(X.index, method="ffill")

        return features

    def fit_transform(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Apply all scipy operations.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            DataFrame with all scipy-based features
        """
        all_features = []

        # Special function features
        if self.config.get("special_functions", False):
            special_features = self.create_special_function_features(X)
            if not special_features.empty:
                all_features.append(special_features)

        # Distance features
        if self.config.get("distance_features", True):
            distance_features = self.create_distance_features(X)
            if not distance_features.empty:
                all_features.append(distance_features)

        # Optimization features
        if self.config.get("optimization_features", False):
            opt_features = self.create_optimization_features(X)
            if not opt_features.empty:
                all_features.append(opt_features)

        # Signal processing features
        if self.config.get("signal_features", False):
            signal_features = self.create_signal_processing_features(X)
            if not signal_features.empty:
                all_features.append(signal_features)

        # Integration features
        if self.config.get("integration_features", False):
            int_features = self.create_integration_features(X)
            if not int_features.empty:
                all_features.append(int_features)

        if all_features:
            result = pd.concat(all_features, axis=1)
            result = result.loc[:, ~result.columns.duplicated()]
            return result

        return pd.DataFrame(index=X.index)
