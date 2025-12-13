"""
Simulation engine layer for SCARCITY.
"""

from .engine import SimulationEngine, SimulationConfig
from .environment import SimulationEnvironment, EnvironmentConfig
from .agents import AgentRegistry
from .dynamics import DynamicsEngine, DynamicsConfig
from .whatif import WhatIfManager, WhatIfConfig
# Visualization module is optional; import lazily to avoid heavy graphics deps.
try:
    from .visualization3d import VisualizationEngine, VisualizationConfig
    _visualization_available = True
except ImportError:  # pragma: no cover - optional dependency
    VisualizationEngine = None  # type: ignore
    VisualizationConfig = None  # type: ignore
    _visualization_available = False
from .monitor import SimulationMonitor, MonitorConfig
from .scheduler import SimulationScheduler, SimulationSchedulerConfig
from .storage import SimulationStorage, SimulationStorageConfig

__all__ = [
"SimulationEngine",
"SimulationConfig",
"SimulationEnvironment",
    "EnvironmentConfig",
    "AgentRegistry",
    "DynamicsEngine",
    "DynamicsConfig",
    "WhatIfManager",
    "WhatIfConfig",
"VisualizationEngine",
"VisualizationConfig",
    "SimulationMonitor",
    "MonitorConfig",
    "SimulationScheduler",
    "SimulationSchedulerConfig",
    "SimulationStorage",
    "SimulationStorageConfig",
]

