"""
Rich terminal display for real-time streaming output.

Uses Rich library for beautiful, live-updating terminal UI.
"""

from __future__ import annotations

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
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.trades: List[Dict[str, Any]] = []
        self.alerts: List[str] = []
        self.iteration = 0
        self.total_trades = 0
        self.start_time = datetime.now()

        # Agent colors (orange1 as primary brand color)
        self._colors = ["orange1", "magenta", "yellow", "green", "cyan", "red"]
        self._agent_colors: Dict[str, str] = {}

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

        self.prices = new_prices
        self.price_changes = changes

    def _render(self) -> Panel:
        """Render the full dashboard."""
        layout = Layout()

        # Build sections
        header = self._render_header()
        prices = self._render_prices()
        agents = self._render_agents()
        trades = self._render_trades()

        # Combine into layout
        content = Group(header, prices, agents, trades)

        return Panel(
            content,
            title=f"[bold orange1]CLIFF[/] - {self.market_name}",
            border_style="orange1",
        )

    def _render_header(self) -> Panel:
        """Render the header section."""
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
        """Render the trades table."""
        if not self.trades:
            return Panel("[dim]No trades yet[/]", title="Recent Trades")

        table = Table(box=None, expand=True)
        table.add_column("Time", style="dim", width=8)
        table.add_column("Agent", width=15)
        table.add_column("Action", width=5)
        table.add_column("Outcome", width=20)
        table.add_column("Size", justify="right", width=8)
        table.add_column("Price", justify="right", width=8)
        table.add_column("Slip", justify="right", width=6)

        for trade in reversed(self.trades[-5:]):
            action = trade["action"].upper()
            action_style = "green" if action == "BUY" else "red"

            table.add_row(
                trade["time"],
                trade["agent_id"][:15],
                Text(action, style=action_style),
                trade["outcome"][:20],
                f"${trade['size']:.0f}",
                f"${trade['price']:.4f}",
                f"{trade['slippage']:.1%}" if trade['slippage'] else "",
            )

        return Panel(table, title="[bold orange1]RECENT TRADES[/]")

    def print_summary(self, summary: Dict[str, Any]) -> None:
        """Print final simulation summary."""
        self.console.print("\n" + "=" * 60)
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
