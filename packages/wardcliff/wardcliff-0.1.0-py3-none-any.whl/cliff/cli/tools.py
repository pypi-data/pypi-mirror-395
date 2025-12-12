"""
Unified Tool Registry for Cliff CLI.

Consolidates all available tools in one place:
1. Native Tools (OpenAI Agents SDK / Codex)
2. Custom Trading Tools (built-in market tools)
3. MCP Servers (60+ external integrations)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Import the full MCP registries
from cliff.integrations.mcp.external.smithery import SMITHERY_SERVERS, get_smithery_categories
from cliff.integrations.mcp.external.github import (
    GITHUB_SERVERS, get_github_categories,
    AUTH_NONE, AUTH_API_KEY, AUTH_MULTI_KEY, AUTH_OAUTH
)
from cliff.integrations.mcp.builtin import BUILTIN_SERVERS
from cliff.cli.config import MCPKeysConfig


# =============================================================================
# NATIVE TOOLS (OpenAI Agents SDK / Codex)
# =============================================================================

NATIVE_TOOLS: Dict[str, Dict[str, Any]] = {
    "web-search": {
        "name": "Web Search",
        "description": "Search the web for current events, news, and real-time data",
        "category": "research",
        "type": "native",
        "sdk_class": "WebSearchTool",
        "enabled_by_default": True,
        "requires_api_key": False,  # Included in OpenAI API
    },
    "code-interpreter": {
        "name": "Code Interpreter",
        "description": "Execute Python code for calculations, analysis, and data processing",
        "category": "analysis",
        "type": "native",
        "sdk_class": "CodeInterpreterTool",
        "enabled_by_default": True,
        "requires_api_key": False,
    },
    "file-search": {
        "name": "File Search",
        "description": "Search documents in OpenAI vector stores for RAG",
        "category": "research",
        "type": "native",
        "sdk_class": "FileSearchTool",
        "enabled_by_default": True,
        "requires_api_key": False,
        "requires_config": "vector_store_ids",  # Optional: provide IDs for specific stores
    },
}


# =============================================================================
# CUSTOM TRADING TOOLS (Built-in Market Tools)
# =============================================================================

CUSTOM_TOOLS: Dict[str, Dict[str, Any]] = {
    "get-portfolio": {
        "name": "Get Portfolio",
        "description": "Check cash balance, positions, cost basis, and P&L",
        "category": "trading",
        "type": "custom",
        "function": "get_portfolio",
        "enabled_by_default": True,
        "always_enabled": True,
    },
    "get-price-history": {
        "name": "Get Price History",
        "description": "See recent trades and price movements in the market",
        "category": "trading",
        "type": "custom",
        "function": "get_price_history",
        "enabled_by_default": True,
        "always_enabled": True,
    },
    "place-trade": {
        "name": "Place Trade",
        "description": "Execute buy/sell orders with outcome, size, and rationale",
        "category": "trading",
        "type": "custom",
        "function": "place_trade",
        "enabled_by_default": True,
        "always_enabled": True,
    },
    "get-latest-prices": {
        "name": "Get Latest Prices",
        "description": "Get current market prices (always call before trading)",
        "category": "trading",
        "type": "custom",
        "function": "get_latest_prices",
        "enabled_by_default": True,
        "always_enabled": True,
    },
    "configure-alerts": {
        "name": "Configure Alerts",
        "description": "Set up price change and trade size alert thresholds",
        "category": "trading",
        "type": "custom",
        "function": "configure_alerts",
        "enabled_by_default": True,
        "always_enabled": True,
    },
    "check-price-alerts": {
        "name": "Check Price Alerts",
        "description": "Check for pending alerts based on configured conditions",
        "category": "trading",
        "type": "custom",
        "function": "check_price_alerts",
        "enabled_by_default": True,
        "always_enabled": True,
    },
}


# =============================================================================
# TOOL REGISTRY
# =============================================================================

@dataclass
class Tool:
    """A tool available to agents."""
    id: str
    name: str
    description: str
    category: str
    tool_type: str  # native, custom, mcp-smithery, mcp-github
    enabled: bool = False
    always_enabled: bool = False
    auth_type: Optional[str] = None  # none, api_key, multi_key, oauth
    env_key: Optional[str] = None
    url: Optional[str] = None
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    tools_count: Optional[int] = None
    official: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    """
    Unified registry of all available tools.

    Categories:
    - Native: OpenAI Agents SDK hosted tools (WebSearch, CodeInterpreter, FileSearch)
    - Custom: Built-in trading tools (portfolio, prices, trades, alerts)
    - MCP: External integrations (60+ Smithery + GitHub servers)
    """

    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._load_all_tools()

    def _load_all_tools(self):
        """Load all tools from the various registries."""
        # 1. Load native tools
        for tool_id, spec in NATIVE_TOOLS.items():
            self._tools[tool_id] = Tool(
                id=tool_id,
                name=spec["name"],
                description=spec["description"],
                category=spec["category"],
                tool_type="native",
                enabled=spec.get("enabled_by_default", False),
                always_enabled=False,
                metadata=spec,
            )

        # 2. Load custom trading tools
        for tool_id, spec in CUSTOM_TOOLS.items():
            self._tools[tool_id] = Tool(
                id=tool_id,
                name=spec["name"],
                description=spec["description"],
                category=spec["category"],
                tool_type="custom",
                enabled=spec.get("enabled_by_default", True),
                always_enabled=spec.get("always_enabled", False),
                metadata=spec,
            )

        # 3. Load Smithery MCP servers
        for server_id, spec in SMITHERY_SERVERS.items():
            env_key = spec.get("env_key")
            is_enabled = bool(env_key and os.environ.get(env_key))

            self._tools[f"mcp-{server_id}"] = Tool(
                id=f"mcp-{server_id}",
                name=server_id.replace("_", " ").title(),
                description=spec.get("description", ""),
                category=spec.get("category", "other"),
                tool_type="mcp-smithery",
                enabled=is_enabled,
                env_key=env_key,
                url=spec.get("url"),
                tools_count=spec.get("tools"),
                metadata=spec,
            )

        # 4. Load GitHub MCP servers with auth_type-aware enabled logic
        mcp_keys_config = MCPKeysConfig.load()

        for server_id, spec in GITHUB_SERVERS.items():
            env_key = spec.get("env_key")
            auth_type = spec.get("auth_type", AUTH_API_KEY)

            # Determine if server is enabled based on auth_type
            if auth_type == AUTH_NONE:
                # No-auth servers: must be explicitly enabled by user
                is_enabled = mcp_keys_config.is_server_enabled(server_id)
            elif auth_type == AUTH_OAUTH:
                # OAuth servers: must be explicitly enabled by user
                is_enabled = mcp_keys_config.is_server_enabled(server_id)
            elif auth_type == AUTH_MULTI_KEY:
                # Multi-key servers: all env vars must be set
                env_keys = spec.get("env_keys", [])
                is_enabled = all(os.environ.get(k) for k in env_keys if k)
            else:
                # API key servers: single env var must be set
                is_enabled = bool(env_key and os.environ.get(env_key))

            self._tools[f"mcp-{server_id}"] = Tool(
                id=f"mcp-{server_id}",
                name=server_id.replace("_", " ").title(),
                description=spec.get("description", ""),
                category=spec.get("category", "other"),
                tool_type="mcp-github",
                enabled=is_enabled,
                auth_type=auth_type,
                env_key=env_key,
                url=spec.get("url"),
                command=spec.get("command"),
                args=spec.get("args", []),
                official=spec.get("official", False),
                metadata=spec,
            )

    def get_all(self) -> List[Tool]:
        """Get all tools."""
        return list(self._tools.values())

    def get(self, tool_id: str) -> Optional[Tool]:
        """Get a specific tool by ID."""
        return self._tools.get(tool_id)

    def get_by_type(self, tool_type: str) -> List[Tool]:
        """Get tools by type (native, custom, mcp-smithery, mcp-github)."""
        return [t for t in self._tools.values() if t.tool_type == tool_type]

    def get_by_category(self, category: str) -> List[Tool]:
        """Get tools by category."""
        return [t for t in self._tools.values() if t.category == category]

    def get_enabled(self) -> List[Tool]:
        """Get all enabled tools."""
        return [t for t in self._tools.values() if t.enabled or t.always_enabled]

    def get_native_tools(self) -> List[Tool]:
        """Get OpenAI Agents SDK native tools."""
        return self.get_by_type("native")

    def get_custom_tools(self) -> List[Tool]:
        """Get custom trading tools."""
        return self.get_by_type("custom")

    def get_mcp_servers(self) -> List[Tool]:
        """Get all MCP servers (Smithery + GitHub)."""
        return [t for t in self._tools.values() if t.tool_type.startswith("mcp-")]

    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        return sorted(set(t.category for t in self._tools.values()))

    def get_tool_types(self) -> List[str]:
        """Get all unique tool types."""
        return sorted(set(t.tool_type for t in self._tools.values()))

    def count_by_type(self) -> Dict[str, int]:
        """Count tools by type."""
        counts = {}
        for t in self._tools.values():
            counts[t.tool_type] = counts.get(t.tool_type, 0) + 1
        return counts

    def count_enabled(self) -> int:
        """Count enabled tools."""
        return len(self.get_enabled())

    def summary(self) -> Dict[str, Any]:
        """Get registry summary."""
        counts = self.count_by_type()
        return {
            "total": len(self._tools),
            "enabled": self.count_enabled(),
            "native": counts.get("native", 0),
            "custom": counts.get("custom", 0),
            "mcp_smithery": counts.get("mcp-smithery", 0),
            "mcp_github": counts.get("mcp-github", 0),
            "categories": self.get_categories(),
        }


# Singleton instance
_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry instance."""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry


def refresh_tool_registry() -> ToolRegistry:
    """Refresh the tool registry (re-check env vars)."""
    global _registry
    _registry = ToolRegistry()
    return _registry
