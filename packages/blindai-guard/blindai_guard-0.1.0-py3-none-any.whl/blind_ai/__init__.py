"""Blind AI - Runtime security for AI agents.

Prevent prompt injection, data exfiltration, and SQL injection in AI agents.

Quick Start:
    ```python
    from blind_ai import ToolGuard

    guard = ToolGuard(api_key="your_key")

    @guard.protect()
    def query_database(sql: str):
        return db.execute(sql)
    ```

For async usage:
    ```python
    from blind_ai import AsyncToolGuard

    guard = AsyncToolGuard(api_key="your_key")

    @guard.protect()
    async def query_database(sql: str):
        return await db.execute(sql)
    ```
"""

__version__ = "0.1.0"

# Core detection (low-level API)
from blind_ai.core.detection.patterns import (
    ALL_PII_PATTERNS,
    ALL_PROMPT_PATTERNS,
    ALL_SQL_PATTERNS,
    PIICategory,
    RiskLevel,
)
from blind_ai.core.detection.static import ActionType, DetectionResult, StaticDetector, ThreatType

# Core models and exceptions
from blind_ai.core.models import InputTooLargeError

# SDK clients (primary API)
from blind_ai.sdk import (
    AsyncToolGuard,
    ToolGuard,
)

# SDK exceptions
from blind_ai.sdk.exceptions import (
    APIError,
    BlindAIError,
    ConfigurationError,
    RetryExhaustedError,
    ThreatBlockedError,
    TimeoutError,
)

# SDK models
from blind_ai.sdk.models import (
    ProtectionResult,
    SDKConfig,
)

# RBAC
from blind_ai.core.rbac import (
    Permission,
    Role,
    UserContext,
)

__all__ = [
    # Version
    "__version__",
    # SDK Clients (Primary API)
    "ToolGuard",
    "AsyncToolGuard",
    # SDK Exceptions
    "BlindAIError",
    "ThreatBlockedError",
    "APIError",
    "TimeoutError",
    "ConfigurationError",
    "RetryExhaustedError",
    "InputTooLargeError",
    # SDK Models
    "ProtectionResult",
    "SDKConfig",
    # RBAC
    "UserContext",
    "Role",
    "Permission",
    # Static Detector (Low-level)
    "StaticDetector",
    "DetectionResult",
    "ActionType",
    "ThreatType",
    # Patterns (Low-level)
    "ALL_SQL_PATTERNS",
    "ALL_PROMPT_PATTERNS",
    "ALL_PII_PATTERNS",
    # Enums
    "PIICategory",
    "RiskLevel",
]
