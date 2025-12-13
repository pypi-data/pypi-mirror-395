"""Federation layer endpoints."""

from fastapi import APIRouter

from ..dependencies import SimulationManagerDep
from app.simulation.manager import SimulationManager

router = APIRouter(tags=["federation"])


@router.get("/nodes", summary="List connected federation nodes")
async def list_nodes(simulation: SimulationManager = SimulationManagerDep) -> dict[str, object]:
    """Return federation node information derived from simulation domains."""

    domains = simulation.get_domains()
    nodes = []
    for domain in domains.domains:
        nodes.append(
            {
                "id": domain.domain_id,
                "name": domain.name,
                "sector": domain.sector,
                "phase": domain.phase,
                "accuracy": domain.accuracy,
                "delta": domain.delta,
                "clients": len(domain.clients),
                "compliance": domain.compliance.frameworks,
            }
        )
    return {"nodes": nodes}


