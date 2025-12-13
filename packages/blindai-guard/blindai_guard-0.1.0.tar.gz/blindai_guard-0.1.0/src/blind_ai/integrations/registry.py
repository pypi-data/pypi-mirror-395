"""Tool registry utilities for Blind AI integrations.

Provides automatic tool registration and inference of security metadata.
"""

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)

# Default confidence thresholds
LOW_CONFIDENCE_THRESHOLD = 0.3
MEDIUM_CONFIDENCE_THRESHOLD = 0.6


class ConfidenceLevel(Enum):
    """Confidence level categories."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"


@dataclass
class RegistryConfig:
    """Configuration for tool registry inference.
    
    Controls confidence thresholds and behavior for auto-registration.
    
    Attributes:
        min_confidence_threshold: Minimum confidence to accept without warning
        require_manual_review_below: Confidence below which manual review is recommended
        strict_mode: If True, raise error when confidence is too low
        default_tool_type: Default tool type when inference fails
        default_trust_level: Default trust level when inference fails
        
    Example:
        ```python
        from blind_ai.integrations import RegistryConfig, infer_tool_type
        
        # Strict configuration
        config = RegistryConfig(
            min_confidence_threshold=0.5,
            require_manual_review_below=0.7,
            strict_mode=True,
        )
        
        tool_type, conf = infer_tool_type(name, desc, return_confidence=True)
        
        if config.should_reject(conf):
            raise ValueError(f"Confidence too low: {conf:.2f}")
        
        if config.needs_review(conf):
            logger.warning(f"Manual review recommended for {name}")
        ```
    """
    min_confidence_threshold: float = LOW_CONFIDENCE_THRESHOLD
    require_manual_review_below: float = MEDIUM_CONFIDENCE_THRESHOLD
    strict_mode: bool = False
    default_tool_type: str = "OTHER"
    default_trust_level: str = "MEDIUM"
    
    def __post_init__(self):
        """Validate configuration."""
        if not 0 <= self.min_confidence_threshold <= 1:
            raise ValueError("min_confidence_threshold must be between 0 and 1")
        if not 0 <= self.require_manual_review_below <= 1:
            raise ValueError("require_manual_review_below must be between 0 and 1")
        if self.min_confidence_threshold > self.require_manual_review_below:
            raise ValueError(
                "min_confidence_threshold should be <= require_manual_review_below"
            )
    
    def get_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Get the confidence level category.
        
        Args:
            confidence: Confidence score (0.0-1.0)
            
        Returns:
            ConfidenceLevel enum value
        """
        if confidence >= self.require_manual_review_below:
            return ConfidenceLevel.HIGH
        elif confidence >= self.min_confidence_threshold:
            return ConfidenceLevel.MEDIUM
        elif confidence > 0:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def should_warn(self, confidence: float) -> bool:
        """Check if confidence is low enough to warrant a warning.
        
        Args:
            confidence: Confidence score (0.0-1.0)
            
        Returns:
            True if warning should be logged
        """
        return confidence < self.min_confidence_threshold
    
    def needs_review(self, confidence: float) -> bool:
        """Check if confidence is low enough to recommend manual review.
        
        Args:
            confidence: Confidence score (0.0-1.0)
            
        Returns:
            True if manual review is recommended
        """
        return confidence < self.require_manual_review_below
    
    def should_reject(self, confidence: float) -> bool:
        """Check if confidence is too low to accept (in strict mode).
        
        Args:
            confidence: Confidence score (0.0-1.0)
            
        Returns:
            True if should reject (only in strict_mode)
        """
        return self.strict_mode and confidence < self.min_confidence_threshold
    
    def validate_inference(
        self,
        name: str,
        inferred_value: str,
        confidence: float,
        value_type: str = "tool type",
    ) -> str:
        """Validate an inference result and handle low confidence.
        
        Args:
            name: Tool name being registered
            inferred_value: The inferred value (tool type or trust level)
            confidence: Confidence score
            value_type: Description of what was inferred ("tool type" or "trust level")
            
        Returns:
            The inferred value (or default if rejected)
            
        Raises:
            ValueError: If strict_mode is True and confidence is too low
        """
        level = self.get_confidence_level(confidence)
        
        if level == ConfidenceLevel.VERY_LOW:
            if self.strict_mode:
                raise ValueError(
                    f"Cannot infer {value_type} for '{name}': confidence is {confidence:.2f}. "
                    f"Please specify {value_type} explicitly."
                )
            logger.warning(
                f"Very low confidence ({confidence:.2f}) inferring {value_type} for '{name}'. "
                f"Using default: {self.default_tool_type if value_type == 'tool type' else self.default_trust_level}"
            )
            return self.default_tool_type if value_type == "tool type" else self.default_trust_level
        
        elif level == ConfidenceLevel.LOW:
            if self.strict_mode:
                raise ValueError(
                    f"Low confidence ({confidence:.2f}) inferring {value_type} for '{name}'. "
                    f"In strict mode, please specify {value_type} explicitly."
                )
            logger.warning(
                f"Low confidence ({confidence:.2f}) inferring {value_type} for '{name}' as {inferred_value}. "
                f"Consider specifying {value_type} explicitly."
            )
        
        elif level == ConfidenceLevel.MEDIUM:
            logger.info(
                f"Medium confidence ({confidence:.2f}) inferring {value_type} for '{name}' as {inferred_value}."
            )
        
        # HIGH confidence - no logging needed
        return inferred_value


# Global default configuration
_default_config = RegistryConfig()


def get_registry_config() -> RegistryConfig:
    """Get the current global registry configuration."""
    return _default_config


def set_registry_config(config: RegistryConfig) -> None:
    """Set the global registry configuration.
    
    Args:
        config: New configuration to use globally
        
    Example:
        ```python
        from blind_ai.integrations import RegistryConfig, set_registry_config
        
        # Use stricter thresholds globally
        set_registry_config(RegistryConfig(
            min_confidence_threshold=0.5,
            strict_mode=True,
        ))
        ```
    """
    global _default_config
    _default_config = config
    logger.info(
        f"Registry config updated: min_threshold={config.min_confidence_threshold}, "
        f"review_below={config.require_manual_review_below}, strict={config.strict_mode}"
    )

# Keywords for inferring tool types (ordered by specificity)
TOOL_TYPE_KEYWORDS: Dict[str, List[str]] = {
    "DATABASE": [
        "sql", "query", "database", "db", "select", "insert", "update", "delete",
        "postgres", "mysql", "sqlite", "mongodb", "redis", "dynamodb", "table",
        "execute_sql", "run_query",
    ],
    "API": [
        "api", "http", "request", "fetch", "post", "rest", "graphql",
        "endpoint", "webhook", "url", "web",
    ],
    "EMAIL": [
        "email", "mail", "smtp", "send_email", "inbox", "gmail",
        "outlook", "sendgrid",
    ],
    "FILE": [
        "file", "read_file", "write_file", "open", "save", "load", "path", "directory",
        "folder", "upload", "download", "storage", "s3", "blob",
    ],
    "COMMAND": [
        "shell", "bash", "command", "terminal", "subprocess",
        "system", "os", "cmd", "powershell",
    ],
    "COMMUNICATION": [
        "slack", "teams", "discord", "chat", "notify", "notification", "sms",
        "twilio", "telegram", "webhook",
    ],
    "SEARCH": [
        "search", "find", "lookup", "query", "index", "elasticsearch", "vector",
        "semantic", "retrieval", "rag",
    ],
    "CODE": [
        "code", "python", "javascript", "execute", "eval", "compile", "script",
        "interpreter", "repl",
    ],
}

# Keywords for inferring trust levels
HIGH_RISK_KEYWORDS: Set[str] = {
    "delete", "drop", "truncate", "remove", "destroy", "kill", "terminate",
    "shell", "bash", "exec", "system", "command", "sudo", "admin", "root",
    "password", "secret", "credential", "token", "key", "auth",
    "send", "email", "sms", "notify", "external", "public",
    "write", "modify", "update", "insert", "create",
}

MEDIUM_RISK_KEYWORDS: Set[str] = {
    "read", "get", "fetch", "query", "select", "list", "search", "find",
    "api", "http", "request", "download", "load",
}

LOW_RISK_KEYWORDS: Set[str] = {
    "format", "parse", "validate", "check", "verify", "calculate", "compute",
    "convert", "transform", "encode", "decode", "hash",
}


def infer_tool_type(
    name: str,
    description: str = "",
    func: Optional[Any] = None,
    return_confidence: bool = False,
) -> Union[str, Tuple[str, float]]:
    """Infer tool type from name, description, and function.
    
    Args:
        name: Tool name
        description: Tool description
        func: Optional function object (for docstring inspection)
        return_confidence: If True, return (tool_type, confidence) tuple
        
    Returns:
        Inferred tool type (e.g., "DATABASE", "API", "FILE")
        If return_confidence=True, returns (tool_type, confidence) tuple
        where confidence is 0.0-1.0
        
    Example:
        ```python
        tool_type = infer_tool_type("execute_sql", "Run SQL queries")
        # Returns: "DATABASE"
        
        # With confidence score
        tool_type, confidence = infer_tool_type(
            "fuzzy_name", "vague description", 
            return_confidence=True
        )
        if confidence < 0.5:
            logger.warning(f"Low confidence ({confidence:.2f}) for tool type")
        ```
    """
    # Combine all text for analysis
    text_parts = [name.lower(), description.lower()]
    
    # Add docstring if available
    if func and hasattr(func, '__doc__') and func.__doc__:
        text_parts.append(func.__doc__.lower())
    
    combined_text = " ".join(text_parts)
    
    # Score each tool type
    scores: Dict[str, int] = {}
    max_possible_scores: Dict[str, int] = {}
    
    for tool_type, keywords in TOOL_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined_text)
        if score > 0:
            scores[tool_type] = score
        max_possible_scores[tool_type] = len(keywords)
    
    # Calculate result and confidence
    if scores:
        best_type = max(scores, key=scores.get)
        best_score = scores[best_type]
        
        # Confidence based on:
        # 1. How many keywords matched vs total keywords for that type
        # 2. How much better the best score is vs second best
        keyword_ratio = best_score / max_possible_scores[best_type]
        
        # Get second best score for comparison
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) > 1:
            score_gap = (best_score - sorted_scores[1]) / best_score
        else:
            score_gap = 1.0  # Only one match = high confidence in that match
        
        # Combined confidence (weighted average)
        confidence = min(1.0, (keyword_ratio * 0.6) + (score_gap * 0.4) + (0.1 * min(best_score, 3)))
        confidence = round(confidence, 2)
        
        if return_confidence:
            return best_type, confidence
        return best_type
    
    # No match
    if return_confidence:
        return "OTHER", 0.0
    return "OTHER"


def infer_trust_level(
    name: str,
    description: str = "",
    tool_type: Optional[str] = None,
    func: Optional[Any] = None,
    return_confidence: bool = False,
) -> Union[str, Tuple[str, float]]:
    """Infer trust level from tool metadata.
    
    Trust levels:
    - LOW: High-risk operations (write, delete, execute, send)
    - MEDIUM: Read operations, API calls
    - HIGH: Safe operations (format, validate, calculate)
    
    Args:
        name: Tool name
        description: Tool description
        tool_type: Optional pre-determined tool type
        func: Optional function object
        return_confidence: If True, return (trust_level, confidence) tuple
        
    Returns:
        Inferred trust level ("HIGH", "MEDIUM", or "LOW")
        If return_confidence=True, returns (trust_level, confidence) tuple
        
    Example:
        ```python
        trust = infer_trust_level("delete_user", "Delete a user from database")
        # Returns: "LOW" (high risk = low trust)
        
        # With confidence score
        trust, confidence = infer_trust_level(
            "ambiguous_tool", "",
            return_confidence=True
        )
        if confidence < 0.5:
            logger.warning(f"Low confidence ({confidence:.2f}) for trust level")
        ```
    """
    # Combine all text for analysis
    text_parts = [name.lower(), description.lower()]
    
    if func and hasattr(func, '__doc__') and func.__doc__:
        text_parts.append(func.__doc__.lower())
    
    combined_text = " ".join(text_parts)
    
    # Check for high-risk keywords first (LOW trust)
    high_risk_score = sum(1 for kw in HIGH_RISK_KEYWORDS if kw in combined_text)
    
    # Check for medium-risk keywords
    medium_risk_score = sum(1 for kw in MEDIUM_RISK_KEYWORDS if kw in combined_text)
    
    # Check for low-risk keywords (HIGH trust)
    low_risk_score = sum(1 for kw in LOW_RISK_KEYWORDS if kw in combined_text)
    
    # Tool type also influences trust
    high_risk_types = {"COMMAND", "EMAIL", "COMMUNICATION", "CODE"}
    medium_risk_types = {"DATABASE", "API", "FILE"}
    
    if tool_type in high_risk_types:
        high_risk_score += 2
    elif tool_type in medium_risk_types:
        medium_risk_score += 1
    
    # Calculate total evidence
    total_score = high_risk_score + medium_risk_score + low_risk_score
    
    # Determine trust level and confidence
    if total_score == 0:
        # No keywords matched - low confidence default
        trust_level = "MEDIUM"
        confidence = 0.2
    elif high_risk_score > medium_risk_score and high_risk_score > low_risk_score:
        trust_level = "LOW"  # High risk = low trust
        # Confidence based on how dominant high_risk is
        confidence = high_risk_score / total_score
        # Boost confidence if score is high
        confidence = min(1.0, confidence + (0.1 * min(high_risk_score, 3)))
    elif low_risk_score > medium_risk_score and low_risk_score > high_risk_score:
        trust_level = "HIGH"  # Low risk = high trust
        confidence = low_risk_score / total_score
        confidence = min(1.0, confidence + (0.1 * min(low_risk_score, 3)))
    else:
        trust_level = "MEDIUM"
        # Medium confidence when scores are close
        if total_score > 0:
            confidence = medium_risk_score / total_score
            confidence = min(1.0, confidence + 0.2)  # Slight boost for having evidence
        else:
            confidence = 0.3
    
    confidence = round(confidence, 2)
    
    if return_confidence:
        return trust_level, confidence
    return trust_level


def extract_allowed_domains(description: str) -> List[str]:
    """Extract potential allowed domains from description.
    
    Args:
        description: Tool description
        
    Returns:
        List of extracted domains
    """
    # Simple domain extraction pattern
    domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    domains = re.findall(domain_pattern, description)
    
    # Filter out common non-domain patterns
    excluded = {'e.g.', 'i.e.', 'etc.', 'vs.'}
    return [d for d in domains if d.lower() not in excluded]


def auto_register_tool(
    guard,
    name: str,
    description: str = "",
    func: Optional[Any] = None,
    trust_level: Optional[str] = None,
    tool_type: Optional[str] = None,
    allowed_domains: Optional[List[str]] = None,
    allowed_roles: Optional[List[str]] = None,
    rate_limit_per_minute: Optional[int] = None,
    require_approval: Optional[bool] = None,
    metadata: Optional[Dict[str, Any]] = None,
    fail_silently: bool = True,
    config: Optional[RegistryConfig] = None,
) -> bool:
    """Auto-register a tool with the guard's tool registry.
    
    Infers trust_level and tool_type if not provided.
    Uses configurable confidence thresholds for validation.
    
    Args:
        guard: ToolGuard or AsyncToolGuard instance
        name: Tool name
        description: Tool description
        func: Optional function for additional inference
        trust_level: Override inferred trust level
        tool_type: Override inferred tool type
        allowed_domains: List of allowed domains
        allowed_roles: List of allowed roles
        rate_limit_per_minute: Rate limit
        require_approval: Whether to require human approval
        metadata: Additional metadata
        fail_silently: If True, log errors but don't raise
        config: Optional RegistryConfig for confidence thresholds
        
    Returns:
        True if registration succeeded, False otherwise
        
    Raises:
        ValueError: If config.strict_mode is True and confidence is too low
        
    Example:
        ```python
        from blind_ai.integrations.registry import auto_register_tool, RegistryConfig
        
        # With default config
        auto_register_tool(
            guard=guard,
            name="execute_sql",
            description="Execute SQL queries against the database",
            trust_level="LOW",  # Override inference
        )
        
        # With strict config
        strict_config = RegistryConfig(strict_mode=True, min_confidence_threshold=0.5)
        auto_register_tool(
            guard=guard,
            name="my_tool",
            description="Does something",
            config=strict_config,  # Will raise if confidence < 0.5
        )
        ```
    """
    # Use provided config or global default
    cfg = config or get_registry_config()
    
    # Infer tool type if not provided (with confidence)
    type_confidence = 1.0
    if tool_type:
        inferred_type = tool_type
    else:
        inferred_type, type_confidence = infer_tool_type(
            name, description, func, return_confidence=True
        )
        # Validate using config (may raise in strict mode)
        try:
            inferred_type = cfg.validate_inference(
                name, inferred_type, type_confidence, "tool type"
            )
        except ValueError:
            if fail_silently:
                logger.error(f"Failed to infer tool type for '{name}' in strict mode")
                return False
            raise
    
    # Infer trust level if not provided (with confidence)
    trust_confidence = 1.0
    if trust_level:
        inferred_trust = trust_level
    else:
        inferred_trust, trust_confidence = infer_trust_level(
            name, description, inferred_type, func, return_confidence=True
        )
        # Validate using config (may raise in strict mode)
        try:
            inferred_trust = cfg.validate_inference(
                name, inferred_trust, trust_confidence, "trust level"
            )
        except ValueError:
            if fail_silently:
                logger.error(f"Failed to infer trust level for '{name}' in strict mode")
                return False
            raise
    
    # Infer require_approval based on trust level if not specified
    if require_approval is None:
        require_approval = inferred_trust == "LOW"
    
    # Extract domains from description if not provided
    if allowed_domains is None:
        allowed_domains = extract_allowed_domains(description)
    
    try:
        # Check if guard has register_tool method
        if not hasattr(guard, 'register_tool'):
            logger.debug(f"Guard does not support tool registration, skipping {name}")
            return False
        
        guard.register_tool(
            name=name,
            trust_level=inferred_trust,
            tool_type=inferred_type,
            description=description,
            allowed_domains=allowed_domains,
            allowed_roles=allowed_roles,
            rate_limit_per_minute=rate_limit_per_minute,
            require_approval=require_approval,
            metadata=metadata,
        )
        
        logger.info(
            f"Auto-registered tool '{name}' "
            f"(type={inferred_type} [{type_confidence:.0%}], "
            f"trust={inferred_trust} [{trust_confidence:.0%}])"
        )
        return True
        
    except Exception as e:
        if fail_silently:
            logger.warning(f"Failed to auto-register tool '{name}': {e}")
            return False
        raise


class ToolRegistryMixin:
    """Mixin class that adds auto-registration to tool wrappers.
    
    Add this to wrapper classes to enable automatic tool registration.
    
    Example:
        ```python
        class MyToolWrapper(ToolRegistryMixin):
            def __init__(self, tool, guard, auto_register=True):
                self.tool = tool
                self.guard = guard
                
                if auto_register:
                    self._auto_register()
        ```
    """
    
    # Subclasses should set these
    tool: Any = None
    guard: Any = None
    
    def _get_tool_name(self) -> str:
        """Get tool name for registration."""
        if hasattr(self, 'name') and self.name:
            return self.name
        if hasattr(self.tool, 'name') and self.tool.name:
            return self.tool.name
        if hasattr(self.tool, '__name__'):
            return self.tool.__name__
        return "unknown_tool"
    
    def _get_tool_description(self) -> str:
        """Get tool description for registration."""
        if hasattr(self, 'description') and self.description:
            return self.description
        if hasattr(self.tool, 'description') and self.tool.description:
            return self.tool.description
        if hasattr(self.tool, '__doc__') and self.tool.__doc__:
            return self.tool.__doc__.split('\n')[0]  # First line
        return ""
    
    def _get_tool_func(self) -> Optional[Any]:
        """Get underlying function for inference."""
        if hasattr(self.tool, 'func'):
            return self.tool.func
        if hasattr(self.tool, '_run'):
            return self.tool._run
        if callable(self.tool):
            return self.tool
        return None
    
    def _auto_register(
        self,
        trust_level: Optional[str] = None,
        tool_type: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """Auto-register this tool with the guard.
        
        Args:
            trust_level: Override inferred trust level
            tool_type: Override inferred tool type
            **kwargs: Additional registration parameters
            
        Returns:
            True if registration succeeded
        """
        return auto_register_tool(
            guard=self.guard,
            name=self._get_tool_name(),
            description=self._get_tool_description(),
            func=self._get_tool_func(),
            trust_level=trust_level,
            tool_type=tool_type,
            **kwargs,
        )
