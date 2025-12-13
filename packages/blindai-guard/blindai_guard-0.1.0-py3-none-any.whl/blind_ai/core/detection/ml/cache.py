"""Result caching for ML detection.

Provides LRU cache for expensive operations like ML inference to reduce
latency for repeated requests.
"""

import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Optional

# Default TTL: 1 hour (3600 seconds)
DEFAULT_TTL_SECONDS = 3600


@dataclass
class CacheEntry:
    """Cache entry with value and timestamp for TTL support."""
    
    value: Any
    timestamp: float


class ResultCache:
    """LRU cache for detection results with TTL support.

    Caches results of expensive operations (ML inference, complex analysis)
    to improve performance for repeated requests. Entries expire after TTL.

    Attributes:
        max_size: Maximum number of cached entries
        ttl_seconds: Time-to-live in seconds for cache entries
        cache: Ordered dictionary for LRU implementation
        hits: Number of cache hits
        misses: Number of cache misses
    """

    # Cache version - increment when detection logic changes to invalidate cache
    CACHE_VERSION: str = "v1"

    def __init__(
        self, 
        max_size: int = 1000, 
        version: Optional[str] = None,
        ttl_seconds: int = DEFAULT_TTL_SECONDS
    ):
        """Initialize result cache.

        Args:
            max_size: Maximum number of cached entries (default: 1000)
            version: Cache version string for invalidation (default: CACHE_VERSION)
            ttl_seconds: Time-to-live in seconds (default: 3600 = 1 hour)
        """
        self.max_size = max_size
        self.version = version or self.CACHE_VERSION
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.expirations = 0  # Track expired entries

    def _compute_key(self, key: str, context: Optional[dict] = None) -> str:
        """Compute cache key from text, context, and version.

        Args:
            key: Primary key (typically input text)
            context: Optional context dictionary for context-aware caching

        Returns:
            Hash string combining key, context, and version
        """
        # Start with version prefix for automatic invalidation on upgrades
        parts = [f"v:{self.version}", key]

        # Include context in key if provided
        if context:
            # Sort keys for consistent hashing
            context_str = "|".join(
                f"{k}:{v}" for k, v in sorted(context.items())
            )
            parts.append(context_str)

        combined = "|".join(parts)

        # Use SHA256 for consistent, collision-resistant hashing
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if a cache entry has expired.
        
        Args:
            entry: Cache entry to check
            
        Returns:
            True if entry is expired
        """
        if self.ttl_seconds <= 0:
            return False  # TTL disabled
        return (time.time() - entry.timestamp) > self.ttl_seconds

    def get(self, key: str, context: Optional[dict] = None) -> Optional[Any]:
        """Get cached result if available and not expired.

        Args:
            key: Cache key (typically hash of input text)
            context: Optional context for context-aware caching
                     (e.g., {"turn_count": 5, "behavioral_flags": ["rapid_fire"]})

        Returns:
            Cached result or None if not found or expired
        """
        cache_key = self._compute_key(key, context)

        if cache_key in self.cache:
            entry = self.cache[cache_key]
            
            # Check if entry has expired
            if self._is_expired(entry):
                del self.cache[cache_key]
                self.expirations += 1
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(cache_key)
            self.hits += 1
            return entry.value

        self.misses += 1
        return None

    def put(self, key: str, value: Any, context: Optional[dict] = None) -> None:
        """Store result in cache with timestamp for TTL.

        Args:
            key: Cache key
            value: Result to cache
            context: Optional context for context-aware caching
        """
        cache_key = self._compute_key(key, context)
        entry = CacheEntry(value=value, timestamp=time.time())

        # Update existing entry
        if cache_key in self.cache:
            self.cache.move_to_end(cache_key)
            self.cache[cache_key] = entry
            return

        # Add new entry
        self.cache[cache_key] = entry

        # Evict oldest entry if cache is full
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)  # Remove oldest (FIFO/LRU)

    def cleanup_expired(self) -> int:
        """Remove all expired entries from cache.
        
        Call periodically to prevent stale data accumulation.
        
        Returns:
            Number of entries removed
        """
        if self.ttl_seconds <= 0:
            return 0  # TTL disabled
            
        expired_keys = [
            key for key, entry in self.cache.items()
            if self._is_expired(entry)
        ]
        
        for key in expired_keys:
            del self.cache[key]
            self.expirations += 1
            
        return len(expired_keys)

    def clear(self) -> None:
        """Clear all cached entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.expirations = 0

    def get_stats(self) -> dict:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats:
                - size: Current cache size
                - max_size: Maximum cache size
                - ttl_seconds: TTL in seconds (0 means disabled)
                - hits: Number of cache hits
                - misses: Number of cache misses
                - expirations: Number of expired entries removed
                - hit_rate: Cache hit rate (0.0 to 1.0)
        """
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0.0

        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
            "hits": self.hits,
            "misses": self.misses,
            "expirations": self.expirations,
            "hit_rate": hit_rate,
        }

    def resize(self, new_size: int) -> None:
        """Resize cache capacity.

        Args:
            new_size: New maximum cache size
        """
        self.max_size = new_size

        # Evict entries if cache is now too large
        while len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def __len__(self) -> int:
        """Get current cache size.

        Returns:
            Number of cached entries
        """
        return len(self.cache)

    def __contains__(self, key: str) -> bool:
        """Check if key is in cache (without context).

        For context-aware checking, use get() method.

        Args:
            key: Cache key to check

        Returns:
            True if key is cached
        """
        cache_key = self._compute_key(key)
        return cache_key in self.cache
