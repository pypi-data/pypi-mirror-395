"""
Prediction market events and event-based trading.

Migrated from prediction_events.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional, Union
from enum import Enum


class OutcomeToken(Enum):
    """Standard binary outcome tokens."""
    YES = "YES"
    NO = "NO"


@dataclass
class PredictionMarketEvent:
    """
    Defines a tradeable prediction market event.

    Each event has a name, description, and set of possible outcomes.
    Agents trade on outcome tokens, with prices representing implied probabilities.
    """
    id: str
    name: str
    description: str
    outcomes: List[str] = field(default_factory=lambda: ["YES", "NO"])
    initial_probabilities: Optional[Dict[str, float]] = None  # Custom starting prices
    resolution_criteria: str = ""
    data_sources: List[str] = field(default_factory=list)  # Event-specific URLs for research
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = False
    winning_outcome: Optional[str] = None

    def __post_init__(self):
        if len(self.outcomes) < 2:
            raise ValueError("Event must have at least 2 outcomes")
        # Validate initial probabilities if provided
        if self.initial_probabilities:
            for outcome in self.outcomes:
                if outcome not in self.initial_probabilities:
                    raise ValueError(f"Missing initial probability for outcome: {outcome}")
            total = sum(self.initial_probabilities.values())
            if abs(total - 1.0) > 0.01:
                raise ValueError(f"Initial probabilities must sum to 1.0, got {total}")

    def resolve(self, winning_outcome: str) -> None:
        """Resolve the event with a winning outcome."""
        if winning_outcome not in self.outcomes:
            raise ValueError(f"Invalid outcome: {winning_outcome}. Must be one of {self.outcomes}")
        self.resolved = True
        self.winning_outcome = winning_outcome

    def to_prompt_context(self, prices: Dict[str, float]) -> str:
        """Generate prompt context for agents."""
        outcome_str = ", ".join(
            f"{outcome} (${prices.get(outcome, 0.50):.2f})"
            for outcome in self.outcomes
        )
        return (
            f"EVENT: \"{self.name}\"\n"
            f"DESCRIPTION: {self.description}\n"
            f"OUTCOMES: {outcome_str}\n"
            f"RESOLUTION: {self.resolution_criteria}"
        )


@dataclass
class OutcomeMarketState:
    """Tracks the state of a single outcome's market."""
    outcome: str
    reserves_token: float  # Outcome tokens in pool
    reserves_quote: float  # Quote currency (e.g., USD) in pool
    total_volume: float = 0.0

    @property
    def price(self) -> float:
        """Current price of outcome token (0-1 representing probability)."""
        if self.reserves_token == 0:
            return 1.0
        return self.reserves_quote / (self.reserves_quote + self.reserves_token)


@dataclass
class TradeResult:
    """Result of an outcome token trade."""
    agent_id: str
    event_id: str
    outcome: str
    direction: Literal["buy", "sell"]
    token_delta: float
    quote_delta: float
    price: float
    timestamp: datetime
    note: str = ""


class EventMarket:
    """
    A prediction market for a single event with multiple outcomes.

    Uses a modified constant-product AMM where each outcome has its own
    liquidity pool. Prices are constrained to approximately sum to 1.0.
    """

    def __init__(
        self,
        event: PredictionMarketEvent,
        initial_liquidity: float = 10000.0,
        quote_symbol: str = "USD",
        fee_bps: float = 30.0,
    ) -> None:
        self.event = event
        self.quote_symbol = quote_symbol
        self.fee_bps = fee_bps

        n_outcomes = len(event.outcomes)

        # Use custom initial probabilities if provided, otherwise uniform
        if event.initial_probabilities:
            initial_prices = event.initial_probabilities
        else:
            uniform_price = 1.0 / n_outcomes
            initial_prices = {outcome: uniform_price for outcome in event.outcomes}

        self.outcome_markets: Dict[str, OutcomeMarketState] = {}
        for outcome in event.outcomes:
            initial_price = initial_prices[outcome]
            # Set reserves so price = initial_price
            # price = reserves_quote / (reserves_quote + reserves_token)
            # initial_price = L / (L + T) => T = L * (1 - initial_price) / initial_price
            # Distribute liquidity proportionally to probability
            reserves_quote = initial_liquidity * initial_price
            if initial_price > 0 and initial_price < 1:
                reserves_token = reserves_quote * (1 - initial_price) / initial_price
            else:
                reserves_token = reserves_quote  # Edge case handling
            self.outcome_markets[outcome] = OutcomeMarketState(
                outcome=outcome,
                reserves_token=reserves_token,
                reserves_quote=reserves_quote,
            )

        self._trade_history: List[TradeResult] = []

    @property
    def fee_rate(self) -> float:
        return self.fee_bps / 10_000.0

    def get_prices(self, normalized: bool = True) -> Dict[str, float]:
        """
        Get current prices for all outcomes.

        Args:
            normalized: If True (default), prices are normalized to sum to 1.0.
                       If False, returns raw AMM prices from reserves.
        """
        raw_prices = {
            outcome: market.price
            for outcome, market in self.outcome_markets.items()
        }

        if not normalized:
            return raw_prices

        price_sum = sum(raw_prices.values())
        if price_sum == 0:
            return raw_prices  # Avoid division by zero

        return {
            outcome: price / price_sum
            for outcome, price in raw_prices.items()
        }

    def get_state(self) -> Dict[str, Union[str, float, Dict]]:
        """Get full market state for logging/display."""
        normalized_prices = self.get_prices(normalized=True)
        raw_prices = self.get_prices(normalized=False)
        return {
            "event_id": self.event.id,
            "event_name": self.event.name,
            "prices": normalized_prices,
            "raw_prices": raw_prices,  # For debugging
            "price_sum_raw": sum(raw_prices.values()),
            "total_volume": sum(m.total_volume for m in self.outcome_markets.values()),
            "resolved": self.event.resolved,
        }

    def swap(
        self,
        *,
        agent_id: str,
        outcome: str,
        direction: Literal["buy", "sell"],
        amount: float,
        note: str = "",
    ) -> TradeResult:
        """
        Execute a trade on an outcome token.

        Args:
            agent_id: ID of the trading agent
            outcome: Which outcome to trade (e.g., "YES", "NO")
            direction: "buy" to acquire outcome tokens, "sell" to dispose
            amount: Quote currency amount (for buy) or token amount (for sell)
            note: Optional trade rationale

        Returns:
            TradeResult with execution details
        """
        if outcome not in self.outcome_markets:
            raise ValueError(f"Invalid outcome: {outcome}")

        if amount <= 0:
            raise ValueError("Trade amount must be positive")

        market = self.outcome_markets[outcome]
        timestamp = datetime.now(timezone.utc)
        fee_rate = self.fee_rate

        if direction == "buy":
            # Agent pays quote currency to receive outcome tokens
            quote_in = amount
            effective_in = quote_in * (1 - fee_rate)

            # Constant product: (R_q + effective_in) * (R_t - tokens_out) = R_q * R_t
            k = market.reserves_quote * market.reserves_token
            new_quote = market.reserves_quote + effective_in
            tokens_out = market.reserves_token - (k / new_quote)

            if tokens_out <= 0:
                raise ValueError("Insufficient liquidity")

            market.reserves_quote += quote_in
            market.reserves_token -= tokens_out
            market.total_volume += quote_in

            result = TradeResult(
                agent_id=agent_id,
                event_id=self.event.id,
                outcome=outcome,
                direction="buy",
                token_delta=tokens_out,
                quote_delta=-quote_in,
                price=quote_in / tokens_out,
                timestamp=timestamp,
                note=note,
            )

        else:  # sell
            # Agent sells outcome tokens to receive quote currency
            tokens_in = amount
            effective_in = tokens_in * (1 - fee_rate)

            k = market.reserves_quote * market.reserves_token
            new_tokens = market.reserves_token + effective_in
            quote_out = market.reserves_quote - (k / new_tokens)

            if quote_out <= 0 or quote_out >= market.reserves_quote:
                raise ValueError("Insufficient liquidity")

            market.reserves_token += tokens_in
            market.reserves_quote -= quote_out
            market.total_volume += quote_out

            result = TradeResult(
                agent_id=agent_id,
                event_id=self.event.id,
                outcome=outcome,
                direction="sell",
                token_delta=-tokens_in,
                quote_delta=quote_out,
                price=quote_out / tokens_in,
                timestamp=timestamp,
                note=note,
            )

        self._trade_history.append(result)
        return result

    def get_price_history(self, limit: int = 50) -> List[Dict]:
        """Get recent trade history."""
        recent = self._trade_history[-limit:] if limit > 0 else self._trade_history
        return [
            {
                "timestamp": t.timestamp.isoformat(),
                "agent_id": t.agent_id,
                "outcome": t.outcome,
                "direction": t.direction,
                "price": t.price,
                "token_delta": t.token_delta,
                "quote_delta": t.quote_delta,
                "note": t.note,
            }
            for t in recent
        ]

    @property
    def trade_history(self) -> List[TradeResult]:
        return list(self._trade_history)


@dataclass
class EventSimulationConfig:
    """
    Configuration for running a prediction market simulation.

    Defines the events to trade, data sources for research,
    and monitor settings for detecting new information.
    """
    events: List[PredictionMarketEvent]
    data_sources: List[str] = field(default_factory=list)
    monitor_prompt: str = ""
    initial_liquidity: float = 10000.0

    def to_agent_context(self, markets: Dict[str, EventMarket]) -> str:
        """Generate context string for agent prompts."""
        lines = ["You are trading in a prediction market with the following events:\n"]
        for event in self.events:
            market = markets.get(event.id)
            if market:
                prices = market.get_prices()
                lines.append(event.to_prompt_context(prices))
                lines.append("")
        return "\n".join(lines)


def create_sample_events() -> List[PredictionMarketEvent]:
    """Create sample prediction events for testing."""
    return [
        PredictionMarketEvent(
            id="fed-rate-dec-2025",
            name="Fed Rate Decision December 2025",
            description="Will the Federal Reserve cut interest rates by 25 basis points at the December 2025 FOMC meeting?",
            outcomes=["YES", "NO"],
            resolution_criteria="Resolves YES if the Fed announces a 25bp rate cut at the December 16-17, 2025 FOMC meeting.",
        ),
        PredictionMarketEvent(
            id="btc-150k-2025",
            name="Bitcoin $150K in 2025",
            description="Will Bitcoin reach $150,000 USD before January 1, 2026?",
            outcomes=["YES", "NO"],
            resolution_criteria="Resolves YES if BTC/USD trades at or above $150,000 on any major exchange before 2026.",
        ),
    ]


def create_multi_outcome_events() -> List[PredictionMarketEvent]:
    """Create multi-outcome prediction events for testing."""
    return [
        PredictionMarketEvent(
            id="super-bowl-2026",
            name="Super Bowl LX Winner 2026",
            description=(
                "Which team will win Super Bowl LX in February 2026? "
                "Research team records, injuries, strength of schedule, and playoff odds. "
                "Look up current NFL standings, point differentials, and betting lines."
            ),
            outcomes=[
                "Kansas City Chiefs",
                "Detroit Lions",
                "Philadelphia Eagles",
                "Buffalo Bills",
                "Baltimore Ravens",
                "San Francisco 49ers",
                "Dallas Cowboys",
                "Green Bay Packers",
                "Other AFC",
                "Other NFC",
            ],
            # No initial_probabilities - starts at uniform 10% each
            # Agents will rebalance through alpha-based trading
            resolution_criteria=(
                "Resolves to the team that wins Super Bowl LX. "
                "If winner not listed individually, resolves to 'Other AFC' or 'Other NFC'."
            ),
            data_sources=[
                "https://www.espn.com/nfl/standings",
                "https://www.espn.com/nfl/injuries",
                "https://www.pro-football-reference.com/years/2024/",
                "https://www.nfl.com/standings/",
                "https://www.footballoutsiders.com/stats/nfl/team-efficiency/2024",
                "https://www.vegasinsider.com/nfl/odds/futures/",
            ],
        ),
        PredictionMarketEvent(
            id="us-president-2028",
            name="US President 2028",
            description=(
                "Who will win the 2028 United States Presidential Election? "
                "Context: Donald Trump won the 2024 election and JD Vance is the sitting Vice President. "
                "Vance is the presumptive Republican frontrunner with incumbency advantage. "
                "On the Democratic side, Gavin Newsom (CA Governor) is the leading candidate, "
                "with Pete Buttigieg, Gretchen Whitmer, and Josh Shapiro as other top-tier contenders."
            ),
            outcomes=[
                "JD Vance",
                "Gavin Newsom",
                "Pete Buttigieg",
                "Gretchen Whitmer",
                "Ron DeSantis",
                "Josh Shapiro",
                "Nikki Haley",
                "AOC",
                "Vivek Ramaswamy",
                "Other",
            ],
            initial_probabilities={
                "JD Vance": 0.28,        # Sitting VP, Republican frontrunner
                "Gavin Newsom": 0.22,    # Leading Democratic candidate
                "Pete Buttigieg": 0.10,  # Cabinet experience, strong fundraiser
                "Gretchen Whitmer": 0.09, # Popular swing-state governor
                "Ron DeSantis": 0.08,    # Florida governor, 2024 runner-up
                "Josh Shapiro": 0.07,    # PA governor, swing state advantage
                "Nikki Haley": 0.06,     # Former UN Ambassador, moderate appeal
                "AOC": 0.04,             # Progressive wing, less likely nominee
                "Vivek Ramaswamy": 0.03, # Outsider candidate
                "Other": 0.03,           # Field is well-covered
            },
            resolution_criteria=(
                "Resolves to the candidate who wins the 2028 US Presidential Election. "
                "If winner is not listed, resolves to 'Other'."
            ),
        ),
        PredictionMarketEvent(
            id="ai-agi-2030",
            name="AGI by 2030",
            description="Which organization will first achieve AGI (Artificial General Intelligence) by 2030?",
            outcomes=[
                "OpenAI",
                "Anthropic",
                "Google DeepMind",
                "Meta AI",
                "xAI",
                "Chinese Lab",
                "Other",
                "None by 2030",
            ],
            resolution_criteria=(
                "Resolves to the first organization to demonstrate AGI as determined by "
                "a consensus of AI researchers or major benchmark achievement. "
                "Resolves 'None by 2030' if no AGI is achieved before Jan 1, 2031."
            ),
        ),
        PredictionMarketEvent(
            id="next-fed-chair-2026",
            name="Next Fed Chair 2026",
            description="Who will be the next Chair of the Federal Reserve after Jerome Powell's term ends?",
            outcomes=[
                "Kevin Warsh",
                "Larry Summers",
                "Neel Kashkari",
                "Lael Brainard",
                "John Williams",
                "Mary Daly",
                "Other",
            ],
            resolution_criteria=(
                "Resolves to the person confirmed as Fed Chair after Powell's current term. "
                "If not listed, resolves to 'Other'."
            ),
        ),
    ]
