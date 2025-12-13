"""Redis-backed tool registry storage.

This module implements persistent storage for tool metadata using Redis.
Tools are stored with a key pattern: `tool:registry:{tool_name}`

Performance characteristics:
- Registration: O(1) Redis SET
- Retrieval: O(1) Redis GET
- Listing: O(N) Redis SCAN (where N = number of tools)

Example:
    >>> import redis
    >>> from blind_ai.core.registry import ToolRegistry, ToolMetadata, TrustLevel
    >>>
    >>> redis_client = redis.Redis(host='localhost', port=6379, db=0)
    >>> registry = ToolRegistry(redis_client)
    >>>
    >>> # Register a tool
    >>> metadata = ToolMetadata(
    ...     name="send_email",
    ...     trust_level=TrustLevel.LOW,
    ...     tool_type="EMAIL"
    ... )
    >>> registry.register(metadata)
    >>>
    >>> # Retrieve tool
    >>> tool = registry.get("send_email")
    >>> print(tool.trust_level)  # TrustLevel.LOW
"""

import json
from typing import Optional

from redis import Redis

from .metadata import ToolMetadata


class ToolRegistry:
    """Redis-backed tool metadata registry.

    Stores and retrieves tool metadata for authorization decisions.

    Attributes:
        redis: Redis client instance
        key_prefix: Redis key prefix (default: "tool:registry:")
    """

    def __init__(self, redis_client: Redis, key_prefix: str = "tool:registry:") -> None:
        """Initialize tool registry.

        Args:
            redis_client: Redis client instance
            key_prefix: Key prefix for tool metadata (default: "tool:registry:")
        """
        self.redis = redis_client
        self.key_prefix = key_prefix

    def _get_key(self, tool_name: str) -> str:
        """Get Redis key for a tool.

        Args:
            tool_name: Tool identifier

        Returns:
            Redis key (e.g., "tool:registry:send_email")
        """
        return f"{self.key_prefix}{tool_name}"

    def register(self, metadata: ToolMetadata) -> None:
        """Register a tool with metadata.

        Args:
            metadata: Tool metadata to register

        Raises:
            ValueError: If tool name is empty
            redis.RedisError: If Redis operation fails

        Example:
            >>> metadata = ToolMetadata(
            ...     name="execute_sql",
            ...     trust_level=TrustLevel.MEDIUM,
            ...     tool_type=ToolType.DATABASE,
            ...     allowed_roles=["admin", "analyst"]
            ... )
            >>> registry.register(metadata)
        """
        if not metadata.name:
            raise ValueError("Tool name cannot be empty")

        key = self._get_key(metadata.name)
        data = json.dumps(metadata.to_dict())

        self.redis.set(key, data)

    def get(self, tool_name: str) -> Optional[ToolMetadata]:
        """Retrieve tool metadata by name.

        Args:
            tool_name: Tool identifier

        Returns:
            ToolMetadata if found, None otherwise

        Example:
            >>> tool = registry.get("send_email")
            >>> if tool and tool.trust_level == TrustLevel.LOW:
            ...     print("Low trust tool - extra validation required")
        """
        key = self._get_key(tool_name)
        data = self.redis.get(key)

        if data is None:
            return None

        try:
            metadata_dict = json.loads(data)
            return ToolMetadata.from_dict(metadata_dict)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Log error but don't crash - treat as missing tool
            # TODO: Add proper logging
            print(f"Warning: Failed to deserialize tool metadata for {tool_name}: {e}")
            return None

    def exists(self, tool_name: str) -> bool:
        """Check if a tool is registered.

        Args:
            tool_name: Tool identifier

        Returns:
            True if tool exists, False otherwise

        Example:
            >>> if registry.exists("send_email"):
            ...     print("Tool is registered")
        """
        key = self._get_key(tool_name)
        return bool(self.redis.exists(key))

    def delete(self, tool_name: str) -> bool:
        """Delete a tool from the registry.

        Args:
            tool_name: Tool identifier

        Returns:
            True if tool was deleted, False if it didn't exist

        Example:
            >>> registry.delete("deprecated_tool")
            True
        """
        key = self._get_key(tool_name)
        return bool(self.redis.delete(key))

    def list_all(self) -> list[ToolMetadata]:
        """List all registered tools.

        Returns:
            List of all tool metadata

        Note:
            This uses SCAN which is O(N). For large registries,
            consider caching or pagination.

        Example:
            >>> tools = registry.list_all()
            >>> for tool in tools:
            ...     print(f"{tool.name}: {tool.trust_level}")
        """
        tools = []
        pattern = f"{self.key_prefix}*"

        # Use SCAN for cursor-based iteration (doesn't block Redis)
        for key in self.redis.scan_iter(match=pattern, count=100):
            data = self.redis.get(key)
            if data:
                try:
                    metadata_dict = json.loads(data)
                    tools.append(ToolMetadata.from_dict(metadata_dict))
                except (json.JSONDecodeError, KeyError, ValueError):
                    # Skip corrupted entries
                    continue

        return tools

    def list_by_trust_level(self, trust_level: str) -> list[ToolMetadata]:
        """List tools by trust level.

        Args:
            trust_level: Trust level to filter by (HIGH/MEDIUM/LOW)

        Returns:
            List of tools with matching trust level

        Example:
            >>> low_trust_tools = registry.list_by_trust_level(TrustLevel.LOW)
            >>> for tool in low_trust_tools:
            ...     print(f"Low trust: {tool.name}")
        """
        all_tools = self.list_all()
        return [t for t in all_tools if t.trust_level.value == trust_level]

    def list_by_type(self, tool_type: str) -> list[ToolMetadata]:
        """List tools by type.

        Args:
            tool_type: Tool type to filter by (DATABASE/API/EMAIL/etc.)

        Returns:
            List of tools with matching type

        Example:
            >>> db_tools = registry.list_by_type(ToolType.DATABASE)
            >>> for tool in db_tools:
            ...     print(f"Database tool: {tool.name}")
        """
        all_tools = self.list_all()
        return [t for t in all_tools if t.tool_type.value == tool_type]

    def clear(self) -> int:
        """Clear all tools from registry.

        Returns:
            Number of tools deleted

        Warning:
            This deletes ALL tools in the registry. Use with caution.

        Example:
            >>> count = registry.clear()
            >>> print(f"Deleted {count} tools")
        """
        pattern = f"{self.key_prefix}*"
        count = 0

        for key in self.redis.scan_iter(match=pattern, count=100):
            self.redis.delete(key)
            count += 1

        return count

    def update(self, metadata: ToolMetadata) -> None:
        """Update an existing tool's metadata.

        Args:
            metadata: Updated tool metadata

        Note:
            This is equivalent to register() - it overwrites existing metadata.

        Example:
            >>> tool = registry.get("send_email")
            >>> tool.rate_limit_per_minute = 50  # Update limit
            >>> registry.update(tool)
        """
        self.register(metadata)  # SET overwrites in Redis
