"""
Feature Lineage Tracking Engine

Tracks the provenance and transformation history of features through a graph-based system.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any, Set, Tuple
from collections import defaultdict, deque
import networkx as nx
import json
import warnings


class FeatureLineageTracker:
    """
    Graph-based feature lineage tracker that maintains the complete history
    of feature transformations and dependencies.

    Features:
    - Track feature creation and transformation steps
    - Build dependency graphs
    - Analyze feature impact on model performance
    - Support for feature versioning and provenance
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize feature lineage tracker.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.graph = nx.DiGraph()
        self.feature_versions: Dict[str, Any] = {}
        self.transformation_history: List[Dict[str, Any]] = []
        self.current_session: Optional[str] = None

    def start_session(self, initial_features: List[str]):
        """
        Start a new feature engineering session.

        Args:
            initial_features: List of initial feature names
        """
        self.current_session = f"session_{len(self.transformation_history)}"

        # Add initial features to graph
        for feature in initial_features:
            self.graph.add_node(
                feature, node_type="original", created_in=self.current_session
            )

        self.transformation_history.append(
            {
                "session": self.current_session,
                "action": "session_start",
                "initial_features": initial_features,
                "timestamp": pd.Timestamp.now(),
            }
        )

    def add_transformation(
        self,
        transformation_type: str,
        input_features: List[str],
        output_features: List[str],
        parameters: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Record a feature transformation.

        Args:
            transformation_type: Type of transformation (e.g., 'log_transform', 'interaction')
            input_features: Features used as input
            output_features: Features created as output
            parameters: Transformation parameters
            metadata: Additional metadata
        """
        if self.current_session is None:
            self.start_session(input_features)

        # Validate inputs exist in graph
        missing_inputs = [f for f in input_features if f not in self.graph]
        if missing_inputs:
            warnings.warn(f"Input features not found in lineage: {missing_inputs}")

        # Add transformation node
        transform_node = f"{transformation_type}_{len(self.transformation_history)}"
        self.graph.add_node(
            transform_node,
            node_type="transformation",
            transformation_type=transformation_type,
            parameters=parameters or {},
            metadata=metadata or {},
            created_in=self.current_session,
        )

        # Add edges from inputs to transformation
        for input_feature in input_features:
            if input_feature in self.graph:
                self.graph.add_edge(input_feature, transform_node)

        # Add edges from transformation to outputs
        for output_feature in output_features:
            self.graph.add_node(
                output_feature,
                node_type="derived",
                created_from=transform_node,
                created_in=self.current_session,
            )
            self.graph.add_edge(transform_node, output_feature)

        # Record in history
        self.transformation_history.append(
            {
                "session": self.current_session,
                "action": "transformation",
                "type": transformation_type,
                "input_features": input_features,
                "output_features": output_features,
                "parameters": parameters,
                "metadata": metadata,
                "timestamp": pd.Timestamp.now(),
            }
        )

    def get_lineage_graph(self) -> Dict[str, Any]:
        """
        Get the complete feature lineage graph.

        Returns:
            Dictionary representation of the lineage graph
        """
        # Convert NetworkX graph to dictionary
        graph_data: Dict[str, Any] = {
            "nodes": [],
            "edges": [],
            "metadata": {
                "total_features": len(
                    [
                        n
                        for n in self.graph.nodes()
                        if self.graph.nodes[n].get("node_type") != "transformation"
                    ]
                ),
                "total_transformations": len(
                    [
                        n
                        for n in self.graph.nodes()
                        if self.graph.nodes[n].get("node_type") == "transformation"
                    ]
                ),
                "sessions": list(
                    set(
                        [
                            self.graph.nodes[n].get("created_in")
                            for n in self.graph.nodes()
                        ]
                    )
                ),
                "transformation_types": list(
                    set(
                        [
                            self.graph.nodes[n].get("transformation_type")
                            for n in self.graph.nodes()
                            if self.graph.nodes[n].get("node_type") == "transformation"
                        ]
                    )
                ),
            },
        }

        # Add nodes
        for node, attrs in self.graph.nodes(data=True):
            graph_data["nodes"].append(
                {
                    "id": node,
                    "type": attrs.get("node_type", "unknown"),
                    "attributes": attrs,
                }
            )

        # Add edges
        for source, target in self.graph.edges():
            graph_data["edges"].append({"source": source, "target": target})

        return graph_data

    def get_feature_dependencies(self, feature: str) -> Dict[str, Any]:
        """
        Get all dependencies for a specific feature.

        Args:
            feature: Feature name

        Returns:
            Dictionary with dependency information
        """
        if feature not in self.graph:
            return {"error": f"Feature {feature} not found in lineage"}

        # Get all predecessors (including indirect)
        all_predecessors = list(nx.ancestors(self.graph, feature))
        all_predecessors.append(feature)  # Include the feature itself

        # Separate by type
        original_features = [
            n
            for n in all_predecessors
            if self.graph.nodes[n].get("node_type") == "original"
        ]
        transformations = [
            n
            for n in all_predecessors
            if self.graph.nodes[n].get("node_type") == "transformation"
        ]
        derived_features = [
            n
            for n in all_predecessors
            if self.graph.nodes[n].get("node_type") == "derived"
        ]

        # Get dependency path
        dependency_path = self._get_dependency_path(feature)

        return {
            "feature": feature,
            "original_features": original_features,
            "transformations": transformations,
            "derived_features": derived_features,
            "dependency_depth": len(dependency_path),
            "dependency_path": dependency_path,
            "creation_session": self.graph.nodes[feature].get("created_in"),
        }

    def get_transformation_impact(self, transformation_node: str) -> Dict[str, Any]:
        """
        Get the impact of a specific transformation.

        Args:
            transformation_node: Transformation node name

        Returns:
            Dictionary with impact information
        """
        if transformation_node not in self.graph:
            return {"error": f"Transformation {transformation_node} not found"}

        # Get all features derived from this transformation
        descendants = nx.descendants(self.graph, transformation_node)
        derived_features = [
            n for n in descendants if self.graph.nodes[n].get("node_type") == "derived"
        ]

        # Get transformation details
        transform_attrs = self.graph.nodes[transformation_node]

        return {
            "transformation": transformation_node,
            "type": transform_attrs.get("transformation_type"),
            "parameters": transform_attrs.get("parameters"),
            "input_features": list(self.graph.predecessors(transformation_node)),
            "output_features": derived_features,
            "total_derived_features": len(derived_features),
            "metadata": transform_attrs.get("metadata", {}),
        }

    def find_feature_roots(self, feature: str) -> List[str]:
        """
        Find the root (original) features that a derived feature depends on.

        Args:
            feature: Feature name

        Returns:
            List of root feature names
        """
        if feature not in self.graph:
            return []

        # Find all original features in the ancestry
        ancestors = nx.ancestors(self.graph, feature)
        root_features = [
            n for n in ancestors if self.graph.nodes[n].get("node_type") == "original"
        ]

        return root_features

    def get_feature_generation(self, generation: int = 0) -> List[str]:
        """
        Get features by their generation level.

        Args:
            generation: Generation level (0 = original, 1 = first derivatives, etc.)

        Returns:
            List of feature names in that generation
        """
        features_by_generation = self._calculate_feature_generations()

        return features_by_generation.get(generation, [])

    def _calculate_feature_generations(self) -> Dict[int, List[str]]:
        """
        Calculate generation levels for all features.
        """
        generations = defaultdict(list)

        # Original features are generation 0
        original_features = [
            n
            for n in self.graph.nodes()
            if self.graph.nodes[n].get("node_type") == "original"
        ]
        generations[0] = original_features

        # Use BFS to calculate generations
        visited = set(original_features)
        queue = deque([(feature, 0) for feature in original_features])

        while queue:
            current_feature, current_gen = queue.popleft()

            # Find features derived from this one
            for successor in self.graph.successors(current_feature):
                if (
                    successor not in visited
                    and self.graph.nodes[successor].get("node_type") == "derived"
                ):
                    new_gen = current_gen + 1
                    generations[new_gen].append(successor)
                    visited.add(successor)
                    queue.append((successor, new_gen))

        return dict(generations)

    def _get_dependency_path(self, feature: str) -> List[Dict[str, Any]]:
        """
        Get the complete dependency path for a feature.
        """
        path = []

        # Use BFS to trace back dependencies
        visited = set()
        queue: deque[Tuple[str, List[str]]] = deque([(feature, [])])

        while queue:
            current, current_path = queue.popleft()

            if current in visited:
                continue
            visited.add(current)

            node_attrs = self.graph.nodes[current]
            path_entry = {
                "feature": current,
                "type": node_attrs.get("node_type"),
                "transformation_type": node_attrs.get("transformation_type"),
                "path": current_path + [current],
            }
            path.append(path_entry)

            # Add predecessors
            for pred in self.graph.predecessors(current):
                if pred not in visited:
                    queue.append((pred, current_path + [current]))

        return path

    def export_lineage(self, format: str = "json") -> Union[str, Dict[str, Any]]:
        """
        Export the feature lineage in different formats.

        Args:
            format: Export format ('json', 'dict')

        Returns:
            Lineage data in specified format
        """
        lineage_data = {
            "graph": self.get_lineage_graph(),
            "history": self.transformation_history,
            "sessions": list(set(h["session"] for h in self.transformation_history)),
            "metadata": {
                "total_sessions": len(
                    set(h["session"] for h in self.transformation_history)
                ),
                "total_transformations": len(
                    [
                        h
                        for h in self.transformation_history
                        if h["action"] == "transformation"
                    ]
                ),
                "created_at": pd.Timestamp.now().isoformat(),
            },
        }

        if format == "json":
            return json.dumps(lineage_data, indent=2, default=str)
        elif format == "dict":
            return lineage_data
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def get_transformation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all transformations performed.
        """
        transformation_counts: defaultdict[str, int] = defaultdict(int)
        feature_counts: defaultdict[str, int] = defaultdict(int)

        for history_entry in self.transformation_history:
            if history_entry["action"] == "transformation":
                transformation_counts[history_entry["type"]] += 1
                feature_counts["input"] += len(history_entry["input_features"])
                feature_counts["output"] += len(history_entry["output_features"])

        return {
            "transformation_counts": dict(transformation_counts),
            "total_transformations": sum(transformation_counts.values()),
            "feature_counts": dict(feature_counts),
            "most_common_transformation": (
                max(transformation_counts, key=lambda k: transformation_counts[k])
                if transformation_counts
                else None
            ),
        }

    def detect_cycles(self) -> List[List[str]]:
        """
        Detect cycles in the feature dependency graph.

        Returns:
            List of cycles found (each cycle is a list of node names)
        """
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []

    def validate_lineage(self) -> Dict[str, Any]:
        """
        Validate the integrity of the feature lineage.

        Returns:
            Validation results
        """
        issues = []

        # Check for orphaned nodes
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get("node_type")
            if node_type == "derived":
                # Derived features should have a transformation predecessor
                predecessors = list(self.graph.predecessors(node))
                transform_preds = [
                    p
                    for p in predecessors
                    if self.graph.nodes[p].get("node_type") == "transformation"
                ]
                if not transform_preds:
                    issues.append(
                        f"Derived feature {node} has no transformation predecessor"
                    )
            elif node_type == "transformation":
                # Transformations should have both inputs and outputs
                if self.graph.in_degree(node) == 0:
                    issues.append(f"Transformation {node} has no input features")
                if self.graph.out_degree(node) == 0:
                    issues.append(f"Transformation {node} has no output features")

        # Check for cycles
        cycles = self.detect_cycles()
        if cycles:
            issues.append(f"Found {len(cycles)} cycles in dependency graph")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "total_nodes": len(self.graph.nodes()),
            "total_edges": len(self.graph.edges()),
            "cycles_detected": len(cycles) > 0,
        }
