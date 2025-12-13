"""
Scheduler for meta-learning updates.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class MetaSchedulerConfig:
    update_interval_windows: int = 10
    latency_target_ms: float = 80.0
    jitter: float = 0.1
    min_interval_windows: int = 3
    max_interval_windows: int = 20


class MetaScheduler:
    """
    Maintains cadence for meta updates using window counts and telemetry.
    """

    def __init__(self, config: Optional[MetaSchedulerConfig] = None):
        self.config = config or MetaSchedulerConfig()
        self._window_counter = 0
        self._last_update_ts = 0.0
        self._interval_windows = self.config.update_interval_windows

    def record_window(self) -> None:
        self._window_counter += 1

    def should_update(self, telemetry: Dict[str, float]) -> bool:
        latency = telemetry.get("latency_ms", self.config.latency_target_ms)
        vram_high = telemetry.get("vram_high", 0.0)
        bandwidth_low = telemetry.get("bandwidth_low", 0.0)

        self._adapt_interval(latency, vram_high, bandwidth_low)
        if self._window_counter >= self._interval_windows:
            self._window_counter = 0
            self._last_update_ts = time.time()
            return True
        return False

    def _adapt_interval(self, latency: float, vram_high: float, bandwidth_low: float) -> None:
        cfg = self.config
        interval = self._interval_windows

        if latency > cfg.latency_target_ms or vram_high:
            interval = max(cfg.min_interval_windows, int(max(1, math.floor(interval * 0.7))))
        if bandwidth_low:
            interval = min(cfg.max_interval_windows, interval + 2)
        if latency < cfg.latency_target_ms * 0.7 and not vram_high:
            interval = max(cfg.min_interval_windows, int(round(interval * 0.8)))

        if cfg.jitter > 0.0:
            jitter = random.uniform(-cfg.jitter, cfg.jitter)
            interval = int(round(interval * (1 + jitter)))
        interval = max(cfg.min_interval_windows, min(cfg.max_interval_windows, interval))
        self._interval_windows = interval

