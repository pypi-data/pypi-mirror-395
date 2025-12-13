"""Policy engine for Blind AI.

Evaluates detection results against YAML-defined policies to determine
final actions (ALLOW, BLOCK, CHALLENGE, LOG).

Policy Rules:
- Conditions: Check detection properties (severity, threat_type, etc.)
- Actions: ALLOW, BLOCK, CHALLENGE, LOG
- Priority: Higher priority rules evaluated first
- Custom functions: contains_pii(), count_threats(), etc.

Example Policy:
```yaml
name: "Default Security Policy"
version: "1.0"
rules:
  - name: "Block critical SQL injections"
    condition: "severity == 'critical' and threat_type == 'sql_injection'"
    action: BLOCK
    priority: 100

  - name: "Challenge high severity threats"
    condition: "severity == 'high'"
    action: CHALLENGE
    priority: 50
```
"""

import ast
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from blind_ai.core.detection.static import ActionType, DetectionResult, ThreatType

# Module logger
logger = logging.getLogger(__name__)


class PolicyAction(Enum):
    """Actions that can be taken based on policy evaluation."""

    ALLOW = "allow"
    BLOCK = "block"
    CHALLENGE = "challenge"
    LOG = "log"


@dataclass
class PolicyRule:
    """A single policy rule.

    Attributes:
        name: Human-readable rule name
        condition: Python expression to evaluate (e.g., "severity == 'critical'")
        action: Action to take if condition is true
        priority: Rule priority (higher = evaluated first)
        enabled: Whether rule is active
        description: Optional description of what rule does
    """

    name: str
    condition: str
    action: PolicyAction
    priority: int = 0
    enabled: bool = True
    description: str = ""

    def __post_init__(self) -> None:
        """Validate rule after initialization."""
        if not self.name:
            raise ValueError("Rule name cannot be empty")
        if not self.condition:
            raise ValueError("Rule condition cannot be empty")


@dataclass
class Policy:
    """A collection of policy rules.

    Attributes:
        name: Policy name
        version: Policy version
        rules: List of policy rules
        metadata: Optional metadata (author, created_at, etc.)
    """

    name: str
    version: str
    rules: list[PolicyRule] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Sort rules by priority after initialization."""
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def add_rule(self, rule: PolicyRule) -> None:
        """Add a rule and re-sort by priority."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)


class SafeEvaluator:
    """Safe evaluator for policy condition expressions.

    Uses Python AST to parse and evaluate expressions in a restricted environment.
    Only allows safe operations (comparisons, boolean logic, literals).

    Security:
    - No function calls except whitelisted custom functions
    - No attribute access except on known safe objects
    - No imports or code execution
    - No file I/O or network access
    """

    # Allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.Compare,
        ast.BoolOp,
        ast.UnaryOp,
        ast.BinOp,
        ast.Name,
        ast.Constant,
        ast.Load,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.In,
        ast.NotIn,
        ast.Is,
        ast.IsNot,
        ast.And,
        ast.Or,
        ast.Not,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.List,
        ast.Tuple,
        ast.Call,  # Only for whitelisted functions
        ast.Attribute,  # Only for safe attribute access
    }

    # Whitelisted custom functions
    CUSTOM_FUNCTIONS = {
        "contains_pii",
        "count_threats",
        "has_threat_type",
        "severity_level",
        "matches_pattern",
    }

    def __init__(self) -> None:
        """Initialize safe evaluator."""
        self._cache: dict[str, ast.Expression] = {}

    def parse(self, expression: str) -> ast.Expression:
        """Parse expression into AST.

        Args:
            expression: Python expression string

        Returns:
            Parsed AST Expression node

        Raises:
            ValueError: If expression is invalid or unsafe
        """
        # Check cache
        if expression in self._cache:
            return self._cache[expression]

        try:
            # Parse expression
            tree = ast.parse(expression, mode="eval")

            # Validate all nodes are safe
            for node in ast.walk(tree):
                if type(node) not in self.ALLOWED_NODES:
                    raise ValueError(
                        f"Unsafe AST node type: {type(node).__name__}"
                    )

                # Check function calls are whitelisted
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id not in self.CUSTOM_FUNCTIONS:
                            raise ValueError(
                                f"Function '{node.func.id}' not allowed"
                            )
                    else:
                        raise ValueError("Only simple function calls allowed")

                # Check attribute access is on known safe objects
                if isinstance(node, ast.Attribute):
                    # Only allow attribute access in the form: variable.attribute
                    if not isinstance(node.value, ast.Name):
                        raise ValueError("Complex attribute access not allowed")

            # Cache parsed expression
            self._cache[expression] = tree
            return tree

        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {e}")

    def evaluate(
        self,
        expression: str,
        context: dict[str, Any],
        custom_functions: dict[str, Any] | None = None,
    ) -> Any:
        """Evaluate expression in given context.

        Args:
            expression: Python expression string
            context: Variables available to expression
            custom_functions: Custom functions available to expression

        Returns:
            Result of expression evaluation

        Raises:
            ValueError: If expression is unsafe or evaluation fails
        """
        # Parse expression
        tree = self.parse(expression)

        # Build safe namespace
        namespace = {
            "__builtins__": {},  # No built-in functions
            **context,
        }

        # Add custom functions
        if custom_functions:
            namespace.update(custom_functions)

        try:
            # Evaluate expression
            result = eval(compile(tree, "<policy>", "eval"), namespace)
            return result
        except Exception as e:
            raise ValueError(f"Expression evaluation failed: {e}")


class PolicyEngine:
    """Policy evaluation engine.

    Evaluates detection results against policy rules to determine final actions.
    """

    def __init__(self, policy: Policy | None = None) -> None:
        """Initialize policy engine.

        Args:
            policy: Policy to use (default: creates default policy)
        """
        self.policy = policy or self._create_default_policy()
        self.evaluator = SafeEvaluator()
        self._custom_functions = self._build_custom_functions()

    def _create_default_policy(self) -> Policy:
        """Create default security policy.

        Returns:
            Default policy with sensible rules
        """
        return Policy(
            name="Default Security Policy",
            version="1.0",
            rules=[
                PolicyRule(
                    name="Block critical SQL injections",
                    condition="severity == 'critical' and threat_type == 'sql_injection'",
                    action=PolicyAction.BLOCK,
                    priority=100,
                    description="Block destructive SQL operations",
                ),
                PolicyRule(
                    name="Block critical prompt injections",
                    condition="severity == 'critical' and threat_type == 'prompt_injection'",
                    action=PolicyAction.BLOCK,
                    priority=100,
                    description="Block prompt manipulation attempts",
                ),
                PolicyRule(
                    name="Challenge critical PII",
                    condition="severity == 'critical' and threat_type == 'pii'",
                    action=PolicyAction.CHALLENGE,
                    priority=90,
                    description="Require confirmation before exposing sensitive PII",
                ),
                PolicyRule(
                    name="Challenge high severity threats",
                    condition="severity == 'high'",
                    action=PolicyAction.CHALLENGE,
                    priority=50,
                    description="Require review for high severity threats",
                ),
                PolicyRule(
                    name="Log medium severity threats",
                    condition="severity == 'medium'",
                    action=PolicyAction.LOG,
                    priority=25,
                    description="Log medium threats for monitoring",
                ),
                PolicyRule(
                    name="Allow low severity",
                    condition="severity == 'low'",
                    action=PolicyAction.ALLOW,
                    priority=10,
                    description="Allow low severity detections",
                ),
            ],
            metadata={
                "author": "Blind AI",
                "description": "Default security policy with balanced protection",
            },
        )

    def _build_custom_functions(self) -> dict[str, Any]:
        """Build custom functions for policy conditions.

        Returns:
            Dictionary of custom function name -> function
        """
        return {
            "contains_pii": self._contains_pii,
            "count_threats": self._count_threats,
            "has_threat_type": self._has_threat_type,
            "severity_level": self._severity_level,
            "matches_pattern": self._matches_pattern,
        }

    def _contains_pii(self, results: list[DetectionResult]) -> bool:
        """Check if results contain PII detection.

        Args:
            results: List of detection results

        Returns:
            True if any result is PII threat
        """
        return any(r.threat_type == ThreatType.PII for r in results)

    def _count_threats(self, results: list[DetectionResult]) -> int:
        """Count total number of threats.

        Args:
            results: List of detection results

        Returns:
            Number of threats detected
        """
        return len(results)

    def _has_threat_type(
        self, results: list[DetectionResult], threat_type: str
    ) -> bool:
        """Check if results contain specific threat type.

        Args:
            results: List of detection results
            threat_type: Threat type to check (e.g., 'sql_injection')

        Returns:
            True if threat type is present
        """
        return any(r.threat_type.value == threat_type for r in results)

    def _severity_level(self, severity: str) -> int:
        """Convert severity to numeric level for comparison.

        Args:
            severity: Severity string (critical, high, medium, low)

        Returns:
            Numeric severity level (4=critical, 3=high, 2=medium, 1=low, 0=unknown)
        """
        levels = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1,
        }
        return levels.get(severity.lower(), 0)

    def _matches_pattern(self, text: str, pattern: str) -> bool:
        """Check if text matches regex pattern.

        Args:
            text: Text to check
            pattern: Regex pattern

        Returns:
            True if pattern matches
        """
        try:
            return bool(re.search(pattern, text, re.IGNORECASE))
        except re.error:
            return False

    def evaluate(self, result: DetectionResult) -> PolicyAction:
        """Evaluate a single detection result against policy.

        Args:
            result: Detection result to evaluate

        Returns:
            Policy action to take

        Raises:
            ValueError: If evaluation fails
        """
        # Build context for rule evaluation
        context = {
            "severity": result.severity,
            "threat_type": result.threat_type.value,
            "pattern_name": result.pattern_name,
            "confidence": result.confidence,
            "matched_text": result.matched_text,
            "description": result.description,
            "action": result.action.value,
        }

        # Evaluate rules in priority order
        for rule in self.policy.rules:
            if not rule.enabled:
                continue

            try:
                # Evaluate rule condition
                matches = self.evaluator.evaluate(
                    rule.condition,
                    context,
                    self._custom_functions,
                )

                # If condition matches, return action
                if matches:
                    return rule.action

            except Exception as e:
                # Log error with details for debugging/auditing
                logger.warning(
                    "Rule '%s' evaluation failed: %s - condition: %s",
                    rule.name,
                    str(e),
                    rule.condition,
                    exc_info=True,
                )
                continue

        # No rules matched - default to detector's recommendation
        return self._convert_action(result.action)

    def evaluate_batch(
        self, results: list[DetectionResult]
    ) -> dict[str, Any]:
        """Evaluate multiple detection results.

        Args:
            results: List of detection results

        Returns:
            Dictionary with:
                - overall_action: Most restrictive action across all results
                - result_actions: List of (result, action) tuples
                - blocked: Number of blocked results
                - challenged: Number of challenged results
                - logged: Number of logged results
                - allowed: Number of allowed results
        """
        if not results:
            return {
                "overall_action": PolicyAction.ALLOW,
                "result_actions": [],
                "blocked": 0,
                "challenged": 0,
                "logged": 0,
                "allowed": 0,
            }

        # Evaluate each result
        result_actions = [(r, self.evaluate(r)) for r in results]

        # Count actions
        action_counts = {
            "blocked": sum(1 for _, a in result_actions if a == PolicyAction.BLOCK),
            "challenged": sum(
                1 for _, a in result_actions if a == PolicyAction.CHALLENGE
            ),
            "logged": sum(1 for _, a in result_actions if a == PolicyAction.LOG),
            "allowed": sum(1 for _, a in result_actions if a == PolicyAction.ALLOW),
        }

        # Determine overall action (most restrictive wins)
        if action_counts["blocked"] > 0:
            overall_action = PolicyAction.BLOCK
        elif action_counts["challenged"] > 0:
            overall_action = PolicyAction.CHALLENGE
        elif action_counts["logged"] > 0:
            overall_action = PolicyAction.LOG
        else:
            overall_action = PolicyAction.ALLOW

        return {
            "overall_action": overall_action,
            "result_actions": result_actions,
            **action_counts,
        }

    def _convert_action(self, action: ActionType) -> PolicyAction:
        """Convert detector ActionType to PolicyAction.

        Args:
            action: Detector action type

        Returns:
            Corresponding policy action
        """
        mapping = {
            ActionType.BLOCK: PolicyAction.BLOCK,
            ActionType.CHALLENGE: PolicyAction.CHALLENGE,
            ActionType.LOG: PolicyAction.LOG,
            ActionType.ALLOW: PolicyAction.ALLOW,
        }
        return mapping.get(action, PolicyAction.LOG)

    def load_policy(self, policy: Policy) -> None:
        """Load a new policy.

        Args:
            policy: Policy to load
        """
        self.policy = policy

    def validate_policy(self) -> list[str]:
        """Validate current policy.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check policy has rules
        if not self.policy.rules:
            errors.append("Policy has no rules")

        # Validate each rule
        for i, rule in enumerate(self.policy.rules):
            # Check rule has name
            if not rule.name:
                errors.append(f"Rule {i}: Missing name")

            # Check rule has condition
            if not rule.condition:
                errors.append(f"Rule {i} ({rule.name}): Missing condition")
            else:
                # Try to parse condition
                try:
                    self.evaluator.parse(rule.condition)
                except ValueError as e:
                    errors.append(
                        f"Rule {i} ({rule.name}): Invalid condition - {e}"
                    )

        return errors
