"""
Caching System for Repeated Operations

Implements intelligent caching for AutoFE-X operations to avoid redundant computations.
"""

import hashlib
import pickle
import os
import json
from typing import Dict, Any, Optional, Callable
from pathlib import Path
import time
import warnings


class OperationCache:
    """
    Intelligent caching system for AutoFE-X operations.
    """

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        max_size_mb: float = 100.0,
        ttl_seconds: Optional[float] = None,
        enabled: bool = True,
    ):
        """
        Initialize operation cache.

        Args:
            cache_dir: Directory for cache files (default: .autofex_cache)
            max_size_mb: Maximum cache size in MB
            ttl_seconds: Time-to-live for cache entries (None = no expiration)
            enabled: Whether caching is enabled
        """
        self.enabled = enabled
        self.cache_dir = Path(cache_dir or ".autofex_cache")
        self.max_size_mb = max_size_mb
        self.ttl_seconds = ttl_seconds

        if self.enabled:
            self.cache_dir.mkdir(exist_ok=True)
            self.metadata_file = self.cache_dir / "cache_metadata.json"
            self.metadata = self._load_metadata()

            # Clean expired entries on initialization
            self._clean_expired()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    metadata: Any = json.load(f)
                    return dict(metadata) if isinstance(metadata, dict) else {}
            except Exception:
                return {}
        return {}

    def _save_metadata(self):
        """Save cache metadata."""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            warnings.warn(f"Failed to save cache metadata: {e}")

    def _get_cache_key(self, operation: str, *args, **kwargs) -> str:
        """
        Generate cache key from operation and arguments.

        Args:
            operation: Operation name
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Cache key (hash)
        """
        # Create a hashable representation
        key_data = {
            "operation": operation,
            "args": args,
            "kwargs": kwargs,
        }

        # Use pickle to handle complex objects, then hash
        try:
            key_bytes = pickle.dumps(key_data, protocol=pickle.HIGHEST_PROTOCOL)
            key_hash = hashlib.sha256(key_bytes).hexdigest()
            return key_hash
        except Exception as e:
            # Fallback to string representation
            key_str = str(key_data)
            return hashlib.sha256(key_str.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cache entry."""
        return self.cache_dir / f"{cache_key}.pkl"

    def _is_expired(self, cache_key: str) -> bool:
        """Check if cache entry is expired."""
        if self.ttl_seconds is None:
            return False

        if cache_key not in self.metadata:
            return True

        entry_time = self.metadata[cache_key].get("timestamp", 0)
        elapsed = time.time() - entry_time
        return bool(elapsed > self.ttl_seconds)

    def _clean_expired(self):
        """Remove expired cache entries."""
        if not self.enabled:
            return

        expired_keys = []
        for cache_key in list(self.metadata.keys()):
            if self._is_expired(cache_key):
                expired_keys.append(cache_key)

        for key in expired_keys:
            self._remove_entry(key)

    def _remove_entry(self, cache_key: str):
        """Remove a cache entry."""
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            try:
                cache_path.unlink()
            except Exception:
                pass

        if cache_key in self.metadata:
            del self.metadata[cache_key]
            self._save_metadata()

    def _get_cache_size_mb(self) -> float:
        """Get current cache size in MB."""
        if not self.cache_dir.exists():
            return 0.0

        total_size = 0
        for file_path in self.cache_dir.glob("*.pkl"):
            try:
                total_size += file_path.stat().st_size
            except Exception:
                pass

        return total_size / (1024 * 1024)  # Convert to MB

    def _evict_oldest(self):
        """Evict oldest cache entries to make room."""
        if not self.metadata:
            return

        # Sort by timestamp (oldest first)
        sorted_entries = sorted(
            self.metadata.items(),
            key=lambda x: x[1].get("timestamp", 0),
        )

        # Remove oldest entries until under limit
        current_size = self._get_cache_size_mb()
        for cache_key, _ in sorted_entries:
            if current_size <= self.max_size_mb:
                break

            entry_path = self._get_cache_path(cache_key)
            if entry_path.exists():
                try:
                    entry_size = entry_path.stat().st_size / (1024 * 1024)
                    self._remove_entry(cache_key)
                    current_size -= entry_size
                except Exception:
                    pass

    def get(
        self,
        operation: str,
        *args,
        **kwargs,
    ) -> Optional[Any]:
        """
        Get cached result.

        Args:
            operation: Operation name
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Cached result or None if not found
        """
        if not self.enabled:
            return None

        cache_key = self._get_cache_key(operation, *args, **kwargs)
        cache_path = self._get_cache_path(cache_key)

        # Check if expired
        if self._is_expired(cache_key):
            self._remove_entry(cache_key)
            return None

        # Check if file exists
        if not cache_path.exists():
            return None

        # Load cached result
        try:
            with open(cache_path, "rb") as f:
                result = pickle.load(f)

            # Update access time
            if cache_key in self.metadata:
                self.metadata[cache_key]["last_accessed"] = time.time()
                self._save_metadata()

            return result
        except Exception as e:
            warnings.warn(f"Failed to load cache entry: {e}")
            return None

    def set(
        self,
        operation: str,
        result: Any,
        *args,
        **kwargs,
    ):
        """
        Cache a result.

        Args:
            operation: Operation name
            result: Result to cache
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        if not self.enabled:
            return

        # Check cache size and evict if needed
        current_size = self._get_cache_size_mb()
        if current_size >= self.max_size_mb:
            self._evict_oldest()

        cache_key = self._get_cache_key(operation, *args, **kwargs)
        cache_path = self._get_cache_path(cache_key)

        try:
            # Save result
            with open(cache_path, "wb") as f:
                pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)

            # Update metadata
            self.metadata[cache_key] = {
                "operation": operation,
                "timestamp": time.time(),
                "last_accessed": time.time(),
                "size_mb": cache_path.stat().st_size / (1024 * 1024),
            }
            self._save_metadata()
        except Exception as e:
            warnings.warn(f"Failed to cache result: {e}")

    def clear(self, operation: Optional[str] = None):
        """
        Clear cache entries.

        Args:
            operation: Optional operation name to clear (None = clear all)
        """
        if not self.enabled:
            return

        if operation is None:
            # Clear all
            for cache_key in list(self.metadata.keys()):
                self._remove_entry(cache_key)
        else:
            # Clear specific operation
            keys_to_remove = [
                key
                for key, data in self.metadata.items()
                if data.get("operation") == operation
            ]
            for key in keys_to_remove:
                self._remove_entry(key)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        if not self.enabled:
            return {"enabled": False}

        return {
            "enabled": True,
            "cache_dir": str(self.cache_dir),
            "size_mb": self._get_cache_size_mb(),
            "max_size_mb": self.max_size_mb,
            "num_entries": len(self.metadata),
            "ttl_seconds": self.ttl_seconds,
        }

    def cache_function(
        self,
        operation: str,
        func: Callable,
        *args,
        **kwargs,
    ) -> Any:
        """
        Execute function with caching.

        Args:
            operation: Operation name
            func: Function to execute
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Function result (from cache or execution)
        """
        # Try to get from cache
        cached_result = self.get(operation, *args, **kwargs)
        if cached_result is not None:
            return cached_result

        # Execute function
        result = func(*args, **kwargs)

        # Cache result
        self.set(operation, result, *args, **kwargs)

        return result
