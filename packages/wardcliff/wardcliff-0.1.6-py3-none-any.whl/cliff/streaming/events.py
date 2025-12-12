"""
Stream event types for real-time terminal output.

Defines the events that flow through the streaming system.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class EventType(Enum):
    """Types of events that can be streamed to the display."""
    # Agent lifecycle
    AGENT_STARTED = "agent_started"
    AGENT_THINKING = "agent_thinking"
    AGENT_RESEARCHING = "agent_researching"
    AGENT_DECISION = "agent_decision"
    AGENT_COMPLETED = "agent_completed"
    AGENT_ERROR = "agent_error"

    # Trade events
    TRADE_ATTEMPT = "trade_attempt"
    TRADE_EXECUTED = "trade_executed"
    TRADE_REJECTED = "trade_rejected"

    # Market events
    PRICE_UPDATE = "price_update"
    PRICE_ALERT = "price_alert"
    MARKET_STATE = "market_state"
    MARKET_CREATED = "market_created"

    # Simulation events
    SIMULATION_START = "simulation_start"
    SIMULATION_END = "simulation_end"
    ITERATION_START = "iteration_start"
    ITERATION_END = "iteration_end"
    CONSENSUS_REACHED = "consensus_reached"

    # Portfolio events
    PORTFOLIO_UPDATE = "portfolio_update"

    # Hypothetical/News events (injected by user)
    NEWS_EVENT = "news_event"


@dataclass
class StreamEvent:
    """
    A single event in the simulation stream.

    All events flowing through the streaming system use this format.
    """
    event_type: EventType
    agent_id: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "type": self.event_type.value,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
        }


@dataclass
class TradeEvent(StreamEvent):
    """Specialized event for trade execution."""
    outcome: str = ""
    action: str = ""  # buy/sell
    size: float = 0.0
    price: float = 0.0
    rationale: str = ""
    slippage: float = 0.0


@dataclass
class PriceEvent(StreamEvent):
    """Specialized event for price updates."""
    prices: Dict[str, float] = field(default_factory=dict)
    changes: Dict[str, float] = field(default_factory=dict)


@dataclass
class AlertEvent(StreamEvent):
    """Specialized event for price alerts."""
    alert_type: str = ""
    outcome: str = ""
    message: str = ""
    priority: str = "normal"


@dataclass
class NewsEvent(StreamEvent):
    """
    Specialized event for user-injected hypotheticals/news.

    These are one-time events that agents react to, simulating
    scenarios like "Satoshi becomes active on his wallet again".
    """
    scenario: str = ""
    source: str = "user"  # "user" or "external"
