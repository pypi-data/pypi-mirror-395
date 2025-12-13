"""
Cross-domain aggregation for meta learning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

from .domain_meta import DomainMetaUpdate


@dataclass
class CrossMetaConfig:
    method: str = "trimmed_mean"
    trim_alpha: float = 0.1
    min_confidence: float = 0.05


class CrossDomainMetaAggregator:
    """
    Combines domain-level meta updates into a global update vector.
    """

    def __init__(self, config: Optional[CrossMetaConfig] = None):
        self.config = config or CrossMetaConfig()

    def aggregate(self, updates: Sequence[DomainMetaUpdate]) -> Tuple[np.ndarray, List[str], Dict[str, float]]:
        cfg = self.config
        filtered = [u for u in updates if u.confidence >= cfg.min_confidence and len(u.vector) > 0]
        if not filtered:
            return np.zeros(0, dtype=np.float32), [], {"participants": 0}

        keys = self._union_keys(filtered)
        matrix = self._stack_vectors(filtered, keys)

        if cfg.method == "median":
            aggregate = np.median(matrix, axis=0)
        else:
            aggregate = self._trimmed_mean(matrix, cfg.trim_alpha)

        meta = {
            "participants": len(filtered),
            "method": cfg.method,
            "trim_alpha": cfg.trim_alpha if cfg.method != "median" else 0.0,
            "confidence_mean": float(np.mean([u.confidence for u in filtered])),
        }
        return aggregate.astype(np.float32), keys, meta

    def _union_keys(self, updates: Sequence[DomainMetaUpdate]) -> List[str]:
        key_set = set()
        for update in updates:
            key_set.update(update.keys)
        return sorted(key_set)

    def _stack_vectors(self, updates: Sequence[DomainMetaUpdate], keys: List[str]) -> np.ndarray:
        key_index = {key: idx for idx, key in enumerate(keys)}
        matrix = np.zeros((len(updates), len(keys)), dtype=np.float32)
        for row, update in enumerate(updates):
            for key, value in zip(update.keys, update.vector):
                matrix[row, key_index[key]] = value
        return matrix

    def _trimmed_mean(self, matrix: np.ndarray, alpha: float) -> np.ndarray:
        if matrix.shape[0] == 1:
            return matrix[0]
        k = int(np.floor(alpha * matrix.shape[0]))
        if k == 0:
            return matrix.mean(axis=0)
        sorted_vals = np.sort(matrix, axis=0)
        trimmed = sorted_vals[k : matrix.shape[0] - k]
        if trimmed.size == 0:
            trimmed = sorted_vals
        return trimmed.mean(axis=0)

