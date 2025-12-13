"""FastAPI entrypoint for the SCIC (Scarcity Control & Intelligence Console)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterator

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import auth, registry, sockets
from .api import (
    drg,
    federation,
    meta,
    memory,
    models as model_api,
    mpie,
    onboarding,
    simulation,
    status,
    telemetry,
    whatif,
)

SimulationManager = Any  # type: ignore[misc,assignment]



def _iter_routers() -> Iterator[tuple[str, FastAPI]]:
    """Yield router + prefix pairs to mount on the API app."""

    yield "/status", status.router
    yield "/telemetry", telemetry.router
    yield "/simulation", simulation.router
    yield "/simulation/whatif", whatif.router
    yield "/mpie", mpie.router
    yield "/federation", federation.router
    yield "/meta", meta.router
    yield "/memory", memory.router
    yield "/drg", drg.router
    yield "/model", model_api.router
    yield "/onboarding", onboarding.router


def create_app() -> FastAPI:
    """Create a configured FastAPI application."""

    app = FastAPI(
        title="SCARCITY Control & Intelligence Console",
        version="1.0.0",
        description="Unified control surface for Scarcity adaptive intelligence stack.",
    )

    settings = _get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

    api_app = FastAPI(title="SCIC API", docs_url=None, redoc_url=None)
    for prefix, router in _iter_routers():
        api_app.include_router(router, prefix=prefix)
    app.mount("/api", api_app)

    # Track relationships for dependency resolution.
    app.state.parent_app = None
    app.state.api_app = api_app
    api_app.state.parent_app = app  # type: ignore[attr-defined]

    sockets.register(app)
    registry.init_registry(Path(settings.model_path))

    @app.get("/health", tags=["system"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


def attach_simulation_manager(app: FastAPI, simulation: SimulationManager) -> None:
    """Attach a simulation manager instance to the SCIC app and its mounted API."""

    app.state.simulation = simulation
    api_app = getattr(app.state, "api_app", None)
    if api_app is not None:
        api_app.state.simulation = simulation  # type: ignore[attr-defined]


class DashboardSettings:
    """Configuration values used by the SCIC backend."""

    def __init__(self, *, allowed_origins: list[str], model_path: str) -> None:
        self.allowed_origins = allowed_origins
        self.model_path = model_path


@lru_cache
def _get_settings() -> DashboardSettings:
    # TODO: load from config/dashboard.yaml; for now use defaults.
    return DashboardSettings(
        allowed_origins=["http://localhost:3000", "https://localhost:3000"],
        model_path="artifacts/meta",
    )


app = create_app()

__all__ = ["create_app", "attach_simulation_manager", "app"]


