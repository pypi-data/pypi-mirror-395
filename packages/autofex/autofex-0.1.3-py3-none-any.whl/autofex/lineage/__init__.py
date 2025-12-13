"""
Feature Lineage Module

Graph-based feature lineage tracking:
- Track feature transformations
- Dependency graphs
- Feature provenance
- Change impact analysis
"""

from .tracker import FeatureLineageTracker

__all__ = ["FeatureLineageTracker"]
