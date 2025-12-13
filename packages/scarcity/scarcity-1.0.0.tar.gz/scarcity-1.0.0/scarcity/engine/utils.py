"""
Numeric utilities for Controller ⇆ Evaluator math.

Provides robust normalization, clipping, and rolling statistics.
"""

import numpy as np
from typing import List, Optional


def clip(x: float, lo: float, hi: float) -> float:
    """Clip value to [lo, hi]."""
    return max(lo, min(hi, x))


def safe_div(a: float, b: float, default: float = 0.0) -> float:
    """Safe division with default fallback."""
    if abs(b) < 1e-12:
        return default
    return a / b


def rolling_ema(new_val: float, old_ema: float, alpha: float) -> float:
    """Compute exponential moving average."""
    if old_ema == 0.0:
        return new_val
    return alpha * new_val + (1 - alpha) * old_ema


def robust_zscore(x: float, median: float, mad: float) -> float:
    """
    Compute robust z-score using median and MAD.
    
    Args:
        x: Value to normalize
        median: Median of the distribution
        mad: Median Absolute Deviation
        
    Returns:
        Z-score, typically clipped to [-3, +3]
    """
    if mad < 1e-12:
        return 0.0
    return (x - median) / mad


def robust_quantiles(values: List[float], quantiles: List[float]) -> List[float]:
    """
    Compute robust quantiles using rank statistics.
    
    Args:
        values: List of numeric values
        quantiles: List of quantile levels (e.g., [0.16, 0.84])
        
    Returns:
        List of quantile values
    """
    if len(values) == 0:
        return [0.0] * len(quantiles)
    
    sorted_vals = np.array(sorted(values))
    n = len(sorted_vals)
    
    result = []
    for q in quantiles:
        idx = int(np.round(q * (n - 1)))
        idx = max(0, min(n - 1, idx))
        result.append(float(sorted_vals[idx]))
    
    return result


def softplus(x: float) -> float:
    """
    Smooth ReLU: log(1 + exp(x))
    
    More numerically stable than naive implementation.
    """
    # For large x, softplus(x) ≈ x
    # For small x, softplus(x) ≈ log(1 + x)
    if x > 20:
        return x
    return np.log1p(np.exp(x))


def tanh_clip(x: float, bound: float = 3.0) -> float:
    """
    Hyperbolic tangent with bounds.
    
    Args:
        x: Input value
        bound: Maximum absolute value before clipping
        
    Returns:
        tanh(x / bound) * bound
    """
    return np.tanh(clip(x / bound, -1.0, 1.0)) * bound


def compute_median_mad(values: List[float]) -> tuple[float, float]:
    """
    Compute robust location and scale estimators.
    
    Args:
        values: List of numeric values
        
    Returns:
        (median, mad) tuple
    """
    if len(values) == 0:
        return 0.0, 1.0
    
    vals = np.array(values)
    median = float(np.median(vals))
    mad = float(np.median(np.abs(vals - median)))
    
    # Prevent division by zero
    if mad < 1e-12:
        mad = 1.0
    
    return median, mad

