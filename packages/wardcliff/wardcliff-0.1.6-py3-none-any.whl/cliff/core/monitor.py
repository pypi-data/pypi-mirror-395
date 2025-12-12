"""
Market Monitor - Agent-Configurable Price and Trade Monitoring.

Agents can configure what conditions trigger alerts via the configureAlerts tool.
This allows agents to set up monitoring for:
- Price changes (% threshold)
- Large trades by other agents
- Price crossing specific thresholds
- Custom conditions

The monitor runs in the background and queues alerts for the agent to check.

Migrated from market_monitor.py
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from cliff.core.events import EventMarket
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AlertType(Enum):
    """Types of alerts the monitor can generate."""
    PRICE_CHANGE = "price_change"
    LARGE_TRADE = "large_trade"
    PRICE_THRESHOLD = "price_threshold"
    AGENT_TRADE = "agent_trade"


@dataclass
class AlertConditions:
    """
    Agent-configurable conditions for generating alerts.

    Set via the configureAlerts tool.
    """
    # Price change alerts
    price_change_pct: float = 0.05  # 5% default
    price_change_outcomes: Optional[List[str]] = None  # None = all outcomes

    # Trade size alerts (when any agent trades > threshold)
    trade_size_threshold: Optional[float] = None  # USD amount
    exclude_self: bool = True  # Don't alert on own trades

    # Price threshold alerts (absolute levels)
    price_above: Optional[Dict[str, float]] = None  # {"Trump": 0.60}
    price_below: Optional[Dict[str, float]] = None  # {"Harris": 0.40}

    # Agent-specific trade alerts
    agent_trade_size: Optional[float] = None  # Alert when another agent trades > X
    watch_agents: Optional[List[str]] = None  # Specific agents to watch (None = all)

    # Control
    enabled: bool = True
    poll_interval: float = 5.0  # seconds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "price_change_pct": self.price_change_pct,
            "price_change_outcomes": self.price_change_outcomes,
            "trade_size_threshold": self.trade_size_threshold,
            "exclude_self": self.exclude_self,
            "price_above": self.price_above,
            "price_below": self.price_below,
            "agent_trade_size": self.agent_trade_size,
            "watch_agents": self.watch_agents,
            "enabled": self.enabled,
            "poll_interval": self.poll_interval,
        }


@dataclass
class PriceAlert:
    """
    Alert generated when configured conditions are met.

    Includes the alert type and details about what triggered it.
    """
    alert_type: str  # AlertType value
    outcome: str
    message: str  # Human-readable description

    # Price info
    old_price: Optional[float] = None
    new_price: Optional[float] = None
    change_pct: Optional[float] = None
    direction: Optional[str] = None  # "up" or "down"

    # Trade info (for trade alerts)
    trade_agent_id: Optional[str] = None
    trade_size: Optional[float] = None
    trade_direction: Optional[str] = None  # "buy" or "sell"

    # Metadata
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    market_id: Optional[str] = None
    market_name: Optional[str] = None
    priority: str = "normal"  # "low", "normal", "high", "urgent"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "alert_type": self.alert_type,
            "outcome": self.outcome,
            "message": self.message,
            "old_price": round(self.old_price, 4) if self.old_price else None,
            "new_price": round(self.new_price, 4) if self.new_price else None,
            "change_pct": round(self.change_pct, 4) if self.change_pct else None,
            "direction": self.direction,
            "trade_agent_id": self.trade_agent_id,
            "trade_size": round(self.trade_size, 2) if self.trade_size else None,
            "trade_direction": self.trade_direction,
            "timestamp": self.timestamp.isoformat(),
            "market_id": self.market_id,
            "market_name": self.market_name,
            "priority": self.priority,
        }


@dataclass
class PriceSnapshot:
    """Point-in-time snapshot of all market prices."""
    prices: Dict[str, float]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    triggered_by: Optional[str] = None  # trade_id or "monitor"


@dataclass
class AgentAlertConfig:
    """
    Agent-configured alert for a specific outcome.

    One-shot behavior: triggers once then auto-deactivates.
    Agent can set new alerts after reviewing triggered ones.
    """
    agent_id: str
    outcome: str
    conditions: Dict[str, Any]  # price_above, price_below, change_pct, large_trade_usd, any_trade
    rationale: str
    status: str = "active"  # "active" | "triggered" | "delivered"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    triggered_at: Optional[datetime] = None

    # Snapshot of price when alert was created (for change_pct calculation)
    baseline_price: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "outcome": self.outcome,
            "conditions": self.conditions,
            "rationale": self.rationale,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "triggered_at": self.triggered_at.isoformat() if self.triggered_at else None,
            "baseline_price": round(self.baseline_price, 4) if self.baseline_price else None,
        }


@dataclass
class RichPriceAlert:
    """
    Enhanced alert with full context for agent decision-making.

    Includes trade attribution, limit order proximity, and position impact.
    """
    # Basic info
    alert_type: str
    outcome: str
    message: str

    # Price movement
    old_price: float
    new_price: float
    change_pct: float
    direction: str  # "up" or "down"

    # Trade attribution (who caused this?)
    triggering_agent: Optional[str] = None
    triggering_trade_usd: Optional[float] = None
    triggering_trade_direction: Optional[str] = None

    # Limit order proximity (agent's orders at risk)
    limit_orders_at_risk: List[Dict[str, Any]] = field(default_factory=list)
    # Each: {order_id, order_type, trigger_price, distance_pct}

    # Position impact
    position_tokens: Optional[float] = None
    avg_entry_price: Optional[float] = None
    unrealized_pnl_before: Optional[float] = None
    unrealized_pnl_after: Optional[float] = None
    pnl_change: Optional[float] = None

    # Original rationale for this alert
    alert_rationale: Optional[str] = None

    # Which condition triggered
    condition_met: Optional[str] = None

    # Metadata
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    market_name: Optional[str] = None
    priority: str = "normal"  # "normal", "high", "urgent"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_type": self.alert_type,
            "outcome": self.outcome,
            "message": self.message,
            "old_price": round(self.old_price, 4),
            "new_price": round(self.new_price, 4),
            "change_pct": round(self.change_pct, 4),
            "direction": self.direction,
            "triggering_agent": self.triggering_agent,
            "triggering_trade_usd": round(self.triggering_trade_usd, 2) if self.triggering_trade_usd else None,
            "triggering_trade_direction": self.triggering_trade_direction,
            "limit_orders_at_risk": self.limit_orders_at_risk,
            "position_tokens": round(self.position_tokens, 4) if self.position_tokens else None,
            "avg_entry_price": round(self.avg_entry_price, 4) if self.avg_entry_price else None,
            "unrealized_pnl_before": round(self.unrealized_pnl_before, 2) if self.unrealized_pnl_before else None,
            "unrealized_pnl_after": round(self.unrealized_pnl_after, 2) if self.unrealized_pnl_after else None,
            "pnl_change": round(self.pnl_change, 2) if self.pnl_change else None,
            "alert_rationale": self.alert_rationale,
            "condition_met": self.condition_met,
            "timestamp": self.timestamp.isoformat(),
            "market_name": self.market_name,
            "priority": self.priority,
        }


class MarketMonitor:
    """
    Agent-configurable market monitor.

    Agents configure what conditions trigger alerts via the configureAlerts tool.
    The monitor runs in the background and queues alerts for agents to check.
    """

    def __init__(
        self,
        market: "EventMarket",
        agent_id: str = "default",
        max_alerts: int = 100,
        on_alert: Optional[Callable[[PriceAlert], None]] = None,
        db_session: Optional["AsyncSession"] = None,
    ):
        """
        Initialize market monitor.

        Args:
            market: EventMarket to monitor
            agent_id: ID of the agent this monitor belongs to
            max_alerts: Maximum alerts to queue
            on_alert: Optional callback when alert is generated
            db_session: Optional database session for persistence
        """
        self.market = market
        self.agent_id = agent_id
        self.max_alerts = max_alerts
        self.on_alert = on_alert
        self.db_session = db_session

        # Agent-configurable conditions (set via configureAlerts tool)
        self.conditions = AlertConditions()

        # State
        self.last_prices: Dict[str, float] = {}
        self.alerts: asyncio.Queue[PriceAlert] = asyncio.Queue(maxsize=max_alerts)
        self.price_history: List[PriceSnapshot] = []
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._subscribers: List[asyncio.Queue] = []

        # Track price thresholds that have already triggered (to avoid repeats)
        self._triggered_above: Set[str] = set()
        self._triggered_below: Set[str] = set()

        # Agent-specific alert configs (new interrupt-based system)
        # Key: agent_id -> list of AgentAlertConfig
        self._agent_alerts: Dict[str, List[AgentAlertConfig]] = {}

        # Triggered alerts ready for injection (agent_id -> list of RichPriceAlert)
        self._triggered_alerts: Dict[str, List[RichPriceAlert]] = {}

        # Last trade info for attribution
        self._last_trade: Optional[Dict[str, Any]] = None

    @property
    def is_running(self) -> bool:
        """Check if monitor is running."""
        return self._running

    # =========================================================================
    # Agent Configuration API
    # =========================================================================

    def configure(
        self,
        price_change_pct: Optional[float] = None,
        price_change_outcomes: Optional[List[str]] = None,
        trade_size_threshold: Optional[float] = None,
        exclude_self: Optional[bool] = None,
        price_above: Optional[Dict[str, float]] = None,
        price_below: Optional[Dict[str, float]] = None,
        agent_trade_size: Optional[float] = None,
        watch_agents: Optional[List[str]] = None,
        enabled: Optional[bool] = None,
        poll_interval: Optional[float] = None,
    ) -> AlertConditions:
        """
        Configure alert conditions. Called by agent via configureAlerts tool.

        Args:
            price_change_pct: Alert when price moves by this % (e.g., 0.05 = 5%)
            price_change_outcomes: Which outcomes to monitor (None = all)
            trade_size_threshold: Alert when any trade exceeds this USD amount
            exclude_self: Don't alert on this agent's own trades
            price_above: Alert when outcome price goes above threshold
            price_below: Alert when outcome price goes below threshold
            agent_trade_size: Alert when another agent trades more than X
            watch_agents: Specific agent IDs to watch (None = all)
            enabled: Turn monitoring on/off
            poll_interval: Seconds between price checks

        Returns:
            Updated AlertConditions
        """
        if price_change_pct is not None:
            self.conditions.price_change_pct = price_change_pct
        if price_change_outcomes is not None:
            self.conditions.price_change_outcomes = price_change_outcomes
        if trade_size_threshold is not None:
            self.conditions.trade_size_threshold = trade_size_threshold
        if exclude_self is not None:
            self.conditions.exclude_self = exclude_self
        if price_above is not None:
            self.conditions.price_above = price_above
            # Reset triggered state for new thresholds
            self._triggered_above = set()
        if price_below is not None:
            self.conditions.price_below = price_below
            self._triggered_below = set()
        if agent_trade_size is not None:
            self.conditions.agent_trade_size = agent_trade_size
        if watch_agents is not None:
            self.conditions.watch_agents = watch_agents
        if enabled is not None:
            self.conditions.enabled = enabled
        if poll_interval is not None:
            self.conditions.poll_interval = poll_interval

        logger.info(
            "Monitor configured for agent %s: %s",
            self.agent_id,
            self.conditions.to_dict()
        )

        return self.conditions

    def get_conditions(self) -> Dict[str, Any]:
        """Get current alert conditions."""
        return self.conditions.to_dict()

    # =========================================================================
    # Lifecycle
    # =========================================================================

    async def start(self) -> None:
        """Start the monitoring loop in background."""
        if self._running:
            logger.warning("Monitor already running")
            return

        self._running = True
        self.last_prices = self.market.get_prices()
        self._record_snapshot("start")

        self._task = asyncio.create_task(self._monitor_loop())
        logger.info(
            "Market monitor started for agent %s: price_change=%.1f%%, interval=%.1fs",
            self.agent_id,
            self.conditions.price_change_pct * 100,
            self.conditions.poll_interval,
        )

    async def stop(self) -> None:
        """Stop the monitoring loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        logger.info("Market monitor stopped for agent %s", self.agent_id)

    async def _monitor_loop(self) -> None:
        """Main monitoring loop - runs in background."""
        while self._running:
            try:
                await asyncio.sleep(self.conditions.poll_interval)
                if self.conditions.enabled:
                    await self._check_prices()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Monitor loop error: %s", e)
                # Continue monitoring despite errors

    async def _check_prices(self) -> None:
        """Check current prices against configured conditions."""
        current_prices = self.market.get_prices()
        market_name = self.market.event.name

        for outcome, price in current_prices.items():
            last_price = self.last_prices.get(outcome)

            # Skip if no change tracking or disabled
            if last_price is None or last_price <= 0:
                self.last_prices[outcome] = price
                continue

            # Check outcomes filter
            if self.conditions.price_change_outcomes:
                if outcome not in self.conditions.price_change_outcomes:
                    continue

            # 1. Price change percentage alerts
            change = (price - last_price) / last_price
            abs_change = abs(change)

            if abs_change >= self.conditions.price_change_pct:
                alert = PriceAlert(
                    alert_type=AlertType.PRICE_CHANGE.value,
                    outcome=outcome,
                    message=f"{outcome} price {'UP' if change > 0 else 'DOWN'} {abs_change:.1%}: ${last_price:.4f} -> ${price:.4f}",
                    old_price=last_price,
                    new_price=price,
                    change_pct=abs_change,
                    direction="up" if change > 0 else "down",
                    market_id=market_name,
                    market_name=market_name,
                    priority="high" if abs_change >= 0.10 else "normal",
                )
                await self._emit_alert(alert)

            # 2. Price threshold alerts (price_above)
            if self.conditions.price_above and outcome in self.conditions.price_above:
                threshold = self.conditions.price_above[outcome]
                key = f"{outcome}_above_{threshold}"
                if price > threshold and key not in self._triggered_above:
                    self._triggered_above.add(key)
                    alert = PriceAlert(
                        alert_type=AlertType.PRICE_THRESHOLD.value,
                        outcome=outcome,
                        message=f"ALERT: {outcome} crossed ABOVE ${threshold:.4f} (now ${price:.4f})",
                        old_price=last_price,
                        new_price=price,
                        market_id=market_name,
                        market_name=market_name,
                        priority="urgent",
                    )
                    await self._emit_alert(alert)
                elif price <= threshold:
                    # Reset if price drops back below
                    self._triggered_above.discard(key)

            # 3. Price threshold alerts (price_below)
            if self.conditions.price_below and outcome in self.conditions.price_below:
                threshold = self.conditions.price_below[outcome]
                key = f"{outcome}_below_{threshold}"
                if price < threshold and key not in self._triggered_below:
                    self._triggered_below.add(key)
                    alert = PriceAlert(
                        alert_type=AlertType.PRICE_THRESHOLD.value,
                        outcome=outcome,
                        message=f"ALERT: {outcome} dropped BELOW ${threshold:.4f} (now ${price:.4f})",
                        old_price=last_price,
                        new_price=price,
                        market_id=market_name,
                        market_name=market_name,
                        priority="urgent",
                    )
                    await self._emit_alert(alert)
                elif price >= threshold:
                    # Reset if price rises back above
                    self._triggered_below.discard(key)

        # Update last prices and record snapshot
        self.last_prices = current_prices
        self._record_snapshot("poll")

    def on_trade(
        self,
        agent_id: str,
        outcome: str,
        direction: str,
        size: float,
        price: float,
    ) -> None:
        """
        Called when a trade occurs. Checks trade-based alert conditions.

        This should be called from the placeTrade tool after execution.
        """
        if not self.conditions.enabled:
            return

        # Skip own trades if configured
        if self.conditions.exclude_self and agent_id == self.agent_id:
            return

        # Check agent watchlist
        if self.conditions.watch_agents:
            if agent_id not in self.conditions.watch_agents:
                return

        market_name = self.market.event.name

        # Trade size threshold alert
        if self.conditions.trade_size_threshold and size >= self.conditions.trade_size_threshold:
            alert = PriceAlert(
                alert_type=AlertType.LARGE_TRADE.value,
                outcome=outcome,
                message=f"LARGE TRADE: Agent {agent_id} {direction.upper()} ${size:.2f} on {outcome}",
                new_price=price,
                trade_agent_id=agent_id,
                trade_size=size,
                trade_direction=direction,
                market_id=market_name,
                market_name=market_name,
                priority="high",
            )
            asyncio.create_task(self._emit_alert(alert))

        # Agent-specific trade size alert
        if self.conditions.agent_trade_size and size >= self.conditions.agent_trade_size:
            alert = PriceAlert(
                alert_type=AlertType.AGENT_TRADE.value,
                outcome=outcome,
                message=f"AGENT TRADE: {agent_id} {direction.upper()} ${size:.2f} on {outcome} @ ${price:.4f}",
                new_price=price,
                trade_agent_id=agent_id,
                trade_size=size,
                trade_direction=direction,
                market_id=market_name,
                market_name=market_name,
                priority="normal",
            )
            asyncio.create_task(self._emit_alert(alert))

    async def _emit_alert(self, alert: PriceAlert) -> None:
        """Emit alert to queue and subscribers."""
        if alert.change_pct is not None and alert.direction is not None:
            logger.warning(
                "PRICE ALERT: %s %s %.1f%% (%.4f -> %.4f)",
                alert.outcome,
                alert.direction.upper(),
                alert.change_pct * 100,
                alert.old_price or 0,
                alert.new_price or 0,
            )
        else:
            logger.warning(
                "ALERT [%s]: %s - %s",
                alert.alert_type,
                alert.outcome,
                alert.message,
            )

        # Add to main queue (drop oldest if full)
        try:
            self.alerts.put_nowait(alert)
        except asyncio.QueueFull:
            # Remove oldest and add new
            try:
                self.alerts.get_nowait()
                self.alerts.put_nowait(alert)
            except asyncio.QueueEmpty:
                pass

        # Notify subscribers
        for queue in self._subscribers:
            try:
                queue.put_nowait(alert)
            except asyncio.QueueFull:
                pass

        # Call callback if provided
        if self.on_alert:
            try:
                self.on_alert(alert)
            except Exception as e:
                logger.error("Alert callback error: %s", e)

        # Persist to database if session available
        if self.db_session:
            await self._persist_alert(alert)

    async def _persist_alert(self, alert: PriceAlert) -> None:
        """Persist alert to database."""
        try:
            from cliff.infrastructure.database import AlertLog
            alert_log = AlertLog(
                market_id=alert.market_id,
                outcome=alert.outcome,
                old_price=alert.old_price,
                new_price=alert.new_price,
                change_pct=alert.change_pct,
            )
            self.db_session.add(alert_log)
            await self.db_session.commit()
        except Exception as e:
            logger.error("Failed to persist alert: %s", e)

    def _record_snapshot(self, triggered_by: str) -> None:
        """Record price snapshot to history."""
        snapshot = PriceSnapshot(
            prices=dict(self.last_prices),
            triggered_by=triggered_by,
        )
        self.price_history.append(snapshot)

        # Keep history bounded
        if len(self.price_history) > 1000:
            self.price_history = self.price_history[-500:]

    # =========================================================================
    # Public API for Agents
    # =========================================================================

    async def check_alerts(self) -> List[PriceAlert]:
        """
        Check for pending price alerts (consumes alerts from queue).

        Returns:
            List of price alerts since last check
        """
        alerts = []
        while not self.alerts.empty():
            try:
                alert = self.alerts.get_nowait()
                alerts.append(alert)
            except asyncio.QueueEmpty:
                break
        return alerts

    async def peek_alerts(self) -> List[PriceAlert]:
        """
        Peek at alerts without consuming them.

        Note: Not perfectly accurate due to async nature.
        """
        alerts = []
        temp = []
        while not self.alerts.empty():
            try:
                alert = self.alerts.get_nowait()
                alerts.append(alert)
                temp.append(alert)
            except asyncio.QueueEmpty:
                break

        # Put them back
        for alert in temp:
            try:
                self.alerts.put_nowait(alert)
            except asyncio.QueueFull:
                break

        return alerts

    def get_latest_prices(self) -> Dict[str, float]:
        """
        Get latest known prices.

        This is fast (no market call) but may be slightly stale.
        """
        return dict(self.last_prices)

    def get_current_prices(self) -> Dict[str, float]:
        """
        Get current prices directly from market.

        Always fresh but requires market call.
        """
        return self.market.get_prices()

    def get_price_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent price snapshots."""
        snapshots = self.price_history[-limit:]
        return [
            {
                "prices": snapshot.prices,
                "timestamp": snapshot.timestamp.isoformat(),
                "triggered_by": snapshot.triggered_by,
            }
            for snapshot in snapshots
        ]

    def subscribe(self) -> asyncio.Queue:
        """
        Subscribe to alerts (for real-time notification).

        Returns queue that will receive alerts.
        """
        queue: asyncio.Queue = asyncio.Queue(maxsize=50)
        self._subscribers.append(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        """Unsubscribe from alerts."""
        if queue in self._subscribers:
            self._subscribers.remove(queue)

    # =========================================================================
    # Trade Integration
    # =========================================================================

    def record_trade_prices(self, trade_id: str) -> None:
        """Record a price snapshot after a trade."""
        self.last_prices = self.market.get_prices()
        self._record_snapshot(f"trade:{trade_id}")

    def record_trade(
        self,
        agent_id: str,
        outcome: str,
        direction: str,
        size_usd: float,
        price: float,
    ) -> None:
        """
        Record trade info for attribution in alerts.

        Called when a trade is executed, before checking alerts.
        """
        self._last_trade = {
            "agent_id": agent_id,
            "outcome": outcome,
            "direction": direction,
            "size_usd": size_usd,
            "price": price,
            "timestamp": datetime.now(timezone.utc),
        }

    # =========================================================================
    # Agent-Specific Alert System (Interrupt-Based)
    # =========================================================================

    def register_agent_alert(
        self,
        agent_id: str,
        outcome: str,
        conditions: Dict[str, Any],
        rationale: str,
    ) -> AgentAlertConfig:
        """
        Register a new alert configuration for an agent.

        One-shot behavior: alert triggers once then auto-deactivates.

        Args:
            agent_id: The agent registering the alert
            outcome: Which outcome to monitor
            conditions: Dict with any of:
                - price_above: float - Alert if price rises above this
                - price_below: float - Alert if price drops below this
                - change_pct: float - Alert on X% move from current price
                - large_trade_usd: float - Alert on trades > this USD amount
                - any_trade: bool - Alert on any trade
            rationale: Why the agent is setting this alert

        Returns:
            The created AgentAlertConfig
        """
        # Get current price as baseline for change_pct
        current_prices = self.market.get_prices()
        baseline_price = current_prices.get(outcome, 0.5)

        config = AgentAlertConfig(
            agent_id=agent_id,
            outcome=outcome,
            conditions=conditions,
            rationale=rationale,
            baseline_price=baseline_price,
        )

        if agent_id not in self._agent_alerts:
            self._agent_alerts[agent_id] = []

        # Remove any existing alert for same outcome (replace)
        self._agent_alerts[agent_id] = [
            a for a in self._agent_alerts[agent_id]
            if a.outcome != outcome or a.status != "active"
        ]

        self._agent_alerts[agent_id].append(config)

        logger.info(
            "[ALERT] Agent %s registered alert for %s: %s (rationale: %s)",
            agent_id, outcome, conditions, rationale[:50]
        )

        return config

    def get_active_alerts_for_agent(self, agent_id: str) -> List[AgentAlertConfig]:
        """Get all active alert configs for an agent."""
        if agent_id not in self._agent_alerts:
            return []
        return [a for a in self._agent_alerts[agent_id] if a.status == "active"]

    def cancel_agent_alert(self, agent_id: str, outcome: str) -> bool:
        """
        Cancel an active alert for an agent.

        Args:
            agent_id: The agent
            outcome: Which outcome's alert to cancel

        Returns:
            True if alert was found and cancelled
        """
        if agent_id not in self._agent_alerts:
            return False

        for alert in self._agent_alerts[agent_id]:
            if alert.outcome == outcome and alert.status == "active":
                alert.status = "cancelled"
                logger.info("[ALERT] Agent %s cancelled alert for %s", agent_id, outcome)
                return True

        return False

    def check_agent_alerts(
        self,
        agent_states: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Check all active agent alerts and trigger any that match conditions.

        Should be called after each trade or periodically.

        Args:
            agent_states: Dict of agent_id -> TradingAgentState for position/order info
        """
        current_prices = self.market.get_prices()
        now = datetime.now(timezone.utc)

        for agent_id, alerts in self._agent_alerts.items():
            for alert in alerts:
                if alert.status != "active":
                    continue

                outcome = alert.outcome
                conditions = alert.conditions
                current_price = current_prices.get(outcome, 0)
                baseline_price = alert.baseline_price or 0

                triggered = False
                condition_met = None

                # Check price_above
                if "price_above" in conditions:
                    threshold = conditions["price_above"]
                    if current_price > threshold:
                        triggered = True
                        condition_met = f"price rose above ${threshold:.4f}"

                # Check price_below
                if not triggered and "price_below" in conditions:
                    threshold = conditions["price_below"]
                    if current_price < threshold:
                        triggered = True
                        condition_met = f"price dropped below ${threshold:.4f}"

                # Check change_pct
                if not triggered and "change_pct" in conditions and baseline_price > 0:
                    threshold = conditions["change_pct"]
                    change = abs(current_price - baseline_price) / baseline_price
                    if change >= threshold:
                        triggered = True
                        direction = "up" if current_price > baseline_price else "down"
                        condition_met = f"price moved {direction} {change:.1%} from ${baseline_price:.4f}"

                # Check large_trade_usd (requires last trade info)
                if not triggered and "large_trade_usd" in conditions and self._last_trade:
                    threshold = conditions["large_trade_usd"]
                    if (self._last_trade["outcome"] == outcome and
                        self._last_trade["size_usd"] >= threshold and
                        self._last_trade["agent_id"] != agent_id):
                        triggered = True
                        condition_met = f"large trade: ${self._last_trade['size_usd']:.0f} by {self._last_trade['agent_id']}"

                # Check any_trade
                if not triggered and conditions.get("any_trade") and self._last_trade:
                    if (self._last_trade["outcome"] == outcome and
                        self._last_trade["agent_id"] != agent_id):
                        triggered = True
                        condition_met = f"trade by {self._last_trade['agent_id']}"

                if triggered:
                    # Build rich alert with context
                    rich_alert = self._build_rich_alert(
                        alert_config=alert,
                        current_price=current_price,
                        condition_met=condition_met,
                        agent_states=agent_states,
                    )

                    # Mark as triggered
                    alert.status = "triggered"
                    alert.triggered_at = now

                    # Queue for injection
                    if agent_id not in self._triggered_alerts:
                        self._triggered_alerts[agent_id] = []
                    self._triggered_alerts[agent_id].append(rich_alert)

                    logger.warning(
                        "[ALERT TRIGGERED] Agent %s: %s - %s",
                        agent_id, outcome, condition_met
                    )

    def _build_rich_alert(
        self,
        alert_config: AgentAlertConfig,
        current_price: float,
        condition_met: str,
        agent_states: Optional[Dict[str, Any]] = None,
    ) -> RichPriceAlert:
        """Build a RichPriceAlert with full context."""
        outcome = alert_config.outcome
        old_price = alert_config.baseline_price or 0
        change = (current_price - old_price) / old_price if old_price > 0 else 0
        direction = "up" if current_price > old_price else "down"

        # Determine priority based on magnitude
        abs_change = abs(change)
        if abs_change >= 0.15:
            priority = "urgent"
        elif abs_change >= 0.08:
            priority = "high"
        else:
            priority = "normal"

        # Get trade attribution
        triggering_agent = None
        triggering_trade_usd = None
        triggering_trade_direction = None
        if self._last_trade and self._last_trade["outcome"] == outcome:
            triggering_agent = self._last_trade["agent_id"]
            triggering_trade_usd = self._last_trade["size_usd"]
            triggering_trade_direction = self._last_trade["direction"]

        # Get position and limit order info if available
        limit_orders_at_risk = []
        position_tokens = None
        avg_entry_price = None
        unrealized_pnl_before = None
        unrealized_pnl_after = None
        pnl_change = None

        if agent_states and alert_config.agent_id in agent_states:
            state = agent_states[alert_config.agent_id]

            # Get position
            if hasattr(state, 'portfolio') and outcome in state.portfolio:
                position_tokens = state.portfolio[outcome]
                if hasattr(state, 'cost_basis') and outcome in state.cost_basis:
                    cost = state.cost_basis[outcome]
                    if position_tokens > 0:
                        avg_entry_price = cost / position_tokens
                        unrealized_pnl_before = position_tokens * old_price - cost
                        unrealized_pnl_after = position_tokens * current_price - cost
                        pnl_change = unrealized_pnl_after - unrealized_pnl_before

            # Get limit orders at risk
            if hasattr(state, 'pending_limit_orders'):
                for order in state.pending_limit_orders:
                    if order.outcome == outcome and order.status == "pending":
                        distance = abs(current_price - order.trigger_price)
                        distance_pct = distance / current_price if current_price > 0 else 0
                        if distance_pct < 0.15:  # Within 15%
                            limit_orders_at_risk.append({
                                "order_id": order.order_id[:8],
                                "order_type": order.order_type,
                                "trigger_price": order.trigger_price,
                                "distance_pct": round(distance_pct, 4),
                                "size": order.size,
                            })

        message = f"{outcome} price {'UP' if direction == 'up' else 'DOWN'} {abs(change):.1%}: ${old_price:.4f} → ${current_price:.4f}"

        return RichPriceAlert(
            alert_type=AlertType.PRICE_CHANGE.value,
            outcome=outcome,
            message=message,
            old_price=old_price,
            new_price=current_price,
            change_pct=abs(change),
            direction=direction,
            triggering_agent=triggering_agent,
            triggering_trade_usd=triggering_trade_usd,
            triggering_trade_direction=triggering_trade_direction,
            limit_orders_at_risk=limit_orders_at_risk,
            position_tokens=position_tokens,
            avg_entry_price=avg_entry_price,
            unrealized_pnl_before=unrealized_pnl_before,
            unrealized_pnl_after=unrealized_pnl_after,
            pnl_change=pnl_change,
            alert_rationale=alert_config.rationale,
            condition_met=condition_met,
            market_name=self.market.event.name if hasattr(self.market, 'event') else None,
            priority=priority,
        )

    def get_triggered_alerts(self, agent_id: str) -> List[RichPriceAlert]:
        """
        Get triggered alerts for an agent (for injection into prompt).

        Does NOT consume them - use mark_alerts_delivered after injection.
        """
        return self._triggered_alerts.get(agent_id, [])

    def mark_alerts_delivered(self, agent_id: str) -> None:
        """
        Mark triggered alerts as delivered (after injection).

        This clears the triggered alerts queue for this agent.
        """
        if agent_id in self._triggered_alerts:
            # Move to delivered status in the config
            for alert in self._agent_alerts.get(agent_id, []):
                if alert.status == "triggered":
                    alert.status = "delivered"

            # Clear the triggered queue
            self._triggered_alerts[agent_id] = []
            logger.info("[ALERT] Marked alerts delivered for agent %s", agent_id)


def build_rich_alert_section(alerts: List[RichPriceAlert], agent_id: str) -> str:
    """
    Build a formatted alert section to inject into agent prompt.

    Returns a string ready to prepend to the agent's turn prompt.
    """
    if not alerts:
        return ""

    sections = []

    for alert in alerts:
        priority_prefix = f"[{alert.priority.upper()}]" if alert.priority != "normal" else ""

        lines = [
            f"=== ALERT: YOUR CONFIGURED CONDITION TRIGGERED ===",
            f"",
            f"{priority_prefix} \"{alert.outcome}\" {alert.message}",
            f"",
        ]

        # Why you set this alert
        if alert.alert_rationale:
            lines.extend([
                f"WHY YOU SET THIS ALERT:",
                f"\"{alert.alert_rationale}\"",
                f"",
            ])

        # What caused it
        if alert.triggering_agent:
            lines.append("WHAT CAUSED IT:")
            trade_dir = alert.triggering_trade_direction.upper() if alert.triggering_trade_direction else "traded"
            lines.append(f"- Agent \"{alert.triggering_agent}\" {trade_dir} ${alert.triggering_trade_usd:.0f}" if alert.triggering_trade_usd else f"- Trade by \"{alert.triggering_agent}\"")
            lines.append("")

        # Position impact
        if alert.position_tokens and alert.position_tokens > 0:
            lines.append("YOUR POSITION IMPACT:")
            entry_str = f" (avg entry: ${alert.avg_entry_price:.4f})" if alert.avg_entry_price else ""
            lines.append(f"- You hold {alert.position_tokens:.2f} tokens{entry_str}")
            if alert.unrealized_pnl_before is not None and alert.unrealized_pnl_after is not None:
                pnl_dir = "UP" if alert.pnl_change and alert.pnl_change > 0 else "DOWN"
                lines.append(f"- Unrealized P&L: ${alert.unrealized_pnl_before:.2f} → ${alert.unrealized_pnl_after:.2f} ({pnl_dir} ${abs(alert.pnl_change or 0):.2f})")
            lines.append("")

        # Limit orders at risk
        if alert.limit_orders_at_risk:
            lines.append("LIMIT ORDER STATUS:")
            for order in alert.limit_orders_at_risk:
                lines.append(f"- {order['order_type']} at ${order['trigger_price']:.4f} is now {order['distance_pct']*100:.1f}% away")
            lines.append("")

        # Condition met
        if alert.condition_met:
            lines.append(f"CONDITION MET: {alert.condition_met}")
            lines.append("")

        lines.append("=" * 52)

        sections.append("\n".join(lines))

    return "\n\n".join(sections) + "\n\n"


class MultiMarketMonitor:
    """
    Monitor multiple markets simultaneously.

    Useful when agents trade on multiple markets in parallel.
    """

    def __init__(self, alert_threshold: float = 0.05, poll_interval: float = 5.0):
        self.alert_threshold = alert_threshold
        self.poll_interval = poll_interval
        self.monitors: Dict[str, MarketMonitor] = {}
        self.combined_alerts: asyncio.Queue[PriceAlert] = asyncio.Queue(maxsize=200)

    def add_market(self, market_id: str, market: "EventMarket") -> MarketMonitor:
        """Add a market to monitor."""
        monitor = MarketMonitor(
            market=market,
            agent_id=market_id,
            on_alert=lambda a: self._on_alert(market_id, a),
        )
        # Configure with the multi-monitor's defaults
        monitor.configure(
            price_change_pct=self.alert_threshold,
            poll_interval=self.poll_interval,
        )
        self.monitors[market_id] = monitor
        return monitor

    def _on_alert(self, market_id: str, alert: PriceAlert) -> None:
        """Forward alert to combined queue."""
        alert.market_id = market_id
        try:
            self.combined_alerts.put_nowait(alert)
        except asyncio.QueueFull:
            pass

    async def start_all(self) -> None:
        """Start all monitors."""
        for monitor in self.monitors.values():
            await monitor.start()

    async def stop_all(self) -> None:
        """Stop all monitors."""
        for monitor in self.monitors.values():
            await monitor.stop()

    async def check_all_alerts(self) -> List[PriceAlert]:
        """Check alerts from all markets."""
        alerts = []
        while not self.combined_alerts.empty():
            try:
                alerts.append(self.combined_alerts.get_nowait())
            except asyncio.QueueEmpty:
                break
        return alerts

    def get_all_prices(self) -> Dict[str, Dict[str, float]]:
        """Get prices from all markets."""
        return {
            market_id: monitor.get_latest_prices()
            for market_id, monitor in self.monitors.items()
        }
