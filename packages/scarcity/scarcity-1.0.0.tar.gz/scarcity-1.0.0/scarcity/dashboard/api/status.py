"""Status endpoints for SCIC."""

from datetime import datetime

from fastapi import APIRouter

from ..dependencies import SimulationManagerDep
from app.simulation.manager import SimulationManager

router = APIRouter(tags=["status"])


@router.get("/", summary="Global system status snapshot")
async def get_status(simulation: SimulationManager = SimulationManagerDep) -> dict[str, object]:
    """Return an aggregate status payload derived from the simulation manager."""

    summary = simulation.get_summary()
    domains = simulation.get_domains()
    risk = simulation.get_risk_status()

    return {
        "layers": {
            "runtime": "online",
            "mpie": "online",
            "simulation": "online",
            "federation": "online",
            "meta": "online",
            "drg": "online",
        },
        "kpis": summary.model_dump(),
        "domains": domains.model_dump(),
        "risk": risk.model_dump(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


