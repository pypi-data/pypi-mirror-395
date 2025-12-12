"""Configuration management for Wardcliff CLI.

Handles persistent storage of:
- API keys (encrypted)
- Data sources
- Agent configurations
- Monitor settings
"""

from __future__ import annotations

import json
import os
import stat
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import base64


def get_config_dir() -> Path:
    """Get the Wardcliff configuration directory."""
    config_dir = Path.home() / ".wardcliff"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_data_dir() -> Path:
    """Get the Wardcliff data directory."""
    data_dir = get_config_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


# =============================================================================
# API Keys Management
# =============================================================================

@dataclass
class APIKeyConfig:
    """Stores API keys with basic obfuscation."""
    openai: Optional[str] = None
    parallel: Optional[str] = None

    @classmethod
    def load(cls) -> "APIKeyConfig":
        """Load API keys from config file."""
        keys_file = get_config_dir() / "keys.json"
        if not keys_file.exists():
            return cls()

        try:
            with open(keys_file) as f:
                data = json.load(f)
            # Decode keys
            return cls(
                openai=_decode_key(data.get("openai")),
                parallel=_decode_key(data.get("parallel")),
            )
        except Exception:
            return cls()

    def save(self) -> None:
        """Save API keys to config file."""
        keys_file = get_config_dir() / "keys.json"
        data = {
            "openai": _encode_key(self.openai),
            "parallel": _encode_key(self.parallel),
        }
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        with open(keys_file, "w") as f:
            json.dump(data, f, indent=2)

        # Set restrictive permissions (owner read/write only)
        os.chmod(keys_file, stat.S_IRUSR | stat.S_IWUSR)

    def get(self, provider: str) -> Optional[str]:
        """Get API key for a provider."""
        return getattr(self, provider.lower().replace("-", "_"), None)

    def set(self, provider: str, key: str) -> None:
        """Set API key for a provider."""
        attr = provider.lower().replace("-", "_")
        if hasattr(self, attr):
            setattr(self, attr, key)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def remove(self, provider: str) -> None:
        """Remove API key for a provider."""
        attr = provider.lower().replace("-", "_")
        if hasattr(self, attr):
            setattr(self, attr, None)

    def apply_to_environment(self) -> None:
        """Apply stored keys to environment variables."""
        if self.openai:
            os.environ.setdefault("OPENAI_API_KEY", self.openai)
        if self.parallel:
            os.environ.setdefault("PARALLEL_API_KEY", self.parallel)


def _encode_key(key: Optional[str]) -> Optional[str]:
    """Basic obfuscation for stored keys (not true encryption)."""
    if key is None:
        return None
    return base64.b64encode(key.encode()).decode()


def _decode_key(encoded: Optional[str]) -> Optional[str]:
    """Decode obfuscated key."""
    if encoded is None:
        return None
    try:
        return base64.b64decode(encoded.encode()).decode()
    except Exception:
        return None


def mask_key(key: str) -> str:
    """Mask an API key for display."""
    if len(key) <= 8:
        return "****"
    return key[:4] + "*" * (len(key) - 8) + key[-4:]


# =============================================================================
# MCP API Keys Management
# =============================================================================

@dataclass
class MCPKeysConfig:
    """Stores MCP server API keys and enabled server list."""
    keys: Dict[str, str] = field(default_factory=dict)
    enabled_servers: List[str] = field(default_factory=list)  # For no-auth and oauth servers

    @classmethod
    def load(cls) -> "MCPKeysConfig":
        """Load MCP keys from config file."""
        keys_file = get_config_dir() / "mcp_keys.json"
        if not keys_file.exists():
            return cls()

        try:
            with open(keys_file) as f:
                data = json.load(f)
            # Decode all keys (skip 'enabled_servers' which is a list)
            keys_data = {k: v for k, v in data.items() if k != "enabled_servers"}
            decoded = {k: _decode_key(v) for k, v in keys_data.items() if v}
            enabled = data.get("enabled_servers", [])
            return cls(
                keys={k: v for k, v in decoded.items() if v},
                enabled_servers=enabled if isinstance(enabled, list) else []
            )
        except Exception:
            return cls()

    def save(self) -> None:
        """Save MCP keys to config file."""
        keys_file = get_config_dir() / "mcp_keys.json"
        # Encode all keys
        data = {k: _encode_key(v) for k, v in self.keys.items() if v}
        # Add enabled servers list (not encoded)
        data["enabled_servers"] = self.enabled_servers

        with open(keys_file, "w") as f:
            json.dump(data, f, indent=2)

        # Set restrictive permissions (owner read/write only)
        os.chmod(keys_file, stat.S_IRUSR | stat.S_IWUSR)

    def get(self, env_key: str) -> Optional[str]:
        """Get API key for an environment variable."""
        return self.keys.get(env_key)

    def set(self, env_key: str, value: str) -> None:
        """Set API key for an environment variable."""
        self.keys[env_key] = value

    def remove(self, env_key: str) -> bool:
        """Remove API key for an environment variable."""
        if env_key in self.keys:
            del self.keys[env_key]
            return True
        return False

    def has(self, env_key: str) -> bool:
        """Check if a key exists."""
        return env_key in self.keys and bool(self.keys[env_key])

    def apply_to_environment(self) -> None:
        """Apply stored MCP keys to environment variables."""
        for env_key, value in self.keys.items():
            if value:
                os.environ.setdefault(env_key, value)

    def get_all(self) -> Dict[str, str]:
        """Get all stored keys (masked for display)."""
        return {k: mask_key(v) for k, v in self.keys.items() if v}

    # Server enable/disable methods
    def enable_server(self, server_name: str) -> None:
        """Enable a server (for no-auth and oauth servers)."""
        if server_name not in self.enabled_servers:
            self.enabled_servers.append(server_name)

    def disable_server(self, server_name: str) -> bool:
        """Disable a server. Returns True if it was enabled."""
        if server_name in self.enabled_servers:
            self.enabled_servers.remove(server_name)
            return True
        return False

    def is_server_enabled(self, server_name: str) -> bool:
        """Check if a server is enabled."""
        return server_name in self.enabled_servers

    def get_enabled_servers(self) -> set:
        """Get set of enabled server names."""
        return set(self.enabled_servers)


# =============================================================================
# Data Sources Management
# =============================================================================

@dataclass
class DataSource:
    """A single data source for agent research."""
    id: str
    type: str  # url, file, rss, api, database
    location: str  # URL, file path, etc.
    name: Optional[str] = None
    description: Optional[str] = None
    event_id: Optional[str] = None  # If associated with specific event
    enabled: bool = True
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_synced: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourcesConfig:
    """Manages data sources."""
    sources: List[DataSource] = field(default_factory=list)

    @classmethod
    def load(cls) -> "SourcesConfig":
        """Load sources from config file."""
        sources_file = get_config_dir() / "sources.json"
        if not sources_file.exists():
            return cls()

        try:
            with open(sources_file) as f:
                data = json.load(f)
            sources = [DataSource(**s) for s in data.get("sources", [])]
            return cls(sources=sources)
        except Exception:
            return cls()

    def save(self) -> None:
        """Save sources to config file."""
        sources_file = get_config_dir() / "sources.json"
        data = {"sources": [asdict(s) for s in self.sources]}
        with open(sources_file, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, source: DataSource) -> None:
        """Add a new data source."""
        # Generate ID if not provided
        if not source.id:
            source.id = f"{source.type}_{len(self.sources) + 1}"
        self.sources.append(source)

    def remove(self, source_id: str) -> bool:
        """Remove a data source by ID."""
        for i, s in enumerate(self.sources):
            if s.id == source_id:
                self.sources.pop(i)
                return True
        return False

    def get_by_event(self, event_id: str) -> List[DataSource]:
        """Get sources associated with an event."""
        return [s for s in self.sources if s.event_id == event_id or s.event_id is None]

    def get_by_type(self, source_type: str) -> List[DataSource]:
        """Get sources by type."""
        return [s for s in self.sources if s.type == source_type]


# =============================================================================
# Agent Configuration
# =============================================================================

@dataclass
class AgentConfig:
    """Configuration for a trading agent."""
    name: str
    background: str
    personality: str
    risk_tolerance: str = "medium"  # low, medium, high
    enabled: bool = True
    model: str = "gpt-5-mini"
    initial_capital: float = 10000.0
    max_position_pct: float = 0.25  # Max % of capital per position
    research_depth: str = "normal"  # quick, normal, thorough
    custom_instructions: Optional[str] = None


@dataclass
class AgentsConfig:
    """Manages agent configurations."""
    agents: List[AgentConfig] = field(default_factory=list)
    thought_history: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "AgentsConfig":
        """Load agents from config file."""
        agents_file = get_config_dir() / "agents.json"
        if not agents_file.exists():
            # Return default agents
            return cls(agents=[
                AgentConfig(
                    name="Marcus",
                    background="quantitative finance",
                    personality="analytical and data-driven",
                    risk_tolerance="medium",
                ),
                AgentConfig(
                    name="Luna",
                    background="political science",
                    personality="intuitive and contrarian",
                    risk_tolerance="high",
                ),
                AgentConfig(
                    name="Atlas",
                    background="economics",
                    personality="conservative and risk-averse",
                    risk_tolerance="low",
                ),
            ])

        try:
            with open(agents_file) as f:
                data = json.load(f)
            agents = [AgentConfig(**a) for a in data.get("agents", [])]
            return cls(
                agents=agents,
                thought_history=data.get("thought_history", {}),
            )
        except Exception:
            return cls()

    def save(self) -> None:
        """Save agents to config file."""
        agents_file = get_config_dir() / "agents.json"
        data = {
            "agents": [asdict(a) for a in self.agents],
            "thought_history": self.thought_history,
        }
        with open(agents_file, "w") as f:
            json.dump(data, f, indent=2)

    def get(self, name: str) -> Optional[AgentConfig]:
        """Get agent by name."""
        for a in self.agents:
            if a.name.lower() == name.lower():
                return a
        return None

    def add(self, agent: AgentConfig) -> None:
        """Add a new agent."""
        self.agents.append(agent)

    def remove(self, name: str) -> bool:
        """Remove an agent by name."""
        for i, a in enumerate(self.agents):
            if a.name.lower() == name.lower():
                self.agents.pop(i)
                return True
        return False

    def record_thought(self, agent_name: str, thought: Dict[str, Any]) -> None:
        """Record an agent's thought/reasoning."""
        if agent_name not in self.thought_history:
            self.thought_history[agent_name] = []
        thought["timestamp"] = datetime.now().isoformat()
        self.thought_history[agent_name].append(thought)
        # Keep last 100 thoughts per agent
        self.thought_history[agent_name] = self.thought_history[agent_name][-100:]

    def get_thoughts(self, agent_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent thoughts for an agent."""
        return self.thought_history.get(agent_name, [])[-limit:]


# =============================================================================
# Monitor Configuration
# =============================================================================

@dataclass
class MonitorConfig:
    """Configuration for the Parallel monitor.

    The Parallel Monitor API supports:
    - prompt: Search objective/query for finding relevant news
    - check_updates(): Method to poll for new content

    CLI-level settings:
    - enabled: Whether monitoring is active
    - poll_interval_seconds: How often to call the API
    """
    enabled: bool = True
    poll_interval_seconds: int = 3600  # 1 hour default
    prompt: str = ""  # Monitor prompt for news detection (sent to Parallel API)
    last_poll: Optional[str] = None
    last_news_detected: Optional[str] = None

    @classmethod
    def load(cls) -> "MonitorConfig":
        """Load monitor config from file."""
        monitor_file = get_config_dir() / "monitor.json"
        if not monitor_file.exists():
            return cls()

        try:
            with open(monitor_file) as f:
                data = json.load(f)
            return cls(**data)
        except Exception:
            return cls()

    def save(self) -> None:
        """Save monitor config to file."""
        monitor_file = get_config_dir() / "monitor.json"
        with open(monitor_file, "w") as f:
            json.dump(asdict(self), f, indent=2)


# =============================================================================
# MCP Server Configuration
# =============================================================================

@dataclass
class MCPServer:
    """Configuration for a single MCP server."""
    id: str
    name: str
    description: str
    category: str  # trading, research, data
    enabled: bool = False
    command: Optional[str] = None  # Command to run server
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    url: Optional[str] = None  # For remote servers


# Default available MCP servers
DEFAULT_MCP_SERVERS = [
    # Trading
    MCPServer(id="polymarket", name="Polymarket", description="Prediction market data and trading", category="trading", enabled=True),
    MCPServer(id="kalshi", name="Kalshi", description="Event contracts market", category="trading"),
    # Research
    MCPServer(id="web-search", name="Web Search", description="Google/Bing web search", category="research", enabled=True),
    MCPServer(id="news", name="News API", description="News aggregation and analysis", category="research", enabled=True),
    MCPServer(id="twitter", name="Twitter/X", description="Social media sentiment", category="research"),
    # Data
    MCPServer(id="fred", name="FRED", description="Federal Reserve economic data", category="data"),
    MCPServer(id="yahoo-finance", name="Yahoo Finance", description="Market and financial data", category="data"),
]


@dataclass
class MCPConfig:
    """Configuration for MCP servers.

    Stores which servers are enabled and any custom server configurations.
    """
    servers: List[MCPServer] = field(default_factory=list)

    @classmethod
    def load(cls) -> "MCPConfig":
        """Load MCP config from file."""
        mcp_file = get_config_dir() / "mcp.json"
        if not mcp_file.exists():
            # Return default servers
            return cls(servers=list(DEFAULT_MCP_SERVERS))

        try:
            with open(mcp_file) as f:
                data = json.load(f)
            servers = [MCPServer(**s) for s in data.get("servers", [])]
            return cls(servers=servers)
        except Exception:
            return cls(servers=list(DEFAULT_MCP_SERVERS))

    def save(self) -> None:
        """Save MCP config to file."""
        mcp_file = get_config_dir() / "mcp.json"
        data = {"servers": [asdict(s) for s in self.servers]}
        with open(mcp_file, "w") as f:
            json.dump(data, f, indent=2)

    def get(self, server_id: str) -> Optional[MCPServer]:
        """Get server by ID."""
        for s in self.servers:
            if s.id == server_id:
                return s
        return None

    def enable(self, server_id: str) -> bool:
        """Enable a server."""
        server = self.get(server_id)
        if server:
            server.enabled = True
            return True
        return False

    def disable(self, server_id: str) -> bool:
        """Disable a server."""
        server = self.get(server_id)
        if server:
            server.enabled = False
            return True
        return False

    def get_enabled(self) -> List[MCPServer]:
        """Get all enabled servers."""
        return [s for s in self.servers if s.enabled]

    def get_by_category(self, category: str) -> List[MCPServer]:
        """Get servers by category."""
        return [s for s in self.servers if s.category == category]

    def add_server(self, server: MCPServer) -> None:
        """Add a custom server."""
        # Remove existing with same ID
        self.servers = [s for s in self.servers if s.id != server.id]
        self.servers.append(server)

    def remove_server(self, server_id: str) -> bool:
        """Remove a custom server."""
        for i, s in enumerate(self.servers):
            if s.id == server_id:
                self.servers.pop(i)
                return True
        return False

    def to_claude_config(self) -> Dict[str, Any]:
        """Generate Claude Code MCP configuration format."""
        config = {"mcpServers": {}}
        for server in self.get_enabled():
            if server.command:
                config["mcpServers"][server.id] = {
                    "command": server.command,
                    "args": server.args,
                    "env": server.env,
                }
            elif server.url:
                config["mcpServers"][server.id] = {
                    "url": server.url,
                }
        return config


# =============================================================================
# Session State (for agent chat)
# =============================================================================

@dataclass
class ChatMessage:
    """A message in an agent chat session."""
    role: str  # user, agent
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ChatSession:
    """An interactive chat session with an agent."""
    agent_name: str
    messages: List[ChatMessage] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session."""
        self.messages.append(ChatMessage(role=role, content=content))

    def get_history(self, limit: int = 10) -> List[ChatMessage]:
        """Get recent message history."""
        return self.messages[-limit:]

    def to_prompt_context(self) -> str:
        """Convert session to context for prompting."""
        lines = []
        for msg in self.messages[-10:]:
            prefix = "User: " if msg.role == "user" else f"{self.agent_name}: "
            lines.append(f"{prefix}{msg.content}")
        return "\n".join(lines)
