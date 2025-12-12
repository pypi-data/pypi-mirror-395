"""
Smithery-Hosted Enterprise MCP Servers

60+ pre-configured MCP servers hosted on Smithery.ai, organized by category.
These servers are enabled automatically when their environment variable is set.

Usage:
    from mcp_servers.external.smithery import SMITHERY_SERVERS, get_enabled_smithery_servers

    # Get all servers with env vars set
    servers = get_enabled_smithery_servers()
"""

import os
from typing import Any, Dict, List, Optional

# Smithery base URL for hosted MCP servers
SMITHERY_BASE = "https://server.smithery.ai"


SMITHERY_SERVERS: Dict[str, Dict[str, Any]] = {
    # ===== Communication & Collaboration =====
    "slack": {
        "url": f"{SMITHERY_BASE}/slack/mcp",
        "env_key": "SLACK_BOT_TOKEN",
        "category": "communication",
        "tools": 142,
        "description": "Messaging, channels, reactions",
    },
    "gmail": {
        "url": f"{SMITHERY_BASE}/gmail/mcp",
        "env_key": "GMAIL_OAUTH_TOKEN",
        "category": "communication",
        "tools": 27,
        "description": "Send, draft, labels, batch ops",
    },
    "outlook": {
        "url": f"{SMITHERY_BASE}/outlook/mcp",
        "env_key": "OUTLOOK_OAUTH_TOKEN",
        "category": "communication",
        "tools": 51,
        "description": "Email, calendar, contacts",
    },
    "discord": {
        "url": f"{SMITHERY_BASE}/discord/mcp",
        "env_key": "DISCORD_BOT_TOKEN",
        "category": "communication",
        "description": "Server/channel management",
    },
    "twilio": {
        "url": f"{SMITHERY_BASE}/@blockehh/mcp_twilio_build/mcp",
        "env_key": "TWILIO_AUTH_TOKEN",
        "category": "communication",
        "description": "SMS, voice, messaging",
    },
    "zoom": {
        "url": f"{SMITHERY_BASE}/zoom/mcp",
        "env_key": "ZOOM_OAUTH_TOKEN",
        "category": "communication",
        "tools": 17,
        "description": "Meetings, webinars, recordings",
    },

    # ===== Knowledge & Documents =====
    "notion": {
        "url": f"{SMITHERY_BASE}/notion/mcp",
        "env_key": "NOTION_API_KEY",
        "category": "knowledge",
        "description": "Pages, databases, search",
    },
    "google_drive": {
        "url": f"{SMITHERY_BASE}/@rishipradeep-think41/google-drive-mcp/mcp",
        "env_key": "GOOGLE_OAUTH_TOKEN",
        "category": "knowledge",
        "description": "Files, folders, sharing",
    },
    "google_sheets": {
        "url": f"{SMITHERY_BASE}/@SarthakS97/sheeter-mcp-server/mcp",
        "env_key": "GOOGLE_OAUTH_TOKEN",
        "category": "knowledge",
        "description": "Spreadsheet automation",
    },
    "google_workspace": {
        "url": f"{SMITHERY_BASE}/@taylorwilsdon/google_workspace_mcp/mcp",
        "env_key": "GOOGLE_OAUTH_TOKEN",
        "category": "knowledge",
        "description": "Gmail+Calendar+Docs+Sheets",
    },
    "dropbox": {
        "url": f"{SMITHERY_BASE}/dropbox/mcp",
        "env_key": "DROPBOX_ACCESS_TOKEN",
        "category": "knowledge",
        "tools": 12,
        "description": "Cloud storage, sync, sharing",
    },
    "box": {
        "url": f"{SMITHERY_BASE}/box/mcp",
        "env_key": "BOX_ACCESS_TOKEN",
        "category": "knowledge",
        "tools": 200,
        "description": "Enterprise content management",
    },
    "airtable": {
        "url": f"{SMITHERY_BASE}/airtable/mcp",
        "env_key": "AIRTABLE_API_KEY",
        "category": "knowledge",
        "tools": 17,
        "description": "Spreadsheet-database hybrid",
    },
    "confluence": {
        "url": f"{SMITHERY_BASE}/confluence/mcp",
        "env_key": "CONFLUENCE_API_TOKEN",
        "category": "knowledge",
        "description": "Knowledge base, docs",
    },

    # ===== Project Management =====
    "linear": {
        "url": f"{SMITHERY_BASE}/linear/mcp",
        "env_key": "LINEAR_API_KEY",
        "category": "project_management",
        "description": "Issues, projects, cycles",
    },
    "jira": {
        "url": f"{SMITHERY_BASE}/@Wajahat-bitsol/jira-mcp-smithery/mcp",
        "env_key": "JIRA_API_TOKEN",
        "category": "project_management",
        "description": "Issues, projects, comments",
    },
    "asana": {
        "url": f"{SMITHERY_BASE}/asana/mcp",
        "env_key": "ASANA_ACCESS_TOKEN",
        "category": "project_management",
        "description": "Tasks, projects, workspaces",
    },
    "clickup": {
        "url": f"{SMITHERY_BASE}/clickup/mcp",
        "env_key": "CLICKUP_API_TOKEN",
        "category": "project_management",
        "description": "Tasks, docs, goals",
    },
    "monday": {
        "url": f"{SMITHERY_BASE}/monday/mcp",
        "env_key": "MONDAY_API_TOKEN",
        "category": "project_management",
        "tools": 62,
        "description": "Work management, boards",
    },
    "trello": {
        "url": f"{SMITHERY_BASE}/trello/mcp",
        "env_key": "TRELLO_API_KEY",
        "category": "project_management",
        "tools": 200,
        "description": "Kanban boards, cards",
    },
    "wrike": {
        "url": f"{SMITHERY_BASE}/wrike/mcp",
        "env_key": "WRIKE_ACCESS_TOKEN",
        "category": "project_management",
        "tools": 38,
        "description": "Project management, Gantt",
    },
    "todoist": {
        "url": f"{SMITHERY_BASE}/@Hint-Services/mcp-todoist/mcp",
        "env_key": "TODOIST_API_TOKEN",
        "category": "project_management",
        "description": "Task management",
    },

    # ===== Development & DevOps =====
    "github": {
        "url": f"{SMITHERY_BASE}/github/mcp",
        "env_key": "GITHUB_TOKEN",
        "category": "development",
        "description": "Repos, issues, PRs",
    },
    "gitlab": {
        "url": f"{SMITHERY_BASE}/gitlab/mcp",
        "env_key": "GITLAB_TOKEN",
        "category": "development",
        "description": "Repos, MRs, CI/CD",
    },
    "pagerduty": {
        "url": f"{SMITHERY_BASE}/pagerduty/mcp",
        "env_key": "PAGERDUTY_API_KEY",
        "category": "devops",
        "description": "Incidents, alerts",
    },
    "sentry": {
        "url": f"{SMITHERY_BASE}/sentry/mcp",
        "env_key": "SENTRY_AUTH_TOKEN",
        "category": "devops",
        "description": "Error tracking",
    },
    "azure_cli": {
        "url": f"{SMITHERY_BASE}/@jdubois/azure-cli-mcp/mcp",
        "env_key": "AZURE_CREDENTIALS",
        "category": "devops",
        "description": "Azure resources",
    },

    # ===== CRM & Sales =====
    "salesforce": {
        "url": f"{SMITHERY_BASE}/salesforce/mcp",
        "env_key": "SALESFORCE_TOKEN",
        "category": "crm",
        "description": "Leads, contacts, opportunities",
    },
    "hubspot": {
        "url": f"{SMITHERY_BASE}/hubspot/mcp",
        "env_key": "HUBSPOT_API_KEY",
        "category": "crm",
        "description": "CRM, email, marketing",
    },
    "pipedrive": {
        "url": f"{SMITHERY_BASE}/pipedrive/mcp",
        "env_key": "PIPEDRIVE_API_TOKEN",
        "category": "crm",
        "tools": 200,
        "description": "Sales pipeline, deals",
    },

    # ===== Finance & Accounting =====
    "stripe": {
        "url": f"{SMITHERY_BASE}/stripe/mcp",
        "env_key": "STRIPE_SECRET_KEY",
        "category": "finance",
        "description": "Payments, customers, invoices",
    },
    "quickbooks": {
        "url": f"{SMITHERY_BASE}/quickbooks/mcp",
        "env_key": "QUICKBOOKS_OAUTH_TOKEN",
        "category": "finance",
        "description": "Accounting, expenses",
    },
    "xero": {
        "url": f"{SMITHERY_BASE}/xero/mcp",
        "env_key": "XERO_OAUTH_TOKEN",
        "category": "finance",
        "tools": 40,
        "description": "Cloud accounting, invoicing",
    },
    "paypal": {
        "url": f"{SMITHERY_BASE}/paypal/mcp",
        "env_key": "PAYPAL_CLIENT_SECRET",
        "category": "finance",
        "tools": 2,
        "description": "Invoices, transactions",
    },
    "harvest": {
        "url": f"{SMITHERY_BASE}/harvest/mcp",
        "env_key": "HARVEST_ACCESS_TOKEN",
        "category": "finance",
        "tools": 58,
        "description": "Time tracking, invoicing",
    },
    "square": {
        "url": f"{SMITHERY_BASE}/square/mcp",
        "env_key": "SQUARE_ACCESS_TOKEN",
        "category": "finance",
        "tools": 26,
        "description": "Payments, POS, disputes",
    },
    "freshbooks": {
        "url": f"{SMITHERY_BASE}/freshbooks/mcp",
        "env_key": "FRESHBOOKS_ACCESS_TOKEN",
        "category": "finance",
        "tools": 2,
        "description": "SMB accounting, projects",
    },

    # ===== Banking & Market Data =====
    "lunchflow": {
        "url": f"{SMITHERY_BASE}/@lunchflow/mcp/mcp",
        "env_key": "LUNCHFLOW_API_KEY",
        "category": "banking",
        "tools": 3,
        "description": "Banking aggregator (20k+ banks, 40+ countries)",
    },
    "fmp": {
        "url": f"{SMITHERY_BASE}/@imbenrabi/financial-modeling-prep-mcp-server/mcp",
        "env_key": "FMP_API_KEY",
        "category": "markets",
        "tools": 250,
        "description": "Stocks, crypto, forex, market data",
    },

    # ===== Customer Support =====
    "zendesk": {
        "url": f"{SMITHERY_BASE}/zendesk/mcp",
        "env_key": "ZENDESK_API_TOKEN",
        "category": "support",
        "description": "Tickets, knowledge base",
    },
    "intercom": {
        "url": f"{SMITHERY_BASE}/intercom/mcp",
        "env_key": "INTERCOM_ACCESS_TOKEN",
        "category": "support",
        "description": "Live chat, messaging",
    },

    # ===== Databases & Data =====
    "postgres": {
        "url": f"{SMITHERY_BASE}/@smithery-ai/postgres/mcp",
        "env_key": "POSTGRES_CONNECTION_STRING",
        "category": "database",
        "description": "Read-only SQL",
    },
    "mysql": {
        "url": f"{SMITHERY_BASE}/@f4ww4z/mcp-mysql-server/mcp",
        "env_key": "MYSQL_CONNECTION_STRING",
        "category": "database",
        "description": "SQL queries",
    },
    "bigquery": {
        "url": f"{SMITHERY_BASE}/mcp-server-bigquery/mcp",
        "env_key": "GOOGLE_APPLICATION_CREDENTIALS",
        "category": "database",
        "description": "Google analytics",
    },
    "snowflake": {
        "url": f"{SMITHERY_BASE}/mcp_snowflake_server/mcp",
        "env_key": "SNOWFLAKE_CONNECTION_STRING",
        "category": "database",
        "description": "Data warehouse",
    },
    "supabase": {
        "url": f"{SMITHERY_BASE}/supabase/mcp",
        "env_key": "SUPABASE_ACCESS_TOKEN",
        "category": "database",
        "tools": 29,
        "description": "Postgres + Edge Functions",
    },

    # ===== Scheduling =====
    "calendly": {
        "url": f"{SMITHERY_BASE}/calendly/mcp",
        "env_key": "CALENDLY_API_KEY",
        "category": "scheduling",
        "tools": 42,
        "description": "Appointment scheduling",
    },

    # ===== E-commerce =====
    "shopify": {
        "url": f"{SMITHERY_BASE}/shopify/mcp",
        "env_key": "SHOPIFY_ACCESS_TOKEN",
        "category": "ecommerce",
        "tools": 36,
        "description": "Products, orders, customers",
    },

    # ===== Marketing =====
    "mailchimp": {
        "url": f"{SMITHERY_BASE}/mailchimp/mcp",
        "env_key": "MAILCHIMP_API_KEY",
        "category": "marketing",
        "tools": 200,
        "description": "Email campaigns, automation",
    },

    # ===== Social Media =====
    "twitter": {
        "url": f"{SMITHERY_BASE}/twitter/mcp",
        "env_key": "TWITTER_BEARER_TOKEN",
        "category": "social",
        "tools": 75,
        "description": "Posts, DMs, lists",
    },
    "linkedin": {
        "url": f"{SMITHERY_BASE}/linkedin/mcp",
        "env_key": "LINKEDIN_ACCESS_TOKEN",
        "category": "social",
        "tools": 4,
        "description": "Posts, company info",
    },
    "youtube": {
        "url": f"{SMITHERY_BASE}/youtube/mcp",
        "env_key": "YOUTUBE_API_KEY",
        "category": "social",
        "tools": 16,
        "description": "Videos, playlists, captions",
    },
    "instagram": {
        "url": f"{SMITHERY_BASE}/instagram/mcp",
        "env_key": "INSTAGRAM_ACCESS_TOKEN",
        "category": "social",
        "tools": 16,
        "description": "Posts, stories, DMs",
    },

    # ===== Design =====
    "figma": {
        "url": f"{SMITHERY_BASE}/@ai-zerolab/mcp-figma/mcp",
        "env_key": "FIGMA_ACCESS_TOKEN",
        "category": "design",
        "description": "Design files, components",
    },
    "miro": {
        "url": f"{SMITHERY_BASE}/miro/mcp",
        "env_key": "MIRO_ACCESS_TOKEN",
        "category": "design",
        "description": "Whiteboard, diagrams",
    },

    # Note: Polymarket moved to github.py (local npx, no Smithery OAuth needed)
}


def get_enabled_smithery_servers(
    categories: Optional[List[str]] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Get Smithery servers that are enabled.

    Servers are enabled if:
    - always_enabled=True (core features like polymarket), OR
    - Their env_key is set

    Args:
        categories: Filter by category (e.g., ["finance", "crm"])

    Returns:
        Dict of server name -> config for enabled servers
    """
    servers = {}
    for name, spec in SMITHERY_SERVERS.items():
        # Filter by category if specified
        if categories and spec.get("category") not in categories:
            continue

        # Check if always enabled or env var is set
        always_enabled = spec.get("always_enabled", False)
        env_key = spec.get("env_key")
        if always_enabled or (env_key and os.environ.get(env_key)):
            servers[name] = {"url": spec["url"]}

    return servers


def get_all_smithery_servers() -> Dict[str, Dict[str, Any]]:
    """
    Get all Smithery servers with their full metadata for frontend display.

    Returns:
        Dict of server name -> full spec including enabled status
    """
    servers = {}
    for name, spec in SMITHERY_SERVERS.items():
        always_enabled = spec.get("always_enabled", False)
        env_key = spec.get("env_key")
        servers[name] = {
            **spec,
            "type": "smithery",
            "enabled": always_enabled or bool(env_key and os.environ.get(env_key)),
        }
    return servers


def get_smithery_categories() -> List[str]:
    """Get all Smithery server categories."""
    categories = set()
    for spec in SMITHERY_SERVERS.values():
        if "category" in spec:
            categories.add(spec["category"])
    return sorted(categories)
