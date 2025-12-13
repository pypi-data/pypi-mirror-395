"""
Interactive Dashboard Engine

Creates comprehensive, interactive dashboards that go beyond basic matplotlib/plotly.
Integrates statistical analysis, visualizations, and actionable insights.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
import warnings

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Create a dummy type for type checking when plotly is not available
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from typing import Any as go  # type: ignore
    else:
        go = None  # type: ignore

try:
    import matplotlib.pyplot as plt
    import seaborn as sns

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class InteractiveDashboard:
    """
    Create comprehensive interactive dashboards with integrated analysis.
    Goes beyond basic plotting to provide actionable insights.
    """

    def __init__(self, backend: str = "plotly"):
        """
        Initialize dashboard creator.

        Args:
            backend: Visualization backend ('plotly', 'matplotlib')
        """
        self.backend = backend if PLOTLY_AVAILABLE else "matplotlib"

    def create_comprehensive_dashboard(
        self,
        result: Any,
        save_path: Optional[str] = None,
        title: str = "AutoFE-X Analysis Dashboard",
    ) -> Any:
        """
        Create a comprehensive interactive dashboard with all analysis results.

        Args:
            result: AutoFEXResult object
            save_path: Path to save dashboard (HTML for plotly, PNG for matplotlib)
            title: Dashboard title

        Returns:
            Dashboard object (plotly Figure or matplotlib figure)
        """
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            return self._create_plotly_dashboard(result, save_path, title)
        else:
            return self._create_matplotlib_dashboard(result, save_path, title)

    def _create_plotly_dashboard(
        self, result: Any, save_path: Optional[str], title: str
    ) -> Any:  # type: ignore
        """Create interactive Plotly dashboard."""
        # Create subplots
        fig = make_subplots(
            rows=3,
            cols=2,
            subplot_titles=(
                "Feature Importance",
                "Data Quality Overview",
                "Leakage Risk Analysis",
                "Feature Engineering Impact",
                "Distribution Analysis",
                "Correlation Heatmap",
            ),
            specs=[
                [{"type": "bar"}, {"type": "indicator"}],
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "histogram"}, {"type": "heatmap"}],
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1,
        )

        # 1. Feature Importance
        importance = result.benchmark_results.get("feature_importance")
        if importance is not None and len(importance) > 0:
            top_features = importance.nlargest(15)
            fig.add_trace(
                go.Bar(
                    x=top_features.values,
                    y=top_features.index,
                    orientation="h",
                    name="Importance",
                    marker=dict(
                        color=top_features.values,
                        colorscale="Viridis",
                        showscale=True,
                    ),
                ),
                row=1,
                col=1,
            )

        # 2. Data Quality Indicators
        quality = result.data_quality_report
        missing_pct = (
            (
                quality.get("missing_values", {}).get("total_missing_cells", 0)
                / (
                    quality.get("overview", {}).get("n_rows", 1)
                    * quality.get("overview", {}).get("n_features", 1)
                )
                * 100
            )
            if quality.get("overview")
            else 0
        )

        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=100 - missing_pct,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Data Quality Score"},
                delta={"reference": 90},
                gauge={
                    "axis": {"range": [None, 100]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, 50], "color": "lightgray"},
                        {"range": [50, 80], "color": "gray"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 90,
                    },
                },
            ),
            row=1,
            col=2,
        )

        # 3. Leakage Risk
        leakage = result.leakage_report.get("overall_assessment", {})
        risk_score = leakage.get("risk_score", 0)
        risk_level = leakage.get("risk_level", "unknown")

        risk_colors = {"low": "green", "medium": "orange", "high": "red"}
        fig.add_trace(
            go.Bar(
                x=["Risk Score"],
                y=[risk_score],
                marker=dict(color=risk_colors.get(risk_level, "gray")),
                text=[f"{risk_level.upper()}"],
                textposition="auto",
            ),
            row=2,
            col=1,
        )

        # 4. Feature Engineering Impact
        original_count = result.original_data.shape[1]
        engineered_count = result.engineered_features.shape[1]
        expansion_ratio = engineered_count / original_count if original_count > 0 else 0

        fig.add_trace(
            go.Bar(
                x=["Original", "Engineered"],
                y=[original_count, engineered_count],
                marker=dict(color=["lightblue", "lightgreen"]),
                text=[original_count, engineered_count],
                textposition="auto",
            ),
            row=2,
            col=2,
        )

        # 5. Distribution Analysis
        if len(result.engineered_features.columns) > 0:
            sample_col = result.engineered_features.select_dtypes(
                include=[np.number]
            ).columns[0]
            if sample_col:
                sample_data = result.engineered_features[sample_col].dropna()
                fig.add_trace(
                    go.Histogram(x=sample_data, name="Distribution", nbinsx=30),
                    row=3,
                    col=1,
                )

        # 6. Correlation Heatmap
        numeric_cols = result.engineered_features.select_dtypes(
            include=[np.number]
        ).columns
        if len(numeric_cols) > 1:
            corr_matrix = result.engineered_features[numeric_cols[:10]].corr()
            fig.add_trace(
                go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.index,
                    colorscale="RdBu",
                    zmid=0,
                ),
                row=3,
                col=2,
            )

        # Update layout
        fig.update_layout(
            height=1200,
            title_text=title,
            title_x=0.5,
            showlegend=False,
            template="plotly_white",
        )

        if save_path:
            fig.write_html(save_path)
        else:
            fig.show()

        return fig

    def _create_matplotlib_dashboard(
        self, result: Any, save_path: Optional[str], title: str
    ):
        """Create matplotlib dashboard."""
        if not MATPLOTLIB_AVAILABLE:
            warnings.warn("Matplotlib not available")
            return None

        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # Feature importance
        ax1 = fig.add_subplot(gs[0, :2])
        importance = result.benchmark_results.get("feature_importance")
        if importance is not None and len(importance) > 0:
            top_features = importance.nlargest(15)
            top_features.plot(kind="barh", ax=ax1, color="steelblue")
            ax1.set_title("Top 15 Feature Importance", fontsize=12, fontweight="bold")

        # Data quality gauge
        ax2 = fig.add_subplot(gs[0, 2])
        quality = result.data_quality_report
        missing_pct = (
            (
                quality.get("missing_values", {}).get("total_missing_cells", 0)
                / (
                    quality.get("overview", {}).get("n_rows", 1)
                    * quality.get("overview", {}).get("n_features", 1)
                )
                * 100
            )
            if quality.get("overview")
            else 0
        )
        quality_score = 100 - missing_pct
        ax2.text(
            0.5,
            0.5,
            f"{quality_score:.1f}%",
            ha="center",
            va="center",
            fontsize=24,
            fontweight="bold",
        )
        ax2.set_title("Data Quality Score", fontsize=10)
        ax2.axis("off")

        # Leakage risk
        ax3 = fig.add_subplot(gs[1, 0])
        leakage = result.leakage_report.get("overall_assessment", {})
        risk_score = leakage.get("risk_score", 0)
        risk_level = leakage.get("risk_level", "unknown")
        risk_colors = {"low": "green", "medium": "orange", "high": "red"}
        ax3.barh([0], [risk_score], color=risk_colors.get(risk_level, "gray"))
        ax3.set_title(f"Leakage Risk: {risk_level.upper()}", fontsize=10)
        ax3.set_xlim(0, 20)

        # Feature expansion
        ax4 = fig.add_subplot(gs[1, 1:])
        original_count = result.original_data.shape[1]
        engineered_count = result.engineered_features.shape[1]
        ax4.bar(
            ["Original", "Engineered"],
            [original_count, engineered_count],
            color=["lightblue", "lightgreen"],
        )
        ax4.set_title("Feature Engineering Impact", fontsize=10)
        ax4.set_ylabel("Feature Count")

        # Distribution
        ax5 = fig.add_subplot(gs[2, 0])
        if len(result.engineered_features.columns) > 0:
            sample_col = result.engineered_features.select_dtypes(
                include=[np.number]
            ).columns[0]
            if sample_col:
                result.engineered_features[sample_col].hist(ax=ax5, bins=30)
                ax5.set_title(f"Distribution: {sample_col}", fontsize=9)

        # Correlation heatmap
        ax6 = fig.add_subplot(gs[2, 1:])
        numeric_cols = result.engineered_features.select_dtypes(
            include=[np.number]
        ).columns
        if len(numeric_cols) > 1:
            corr_matrix = result.engineered_features[numeric_cols[:10]].corr()
            sns.heatmap(corr_matrix, annot=False, cmap="coolwarm", center=0, ax=ax6)
            ax6.set_title("Feature Correlation Heatmap", fontsize=10)

        fig.suptitle(title, fontsize=16, fontweight="bold", y=0.98)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        else:
            plt.show()

        return fig

    def create_insights_report(
        self, result: Any, save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate actionable insights and recommendations.

        Args:
            result: AutoFEXResult object
            save_path: Path to save report (JSON or HTML)

        Returns:
            Dictionary with insights and recommendations
        """
        insights: Dict[str, Any] = {
            "summary": {},
            "recommendations": [],
            "warnings": [],
            "opportunities": [],
        }
        # Type annotations for nested structures
        insights_summary: Dict[str, Any] = insights["summary"]  # type: ignore
        insights_recommendations: List[str] = insights["recommendations"]  # type: ignore
        insights_warnings: List[str] = insights["warnings"]  # type: ignore
        insights_opportunities: List[str] = insights["opportunities"]  # type: ignore

        # Data quality insights
        quality = result.data_quality_report
        missing_pct = (
            (
                quality.get("missing_values", {}).get("total_missing_cells", 0)
                / (
                    quality.get("overview", {}).get("n_rows", 1)
                    * quality.get("overview", {}).get("n_features", 1)
                )
                * 100
            )
            if quality.get("overview")
            else 0
        )

        if missing_pct > 10:
            insights_warnings.append(
                f"High missing data: {missing_pct:.1f}%. Consider imputation strategies."
            )
            insights_recommendations.append(
                "Use imputation (KNN, iterative) for missing values"
            )

        # Feature engineering insights
        original_count = result.original_data.shape[1]
        engineered_count = result.engineered_features.shape[1]
        expansion_ratio = engineered_count / original_count if original_count > 0 else 0

        insights_summary["feature_expansion"] = expansion_ratio
        if expansion_ratio > 10:
            insights_opportunities.append(
                f"Large feature expansion ({expansion_ratio:.1f}x). Consider feature selection."
            )
        elif expansion_ratio < 2:
            insights_opportunities.append(
                "Low feature expansion. Consider transformations."
            )

        # Leakage insights
        leakage = result.leakage_report.get("overall_assessment", {})
        risk_level = leakage.get("risk_level", "unknown")
        if risk_level == "high":
            insights_warnings.append(
                "HIGH LEAKAGE RISK detected. Review features before model training."
            )
            insights_recommendations.append(
                "Remove or investigate features flagged in leakage report"
            )

        # Performance insights
        benchmark = result.benchmark_results
        if benchmark.get("best_configurations"):
            best = benchmark["best_configurations"].get("best_overall")
            if best:
                insights_summary["best_model"] = best.get("model")
                insights_summary["best_performance"] = best.get("performance")
                insights_opportunities.append(
                    f"Best model: {best.get('model')} with {best.get('performance', 0):.3f} performance"
                )

        # Save report
        if save_path:
            if save_path.endswith(".html"):
                self._save_html_report(insights, save_path)
            else:
                import json

                with open(save_path, "w") as f:
                    json.dump(insights, f, indent=2, default=str)

        return insights

    def _save_html_report(self, insights: Dict[str, Any], save_path: str):
        """Save insights as HTML report."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AutoFE-X Insights Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
                .warning {{ color: #dc3545; }}
                .opportunity {{ color: #28a745; }}
                .recommendation {{ color: #007bff; }}
                ul {{ line-height: 1.8; }}
            </style>
        </head>
        <body>
            <h1>AutoFE-X Insights Report</h1>
            
            <div class="section">
                <h2>Summary</h2>
                <ul>
                    {''.join([f'<li><strong>{k}:</strong> {v}</li>' for k, v in insights['summary'].items()])}
                </ul>
            </div>
            
            <div class="section">
                <h2 class="warning">Warnings</h2>
                <ul>
                    {''.join([f'<li>{w}</li>' for w in insights['warnings']])}
                </ul>
            </div>
            
            <div class="section">
                <h2 class="opportunity">Opportunities</h2>
                <ul>
                    {''.join([f'<li>{o}</li>' for o in insights['opportunities']])}
                </ul>
            </div>
            
            <div class="section">
                <h2 class="recommendation">Recommendations</h2>
                <ul>
                    {''.join([f'<li>{r}</li>' for r in insights['recommendations']])}
                </ul>
            </div>
        </body>
        </html>
        """
        with open(save_path, "w") as f:
            f.write(html)
