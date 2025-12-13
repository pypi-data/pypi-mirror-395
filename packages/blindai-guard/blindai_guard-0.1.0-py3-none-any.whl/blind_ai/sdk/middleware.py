"""Middleware components for Blind AI SDK.

Provides rate limiting, caching, and progressive rollout capabilities.
"""

import hashlib
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from .exceptions import BlindAIError
from .models import ProtectionResult

logger = logging.getLogger(__name__)


# =============================================================================
# Exceptions
# =============================================================================

class RateLimitExceeded(BlindAIError):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after_seconds: Optional[float] = None,
    ):
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


# =============================================================================
# Rate Limiting
# =============================================================================

class TokenBucket:
    """Token bucket rate limiter.
    
    Implements the token bucket algorithm for rate limiting.
    Tokens are added at a constant rate up to a maximum capacity.
    
    Example:
        ```python
        # 100 requests per minute
        bucket = TokenBucket(rate=100, per_seconds=60)
        
        if bucket.consume():
            # Request allowed
            process_request()
        else:
            # Rate limited
            raise RateLimitExceeded()
        ```
    """
    
    def __init__(
        self,
        rate: int,
        per_seconds: float = 60.0,
        burst: Optional[int] = None,
    ):
        """Initialize token bucket.
        
        Args:
            rate: Number of tokens (requests) allowed per time period
            per_seconds: Time period in seconds (default: 60 = per minute)
            burst: Maximum burst capacity (default: same as rate)
        """
        self.rate = rate
        self.per_seconds = per_seconds
        self.capacity = burst or rate
        self.tokens = float(self.capacity)
        self.last_update = time.monotonic()
        self._lock = threading.Lock()
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_update
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * (self.rate / self.per_seconds)
        )
        self.last_update = now
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed, False if rate limited
        """
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_time(self, tokens: int = 1) -> float:
        """Get time to wait until tokens are available.
        
        Args:
            tokens: Number of tokens needed
            
        Returns:
            Seconds to wait (0 if tokens available now)
        """
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                return 0.0
            needed = tokens - self.tokens
            return needed / (self.rate / self.per_seconds)
    
    @property
    def available(self) -> float:
        """Get current available tokens."""
        with self._lock:
            self._refill()
            return self.tokens


class SlidingWindowRateLimiter:
    """Sliding window rate limiter.
    
    More accurate than token bucket for strict rate limiting.
    Tracks actual request timestamps within the window.
    
    Example:
        ```python
        # 100 requests per minute with sliding window
        limiter = SlidingWindowRateLimiter(limit=100, window_seconds=60)
        
        if limiter.allow():
            process_request()
        ```
    """
    
    def __init__(self, limit: int, window_seconds: float = 60.0):
        """Initialize sliding window limiter.
        
        Args:
            limit: Maximum requests per window
            window_seconds: Window size in seconds
        """
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: List[float] = []
        self._lock = threading.Lock()
    
    def _cleanup(self) -> None:
        """Remove expired timestamps."""
        cutoff = time.monotonic() - self.window_seconds
        self.requests = [t for t in self.requests if t > cutoff]
    
    def allow(self) -> bool:
        """Check if request is allowed.
        
        Returns:
            True if allowed, False if rate limited
        """
        with self._lock:
            self._cleanup()
            if len(self.requests) < self.limit:
                self.requests.append(time.monotonic())
                return True
            return False
    
    def remaining(self) -> int:
        """Get remaining requests in current window."""
        with self._lock:
            self._cleanup()
            return max(0, self.limit - len(self.requests))
    
    def reset_time(self) -> float:
        """Get seconds until oldest request expires."""
        with self._lock:
            self._cleanup()
            if not self.requests:
                return 0.0
            oldest = min(self.requests)
            return max(0.0, (oldest + self.window_seconds) - time.monotonic())


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting.
    
    Attributes:
        requests_per_minute: Maximum requests per minute
        burst_size: Maximum burst capacity (default: 2x rate)
        per_tool_limits: Optional per-tool rate limits
        per_user_limits: Optional per-user rate limits
        algorithm: Rate limiting algorithm ("token_bucket" or "sliding_window")
    """
    requests_per_minute: int = 100
    burst_size: Optional[int] = None
    per_tool_limits: Optional[Dict[str, int]] = None
    per_user_limits: Optional[Dict[str, int]] = None
    algorithm: str = "token_bucket"


class RateLimiter:
    """Composite rate limiter with per-tool and per-user limits.
    
    Example:
        ```python
        config = RateLimitConfig(
            requests_per_minute=100,
            per_tool_limits={"dangerous_tool": 10},
            per_user_limits={"free_tier": 20},
        )
        limiter = RateLimiter(config)
        
        # Check rate limit
        if not limiter.check(tool_name="my_tool", user_id="user-123"):
            raise RateLimitExceeded()
        ```
    """
    
    def __init__(self, config: RateLimitConfig):
        """Initialize rate limiter.
        
        Args:
            config: Rate limit configuration
        """
        self.config = config
        
        # Global limiter
        if config.algorithm == "sliding_window":
            self._global = SlidingWindowRateLimiter(
                limit=config.requests_per_minute,
                window_seconds=60.0,
            )
        else:
            self._global = TokenBucket(
                rate=config.requests_per_minute,
                per_seconds=60.0,
                burst=config.burst_size,
            )
        
        # Per-tool limiters
        self._tool_limiters: Dict[str, Any] = {}
        
        # Per-user limiters
        self._user_limiters: Dict[str, Any] = {}
        
        self._lock = threading.Lock()
    
    def _get_tool_limiter(self, tool_name: str) -> Optional[Any]:
        """Get or create per-tool limiter."""
        if not self.config.per_tool_limits:
            return None
        
        limit = self.config.per_tool_limits.get(tool_name)
        if limit is None:
            return None
        
        with self._lock:
            if tool_name not in self._tool_limiters:
                if self.config.algorithm == "sliding_window":
                    self._tool_limiters[tool_name] = SlidingWindowRateLimiter(limit, 60.0)
                else:
                    self._tool_limiters[tool_name] = TokenBucket(limit, 60.0)
            return self._tool_limiters[tool_name]
    
    def _get_user_limiter(self, user_id: str) -> Optional[Any]:
        """Get or create per-user limiter."""
        if not self.config.per_user_limits:
            return None
        
        # Check for user-specific limit or default
        limit = self.config.per_user_limits.get(user_id)
        if limit is None:
            limit = self.config.per_user_limits.get("default")
        if limit is None:
            return None
        
        with self._lock:
            if user_id not in self._user_limiters:
                if self.config.algorithm == "sliding_window":
                    self._user_limiters[user_id] = SlidingWindowRateLimiter(limit, 60.0)
                else:
                    self._user_limiters[user_id] = TokenBucket(limit, 60.0)
            return self._user_limiters[user_id]
    
    def check(
        self,
        tool_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> bool:
        """Check if request is allowed by all applicable rate limits.
        
        Args:
            tool_name: Optional tool name for per-tool limits
            user_id: Optional user ID for per-user limits
            
        Returns:
            True if allowed, False if any limit exceeded
        """
        # Check global limit
        if isinstance(self._global, TokenBucket):
            if not self._global.consume():
                return False
        else:
            if not self._global.allow():
                return False
        
        # Check per-tool limit
        if tool_name:
            tool_limiter = self._get_tool_limiter(tool_name)
            if tool_limiter:
                if isinstance(tool_limiter, TokenBucket):
                    if not tool_limiter.consume():
                        return False
                else:
                    if not tool_limiter.allow():
                        return False
        
        # Check per-user limit
        if user_id:
            user_limiter = self._get_user_limiter(user_id)
            if user_limiter:
                if isinstance(user_limiter, TokenBucket):
                    if not user_limiter.consume():
                        return False
                else:
                    if not user_limiter.allow():
                        return False
        
        return True
    
    def get_status(
        self,
        tool_name: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get current rate limit status.
        
        Returns:
            Dictionary with remaining requests and reset times
        """
        status = {"global": {}}
        
        if isinstance(self._global, TokenBucket):
            status["global"]["remaining"] = int(self._global.available)
            status["global"]["reset_seconds"] = self._global.wait_time()
        else:
            status["global"]["remaining"] = self._global.remaining()
            status["global"]["reset_seconds"] = self._global.reset_time()
        
        if tool_name:
            tool_limiter = self._get_tool_limiter(tool_name)
            if tool_limiter:
                if isinstance(tool_limiter, TokenBucket):
                    status["tool"] = {
                        "remaining": int(tool_limiter.available),
                        "reset_seconds": tool_limiter.wait_time(),
                    }
                else:
                    status["tool"] = {
                        "remaining": tool_limiter.remaining(),
                        "reset_seconds": tool_limiter.reset_time(),
                    }
        
        return status


# =============================================================================
# Caching
# =============================================================================

@dataclass
class CacheEntry:
    """A cached protection result."""
    result: ProtectionResult
    created_at: float
    hits: int = 0


@dataclass
class CacheConfig:
    """Configuration for result caching.
    
    Attributes:
        enabled: Whether caching is enabled
        ttl_seconds: Time-to-live for cache entries
        max_size: Maximum number of cached entries
        cache_threats: Whether to cache threat results (default: False for safety)
        similarity_enabled: Enable semantic similarity matching
        similarity_threshold: Minimum similarity score for cache hit (0.0-1.0)
    """
    enabled: bool = True
    ttl_seconds: float = 300.0  # 5 minutes
    max_size: int = 1000
    cache_threats: bool = False  # Don't cache threats by default
    similarity_enabled: bool = False
    similarity_threshold: float = 0.95


class ResultCache:
    """LRU cache for protection results.
    
    Caches results to avoid redundant API calls for identical inputs.
    
    Example:
        ```python
        cache = ResultCache(CacheConfig(ttl_seconds=300))
        
        # Check cache
        cached = cache.get("SELECT * FROM users")
        if cached:
            return cached
        
        # Make API call
        result = guard.check(text)
        
        # Cache result
        cache.set(text, result)
        ```
    """
    
    def __init__(self, config: CacheConfig):
        """Initialize cache.
        
        Args:
            config: Cache configuration
        """
        self.config = config
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: List[str] = []  # For LRU eviction
        self._lock = threading.Lock()
        
        # Optional: similarity index for semantic caching
        self._embeddings: Dict[str, List[float]] = {}
    
    def _hash_key(self, text: str, context_id: Optional[str] = None) -> str:
        """Generate cache key from text and context."""
        key_data = text
        if context_id:
            key_data = f"{context_id}:{text}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired."""
        return (time.monotonic() - entry.created_at) > self.config.ttl_seconds
    
    def _evict_if_needed(self) -> None:
        """Evict oldest entries if cache is full."""
        while len(self._cache) >= self.config.max_size and self._access_order:
            oldest_key = self._access_order.pop(0)
            self._cache.pop(oldest_key, None)
            self._embeddings.pop(oldest_key, None)
    
    def _update_access(self, key: str) -> None:
        """Update access order for LRU."""
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
    
    def get(
        self,
        text: str,
        context_id: Optional[str] = None,
    ) -> Optional[ProtectionResult]:
        """Get cached result.
        
        Args:
            text: Input text
            context_id: Optional context ID
            
        Returns:
            Cached ProtectionResult or None if not found/expired
        """
        if not self.config.enabled:
            return None
        
        key = self._hash_key(text, context_id)
        
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                # Try similarity matching if enabled
                if self.config.similarity_enabled:
                    similar_result = self._find_similar(text)
                    if similar_result:
                        return similar_result
                return None
            
            if self._is_expired(entry):
                del self._cache[key]
                if key in self._access_order:
                    self._access_order.remove(key)
                return None
            
            entry.hits += 1
            self._update_access(key)
            
            logger.debug(f"Cache hit for key {key[:8]}... (hits: {entry.hits})")
            return entry.result
    
    def set(
        self,
        text: str,
        result: ProtectionResult,
        context_id: Optional[str] = None,
    ) -> None:
        """Cache a result.
        
        Args:
            text: Input text
            result: Protection result to cache
            context_id: Optional context ID
        """
        if not self.config.enabled:
            return
        
        # Don't cache threats unless explicitly enabled
        if result.is_threat and not self.config.cache_threats:
            return
        
        key = self._hash_key(text, context_id)
        
        with self._lock:
            self._evict_if_needed()
            
            self._cache[key] = CacheEntry(
                result=result,
                created_at=time.monotonic(),
            )
            self._update_access(key)
            
            logger.debug(f"Cached result for key {key[:8]}...")
    
    def _find_similar(self, text: str) -> Optional[ProtectionResult]:
        """Find similar cached result using embeddings.
        
        Note: Requires external embedding function to be set.
        """
        # Placeholder for semantic similarity
        # In production, this would use sentence embeddings
        return None
    
    def invalidate(self, text: str, context_id: Optional[str] = None) -> bool:
        """Invalidate a specific cache entry.
        
        Args:
            text: Input text
            context_id: Optional context ID
            
        Returns:
            True if entry was found and removed
        """
        key = self._hash_key(text, context_id)
        
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                if key in self._access_order:
                    self._access_order.remove(key)
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._embeddings.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        with self._lock:
            total_hits = sum(e.hits for e in self._cache.values())
            return {
                "size": len(self._cache),
                "max_size": self.config.max_size,
                "total_hits": total_hits,
                "ttl_seconds": self.config.ttl_seconds,
            }


# =============================================================================
# Progressive Rollout
# =============================================================================

@dataclass
class RolloutConfig:
    """Configuration for progressive rollout.
    
    Attributes:
        percentage: Percentage of traffic to protect (0-100)
        user_hash_func: Function to hash user ID for consistent bucketing
        sticky: If True, same user always gets same treatment
        ramp_schedule: Optional schedule for automatic ramp-up
        fallback_action: Action when not in rollout ("allow" or "log_only")
    """
    percentage: float = 100.0
    user_hash_func: Optional[Callable[[str], int]] = None
    sticky: bool = True
    ramp_schedule: Optional[List[Tuple[float, float]]] = None  # [(hours, percentage), ...]
    fallback_action: str = "allow"


class ProgressiveRollout:
    """Progressive rollout controller for gradual feature enablement.
    
    Allows gradually rolling out protection to a percentage of traffic.
    
    Example:
        ```python
        # Start with 10% of traffic
        rollout = ProgressiveRollout(RolloutConfig(percentage=10))
        
        # Check if user should be protected
        if rollout.is_enabled(user_id="user-123"):
            result = guard.check(text)
        else:
            # Skip protection for this user
            pass
        
        # Increase rollout
        rollout.set_percentage(50)
        ```
    """
    
    def __init__(self, config: RolloutConfig):
        """Initialize rollout controller.
        
        Args:
            config: Rollout configuration
        """
        self.config = config
        self._percentage = config.percentage
        self._start_time = time.monotonic()
        self._lock = threading.Lock()
        
        # Stats
        self._total_checks = 0
        self._enabled_checks = 0
    
    def _hash_user(self, user_id: str) -> int:
        """Hash user ID to bucket (0-99)."""
        if self.config.user_hash_func:
            return self.config.user_hash_func(user_id) % 100
        
        # Default: SHA256 hash
        hash_bytes = hashlib.sha256(user_id.encode()).digest()
        return int.from_bytes(hash_bytes[:4], 'big') % 100
    
    def _get_current_percentage(self) -> float:
        """Get current percentage, accounting for ramp schedule."""
        if not self.config.ramp_schedule:
            return self._percentage
        
        elapsed_hours = (time.monotonic() - self._start_time) / 3600
        
        current_percentage = self._percentage
        for hours, percentage in sorted(self.config.ramp_schedule):
            if elapsed_hours >= hours:
                current_percentage = percentage
        
        return current_percentage
    
    def is_enabled(self, user_id: Optional[str] = None) -> bool:
        """Check if protection is enabled for this request.
        
        Args:
            user_id: Optional user ID for sticky bucketing
            
        Returns:
            True if protection should be applied
        """
        with self._lock:
            self._total_checks += 1
            
            percentage = self._get_current_percentage()
            
            if percentage >= 100:
                self._enabled_checks += 1
                return True
            
            if percentage <= 0:
                return False
            
            if user_id and self.config.sticky:
                # Sticky: same user always gets same treatment
                bucket = self._hash_user(user_id)
                enabled = bucket < percentage
            else:
                # Random: each request independently sampled
                import random
                enabled = random.random() * 100 < percentage
            
            if enabled:
                self._enabled_checks += 1
            
            return enabled
    
    def set_percentage(self, percentage: float) -> None:
        """Update rollout percentage.
        
        Args:
            percentage: New percentage (0-100)
        """
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        
        with self._lock:
            old = self._percentage
            self._percentage = percentage
            logger.info(f"Rollout percentage changed: {old}% -> {percentage}%")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rollout statistics.
        
        Returns:
            Dictionary with rollout stats
        """
        with self._lock:
            return {
                "current_percentage": self._get_current_percentage(),
                "configured_percentage": self._percentage,
                "total_checks": self._total_checks,
                "enabled_checks": self._enabled_checks,
                "actual_percentage": (
                    (self._enabled_checks / self._total_checks * 100)
                    if self._total_checks > 0 else 0
                ),
            }


# =============================================================================
# Middleware Wrapper
# =============================================================================

class MiddlewareGuard:
    """Guard wrapper with rate limiting, caching, and rollout support.
    
    Wraps any guard with middleware capabilities.
    
    Example:
        ```python
        from blind_ai.sdk import ToolGuard
        from blind_ai.sdk.middleware import (
            MiddlewareGuard,
            RateLimitConfig,
            CacheConfig,
            RolloutConfig,
        )
        
        guard = ToolGuard(base_url="http://localhost:8000")
        
        middleware_guard = MiddlewareGuard(
            guard=guard,
            rate_limit=RateLimitConfig(requests_per_minute=100),
            cache=CacheConfig(ttl_seconds=300),
            rollout=RolloutConfig(percentage=50),
        )
        
        # Use like normal guard
        result = middleware_guard.check("SELECT * FROM users", user_id="user-123")
        ```
    """
    
    def __init__(
        self,
        guard: Any,
        rate_limit: Optional[RateLimitConfig] = None,
        cache: Optional[CacheConfig] = None,
        rollout: Optional[RolloutConfig] = None,
    ):
        """Initialize middleware guard.
        
        Args:
            guard: Underlying guard to wrap
            rate_limit: Rate limiting configuration
            cache: Caching configuration
            rollout: Progressive rollout configuration
        """
        self.guard = guard
        
        self.rate_limiter = RateLimiter(rate_limit) if rate_limit else None
        self.cache = ResultCache(cache) if cache else None
        self.rollout = ProgressiveRollout(rollout) if rollout else None
    
    def check(
        self,
        text: str,
        context_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        user: Optional[Any] = None,
        tool_name: Optional[str] = None,
    ) -> ProtectionResult:
        """Check with middleware applied.
        
        Args:
            text: Text to check
            context_id: Optional context ID
            metadata: Optional metadata
            user: Optional user context
            tool_name: Optional tool name for rate limiting
            
        Returns:
            ProtectionResult
            
        Raises:
            RateLimitExceeded: If rate limit exceeded
            ThreatBlockedError: If threat detected
        """
        user_id = user.user_id if user and hasattr(user, 'user_id') else None
        
        # Check rollout
        if self.rollout and not self.rollout.is_enabled(user_id):
            # Not in rollout - return safe result
            logger.debug(f"Rollout: skipping check for user {user_id}")
            return ProtectionResult(
                is_threat=False,
                threat_level="none",
                final_action="allow",
                threats_detected=[],
                confidence=0.0,
                processing_time_ms=0,
                metadata={"rollout_skipped": True},
            )
        
        # Check rate limit
        if self.rate_limiter:
            if not self.rate_limiter.check(tool_name=tool_name, user_id=user_id):
                status = self.rate_limiter.get_status(tool_name, user_id)
                raise RateLimitExceeded(
                    message="Rate limit exceeded",
                    retry_after_seconds=status.get("global", {}).get("reset_seconds"),
                )
        
        # Check cache
        if self.cache:
            cached = self.cache.get(text, context_id)
            if cached:
                logger.debug("Returning cached result")
                return cached
        
        # Make actual check
        result = self.guard.check(
            text=text,
            context_id=context_id,
            metadata=metadata,
            user=user,
        )
        
        # Cache result
        if self.cache:
            self.cache.set(text, result, context_id)
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get middleware statistics.
        
        Returns:
            Dictionary with all middleware stats
        """
        stats = {}
        
        if self.rate_limiter:
            stats["rate_limit"] = self.rate_limiter.get_status()
        
        if self.cache:
            stats["cache"] = self.cache.get_stats()
        
        if self.rollout:
            stats["rollout"] = self.rollout.get_stats()
        
        return stats
    
    # Delegate other attributes to underlying guard
    def __getattr__(self, name: str) -> Any:
        return getattr(self.guard, name)
