"""
External MCP Servers

Pre-configured MCP servers from Smithery and GitHub that can be enabled
with a single button click (by setting their environment variable).

Frontend Display:
- Show all servers with enable/disable toggle
- Servers auto-enable when env var is set
- Group by category (communication, finance, etc.)
"""

from typing import Any, Dict, List, Optional

from .smithery import (
    SMITHERY_SERVERS,
    get_enabled_smithery_servers,
    get_all_smithery_servers,
    get_smithery_categories,
)
from .github import (
    GITHUB_SERVERS,
    get_enabled_github_servers,
    get_all_github_servers,
    get_github_categories,
)

__all__ = [
    "SMITHERY_SERVERS",
    "GITHUB_SERVERS",
    "get_enabled_external_servers",
    "get_all_external_servers",
    "get_external_categories",
]


def get_enabled_external_servers(
    categories: Optional[List[str]] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Get all external servers (Smithery + GitHub) that have their env vars set.

    Args:
        categories: Filter by category

    Returns:
        Dict of server name -> config for enabled servers
    """
    servers = {}
    servers.update(get_enabled_smithery_servers(categories))
    servers.update(get_enabled_github_servers(categories))
    return servers


def get_all_external_servers() -> Dict[str, Dict[str, Any]]:
    """
    Get all external servers with their full metadata for frontend display.

    Returns:
        Dict of server name -> full spec including enabled status and type
    """
    servers = {}
    servers.update(get_all_smithery_servers())
    servers.update(get_all_github_servers())
    return servers


def get_external_categories() -> List[str]:
    """Get all categories across Smithery and GitHub servers."""
    categories = set(get_smithery_categories())
    categories.update(get_github_categories())
    return sorted(categories)
