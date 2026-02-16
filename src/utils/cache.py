"""Simple file-based cache with TTL."""

import json
import os
import time
from pathlib import Path
from typing import Any, Optional

from .logger import get_logger

logger = get_logger(__name__)


class FileCache:
    """File-based cache with time-to-live (TTL) support."""

    def __init__(self, cache_dir: str = "private/cache", ttl_seconds: int = 3600):
        """
        Initialize file cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time-to-live for cache entries in seconds
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds

    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key."""
        # Use hash to create safe filename
        import hashlib
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r') as f:
                cache_entry = json.load(f)

            # Check if expired
            if time.time() - cache_entry['timestamp'] > self.ttl_seconds:
                logger.debug(f"Cache expired for key: {key}")
                cache_path.unlink()  # Delete expired entry
                return None

            logger.debug(f"Cache hit for key: {key}")
            return cache_entry['value']

        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Invalid cache file for key {key}: {e}")
            cache_path.unlink()  # Delete corrupted entry
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Store value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON-serializable)
        """
        cache_path = self._get_cache_path(key)

        cache_entry = {
            'timestamp': time.time(),
            'value': value
        }

        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_entry, f)
            logger.debug(f"Cached value for key: {key}")
        except TypeError as e:
            logger.error(f"Cannot cache non-JSON-serializable value: {e}")
