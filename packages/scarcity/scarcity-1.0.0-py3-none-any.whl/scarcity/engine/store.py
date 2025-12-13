"""
HypergraphStore — Online hypergraph memory for MPIE.

Maintains compact, evolving graph of relationships with edges, hyperedges,
regimes, partitions, indexing, decay, and schema versioning.
"""

import logging
import numpy as np
import hashlib
from typing import Dict, Any, List, Tuple, Optional, Set
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
import heapq

logger = logging.getLogger(__name__)


@dataclass
class EdgeRec:
    """Edge record for storage."""
    weight: float  # EMA of effect (fp32)
    var: float  # running variance (fp32)
    stability: float  # EMA of stability (fp32)
    ci_lo: float  # fp16
    ci_hi: float  # fp16
    regime_id: int  # -1 if global
    last_seen: int  # window_id
    hits: int  # acceptance count
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class HyperRec:
    """Hyperedge record."""
    order: int  # number of sources
    weight: float
    stability: float
    ci_lo: float
    ci_hi: float
    regime_id: int
    last_seen: int
    hits: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class HypergraphStore:
    """
    Online hypergraph store with bounded memory.
    
    Maintains edges, hyperedges, indexes, partitions, and regimes.
    """
    
    def __init__(
        self,
        max_edges: int = 10000,
        max_hyperedges: int = 1000,
        topk_per_node: int = 32,
        decay_factor: float = 0.995,
        alpha_weight: float = 0.2,
        alpha_stability: float = 0.2,
        gc_interval: int = 25
    ):
        """
        Initialize hypergraph store.
        
        Args:
            max_edges: Maximum number of edges
            max_hyperedges: Maximum number of hyperedges
            topk_per_node: Maximum neighbors per node in index
            decay_factor: Per-window decay factor
            alpha_weight: EMA coefficient for weight
            alpha_stability: EMA coefficient for stability
            gc_interval: Windows between GC calls
        """
        self.max_edges = max_edges
        self.max_hyperedges = max_hyperedges
        self.topk_per_node = topk_per_node
        self.decay_factor = decay_factor
        self.alpha_weight = alpha_weight
        self.alpha_stability = alpha_stability
        self.gc_interval = gc_interval
        
        # Node registry
        self.nodes: Dict[int, Dict[str, Any]] = {}  # node_id -> {name, domain, schema_ver, flags}
        
        # Edge storage: (src_id, dst_id) -> EdgeRec
        self.edges: Dict[Tuple[int, int], EdgeRec] = {}
        
        # Hyperedge storage: frozenset(sources) -> HyperRec
        self.hyperedges: Dict[frozenset, HyperRec] = {}
        
        # Indexes: node_id -> heap of (score, neighbor_id, key)
        self.out_index: Dict[int, List[Tuple[float, int, Tuple[int, int]]]] = defaultdict(list)
        self.in_index: Dict[int, List[Tuple[float, int, Tuple[int, int]]]] = defaultdict(list)
        
        # Domain partitions: domain_id -> Set[edge_keys]
        self.domain_partitions: Dict[int, Set[Tuple[int, int]]] = defaultdict(set)
        
        # Regime buffers: edge_key -> List[regime_counts]
        self.regime_buffers: Dict[Tuple[int, int], List[int]] = defaultdict(lambda: [0] * 4)
        
        # State
        self.current_window = 0
        self.schema_hash = None
        self.next_node_id = 0
        self.gc_counter = 0
        
        # Statistics
        self._stats = {
            'edges_added': 0,
            'edges_pruned': 0,
            'hyperedges_added': 0,
            'hyperedges_pruned': 0,
            'promotions': 0,
            'demotions': 0,
            'gc_cycles': 0
        }
        
        logger.info(
            f"HypergraphStore initialized: max_edges={max_edges}, "
            f"max_hyperedges={max_hyperedges}, topk={topk_per_node}"
        )
    
    def get_or_create_node(self, name: str, domain: int = 0, schema_ver: int = 0) -> int:
        """
        Get or create a node.
        
        Args:
            name: Node name
            domain: Domain identifier
            schema_ver: Schema version
            
        Returns:
            Node ID
        """
        # Check if node exists
        for node_id, node_data in self.nodes.items():
            if node_data['name'] == name and node_data['schema_ver'] == schema_ver:
                return node_id
        
        # Create new node
        node_id = self.next_node_id
        self.next_node_id += 1
        
        self.nodes[node_id] = {
            'name': name,
            'domain': domain,
            'schema_ver': schema_ver,
            'flags': 0
        }
        
        return node_id
    
    def upsert_edge(
        self,
        src_id: int,
        dst_id: int,
        effect: float,
        ci_lo: float,
        ci_hi: float,
        stability: float,
        regime_id: int = -1,
        ts: Optional[int] = None
    ) -> None:
        """
        Insert or update an edge.
        
        Args:
            src_id: Source node ID
            dst_id: Destination node ID
            effect: Effect estimate
            ci_lo: Lower CI bound
            ci_hi: Upper CI bound
            stability: Stability metric
            regime_id: Regime identifier
            ts: Timestamp/window_id (defaults to current)
        """
        if ts is None:
            ts = self.current_window
        
        key = (src_id, dst_id)
        
        if key in self.edges:
            # Update existing edge
            edge = self.edges[key]
            
            # EMA update for weight
            edge.weight = (1 - self.alpha_weight) * edge.weight + self.alpha_weight * effect
            
            # EMA update for stability
            edge.stability = (1 - self.alpha_stability) * edge.stability + self.alpha_stability * stability
            
            # Update CI
            edge.ci_lo = ci_lo
            edge.ci_hi = ci_hi
            
            # Update metadata
            edge.regime_id = regime_id
            edge.last_seen = ts
            edge.hits += 1
            
            # Update CI sanity check (only down-weight if too uncertain)
            ci_width = ci_hi - ci_lo
            if abs(edge.weight) > 1e-6 and ci_width > 0.5 * abs(edge.weight):
                edge.weight *= 0.5  # Down-weight uncertain edges
                logger.debug(f"Edge {key} down-weighted due to high CI width: {ci_width}")
            
        else:
            # Create new edge
            self.edges[key] = EdgeRec(
                weight=effect,
                var=0.0,
                stability=stability,
                ci_lo=ci_lo,
                ci_hi=ci_hi,
                regime_id=regime_id,
                last_seen=ts,
                hits=1
            )
            
            self._stats['edges_added'] += 1
        
        # Update indexes
        self._update_indexes(key)
        
        # Update domain partition
        if src_id in self.nodes:
            domain = self.nodes[src_id]['domain']
            self.domain_partitions[domain].add(key)
    
    def upsert_hyperedge(
        self,
        sources: List[int],
        effect: float,
        ci_lo: float,
        ci_hi: float,
        stability: float,
        regime_id: int = -1,
        ts: Optional[int] = None,
    ) -> None:
        """
        Insert or update a hyperedge.
        """
        if not sources:
            return
        key = frozenset(int(src) for src in sources)
        timestamp = ts if ts is not None else self.current_window

        if key in self.hyperedges:
            hyper = self.hyperedges[key]
            hyper.weight = (1 - self.alpha_weight) * hyper.weight + self.alpha_weight * effect
            hyper.stability = max(hyper.stability, stability)
            hyper.ci_lo = ci_lo
            hyper.ci_hi = ci_hi
            hyper.regime_id = regime_id
            hyper.last_seen = timestamp
            hyper.hits += 1
        else:
            self.hyperedges[key] = HyperRec(
                order=len(key),
                weight=effect,
                stability=stability,
                ci_lo=ci_lo,
                ci_hi=ci_hi,
                regime_id=regime_id,
                last_seen=timestamp,
                hits=1,
            )
            self._stats['hyperedges_added'] += 1

    def _update_indexes(self, key: Tuple[int, int]) -> None:
        """Update out/in indexes for a key."""
        src_id, dst_id = key
        edge = self.edges[key]
        score = edge.weight * edge.stability
        
        # Update out_index for src
        heap = self.out_index[src_id]
        heapq.heappush(heap, (-score, dst_id, key))  # Negative for max-heap
        
        # Keep only top-k
        if len(heap) > self.topk_per_node:
            self.out_index[src_id] = heapq.nsmallest(self.topk_per_node, heap)
            heapq.heapify(self.out_index[src_id])
        
        # Update in_index for dst
        heap = self.in_index[dst_id]
        heapq.heappush(heap, (-score, src_id, key))
        
        if len(heap) > self.topk_per_node:
            self.in_index[dst_id] = heapq.nsmallest(self.topk_per_node, heap)
            heapq.heapify(self.in_index[dst_id])
    
    def top_k_neighbors(self, node_id: int, k: int, direction: str = "out", domain: Optional[int] = None) -> List[Tuple[int, float]]:
        """
        Get top-k neighbors of a node.
        
        Args:
            node_id: Node identifier
            k: Number of neighbors to return
            direction: "out" or "in"
            domain: Optional domain filter
            
        Returns:
            List of (neighbor_id, score) tuples
        """
        index = self.out_index[node_id] if direction == "out" else self.in_index[node_id]
        
        neighbors = []
        for neg_score, neighbor_id, key in index[:k]:
            # Filter by domain if specified
            if domain is not None:
                if direction == "out":
                    src_domain = self.nodes[node_id].get('domain')
                else:
                    src_domain = self.nodes[neighbor_id].get('domain')
                if src_domain != domain:
                    continue
            
            neighbors.append((neighbor_id, -neg_score))  # Convert back to positive
        
        return neighbors
    
    def decay(self, ts: int) -> None:
        """
        Apply temporal decay to all edges.
        
        Args:
            ts: Current timestamp/window_id
        """
        self.current_window = ts
        
        # Decay edges
        for key, edge in self.edges.items():
            edge.weight *= self.decay_factor
            edge.stability *= 0.997  # Slightly different decay for stability
            
            # Check for stale edges
            age = ts - edge.last_seen
            if age > 600:  # T_stale
                edge.weight *= 0.5
        
        # Decay hyperedges
        for hyper_rec in self.hyperedges.values():
            hyper_rec.weight *= self.decay_factor
            hyper_rec.stability *= 0.997
    
    def prune(self) -> None:
        """Remove weak or stale edges."""
        to_remove = []
        
        for key, edge in self.edges.items():
            # Check pruning criteria
            if (abs(edge.weight) < 0.02 or  # epsilon_weight
                edge.stability < 0.4 or  # epsilon_stability
                (self.current_window - edge.last_seen) > 5000):  # T_prune
                to_remove.append(key)
        
        for key in to_remove:
            del self.edges[key]
            self._stats['edges_pruned'] += 1
        
        # Prune hyperedges
        to_remove_hyper = []
        for key, hyper_rec in self.hyperedges.items():
            if (abs(hyper_rec.weight) < 0.02 or
                hyper_rec.stability < 0.4 or
                (self.current_window - hyper_rec.last_seen) > 5000):
                to_remove_hyper.append(key)
        
        for key in to_remove_hyper:
            del self.hyperedges[key]
            self._stats['hyperedges_pruned'] += 1
    
    def remove_edge(self, src_id: int, dst_id: int) -> bool:
        """
        Remove an edge if present.
        """
        key = (src_id, dst_id)
        if key in self.edges:
            del self.edges[key]
            self._stats['edges_pruned'] += 1
            return True
        return False

    def gc(self, ts: int) -> None:
        """
        Periodic garbage collection (decay + prune).
        
        Args:
            ts: Current timestamp
        """
        self.gc_counter += 1
        if self.gc_counter % self.gc_interval == 0:
            self.decay(ts)
            self.prune()
            self._stats['gc_cycles'] += 1
    
    def get_edge(self, src_id: int, dst_id: int) -> Optional[EdgeRec]:
        """Get edge record."""
        return self.edges.get((src_id, dst_id))
    
    def snapshot(self, include_regimes: bool = True) -> Dict[str, Any]:
        """
        Create a snapshot of the store.
        
        Args:
            include_regimes: Whether to include regime data
            
        Returns:
            Dictionary snapshot
        """
        return {
            'version': '1.0',
            'schema_hash': self.schema_hash,
            'current_window': self.current_window,
            'nodes': {nid: data for nid, data in self.nodes.items()},
            'edges': {str(k): e.to_dict() for k, e in self.edges.items()},
            'hyperedges': {str(k): h.to_dict() for k, h in self.hyperedges.items()},
            'stats': self.get_stats()
        }
    
    def stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        edges_active = len(self.edges)
        hyperedges_active = len(self.hyperedges)

        if edges_active == 0:
            avg_weight = 0.0
            avg_stability = 0.0
        else:
            weights = [e.weight for e in self.edges.values()]
            stabilities = [e.stability for e in self.edges.values()]
            avg_weight = float(np.mean(weights))
            avg_stability = float(np.mean(stabilities))

        return {
            'n_edges': edges_active,
            'n_hyperedges': hyperedges_active,
            'edges_active': edges_active,
            'hyperedges_active': hyperedges_active,
            'avg_weight': avg_weight,
            'avg_stability': avg_stability,
            'pruned_last_min': self._stats['edges_pruned'],
            'promotions': self._stats['promotions'],
            'demotions': self._stats['demotions'],
            'gc_cycles': self._stats['gc_cycles']
        }
    
    # Compatibility with old API
    def update_edges(self, evaluation_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Update store with accepted edges (compatibility method)."""
        ingested: List[Dict[str, Any]] = []

        for payload in evaluation_results:
            if not isinstance(payload, dict):
                continue

            source_name = payload.get('source') or payload.get('source_name')
            target_name = payload.get('target') or payload.get('target_name')
            if not source_name or not target_name:
                continue

            domain = int(payload.get('domain', 0) or 0)
            schema_ver = int(payload.get('schema_version', payload.get('schema_ver', 0)) or 0)
            ts = int(payload.get('window_id', self.current_window))
            self.current_window = max(self.current_window, ts)

            effect = float(payload.get('gain', payload.get('effect', 0.0)))
            ci_lo = float(payload.get('ci_lo', payload.get('ci_lower', 0.0)))
            ci_hi = float(payload.get('ci_hi', payload.get('ci_upper', 0.0)))
            stability = float(payload.get('stability', payload.get('stability_score', 0.0)))
            regime_id = int(payload.get('regime_id', -1))

            src_id = self.get_or_create_node(str(source_name), domain=domain, schema_ver=schema_ver)
            dst_id = self.get_or_create_node(str(target_name), domain=domain, schema_ver=schema_ver)
            self.upsert_edge(
                src_id=src_id,
                dst_id=dst_id,
                effect=effect,
                ci_lo=ci_lo,
                ci_hi=ci_hi,
                stability=stability,
                regime_id=regime_id,
                ts=ts
            )

            vars_payload = payload.get('vars') or payload.get('variables')
            if isinstance(vars_payload, (list, tuple)) and len(vars_payload) >= 2:
                hyper_nodes = [
                    self.get_or_create_node(str(var_name), domain=domain, schema_ver=schema_ver)
                    for var_name in vars_payload
                ]
                self.upsert_hyperedge(
                    sources=hyper_nodes,
                    effect=effect,
                    ci_lo=ci_lo,
                    ci_hi=ci_hi,
                    stability=stability,
                    regime_id=regime_id,
                    ts=ts
                )

            ingested.append({
                'path_id': payload.get('path_id'),
                'source_id': src_id,
                'target_id': dst_id,
                'effect': effect,
                'window_id': ts
            })

        if ingested:
            self.gc(self.current_window)

        return ingested
    
    def get_edge_count(self) -> int:
        """Get current number of edges."""
        return len(self.edges)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        return self.stats()


# Alias for backward compatibility
Store = HypergraphStore
