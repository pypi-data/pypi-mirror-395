"""
Parallel Processing Utilities

Provides parallel processing capabilities for AutoFE-X operations.
"""

import pandas as pd
import numpy as np
from typing import List, Callable, Any, Optional, Dict, Tuple
import warnings

try:
    from joblib import Parallel, delayed

    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    warnings.warn("joblib not available. Parallel processing will be disabled.")

try:
    import multiprocessing as mp

    MULTIPROCESSING_AVAILABLE = True
except ImportError:
    MULTIPROCESSING_AVAILABLE = False


def get_n_jobs(n_jobs: Optional[int] = None) -> int:
    """
    Get number of jobs for parallel processing.

    Args:
        n_jobs: Number of jobs (-1 for all CPUs, None for 1)

    Returns:
        Number of jobs to use
    """
    if n_jobs is None:
        return 1

    if n_jobs == -1:
        if MULTIPROCESSING_AVAILABLE:
            return mp.cpu_count()
        return 1

    return max(1, n_jobs)


def parallel_apply(
    func: Callable,
    items: List[Any],
    n_jobs: Optional[int] = None,
    backend: str = "threading",
    verbose: int = 0,
    progress_callback: Optional[Callable] = None,
) -> List[Any]:
    """
    Apply a function to a list of items in parallel.

    Args:
        func: Function to apply
        items: List of items to process
        n_jobs: Number of parallel jobs (-1 for all CPUs, None for sequential)
        backend: Backend ('threading', 'multiprocessing', 'loky')
        verbose: Verbosity level
        progress_callback: Optional callback for progress updates

    Returns:
        List of results
    """
    if not JOBLIB_AVAILABLE or n_jobs is None or n_jobs == 1:
        # Sequential processing
        results = []
        for i, item in enumerate(items):
            result = func(item)
            results.append(result)
            if progress_callback:
                progress_callback(i + 1, len(items))
        return results

    # Parallel processing
    n_jobs = get_n_jobs(n_jobs)

    # Use joblib for parallel processing
    results = Parallel(n_jobs=n_jobs, backend=backend, verbose=verbose)(
        delayed(func)(item) for item in items
    )

    if progress_callback:
        progress_callback(len(items), len(items))

    return list(results)  # type: ignore[no-any-return]


def parallel_transform_columns(
    X: pd.DataFrame,
    transform_func: Callable,
    columns: List[str],
    n_jobs: Optional[int] = None,
    backend: str = "threading",
    verbose: int = 0,
    progress_callback: Optional[Callable] = None,
) -> List[Any]:
    """
    Transform multiple columns in parallel.

    Args:
        X: Input DataFrame
        transform_func: Function that takes (series, col_name) and returns List[pd.DataFrame]
        columns: List of column names to transform
        n_jobs: Number of parallel jobs
        backend: Backend for parallel processing
        verbose: Verbosity level
        progress_callback: Optional callback for progress updates

    Returns:
        List of DataFrames with transformed features
    """
    if not columns:
        return []

    def _transform_column(col_name: str) -> List[pd.DataFrame]:
        """Transform a single column."""
        result: Any = transform_func(X[col_name], col_name)
        return list(result) if isinstance(result, list) else [result]  # type: ignore[no-any-return]

    # Process columns in parallel
    if n_jobs is None or n_jobs == 1 or not JOBLIB_AVAILABLE:
        # Sequential processing
        all_features = []
        for i, col in enumerate(columns):
            features = _transform_column(col)
            all_features.extend(features)
            if progress_callback:
                progress_callback(i + 1, len(columns))
        return all_features
    else:
        # Parallel processing
        n_jobs = get_n_jobs(n_jobs)
        parallel_results = Parallel(n_jobs=n_jobs, backend=backend, verbose=verbose)(
            delayed(_transform_column)(col) for col in columns
        )
        # Flatten list of lists
        all_features = []
        for features_list in parallel_results:
            all_features.extend(features_list)
        if progress_callback:
            progress_callback(len(columns), len(columns))
        return all_features


def parallel_feature_creation(
    feature_funcs: List[Callable],
    X: pd.DataFrame,
    y: Optional[pd.Series] = None,
    n_jobs: Optional[int] = None,
    backend: str = "threading",
    verbose: int = 0,
    progress_callback: Optional[Callable] = None,
) -> List[pd.DataFrame]:
    """
    Create multiple feature sets in parallel.

    Args:
        feature_funcs: List of functions that create features
        X: Input DataFrame
        y: Target variable (optional)
        n_jobs: Number of parallel jobs
        backend: Backend for parallel processing
        verbose: Verbosity level
        progress_callback: Optional callback for progress updates

    Returns:
        List of feature DataFrames
    """

    def _create_features(func: Callable) -> pd.DataFrame:
        """Create features using a function."""
        if y is not None:
            return func(X, y)
        return func(X)

    if n_jobs is None or n_jobs == 1 or not JOBLIB_AVAILABLE:
        # Sequential processing
        results = []
        for i, func in enumerate(feature_funcs):
            result = _create_features(func)
            results.append(result)
            if progress_callback:
                progress_callback(i + 1, len(feature_funcs))
        return results

    # Parallel processing
    n_jobs = get_n_jobs(n_jobs)
    results = Parallel(n_jobs=n_jobs, backend=backend, verbose=verbose)(
        delayed(_create_features)(func) for func in feature_funcs
    )

    if progress_callback:
        progress_callback(len(feature_funcs), len(feature_funcs))

    return list(results)  # type: ignore[no-any-return]
