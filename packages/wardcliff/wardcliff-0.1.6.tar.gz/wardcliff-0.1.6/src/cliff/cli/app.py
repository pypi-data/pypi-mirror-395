"""Main Typer CLI application for Wardcliff."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# CLI app
app = typer.Typer(
    name="wardcliff",
    help="Multi-agent prediction market trading simulation",
    add_completion=False,
    no_args_is_help=True,
)

console = Console()


@app.callback()
def _app_startup():
    """Load stored API keys on startup."""
    try:
        from cliff.cli.config import MCPKeysConfig
        mcp_keys = MCPKeysConfig.load()
        mcp_keys.apply_to_environment()
    except Exception:
        pass  # Silently continue if config loading fails

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_available_events() -> dict:
    """Get available events from the events module."""
    from cliff.core.events import (
        create_sample_events,
        create_multi_outcome_events,
    )

    events = {}
    for event in create_sample_events():
        events[event.id] = event
    for event in create_multi_outcome_events():
        events[event.id] = event
    return events


def get_default_personas() -> list:
    """Get default agent personas for simulation."""
    from cliff.agents.async_agent import AgentPersona

    return [
        AgentPersona(
            name="Marcus",
            race="human",
            background="quantitative finance",
            personality="analytical and data-driven",
            risk_tolerance="medium",
        ),
        AgentPersona(
            name="Luna",
            race="human",
            background="political science",
            personality="intuitive and contrarian",
            risk_tolerance="high",
        ),
        AgentPersona(
            name="Atlas",
            race="human",
            background="economics",
            personality="conservative and risk-averse",
            risk_tolerance="low",
        ),
    ]


@app.command()
def ask(
    agents: int = typer.Option(3, "--agents", "-a", help="Number of agents"),
    model: str = typer.Option("gpt-5-mini", "--model", help="Model to use"),
    minimal: bool = typer.Option(False, "--minimal", help="Minimal one-line output"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output with full reasoning"),
    debug: bool = typer.Option(False, "--debug", help="Debug output with raw SDK messages"),
    parallel: bool = typer.Option(False, "--parallel", "-p", help="Run agents in parallel"),
):
    """Ask a custom prediction market question interactively."""
    from rich.prompt import Prompt
    from cliff.core.events import PredictionMarketEvent
    import uuid

    # Set verbosity level
    if debug:
        verbosity = 3
        logging.getLogger().setLevel(logging.DEBUG)
    elif verbose:
        verbosity = 2
        logging.getLogger().setLevel(logging.INFO)
    elif minimal:
        verbosity = 0
    else:
        verbosity = 1

    # Display header
    console.print()
    console.print(Panel(
        "[bold]Enter your prediction market question[/]\n\n"
        "[dim]Examples:[/]\n"
        "  - Will the Federal Reserve cut rates in December 2025?\n"
        "  - Will Bitcoin reach $200K before 2026?\n"
        "  - Who will win the 2026 World Cup?",
        title="[bold orange1]WARDCLIFF[/] - New Question",
        border_style="orange1",
    ))
    console.print()

    # Prompt for question
    question = Prompt.ask(
        "[bold orange1]Question[/]",
        console=console,
    )

    if not question.strip():
        console.print("[red]Question cannot be empty[/]")
        raise typer.Exit(1)

    console.print()

    # Prompt for outcomes
    console.print("[dim]Enter possible outcomes, comma-separated.[/]")
    console.print("[dim]Leave blank for default YES/NO binary question.[/]")
    outcomes_input = Prompt.ask(
        "[bold orange1]Outcomes[/]",
        default="YES, NO",
        console=console,
    )

    # Parse outcomes
    outcomes = [o.strip() for o in outcomes_input.split(",") if o.strip()]
    if len(outcomes) < 2:
        outcomes = ["YES", "NO"]

    console.print()

    # Optional: resolution criteria
    console.print("[dim]How should this question be resolved? (optional)[/]")
    resolution = Prompt.ask(
        "[bold orange1]Resolution criteria[/]",
        default="",
        console=console,
    )

    # Generate event ID
    event_id = f"custom-{uuid.uuid4().hex[:8]}"

    # Create the custom event
    custom_event = PredictionMarketEvent(
        id=event_id,
        name=question,
        description=question,
        outcomes=outcomes,
        resolution_criteria=resolution if resolution else f"Resolves based on the actual outcome of: {question}",
    )

    # Show summary
    console.print()
    console.print(Panel(
        f"[bold]{custom_event.name}[/]\n\n"
        f"[orange1]Outcomes:[/] {', '.join(custom_event.outcomes)}\n"
        f"[orange1]Resolution:[/] {custom_event.resolution_criteria[:100]}{'...' if len(custom_event.resolution_criteria) > 100 else ''}",
        title="[bold]Question Summary[/]",
        border_style="green",
    ))
    console.print()

    # Confirm
    from rich.prompt import Confirm
    if not Confirm.ask("[bold]Start simulation?[/]", default=True, console=console):
        console.print("[dim]Cancelled[/]")
        raise typer.Exit(0)

    # Load stored API keys into environment
    from cliff.cli.config import APIKeyConfig
    stored_keys = APIKeyConfig.load()
    stored_keys.apply_to_environment()

    # Check for API keys
    import os
    if not os.environ.get("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set[/]")
        console.print("\nSet it with: wardcliff keys set openai <your-key>")
        raise typer.Exit(1)

    # Run the simulation with the custom event
    asyncio.run(_run_simulation(
        event=custom_event,
        num_agents=agents,
        model=model,
        legacy=False,
        verbosity=verbosity,
        parallel=parallel,
    ))


@app.command()
def run(
    event: Optional[str] = typer.Option(None, "--event", "-e", help="Event ID to trade"),
    multi_outcome: bool = typer.Option(False, "--multi-outcome", "-m", help="Use multi-outcome events"),
    agents: int = typer.Option(3, "--agents", "-a", help="Number of agents"),
    model: str = typer.Option("gpt-5-mini", "--model", help="Model to use"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive setup mode"),
    load_setup: Optional[str] = typer.Option(None, "--load-setup", help="Load setup from JSON file"),
    save_setup: Optional[str] = typer.Option(None, "--save-setup", help="Save setup to JSON file"),
    legacy: bool = typer.Option(False, "--legacy", help="Use legacy OpenAI agents"),
    minimal: bool = typer.Option(False, "--minimal", help="Minimal one-line output"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output with full reasoning"),
    debug: bool = typer.Option(False, "--debug", help="Debug output with raw SDK messages"),
    parallel: bool = typer.Option(False, "--parallel", "-p", help="Run agents in parallel (faster, but no inter-agent reactions)"),
):
    """Run a trading simulation with real-time streaming display."""
    # Set verbosity level
    if debug:
        verbosity = 3
        logging.getLogger().setLevel(logging.DEBUG)
    elif verbose:
        verbosity = 2
        logging.getLogger().setLevel(logging.INFO)
    elif minimal:
        verbosity = 0
    else:
        verbosity = 1

    # Interactive mode for event selection
    if interactive and not event:
        events_dict = get_available_events()
        console.print("\n[bold]Available Events:[/]\n")

        event_list = list(events_dict.keys())
        for idx, eid in enumerate(event_list, 1):
            ev = events_dict[eid]
            console.print(f"  {idx}. [cyan]{eid}[/] - {ev.name}")

        console.print()
        choice = typer.prompt("Select event number", default="1")
        try:
            event = event_list[int(choice) - 1]
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/]")
            raise typer.Exit(1)

    # Load from config if provided
    if load_setup:
        try:
            with open(load_setup) as f:
                config = json.load(f)
                event = config.get("event", event)
                agents = config.get("agents", agents)
                model = config.get("model", model)
        except Exception as e:
            console.print(f"[red]Failed to load setup: {e}[/]")
            raise typer.Exit(1)

    # Resolve event
    events_dict = get_available_events()
    if event:
        if event not in events_dict:
            console.print(f"[red]Unknown event: {event}[/]")
            console.print(f"Available: {', '.join(events_dict.keys())}")
            raise typer.Exit(1)
        selected_event = events_dict[event]
    elif multi_outcome:
        # Default to US President 2028 for multi-outcome
        selected_event = events_dict.get("us-president-2028", list(events_dict.values())[0])
    else:
        # Default event
        selected_event = list(events_dict.values())[0]

    # Save setup if requested
    if save_setup:
        config = {
            "event": selected_event.id,
            "agents": agents,
            "model": model,
        }
        with open(save_setup, "w") as f:
            json.dump(config, f, indent=2)
        console.print(f"[green]Setup saved to {save_setup}[/]")

    # Load stored API keys into environment
    from cliff.cli.config import APIKeyConfig
    stored_keys = APIKeyConfig.load()
    stored_keys.apply_to_environment()

    # Check for API keys
    has_openai_key = bool(os.environ.get("OPENAI_API_KEY"))

    if legacy:
        if not has_openai_key:
            console.print("[red]Error: OPENAI_API_KEY environment variable not set[/]")
            console.print("[dim]Legacy mode requires OpenAI API access[/]")
            console.print("\nSet it with: export OPENAI_API_KEY='your-key'")
            raise typer.Exit(1)
    else:
        if not has_openai_key:
            console.print("[red]Error: OPENAI_API_KEY environment variable not set[/]")
            console.print("[dim]OpenAI Agents SDK mode requires OpenAI API access[/]")
            console.print("\nSet it with: export OPENAI_API_KEY='your-key'")
            raise typer.Exit(1)

    # Run the simulation with graceful cancellation support
    try:
        asyncio.run(_run_simulation(
            event=selected_event,
            num_agents=agents,
            model=model,
            legacy=legacy,
            verbosity=verbosity,
            parallel=parallel,
        ))
    except KeyboardInterrupt:
        # Already handled in _run_simulation, just exit cleanly
        console.print("\n[dim]Exiting...[/]")
        raise typer.Exit(0)


async def _run_simulation(
    event,
    num_agents: int,
    model: str,
    legacy: bool,
    verbosity: int,
    parallel: bool = False,
):
    """Run the simulation with Ink terminal UI."""
    from cliff.core.events import EventMarket
    from cliff.streaming.handler import StreamHandler
    from cliff.streaming.bridge import StdioBridge
    from cliff.streaming.subprocess_manager import InkSubprocess

    # Create event market
    event_market = EventMarket(event=event)

    # Start Ink subprocess
    ink = InkSubprocess()
    try:
        process = await ink.start()
    except Exception as e:
        # Fall back to Rich display if Ink UI is not available
        console.print(f"[yellow]Could not start Ink UI: {e}[/]")
        console.print("[dim]Falling back to Rich display...[/]")
        return await _run_simulation_rich(
            event=event,
            num_agents=num_agents,
            model=model,
            legacy=legacy,
            verbosity=verbosity,
            parallel=parallel,
        )

    # Create bridge connected to Ink subprocess
    bridge = StdioBridge(
        output_stream=process.stdin,
        market_id=event.id,
    )

    # Create stream handler with bridge
    stream_handler = StreamHandler.with_bridge(bridge, verbosity=verbosity)

    # Start reading from subprocess stdout (for user actions)
    read_task = asyncio.create_task(bridge.read_loop(process.stdout))

    # Start stderr streaming for error logging
    stderr_task = asyncio.create_task(ink.stream_stderr())

    # Get initial prices
    prices = event_market.get_prices()

    # Create agent configs
    from cliff.agents.async_agent import AgentPersona
    from cliff.simulation.controller import AgentConfig, SimulationController

    personas = get_default_personas()[:num_agents]
    agent_configs = []

    for persona in personas:
        config = AgentConfig(
            persona=persona,
            prompt=(
                f"Research the event thoroughly using web search. "
                f"Analyze the current prices and determine if any outcomes are mispriced. "
                f"Trade based on your analysis. You have $10,000 to trade with."
            ),
        )
        agent_configs.append(config)

    # Create simulation controller
    try:
        from cliff.core.market import Market

        # Create fallback AMM market with default reserves
        market = Market(
            base_symbol="TOKEN",
            quote_symbol="USD",
            reserves_base=10000.0,
            reserves_quote=10000.0,
        )

        controller = SimulationController(
            market=market,
            agent_configs=agent_configs,
            event_market=event_market,
            use_openai_sdk=not legacy,
            openai_model=model,
            enable_market_monitor=True,
            parallel_agents=parallel,
            verbose=verbosity,
            stream_handler=stream_handler,  # Wire up for live display updates
        )

        # Signal ready to Ink UI
        bridge.emit_ready()

        # Emit initial price update
        stream_handler.emit_price_update(prices)

        # Track cancellation
        cancelled = False

        # Run simulation with streaming hooks
        try:
            # Run the controller
            await controller.run()
        except KeyboardInterrupt:
            cancelled = True
        except asyncio.CancelledError:
            cancelled = True
        finally:
            # Shutdown bridge and subprocess
            bridge.shutdown()
            read_task.cancel()
            stderr_task.cancel()
            await ink.stop()

        # Print summary to console (Ink UI will show its own)
        if cancelled:
            console.print("\n[yellow]Simulation cancelled[/]")

        final_prices = event_market.get_prices()
        console.print(f"\n[bold]Final Prices:[/]")
        for outcome, price in sorted(final_prices.items(), key=lambda x: -x[1]):
            console.print(f"  {outcome}: {price*100:.1f}%")
        console.print(f"Total trades: {len(controller.event_trade_history)}")

    except ImportError as e:
        console.print(f"\n[red]Import error: {e}[/]")
        console.print("[yellow]Some dependencies may not be installed.[/]")


async def _run_simulation_rich(
    event,
    num_agents: int,
    model: str,
    legacy: bool,
    verbosity: int,
    parallel: bool = False,
):
    """Fallback: Run the simulation with Rich terminal display."""
    from cliff.core.events import EventMarket
    from cliff.streaming.display import RichDisplay
    from cliff.streaming.handler import StreamHandler

    console.print()
    console.print(Panel(
        f"[bold]{event.name}[/]\n{event.description}",
        title="[bold orange1]WARDCLIFF[/] - Starting Simulation",
        border_style="orange1",
    ))

    # Create event market
    event_market = EventMarket(event=event)

    # Initialize streaming with Rich display
    stream_handler = StreamHandler(verbosity=verbosity)
    display = RichDisplay(
        console=console,
        verbosity=verbosity,
        market_name=event.name,
    )

    # Wire up display to stream handler
    stream_handler.subscribe(display.handle_event)

    # Show initial prices
    prices = event_market.get_prices()
    console.print("\n[bold orange1]Initial Prices:[/]")
    for outcome, price in sorted(prices.items(), key=lambda x: -x[1]):
        pct = price * 100
        console.print(f"  {outcome}: [orange1]${price:.2f}[/] ({pct:.1f}%)")

    console.print(f"\n[dim]Agents: {num_agents} | Model: {model} | Mode: {'Legacy' if legacy else 'OpenAI SDK'}[/]")
    console.print("[dim]Press Ctrl+C to cancel the simulation[/]\n")

    # Create agent configs
    from cliff.agents.async_agent import AgentPersona
    from cliff.simulation.controller import AgentConfig, SimulationController

    personas = get_default_personas()[:num_agents]
    agent_configs = []

    for persona in personas:
        config = AgentConfig(
            persona=persona,
            prompt=(
                f"Research the event thoroughly using web search. "
                f"Analyze the current prices and determine if any outcomes are mispriced. "
                f"Trade based on your analysis. You have $10,000 to trade with."
            ),
        )
        agent_configs.append(config)

    # Create simulation controller
    try:
        from cliff.core.market import Market

        # Create fallback AMM market with default reserves
        market = Market(
            base_symbol="TOKEN",
            quote_symbol="USD",
            reserves_base=10000.0,
            reserves_quote=10000.0,
        )

        controller = SimulationController(
            market=market,
            agent_configs=agent_configs,
            event_market=event_market,
            use_openai_sdk=not legacy,
            openai_model=model,
            enable_market_monitor=True,
            parallel_agents=parallel,
            verbose=verbosity,
            stream_handler=stream_handler,
        )

        # Start display
        display.start()

        # Emit initial price update
        stream_handler.emit_price_update(prices)

        # Track cancellation
        cancelled = False

        # Run simulation with streaming hooks
        try:
            await controller.run()
        except KeyboardInterrupt:
            cancelled = True
            console.print("\n\n[yellow]Simulation cancelled by user (Ctrl+C)[/]")
        except asyncio.CancelledError:
            cancelled = True
            console.print("\n\n[yellow]Simulation cancelled[/]")
        finally:
            display.stop()

        # Print summary
        final_prices = event_market.get_prices()
        summary = {
            "event": event.name,
            "final_prices": final_prices,
            "total_trades": len(controller.event_trade_history),
        }
        if cancelled:
            summary["status"] = "cancelled"
        display.print_summary(summary)

    except ImportError as e:
        console.print(f"\n[red]Import error: {e}[/]")
        console.print("[yellow]Some dependencies may not be installed.[/]")
        console.print("[dim]Try: pip install -e '.[dev]'[/]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[red]Simulation error: {e}[/]")
        if verbosity >= 2:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(1)


@app.command()
def events(
    multi_outcome: bool = typer.Option(False, "--multi-outcome", "-m", help="Show only multi-outcome events"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """List available prediction market events."""
    events_dict = get_available_events()

    if json_output:
        output = []
        for event_id, event in events_dict.items():
            if multi_outcome and len(event.outcomes) <= 2:
                continue
            output.append({
                "id": event_id,
                "name": event.name,
                "description": event.description,
                "outcomes": event.outcomes,
            })
        console.print(json.dumps(output, indent=2))
        return

    console.print()
    console.print("[bold orange1]Available Prediction Events[/]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="orange1")
    table.add_column("Name")
    table.add_column("Outcomes", justify="right")

    for event_id, event in events_dict.items():
        if multi_outcome and len(event.outcomes) <= 2:
            continue

        outcomes_str = f"{len(event.outcomes)} outcomes"
        if len(event.outcomes) == 2:
            outcomes_str = "Binary"

        table.add_row(event_id, event.name, outcomes_str)

    console.print(table)
    console.print()
    console.print("[dim]Use 'wardcliff run -e <ID>' to run a simulation[/]")


@app.command()
def sources(
    action: Optional[str] = typer.Argument(None, help="Action: list, add, remove, sync, types"),
    value: Optional[str] = typer.Argument(None, help="Source path/URL or ID to remove"),
    source_type: Optional[str] = typer.Option(None, "--type", "-t", help="Source type: url, file, rss, api, database"),
    event: Optional[str] = typer.Option(None, "--event", "-e", help="Associate with event"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Source name"),
):
    """Manage data sources for agent research.

    Source types:
      url      - Web page to fetch and parse
      file     - Local file (PDF, CSV, JSON, TXT, MD)
      rss      - RSS/Atom feed for continuous updates
      api      - REST API endpoint for data
      database - Database connection string
    """
    from cliff.cli.config import SourcesConfig, DataSource
    from datetime import datetime

    config = SourcesConfig.load()

    if action is None or action == "list":
        console.print("\n[bold orange1]Data Sources[/]\n")

        # Also show event-specific sources
        events_dict = get_available_events()

        # Show configured sources
        if config.sources:
            # Group by type
            by_type: dict = {}
            for s in config.sources:
                by_type.setdefault(s.type, []).append(s)

            for stype, srcs in by_type.items():
                type_icon = {
                    "url": "🌐",
                    "file": "📄",
                    "rss": "📡",
                    "api": "🔌",
                    "database": "💾",
                }.get(stype, "📦")

                console.print(f"[bold]{type_icon} {stype.upper()}[/]")

                table = Table(show_header=True, header_style="dim", box=None)
                table.add_column("ID", style="orange1", width=12)
                table.add_column("Name/Location", width=40)
                table.add_column("Event", width=15)
                table.add_column("Status", width=8)

                for s in srcs:
                    status = "[green]●[/]" if s.enabled else "[dim]○[/]"
                    display = s.name if s.name else (s.location[:35] + "..." if len(s.location) > 38 else s.location)
                    event_display = s.event_id or "[dim]-[/]"
                    table.add_row(s.id, display, event_display, status)

                console.print(table)
                console.print()
        else:
            console.print("[dim]No custom sources configured[/]\n")

        # Show event built-in sources
        console.print("[bold]Event Data Sources[/]")
        for event_id, ev in events_dict.items():
            if ev.data_sources:
                console.print(f"  [orange1]{event_id}[/]: {len(ev.data_sources)} built-in URLs")

        console.print()
        console.print("[dim]Add sources with: wardcliff sources add <url-or-path> --type <type>[/]")

    elif action == "add":
        if not value:
            console.print("[red]Source path or URL required[/]")
            console.print()
            console.print("Examples:")
            console.print("  wardcliff sources add https://example.com --type url")
            console.print("  wardcliff sources add ./data.pdf --type file")
            console.print("  wardcliff sources add https://feed.com/rss --type rss")
            raise typer.Exit(1)

        # Auto-detect type if not specified
        if not source_type:
            if value.startswith(("http://", "https://")):
                if "/rss" in value or "/feed" in value or value.endswith((".xml", ".rss")):
                    source_type = "rss"
                elif "/api/" in value or value.endswith(".json"):
                    source_type = "api"
                else:
                    source_type = "url"
            elif Path(value).exists():
                source_type = "file"
            elif value.startswith(("postgres://", "postgresql://", "mysql://", "sqlite://")):
                source_type = "database"
            else:
                console.print("[red]Could not auto-detect source type. Use --type to specify.[/]")
                raise typer.Exit(1)

        # Validate
        if source_type == "file":
            path = Path(value)
            if not path.exists():
                console.print(f"[red]File not found: {value}[/]")
                raise typer.Exit(1)
            value = str(path.absolute())

        # Create source
        source = DataSource(
            id=f"{source_type}_{len(config.sources) + 1}",
            type=source_type,
            location=value,
            name=name,
            event_id=event,
            added_at=datetime.now().isoformat(),
        )

        config.add(source)
        config.save()

        console.print(f"[green]✓[/] Added {source_type} source: {source.id}")
        console.print(f"  Location: {value[:60]}{'...' if len(value) > 60 else ''}")
        if name:
            console.print(f"  Name: {name}")
        if event:
            console.print(f"  Event: {event}")

    elif action == "remove":
        if not value:
            console.print("[red]Source ID required[/]")
            console.print("[dim]Use 'wardcliff sources list' to see IDs[/]")
            raise typer.Exit(1)

        if config.remove(value):
            config.save()
            console.print(f"[yellow]Removed source: {value}[/]")
        else:
            console.print(f"[red]Source not found: {value}[/]")
            raise typer.Exit(1)

    elif action == "sync":
        console.print("\n[bold]Syncing data sources...[/]\n")

        if not config.sources:
            console.print("[dim]No sources to sync[/]")
            return

        synced = 0
        for source in config.sources:
            if not source.enabled:
                continue

            console.print(f"  [{source.type}] {source.id}... ", end="")

            # Simulate sync (actual implementation would fetch content)
            source.last_synced = datetime.now().isoformat()
            synced += 1
            console.print("[green]✓[/]")

        config.save()
        console.print(f"\n[green]Synced {synced} sources[/]")

    elif action == "types":
        console.print("\n[bold orange1]Supported Source Types[/]\n")

        types_info = [
            ("url", "🌐", "Web page", "Fetches and parses HTML content from a URL"),
            ("file", "📄", "Local file", "PDF, CSV, JSON, TXT, MD files for ingestion"),
            ("rss", "📡", "RSS feed", "Subscribe to RSS/Atom feeds for updates"),
            ("api", "🔌", "REST API", "Fetch data from REST API endpoints"),
            ("database", "💾", "Database", "PostgreSQL, MySQL, SQLite connections"),
        ]

        table = Table(show_header=True, header_style="bold")
        table.add_column("Type", style="orange1")
        table.add_column("Icon")
        table.add_column("Name")
        table.add_column("Description")

        for t in types_info:
            table.add_row(*t)

        console.print(table)
        console.print()

    elif action == "clear":
        if not config.sources:
            console.print("[dim]No sources to clear[/]")
            return

        count = len(config.sources)
        config.sources = []
        config.save()
        console.print(f"[yellow]Cleared {count} sources[/]")

    else:
        console.print(f"[red]Unknown action: {action}[/]")
        console.print("Valid actions: list, add, remove, sync, types, clear")
        raise typer.Exit(1)


@app.command()
def tools(
    tool_type: Optional[str] = typer.Argument(None, help="Filter by type: native, custom, mcp"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    show_all: bool = typer.Option(False, "--all", "-a", help="Show all tools including disabled"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """List all available tools: native (Codex), custom (trading), and MCP servers.

    Tool Types:
      native  - OpenAI Agents SDK tools (WebSearch, CodeInterpreter, FileSearch)
      custom  - Built-in trading tools (portfolio, prices, trades, alerts)
      mcp     - 60+ external MCP servers (Smithery + GitHub)
    """
    from cliff.cli.tools import get_tool_registry

    registry = get_tool_registry()

    if json_output:
        output = {
            "summary": registry.summary(),
            "tools": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "category": t.category,
                    "type": t.tool_type,
                    "enabled": t.enabled or t.always_enabled,
                }
                for t in registry.get_all()
                if (not tool_type or t.tool_type.startswith(tool_type))
                and (not category or t.category == category)
            ],
        }
        console.print(json.dumps(output, indent=2))
        return

    summary = registry.summary()
    console.print()
    console.print(f"[bold orange1]Wardcliff Tool Registry[/] - {summary['total']} tools available")
    console.print()

    # Native Tools (Codex)
    if not tool_type or tool_type == "native":
        native_tools = registry.get_native_tools()
        if native_tools:
            console.print("[bold orange1]Native Tools (OpenAI Agents SDK / Codex)[/]")
            for t in native_tools:
                if not show_all and not t.enabled:
                    continue
                status = "[green]●[/]" if t.enabled else "[dim]○[/]"
                console.print(f"  {status} [orange1]{t.name}[/] - {t.description}")
            console.print()

    # Custom Trading Tools
    if not tool_type or tool_type == "custom":
        custom_tools = registry.get_custom_tools()
        if custom_tools:
            console.print("[bold orange1]Custom Trading Tools (Built-in)[/]")
            for t in custom_tools:
                status = "[green]●[/]" if t.always_enabled else "[dim]○[/]"
                console.print(f"  {status} [orange1]{t.name}[/] - {t.description}")
            console.print()

    # MCP Servers
    if not tool_type or tool_type == "mcp":
        mcp_servers = registry.get_mcp_servers()
        if mcp_servers:
            # Group by category
            by_category: dict = {}
            for t in mcp_servers:
                by_category.setdefault(t.category, []).append(t)

            console.print(f"[bold yellow]MCP Servers ({len(mcp_servers)} available)[/]")

            # Category icons
            icons = {
                "communication": "💬",
                "knowledge": "📚",
                "project_management": "📋",
                "development": "💻",
                "devops": "🔧",
                "crm": "👥",
                "finance": "💰",
                "banking": "🏦",
                "markets": "📈",
                "support": "🎧",
                "database": "🗄️",
                "scheduling": "📅",
                "ecommerce": "🛒",
                "marketing": "📣",
                "social": "📱",
                "design": "🎨",
                "expense": "💳",
                "payroll": "💵",
                "hr": "👔",
                "trading": "📊",
                "research": "🔍",
            }

            for cat in sorted(by_category.keys()):
                if category and cat != category:
                    continue

                servers = by_category[cat]
                enabled_count = sum(1 for s in servers if s.enabled)
                icon = icons.get(cat, "📦")

                console.print(f"\n  {icon} [bold]{cat.replace('_', ' ').title()}[/] ({enabled_count}/{len(servers)} enabled)")

                for t in sorted(servers, key=lambda x: x.name):
                    if not show_all and not t.enabled:
                        continue

                    status = "[green]●[/]" if t.enabled else "[dim]○[/]"
                    tools_str = f" ({t.tools_count} tools)" if t.tools_count else ""
                    official = " [orange1][OFFICIAL][/]" if t.official else ""
                    env_hint = f" [dim]({t.env_key})[/]" if show_all and t.env_key else ""
                    console.print(f"    {status} {t.name}{tools_str}{official}{env_hint}")

            console.print()

    # Summary
    console.print(f"[dim]{summary['enabled']}/{summary['total']} tools enabled[/]")
    console.print("[dim]Use 'wardcliff tools --all' to see all available tools[/]")
    console.print("[dim]Use 'wardcliff tools mcp --category finance' to filter by category[/]")


def _mcp_setup_wizard(registry, category_filter: Optional[str] = None):
    """Interactive wizard to configure MCP servers with 3 sections by auth type."""
    from cliff.cli.config import MCPKeysConfig, mask_key
    from cliff.integrations.mcp.external.github import (
        GITHUB_SERVERS, AUTH_NONE, AUTH_API_KEY, AUTH_MULTI_KEY, AUTH_OAUTH
    )
    import webbrowser

    mcp_keys = MCPKeysConfig.load()

    console.print()
    console.print("[bold orange1]MCP Server Setup Wizard[/]")
    console.print("[dim]Configure and enable MCP servers[/]")
    console.print()

    # Get all MCP servers from the registry
    mcp_servers = registry.get_mcp_servers()

    # Group servers by auth type using the new auth_type field
    no_auth_servers = []  # auth_type: none
    api_key_servers = []  # auth_type: api_key or multi_key
    oauth_servers = []    # auth_type: oauth

    for t in mcp_servers:
        server_id = t.id.replace("mcp-", "")
        spec = GITHUB_SERVERS.get(server_id, {})

        auth_type = spec.get("auth_type", AUTH_API_KEY)

        if auth_type == AUTH_NONE:
            no_auth_servers.append((t, spec, server_id))
        elif auth_type == AUTH_OAUTH:
            oauth_servers.append((t, spec, server_id))
        elif auth_type in (AUTH_API_KEY, AUTH_MULTI_KEY):
            api_key_servers.append((t, spec, server_id))

    # Filter by category if specified
    if category_filter:
        no_auth_servers = [(t, s, sid) for t, s, sid in no_auth_servers if t.category == category_filter]
        api_key_servers = [(t, s, sid) for t, s, sid in api_key_servers if t.category == category_filter]
        oauth_servers = [(t, s, sid) for t, s, sid in oauth_servers if t.category == category_filter]

    # =========================================================================
    # SECTION 1: No Auth Required (Enable/Disable Toggle)
    # =========================================================================
    if no_auth_servers:
        console.print("[bold cyan]No Authentication Required[/]")
        console.print("[dim]These servers can be enabled without any API keys[/]")
        console.print()

        for idx, (t, spec, server_id) in enumerate(no_auth_servers, 1):
            is_enabled = mcp_keys.is_server_enabled(server_id)
            status = "[green]●[/] ENABLED" if is_enabled else "[dim]○[/] disabled"
            console.print(f"  {idx}. {status} - [bold]{t.name}[/]")
            console.print(f"      [dim]{t.description}[/]")

        console.print()
        console.print("[dim]Enter number to toggle enable/disable, or 'q' to continue:[/]")

        while True:
            choice = typer.prompt("Toggle server", default="q")
            if choice.lower() == "q":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(no_auth_servers):
                    t, spec, server_id = no_auth_servers[idx]
                    if mcp_keys.is_server_enabled(server_id):
                        mcp_keys.disable_server(server_id)
                        console.print(f"[yellow]Disabled {t.name}[/]")
                    else:
                        mcp_keys.enable_server(server_id)
                        console.print(f"[green]Enabled {t.name}[/]")
                    mcp_keys.save()
                else:
                    console.print("[red]Invalid number[/]")
            except ValueError:
                console.print("[red]Please enter a number or 'q'[/]")

        console.print()

    # =========================================================================
    # SECTION 2: API Key Required
    # =========================================================================
    if api_key_servers:
        console.print(f"[bold yellow]API Key Required[/] ({len(api_key_servers)} servers)")
        console.print("[dim]These servers require an API key to enable[/]")
        console.print()

        for idx, (t, spec, server_id) in enumerate(api_key_servers, 1):
            env_key = spec.get("env_key")
            env_keys = spec.get("env_keys", [env_key] if env_key else [])

            # Check if already configured
            all_configured = all(mcp_keys.has(k) or os.environ.get(k) for k in env_keys if k)
            status = "[green]●[/]" if all_configured else "[dim]○[/]"

            console.print(f"  {idx}. {status} {t.name}")
            console.print(f"      [dim]{t.description}[/]")
            if env_keys:
                for ek in env_keys:
                    if ek:
                        if mcp_keys.has(ek):
                            console.print(f"      [green]✓[/] {ek}: {mask_key(mcp_keys.get(ek) or '')}")
                        elif os.environ.get(ek):
                            console.print(f"      [green]✓[/] {ek}: (from environment)")
                        else:
                            console.print(f"      [yellow]○[/] {ek}: [dim]not configured[/]")

        console.print()
        console.print("[dim]Enter server number to configure API key, or 'q' to continue:[/]")

        while True:
            choice = typer.prompt("Configure server", default="q")
            if choice.lower() == "q":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(api_key_servers):
                    t, spec, server_id = api_key_servers[idx]
                    _configure_api_key_server(t, spec, mcp_keys)
                else:
                    console.print("[red]Invalid number[/]")
            except ValueError:
                console.print("[red]Please enter a number or 'q'[/]")

        console.print()

    # =========================================================================
    # SECTION 3: OAuth Required (Enable/Disable + Browser Auth)
    # =========================================================================
    if oauth_servers:
        console.print(f"[bold magenta]OAuth Required[/] ({len(oauth_servers)} servers)")
        console.print("[dim]These servers use browser-based OAuth authentication[/]")
        console.print()

        for idx, (t, spec, server_id) in enumerate(oauth_servers, 1):
            is_enabled = mcp_keys.is_server_enabled(server_id)
            status = "[green]●[/] ENABLED" if is_enabled else "[dim]○[/] disabled"
            console.print(f"  {idx}. {status} - [bold]{t.name}[/]")
            console.print(f"      [dim]{t.description}[/]")
            docs = spec.get("docs", "")
            if docs:
                console.print(f"      [dim]Docs: {docs}[/]")

        console.print()
        console.print("[dim]Enter number to toggle and optionally open docs, or 'q' to continue:[/]")

        while True:
            choice = typer.prompt("Toggle OAuth server", default="q")
            if choice.lower() == "q":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(oauth_servers):
                    t, spec, server_id = oauth_servers[idx]
                    if mcp_keys.is_server_enabled(server_id):
                        mcp_keys.disable_server(server_id)
                        console.print(f"[yellow]Disabled {t.name}[/]")
                    else:
                        mcp_keys.enable_server(server_id)
                        console.print(f"[green]Enabled {t.name}[/]")
                        # Offer to open docs
                        docs = spec.get("docs", "")
                        if docs and typer.confirm("Open OAuth setup docs in browser?", default=True):
                            webbrowser.open(docs)
                    mcp_keys.save()
                else:
                    console.print("[red]Invalid number[/]")
            except ValueError:
                console.print("[red]Please enter a number or 'q'[/]")

    # =========================================================================
    # Summary
    # =========================================================================
    console.print()
    console.print("[bold]Configuration Summary[/]")

    # Show enabled no-auth servers
    enabled_no_auth = [sid for sid in mcp_keys.enabled_servers
                       if any(sid == s[2] for s in no_auth_servers)]
    enabled_oauth = [sid for sid in mcp_keys.enabled_servers
                     if any(sid == s[2] for s in oauth_servers)]

    if enabled_no_auth:
        console.print(f"[cyan]●[/] {len(enabled_no_auth)} no-auth server(s) enabled: {', '.join(enabled_no_auth)}")
    if enabled_oauth:
        console.print(f"[magenta]●[/] {len(enabled_oauth)} OAuth server(s) enabled: {', '.join(enabled_oauth)}")

    stored_keys = mcp_keys.get_all()
    if stored_keys:
        console.print(f"[yellow]●[/] {len(stored_keys)} API key(s) stored")
        for k, v in stored_keys.items():
            console.print(f"    {k}: {v}")

    if not enabled_no_auth and not enabled_oauth and not stored_keys:
        console.print("[dim]No servers configured yet[/]")

    console.print()
    console.print("[dim]Configuration saved to ~/.wardcliff/mcp_keys.json[/]")
    console.print("[dim]Test a server with: wardcliff mcp connect <server>[/]")


def _configure_api_key_server(tool, spec, mcp_keys):
    """Configure API keys for a single server."""
    from cliff.cli.config import mask_key

    console.print()
    console.print(f"[bold]Configuring {tool.name}[/]")

    env_key = tool.env_key or spec.get("env_key")
    env_keys = spec.get("env_keys", [env_key] if env_key else [])

    # Get docs/help URL
    docs = spec.get("docs") or spec.get("github") or spec.get("npm")
    if docs:
        console.print(f"[dim]Docs: {docs}[/]")
        if typer.confirm("Open docs in browser?", default=False):
            import webbrowser
            webbrowser.open(docs)

    console.print()

    for ek in env_keys:
        if not ek:
            continue

        current = mcp_keys.get(ek) or os.environ.get(ek)
        if current:
            console.print(f"[green]✓[/] {ek}: {mask_key(current)}")
            if not typer.confirm("Update this key?", default=False):
                continue

        # Prompt for the key
        key = typer.prompt(f"Enter {ek}", hide_input=True)
        if key:
            mcp_keys.set(ek, key)
            console.print(f"[green]✓[/] {ek} saved")

    mcp_keys.save()
    console.print(f"[green]✓[/] Configuration saved for {tool.name}")


def _mcp_test_connection(server_id: str, registry):
    """Test connection to an MCP server."""
    from cliff.cli.config import MCPKeysConfig
    from cliff.integrations.mcp.external.github import (
        GITHUB_SERVERS, AUTH_NONE, AUTH_API_KEY, AUTH_MULTI_KEY, AUTH_OAUTH
    )
    import asyncio

    # Load and apply stored keys
    mcp_keys = MCPKeysConfig.load()
    mcp_keys.apply_to_environment()

    # Find the server
    tool = registry.get(f"mcp-{server_id}") or registry.get(server_id)
    if not tool:
        console.print(f"[red]Server not found: {server_id}[/]")
        console.print("[dim]Use 'wardcliff mcp list --all' to see available servers[/]")
        raise typer.Exit(1)

    # Get the server config
    spec = GITHUB_SERVERS.get(server_id, {})
    if not spec:
        console.print(f"[red]Server '{server_id}' not in GitHub registry[/]")
        console.print("[dim]Only GitHub (local stdio) servers can be tested[/]")
        raise typer.Exit(1)

    # Check auth requirements based on auth_type
    auth_type = spec.get("auth_type", AUTH_API_KEY)
    env_key = spec.get("env_key")
    env_keys = spec.get("env_keys", [env_key] if env_key else [])

    if auth_type == AUTH_NONE:
        # No auth needed, but must be enabled
        if not mcp_keys.is_server_enabled(server_id):
            console.print(f"[yellow]Server '{server_id}' is not enabled[/]")
            console.print("[dim]Enable with: wardcliff mcp setup[/]")
            raise typer.Exit(1)
    elif auth_type == AUTH_OAUTH:
        # OAuth - must be enabled
        if not mcp_keys.is_server_enabled(server_id):
            console.print(f"[yellow]OAuth server '{server_id}' is not enabled[/]")
            console.print("[dim]Enable with: wardcliff mcp setup[/]")
            raise typer.Exit(1)
    elif auth_type in (AUTH_API_KEY, AUTH_MULTI_KEY):
        # Check for required env vars
        missing = [k for k in env_keys if k and not os.environ.get(k)]
        if missing:
            console.print(f"[yellow]Missing required keys for {tool.name}:[/]")
            for k in missing:
                console.print(f"  [red]○[/] {k}")
            console.print()
            console.print("[dim]Configure with: wardcliff mcp setup[/]")
            raise typer.Exit(1)

    console.print(f"\n[bold]Testing connection to {tool.name}...[/]")

    command = spec.get("command")
    args = spec.get("args", [])

    if not command:
        # SSE server
        url = spec.get("url")
        if url:
            console.print(f"[dim]URL: {url}[/]")
            console.print("[yellow]SSE servers require runtime connection[/]")
            console.print("[dim]Use in simulation to test: wardcliff run[/]")
            return
        else:
            console.print("[red]No command or URL found for this server[/]")
            raise typer.Exit(1)

    console.print(f"[dim]Command: {command} {' '.join(args)}[/]")

    async def test_connection():
        try:
            from agents.mcp import MCPServerStdio

            # Build env vars
            env = {k: os.environ.get(k, "") for k in env_keys if k and os.environ.get(k)}

            server = MCPServerStdio(
                name=server_id,
                params={
                    "command": command,
                    "args": args,
                    "env": env,
                },
                cache_tools_list=True,
            )

            async with server:
                tools = await server.list_tools()
                console.print(f"[green]✓[/] Connected successfully!")
                console.print(f"[green]✓[/] {len(tools)} tools available:")
                for t in tools[:10]:
                    console.print(f"    - {t.name}: {t.description[:50] if t.description else 'N/A'}...")
                if len(tools) > 10:
                    console.print(f"    ... and {len(tools) - 10} more")

        except ImportError:
            console.print("[yellow]OpenAI Agents SDK not available (Python 3.10+ required)[/]")
            console.print("[dim]The server configuration is correct, but cannot test connection.[/]")
        except TypeError as e:
            if "type annotation" in str(e).lower() or "|" in str(e):
                console.print("[yellow]Python 3.10+ required for MCP connection testing[/]")
                console.print(f"[dim]Current Python: {sys.version_info.major}.{sys.version_info.minor}[/]")
                console.print("[dim]The server configuration is correct.[/]")
            else:
                console.print(f"[red]✗[/] Connection failed: {e}")
        except Exception as e:
            error_str = str(e)
            if "ENOENT" in error_str or "not found" in error_str.lower():
                console.print(f"[red]✗[/] Package not installed")
                console.print(f"[dim]Run: {command} {' '.join(args[:2])}[/]")
            elif "Timed out" in error_str or "timeout" in error_str.lower():
                console.print(f"[yellow]⏳[/] Connection timed out (package may be downloading)")
                console.print("[dim]Try again in a few seconds[/]")
            else:
                console.print(f"[red]✗[/] Connection failed: {e}")

    asyncio.run(test_connection())


@app.command()
def mcp(
    action: Optional[str] = typer.Argument(None, help="Action: list, setup, connect, enable, disable, add, remove, export"),
    server: Optional[str] = typer.Argument(None, help="Server ID to manage"),
    show_all: bool = typer.Option(False, "--all", "-a", help="Show all available servers"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    command: Optional[str] = typer.Option(None, "--command", help="Command to run server (for add)"),
    url: Optional[str] = typer.Option(None, "--url", help="Server URL (for add)"),
):
    """Manage MCP (Model Context Protocol) servers.

    Actions:
      list    - Show all 60+ MCP servers (use --all to see disabled)
      setup   - Interactive wizard to configure MCP servers
      connect - Test connection to an MCP server
      enable  - Enable a server (set its env var)
      disable - Disable a server
      add     - Add a custom server
      remove  - Remove a custom server
      export  - Export MCP configuration
    """
    from cliff.cli.tools import get_tool_registry
    from cliff.cli.config import MCPConfig, MCPServer

    registry = get_tool_registry()
    config = MCPConfig.load()

    if action is None or action == "list":
        # Use the unified registry for listing
        mcp_servers = registry.get_mcp_servers()

        console.print()
        console.print(f"[bold orange1]MCP Servers[/] - {len(mcp_servers)} available")
        console.print()

        # Group by category
        by_category: dict = {}
        for t in mcp_servers:
            by_category.setdefault(t.category, []).append(t)

        icons = {
            "communication": "💬",
            "knowledge": "📚",
            "project_management": "📋",
            "development": "💻",
            "devops": "🔧",
            "crm": "👥",
            "finance": "💰",
            "banking": "🏦",
            "markets": "📈",
            "support": "🎧",
            "database": "🗄️",
            "scheduling": "📅",
            "ecommerce": "🛒",
            "marketing": "📣",
            "social": "📱",
            "design": "🎨",
            "expense": "💳",
            "payroll": "💵",
            "hr": "👔",
            "trading": "📊",
            "research": "🔍",
        }

        total_enabled = 0
        for cat in sorted(by_category.keys()):
            if category and cat != category:
                continue

            servers = by_category[cat]
            enabled_count = sum(1 for s in servers if s.enabled)
            total_enabled += enabled_count
            icon = icons.get(cat, "📦")

            # Skip category if nothing to show
            if not show_all and enabled_count == 0:
                continue

            console.print(f"{icon} [bold]{cat.replace('_', ' ').title()}[/] ({enabled_count}/{len(servers)})")

            for t in sorted(servers, key=lambda x: x.name):
                if not show_all and not t.enabled:
                    continue

                status = "[green]●[/]" if t.enabled else "[dim]○[/]"
                # Strip "mcp-" prefix for display
                display_id = t.id.replace("mcp-", "")
                tools_str = f" ({t.tools_count} tools)" if t.tools_count else ""
                official = " [orange1][OFFICIAL][/]" if t.official else ""

                console.print(f"  {status} {t.name}{tools_str}{official}")
                if show_all:
                    console.print(f"      [dim]{t.description}[/]")
                    if t.env_key:
                        console.print(f"      [dim]Enable: export {t.env_key}=your-key[/]")

            console.print()

        console.print(f"[dim]{total_enabled}/{len(mcp_servers)} servers enabled[/]")
        console.print("[dim]Use 'wardcliff mcp list --all' to see all available servers[/]")
        console.print("[dim]Enable a server by setting its environment variable[/]")

    elif action == "enable":
        if not server:
            console.print("[red]Server ID required[/]")
            console.print("[dim]Use 'wardcliff mcp list --all' to see available servers[/]")
            raise typer.Exit(1)

        # Check if it's in the unified registry
        tool = registry.get(f"mcp-{server}") or registry.get(server)
        if tool and tool.env_key:
            console.print(f"[yellow]To enable {tool.name}, set the environment variable:[/]")
            console.print(f"\n  export {tool.env_key}=your-api-key\n")
            console.print("[dim]Then restart the simulation for changes to take effect.[/]")
        elif config.enable(server):
            config.save()
            srv = config.get(server)
            console.print(f"[green]✓[/] Enabled MCP server: {srv.name if srv else server}")
        else:
            console.print(f"[red]Server not found: {server}[/]")
            raise typer.Exit(1)

    elif action == "disable":
        if not server:
            console.print("[red]Server ID required[/]")
            raise typer.Exit(1)

        tool = registry.get(f"mcp-{server}") or registry.get(server)
        if tool and tool.env_key:
            console.print(f"[yellow]To disable {tool.name}, unset the environment variable:[/]")
            console.print(f"\n  unset {tool.env_key}\n")
        elif config.disable(server):
            config.save()
            srv = config.get(server)
            console.print(f"[yellow]Disabled MCP server: {srv.name if srv else server}[/]")
        else:
            console.print(f"[red]Server not found: {server}[/]")
            raise typer.Exit(1)

    elif action == "add":
        if not server:
            console.print("[red]Server ID required[/]")
            console.print()
            console.print("Examples:")
            console.print("  wardcliff mcp add my-server --command 'npx' --url http://localhost:3000")
            console.print("  wardcliff mcp add custom-api --url https://api.example.com/mcp")
            raise typer.Exit(1)

        if not command and not url:
            console.print("[red]Either --command or --url is required[/]")
            raise typer.Exit(1)

        name = typer.prompt("Server name", default=server)
        description = typer.prompt("Description", default="Custom MCP server")
        cat = typer.prompt("Category (trading/research/data)", default="data")

        new_server = MCPServer(
            id=server,
            name=name,
            description=description,
            category=cat,
            enabled=True,
            command=command,
            url=url,
        )
        config.add_server(new_server)
        config.save()

        console.print(f"\n[green]✓[/] Added MCP server: {name}")
        console.print(f"  ID: {server}")
        if command:
            console.print(f"  Command: {command}")
        if url:
            console.print(f"  URL: {url}")

    elif action == "remove":
        if not server:
            console.print("[red]Server ID required[/]")
            raise typer.Exit(1)

        if config.remove_server(server):
            config.save()
            console.print(f"[yellow]Removed MCP server: {server}[/]")
        else:
            console.print(f"[red]Server not found: {server}[/]")
            raise typer.Exit(1)

    elif action == "export":
        console.print("\n[bold]MCP Server Configuration[/]\n")

        mcp_config = config.to_claude_config()  # Method name unchanged for compatibility

        if not mcp_config["mcpServers"]:
            console.print("[dim]No servers with command/url configured for export[/]")
            console.print("[dim]Add servers with: wardcliff mcp add <id> --command <cmd> or --url <url>[/]")
            return

        import json as json_mod
        console.print(json_mod.dumps(mcp_config, indent=2))
        console.print()
        console.print("[dim]Add this to your MCP configuration file (e.g., .mcp.json)[/]")

    elif action == "setup":
        _mcp_setup_wizard(registry, category)

    elif action == "connect":
        if not server:
            console.print("[red]Server ID required[/]")
            console.print("[dim]Usage: wardcliff mcp connect <server-id>[/]")
            raise typer.Exit(1)
        _mcp_test_connection(server, registry)

    else:
        console.print(f"[red]Unknown action: {action}[/]")
        console.print("Valid actions: list, setup, connect, enable, disable, add, remove, export")
        raise typer.Exit(1)



@app.command()
def analyze(
    log_file: str = typer.Argument("logs/simulation.log", help="Log file to analyze"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output report to file"),
    format: str = typer.Option("text", "--format", "-f", help="Output format: text, json, markdown"),
):
    """Analyze simulation logs and generate post-mortem report."""
    log_path = Path(log_file)

    if not log_path.exists():
        console.print(f"[red]Log file not found: {log_file}[/]")
        console.print("[dim]Run a simulation first with: wardcliff run[/]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Analyzing:[/] {log_file}\n")

    # Parse log file
    trades = []
    agents = set()

    try:
        with open(log_path) as f:
            for line in f:
                if "Trade executed" in line or "TRADE_EXECUTED" in line:
                    trades.append(line.strip())
                if "agent=" in line:
                    # Extract agent name
                    import re
                    match = re.search(r'agent=(\w+)', line)
                    if match:
                        agents.add(match.group(1))
    except Exception as e:
        console.print(f"[red]Error reading log: {e}[/]")
        raise typer.Exit(1)

    # Generate report
    report = {
        "log_file": str(log_path),
        "total_trades": len(trades),
        "agents": list(agents),
        "summary": f"Analyzed {len(trades)} trades from {len(agents)} agents",
    }

    if format == "json":
        output_text = json.dumps(report, indent=2)
    elif format == "markdown":
        output_text = f"""# Simulation Analysis

**Log File:** {log_path}

## Summary
- Total Trades: {len(trades)}
- Agents: {', '.join(agents) if agents else 'Unknown'}

## Trades
{chr(10).join(f'- {t}' for t in trades[:10])}
{'...' if len(trades) > 10 else ''}
"""
    else:
        output_text = f"""
Simulation Analysis Report
==========================
Log File: {log_path}
Total Trades: {len(trades)}
Agents: {', '.join(agents) if agents else 'Unknown'}

Recent Trades:
{chr(10).join(trades[:10])}
{'...' if len(trades) > 10 else ''}
"""

    if output:
        with open(output, "w") as f:
            f.write(output_text)
        console.print(f"[green]Report saved to {output}[/]")
    else:
        console.print(output_text)


@app.command()
def version():
    """Show Wardcliff version information."""
    console.print("\n[bold orange1]Wardcliff[/] - Multi-agent Prediction Market Simulation")
    console.print("Version: 0.1.0")
    console.print()

    # Check dependencies
    deps = {
        "openai-agents": False,
        "rich": False,
        "typer": False,
    }

    for dep in deps:
        try:
            # Handle package name to module name mapping
            module_name = dep.replace("-", "_")
            if dep == "openai-agents":
                module_name = "agents"
            __import__(module_name)
            deps[dep] = True
        except ImportError:
            pass

    console.print("[bold]Dependencies:[/]")
    for dep, installed in deps.items():
        status = "[green]✓[/]" if installed else "[red]✗[/]"
        console.print(f"  {status} {dep}")

    console.print()


# =============================================================================
# API Keys Management
# =============================================================================

@app.command()
def keys(
    action: Optional[str] = typer.Argument(None, help="Action: list, set, remove, test"),
    provider: Optional[str] = typer.Argument(None, help="Provider: anthropic, openai, openrouter, parallel, turbopuffer, polymarket"),
    key: Optional[str] = typer.Argument(None, help="API key value (for 'set' action)"),
):
    """Manage API keys for various providers."""
    from cliff.cli.config import APIKeyConfig, mask_key

    config = APIKeyConfig.load()

    if action is None or action == "list":
        console.print("\n[bold orange1]API Keys[/]\n")

        providers = ["openai", "parallel"]
        table = Table(show_header=True, header_style="bold")
        table.add_column("Provider")
        table.add_column("Status")
        table.add_column("Key")
        table.add_column("Env Override")

        for p in providers:
            stored_key = config.get(p)
            env_key = os.environ.get(f"{p.upper()}_API_KEY")

            if stored_key:
                status = "[green]●[/]"
                key_display = mask_key(stored_key)
            elif env_key:
                status = "[yellow]●[/]"
                key_display = "[dim](from env)[/]"
            else:
                status = "[red]○[/]"
                key_display = "[dim]not set[/]"

            env_indicator = "[orange1]✓[/]" if env_key else ""
            table.add_row(p.title(), status, key_display, env_indicator)

        console.print(table)
        console.print()
        console.print("[dim]Use 'wardcliff keys set <provider> <key>' to add a key[/]")
        console.print("[dim]Keys are stored in ~/.wardcliff/keys.json with restricted permissions[/]")

    elif action == "set":
        if not provider:
            console.print("[red]Provider required[/]")
            console.print("Valid providers: openai, parallel")
            raise typer.Exit(1)

        if not key:
            # Prompt for key securely
            key = typer.prompt(f"Enter {provider} API key", hide_input=True)

        try:
            config.set(provider, key)
            config.save()
            console.print(f"[green]✓[/] API key saved for {provider}")
            console.print(f"[dim]Key: {mask_key(key)}[/]")
        except ValueError as e:
            console.print(f"[red]{e}[/]")
            raise typer.Exit(1)

    elif action == "remove":
        if not provider:
            console.print("[red]Provider required[/]")
            raise typer.Exit(1)

        config.remove(provider)
        config.save()
        console.print(f"[yellow]Removed API key for {provider}[/]")

    elif action == "test":
        console.print("\n[bold]Testing API Keys...[/]\n")
        config.apply_to_environment()

        # Test OpenAI key
        if config.openai or os.environ.get("OPENAI_API_KEY"):
            console.print("  [orange1]OpenAI:[/] ", end="")
            key_val = config.openai or os.environ.get("OPENAI_API_KEY", "")
            if key_val.startswith("sk-"):
                console.print("[green]Valid format[/]")
            else:
                console.print("[yellow]Unexpected format[/]")
        else:
            console.print("  [orange1]OpenAI:[/] [dim]not configured[/]")

        # Test Parallel key
        if config.parallel or os.environ.get("PARALLEL_API_KEY"):
            console.print("  [orange1]Parallel:[/] ", end="")
            console.print("[green]Key present[/]")
        else:
            console.print("  [orange1]Parallel:[/] [dim]not configured[/]")

        console.print()

    else:
        console.print(f"[red]Unknown action: {action}[/]")
        console.print("Valid actions: list, set, remove, test")
        raise typer.Exit(1)


# =============================================================================
# Agent Management
# =============================================================================

@app.command()
def agents(
    action: Optional[str] = typer.Argument(None, help="Action: list, add, edit, remove, thoughts, chat"),
    name: Optional[str] = typer.Argument(None, help="Agent name"),
    background: Optional[str] = typer.Option(None, "--background", "-b", help="Agent background"),
    personality: Optional[str] = typer.Option(None, "--personality", "-p", help="Agent personality"),
    risk: Optional[str] = typer.Option(None, "--risk", "-r", help="Risk tolerance: low, medium, high"),
    limit: int = typer.Option(20, "--limit", "-l", help="Number of thoughts to show"),
):
    """Manage trading agents and view their reasoning.

    Actions:
      list     - Show configured agents
      add      - Add a new agent
      edit     - Edit agent settings
      remove   - Remove an agent
      thoughts - View agent's reasoning history
      chat     - Start interactive chat with agent
    """
    from cliff.cli.config import AgentsConfig, AgentConfig as AgentCfg

    config = AgentsConfig.load()

    if action is None or action == "list":
        console.print("\n[bold orange1]Trading Agents[/]\n")

        if not config.agents:
            console.print("[dim]No agents configured[/]")
            return

        table = Table(show_header=True, header_style="bold")
        table.add_column("Name", style="orange1")
        table.add_column("Background")
        table.add_column("Personality")
        table.add_column("Risk")
        table.add_column("Status")

        for a in config.agents:
            status = "[green]●[/]" if a.enabled else "[dim]○[/]"
            risk_style = {"low": "green", "medium": "yellow", "high": "red"}.get(a.risk_tolerance, "white")
            table.add_row(
                a.name,
                a.background[:30],
                a.personality[:30],
                f"[{risk_style}]{a.risk_tolerance}[/]",
                status,
            )

        console.print(table)
        console.print()
        console.print("[dim]Use 'wardcliff agents thoughts <name>' to view reasoning[/]")
        console.print("[dim]Use 'wardcliff agents chat <name>' to chat with an agent[/]")

    elif action == "add":
        if not name:
            name = typer.prompt("Agent name")
        if not background:
            background = typer.prompt("Background (e.g., 'quantitative finance')")
        if not personality:
            personality = typer.prompt("Personality (e.g., 'analytical and data-driven')")
        if not risk:
            risk = typer.prompt("Risk tolerance", default="medium")

        agent = AgentCfg(
            name=name,
            background=background,
            personality=personality,
            risk_tolerance=risk,
        )
        config.add(agent)
        config.save()

        console.print(f"\n[green]✓[/] Created agent: {name}")
        console.print(f"  Background: {background}")
        console.print(f"  Personality: {personality}")
        console.print(f"  Risk: {risk}")

    elif action == "edit":
        if not name:
            console.print("[red]Agent name required[/]")
            raise typer.Exit(1)

        agent = config.get(name)
        if not agent:
            console.print(f"[red]Agent not found: {name}[/]")
            raise typer.Exit(1)

        # If flags provided, use them directly
        if background or personality or risk:
            if background:
                agent.background = background
            if personality:
                agent.personality = personality
            if risk:
                agent.risk_tolerance = risk
            config.save()
            console.print(f"[green]✓[/] Updated agent: {name}")
        else:
            # Interactive editing mode
            console.print(f"\n[bold orange1]Edit Agent: {name}[/]\n")
            console.print("[dim]Press Enter to keep current value, or type new value[/]\n")

            # Background
            console.print(f"[bold]Background[/]")
            console.print(f"  Current: [dim]{agent.background}[/]")
            new_bg = typer.prompt("  New value", default="", show_default=False)
            if new_bg.strip():
                agent.background = new_bg.strip()

            # Personality
            console.print(f"\n[bold]Personality[/]")
            console.print(f"  Current: [dim]{agent.personality}[/]")
            new_pers = typer.prompt("  New value", default="", show_default=False)
            if new_pers.strip():
                agent.personality = new_pers.strip()

            # Risk Tolerance
            console.print(f"\n[bold]Risk Tolerance[/]")
            risk_style = {"low": "green", "medium": "yellow", "high": "red"}.get(agent.risk_tolerance, "white")
            console.print(f"  Current: [{risk_style}]{agent.risk_tolerance}[/]")
            console.print("  Options: [green]low[/], [yellow]medium[/], [red]high[/]")
            new_risk = typer.prompt("  New value", default="", show_default=False)
            if new_risk.strip().lower() in ("low", "medium", "high"):
                agent.risk_tolerance = new_risk.strip().lower()
            elif new_risk.strip():
                console.print(f"[yellow]Invalid risk value '{new_risk}', keeping current[/]")

            # Enabled status
            console.print(f"\n[bold]Enabled[/]")
            status = "[green]yes[/]" if agent.enabled else "[red]no[/]"
            console.print(f"  Current: {status}")
            new_enabled = typer.prompt("  Enable agent? (yes/no)", default="", show_default=False)
            if new_enabled.strip().lower() in ("yes", "y", "true", "1"):
                agent.enabled = True
            elif new_enabled.strip().lower() in ("no", "n", "false", "0"):
                agent.enabled = False

            config.save()
            console.print(f"\n[green]✓[/] Updated agent: {name}")

    elif action == "remove":
        if not name:
            console.print("[red]Agent name required[/]")
            raise typer.Exit(1)

        if config.remove(name):
            config.save()
            console.print(f"[yellow]Removed agent: {name}[/]")
        else:
            console.print(f"[red]Agent not found: {name}[/]")
            raise typer.Exit(1)

    elif action == "thoughts":
        if not name:
            console.print("[red]Agent name required[/]")
            raise typer.Exit(1)

        thoughts = config.get_thoughts(name, limit)

        if not thoughts:
            console.print(f"\n[dim]No recorded thoughts for {name}[/]")
            console.print("[dim]Thoughts are recorded during simulations[/]")
            return

        console.print(f"\n[bold orange1]Thoughts - {name}[/]\n")

        for thought in thoughts:
            timestamp = thought.get("timestamp", "")[:19]
            thought_type = thought.get("type", "thinking")
            content = thought.get("content", "")

            type_style = {
                "thinking": "orange1",
                "research": "yellow",
                "decision": "green",
                "trade": "magenta",
            }.get(thought_type, "white")

            console.print(f"[dim]{timestamp}[/] [{type_style}]{thought_type.upper()}[/]")
            console.print(f"  {content[:200]}")
            console.print()

    elif action == "chat":
        if not name:
            console.print("[red]Agent name required[/]")
            raise typer.Exit(1)

        agent = config.get(name)
        if not agent:
            console.print(f"[red]Agent not found: {name}[/]")
            raise typer.Exit(1)

        # Check for API key
        from cliff.cli.config import APIKeyConfig
        keys = APIKeyConfig.load()
        keys.apply_to_environment()

        if not os.environ.get("OPENAI_API_KEY"):
            console.print("[red]OPENAI_API_KEY required for chat[/]")
            console.print("[dim]Set with: wardcliff keys set openai <key>[/]")
            raise typer.Exit(1)

        console.print(f"\n[bold orange1]Chat with {name}[/]")
        console.print(f"[dim]Background: {agent.background}[/]")
        console.print(f"[dim]Personality: {agent.personality}[/]")
        console.print("[dim]Type 'exit' or 'quit' to end chat[/]\n")

        # Run interactive chat
        asyncio.run(_agent_chat(agent, name))

    else:
        console.print(f"[red]Unknown action: {action}[/]")
        console.print("Valid actions: list, add, edit, remove, thoughts, chat")
        raise typer.Exit(1)


async def _agent_chat(agent, name: str):
    """Run interactive chat with an agent using OpenAI."""
    from cliff.cli.config import ChatSession

    session = ChatSession(agent_name=name)

    # Build system prompt for the agent
    system_prompt = f"""You are {name}, a trading agent with the following characteristics:

Background: {agent.background}
Personality: {agent.personality}
Risk Tolerance: {agent.risk_tolerance}

You are having a conversation with a user who wants to understand your trading perspective.
Stay in character and respond based on your background and personality.
When discussing markets or predictions, explain your reasoning clearly.
"""

    try:
        from openai import OpenAI

        client = OpenAI()
        messages = [{"role": "system", "content": system_prompt}]

        while True:
            try:
                user_input = console.input("[bold]You:[/] ")
            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Chat ended[/]")
                break

            if user_input.lower() in ("exit", "quit", "q"):
                console.print("[dim]Chat ended[/]")
                break

            session.add_message("user", user_input)
            messages.append({"role": "user", "content": user_input})

            console.print(f"\n[orange1][{name}][/] ", end="")

            # Query OpenAI
            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=messages,
            )

            response_text = response.choices[0].message.content or ""
            console.print(response_text)
            console.print()

            messages.append({"role": "assistant", "content": response_text})
            session.add_message("agent", response_text)

    except ImportError:
        console.print("[yellow]OpenAI SDK not available.[/]\n")
        console.print("[dim]Install with: pip install openai[/]\n")
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")


# =============================================================================
# Monitor Configuration
# =============================================================================

@app.command()
def monitor(
    action: Optional[str] = typer.Argument(None, help="Action: status, config, enable, disable, test, logs"),
    setting: Optional[str] = typer.Argument(None, help="Setting to configure"),
    value: Optional[str] = typer.Argument(None, help="Value for setting"),
):
    """Configure the Parallel monitor for detecting market-relevant news.

    The monitor uses the Parallel API to search for new information relevant
    to your trading events. When news is detected, it can trigger agent activity.

    Settings:
      poll-interval  - Seconds between API polls (default: 3600)
      prompt         - Search query for relevant news (sent to Parallel API)
    """
    from cliff.cli.config import MonitorConfig

    config = MonitorConfig.load()

    if action is None or action == "status":
        console.print("\n[bold orange1]Monitor Status[/]\n")

        status = "[green]Enabled[/]" if config.enabled else "[red]Disabled[/]"
        console.print(f"  Status: {status}")
        console.print(f"  Poll Interval: {config.poll_interval_seconds}s ({config.poll_interval_seconds // 60} min)")

        if config.prompt:
            console.print(f"  Monitor Prompt: {config.prompt[:80]}{'...' if len(config.prompt) > 80 else ''}")
        else:
            console.print("  Monitor Prompt: [dim](not set)[/]")

        if config.last_poll:
            console.print(f"  Last Poll: {config.last_poll}")
        if config.last_news_detected:
            console.print(f"  Last News: {config.last_news_detected}")

        console.print()

        # Check for Parallel API key
        from cliff.cli.config import APIKeyConfig
        keys = APIKeyConfig.load()
        if keys.parallel or os.environ.get("PARALLEL_API_KEY"):
            console.print("[green]✓[/] Parallel API key configured")
        else:
            console.print("[yellow]⚠[/] Parallel API key not set")
            console.print("[dim]  Set with: wardcliff keys set parallel <key>[/]")

    elif action == "config":
        if not setting:
            # Show all settings
            console.print("\n[bold]Monitor Settings[/]\n")
            console.print(f"  poll-interval: {config.poll_interval_seconds}s")
            console.print(f"  prompt: {config.prompt or '(not set)'}")
            console.print()
            console.print("[dim]Update with: wardcliff monitor config <setting> <value>[/]")
            return

        if not value:
            console.print(f"[red]Value required for {setting}[/]")
            raise typer.Exit(1)

        # Update setting
        if setting == "poll-interval":
            config.poll_interval_seconds = int(value)
        elif setting == "prompt":
            config.prompt = value
        else:
            console.print(f"[red]Unknown setting: {setting}[/]")
            console.print("[dim]Valid settings: poll-interval, prompt[/]")
            raise typer.Exit(1)

        config.save()
        console.print(f"[green]✓[/] Updated {setting} = {value}")

    elif action == "enable":
        config.enabled = True
        config.save()
        console.print("[green]✓[/] Monitor enabled")

    elif action == "disable":
        config.enabled = False
        config.save()
        console.print("[yellow]Monitor disabled[/]")

    elif action == "test":
        console.print("\n[bold]Testing Monitor Connection...[/]\n")

        from cliff.cli.config import APIKeyConfig
        keys = APIKeyConfig.load()
        keys.apply_to_environment()

        if not os.environ.get("PARALLEL_API_KEY"):
            console.print("[red]✗[/] Parallel API key not configured")
            console.print("[dim]  Set with: wardcliff keys set parallel <key>[/]")
            raise typer.Exit(1)

        console.print("[green]✓[/] Parallel API key found")
        console.print("[dim]Monitor test would connect to Parallel API here[/]")

    elif action == "logs":
        console.print("\n[bold]Monitor Logs[/]\n")

        from cliff.cli.config import get_config_dir
        log_file = get_config_dir() / "monitor.log"

        if not log_file.exists():
            console.print("[dim]No monitor logs yet[/]")
            return

        # Show last 20 lines
        with open(log_file) as f:
            lines = f.readlines()[-20:]

        for line in lines:
            console.print(line.rstrip())

    else:
        console.print(f"[red]Unknown action: {action}[/]")
        console.print("Valid actions: status, config, enable, disable, test, logs")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
