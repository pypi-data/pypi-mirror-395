"""
Packet schemas exchanged by the SCARCITY federated learning layer.

All packets are dataclasses with helper methods for serialisation and validation.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple
import hashlib


def _hash_schema(schema_hash: str, domain_id: int) -> str:
    """Create a composite hash for schema-domain pairing."""
    composite = f"{schema_hash}:{domain_id}".encode("utf-8")
    return hashlib.blake2b(composite, digest_size=12).hexdigest()


@dataclass
class Provenance:
    config_hash: str
    tier_set: Sequence[str]
    encoder_profile: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config_hash": self.config_hash,
            "tier_set": list(self.tier_set),
            "encoder_profile": dict(self.encoder_profile),
        }


@dataclass
class PathPack:
    schema_hash: str
    window_range: Tuple[int, int]
    domain_id: int
    revision: int
    edges: List[Tuple[str, str, float, float, float, int]]
    hyperedges: List[Dict[str, Any]]
    operator_stats: Dict[str, float]
    provenance: Provenance

    def composite_id(self) -> str:
        return _hash_schema(self.schema_hash, self.domain_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_hash": self.schema_hash,
            "window_range": list(self.window_range),
            "domain_id": self.domain_id,
            "revision": self.revision,
            "edges": [list(edge) for edge in self.edges],
            "hyper": self.hyperedges,
            "operator_stats": dict(self.operator_stats),
            "provenance": self.provenance.to_dict(),
        }

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "PathPack":
        provenance = Provenance(**payload["provenance"])
        edges = [tuple(edge) for edge in payload.get("edges", [])]
        return PathPack(
            schema_hash=payload["schema_hash"],
            window_range=tuple(payload["window_range"]),
            domain_id=payload["domain_id"],
            revision=payload["revision"],
            edges=edges,  # type: ignore[arg-type]
            hyperedges=list(payload.get("hyper", [])),
            operator_stats=dict(payload.get("operator_stats", {})),
            provenance=provenance,
        )


@dataclass
class EdgeDelta:
    schema_hash: str
    domain_id: int
    revision: int
    upserts: List[Tuple[str, float, float, int, int, int]]
    prunes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_hash": self.schema_hash,
            "domain_id": self.domain_id,
            "revision": self.revision,
            "upserts": [list(u) for u in self.upserts],
            "prunes": list(self.prunes),
        }

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "EdgeDelta":
        upserts = [tuple(item) for item in payload.get("upserts", [])]
        return EdgeDelta(
            schema_hash=payload["schema_hash"],
            domain_id=payload["domain_id"],
            revision=payload["revision"],
            upserts=upserts,  # type: ignore[arg-type]
            prunes=list(payload.get("prunes", [])),
        )


@dataclass
class PolicyPack:
    controller: Dict[str, float]
    evaluator: Dict[str, float]
    drg: Dict[str, float]
    evidence: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "PolicyPack":
        return PolicyPack(
            controller=dict(payload.get("controller", {})),
            evaluator=dict(payload.get("evaluator", {})),
            drg=dict(payload.get("drg", {})),
            evidence=dict(payload.get("evidence", {})),
        )


@dataclass
class CausalPair:
    source: str
    target: str
    probability: float
    direction: int
    regime: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "src": self.source,
            "dst": self.target,
            "prob": float(self.probability),
            "direction": int(self.direction),
            "regime": self.regime,
        }


@dataclass
class ConceptLink:
    concept_id: str
    score: float
    links: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.concept_id,
            "score": float(self.score),
            "links": list(self.links),
        }


@dataclass
class CausalSemanticPack:
    schema_hash: str
    domain_id: int
    revision: int
    pairs: List[CausalPair]
    concepts: List[ConceptLink]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_hash": self.schema_hash,
            "domain_id": self.domain_id,
            "revision": self.revision,
            "pairs": [pair.to_dict() for pair in self.pairs],
            "concepts": [concept.to_dict() for concept in self.concepts],
        }

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "CausalSemanticPack":
        pairs = [
            CausalPair(
                source=item["src"],
                target=item["dst"],
                probability=item["prob"],
                direction=item.get("direction", 1),
                regime=item.get("regime"),
            )
            for item in payload.get("pairs", [])
        ]
        concepts = [
            ConceptLink(concept_id=item["id"], score=item["score"], links=item.get("links", []))
            for item in payload.get("concepts", [])
        ]
        return CausalSemanticPack(
            schema_hash=payload["schema_hash"],
            domain_id=payload["domain_id"],
            revision=payload["revision"],
            pairs=pairs,
            concepts=concepts,
        )


PacketType = Tuple[str, Dict[str, Any]]


def serialise_packet(packet: Any) -> PacketType:
    """Return typed payload for bus transport."""
    if isinstance(packet, PathPack):
        return ("federation.path_pack", packet.to_dict())
    if isinstance(packet, EdgeDelta):
        return ("federation.edge_delta", packet.to_dict())
    if isinstance(packet, PolicyPack):
        return ("federation.policy_pack", packet.to_dict())
    if isinstance(packet, CausalSemanticPack):
        return ("federation.causal_pack", packet.to_dict())
    raise TypeError(f"Unsupported packet type: {type(packet)}")


def normalise_packets(payloads: Sequence[PacketType]) -> Dict[str, List[Dict[str, Any]]]:
    """Group packets by topic for efficient batching."""
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for topic, payload in payloads:
        grouped.setdefault(topic, []).append(payload)
    return grouped

