"""
Benchmarking Module

Auto-benchmarking of feature sets:
- Performance comparison across models
- Feature importance analysis
- Ablation studies
- Cross-validation benchmarking
"""

from .benchmarker import FeatureBenchmarker

__all__ = ["FeatureBenchmarker"]
