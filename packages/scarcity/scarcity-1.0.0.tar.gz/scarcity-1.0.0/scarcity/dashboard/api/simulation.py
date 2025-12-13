"""Simulation control and introspection endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import numpy as np
from fastapi import APIRouter

from ..dependencies import SimulationManagerDep
from ...simulation.visualization3d import VisualizationConfig, VisualizationEngine

SimulationManager = Any  # type: ignore[misc,assignment]

router = APIRouter(tags=["simulation"])

_visualization_engine = VisualizationEngine(VisualizationConfig())


@router.post("/control", summary="Control simulation execution")
async def control_simulation(action: str, simulation: SimulationManager = SimulationManagerDep) -> dict[str, str]:
    """Stub endpoint to start/pause/resume the simulation manager."""

    return {"status": "accepted", "action": action}


@router.get("/state", summary="Current simulation state snapshot")
async def simulation_state(simulation: SimulationManager = SimulationManagerDep) -> dict[str, object]:
    """Return the latest simulation state derived from domains and events."""

    domains = simulation.get_domains()
    frame = _render_visualization(domains.domains)
    state = {
        "domains": domains.model_dump(),
        "visualization": frame,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    return state


def _render_visualization(domains: list[Any]) -> Dict[str, object]:
    if not domains:
        return {"frame_id": 0, "positions": [], "colors": [], "edges": []}

    count = len(domains)
    angles = np.linspace(0, 2 * np.pi, count, endpoint=False)
    radius = 5.0
    positions = np.stack(
        [
            radius * np.cos(angles),
            radius * np.sin(angles),
            np.zeros_like(angles),
        ],
        axis=1,
    ).astype(np.float32)

    values = np.array([domain.accuracy for domain in domains], dtype=np.float32)
    stability = np.tile(np.linspace(0.2, 0.8, count, dtype=np.float32), (3, 1))
    adjacency = np.zeros((count, count), dtype=np.float32)
    for idx in range(count):
        adjacency[idx, (idx + 1) % count] = 1.0

    frame = _visualization_engine.render_frame(
        positions,
        values,
        adjacency,
        stability,
        lod=0.9,
    )
    return {
        "frame_id": frame["frame_id"],
        "positions": frame["positions"].tolist(),
        "colors": frame["colors"].tolist(),
        "edges": frame["edges"].tolist(),
    }


