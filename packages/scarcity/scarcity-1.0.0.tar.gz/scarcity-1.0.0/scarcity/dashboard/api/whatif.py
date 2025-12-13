"""What-if scenario endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter

from ..dependencies import SimulationManagerDep
from app.simulation.manager import SimulationManager

router = APIRouter(tags=["whatif"])


@router.post("/run", summary="Execute a what-if scenario")
async def run_whatif(
    payload: dict[str, Any],
    simulation: SimulationManager = SimulationManagerDep
) -> dict[str, Any]:
    """Execute a what-if scenario via the simulation manager."""

    scenario_id = payload.get("scenario_id", "custom")
    magnitude = float(payload.get("magnitude", 0.5))
    target_domain = payload.get("domain_id")
    horizon = int(payload.get("horizon", 12))
    result = simulation.run_whatif(
        scenario_id=scenario_id,
        magnitude=magnitude,
        domain_id=target_domain,
        horizon=horizon
    )
    result["timestamp"] = datetime.utcnow().isoformat() + "Z"
    return result


