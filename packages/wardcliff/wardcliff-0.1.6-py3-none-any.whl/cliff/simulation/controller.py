from __future__ import annotations

import asyncio
import logging
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

# Conditionally import OpenAI (only needed for legacy mode)
try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

from cliff.agents.async_agent import AgentPersona, AsyncTradingAgent, SubAgentConfig
from cliff.core.market import Market, TradeExecution
from cliff.core.metrics import MetricsRecorder
from cliff.core.events import EventMarket, TradeResult as EventTradeResult

# Simulation logger for comprehensive output
try:
    from cliff.streaming.logger import SimulationLogger, set_simulation_logger
    SIMULATION_LOGGER_AVAILABLE = True
except ImportError:
    SIMULATION_LOGGER_AVAILABLE = False
    SimulationLogger = None
    set_simulation_logger = None

# Stream handler for real-time display
try:
    from cliff.streaming.handler import StreamHandler
    STREAM_HANDLER_AVAILABLE = True
except ImportError:
    STREAM_HANDLER_AVAILABLE = False
    StreamHandler = None

# Optional external integrations
try:
    from data_sources import WebDatasetManager
except ImportError:
    # Stub class when data_sources is not installed
    class WebDatasetManager:
        """Stub WebDatasetManager for when data_sources is not installed."""
        def __init__(self):
            self.version = 0
        def add_urls(self, urls):
            pass

try:
    from parallel_client import (
        ParallelClientError,
        ParallelExtractClient,
        ParallelMonitorClient,
    )
except ImportError:
    ParallelClientError = Exception
    ParallelExtractClient = None
    ParallelMonitorClient = None

# Conditionally import Turbopuffer (only needed for legacy mode)
try:
    from turbopuffer_client import TurbopufferClient, TurbopufferError
except ImportError:
    TurbopufferClient = None
    TurbopufferError = Exception

# OpenAI Agents SDK imports (optional - only needed for OpenAI SDK mode)
try:
    from cliff.agents.openai_agent import (
        TradingAgentState,
        TradingContext,
        create_trading_agent,
        build_trading_system_prompt,
        run_trading_agent,
    )
    from agents import Runner
    from agents.run import RunConfig
    from agents.model_settings import ModelSettings, Reasoning
    from agents.stream_events import RunItemStreamEvent, RawResponsesStreamEvent
    from agents.items import (
        ReasoningItem,
        MessageOutputItem,
        ToolCallItem,
        ToolCallOutputItem,
        HandoffCallItem,
        HandoffOutputItem,
    )
    OPENAI_SDK_AVAILABLE = True
except ImportError:
    OPENAI_SDK_AVAILABLE = False

# Market monitor (optional - for price alerts)
try:
    from cliff.core.monitor import MarketMonitor, PriceAlert, build_rich_alert_section
    MARKET_MONITOR_AVAILABLE = True
except ImportError:
    MARKET_MONITOR_AVAILABLE = False
    build_rich_alert_section = None

# Database (optional - for persistence)
try:
    from database import DatabaseManager, get_session, TradeRepository
    from document_manager import DocumentManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    persona: AgentPersona
    prompt: str
    sub_agent_config: Optional[SubAgentConfig] = None


@dataclass
class AgentRuntime:
    config: AgentConfig
    agent: AsyncTradingAgent
    task: Optional[asyncio.Task] = None


@dataclass
class OpenAIAgentRuntime:
    """Runtime for OpenAI Agents SDK-based agents."""
    agent_id: str
    state: Any  # TradingAgentState
    task: Optional[asyncio.Task] = None
    last_action: Optional[str] = None  # Track for consensus detection
    market_monitor: Any = None  # MarketMonitor instance


class SimulationController:
    """
    Coordinates multiple trading agents interacting with a shared market.

    Supports both:
    - Legacy AsyncTradingAgent (OpenAI-based)
    - OpenAI Agents SDK agents (native function_tool)

    For event markets, implements consensus-based termination (all agents hold).
    """

    def __init__(
        self,
        *,
        market: Market,
        agent_configs: List[AgentConfig],
        openai_client: Optional[AsyncOpenAI] = None,
        parallel_extract: Optional[ParallelExtractClient] = None,
        parallel_monitor: Optional[ParallelMonitorClient] = None,
        dataset: Optional[WebDatasetManager] = None,
        metrics: Optional[MetricsRecorder] = None,
        turbopuffer_client: Optional[TurbopufferClient] = None,
        event_market: Optional[EventMarket] = None,
        use_openai_sdk: bool = True,  # OpenAI Agents SDK is now the default
        openai_model: str = "gpt-5-mini",
        # New: Market monitor and DB options
        enable_market_monitor: bool = True,
        price_alert_threshold: float = 0.05,
        enable_db_persistence: bool = False,
        project_id: Optional[Union[str, UUID]] = None,
        db_market_id: Optional[Union[str, UUID]] = None,
        llm_model: str = "gpt-5-mini",
        parallel_agents: bool = False,  # Run agents in parallel (faster, no inter-agent reactions)
        verbose: int = 0,  # 0=minimal, 1=normal, 2=verbose (show reasoning), 3=debug
        # Comprehensive simulation logging
        enable_simulation_log: bool = True,
        log_file: Optional[str] = None,
        log_dir: str = "logs",
        # Real-time streaming display
        stream_handler: Optional[Any] = None,  # StreamHandler for live display updates
    ) -> None:
        self.market = market
        self.parallel_agents = parallel_agents
        self.verbose = verbose
        self.event_market = event_market
        self._market_lock = asyncio.Lock()
        self._broadcast_lock = asyncio.Lock()

        self._trade_history: List[TradeExecution] = []
        self._event_trade_history: List[EventTradeResult] = []

        # Simulation logger for comprehensive output
        self._sim_logger: Optional[SimulationLogger] = None
        self._log_file = log_file
        self._log_dir = log_dir
        self._enable_simulation_log = enable_simulation_log and SIMULATION_LOGGER_AVAILABLE
        self._simulation_start_time: Optional[float] = None

        # Stream handler for real-time display
        self._stream_handler = stream_handler
        self._openai_client = openai_client
        self.metrics = metrics or MetricsRecorder()
        self.dataset = dataset or WebDatasetManager()
        self.agent_configs = agent_configs
        self._runtimes: List[AgentRuntime] = []
        self._last_dataset_version = self.dataset.version
        self.doc_update_file = Path(
            os.getenv("TURBOPUFFER_UPDATE_FILE", "turbopuffer_updates.json")
        )

        if parallel_extract is not None:
            self.parallel_extract = parallel_extract
        else:
            try:
                self.parallel_extract = ParallelExtractClient.from_env()
            except ParallelClientError:
                self.parallel_extract = None

        # ParallelMonitorClient - ONLY used for background monitoring of market-relevant news
        # This is the ONLY Parallel API usage. OpenAI agents use native WebSearch for research.
        # The monitor polls for new information and triggers agent restarts when news is detected.
        if parallel_monitor is not None:
            self.parallel_monitor = parallel_monitor
        else:
            try:
                self.parallel_monitor = ParallelMonitorClient.from_env()
            except ParallelClientError:
                self.parallel_monitor = None

        if turbopuffer_client is not None:
            self.turbopuffer = turbopuffer_client
        else:
            try:
                self.turbopuffer = TurbopufferClient.from_env()
            except TurbopufferError:
                self.turbopuffer = None

        self._trade_lock = asyncio.Lock()

        # OpenAI Agents SDK mode
        self.use_openai_sdk = use_openai_sdk
        self.openai_model = openai_model
        self._openai_runtimes: List[OpenAIAgentRuntime] = []

        # Persistent agent states (portfolios survive across iterations)
        self._agent_states: Dict[str, TradingAgentState] = {}

        # LLM model for legacy OpenAI-based agents
        self.llm_model = llm_model

        if use_openai_sdk and not OPENAI_SDK_AVAILABLE:
            raise ImportError(
                "OpenAI Agents SDK requested but not available. "
                "Install with: pip install openai-agents"
            )

        # Market monitor for price alerts
        self.enable_market_monitor = enable_market_monitor
        self.price_alert_threshold = price_alert_threshold
        self._market_monitor: Optional[Any] = None

        if enable_market_monitor and event_market and MARKET_MONITOR_AVAILABLE:
            self._market_monitor = MarketMonitor(
                market=event_market,
                agent_id="controller",
                on_alert=self._on_price_alert,
            )
            # Configure alert conditions (now done via configure() method)
            self._market_monitor.configure(
                price_change_pct=price_alert_threshold,
                poll_interval=5.0,
            )
            logger.info(
                "Market monitor enabled: threshold=%.1f%%",
                price_alert_threshold * 100
            )

        # Database persistence
        self.enable_db_persistence = enable_db_persistence
        self.project_id = str(project_id) if project_id else None
        self.db_market_id = str(db_market_id) if db_market_id else None
        self._db_manager: Optional[Any] = None
        self._doc_manager: Optional[Any] = None

        if enable_db_persistence and DATABASE_AVAILABLE:
            logger.info("Database persistence enabled (will initialize on run)")

    def _on_price_alert(self, alert: "PriceAlert") -> None:
        """Callback when market monitor detects significant price change or trade."""
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

    async def _check_all_limit_orders(self) -> None:
        """Check and execute limit orders for ALL agents.

        This is called after each agent completes trading in sequential mode,
        allowing one agent's trade to trigger another agent's take-profit or stop-loss.
        """
        if not self._agent_states:
            return

        total_executed = 0
        for agent_id, state in self._agent_states.items():
            # Check if the state has the limit order check function
            if hasattr(state, '_check_limit_orders') and callable(state._check_limit_orders):
                try:
                    executed = await state._check_limit_orders()
                    if executed:
                        total_executed += len(executed)
                        for order in executed:
                            logger.info(
                                "[LIMIT] %s's %s order triggered: %s %s @ %.4f",
                                agent_id, order['order_type'], order['action'].upper(),
                                order['outcome'], order['fill_price']
                            )
                            # Sync to trade history
                            for trade in state.event_trade_log:
                                if trade not in self._event_trade_history:
                                    self._event_trade_history.append(trade)
                except Exception as e:
                    logger.error("[LIMIT] Error checking orders for %s: %s", agent_id, str(e))

        if total_executed > 0:
            logger.info("[LIMIT] Executed %d limit order(s) across all agents", total_executed)
            # Emit price update after limit orders execute (for real-time chart updates)
            if self._stream_handler and self.event_market:
                self._stream_handler.emit_price_update(self.event_market.get_prices())

        # Check agent-specific alerts (interrupt-based system)
        # This will trigger any alerts whose conditions have been met
        if self._market_monitor:
            try:
                self._market_monitor.check_agent_alerts(agent_states=self._agent_states)
            except Exception as e:
                logger.error("[ALERT] Error checking agent alerts: %s", str(e))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    async def run(self) -> None:
        """
        Run all agents concurrently until they complete their individual plans.

        For event markets:
        - Continues until ALL agents decide to hold (consensus)
        - Restarts when Parallel monitor detects new information
        - Background monitor polling runs continuously

        Supports both legacy AsyncTradingAgent and OpenAI Agents SDK agents.
        """
        self._running = True
        self._new_info_event = asyncio.Event()
        self._simulation_start_time = time.time()

        # Initialize simulation logger for comprehensive output
        if self._enable_simulation_log:
            self._sim_logger = SimulationLogger(
                log_file=self._log_file,
                log_dir=self._log_dir,
                console_output=False,  # Don't duplicate to console
                include_timestamps=True,
                include_step_numbers=True,
            )
            agent_names = [cfg.persona.name for cfg in self.agent_configs]
            event_name = self.event_market.event.name if self.event_market else "Simulation"
            prompt = self.event_market.event.description if self.event_market else "Trading simulation"
            initial_prices = self.event_market.get_prices() if self.event_market else {}

            log_path = self._sim_logger.start_session(
                prompt=prompt,
                agents=agent_names,
                event_name=event_name,
                initial_prices=initial_prices,
                metadata={
                    "model": self.openai_model,
                    "mode": "OpenAI Agents SDK" if self.use_openai_sdk else "Legacy",
                    "parallel": self.parallel_agents,
                },
            )
            set_simulation_logger(self._sim_logger)
            logger.info("Simulation log: %s", log_path)

        # Initialize database if persistence enabled
        if self.enable_db_persistence and DATABASE_AVAILABLE:
            self._db_manager = DatabaseManager()
            await self._db_manager.initialize()
            logger.info("Database initialized for persistence")

        # Start market monitor if enabled
        if self._market_monitor:
            await self._market_monitor.start()
            logger.info("Market monitor started")

        # Sync monitor prompt to event if both are available
        if self.event_market and self.parallel_monitor:
            event = self.event_market.event
            self.parallel_monitor.set_monitor_prompt(
                f"{event.name}: {event.description}"
            )
            logger.info("Monitor prompt synced to event: %s", event.name)

        # Start background monitor polling
        monitor_task = asyncio.create_task(self._monitor_loop())
        iteration = 0

        agent_mode = "OpenAI Agents SDK" if self.use_openai_sdk else "Legacy OpenAI"
        logger.info("Using %s agents", agent_mode)

        try:
            while self._running:
                iteration += 1
                dataset_version = self.dataset.version
                market_type = "event" if self.event_market else "AMM"

                # Log iteration start
                if self._sim_logger:
                    self._sim_logger.iteration_start(iteration, len(self.agent_configs))
                if self._stream_handler:
                    self._stream_handler.emit_iteration(iteration, 0, is_start=True)

                len_before_trades = len(self._trade_history)
                len_before_event_trades = len(self._event_trade_history)

                if self.use_openai_sdk:
                    # OpenAI Agents SDK mode
                    await self._run_openai_iteration(iteration, market_type)
                else:
                    # Legacy OpenAI mode
                    await self._run_legacy_iteration(iteration, market_type)

                # Calculate trades executed
                trades_executed = len(self._trade_history) - len_before_trades
                event_trades_executed = len(self._event_trade_history) - len_before_event_trades
                total_trades = trades_executed + event_trades_executed

                # Log iteration summary
                all_holding = self._check_all_agents_holding() if self.event_market else False
                current_prices = self.event_market.get_prices() if self.event_market else {}

                # Log iteration end to simulation logger
                if self._sim_logger:
                    self._sim_logger.iteration_end(iteration, total_trades, current_prices)

                # Emit iteration end and price update to stream handler
                if self._stream_handler:
                    self._stream_handler.emit_iteration(iteration, total_trades, is_start=False)
                    self._stream_handler.emit_price_update(current_prices)

                logger.info(
                    "=== Iteration %d Summary ===\n"
                    "  Agent mode: %s\n"
                    "  Trades executed: %d (AMM: %d, Event: %d)\n"
                    "  Current prices: %s\n"
                    "  All agents holding: %s",
                    iteration,
                    agent_mode,
                    total_trades, trades_executed, event_trades_executed,
                    current_prices,
                    all_holding,
                )

                # Check termination conditions
                should_continue = await self._should_continue(total_trades, dataset_version)

                if not should_continue:
                    if all_holding:
                        logger.info("Consensus reached - all agents holding. Waiting for new information...")
                        try:
                            await asyncio.wait_for(self._new_info_event.wait(), timeout=60.0)
                            self._new_info_event.clear()
                            logger.info("New information detected. Restarting agents...")
                        except asyncio.TimeoutError:
                            logger.info("Timeout waiting for new info. Simulation complete.")
                            break
                    else:
                        logger.info("No further iterations required.")
                        break
        finally:
            self._running = False
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

            # Stop market monitor
            if self._market_monitor:
                await self._market_monitor.stop()
                logger.info("Market monitor stopped")

            # Close database
            if self._db_manager:
                await self._db_manager.close()
                logger.info("Database connection closed")

            # End simulation logger session with summary
            if self._sim_logger:
                duration = time.time() - self._simulation_start_time if self._simulation_start_time else 0
                final_prices = self.event_market.get_prices() if self.event_market else {}
                total_trades = len(self._trade_history) + len(self._event_trade_history)

                # Calculate agent P&Ls
                agent_pnls = {}
                for agent_id, state in self._agent_states.items():
                    # Unrealized P&L from positions
                    unrealized = 0.0
                    for outcome, tokens in state.portfolio.items():
                        if tokens > 0 and outcome in final_prices:
                            current_value = tokens * final_prices[outcome]
                            cost = state.cost_basis.get(outcome, 0.0)
                            unrealized += current_value - cost
                    total_pnl = state.realized_pnl + unrealized
                    agent_pnls[agent_id] = total_pnl

                self._sim_logger.summary(
                    duration_seconds=duration,
                    total_iterations=iteration,
                    total_trades=total_trades,
                    final_prices=final_prices,
                    agent_pnls=agent_pnls,
                )
                self._sim_logger.end_session()
                set_simulation_logger(None)

    async def _run_legacy_iteration(self, iteration: int, market_type: str) -> None:
        """Run one iteration using legacy OpenAI-based agents."""
        self._runtimes = [self._build_runtime(cfg) for cfg in self.agent_configs]
        logger.info(
            "=== Starting %s simulation iteration %d for %d agents (OpenAI) ===",
            market_type, iteration, len(self._runtimes)
        )

        tasks = []
        for runtime in self._runtimes:
            task = asyncio.create_task(runtime.agent.run(runtime.config.prompt))
            runtime.task = task
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def _run_openai_iteration(self, iteration: int, market_type: str) -> None:
        """Run one iteration using OpenAI Agents SDK agents.

        Supports both sequential (default) and parallel execution modes.
        - Sequential: Agents run one at a time, can react to each other's trades
        - Parallel: All agents run simultaneously, faster but no inter-agent reactions
        """
        self._openai_runtimes = []

        mode_str = "parallel" if self.parallel_agents else "sequential"
        logger.info(
            "=== Starting %s simulation iteration %d for %d agents (OpenAI SDK, %s) ===",
            market_type, iteration, len(self.agent_configs), mode_str
        )

        if self.parallel_agents:
            # Run all agents in parallel
            tasks = []
            for idx, cfg in enumerate(self.agent_configs):
                agent_id = cfg.persona.name
                task = asyncio.create_task(
                    self._run_single_openai_agent(agent_id, cfg, idx)
                )
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
            # Check limit orders once after all parallel agents complete
            await self._check_all_limit_orders()
        else:
            # Run agents sequentially (default)
            for idx, cfg in enumerate(self.agent_configs):
                agent_id = cfg.persona.name
                await self._run_single_openai_agent(agent_id, cfg, idx)
                # After each agent trades, check ALL agents' limit orders
                # This allows one agent's trade to trigger another's take-profit/stop-loss
                await self._check_all_limit_orders()

    async def _run_single_openai_agent(
        self, agent_id: str, config: AgentConfig, idx: int
    ) -> None:
        """Run a single OpenAI Agents SDK agent."""
        if not OPENAI_SDK_AVAILABLE:
            logger.error("OpenAI Agents SDK not available")
            return

        # Get or create persistent agent state (portfolios survive across iterations)
        if agent_id in self._agent_states:
            # Reuse existing state - portfolio persists!
            state = self._agent_states[agent_id]
            # Update market references (they might have changed)
            state.event_market = self.event_market
            state.market = self.market
            state.market_lock = self._market_lock
            state.market_monitor = self._market_monitor
            state.stream_handler = self._stream_handler
            logger.info(
                "[%s] Resuming with persistent portfolio: $%.2f cash, %d positions",
                agent_id, state.cash_balance, len(state.portfolio)
            )
        else:
            # First iteration - create new state
            state = TradingAgentState(
                event_market=self.event_market,
                market=self.market,
                market_lock=self._market_lock,
                market_monitor=self._market_monitor,
                stream_handler=self._stream_handler,
                initial_capital=10000.0,
                cash_balance=10000.0,
                agent_id=agent_id,
                db_market_id=self.db_market_id,
            )
            self._agent_states[agent_id] = state
            logger.info("[%s] Created new portfolio with $%.2f", agent_id, state.cash_balance)

        # Create runtime for tracking
        runtime = OpenAIAgentRuntime(
            agent_id=agent_id,
            state=state,
            market_monitor=self._market_monitor,
        )
        self._openai_runtimes.append(runtime)

        # Build system prompt
        if self.event_market:
            system_prompt = build_trading_system_prompt(
                self.event_market.event, agent_id
            )
        else:
            system_prompt = f"You are {agent_id}, an autonomous trading agent."

        # Load MCP servers for external integrations
        try:
            from cliff.integrations.mcp.openai_adapter import load_openai_mcp_servers
            mcp_servers = load_openai_mcp_servers()
        except ImportError:
            mcp_servers = []

        # Create agent
        agent = create_trading_agent(
            state=state,
            event=self.event_market.event if self.event_market else None,
            model=self.openai_model,
            mcp_servers=mcp_servers,
        )

        # Create context for guardrails
        context = TradingContext(state=state)

        # Check for triggered alerts to inject (interrupt-based alerts)
        alert_section = ""
        if self._market_monitor and build_rich_alert_section:
            triggered_alerts = self._market_monitor.get_triggered_alerts(agent_id)
            if triggered_alerts:
                alert_section = build_rich_alert_section(triggered_alerts, agent_id)
                # Mark alerts as delivered after injection
                self._market_monitor.mark_alerts_delivered(agent_id)
                logger.info(
                    "[ALERT] Injecting %d alert(s) into %s's prompt",
                    len(triggered_alerts), agent_id
                )

        # Build initial prompt
        if self.event_market:
            prices = self.event_market.get_prices()
            initial_prompt = f"""{alert_section}You are now trading on: {self.event_market.event.name}

Current prices:
{json.dumps({k: f"${v:.2f}" for k, v in prices.items()}, indent=2)}

Your persona: {config.persona.short_prompt()}

Task: {config.prompt}

Start by checking your portfolio, then research and trade.
"""
        else:
            initial_prompt = alert_section + config.prompt

        # Run the agent with streaming to capture reasoning traces
        logger.info("Starting OpenAI agent: %s", agent_id)

        # Emit agent start event
        if self._stream_handler:
            self._stream_handler.emit_agent_start(agent_id)

        try:
            # Request reasoning traces for thinking models like gpt-5-mini
            # Note: summary="detailed" requires verified OpenAI organization
            # Visit https://platform.openai.com/settings/organization/general to verify
            # If not verified, reasoning will be empty/blank but trading will still work
            model_settings = ModelSettings(
                reasoning=Reasoning(effort="medium", summary="detailed"),
            )
            run_config = RunConfig(
                workflow_name=f"trading_{agent_id}",
                model_settings=model_settings,
            )
            result = Runner.run_streamed(
                agent,
                initial_prompt,
                context=context,
                run_config=run_config,
                max_turns=1000,  # Effectively no limit - agents run until they hold
            )

            # Process stream events to capture reasoning and tool calls
            async for event in result.stream_events():
                await self._process_stream_event(event, agent_id)

            # Check trade history to determine last action
            if state.event_trade_log:
                last_trade = state.event_trade_log[-1]
                runtime.last_action = last_trade.direction
            else:
                runtime.last_action = "hold"

            logger.info(
                "OpenAI agent %s completed. Last action: %s",
                agent_id, runtime.last_action
            )

            # Emit agent complete event
            if self._stream_handler:
                self._stream_handler.emit_agent_complete(agent_id, runtime.last_action)

            # Sync trade history from state
            for trade in state.event_trade_log:
                if trade not in self._event_trade_history:
                    self._event_trade_history.append(trade)

            # Emit price update after agent completes (for real-time chart updates)
            if self._stream_handler and self.event_market:
                self._stream_handler.emit_price_update(self.event_market.get_prices())

        except Exception as e:
            error_detail = str(e)
            if hasattr(e, 'exceptions'):
                nested = [f"{type(ex).__name__}: {ex}" for ex in e.exceptions]
                error_detail = f"{error_detail} -> {nested}"
            elif e.__cause__:
                error_detail = f"{error_detail} -> Caused by: {e.__cause__}"
            logger.error("OpenAI agent %s failed: %s", agent_id, error_detail)
            runtime.last_action = "hold"

    async def _process_stream_event(self, event, agent_id: str) -> None:
        """Process a stream event from the OpenAI Agents SDK.

        Logs reasoning traces, messages, tool calls based on verbosity level.
        """
        if not OPENAI_SDK_AVAILABLE:
            return

        # Debug: Log ALL events at verbosity 3 to see what's coming through
        if self.verbose >= 3:
            event_type = type(event).__name__
            logger.debug("[%s] 📨 Event: %s", agent_id, event_type)

        # Handle RunItemStreamEvent - the main event type with reasoning/tools/messages
        if isinstance(event, RunItemStreamEvent):
            item = event.item

            # Debug: Log item type at verbosity 3
            if self.verbose >= 3:
                item_type = type(item).__name__
                logger.debug("[%s] 📦 Item: %s (name=%s)", agent_id, item_type, getattr(event, 'name', 'N/A'))

            # Reasoning traces (thinking steps) - shown by default
            if isinstance(item, ReasoningItem) and self.verbose >= 1:
                raw = item.raw_item
                # Extract summary text (high-level thinking summaries)
                if hasattr(raw, 'summary') and raw.summary:
                    for s in raw.summary:
                        if hasattr(s, 'text') and s.text:
                            logger.info("[%s] 💭 Thinking: %s", agent_id, s.text)
                            # Log to simulation logger
                            if self._sim_logger:
                                self._sim_logger.thinking(agent_id, s.text)
                            # Emit to stream handler
                            if self._stream_handler:
                                self._stream_handler.emit_agent_thinking(agent_id, s.text)
                # Extract encrypted_content (detailed reasoning from thinking models)
                # This requires response_include=["reasoning.encrypted_content"]
                if hasattr(raw, 'encrypted_content') and raw.encrypted_content:
                    reasoning_text = raw.encrypted_content[:500] + "..." if len(raw.encrypted_content) > 500 else raw.encrypted_content
                    logger.info("[%s] 💭 Reasoning: %s", agent_id, reasoning_text)
                    # Log to simulation logger
                    if self._sim_logger:
                        self._sim_logger.thinking(agent_id, reasoning_text)
                    # Emit to stream handler
                    if self._stream_handler:
                        self._stream_handler.emit_agent_thinking(agent_id, reasoning_text)
                # Extract content (detailed reasoning)
                if hasattr(raw, 'content') and raw.content and self.verbose >= 3:
                    for c in raw.content:
                        if hasattr(c, 'text') and c.text:
                            logger.debug("[%s] 💭 Detail: %s", agent_id, c.text)

            # Message output (agent's response) - verbose mode (2+)
            elif isinstance(item, MessageOutputItem) and self.verbose >= 2:
                raw = item.raw_item
                if hasattr(raw, 'content') and raw.content:
                    for content_item in raw.content:
                        if hasattr(content_item, 'text'):
                            text = content_item.text
                            full_text = text  # Keep full text for simulation logger
                            # Truncate long messages for standard logging
                            if len(text) > 500:
                                text = text[:500] + "..."
                            logger.info("[%s] 💬 Response: %s", agent_id, text)
                            # Log full response to simulation logger
                            if self._sim_logger:
                                self._sim_logger.response(agent_id, full_text)

            # Tool calls - always log (1+)
            elif isinstance(item, ToolCallItem) and self.verbose >= 1:
                raw = item.raw_item
                # Extract function name - different tool types have different structures
                tool_name = "unknown"
                tool_args = ""
                tool_args_dict = {}

                # Function tool call (custom tools like get_portfolio, place_trade)
                if hasattr(raw, 'name') and raw.name:
                    tool_name = raw.name
                    if hasattr(raw, 'arguments') and raw.arguments:
                        # Parse args for both display and logging
                        try:
                            tool_args_dict = json.loads(raw.arguments)
                            if self.verbose >= 2:
                                # Show first 2 key args for console
                                arg_preview = ", ".join(f"{k}={v}" for k, v in list(tool_args_dict.items())[:2])
                                tool_args = f"({arg_preview})"
                        except:
                            tool_args = ""
                # Hosted tool calls (web_search, code_interpreter)
                elif hasattr(raw, 'type'):
                    tool_name = raw.type
                    if raw.type == 'web_search_call' and hasattr(raw, 'query'):
                        tool_args_dict = {"query": getattr(raw, 'query', '')}
                        if self.verbose >= 2:
                            tool_args = f"(query={raw.query[:50]}...)" if len(getattr(raw, 'query', '')) > 50 else f"(query={getattr(raw, 'query', '')})"
                    elif raw.type == 'code_interpreter_call' and hasattr(raw, 'code'):
                        code_preview = getattr(raw, 'code', '')[:60].replace('\n', ' ')
                        tool_args_dict = {"code": code_preview}
                        if self.verbose >= 2:
                            tool_args = f"({code_preview}...)"

                logger.info("[%s] 🔧 Tool call: %s%s", agent_id, tool_name, tool_args)

                # Log to simulation logger
                if self._sim_logger:
                    self._sim_logger.action(agent_id, tool_name, tool_args_dict if tool_args_dict else None)

                # Emit to stream handler - special handling for web search
                if self._stream_handler:
                    if tool_name == 'web_search_call':
                        query = tool_args_dict.get('query', '')
                        self._stream_handler.emit_agent_researching(agent_id, query)
                    else:
                        # For other tool calls, emit as thinking with tool info
                        tool_desc = f"Using {tool_name}"
                        if tool_args_dict:
                            arg_preview = ", ".join(f"{k}={v}" for k, v in list(tool_args_dict.items())[:2])
                            tool_desc = f"Using {tool_name}({arg_preview})"
                        self._stream_handler.emit_agent_thinking(agent_id, tool_desc)

            # Tool output - debug mode (3)
            elif isinstance(item, ToolCallOutputItem) and self.verbose >= 3:
                raw = item.raw_item
                output = str(raw)[:200] if raw else "None"
                logger.debug("[%s] 📤 Tool output: %s...", agent_id, output)

            # Handoffs - always log
            elif isinstance(item, HandoffCallItem):
                logger.info("[%s] 🔀 Handoff requested", agent_id)
            elif isinstance(item, HandoffOutputItem):
                logger.info("[%s] 🔀 Handoff completed", agent_id)

    async def _monitor_loop(self) -> None:
        """Background task that polls Parallel monitor API for new market-relevant information."""
        logger.info("Background monitor polling started (1 hour interval)")
        while self._running:
            await asyncio.sleep(3600)  # Poll every hour (Parallel API rate limit)
            if not self.parallel_monitor:
                continue

            try:
                updates = await self.parallel_monitor.check_updates()
                if updates:
                    new_urls = [u.get("url") for u in updates if u.get("url")]
                    if new_urls:
                        self.dataset.add_urls(new_urls)
                        logger.info("Monitor detected %d new URLs: %s", len(new_urls), new_urls[:3])
                        self._new_info_event.set()
            except Exception as e:
                logger.warning("Monitor poll failed: %s", e)

    @property
    def trade_history(self) -> List[TradeExecution]:
        return list(self._trade_history)

    @property
    def event_trade_history(self) -> List[EventTradeResult]:
        return list(self._event_trade_history)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_runtime(self, config: AgentConfig) -> AgentRuntime:
        async def trade_callback(trade: TradeExecution) -> None:
            async with self._broadcast_lock:
                self._trade_history.append(trade)
                logger.info(
                    "Trade executed: agent=%s direction=%s price=%.4f",
                    trade.agent_id,
                    trade.direction,
                    trade.price,
                )
                for runtime in self._runtimes:
                    runtime.agent.observe_market_trade(trade)

        async def event_trade_callback(trade: EventTradeResult) -> None:
            async with self._broadcast_lock:
                self._event_trade_history.append(trade)
                logger.info(
                    "Event trade executed: agent=%s outcome=%s direction=%s price=%.4f",
                    trade.agent_id,
                    trade.outcome,
                    trade.direction,
                    trade.price,
                )

        agent = AsyncTradingAgent(
            persona=config.persona,
            market=self.market,
            openai_client=self._openai_client,
            parallel_extract=self.parallel_extract,
            parallel_monitor=self.parallel_monitor,
            sub_agent_config=config.sub_agent_config,
            market_lock=self._market_lock,
            trade_callback=trade_callback,
            event_trade_callback=event_trade_callback,
            metrics=self.metrics,
            dataset=self.dataset,
            turbopuffer_client=self.turbopuffer,
            event_market=self.event_market,
            llm_model=self.llm_model,
        )

        return AgentRuntime(config=config, agent=agent)

    async def _should_continue(self, trades_executed: int, dataset_version: int) -> bool:
        """
        Determine if simulation should continue.

        For event markets:
        - Continue if NOT all agents are holding (still divergent views)
        - If all holding (consensus), check for new information
        - Only stop when consensus AND no new information

        Returns True to continue, False to stop.
        """
        # For event markets, check if there's still divergent opinion
        if self.event_market:
            all_holding = self._check_all_agents_holding()
            if not all_holding:
                # Agents still have different views - continue trading
                logger.info("Agents still have divergent views. Continuing...")
                return True
            # All holding - consensus reached, need new info to continue

        # Check for new dataset entries (from manual adds or monitor)
        if self.dataset.version != dataset_version:
            logger.info("New dataset entries detected. Restarting agents.")
            return True

        # Check for document ingestion updates
        if self._consume_document_updates():
            logger.info("New document ingestions detected. Restarting agents.")
            return True

        # If background monitor already found new info, it will have set the event
        # Don't duplicate the monitor check here - let the main loop handle waiting

        logger.info("No new information available.")
        return False

    def _check_all_agents_holding(self) -> bool:
        """Check if all agents decided to hold (consensus reached)."""
        if self.use_openai_sdk:
            # Check OpenAI Agents SDK agents
            if not self._openai_runtimes:
                return True

            for runtime in self._openai_runtimes:
                if runtime.last_action is None:
                    logger.debug("OpenAI agent %s has no last action.", runtime.agent_id)
                    return False
                if runtime.last_action != "hold":
                    logger.debug(
                        "OpenAI agent %s last action was %s, not hold.",
                        runtime.agent_id,
                        runtime.last_action,
                    )
                    return False
            return True
        else:
            # Check legacy agents
            if not self._runtimes:
                return True

            for runtime in self._runtimes:
                agent = runtime.agent
                if agent.last_decision is None:
                    logger.debug("Agent %s has no last decision.", agent.persona.name)
                    return False
                if agent.last_decision.action != "hold":
                    logger.debug(
                        "Agent %s last action was %s, not hold.",
                        agent.persona.name,
                        agent.last_decision.action,
                    )
                    return False

            return True

    def _consume_document_updates(self) -> bool:
        if not self.doc_update_file.exists():
            return False
        try:
            data = json.loads(self.doc_update_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = []
        self.doc_update_file.write_text("[]", encoding="utf-8")
        return bool(data)


