"""Tool registry for metadata-driven authorization.

This module provides tool registration and metadata management for Layer 2
authorization features. Tools can be registered with trust levels, allowed
domains, rate limits, and other security metadata.

Example:
    >>> from blind_ai.core.registry import ToolMetadata, TrustLevel, ToolType
    >>> from blind_ai.core.registry import ToolRegistry
    >>>
    >>> # Register a tool
    >>> metadata = ToolMetadata(
    ...     name="send_email",
    ...     trust_level=TrustLevel.LOW,
    ...     tool_type=ToolType.COMMUNICATION,
    ...     allowed_domains=["company.com"],
    ...     rate_limit_per_minute=100
    ... )
    >>>
    >>> registry = ToolRegistry(redis_client=redis)
    >>> registry.register(metadata)
    >>>
    >>> # Retrieve tool metadata
    >>> tool = registry.get("send_email")
    >>> print(tool.trust_level)  # TrustLevel.LOW
"""

from .metadata import ToolMetadata, TrustLevel, ToolType
from .storage import ToolRegistry

__all__ = [
    "ToolMetadata",
    "TrustLevel",
    "ToolType",
    "ToolRegistry",
]
