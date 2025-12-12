"""
Multi-market orchestrator for concurrent prediction market trading.

Coordinates multiple SimulationController instances, each trading on a
separate market with duplicated agent personas.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

from cliff.core.events import EventMarket, Event, Outcome
from cliff.core.market import Market
from cliff.streaming.bridge import MultiBridge, StdioBridge
from cliff.streaming.handler import StreamHandler
from .controller import AgentConfig, SimulationController

logger = logging.getLogger(__name__)


@dataclass
class MarketContext:
    """Container for a single market's simulation state."""

    market_id: str
    event_market: EventMarket
    controller: SimulationController
    bridge: StdioBridge
    stream_handler: StreamHandler
    task: Optional[asyncio.Task] = None
    status: str = "pending"  # pending, running, paused, completed


@dataclass
class OrchestratorConfig:
    """Configuration for the multi-market orchestrator."""

    # Agent personas to duplicate for each market
    agent_configs: List[AgentConfig] = field(default_factory=list)

    # Model settings
    openai_model: str = "gpt-5-mini"
    parallel_agents: bool = False
    verbose: int = 1

    # Market monitoring
    enable_market_monitor: bool = True
    price_alert_threshold: float = 0.05

    # Database persistence
    enable_db_persistence: bool = False
    project_id: Optional[str] = None


class MultiMarketOrchestrator:
    """
    Orchestrates multiple concurrent prediction market simulations.

    Key responsibilities:
    - Create and manage multiple markets
    - Duplicate agent personas for each market
    - Route IPC messages to correct market context
    - Handle user actions (create market, inject news, etc.)
    - Coordinate lifecycle across all markets
    """

    def __init__(
        self,
        config: OrchestratorConfig,
        multi_bridge: Optional[MultiBridge] = None,
    ):
        """
        Initialize the orchestrator.

        Args:
            config: Orchestrator configuration
            multi_bridge: Shared bridge for Ink UI communication
        """
        self.config = config
        self._multi_bridge = multi_bridge or MultiBridge()
        self._markets: Dict[str, MarketContext] = {}
        self._running = False
        self._lock = asyncio.Lock()

        # Register handlers for UI requests
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register JSON-RPC handlers for all bridges."""
        # These will be registered when bridges are created
        pass

    def _setup_bridge_handlers(self, bridge: StdioBridge, market_id: str) -> None:
        """Set up handlers for a specific market's bridge."""
        bridge.register_handler("inject_news", self._handle_inject_news)
        bridge.register_handler("pause_market", self._handle_pause_market)
        bridge.register_handler("resume_market", self._handle_resume_market)
        bridge.register_handler("close_market", self._handle_close_market)
        bridge.register_handler("get_portfolio", self._handle_get_portfolio)

    async def create_market(
        self,
        name: str,
        description: str,
        outcomes: List[str],
        market_id: Optional[str] = None,
    ) -> str:
        """
        Create a new market with duplicated agent personas.

        Args:
            name: Market/event name
            description: Full description
            outcomes: List of outcome names
            market_id: Optional ID (generated if not provided)

        Returns:
            The market ID
        """
        async with self._lock:
            market_id = market_id or str(uuid4())[:8]

            logger.info("Creating market: %s (%s)", name, market_id)

            # Create the event and market
            event = Event(
                id=market_id,
                name=name,
                description=description,
                outcomes=[Outcome(name=o) for o in outcomes],
            )
            event_market = EventMarket(event=event)

            # Create a basic AMM market for legacy compatibility
            amm_market = Market()

            # Create bridge for this market
            bridge = self._multi_bridge.get_or_create(market_id)
            self._setup_bridge_handlers(bridge, market_id)

            # Create stream handler that routes to this bridge
            stream_handler = StreamHandler.with_bridge(
                bridge, verbosity=self.config.verbose
            )

            # Create controller with duplicated agents
            controller = SimulationController(
                market=amm_market,
                agent_configs=self.config.agent_configs,
                event_market=event_market,
                use_openai_sdk=True,
                openai_model=self.config.openai_model,
                parallel_agents=self.config.parallel_agents,
                verbose=self.config.verbose,
                enable_market_monitor=self.config.enable_market_monitor,
                price_alert_threshold=self.config.price_alert_threshold,
                enable_db_persistence=self.config.enable_db_persistence,
                project_id=self.config.project_id,
                db_market_id=market_id,
                stream_handler=stream_handler,
            )

            # Store context
            context = MarketContext(
                market_id=market_id,
                event_market=event_market,
                controller=controller,
                bridge=bridge,
                stream_handler=stream_handler,
                status="pending",
            )
            self._markets[market_id] = context

            # Emit market created event
            stream_handler.emit_market_created(
                market_id=market_id,
                name=name,
                outcomes=outcomes,
                prices=event_market.get_prices(),
            )

            logger.info(
                "Market %s created with %d agents",
                market_id,
                len(self.config.agent_configs),
            )

            return market_id

    async def start_market(self, market_id: str) -> None:
        """Start trading simulation for a market."""
        async with self._lock:
            if market_id not in self._markets:
                raise ValueError(f"Market not found: {market_id}")

            context = self._markets[market_id]
            if context.status == "running":
                logger.warning("Market %s already running", market_id)
                return

            context.status = "running"
            context.bridge.emit_ready()

            # Start controller in background task
            context.task = asyncio.create_task(
                self._run_market(context)
            )

            logger.info("Started market: %s", market_id)

    async def _run_market(self, context: MarketContext) -> None:
        """Run the simulation for a single market."""
        try:
            await context.controller.run()
            context.status = "completed"
            logger.info("Market %s completed", context.market_id)
        except asyncio.CancelledError:
            context.status = "paused"
            logger.info("Market %s paused", context.market_id)
        except Exception as e:
            context.status = "error"
            logger.error("Market %s error: %s", context.market_id, e)

    async def stop_market(self, market_id: str) -> None:
        """Stop and remove a market."""
        async with self._lock:
            if market_id not in self._markets:
                return

            context = self._markets[market_id]

            # Cancel running task
            if context.task and not context.task.done():
                context.task.cancel()
                try:
                    await context.task
                except asyncio.CancelledError:
                    pass

            # Clean up bridge
            self._multi_bridge.remove(market_id)

            # Remove context
            del self._markets[market_id]

            logger.info("Stopped market: %s", market_id)

    async def inject_news(self, market_id: str, scenario: str) -> None:
        """
        Inject a hypothetical scenario into a market.

        This emits a news event that agents will react to.

        Args:
            market_id: Target market
            scenario: The hypothetical text (e.g., "Satoshi becomes active on wallet")
        """
        if market_id not in self._markets:
            raise ValueError(f"Market not found: {market_id}")

        context = self._markets[market_id]

        # Emit news event through stream handler
        context.stream_handler.emit_news_event(scenario, source="user")

        # Signal to controller that new information is available
        if hasattr(context.controller, "_new_info_event"):
            context.controller._new_info_event.set()

        logger.info("Injected news into %s: %s", market_id, scenario[:50])

    async def run(self) -> None:
        """
        Main orchestrator loop.

        Waits for all markets to complete or for shutdown signal.
        """
        self._running = True

        logger.info("Orchestrator started with %d agent configs", len(self.config.agent_configs))

        try:
            while self._running:
                # Check for completed markets
                async with self._lock:
                    completed = [
                        mid for mid, ctx in self._markets.items()
                        if ctx.status in ("completed", "error")
                    ]

                # If all markets done and no new ones expected, exit
                if not self._markets:
                    await asyncio.sleep(0.5)
                    continue

                # Wait a bit before next check
                await asyncio.sleep(1.0)

        except asyncio.CancelledError:
            logger.info("Orchestrator cancelled")
        finally:
            await self.shutdown()

    async def shutdown(self) -> None:
        """Gracefully shutdown all markets."""
        self._running = False

        async with self._lock:
            market_ids = list(self._markets.keys())

        for market_id in market_ids:
            await self.stop_market(market_id)

        self._multi_bridge.shutdown_all()
        logger.info("Orchestrator shutdown complete")

    # JSON-RPC handlers for Ink UI

    async def _handle_inject_news(self, market_id: str, scenario: str) -> dict:
        """Handle inject_news request from UI."""
        await self.inject_news(market_id, scenario)
        return {"success": True}

    async def _handle_pause_market(self, market_id: str) -> dict:
        """Handle pause_market request from UI."""
        if market_id not in self._markets:
            return {"success": False, "error": "Market not found"}

        context = self._markets[market_id]
        if context.task and not context.task.done():
            context.task.cancel()

        return {"success": True}

    async def _handle_resume_market(self, market_id: str) -> dict:
        """Handle resume_market request from UI."""
        await self.start_market(market_id)
        return {"success": True}

    async def _handle_close_market(self, market_id: str) -> dict:
        """Handle close_market request from UI."""
        await self.stop_market(market_id)
        return {"success": True}

    async def _handle_get_portfolio(self, market_id: str, agent_id: str) -> dict:
        """Handle get_portfolio request from UI."""
        if market_id not in self._markets:
            return {"error": "Market not found"}

        context = self._markets[market_id]
        states = context.controller._agent_states

        if agent_id not in states:
            return {"error": "Agent not found"}

        state = states[agent_id]
        return {
            "cash": state.cash_balance,
            "portfolio": dict(state.portfolio),
            "realized_pnl": state.realized_pnl,
        }

    # Properties

    @property
    def market_ids(self) -> List[str]:
        """Get all active market IDs."""
        return list(self._markets.keys())

    def get_market_status(self, market_id: str) -> Optional[str]:
        """Get status of a specific market."""
        ctx = self._markets.get(market_id)
        return ctx.status if ctx else None

    def get_market_prices(self, market_id: str) -> Optional[Dict[str, float]]:
        """Get current prices for a market."""
        ctx = self._markets.get(market_id)
        if ctx:
            return ctx.event_market.get_prices()
        return None
