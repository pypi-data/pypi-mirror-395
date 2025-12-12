"""
Rich terminal display for real-time streaming output.

Uses Rich library for beautiful, live-updating terminal UI.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .events import EventType, StreamEvent


class RichDisplay:
    """
    Rich-based terminal display for simulation output.

    Creates a live-updating dashboard showing:
    - Market prices with change indicators
    - Agent status and activity
    - Recent trades
    - Price alerts
    """

    def __init__(
        self,
        console: Optional[Console] = None,
        verbosity: int = 1,
        market_name: str = "Trading Simulation",
    ):
        """
        Initialize the display.

        Args:
            console: Rich Console instance (creates new if None)
            verbosity: Output detail level (0=minimal, 1=normal, 2=verbose)
            market_name: Name to show in header
        """
        self.console = console or Console()
        self.verbosity = verbosity
        self.market_name = market_name
        self._live: Optional[Live] = None

        # State tracking
        self.prices: Dict[str, float] = {}
        self.price_changes: Dict[str, float] = {}
        self.price_history: Dict[str, List[float]] = {}  # outcome -> price history
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.trades: List[Dict[str, Any]] = []
        self.alerts: List[str] = []
        self.iteration = 0
        self.total_trades = 0
        self.start_time = datetime.now()

        # P&L tracking
        self.initial_capital = 10000.0
        self.last_turn_value = 10000.0
        self.current_value = 10000.0
        self.all_time_pnl = 0.0
        self.turn_pnl = 0.0

        # Agent colors (orange1 as primary brand color)
        self._colors = ["orange1", "magenta", "yellow", "green", "cyan", "red"]
        self._agent_colors: Dict[str, str] = {}

        # Throttle display updates to prevent blocking async loop
        self._last_update = 0.0
        self._update_interval = 0.1  # Max 10 updates/second

    def _get_agent_color(self, agent_id: str) -> str:
        """Get consistent color for an agent."""
        if agent_id not in self._agent_colors:
            idx = len(self._agent_colors) % len(self._colors)
            self._agent_colors[agent_id] = self._colors[idx]
        return self._agent_colors[agent_id]

    def start(self) -> None:
        """Start the live display."""
        if self.verbosity == 0:
            return  # Minimal mode doesn't use live display

        self._live = Live(
            self._render(),
            console=self.console,
            refresh_per_second=4,
            screen=True,
        )
        self._live.start()

    def stop(self) -> None:
        """Stop the live display."""
        if self._live:
            self._live.stop()
            self._live = None

    def update(self) -> None:
        """Refresh the display."""
        if self._live:
            self._live.update(self._render())

    def handle_event(self, event: StreamEvent) -> None:
        """
        Handle a stream event and update the display.

        This is the main entry point called by StreamHandler.
        """
        if self.verbosity == 0:
            # Minimal mode - just print trade lines
            self._handle_minimal(event)
            return

        # Update internal state based on event
        if event.event_type == EventType.AGENT_STARTED:
            self.agents[event.agent_id] = {
                "status": "starting",
                "activity": "Initializing...",
                "trades": 0,
                "pnl": 0.0,
            }

        elif event.event_type == EventType.AGENT_THINKING:
            if event.agent_id in self.agents:
                text = event.data.get("text", "")[:80]
                self.agents[event.agent_id]["status"] = "thinking"
                self.agents[event.agent_id]["activity"] = text

        elif event.event_type == EventType.AGENT_RESEARCHING:
            if event.agent_id in self.agents:
                query = event.data.get("query", "")[:60]
                self.agents[event.agent_id]["status"] = "researching"
                self.agents[event.agent_id]["activity"] = f'Searching: "{query}"'

        elif event.event_type == EventType.TRADE_EXECUTED:
            self._handle_trade(event)

        elif event.event_type == EventType.PRICE_UPDATE:
            self._handle_price_update(event)

        elif event.event_type == EventType.PRICE_ALERT:
            msg = event.data.get("message", "Alert")
            self.alerts.append(msg)
            self.alerts = self.alerts[-5:]  # Keep last 5

        elif event.event_type == EventType.AGENT_COMPLETED:
            if event.agent_id in self.agents:
                self.agents[event.agent_id]["status"] = "done"
                self.agents[event.agent_id]["activity"] = f"Decided: {event.data.get('decision', 'hold')}"

        elif event.event_type == EventType.ITERATION_END:
            self.iteration = event.data.get("iteration", self.iteration)
            self.total_trades = event.data.get("trades", self.total_trades)
            # Update turn P&L tracking
            if self.current_value > 0:
                self.last_turn_value = self.current_value

        elif event.event_type == EventType.PORTFOLIO_UPDATE:
            # Update P&L metrics
            self.current_value = event.data.get("total_value", self.current_value)
            if self.initial_capital > 0:
                self.all_time_pnl = (self.current_value - self.initial_capital) / self.initial_capital
            if self.last_turn_value > 0:
                self.turn_pnl = (self.current_value - self.last_turn_value) / self.last_turn_value

            # Update per-agent metrics if provided
            agent_id = event.agent_id
            if agent_id and agent_id in self.agents:
                self.agents[agent_id]["cash"] = event.data.get("cash", 0)
                self.agents[agent_id]["pnl"] = event.data.get("pnl", 0)

        # Throttle display updates to prevent blocking async event loop
        now = time.monotonic()
        if now - self._last_update >= self._update_interval:
            self._last_update = now
            self.update()

    def _handle_minimal(self, event: StreamEvent) -> None:
        """Handle event in minimal mode - just print key events."""
        if event.event_type == EventType.TRADE_EXECUTED:
            data = event.data
            action = data.get("action", "").upper()
            style = "green" if action == "BUY" else "red"
            self.console.print(
                f"[dim][{datetime.now().strftime('%H:%M:%S')}][/] "
                f"{event.agent_id} [{style}]{action}[/] "
                f"{data.get('outcome')} ${data.get('size', 0):.0f} @ ${data.get('price', 0):.4f}"
            )
        elif event.event_type == EventType.ITERATION_END:
            self.console.print(
                f"[dim]Iteration {event.data.get('iteration')}: "
                f"{event.data.get('trades')} trades[/]"
            )

    def _handle_trade(self, event: StreamEvent) -> None:
        """Process a trade event."""
        data = event.data
        trade = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent_id": event.agent_id,
            "action": data.get("action", ""),
            "outcome": data.get("outcome", ""),
            "size": data.get("size", 0),
            "price": data.get("price", 0),
            "slippage": data.get("slippage", 0),
            "rationale": data.get("rationale", "") or data.get("note", ""),
        }
        self.trades.append(trade)
        self.trades = self.trades[-10:]  # Keep last 10

        # Update agent stats
        if event.agent_id in self.agents:
            self.agents[event.agent_id]["trades"] = self.agents[event.agent_id].get("trades", 0) + 1
            self.agents[event.agent_id]["status"] = "traded"
            action = data.get("action", "").upper()
            self.agents[event.agent_id]["activity"] = f"{action} {data.get('outcome')} @ ${data.get('price', 0):.4f}"

    def _handle_price_update(self, event: StreamEvent) -> None:
        """Process a price update event."""
        new_prices = event.data.get("prices", {})
        changes = event.data.get("changes", {})

        # Calculate changes if not provided
        if not changes and self.prices:
            for outcome, price in new_prices.items():
                if outcome in self.prices and self.prices[outcome] > 0:
                    change = (price - self.prices[outcome]) / self.prices[outcome]
                    changes[outcome] = change

        # Track price history for chart
        for outcome, price in new_prices.items():
            if outcome not in self.price_history:
                self.price_history[outcome] = []
            self.price_history[outcome].append(price)
            # Keep last 60 data points
            if len(self.price_history[outcome]) > 60:
                self.price_history[outcome] = self.price_history[outcome][-60:]

        self.prices = new_prices
        self.price_changes = changes

    def _render_chart(self, width: int = 50, height: int = 6) -> Panel:
        """Render Polymarket-style multi-line price chart with colored lines."""
        if not self.price_history or not any(self.price_history.values()):
            return Panel("[dim]No price history yet[/]", title="[bold orange1]PRICE CHART[/]")

        # Chart colors for each outcome
        chart_colors = ["orange1", "cyan", "magenta", "yellow", "green", "red"]
        sorted_outcomes = sorted(self.price_history.keys())
        outcome_colors: Dict[str, str] = {}
        for i, outcome in enumerate(sorted_outcomes):
            outcome_colors[outcome] = chart_colors[i % len(chart_colors)]

        # Get max data points across all outcomes
        max_points = max(len(h) for h in self.price_history.values())
        if max_points < 2:
            return Panel("[dim]Collecting price data...[/]", title="[bold orange1]PRICE CHART[/]")

        # Fixed Y-axis: 0% to 100% for prediction markets
        y_min, y_max = 0.0, 1.0

        # Braille character mapping (2 columns x 4 rows per character)
        BRAILLE_BASE = 0x2800
        DOT_MAP = [
            [0x01, 0x08],  # row 0: dots 1, 4
            [0x02, 0x10],  # row 1: dots 2, 5
            [0x04, 0x20],  # row 2: dots 3, 6
            [0x40, 0x80],  # row 3: dots 7, 8
        ]

        char_width = width
        char_height = height

        # Create separate grid per outcome for colored rendering
        outcome_grids: Dict[str, List[List[int]]] = {}
        for outcome in sorted_outcomes:
            outcome_grids[outcome] = [[0 for _ in range(char_width)] for _ in range(char_height)]

        def _plot_line(grid, x1, y1, x2, y2):
            """Draw line between two points using Bresenham's algorithm."""
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
                # Plot current point
                char_x = x1 // 2
                char_y = y1 // 4
                dot_col = x1 % 2
                dot_row = y1 % 4
                if 0 <= char_x < char_width and 0 <= char_y < char_height:
                    grid[char_y][char_x] |= DOT_MAP[dot_row][dot_col]

                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy

        # Plot each outcome into its own grid with connected lines
        for outcome, prices in self.price_history.items():
            if not prices:
                continue

            grid = outcome_grids[outcome]
            x_positions = char_width * 2
            resampled = []
            for i in range(x_positions):
                idx = int(i * len(prices) / x_positions)
                idx = min(idx, len(prices) - 1)
                resampled.append(prices[idx])

            # Convert prices to y-coordinates in dot space
            prev_x, prev_y = None, None
            for x, price in enumerate(resampled):
                y_norm = (price - y_min) / (y_max - y_min)
                y_norm = max(0, min(1, y_norm))
                y_dot = int((1 - y_norm) * (char_height * 4 - 1))
                y_dot = max(0, min(char_height * 4 - 1, y_dot))

                if prev_x is not None and prev_y is not None:
                    # Draw line from previous point to current point
                    _plot_line(grid, prev_x, prev_y, x, y_dot)
                else:
                    # First point - just plot it
                    char_x = x // 2
                    char_y = y_dot // 4
                    dot_col = x % 2
                    dot_row = y_dot % 4
                    if 0 <= char_x < char_width and 0 <= char_y < char_height:
                        grid[char_y][char_x] |= DOT_MAP[dot_row][dot_col]

                prev_x, prev_y = x, y_dot

        # Render grid with colors - each outcome rendered in its own color
        lines = []
        lines.append(Text("100%│", style="dim"))

        for row_idx in range(char_height):
            line = Text()
            if row_idx == char_height // 2:
                line.append(" 50%│", style="dim")
            elif row_idx == char_height - 1:
                line.append("  0%│", style="dim")
            else:
                line.append("    │", style="dim")

            # For each column, render each outcome's dots in its color
            for col_idx in range(char_width):
                # Collect all outcomes that have dots in this cell
                outcomes_in_cell = []
                combined_val = 0
                for outcome in sorted_outcomes:
                    char_val = outcome_grids[outcome][row_idx][col_idx]
                    if char_val > 0:
                        outcomes_in_cell.append((outcome, char_val))
                        combined_val |= char_val

                if len(outcomes_in_cell) == 0:
                    line.append(" ")
                elif len(outcomes_in_cell) == 1:
                    # Single outcome - use its color
                    outcome, char_val = outcomes_in_cell[0]
                    line.append(chr(BRAILLE_BASE + char_val), style=f"bold {outcome_colors[outcome]}")
                else:
                    # Multiple outcomes overlap - combine patterns, use white
                    line.append(chr(BRAILLE_BASE + combined_val), style="bold white")

            lines.append(line)

        # X-axis
        x_axis = Text("    └" + "─" * char_width, style="dim")
        lines.append(x_axis)

        # Legend with colored dots
        legend = Text("     ")
        for outcome in sorted(self.price_history.keys()):
            color = outcome_colors[outcome]
            price = self.prices.get(outcome, 0)
            short_name = outcome[:12]
            legend.append("● ", style=color)
            legend.append(f"{short_name} ${price:.2f}  ", style=color)
        lines.append(legend)

        content = Group(*lines)
        return Panel(content, title="[bold orange1]PRICE CHART[/]")

    def _render(self) -> Panel:
        """Render the full dashboard."""
        layout = Layout()

        # Build sections
        header = self._render_header()
        chart = self._render_chart()
        prices = self._render_prices()
        agents = self._render_agents()
        trades = self._render_trades()

        # Combine into layout
        content = Group(header, chart, prices, agents, trades)

        return Panel(
            content,
            title=f"[bold orange1]CLIFF[/] - {self.market_name}",
            border_style="orange1",
        )

    def _render_header(self) -> Panel:
        """Render the header section with P&L."""
        elapsed = datetime.now() - self.start_time
        elapsed_str = f"{int(elapsed.total_seconds() // 60):02d}:{int(elapsed.total_seconds() % 60):02d}"

        header_text = Text()
        header_text.append(f"Iteration: {self.iteration}", style="bold orange1")
        header_text.append(" | ")
        header_text.append(f"Trades: {self.total_trades}")
        header_text.append(" | ")
        header_text.append(f"Agents: {len(self.agents)}")
        header_text.append(" | ")
        header_text.append(f"Time: {elapsed_str}")

        # P&L display
        header_text.append(" | P&L: ")
        pnl_style = "green" if self.all_time_pnl >= 0 else "red"
        header_text.append(f"{self.all_time_pnl:+.1%}", style=pnl_style)
        header_text.append(" all-time", style="dim")
        header_text.append(" | ")
        turn_style = "green" if self.turn_pnl >= 0 else "red"
        header_text.append(f"{self.turn_pnl:+.1%}", style=turn_style)
        header_text.append(" this turn", style="dim")

        return Panel(header_text, style="dim")

    def _render_prices(self) -> Panel:
        """Render the prices section."""
        if not self.prices:
            return Panel("[dim]No price data yet[/]", title="Prices")

        table = Table(box=None, expand=True, show_header=False, padding=(0, 1))
        table.add_column("Outcome", style="bold")
        table.add_column("Price", justify="right")
        table.add_column("Bar", width=12)
        table.add_column("Change", justify="right", width=8)

        for outcome, price in sorted(self.prices.items(), key=lambda x: -x[1]):
            change = self.price_changes.get(outcome, 0)
            change_style = "green" if change > 0 else "red" if change < 0 else "dim"

            # Price bar
            bar_len = int(price * 10)
            bar = Text("=" * bar_len + " " * (10 - bar_len), style="orange1")

            # Change text
            change_text = f"{change:+.1%}" if change else ""

            table.add_row(
                outcome[:20],
                f"${price:.2f}",
                bar,
                Text(change_text, style=change_style),
            )

        return Panel(table, title="[bold orange1]PRICES[/]")

    def _render_agents(self) -> Group:
        """Render agent panels."""
        panels = []

        for agent_id, data in self.agents.items():
            color = self._get_agent_color(agent_id)
            status = data.get("status", "idle").upper()
            activity = data.get("activity", "")[:60]
            trades = data.get("trades", 0)
            pnl = data.get("pnl", 0)

            content = Text()
            content.append(f"[{status}] ", style=f"bold {color}")
            content.append(activity)
            content.append(f"\nTrades: {trades}", style="dim")
            if pnl != 0:
                pnl_style = "green" if pnl > 0 else "red"
                content.append(f" | P&L: ", style="dim")
                content.append(f"${pnl:+.2f}", style=pnl_style)

            panels.append(Panel(content, title=f"[{color}]{agent_id}[/]", border_style=color))

        return Group(*panels) if panels else Panel("[dim]No agents running[/]", title="Agents")

    def _render_trades(self) -> Panel:
        """Render the trade log with investment memos."""
        if not self.trades:
            return Panel("[dim]No trades yet[/]", title="[bold orange1]TRADE LOG[/]")

        lines = []
        for trade in reversed(self.trades[-5:]):
            action = trade["action"].upper()
            action_style = "green" if action == "BUY" else "red"

            # Main trade line
            line = Text()
            line.append(f"{trade['time']} ", style="dim")
            line.append(f"{trade['agent_id'][:12]} ", style="bold")
            line.append(f"{action} ", style=action_style)
            line.append(f"{trade['outcome'][:15]} ", style="white")
            line.append(f"${trade['size']:.0f} ", style="cyan")
            line.append(f"@ ${trade['price']:.4f}", style="dim")
            lines.append(line)

            # Memo line (if present) - show full memo with word wrapping
            rationale = trade.get("rationale", "")
            if rationale:
                memo = Text()
                memo.append("       ", style="dim")  # indent
                memo.append(f'"{rationale}"', style="italic dim")
                lines.append(memo)

        content = Group(*lines)
        return Panel(content, title="[bold orange1]TRADE LOG[/]")

    def print_summary(self, summary: Dict[str, Any]) -> None:
        """Print final simulation summary."""
        self.console.print("\n" + "=" * 60)
        status = summary.get("status", "complete")
        if status == "cancelled":
            self.console.print("[bold yellow]SIMULATION CANCELLED[/]")
        else:
            self.console.print("[bold orange1]SIMULATION COMPLETE[/]")
        self.console.print("=" * 60)

        # Final prices
        if self.prices:
            self.console.print("\n[bold]Final Prices:[/]")
            for outcome, price in sorted(self.prices.items(), key=lambda x: -x[1]):
                implied_pct = price * 100
                self.console.print(f"  {outcome}: ${price:.4f} ({implied_pct:.1f}%)")

        # Trade summary
        self.console.print(f"\n[bold]Total Trades:[/] {self.total_trades}")
        self.console.print(f"[bold]Iterations:[/] {self.iteration}")

        elapsed = datetime.now() - self.start_time
        self.console.print(f"[bold]Duration:[/] {int(elapsed.total_seconds())} seconds")
