"""
Meta packet validation utilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence

import numpy as np

from .domain_meta import DomainMetaUpdate


@dataclass
class MetaValidatorConfig:
    min_confidence: float = 0.1
    max_keys: int = 32
    max_score_delta: float = 1.0


class MetaPacketValidator:
    def __init__(self, config: Optional[MetaValidatorConfig] = None):
        self.config = config or MetaValidatorConfig()

    def validate_update(self, update: DomainMetaUpdate) -> bool:
        cfg = self.config
        if update.confidence < cfg.min_confidence:
            return False
        if len(update.keys) > cfg.max_keys:
            return False
        if abs(update.score_delta) > cfg.max_score_delta:
            return False
        if not all(np.isfinite(update.vector)):
            return False
        return True

