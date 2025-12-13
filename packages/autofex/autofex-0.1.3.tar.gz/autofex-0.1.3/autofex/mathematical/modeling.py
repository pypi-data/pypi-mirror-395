"""
Mathematical Modeling Features

Leverages numpy, pandas, scipy, and scikit-learn for mathematical
transformations and modeling-based feature engineering.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
from scipy import stats, optimize, signal
from scipy.interpolate import interp1d, splrep, splev
from sklearn.decomposition import PCA, FastICA, FactorAnalysis
from sklearn.manifold import TSNE, MDS, Isomap
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer
from sklearn.cluster import KMeans, DBSCAN
import warnings


class MathematicalModelingEngine:
    """
    Mathematical modeling for feature engineering using
    numpy, pandas, scipy, and scikit-learn.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize mathematical modeling engine.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.n_components_pca = self.config.get("n_components_pca", 5)
        self.n_components_ica = self.config.get("n_components_ica", 5)
        self.n_clusters = self.config.get("n_clusters", 5)
        self.polynomial_degree = self.config.get("polynomial_degree", 3)
        self.spline_degree = self.config.get("spline_degree", 3)
        self.n_knots = self.config.get("n_knots", 5)

    def create_polynomial_features(
        self, X: pd.DataFrame, degree: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Create polynomial features using scikit-learn.

        Args:
            X: Input DataFrame
            degree: Polynomial degree (default: from config)

        Returns:
            DataFrame with polynomial features
        """
        degree = degree or self.polynomial_degree
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        poly = PolynomialFeatures(
            degree=degree,
            include_bias=False,
            interaction_only=False,
        )

        poly_features = poly.fit_transform(X_numeric)
        feature_names = poly.get_feature_names_out(numeric_cols)

        return pd.DataFrame(
            poly_features,
            columns=feature_names,
            index=X.index,
        )

    def create_spline_features(
        self, X: pd.DataFrame, n_knots: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Create spline features using scikit-learn.

        Args:
            X: Input DataFrame
            n_knots: Number of knots (default: from config)

        Returns:
            DataFrame with spline features
        """
        n_knots = n_knots or self.n_knots
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        spline = SplineTransformer(
            n_knots=n_knots,
            degree=self.spline_degree,
            include_bias=False,
        )

        spline_features = spline.fit_transform(X_numeric)
        feature_names = [
            f"{col}_spline_{i}"
            for col in numeric_cols
            for i in range(spline_features.shape[1] // len(numeric_cols))
        ]

        return pd.DataFrame(
            spline_features,
            columns=feature_names[: spline_features.shape[1]],
            index=X.index,
        )

    def create_pca_features(
        self, X: pd.DataFrame, n_components: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Create PCA features for dimensionality reduction.

        Args:
            X: Input DataFrame
            n_components: Number of components (default: from config)

        Returns:
            DataFrame with PCA features
        """
        n_components = n_components or self.n_components_pca
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        # Standardize before PCA
        X_std = (X_numeric - X_numeric.mean()) / (X_numeric.std() + 1e-8)

        n_components = min(n_components, X_std.shape[1], X_std.shape[0])

        pca = PCA(n_components=n_components)
        pca_features = pca.fit_transform(X_std)

        return pd.DataFrame(
            pca_features,
            columns=[f"pca_{i+1}" for i in range(n_components)],
            index=X.index,
        )

    def create_ica_features(
        self, X: pd.DataFrame, n_components: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Create Independent Component Analysis (ICA) features.

        Args:
            X: Input DataFrame
            n_components: Number of components (default: from config)

        Returns:
            DataFrame with ICA features
        """
        n_components = n_components or self.n_components_ica
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        # Standardize before ICA
        X_std = (X_numeric - X_numeric.mean()) / (X_numeric.std() + 1e-8)

        n_components = min(n_components, X_std.shape[1], X_std.shape[0])

        ica = FastICA(n_components=n_components, random_state=42, max_iter=1000)
        ica_features = ica.fit_transform(X_std)

        return pd.DataFrame(
            ica_features,
            columns=[f"ica_{i+1}" for i in range(n_components)],
            index=X.index,
        )

    def create_factor_analysis_features(
        self, X: pd.DataFrame, n_components: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Create Factor Analysis features.

        Args:
            X: Input DataFrame
            n_components: Number of factors (default: from config)

        Returns:
            DataFrame with factor analysis features
        """
        n_components = n_components or self.n_components_pca
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        # Standardize
        X_std = (X_numeric - X_numeric.mean()) / (X_numeric.std() + 1e-8)

        n_components = min(n_components, X_std.shape[1], X_std.shape[0])

        fa = FactorAnalysis(n_components=n_components, random_state=42)
        fa_features = fa.fit_transform(X_std)

        return pd.DataFrame(
            fa_features,
            columns=[f"factor_{i+1}" for i in range(n_components)],
            index=X.index,
        )

    def create_cluster_features(
        self, X: pd.DataFrame, n_clusters: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Create cluster-based features using KMeans.

        Args:
            X: Input DataFrame
            n_clusters: Number of clusters (default: from config)

        Returns:
            DataFrame with cluster features
        """
        n_clusters = n_clusters or self.n_clusters
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        # Standardize
        X_std = (X_numeric - X_numeric.mean()) / (X_numeric.std() + 1e-8)

        n_clusters = min(n_clusters, len(X))

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_std)

        # Distance to cluster centers
        distances = kmeans.transform(X_std)

        features = pd.DataFrame(
            {
                "cluster_label": cluster_labels,
            },
            index=X.index,
        )

        # Add distances to each cluster center
        for i in range(n_clusters):
            features[f"distance_to_cluster_{i}"] = distances[:, i]

        return features

    def create_manifold_features(
        self, X: pd.DataFrame, method: str = "tsne", n_components: int = 2
    ) -> pd.DataFrame:
        """
        Create manifold learning features (t-SNE, MDS, Isomap).

        Args:
            X: Input DataFrame
            method: Method ('tsne', 'mds', 'isomap')
            n_components: Number of components

        Returns:
            DataFrame with manifold features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        X_numeric = X[numeric_cols].fillna(X[numeric_cols].mean())

        # Standardize
        X_std = (X_numeric - X_numeric.mean()) / (X_numeric.std() + 1e-8)

        # Limit sample size for t-SNE (it's slow)
        max_samples = 1000 if method == "tsne" else len(X_std)
        if len(X_std) > max_samples:
            X_std = X_std.sample(n=max_samples, random_state=42)
            indices = X_std.index
        else:
            indices = X_std.index

        if method == "tsne":
            manifold = TSNE(n_components=n_components, random_state=42, perplexity=30)
        elif method == "mds":
            manifold = MDS(n_components=n_components, random_state=42)
        elif method == "isomap":
            manifold = Isomap(n_components=n_components, n_neighbors=10)
        else:
            raise ValueError(f"Unknown method: {method}")

        manifold_features = manifold.fit_transform(X_std)

        # Create full DataFrame (fill missing with NaN if subsampled)
        if len(indices) < len(X):
            full_features = np.full((len(X), n_components), np.nan)
            full_features[X.index.get_indexer(indices)] = manifold_features
        else:
            full_features = manifold_features

        return pd.DataFrame(
            full_features,
            columns=[f"{method}_{i+1}" for i in range(n_components)],
            index=X.index,
        )

    def create_interpolation_features(
        self, X: pd.DataFrame, method: str = "linear"
    ) -> pd.DataFrame:
        """
        Create interpolation-based features using scipy.

        Args:
            X: Input DataFrame
            method: Interpolation method ('linear', 'cubic', 'spline')

        Returns:
            DataFrame with interpolation features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col].dropna()

            if len(series) < 4:
                continue

            x_old = np.arange(len(series))
            y_old = series.values

            # Create new x points (more dense)
            x_new = np.linspace(0, len(series) - 1, len(series) * 2)

            try:
                if method == "linear":
                    interp_func = interp1d(
                        x_old, y_old, kind="linear", fill_value="extrapolate"
                    )
                elif method == "cubic":
                    interp_func = interp1d(
                        x_old, y_old, kind="cubic", fill_value="extrapolate"
                    )
                elif method == "spline":
                    tck = splrep(x_old, y_old, s=0)
                    y_new = splev(x_new, tck)
                    features.append(
                        pd.DataFrame(
                            {
                                f"{col}_spline_interp": np.interp(
                                    np.arange(len(X)), x_new, y_new
                                )
                            },
                            index=X.index,
                        )
                    )
                    continue
                else:
                    continue

                y_new = interp_func(x_new)

                # Map back to original index length
                interp_values = np.interp(np.arange(len(X)), x_new, y_new)

                features.append(
                    pd.DataFrame(
                        {f"{col}_{method}_interp": interp_values},
                        index=X.index,
                    )
                )
            except Exception as e:
                warnings.warn(f"Interpolation failed for {col}: {e}")
                continue

        if features:
            return pd.concat(features, axis=1)
        return pd.DataFrame(index=X.index)

    def create_signal_processing_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create signal processing features using scipy.signal.

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

            # FFT features
            try:
                fft_values = np.fft.fft(series)
                fft_magnitude = np.abs(fft_values)
                features.append(
                    pd.DataFrame(
                        {
                            f"{col}_fft_magnitude_mean": [np.mean(fft_magnitude)],
                            f"{col}_fft_magnitude_std": [np.std(fft_magnitude)],
                            f"{col}_fft_magnitude_max": [np.max(fft_magnitude)],
                        },
                        index=[X.index[0]],
                    )
                )
            except Exception:
                pass

            # Spectral features
            try:
                freqs, psd = signal.welch(series, nperseg=min(256, len(series)))
                features.append(
                    pd.DataFrame(
                        {
                            f"{col}_spectral_centroid": [
                                np.sum(freqs * psd) / np.sum(psd)
                            ],
                            f"{col}_spectral_rolloff": [
                                (
                                    freqs[
                                        np.where(np.cumsum(psd) >= 0.85 * np.sum(psd))[
                                            0
                                        ][0]
                                    ]
                                    if len(
                                        np.where(np.cumsum(psd) >= 0.85 * np.sum(psd))[
                                            0
                                        ]
                                    )
                                    > 0
                                    else 0
                                )
                            ],
                        },
                        index=[X.index[0]],
                    )
                )
            except Exception:
                pass

            # Autocorrelation
            try:
                autocorr = np.correlate(series, series, mode="full")
                autocorr = autocorr[len(autocorr) // 2 :]
                autocorr = autocorr / autocorr[0] if autocorr[0] != 0 else autocorr

                features.append(
                    pd.DataFrame(
                        {
                            f"{col}_autocorr_lag1": [
                                autocorr[1] if len(autocorr) > 1 else 0
                            ],
                            f"{col}_autocorr_lag5": [
                                autocorr[5] if len(autocorr) > 5 else 0
                            ],
                        },
                        index=[X.index[0]],
                    )
                )
            except Exception:
                pass

        if features:
            # Expand single-row features to full length
            result = pd.concat(features, axis=1)
            if len(result) == 1:
                result = result.reindex(X.index, method="ffill")
            return result
        return pd.DataFrame(index=X.index)

    def create_distribution_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create distribution-based features using scipy.stats.

        Args:
            X: Input DataFrame

        Returns:
            DataFrame with distribution features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col].dropna()

            if len(series) < 3:
                continue

            dist_features = {}

            # Fit various distributions
            distributions = [
                ("norm", stats.norm),
                ("expon", stats.expon),
                ("gamma", stats.gamma),
                ("beta", stats.beta),
            ]

            for dist_name, dist in distributions:
                try:
                    params = dist.fit(series)
                    # Calculate log-likelihood
                    log_likelihood: float = float(np.sum(dist.logpdf(series, *params)))
                    dist_features[f"{col}_{dist_name}_loglik"] = log_likelihood

                    # AIC (Akaike Information Criterion)
                    n_params = len(params)
                    aic = 2 * n_params - 2 * log_likelihood
                    dist_features[f"{col}_{dist_name}_aic"] = aic
                except Exception:
                    pass

            # Moments
            dist_features[f"{col}_skewness"] = stats.skew(series)
            dist_features[f"{col}_kurtosis"] = stats.kurtosis(series)

            # Entropy
            try:
                hist, _ = np.histogram(series, bins=min(50, len(series.unique())))
                hist = hist / hist.sum() if hist.sum() > 0 else hist
                entropy: float = float(-np.sum(hist * np.log(hist + 1e-10)))
                dist_features[f"{col}_entropy"] = entropy
            except Exception:
                pass

            if dist_features:
                features.append(pd.DataFrame(dist_features, index=[X.index[0]]))

        if features:
            result = pd.concat(features, axis=1)
            if len(result) == 1:
                result = result.reindex(X.index, method="ffill")
            return result
        return pd.DataFrame(index=X.index)

    def create_optimization_features(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Create optimization-based features using scipy.optimize.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            DataFrame with optimization features
        """
        numeric_cols = X.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame(index=X.index)

        features = []

        for col in numeric_cols:
            series = X[col].dropna().values

            if len(series) < 5:
                continue

            opt_features = {}

            # Fit polynomial to data
            try:
                x = np.arange(len(series))
                coeffs = np.polyfit(x, series, deg=min(3, len(series) - 1))
                opt_features[f"{col}_polyfit_coeff0"] = (
                    coeffs[0] if len(coeffs) > 0 else 0
                )
                opt_features[f"{col}_polyfit_coeff1"] = (
                    coeffs[1] if len(coeffs) > 1 else 0
                )
            except Exception:
                pass

            # Curve fitting (exponential)
            if y is not None and len(series) == len(y):
                try:

                    def exp_func(x, a, b, c):
                        return a * np.exp(b * x) + c

                    popt, _ = optimize.curve_fit(
                        exp_func,
                        np.arange(len(series)),
                        series,
                        maxfev=1000,
                    )
                    opt_features[f"{col}_expfit_a"] = popt[0]
                    opt_features[f"{col}_expfit_b"] = popt[1]
                except Exception:
                    pass

            if opt_features:
                features.append(pd.DataFrame(opt_features, index=[X.index[0]]))

        if features:
            result = pd.concat(features, axis=1)
            if len(result) == 1:
                result = result.reindex(X.index, method="ffill")
            return result
        return pd.DataFrame(index=X.index)

    def fit_transform(
        self, X: pd.DataFrame, y: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Apply all mathematical modeling transformations.

        Args:
            X: Input DataFrame
            y: Target variable (optional)

        Returns:
            DataFrame with all mathematical modeling features
        """
        all_features = []

        # Polynomial features
        if self.config.get("polynomial_features", True):
            poly_features = self.create_polynomial_features(X)
            if not poly_features.empty:
                all_features.append(poly_features)

        # Spline features
        if self.config.get("spline_features", True):
            spline_features = self.create_spline_features(X)
            if not spline_features.empty:
                all_features.append(spline_features)

        # PCA features
        if self.config.get("pca_features", True):
            pca_features = self.create_pca_features(X)
            if not pca_features.empty:
                all_features.append(pca_features)

        # ICA features
        if self.config.get("ica_features", False):
            ica_features = self.create_ica_features(X)
            if not ica_features.empty:
                all_features.append(ica_features)

        # Cluster features
        if self.config.get("cluster_features", True):
            cluster_features = self.create_cluster_features(X)
            if not cluster_features.empty:
                all_features.append(cluster_features)

        # Distribution features
        if self.config.get("distribution_features", True):
            dist_features = self.create_distribution_features(X)
            if not dist_features.empty:
                all_features.append(dist_features)

        # Signal processing features
        if self.config.get("signal_features", False):
            signal_features = self.create_signal_processing_features(X)
            if not signal_features.empty:
                all_features.append(signal_features)

        # Optimization features
        if self.config.get("optimization_features", False):
            opt_features = self.create_optimization_features(X, y)
            if not opt_features.empty:
                all_features.append(opt_features)

        if all_features:
            result = pd.concat(all_features, axis=1)
            # Remove duplicate columns
            result = result.loc[:, ~result.columns.duplicated()]
            return result

        return pd.DataFrame(index=X.index)
