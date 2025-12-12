# Wardcliff

Multi-agent prediction market trading simulation with real-time terminal streaming.

Wardcliff runs multiple AI trading agents that research and trade on prediction market events. Watch them think, research, and trade in real-time with a beautiful terminal dashboard.

## Installation

### Install with pip (Recommended)

```bash
pip install wardcliff
```

### Install with pipx (Isolated Environment)

```bash
pipx install wardcliff
```

### Install from Source

```bash
git clone https://github.com/yourorg/wardcliff.git
cd wardcliff
pip install -e .
```

After installation, the `wardcliff` command will be available globally in your terminal.

## Quick Start

### Run Your First Simulation

```bash
# Interactive mode - select event from menu
wardcliff run --interactive

# Run on a specific event
wardcliff run -e us-president-2028 -a 3
```

## Commands

### `wardcliff run` - Run a Trading Simulation

```bash
wardcliff run [OPTIONS]

Options:
  -e, --event TEXT          Event ID to trade
  -m, --multi-outcome       Use multi-outcome events
  -a, --agents INTEGER      Number of agents (default: 3)
  --model TEXT              Model to use
  -i, --interactive         Interactive setup mode
  --load-setup TEXT         Load setup from JSON file
  --save-setup TEXT         Save setup to JSON file
  --legacy                  Use legacy OpenAI agents
  --minimal                 Minimal one-line output
  -v, --verbose             Verbose output with full reasoning
  --debug                   Debug output with raw SDK messages
```

### `wardcliff events` - List Available Events

```bash
wardcliff events                 # List all events
wardcliff events --multi-outcome # Show only multi-outcome events
wardcliff events --json          # Output as JSON
```

### `wardcliff sources` - Manage Data Sources

```bash
wardcliff sources list                    # List all data sources
wardcliff sources list -e super-bowl-2026 # List sources for specific event
wardcliff sources add-url "https://..."   # Add URL to research
wardcliff sources add-doc "./report.pdf"  # Add document to ingest
wardcliff sources clear                   # Clear all sources
```

### `wardcliff mcp` - Manage MCP Servers

```bash
wardcliff mcp list              # Show enabled servers
wardcliff mcp list --all        # Show all available servers
wardcliff mcp enable polymarket # Enable a server
wardcliff mcp disable twitter   # Disable a server
```

### `wardcliff analyze` - Analyze Simulation Logs

```bash
wardcliff analyze logs/simulation.log          # Analyze log file
wardcliff analyze -o report.md --format md     # Output markdown report
wardcliff analyze --format json                # Output JSON
```

### `wardcliff version` - Show Version Info

```bash
wardcliff version  # Show version and check dependencies
```

## Display Modes

### Default Dashboard (Rich UI)

The default mode shows a live-updating dashboard with:
- Market prices with change indicators
- Agent status and activity
- Recent trades
- Price alerts

### Minimal Mode (`--minimal`)

One-line output per trade, suitable for scripting:
```
[14:32:15] Marcus BUY YES $500 @ $0.4521
[14:32:18] Luna SELL NO $250 @ $0.5479
```

### Verbose Mode (`--verbose`)

Full reasoning traces from each agent.

### Debug Mode (`--debug`)

Raw SDK messages for debugging.

## Building from Source

### Development Install

```bash
git clone https://github.com/yourorg/wardcliff.git
cd wardcliff
pip install -e ".[dev]"
```

### Build Standalone Binary

```bash
# Install build dependencies
pip install -e ".[build]"

# Build binary
./scripts/build.sh

# Binary will be at dist/wardcliff
./dist/wardcliff --help
```

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## Configuration

### Environment Variables

**Required:**
- `OPENAI_API_KEY` - Required for OpenAI Agents SDK

**Optional:**
- `DATABASE_URL` - Database connection (default: SQLite)
- `PARALLEL_API_KEY` - For Parallel news monitoring

**MCP Servers (21 local stdio via npx - set env var to enable):**

| Category | Server | Env Var |
|----------|--------|---------|
| **Markets** | Polymarket | (always on) |
| | Alpha Vantage | `ALPHAVANTAGE_API_KEY` |
| | Twelve Data | `TWELVEDATA_API_KEY` |
| **Research** | Brave Search | `BRAVE_API_KEY` |
| | Tavily | `TAVILY_API_KEY` |
| **Communication** | Slack | `SLACK_BOT_TOKEN` + `SLACK_TEAM_ID` |
| | Gmail | `GMAIL_CREDENTIALS` |
| **Knowledge** | Notion | `NOTION_TOKEN` |
| | Google Drive | `GOOGLE_CREDENTIALS` |
| **Project Mgmt** | Linear | `LINEAR_API_KEY` |
| | Jira | `JIRA_API_TOKEN` + `JIRA_EMAIL` + `JIRA_HOST` |
| | Asana | `ASANA_ACCESS_TOKEN` |
| **Development** | GitHub | `GITHUB_TOKEN` |
| | Sentry | `SENTRY_AUTH_TOKEN` |
| **CRM** | HubSpot | `HUBSPOT_ACCESS_TOKEN` |
| **Expense** | Brex | `BREX_API_KEY` |
| | Ramp | `RAMP_CLIENT_ID` + `RAMP_CLIENT_SECRET` |
| **Banking** | Plaid | `PLAID_CLIENT_ID` + `PLAID_SECRET` |
| | Mercury | `MERCURY_API_KEY` |
| **HR** | BambooHR | `BAMBOOHR_API_KEY` + `BAMBOOHR_SUBDOMAIN` |
| **Payroll** | ADP | `ADP_API_KEY` |

See `src/cliff/integrations/mcp/external/github.py` for full server list with sources.

### Config Files

Wardcliff looks for configuration in:
- `~/.wardcliff/config.json` - Global settings
- `~/.wardcliff/mcp.json` - MCP server configuration
- `./.wardcliff.json` - Project-specific settings

## Available Events

### Binary Events
- `fed-rate-dec-2025` - Fed Rate Decision December 2025
- `btc-150k-2025` - Bitcoin $150K in 2025

### Multi-Outcome Events
- `us-president-2028` - US President 2028
- `super-bowl-2026` - Super Bowl LX Winner 2026
- `ai-agi-2030` - AGI by 2030
- `next-fed-chair-2026` - Next Fed Chair 2026

## Architecture

```
src/cliff/
├── cli/           # Typer CLI commands
├── core/          # Market engine, events, metrics
├── agents/        # OpenAI Agents SDK trading agents
├── simulation/    # Controller and orchestration
├── streaming/     # Real-time event streaming
└── infrastructure/# Database, config, logging
```

## License

MIT License
