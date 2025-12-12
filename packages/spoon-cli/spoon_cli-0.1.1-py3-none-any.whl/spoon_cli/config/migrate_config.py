"""
Simple configuration migration utilities for CLI.
"""

import logging
from typing import Any
logger = logging.getLogger(__name__)


def migrate_config(
    input_file: str = "config.json",
    output_file: str = None,
    backup: bool = True,
    validate: bool = True,
    dry_run: bool = False
) -> bool:
    """Simple configuration migration stub."""
    logger.info("Configuration migration not implemented in CLI version")
    return True


def interactive_migration() -> bool:
    """Interactive configuration migration stub."""
    logger.info("Interactive configuration migration not implemented in CLI version")
    return True


def validate_environment_variables(config_data: dict[str, Any]) -> list[str]:
    """Validate environment variables in configuration."""
    missing_vars = []
    if "api_keys" in config_data:
        for provider, key in config_data["api_keys"].items():
            if not key or key.startswith("your-") or key == "":
                missing_vars.append(f"api_keys.{provider}")
    return missing_vars


def check_mcp_server_availability(config_data: dict[str, Any]) -> list[str]:
    """Check MCP server availability."""
    unavailable = []
    if "agents" in config_data:
        for agent_name, agent_config in config_data["agents"].items():
            if "tools" in agent_config:
                for tool in agent_config["tools"]:
                    if tool.get("type") == "mcp":
                        mcp_server = tool.get("mcp_server", {})
                        command = mcp_server.get("command")
                        if not command:
                            unavailable.append(f"{agent_name}.{tool.get('name', 'unknown')}")
    return unavailable

