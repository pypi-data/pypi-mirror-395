"""
Packet validation and policy enforcement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

from .packets import PathPack, EdgeDelta, PolicyPack, CausalSemanticPack


@dataclass
class ValidatorConfig:
    trust_min: float = 0.2
    allow_policy_share: bool = True
    max_edges: int = 2048
    max_concepts: int = 256


class PacketValidator:
    def __init__(self, config: ValidatorConfig):
        self.config = config

    def validate_path_pack(self, pack: PathPack, trust: float) -> bool:
        if trust < self.config.trust_min:
            return False
        if len(pack.edges) > self.config.max_edges:
            return False
        if not pack.operator_stats:
            return False
        return True

    def validate_edge_delta(self, delta: EdgeDelta, trust: float) -> bool:
        if trust < self.config.trust_min:
            return False
        if len(delta.upserts) + len(delta.prunes) > self.config.max_edges:
            return False
        return True

    def validate_policy_pack(self, pack: PolicyPack, trust: float) -> bool:
        if not self.config.allow_policy_share:
            return False
        if trust < self.config.trust_min:
            return False
        return True

    def validate_causal_pack(self, pack: CausalSemanticPack, trust: float) -> bool:
        if trust < self.config.trust_min:
            return False
        if len(pack.concepts) > self.config.max_concepts:
            return False
        return True

