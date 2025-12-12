"""
Constant Product Market Maker (CPMM) implementation.

Migrated from market_engine.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional, Union


class MarketError(Exception):
    """Base class for market-related exceptions."""


class InvalidSwapDirection(MarketError):
    """Raised when an unsupported swap direction is requested."""


class InsufficientLiquidity(MarketError):
    """Raised when the requested trade would drain pool reserves."""


SwapDirection = Literal["buy", "sell"]


@dataclass(frozen=True)
class TradeExecution:
    """
    Record of a single trade execution against the automated market maker.

    Attributes:
        agent_id: Identifier for the trading agent.
        direction: 'buy' if the agent bought the base asset, 'sell' otherwise.
        base_delta: Change in the agent's base asset holdings (positive = received).
        quote_delta: Change in the agent's quote currency holdings (positive = received).
        price: Volume-weighted average execution price (quote/base).
        timestamp: UTC timestamp of the trade.
        meta: Additional contextual information about the trade.
    """

    agent_id: str
    direction: SwapDirection
    base_delta: float
    quote_delta: float
    price: float
    timestamp: datetime
    meta: Dict[str, Union[float, str]]


class Market:
    """
    Constant Product Market Maker (CPMM) implementation for a single asset pair.

    The market maintains reserves of a base asset and a quote asset (e.g. USD).
    Agents can swap quote->base (buy) or base->quote (sell), and the price moves
    according to the invariant x * y = k.
    """

    def __init__(
        self,
        *,
        base_symbol: str,
        quote_symbol: str,
        reserves_base: float,
        reserves_quote: float,
        fee_bps: float = 30.0,
        min_reserve: float = 1e-9,
    ) -> None:
        if reserves_base <= 0 or reserves_quote <= 0:
            raise ValueError("Initial reserves must be positive for both assets.")
        self.base_symbol = base_symbol
        self.quote_symbol = quote_symbol
        self.reserves_base = float(reserves_base)
        self.reserves_quote = float(reserves_quote)
        self.fee_bps = float(fee_bps)
        self.min_reserve = float(min_reserve)

        self._trade_history: List[TradeExecution] = []

    @property
    def fee_rate(self) -> float:
        """Return the trading fee as a fraction (e.g. 0.003)."""
        return self.fee_bps / 10_000.0

    @property
    def invariant(self) -> float:
        """Return the current constant product invariant."""
        return self.reserves_base * self.reserves_quote

    def get_price(self) -> float:
        """
        Spot price for one unit of the base asset in quote currency.

        When reserves are B (base) and Q (quote), price = Q / B.
        """
        return self.reserves_quote / self.reserves_base

    def get_state(self) -> Dict[str, float]:
        """Return a serialisable snapshot of the market reserves and price."""
        return {
            "reserves_base": self.reserves_base,
            "reserves_quote": self.reserves_quote,
            "price": self.get_price(),
            "fee_bps": self.fee_bps,
            "invariant": self.invariant,
        }

    def _current_timestamp(self) -> datetime:
        """Return a timezone-aware UTC timestamp."""
        return datetime.now(timezone.utc)

    def swap(
        self,
        *,
        agent_id: str,
        direction: SwapDirection,
        amount: float,
        note: Optional[str] = None,
    ) -> TradeExecution:
        """
        Execute a swap against the AMM.

        Args:
            agent_id: Identifier for the actor performing the swap.
            direction: 'buy' for quote->base, 'sell' for base->quote.
            amount: Input amount supplied by the agent (quote if buy, base if sell).
            note: Optional free-form note stored in trade metadata.

        Returns:
            TradeExecution describing the resulting asset deltas and execution price.

        Raises:
            InvalidSwapDirection: If direction is not 'buy' or 'sell'.
            InsufficientLiquidity: If the trade would deplete pool reserves.
        """
        if amount <= 0:
            raise ValueError("Swap amount must be positive.")

        pre_price = self.get_price()
        k = self.invariant
        fee_rate = self.fee_rate
        timestamp = self._current_timestamp()

        if direction == "buy":
            quote_in = float(amount)
            effective_in = quote_in * (1.0 - fee_rate)
            new_quote_reserve = self.reserves_quote + effective_in
            base_out = self.reserves_base - (k / new_quote_reserve)
            if base_out <= 0:
                raise InsufficientLiquidity("Trade would consume all base liquidity.")

            self.reserves_quote += quote_in
            self.reserves_base -= base_out

            price = quote_in / base_out
            base_delta = base_out
            quote_delta = -quote_in

        elif direction == "sell":
            base_in = float(amount)
            effective_in = base_in * (1.0 - fee_rate)
            new_base_reserve = self.reserves_base + effective_in
            quote_out = self.reserves_quote - (k / new_base_reserve)
            if quote_out <= 0 or quote_out >= self.reserves_quote:
                raise InsufficientLiquidity(
                    "Trade would consume all quote liquidity."
                )

            self.reserves_base += base_in
            self.reserves_quote -= quote_out

            price = quote_out / base_in
            base_delta = -base_in
            quote_delta = quote_out

        else:
            raise InvalidSwapDirection(direction)

        execution = TradeExecution(
            agent_id=agent_id,
            direction=direction,
            base_delta=base_delta,
            quote_delta=quote_delta,
            price=price,
            timestamp=timestamp,
            meta={
                "fee_paid": abs(amount) * fee_rate,
                "note": note or "",
                "reserves_base": self.reserves_base,
                "reserves_quote": self.reserves_quote,
                "pre_price": pre_price,
                "post_price": self.get_price(),
            },
        )

        self._trade_history.append(execution)
        return execution

    @property
    def trade_history(self) -> List[TradeExecution]:
        """Return an immutable list of trade executions."""
        return list(self._trade_history)

    def get_price_history(self, limit: int = 50) -> List[Dict[str, Union[str, float]]]:
        """
        Return the most recent price prints with contextual metadata.

        Args:
            limit: Maximum number of executions to include (most recent first).
        """
        limit = max(1, int(limit))
        recent = self._trade_history[-limit:]
        history: List[Dict[str, Union[str, float]]] = []
        for trade in recent:
            history.append(
                {
                    "timestamp": trade.timestamp.isoformat(),
                    "agent_id": trade.agent_id,
                    "direction": trade.direction,
                    "price": trade.price,
                    "base_delta": trade.base_delta,
                    "quote_delta": trade.quote_delta,
                    "note": trade.meta.get("note", ""),
                    "post_price": trade.meta.get("post_price"),
                }
            )
        return history

    def reset_history(self) -> None:
        """Clear accumulated trade history (useful for tests)."""
        self._trade_history.clear()
