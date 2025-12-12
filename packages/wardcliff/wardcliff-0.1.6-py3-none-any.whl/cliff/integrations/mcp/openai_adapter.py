"""
OpenAI Agents SDK MCP Adapter

Converts existing MCP server configurations to OpenAI Agents SDK format.
Supports both HTTP-based servers (Smithery) and stdio-based servers.

Usage:
    from cliff.integrations.mcp.openai_adapter import load_openai_mcp_servers

    servers = load_openai_mcp_servers()
    agent = Agent(name="trader", mcp_servers=servers)
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def load_openai_mcp_servers(
    config_path: Optional[Path] = None,
    include_smithery: bool = True,
    include_github: bool = True,
    categories: Optional[List[str]] = None,
) -> List[Any]:
    """
    Load MCP servers in OpenAI Agents SDK format.

    Converts existing server configurations to OpenAI's MCPServerStreamableHttp
    and MCPServerStdio classes.

    Args:
        config_path: Path to .mcp.json for custom servers
        include_smithery: Include Smithery-hosted servers
        include_github: Include GitHub-hosted servers
        categories: Filter by category

    Returns:
        List of MCP server instances for OpenAI Agent's mcp_servers parameter
    """
    try:
        from agents.mcp import MCPServerStreamableHttp, MCPServerStdio
    except ImportError:
        logger.warning("openai-agents not installed, returning empty server list")
        return []

    servers = []

    # Load Smithery servers (HTTP-based)
    # Note: Smithery uses OAuth authentication, not API keys
    # These servers require browser-based OAuth flow to work
    if include_smithery:
        from .external.smithery import get_enabled_smithery_servers
        smithery_servers = get_enabled_smithery_servers(categories)

        if smithery_servers:
            logger.info(
                f"Smithery servers require OAuth authentication. "
                f"Use local stdio servers instead for programmatic access."
            )

        for name, config in smithery_servers.items():
            url = config.get("url")
            if url:
                try:
                    server = MCPServerStreamableHttp(
                        name=name,
                        params={"url": url},
                        cache_tools_list=True,
                    )
                    servers.append(server)
                    logger.debug(f"Added Smithery MCP server: {name}")
                except Exception as e:
                    logger.warning(f"Failed to create Smithery server {name}: {e}")

    # Load GitHub servers (stdio-based)
    if include_github:
        from .external.github import get_enabled_github_servers
        github_servers = get_enabled_github_servers(categories)

        for name, config in github_servers.items():
            command = config.get("command")
            args = config.get("args", [])
            env = config.get("env", {})

            # Resolve env vars
            resolved_env = {}
            for key, val in env.items():
                if isinstance(val, str) and val.startswith("${") and val.endswith("}"):
                    env_var = val[2:-1]
                    resolved_env[key] = os.environ.get(env_var, "")
                else:
                    resolved_env[key] = val

            if command:
                try:
                    server = MCPServerStdio(
                        name=name,
                        params={
                            "command": command,
                            "args": args,
                            "env": resolved_env,
                        },
                        cache_tools_list=True,
                    )
                    servers.append(server)
                    logger.debug(f"Added GitHub MCP server: {name}")
                except Exception as e:
                    logger.warning(f"Failed to create GitHub server {name}: {e}")

    # Load custom servers from .mcp.json
    if config_path and config_path.exists():
        from .custom import load_custom_servers
        custom_servers = load_custom_servers(config_path)

        for name, config in custom_servers.items():
            # Determine if HTTP or stdio
            if "url" in config:
                try:
                    server = MCPServerStreamableHttp(
                        name=name,
                        params={"url": config["url"], "headers": config.get("headers", {})},
                        cache_tools_list=True,
                    )
                    servers.append(server)
                except Exception as e:
                    logger.warning(f"Failed to create custom HTTP server {name}: {e}")
            elif "command" in config:
                try:
                    server = MCPServerStdio(
                        name=name,
                        params={
                            "command": config["command"],
                            "args": config.get("args", []),
                            "env": config.get("env", {}),
                        },
                        cache_tools_list=True,
                    )
                    servers.append(server)
                except Exception as e:
                    logger.warning(f"Failed to create custom stdio server {name}: {e}")

    logger.info(f"Loaded {len(servers)} OpenAI MCP servers")
    return servers


def get_server_count() -> Dict[str, int]:
    """Get count of available servers by type."""
    from .external.smithery import SMITHERY_SERVERS
    from .external.github import GITHUB_SERVERS

    # Count enabled servers (always_enabled or env var set)
    smithery_enabled = sum(
        1 for spec in SMITHERY_SERVERS.values()
        if spec.get("always_enabled") or (spec.get("env_key") and os.environ.get(spec["env_key"]))
    )
    github_enabled = sum(
        1 for spec in GITHUB_SERVERS.values()
        if spec.get("always_enabled") or (spec.get("env_key") and os.environ.get(spec["env_key"]))
    )

    return {
        "smithery_total": len(SMITHERY_SERVERS),
        "smithery_enabled": smithery_enabled,
        "github_total": len(GITHUB_SERVERS),
        "github_enabled": github_enabled,
        "total_enabled": smithery_enabled + github_enabled,
    }
