"""Blind AI Python SDK.

Provides easy-to-use client for protecting tool calls from threats.

Example:
    ```python
    from blind_ai.sdk import ToolGuard, ThreatBlockedError

    # Initialize client
    guard = ToolGuard(
        api_key="your-api-key",
        base_url="http://localhost:8000"
    )

    # Protect a function with decorator
    @guard.protect
    def execute_sql(query: str):
        return db.execute(query)

    # Use it
    try:
        result = execute_sql("DROP TABLE users")
    except ThreatBlockedError as e:
        print(f"Blocked threat: {e.threat_level}")

    # Or check manually
    result = guard.check("SELECT * FROM users")
    if result.is_threat:
        print(f"Threat detected: {result.threat_level}")
    ```

Async Example:
    ```python
    from blind_ai.sdk import AsyncToolGuard

    guard = AsyncToolGuard(base_url="http://localhost:8000")

    @guard.protect
    async def fetch_data(query: str):
        return await db.execute(query)

    result = await fetch_data("SELECT * FROM users")
    ```
"""

from ..core.rbac import Permission, Role, UserContext
from ..core.validation import ParameterSchema, ParameterValidator, SchemaType, ValidationError
from .async_client import AsyncToolGuard
from .circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitBreakerOpen, CircuitState
from .client import ProgressMetadata, SessionContext, ToolGuard
from .testing import (
    MockConfig,
    MockGuard,
    RecordedCheck,
    RecordingGuard,
    ReplayGuard,
    create_test_guard,
)
from .middleware import (
    CacheConfig,
    MiddlewareGuard,
    ProgressiveRollout,
    RateLimitConfig,
    RateLimitExceeded,
    RateLimiter,
    ResultCache,
    RolloutConfig,
    TokenBucket,
)
from .exceptions import (
    APIError,
    BlindAIError,
    ConfigurationError,
    RetryExhaustedError,
    ThreatBlockedError,
    TimeoutError,
)
from .hooks import EventHooks, EventType, SecurityEvent
from .models import ProtectionResult, SDKConfig

__all__ = [
    # Main clients
    "ToolGuard",
    "AsyncToolGuard",
    # Core
    "SessionContext",
    "ProgressMetadata",
    # Exceptions
    "BlindAIError",
    "ThreatBlockedError",
    "APIError",
    "TimeoutError",
    "ConfigurationError",
    "RetryExhaustedError",
    "ValidationError",
    "CircuitBreakerOpen",
    # Models
    "ProtectionResult",
    "SDKConfig",
    # Event Hooks
    "EventHooks",
    "EventType",
    "SecurityEvent",
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitState",
    # RBAC
    "UserContext",
    "Role",
    "Permission",
    # Validation
    "ParameterSchema",
    "ParameterValidator",
    "SchemaType",
    # Testing
    "MockGuard",
    "MockConfig",
    "RecordingGuard",
    "ReplayGuard",
    "RecordedCheck",
    "create_test_guard",
    # Middleware
    "MiddlewareGuard",
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitExceeded",
    "TokenBucket",
    "ResultCache",
    "CacheConfig",
    "ProgressiveRollout",
    "RolloutConfig",
]
