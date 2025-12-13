"""
Evaluation Operators — Online scoring primitives.

R² gain, NLL gain, and Granger-like tests for path evaluation.
"""

import numpy as np


def r2_gain(y_true, y_pred, baseline_pred):
    """Compute R² gain vs baseline."""
    ss_res_pred = np.sum((y_true - y_pred) ** 2)
    ss_res_base = np.sum((y_true - baseline_pred) ** 2)
    
    if ss_res_base == 0:
        return 0.0
    
    r2_pred = 1 - ss_res_pred / np.var(y_true) if np.var(y_true) > 0 else 0
    r2_base = 1 - ss_res_base / np.var(y_true) if np.var(y_true) > 0 else 0
    
    return r2_pred - r2_base


def nll_gain(y_true, y_pred, baseline_pred):
    """Compute NLL gain vs baseline."""
    # Simplified: MSE-based approximation
    return r2_gain(y_true, y_pred, baseline_pred)


def granger_step(x, y, lag=1):
    """Granger causality test (lightweight)."""
    # Simplified: correlation-based
    return np.corrcoef(x[:-lag], y[lag:])[0, 1] if len(x) > lag else 0.0

