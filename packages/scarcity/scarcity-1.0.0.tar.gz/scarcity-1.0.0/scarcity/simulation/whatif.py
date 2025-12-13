"""
Counterfactual / what-if scenario manager.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np  # type: ignore

from .environment import SimulationEnvironment, EnvironmentState
from .dynamics import DynamicsEngine, DynamicsConfig


@dataclass
class WhatIfConfig:
    horizon_steps: int = 12
    bootstrap_runs: int = 8
    noise_sigma: float = 0.02


class WhatIfManager:
    def __init__(
        self,
        environment: SimulationEnvironment,
        dynamics_config: DynamicsConfig,
        config: WhatIfConfig,
    ):
        self.env = environment
        self.base_dynamics = DynamicsEngine(environment, dynamics_config)
        self.config = config
        self._rng = np.random.default_rng(environment.config.seed + 13)

    def run_scenario(
        self,
        scenario_id: str,
        node_shocks: Optional[Dict[str, float]] = None,
        edge_shocks: Optional[Dict[Tuple[str, str], float]] = None,
        horizon: Optional[int] = None,
    ) -> Dict[str, any]:
        horizon = horizon or self.config.horizon_steps
        baseline_state = self.env.clone_state()
        perturbed_state = self._apply_shocks(baseline_state, node_shocks, edge_shocks)

        baseline_traj = self._simulate_trajectory(baseline_state, horizon)
        perturbed_traj = self._simulate_trajectory(perturbed_state, horizon)

        deltas = [
            {
                node_id: perturbed_traj[t][node_id] - baseline_traj[t][node_id]
                for node_id in baseline_traj[t]
            }
            for t in range(horizon + 1)
        ]

        ci = self._bootstrap_ci(baseline_state, node_shocks, edge_shocks, horizon, baseline_traj)

        top_impacts = self._top_impacts(deltas[-1])

        return {
            "scenario_id": scenario_id,
            "horizon": horizon,
            "delta": deltas,
            "confidence_interval": ci,
            "top_impacts": top_impacts,
        }

    def _simulate_trajectory(self, start_state: EnvironmentState, horizon: int) -> List[Dict[str, float]]:
        original_state = self.env.clone_state()
        self.env.set_state(copy.deepcopy(start_state))
        dynamics = DynamicsEngine(self.env, self.base_dynamics.config)
        trajectory = [dict(zip(start_state.node_ids, start_state.values.tolist()))]
        for _ in range(horizon):
            trajectory.append(dynamics.step())
        self.env.set_state(original_state)
        return trajectory

    def _apply_shocks(
        self,
        state: EnvironmentState,
        node_shocks: Optional[Dict[str, float]],
        edge_shocks: Optional[Dict[Tuple[str, str], float]],
    ) -> EnvironmentState:
        shocked = EnvironmentState(
            values=state.values.copy(),
            node_ids=state.node_ids.copy(),
            adjacency=state.adjacency.copy(),
            stability=state.stability.copy(),
            timestamp=state.timestamp,
        )
        if node_shocks:
            for node_id, delta in node_shocks.items():
                if node_id in shocked.node_ids:
                    idx = shocked.node_ids.index(node_id)
                    shocked.values[idx] += delta
        if edge_shocks:
            for (src, dst), delta in edge_shocks.items():
                if src in shocked.node_ids and dst in shocked.node_ids:
                    i = shocked.node_ids.index(src)
                    j = shocked.node_ids.index(dst)
                    shocked.adjacency[i, j] += delta
        return shocked

    def _bootstrap_ci(
        self,
        start_state: EnvironmentState,
        node_shocks: Optional[Dict[str, float]],
        edge_shocks: Optional[Dict[Tuple[str, str], float]],
        horizon: int,
        baseline_traj: List[Dict[str, float]],
    ) -> Tuple[float, float]:
        if self.config.bootstrap_runs <= 1:
            return (0.0, 0.0)

        impacts = []
        for _ in range(self.config.bootstrap_runs):
            noise_shocks = {
                node_id: self._rng.normal(0.0, self.config.noise_sigma)
                for node_id in (node_shocks or {})
            }
            perturbed = self._apply_shocks(start_state, noise_shocks, edge_shocks)
            traj = self._simulate_trajectory(perturbed, horizon)
            impacts.append(
                sum(
                    abs(traj[-1][node] - baseline_traj[-1][node])
                    for node in baseline_traj[-1]
                )
            )
        if not impacts:
            return (0.0, 0.0)
        impacts = np.asarray(impacts, dtype=np.float32)
        mean = float(np.mean(impacts))
        std = float(np.std(impacts))
        return (mean - std, mean + std)

    def _top_impacts(self, final_delta: Dict[str, float], k: int = 5) -> List[Dict[str, float]]:
        sorted_nodes = sorted(final_delta.items(), key=lambda kv: abs(kv[1]), reverse=True)
        return [{"id": node, "delta": float(delta)} for node, delta in sorted_nodes[:k]]

