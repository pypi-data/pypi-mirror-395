"""Shared dependencies for SCIC backend."""

from typing import Any, cast

from fastapi import Depends, HTTPException, Request, status

SimulationManager = Any  # type: ignore[misc,assignment]


def get_simulation_manager(request: Request) -> SimulationManager:
    """Resolve the simulation manager from the application state hierarchy."""

    app = request.app
    # Walk up mounted applications if necessary
    while app is not None:
        simulation = getattr(app.state, "simulation", None)
        if simulation is not None:
            return cast(SimulationManager, simulation)
        app = getattr(app.state, "parent_app", None)
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Simulation manager unavailable")


SimulationManagerDep = Depends(get_simulation_manager)

__all__ = ["SimulationManagerDep", "get_simulation_manager"]


