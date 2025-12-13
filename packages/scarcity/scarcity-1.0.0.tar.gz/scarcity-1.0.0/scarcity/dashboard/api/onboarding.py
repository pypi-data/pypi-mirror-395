"""FastAPI router exposing onboarding flows."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from pydantic import BaseModel, Field

from ..onboarding import baskets, clients, domains, gossip, ingestion

router = APIRouter(tags=["onboarding"])


# --------------------------------------------------------------------------- #
# Pydantic models


class DomainModel(BaseModel):
    id: str
    name: str
    description: str
    schema_hash_current: str | None = None
    created_at: datetime


class DomainListResponse(BaseModel):
    domains: List[DomainModel]
    selected_domain: DomainModel | None = None


class DomainCreateRequest(BaseModel):
    name: str
    description: str | None = None


class ClientRegistrationRequest(BaseModel):
    display_name: str
    domain_id: str
    profile_class: str = Field(default="cpu")
    vram_gb: float = Field(default=0.0, ge=0.0)
    email: str | None = None


class ClientRegistrationResponse(BaseModel):
    client_id: str
    api_key: str | None
    state: str
    domain_id: str


class HeartbeatRequest(BaseModel):
    metrics: Dict[str, float] | None = None


class UploadResponse(BaseModel):
    upload_id: str
    rows: int
    schema_hash: str
    columns: List[Dict[str, Any]]


class UploadCommitRequest(BaseModel):
    upload_id: str
    mapping: List[Dict[str, str]]


class BasketAssignRequest(BaseModel):
    client_id: str


class BasketAssignmentResponse(BaseModel):
    basket_id: str
    label: str
    capacity: int
    policy: Dict[str, Any]
    peers: List[Dict[str, Any]]


class GossipRelayRequest(BaseModel):
    basket_id: str
    payload: Dict[str, Any]


def _to_domain_model(domain_obj) -> DomainModel:
    return DomainModel.model_validate(domain_obj)


def _require_api_client(api_key: str | None) -> clients.Client:
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key.")
    try:
        return clients.authenticate_api_key(api_key)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


# --------------------------------------------------------------------------- #
# Domain management


@router.get("/domains", response_model=DomainListResponse)
def list_domains(domain_id: str | None = None) -> DomainListResponse:
    domain_objects = domains.list_domains(domain_id=domain_id)
    domains_payload = [_to_domain_model(domain) for domain in domain_objects]
    selected = domains_payload[0] if domain_id and domains_payload else None
    return DomainListResponse(domains=domains_payload, selected_domain=selected)


@router.post("/domains", response_model=DomainModel, status_code=201)
def create_domain(payload: DomainCreateRequest) -> DomainModel:
    try:
        domain = domains.create_domain(payload.name, payload.description)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _to_domain_model(domain)


@router.get("/domains/{domain_id}", response_model=DomainModel)
def get_domain(domain_id: str) -> DomainModel:
    domain = domains.get_domain(domain_id)
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found.")
    return _to_domain_model(domain)


# --------------------------------------------------------------------------- #
# Client registration


@router.post("/clients/register", response_model=ClientRegistrationResponse, status_code=201)
def register_client(payload: ClientRegistrationRequest) -> ClientRegistrationResponse:
    try:
        client, api_key = clients.register_client(
            display_name=payload.display_name,
            domain_id=payload.domain_id,
            profile_class=payload.profile_class,
            vram_gb=payload.vram_gb,
            email=payload.email,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ClientRegistrationResponse(
        client_id=client.id,
        api_key=api_key,
        state=client.state.value,
        domain_id=client.domain_id,
    )


@router.post("/clients/heartbeat", response_model=Dict[str, Any])
def heartbeat(
    payload: HeartbeatRequest,
    api_key: str | None = Header(default=None, alias="X-Client-Key"),
) -> Dict[str, Any]:
    client = _require_api_client(api_key)
    updated = clients.record_heartbeat(client.id, payload.metrics)
    return {
        "client_id": updated.id,
        "state": updated.state.value,
        "last_seen": updated.last_seen.isoformat() + "Z" if updated.last_seen else None,
    }


@router.get("/clients", response_model=List[ClientRegistrationResponse])
def list_clients(domain_id: str | None = None) -> List[ClientRegistrationResponse]:
    client_objects = clients.list_clients(domain_id=domain_id)
    return [
        ClientRegistrationResponse(client_id=client.id, api_key=None, state=client.state.value, domain_id=client.domain_id)
        for client in client_objects
    ]


# --------------------------------------------------------------------------- #
# Ingestion


@router.post("/ingestion/upload", response_model=UploadResponse, status_code=201)
async def upload_csv(
    domain_id: str,
    file: UploadFile = File(...),
    api_key: str | None = Header(default=None, alias="X-Client-Key"),
) -> UploadResponse:
    client = _require_api_client(api_key)
    try:
        record = ingestion.create_upload(client.id, domain_id, file.filename, file.file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    columns_payload = [asdict(column) for column in record.columns]
    return UploadResponse(upload_id=record.id, rows=record.rows, schema_hash=record.schema_hash, columns=columns_payload)


@router.get("/ingestion/schema/{upload_id}", response_model=UploadResponse)
def preview_schema(upload_id: str) -> UploadResponse:
    try:
        record = ingestion.preview_schema(upload_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    columns_payload = [asdict(column) for column in record.columns]
    return UploadResponse(upload_id=record.id, rows=record.rows, schema_hash=record.schema_hash, columns=columns_payload)


@router.post("/ingestion/commit", response_model=UploadResponse)
def commit_upload(payload: UploadCommitRequest) -> UploadResponse:
    try:
        record = ingestion.commit_upload(payload.upload_id, payload.mapping)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    columns_payload = [asdict(column) for column in record.columns]
    return UploadResponse(upload_id=record.id, rows=record.rows, schema_hash=record.schema_hash, columns=columns_payload)


# --------------------------------------------------------------------------- #
# Baskets


@router.post("/baskets/assign", response_model=BasketAssignmentResponse)
def assign_basket(
    payload: BasketAssignRequest,
    api_key: str | None = Header(default=None, alias="X-Client-Key"),
) -> BasketAssignmentResponse:
    client = _require_api_client(api_key)
    if client.id != payload.client_id:
        raise HTTPException(status_code=403, detail="Client mismatch.")
    try:
        basket_obj, peers = baskets.assign_client(payload.client_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return BasketAssignmentResponse(
        basket_id=basket_obj.id,
        label=basket_obj.label,
        capacity=basket_obj.capacity,
        policy=basket_obj.policy,
        peers=peers,
    )


@router.get("/baskets/{basket_id}/peers", response_model=List[Dict[str, Any]])
def basket_peers(basket_id: str) -> List[Dict[str, Any]]:
    try:
        return baskets.list_peers(basket_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# --------------------------------------------------------------------------- #
# Gossip


@router.post("/gossip/send", response_model=Dict[str, Any])
async def send_gossip(
    payload: GossipRelayRequest,
    api_key: str | None = Header(default=None, alias="X-Client-Key"),
) -> Dict[str, Any]:
    client = _require_api_client(api_key)
    if client.basket_id != payload.basket_id:
        raise HTTPException(status_code=403, detail="Client not part of basket.")
    await gossip.relay_message(payload.basket_id, client.id, payload.payload)
    return {"status": "ok"}


@router.get("/gossip/history", response_model=List[Dict[str, Any]])
def gossip_history(limit: int = 50) -> List[Dict[str, Any]]:
    return gossip.gossip_history(limit=limit)


