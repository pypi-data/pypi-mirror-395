"""
GitHub-Hosted MCP Servers

Local stdio MCP servers that run via npx/uvx.

Auth Types:
    - "none": No authentication required (user must explicitly enable)
    - "api_key": Single API key via environment variable
    - "multi_key": Multiple API keys via environment variables
    - "oauth": Browser-based OAuth flow (user must explicitly enable)

Usage:
    from mcp_servers.external.github import GITHUB_SERVERS, get_enabled_github_servers

    # Get all servers with env vars set
    servers = get_enabled_github_servers()

Sources:
    - MCP Registry: https://registry.modelcontextprotocol.io
    - Official servers: https://github.com/modelcontextprotocol/servers
"""

import os
from typing import Any, Dict, List, Optional, Set


# Auth type constants
AUTH_NONE = "none"  # No auth required, but must be explicitly enabled
AUTH_API_KEY = "api_key"  # Single API key
AUTH_MULTI_KEY = "multi_key"  # Multiple API keys
AUTH_OAUTH = "oauth"  # Browser-based OAuth


GITHUB_SERVERS: Dict[str, Dict[str, Any]] = {
    # ===== Core (No Auth - Must Enable) =====
    "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "category": "core",
        "auth_type": AUTH_NONE,
        "official": True,
        "description": "Knowledge graph-based persistent memory",
    },
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
        "category": "core",
        "auth_type": AUTH_NONE,
        "official": True,
        "description": "Secure file operations with configurable access",
    },
    "fetch": {
        "command": "mcp-server-fetch",
        "args": [],
        "category": "core",
        "auth_type": AUTH_NONE,
        "official": True,
        "description": "HTTP requests - web scraping, API calls",
        "pip_package": "mcp-server-fetch",  # Install with: pip install mcp-server-fetch
    },
    "git": {
        "command": "mcp-server-git",
        "args": [],
        "category": "development",
        "auth_type": AUTH_NONE,
        "official": True,
        "description": "Git operations on local repositories",
        "pip_package": "mcp-server-git",
    },
    "sqlite": {
        "command": "mcp-server-sqlite",
        "args": [],
        "category": "database",
        "auth_type": AUTH_NONE,
        "official": True,
        "description": "SQLite database queries and operations",
        "pip_package": "mcp-server-sqlite",
    },
    "sequential_thinking": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
        "category": "core",
        "auth_type": AUTH_NONE,
        "official": True,
        "description": "Structured step-by-step reasoning for complex tasks",
    },
    "time": {
        "command": "mcp-server-time",
        "args": [],
        "category": "core",
        "auth_type": AUTH_NONE,
        "official": True,
        "description": "Current time, timezone conversions, time calculations",
        "pip_package": "mcp-server-time",
    },

    # ===== Prediction Markets =====
    "polymarket": {
        "command": "npx",
        "args": ["-y", "polymarket-mcp@1.0.0"],
        "category": "markets",
        "npm": "https://npm.im/polymarket-mcp",
        "auth_type": AUTH_NONE,  # No API key needed for read-only market data
        "description": "Polymarket prediction markets: market data, prices",
    },

    # ===== Financial Data =====
    "alphavantage": {
        "command": "uvx",
        "args": ["alphavantage-mcp"],
        "env_key": "ALPHAVANTAGE_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "markets",
        "docs": "https://mcp.alphavantage.co/",
        "official": True,
        "tools": 100,
        "description": "Stocks, crypto, forex, commodities, 53 technical indicators",
        "pip_package": "alphavantage-mcp",
    },
    "twelvedata": {
        "command": "uvx",
        "args": ["mcp-server-twelve-data"],
        "env_key": "TWELVEDATA_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "markets",
        "github": "https://github.com/twelvedata/mcp",
        "official": True,
        "description": "Real-time market data, quotes, technicals via WebSocket",
        "pip_package": "mcp-server-twelve-data",
        "requires_python": ">=3.13",  # Not compatible with Python <3.13
    },

    # ===== Search & Research =====
    "brave_search": {
        "command": "npx",
        "args": ["-y", "@brave/brave-search-mcp-server"],
        "env_key": "BRAVE_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "research",
        "github": "https://github.com/brave/brave-search-mcp-server",
        "official": True,
        "description": "Web, news, image, video search with AI summaries",
    },
    "tavily": {
        "command": "npx",
        "args": ["-y", "tavily-mcp@latest"],
        "env_key": "TAVILY_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "research",
        "github": "https://github.com/tavily-ai/tavily-mcp",
        "official": True,
        "description": "AI-optimized search for LLMs and RAG workflows",
    },

    # ===== Communication =====
    "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "env_keys": ["SLACK_BOT_TOKEN", "SLACK_TEAM_ID"],
        "auth_type": AUTH_MULTI_KEY,
        "category": "communication",
        "github": "https://github.com/modelcontextprotocol/servers",
        "official": True,
        "description": "Slack channels, messages, users, reactions",
    },
    "discord": {
        "command": "npx",
        "args": ["-y", "discord-mcp"],
        "env_key": "DISCORD_BOT_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "communication",
        "github": "https://github.com/olivierdebeufderijcker/discord-mcp",
        "description": "Discord channels, messages, file uploads",
    },
    "gmail": {
        "command": "npx",
        "args": ["-y", "@shinzolabs/gmail-mcp"],
        "env_key": "GMAIL_CREDENTIALS",
        "auth_type": AUTH_API_KEY,
        "category": "communication",
        "github": "https://github.com/shinzo-labs/gmail-mcp",
        "description": "Gmail messages, threads, labels, drafts, search",
    },

    # ===== Knowledge & Documents =====
    "notion": {
        "command": "npx",
        "args": ["-y", "@notionhq/notion-mcp-server"],
        "env_key": "NOTION_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "knowledge",
        "github": "https://github.com/makenotion/notion-mcp-server",
        "official": True,
        "description": "Notion pages, databases, blocks, comments",
    },
    "google_drive": {
        "command": "npx",
        "args": ["-y", "mcp-server-google-workspace"],
        "env_key": "GOOGLE_CREDENTIALS",
        "auth_type": AUTH_API_KEY,
        "category": "knowledge",
        "npm": "https://npm.im/mcp-server-google-workspace",
        "description": "Google Drive, Docs, Sheets, Calendar",
    },
    "aws_kb_retrieval": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-aws-kb-retrieval"],
        "env_keys": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        "auth_type": AUTH_MULTI_KEY,
        "category": "knowledge",
        "github": "https://github.com/modelcontextprotocol/servers",
        "official": True,
        "description": "AWS Knowledge Base retrieval for RAG workflows",
    },

    # ===== Location =====
    "google_maps": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-google-maps"],
        "env_key": "GOOGLE_MAPS_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "location",
        "github": "https://github.com/modelcontextprotocol/servers",
        "official": True,
        "description": "Google Maps places, directions, geocoding",
    },

    # ===== Project Management =====
    "linear": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"],
        "env_key": "LINEAR_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "project_management",
        "docs": "https://linear.app/docs/mcp",
        "official": True,
        "description": "Linear issues, projects, cycles, comments",
    },
    "jira": {
        "command": "npx",
        "args": ["-y", "@aashari/mcp-server-atlassian-jira"],
        "env_keys": ["JIRA_API_TOKEN", "JIRA_EMAIL", "JIRA_HOST"],
        "auth_type": AUTH_MULTI_KEY,
        "category": "project_management",
        "github": "https://github.com/aashari/mcp-server-atlassian-jira",
        "description": "Jira issues, projects, JQL search, dev info",
    },
    "atlassian": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"],
        "auth_type": AUTH_OAUTH,  # OAuth handled via browser
        "category": "project_management",
        "docs": "https://www.atlassian.com/platform/remote-mcp-server",
        "official": True,
        "description": "Official Atlassian - Jira + Confluence (OAuth)",
    },
    "asana": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.asana.com/sse"],
        "env_key": "ASANA_ACCESS_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "project_management",
        "official": True,
        "description": "Asana tasks, projects, workspaces",
    },
    "clickup": {
        "command": "npx",
        "args": ["-y", "@taazkareem/clickup-mcp-server"],
        "env_key": "CLICKUP_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "project_management",
        "github": "https://github.com/taazkareem/clickup-mcp-server",
        "description": "ClickUp tasks, projects, workspaces",
    },

    # ===== Development =====
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env_key": "GITHUB_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "development",
        "github": "https://github.com/modelcontextprotocol/servers",
        "official": True,
        "description": "GitHub repos, issues, PRs, code search",
    },
    "sentry": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.sentry.dev/mcp"],
        "env_key": "SENTRY_AUTH_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "development",
        "docs": "https://docs.sentry.io/product/sentry-mcp/",
        "official": True,
        "description": "Sentry issues, stacktraces, AI root cause analysis",
    },
    "gitlab": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-gitlab"],
        "env_key": "GITLAB_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "development",
        "github": "https://github.com/modelcontextprotocol/servers",
        "official": True,
        "description": "GitLab repos, issues, merge requests, pipelines",
    },

    # ===== CRM =====
    "hubspot": {
        "command": "npx",
        "args": ["-y", "@hubspot/mcp-server"],
        "env_key": "HUBSPOT_ACCESS_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "crm",
        "docs": "https://developers.hubspot.com/mcp",
        "official": True,
        "description": "HubSpot contacts, companies, deals, engagements",
    },

    # ===== Finance =====
    "stripe": {
        "command": "npx",
        "args": ["-y", "@stripe/mcp"],
        "env_key": "STRIPE_SECRET_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "finance",
        "docs": "https://github.com/stripe/agent-toolkit",
        "official": True,
        "description": "Stripe payments, customers, subscriptions",
    },

    # ===== Expense Management =====
    "brex": {
        "command": "npx",
        "args": ["mcp-brex"],
        "env_key": "BREX_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "expense",
        "github": "https://github.com/crazyrabbitLTC/mcp-brex-server",
        "description": "Corporate cards, expense tracking",
    },
    "ramp": {
        "command": "uvx",
        "args": ["ramp-mcp"],
        "env_keys": ["RAMP_CLIENT_ID", "RAMP_CLIENT_SECRET"],
        "auth_type": AUTH_MULTI_KEY,
        "category": "expense",
        "github": "https://github.com/ramp-public/ramp_mcp",
        "official": True,
        "description": "Expense management, spend analysis",
    },

    # ===== Banking =====
    "plaid": {
        "url": "https://api.dashboard.plaid.com/mcp/sse",
        "transport": "sse",
        "env_keys": ["PLAID_CLIENT_ID", "PLAID_SECRET"],
        "auth_type": AUTH_MULTI_KEY,
        "category": "banking",
        "docs": "https://plaid.com/docs/resources/mcp/",
        "official": True,
        "description": "Banking connections API",
    },
    "mercury": {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/jbdamask/mcp-mercury-banking", "mcp-mercury-banking"],
        "env_key": "MERCURY_API_KEY",
        "auth_type": AUTH_API_KEY,
        "category": "banking",
        "github": "https://github.com/jbdamask/mcp-mercury-banking",
        "description": "Startup banking (read-only)",
        "install_note": "Requires: pip install git+https://github.com/jbdamask/mcp-mercury-banking",
    },

    # ===== HR =====
    "bamboohr": {
        "command": "npx",
        "args": ["-y", "@aot-tech/bamboohr-mcp-server"],
        "env_keys": ["BAMBOOHR_API_KEY", "BAMBOOHR_SUBDOMAIN"],
        "auth_type": AUTH_MULTI_KEY,
        "category": "hr",
        "npm": "https://npm.im/@aot-tech/bamboohr-mcp-server",
        "description": "HR, employee data, time off",
    },

    # ===== Infrastructure =====
    "cloudflare": {
        "command": "npx",
        "args": ["-y", "@cloudflare/mcp-server-cloudflare"],
        "env_key": "CLOUDFLARE_API_TOKEN",
        "auth_type": AUTH_API_KEY,
        "category": "infrastructure",
        "github": "https://github.com/cloudflare/mcp-server-cloudflare",
        "official": True,
        "description": "Cloudflare Workers, DNS, security",
    },
}


def get_enabled_github_servers(
    categories: Optional[List[str]] = None,
    enabled_servers: Optional[Set[str]] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Get GitHub servers that are enabled.

    Servers are enabled based on auth_type:
    - "none": User must explicitly enable (check enabled_servers)
    - "api_key": Single env var must be set
    - "multi_key": All env vars must be set
    - "oauth": User must explicitly enable (check enabled_servers)

    Args:
        categories: Filter by category (e.g., ["banking", "expense"])
        enabled_servers: Set of server names user has explicitly enabled
                        (for auth_type="none" and "oauth" servers)

    Returns:
        Dict of server name -> config for enabled servers
    """
    if enabled_servers is None:
        enabled_servers = set()

    servers = {}
    for name, spec in GITHUB_SERVERS.items():
        # Filter by category if specified
        if categories and spec.get("category") not in categories:
            continue

        auth_type = spec.get("auth_type", AUTH_API_KEY)
        is_enabled = False

        if auth_type == AUTH_NONE:
            # No auth required, but must be explicitly enabled
            is_enabled = name in enabled_servers
        elif auth_type == AUTH_OAUTH:
            # OAuth - must be explicitly enabled
            is_enabled = name in enabled_servers
        elif auth_type == AUTH_API_KEY:
            # Single API key
            env_key = spec.get("env_key")
            is_enabled = bool(env_key and os.environ.get(env_key))
        elif auth_type == AUTH_MULTI_KEY:
            # Multiple API keys - all must be set
            env_keys = spec.get("env_keys", [])
            is_enabled = all(os.environ.get(key) for key in env_keys)

        if is_enabled:
            # Build server config
            env_keys = spec.get("env_keys", [spec.get("env_key")])
            if "url" in spec:
                # SSE transport (like Plaid)
                server_config = {
                    "url": spec["url"],
                    "transport": spec.get("transport", "sse"),
                }
            else:
                # Command-based (npx, uvx, python)
                server_config = {
                    "command": spec["command"],
                    "args": spec["args"],
                    "env": {key: os.environ[key] for key in env_keys if key and os.environ.get(key)},
                }

            servers[name] = server_config

    return servers


def get_all_github_servers(enabled_servers: Optional[Set[str]] = None) -> Dict[str, Dict[str, Any]]:
    """
    Get all GitHub servers with their full metadata for frontend display.

    Args:
        enabled_servers: Set of server names user has explicitly enabled

    Returns:
        Dict of server name -> full spec including enabled status
    """
    if enabled_servers is None:
        enabled_servers = set()

    servers = {}
    for name, spec in GITHUB_SERVERS.items():
        auth_type = spec.get("auth_type", AUTH_API_KEY)

        if auth_type == AUTH_NONE:
            is_enabled = name in enabled_servers
        elif auth_type == AUTH_OAUTH:
            is_enabled = name in enabled_servers
        elif auth_type == AUTH_API_KEY:
            env_key = spec.get("env_key")
            is_enabled = bool(env_key and os.environ.get(env_key))
        elif auth_type == AUTH_MULTI_KEY:
            env_keys = spec.get("env_keys", [])
            is_enabled = all(os.environ.get(key) for key in env_keys)
        else:
            is_enabled = False

        servers[name] = {
            **spec,
            "type": "github",
            "enabled": is_enabled,
        }
    return servers


def get_github_categories() -> List[str]:
    """Get all GitHub server categories."""
    categories = set()
    for spec in GITHUB_SERVERS.values():
        if "category" in spec:
            categories.add(spec["category"])
    return sorted(categories)
