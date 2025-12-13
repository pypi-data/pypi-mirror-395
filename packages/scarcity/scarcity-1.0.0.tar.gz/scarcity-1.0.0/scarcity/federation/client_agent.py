"""
Federated client agent coordinating local exports and incoming aggregates.
"""

from __future__ import annotations

import asyncio
import contextlib
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Sequence, Tuple

import numpy as np

from scarcity.runtime import EventBus, get_bus
from .aggregator import FederatedAggregator, AggregationConfig
from .packets import (
    PathPack,
    EdgeDelta,
    PolicyPack,
    CausalSemanticPack,
    serialise_packet,
)
from .privacy_guard import PrivacyGuard, PrivacyConfig
from .validator import PacketValidator, ValidatorConfig
from .scheduler import FederationScheduler, SchedulerConfig
from .trust_scorer import TrustScorer, TrustConfig
from .codec import PayloadCodec, CodecConfig
from .reconciler import StoreReconciler
from .transport import BaseTransport, LoopbackTransport, TransportConfig


@dataclass
class ClientAgentConfig:
    aggregation: AggregationConfig = field(default_factory=AggregationConfig)
    privacy: PrivacyConfig = field(default_factory=PrivacyConfig)
    validator: ValidatorConfig = field(default_factory=ValidatorConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    codec: CodecConfig = field(default_factory=CodecConfig)
    transport: TransportConfig = field(default_factory=lambda: TransportConfig(protocol="loopback"))
    trust: TrustConfig = field(default_factory=TrustConfig)


class FederationClientAgent:
    """
    Manages federation duties for a single node.
    """

    def __init__(
        self,
        node_id: str,
        reconciler: StoreReconciler,
        bus: Optional[EventBus] = None,
        config: Optional[ClientAgentConfig] = None,
        transport: Optional[BaseTransport] = None,
    ):
        self.node_id = node_id
        self.reconciler = reconciler
        self.bus = bus or get_bus()
        self.config = config or ClientAgentConfig()

        self.aggregator = FederatedAggregator(self.config.aggregation)
        self.privacy_guard = PrivacyGuard(self.config.privacy)
        self.validator = PacketValidator(self.config.validator)
        self.scheduler = FederationScheduler(self.config.scheduler)
        self.trust = TrustScorer(self.config.trust)
        self.codec = PayloadCodec(self.config.codec)
        self.transport = transport or LoopbackTransport(self.config.transport)
        self.transport.register_handler(self._handle_remote_packet)

        self._lock = asyncio.Lock()
        self._outbound_queue: asyncio.Queue[Tuple[str, Dict[str, Any]]] = asyncio.Queue()
        self._export_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self.bus.subscribe("processing_metrics", self._on_processing_metrics)
        await self.transport.start()
        self._export_task = asyncio.create_task(self._export_loop())

    async def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        self.bus.unsubscribe("processing_metrics", self._on_processing_metrics)
        if self._export_task:
            self._export_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._export_task
        await self.transport.stop()

    async def publish_packets(self, packets: Sequence[Any]) -> None:
        for packet in packets:
            topic, payload = serialise_packet(packet)
            await self._outbound_queue.put((topic, payload))

    async def aggregate_updates(self, updates: Sequence[Sequence[float]]) -> Tuple[np.ndarray, dict]:
        noisy_updates = self.privacy_guard.apply_noise(updates)
        return self.aggregator.aggregate(noisy_updates)

    async def receive_aggregated(self, packet: Dict[str, Any], trust: float) -> Dict[str, int]:
        """Apply validated aggregated packet to the local store."""
        if "edges" in packet:
            pack = PathPack.from_dict(packet)
            if not self.validator.validate_path_pack(pack, trust):
                return {}
            return self.reconciler.merge_path_pack(pack)
        if "upserts" in packet:
            delta = EdgeDelta.from_dict(packet)
            if not self.validator.validate_edge_delta(delta, trust):
                return {}
            return self.reconciler.merge_edge_delta(delta)
        if "pairs" in packet:
            causal = CausalSemanticPack.from_dict(packet)
            if not self.validator.validate_causal_pack(causal, trust):
                return {}
            return self.reconciler.merge_causal_pack(causal)
        return {}

    async def _export_loop(self) -> None:
        try:
            while self._running:
                topic, payload = await self._outbound_queue.get()
                await self.transport.send(topic, payload)
                self.scheduler.mark_export()
        except asyncio.CancelledError:
            pass

    async def _handle_remote_packet(self, topic: str, payload: Dict[str, Any]) -> None:
        trust = self.trust.score(payload.get("peer_id", "unknown"))
        await self.receive_aggregated(payload, trust)

    async def _on_processing_metrics(self, topic: str, metrics: Dict[str, Any]) -> None:
        telemetry = {
            "latency_ms": metrics.get("engine_latency_ms", 0.0),
            "bandwidth_free": metrics.get("bandwidth_free", 0.0),
            "vram_high": metrics.get("vram_high", 0.0),
        }
        if self.scheduler.should_export(telemetry):
            await self._outbound_queue.put(("federation.health", metrics))



