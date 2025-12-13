"""Basket assignment and cohort balancing utilities."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from . import clients, domains
from .state import STATE, STATE_LOCK, Basket, ClientState, generate_id

DEFAULT_CAPACITY = 15
DEFAULT_POLICY = {"target_size": DEFAULT_CAPACITY, "k_random_peers": 3}


def _baskets_for_domain(domain_id: str) -> Iterable[Basket]:
    return (basket for basket in STATE.baskets.values() if basket.domain_id == domain_id)


def _make_label(domain_id: str, existing_count: int) -> str:
    suffix = chr(65 + existing_count) if existing_count < 26 else str(existing_count + 1)
    return f"{domain_id}-{suffix}"


def get_basket(basket_id: str) -> Basket | None:
    with STATE_LOCK:
        return STATE.baskets.get(basket_id)


def list_peers(basket_id: str) -> List[dict]:
    with STATE_LOCK:
        basket = STATE.baskets.get(basket_id)
        if not basket:
            raise ValueError("Basket not found.")
        peers = []
        for client_id in basket.members:
            client = STATE.clients.get(client_id)
            if not client:
                continue
            peers.append(
                {
                    "client_id": client.id,
                    "display_name": client.display_name,
                    "trust": round(client.trust, 2),
                    "last_seen": client.last_seen.isoformat() if client.last_seen else None,
                    "state": client.state.value,
                }
            )
        peers.sort(key=lambda item: item["display_name"].lower())
        return peers


def assign_client(client_id: str) -> Tuple[Basket, List[dict]]:
    """Assign client to a basket, creating a new one if needed."""

    client = clients.get_client(client_id)
    if not client:
        raise ValueError("Client not found.")

    domain = domains.get_domain(client.domain_id)
    if not domain:
        raise ValueError("Domain not found.")

    schema_hash = domain.schema_hash_current
    profile_class = client.profile_class

    with STATE_LOCK:
        # Try to find an existing basket that matches schema/profile and has capacity.
        candidate: Basket | None = None
        for basket in _baskets_for_domain(client.domain_id):
            schema_match = schema_hash is None or basket.schema_hash in (None, schema_hash)
            profile_match = basket.profile_class in (None, profile_class)
            if schema_match and profile_match and len(basket.members) < basket.capacity:
                candidate = basket
                break

        if candidate is None:
            index = sum(1 for _ in _baskets_for_domain(client.domain_id))
            basket_id = generate_id("basket")
            label = _make_label(client.domain_id, index)
            candidate = Basket(
                id=basket_id,
                domain_id=client.domain_id,
                label=label,
                capacity=DEFAULT_CAPACITY,
                policy=dict(DEFAULT_POLICY),
                schema_hash=schema_hash,
                profile_class=profile_class,
            )
            STATE.baskets[candidate.id] = candidate

        if client.id not in candidate.members:
            candidate.members.append(client.id)

        client_record = STATE.clients[client.id]
        client_record.basket_id = candidate.id
        client_record.state = ClientState.ACTIVE

        peers = [
            {
                "client_id": STATE.clients[member].id,
                "display_name": STATE.clients[member].display_name,
                "trust": round(STATE.clients[member].trust, 2),
                "last_seen": STATE.clients[member].last_seen.isoformat()
                if STATE.clients[member].last_seen
                else None,
                "state": STATE.clients[member].state.value,
            }
            for member in candidate.members
        ]

        return candidate, peers


