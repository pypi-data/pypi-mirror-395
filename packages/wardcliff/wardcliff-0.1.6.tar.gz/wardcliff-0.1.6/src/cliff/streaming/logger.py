"""
Comprehensive simulation logger for rich, structured output.

Produces detailed step-by-step logs in a format that captures everything:
- Agent reasoning (THINKING)
- Tool calls (ACTION)
- Agent responses (RESPONSE)
- Trade executions (TRADE)
- Limit order events (LIMIT_ORDER)
- Price alerts (ALERT)
- Portfolio state (PORTFOLIO)
- Price updates (PRICE)
- Errors and warnings (ERROR/WARNING)

Format matches the structured logging used in game AI systems:
================================================================================
SIMULATION SESSION: [ISO-8601 Timestamp]
PROMPT: [Event description]
AGENTS: [List of agents]
================================================================================
[timestamp] Step   1 | THINKING | Agent reasoning text...
[timestamp] Step   2 | ACTION   | get_portfolio()
[timestamp] Step   3 | RESPONSE | Portfolio: $10000 cash, ...
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO

logger = logging.getLogger(__name__)


class LogEventType(Enum):
    """Types of events that can be logged."""
    # Agent events
    THINKING = "THINKING"
    ACTION = "ACTION"
    RESPONSE = "RESPONSE"

    # Trade events
    TRADE = "TRADE"
    LIMIT_ORDER = "LIMIT_ORDER"
    ORDER_FILL = "ORDER_FILL"

    # Alert events
    ALERT = "ALERT"
    ALERT_CONFIG = "ALERT_CFG"

    # Market events
    PRICE = "PRICE"
    PORTFOLIO = "PORTFOLIO"

    # System events
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    # Session events
    SESSION_START = "SESSION"
    ITERATION = "ITERATION"
    SUMMARY = "SUMMARY"


@dataclass
class LogEntry:
    """A single log entry with full metadata."""
    timestamp: datetime
    step: int
    event_type: LogEventType
    content: str
    agent_id: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)


class SimulationLogger:
    """
    Comprehensive simulation logger.

    Writes detailed, structured logs to a file and optionally to console.
    Each simulation session gets a full log with headers and step tracking.
    """

    def __init__(
        self,
        log_file: Optional[str] = None,
        log_dir: str = "logs",
        console_output: bool = True,
        include_timestamps: bool = True,
        include_step_numbers: bool = True,
        max_content_length: int = 0,  # 0 = unlimited
    ):
        """
        Initialize the simulation logger.

        Args:
            log_file: Specific log file path (optional, auto-generated if None)
            log_dir: Directory for log files
            console_output: Also print to console
            include_timestamps: Include ISO timestamps in each line
            include_step_numbers: Include step numbers
            max_content_length: Truncate content longer than this (0 = no limit)
        """
        self.log_dir = Path(log_dir)
        self.console_output = console_output
        self.include_timestamps = include_timestamps
        self.include_step_numbers = include_step_numbers
        self.max_content_length = max_content_length

        # Step tracking per agent
        self._step_counters: Dict[str, int] = {}
        self._global_step: int = 0

        # Session info
        self._session_start: Optional[datetime] = None
        self._session_prompt: str = ""
        self._session_agents: List[str] = []

        # Log file handle
        self._log_file: Optional[TextIO] = None
        self._log_path: Optional[Path] = None

        # Initialize log file
        if log_file:
            self._log_path = Path(log_file)

    def start_session(
        self,
        prompt: str,
        agents: List[str],
        event_name: Optional[str] = None,
        initial_prices: Optional[Dict[str, float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start a new logging session.

        Args:
            prompt: The simulation prompt/task description
            agents: List of agent IDs participating
            event_name: Name of the prediction market event
            initial_prices: Starting prices for outcomes
            metadata: Additional session metadata

        Returns:
            Path to the log file
        """
        self._session_start = datetime.now(timezone.utc)
        self._session_prompt = prompt
        self._session_agents = agents
        self._step_counters = {agent: 0 for agent in agents}
        self._global_step = 0

        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Generate log file name if not specified
        if self._log_path is None:
            timestamp = self._session_start.strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c if c.isalnum() else "_" for c in (event_name or "simulation")[:30])
            self._log_path = self.log_dir / f"{safe_name}_{timestamp}.log"

        # Open log file
        self._log_file = open(self._log_path, "w", encoding="utf-8")

        # Write session header
        self._write_header(event_name, initial_prices, metadata)

        logger.info("Simulation logger started: %s", self._log_path)
        return str(self._log_path)

    def _write_header(
        self,
        event_name: Optional[str],
        initial_prices: Optional[Dict[str, float]],
        metadata: Optional[Dict[str, Any]],
    ) -> None:
        """Write the session header."""
        header_lines = [
            "=" * 80,
            f"SIMULATION SESSION: {self._session_start.isoformat()}",
            f"EVENT: {event_name or 'N/A'}",
            f"PROMPT: {self._session_prompt}",
            f"AGENTS: {', '.join(self._session_agents)}",
        ]

        if initial_prices:
            prices_str = ", ".join(f"{k}: ${v:.4f}" for k, v in initial_prices.items())
            header_lines.append(f"INITIAL PRICES: {prices_str}")

        if metadata:
            for key, value in metadata.items():
                header_lines.append(f"{key.upper()}: {value}")

        header_lines.append("=" * 80)
        header_lines.append("")  # Blank line after header

        header = "\n".join(header_lines)
        self._write_raw(header)

    def _write_raw(self, text: str) -> None:
        """Write raw text to log file and optionally console."""
        if self._log_file:
            self._log_file.write(text + "\n")
            self._log_file.flush()

        if self.console_output:
            print(text)

    def _format_entry(self, entry: LogEntry) -> str:
        """Format a log entry as a single line."""
        parts = []

        # Timestamp
        if self.include_timestamps:
            parts.append(f"[{entry.timestamp.isoformat()}]")

        # Step number (padded to 4 digits)
        if self.include_step_numbers:
            parts.append(f"Step {entry.step:4d}")

        # Agent ID (if present)
        if entry.agent_id:
            parts.append(f"[{entry.agent_id}]")

        # Event type (padded to 10 chars for alignment)
        parts.append(f"| {entry.event_type.value:10s}")

        # Content
        content = entry.content
        if self.max_content_length > 0 and len(content) > self.max_content_length:
            content = content[:self.max_content_length] + "..."

        # Replace newlines with spaces for single-line output
        content = content.replace("\n", " ").replace("\r", "")
        parts.append(f"| {content}")

        return " ".join(parts)

    def _get_next_step(self, agent_id: Optional[str] = None) -> int:
        """Get the next step number."""
        self._global_step += 1
        if agent_id and agent_id in self._step_counters:
            self._step_counters[agent_id] += 1
        return self._global_step

    def log(
        self,
        event_type: LogEventType,
        content: str,
        agent_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log an event.

        Args:
            event_type: Type of event
            content: Human-readable content
            agent_id: ID of the agent (if agent-specific)
            data: Additional structured data
        """
        entry = LogEntry(
            timestamp=datetime.now(timezone.utc),
            step=self._get_next_step(agent_id),
            event_type=event_type,
            content=content,
            agent_id=agent_id,
            data=data or {},
        )

        formatted = self._format_entry(entry)
        self._write_raw(formatted)

    # =========================================================================
    # Convenience methods for common event types
    # =========================================================================

    def thinking(self, agent_id: str, text: str) -> None:
        """Log agent thinking/reasoning."""
        self.log(LogEventType.THINKING, text, agent_id=agent_id)

    def action(self, agent_id: str, tool_name: str, args: Optional[Dict[str, Any]] = None) -> None:
        """Log a tool call/action."""
        if args:
            # Format args nicely
            args_str = ", ".join(f"{k}={v}" for k, v in args.items())
            content = f"{tool_name}({args_str})"
        else:
            content = f"{tool_name}()"
        self.log(LogEventType.ACTION, content, agent_id=agent_id, data={"tool": tool_name, "args": args})

    def response(self, agent_id: str, text: str) -> None:
        """Log agent response/output."""
        self.log(LogEventType.RESPONSE, text, agent_id=agent_id)

    def trade(
        self,
        agent_id: str,
        outcome: str,
        action: str,
        size: float,
        price_before: float,
        price_after: float,
        rationale: str = "",
    ) -> None:
        """Log a trade execution."""
        slippage = abs(price_after - price_before) / price_before * 100 if price_before > 0 else 0
        content = (
            f"{action.upper()} {outcome} | "
            f"Size: ${size:.2f} | "
            f"Price: ${price_before:.4f} -> ${price_after:.4f} | "
            f"Slippage: {slippage:.2f}%"
        )
        if rationale:
            content += f" | Rationale: {rationale[:100]}"

        self.log(
            LogEventType.TRADE,
            content,
            agent_id=agent_id,
            data={
                "outcome": outcome,
                "action": action,
                "size": size,
                "price_before": price_before,
                "price_after": price_after,
                "slippage_pct": slippage,
                "rationale": rationale,
            },
        )

    def limit_order(
        self,
        agent_id: str,
        order_type: str,
        outcome: str,
        trigger_price: float,
        size: float,
        order_id: str,
    ) -> None:
        """Log a limit order placement."""
        content = (
            f"{order_type.upper()} {outcome} | "
            f"Trigger: ${trigger_price:.4f} | "
            f"Size: {size:.2f} | "
            f"ID: {order_id}"
        )
        self.log(
            LogEventType.LIMIT_ORDER,
            content,
            agent_id=agent_id,
            data={
                "order_type": order_type,
                "outcome": outcome,
                "trigger_price": trigger_price,
                "size": size,
                "order_id": order_id,
            },
        )

    def order_fill(
        self,
        agent_id: str,
        order_id: str,
        order_type: str,
        outcome: str,
        fill_price: float,
        size: float,
    ) -> None:
        """Log a limit order fill."""
        content = (
            f"FILLED {order_type.upper()} {outcome} | "
            f"Fill Price: ${fill_price:.4f} | "
            f"Size: {size:.2f} | "
            f"ID: {order_id}"
        )
        self.log(
            LogEventType.ORDER_FILL,
            content,
            agent_id=agent_id,
            data={
                "order_id": order_id,
                "order_type": order_type,
                "outcome": outcome,
                "fill_price": fill_price,
                "size": size,
            },
        )

    def alert(
        self,
        agent_id: str,
        outcome: str,
        message: str,
        alert_type: str = "price",
        priority: str = "normal",
    ) -> None:
        """Log a triggered alert."""
        content = f"[{priority.upper()}] {outcome} | {message}"
        self.log(
            LogEventType.ALERT,
            content,
            agent_id=agent_id,
            data={
                "outcome": outcome,
                "alert_type": alert_type,
                "priority": priority,
                "message": message,
            },
        )

    def alert_configured(
        self,
        agent_id: str,
        outcome: str,
        conditions: Dict[str, Any],
        rationale: str,
    ) -> None:
        """Log alert configuration."""
        cond_str = ", ".join(f"{k}={v}" for k, v in conditions.items())
        content = f"Configured for {outcome}: {cond_str} | {rationale[:50]}"
        self.log(
            LogEventType.ALERT_CONFIG,
            content,
            agent_id=agent_id,
            data={"outcome": outcome, "conditions": conditions, "rationale": rationale},
        )

    def portfolio(
        self,
        agent_id: str,
        cash: float,
        positions: Dict[str, float],
        total_value: float,
        pnl: float,
    ) -> None:
        """Log portfolio state."""
        pos_str = ", ".join(f"{k}: {v:.2f}" for k, v in positions.items()) if positions else "none"
        content = (
            f"Cash: ${cash:.2f} | "
            f"Positions: {pos_str} | "
            f"Total: ${total_value:.2f} | "
            f"P&L: ${pnl:+.2f}"
        )
        self.log(
            LogEventType.PORTFOLIO,
            content,
            agent_id=agent_id,
            data={"cash": cash, "positions": positions, "total_value": total_value, "pnl": pnl},
        )

    def price_update(
        self,
        prices: Dict[str, float],
        changes: Optional[Dict[str, float]] = None,
    ) -> None:
        """Log price update."""
        parts = []
        for outcome, price in prices.items():
            if changes and outcome in changes:
                change = changes[outcome]
                sign = "+" if change >= 0 else ""
                parts.append(f"{outcome}: ${price:.4f} ({sign}{change*100:.2f}%)")
            else:
                parts.append(f"{outcome}: ${price:.4f}")
        content = " | ".join(parts)
        self.log(LogEventType.PRICE, content, data={"prices": prices, "changes": changes})

    def iteration_start(self, iteration: int, agent_count: int) -> None:
        """Log iteration start."""
        content = f"=== Starting Iteration {iteration} ({agent_count} agents) ==="
        self.log(LogEventType.ITERATION, content)

    def iteration_end(self, iteration: int, trades: int, prices: Dict[str, float]) -> None:
        """Log iteration end."""
        prices_str = ", ".join(f"{k}: ${v:.4f}" for k, v in prices.items())
        content = f"=== Iteration {iteration} Complete | Trades: {trades} | Prices: {prices_str} ==="
        self.log(LogEventType.ITERATION, content, data={"iteration": iteration, "trades": trades, "prices": prices})

    def info(self, message: str, agent_id: Optional[str] = None) -> None:
        """Log informational message."""
        self.log(LogEventType.INFO, message, agent_id=agent_id)

    def warning(self, message: str, agent_id: Optional[str] = None) -> None:
        """Log warning message."""
        self.log(LogEventType.WARNING, message, agent_id=agent_id)

    def error(self, message: str, agent_id: Optional[str] = None) -> None:
        """Log error message."""
        self.log(LogEventType.ERROR, message, agent_id=agent_id)

    def summary(
        self,
        duration_seconds: float,
        total_iterations: int,
        total_trades: int,
        final_prices: Dict[str, float],
        agent_pnls: Dict[str, float],
    ) -> None:
        """Log session summary."""
        self._write_raw("")  # Blank line before summary
        self._write_raw("=" * 80)
        self._write_raw("SESSION SUMMARY")
        self._write_raw("=" * 80)
        self._write_raw(f"Duration: {duration_seconds:.1f} seconds")
        self._write_raw(f"Iterations: {total_iterations}")
        self._write_raw(f"Total Trades: {total_trades}")
        self._write_raw(f"Final Prices: {json.dumps({k: f'${v:.4f}' for k, v in final_prices.items()})}")
        self._write_raw("")
        self._write_raw("Agent P&L:")
        for agent, pnl in agent_pnls.items():
            self._write_raw(f"  {agent}: ${pnl:+.2f}")
        self._write_raw("=" * 80)

    def end_session(self) -> None:
        """End the logging session and close the file."""
        if self._log_file:
            self._log_file.close()
            self._log_file = None
            logger.info("Simulation log saved: %s", self._log_path)

    def __enter__(self) -> "SimulationLogger":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.end_session()


# Global logger instance for easy access
_simulation_logger: Optional[SimulationLogger] = None


def get_simulation_logger() -> Optional[SimulationLogger]:
    """Get the global simulation logger instance."""
    return _simulation_logger


def set_simulation_logger(logger: SimulationLogger) -> None:
    """Set the global simulation logger instance."""
    global _simulation_logger
    _simulation_logger = logger
