"""
Unified Rich terminal display for real-time streaming output.

Three-pane interactive UI with keyboard controls:
- Left: Market selector
- Center: Live market data (chart, agents, trades)
- Right: Sources, MCP servers, commands
"""

from __future__ import annotations

import asyncio
import os
import select
import sys
import termios
import tty
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .events import EventType, StreamEvent

# Agent personas for display (name -> short persona description)
AGENT_PERSONAS = {
    "Marcus": "Quant, analytical",
    "Luna": "PoliSci, contrarian",
    "Atlas": "Econ, conservative",
}

if TYPE_CHECKING:
    from cliff.simulation.controller import SimulationController


class UnifiedDisplay:
    """
    Three-pane Rich terminal UI with keyboard controls.

    Layout:
    ┌─────────────────────────────────────────────────────────┐
    │                        HEADER                            │
    ├────────────┬────────────────────────┬───────────────────┤
    │  MARKETS   │       DASHBOARD        │     CONTROLS      │
    │            │                        │                   │
    │ > Market 1 │  Price Chart (Braille) │  [S]ources        │
    │   Market 2 │  Agents                │  [M]CP Servers    │
    │            │  Trade Log             │  [C]ommands       │
    ├────────────┴────────────────────────┴───────────────────┤
    │ Tab: switch | ↑↓: navigate | i: inject | p: pause | q: quit │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        controller: Optional["SimulationController"] = None,
        console: Optional[Console] = None,
        verbosity: int = 1,
        market_name: str = "Trading Simulation",
    ):
        self.controller = controller
        self.console = console or Console()
        self.verbosity = verbosity
        self.market_name = market_name
        self._live: Optional[Live] = None
        self._running = False
        self._input_task: Optional[asyncio.Task] = None

        # UI State
        self.focused_pane = "left"  # left, center, right
        self.selected_market_idx = 0
        self.selected_control_idx = 0  # 0=sources, 1=mcp, 2=commands
        self.input_mode = False
        self.input_buffer = ""
        self.input_prompt = ""
        self.input_type = ""  # "inject", "new_market", "market_desc", "market_outcomes", "add_source"

        # Multi-step market creation state
        self._pending_market: Dict[str, Any] = {}

        # Market State
        self.markets: Dict[str, Dict[str, Any]] = {}
        self.selected_market_id: Optional[str] = None

        # Price/Trading State (per market, keyed by market_id)
        self.prices: Dict[str, float] = {}
        self.price_changes: Dict[str, float] = {}
        self.price_history: Dict[str, List[float]] = {}
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.trades: List[Dict[str, Any]] = []

        # Simulation State
        self.iteration = 0
        self.total_trades = 0
        self.trade_counter = 0  # Incremental trade numbering for display
        self.start_time = datetime.now()
        self.paused = False

        # P&L tracking
        self.initial_capital = 10000.0
        self.current_value = 10000.0
        self.all_time_pnl = 0.0

        # Sources (research data sources)
        self.sources: List[Dict[str, Any]] = []

        # MCP Servers
        self.mcp_servers: List[Dict[str, Any]] = []
        self._load_mcp_servers()

        # Agent colors
        self._colors = ["orange1", "magenta", "yellow", "green", "cyan", "red"]
        self._agent_colors: Dict[str, str] = {}

        # Throttle display updates
        self._last_update = 0.0
        self._update_interval = 0.1

        # Callbacks for actions
        self._on_inject_news: Optional[Callable[[str], None]] = None
        self._on_pause: Optional[Callable[[], None]] = None
        self._on_quit: Optional[Callable[[], None]] = None
        self._on_market_created: Optional[Callable[[Dict[str, Any]], None]] = None
        self._on_source_added: Optional[Callable[[Dict[str, Any]], None]] = None

    def _load_mcp_servers(self) -> None:
        """Load MCP server list for display."""
        try:
            from cliff.integrations.mcp import get_all_servers
            all_servers = get_all_servers()

            # Flatten into list for display
            for server_type, servers in all_servers.items():
                for name, spec in servers.items():
                    self.mcp_servers.append({
                        "name": name,
                        "type": server_type,
                        "description": spec.get("description", ""),
                        "enabled": server_type == "builtin",  # Builtin always enabled
                    })
        except ImportError:
            pass

    def _get_agent_color(self, agent_id: str) -> str:
        """Get consistent color for an agent."""
        if agent_id not in self._agent_colors:
            idx = len(self._agent_colors) % len(self._colors)
            self._agent_colors[agent_id] = self._colors[idx]
        return self._agent_colors[agent_id]

    def set_callbacks(
        self,
        on_inject_news: Optional[Callable[[str], None]] = None,
        on_pause: Optional[Callable[[], None]] = None,
        on_quit: Optional[Callable[[], None]] = None,
        on_market_created: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_source_added: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        """Set callback functions for UI actions."""
        self._on_inject_news = on_inject_news
        self._on_pause = on_pause
        self._on_quit = on_quit
        self._on_market_created = on_market_created
        self._on_source_added = on_source_added

    def start(self) -> None:
        """Start the live display."""
        if self.verbosity == 0:
            return

        self._running = True
        # Use screen=False to avoid conflicts with keyboard input
        self._live = Live(
            self._render(),
            console=self.console,
            refresh_per_second=4,
            screen=False,
            transient=False,
        )
        self._live.start()

        # Start keyboard input handler
        self._input_task = asyncio.create_task(self._input_loop())

        # Start periodic refresh task to keep time updating
        self._refresh_task = asyncio.create_task(self._periodic_refresh())

    def stop(self) -> None:
        """Stop the live display."""
        self._running = False
        if self._input_task:
            self._input_task.cancel()
        if hasattr(self, '_refresh_task') and self._refresh_task:
            self._refresh_task.cancel()
        if self._live:
            self._live.stop()
            self._live = None

    async def _periodic_refresh(self) -> None:
        """Periodically refresh the display to keep time updating."""
        try:
            while self._running:
                await asyncio.sleep(1.0)  # Refresh every second
                self.update()
        except asyncio.CancelledError:
            pass

    def update(self) -> None:
        """Refresh the display."""
        if self._live:
            self._live.update(self._render())

    # -------------------------------------------------------------------------
    # Keyboard Input
    # -------------------------------------------------------------------------
    async def _input_loop(self) -> None:
        """Async keyboard input handling without blocking Rich Live rendering."""
        if not sys.stdin.isatty():
            return

        import threading
        import queue

        key_queue: queue.Queue = queue.Queue()
        stop_event = threading.Event()

        def read_keys():
            """Thread function to read keys in raw mode."""
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                # Use cbreak mode instead of raw mode - allows Rich to render
                tty.setcbreak(fd)
                while not stop_event.is_set():
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1)
                        key_queue.put(key)
            except Exception:
                pass
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # Start key reader thread
        key_thread = threading.Thread(target=read_keys, daemon=True)
        key_thread.start()

        try:
            while self._running:
                try:
                    # Non-blocking check for keys
                    key = key_queue.get_nowait()
                    await self._handle_key(key)
                except queue.Empty:
                    await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            pass
        finally:
            stop_event.set()
            key_thread.join(timeout=0.5)

    async def _handle_key(self, key: str) -> None:
        """Handle a single keypress."""
        # Input mode - typing text
        if self.input_mode:
            if key == "\x1b":  # Escape - cancel current input
                self.input_mode = False
                self.input_buffer = ""
                self._pending_market = {}  # Clear any pending market creation
            elif key in ("\r", "\n"):  # Enter (handle both carriage return and newline)
                await self._submit_input()
            elif key == "\x7f":  # Backspace
                self.input_buffer = self.input_buffer[:-1]
            elif key.isprintable():
                self.input_buffer += key
            self.update()
            return

        # Navigation keys
        if key == "\t":  # Tab
            panes = ["left", "center", "right"]
            idx = panes.index(self.focused_pane)
            self.focused_pane = panes[(idx + 1) % 3]
        elif key == "\x1b":  # Escape sequence (arrow keys)
            # Read the rest of the escape sequence
            if select.select([sys.stdin], [], [], 0.1)[0]:
                seq = sys.stdin.read(2)
                if seq == "[A":  # Up arrow
                    await self._navigate_up()
                elif seq == "[B":  # Down arrow
                    await self._navigate_down()

        # Action keys
        elif key == "i":  # Inject news
            self.input_mode = True
            self.input_type = "inject"
            self.input_prompt = "Inject scenario: "
            self.input_buffer = ""
        elif key == "n":  # New market
            self.input_mode = True
            self.input_type = "new_market"
            self.input_prompt = "New market question: "
            self.input_buffer = ""
        elif key == "a":  # Add source
            self.input_mode = True
            self.input_type = "add_source"
            self.input_prompt = "Add source URL: "
            self.input_buffer = ""
        elif key == "p":  # Pause/Resume
            if self.controller and hasattr(self.controller, 'toggle_pause'):
                self.paused = self.controller.toggle_pause()
            else:
                self.paused = not self.paused
            if self._on_pause:
                self._on_pause()
        elif key == "q":  # Quit
            if self._on_quit:
                self._on_quit()
            self._running = False
        elif key == "s":  # Focus sources
            self.focused_pane = "right"
            self.selected_control_idx = 0
        elif key == "m":  # Focus MCP
            self.focused_pane = "right"
            self.selected_control_idx = 1
        elif key == "c":  # Focus commands (Quick Actions)
            self.focused_pane = "right"
            self.selected_control_idx = 2

        self.update()

    async def _navigate_up(self) -> None:
        """Navigate up within current pane."""
        if self.focused_pane == "left":
            if self.selected_market_idx > 0:
                self.selected_market_idx -= 1
                market_ids = list(self.markets.keys())
                if market_ids:
                    self.selected_market_id = market_ids[self.selected_market_idx]
        elif self.focused_pane == "right":
            if self.selected_control_idx > 0:
                self.selected_control_idx -= 1

    async def _navigate_down(self) -> None:
        """Navigate down within current pane."""
        if self.focused_pane == "left":
            market_ids = list(self.markets.keys())
            if self.selected_market_idx < len(market_ids) - 1:
                self.selected_market_idx += 1
                self.selected_market_id = market_ids[self.selected_market_idx]
        elif self.focused_pane == "right":
            if self.selected_control_idx < 2:
                self.selected_control_idx += 1

    async def _submit_input(self) -> None:
        """Submit the current input buffer based on input type."""
        text = self.input_buffer.strip()

        if self.input_type == "inject":
            if text and self._on_inject_news:
                self._on_inject_news(text)
            self.input_mode = False
            self.input_buffer = ""

        elif self.input_type == "new_market":
            # Step 1: Market question (required)
            if not text:
                return  # Don't proceed without a question
            self._pending_market = {"question": text}
            # Move to step 2: description (optional)
            self.input_type = "market_desc"
            self.input_prompt = "Description (optional, Enter to skip): "
            self.input_buffer = ""

        elif self.input_type == "market_desc":
            # Step 2: Description (optional - empty is OK)
            self._pending_market["description"] = text if text else None
            # Move to step 3: outcomes (required)
            self.input_type = "market_outcomes"
            self.input_prompt = "Outcomes (comma-separated, min 2, e.g. 'YES, NO'): "
            self.input_buffer = ""

        elif self.input_type == "market_outcomes":
            # Step 3: Outcomes (required, minimum 2)
            if not text:
                # Default to YES, NO if empty
                outcomes = ["YES", "NO"]
            else:
                # Parse comma-separated outcomes
                outcomes = [o.strip() for o in text.split(",") if o.strip()]

            if len(outcomes) < 2:
                # Not enough outcomes - prompt again
                self.input_prompt = "Need at least 2 outcomes (e.g. 'YES, NO'): "
                self.input_buffer = ""
                return

            # Create the market
            import uuid
            market_id = f"user-{uuid.uuid4().hex[:8]}"
            market_data = {
                "id": market_id,
                "name": self._pending_market.get("question", "New Market")[:40],
                "question": self._pending_market.get("question", "New Market"),
                "description": self._pending_market.get("description"),
                "status": "pending",
                "outcomes": outcomes,
            }
            self.markets[market_id] = market_data
            self.selected_market_id = market_id
            self.selected_market_idx = len(self.markets) - 1

            # Trigger callback to actually create the market/run simulation
            if self._on_market_created:
                self._on_market_created(market_data)

            # Clear state and exit input mode
            self._pending_market = {}
            self.input_mode = False
            self.input_buffer = ""

        elif self.input_type == "add_source":
            if text:
                # Add a new data source
                source_data = {
                    "name": text[:30] if not text.startswith("http") else text.split("/")[-1][:20],
                    "url": text,
                    "enabled": True,
                }
                self.sources.append(source_data)

                # Trigger callback to persist source
                if self._on_source_added:
                    self._on_source_added(source_data)
            self.input_mode = False
            self.input_buffer = ""

        else:
            # Unknown input type - just exit
            self.input_mode = False
            self.input_buffer = ""

    # -------------------------------------------------------------------------
    # Event Handling
    # -------------------------------------------------------------------------
    def handle_event(self, event: StreamEvent) -> None:
        """Handle a stream event and update the display."""
        if self.verbosity == 0:
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
                text = event.data.get("text", "")[:60]
                self.agents[event.agent_id]["status"] = "thinking"
                self.agents[event.agent_id]["activity"] = text

        elif event.event_type == EventType.AGENT_RESEARCHING:
            if event.agent_id in self.agents:
                query = event.data.get("query", "")[:50]
                self.agents[event.agent_id]["status"] = "researching"
                self.agents[event.agent_id]["activity"] = f'"{query}"'

        elif event.event_type == EventType.TRADE_EXECUTED:
            self._handle_trade(event)

        elif event.event_type == EventType.PRICE_UPDATE:
            self._handle_price_update(event)

        elif event.event_type == EventType.AGENT_COMPLETED:
            if event.agent_id in self.agents:
                self.agents[event.agent_id]["status"] = "done"
                decision = event.data.get("decision", "hold")
                self.agents[event.agent_id]["activity"] = f"Decided: {decision}"

        elif event.event_type == EventType.ITERATION_END:
            self.iteration = event.data.get("iteration", self.iteration)
            self.total_trades = event.data.get("trades", self.total_trades)

        elif event.event_type == EventType.PORTFOLIO_UPDATE:
            self.current_value = event.data.get("total_value", self.current_value)
            if self.initial_capital > 0:
                self.all_time_pnl = (self.current_value - self.initial_capital) / self.initial_capital

            agent_id = event.agent_id
            if agent_id and agent_id in self.agents:
                self.agents[agent_id]["cash"] = event.data.get("cash", 0)
                self.agents[agent_id]["pnl"] = event.data.get("pnl", 0)

        elif event.event_type == EventType.MARKET_CREATED:
            market_id = event.data.get("market_id", "default")
            self.markets[market_id] = {
                "name": event.data.get("name", "Market"),
                "status": "running",
                "outcomes": event.data.get("outcomes", []),
            }
            if not self.selected_market_id:
                self.selected_market_id = market_id

        # Throttled update
        import time
        now = time.monotonic()
        if now - self._last_update >= self._update_interval:
            self._last_update = now
            self.update()

    def _handle_minimal(self, event: StreamEvent) -> None:
        """Handle event in minimal mode."""
        if event.event_type == EventType.TRADE_EXECUTED:
            data = event.data
            action = data.get("action", "").upper()
            style = "green" if action == "BUY" else "red"
            self.console.print(
                f"[dim][{datetime.now().strftime('%H:%M:%S')}][/] "
                f"{event.agent_id} [{style}]{action}[/] "
                f"{data.get('outcome')} ${data.get('size', 0):.0f} @ {data.get('price', 0)*100:.1f}%"
            )

    def _handle_trade(self, event: StreamEvent) -> None:
        """Process a trade event."""
        data = event.data
        self.trade_counter += 1
        trade = {
            "number": self.trade_counter,
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent_id": event.agent_id,
            "action": data.get("action", ""),
            "outcome": data.get("outcome", ""),
            "size": data.get("size", 0),
            "price": data.get("price", 0),
            "rationale": data.get("rationale", "") or data.get("note", ""),
        }
        self.trades.append(trade)
        self.trades = self.trades[-20:]  # Keep last 20 trades for table display

        if event.agent_id in self.agents:
            self.agents[event.agent_id]["trades"] = self.agents[event.agent_id].get("trades", 0) + 1
            self.agents[event.agent_id]["status"] = "traded"
            action = data.get("action", "").upper()
            price = data.get('price', 0)
            price_str = f"${price:,.0f}" if price >= 1 else f"${price:.4f}"
            self.agents[event.agent_id]["activity"] = f"{action} {data.get('outcome')} @ {price_str}"

    def _handle_price_update(self, event: StreamEvent) -> None:
        """Process a price update event."""
        new_prices = event.data.get("prices", {})
        changes = event.data.get("changes", {})

        if not changes and self.prices:
            for outcome, price in new_prices.items():
                if outcome in self.prices and self.prices[outcome] > 0:
                    change = (price - self.prices[outcome]) / self.prices[outcome]
                    changes[outcome] = change

        for outcome, price in new_prices.items():
            if outcome not in self.price_history:
                self.price_history[outcome] = []
            self.price_history[outcome].append(price)
            if len(self.price_history[outcome]) > 60:
                self.price_history[outcome] = self.price_history[outcome][-60:]

        self.prices = new_prices
        self.price_changes = changes

    # -------------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------------
    def _pane_style(self, pane: str) -> str:
        """Get border style for a pane based on focus."""
        return "orange1 bold" if self.focused_pane == pane else "dim"

    def _render(self) -> Layout:
        """Render the full three-pane layout."""
        layout = Layout()

        # Split into header, body, footer
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=1),
        )

        # Split body into three panes
        layout["body"].split_row(
            Layout(name="left", size=22),
            Layout(name="center"),
            Layout(name="right", size=30),
        )

        # Render each section
        layout["header"].update(self._render_header())
        layout["left"].update(self._render_markets_pane())
        layout["center"].update(self._render_dashboard())
        layout["right"].update(self._render_controls_pane())
        layout["footer"].update(self._render_footer())

        return layout

    def _render_header(self) -> Panel:
        """Render the header with status info."""
        elapsed = datetime.now() - self.start_time
        elapsed_str = f"{int(elapsed.total_seconds() // 60):02d}:{int(elapsed.total_seconds() % 60):02d}"

        header = Text()
        header.append("CLIFF", style="bold orange1")
        header.append(f" - {self.market_name}", style="white")
        header.append(" | ")
        header.append(f"Iter: {self.iteration}", style="cyan")
        header.append(" | ")
        header.append(f"Trades: {self.total_trades}", style="green")
        header.append(" | ")
        header.append(f"Time: {elapsed_str}", style="dim")
        header.append(" | ")

        status = "PAUSED" if self.paused else "RUNNING"
        status_style = "yellow bold" if self.paused else "green"
        header.append(status, style=status_style)

        header.append(" | P&L: ")
        pnl_style = "green" if self.all_time_pnl >= 0 else "red"
        header.append(f"{self.all_time_pnl:+.1%}", style=pnl_style)

        return Panel(header, border_style="orange1")

    def _render_footer(self) -> Text:
        """Render the footer with key hints."""
        if self.input_mode:
            footer = Text()

            # Show step indicator for multi-step market creation
            if self.input_type == "new_market":
                footer.append("[1/3] ", style="cyan bold")
            elif self.input_type == "market_desc":
                footer.append("[2/3] ", style="cyan bold")
            elif self.input_type == "market_outcomes":
                footer.append("[3/3] ", style="cyan bold")

            footer.append(self.input_prompt, style="cyan")
            footer.append(self.input_buffer)
            footer.append("█", style="blink")
            footer.append("  ", style="dim")
            footer.append("Esc", style="yellow")
            footer.append(" cancel  ", style="dim")
            footer.append("Enter", style="green")

            # Custom action hint based on step
            if self.input_type == "market_desc":
                footer.append(" skip/submit", style="dim")
            elif self.input_type == "market_outcomes":
                footer.append(" create market", style="dim")
            else:
                footer.append(" submit", style="dim")
            return footer

        footer = Text()
        footer.append(" ", style="dim")
        footer.append("i", style="cyan bold")
        footer.append(" inject  ", style="dim")
        footer.append("n", style="cyan bold")
        footer.append(" new market  ", style="dim")
        footer.append("p", style="cyan bold")
        footer.append(" pause  ", style="dim")
        footer.append("q", style="cyan bold")
        footer.append(" quit  ", style="dim")
        footer.append("↑↓", style="cyan bold")
        footer.append(" navigate  ", style="dim")
        footer.append("Tab", style="cyan bold")
        footer.append(" switch pane", style="dim")
        return footer

    def _render_markets_pane(self) -> Panel:
        """Render the left pane with market selector."""
        content = Text()

        if not self.markets:
            # Show current market if no multi-market mode
            content.append("> ", style="orange1 bold")
            content.append(f"{self.market_name[:18]}\n", style="white bold")
            content.append("  Status: ", style="dim")
            status = "PAUSED" if self.paused else "RUNNING"
            content.append(status, style="yellow" if self.paused else "green")
        else:
            market_ids = list(self.markets.keys())
            for idx, market_id in enumerate(market_ids):
                market = self.markets[market_id]
                selected = idx == self.selected_market_idx
                prefix = "> " if selected else "  "
                style = "orange1 bold" if selected else "white"

                status = market.get("status", "running")
                status_icons = {
                    "running": ("●", "green"),
                    "paused": ("⏸", "yellow"),
                    "completed": ("✓", "green"),
                }
                icon, icon_style = status_icons.get(status, ("○", "dim"))

                content.append(prefix, style=style)
                content.append(f"{icon} ", style=icon_style)
                content.append(f"{market['name'][:15]}\n", style=style)

        return Panel(
            content,
            title="[bold]MARKETS[/]",
            border_style=self._pane_style("left"),
        )

    def _render_dashboard(self) -> Panel:
        """Render the center pane with chart, agents, trades."""
        sections = []

        # Price chart
        sections.append(self._render_chart())

        # Agents
        sections.append(self._render_agents())

        # Trade log
        sections.append(self._render_trades())

        return Panel(
            Group(*sections),
            title="[bold]DASHBOARD[/]",
            border_style=self._pane_style("center"),
        )

    def _render_chart(self, width: int = 45, height: int = 5) -> Panel:
        """Render braille price chart."""
        if not self.price_history or not any(self.price_history.values()):
            return Panel("[dim]Waiting for price data...[/]", title="[orange1]PRICES[/]")

        chart_colors = ["orange1", "cyan", "magenta", "yellow", "green", "red"]
        sorted_outcomes = sorted(self.price_history.keys())
        outcome_colors = {}
        for i, outcome in enumerate(sorted_outcomes):
            outcome_colors[outcome] = chart_colors[i % len(chart_colors)]

        max_points = max(len(h) for h in self.price_history.values())
        if max_points < 2:
            return Panel("[dim]Collecting data...[/]", title="[orange1]PRICES[/]")

        BRAILLE_BASE = 0x2800
        DOT_MAP = [
            [0x01, 0x08],
            [0x02, 0x10],
            [0x04, 0x20],
            [0x40, 0x80],
        ]

        char_width = width
        char_height = height
        y_min, y_max = 0.0, 1.0

        outcome_grids: Dict[str, List[List[int]]] = {}
        for outcome in sorted_outcomes:
            outcome_grids[outcome] = [[0 for _ in range(char_width)] for _ in range(char_height)]

        def _plot_line(grid, x1, y1, x2, y2):
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
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

            prev_x, prev_y = None, None
            for x, price in enumerate(resampled):
                y_norm = (price - y_min) / (y_max - y_min)
                y_norm = max(0, min(1, y_norm))
                y_dot = int((1 - y_norm) * (char_height * 4 - 1))
                y_dot = max(0, min(char_height * 4 - 1, y_dot))

                if prev_x is not None and prev_y is not None:
                    _plot_line(grid, prev_x, prev_y, x, y_dot)
                else:
                    char_x = x // 2
                    char_y = y_dot // 4
                    dot_col = x % 2
                    dot_row = y_dot % 4
                    if 0 <= char_x < char_width and 0 <= char_y < char_height:
                        grid[char_y][char_x] |= DOT_MAP[dot_row][dot_col]

                prev_x, prev_y = x, y_dot

        lines = []
        for row_idx in range(char_height):
            line = Text()
            if row_idx == 0:
                line.append("100│", style="dim")
            elif row_idx == char_height // 2:
                line.append(" 50│", style="dim")
            elif row_idx == char_height - 1:
                line.append("  0│", style="dim")
            else:
                line.append("   │", style="dim")

            for col_idx in range(char_width):
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
                    outcome, char_val = outcomes_in_cell[0]
                    line.append(chr(BRAILLE_BASE + char_val), style=f"bold {outcome_colors[outcome]}")
                else:
                    line.append(chr(BRAILLE_BASE + combined_val), style="bold white")

            lines.append(line)

        x_axis = Text("   └" + "─" * char_width, style="dim")
        lines.append(x_axis)

        legend = Text("    ")
        for outcome in sorted_outcomes:
            color = outcome_colors[outcome]
            price = self.prices.get(outcome, 0)
            short_name = outcome[:10]
            legend.append("● ", style=color)
            legend.append(f"{short_name} {price*100:.0f}%  ", style=color)
        lines.append(legend)

        return Panel(Group(*lines), title="[orange1]PRICES[/]", padding=(0, 1))

    def _render_agents(self) -> Panel:
        """Render agent status cards."""
        if not self.agents:
            return Panel("[dim]No agents running[/]", title="[orange1]AGENTS[/]")

        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), expand=True)
        table.add_column("Agent", style="bold", width=12)
        table.add_column("Status", width=12)
        table.add_column("Activity", no_wrap=True)

        status_icons = {
            "thinking": ("●", "cyan"),
            "researching": ("◎", "yellow"),
            "traded": ("◉", "green"),
            "done": ("✓", "green"),
            "starting": ("○", "dim"),
            "idle": ("○", "dim"),
        }

        for agent_id, data in self.agents.items():
            color = self._get_agent_color(agent_id)
            status = data.get("status", "idle")
            icon, icon_style = status_icons.get(status, ("○", "dim"))
            activity = data.get("activity", "")[:30]
            pnl = data.get("pnl", 0)

            # Build status cell with proper styling
            status_text = Text()
            status_text.append(f"{icon} ", style=icon_style)
            status_text.append(status[:8])

            # Build activity cell with optional P&L
            activity_text = Text(activity)
            if pnl != 0:
                pnl_style = "green" if pnl > 0 else "red"
                activity_text.append(f" ${pnl:+.0f}", style=pnl_style)

            table.add_row(
                Text(agent_id[:11], style=color),
                status_text,
                activity_text,
            )

        return Panel(table, title="[orange1]AGENTS[/]", padding=(0, 0))

    def _render_trades(self) -> Panel:
        """Render the trade log as a Rich Table."""
        if not self.trades:
            return Panel("[dim]No trades yet[/]", title="[orange1]TRADE LOG[/]")

        # Create table with columns: #, Time, Outcome, Action, Size, Price, Memo, Agent
        table = Table(
            box=box.SIMPLE,
            show_header=True,
            header_style="bold dim",
            padding=(0, 1),
            expand=True,
        )
        table.add_column("#", style="dim", width=3, justify="right")
        table.add_column("Time", style="dim", width=8)
        table.add_column("Outcome", width=14)
        table.add_column("Act", width=4)
        table.add_column("Size", width=7, justify="right")
        table.add_column("Price", style="cyan", width=6, justify="right")
        table.add_column("Investment Memo", ratio=1, overflow="ellipsis")
        table.add_column("Agent", width=18)

        # Show last 8 trades (most recent first, oldest at bottom)
        for trade in reversed(self.trades[-8:]):
            action = trade["action"].upper()
            action_style = "green" if action == "BUY" else "red"

            # Format price as percentage
            price = trade.get("price", 0)
            price_str = f"{price*100:.1f}%" if price < 1 else f"${price:,.0f}"

            # Format size
            size = trade.get("size", 0)
            size_str = f"${size:,.0f}"

            # Truncate memo for display
            memo = trade.get("rationale", "")[:60]
            if len(trade.get("rationale", "")) > 60:
                memo += "..."

            # Agent name with persona
            agent_id = trade.get("agent_id", "")
            persona = AGENT_PERSONAS.get(agent_id, "")
            agent_display = f"{agent_id}"
            if persona:
                agent_display += f" [dim]({persona})[/]"

            table.add_row(
                str(trade.get("number", "")),
                trade.get("time", ""),
                trade.get("outcome", "")[:14],
                Text(action, style=action_style),
                size_str,
                price_str,
                Text(memo, style="italic dim"),
                agent_display,
            )

        return Panel(table, title="[orange1]TRADE LOG[/]", padding=(0, 0))

    def _render_controls_pane(self) -> Panel:
        """Render the right pane with sources, MCP, commands."""
        sections = []

        # Sources section
        is_selected = self.focused_pane == "right" and self.selected_control_idx == 0
        src_title_style = "orange1 bold" if is_selected else "white"
        sources_content = Text()
        sources_content.append("Sources", style=src_title_style)
        sources_content.append("  ")
        sources_content.append("s", style="cyan dim")
        sources_content.append(" to focus\n", style="dim")
        if self.sources:
            for src in self.sources[:3]:
                icon = "●" if src.get("enabled") else "○"
                icon_style = "green" if src.get("enabled") else "dim"
                sources_content.append(f"  {icon} ", style=icon_style)
                sources_content.append(f"{src.get('name', 'source')[:16]}\n")
        else:
            sources_content.append("  ", style="dim")
            sources_content.append("a", style="cyan")
            sources_content.append(" to add source\n", style="dim")
        sections.append(Panel(sources_content, box=box.SIMPLE))

        # MCP section
        is_selected = self.focused_pane == "right" and self.selected_control_idx == 1
        mcp_title_style = "orange1 bold" if is_selected else "white"
        mcp_content = Text()
        mcp_content.append("MCP Servers", style=mcp_title_style)
        mcp_content.append("  ")
        mcp_content.append("m", style="cyan dim")
        mcp_content.append(" to focus\n", style="dim")
        enabled_servers = [s for s in self.mcp_servers if s.get("enabled")]
        disabled_servers = [s for s in self.mcp_servers if not s.get("enabled")]
        for server in enabled_servers[:2]:
            mcp_content.append("  ● ", style="green")
            mcp_content.append(f"{server['name'][:16]}\n")
        for server in disabled_servers[:2]:
            mcp_content.append("  ○ ", style="dim")
            mcp_content.append(f"{server['name'][:16]}\n", style="dim")
        total_mcp = len(self.mcp_servers)
        shown = min(4, total_mcp)
        if total_mcp > shown:
            mcp_content.append(f"  +{total_mcp - shown} more ", style="dim")
            mcp_content.append("(Enter to view all)\n", style="dim")
        sections.append(Panel(mcp_content, box=box.SIMPLE))

        # Quick actions section
        is_selected = self.focused_pane == "right" and self.selected_control_idx == 2
        cmd_title_style = "orange1 bold" if is_selected else "white"
        cmd_content = Text()
        cmd_content.append("Quick Actions\n", style=cmd_title_style)
        cmd_content.append("  ")
        cmd_content.append("i", style="cyan bold")
        cmd_content.append(" Inject scenario\n", style="white")
        cmd_content.append("  ")
        cmd_content.append("p", style="cyan bold")
        cmd_content.append(" Pause/Resume\n", style="white")
        cmd_content.append("  ")
        cmd_content.append("q", style="cyan bold")
        cmd_content.append(" Quit simulation\n", style="white")
        sections.append(Panel(cmd_content, box=box.SIMPLE))

        return Panel(
            Group(*sections),
            title="[bold]CONTROLS[/]",
            border_style=self._pane_style("right"),
        )

    def print_summary(self, summary: Dict[str, Any]) -> None:
        """Print final simulation summary."""
        self.console.print("\n" + "=" * 60)
        status = summary.get("status", "complete")
        if status == "cancelled":
            self.console.print("[bold yellow]SIMULATION CANCELLED[/]")
        else:
            self.console.print("[bold orange1]SIMULATION COMPLETE[/]")
        self.console.print("=" * 60)

        if self.prices:
            self.console.print("\n[bold]Final Prices:[/]")
            for outcome, price in sorted(self.prices.items(), key=lambda x: -x[1]):
                implied_pct = price * 100
                self.console.print(f"  {outcome}: {implied_pct:.1f}%")

        self.console.print(f"\n[bold]Total Trades:[/] {self.total_trades}")
        self.console.print(f"[bold]Iterations:[/] {self.iteration}")

        elapsed = datetime.now() - self.start_time
        self.console.print(f"[bold]Duration:[/] {int(elapsed.total_seconds())} seconds")
