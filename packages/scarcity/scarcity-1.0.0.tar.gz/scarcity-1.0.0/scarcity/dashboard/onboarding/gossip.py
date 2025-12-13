"""Gossip and peer-to-peer coordination helpers."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict, List

from fastapi import WebSocket, WebSocketDisconnect

from . import baskets, clients
from .state import STATE, STATE_LOCK, GossipMessage

Connection = WebSocket

_connections: Dict[str, List[tuple[str, Connection]]] = {}
_connections_lock = asyncio.Lock()


def _store_history(basket_id: str, from_client: str, payload: Dict[str, Any]) -> None:
    with STATE_LOCK:
        STATE.gossip_history.append(GossipMessage(basket_id=basket_id, from_client=from_client, payload=payload))


async def _broadcast_peers(
    basket_id: str,
    *,
    event: str,
    source_client: str | None = None,
    exclude: set[str] | None = None,
) -> None:
    try:
        peers_snapshot = baskets.list_peers(basket_id)
    except ValueError:
        return

    payload = {
        "type": "peers",
        "basket_id": basket_id,
        "event": event,
        "source_client": source_client,
        "peers": peers_snapshot,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    async with _connections_lock:
        targets = list(_connections.get(basket_id, []))

    for peer_id, connection in targets:
        if exclude and peer_id in exclude:
            continue
        try:
            await connection.send_json(payload)
        except Exception:
            continue


async def register_connection(client_id: str, basket_id: str, websocket: WebSocket) -> None:
    """Register a WebSocket connection for gossip messages."""

    client = clients.get_client(client_id)
    if not client:
        await websocket.close(code=4403)
        return

    if client.basket_id != basket_id:
        await websocket.close(code=4403)
        return

    await websocket.accept()

    async with _connections_lock:
        bucket = _connections.setdefault(basket_id, [])
        bucket.append((client_id, websocket))

    await websocket.send_json(
        {
            "type": "joined",
            "client_id": client_id,
            "basket_id": basket_id,
            "peers": baskets.list_peers(basket_id),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )

    await _broadcast_peers(basket_id, event="peer_joined", source_client=client_id, exclude={client_id})

    try:
        while True:
            message = await websocket.receive_json()
            await relay_message(basket_id, client_id, message)
    except WebSocketDisconnect:
        pass
    finally:
        async with _connections_lock:
            peers = _connections.get(basket_id, [])
            _connections[basket_id] = [item for item in peers if item[1] is not websocket]
            if _connections.get(basket_id):
                pass
            else:
                _connections.pop(basket_id, None)
        await _broadcast_peers(basket_id, event="peer_left", source_client=client_id, exclude={client_id})


async def relay_message(basket_id: str, from_client: str, payload: Dict[str, Any]) -> None:
    """Relay gossip payload to peers in the same basket."""

    _store_history(basket_id, from_client, payload)

    async with _connections_lock:
        peers = list(_connections.get(basket_id, []))

    message = {
        "type": "gossip",
        "basket_id": basket_id,
        "from_client": from_client,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    for peer_id, connection in peers:
        if peer_id == from_client:
            continue
        try:
            await connection.send_json(message)
        except Exception:  # pragma: no cover - defensive cleanup
            continue


def peers_for_basket(basket_id: str) -> List[dict]:
    """Return peer metadata for a basket."""

    return baskets.list_peers(basket_id)


def gossip_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Return recent gossip messages for diagnostics."""

    with STATE_LOCK:
        recent = STATE.gossip_history[-limit:]
        return [
            {
                "basket_id": item.basket_id,
                "from_client": item.from_client,
                "payload": item.payload,
                "timestamp": item.timestamp.isoformat() + "Z",
            }
            for item in recent
        ]


