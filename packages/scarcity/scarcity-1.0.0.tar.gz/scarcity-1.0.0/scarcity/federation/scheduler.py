"""
Adaptive scheduler for the SCARCITY federation layer.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class SchedulerConfig:
    base_export_interval: float = 10.0
    min_export_interval: float = 2.0
    max_export_interval: float = 120.0
    latency_target_ms: float = 120.0
    high_latency_backoff: float = 1.25
    vram_penalty: float = 1.4
    bandwidth_boost: float = 0.7
    jitter: float = 0.1
    ema_alpha: float = 0.2
    max_payload_kb: int = 256
    min_payload_kb: int = 64


class FederationScheduler:
    """
    Decides when federation exports should happen based on latency and resource metrics.
    """

    def __init__(self, config: SchedulerConfig):
        self.config = config
        self._last_export_ts = 0.0
        self._interval = config.base_export_interval
        self._latency_ema = config.latency_target_ms

    def should_export(self, telemetry: Dict[str, float]) -> bool:
        now = time.time()
        elapsed = now - self._last_export_ts
        self._update_interval(telemetry)
        return elapsed >= self._interval

    def mark_export(self) -> None:
        self._last_export_ts = time.time()

    def max_payload_bytes(self, drg_util: Dict[str, float]) -> int:
        cfg = self.config
        limit_kb = cfg.max_payload_kb

        if drg_util.get("bandwidth_low", 0.0):
            limit_kb = max(cfg.min_payload_kb, int(limit_kb * 0.5))
        elif drg_util.get("bandwidth_free", 0.0):
            limit_kb = int(limit_kb * 1.2)

        if drg_util.get("cpu_util_high", 0.0):
            limit_kb = max(cfg.min_payload_kb, int(limit_kb * 0.7))

        return limit_kb * 1024

    def notify_success(self, payload_bytes: int) -> None:
        cfg = self.config
        fraction = payload_bytes / float(cfg.max_payload_kb * 1024)
        if fraction < 0.3:
            self._interval = max(cfg.min_export_interval, self._interval * 0.9)

    def _update_interval(self, telemetry: Dict[str, float]) -> None:
        cfg = self.config
        latency = telemetry.get("latency_ms", cfg.latency_target_ms)
        bandwidth_free = telemetry.get("bandwidth_free", 0.0)
        bandwidth_low = telemetry.get("bandwidth_low", 0.0)
        vram_high = telemetry.get("vram_high", 0.0)

        self._latency_ema = (1 - cfg.ema_alpha) * self._latency_ema + cfg.ema_alpha * latency

        interval = cfg.base_export_interval
        if self._latency_ema > cfg.latency_target_ms:
            interval *= cfg.high_latency_backoff
        if vram_high:
            interval *= cfg.vram_penalty
        if bandwidth_free:
            interval *= cfg.bandwidth_boost
        if bandwidth_low:
            interval *= 1.2

        jitter = random.uniform(-cfg.jitter, cfg.jitter) * interval
        interval = interval + jitter
        interval = max(cfg.min_export_interval, min(cfg.max_export_interval, interval))

        self._interval = interval