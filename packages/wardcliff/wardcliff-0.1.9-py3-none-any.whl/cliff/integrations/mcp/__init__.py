"""
MCP Servers - Unified API

This module provides a unified interface to all MCP servers:
- builtin: Core trading tools (always on)
- external: Smithery + GitHub servers (one-button enable)
- custom: User-defined servers (.mcp.json)

Frontend API:
    from mcp_servers import get_all_servers, load_mcp_servers

    # Get all servers grouped by type for UI display
    servers = get_all_servers()
    # Returns: {"builtin": {...}, "external": {...}, "custom": {...}}

    # Load enabled servers for agent options
    enabled = load_mcp_servers()
    # Returns: Dict of server name -> config (only enabled servers)
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .builtin import get_builtin_servers, get_builtin_tool_names, BUILTIN_SERVERS
from .external import (
    get_enabled_external_servers,
    get_all_external_servers,
    get_external_categories,
    SMITHERY_SERVERS,
    GITHUB_SERVERS,
)
from .custom import load_custom_servers, get_all_custom_servers

logger = logging.getLogger(__name__)

__all__ = [
    # Main API for frontend
    "get_all_servers",
    "load_mcp_servers",
    # Builtin
    "get_builtin_servers",
    "get_builtin_tool_names",
    "BUILTIN_SERVERS",
    # External
    "get_enabled_external_servers",
    "get_all_external_servers",
    "get_external_categories",
    "SMITHERY_SERVERS",
    "GITHUB_SERVERS",
    # Custom
    "load_custom_servers",
    "get_all_custom_servers",
    # Backward compat (for mcp_registry)
    "ENTERPRISE_SERVERS",
]

# Backward compatibility alias
ENTERPRISE_SERVERS = SMITHERY_SERVERS


def get_all_servers(
    config_path: Optional[Path] = None,
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Get all servers organized by type for frontend display.

    Args:
        config_path: Path to .mcp.json for custom servers

    Returns:
        {
            "builtin": {"trading": {...}},       # Always enabled
            "external": {"slack": {...}, ...},   # One-button enable
            "custom": {"internal-api": {...}},   # User configured
        }
    """
    return {
        "builtin": get_builtin_servers(),
        "external": get_all_external_servers(),
        "custom": get_all_custom_servers(config_path),
    }


def load_mcp_servers(
    config_path: Optional[Path] = None,
    include_smithery: bool = True,
    include_github: bool = True,
    categories: Optional[List[str]] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Load all enabled MCP servers for agent options.

    This is the main function to get servers for the OpenAI Agents SDK options.
    Servers are enabled when their environment variable is set.

    Args:
        config_path: Path to .mcp.json for custom servers
        include_smithery: Include Smithery-hosted servers
        include_github: Include GitHub-hosted servers
        categories: Filter by category

    Returns:
        Dict of server name -> server config for mcp_servers parameter

    Example:
        from mcp_servers import load_mcp_servers

        servers = load_mcp_servers()
        agent = Agent(..., mcp_servers=servers)
    """
    servers: Dict[str, Dict[str, Any]] = {}

    # 1. Load custom servers from .mcp.json (highest priority)
    servers.update(load_custom_servers(config_path))

    # 2. Load enabled external servers (Smithery + GitHub)
    if include_smithery or include_github:
        # Get external servers, filtering by include flags
        from .external.smithery import get_enabled_smithery_servers
        from .external.github import get_enabled_github_servers

        if include_smithery:
            servers.update(get_enabled_smithery_servers(categories))
        if include_github:
            servers.update(get_enabled_github_servers(categories))

    logger.info(f"Loaded {len(servers)} MCP servers")
    return servers


def get_server_info(name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a specific MCP server.

    Args:
        name: Server name (e.g., "slack", "brex", "trading")

    Returns:
        Server spec dict or None if not found
    """
    if name in BUILTIN_SERVERS:
        return {**BUILTIN_SERVERS[name], "type": "builtin"}
    if name in SMITHERY_SERVERS:
        return {**SMITHERY_SERVERS[name], "type": "smithery"}
    if name in GITHUB_SERVERS:
        return {**GITHUB_SERVERS[name], "type": "github"}
    return None


def list_servers_by_category(category: str) -> List[str]:
    """
    List all servers in a specific category.

    Args:
        category: Category name (e.g., "finance", "communication")

    Returns:
        List of server names
    """
    servers = []
    for name, spec in SMITHERY_SERVERS.items():
        if spec.get("category") == category:
            servers.append(name)
    for name, spec in GITHUB_SERVERS.items():
        if spec.get("category") == category:
            servers.append(name)
    return servers


def get_all_categories() -> List[str]:
    """Get all available server categories."""
    return get_external_categories()


def print_server_catalog():
    """Print a formatted catalog of all available MCP servers."""
    print("\n" + "=" * 60)
    print("MCP SERVER CATALOG")
    print("=" * 60)

    # Builtin
    print("\n### BUILTIN (Always On)")
    for name, spec in BUILTIN_SERVERS.items():
        print(f"  - {name}: {spec.get('description', '')}")

    # External by category
    for category in get_all_categories():
        servers = list_servers_by_category(category)
        if servers:
            print(f"\n### {category.upper().replace('_', ' ')} ({len(servers)} servers)")
            for name in servers:
                spec = get_server_info(name)
                if spec:
                    tools = spec.get("tools", "-")
                    if isinstance(tools, list):
                        tools = len(tools)
                    desc = spec.get("description", "")
                    source = spec.get("type", "smithery")
                    official = " [OFFICIAL]" if spec.get("official") else ""
                    print(f"  - {name}: {desc} ({tools} tools) [{source}]{official}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    print_server_catalog()
