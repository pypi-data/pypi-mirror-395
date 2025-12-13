"""Dynamic Resource Governor endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter

from ..dependencies import SimulationManagerDep

SimulationManager = Any  # type: ignore[misc,assignment]

router = APIRouter(tags=["drg"])


@router.get("/signals", summary="Return recent DRG signals")
async def recent_signals(simulation: SimulationManager = SimulationManagerDep) -> dict[str, object]:
    """Return synthetic DRG signal data derived from KPI volatility."""

    summary = simulation.get_summary()
    signals = []
    for metric in summary.metrics:
        if metric.delta > 0.5:
            signals.append({"type": "util_low", "metric": metric.id, "value": metric.delta})
        elif metric.delta < -0.5:
            signals.append({"type": "vram_high", "metric": metric.id, "value": metric.delta})
    return {
        "signals": signals,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


