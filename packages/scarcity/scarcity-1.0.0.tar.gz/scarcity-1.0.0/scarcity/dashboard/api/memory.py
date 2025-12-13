"""Global Memory Store endpoints."""

from typing import Any

from fastapi import APIRouter

from ..dependencies import SimulationManagerDep

SimulationManager = Any  # type: ignore[misc,assignment]

router = APIRouter(tags=["memory"])


@router.get("/query", summary="Query causal/semantic memory graph")
async def query_memory(q: str | None = None, simulation: SimulationManager = SimulationManagerDep) -> dict[str, object]:
    """Return placeholder search results from the global memory store."""

    domains = simulation.get_domains()
    results = []
    for domain in domains.domains:
        if q and q.lower() not in domain.name.lower():
            continue
        results.append(
            {
                "domain_id": domain.domain_id,
                "name": domain.name,
                "sector": domain.sector,
                "phase": domain.phase,
                "accuracy": domain.accuracy,
                "compliance": domain.compliance.frameworks,
            }
        )
    return {"query": q, "results": results}


