"""Pydantic schemas for SCIC backend."""

from datetime import datetime

from pydantic import BaseModel


class TelemetryMetric(BaseModel):
    """Minimal telemetry data contract."""

    layer: str
    metrics: dict[str, float]
    timestamp: datetime | None = None


__all__ = ["TelemetryMetric"]


