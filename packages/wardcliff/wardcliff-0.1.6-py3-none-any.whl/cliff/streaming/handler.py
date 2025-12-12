"""
Stream handler for routing events to displays.

Routes SDK messages and simulation events to the appropriate display handlers.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from .events import EventType, StreamEvent

if TYPE_CHECKING:
    from .bridge import StdioBridge

logger = logging.getLogger(__name__)


class StreamHandler:
    """
    Routes simulation events to display handlers.

    Intercepts messages from the OpenAI Agents SDK and simulation controller,
    transforms them to StreamEvents, and dispatches to registered handlers.
    """

    def __init__(self, verbosity: int = 1):
        """
        Initialize the stream handler.

        Args:
            verbosity: Output level (0=minimal, 1=normal, 2=verbose, 3=debug)
        """
        self.verbosity = verbosity
        self._handlers: Dict[EventType, List[Callable[[StreamEvent], None]]] = {}
        self._global_handlers: List[Callable[[StreamEvent], None]] = []
        self.agent_colors: Dict[str, str] = {}
        self._color_index = 0
        self._colors = ["cyan", "magenta", "yellow", "green", "blue", "red"]

    def subscribe(
        self,
        handler: Callable[[StreamEvent], None],
        event_types: Optional[List[EventType]] = None,
    ) -> None:
        """
        Register a handler for events.

        Args:
            handler: Callback function to receive events
            event_types: Specific event types to receive (None = all)
        """
        if event_types is None:
            self._global_handlers.append(handler)
        else:
            for event_type in event_types:
                if event_type not in self._handlers:
                    self._handlers[event_type] = []
                self._handlers[event_type].append(handler)

    def unsubscribe(self, handler: Callable[[StreamEvent], None]) -> None:
        """Remove a handler from all subscriptions."""
        if handler in self._global_handlers:
            self._global_handlers.remove(handler)
        for handlers in self._handlers.values():
            if handler in handlers:
                handlers.remove(handler)

    def emit(self, event: StreamEvent) -> None:
        """
        Emit an event to all registered handlers.

        Args:
            event: The event to dispatch
        """
        # Global handlers receive all events
        for handler in self._global_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error("Handler error: %s", e)

        # Type-specific handlers
        if event.event_type in self._handlers:
            for handler in self._handlers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error("Handler error: %s", e)

    def get_agent_color(self, agent_id: str) -> str:
        """Get a consistent color for an agent."""
        if agent_id not in self.agent_colors:
            self.agent_colors[agent_id] = self._colors[self._color_index % len(self._colors)]
            self._color_index += 1
        return self.agent_colors[agent_id]

    @classmethod
    def with_bridge(cls, bridge: "StdioBridge", verbosity: int = 1) -> "StreamHandler":
        """
        Create a StreamHandler that routes events through a StdioBridge.

        This is used for the Ink UI, replacing RichDisplay as the subscriber.

        Args:
            bridge: The StdioBridge instance connected to the Ink subprocess
            verbosity: Output level (0=minimal, 1=normal, 2=verbose, 3=debug)

        Returns:
            A StreamHandler with the bridge subscribed as a global handler
        """
        handler = cls(verbosity=verbosity)
        handler.subscribe(bridge.handle_event)
        return handler

    # =========================================================================
    # Helper methods to emit common events
    # =========================================================================

    def emit_agent_start(self, agent_id: str) -> None:
        """Emit agent started event."""
        self.emit(StreamEvent(
            event_type=EventType.AGENT_STARTED,
            agent_id=agent_id,
        ))

    def emit_agent_thinking(self, agent_id: str, text: str) -> None:
        """Emit agent thinking/reasoning event."""
        # Truncate based on verbosity
        max_len = {0: 0, 1: 100, 2: 500, 3: 10000}.get(self.verbosity, 100)
        if max_len == 0:
            return  # Skip in minimal mode

        display_text = text[:max_len] + "..." if len(text) > max_len else text
        self.emit(StreamEvent(
            event_type=EventType.AGENT_THINKING,
            agent_id=agent_id,
            data={"text": display_text, "full_text": text if self.verbosity >= 3 else None},
        ))

    def emit_agent_researching(self, agent_id: str, query: str) -> None:
        """Emit agent researching event."""
        self.emit(StreamEvent(
            event_type=EventType.AGENT_RESEARCHING,
            agent_id=agent_id,
            data={"query": query},
        ))

    def emit_agent_complete(self, agent_id: str, decision: str = "hold") -> None:
        """Emit agent completed event."""
        self.emit(StreamEvent(
            event_type=EventType.AGENT_COMPLETED,
            agent_id=agent_id,
            data={"decision": decision},
        ))

    def emit_trade(
        self,
        agent_id: str,
        outcome: str,
        action: str,
        size: float,
        price: float,
        rationale: str = "",
        slippage: float = 0.0,
    ) -> None:
        """Emit trade executed event."""
        self.emit(StreamEvent(
            event_type=EventType.TRADE_EXECUTED,
            agent_id=agent_id,
            data={
                "outcome": outcome,
                "action": action,
                "size": size,
                "price": price,
                "rationale": rationale,
                "slippage": slippage,
            },
        ))

    def emit_price_update(self, prices: Dict[str, float], changes: Optional[Dict[str, float]] = None) -> None:
        """Emit price update event."""
        self.emit(StreamEvent(
            event_type=EventType.PRICE_UPDATE,
            data={"prices": prices, "changes": changes or {}},
        ))

    def emit_alert(self, alert_type: str, outcome: str, message: str, priority: str = "normal") -> None:
        """Emit price alert event."""
        self.emit(StreamEvent(
            event_type=EventType.PRICE_ALERT,
            data={
                "alert_type": alert_type,
                "outcome": outcome,
                "message": message,
                "priority": priority,
            },
        ))

    def emit_iteration(self, iteration: int, trades: int, is_start: bool = True) -> None:
        """Emit iteration start/end event."""
        self.emit(StreamEvent(
            event_type=EventType.ITERATION_START if is_start else EventType.ITERATION_END,
            data={"iteration": iteration, "trades": trades},
        ))

    def emit_simulation_end(self, summary: Dict[str, Any]) -> None:
        """Emit simulation end event."""
        self.emit(StreamEvent(
            event_type=EventType.SIMULATION_END,
            data=summary,
        ))

    def emit_portfolio_update(
        self,
        agent_id: Optional[str] = None,
        total_value: float = 0.0,
        cash: float = 0.0,
        pnl: float = 0.0,
    ) -> None:
        """Emit portfolio update event for P&L tracking."""
        self.emit(StreamEvent(
            event_type=EventType.PORTFOLIO_UPDATE,
            agent_id=agent_id,
            data={
                "total_value": total_value,
                "cash": cash,
                "pnl": pnl,
            },
        ))

    def emit_news_event(self, scenario: str, source: str = "user") -> None:
        """
        Emit a news/hypothetical event that agents will react to.

        This is used for user-injected scenarios like "Satoshi becomes active".
        All agents in the market will receive this as a one-time news event.

        Args:
            scenario: The hypothetical scenario text
            source: Origin of the news ("user" or "external")
        """
        self.emit(StreamEvent(
            event_type=EventType.NEWS_EVENT,
            data={
                "scenario": scenario,
                "source": source,
            },
        ))

    def emit_market_created(
        self,
        market_id: str,
        name: str,
        outcomes: List[str],
        prices: Dict[str, float],
    ) -> None:
        """
        Emit market created event.

        Args:
            market_id: Unique identifier for the market
            name: Human-readable market name
            outcomes: List of outcome names
            prices: Initial prices for each outcome
        """
        self.emit(StreamEvent(
            event_type=EventType.MARKET_CREATED,
            data={
                "market_id": market_id,
                "name": name,
                "outcomes": outcomes,
                "prices": prices,
            },
        ))

    # =========================================================================
    # SDK Message Processing
    # =========================================================================

    def process_sdk_message(self, message: Any, agent_id: str) -> None:
        """
        Process a message from the OpenAI Agents SDK stream.

        This is called for each message yielded by the agent runner.
        """
        # Legacy Claude SDK support - can be removed once fully migrated
        try:
            from claude_code_sdk import AssistantMessage, TextBlock
        except ImportError:
            return

        if hasattr(message, 'content'):
            for block in message.content:
                # Text blocks contain reasoning
                if isinstance(block, TextBlock):
                    self.emit_agent_thinking(agent_id, block.text)

                # Tool use blocks
                elif hasattr(block, 'name'):
                    tool_name = getattr(block, 'name', '')
                    tool_input = getattr(block, 'input', {})

                    # Detect trade tools
                    if 'placeTrade' in tool_name:
                        # Trade attempt - actual execution will come from hooks
                        self.emit(StreamEvent(
                            event_type=EventType.TRADE_ATTEMPT,
                            agent_id=agent_id,
                            data=tool_input,
                        ))

                    # Detect research tools
                    elif 'WebSearch' in tool_name:
                        query = tool_input.get('query', '')
                        self.emit_agent_researching(agent_id, query)
