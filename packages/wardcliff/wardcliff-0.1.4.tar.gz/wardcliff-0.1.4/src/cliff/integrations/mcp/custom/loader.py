"""
Custom MCP Server Loader

Load user-defined MCP servers from .mcp.json configuration file.
This allows users to add their own internal tools, databases, etc.

Example .mcp.json:
{
  "mcpServers": {
    "internal-api": {
      "command": "node",
      "args": ["./mcp-servers/internal-api/index.js"],
      "env": {
        "API_KEY": "${INTERNAL_API_KEY}"
      }
    },
    "warehouse": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${WAREHOUSE_DB_URL}"
      }
    }
  }
}
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def load_custom_servers(
    config_path: Optional[Path] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Load custom MCP servers from .mcp.json configuration.

    Args:
        config_path: Path to .mcp.json (default: .mcp.json in cwd)

    Returns:
        Dict of server name -> server config
    """
    if config_path is None:
        config_path = Path(".mcp.json")

    servers = {}

    if not config_path.exists():
        return servers

    try:
        with open(config_path) as f:
            config = json.load(f)
            custom_servers = config.get("mcpServers", {})

            # Process env var substitution
            for name, spec in custom_servers.items():
                servers[name] = _process_env_vars(spec)

            logger.info(f"Loaded {len(servers)} custom servers from {config_path}")

    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Failed to load {config_path}: {e}")

    return servers


def _process_env_vars(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process environment variable substitution in server config.

    Replaces ${VAR_NAME} with actual environment variable values.
    """
    result = {}

    for key, value in spec.items():
        if isinstance(value, str):
            # Handle ${VAR_NAME} substitution
            if value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                result[key] = os.environ.get(env_var, value)
            else:
                result[key] = value
        elif isinstance(value, dict):
            result[key] = _process_env_vars(value)
        elif isinstance(value, list):
            result[key] = [
                _process_env_vars(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def get_all_custom_servers(
    config_path: Optional[Path] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Get all custom servers with metadata for frontend display.

    Args:
        config_path: Path to .mcp.json

    Returns:
        Dict of server name -> full spec with type='custom'
    """
    servers = load_custom_servers(config_path)

    # Add type metadata for frontend
    for name, spec in servers.items():
        spec["type"] = "custom"
        spec["enabled"] = True  # Custom servers are always enabled if configured

    return servers
