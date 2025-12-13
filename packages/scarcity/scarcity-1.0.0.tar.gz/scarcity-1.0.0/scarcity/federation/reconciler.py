"""
Utilities for merging aggregated federation updates into the local store.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional

import numpy as np

from scarcity.engine.store import HypergraphStore
from .packets import EdgeDelta, PathPack, CausalSemanticPack


@dataclass
class ReconcilerConfig:
    decay_factor: float = 0.05
    min_weight: float = 1e-4


class StoreReconciler:
    def __init__(self, store: HypergraphStore, config: Optional[ReconcilerConfig] = None):
        self.store = store
        self.config = config or ReconcilerConfig()

    def merge_path_pack(self, pack: PathPack) -> Dict[str, int]:
        inserted = 0
        updated = 0

        for src, dst, weight, ci, stability, regime in pack.edges:
            if abs(weight) < self.config.min_weight:
                continue
            self.store.upsert_edge(
                src_id=int(src),
                dst_id=int(dst),
                effect=weight,
                ci_lo=-ci,
                ci_hi=ci,
                stability=stability,
                regime_id=regime,
            )
            updated += 1

        for hyper in pack.hyperedges:
            sources = hyper.get("S", [])
            if not sources:
                continue
            self.store.upsert_hyperedge(
                sources=[int(s) for s in sources],
                effect=hyper.get("w", 0.0),
                ci_lo=hyper.get("ci", 0.0),
                ci_hi=hyper.get("ci", 0.0),
                stability=hyper.get("st", 0.5),
                regime_id=hyper.get("reg", -1),
            )
            inserted += 1

        return {"edges_updated": updated, "hyperedges_inserted": inserted}

    def merge_edge_delta(self, delta: EdgeDelta) -> Dict[str, int]:
        updated = 0
        pruned = 0
        for key, weight_delta, stability_delta, hits_delta, regime, last_seen in delta.upserts:
            src, dst = key.split("->")
            edge = self.store.get_edge(int(src), int(dst))
            weight = weight_delta
            stability = stability_delta
            if edge is not None:
                weight = (1 - self.config.decay_factor) * edge.weight + weight_delta
                stability = max(edge.stability, stability_delta)
            self.store.upsert_edge(
                src_id=int(src),
                dst_id=int(dst),
                effect=weight,
                ci_lo=edge.ci_lo if edge else -0.1,
                ci_hi=edge.ci_hi if edge else 0.1,
                stability=stability,
                regime_id=regime,
                ts=last_seen,
            )
            updated += 1

        for key in delta.prunes:
            src, dst = key.split("->")
            if self.store.remove_edge(int(src), int(dst)):
                pruned += 1

        return {"edges_updated": updated, "edges_pruned": pruned}

    def merge_causal_pack(self, pack: CausalSemanticPack) -> Dict[str, int]:
        accepted = 0
        for pair in pack.pairs:
            self.store.upsert_edge(
                src_id=int(pair.source),
                dst_id=int(pair.target),
                effect=pair.probability,
                ci_lo=-0.1,
                ci_hi=0.1,
                stability=max(0.5, pair.probability),
                regime_id=pair.regime or -1,
            )
            accepted += 1
        return {"causal_pairs": accepted}

