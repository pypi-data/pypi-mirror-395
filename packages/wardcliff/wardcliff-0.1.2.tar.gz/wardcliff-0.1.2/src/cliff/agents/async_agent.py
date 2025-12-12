from __future__ import annotations

import asyncio
import inspect
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from typing import Any, Awaitable, Callable, Dict, List, Literal, Optional, Type, TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, field_validator, validator

from cliff.core.market import Market, TradeExecution
from cliff.core.metrics import MetricsRecorder
from cliff.core.events import EventMarket, PredictionMarketEvent, TradeResult as EventTradeResult

# Optional external integrations - may not be installed
try:
    from data_sources import WebDatasetManager
except ImportError:
    WebDatasetManager = None

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

try:
    from turbopuffer_client import TurbopufferClient, TurbopufferError
except ImportError:
    TurbopufferClient = None
    TurbopufferError = Exception

try:
    from communication import EmailClient, SMSClient
except ImportError:
    EmailClient = None
    SMSClient = None

TModel = TypeVar("TModel", bound=BaseModel)

logger = logging.getLogger(__name__)

# Plan configuration - soft limits to guide planning
MAX_PLAN_STEPS = 20  # Soft maximum for plan length
MAX_STEPS_PER_INJECTION = 3  # Limit dynamic planning growth
MAX_CONSECUTIVE_SAME_TOOL = 2  # Force tool diversity

SwapDirection = Literal["buy", "sell", "hold"]


class AgentPersona(BaseModel):
    """Describes the immutable characteristics of an agent."""

    name: str
    race: str
    background: str
    personality: str
    risk_tolerance: Literal["low", "medium", "high"] = "medium"
    description: Optional[str] = Field(
        None, description="Optional free-form summary of the persona."
    )

    def short_prompt(self) -> str:
        return (
            f"You are {self.name}, a {self.race} trader with a {self.personality} "
            f"disposition and {self.background} background. "
            f"Risk tolerance: {self.risk_tolerance}."
        )


class SubAgentConfig(BaseModel):
    """
    Rule-based trigger configuration for the price-movement watcher.
    """

    percent_move_threshold: float = Field(
        ...,
        gt=0,
        description="Relative price move (e.g., 0.01 for 1%) that triggers an interrupt.",
    )
    cooldown_seconds: int = Field(
        60,
        ge=0,
        description="Minimum number of seconds between interrupts.",
    )
    min_trade_notional: float = Field(
        0.0,
        ge=0,
        description="Ignore trades below this notional (quote currency).",
    )
    note: Optional[str] = Field(
        None,
        description="Additional instruction about how to respond to a trigger.",
    )


class Plan(BaseModel):
    plan: str
    steps: List[str]


class FunctionCall(BaseModel):
    function: str
    args: List[str]

    @field_validator('args', mode='before')
    @classmethod
    def coerce_args_to_strings(cls, v):
        """Coerce all args to strings (LLMs may return int/float)."""
        if isinstance(v, list):
            return [str(item) for item in v]
        return v


class ThoughtAndFunction(BaseModel):
    thoughts: str
    function_call: FunctionCall


class StepSummary(BaseModel):
    notes: str
    next_steps: Optional[List[str]] = None


class PaperInfo(BaseModel):
    paper: str = Field(..., description="Research paper title")
    notes: str = Field(..., description="Summary of the research paper")


class Papers(BaseModel):
    papers: List[PaperInfo] = Field(default_factory=list)


class TradingDecision(BaseModel):
    action: SwapDirection
    size: float = Field(..., ge=0)
    rationale: str

    @validator("action")
    def validate_action(cls, value: SwapDirection) -> SwapDirection:
        if value not in {"buy", "sell", "hold"}:
            raise ValueError(f"Unsupported trading action: {value}")
        return value


class EventTradingDecision(BaseModel):
    """Trading decision for event-based prediction markets."""
    outcome: str = Field(..., description="Which outcome to trade (e.g., 'YES', 'NO')")
    action: SwapDirection
    size: float = Field(..., ge=0, description="Amount in quote currency (buy) or tokens (sell)")
    rationale: str = Field(..., description="Brief explanation of the trade thesis based on real data")
    estimated_probability: float = Field(
        default=0.5,
        ge=0,
        le=1,
        description="Agent's probability estimate for the outcome (0-1)"
    )

    @validator("action")
    def validate_action(cls, value: SwapDirection) -> SwapDirection:
        if value not in {"buy", "sell", "hold"}:
            raise ValueError(f"Unsupported trading action: {value}")
        return value


class SubAgentAssessment(BaseModel):
    percent_move_threshold: float = Field(..., gt=0)
    cooldown_seconds: int = Field(ge=0, default=60)
    min_trade_notional: float = Field(ge=0, default=0)
    note: Optional[str] = None


STRUCTURED_INSTRUCTIONS: Dict[Type[BaseModel], str] = {
    Plan: 'Return JSON {"plan": string, "steps": [string, ...]}.',
    ThoughtAndFunction: (
        'Return JSON {"thoughts": string, "function_call": {"function": string, "args": [string, ...]}}.'
    ),
    StepSummary: (
        'Return JSON {"notes": string, "next_steps": [string, ...] or null}.'
    ),
    Papers: (
        'Return JSON {"papers": [{"paper": string, "notes": string}, ...]}.'
    ),
    TradingDecision: (
        'Return JSON {"action": "buy" | "sell" | "hold", "size": number, "rationale": string}.'
    ),
    EventTradingDecision: (
        'Return JSON {"outcome": string, "action": "buy" | "sell" | "hold", "size": number, '
        '"rationale": string, "estimated_probability": number (0-1)}.'
    ),
    SubAgentAssessment: (
        'Return JSON {"percent_move_threshold": number, "cooldown_seconds": integer, '
        '"min_trade_notional": number, "note": string or null}.'
    ),
}


@dataclass
class InterruptState:
    last_price: Optional[float] = None
    last_triggered: Optional[datetime] = None
    last_trade: Optional[TradeExecution] = None


class AsyncTradingAgent:
    """
    Asynchronous trading agent that plans, researches, and trades against an AMM.

    A rule-based sub-agent monitors price movements and can interrupt the main loop
    when significant moves occur.
    """

    def __init__(
        self,
        *,
        persona: AgentPersona,
        market: Market,
        openai_client: Optional[AsyncOpenAI] = None,
        parallel_extract: Optional[ParallelExtractClient] = None,
        parallel_monitor: Optional[ParallelMonitorClient] = None,
        sub_agent_config: Optional[SubAgentConfig] = None,
        market_lock: Optional[asyncio.Lock] = None,
        trade_callback: Optional[
            Callable[[TradeExecution], Optional[Awaitable[None]]]
        ] = None,
        event_trade_callback: Optional[
            Callable[[EventTradeResult], Optional[Awaitable[None]]]
        ] = None,
        llm_model: str = "gpt-5-mini",
        metrics: Optional[MetricsRecorder] = None,
        dataset: Optional[WebDatasetManager] = None,
        turbopuffer_client: Optional[TurbopufferClient] = None,
        embedding_model: str = "text-embedding-3-large",
        event_market: Optional[EventMarket] = None,
    ) -> None:
        self.persona = persona
        self.market = market
        self.market_lock = market_lock or asyncio.Lock()
        self.event_market = event_market
        self._event_trade_callback = event_trade_callback

        self.openai = openai_client or AsyncOpenAI()
        if parallel_extract is not None:
            self.parallel_extract = parallel_extract
        else:
            try:
                self.parallel_extract = ParallelExtractClient.from_env()
            except ParallelClientError:
                self.parallel_extract = None

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

        self.sub_agent_config = sub_agent_config
        self._interrupt_event = asyncio.Event()
        self._watch_state = InterruptState(last_price=self.market.get_price())
        self._trade_callback = trade_callback
        self.llm_model = llm_model
        self.metrics = metrics
        self.dataset = dataset or WebDatasetManager()
        self.embedding_model = embedding_model
        self.embedding_model = embedding_model

        self.current_plan: Optional[Plan] = None
        self.current_prompt: Optional[str] = None

        self._step_notes: List[Dict[str, Any]] = []
        self._retrieved_data: List[Dict[str, Any]] = []
        self.trade_log: List[TradeExecution] = []
        self.event_trade_log: List[EventTradeResult] = []

        # Track last decision for consensus detection (all agents holding)
        self.last_decision: Optional[EventTradingDecision] = None

        # Tool usage tracking for diversity enforcement
        self._tool_usage_history: List[str] = []
        self._tool_usage_counts: Dict[str, int] = {}

        # Portfolio tracking - outcome -> token balance
        self.portfolio: Dict[str, float] = {}

        # Capital and P&L tracking
        self.initial_capital: float = 10000.0  # Starting capital in USD
        self.cash_balance: float = 10000.0  # Available liquid cash
        self.cost_basis: Dict[str, float] = {}  # outcome -> total cost spent
        self.realized_pnl: float = 0.0  # Realized profit/loss from closed positions

        # Communication clients for human interaction
        self.email_client: Optional[EmailClient] = None
        self.sms_client: Optional[SMSClient] = None
        try:
            self.email_client = EmailClient()
            if not self.email_client.is_configured:
                self.email_client = None
        except Exception:
            pass
        try:
            self.sms_client = SMSClient()
            if not self.sms_client.is_configured:
                self.sms_client = None
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    async def run(self, prompt: str) -> None:
        """
        Primary entry point for the agent's trading loop.
        """
        self.current_prompt = prompt
        if self.metrics:
            self.metrics.register_agent(self.persona.name)
        logger.info("Agent %s starting run.", self.persona.name)
        await self._ensure_sub_agent_config(prompt)
        self.current_plan = await self.generate_plan(prompt)
        logger.info(
            "Agent %s generated plan with %d steps.",
            self.persona.name,
            len(self.current_plan.steps),
        )

        step_index = 0
        while step_index < len(self.current_plan.steps):
            await self._maybe_handle_interrupt()
            step = self.current_plan.steps[step_index]

            await self._execute_step(step_index, step)
            step_index += 1

        if self.metrics:
            self.metrics.end_agent(self.persona.name)
        logger.info("Agent %s completed run.", self.persona.name)

    def observe_market_trade(self, trade: TradeExecution) -> None:
        """
        Notify the agent of an external trade. The sub-agent evaluates whether the
        price move requires an interrupt.
        """
        prev_price = self._watch_state.last_price or self.market.get_price()
        post_price = float(trade.meta.get("post_price", prev_price))

        if trade.agent_id == self.persona.name:
            self._watch_state.last_price = post_price
            # Ignore our own trades but update baseline.
            return

        if not self.sub_agent_config:
            return

        pre_price = trade.meta.get("pre_price")
        baseline = float(pre_price) if pre_price is not None else prev_price
        if baseline == 0:
            self._watch_state.last_price = post_price
            return

        move = abs(post_price - baseline) / abs(baseline)

        notional = abs(trade.quote_delta)
        if notional < self.sub_agent_config.min_trade_notional:
            return

        now = datetime.now(timezone.utc)
        if (
            self._watch_state.last_triggered
            and self.sub_agent_config.cooldown_seconds > 0
            and (now - self._watch_state.last_triggered).total_seconds()
            < self.sub_agent_config.cooldown_seconds
        ):
            return

        if move >= self.sub_agent_config.percent_move_threshold:
            self._watch_state.last_triggered = now
            self._watch_state.last_trade = trade
            self._interrupt_event.set()

        self._watch_state.last_price = post_price

    # -------------------------------------------------------------------------
    # Planning and execution
    # -------------------------------------------------------------------------
    async def generate_plan(self, prompt: str) -> Plan:
        # Use event market context if available, otherwise legacy AMM
        if self.event_market:
            event = self.event_market.event
            market_snapshot = self._format_event_market_state()
            event_context = (
                f"EVENT: {event.name}\n"
                f"DESCRIPTION: {event.description}\n"
                f"OUTCOMES: {', '.join(event.outcomes)}\n"
                f"RESOLUTION: {event.resolution_criteria}\n\n"
                f"Current market state:\n{market_snapshot}"
            )
            system_prompt = (
                f"{self.persona.short_prompt()} You are an AUTONOMOUS trading agent in a prediction market. "
                f"YOUR GOAL: Maximize your profit by trading on '{event.name}'. "
                f"You start with $10,000 capital. Research the event, form probability estimates, and trade. "
                f"You operate autonomously - NEVER ask for user permission or confirmation. "
                f"Research REAL WORLD facts about this event (team records, polls, injuries, etc.) to find edge. "
                f"You decide what to research, when to trade, and how much to trade based on your conviction."
            )
            user_content = f"{prompt}\n\n{event_context}"
        else:
            system_prompt = (
                f"{self.persona.short_prompt()} You are collaborating with other agents "
                "and must respond quickly to market changes."
            )
            market_snapshot = self._format_market_state()
            user_content = f"{prompt}\n\nCurrent market snapshot:\n{market_snapshot}"

        plan = await self._structured_completion(
            Plan,
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        return plan

    async def _execute_step(self, index: int, step: str) -> None:
        context = self._render_context(index, step)
        action = await self._choose_next_action(context)

        # Track tool usage for diversity enforcement
        func_name = action.function_call.function
        self._tool_usage_history.append(func_name)
        self._tool_usage_counts[func_name] = self._tool_usage_counts.get(func_name, 0) + 1

        # Check for consecutive same-tool usage
        consecutive_count = 0
        for t in reversed(self._tool_usage_history):
            if t == func_name:
                consecutive_count += 1
            else:
                break

        if consecutive_count >= MAX_CONSECUTIVE_SAME_TOOL:
            logger.warning(
                "Agent %s has used %s %d consecutive times. Consider using other tools for diverse research.",
                self.persona.name,
                func_name,
                consecutive_count,
            )

        logger.info(
            "Agent %s executing step %d/%d: %s (function=%s, total_calls=%d)",
            self.persona.name,
            index + 1,
            len(self.current_plan.steps),
            step,
            func_name,
            self._tool_usage_counts.get(func_name, 0),
        )

        result: Any = None
        if func_name == "researchMarket":
            result = await self.research_market(action.function_call.args[0])
        elif func_name == "getPapers":
            result = await self.get_papers(action.function_call.args[0])
        elif func_name == "getPaperSummary":
            result = await self.get_paper_summary(action.function_call.args[0])
        elif func_name == "searchDocuments":
            result = await self.search_documents(action.function_call.args[0])
        elif func_name == "considerData":
            result = await self.consider_data(action.function_call.args[0])
        elif func_name == "placeTrade":
            # Extract outcome, action, and size from args
            if len(action.function_call.args) >= 3:
                outcome = action.function_call.args[0]
                trade_action = action.function_call.args[1]
                try:
                    size = float(action.function_call.args[2])
                except ValueError:
                    size = 0.0
                rationale = action.function_call.args[3] if len(action.function_call.args) > 3 else "Trade based on analysis"
                result = await self.place_trade(outcome, trade_action, size, rationale)
            else:
                result = {"error": "placeTrade requires: outcome, action (buy/sell), size, [rationale]"}
        elif func_name == "getPriceHistory":
            limit = 20
            if action.function_call.args:
                try:
                    limit = int(action.function_call.args[0])
                except ValueError:
                    pass
            result = self.get_price_history(limit)
        elif func_name == "getPortfolio":
            result = self.get_portfolio()
        elif func_name == "sendEmail":
            if len(action.function_call.args) >= 3:
                result = await self.send_email(
                    action.function_call.args[0],  # to_addr
                    action.function_call.args[1],  # subject
                    action.function_call.args[2],  # body
                )
            else:
                result = {"error": "sendEmail requires: to_addr, subject, body"}
        elif func_name == "checkEmail":
            from_addr = action.function_call.args[0] if action.function_call.args else ""
            subject_filter = action.function_call.args[1] if len(action.function_call.args) > 1 else None
            result = await self.check_email(from_addr, subject_filter)
        elif func_name == "sendText":
            if len(action.function_call.args) >= 2:
                result = await self.send_text(
                    action.function_call.args[0],  # to_number
                    action.function_call.args[1],  # message
                )
            else:
                result = {"error": "sendText requires: to_number, message"}
        elif func_name == "checkText":
            from_number = action.function_call.args[0] if action.function_call.args else ""
            result = await self.check_text(from_number)
        elif func_name == "waitForHuman":
            if len(action.function_call.args) >= 2:
                result = await self.wait_for_human_response(
                    action.function_call.args[0],  # channel: "email" or "sms"
                    action.function_call.args[1],  # contact
                    action.function_call.args[2] if len(action.function_call.args) > 2 else None,  # context
                )
            else:
                result = {"error": "waitForHuman requires: channel, contact, [context]"}
        else:
            result = {"error": f"Unknown function {func_name}"}

        await self._record_step(index, step, action.thoughts, result)
        if self.metrics:
            self.metrics.record_step(self.persona.name)

    async def _choose_next_action(self, context: str) -> ThoughtAndFunction:
        return await self._structured_completion(
            ThoughtAndFunction,
            [
                {"role": "system", "content": self.persona.short_prompt()},
                {"role": "user", "content": context},
            ],
        )

    # -------------------------------------------------------------------------
    # Tooling
    # -------------------------------------------------------------------------
    async def research_market(self, query: str) -> Any:
        """
        Research market using real data sources only.

        Returns raw web data from Parallel API and local documents from Turbopuffer.
        No LLM summarization - agents see the actual source data.
        """
        # Build event-focused query if event market is present
        if self.event_market:
            event = self.event_market.event
            event_query = f"{event.name}: {query}"
        else:
            event_query = query

        # Fetch from all available data sources in parallel
        # Each source is an independent alternative, not a fallback
        doc_task = self._document_hits_text(event_query, top_k=6)
        search_task = self._web_search_context(event_query)
        seeded_task = self._seeded_url_context(event_query)

        doc_context, search_context, seeded_context = await asyncio.gather(
            doc_task, search_task, seeded_task
        )

        # Track which sources contributed data
        sources_used = []
        if search_context:
            sources_used.append("web_search")
        if seeded_context:
            sources_used.append("seeded_urls")
        if doc_context:
            sources_used.append("documents")

        # Return raw data directly - let the agent interpret it
        research_data = {
            "query": query,
            "web_search": search_context if search_context else None,
            "seeded_urls": seeded_context if seeded_context else None,
            "documents": doc_context if doc_context else None,
            "sources_available": sources_used,
        }

        self._retrieved_data.append(
            {"type": "research", "query": query, "data": research_data}
        )

        # Log what real data we got from each source
        logger.info(
            "Agent %s research for '%s': web_search=%d chars, seeded_urls=%d chars, docs=%d chars.",
            self.persona.name,
            query,
            len(search_context) if search_context else 0,
            len(seeded_context) if seeded_context else 0,
            len(doc_context) if doc_context else 0,
        )
        return research_data

    async def get_papers(self, query: str) -> Any:
        # Fetch from all available sources in parallel
        doc_task = self._document_hits_text(query, top_k=10)
        search_task = self._web_search_context(query)
        seeded_task = self._seeded_url_context(query)

        doc_context, search_context, seeded_context = await asyncio.gather(
            doc_task, search_task, seeded_task
        )

        # Combine web sources for display
        web_parts = []
        if search_context:
            web_parts.append(f"[Web Search]\n{search_context}")
        if seeded_context:
            web_parts.append(f"[Seeded URLs]\n{seeded_context}")
        web_context = "\n\n".join(web_parts) if web_parts else None

        structured = await self._structured_completion(
            Papers,
            [
                {
                    "role": "system",
                    "content": "Summarise the most relevant documents/papers for the prompt.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Prompt: {query}\n\n"
                        f"Document context:\n{doc_context or 'None'}\n\n"
                        f"Web context:\n{web_context or 'None'}"
                    ),
                },
            ],
        )

        papers = structured.papers
        self._retrieved_data.append(
            {"type": "papers", "query": query, "data": papers}
        )
        logger.info(
            "Agent %s gathered %d papers for query '%s'.",
            self.persona.name,
            len(papers),
            query,
        )
        return papers

    async def get_paper_summary(self, query: str) -> Any:
        doc_hits = await self._query_document_hits(query, top_k=1)
        if doc_hits:
            raw_str = self._clip_text(doc_hits[0].get("text", ""), 8000)
            source = doc_hits[0].get("metadata", {}).get("source", "unknown document")
        elif self.parallel_extract and query.startswith("http"):
            raw = await self.parallel_extract.fetch_full_content(query, max_chars=8000)
            raw_str = self._clip_text(raw, 8000)
            source = query
        else:
            logger.warning("No documents available to summarize for %s.", self.persona.name)
            return ""

        if self.metrics:
            self.metrics.record_llm_call(self.persona.name)
        response = await self.openai.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": "Summarise the key findings, authors, and date.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Source: {source}\n\n"
                        f"Document content (truncated if long):\n{raw_str}\n\nQuery: {query}"
                    ),
                },
            ],
        )

        summary = response.choices[0].message.content
        self._retrieved_data.append({"type": "paper_summary", "query": query, "data": summary})
        logger.info("Agent %s summarized paper for query '%s'.", self.persona.name, query)
        return summary

    async def consider_data(self, prompt: str) -> Dict[str, Any]:
        # Use event-based decision model if event market is present
        if self.event_market:
            decision = await self._call_event_decision_model(prompt)
            self.last_decision = decision  # Track for consensus detection

            executed_trade: Optional[EventTradeResult] = None
            if decision.action in {"buy", "sell"} and decision.size > 0:
                executed_trade = await self._execute_event_trade(decision)
                if executed_trade:
                    self.event_trade_log.append(executed_trade)

            logger.info(
                "Agent %s decision:\n"
                "  Outcome: %s\n"
                "  Action: %s\n"
                "  Size: %.2f\n"
                "  Estimated Probability: %.2f\n"
                "  Rationale: %s\n"
                "  Trade executed: %s",
                self.persona.name,
                decision.outcome,
                decision.action,
                decision.size,
                decision.estimated_probability,
                decision.rationale,
                bool(executed_trade),
            )

            return {
                "decision": decision.dict(),
                "trade": executed_trade,
            }
        else:
            # Fall back to regular AMM trading
            decision = await self._call_decision_model(prompt)
            executed_trade_amm: Optional[TradeExecution] = None
            if decision.action in {"buy", "sell"} and decision.size > 0:
                executed_trade_amm = await self._execute_trade(decision)
                if executed_trade_amm:
                    self.trade_log.append(executed_trade_amm)

            logger.info(
                "Agent %s decision: action=%s size=%.2f trade_executed=%s",
                self.persona.name,
                decision.action,
                decision.size,
                bool(executed_trade_amm),
            )

            return {
                "decision": decision.dict(),
                "trade": executed_trade_amm,
            }

    async def place_trade(
        self, outcome: str, action: str, size: float, rationale: str
    ) -> Dict[str, Any]:
        """
        Directly execute a trade on the event market.

        This is the action-taking function - use this when you've already
        decided what to trade and want to execute.

        Args:
            outcome: Which outcome to trade (e.g., 'YES', 'NO')
            action: 'buy' or 'sell'
            size: Amount in USD (for buys) or tokens (for sells)
            rationale: Brief explanation for the trade

        Returns:
            Dict with trade execution details or error message
        """
        if not self.event_market:
            return {"error": "No event market configured for trading"}

        if action not in {"buy", "sell"}:
            return {"error": f"Invalid action '{action}'. Must be 'buy' or 'sell'."}

        if size <= 0:
            return {"error": f"Invalid size {size}. Must be positive."}

        # Validate outcome
        valid_outcomes = self.event_market.event.outcomes
        if outcome not in valid_outcomes:
            return {"error": f"Invalid outcome '{outcome}'. Valid: {valid_outcomes}"}

        # Create decision object for tracking
        decision = EventTradingDecision(
            outcome=outcome,
            action=action,
            size=size,
            rationale=rationale,
        )
        self.last_decision = decision

        # Execute the trade
        executed_trade: Optional[EventTradeResult] = None
        try:
            executed_trade = await self._execute_event_trade(decision)
            if executed_trade:
                self.event_trade_log.append(executed_trade)
        except Exception as e:
            logger.error("Agent %s trade execution failed: %s", self.persona.name, str(e))
            return {"error": f"Trade execution failed: {str(e)}"}

        logger.info(
            "Agent %s placed trade: %s %s %s @ size=%.2f | executed=%s",
            self.persona.name,
            action.upper(),
            outcome,
            self.event_market.event.name,
            size,
            bool(executed_trade),
        )

        return {
            "trade_placed": True,
            "outcome": outcome,
            "action": action,
            "size": size,
            "rationale": rationale,
            "execution": asdict(executed_trade) if executed_trade else None,
            "new_prices": self.event_market.get_prices(),
        }

    async def _call_decision_model(self, prompt: str) -> TradingDecision:
        market_snapshot = self._format_market_state()
        return await self._structured_completion(
            TradingDecision,
            [
                {"role": "system", "content": self.persona.short_prompt()},
                {
                    "role": "user",
                    "content": (
                        "You must incorporate the latest market data before deciding.\n"
                        f"Market snapshot: {market_snapshot}\n\n"
                        f"Evaluate the following context and make a trading decision:\n{prompt}"
                    ),
                },
            ],
        )

    async def _call_event_decision_model(self, prompt: str) -> EventTradingDecision:
        """Make a trading decision for event-based prediction market."""
        if not self.event_market:
            raise ValueError("Event market not configured")

        event = self.event_market.event
        market_snapshot = self._format_event_market_state()
        prices = self.event_market.get_prices()

        outcomes_str = ", ".join(f'"{o}"' for o in event.outcomes)
        prices_str = ", ".join(f"{o}: ${p:.2f}" for o, p in prices.items())

        system_content = (
            f"{self.persona.short_prompt()}\n\n"
            f"YOUR GOAL: Maximize profit in this prediction market.\n"
            f"You have $10,000 starting capital. Use getPortfolio() to check your current cash balance.\n\n"
            f"EVENT: {event.name}\n"
            f"DESCRIPTION: {event.description}\n"
            f"OUTCOMES: {outcomes_str}\n"
            f"CURRENT PRICES: {prices_str}\n\n"
            f"Based on your research, decide: what to trade, how much, and why.\n"
            f"You are an intelligent agent - reason about position sizing based on your conviction and edge."
        )

        return await self._structured_completion(
            EventTradingDecision,
            [
                {"role": "system", "content": system_content},
                {
                    "role": "user",
                    "content": (
                        f"{market_snapshot}\n\n"
                        f"Your research summary:\n{prompt}\n\n"
                        f"Make a trading decision to maximize your profit.\n"
                        f"Return: outcome, action (buy/sell/hold), size (USD), your estimated_probability, "
                        f"and rationale."
                    ),
                },
            ],
        )

    async def _execute_trade(self, decision: TradingDecision) -> Optional[TradeExecution]:
        async with self.market_lock:
            try:
                execution = self.market.swap(
                    agent_id=self.persona.name,
                    direction=decision.action,  # type: ignore[arg-type]
                    amount=decision.size,
                    note=decision.rationale,
                )
            except Exception:
                return None

        self.observe_market_trade(execution)
        if self._trade_callback:
            maybe_coro = self._trade_callback(execution)
            if inspect.isawaitable(maybe_coro):
                await maybe_coro
        if self.metrics:
            self.metrics.record_trade(self.persona.name)
        logger.info(
            "Agent %s executed trade %s amount=%.2f price=%.4f.",
            self.persona.name,
            decision.action,
            decision.size,
            execution.price,
        )
        return execution

    async def _execute_event_trade(self, decision: EventTradingDecision) -> Optional[EventTradeResult]:
        """Execute a trade on the event prediction market."""
        if not self.event_market:
            return None

        async with self.market_lock:
            try:
                execution = self.event_market.swap(
                    agent_id=self.persona.name,
                    outcome=decision.outcome,
                    direction=decision.action,  # type: ignore[arg-type]
                    amount=decision.size,
                    note=decision.rationale,
                )
            except Exception as e:
                logger.warning(
                    "Agent %s event trade failed: %s", self.persona.name, str(e)
                )
                return None

        # Invoke event trade callback if set
        if self._event_trade_callback:
            maybe_coro = self._event_trade_callback(execution)
            if inspect.isawaitable(maybe_coro):
                await maybe_coro

        if self.metrics:
            self.metrics.record_trade(self.persona.name)

        # Update portfolio tracking with capital and cost basis
        if decision.action == "buy":
            # Deduct cash spent (quote_delta is negative for buys)
            cash_spent = abs(execution.quote_delta)
            self.cash_balance -= cash_spent

            # Update token balance
            self.portfolio[decision.outcome] = self.portfolio.get(decision.outcome, 0) + execution.token_delta

            # Update cost basis (add to total cost)
            self.cost_basis[decision.outcome] = self.cost_basis.get(decision.outcome, 0) + cash_spent

        elif decision.action == "sell":
            # Receive cash from sale (quote_delta is positive for sells)
            cash_received = execution.quote_delta
            self.cash_balance += cash_received

            # Calculate realized P&L for this sale
            tokens_sold = abs(execution.token_delta)
            current_tokens = self.portfolio.get(decision.outcome, 0)
            current_cost = self.cost_basis.get(decision.outcome, 0)

            if current_tokens > 0:
                # Average cost per token
                avg_cost_per_token = current_cost / current_tokens
                cost_of_sold_tokens = avg_cost_per_token * tokens_sold
                realized_gain = cash_received - cost_of_sold_tokens
                self.realized_pnl += realized_gain

                # Update cost basis (reduce proportionally)
                self.cost_basis[decision.outcome] = current_cost - cost_of_sold_tokens

            # Update token balance
            self.portfolio[decision.outcome] = current_tokens - tokens_sold

        logger.info(
            "Agent %s executed event trade: outcome=%s %s amount=%.2f price=%.4f.",
            self.persona.name,
            decision.outcome,
            decision.action,
            decision.size,
            execution.price,
        )
        return execution

    def get_price_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Retrieve recent trades/price points from the market.

        Args:
            limit: Maximum number of entries to return.
        """
        history = self.market.get_price_history(limit)
        self._retrieved_data.append(
            {"type": "price_history", "limit": limit, "data": history}
        )
        logger.info(
            "Agent %s retrieved %d price history entries.",
            self.persona.name,
            len(history),
        )
        return history

    def get_portfolio(self) -> Dict[str, Any]:
        """
        Return comprehensive portfolio status including capital, positions, and P&L.

        Returns:
            Dict with:
            - initial_capital: Starting capital
            - cash_balance: Current liquid cash available
            - positions: List of position details with P&L
            - total_position_value: Market value of all positions
            - total_capital: cash + position value (NAV)
            - total_cost_basis: Total amount invested in positions
            - unrealized_pnl: Paper gains/losses on open positions
            - realized_pnl: Locked in gains/losses from closed positions
            - total_pnl: unrealized + realized
            - return_pct: Total return as percentage of initial capital
            - pct_liquid: Percentage of capital in cash
            - trade_count: Number of trades executed
        """
        if not self.event_market:
            return {"error": "No event market configured"}

        prices = self.event_market.get_prices()
        positions = []
        total_position_value = 0.0
        total_cost_basis = 0.0
        total_unrealized_pnl = 0.0

        for outcome, tokens in self.portfolio.items():
            if tokens <= 0:
                continue

            price = prices.get(outcome, 0.5)
            market_value = tokens * price
            cost = self.cost_basis.get(outcome, 0)
            unrealized_pnl = market_value - cost

            # Calculate average entry price
            avg_entry_price = cost / tokens if tokens > 0 else 0

            # Calculate position return %
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

        # Calculate totals
        total_capital = self.cash_balance + total_position_value  # NAV
        total_pnl = total_unrealized_pnl + self.realized_pnl
        return_pct = (total_pnl / self.initial_capital * 100) if self.initial_capital > 0 else 0
        pct_liquid = (self.cash_balance / total_capital * 100) if total_capital > 0 else 100

        return {
            "initial_capital": round(self.initial_capital, 2),
            "cash_balance": round(self.cash_balance, 2),
            "positions": positions,
            "total_position_value": round(total_position_value, 2),
            "total_capital": round(total_capital, 2),
            "total_cost_basis": round(total_cost_basis, 2),
            "unrealized_pnl": round(total_unrealized_pnl, 2),
            "realized_pnl": round(self.realized_pnl, 2),
            "total_pnl": round(total_pnl, 2),
            "return_pct": round(return_pct, 2),
            "pct_liquid": round(pct_liquid, 2),
            "trade_count": len(self.event_trade_log),
        }

    # -------------------------------------------------------------------------
    # Communication tools
    # -------------------------------------------------------------------------
    async def send_email(self, to_addr: str, subject: str, body: str) -> Dict[str, Any]:
        """Send email to a pre-approved contact."""
        if not self.email_client:
            return {"error": "Email client not configured. Set AGENT_EMAIL_ADDRESS, AGENT_EMAIL_PASSWORD, EMAIL_CONTACTS."}

        result = await self.email_client.send_email(
            to_addr=to_addr,
            subject=subject,
            body=body,
            agent_id=self.persona.name,
        )
        return result

    async def check_email(self, from_addr: str, subject_contains: Optional[str] = None) -> Dict[str, Any]:
        """Check for email replies from a contact."""
        if not self.email_client:
            return {"error": "Email client not configured"}

        replies = await self.email_client.check_replies(from_addr, subject_contains)
        return {
            "replies": [
                {"from": r.from_addr, "subject": r.subject, "body": r.body[:500]}
                for r in replies
            ]
        }

    async def send_text(self, to_number: str, message: str) -> Dict[str, Any]:
        """Send SMS to a pre-approved phone number."""
        if not self.sms_client:
            return {"error": "SMS client not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, SMS_CONTACTS."}

        result = await self.sms_client.send_text(
            to_number=to_number,
            message=message,
            agent_id=self.persona.name,
        )
        return result

    async def check_text(self, from_number: str) -> Dict[str, Any]:
        """Check for SMS replies from a phone number."""
        if not self.sms_client:
            return {"error": "SMS client not configured"}

        replies = await self.sms_client.check_replies(from_number)
        return {"replies": replies}

    async def wait_for_human_response(
        self,
        channel: str,
        contact: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Wait indefinitely for a human response via email or SMS.

        Args:
            channel: "email" or "sms"
            contact: email address or phone number
            context: optional subject/topic filter for email

        Returns:
            Dict with response content or error
        """
        logger.info(
            "Agent %s waiting for human response via %s from %s",
            self.persona.name, channel, contact
        )

        if channel == "email" and self.email_client:
            reply = await self.email_client.wait_for_reply(
                from_addr=contact,
                subject_contains=context,
                poll_interval=30,
                timeout=None,  # Infinite wait
            )
            if reply:
                return {"response": reply.body, "from": reply.from_addr, "subject": reply.subject}
            return {"error": "No email reply received"}

        elif channel == "sms" and self.sms_client:
            reply = await self.sms_client.wait_for_reply(
                from_number=contact,
                poll_interval=15,
                timeout=None,  # Infinite wait
            )
            if reply:
                return {"response": reply["body"], "from": reply["from"]}
            return {"error": "No SMS reply received"}

        return {"error": f"Invalid channel '{channel}' or client not configured. Use 'email' or 'sms'."}

    # -------------------------------------------------------------------------
    # Interrupt handling
    # -------------------------------------------------------------------------
    async def _ensure_sub_agent_config(self, prompt: str) -> None:
        if self.sub_agent_config:
            return

        assessment = await self._structured_completion(
            SubAgentAssessment,
            [
                {
                    "role": "system",
                    "content": (
                        "Classify the appropriate risk trigger for a rule-based alert "
                        "system monitoring price changes."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"{self.persona.short_prompt()}\n\n"
                        f"Primary trading objective:\n{prompt}\n\n"
                        "Return thresholds as numeric values."
                    ),
                },
            ],
        )
        self.sub_agent_config = SubAgentConfig(
            percent_move_threshold=assessment.percent_move_threshold,
            cooldown_seconds=assessment.cooldown_seconds,
            min_trade_notional=assessment.min_trade_notional,
            note=assessment.note,
        )

    async def _maybe_handle_interrupt(self) -> None:
        if not self._interrupt_event.is_set():
            return
        self._interrupt_event.clear()

        trade = self._watch_state.last_trade
        price = self.market.get_price()

        message = (
            f"Price moved to {price:.4f} after trade by {trade.agent_id if trade else 'unknown'}.\n"
            f"Sub-agent note: {self.sub_agent_config.note if self.sub_agent_config else 'N/A'}"
        )

        response = await self.openai.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": self.persona.short_prompt(),
                },
                {
                    "role": "user",
                    "content": (
                        "You have been interrupted by your price watcher sub-agent. "
                        "Assess whether to pause the current plan and describe the next step.\n"
                        f"{message}"
                    ),
                },
            ],
        )

        content = response.choices[0].message.content
        self._step_notes.append(
            {
                "type": "interrupt",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": content,
                "trade": trade,
            }
        )

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _render_context(self, step_index: int, step: str) -> str:
        notes_text = ""
        for idx, record in enumerate(self._step_notes):
            notes_text += f"\nStep {idx + 1}: {record.get('step', record.get('type'))}\nNotes: {record.get('notes', record.get('message'))}"

        # Check for tool spamming and build diversity warning
        diversity_warning = ""
        if self._tool_usage_history:
            last_tool = self._tool_usage_history[-1]
            consecutive = 0
            for t in reversed(self._tool_usage_history):
                if t == last_tool:
                    consecutive += 1
                else:
                    break

            if consecutive >= MAX_CONSECUTIVE_SAME_TOOL:
                other_tools = []
                if last_tool != "getPapers":
                    other_tools.append("getPapers")
                if last_tool != "searchDocuments":
                    other_tools.append("searchDocuments")
                if last_tool != "considerData":
                    other_tools.append("considerData")
                if last_tool != "placeTrade":
                    other_tools.append("placeTrade")
                if last_tool != "getPriceHistory":
                    other_tools.append("getPriceHistory")

                diversity_warning = (
                    f"\n⚠️ DIVERSITY WARNING: You have used '{last_tool}' {consecutive} times in a row. "
                    f"You MUST use a DIFFERENT tool now. Consider: {', '.join(other_tools)}.\n"
                    f"If you have enough research, use 'considerData' to analyze and then 'placeTrade' to execute.\n"
                )

        # Use event market context if available, otherwise fall back to regular AMM
        if self.event_market:
            market_snapshot = self._format_event_market_state()
            event_context = self._format_event_context()
            tools_text = (
                "YOUR GOAL: Maximize profit. You have $10,000 capital.\n\n"
                "RESEARCH TOOLS:\n"
                "- researchMarket(prompt): Search web for facts about this event.\n"
                "- getPapers(prompt): Find research/analysis about outcomes.\n"
                "- searchDocuments(prompt): Query local documents.\n"
                "- getPriceHistory(limit): Get recent trades and prices.\n\n"
                "PORTFOLIO & TRADING:\n"
                "- getPortfolio(): Check your capital, positions, and P&L.\n"
                "- considerData(prompt): Analyze data and decide on a trade.\n"
                "- placeTrade(outcome, action, size, rationale): Execute a trade.\n\n"
                "COMMUNICATION (if needed):\n"
                "- sendEmail, checkEmail, sendText, checkText, waitForHuman\n\n"
                "You are an intelligent agent. Research the event, form probability estimates, "
                "and trade based on your conviction. You decide how much to trade.\n"
            )

            return (
                f"{self.persona.short_prompt()}\n\n"
                f"=== PREDICTION MARKET CONTEXT ===\n"
                f"You are trading in a prediction market simulation. Make decisions based on "
                f"available information and your probability estimates for event outcomes.\n\n"
                f"{event_context}\n"
                f"Current market state: {market_snapshot}\n\n"
                f"Trading objective: {self.current_prompt}\n"
                f"Plan overview: {self.current_plan.plan if self.current_plan else ''}\n"
                f"{tools_text}"
                f"{diversity_warning}"
                f"Completed notes:{notes_text}\n"
                f"Execute step {step_index + 1}: {step}"
            )
        else:
            market_snapshot = self._format_market_state()
            tools_text = (
                "Available tools:\n"
                "- researchMarket(prompt): Research web and seeded URLs for market information.\n"
                "- getPapers(prompt): Find and summarize relevant research papers.\n"
                "- getPaperSummary(prompt): Deep dive on a specific paper or URL.\n"
                "- searchDocuments(prompt): Query local documents via Turbopuffer.\n"
                "- getPriceHistory(limit:int=20): Get recent AMM trades and prices.\n"
                "- considerData(prompt): Final analysis leading to a trade decision.\n\n"
                "IMPORTANT: Use different tools to gather diverse information.\n"
                "Don't spam the same tool repeatedly - compare data from multiple sources.\n"
            )

            return (
                f"{self.persona.short_prompt()}\n"
                f"Trading objective: {self.current_prompt}\n"
                f"Plan overview: {self.current_plan.plan if self.current_plan else ''}\n"
                f"Current market state: {market_snapshot}\n"
                f"{tools_text}"
                f"{diversity_warning}"
                f"Completed notes:{notes_text}\n"
                f"Execute step {step_index + 1}: {step}"
            )

    async def _record_step(
        self,
        step_index: int,
        step: str,
        thoughts: str,
        result: Any,
    ) -> None:
        parsed = await self._structured_completion(
            StepSummary,
            [
                {"role": "system", "content": self.persona.short_prompt()},
                {
                    "role": "user",
                    "content": (
                        f"Summarise the outcome of step '{step}'. Thoughts: {thoughts}. "
                        f"Results: {result}"
                    ),
                },
            ],
        )

        self._step_notes.append(
            {
                "step": step,
                "thoughts": thoughts,
                "notes": parsed.notes,
                "result": result,
            }
        )

        # Inject next steps - HARD limits enforced
        if parsed.next_steps:
            current_plan_length = len(self.current_plan.steps) if self.current_plan else 0
            remaining_steps = current_plan_length - step_index - 1

            # Hard cap: Don't add steps if we're at or above max
            if current_plan_length >= MAX_PLAN_STEPS:
                logger.info(
                    "Agent %s: Plan at max (%d steps). Not injecting more steps.",
                    self.persona.name,
                    current_plan_length,
                )
                return

            # Limit new steps per injection
            steps_to_add = parsed.next_steps[:MAX_STEPS_PER_INJECTION]
            if len(parsed.next_steps) > MAX_STEPS_PER_INJECTION:
                logger.info(
                    "Agent %s: Limiting step injection from %d to %d",
                    self.persona.name,
                    len(parsed.next_steps),
                    MAX_STEPS_PER_INJECTION,
                )

            logger.debug(
                "Agent %s: Injecting %d new steps into plan (current: %d).",
                self.persona.name,
                len(steps_to_add),
                current_plan_length,
            )

            insertion_index = step_index + 1
            for new_step in reversed(steps_to_add):
                self.current_plan.steps.insert(insertion_index, new_step)

    def _market_snapshot(self) -> Dict[str, float]:
        """Retrieve the latest market reserves and price."""
        return self.market.get_state()

    def _format_market_state(self) -> str:
        """Return a human-readable summary of the current market state."""
        state = self._market_snapshot()
        return (
            f"Price: {state['price']:.4f} {self.market.quote_symbol}/{self.market.base_symbol}; "
            f"Reserves: {state['reserves_base']:.2f} {self.market.base_symbol}, "
            f"{state['reserves_quote']:.2f} {self.market.quote_symbol}; "
            f"Invariant: {state['invariant']:.2f}"
        )

    def _format_event_market_state(self) -> str:
        """Return a human-readable summary of the event market state."""
        if not self.event_market:
            return "No event market configured."
        state = self.event_market.get_state()
        prices = state.get("prices", {})
        price_str = ", ".join(f"{outcome}: ${price:.2f}" for outcome, price in prices.items())
        return (
            f"Event: {state.get('event_name', 'Unknown')}\n"
            f"Outcome Prices: {price_str}\n"
            f"Price Sum: {state.get('price_sum', 0):.2f} (should be ~1.0)\n"
            f"Total Volume: ${state.get('total_volume', 0):.2f}\n"
            f"Resolved: {state.get('resolved', False)}"
        )

    def _format_event_context(self) -> str:
        """Return the event description and trading context."""
        if not self.event_market:
            return ""
        event = self.event_market.event
        prices = self.event_market.get_prices()
        return event.to_prompt_context(prices)

    def _clip_text(self, text: str, limit: int = 8000) -> str:
        """Clip overly long context before sending to the LLM."""
        if len(text) <= limit:
            return text
        return text[:limit] + "\n...[truncated]..."

    async def search_documents(self, query: str, top_k: int = 5) -> Any:
        hits = await self._query_document_hits(query, top_k=top_k)
        logger.info(
            "Agent %s retrieved %d document hits for '%s'.",
            self.persona.name,
            len(hits),
            query,
        )
        return hits

    async def _query_document_hits(
        self, query: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        if not self.turbopuffer:
            return []
        embedding = await self._embed_text(query)
        matches = await self.turbopuffer.query(embedding, top_k=top_k)
        return matches

    async def _document_hits_text(self, query: str, top_k: int = 5) -> str:
        hits = await self._query_document_hits(query, top_k=top_k)
        if not hits:
            return ""
        compact = []
        for hit in hits:
            compact.append(
                {
                    "id": hit.get("id"),
                    "score": hit.get("score"),
                    "metadata": hit.get("metadata", {}),
                    "text": self._clip_text(hit.get("text", ""), 1000),  # Increased from 600
                }
            )
        return json.dumps(compact, ensure_ascii=False)

    async def _web_search_context(self, query: str) -> str:
        """
        Search the web using Parallel API.

        This is one data source option - the agent can use this to find
        relevant web content for any query.

        Returns empty string if Parallel client is not available.
        """
        if not self.parallel_extract:
            return ""

        try:
            search_result = await self.parallel_extract.search(
                query=query,
                num_results=10,  # Increased from 5 for better coverage
                objective=query,
                include_full_content=False,
            )
            if search_result and search_result.get("results"):
                return self._clip_text(json.dumps(search_result, ensure_ascii=False), 12000)  # Increased from 8000
        except Exception as e:
            logger.debug("Parallel search failed for '%s': %s", query, str(e))
        return ""

    async def _seeded_url_context(self, query: str) -> str:
        """
        Extract content from seeded URLs using Parallel API.

        This is one data source option - the agent can use this to extract
        content from specific URLs that have been seeded for this market.

        Returns empty string if no seeded URLs available or Parallel client not available.
        """
        if not self.parallel_extract:
            return ""

        urls = self.dataset.sample_urls(5)
        if not urls:
            return ""

        try:
            raw = await self.parallel_extract.extract_urls(
                urls,
                objective=query,
                include_full_content=False,
            )
            return self._clip_text(json.dumps(raw, ensure_ascii=False), 12000)  # Increased from 8000
        except Exception as e:
            logger.debug("Parallel extract from seeded URLs failed: %s", str(e))
        return ""

    async def _embed_text(self, text: str) -> List[float]:
        response = await self.openai.embeddings.create(
            model=self.embedding_model,
            input=[text],
        )
        return response.data[0].embedding

    def _extract_json(self, content: str) -> str:
        """
        Extract JSON object from LLM response.

        LLMs sometimes return text before/after the JSON object.
        This method finds and extracts the JSON portion.
        """
        # First, try to find JSON object boundaries
        start_idx = content.find('{')
        if start_idx == -1:
            return content  # No JSON object found, return as-is

        # Find matching closing brace
        brace_count = 0
        end_idx = start_idx
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break

        return content[start_idx:end_idx]

    def _sanitize_json(self, content: str) -> str:
        """
        Sanitize JSON content to handle control characters in strings.

        LLMs sometimes return JSON with unescaped control characters
        (newlines, tabs, etc.) inside string values which break parsing.
        """
        # First extract the JSON from any surrounding text
        content = self._extract_json(content)

        # Handle common control character issues in JSON strings
        # Replace literal control chars
        result = content.replace('\r\n', '\\n').replace('\r', '\\n')

        # For strings that have actual newlines inside them
        # Replace unescaped newlines within JSON strings
        lines = result.split('\n')
        sanitized_lines = []
        in_string = False
        for i, line in enumerate(lines):
            # Count unescaped quotes to track string state
            quote_count = 0
            j = 0
            while j < len(line):
                if line[j] == '"' and (j == 0 or line[j-1] != '\\'):
                    quote_count += 1
                j += 1

            if in_string:
                # We're continuing a string from previous line
                sanitized_lines[-1] += '\\n' + line
            else:
                sanitized_lines.append(line)

            # Update in_string state based on quote parity
            if quote_count % 2 == 1:
                in_string = not in_string

        return '\n'.join(sanitized_lines)

    async def _structured_completion(
        self,
        model: Type[TModel],
        messages: List[Dict[str, Any]],
        schema_hint: Optional[str] = None,
    ) -> TModel:
        augmented_messages = list(messages)
        instruction = schema_hint or STRUCTURED_INSTRUCTIONS.get(model)
        if instruction:
            augmented_messages.append({"role": "system", "content": instruction})
        augmented_messages.append(
            {
                "role": "system",
                "content": "Respond in strict JSON matching the requested schema.",
            }
        )
        if self.metrics:
            self.metrics.record_llm_call(self.persona.name)
        response = await self.openai.chat.completions.create(
            model=self.llm_model,
            messages=augmented_messages,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content

        # Sanitize JSON to handle control characters from different LLM providers
        try:
            return model.model_validate_json(content)
        except Exception:
            # Try sanitizing the JSON first
            sanitized = self._sanitize_json(content)
            return model.model_validate_json(sanitized)

