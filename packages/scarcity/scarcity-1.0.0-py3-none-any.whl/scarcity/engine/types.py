"""
Type definitions for Controller ⇆ Evaluator interaction.

Defines shared data structures for online bandit learning and path evaluation.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any


@dataclass
class Candidate:
    """
    A candidate path to explore.
    
    Attributes:
        path_id: Deterministic UUID based on (vars,lags,ops,schema_hash)
        vars: Variable indices forming the path
        lags: Lag values for each variable (same length as vars)
        ops: Operations applied (e.g., "sketch", "attn")
        root: First variable index (for bandit arm selection)
        depth: Path length
        domain: Shard/domain identifier
        gen_reason: How this candidate was generated ("UCB", "random", "diversity", etc.)
    """
    path_id: str
    vars: Tuple[int, ...]
    lags: Tuple[int, ...]
    ops: Tuple[str, ...]
    root: int
    depth: int
    domain: int
    gen_reason: str


@dataclass
class EvalResult:
    """
    Evaluation result for a candidate path.
    
    Attributes:
        path_id: Reference to the candidate
        gain: ΔR² or −ΔNLL (positive is good)
        ci_lo: Lower bound of confidence interval
        ci_hi: Upper bound of confidence interval
        stability: Stability score in [0,1]
        cost_ms: Computation time in milliseconds
        accepted: Whether path passed acceptance gates
        extras: Optional additional metrics (granger_p, holdout_rows, etc.)
    """
    path_id: str
    gain: float
    ci_lo: float
    ci_hi: float
    stability: float
    cost_ms: float
    accepted: bool
    extras: Dict[str, Any]


@dataclass
class Reward:
    """
    Shaped reward signal for bandit learning.
    
    Attributes:
        path_id: Reference to the candidate
        arm_key: Bandit arm identifier (e.g., (src, dst) or root variable)
        value: Shaped reward in [-1, +1]
        latency_penalty: Non-negative penalty term
        diversity_bonus: Non-negative bonus term
        accepted: Echo of acceptance status
    """
    path_id: str
    arm_key: Tuple[int, int]
    value: float
    latency_penalty: float
    diversity_bonus: float
    accepted: bool

