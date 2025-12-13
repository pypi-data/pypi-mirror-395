"""
Telemetry helpers for the meta-learning layer.
"""

from __future__ import annotations

import time
from typing import Dict, Optional

from scarcity.runtime import EventBus, get_bus


def build_meta_metrics_snapshot(
    reward: float,
    update_rate: float,
    gain: float,
    confidence: float,
    drift_score: float,
    latency_ms: float,
    storage_mb: float,
    extras: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    snapshot = {
        "meta_reward": float(reward),
        "meta_update_rate": float(update_rate),
        "meta_gain": float(gain),
        "meta_confidence": float(confidence),
        "meta_drift_score": float(drift_score),
        "meta_latency_ms": float(latency_ms),
        "meta_storage_mb": float(storage_mb),
        "timestamp": time.time(),
    }
    if extras:
        snapshot.update({k: float(v) for k, v in extras.items()})
    return snapshot


async def publish_meta_metrics(bus: Optional[EventBus], snapshot: Dict[str, float]) -> None:
    bus = bus or get_bus()
    await bus.publish("meta_metrics", snapshot)

