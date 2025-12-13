"""Meta layer endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter

from ..dependencies import SimulationManagerDep

SimulationManager = Any  # type: ignore[misc,assignment]

router = APIRouter(tags=["meta"])


@router.get("/priors", summary="Retrieve latest global priors")
async def list_priors(simulation: SimulationManager = SimulationManagerDep) -> dict[str, object]:
    """Return the current meta prior payload."""

    scarcity = simulation._meta_scarcity  # noqa: SLF001 - accessing simulation state
    curve_levels = [0.1, 0.3, 0.5, 0.7, scarcity, 1.0]
    curve = [
        {"scarcity": round(level, 2), "meta_accuracy": round(0.65 + level * 0.3, 3)}
        for level in curve_levels
    ]
    return {
        "revision": int(scarcity * 100),
        "scarcity_level": round(scarcity, 2),
        "curve": curve,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.post("/deploy", summary="Deploy a new meta prior revision")
async def deploy_prior(revision: int) -> dict[str, object]:
    """Accept a request to deploy a new global prior."""

    return {"status": "accepted", "revision": revision}


