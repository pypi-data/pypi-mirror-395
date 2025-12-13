"""
Simulation engine orchestrator.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from scarcity.runtime import EventBus, get_bus

from .agents import AgentRegistry
from .environment import EnvironmentConfig, SimulationEnvironment
from .dynamics import DynamicsConfig, DynamicsEngine
from .scheduler import SimulationScheduler, SimulationSchedulerConfig
from .monitor import SimulationMonitor, MonitorConfig
from .whatif import WhatIfConfig, WhatIfManager
from .visualization3d import VisualizationConfig, VisualizationEngine
from .storage import SimulationStorage, SimulationStorageConfig

import contextlib
import numpy as np  # type: ignore


@dataclass
class SimulationConfig:
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    dynamics: DynamicsConfig = field(default_factory=DynamicsConfig)
    scheduler: SimulationSchedulerConfig = field(default_factory=SimulationSchedulerConfig)
    monitor: MonitorConfig = field(default_factory=MonitorConfig)
    whatif: WhatIfConfig = field(default_factory=WhatIfConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    storage: SimulationStorageConfig = field(default_factory=SimulationStorageConfig)


class SimulationEngine:
    """
    Integrates the simulation loop with SCARCITY runtime.
    """

    def __init__(
        self,
        registry: AgentRegistry,
        config: SimulationConfig,
        bus: Optional[EventBus] = None,
    ):
        self.registry = registry
        self.config = config
        self.bus = bus or get_bus()

        self.environment = SimulationEnvironment(registry, config.environment)
        self.dynamics = DynamicsEngine(self.environment, config.dynamics)
        self.scheduler = SimulationScheduler(config.scheduler)
        self.monitor = SimulationMonitor(config.monitor)
        self.visualization = VisualizationEngine(config.visualization)
        self.storage = SimulationStorage(config.storage)
        self.whatif = WhatIfManager(self.environment, config.dynamics, config.whatif)

        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._lod = 1.0
        self._last_frame: Dict[str, Any] = {}

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self.bus.subscribe("engine.insight", self._handle_insight)  # type: ignore[arg-type]
        self.bus.subscribe("telemetry", self._handle_telemetry)  # type: ignore[arg-type]
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
        self.bus.unsubscribe("engine.insight", self._handle_insight)  # type: ignore[arg-type]
        self.bus.unsubscribe("telemetry", self._handle_telemetry)  # type: ignore[arg-type]

    async def _run_loop(self) -> None:
        try:
            while self._running:
                if not self.scheduler.should_step():
                    await asyncio.sleep(0.001)
                    continue
                state_snapshot = self.dynamics.step()
                telemetry = self.monitor.tick()
                await self.bus.publish("simulation.state", {"state": state_snapshot})
                await self.bus.publish("simulation.telemetry", telemetry)
                self._maybe_render_frame(state_snapshot)
                self.scheduler.mark_step()
        except asyncio.CancelledError:  # pragma: no cover - shutdown path
            pass

    def run_whatif(
        self,
        scenario_id: str,
        node_shocks: Optional[Dict[str, float]] = None,
        edge_shocks: Optional[Dict[tuple, float]] = None,
        horizon: Optional[int] = None,
    ) -> Dict[str, Any]:
        result = self.whatif.run_scenario(scenario_id, node_shocks, edge_shocks, horizon)
        self.storage.save_whatif(result)
        asyncio.create_task(self.bus.publish("whatif.result", result))
        return result

    async def _handle_insight(self, topic: str, payload: Dict[str, Any]) -> None:
        edges = payload.get("edges", [])
        self.registry.update_edges(edges)
        adjacency, stability, node_ids = self.registry.adjacency_matrix()
        state = self.environment.state()
        state.adjacency = adjacency
        state.stability = stability
        state.node_ids = node_ids

    async def _handle_telemetry(self, topic: str, payload: Dict[str, Any]) -> None:
        self.scheduler.adapt(payload)
        if payload.get("vram_high", 0.0):
            self._lod = max(0.5, self._lod * 0.8)
        elif payload.get("util_low", 0.0):
            self._lod = min(1.0, self._lod * 1.1)

    def _maybe_render_frame(self, state_snapshot: Dict[str, float]) -> None:
        node_positions = self.registry.node_embeddings()
        node_values = np.array(list(state_snapshot.values()), dtype=np.float32)
        adjacency = self.environment.state().adjacency
        stability = self.environment.state().stability
        frame = self.visualization.render_frame(node_positions, node_values, adjacency, stability, lod=self._lod)
        self._last_frame = {
            "positions": node_positions,
            "values": node_values,
            "adjacency": adjacency,
            "stability": stability,
            "frame_id": frame["frame_id"],
        }
        asyncio.create_task(self.bus.publish("simulation.frame", frame))

    def visualizer_snapshot(self) -> Dict[str, Any]:
        if not self._last_frame:
            node_positions = self.registry.node_embeddings()
            state = self.environment.state()
            values = np.zeros(len(node_positions), dtype=np.float32)
            self._last_frame = {
                "positions": node_positions,
                "values": values,
                "adjacency": state.adjacency,
                "stability": state.stability,
                "frame_id": 0,
            }
        return self._last_frame

