"""
Privacy and secure aggregation utilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple
import secrets
import numpy as np


@dataclass
class PrivacyConfig:
    secure_aggregation: bool = True
    dp_noise_sigma: float = 0.0
    seed_length: int = 16


class PrivacyGuard:
    """
    Applies differential privacy noise and simple secure aggregation masking.

    Secure aggregation is approximated by generating common masks that can be
    cancelled by the aggregator; a production deployment should integrate with
    a full SA protocol.
    """

    def __init__(self, config: PrivacyConfig):
        self.config = config

    def apply_noise(self, values: Sequence[Sequence[float]]) -> np.ndarray:
        array = np.asarray(values, dtype=np.float32)
        if self.config.dp_noise_sigma <= 0:
            return array
        noise = np.random.normal(0.0, self.config.dp_noise_sigma, size=array.shape)
        return array + noise.astype(np.float32)

    def secure_mask(self, array: np.ndarray) -> Tuple[np.ndarray, bytes]:
        if not self.config.secure_aggregation:
            return array, b""
        mask_seed = secrets.token_bytes(self.config.seed_length)
        rng = np.random.default_rng(int.from_bytes(mask_seed, "big", signed=False))
        mask = rng.normal(0.0, 1.0, size=array.shape).astype(np.float32)
        return array + mask, mask_seed

    def unmask(self, masked_sum: np.ndarray, seeds: Iterable[bytes], count: int) -> np.ndarray:
        """Remove the combined mask using provided seeds."""
        if not self.config.secure_aggregation or count == 0:
            return masked_sum
        combined_mask = np.zeros_like(masked_sum, dtype=np.float32)
        for seed in seeds:
            rng = np.random.default_rng(int.from_bytes(seed, "big", signed=False))
            combined_mask += rng.normal(0.0, 1.0, size=masked_sum.shape).astype(np.float32)
        return masked_sum - combined_mask

