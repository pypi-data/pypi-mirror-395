"""
High-level meta-learning agent orchestrating domain and global updates.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import numpy as np

from scarcity.runtime import EventBus, get_bus
from .domain_meta import DomainMetaLearner, DomainMetaConfig, DomainMetaUpdate
from .cross_meta import CrossDomainMetaAggregator, CrossMetaConfig
from .optimizer import OnlineReptileOptimizer, MetaOptimizerConfig
from .scheduler import MetaScheduler, MetaSchedulerConfig
from .validator import MetaPacketValidator, MetaValidatorConfig
from .storage import MetaStorageManager, MetaStorageConfig
from .telemetry_hooks import build_meta_metrics_snapshot, publish_meta_metrics


@dataclass
class MetaLearningConfig:
    domain: DomainMetaConfig = field(default_factory=DomainMetaConfig)
    cross: CrossMetaConfig = field(default_factory=CrossMetaConfig)
    optimizer: MetaOptimizerConfig = field(default_factory=MetaOptimizerConfig)
    scheduler: MetaSchedulerConfig = field(default_factory=MetaSchedulerConfig)
    validator: MetaValidatorConfig = field(default_factory=MetaValidatorConfig)
    storage: MetaStorageConfig = field(default_factory=MetaStorageConfig)


class MetaLearningAgent:
    """
    Coordinates domain meta updates, aggregation, optimisation, storage, and telemetry.
    """

    def __init__(
        self,
        bus: Optional[EventBus] = None,
        config: Optional[MetaLearningConfig] = None,
    ):
        self.bus = bus or get_bus()
        self.config = config or MetaLearningConfig()

        self.domain_meta = DomainMetaLearner(self.config.domain)
        self.cross_meta = CrossDomainMetaAggregator(self.config.cross)
        self.optimizer = OnlineReptileOptimizer(self.config.optimizer)
        self.scheduler = MetaScheduler(self.config.scheduler)
        self.validator = MetaPacketValidator(self.config.validator)
        self.storage = MetaStorageManager(self.config.storage)

        self._running = False
        self._pending_updates: Dict[str, DomainMetaUpdate] = {}
        self._global_prior = self.storage.load_prior()

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self.bus.subscribe("processing_metrics", self._handle_processing_metrics)
        self.bus.subscribe("federation.policy_pack", self._handle_policy_pack)

    async def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        self.bus.unsubscribe("processing_metrics", self._handle_processing_metrics)
        self.bus.unsubscribe("federation.policy_pack", self._handle_policy_pack)

    async def _handle_policy_pack(self, topic: str, payload: Dict[str, Any]) -> None:
        domain_id = str(payload.get("domain_id", "unknown"))
        metrics = payload.get("metrics", {})
        controller = payload.get("controller", {})
        evaluator = payload.get("evaluator", {})
        params = {**controller, **evaluator}
        update = self.domain_meta.observe(domain_id, metrics, params)
        if self.validator.validate_update(update):
            self._pending_updates[domain_id] = update

    async def _handle_processing_metrics(self, topic: str, metrics: Dict[str, float]) -> None:
        self.scheduler.record_window()
        if not self.scheduler.should_update(metrics):
            return

        if not self._pending_updates:
            return

        aggregated_vector, keys, meta = self.cross_meta.aggregate(list(self._pending_updates.values()))
        self._pending_updates.clear()

        if aggregated_vector.size == 0:
            return

        reward = float(metrics.get("meta_score", metrics.get("gain_p50", 0.0)))
        drg_profile = {
            "vram_high": metrics.get("vram_high", 0.0),
            "latency_high": metrics.get("latency_ms", 0.0) > self.config.scheduler.latency_target_ms,
            "bandwidth_free": metrics.get("bandwidth_free", 0.0),
            "bandwidth_low": metrics.get("bandwidth_low", 0.0),
        }

        prior = self.optimizer.apply(aggregated_vector, keys, reward, drg_profile)

        if self.optimizer.should_rollback(reward):
            prior = self.optimizer.rollback()

        self._global_prior.update(prior)
        self.storage.save_prior(self._global_prior)

        snapshot = build_meta_metrics_snapshot(
            reward=reward,
            update_rate=meta.get("participants", 0) / max(1, self.config.scheduler.update_interval_windows),
            gain=float(np.mean(aggregated_vector)),
            confidence=meta.get("confidence_mean", 0.0),
            drift_score=self.optimizer.state.reward_ema,
            latency_ms=metrics.get("latency_ms", 0.0),
            storage_mb=self._estimate_storage_mb(),
        )
        await publish_meta_metrics(self.bus, snapshot)
        await self.bus.publish("meta_prior_update", {"prior": self._global_prior, "meta": meta})

    def _estimate_storage_mb(self) -> float:
        root = self.config.storage.root
        total_bytes = 0
        if root.exists():
            for path in root.glob("**/*"):
                if path.is_file():
                    total_bytes += path.stat().st_size
        return total_bytes / (1024 * 1024)

