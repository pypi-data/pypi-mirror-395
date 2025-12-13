"""Telemetry endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter

from ..dependencies import SimulationManagerDep

SimulationManager = Any  # type: ignore[misc,assignment]

router = APIRouter(tags=["telemetry"])


@router.get("/", summary="Latest telemetry snapshot")
async def get_latest_telemetry(simulation: SimulationManager = SimulationManagerDep) -> dict[str, object]:
    """Return telemetry data sourced from the simulation manager."""

    summary = simulation.get_summary()
    metrics = {
        metric.id: {
            "label": metric.label,
            "value": metric.value,
            "unit": metric.unit,
            "delta": metric.delta,
            "trend": metric.trend,
        }
        for metric in summary.metrics
    }

    return {
        "layer": summary.mode,
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

"""Telemetry endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["telemetry"])


@router.get("/", summary="Latest telemetry snapshot")
async def get_latest_telemetry() -> dict[str, object]:
    """Return placeholder telemetry data."""

    return {
        "layer": "global",
        "metrics": {
            "fps": 0.0,
            "nodes": 0,
            "edges": 0,
            "vram_util": 0.0,
            "cpu_util": 0.0,
            "drift": 0.0,
        },
        "timestamp": None,
    }


