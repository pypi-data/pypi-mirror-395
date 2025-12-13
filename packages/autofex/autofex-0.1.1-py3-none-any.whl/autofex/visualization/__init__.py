"""
Visualization Module

Visualization capabilities for:
- Feature importance plots
- Data quality dashboards
- Leakage detection visualizations
- Feature lineage graphs
- Interactive dashboards
- Multi-dimensional visualizations (2D, 3D, 4D, 5D)
"""

from .plotter import FeatureVisualizer

try:
    from .dashboard import InteractiveDashboard

    _DASHBOARD_AVAILABLE = True
except ImportError:
    _DASHBOARD_AVAILABLE = False
    InteractiveDashboard = None  # type: ignore

try:
    from .multidimensional import MultiDimensionalVisualizer

    _MULTIDIM_AVAILABLE = True
except ImportError:
    _MULTIDIM_AVAILABLE = False
    MultiDimensionalVisualizer = None  # type: ignore

__all__ = ["FeatureVisualizer"]

if _DASHBOARD_AVAILABLE:
    __all__.append("InteractiveDashboard")

if _MULTIDIM_AVAILABLE:
    __all__.append("MultiDimensionalVisualizer")
