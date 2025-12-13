"""
MPIE Orchestrator — Event-driven engine coordinator.

Coordinates the online inference pipeline: Controller → Encoder → Evaluator → Store → Exporter.
Implements full Controller ⇆ Evaluator online interaction contract.
"""

import asyncio
import logging
import numpy as np  # type: ignore
from typing import Dict, Any, Optional, List
from collections import deque
import time
from dataclasses import asdict

from scarcity.runtime import EventBus, get_bus
from scarcity.engine.controller import BanditRouter
from scarcity.engine.encoder import Encoder
from scarcity.engine.evaluator import Evaluator
from scarcity.engine.store import HypergraphStore
from scarcity.engine.exporter import Exporter
from scarcity.engine.types import Candidate, EvalResult, Reward
from scarcity.engine.resource_profile import clone_default_profile

logger = logging.getLogger(__name__)


class MPIEOrchestrator:
    """
    Multi-Path Inference Engine orchestrator.
    
    Coordinates online inference pipeline under resource constraints.
    Never blocks; maintains bounded state only.
    """
    
    def __init__(self, bus: Optional[EventBus] = None):
        """
        Initialize MPIE orchestrator.
        
        Args:
            bus: EventBus instance (defaults to global bus)
        """
        self.bus = bus if bus else get_bus()
        
        # Get default resource profile
        self.last_resource_profile = self._get_default_profile()
        
        # Initialize subsystems
        rng = np.random.default_rng()
        self.controller = BanditRouter(drg=self.last_resource_profile, rng=rng)
        self.encoder = Encoder(drg=self.last_resource_profile)
        self.evaluator = Evaluator(drg=self.last_resource_profile, rng=rng)
        self.store = HypergraphStore()
        self.exporter = Exporter()
        
        # Bounded state
        self.profile_history = deque(maxlen=3)
        
        # Rolling statistics
        self.latency_ema = 0.0
        self.acceptance_counts = deque(maxlen=100)
        
        # Flags
        self.oom_backoff = False
        self.running = False
        
        # Stats
        self._stats = {
            'windows_processed': 0,
            'oom_incidents': 0,
            'avg_latency_ms': 0.0
        }
        
        logger.info("MPIE Orchestrator initialized with full Controller⇆Evaluator contract")
    
    async def start(self) -> None:
        """Start the orchestrator and subscribe to events."""
        if self.running:
            logger.warning("MPIE already running")
            return
        
        self.running = True
        
        # Subscribe to input events
        self.bus.subscribe("data_window", self._handle_data_window)
        self.bus.subscribe("resource_profile", self._handle_resource_profile)
        self.bus.subscribe("meta_policy_update", self._handle_meta_policy_update)
        
        logger.info("MPIE Orchestrator started with full subsystems")
    
    async def stop(self) -> None:
        """Stop the orchestrator."""
        if not self.running:
            return
        
        self.running = False
        
        # Unsubscribe
        self.bus.unsubscribe("data_window", self._handle_data_window)
        self.bus.unsubscribe("resource_profile", self._handle_resource_profile)
        self.bus.unsubscribe("meta_policy_update", self._handle_meta_policy_update)
        
        logger.info("MPIE Orchestrator stopped")
    
    async def _handle_data_window(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Handle incoming data window event.
        
        Implements full Controller ⇆ Evaluator online interaction contract.
        
        Args:
            topic: Event topic
            data: Window data
        """
        if not self.running:
            return
        
        start_time = time.time()
        
        try:
            # Step 1: Get current resource profile
            resource_profile = self.last_resource_profile or self._get_default_profile()
            
            # Step 2: Propose paths (Controller.propose returns List[Candidate])
            candidates = self.controller.propose(
                window_meta={'length': len(data.get('data', [])), 'timestamp': time.time()},
                schema=data.get('schema', {}),
                budget=resource_profile.get('n_paths', 200)
            )
            candidate_lookup = {cand.path_id: cand for cand in candidates}
            
            # Step 3: Extract window tensor
            window_tensor = data.get('data')
            if window_tensor is None:
                logger.warning("No data in window")
                return
            
            if isinstance(window_tensor, list):
                window_tensor = np.array(window_tensor)

            schema_obj = data.get('schema', {}) or {}
            var_names = self._resolve_var_names(schema_obj, window_tensor.shape[1])
            
            # Step 4: Score candidates (Evaluator.score returns List[EvalResult])
            results = self.evaluator.score(window_tensor, candidates)
            
            # Step 5: Build diversity lookup from Controller
            diversity_dict = {cand.path_id: self.controller.diversity_score(cand) for cand in candidates}
            D_lookup = lambda pid: diversity_dict.get(pid, 0.0)
            
            # Step 6: Produce rewards (Evaluator.make_rewards returns List[Reward])
            rewards = self.evaluator.make_rewards(results, D_lookup, candidates=candidates)
            
            # Step 7: Update Controller with rewards (bandit learning)
            self.controller.update(rewards)
            accepted_candidates: List[Candidate] = []
            store_payloads: List[Dict[str, Any]] = []
            for result in results:
                if not result.accepted:
                    continue
                candidate = candidate_lookup.get(result.path_id)
                if not candidate:
                    continue
                accepted_candidates.append(candidate)
                resolved_vars = [self._var_name(var_names, idx) for idx in candidate.vars]
                store_payloads.append({
                    'path_id': result.path_id,
                    'gain': result.gain,
                    'ci_lo': result.ci_lo,
                    'ci_hi': result.ci_hi,
                    'stability': result.stability,
                    'cost_ms': result.cost_ms,
                    'domain': candidate.domain,
                    'window_id': data.get('window_id', self._stats['windows_processed']),
                    'schema_version': schema_obj.get('version', 0),
                    'source': resolved_vars[0],
                    'target': resolved_vars[-1],
                    'vars': resolved_vars,
                    'var_indices': list(candidate.vars),
                    'lags': list(candidate.lags),
                    'ops': list(candidate.ops),
                })
            self.controller.register_acceptances(accepted_candidates)
            
            # Step 8: Update store with accepted results
            accepted = [r for r in results if r.accepted]
            accepted_payloads = [asdict(r) for r in accepted]
            if self.store and store_payloads:
                self.store.update_edges(store_payloads)
                await self.bus.publish(
                    "engine.insight",
                    {
                        "edges": store_payloads,
                        "window_id": data.get('window_id', self._stats['windows_processed']),
                        "timestamp": time.time(),
                    },
                )
            
            # Step 9: Export insights
            if self.exporter:
                self.exporter.emit_insights(accepted_payloads, resource_profile)
            
            # Step 10: Update metrics
            latency_ms = (time.time() - start_time) * 1000
            self._update_latency(latency_ms)
            self.acceptance_counts.append(len(accepted))
            self._stats['windows_processed'] += 1
            
            # Step 11: Publish comprehensive metrics
            await self._publish_metrics(latency_ms, len(candidates), len(accepted))
            
        except Exception as e:
            logger.error(f"Error processing data window: {e}", exc_info=True)
    
    async def _handle_resource_profile(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Handle resource profile update from DRG.
        
        Args:
            topic: Event topic
            data: Resource profile
        """
        self.last_resource_profile = data
        self.profile_history.append(data)
        
        logger.debug(f"Resource profile updated: {data}")
        
        # Propagate to subsystems
        if self.controller:
            self.controller.update_resource_profile(data)
        if self.evaluator:
            self.evaluator.drg = data
            if 'resamples' in data:
                self.evaluator.resamples = int(max(1, data['resamples']))
            if 'gain_min' in data:
                self.evaluator.gain_min = float(data['gain_min'])
    
    def _get_default_profile(self) -> Dict[str, Any]:
        """Get default resource profile."""
        return clone_default_profile()
    
    def _update_latency(self, latency_ms: float) -> None:
        """Update EMA of latency."""
        alpha = 0.3
        if self.latency_ema == 0:
            self.latency_ema = latency_ms
        else:
            self.latency_ema = alpha * latency_ms + (1 - alpha) * self.latency_ema
        
        self._stats['avg_latency_ms'] = self.latency_ema
    
    async def _publish_metrics(self, latency_ms: float, n_candidates: int, n_accepted: int) -> None:
        """Publish comprehensive processing metrics to bus."""
        # Get Controller stats
        ctrl_stats = self.controller.get_stats() if self.controller else {}
        
        # Get Evaluator stats
        eval_stats = self.evaluator.get_stats() if self.evaluator else {}
        
        # Compute diversity index from candidates (if available)
        # This is a placeholder - full implementation would track proposed diversity
        diversity_index = 0.0
        
        metrics = {
            # Orchestrator metrics
            'engine_latency_ms': latency_ms,
            'n_candidates': n_candidates,
            'accepted_count': n_accepted,
            'accept_rate': n_accepted / max(n_candidates, 1),
            'edges_active': self.store.get_edge_count() if self.store else 0,
            'oom_flag': self.oom_backoff,
            
            # Controller metrics (from §9)
            'proposal_entropy': ctrl_stats.get('proposal_entropy', 0.0),
            'diversity_index': diversity_index,
            'arm_mean_r_topk': ctrl_stats.get('arm_mean_r_topk', []),
            'drift_detections': ctrl_stats.get('drift_detections', 0),
            'thompson_mode': ctrl_stats.get('thompson_mode', False),
            
            # Evaluator metrics (from §9)
            'eval_accept_rate': eval_stats.get('accept_rate', 0.0),
            'gain_p50': eval_stats.get('gain_p50', 0.0),
            'gain_p90': eval_stats.get('gain_p90', 0.0),
            'ci_width_avg': eval_stats.get('ci_width_avg', 0.0),
            'stability_avg': eval_stats.get('stability_avg', 0.0),
            'total_evaluated': eval_stats.get('total_evaluated', 0)
        }
        
        await self.bus.publish("processing_metrics", metrics)

    async def _handle_meta_policy_update(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Apply meta-layer policy updates to subsystems.
        """
        if not data:
            return

        controller_cfg = data.get('controller', {})
        if controller_cfg and self.controller:
            self.controller.apply_meta_update(
                tau=controller_cfg.get('tau'),
                gamma_diversity=controller_cfg.get('gamma_diversity')
            )

        evaluator_cfg = data.get('evaluator', {})
        if evaluator_cfg and self.evaluator:
            self.evaluator.apply_meta_update(
                g_min=evaluator_cfg.get('g_min'),
                lambda_ci=evaluator_cfg.get('lambda_ci')
            )

        operator_cfg = data.get('operators', {})
        if operator_cfg:
            if 'tier3_topk' in operator_cfg:
                self.last_resource_profile['tier3_topk'] = operator_cfg['tier3_topk']
            if 'tier2' in operator_cfg:
                self.last_resource_profile['tier2_enabled'] = (operator_cfg['tier2'] != 'off')

    def _resolve_var_names(self, schema: Dict[str, Any], width: int) -> List[str]:
        """
        Resolve variable names from schema or fall back to positional identifiers.
        """
        fields = schema.get('fields', {}) if isinstance(schema, dict) else {}
        if isinstance(fields, dict) and fields:
            return list(fields.keys())
        if isinstance(fields, list) and fields:
            names = []
            for idx, entry in enumerate(fields):
                if isinstance(entry, dict) and entry.get('name'):
                    names.append(str(entry['name']))
                else:
                    names.append(f"var_{idx}")
            return names
        return [f"var_{idx}" for idx in range(width)]

    @staticmethod
    def _var_name(var_names: List[str], index: int) -> str:
        if 0 <= index < len(var_names):
            return var_names[index]
        return f"var_{index}"

    
    def set_oom_flag(self) -> None:
        """Set OOM backoff flag."""
        self.oom_backoff = True
        self._stats['oom_incidents'] += 1
        logger.warning("OOM flag set - reducing work next cycle")
    
    def clear_oom_flag(self) -> None:
        """Clear OOM backoff flag."""
        self.oom_backoff = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            **self._stats,
            'running': self.running,
            'oom_backoff': self.oom_backoff,
            'avg_accept_rate': sum(self.acceptance_counts) / max(len(self.acceptance_counts), 1)
        }

