"""
Feature Visualization Engine

Creates visualizations for feature importance, data quality, and lineage.
"""

import pandas as pd
from typing import Dict, Optional, Any
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress Plotly import warnings - it's an optional dependency
warnings.filterwarnings("ignore", message=".*Plotly.*", category=UserWarning)

try:
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Plotly is optional - no warning needed


class FeatureVisualizer:
    """
    Create visualizations for AutoFE-X results.
    """

    def __init__(self, style: str = "seaborn", backend: str = "matplotlib"):
        """
        Initialize feature visualizer.

        Args:
            style: Plot style ('seaborn', 'ggplot', 'classic')
            backend: Visualization backend ('matplotlib', 'plotly')
        """
        self.style = style
        self.backend = backend if PLOTLY_AVAILABLE else "matplotlib"

        if self.backend == "matplotlib":
            plt.style.use(style)
            sns.set_palette("husl")

    def plot_feature_importance(
        self,
        importance_scores: pd.Series,
        top_n: int = 20,
        figsize: tuple = (10, 6),
        save_path: Optional[str] = None,
    ):
        """
        Plot feature importance scores.

        Args:
            importance_scores: Series with feature importance scores
            top_n: Number of top features to show
            figsize: Figure size
            save_path: Path to save figure (optional)
        """
        top_features = importance_scores.nlargest(top_n)

        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=top_features.values,
                        y=top_features.index,
                        orientation="h",
                        marker=dict(color=top_features.values, colorscale="Viridis"),
                    )
                ]
            )
            fig.update_layout(
                title=f"Top {top_n} Feature Importance",
                xaxis_title="Importance Score",
                yaxis_title="Feature",
                height=600,
            )
            if save_path:
                fig.write_html(save_path)
            return fig
        else:
            plt.figure(figsize=figsize)
            top_features.plot(kind="barh")
            plt.title(f"Top {top_n} Feature Importance")
            plt.xlabel("Importance Score")
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")
            else:
                plt.show()

    def plot_data_quality_summary(
        self, quality_report: Dict[str, Any], save_path: Optional[str] = None
    ):
        """
        Create data quality summary visualization.

        Args:
            quality_report: Data quality report from DataProfiler
            save_path: Path to save figure (optional)
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Missing values
        missing = quality_report.get("missing_values", {})
        missing_pct = missing.get("missing_percentages", {})
        if missing_pct:
            missing_df = pd.Series(missing_pct)
            missing_df[missing_df > 0].head(10).plot(
                kind="barh", ax=axes[0, 0], color="coral"
            )
            axes[0, 0].set_title("Top 10 Missing Value Percentages")
            axes[0, 0].set_xlabel("Missing %")

        # Outliers
        outliers = quality_report.get("outliers", {})
        outlier_counts = {
            col: data.get("outlier_count", 0)
            for col, data in outliers.items()
            if isinstance(data, dict)
        }
        if outlier_counts:
            outlier_df = pd.Series(outlier_counts)
            outlier_df[outlier_df > 0].head(10).plot(
                kind="barh", ax=axes[0, 1], color="skyblue"
            )
            axes[0, 1].set_title("Top 10 Outlier Counts")
            axes[0, 1].set_xlabel("Outlier Count")

        # Correlations
        correlations = quality_report.get("correlations", {})
        high_corr = correlations.get("highly_correlated_pairs", [])
        if high_corr:
            corr_df = pd.DataFrame(high_corr)
            if len(corr_df) > 0:
                corr_df["abs_correlation"].head(10).plot(
                    kind="barh", ax=axes[1, 0], color="lightgreen"
                )
                axes[1, 0].set_title("Top Correlated Feature Pairs")
                axes[1, 0].set_xlabel("Correlation")

        # Cardinality
        cardinality = quality_report.get("cardinality", {})
        if cardinality:
            card_df = pd.DataFrame(cardinality).T
            card_df["unique_values"].head(10).plot(
                kind="barh", ax=axes[1, 1], color="plum"
            )
            axes[1, 1].set_title("Top 10 Feature Cardinality")
            axes[1, 1].set_xlabel("Unique Values")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()

    def plot_leakage_risk(
        self, leakage_report: Dict[str, Any], save_path: Optional[str] = None
    ):
        """
        Visualize leakage detection results.

        Args:
            leakage_report: Leakage detection report
            save_path: Path to save figure (optional)
        """
        assessment = leakage_report.get("overall_assessment", {})
        risk_level = assessment.get("risk_level", "unknown")
        risk_score = assessment.get("risk_score", 0)

        # Risk level colors
        risk_colors = {"low": "green", "medium": "orange", "high": "red"}

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Risk score gauge
        axes[0].barh([0], [risk_score], color=risk_colors.get(risk_level, "gray"))
        axes[0].set_xlim(0, 20)
        axes[0].set_title(f"Leakage Risk Score: {risk_score}")
        axes[0].set_xlabel("Risk Score")
        axes[0].text(
            risk_score / 2,
            0,
            risk_level.upper(),
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
        )

        # Risk factors
        risk_factors = assessment.get("risk_factors", [])
        if risk_factors:
            factors_df = pd.DataFrame({"count": [1] * len(risk_factors)})
            axes[1].barh(range(len(risk_factors)), [1] * len(risk_factors))
            axes[1].set_yticks(range(len(risk_factors)))
            axes[1].set_yticklabels(risk_factors, fontsize=8)
            axes[1].set_title("Risk Factors")
            axes[1].set_xlabel("Count")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()

    def plot_feature_lineage_graph(
        self, lineage_graph: Dict[str, Any], save_path: Optional[str] = None
    ):
        """
        Visualize feature lineage as a graph.

        Args:
            lineage_graph: Feature lineage graph from tracker
            save_path: Path to save figure (optional)
        """
        try:
            import networkx as nx

            # Create NetworkX graph
            G = nx.DiGraph()

            nodes = lineage_graph.get("nodes", [])
            edges = lineage_graph.get("edges", [])

            # Add nodes
            for node in nodes:
                node_id = node.get("id")
                node_type = node.get("type", "unknown")
                G.add_node(node_id, node_type=node_type)

            # Add edges
            for edge in edges:
                G.add_edge(edge.get("source"), edge.get("target"))

            # Plot
            plt.figure(figsize=(14, 10))

            # Layout
            pos = nx.spring_layout(G, k=1, iterations=50)

            # Color nodes by type
            node_colors = []
            for node in G.nodes():
                node_type = G.nodes[node].get("node_type", "unknown")
                if node_type == "original":
                    node_colors.append("lightblue")
                elif node_type == "derived":
                    node_colors.append("lightgreen")
                elif node_type == "transformation":
                    node_colors.append("lightcoral")
                else:
                    node_colors.append("gray")

            nx.draw(
                G,
                pos,
                with_labels=True,
                node_color=node_colors,
                node_size=1000,
                font_size=8,
                font_weight="bold",
                arrows=True,
                edge_color="gray",
                alpha=0.7,
            )

            plt.title("Feature Lineage Graph", fontsize=16, fontweight="bold")
            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches="tight")
            else:
                plt.show()

        except ImportError:
            warnings.warn("NetworkX required for lineage graph visualization")
