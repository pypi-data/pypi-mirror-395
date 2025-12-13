"""Client registration and lifecycle management."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from . import domains
from .state import (
    STATE,
    STATE_LOCK,
    Client,
    ClientState,
    generate_id,
    hash_api_key,
    issue_api_key,
)


def _ensure_domain(domain_id: str) -> None:
    if not domains.get_domain(domain_id):
        raise ValueError("Domain not found.")


def _now() -> datetime:
    return datetime.utcnow()


def register_client(
    *,
    display_name: str,
    domain_id: str,
    profile_class: str,
    vram_gb: float,
    email: Optional[str] = None,
) -> tuple[Client, str]:
    """Register a new client and issue an API key."""

    _ensure_domain(domain_id)

    client_id = generate_id("client")
    api_key, api_hash = issue_api_key()

    client = Client(
        id=client_id,
        display_name=display_name,
        domain_id=domain_id,
        profile_class=profile_class,
        vram_gb=vram_gb,
        api_key_hash=api_hash,
        email=email,
        state=ClientState.REGISTERED,
        created_at=_now(),
        trust=0.8,
    )

    with STATE_LOCK:
        STATE.clients[client_id] = client
        STATE.api_keys[api_hash] = client_id

    return client, api_key


def get_client(client_id: str) -> Optional[Client]:
    """Return a client by identifier."""

    with STATE_LOCK:
        return STATE.clients.get(client_id)


def list_clients(domain_id: Optional[str] = None) -> list[Client]:
    """List clients, optionally filtering by domain."""

    with STATE_LOCK:
        if domain_id:
            return [client for client in STATE.clients.values() if client.domain_id == domain_id]
        return list(STATE.clients.values())


def authenticate_api_key(api_key: str) -> Client:
    """Return the client associated with an API key."""

    api_hash = hash_api_key(api_key)
    with STATE_LOCK:
        client_id = STATE.api_keys.get(api_hash)
        if not client_id:
            raise ValueError("Invalid API key.")
        client = STATE.clients[client_id]
    return client


def record_heartbeat(client_id: str, metrics: Optional[Dict[str, float]] = None) -> Client:
    """Mark a heartbeat for the given client."""

    del metrics  # currently unused; placeholder for telemetry influence

    with STATE_LOCK:
        client = STATE.clients.get(client_id)
        if not client:
            raise ValueError("Client not found.")
        client.last_seen = _now()
        if client.state == ClientState.REGISTERED:
            client.state = ClientState.SYNCING
        return client


def set_state(client_id: str, state: ClientState) -> Client:
    """Update the lifecycle state for a client."""

    with STATE_LOCK:
        client = STATE.clients.get(client_id)
        if not client:
            raise ValueError("Client not found.")
        client.state = state
        return client


def assign_basket(client_id: str, basket_id: str) -> None:
    """Associate a client with a basket."""

    with STATE_LOCK:
        client = STATE.clients.get(client_id)
        if not client:
            raise ValueError("Client not found.")
        client.basket_id = basket_id


