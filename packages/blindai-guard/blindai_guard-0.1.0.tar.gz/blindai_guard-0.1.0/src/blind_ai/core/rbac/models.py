"""RBAC data models for user context, roles, and permissions."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class Permission(str, Enum):
    """Standard permissions for tool operations."""

    READ = "READ"  # View tool metadata
    EXECUTE = "EXECUTE"  # Execute tools
    REGISTER = "REGISTER"  # Register new tools
    DELETE = "DELETE"  # Delete tools
    ADMIN = "ADMIN"  # Full administrative access


class Role(str, Enum):
    """Standard roles with predefined permissions."""

    GUEST = "GUEST"  # Read-only access
    USER = "USER"  # Execute trusted tools
    POWER_USER = "POWER_USER"  # Execute all tools
    ADMIN = "ADMIN"  # Full access


# Role -> Permission mapping
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.GUEST: {Permission.READ},
    Role.USER: {Permission.READ, Permission.EXECUTE},
    Role.POWER_USER: {Permission.READ, Permission.EXECUTE},
    Role.ADMIN: {Permission.READ, Permission.EXECUTE, Permission.REGISTER, Permission.DELETE, Permission.ADMIN},
}


@dataclass
class UserContext:
    """User context for authorization decisions.

    Attributes:
        user_id: Unique user identifier
        role: User's primary role
        permissions: Additional permissions beyond role
        session_id: Optional session identifier for tracking
        metadata: Additional user metadata (department, region, etc.)
        created_at: Context creation timestamp
    """

    user_id: str
    role: Role
    permissions: set[Permission] = field(default_factory=set)
    session_id: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        """Validate and normalize user context."""
        if not self.user_id:
            raise ValueError("user_id cannot be empty")

        # Convert string role to enum
        if isinstance(self.role, str):
            self.role = Role(self.role.upper())

        # Convert string permissions to enums
        if self.permissions:
            self.permissions = {
                Permission(p.upper()) if isinstance(p, str) else p
                for p in self.permissions
            }

    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission.

        Args:
            permission: Permission to check

        Returns:
            True if user has permission (via role or explicit grant)
        """
        # Admin role has all permissions
        if self.role == Role.ADMIN:
            return True

        # Check role permissions
        role_perms = ROLE_PERMISSIONS.get(self.role, set())
        if permission in role_perms:
            return True

        # Check explicit permissions
        return permission in self.permissions

    def can_execute_tool(self, tool_allowed_roles: list[str]) -> bool:
        """Check if user can execute a tool based on allowed_roles.

        Args:
            tool_allowed_roles: List of allowed roles from tool metadata

        Returns:
            True if user's role is in allowed list or list is empty
        """
        # Empty list means no restrictions
        if not tool_allowed_roles:
            return True

        # Check if user's role is allowed
        return self.role.value in tool_allowed_roles

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "user_id": self.user_id,
            "role": self.role.value,
            "permissions": [p.value for p in self.permissions],
            "session_id": self.session_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserContext":
        """Deserialize from dictionary."""
        return cls(
            user_id=data["user_id"],
            role=Role(data["role"]),
            permissions={Permission(p) for p in data.get("permissions", [])},
            session_id=data.get("session_id"),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"])
            if "created_at" in data
            else datetime.utcnow(),
        )
