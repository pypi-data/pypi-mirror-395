"""YAML policy parser for Blind AI.

Loads and validates policy definitions from YAML files.
"""

import os
from pathlib import Path
from typing import Any

import yaml

from .policy import Policy, PolicyAction, PolicyRule


class PolicyParseError(Exception):
    """Raised when policy parsing fails."""

    pass


class PolicyParser:
    """Parser for YAML policy files."""

    def __init__(self) -> None:
        """Initialize policy parser."""
        self.policies_dir = Path(__file__).parent / "policies"

    def load_from_file(self, file_path: str | Path) -> Policy:
        """Load policy from YAML file.

        Args:
            file_path: Path to YAML policy file

        Returns:
            Parsed Policy object

        Raises:
            PolicyParseError: If parsing fails
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Policy file not found: {file_path}")

        try:
            with open(file_path) as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise PolicyParseError(f"Invalid YAML syntax: {e}")

        return self._parse_policy(data, source=str(file_path))

    def load_builtin(self, name: str) -> Policy:
        """Load built-in policy by name.

        Args:
            name: Policy name ('default', 'strict', or 'permissive')

        Returns:
            Parsed Policy object

        Raises:
            PolicyParseError: If policy not found or invalid
        """
        if name not in ["default", "strict", "permissive"]:
            raise PolicyParseError(
                f"Unknown built-in policy: {name}. "
                f"Valid options: default, strict, permissive"
            )

        policy_file = self.policies_dir / f"{name}.yaml"
        if not policy_file.exists():
            raise PolicyParseError(f"Built-in policy file not found: {policy_file}")

        return self.load_from_file(policy_file)

    def load_from_string(self, yaml_content: str) -> Policy:
        """Load policy from YAML string.

        Args:
            yaml_content: YAML policy content

        Returns:
            Parsed Policy object

        Raises:
            PolicyParseError: If parsing fails
        """
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise PolicyParseError(f"Invalid YAML syntax: {e}")

        return self._parse_policy(data, source="<string>")

    def _parse_policy(self, data: dict[str, Any], source: str) -> Policy:
        """Parse policy data structure.

        Args:
            data: Parsed YAML data
            source: Source identifier for error messages

        Returns:
            Policy object

        Raises:
            PolicyParseError: If policy structure is invalid
        """
        # Validate required fields
        if not isinstance(data, dict):
            raise PolicyParseError(f"{source}: Policy must be a dictionary")

        if "name" not in data:
            raise PolicyParseError(f"{source}: Missing required field 'name'")

        if "version" not in data:
            raise PolicyParseError(f"{source}: Missing required field 'version'")

        if "rules" not in data:
            raise PolicyParseError(f"{source}: Missing required field 'rules'")

        if not isinstance(data["rules"], list):
            raise PolicyParseError(f"{source}: 'rules' must be a list")

        # Parse rules
        rules = []
        for i, rule_data in enumerate(data["rules"]):
            try:
                rule = self._parse_rule(rule_data, rule_index=i)
                rules.append(rule)
            except PolicyParseError as e:
                raise PolicyParseError(f"{source}: Rule {i}: {e}")

        # Extract metadata
        metadata = data.get("metadata", {})
        if "description" in data:
            metadata["description"] = data["description"]

        # Create policy
        return Policy(
            name=data["name"],
            version=data["version"],
            rules=rules,
            metadata=metadata,
        )

    def _parse_rule(self, data: dict[str, Any], rule_index: int) -> PolicyRule:
        """Parse a single rule.

        Args:
            data: Rule data dictionary
            rule_index: Rule index for error messages

        Returns:
            PolicyRule object

        Raises:
            PolicyParseError: If rule structure is invalid
        """
        if not isinstance(data, dict):
            raise PolicyParseError("Rule must be a dictionary")

        # Validate required fields
        if "name" not in data:
            raise PolicyParseError("Missing required field 'name'")

        if "condition" not in data:
            raise PolicyParseError("Missing required field 'condition'")

        if "action" not in data:
            raise PolicyParseError("Missing required field 'action'")

        # Parse action
        action_str = data["action"]
        if isinstance(action_str, str):
            action_str = action_str.upper()

        try:
            action = PolicyAction[action_str]
        except KeyError:
            raise PolicyParseError(
                f"Invalid action '{action_str}'. "
                f"Valid options: {', '.join(a.name for a in PolicyAction)}"
            )

        # Create rule
        return PolicyRule(
            name=data["name"],
            condition=data["condition"],
            action=action,
            priority=data.get("priority", 0),
            enabled=data.get("enabled", True),
            description=data.get("description", ""),
        )

    def save_to_file(self, policy: Policy, file_path: str | Path) -> None:
        """Save policy to YAML file.

        Args:
            policy: Policy to save
            file_path: Output file path

        Raises:
            PolicyParseError: If serialization fails
        """
        file_path = Path(file_path)

        # Convert policy to dict
        data = {
            "name": policy.name,
            "version": policy.version,
            "rules": [
                {
                    "name": rule.name,
                    "condition": rule.condition,
                    "action": rule.action.value,
                    "priority": rule.priority,
                    "enabled": rule.enabled,
                    "description": rule.description,
                }
                for rule in policy.rules
            ],
        }

        # Add metadata if present
        if policy.metadata:
            data["metadata"] = policy.metadata

        # Write to file
        try:
            with open(file_path, "w") as f:
                yaml.dump(
                    data,
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                )
        except Exception as e:
            raise PolicyParseError(f"Failed to write policy file: {e}")

    def list_builtin_policies(self) -> list[str]:
        """List available built-in policies.

        Returns:
            List of policy names
        """
        if not self.policies_dir.exists():
            return []

        return [
            f.stem
            for f in self.policies_dir.glob("*.yaml")
            if f.is_file()
        ]
