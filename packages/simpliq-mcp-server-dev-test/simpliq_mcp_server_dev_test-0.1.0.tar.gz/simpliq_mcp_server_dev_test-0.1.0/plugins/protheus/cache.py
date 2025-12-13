# -*- coding: utf-8 -*-
"""
Protheus Dictionary Cache System

Provides persistent caching for Protheus data dictionary to improve performance.

Author: SimpliQ Development Team
Date: 2025-11-18
"""

import pickle
import os
import hashlib
import logging
from typing import Any, Optional, Dict
from pathlib import Path
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ProtheusDictionaryCache:
    """Persistent cache for Protheus data dictionary."""

    def __init__(self, cache_dir: Optional[str] = None, ttl_hours: int = 24):
        """
        Initialize the cache system.

        Args:
            cache_dir: Directory for cache files (default: .cache/protheus)
            ttl_hours: Time-to-live for cache entries in hours (default: 24)
        """
        if cache_dir is None:
            # Default to .cache/protheus in current directory
            cache_dir = os.path.join(os.getcwd(), ".cache", "protheus")

        self.cache_dir = Path(cache_dir)
        self.ttl_hours = ttl_hours
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Ensure cache directory exists."""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Cache directory: {self.cache_dir}")
        except Exception as e:
            logger.warning(f"Failed to create cache directory: {e}")

    def _get_cache_key(self, operation: str, **params) -> str:
        """
        Generate cache key from operation and parameters.

        Args:
            operation: Operation type (e.g., "tables", "columns", "indexes")
            **params: Parameters for the operation

        Returns:
            Cache key string
        """
        # Sort params for consistent hashing
        param_str = "_".join(f"{k}={v}" for k, v in sorted(params.items()))
        key = f"{operation}_{param_str}"

        # Use hash for long keys
        if len(key) > 200:
            key_hash = hashlib.md5(key.encode()).hexdigest()
            key = f"{operation}_{key_hash}"

        return key

    def _get_cache_path(self, cache_key: str) -> Path:
        """
        Get file path for cache key.

        Args:
            cache_key: Cache key

        Returns:
            Path to cache file
        """
        # Sanitize key for filename
        safe_key = cache_key.replace("/", "_").replace("\\", "_")
        return self.cache_dir / f"{safe_key}.pkl"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """
        Check if cache file is still valid (not expired).

        Args:
            cache_path: Path to cache file

        Returns:
            True if cache is valid, False otherwise
        """
        if not cache_path.exists():
            return False

        try:
            # Check modification time
            mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
            age = datetime.now() - mtime

            if age > timedelta(hours=self.ttl_hours):
                logger.debug(f"Cache expired: {cache_path.name} (age: {age})")
                return False

            return True

        except Exception as e:
            logger.warning(f"Error checking cache validity: {e}")
            return False

    def get(self, operation: str, **params) -> Optional[Any]:
        """
        Get cached data.

        Args:
            operation: Operation type
            **params: Operation parameters

        Returns:
            Cached data or None if not found/expired
        """
        cache_key = self._get_cache_key(operation, **params)
        cache_path = self._get_cache_path(cache_key)

        if not self._is_cache_valid(cache_path):
            return None

        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
                logger.debug(f"Cache hit: {cache_key}")
                return data

        except Exception as e:
            logger.warning(f"Error loading cache {cache_key}: {e}")
            # Remove corrupted cache file
            try:
                cache_path.unlink()
            except:
                pass
            return None

    def set(self, data: Any, operation: str, **params) -> bool:
        """
        Store data in cache.

        Args:
            data: Data to cache
            operation: Operation type
            **params: Operation parameters

        Returns:
            True if successful, False otherwise
        """
        cache_key = self._get_cache_key(operation, **params)
        cache_path = self._get_cache_path(cache_key)

        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                logger.debug(f"Cache stored: {cache_key}")
                return True

        except Exception as e:
            logger.warning(f"Error storing cache {cache_key}: {e}")
            return False

    def invalidate(self, operation: Optional[str] = None, **params):
        """
        Invalidate cache entries.

        Args:
            operation: Operation type to invalidate (None = all)
            **params: Operation parameters to match
        """
        if operation is None:
            # Invalidate all
            try:
                for cache_file in self.cache_dir.glob("*.pkl"):
                    cache_file.unlink()
                logger.info("Cleared all cache entries")
            except Exception as e:
                logger.warning(f"Error clearing cache: {e}")
        else:
            # Invalidate specific entry
            cache_key = self._get_cache_key(operation, **params)
            cache_path = self._get_cache_path(cache_key)

            try:
                if cache_path.exists():
                    cache_path.unlink()
                    logger.debug(f"Cache invalidated: {cache_key}")
            except Exception as e:
                logger.warning(f"Error invalidating cache {cache_key}: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        try:
            cache_files = list(self.cache_dir.glob("*.pkl"))
            total_size = sum(f.stat().st_size for f in cache_files)

            valid_count = sum(1 for f in cache_files if self._is_cache_valid(f))
            expired_count = len(cache_files) - valid_count

            return {
                "total_entries": len(cache_files),
                "valid_entries": valid_count,
                "expired_entries": expired_count,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "cache_dir": str(self.cache_dir),
                "ttl_hours": self.ttl_hours
            }

        except Exception as e:
            logger.warning(f"Error getting cache stats: {e}")
            return {
                "error": str(e),
                "cache_dir": str(self.cache_dir)
            }

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        removed = 0

        try:
            for cache_file in self.cache_dir.glob("*.pkl"):
                if not self._is_cache_valid(cache_file):
                    cache_file.unlink()
                    removed += 1

            if removed > 0:
                logger.info(f"Removed {removed} expired cache entries")

        except Exception as e:
            logger.warning(f"Error cleaning up cache: {e}")

        return removed
