"""WebSocket channel registration."""

from typing import AsyncIterator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .onboarding import clients, gossip


def _get_simulation(websocket: WebSocket):
    simulation = getattr(websocket.app.state, "simulation", None)
    if simulation is None:
        raise RuntimeError("Simulation manager not available for websocket channel.")
    return simulation


async def _relay(stream: AsyncIterator[dict], websocket: WebSocket) -> None:
    try:
        async for payload in stream:
            await websocket.send_json(payload)
    except WebSocketDisconnect:
        return


def register(app: FastAPI) -> None:
    """Attach websocket endpoints to the FastAPI app."""

    @app.websocket("/ws/telemetry")
    async def telemetry_stream(websocket: WebSocket) -> None:
        simulation = _get_simulation(websocket)
        await websocket.accept()
        await _relay(simulation.metrics_stream("stakeholder"), websocket)

    @app.websocket("/ws/alerts")
    async def alerts_stream(websocket: WebSocket) -> None:
        simulation = _get_simulation(websocket)
        await websocket.accept()
        await _relay(simulation.meta_stream(), websocket)

    @app.websocket("/ws/gossip")
    async def gossip_router(websocket: WebSocket, client_id: str, basket_id: str, api_key: str) -> None:
        try:
            client = clients.authenticate_api_key(api_key)
        except ValueError:
            await websocket.close(code=4403)
            return
        if client.id != client_id:
            await websocket.close(code=4403)
            return
        await gossip.register_connection(client_id, basket_id, websocket)


