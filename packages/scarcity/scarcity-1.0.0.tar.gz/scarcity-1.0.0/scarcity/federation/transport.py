"""
Abstract transport interfaces for federation networking.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Optional


PacketHandler = Callable[[str, Dict[str, Any]], Awaitable[None]]


@dataclass
class TransportConfig:
    protocol: str = "grpc"
    endpoint: Optional[str] = None
    reconnect_backoff: float = 5.0


class BaseTransport:
    def __init__(self, config: TransportConfig):
        self.config = config
        self._handler: Optional[PacketHandler] = None
        self._running = False

    def register_handler(self, handler: PacketHandler) -> None:
        self._handler = handler

    async def start(self) -> None:
        self._running = True

    async def stop(self) -> None:
        self._running = False

    async def send(self, topic: str, payload: Dict[str, Any]) -> None:
        raise NotImplementedError

    async def _dispatch(self, topic: str, payload: Dict[str, Any]) -> None:
        if self._handler is not None:
            await self._handler(topic, payload)


class LoopbackTransport(BaseTransport):
    """
    In-process transport that simply routes messages back to registered handler.
    Useful for unit tests or single-node development.
    """

    async def send(self, topic: str, payload: Dict[str, Any]) -> None:
        await self._dispatch(topic, payload)


class SimulatedNetworkTransport(BaseTransport):
    """
    Simulates latency and backpressure without external dependencies.
    """

    def __init__(self, config: TransportConfig, latency_ms: float = 20.0):
        super().__init__(config)
        self.latency_ms = latency_ms

    async def send(self, topic: str, payload: Dict[str, Any]) -> None:
        await asyncio.sleep(self.latency_ms / 1000.0)
        await self._dispatch(topic, payload)

