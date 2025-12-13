"""
Trust scoring heuristics for federated participants.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np


@dataclass
class TrustConfig:
    decay: float = 0.98
    min_trust: float = 0.0
    max_trust: float = 1.0
    agreement_weight: float = 0.6
    compliance_weight: float = 0.3
    impact_weight: float = 0.1
    penalty: float = 0.2


class TrustScorer:
    def __init__(self, config: Optional[TrustConfig] = None):
        self.config = config or TrustConfig()
        self._scores: Dict[str, float] = {}

    def update(
        self,
        peer_id: str,
        agreement: float,
        compliance: float,
        impact_delta: float,
        violation: bool = False,
    ) -> float:
        cfg = self.config
        trust = self._scores.get(peer_id, 0.5)

        weighted_score = (
            cfg.agreement_weight * np.clip(agreement, 0.0, 1.0)
            + cfg.compliance_weight * np.clip(compliance, 0.0, 1.0)
            + cfg.impact_weight * np.clip(impact_delta, -1.0, 1.0)
        )

        trust = cfg.decay * trust + (1 - cfg.decay) * weighted_score
        if violation:
            trust = max(cfg.min_trust, trust - cfg.penalty)

        trust = float(np.clip(trust, cfg.min_trust, cfg.max_trust))
        self._scores[peer_id] = trust
        return trust

    def score(self, peer_id: str) -> float:
        return self._scores.get(peer_id, 0.5)

    def sandbox(self, peer_id: str) -> None:
        self._scores[peer_id] = max(self.config.min_trust, 0.1)

    def trusted_peers(self, threshold: float = 0.5) -> Dict[str, float]:
        return {peer: score for peer, score in self._scores.items() if score >= threshold}

