"""
Engine Layer for SCARCITY.

Multi-Path Inference Engine (MPIE) for online learning and adaptive inference.
"""

from .engine import MPIEOrchestrator
from .controller import BanditRouter, Controller
from .encoder import Encoder, EncodedBatch
from .evaluator import Evaluator
from .store import Store, HypergraphStore
from .exporter import Exporter
from .types import Candidate, EvalResult, Reward
from . import utils as engine_utils

__all__ = [
    'MPIEOrchestrator',
    'BanditRouter',
    'Controller',
    'Encoder',
    'EncodedBatch',
    'Evaluator',
    'Store',
    'HypergraphStore',
    'Exporter',
    'Candidate',
    'EvalResult',
    'Reward',
    'engine_utils',
]

