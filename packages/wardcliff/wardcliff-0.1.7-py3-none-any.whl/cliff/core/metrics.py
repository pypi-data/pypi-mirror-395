"""
Simulation metrics recording.

Migrated from metrics.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Dict, Optional


@dataclass
class AgentMetrics:
    agent_id: str
    steps_completed: int = 0
    trades_executed: int = 0
    llm_calls: int = 0
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None

    @property
    def duration_seconds(self) -> float:
        end = self.end_time or datetime.utcnow()
        return (end - self.start_time).total_seconds()


@dataclass
class SimulationMetrics:
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    agent_metrics: Dict[str, AgentMetrics] = field(default_factory=dict)

    def duration_seconds(self) -> float:
        end = self.end_time or datetime.utcnow()
        return (end - self.start_time).total_seconds()


class MetricsRecorder:
    """
    Thread-safe recorder for simulation benchmarks.
    """

    def __init__(self) -> None:
        self.simulation = SimulationMetrics()
        self._lock = Lock()

    def register_agent(self, agent_id: str) -> None:
        with self._lock:
            if agent_id not in self.simulation.agent_metrics:
                self.simulation.agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id)

    def record_step(self, agent_id: str) -> None:
        with self._lock:
            self._ensure_agent(agent_id)
            self.simulation.agent_metrics[agent_id].steps_completed += 1

    def record_trade(self, agent_id: str) -> None:
        with self._lock:
            self._ensure_agent(agent_id)
            self.simulation.agent_metrics[agent_id].trades_executed += 1

    def record_llm_call(self, agent_id: str) -> None:
        with self._lock:
            self._ensure_agent(agent_id)
            self.simulation.agent_metrics[agent_id].llm_calls += 1

    def end_agent(self, agent_id: str) -> None:
        with self._lock:
            self._ensure_agent(agent_id)
            self.simulation.agent_metrics[agent_id].end_time = datetime.utcnow()

    def finish_simulation(self) -> None:
        with self._lock:
            self.simulation.end_time = datetime.utcnow()

    def summary(self) -> Dict[str, Dict[str, float]]:
        with self._lock:
            return {
                "simulation": {
                    "start_time": self.simulation.start_time.isoformat(),
                    "end_time": (
                        self.simulation.end_time.isoformat()
                        if self.simulation.end_time
                        else None
                    ),
                    "duration_seconds": self.simulation.duration_seconds(),
                },
                "agents": {
                    agent_id: {
                        "steps_completed": metrics.steps_completed,
                        "trades_executed": metrics.trades_executed,
                        "llm_calls": metrics.llm_calls,
                        "duration_seconds": metrics.duration_seconds,
                        "start_time": metrics.start_time.isoformat(),
                        "end_time": (
                            metrics.end_time.isoformat()
                            if metrics.end_time
                            else None
                        ),
                    }
                    for agent_id, metrics in self.simulation.agent_metrics.items()
                },
            }

    def _ensure_agent(self, agent_id: str) -> None:
        if agent_id not in self.simulation.agent_metrics:
            self.simulation.agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id)
