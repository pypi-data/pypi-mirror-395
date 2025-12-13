"""
Controller — Online bandit policy for path proposal.

Implements BanditRouter with UCB/Thompson Sampling, diversity tracking,
and online reward updates per Controller ⇆ Evaluator contract.
"""

import logging
import numpy as np
import hashlib
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict

from scarcity.engine.types import Candidate, Reward
from scarcity.engine.utils import clip, rolling_ema

logger = logging.getLogger(__name__)


class BanditRouter:
    """
    Online bandit router for path proposal.
    
    Balances exploration vs exploitation using UCB/Thompson Sampling.
    Ensures diversity and respects resource caps.
    """
    
    def __init__(self, drg: Optional[Dict[str, Any]] = None, rng: Optional[np.random.Generator] = None):
        """
        Initialize bandit router.
        
        Args:
            drg: Data Resource Governor profile with defaults
            rng: Random number generator
        """
        self.drg = drg or {}
        self.rng = rng if rng else np.random.default_rng()
        
        # Bandit state per arm (root variable)
        # Format: {arm_key: {'n', 'mean_r', 'var_r', 'M2', 'cost_ms_ema', 'total_pulls'}}
        self.arm_stats: Dict[int, Dict[str, float]] = defaultdict(
            lambda: {
                'n': 0,
                'mean_r': 0.0,
                'var_r': 0.0,
                'M2': 0.0,  # Welford variance accumulator
                'cost_ms_ema': 0.0,
                'total_pulls': 0
            }
        )
        
        # Diversity tracking (per-variable exposure counts, EMA)
        self.variable_coverage: Dict[int, float] = defaultdict(float)
        self.diversity_min = 1.0
        self.diversity_max = 0.0
        
        # Drift detection (Page-Hinkley)
        self.global_reward_mean = 0.0
        self.global_reward_var = 1.0
        self.page_hinkley_sum = 0.0
        self.drift_count = 0
        self.thompson_mode = False
        self.thompson_windows_remaining = 0
        
        # State
        self.temperature = self.drg.get('tau', 0.8)  # UCB exploration temp
        self.diversity_weight = self.drg.get('gamma', 0.3)
        self.cost_weight = self.drg.get('eta', 0.1)
        self.coverage_decay = self.drg.get('rho', 0.995)
        self.epsilon = self.drg.get('epsilon', 0.05)  # ε-greedy floor
        
        # Tracking
        self.total_windows = 0
        self.schema_hash = None
        
        logger.info(f"BanditRouter initialized: τ={self.temperature}, γ={self.diversity_weight}, η={self.cost_weight}")
    
    def propose(self, window_meta: Dict[str, Any], schema: Dict[str, Any], budget: int) -> List[Candidate]:
        """
        Propose candidate paths for current window.
        
        Args:
            window_meta: Window metadata (length, timestamp, etc.)
            schema: Variable schema with fields
            budget: Maximum number of candidates to return (n_paths)
            
        Returns:
            List of Candidate objects
        """
        # Update schema tracking
        raw_fields = schema.get('fields', {})
        if isinstance(raw_fields, dict):
            schema_field_names = sorted(raw_fields.keys())
        elif isinstance(raw_fields, list):
            schema_field_names = sorted(
                str(field.get('name', f"var_{idx}"))
                for idx, field in enumerate(raw_fields)
                if isinstance(field, dict)
            )
        else:
            schema_field_names = []
        schema_str = str(schema_field_names)
        self.schema_hash = hashlib.md5(schema_str.encode()).hexdigest()[:8]
        
        # Get variable set
        fields = raw_fields
        if isinstance(fields, dict):
            variable_names = list(fields.keys())
        elif isinstance(fields, list):
            variable_names = [str(field.get('name', f"var_{idx}")) for idx, field in enumerate(fields)]
        else:
            variable_names = []
        
        n_vars = len(variable_names)
        if n_vars < 2:
            return []
        
        # Decay coverage counters
        for v in self.variable_coverage:
            self.variable_coverage[v] *= self.coverage_decay
        
        # Get DRG parameters
        max_len = self.drg.get('max_path_len', 5)
        branch_width = self.drg.get('branch_width', 1)
        max_lag = self.drg.get('max_lag', 3)
        domain = self.drg.get('domain', 0)
        
        candidates = []
        
        # Assemble root set (mix of UCB arms, diversity picks, random)
        root_set = self._select_root_set(n_vars, budget, branch_width)
        
        # Expand each root into full paths
        for root_idx, gen_reason in root_set:
            if len(candidates) >= budget:
                break
            
            # Generate path variations
            for _ in range(branch_width):
                if len(candidates) >= budget:
                    break
                
                # Build path
                vars_tuple, lags_tuple, ops_tuple = self._build_path(root_idx, n_vars, max_len, max_lag)
                
                # Create path_id
                path_id = self._make_path_id(vars_tuple, lags_tuple, ops_tuple)
                
                # Build candidate
                cand = Candidate(
                    path_id=path_id,
                    vars=vars_tuple,
                    lags=lags_tuple,
                    ops=ops_tuple,
                    root=root_idx,
                    depth=len(vars_tuple),
                    domain=domain,
                    gen_reason=gen_reason
                )
                
                candidates.append(cand)
        
        self.total_windows += 1
        
        logger.debug(f"Proposed {len(candidates)} candidates (budget={budget})")
        return candidates
    
    def diversity_score(self, candidate: Candidate) -> float:
        """
        Compute diversity score for a candidate.
        
        Args:
            candidate: Candidate path
            
        Returns:
            Diversity score D(path) ∈ [0,1]
        """
        # Coverage: 1 / sqrt(1 + c[v])
        cov_scores = []
        for v in candidate.vars:
            c_v = self.variable_coverage[v]
            cov = 1.0 / np.sqrt(1.0 + c_v)
            cov_scores.append(cov)
        
        D = np.mean(cov_scores) if cov_scores else 0.0
        
        # Normalize using rolling min/max
        if D < self.diversity_min:
            self.diversity_min = D
        if D > self.diversity_max:
            self.diversity_max = D
        
        range_val = self.diversity_max - self.diversity_min
        if range_val < 1e-12:
            return 0.0
        
        D_norm = (D - self.diversity_min) / range_val
        return float(clip(D_norm, 0.0, 1.0))

    def apply_meta_update(self, tau: Optional[float] = None, gamma_diversity: Optional[float] = None) -> None:
        """
        Apply meta-layer parameter updates.
        """
        if tau is not None:
            self.temperature = float(np.clip(tau, 0.3, 1.5))
        if gamma_diversity is not None:
            self.diversity_weight = float(np.clip(gamma_diversity, 0.0, 1.0))

    def update_resource_profile(self, profile: Dict[str, Any]) -> None:
        """
        Update DRG-aware settings from resource profile.
        """
        self.drg = profile
        if 'tau' in profile:
            self.temperature = float(np.clip(profile['tau'], 0.3, 1.5))
        if 'gamma' in profile:
            self.diversity_weight = float(np.clip(profile['gamma'], 0.0, 1.0))
    
    def update(self, rewards: List[Reward]) -> None:
        """
        Update bandit statistics from rewards.
        
        Args:
            rewards: List of Reward objects from Evaluator
        """
        for reward in rewards:
            arm_key = reward.arm_key[0]  # Use root variable as arm
            
            if arm_key not in self.arm_stats:
                continue
            
            stats = self.arm_stats[arm_key]
            n = stats['n']
            mean_r = stats['mean_r']
            
            # Welford update
            stats['total_pulls'] += 1
            stats['n'] = n + 1
            
            delta = reward.value - mean_r
            stats['mean_r'] = mean_r + delta / stats['n']
            
            # Variance accumulator
            stats['M2'] += delta * (reward.value - stats['mean_r'])
            if n > 0:
                stats['var_r'] = stats['M2'] / n
            
            # Cost tracking prefers direct latency penalty feedback
            stats['cost_ms_ema'] = rolling_ema(
                reward.latency_penalty,
                stats['cost_ms_ema'],
                alpha=0.2
            )
            
            # Diversity tracking (only for accepted)
            if reward.accepted:
                # Note: We don't have full candidate info here, so we track per root
                # This is an approximation; full implementation would track per variable
                self.variable_coverage[arm_key] += 1
            
            # Global reward tracking for drift detection
            self._update_global_stats(reward.value)
        
        # Check for drift
        if self._detect_drift():
            self._handle_drift()

    def register_acceptances(self, accepted: List[Candidate]) -> None:
        """
        Update per-variable coverage counters for accepted candidates.
        """
        if not accepted:
            return
        for cand in accepted:
            for var_idx in cand.vars:
                self.variable_coverage[var_idx] += 1.0
    
    def _select_root_set(self, n_vars: int, budget: int, branch_width: int) -> List[Tuple[int, str]]:
        """
        Select root variables for path expansion.
        
        Returns:
            List of (variable_index, generation_reason) tuples
        """
        roots_needed = min(budget // max(branch_width, 1), n_vars)
        
        # Get UCB scores for all arms
        ucb_scores = self._compute_ucb_scores()
        
        # Sort by score
        sorted_arms = sorted(ucb_scores.items(), key=lambda x: x[1], reverse=True)
        
        root_set = []
        
        # Top UCB arms (exploitation)
        n_ucb = int(0.6 * roots_needed)
        for i, (arm, score) in enumerate(sorted_arms[:n_ucb]):
            if i < roots_needed:
                root_set.append((arm, "UCB"))
        
        # Diversity picks (exploration)
        n_div = int(0.25 * roots_needed)
        div_picks = self._select_diversity_roots(n_vars, n_div)
        for arm in div_picks:
            if len(root_set) < roots_needed:
                root_set.append((arm, "diversity"))
        
        # Random picks (ε-greedy)
        n_random = roots_needed - len(root_set)
        random_picks = self.rng.choice(n_vars, size=min(n_random, n_vars), replace=False)
        for arm in random_picks:
            root_set.append((arm, "random"))
        
        return root_set
    
    def _compute_ucb_scores(self) -> Dict[int, float]:
        """Compute UCB scores for all arms."""
        scores = {}
        T = sum(stats['total_pulls'] for stats in self.arm_stats.values())
        
        for arm, stats in self.arm_stats.items():
            n = stats['n']
            mean_r = stats['mean_r']
            cost_est = stats['cost_ms_ema']
            
            # UCB exploration term
            if n == 0:
                ucb_explore = float('inf')
            else:
                ucb_explore = self.temperature * np.sqrt(2 * np.log(max(T, 1)) / n)
            
            # Diversity bonus (approximate)
            D_est = 1.0 / np.sqrt(1.0 + self.variable_coverage[arm])
            
            # Final score
            ucb = mean_r + ucb_explore + self.diversity_weight * D_est - self.cost_weight * cost_est
            scores[arm] = ucb
        
        return scores
    
    def _select_diversity_roots(self, n_vars: int, n_picks: int) -> List[int]:
        """Select root variables based on low coverage."""
        if n_picks <= 0:
            return []
        
        # Score by inverse coverage
        scores = [(v, 1.0 / np.sqrt(1.0 + self.variable_coverage[v])) for v in range(n_vars)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return [v for v, _ in scores[:n_picks]]
    
    def _build_path(self, root: int, n_vars: int, max_len: int, max_lag: int) -> Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[str, ...]]:
        """
        Build a path from root variable.
        
        Returns:
            (vars, lags, ops) tuples
        """
        path_len = self.rng.integers(2, max_len + 1)
        vars_list = [root]
        lags_list = [0]
        ops_list = ["sketch"]
        
        # Expand path
        for _ in range(path_len - 1):
            next_var = self.rng.integers(0, n_vars)
            while next_var in vars_list:
                next_var = self.rng.integers(0, n_vars)
            
            vars_list.append(next_var)
            lags_list.append(self.rng.integers(0, max_lag + 1))
            ops_list.append("attn")
        
        return tuple(vars_list), tuple(lags_list), tuple(ops_list)
    
    def _make_path_id(self, vars_tuple: Tuple[int, ...], lags_tuple: Tuple[int, ...], ops_tuple: Tuple[str, ...]) -> str:
        """Generate deterministic path_id."""
        parts = [
            f"vars:{vars_tuple}",
            f"lags:{lags_tuple}",
            f"ops:{ops_tuple}",
            f"schema:{self.schema_hash}"
        ]
        path_str = "|".join(parts)
        return hashlib.md5(path_str.encode()).hexdigest()[:16]
    
    def _update_global_stats(self, reward: float) -> None:
        """Update global reward statistics for drift detection."""
        # Page-Hinkley detector
        old_mean = self.global_reward_mean
        self.global_reward_mean = rolling_ema(reward, self.global_reward_mean, alpha=0.01)
        
        diff = reward - old_mean - self.drift_threshold()
        self.page_hinkley_sum += diff
        self.page_hinkley_sum = max(0.0, self.page_hinkley_sum)
        
        # Update variance
        self.global_reward_var = rolling_ema((reward - self.global_reward_mean) ** 2, self.global_reward_var, alpha=0.01)
    
    def _detect_drift(self) -> bool:
        """Detect non-stationarity via Page-Hinkley."""
        if self.page_hinkley_sum > 100.0:  # Drift threshold
            return True
        return False
    
    def _handle_drift(self) -> None:
        """Handle detected drift."""
        logger.warning("Drift detected - adjusting exploration")
        
        self.drift_count += 1
        self.temperature = min(1.2, self.temperature + 0.2)
        
        # Switch to Thompson for K windows
        self.thompson_mode = True
        self.thompson_windows_remaining = 50
        
        # Reset arm statistics
        for stats in self.arm_stats.values():
            stats['n'] = max(1, int(0.7 * stats['n']))
        
        self.page_hinkley_sum = 0.0
    
    def drift_threshold(self) -> float:
        """Compute adaptive drift threshold."""
        std = np.sqrt(self.global_reward_var)
        return 0.05 * std if std > 0 else 0.1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get controller statistics."""
        # Compute entropy over arm selection
        probs = [stats['n'] / max(1, sum(s['n'] for s in self.arm_stats.values())) 
                 for stats in self.arm_stats.values()]
        entropy = -sum(p * np.log(p + 1e-12) for p in probs if p > 0)
        
        # Top-K arm means
        arm_means = [(arm, stats['mean_r']) for arm, stats in self.arm_stats.items()]
        arm_means.sort(key=lambda x: x[1], reverse=True)
        topk_means = [r for _, r in arm_means[:5]]
        
        return {
            'n_arms': len(self.arm_stats),
            'temperature': self.temperature,
            'diversity_weight': self.diversity_weight,
            'proposal_entropy': float(entropy),
            'arm_mean_r_topk': topk_means,
            'drift_detections': self.drift_count,
            'thompson_mode': self.thompson_mode,
            'total_windows': self.total_windows
        }


# Backward compatibility alias
Controller = BanditRouter
