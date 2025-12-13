"""
Robust aggregation utilities for SCARCITY federation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List, Sequence, Tuple

import numpy as np


class AggregationMethod(str, Enum):
    MEDIAN = "median"
    TRIMMED_MEAN = "trimmed_mean"
    KRUM = "krum"
    MULTI_KRUM = "multi_krum"
    BULYAN = "bulyan"


@dataclass
class AggregationConfig:
    method: AggregationMethod = AggregationMethod.TRIMMED_MEAN
    trim_alpha: float = 0.1
    multi_krum_m: int = 5
    trust_min: float = 0.2


def _stack_updates(updates: Sequence[Sequence[float]]) -> np.ndarray:
    if not updates:
        raise ValueError("No updates supplied")
    array = np.asarray(updates, dtype=np.float32)
    if len({arr.shape for arr in array}) > 1:
        raise ValueError("Updates must share the same shape")
    return array


def _pairwise_distances(array: np.ndarray) -> np.ndarray:
    norms = np.sum(array ** 2, axis=1, keepdims=True)
    distances = norms + norms.T - 2.0 * array @ array.T
    np.maximum(distances, 0.0, out=distances)
    return distances


def _trimmed_mean(array: np.ndarray, alpha: float) -> np.ndarray:
    if array.shape[0] == 1:
        return array[0]

    total = array.shape[0]
    trim_count = int(round(alpha * total))
    if alpha > 0.0 and trim_count == 0:
        trim_count = 1
    trim_count = min(trim_count, total - 2)

    if trim_count <= 0:
        return np.mean(array, axis=0)

    median = np.median(array, axis=0)
    distances = np.linalg.norm(array - median, axis=1)
    keep = np.argsort(distances)[: total - trim_count]
    trimmed = array[keep]
    return np.mean(trimmed, axis=0)


def _krum_select(array: np.ndarray, m: int) -> Tuple[np.ndarray, List[int]]:
    distances = _pairwise_distances(array)
    n = array.shape[0]
    scores = np.zeros(n, dtype=np.float32)
    neighbours = max(1, min(n - 2, n - m - 2))
    for i in range(n):
        sorted_indices = np.argsort(distances[i])
        scores[i] = np.sum(distances[i, sorted_indices[1 : neighbours + 1]])
    selected = np.argsort(scores)[:m]
    return array[selected], selected.tolist()


def _bulyan(array: np.ndarray, m: int, alpha: float) -> np.ndarray:
    if array.shape[0] <= m:
        return np.mean(array, axis=0)
    selected, _ = _krum_select(array, m)
    return _trimmed_mean(selected, alpha)


class FederatedAggregator:
    """Entry-point for federated aggregation with fallback logic."""

    def __init__(self, config: AggregationConfig):
        self.config = config

    def aggregate(self, updates: Sequence[Sequence[float]]) -> Tuple[np.ndarray, dict]:
        array = _stack_updates(updates)
        method = self.config.method
        meta: dict = {"method": method.value, "participants": array.shape[0]}

        if method == AggregationMethod.MEDIAN:
            meta["trim_alpha"] = 0.0
            return np.median(array, axis=0), meta

        if method == AggregationMethod.TRIMMED_MEAN:
            meta["trim_alpha"] = self.config.trim_alpha
            return _trimmed_mean(array, self.config.trim_alpha), meta

        if method == AggregationMethod.KRUM:
            selected, indices = _krum_select(array, 1)
            meta["selected"] = indices
            return selected.mean(axis=0), meta

        if method == AggregationMethod.MULTI_KRUM:
            m = min(self.config.multi_krum_m, array.shape[0])
            selected, indices = _krum_select(array, m)
            meta["selected"] = indices
            return np.mean(selected, axis=0), meta

        if method == AggregationMethod.BULYAN:
            m = min(self.config.multi_krum_m, array.shape[0])
            meta["selected_size"] = m
            meta["trim_alpha"] = self.config.trim_alpha
            return _bulyan(array, m, self.config.trim_alpha), meta

        raise ValueError(f"Unsupported aggregation method: {method}")

    @staticmethod
    def detect_outliers(updates: Sequence[Sequence[float]], reference: Sequence[float], z_thresh: float = 4.0) -> List[int]:
        """Return indices of updates that diverge strongly from the aggregate."""
        array = _stack_updates(updates)
        ref = np.asarray(reference, dtype=np.float32)
        diff_norms = np.linalg.norm(array - ref, axis=1)
        mean = float(np.mean(diff_norms))
        std = float(np.std(diff_norms) + 1e-6)
        z_scores = (diff_norms - mean) / std
        return [i for i, z in enumerate(z_scores) if z > z_thresh]

