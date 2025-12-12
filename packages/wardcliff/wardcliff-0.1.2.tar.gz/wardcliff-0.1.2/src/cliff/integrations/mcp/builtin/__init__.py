"""
Builtin MCP Servers

Core MCP servers that are always enabled and part of the trading system.

Frontend Display:
- Always show as active (green)
- Cannot be disabled
- Part of core functionality

Note: The actual trading server creation requires TradingAgentState,
so we provide metadata here and the factory function remains in
claude_trading_agent.py.
"""

from typing import Any, Dict


# Metadata about builtin servers for frontend display
BUILTIN_SERVERS: Dict[str, Dict[str, Any]] = {
    "trading": {
        "name": "Trading",
        "description": "Core trading tools: getPortfolio, getPriceHistory, placeTrade, configureAlerts, checkPriceAlerts, getLatestPrices",
        "tools": [
            {
                "name": "getPortfolio",
                "description": "Check cash balance, positions, P&L, and current market prices",
            },
            {
                "name": "getPriceHistory",
                "description": "See recent trades and price movements",
            },
            {
                "name": "placeTrade",
                "description": "Execute buy/sell orders with rationale (captures price before/after)",
            },
            {
                "name": "configureAlerts",
                "description": "Configure what market conditions trigger alerts (price %, thresholds, other agent trades)",
            },
            {
                "name": "checkPriceAlerts",
                "description": "Check for pending alerts based on configured conditions",
            },
            {
                "name": "getLatestPrices",
                "description": "Get current market prices (call before every trade)",
            },
        ],
        "always_enabled": True,
        "category": "trading",
    },
}


def get_builtin_servers() -> Dict[str, Dict[str, Any]]:
    """
    Get builtin servers with metadata for frontend display.

    Returns:
        Dict of server name -> metadata (always_enabled=True)
    """
    servers = {}
    for name, spec in BUILTIN_SERVERS.items():
        servers[name] = {
            **spec,
            "type": "builtin",
            "enabled": True,  # Always enabled
        }
    return servers


def get_builtin_tool_names() -> list[str]:
    """Get list of builtin MCP tool names for allowed_tools."""
    return [
        "mcp__trading__getPortfolio",
        "mcp__trading__getPriceHistory",
        "mcp__trading__placeTrade",
        "mcp__trading__configureAlerts",
        "mcp__trading__checkPriceAlerts",
        "mcp__trading__getLatestPrices",
    ]
