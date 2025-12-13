"""Chain tracking and pattern detection."""

from typing import Optional

from .models import ChainPattern, ToolCall, ToolChain


# Built-in suspicious patterns
DEFAULT_PATTERNS = [
    ChainPattern(
        name="data_exfiltration",
        sequence=["query_database", "send_email"],
        description="Query followed by external communication",
        severity="high",
    ),
    ChainPattern(
        name="privilege_escalation",
        sequence=["list_users", "modify_user", "query_database"],
        description="User enumeration -> modification -> data access",
        severity="critical",
    ),
    ChainPattern(
        name="recon_and_attack",
        sequence=["search_files", "read_file", "execute_command"],
        description="File discovery -> read -> execution",
        severity="high",
    ),
]


class ChainTracker:
    """Tracks tool call chains and detects patterns."""

    def __init__(self, patterns: Optional[list[ChainPattern]] = None):
        """Initialize tracker.

        Args:
            patterns: Custom patterns (defaults to built-in patterns)
        """
        self.patterns = patterns or DEFAULT_PATTERNS
        self.sessions: dict[str, ToolChain] = {}

    def record_call(
        self,
        session_id: str,
        tool_name: str,
        parameters: dict,
        user_id: Optional[str] = None,
    ) -> ToolChain:
        """Record a tool call and return updated chain.

        Args:
            session_id: Session identifier
            tool_name: Tool that was called
            parameters: Tool parameters
            user_id: User making the call

        Returns:
            Updated tool chain
        """
        # Get or create chain
        if session_id not in self.sessions:
            self.sessions[session_id] = ToolChain(session_id=session_id, user_id=user_id)

        chain = self.sessions[session_id]

        # Add call
        call = ToolCall(
            tool_name=tool_name,
            parameters=parameters,
            user_id=user_id,
            session_id=session_id,
        )
        chain.add_call(call)

        return chain

    def detect_patterns(self, session_id: str) -> list[ChainPattern]:
        """Detect matching patterns in a session's chain.

        Args:
            session_id: Session to check

        Returns:
            List of matched patterns
        """
        if session_id not in self.sessions:
            return []

        chain = self.sessions[session_id]
        matched = []

        for pattern in self.patterns:
            if chain.matches_pattern(pattern):
                matched.append(pattern)

        return matched

    def get_chain(self, session_id: str) -> Optional[ToolChain]:
        """Get tool chain for a session.

        Args:
            session_id: Session identifier

        Returns:
            Tool chain or None if not found
        """
        return self.sessions.get(session_id)

    def clear_session(self, session_id: str) -> None:
        """Clear a session's chain.

        Args:
            session_id: Session to clear
        """
        if session_id in self.sessions:
            del self.sessions[session_id]

    def add_pattern(self, pattern: ChainPattern) -> None:
        """Add a custom pattern.

        Args:
            pattern: Pattern to add
        """
        self.patterns.append(pattern)
