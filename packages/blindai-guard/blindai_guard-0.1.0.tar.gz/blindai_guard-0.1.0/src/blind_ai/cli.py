"""Blind AI Command Line Interface.

Provides CLI commands for initializing, scanning, testing, and serving
the Blind AI security layer.

Usage:
    blind-ai init [--config FILE]
    blind-ai scan <file_or_text> [--format json|text]
    blind-ai test [--verbose]
    blind-ai serve [--host HOST] [--port PORT]
    blind-ai policies [list|validate] [--path PATH]
    blind-ai version
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

# Import version
from blind_ai import __version__


def get_default_config() -> dict:
    """Get default configuration template."""
    return {
        "version": "1.0",
        "api": {
            "base_url": "http://localhost:8000",
            "timeout": 10.0,
            "max_retries": 3,
            "fail_open": False,
        },
        "detection": {
            "enable_static": True,
            "enable_ml": True,
            "enable_policy": True,
            "parallel_execution": True,
        },
        "logging": {
            "level": "INFO",
            "format": "json",
        },
        "policies": {
            "path": "./policies",
            "default": "default.yaml",
        },
    }


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize Blind AI configuration.

    Creates a configuration file and directory structure for Blind AI.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    config_file = args.config or "blindai.yaml"
    config_path = Path(config_file)

    # Check if already exists
    if config_path.exists() and not args.force:
        print(f"Error: Configuration file '{config_file}' already exists.")
        print("Use --force to overwrite.")
        return 1

    # Create config directory if needed
    config_dir = config_path.parent
    if config_dir and not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    # Create policies directory
    policies_dir = Path("policies")
    if not policies_dir.exists():
        policies_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created policies directory: {policies_dir}")

    # Write default config
    config = get_default_config()

    try:
        import yaml
        config_content = yaml.dump(config, default_flow_style=False, sort_keys=False)
    except ImportError:
        # Fallback to JSON if PyYAML not available
        config_content = json.dumps(config, indent=2)
        config_file = config_file.replace(".yaml", ".json")
        config_path = Path(config_file)

    config_path.write_text(config_content)
    print(f"Created configuration file: {config_file}")

    # Create default policy file
    default_policy = """# Default Blind AI Security Policy
name: "Default Security Policy"
version: "1.0"
description: "Standard security policy for AI agent tool calls"

rules:
  - name: "block_critical_sql_injection"
    description: "Block all critical SQL injection attempts"
    condition: "severity == 'critical' and threat_type == 'sql_injection'"
    action: BLOCK
    priority: 100

  - name: "block_critical_prompt_injection"
    description: "Block critical prompt injection attacks"
    condition: "severity == 'critical' and threat_type == 'prompt_injection'"
    action: BLOCK
    priority: 100

  - name: "block_pii_exfiltration"
    description: "Block attempts to exfiltrate PII data"
    condition: "contains_pii(results) and severity in ['high', 'critical']"
    action: BLOCK
    priority: 95

  - name: "challenge_high_severity"
    description: "Require human approval for high severity threats"
    condition: "severity == 'high'"
    action: CHALLENGE
    priority: 50

  - name: "log_medium_severity"
    description: "Log medium severity issues for review"
    condition: "severity == 'medium'"
    action: LOG
    priority: 25

  - name: "allow_low_severity"
    description: "Allow low severity with logging"
    condition: "severity == 'low'"
    action: LOG
    priority: 10
"""
    default_policy_path = policies_dir / "default.yaml"
    if not default_policy_path.exists():
        default_policy_path.write_text(default_policy)
        print(f"Created default policy: {default_policy_path}")

    # Create .env template
    env_template = """# Blind AI Environment Configuration
# Copy this file to .env and fill in your values

# API Key (get from https://blindai.com/settings/api-keys)
BLIND_AI_API_KEY=your_api_key_here

# API Endpoint (default: http://localhost:8000)
BLIND_AI_BASE_URL=http://localhost:8000

# Redis Configuration (for tool registry)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# ClickHouse Configuration (for audit logs)
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_DB=blind_ai
"""
    env_path = Path(".env.example")
    if not env_path.exists():
        env_path.write_text(env_template)
        print(f"Created environment template: {env_path}")

    print("\n✅ Blind AI initialized successfully!")
    print("\nNext steps:")
    print("  1. Copy .env.example to .env and add your API key")
    print("  2. Review and customize policies/default.yaml")
    print("  3. Start the server: blind-ai serve")
    print("  4. Test detection: blind-ai scan 'DROP TABLE users'")

    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    """Scan text or file for security threats.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for safe, 1 for threat detected, 2 for error)
    """
    from blind_ai.core.detection.static import StaticDetector

    # Determine input
    input_text = args.input

    # Check if input is a file path
    if os.path.isfile(input_text):
        try:
            with open(input_text, "r", encoding="utf-8") as f:
                input_text = f.read()
            if args.verbose:
                print(f"Scanning file: {args.input}")
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 2
    elif args.verbose:
        print(f"Scanning text: {input_text[:100]}...")

    # Initialize detector
    detector = StaticDetector()

    # Perform detection
    try:
        results = detector.detect(input_text)
    except Exception as e:
        print(f"Error during detection: {e}", file=sys.stderr)
        return 2

    # Format output
    if args.format == "json":
        output = {
            "input_length": len(input_text),
            "is_threat": len(results) > 0,
            "threat_count": len(results),
            "threats": [r.to_dict() for r in results],
        }
        print(json.dumps(output, indent=2))
    else:
        # Text format
        if not results:
            print("✅ No threats detected")
            return 0

        print(f"⚠️  {len(results)} threat(s) detected:\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result.severity}] {result.threat_type.value}")
            print(f"   Pattern: {result.pattern_name}")
            print(f"   Description: {result.description}")
            print(f"   Action: {result.action.value}")
            # Mask matched text to prevent PII/sensitive data exposure in logs
            masked_text = _mask_sensitive_text(result.matched_text)
            print(f"   Matched: '{masked_text}'")
            print()

    return 1 if results else 0


def _mask_sensitive_text(text: str, max_visible: int = 20) -> str:
    """Mask potentially sensitive text for safe display/logging.
    
    Shows first and last few characters with middle masked.
    This prevents accidental exposure of PII, credentials, or
    other sensitive data in logs while still being useful for debugging.
    
    Args:
        text: Text to mask
        max_visible: Maximum characters to show (split between start/end)
        
    Returns:
        Masked text like "SELE...RE 1" for "SELECT * FROM users WHERE 1"
    """
    if len(text) <= max_visible:
        return text
    
    half = max_visible // 2
    return f"{text[:half]}...{text[-half:]}"


def cmd_test(args: argparse.Namespace) -> int:
    """Run Blind AI test suite.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code from pytest
    """
    try:
        import pytest
    except ImportError:
        print("Error: pytest not installed. Install with: pip install pytest")
        return 2

    # Build pytest arguments
    pytest_args = ["tests/"]

    if args.verbose:
        pytest_args.append("-v")

    if args.coverage:
        pytest_args.extend(["--cov=blind_ai", "--cov-report=term-missing"])

    if args.unit_only:
        pytest_args.append("tests/unit/")
    elif args.integration_only:
        pytest_args.append("tests/integration/")

    if args.pattern:
        pytest_args.extend(["-k", args.pattern])

    print(f"Running: pytest {' '.join(pytest_args)}")
    return pytest.main(pytest_args)


def cmd_serve(args: argparse.Namespace) -> int:
    """Start the Blind AI API server.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for clean shutdown, 1 for error)
    """
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn not installed. Install with: pip install uvicorn")
        return 2

    host = args.host or os.getenv("BLIND_AI_HOST", "0.0.0.0")
    port = args.port or int(os.getenv("BLIND_AI_PORT", "8000"))
    reload = args.reload
    workers = args.workers or 1

    print(f"🚀 Starting Blind AI API server...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Workers: {workers}")
    print(f"   Reload: {reload}")
    print(f"\n   API docs: http://{host}:{port}/docs")
    print(f"   Health: http://{host}:{port}/health\n")

    try:
        uvicorn.run(
            "blind_ai.api.app:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers if not reload else 1,
            log_level="info" if args.verbose else "warning",
        )
        return 0
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1


def cmd_policies(args: argparse.Namespace) -> int:
    """Manage security policies.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    policies_path = Path(args.path or "policies")

    if args.action == "list":
        # List all policy files
        if not policies_path.exists():
            print(f"Policies directory not found: {policies_path}")
            return 1

        policy_files = list(policies_path.glob("*.yaml")) + list(policies_path.glob("*.yml"))

        if not policy_files:
            print(f"No policy files found in: {policies_path}")
            return 1

        print(f"Found {len(policy_files)} policy file(s):\n")
        for pf in policy_files:
            print(f"  📄 {pf.name}")

            # Try to read and show summary
            try:
                import yaml
                with open(pf, "r") as f:
                    policy = yaml.safe_load(f)
                name = policy.get("name", "Unnamed")
                version = policy.get("version", "Unknown")
                rules_count = len(policy.get("rules", []))
                print(f"     Name: {name}")
                print(f"     Version: {version}")
                print(f"     Rules: {rules_count}")
            except Exception:
                pass
            print()

        return 0

    elif args.action == "validate":
        # Validate policy files
        if not policies_path.exists():
            print(f"Policies directory not found: {policies_path}")
            return 1

        policy_files = list(policies_path.glob("*.yaml")) + list(policies_path.glob("*.yml"))

        if not policy_files:
            print(f"No policy files found in: {policies_path}")
            return 1

        all_valid = True
        for pf in policy_files:
            print(f"Validating: {pf.name}... ", end="")
            try:
                import yaml
                with open(pf, "r") as f:
                    policy = yaml.safe_load(f)

                # Basic validation
                errors = []
                if "name" not in policy:
                    errors.append("Missing 'name' field")
                if "version" not in policy:
                    errors.append("Missing 'version' field")
                if "rules" not in policy:
                    errors.append("Missing 'rules' field")
                elif not isinstance(policy["rules"], list):
                    errors.append("'rules' must be a list")
                else:
                    for i, rule in enumerate(policy["rules"]):
                        if "name" not in rule:
                            errors.append(f"Rule {i+1}: missing 'name'")
                        if "condition" not in rule:
                            errors.append(f"Rule {i+1}: missing 'condition'")
                        if "action" not in rule:
                            errors.append(f"Rule {i+1}: missing 'action'")
                        elif rule["action"] not in ["ALLOW", "BLOCK", "CHALLENGE", "LOG"]:
                            errors.append(f"Rule {i+1}: invalid action '{rule['action']}'")

                if errors:
                    print("❌ INVALID")
                    for err in errors:
                        print(f"     - {err}")
                    all_valid = False
                else:
                    print("✅ VALID")

            except yaml.YAMLError as e:
                print(f"❌ YAML ERROR: {e}")
                all_valid = False
            except Exception as e:
                print(f"❌ ERROR: {e}")
                all_valid = False

        return 0 if all_valid else 1

    else:
        print(f"Unknown action: {args.action}")
        print("Use: blind-ai policies list|validate")
        return 1


def cmd_version(args: argparse.Namespace) -> int:
    """Show version information.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (always 0)
    """
    print(f"Blind AI v{__version__}")
    print("Runtime security for AI agents")
    print("https://github.com/blindai/blind-ai")
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="blind-ai",
        description="Blind AI - Runtime security for AI agents",
        epilog="For more information, visit https://docs.blindai.dev",
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize Blind AI configuration",
        description="Create configuration files and directory structure",
    )
    init_parser.add_argument(
        "-c", "--config",
        help="Configuration file path (default: blindai.yaml)",
        default="blindai.yaml",
    )
    init_parser.add_argument(
        "-f", "--force",
        help="Overwrite existing configuration",
        action="store_true",
    )

    # scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan text or file for security threats",
        description="Analyze input for SQL injection, prompt injection, and PII",
    )
    scan_parser.add_argument(
        "input",
        help="Text to scan or path to file",
    )
    scan_parser.add_argument(
        "-f", "--format",
        help="Output format (default: text)",
        choices=["text", "json"],
        default="text",
    )
    scan_parser.add_argument(
        "-v", "--verbose",
        help="Verbose output",
        action="store_true",
    )

    # test command
    test_parser = subparsers.add_parser(
        "test",
        help="Run Blind AI test suite",
        description="Execute unit and integration tests",
    )
    test_parser.add_argument(
        "-v", "--verbose",
        help="Verbose test output",
        action="store_true",
    )
    test_parser.add_argument(
        "--coverage",
        help="Run with coverage reporting",
        action="store_true",
    )
    test_parser.add_argument(
        "--unit-only",
        help="Run only unit tests",
        action="store_true",
    )
    test_parser.add_argument(
        "--integration-only",
        help="Run only integration tests",
        action="store_true",
    )
    test_parser.add_argument(
        "-k", "--pattern",
        help="Run tests matching pattern",
    )

    # serve command
    serve_parser = subparsers.add_parser(
        "serve",
        help="Start the Blind AI API server",
        description="Run the FastAPI server for threat detection",
    )
    serve_parser.add_argument(
        "-H", "--host",
        help="Host to bind (default: 0.0.0.0)",
        default="0.0.0.0",
    )
    serve_parser.add_argument(
        "-p", "--port",
        help="Port to bind (default: 8000)",
        type=int,
        default=8000,
    )
    serve_parser.add_argument(
        "-r", "--reload",
        help="Enable auto-reload for development",
        action="store_true",
    )
    serve_parser.add_argument(
        "-w", "--workers",
        help="Number of worker processes",
        type=int,
        default=1,
    )
    serve_parser.add_argument(
        "-v", "--verbose",
        help="Verbose logging",
        action="store_true",
    )

    # policies command
    policies_parser = subparsers.add_parser(
        "policies",
        help="Manage security policies",
        description="List and validate policy files",
    )
    policies_parser.add_argument(
        "action",
        help="Action to perform",
        choices=["list", "validate"],
    )
    policies_parser.add_argument(
        "-p", "--path",
        help="Policies directory path (default: ./policies)",
        default="policies",
    )

    # version command (explicit subcommand)
    subparsers.add_parser(
        "version",
        help="Show version information",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command line arguments (defaults to sys.argv)

    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    # Route to command handler
    commands = {
        "init": cmd_init,
        "scan": cmd_scan,
        "test": cmd_test,
        "serve": cmd_serve,
        "policies": cmd_policies,
        "version": cmd_version,
    }

    handler = commands.get(args.command)
    if handler:
        try:
            return handler(args)
        except KeyboardInterrupt:
            print("\nInterrupted")
            return 130
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
