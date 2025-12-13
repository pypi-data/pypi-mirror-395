"""
Multi-Dimensional Visualization

Goes beyond basic Matplotlib and Plotly with:
- 2D: Enhanced scatter, density, contour plots
- 3D: Interactive 3D scatter, surface, volume rendering
- 4D: Color + size encoding, animated 3D
- 5D: Multi-panel linked views, parallel coordinates
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union, Any, Dict
import warnings

# Suppress optional dependency warnings
warnings.filterwarnings("ignore", message=".*Plotly.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*", category=UserWarning)

try:
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    # Matplotlib is optional - no warning needed

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Plotly is optional - no warning needed
    # Create a dummy type for type checking when plotly is not available
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from typing import Any as go  # type: ignore
    else:
        go = None  # type: ignore

try:
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn(
        "Scikit-learn not available. Dimensionality reduction will be limited."
    )


class MultiDimensionalVisualizer:
    """
    Multi-dimensional visualization (2D, 3D, 4D, 5D)
    that goes beyond basic Matplotlib and Plotly.
    """

    def __init__(self, backend: str = "plotly"):
        """
        Initialize multi-dimensional visualizer.

        Args:
            backend: Visualization backend ('plotly', 'matplotlib')
        """
        self.backend = backend if PLOTLY_AVAILABLE else "matplotlib"

    def plot_2d(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        color: Optional[Union[pd.Series, np.ndarray]] = None,
        size: Optional[Union[pd.Series, np.ndarray]] = None,
        title: str = "2D Plot",
        save_path: Optional[str] = None,
    ) -> Any:
        """
        2D visualization with density, contours, and encoding.

        Args:
            x: X-axis data
            y: Y-axis data
            color: Color encoding (optional)
            size: Size encoding (optional)
            title: Plot title
            save_path: Path to save figure

        Returns:
            Figure object
        """
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            return self._plot_2d_plotly(x, y, color, size, title, save_path)
        else:
            return self._plot_2d_matplotlib(x, y, color, size, title, save_path)

    def _plot_2d_plotly(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        color: Optional[Union[pd.Series, np.ndarray]],
        size: Optional[Union[pd.Series, np.ndarray]],
        title: str,
        save_path: Optional[str],
    ) -> Any:  # type: ignore
        """Create 2D plot with Plotly."""
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Scatter Plot",
                "Density Contour",
                "Hexbin",
                "Marginal Distributions",
            ),
            specs=[
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}],
            ],
        )

        # Scatter plot
        scatter_kwargs: Dict[str, Any] = {
            "x": x,
            "y": y,
            "mode": "markers",
            "name": "Data",
        }
        marker_dict: Dict[str, Any] = {}  # type: ignore
        if color is not None:
            marker_dict = {
                "color": color,
                "colorscale": "Viridis",
                "showscale": True,
            }
        if size is not None:
            if not marker_dict:
                marker_dict = {}
            marker_dict["size"] = (size - size.min()) / (
                size.max() - size.min()
            ) * 20 + 5
        if marker_dict:
            scatter_kwargs["marker"] = marker_dict

        fig.add_trace(go.Scatter(**scatter_kwargs), row=1, col=1)

        # Density contour
        fig.add_trace(
            go.Histogram2dContour(x=x, y=y, colorscale="Blues", showscale=True),
            row=1,
            col=2,
        )

        # Hexbin (2D histogram)
        fig.add_trace(
            go.Histogram2d(x=x, y=y, colorscale="YlOrRd", showscale=True),
            row=2,
            col=1,
        )

        # Marginal distributions
        fig.add_trace(go.Histogram(x=x, name="X distribution"), row=2, col=2)
        fig.add_trace(
            go.Histogram(y=y, name="Y distribution", orientation="h"), row=2, col=2
        )

        fig.update_layout(height=800, title_text=title, showlegend=False)

        if save_path:
            fig.write_html(save_path)
        else:
            fig.show()

        return fig

    def _plot_2d_matplotlib(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        color: Optional[Union[pd.Series, np.ndarray]],
        size: Optional[Union[pd.Series, np.ndarray]],
        title: str,
        save_path: Optional[str],
    ):
        """Create 2D plot with Matplotlib."""
        if not MATPLOTLIB_AVAILABLE:
            return None

        fig, axes = plt.subplots(2, 2, figsize=(14, 12))

        # Scatter plot
        scatter = axes[0, 0].scatter(
            x, y, c=color, s=size if size is not None else 50, cmap="viridis", alpha=0.6
        )
        axes[0, 0].set_xlabel("X")
        axes[0, 0].set_ylabel("Y")
        axes[0, 0].set_title("Scatter Plot")
        if color is not None:
            plt.colorbar(scatter, ax=axes[0, 0])

        # Density contour
        axes[0, 1].hist2d(x, y, bins=30, cmap="Blues")
        axes[0, 1].set_xlabel("X")
        axes[0, 1].set_ylabel("Y")
        axes[0, 1].set_title("Density Contour")

        # Hexbin
        axes[1, 0].hexbin(x, y, gridsize=20, cmap="YlOrRd")
        axes[1, 0].set_xlabel("X")
        axes[1, 0].set_ylabel("Y")
        axes[1, 0].set_title("Hexbin")

        # Marginal distributions
        axes[1, 1].hist(x, bins=30, alpha=0.5, label="X", orientation="vertical")
        axes[1, 1].hist(y, bins=30, alpha=0.5, label="Y", orientation="horizontal")
        axes[1, 1].set_title("Marginal Distributions")
        axes[1, 1].legend()

        fig.suptitle(title, fontsize=16, fontweight="bold")

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()

        return fig

    def plot_3d(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        z: Union[pd.Series, np.ndarray],
        color: Optional[Union[pd.Series, np.ndarray]] = None,
        size: Optional[Union[pd.Series, np.ndarray]] = None,
        title: str = "3D Plot",
        save_path: Optional[str] = None,
    ) -> Any:
        """
        3D visualization with interactive controls.

        Args:
            x: X-axis data
            y: Y-axis data
            z: Z-axis data
            color: Color encoding (optional)
            size: Size encoding (optional)
            title: Plot title
            save_path: Path to save figure

        Returns:
            Figure object
        """
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            return self._plot_3d_plotly(x, y, z, color, size, title, save_path)
        else:
            return self._plot_3d_matplotlib(x, y, z, color, size, title, save_path)

    def _plot_3d_plotly(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        z: Union[pd.Series, np.ndarray],
        color: Optional[Union[pd.Series, np.ndarray]],
        size: Optional[Union[pd.Series, np.ndarray]],
        title: str,
        save_path: Optional[str],
    ) -> Any:  # type: ignore
        """Create 3D plot with Plotly."""
        fig = go.Figure()

        # 3D scatter
        scatter_kwargs: Dict[str, Any] = {
            "x": x,
            "y": y,
            "z": z,
            "mode": "markers",
            "name": "3D Data",
            "marker": {},
        }
        marker_dict: Dict[str, Any] = scatter_kwargs["marker"]  # type: ignore

        if color is not None:
            marker_dict["color"] = color
            marker_dict["colorscale"] = "Viridis"
            marker_dict["showscale"] = True

        if size is not None:
            marker_dict["size"] = (size - size.min()) / (
                size.max() - size.min()
            ) * 20 + 5
        else:
            marker_dict["size"] = 5

        fig.add_trace(go.Scatter3d(**scatter_kwargs))

        # Add surface if possible
        if len(x) > 10:
            try:
                from scipy.interpolate import griddata

                xi = np.linspace(x.min(), x.max(), 20)
                yi = np.linspace(y.min(), y.max(), 20)
                xi, yi = np.meshgrid(xi, yi)
                zi = griddata((x, y), z, (xi, yi), method="cubic")

                fig.add_trace(
                    go.Surface(
                        x=xi,
                        y=yi,
                        z=zi,
                        colorscale="Blues",
                        showscale=False,
                        opacity=0.5,
                    )
                )
            except Exception:
                pass

        fig.update_layout(
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
            ),
            title=title,
            height=800,
        )

        if save_path:
            fig.write_html(save_path)
        else:
            fig.show()

        return fig

    def _plot_3d_matplotlib(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        z: Union[pd.Series, np.ndarray],
        color: Optional[Union[pd.Series, np.ndarray]],
        size: Optional[Union[pd.Series, np.ndarray]],
        title: str,
        save_path: Optional[str],
    ):
        """Create 3D plot with Matplotlib."""
        if not MATPLOTLIB_AVAILABLE:
            return None

        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection="3d")

        scatter = ax.scatter(
            x,
            y,
            z,
            c=color,
            s=size if size is not None else 50,
            cmap="viridis",
            alpha=0.6,
        )
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(title)

        if color is not None:
            plt.colorbar(scatter, ax=ax)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()

        return fig

    def plot_4d(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        z: Union[pd.Series, np.ndarray],
        color: Union[pd.Series, np.ndarray],
        size: Optional[Union[pd.Series, np.ndarray]] = None,
        title: str = "4D Plot",
        save_path: Optional[str] = None,
    ) -> Any:
        """
        4D visualization (3D + color encoding).

        Args:
            x: X-axis data
            y: Y-axis data
            z: Z-axis data
            color: Color encoding (4th dimension)
            size: Size encoding (optional, 5th dimension)
            title: Plot title
            save_path: Path to save figure

        Returns:
            Figure object
        """
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            return self._plot_4d_plotly(x, y, z, color, size, title, save_path)
        else:
            return self._plot_4d_matplotlib(x, y, z, color, size, title, save_path)

    def _plot_4d_plotly(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        z: Union[pd.Series, np.ndarray],
        color: Union[pd.Series, np.ndarray],
        size: Optional[Union[pd.Series, np.ndarray]],
        title: str,
        save_path: Optional[str],
    ) -> Any:  # type: ignore
        """Create 4D plot with Plotly."""
        fig = go.Figure()

        scatter_kwargs: Dict[str, Any] = {
            "x": x,
            "y": y,
            "z": z,
            "mode": "markers",
            "marker": {
                "color": color,
                "colorscale": "Viridis",
                "showscale": True,
                "colorbar": dict(title="4th Dimension"),
            },
        }
        marker_dict: Dict[str, Any] = scatter_kwargs["marker"]  # type: ignore

        if size is not None:
            marker_dict["size"] = (size - size.min()) / (
                size.max() - size.min()
            ) * 20 + 5
        else:
            marker_dict["size"] = 8

        fig.add_trace(go.Scatter3d(**scatter_kwargs))

        fig.update_layout(
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
            ),
            title=title,
            height=800,
        )

        if save_path:
            fig.write_html(save_path)
        else:
            fig.show()

        return fig

    def _plot_4d_matplotlib(
        self,
        x: Union[pd.Series, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        z: Union[pd.Series, np.ndarray],
        color: Union[pd.Series, np.ndarray],
        size: Optional[Union[pd.Series, np.ndarray]],
        title: str,
        save_path: Optional[str],
    ):
        """Create 4D plot with Matplotlib."""
        if not MATPLOTLIB_AVAILABLE:
            return None

        fig = plt.figure(figsize=(14, 6))

        # 3D scatter with color
        ax1 = fig.add_subplot(121, projection="3d")
        scatter1 = ax1.scatter(
            x,
            y,
            z,
            c=color,
            s=size if size is not None else 50,
            cmap="viridis",
            alpha=0.6,
        )
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")
        ax1.set_title("4D: 3D + Color")
        plt.colorbar(scatter1, ax=ax1, label="4th Dimension")

        # 2D projection with color
        ax2 = fig.add_subplot(122)
        scatter2 = ax2.scatter(
            x, y, c=color, s=size if size is not None else 50, cmap="viridis", alpha=0.6
        )
        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        ax2.set_title("2D Projection with Color")
        plt.colorbar(scatter2, ax=ax2, label="4th Dimension")

        fig.suptitle(title, fontsize=16, fontweight="bold")

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()

        return fig

    def plot_5d(
        self,
        data: pd.DataFrame,
        dims: List[str],
        color_col: Optional[str] = None,
        size_col: Optional[str] = None,
        title: str = "5D Plot",
        save_path: Optional[str] = None,
    ) -> Any:
        """
        5D visualization using multiple encoding methods.

        Args:
            data: DataFrame with all dimensions
            dims: List of column names for dimensions (must be 5)
            color_col: Column name for color encoding
            size_col: Column name for size encoding
            title: Plot title
            save_path: Path to save figure

        Returns:
            Figure object
        """
        if len(dims) < 5:
            raise ValueError("Need at least 5 dimensions for 5D plot")

        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            return self._plot_5d_plotly(
                data, dims, color_col, size_col, title, save_path
            )
        else:
            return self._plot_5d_matplotlib(
                data, dims, color_col, size_col, title, save_path
            )

    def _plot_5d_plotly(
        self,
        data: pd.DataFrame,
        dims: List[str],
        color_col: Optional[str],
        size_col: Optional[str],
        title: str,
        save_path: Optional[str],
    ) -> Any:  # type: ignore
        """Create 5D plot with Plotly."""
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "3D Scatter (XYZ)",
                "Parallel Coordinates",
                "PCA 2D",
                "t-SNE 2D",
            ),
            specs=[
                [{"type": "scatter3d"}, {"type": "parcoords"}],
                [{"type": "scatter"}, {"type": "scatter"}],
            ],
        )

        x, y, z = data[dims[0]], data[dims[1]], data[dims[2]]

        # 3D scatter
        scatter_kwargs: Dict[str, Any] = {
            "x": x,
            "y": y,
            "z": z,
            "mode": "markers",
            "marker": {},
        }
        marker_dict: Dict[str, Any] = scatter_kwargs["marker"]  # type: ignore

        if color_col:
            marker_dict["color"] = data[color_col]
            marker_dict["colorscale"] = "Viridis"
            marker_dict["showscale"] = True

        if size_col:
            size_norm = (data[size_col] - data[size_col].min()) / (
                data[size_col].max() - data[size_col].min()
            )
            marker_dict["size"] = size_norm * 20 + 5

        fig.add_trace(go.Scatter3d(**scatter_kwargs), row=1, col=1)

        # Parallel coordinates
        if SKLEARN_AVAILABLE and len(dims) >= 5:
            fig.add_trace(
                go.Parcoords(
                    line=dict(
                        color=data[color_col] if color_col else "blue",
                        colorscale="Viridis",
                    ),
                    dimensions=[dict(label=dim, values=data[dim]) for dim in dims[:5]],
                ),
                row=1,
                col=2,
            )

        # PCA 2D
        if SKLEARN_AVAILABLE:
            try:
                pca = PCA(n_components=2)
                pca_data = data[dims[:5]].dropna()
                pca_result = pca.fit_transform(pca_data)

                fig.add_trace(
                    go.Scatter(
                        x=pca_result[:, 0],
                        y=pca_result[:, 1],
                        mode="markers",
                        marker=dict(
                            color=(
                                data.loc[pca_data.index, color_col]
                                if color_col
                                else "blue"
                            ),
                            colorscale="Viridis",
                            showscale=bool(color_col),
                        ),
                        name="PCA",
                    ),
                    row=2,
                    col=1,
                )
            except Exception:
                pass

        # t-SNE 2D
        if SKLEARN_AVAILABLE and len(data) < 1000:  # t-SNE is slow for large data
            try:
                tsne = TSNE(n_components=2, random_state=42)
                tsne_data = data[dims[:5]].dropna()
                tsne_result = tsne.fit_transform(tsne_data)

                fig.add_trace(
                    go.Scatter(
                        x=tsne_result[:, 0],
                        y=tsne_result[:, 1],
                        mode="markers",
                        marker=dict(
                            color=(
                                data.loc[tsne_data.index, color_col]
                                if color_col
                                else "blue"
                            ),
                            colorscale="Viridis",
                            showscale=bool(color_col),
                        ),
                        name="t-SNE",
                    ),
                    row=2,
                    col=2,
                )
            except Exception:
                pass

        fig.update_layout(height=1000, title_text=title, showlegend=False)

        if save_path:
            fig.write_html(save_path)
        else:
            fig.show()

        return fig

    def _plot_5d_matplotlib(
        self,
        data: pd.DataFrame,
        dims: List[str],
        color_col: Optional[str],
        size_col: Optional[str],
        title: str,
        save_path: Optional[str],
    ):
        """Create 5D plot with Matplotlib."""
        if not MATPLOTLIB_AVAILABLE:
            return None

        fig = plt.figure(figsize=(16, 12))

        # 3D scatter
        ax1 = fig.add_subplot(221, projection="3d")
        x, y, z = data[dims[0]], data[dims[1]], data[dims[2]]
        scatter1 = ax1.scatter(
            x,
            y,
            z,
            c=data[color_col] if color_col else "blue",
            s=data[size_col] * 10 if size_col else 50,
            cmap="viridis",
            alpha=0.6,
        )
        ax1.set_xlabel(dims[0])
        ax1.set_ylabel(dims[1])
        ax1.set_zlabel(dims[2])
        ax1.set_title("3D Scatter (XYZ)")
        if color_col:
            plt.colorbar(scatter1, ax=ax1)

        # Pair plot
        ax2 = fig.add_subplot(222)
        if len(dims) >= 4:
            ax2.scatter(
                data[dims[0]],
                data[dims[3]],
                c=data[color_col] if color_col else "blue",
                s=data[size_col] * 10 if size_col else 50,
                cmap="viridis",
                alpha=0.6,
            )
            ax2.set_xlabel(dims[0])
            ax2.set_ylabel(dims[3])
            ax2.set_title("Dimension 1 vs 4")

        # PCA
        if SKLEARN_AVAILABLE:
            try:
                ax3 = fig.add_subplot(223)
                pca = PCA(n_components=2)
                pca_data = data[dims[:5]].dropna()
                pca_result = pca.fit_transform(pca_data)
                scatter3 = ax3.scatter(
                    pca_result[:, 0],
                    pca_result[:, 1],
                    c=data.loc[pca_data.index, color_col] if color_col else "blue",
                    cmap="viridis",
                    alpha=0.6,
                )
                ax3.set_xlabel("PC1")
                ax3.set_ylabel("PC2")
                ax3.set_title("PCA 2D")
                if color_col:
                    plt.colorbar(scatter3, ax=ax3)
            except Exception:
                pass

        # Correlation heatmap
        ax4 = fig.add_subplot(224)
        corr_matrix = data[dims[:5]].corr()
        im = ax4.imshow(corr_matrix, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)
        ax4.set_xticks(range(len(dims[:5])))
        ax4.set_yticks(range(len(dims[:5])))
        ax4.set_xticklabels(dims[:5], rotation=45)
        ax4.set_yticklabels(dims[:5])
        ax4.set_title("Correlation Matrix")
        plt.colorbar(im, ax=ax4)

        fig.suptitle(title, fontsize=16, fontweight="bold")

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()

        return fig
