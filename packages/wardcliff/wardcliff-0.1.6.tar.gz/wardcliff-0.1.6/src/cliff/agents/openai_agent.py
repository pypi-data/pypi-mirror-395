"""
OpenAI Agents SDK Trading Agent for Prediction Markets.

This module provides an OpenAI Agents SDK-based trading agent. It uses native
@function_tool decorators for trading tools
and OpenAI's guardrails for validation.

Key features:
- Native @function_tool for 6 trading tools
- Input guardrails for trade validation and rate limiting
- Handoffs for specialized subagents (researcher, analyst)
- SQLiteSession for conversation persistence
- External MCP server support for 60+ enterprise integrations
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional
import uuid

from agents import Agent, Runner, function_tool, input_guardrail
from agents import GuardrailFunctionOutput, RunContextWrapper
from agents.run import RunConfig

# Import all available hosted tools from the OpenAI Agents SDK
try:
    from agents import WebSearchTool, CodeInterpreterTool, FileSearchTool
    HOSTED_TOOLS_AVAILABLE = True
except ImportError:
    HOSTED_TOOLS_AVAILABLE = False
    WebSearchTool = None
    CodeInterpreterTool = None
    FileSearchTool = None

# Import MCP support
try:
    from agents import HostedMCPTool
    from agents.mcp import MCPServerStdio, MCPServerStreamableHttp
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    HostedMCPTool = None
    MCPServerStdio = None
    MCPServerStreamableHttp = None

from cliff.core.events import EventMarket, PredictionMarketEvent, TradeResult as EventTradeResult
from cliff.core.market import Market

# Simulation logger for comprehensive output
try:
    from cliff.streaming.logger import get_simulation_logger
    SIMULATION_LOGGER_AVAILABLE = True
except ImportError:
    SIMULATION_LOGGER_AVAILABLE = False
    get_simulation_logger = lambda: None

logger = logging.getLogger(__name__)


# =============================================================================
# LIMIT ORDER TYPES
# =============================================================================

@dataclass
class LimitOrder:
    """
    A limit order that executes automatically when price conditions are met.

    Order types:
    - limit_buy: Buy when price drops TO or BELOW trigger_price
    - limit_sell: Sell when price rises TO or ABOVE trigger_price
    - stop_loss: Sell when price drops TO or BELOW trigger_price (cut losses)
    - take_profit: Sell when price rises TO or ABOVE trigger_price (lock in gains)
    """
    order_id: str
    agent_id: str
    outcome: str
    order_type: Literal["limit_buy", "limit_sell", "stop_loss", "take_profit"]
    trigger_price: float  # Price at which order triggers
    size: float  # USD for buys, tokens for sells
    rationale: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None  # Optional expiration
    status: Literal["pending", "filled", "cancelled", "expired"] = "pending"
    fill_price: Optional[float] = None  # Price at which order was filled
    filled_at: Optional[datetime] = None


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

@dataclass
class TradingAgentState:
    """
    Shared state for the trading agent.

    This holds all the mutable state that tools need access to:
    - Market/event market references
    - Portfolio tracking
    - Trade history
    - Market monitor for price alerts
    """
    # Market references
    event_market: Optional[EventMarket] = None
    market: Optional[Market] = None
    market_lock: Optional[asyncio.Lock] = None

    # Market monitor for price alerts
    market_monitor: Optional[Any] = None

    # Stream handler for live display updates
    stream_handler: Optional[Any] = None

    # Portfolio tracking
    initial_capital: float = 10000.0
    cash_balance: float = 10000.0
    portfolio: Dict[str, float] = field(default_factory=dict)
    cost_basis: Dict[str, float] = field(default_factory=dict)
    realized_pnl: float = 0.0

    # Trade history
    event_trade_log: List[EventTradeResult] = field(default_factory=list)

    # Limit orders (pending orders that execute on price triggers)
    pending_limit_orders: List[LimitOrder] = field(default_factory=list)
    filled_limit_orders: List[LimitOrder] = field(default_factory=list)

    # Agent identity
    agent_id: str = "openai_agent"

    # Rate limiting
    max_trades_per_minute: int = 10

    # Database IDs for persistence (optional)
    db_agent_id: Optional[str] = None
    db_market_id: Optional[str] = None

    def __post_init__(self):
        if self.market_lock is None:
            self.market_lock = asyncio.Lock()


# =============================================================================
# CONTEXT FOR GUARDRAILS AND TOOLS
# =============================================================================

@dataclass
class TradingContext:
    """Context passed to guardrails and available during agent runs."""
    state: TradingAgentState
    max_trades_per_minute: int = 10


# =============================================================================
# GUARDRAILS: Trade Validation & Rate Limiting
# =============================================================================

@input_guardrail
async def trade_rate_limit_guardrail(
    ctx: RunContextWrapper[TradingContext],
    agent: Agent,
    input_data: str | list,
) -> GuardrailFunctionOutput:
    """
    Validate trading rate limits before agent processes input.

    Triggers if more than max_trades_per_minute trades in the last 60 seconds.
    """
    state = ctx.context.state
    now = datetime.now(timezone.utc)

    # Count recent trades
    recent_trades = []
    for trade in state.event_trade_log:
        if hasattr(trade, 'timestamp'):
            trade_time = trade.timestamp
            if isinstance(trade_time, str):
                trade_time = datetime.fromisoformat(trade_time.replace('Z', '+00:00'))
            if (now - trade_time).total_seconds() < 60:
                recent_trades.append(trade)

    if len(recent_trades) >= ctx.context.max_trades_per_minute:
        logger.warning(
            "[GUARDRAIL] Rate limit triggered: %d trades in last minute (max: %d)",
            len(recent_trades), ctx.context.max_trades_per_minute
        )
        return GuardrailFunctionOutput(
            output_info={"rate_limited": True, "recent_trades": len(recent_trades)},
            tripwire_triggered=True,
        )

    return GuardrailFunctionOutput(
        output_info={"validated": True, "recent_trades": len(recent_trades)},
        tripwire_triggered=False,
    )


# =============================================================================
# TRADING TOOLS
# =============================================================================

def create_trading_tools(state: TradingAgentState):
    """
    Create native @function_tool trading tools with state access.

    Returns a list of tool functions that can be passed to Agent().
    """

    @function_tool
    async def get_portfolio() -> str:
        """Get current portfolio state including cash, positions, and P&L.

        Returns comprehensive portfolio status with:
        - Cash balance
        - All positions with current values
        - Unrealized and realized P&L
        - Return percentage
        """
        if not state.event_market:
            return json.dumps({"error": "No event market configured"})

        prices = state.event_market.get_prices()
        positions = []
        total_position_value = 0.0
        total_cost_basis = 0.0
        total_unrealized_pnl = 0.0

        for outcome, tokens in state.portfolio.items():
            if tokens <= 0:
                continue

            price = prices.get(outcome, 0.5)
            market_value = tokens * price
            cost = state.cost_basis.get(outcome, 0)
            unrealized_pnl = market_value - cost
            avg_entry_price = cost / tokens if tokens > 0 else 0
            position_return_pct = (unrealized_pnl / cost * 100) if cost > 0 else 0

            total_position_value += market_value
            total_cost_basis += cost
            total_unrealized_pnl += unrealized_pnl

            positions.append({
                "outcome": outcome,
                "tokens": round(tokens, 4),
                "avg_entry_price": round(avg_entry_price, 4),
                "current_price": round(price, 4),
                "cost_basis": round(cost, 2),
                "market_value": round(market_value, 2),
                "unrealized_pnl": round(unrealized_pnl, 2),
                "return_pct": round(position_return_pct, 2),
            })

        total_capital = state.cash_balance + total_position_value
        total_pnl = total_unrealized_pnl + state.realized_pnl
        return_pct = (total_pnl / state.initial_capital * 100) if state.initial_capital > 0 else 0
        pct_liquid = (state.cash_balance / total_capital * 100) if total_capital > 0 else 100

        portfolio_data = {
            "initial_capital": round(state.initial_capital, 2),
            "cash_balance": round(state.cash_balance, 2),
            "positions": positions,
            "total_position_value": round(total_position_value, 2),
            "total_capital": round(total_capital, 2),
            "total_cost_basis": round(total_cost_basis, 2),
            "unrealized_pnl": round(total_unrealized_pnl, 2),
            "realized_pnl": round(state.realized_pnl, 2),
            "total_pnl": round(total_pnl, 2),
            "return_pct": round(return_pct, 2),
            "pct_liquid": round(pct_liquid, 2),
            "trade_count": len(state.event_trade_log),
        }

        return json.dumps(portfolio_data, indent=2)

    @function_tool
    async def get_price_history(limit: int = 50) -> str:
        """Get recent trades and price history from the market.

        Args:
            limit: Maximum number of trades to return (default 50)

        Returns:
            JSON with recent trades and current prices
        """
        if state.event_market:
            history = []
            for trade in state.event_trade_log[-limit:]:
                history.append({
                    "timestamp": trade.timestamp.isoformat() if hasattr(trade, 'timestamp') else datetime.now(timezone.utc).isoformat(),
                    "agent_id": trade.agent_id,
                    "outcome": trade.outcome,
                    "direction": trade.direction,
                    "price": round(trade.price, 4),
                    "token_delta": round(trade.token_delta, 4),
                    "quote_delta": round(trade.quote_delta, 4),
                })

            current_prices = state.event_market.get_prices()

            return json.dumps({
                "recent_trades": history,
                "current_prices": {k: round(v, 4) for k, v in current_prices.items()},
                "total_trades": len(state.event_trade_log),
            }, indent=2)

        elif state.market:
            history = state.market.get_price_history(limit)
            return json.dumps(history, indent=2)

        return json.dumps({"error": "No market configured"})

    @function_tool
    async def place_trade(outcome: str, action: str, size: float, rationale: str) -> str:
        """Execute a trade on the prediction market.

        CRITICAL: Always call get_latest_prices() before placing a trade!

        Args:
            outcome: Which outcome to trade (e.g., 'Kansas City Chiefs')
            action: 'buy' or 'sell'
            size: Amount in USD (for buys) or tokens (for sells)
            rationale: REQUIRED - A detailed investment memo explaining your thesis.
                      Must include: (1) your analysis, (2) why the price is wrong,
                      (3) expected outcome. Minimum 50 characters.

        Returns:
            JSON with trade execution details or error
        """
        # Validate rationale is provided and meaningful (requires proper investment memo)
        if not rationale or len(rationale.strip()) < 50:
            return json.dumps({
                "error": "Investment memo required (min 50 chars). Include: analysis, mispricing thesis, and expected outcome."
            })

        if not state.event_market:
            return json.dumps({"error": "No event market configured"})

        if action not in {"buy", "sell"}:
            return json.dumps({"error": f"Invalid action '{action}'. Must be 'buy' or 'sell'."})

        if size <= 0:
            return json.dumps({"error": f"Invalid size {size}. Must be positive."})

        # Validate outcome
        valid_outcomes = state.event_market.event.outcomes
        if outcome not in valid_outcomes:
            return json.dumps({"error": f"Invalid outcome '{outcome}'. Valid: {valid_outcomes}"})

        # Check cash for buys
        if action == "buy" and size > state.cash_balance:
            return json.dumps({
                "error": f"Insufficient funds. Want to spend ${size:.2f} but only have ${state.cash_balance:.2f} cash."
            })

        # Check tokens for sells
        if action == "sell":
            current_tokens = state.portfolio.get(outcome, 0)
            if size > current_tokens:
                return json.dumps({
                    "error": f"Insufficient tokens. Want to sell {size:.4f} but only have {current_tokens:.4f} {outcome} tokens."
                })

        # Enforce max trade size (50% of cash)
        max_trade_size = state.cash_balance * 0.5
        original_size = size
        if action == "buy" and size > max_trade_size:
            logger.warning(
                "[TOOL] Trade size %.2f exceeds 50%% limit (%.2f). Reducing.",
                size, max_trade_size
            )
            size = max_trade_size
            rationale = f"[SIZE REDUCED from {original_size:.2f}] {rationale}"

        # Execute trade with price tracking
        try:
            async with state.market_lock:
                # Capture price BEFORE trade
                prices_before = state.event_market.get_prices()
                price_before = prices_before.get(outcome, 0.5)

                logger.info("Pre-trade price for %s: %.4f", outcome, price_before)

                # Execute trade
                execution = state.event_market.swap(
                    agent_id=state.agent_id,
                    outcome=outcome,
                    direction=action,
                    amount=size,
                    note=rationale,
                )

                # Capture price AFTER trade
                prices_after = state.event_market.get_prices()
                price_after = prices_after.get(outcome, 0.5)

                # Calculate slippage
                if price_before > 0:
                    actual_slippage = abs(price_after - price_before) / price_before
                else:
                    actual_slippage = 0.0

                logger.info(
                    "Post-trade price for %s: %.4f (slippage: %.2f%%)",
                    outcome, price_after, actual_slippage * 100
                )

                # Update market monitor if available
                if state.market_monitor:
                    state.market_monitor.record_trade_prices(str(execution.timestamp))
                    # Record trade for alert attribution
                    state.market_monitor.record_trade(
                        agent_id=state.agent_id,
                        outcome=outcome,
                        direction=action,
                        size_usd=size if action == "buy" else abs(execution.quote_delta),
                        price=execution.price,
                    )
                    state.market_monitor.on_trade(
                        agent_id=state.agent_id,
                        outcome=outcome,
                        direction=action,
                        size=size,
                        price=execution.price,
                    )

                # Log trade to simulation logger
                sim_logger = get_simulation_logger()
                if sim_logger:
                    sim_logger.trade(
                        agent_id=state.agent_id,
                        outcome=outcome,
                        action=action,
                        size=size,
                        price_before=price_before,
                        price_after=price_after,
                        rationale=rationale,
                    )

                # Emit trade event to stream handler for live display
                if state.stream_handler:
                    slippage = abs(price_after - price_before) / price_before if price_before > 0 else 0
                    state.stream_handler.emit_trade(
                        agent_id=state.agent_id,
                        outcome=outcome,
                        action=action,
                        size=size,
                        price=price_after,
                        rationale=rationale,
                        slippage=slippage,
                    )
                    # Also emit price update after trade
                    prices_after = state.event_market.get_prices()
                    state.stream_handler.emit_price_update(prices_after)

        except Exception as e:
            logger.error("Trade execution failed: %s", str(e))
            return json.dumps({"error": f"Trade failed: {str(e)}"})

        # Update portfolio tracking
        if action == "buy":
            cash_spent = abs(execution.quote_delta)
            state.cash_balance -= cash_spent
            state.portfolio[outcome] = state.portfolio.get(outcome, 0) + execution.token_delta
            state.cost_basis[outcome] = state.cost_basis.get(outcome, 0) + cash_spent

        elif action == "sell":
            cash_received = execution.quote_delta
            state.cash_balance += cash_received

            tokens_sold = abs(execution.token_delta)
            current_tokens = state.portfolio.get(outcome, 0)
            current_cost = state.cost_basis.get(outcome, 0)

            if current_tokens > 0:
                avg_cost_per_token = current_cost / current_tokens
                cost_of_sold_tokens = avg_cost_per_token * tokens_sold
                realized_gain = cash_received - cost_of_sold_tokens
                state.realized_pnl += realized_gain
                state.cost_basis[outcome] = current_cost - cost_of_sold_tokens

            state.portfolio[outcome] = current_tokens - tokens_sold

        # Log trade
        state.event_trade_log.append(execution)

        # Emit portfolio update for P&L tracking
        if state.stream_handler:
            # Calculate total portfolio value
            total_value = state.cash_balance
            for out, tokens in state.portfolio.items():
                if tokens > 0 and out in prices_after:
                    total_value += tokens * prices_after[out]
            # Calculate P&L
            pnl = total_value - state.initial_capital
            state.stream_handler.emit_portfolio_update(
                agent_id=state.agent_id,
                total_value=total_value,
                cash=state.cash_balance,
                pnl=pnl,
            )

        logger.info(
            "Agent %s executed trade: %s %s %s @ price_before=%.4f price_after=%.4f size=%.2f slippage=%.2f%%",
            state.agent_id, action.upper(), outcome, state.event_market.event.name,
            price_before, price_after, size, actual_slippage * 100
        )

        return json.dumps({
            "trade_executed": True,
            "outcome": outcome,
            "action": action,
            "size": size,
            "price_before": round(price_before, 4),
            "price_after": round(price_after, 4),
            "slippage": round(actual_slippage, 4),
            "execution_price": round(execution.price, 4),
            "token_delta": round(execution.token_delta, 4),
            "quote_delta": round(execution.quote_delta, 4),
            "rationale": rationale,
            "all_prices_after": {k: round(v, 4) for k, v in prices_after.items()},
            "cash_balance": round(state.cash_balance, 2),
        }, indent=2)

    @function_tool
    async def get_latest_prices() -> str:
        """Get current market prices. ALWAYS call this before placing a trade!

        Returns:
            JSON with current prices for all outcomes and timestamp
        """
        if not state.event_market:
            return json.dumps({"error": "No event market configured"})

        prices = state.event_market.get_prices()

        return json.dumps({
            "prices": {k: round(v, 4) for k, v in prices.items()},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "market_name": state.event_market.event.name,
            "outcomes": state.event_market.event.outcomes,
        }, indent=2)

    @function_tool
    async def configure_alerts(
        outcome: str,
        conditions: str,
        rationale: str
    ) -> str:
        """Configure custom alert conditions for an outcome. Alerts will INTERRUPT your turn when triggered.

        Use this after analyzing the market to set up monitoring while you research.
        When conditions are met, you'll see a detailed alert at the START of your next turn.

        ONE-SHOT BEHAVIOR: Alerts trigger once then auto-deactivate. Set new alerts after reviewing.

        Args:
            outcome: Which outcome to monitor (e.g., 'Kansas City Chiefs', 'YES')
            conditions: JSON object with alert conditions. Available conditions:
                {
                    "price_above": 0.45,      // Alert if price rises ABOVE this
                    "price_below": 0.25,      // Alert if price drops BELOW this
                    "change_pct": 0.05,       // Alert on 5% move in either direction from current price
                    "large_trade_usd": 1000,  // Alert on trades > $1000 by other agents
                    "any_trade": true         // Alert on any trade by other agents (for illiquid markets)
                }
            rationale: Why you're setting these alerts (helps you remember context when it triggers)

        Returns:
            JSON with confirmation of configured alerts

        Example:
            configure_alerts(
                outcome="YES",
                conditions='{"price_below": 0.30, "change_pct": 0.08}',
                rationale="Bought at $0.35, want to know if thesis breaking or big move"
            )
        """
        if not state.market_monitor:
            return json.dumps({
                "error": "No market monitor available",
                "configured": False,
            })

        if not state.event_market:
            return json.dumps({"error": "No event market configured"})

        # Validate outcome
        valid_outcomes = state.event_market.event.outcomes
        if outcome not in valid_outcomes:
            return json.dumps({"error": f"Invalid outcome '{outcome}'. Valid: {valid_outcomes}"})

        # Parse conditions
        try:
            cond_dict = json.loads(conditions)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON in conditions: {str(e)}"})

        # Validate conditions
        valid_keys = {"price_above", "price_below", "change_pct", "large_trade_usd", "any_trade"}
        for key in cond_dict:
            if key not in valid_keys:
                return json.dumps({"error": f"Unknown condition '{key}'. Valid: {valid_keys}"})

        if not cond_dict:
            return json.dumps({"error": "Must specify at least one condition"})

        # Register the alert
        alert_config = state.market_monitor.register_agent_alert(
            agent_id=state.agent_id,
            outcome=outcome,
            conditions=cond_dict,
            rationale=rationale,
        )

        logger.info("Agent %s configured alert for %s: %s", state.agent_id, outcome, cond_dict)

        current_price = state.event_market.get_prices().get(outcome, 0)

        return json.dumps({
            "configured": True,
            "outcome": outcome,
            "conditions": cond_dict,
            "rationale": rationale,
            "baseline_price": round(current_price, 4),
            "message": f"Alert configured for {outcome}. You will be interrupted when conditions are met.",
            "behavior": "ONE-SHOT: Alert will trigger once, then deactivate. Set new alerts after reviewing.",
        }, indent=2)

    @function_tool
    async def get_active_alerts() -> str:
        """See your currently active alert configurations.

        Shows all alerts you've configured that haven't triggered yet.

        Returns:
            JSON list of active alerts with their conditions and status
        """
        if not state.market_monitor:
            return json.dumps({
                "alerts": [],
                "message": "No market monitor available"
            })

        active = state.market_monitor.get_active_alerts_for_agent(state.agent_id)

        if not active:
            return json.dumps({
                "alerts": [],
                "count": 0,
                "message": "No active alerts. Use configure_alerts() to set up monitoring."
            })

        # Get current prices for context
        current_prices = state.event_market.get_prices() if state.event_market else {}

        alert_list = []
        for alert in active:
            current = current_prices.get(alert.outcome, 0)
            alert_list.append({
                "outcome": alert.outcome,
                "conditions": alert.conditions,
                "rationale": alert.rationale[:50] + "..." if len(alert.rationale) > 50 else alert.rationale,
                "baseline_price": round(alert.baseline_price, 4) if alert.baseline_price else None,
                "current_price": round(current, 4),
                "created_at": alert.created_at.isoformat(),
            })

        return json.dumps({
            "alerts": alert_list,
            "count": len(alert_list),
            "message": f"You have {len(alert_list)} active alert(s) monitoring the market."
        }, indent=2)

    @function_tool
    async def cancel_alert(outcome: str) -> str:
        """Cancel an active alert for an outcome.

        Use this if you no longer want to be alerted about an outcome.

        Args:
            outcome: Which outcome's alert to cancel

        Returns:
            JSON with cancellation confirmation
        """
        if not state.market_monitor:
            return json.dumps({"error": "No market monitor available"})

        cancelled = state.market_monitor.cancel_agent_alert(state.agent_id, outcome)

        if cancelled:
            logger.info("Agent %s cancelled alert for %s", state.agent_id, outcome)
            return json.dumps({
                "cancelled": True,
                "outcome": outcome,
                "message": f"Alert for {outcome} has been cancelled."
            })
        else:
            return json.dumps({
                "cancelled": False,
                "outcome": outcome,
                "message": f"No active alert found for {outcome}."
            })

    # =========================================================================
    # LIMIT ORDER HELPER FUNCTION
    # =========================================================================

    async def check_and_execute_limit_orders() -> List[Dict]:
        """
        Check all pending limit orders and execute any that have triggered.
        Returns list of executed orders.
        """
        if not state.event_market:
            return []

        executed = []
        current_prices = state.event_market.get_prices()
        now = datetime.now(timezone.utc)

        # Check each pending order
        orders_to_remove = []
        for order in state.pending_limit_orders:
            if order.status != "pending":
                continue

            # Check expiration
            if order.expires_at and now > order.expires_at:
                order.status = "expired"
                orders_to_remove.append(order)
                logger.info("[LIMIT] Order %s expired", order.order_id[:8])
                continue

            current_price = current_prices.get(order.outcome, 0)
            should_trigger = False

            # Check trigger conditions
            if order.order_type == "limit_buy":
                # Buy when price drops to or below trigger
                should_trigger = current_price <= order.trigger_price
            elif order.order_type in ("limit_sell", "take_profit"):
                # Sell when price rises to or above trigger
                should_trigger = current_price >= order.trigger_price
            elif order.order_type == "stop_loss":
                # Sell when price drops to or below trigger
                should_trigger = current_price <= order.trigger_price

            if should_trigger:
                logger.info(
                    "[LIMIT] Triggering %s order %s: %s @ %.4f (current: %.4f)",
                    order.order_type, order.order_id[:8], order.outcome,
                    order.trigger_price, current_price
                )

                # Determine action based on order type
                action = "buy" if order.order_type == "limit_buy" else "sell"

                # Validate we can still execute
                can_execute = True
                if action == "buy" and order.size > state.cash_balance:
                    logger.warning("[LIMIT] Order %s failed: insufficient cash", order.order_id[:8])
                    can_execute = False
                elif action == "sell":
                    current_tokens = state.portfolio.get(order.outcome, 0)
                    if order.size > current_tokens:
                        logger.warning("[LIMIT] Order %s failed: insufficient tokens", order.order_id[:8])
                        can_execute = False

                if can_execute:
                    try:
                        # Execute the trade
                        execution = state.event_market.swap(
                            agent_id=state.agent_id,
                            outcome=order.outcome,
                            direction=action,
                            amount=order.size,
                            note=f"[LIMIT ORDER {order.order_type}] {order.rationale}",
                        )

                        # Update portfolio
                        if action == "buy":
                            cash_spent = abs(execution.quote_delta)
                            state.cash_balance -= cash_spent
                            state.portfolio[order.outcome] = state.portfolio.get(order.outcome, 0) + execution.token_delta
                            state.cost_basis[order.outcome] = state.cost_basis.get(order.outcome, 0) + cash_spent
                        else:
                            cash_received = execution.quote_delta
                            state.cash_balance += cash_received
                            tokens_sold = abs(execution.token_delta)
                            current_tokens = state.portfolio.get(order.outcome, 0)
                            current_cost = state.cost_basis.get(order.outcome, 0)
                            if current_tokens > 0:
                                avg_cost_per_token = current_cost / current_tokens
                                cost_of_sold_tokens = avg_cost_per_token * tokens_sold
                                realized_gain = cash_received - cost_of_sold_tokens
                                state.realized_pnl += realized_gain
                                state.cost_basis[order.outcome] = current_cost - cost_of_sold_tokens
                            state.portfolio[order.outcome] = current_tokens - tokens_sold

                        # Log trade
                        state.event_trade_log.append(execution)

                        # Update order status
                        order.status = "filled"
                        order.fill_price = execution.price
                        order.filled_at = now
                        state.filled_limit_orders.append(order)
                        orders_to_remove.append(order)

                        executed.append({
                            "order_id": order.order_id,
                            "order_type": order.order_type,
                            "outcome": order.outcome,
                            "trigger_price": order.trigger_price,
                            "fill_price": execution.price,
                            "size": order.size,
                            "action": action,
                        })

                        logger.info(
                            "[LIMIT] Order %s FILLED: %s %s %.2f @ %.4f",
                            order.order_id[:8], action.upper(), order.outcome,
                            order.size, execution.price
                        )

                        # Log to simulation logger
                        sim_logger = get_simulation_logger()
                        if sim_logger:
                            sim_logger.order_fill(
                                agent_id=state.agent_id,
                                order_id=order.order_id,
                                order_type=order.order_type,
                                outcome=order.outcome,
                                fill_price=execution.price,
                                size=order.size,
                            )

                    except Exception as e:
                        logger.error("[LIMIT] Order %s execution failed: %s", order.order_id[:8], str(e))
                        order.status = "cancelled"
                        orders_to_remove.append(order)

        # Remove processed orders from pending list
        for order in orders_to_remove:
            if order in state.pending_limit_orders:
                state.pending_limit_orders.remove(order)

        return executed

    # =========================================================================
    # LIMIT ORDER TOOLS
    # =========================================================================

    @function_tool
    async def place_limit_order(
        outcome: str,
        order_type: str,
        trigger_price: float,
        amount: float,
        rationale: str
    ) -> str:
        """Place a limit order that executes automatically when price conditions are met.

        Use this to set take-profit, stop-loss, or opportunistic entry orders that
        will execute even when it's not your turn to trade.

        Args:
            outcome: Which outcome to trade (e.g., 'Team A')
            order_type: One of:
                - 'limit_buy': Buy when price drops TO or BELOW trigger_price
                - 'limit_sell': Sell when price rises TO or ABOVE trigger_price
                - 'stop_loss': Sell when price drops TO or BELOW trigger_price
                - 'take_profit': Sell when price rises TO or ABOVE trigger_price
            trigger_price: Price at which order triggers (0.0 to 1.0)
            amount:
                - For limit_buy: USD amount to spend (e.g., 500 means spend $500)
                - For limit_sell/stop_loss/take_profit: NUMBER OF TOKENS to sell (e.g., 50 means sell 50 tokens)
            rationale: Brief explanation for the order

        Returns:
            JSON with order confirmation or error

        Examples:
            # Buy $500 worth if price drops to 0.25
            place_limit_order("Team A", "limit_buy", 0.25, 500, "Buy the dip")

            # Sell 50 tokens if price rises to 0.45 (take profit)
            place_limit_order("Team A", "take_profit", 0.45, 50, "Lock in gains")

            # Sell 50 tokens if price drops to 0.20 (stop loss)
            place_limit_order("Team A", "stop_loss", 0.20, 50, "Cut losses")
        """
        if not state.event_market:
            return json.dumps({"error": "No event market configured"})

        # Validate order type
        valid_types = {"limit_buy", "limit_sell", "stop_loss", "take_profit"}
        if order_type not in valid_types:
            return json.dumps({
                "error": f"Invalid order_type '{order_type}'. Must be one of: {valid_types}"
            })

        # Validate outcome
        valid_outcomes = state.event_market.event.outcomes
        if outcome not in valid_outcomes:
            return json.dumps({"error": f"Invalid outcome '{outcome}'. Valid: {valid_outcomes}"})

        # Validate trigger price
        if trigger_price <= 0 or trigger_price >= 1:
            return json.dumps({"error": f"Invalid trigger_price {trigger_price}. Must be between 0 and 1."})

        # Validate amount
        if amount <= 0:
            return json.dumps({"error": f"Invalid amount {amount}. Must be positive."})

        # For buy orders, check cash availability
        if order_type == "limit_buy" and amount > state.cash_balance:
            return json.dumps({
                "error": f"Insufficient funds. Order requires ${amount:.2f} but only have ${state.cash_balance:.2f} cash.",
                "suggestion": "Reduce amount or wait for funds"
            })

        # For sell orders, check token availability (amount = number of tokens)
        if order_type in ("limit_sell", "stop_loss", "take_profit"):
            current_tokens = state.portfolio.get(outcome, 0)
            if amount > current_tokens:
                return json.dumps({
                    "error": f"Insufficient tokens. Order requires {amount:.4f} tokens but only have {current_tokens:.4f} {outcome} tokens.",
                    "suggestion": "Reduce token amount or buy more tokens first"
                })

        # Get current price for context
        current_prices = state.event_market.get_prices()
        current_price = current_prices.get(outcome, 0)

        # Validate order makes sense
        if order_type == "limit_buy" and trigger_price >= current_price:
            return json.dumps({
                "warning": f"Trigger price {trigger_price:.4f} >= current price {current_price:.4f}. "
                           "This limit_buy will trigger immediately. Use place_trade for immediate execution.",
                "suggestion": "Set trigger_price below current price, or use place_trade"
            })

        if order_type in ("limit_sell", "take_profit") and trigger_price <= current_price:
            return json.dumps({
                "warning": f"Trigger price {trigger_price:.4f} <= current price {current_price:.4f}. "
                           "This sell order will trigger immediately. Use place_trade for immediate execution.",
                "suggestion": "Set trigger_price above current price, or use place_trade"
            })

        if order_type == "stop_loss" and trigger_price >= current_price:
            return json.dumps({
                "warning": f"Trigger price {trigger_price:.4f} >= current price {current_price:.4f}. "
                           "Stop-loss should be BELOW current price to limit losses.",
                "suggestion": "Set trigger_price below current price"
            })

        # Create the order (internally stored as 'size')
        order = LimitOrder(
            order_id=str(uuid.uuid4()),
            agent_id=state.agent_id,
            outcome=outcome,
            order_type=order_type,
            trigger_price=trigger_price,
            size=amount,  # amount is USD for buys, tokens for sells
            rationale=rationale,
        )

        state.pending_limit_orders.append(order)

        logger.info(
            "[LIMIT] Agent %s placed %s order: %s @ %.4f (current: %.4f) amount=%.2f",
            state.agent_id, order_type, outcome, trigger_price, current_price, amount
        )

        # Log to simulation logger
        sim_logger = get_simulation_logger()
        if sim_logger:
            sim_logger.limit_order(
                agent_id=state.agent_id,
                order_type=order_type,
                outcome=outcome,
                trigger_price=trigger_price,
                size=amount,
                order_id=order.order_id,
            )

        # Build descriptive response
        is_buy = order_type == "limit_buy"
        amount_desc = f"${amount:.2f} USD" if is_buy else f"{amount:.2f} tokens"

        return json.dumps({
            "order_placed": True,
            "order_id": order.order_id,
            "order_type": order_type,
            "outcome": outcome,
            "trigger_price": round(trigger_price, 4),
            "current_price": round(current_price, 4),
            "amount": round(amount, 4),
            "amount_type": "usd" if is_buy else "tokens",
            "rationale": rationale,
            "status": "pending",
            "message": f"Order will {'buy' if is_buy else 'sell'} {amount_desc} of {outcome} when price {'drops to' if order_type in ('limit_buy', 'stop_loss') else 'rises to'} {trigger_price:.4f}"
        }, indent=2)

    @function_tool
    async def get_pending_orders() -> str:
        """Get all pending limit orders for this agent.

        Returns:
            JSON with list of pending orders and their status
        """
        if not state.event_market:
            return json.dumps({"error": "No event market configured"})

        current_prices = state.event_market.get_prices()

        pending = []
        for order in state.pending_limit_orders:
            if order.status == "pending":
                current_price = current_prices.get(order.outcome, 0)
                distance = abs(current_price - order.trigger_price)
                distance_pct = (distance / current_price * 100) if current_price > 0 else 0

                pending.append({
                    "order_id": order.order_id[:8] + "...",
                    "order_type": order.order_type,
                    "outcome": order.outcome,
                    "trigger_price": round(order.trigger_price, 4),
                    "current_price": round(current_price, 4),
                    "distance_pct": round(distance_pct, 2),
                    "size": round(order.size, 4),
                    "rationale": order.rationale[:50] + "..." if len(order.rationale) > 50 else order.rationale,
                    "created_at": order.created_at.isoformat(),
                })

        recently_filled = []
        for order in state.filled_limit_orders[-5:]:  # Last 5 filled
            recently_filled.append({
                "order_id": order.order_id[:8] + "...",
                "order_type": order.order_type,
                "outcome": order.outcome,
                "trigger_price": round(order.trigger_price, 4),
                "fill_price": round(order.fill_price, 4) if order.fill_price else None,
                "size": round(order.size, 4),
                "filled_at": order.filled_at.isoformat() if order.filled_at else None,
            })

        return json.dumps({
            "pending_orders": pending,
            "pending_count": len(pending),
            "recently_filled": recently_filled,
            "message": f"You have {len(pending)} pending limit order(s)"
        }, indent=2)

    @function_tool
    async def cancel_order(order_id: str) -> str:
        """Cancel a pending limit order.

        Args:
            order_id: The order ID (or first 8 characters) to cancel

        Returns:
            JSON with cancellation confirmation or error
        """
        # Find the order (match full ID or prefix)
        target_order = None
        for order in state.pending_limit_orders:
            if order.order_id == order_id or order.order_id.startswith(order_id):
                target_order = order
                break

        if not target_order:
            return json.dumps({
                "error": f"Order not found: {order_id}",
                "pending_orders": len(state.pending_limit_orders)
            })

        if target_order.status != "pending":
            return json.dumps({
                "error": f"Order {order_id} is not pending (status: {target_order.status})"
            })

        # Cancel the order
        target_order.status = "cancelled"
        state.pending_limit_orders.remove(target_order)

        logger.info("[LIMIT] Order %s cancelled by agent", target_order.order_id[:8])

        return json.dumps({
            "cancelled": True,
            "order_id": target_order.order_id,
            "order_type": target_order.order_type,
            "outcome": target_order.outcome,
            "trigger_price": round(target_order.trigger_price, 4),
            "size": round(target_order.size, 4),
            "message": "Order cancelled successfully"
        }, indent=2)

    @function_tool
    async def place_bracket_orders(
        outcome: str,
        take_profits: str,
        stop_losses: str,
        rationale: str
    ) -> str:
        """Place multiple take-profit and stop-loss orders at once (bracket orders).

        This is the recommended way to protect a position - set multiple exit levels
        in a single call. Each take-profit/stop-loss specifies a price and number of TOKENS to sell.

        Args:
            outcome: Which outcome to set orders for (e.g., 'Team A')
            take_profits: JSON array of take-profit levels with 'price' and 'tokens' (number of tokens to sell)
                Example: '[{"price": 0.45, "tokens": 30}, {"price": 0.55, "tokens": 20}]'
            stop_losses: JSON array of stop-loss levels with 'price' and 'tokens' (number of tokens to sell)
                Example: '[{"price": 0.20, "tokens": 25}, {"price": 0.15, "tokens": 25}]'
            rationale: Overall reasoning for this bracket strategy

        Returns:
            JSON with all orders placed or errors

        Example:
            place_bracket_orders(
                outcome="Team A",
                take_profits='[{"price": 0.40, "tokens": 30}, {"price": 0.50, "tokens": 30}, {"price": 0.60, "tokens": 40}]',
                stop_losses='[{"price": 0.25, "tokens": 50}, {"price": 0.18, "tokens": 50}]',
                rationale="Scale out at 3 profit targets, 2-tier stop loss"
            )
            # This sells 30 tokens at $0.40, 30 at $0.50, 40 at $0.60 (take profits)
            # Or sells 50 tokens at $0.25, 50 at $0.18 if price drops (stop losses)
        """
        if not state.event_market:
            return json.dumps({"error": "No event market configured"})

        # Validate outcome
        valid_outcomes = state.event_market.event.outcomes
        if outcome not in valid_outcomes:
            return json.dumps({"error": f"Invalid outcome '{outcome}'. Valid: {valid_outcomes}"})

        # Parse take_profits and stop_losses
        try:
            tp_list = json.loads(take_profits) if take_profits else []
            sl_list = json.loads(stop_losses) if stop_losses else []
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON format: {str(e)}"})

        if not tp_list and not sl_list:
            return json.dumps({"error": "Must specify at least one take_profit or stop_loss"})

        # Validate structure - accept both 'tokens' and 'size' for backwards compatibility
        for i, tp in enumerate(tp_list):
            if not isinstance(tp, dict) or "price" not in tp:
                return json.dumps({"error": f"take_profits[{i}] must have 'price' field"})
            if "tokens" not in tp and "size" not in tp:
                return json.dumps({"error": f"take_profits[{i}] must have 'tokens' field (number of tokens to sell)"})
            # Normalize to 'tokens'
            if "size" in tp and "tokens" not in tp:
                tp["tokens"] = tp["size"]
        for i, sl in enumerate(sl_list):
            if not isinstance(sl, dict) or "price" not in sl:
                return json.dumps({"error": f"stop_losses[{i}] must have 'price' field"})
            if "tokens" not in sl and "size" not in sl:
                return json.dumps({"error": f"stop_losses[{i}] must have 'tokens' field (number of tokens to sell)"})
            # Normalize to 'tokens'
            if "size" in sl and "tokens" not in sl:
                sl["tokens"] = sl["size"]

        # Get current price
        current_prices = state.event_market.get_prices()
        current_price = current_prices.get(outcome, 0)

        # Calculate total tokens needed
        total_tp_tokens = sum(tp["tokens"] for tp in tp_list)
        total_sl_tokens = sum(sl["tokens"] for sl in sl_list)
        current_tokens = state.portfolio.get(outcome, 0)

        # Validate we have enough tokens (check max of tp/sl since they're mutually exclusive exits)
        max_required = max(total_tp_tokens, total_sl_tokens) if tp_list and sl_list else (total_tp_tokens or total_sl_tokens)
        if max_required > current_tokens:
            return json.dumps({
                "error": f"Insufficient tokens. Need {max_required:.2f} tokens but have {current_tokens:.2f}",
                "take_profit_total_tokens": total_tp_tokens,
                "stop_loss_total_tokens": total_sl_tokens,
                "current_tokens": current_tokens
            })

        # Validate take-profit prices are above current
        for tp in tp_list:
            if tp["price"] <= current_price:
                return json.dumps({
                    "error": f"Take-profit price {tp['price']:.4f} must be above current price {current_price:.4f}"
                })

        # Validate stop-loss prices are below current
        for sl in sl_list:
            if sl["price"] >= current_price:
                return json.dumps({
                    "error": f"Stop-loss price {sl['price']:.4f} must be below current price {current_price:.4f}"
                })

        # Place all orders
        placed_orders = []

        for tp in tp_list:
            order = LimitOrder(
                order_id=str(uuid.uuid4()),
                agent_id=state.agent_id,
                outcome=outcome,
                order_type="take_profit",
                trigger_price=tp["price"],
                size=tp["tokens"],  # internally stored as 'size'
                rationale=f"{rationale} [TP @ {tp['price']:.2f}]",
            )
            state.pending_limit_orders.append(order)
            placed_orders.append({
                "order_id": order.order_id[:8] + "...",
                "type": "take_profit",
                "price": tp["price"],
                "tokens": tp["tokens"]
            })
            logger.info(
                "[BRACKET] %s: take_profit %s @ %.4f tokens=%.2f",
                state.agent_id, outcome, tp["price"], tp["tokens"]
            )
            # Log to simulation logger
            sim_logger = get_simulation_logger()
            if sim_logger:
                sim_logger.limit_order(
                    agent_id=state.agent_id,
                    order_type="take_profit",
                    outcome=outcome,
                    trigger_price=tp["price"],
                    size=tp["tokens"],
                    order_id=order.order_id,
                )

        for sl in sl_list:
            order = LimitOrder(
                order_id=str(uuid.uuid4()),
                agent_id=state.agent_id,
                outcome=outcome,
                order_type="stop_loss",
                trigger_price=sl["price"],
                size=sl["tokens"],  # internally stored as 'size'
                rationale=f"{rationale} [SL @ {sl['price']:.2f}]",
            )
            state.pending_limit_orders.append(order)
            placed_orders.append({
                "order_id": order.order_id[:8] + "...",
                "type": "stop_loss",
                "price": sl["price"],
                "tokens": sl["tokens"]
            })
            logger.info(
                "[BRACKET] %s: stop_loss %s @ %.4f tokens=%.2f",
                state.agent_id, outcome, sl["price"], sl["tokens"]
            )
            # Log to simulation logger
            sim_logger = get_simulation_logger()
            if sim_logger:
                sim_logger.limit_order(
                    agent_id=state.agent_id,
                    order_type="stop_loss",
                    outcome=outcome,
                    trigger_price=sl["price"],
                    size=sl["tokens"],
                    order_id=order.order_id,
                )

        return json.dumps({
            "bracket_placed": True,
            "outcome": outcome,
            "current_price": round(current_price, 4),
            "orders_placed": len(placed_orders),
            "orders": placed_orders,
            "take_profit_count": len(tp_list),
            "take_profit_total_tokens": total_tp_tokens,
            "stop_loss_count": len(sl_list),
            "stop_loss_total_tokens": total_sl_tokens,
            "rationale": rationale,
            "message": f"Placed {len(tp_list)} take-profit(s) totaling {total_tp_tokens:.0f} tokens and {len(sl_list)} stop-loss(es) totaling {total_sl_tokens:.0f} tokens for {outcome}"
        }, indent=2)

    # Store the check function on state so it can be called externally
    state._check_limit_orders = check_and_execute_limit_orders

    return [
        get_portfolio,
        get_price_history,
        place_trade,
        get_latest_prices,
        configure_alerts,
        get_active_alerts,
        cancel_alert,
        place_limit_order,
        place_bracket_orders,
        get_pending_orders,
        cancel_order,
    ]


# =============================================================================
# SUBAGENTS VIA HANDOFFS
# =============================================================================

def create_subagents(model: str = "gpt-5-mini") -> Dict[str, Agent]:
    """
    Create specialized subagents for research/analysis/execution.

    These can be used as handoffs from the main trading agent.
    """
    researcher = Agent(
        name="researcher",
        instructions="""You are a research specialist focused on gathering factual information.
Your task is to search the web and compile relevant data for prediction market analysis.
Focus on:
- Recent news and developments
- Statistical data and historical trends
- Expert opinions and forecasts
- Official announcements and schedules
Write your findings clearly and cite sources when possible.""",
        model=model,
    )

    analyst = Agent(
        name="analyst",
        instructions="""You are a quantitative analyst focused on market analysis.
Your task is to evaluate probability estimates and risk management.
Focus on:
- Probability estimation from available data
- Position sizing and Kelly criterion
- Risk/reward analysis
- Portfolio correlation and diversification
Provide clear recommendations with your reasoning.""",
        model=model,
    )

    return {"researcher": researcher, "analyst": analyst}


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

def build_trading_system_prompt(event: PredictionMarketEvent, agent_id: str) -> str:
    """Build a comprehensive system prompt for the trading agent."""
    outcomes_str = ", ".join(f'"{o}"' for o in event.outcomes)

    return f"""You are {agent_id}, an autonomous AI trading agent operating in a prediction market.

EVENT: {event.name}
DESCRIPTION: {event.description}
OUTCOMES: {outcomes_str}
RESOLUTION: {event.resolution_criteria}

YOUR OBJECTIVE: Maximize profit by trading on this prediction market.
- You start with $10,000 capital
- Use your knowledge and analysis to form probability estimates
- Trade when you find edge between your estimate and market price
- Manage risk with proper position sizing

=== CRITICAL: ALWAYS CHECK PRICES BEFORE TRADING ===

BEFORE making ANY trade:
1. Call get_latest_prices() to get current market state
2. Form your own probability estimate for each outcome
3. If market price differs from your estimate by >5%, that's tradeable edge
4. Size your position: larger edge = larger position (max 50% of cash)

=== TRADING STRATEGY ===

You MUST trade based on your analysis - don't wait for external research.

1. CHECK PRICES with get_latest_prices() first
2. Form probability estimates using your knowledge:
   - Historical data and patterns you know
   - Known strengths/weaknesses of teams/candidates/outcomes
   - Base rates and priors for this type of event
3. Calculate edge: edge = (your_probability - market_price) / market_price
4. If |edge| > 5%: TRADE! Buy if your_prob > market_price, sell if lower
5. Size position based on edge magnitude:
   - 5-10% edge: $500-1000
   - 10-20% edge: $1000-2000
   - 20%+ edge: $2000-3000

=== PROBABILITY ESTIMATION FRAMEWORK ===

For sports: Consider team records, head-to-head history, home/away, injuries, momentum
For elections: Consider polls, incumbency, historical patterns, demographics
For other events: Use base rates, known factors, and logical reasoning

Even without live data, you have extensive knowledge to form estimates.
Make a decision based on what you know NOW.

=== WHEN TO HOLD ===

Only HOLD when your probability estimate matches the market price within 5%.
HOLD signals: "My view aligns with the market - no edge to exploit."

Do NOT hold just because you lack perfect information.
Markets are about expected value under uncertainty - trade on your best estimate!

=== WHEN TO SELL ===

IMPORTANT: Check your portfolio! If you have positions from previous trading:

1. TAKE PROFITS: If a position has moved in your favor and price now EXCEEDS your estimate:
   - Example: You bought at $0.20, price is now $0.40, but your estimate is 30% ($0.30)
   - SELL some or all tokens to lock in profit!

2. CUT LOSSES: If your probability estimate has DECREASED:
   - Example: You bought at $0.30, but new info suggests only 15% probability
   - SELL to limit losses before price drops further

3. REBALANCE: If you're overexposed to one outcome:
   - Consider selling partial positions to diversify
   - Free up cash to buy better opportunities

To sell: place_trade(outcome="...", action="sell", size=<tokens>, rationale="...")
Note: For sells, 'size' is in TOKENS (not USD). Check get_portfolio() for your token balances.

=== LIMIT ORDERS ===

You can place limit orders that execute AUTOMATICALLY when prices move, even when it's not your turn!
This is CRITICAL for protecting profits and limiting losses between your trading turns.

Order types:
- 'take_profit': Sell TOKENS when price RISES to your trigger (lock in gains!)
- 'stop_loss': Sell TOKENS when price DROPS to your trigger (cut losses!)
- 'limit_buy': Spend USD when price DROPS to your trigger (buy the dip)
- 'limit_sell': Sell TOKENS when price RISES to your trigger

**BEST PRACTICE - USE BRACKET ORDERS TO SCALE OUT:**
After buying, set MULTIPLE take-profits at different price levels to scale out of your position,
plus MULTIPLE stop-losses as a tiered safety net. Use place_bracket_orders() to do this in ONE call!

Example: After buying 100 tokens of "Team A" at $0.30, set a bracket:
  place_bracket_orders(
    outcome="Team A",
    take_profits='[{{"price": 0.40, "tokens": 30}}, {{"price": 0.50, "tokens": 40}}, {{"price": 0.60, "tokens": 30}}]',
    stop_losses='[{{"price": 0.22, "tokens": 50}}, {{"price": 0.15, "tokens": 50}}]',
    rationale="Scale out at 3 profit targets, 2-tier stop loss protection"
  )

This sets:
- Sell 30 tokens at $0.40 (33% profit), 40 tokens at $0.50 (67% profit), 30 tokens at $0.60 (100% profit)
- If price drops, sell 50 tokens at $0.22 (27% loss), remaining 50 at $0.15 (50% loss) as last resort

For simpler setups, use place_limit_order() for single orders:
  place_limit_order(outcome="Team A", order_type="take_profit", trigger_price=0.45, amount=50, rationale="...")
  # amount = number of TOKENS for sells, USD for buys

Use get_pending_orders() to review active orders, cancel_order(order_id) to cancel.

=== ALERT WORKFLOW ===

IMPORTANT: Alerts let you research without constantly checking prices. Set up alerts, then focus on research.
When your conditions trigger, you'll see a detailed ALERT section at the START of your next turn.

1. After analyzing the market, use configure_alerts() to set custom monitoring conditions
2. Focus on research without constantly checking prices
3. If your conditions trigger, you'll see an ALERT section at the start of your turn
4. Review the alert context and decide whether to act
5. Set NEW alerts after reviewing (one-shot behavior: alerts deactivate after triggering)

Example workflow:
- Analyze: "YES at $0.35 looks undervalued, my estimate is 45%"
- Buy: place_trade("YES", "buy", 500, "Edge: 10%")
- Protect: place_bracket_orders(...) for take-profit/stop-loss
- Monitor: configure_alerts("YES", '{{"price_below": 0.30, "change_pct": 0.10}}', "Alert if thesis breaks")
- Research: Focus on gathering more information
- [Later, if alert triggers]: React to the market change with full context

=== AVAILABLE TOOLS ===

Market Tools:
- get_portfolio(): Check cash, positions, P&L
- get_price_history(limit): See recent trades and price movements
- get_latest_prices(): Get current prices (CALL BEFORE EVERY TRADE!)
- place_trade(outcome, action, size, rationale): Execute buy/sell

Alert Tools (INTERRUPT-BASED):
- configure_alerts(outcome, conditions, rationale): Set custom alert conditions for an outcome
    conditions: JSON like '{{"price_below": 0.30, "change_pct": 0.08, "large_trade_usd": 1000}}'
    ONE-SHOT: Alerts trigger once then deactivate. Set new alerts after reviewing.
- get_active_alerts(): See your currently active alert configurations
- cancel_alert(outcome): Cancel an active alert before it triggers

Limit Order Tools:
- place_bracket_orders(outcome, take_profits, stop_losses, rationale): Set multiple TP/SL at once (RECOMMENDED!)
    take_profits/stop_losses: JSON arrays like '[{{"price": 0.45, "tokens": 30}}, ...]'
- place_limit_order(outcome, order_type, trigger_price, amount, rationale): Set a single automatic order
    amount: USD for limit_buy, NUMBER OF TOKENS for take_profit/stop_loss/limit_sell
- get_pending_orders(): View your active limit orders
- cancel_order(order_id): Cancel a pending limit order

=== ACTION REQUIRED ===

You operate AUTONOMOUSLY. Make decisions NOW based on your knowledge.
1. Get prices
2. Form estimates
3. TRADE if you see edge, or explicitly state why prices are fair
4. Document your reasoning with every decision

Don't hesitate. Don't wait for more data. Analyze and ACT.
"""


# =============================================================================
# MAIN AGENT CREATION
# =============================================================================

def create_trading_agent(
    state: TradingAgentState,
    event: PredictionMarketEvent,
    model: str = "gpt-5-mini",
    mcp_servers: Optional[list] = None,
    enable_web_search: bool = True,
    enable_code_interpreter: bool = True,
    vector_store_ids: Optional[List[str]] = None,
) -> Agent:
    """
    Create the main trading agent with tools and guardrails.

    Args:
        state: Shared trading state
        event: The prediction market event
        model: Model to use (default gpt-5-mini)
        mcp_servers: Optional list of MCP servers for external integrations
        enable_web_search: Enable WebSearchTool for live data research
        enable_code_interpreter: Enable CodeInterpreterTool for calculations
        vector_store_ids: OpenAI Vector Store IDs for FileSearchTool

    Returns:
        Configured Agent instance
    """
    # Start with custom trading tools
    tools = create_trading_tools(state)

    # Add OpenAI Hosted Tools if available
    if HOSTED_TOOLS_AVAILABLE:
        # WebSearchTool - allows agent to search the web for current events
        if enable_web_search and WebSearchTool:
            tools.append(WebSearchTool())
            logger.info("WebSearchTool enabled for agent %s", state.agent_id)

        # CodeInterpreterTool - allows agent to run Python code for analysis
        if enable_code_interpreter and CodeInterpreterTool:
            tools.append(CodeInterpreterTool(tool_config={
                "type": "code_interpreter",
                "container": {"type": "auto"}  # Auto-managed sandbox container
            }))
            logger.info("CodeInterpreterTool enabled for agent %s", state.agent_id)

        # FileSearchTool - allows agent to search documents in vector stores
        if vector_store_ids and FileSearchTool:
            tools.append(FileSearchTool(
                max_num_results=5,
                vector_store_ids=vector_store_ids,
            ))
            logger.info("FileSearchTool enabled with %d vector stores", len(vector_store_ids))
    else:
        logger.warning("Hosted tools not available - install openai-agents>=0.0.7")

    subagents = create_subagents(model)
    system_prompt = build_trading_system_prompt(event, state.agent_id)

    # Build enhanced system prompt with tool descriptions
    if HOSTED_TOOLS_AVAILABLE and (enable_web_search or enable_code_interpreter):
        tool_section = """

=== ADDITIONAL TOOLS AVAILABLE ===

"""
        if enable_web_search:
            tool_section += """WebSearchTool: Search the web for current news, statistics, and market data.
  - Use this to research teams, players, injuries, recent performance
  - Search for betting lines, expert predictions, and breaking news
  - Example: "Search for Kansas City Chiefs 2025 playoff odds"

"""
        if enable_code_interpreter:
            tool_section += """CodeInterpreterTool: Execute Python code for calculations and analysis.
  - Use this for probability calculations, Kelly criterion, expected value
  - Analyze historical data, compute correlations, run simulations
  - Example: Calculate optimal position size based on edge

"""
        system_prompt += tool_section

    agent = Agent(
        name=state.agent_id,
        instructions=system_prompt,
        model=model,
        tools=tools,
        handoffs=[subagents["researcher"], subagents["analyst"]],
        input_guardrails=[trade_rate_limit_guardrail],
        mcp_servers=mcp_servers or [],
    )

    return agent


# =============================================================================
# MCP TOOL CONFIGURATIONS
# =============================================================================

def create_financial_mcp_tools() -> List:
    """
    Create MCP tools for financial data and research.

    Returns list of HostedMCPTool instances for finance-related MCPs.
    """
    if not MCP_AVAILABLE or not HostedMCPTool:
        logger.warning("MCP tools not available")
        return []

    tools = []

    # Context7 - Documentation and context retrieval
    # Useful for looking up API docs, financial terminology, etc.
    try:
        import os
        context7_key = os.environ.get("CONTEXT7_API_KEY")
        if context7_key:
            tools.append(HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "context7",
                    "server_url": "https://mcp.context7.com/mcp",
                    "authorization": f"Bearer {context7_key}",
                    "require_approval": "never",
                }
            ))
            logger.info("Context7 MCP tool configured")
    except Exception as e:
        logger.debug("Context7 MCP not configured: %s", e)

    return tools


def get_available_tools_summary() -> Dict[str, bool]:
    """
    Get a summary of which tools are available in the current environment.

    Returns:
        Dict mapping tool name to availability status
    """
    return {
        "function_tools": True,  # Always available (custom trading tools)
        "WebSearchTool": HOSTED_TOOLS_AVAILABLE and WebSearchTool is not None,
        "CodeInterpreterTool": HOSTED_TOOLS_AVAILABLE and CodeInterpreterTool is not None,
        "FileSearchTool": HOSTED_TOOLS_AVAILABLE and FileSearchTool is not None,
        "HostedMCPTool": MCP_AVAILABLE and HostedMCPTool is not None,
        "MCPServerStdio": MCP_AVAILABLE and MCPServerStdio is not None,
        "MCPServerStreamableHttp": MCP_AVAILABLE and MCPServerStreamableHttp is not None,
    }


# =============================================================================
# AGENT EXECUTION
# =============================================================================

async def run_trading_agent(
    event_market: EventMarket,
    agent_id: str = "openai_agent",
    model: str = "gpt-5-mini",
    initial_capital: float = 10000.0,
    mcp_servers: Optional[list] = None,
):
    """
    Run an OpenAI Agents SDK trading agent on an event market.

    Args:
        event_market: The prediction market to trade on
        agent_id: Unique identifier for this agent
        model: Model to use
        initial_capital: Starting capital in USD
        mcp_servers: Optional MCP servers for external integrations

    Yields:
        Events from the agent execution
    """
    # Initialize state
    state = TradingAgentState(
        event_market=event_market,
        market_lock=asyncio.Lock(),
        initial_capital=initial_capital,
        cash_balance=initial_capital,
        agent_id=agent_id,
    )

    # Create context for guardrails
    context = TradingContext(state=state)

    # Create agent
    agent = create_trading_agent(state, event_market.event, model, mcp_servers)

    # Initial prompt
    prices = event_market.get_prices()
    prompt = f"""
You are now trading on the prediction market for: {event_market.event.name}

Current market prices:
{json.dumps({k: f"${v:.2f}" for k, v in prices.items()}, indent=2)}

Your task:
1. Research this event
2. Analyze the market prices vs your probability estimates
3. Trade when you find edge
4. Document your reasoning

Start by checking your portfolio with get_portfolio(), then research the event.
"""

    # Run with streaming
    run_config = RunConfig(workflow_name=f"trading_{agent_id}")

    async for event in Runner.run_streamed(
        agent,
        prompt,
        context=context,
        run_config=run_config,
    ):
        yield event


# =============================================================================
# TRADING SESSION: Multi-Turn Conversations
# =============================================================================

class TradingSession:
    """
    Persistent trading session using OpenAI Agents SDK.

    Maintains conversation context across multiple exchanges.

    Usage:
        async with TradingSession(event_market, agent_id) as session:
            await session.start()
            response = await session.send("Research latest news")
            response = await session.send("What's my portfolio?")
            await session.send("Buy $500 on Chiefs")
    """

    def __init__(
        self,
        event_market: EventMarket,
        agent_id: str = "openai_agent",
        model: str = "gpt-5-mini",
        initial_capital: float = 10000.0,
        mcp_servers: Optional[list] = None,
    ):
        self.event_market = event_market
        self.agent_id = agent_id
        self.model = model
        self.initial_capital = initial_capital
        self.mcp_servers = mcp_servers

        self._state: Optional[TradingAgentState] = None
        self._agent: Optional[Agent] = None
        self._context: Optional[TradingContext] = None
        self._conversation_history: List[Dict[str, Any]] = []

    async def __aenter__(self):
        """Async context manager entry - initialize session."""
        self._state = TradingAgentState(
            event_market=self.event_market,
            market_lock=asyncio.Lock(),
            initial_capital=self.initial_capital,
            cash_balance=self.initial_capital,
            agent_id=self.agent_id,
        )

        self._context = TradingContext(state=self._state)

        self._agent = create_trading_agent(
            self._state,
            self.event_market.event,
            self.model,
            self.mcp_servers,
        )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup."""
        pass

    @property
    def state(self) -> TradingAgentState:
        """Access agent state (portfolio, trades, etc.)."""
        return self._state

    @property
    def conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self._conversation_history

    async def start(self) -> str:
        """
        Initialize the trading session with market context.

        Returns:
            Initial response from the agent
        """
        prices = self.event_market.get_prices()
        initial_prompt = f"""
You are now trading on: {self.event_market.event.name}

Current market prices:
{json.dumps({k: f"${v:.2f}" for k, v in prices.items()}, indent=2)}

Start by checking your portfolio with get_portfolio(), then research the event.
"""
        return await self.send(initial_prompt)

    async def send(self, prompt: str) -> str:
        """
        Send a message and get response.

        Uses conversation history for context continuity.

        Args:
            prompt: User message

        Returns:
            Agent response
        """
        # Build input with history
        if self._conversation_history:
            input_data = self._conversation_history + [{"role": "user", "content": prompt}]
        else:
            input_data = prompt

        result = await Runner.run(
            self._agent,
            input_data,
            context=self._context,
        )

        # Update conversation history
        self._conversation_history.append({"role": "user", "content": prompt})
        self._conversation_history.append({"role": "assistant", "content": result.final_output})

        return result.final_output

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get current portfolio state as dict."""
        if not self._state:
            return {}

        prices = self.event_market.get_prices()
        total_value = self._state.cash_balance
        for outcome, tokens in self._state.portfolio.items():
            total_value += tokens * prices.get(outcome, 0.5)

        return {
            "cash": round(self._state.cash_balance, 2),
            "positions": dict(self._state.portfolio),
            "total_value": round(total_value, 2),
            "pnl": round(total_value - self._state.initial_capital, 2),
            "return_pct": round(
                (total_value / self._state.initial_capital - 1) * 100, 2
            ),
            "trades": len(self._state.event_trade_log),
        }
