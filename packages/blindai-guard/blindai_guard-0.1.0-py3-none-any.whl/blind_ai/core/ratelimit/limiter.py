"""Token bucket rate limiter with Redis backend."""

import re
import time
from typing import Optional

from redis import Redis


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: float):
        super().__init__(message)
        self.retry_after = retry_after


# Pattern for valid Redis key characters (alphanumeric, underscore, dash, colon)
VALID_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9_:\-\.]+$")


def sanitize_key(key: str) -> str:
    """Sanitize a rate limiter key to prevent injection attacks.

    Args:
        key: The raw key to sanitize

    Returns:
        Sanitized key safe for Redis

    Raises:
        ValueError: If key contains invalid characters that can't be sanitized
    """
    if not key:
        raise ValueError("Rate limiter key cannot be empty")

    # If key is already valid, return as-is
    if VALID_KEY_PATTERN.match(key):
        return key

    # Replace invalid characters with underscore
    sanitized = re.sub(r"[^a-zA-Z0-9_:\-\.]", "_", key)

    # Ensure result is not empty after sanitization
    if not sanitized or sanitized == "_" * len(sanitized):
        raise ValueError(f"Key '{key}' contains no valid characters")

    return sanitized


class RateLimiter:
    """Token bucket rate limiter using Redis.

    Uses sliding window algorithm for accurate rate limiting.
    """

    def __init__(self, redis_client: Redis, key_prefix: str = "ratelimit:"):
        """Initialize rate limiter.

        Args:
            redis_client: Redis client
            key_prefix: Prefix for Redis keys
        """
        self.redis = redis_client
        self.key_prefix = key_prefix

    def check_rate_limit(
        self,
        key: str,
        limit: int,
        window_seconds: int = 60,
    ) -> None:
        """Check if request is within rate limit.

        Uses sliding window counter algorithm.

        Args:
            key: Unique identifier (e.g., "user:123:tool:send_email")
            limit: Maximum requests allowed in window
            window_seconds: Time window in seconds (default: 60)

        Raises:
            RateLimitExceeded: If rate limit exceeded
            ValueError: If key is invalid
        """
        # Sanitize key to prevent injection attacks
        sanitized_key = sanitize_key(key)
        redis_key = f"{self.key_prefix}{sanitized_key}"
        current_time = time.time()
        window_start = current_time - window_seconds

        # Remove old entries outside the window
        self.redis.zremrangebyscore(redis_key, 0, window_start)

        # Count requests in current window
        current_count = self.redis.zcard(redis_key)

        if current_count >= limit:
            # Get oldest entry timestamp
            oldest = self.redis.zrange(redis_key, 0, 0, withscores=True)
            if oldest:
                retry_after = window_seconds - (current_time - oldest[0][1])
                raise RateLimitExceeded(
                    f"Rate limit exceeded: {limit} requests per {window_seconds}s",
                    retry_after=max(0, retry_after),
                )

        # Add current request
        self.redis.zadd(redis_key, {str(current_time): current_time})

        # Set expiry on key
        self.redis.expire(redis_key, window_seconds)

    def get_remaining(
        self,
        key: str,
        limit: int,
        window_seconds: int = 60,
    ) -> int:
        """Get remaining requests in current window.

        Args:
            key: Unique identifier
            limit: Maximum requests allowed
            window_seconds: Time window in seconds

        Returns:
            Number of remaining requests
        """
        sanitized_key = sanitize_key(key)
        redis_key = f"{self.key_prefix}{sanitized_key}"
        current_time = time.time()
        window_start = current_time - window_seconds

        # Remove old entries
        self.redis.zremrangebyscore(redis_key, 0, window_start)

        # Count current requests
        current_count = self.redis.zcard(redis_key)
        return max(0, limit - current_count)

    def reset(self, key: str) -> None:
        """Reset rate limit for a key.

        Args:
            key: Unique identifier
        """
        sanitized_key = sanitize_key(key)
        redis_key = f"{self.key_prefix}{sanitized_key}"
        self.redis.delete(redis_key)
