"""
Online Reptile optimizer for meta learning.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np


@dataclass
class MetaOptimizerConfig:
    beta_init: float = 0.1
    beta_max: float = 0.3
    ema_alpha: float = 0.3
    rollback_delta: float = 0.1
    backup_versions: int = 10


@dataclass
class MetaOptimizerState:
    prior: Dict[str, float] = field(default_factory=dict)
    beta: float = 0.1
    reward_ema: float = 0.0
    history: List[Dict[str, float]] = field(default_factory=list)
    last_reward: float = 0.0


class OnlineReptileOptimizer:
    """
    Maintains a global meta prior using a Reptile-style EMA and supports rollback.
    """

    def __init__(self, config: Optional[MetaOptimizerConfig] = None):
        self.config = config or MetaOptimizerConfig()
        self.state = MetaOptimizerState(beta=self.config.beta_init)

    def apply(
        self,
        aggregated_vector: np.ndarray,
        keys: List[str],
        reward: float,
        drg_profile: Dict[str, float],
    ) -> Dict[str, float]:
        cfg = self.config
        state = self.state

        self._update_beta(drg_profile)

        if not state.prior:
            state.prior = {key: 0.0 for key in keys}

        self._record_history()

        prior_vector = np.array([state.prior.get(key, 0.0) for key in keys], dtype=np.float32)
        updated_vector = prior_vector + state.beta * aggregated_vector

        state.prior = dict(zip(keys, updated_vector.tolist()))
        self._update_reward(reward)

        return dict(state.prior)

    def rollback(self) -> Dict[str, float]:
        if not self.state.history:
            return self.state.prior
        self.state.prior = self.state.history.pop()
        return self.state.prior

    def should_rollback(self, reward: float) -> bool:
        delta = self.state.reward_ema - reward
        return delta > self.config.rollback_delta

    def _update_beta(self, drg_profile: Dict[str, float]) -> None:
        cfg = self.config
        vram_high = drg_profile.get("vram_high", 0.0)
        latency_high = drg_profile.get("latency_high", 0.0)
        bandwidth_free = drg_profile.get("bandwidth_free", 0.0)

        beta = self.state.beta
        if vram_high or latency_high:
            beta *= 0.8
        if bandwidth_free:
            beta *= 1.1
        beta = min(cfg.beta_max, max(cfg.beta_init * 0.5, beta))
        self.state.beta = beta

    def _update_reward(self, reward: float) -> None:
        cfg = self.config
        state = self.state
        state.reward_ema = (1 - cfg.ema_alpha) * state.reward_ema + cfg.ema_alpha * reward
        state.last_reward = reward

    def _record_history(self) -> None:
        cfg = self.config
        state = self.state
        state.history.append(dict(state.prior))
        if len(state.history) > cfg.backup_versions:
            state.history = state.history[-cfg.backup_versions :]

