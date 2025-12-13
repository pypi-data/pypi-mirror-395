"""Shared state and data structures for onboarding services."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import secrets
from threading import Lock
from typing import Any, Dict, List, Optional


class ClientState(str, Enum):
    """Lifecycle states for registered clients."""

    NEW = "NEW"
    REGISTERED = "REGISTERED"
    SYNCING = "SYNCING"
    ACTIVE = "ACTIVE"
    QUARANTINED = "QUARANTINED"


@dataclass(slots=True)
class Domain:
    """Domain metadata."""

    id: str
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    schema_hash_current: Optional[str] = None


@dataclass(slots=True)
class Client:
    """Client registration details."""

    id: str
    display_name: str
    domain_id: str
    profile_class: str
    vram_gb: float
    api_key_hash: str
    email: Optional[str] = None
    state: ClientState = ClientState.REGISTERED
    trust: float = 0.75
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_seen: Optional[datetime] = None
    basket_id: Optional[str] = None


@dataclass(slots=True)
class UploadColumn:
    """Column inference for uploaded CSV data."""

    name: str
    suggested_dtype: str
    role: str
    null_pct: float


@dataclass(slots=True)
class UploadRecord:
    """Tracked upload metadata."""

    id: str
    client_id: str
    domain_id: str
    filename: str
    path: str
    rows: int
    columns: List[UploadColumn]
    schema_hash: str
    status: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    errors: List[str] = field(default_factory=list)


@dataclass(slots=True)
class Basket:
    """Basket (cohort) grouping clients together."""

    id: str
    domain_id: str
    label: str
    capacity: int
    policy: Dict[str, Any]
    schema_hash: Optional[str] = None
    profile_class: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    members: List[str] = field(default_factory=list)


@dataclass(slots=True)
class GossipMessage:
    """Stored gossip message for audit/debug."""

    basket_id: str
    from_client: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class OnboardingState:
    """Container for in-memory onboarding state."""

    domains: Dict[str, Domain] = field(default_factory=dict)
    clients: Dict[str, Client] = field(default_factory=dict)
    uploads: Dict[str, UploadRecord] = field(default_factory=dict)
    baskets: Dict[str, Basket] = field(default_factory=dict)
    api_keys: Dict[str, str] = field(default_factory=dict)
    gossip_history: List[GossipMessage] = field(default_factory=list)


STATE = OnboardingState()
STATE_LOCK = Lock()


def generate_id(prefix: str) -> str:
    """Return a short unique identifier with the given prefix."""

    token = secrets.token_hex(6)
    return f"{prefix}_{token}"


def hash_api_key(value: str) -> str:
    """Hash an API key for storage."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def issue_api_key() -> tuple[str, str]:
    """Generate a new API key and return plaintext plus hash."""

    plain = secrets.token_urlsafe(24)
    return plain, hash_api_key(plain)


