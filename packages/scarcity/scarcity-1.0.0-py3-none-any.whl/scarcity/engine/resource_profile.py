"""
Shared resource profile utilities for SCARCITY engine.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Any

DEFAULT_RESOURCE_PROFILE: Dict[str, Any] = {
    'n_paths': 200,
    'precision': 'fp16',
    'sketch_dim': 512,
    'window_size': 256,
    'resamples': 8,
    'export_interval': 10,
    'branch_width': 1,
    'tier2_enabled': True,
    'tier3_topk': 5,
}


def clone_default_profile() -> Dict[str, Any]:
    """Return a fresh copy of the default resource profile."""
    return deepcopy(DEFAULT_RESOURCE_PROFILE)

