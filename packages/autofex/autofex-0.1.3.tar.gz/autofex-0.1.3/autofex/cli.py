"""
Command-line interface for AutoFE-X.
"""

import sys
import argparse
from typing import Optional

try:
    from . import __version__
except ImportError:
    __version__ = "unknown"


def version_command() -> None:
    """Print the version and exit."""
    print(f"autofex {__version__}")
    sys.exit(0)


def info_command() -> None:
    """Print package information."""
    print(
        "AutoFE-X: Automated Feature Engineering + Data Profiling + Leakage Detection"
    )
    print(f"Version: {__version__}")
    print("\nCore Components:")
    print("  • AutoFEX - Main orchestration class")
    print("  • FeatureEngineer - Feature engineering pipeline")
    print("  • DataProfiler - Data quality analysis")
    print("  • LeakageDetector - Leakage detection algorithms")
    print("  • FeatureBenchmarker - Model benchmarking")
    print("  • FeatureLineageTracker - Feature lineage tracking")
    print("\nQuick Start:")
    print("  from autofex import AutoFEX")
    print("  afx = AutoFEX()")
    print("  result = afx.process(X, y)")
    print("\nDocumentation: https://github.com/sudo-de/autofe-x")
    sys.exit(0)


def components_command() -> None:
    """List all available components."""
    print("Available AutoFE-X Components:\n")

    # Core components (always available)
    print("Core Components:")
    print("  • AutoFEX")
    print("  • FeatureEngineer")
    print("  • DataProfiler")
    print("  • LeakageDetector")
    print("  • FeatureBenchmarker")
    print("  • FeatureLineageTracker")

    # Try to import optional components
    print("\nOptional Components (if dependencies available):")
    try:
        from . import FeatureSelector

        print("  ✓ FeatureSelector")
    except (ImportError, AttributeError):
        print("  ✗ FeatureSelector (not available)")

    try:
        from . import StatisticalAnalyzer

        print("  ✓ StatisticalAnalyzer")
    except (ImportError, AttributeError):
        print("  ✗ StatisticalAnalyzer (not available)")

    try:
        from . import MultiDimensionalVisualizer

        print("  ✓ MultiDimensionalVisualizer")
    except (ImportError, AttributeError):
        print("  ✗ MultiDimensionalVisualizer (not available)")

    try:
        from . import PandasOperations

        print("  ✓ PandasOperations")
    except (ImportError, AttributeError):
        print("  ✗ PandasOperations (not available)")

    try:
        from . import NumpyOperations

        print("  ✓ NumpyOperations")
    except (ImportError, AttributeError):
        print("  ✗ NumpyOperations (not available)")

    try:
        from . import ScipyOperations

        print("  ✓ ScipyOperations")
    except (ImportError, AttributeError):
        print("  ✗ ScipyOperations (not available)")

    sys.exit(0)


def main(args: Optional[list] = None) -> None:
    """
    Main CLI entry point.

    Args:
        args: Command-line arguments (defaults to sys.argv)
    """
    parser = argparse.ArgumentParser(
        prog="autofex",
        description="AutoFE-X: Automated Feature Engineering + Data Profiling + Leakage Detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  autofex --version              Show version
  autofex --info                 Show package information
  autofex --components           List available components

For more information, visit: https://github.com/sudo-de/autofe-x
        """,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Show version and exit",
    )

    parser.add_argument(
        "--info",
        "-i",
        action="store_true",
        help="Show package information and quick start guide",
    )

    parser.add_argument(
        "--components",
        "-c",
        action="store_true",
        help="List all available components",
    )

    # Parse arguments
    parsed_args = parser.parse_args(args)

    if parsed_args.version:
        version_command()
    elif parsed_args.info:
        info_command()
    elif parsed_args.components:
        components_command()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
