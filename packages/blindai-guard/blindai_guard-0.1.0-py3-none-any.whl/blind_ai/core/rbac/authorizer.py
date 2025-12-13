"""RBAC authorization logic for tool access control."""

from typing import Optional

from ..ratelimit import RateLimiter, RateLimitExceeded
from ..registry import ToolMetadata, ToolRegistry
from .models import Permission, UserContext


class AuthorizationError(Exception):
    """Raised when authorization fails."""

    pass


class RBACAuthorizer:
    """Handles role-based authorization for tool execution.

    Integrates with ToolRegistry to enforce allowed_roles restrictions
    and rate limiting.
    """

    def __init__(
        self,
        tool_registry: Optional[ToolRegistry] = None,
        rate_limiter: Optional[RateLimiter] = None,
    ):
        """Initialize authorizer.

        Args:
            tool_registry: Tool registry for metadata lookup
            rate_limiter: Rate limiter for enforcement
        """
        self.tool_registry = tool_registry
        self.rate_limiter = rate_limiter

    def authorize_tool_execution(
        self, user: UserContext, tool_name: str, tool_metadata: Optional[ToolMetadata] = None
    ) -> None:
        """Authorize user to execute a tool.

        Args:
            user: User context
            tool_name: Tool to execute
            tool_metadata: Optional pre-fetched metadata (avoids registry lookup)

        Raises:
            AuthorizationError: If user lacks permission
            RateLimitExceeded: If rate limit exceeded
        """
        # Check basic execute permission
        if not user.has_permission(Permission.EXECUTE):
            raise AuthorizationError(
                f"User {user.user_id} lacks EXECUTE permission"
            )

        # Get tool metadata if not provided
        if tool_metadata is None and self.tool_registry:
            tool_metadata = self.tool_registry.get(tool_name)

        # If tool has role restrictions, check them
        if tool_metadata and tool_metadata.allowed_roles:
            if not user.can_execute_tool(tool_metadata.allowed_roles):
                raise AuthorizationError(
                    f"User role {user.role.value} not in allowed roles {tool_metadata.allowed_roles} for tool {tool_name}"
                )

        # Check rate limits
        if self.rate_limiter and tool_metadata and tool_metadata.rate_limit_per_minute:
            rate_key = f"user:{user.user_id}:tool:{tool_name}"
            self.rate_limiter.check_rate_limit(
                key=rate_key,
                limit=tool_metadata.rate_limit_per_minute,
                window_seconds=60,
            )

    def authorize_tool_registration(self, user: UserContext) -> None:
        """Authorize user to register tools.

        Args:
            user: User context

        Raises:
            AuthorizationError: If user lacks permission
        """
        if not user.has_permission(Permission.REGISTER):
            raise AuthorizationError(
                f"User {user.user_id} lacks REGISTER permission"
            )

    def authorize_tool_deletion(self, user: UserContext) -> None:
        """Authorize user to delete tools.

        Args:
            user: User context

        Raises:
            AuthorizationError: If user lacks permission
        """
        if not user.has_permission(Permission.DELETE):
            raise AuthorizationError(
                f"User {user.user_id} lacks DELETE permission"
            )
