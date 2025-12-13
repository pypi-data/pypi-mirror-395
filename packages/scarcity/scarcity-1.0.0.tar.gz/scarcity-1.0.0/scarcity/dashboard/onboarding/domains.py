"""Domain management services."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .state import STATE, STATE_LOCK, Domain, generate_id

CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "domains.json"


def _load_config_domains() -> None:
    """Load domain definitions from configuration file."""

    if not CONFIG_PATH.exists():
        return

    try:
        payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return

    if not isinstance(payload, list):
        return

    with STATE_LOCK:
        for entry in payload:
            if not isinstance(entry, dict):
                continue
            domain_id = entry.get("id") or generate_id("domain")
            if domain_id in STATE.domains:
                continue
            created_raw = entry.get("created_at")
            if isinstance(created_raw, str) and created_raw.endswith("Z"):
                created_raw = created_raw.replace("Z", "+00:00")
            try:
                created_at = datetime.fromisoformat(created_raw) if created_raw else datetime.utcnow()
            except ValueError:
                created_at = datetime.utcnow()
            domain = Domain(
                id=domain_id,
                name=str(entry.get("name", "")).strip(),
                description=str(entry.get("description", "")).strip(),
                created_at=created_at,
            )
            schema_hash = entry.get("schema_hash_current") or entry.get("schema_hash")
            if isinstance(schema_hash, str) and schema_hash:
                domain.schema_hash_current = schema_hash
            STATE.domains[domain_id] = domain


def _persist_config() -> None:
    """Persist current domain state to configuration file."""

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STATE_LOCK:
        data = [
            {
                "id": domain.id,
                "name": domain.name,
                "description": domain.description,
                "created_at": domain.created_at.isoformat(),
                "schema_hash_current": domain.schema_hash_current,
            }
            for domain in STATE.domains.values()
        ]
    CONFIG_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


_load_config_domains()


def list_domains(domain_id: Optional[str] = None) -> list[Domain]:
    """Return domains, optionally filtering for a specific id."""

    with STATE_LOCK:
        if domain_id:
            domain = STATE.domains.get(domain_id)
            return [domain] if domain else []
        return list(STATE.domains.values())


def create_domain(name: str, description: str | None = None) -> Domain:
    """Create and store a new domain definition."""

    with STATE_LOCK:
        # Ensure case-insensitive uniqueness on name.
        for existing in STATE.domains.values():
            if existing.name.lower() == name.lower():
                raise ValueError("Domain name already exists.")

        domain_id = generate_id("domain")
        domain = Domain(
            id=domain_id,
            name=name,
            description=description or "",
            created_at=datetime.utcnow(),
        )
        STATE.domains[domain_id] = domain
    _persist_config()
    return domain


def get_domain(domain_id: str) -> Domain | None:
    """Return domain by id."""

    with STATE_LOCK:
        return STATE.domains.get(domain_id)


def update_schema(domain_id: str, schema_hash: str) -> Domain:
    """Update the stored schema hash for a domain."""

    with STATE_LOCK:
        domain = STATE.domains.get(domain_id)
        if domain is None:
            raise ValueError("Domain not found.")
        if domain.schema_hash_current and domain.schema_hash_current != schema_hash:
            raise ValueError("Schema hash mismatch for domain.")
        domain.schema_hash_current = schema_hash
    _persist_config()
    return domain



