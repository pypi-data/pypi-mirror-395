"""Tool metadata models for Layer 2 authorization.

This module defines the metadata models used to describe tools in the registry:
- TrustLevel: HIGH, MEDIUM, LOW security classification
- ToolType: DATABASE, API, EMAIL, FILE, COMMAND, etc.
- ToolMetadata: Complete tool description with security attributes

Trust levels guide policy decisions:
- HIGH: Trusted internal tools (read-only queries, safe operations)
- MEDIUM: Moderate risk tools (write operations, external APIs with validation)
- LOW: Untrusted tools (external communication, data exfiltration risk)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..validation import ParameterSchema


class TrustLevel(str, Enum):
    """Security trust level for tools.

    Trust levels indicate the inherent risk of a tool and guide policy decisions.

    Attributes:
        HIGH: Trusted internal tools with minimal risk
            - Read-only database queries
            - Safe calculation functions
            - Internal API calls to trusted services
        MEDIUM: Moderate risk tools requiring validation
            - Write operations to internal systems
            - External API calls with input validation
            - File operations in controlled directories
        LOW: Untrusted tools with high risk
            - External communication (email, webhooks)
            - Arbitrary command execution
            - File operations in sensitive directories
            - Data exfiltration vectors
    """

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ToolType(str, Enum):
    """Functional classification of tools.

    Tool types enable policy rules based on functionality.

    Example:
        >>> # Block all database tools for non-admin users
        >>> condition: "tool.tool_type == 'DATABASE' and user.role != 'admin'"
    """

    DATABASE = "DATABASE"  # SQL queries, database operations
    API = "API"  # External API calls
    EMAIL = "EMAIL"  # Email sending
    COMMUNICATION = "COMMUNICATION"  # Webhooks, Slack, etc.
    FILE = "FILE"  # File read/write operations
    COMMAND = "COMMAND"  # Shell command execution
    SEARCH = "SEARCH"  # Web search, document search
    CALCULATION = "CALCULATION"  # Math, data processing
    OTHER = "OTHER"  # Uncategorized tools


@dataclass
class ToolMetadata:
    """Complete metadata for a registered tool.

    Attributes:
        name: Unique tool identifier (e.g., "send_email", "execute_sql")
        trust_level: Security classification (HIGH/MEDIUM/LOW)
        tool_type: Functional classification (DATABASE/API/EMAIL/etc.)
        description: Human-readable description of tool purpose
        allowed_domains: Whitelist of domains for external calls (optional)
        allowed_roles: Roles permitted to use this tool (optional, empty = all)
        rate_limit_per_minute: Max calls per minute per user (optional)
        require_approval: Whether calls require human approval (default: False)
        metadata: Additional custom metadata (optional)

    Example:
        >>> metadata = ToolMetadata(
        ...     name="send_email",
        ...     trust_level=TrustLevel.LOW,
        ...     tool_type=ToolType.EMAIL,
        ...     description="Send email to external recipients",
        ...     allowed_domains=["company.com", "partner.com"],
        ...     allowed_roles=["user", "admin"],
        ...     rate_limit_per_minute=100
        ... )
    """

    name: str
    trust_level: TrustLevel
    tool_type: ToolType
    description: str = ""
    allowed_domains: list[str] = field(default_factory=list)
    allowed_roles: list[str] = field(default_factory=list)
    rate_limit_per_minute: Optional[int] = None
    require_approval: bool = False
    parameter_schemas: dict[str, "ParameterSchema"] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate metadata after initialization."""
        if not self.name:
            raise ValueError("Tool name cannot be empty")

        # Convert string enums to enum instances if needed
        if isinstance(self.trust_level, str):
            self.trust_level = TrustLevel(self.trust_level)
        if isinstance(self.tool_type, str):
            self.tool_type = ToolType(self.tool_type)

        # Validate trust level
        if self.trust_level not in TrustLevel:
            raise ValueError(
                f"Invalid trust_level: {self.trust_level}. "
                f"Must be one of {[e.value for e in TrustLevel]}"
            )

        # Validate tool type
        if self.tool_type not in ToolType:
            raise ValueError(
                f"Invalid tool_type: {self.tool_type}. "
                f"Must be one of {[e.value for e in ToolType]}"
            )

        # Validate rate limit
        if self.rate_limit_per_minute is not None and self.rate_limit_per_minute <= 0:
            raise ValueError("rate_limit_per_minute must be positive")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation suitable for JSON/Redis storage
        """
        return {
            "name": self.name,
            "trust_level": self.trust_level.value,
            "tool_type": self.tool_type.value,
            "description": self.description,
            "allowed_domains": self.allowed_domains,
            "allowed_roles": self.allowed_roles,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "require_approval": self.require_approval,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToolMetadata":
        """Create from dictionary.

        Args:
            data: Dictionary with tool metadata

        Returns:
            ToolMetadata instance
        """
        return cls(
            name=data["name"],
            trust_level=TrustLevel(data["trust_level"]),
            tool_type=ToolType(data["tool_type"]),
            description=data.get("description", ""),
            allowed_domains=data.get("allowed_domains", []),
            allowed_roles=data.get("allowed_roles", []),
            rate_limit_per_minute=data.get("rate_limit_per_minute"),
            require_approval=data.get("require_approval", False),
            metadata=data.get("metadata", {}),
        )

    def is_allowed_for_role(self, role: str) -> bool:
        """Check if a role is allowed to use this tool.

        Args:
            role: User role to check

        Returns:
            True if role is allowed (or no restrictions), False otherwise
        """
        # Empty allowed_roles means no restrictions
        if not self.allowed_roles:
            return True

        return role in self.allowed_roles

    def is_domain_allowed(self, domain: str) -> bool:
        """Check if a domain is in the allowed list.

        Args:
            domain: Domain to check (e.g., "example.com")

        Returns:
            True if domain is allowed (or no restrictions), False otherwise
        """
        # Empty allowed_domains means no restrictions
        if not self.allowed_domains:
            return True

        # Exact match
        if domain in self.allowed_domains:
            return True

        # Subdomain match (e.g., "api.company.com" matches "company.com")
        for allowed in self.allowed_domains:
            if domain.endswith(f".{allowed}"):
                return True

        return False
