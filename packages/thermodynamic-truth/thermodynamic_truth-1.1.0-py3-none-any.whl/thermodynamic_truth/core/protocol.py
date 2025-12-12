"""
Thermodynamic Truth Protocol - Main Implementation

This is the core consensus protocol that integrates all thermodynamic components:
- State representation and ensembles
- Proof-of-Work for Sybil resistance
- Annealing for convergence
- Byzantine fault detection
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import time
import logging

from .state import ConsensusState, ThermodynamicEnsemble, create_genesis_state
from .pow import ProofOfWork, EnergyBudget
from .annealing import ThermodynamicAnnealer, AnnealingSchedule, ParallelTempering


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThermodynamicTruth:
    """
    Main Thermodynamic Truth consensus protocol.

    This class orchestrates the entire consensus process:
    1. Nodes propose states with Proof-of-Work
    2. States are collected into thermodynamic ensembles
    3. Annealing drives convergence to low-energy states
    4. Byzantine states are filtered using entropy metrics
    5. Consensus is achieved when variance drops below threshold
    """

    def __init__(
        self,
        node_id: str,
        pow_difficulty: float = 2.0,
        energy_per_hash: float = 1e-9,
        energy_budget: float = 1000.0,
        use_parallel_tempering: bool = True,
        n_replicas: int = 4,
        convergence_threshold: float = 0.05,
        byzantine_threshold: float = 3.0,
    ):
        """
        Initialize the Thermodynamic Truth protocol.

        Args:
            node_id: Unique identifier for this node
            pow_difficulty: Base Proof-of-Work difficulty
            energy_per_hash: Energy cost per hash (Joules)
            energy_budget: Energy budget per epoch
            use_parallel_tempering: Enable parallel tempering
            n_replicas: Number of temperature replicas
            convergence_threshold: Variance threshold for consensus
            byzantine_threshold: Standard deviations for Byzantine detection
        """
        self.node_id = node_id
        self.convergence_threshold = convergence_threshold
        self.byzantine_threshold = byzantine_threshold

        # Initialize components
        self.pow_engine = ProofOfWork(
            base_difficulty=pow_difficulty, energy_per_hash=energy_per_hash
        )

        self.energy_budget = EnergyBudget(budget_per_epoch=energy_budget, epoch_duration=60.0)

        self.annealer = ThermodynamicAnnealer(
            schedule=AnnealingSchedule(
                T_initial=10.0, T_final=0.01, schedule_type="exponential", alpha=0.95
            ),
            use_parallel_tempering=use_parallel_tempering,
            n_replicas=n_replicas,
        )

        # State tracking
        self.current_ensemble = ThermodynamicEnsemble()
        self.consensus_history = []
        self.round_number = 0

        logger.info(f"Initialized ThermoTruth protocol for node {node_id}")

    def propose_state(
        self, state_value: np.ndarray, adaptive_difficulty: bool = True
    ) -> Optional[ConsensusState]:
        """
        Propose a new consensus state with Proof-of-Work.

        Args:
            state_value: The state data to propose
            adaptive_difficulty: Use adaptive difficulty based on entropy

        Returns:
            ConsensusState if successful, None if budget insufficient
        """
        # Determine difficulty
        if adaptive_difficulty:
            entropy = self.current_ensemble.compute_entropy()
            byzantine_fraction = self._estimate_byzantine_fraction()
            difficulty = self.pow_engine.compute_adaptive_difficulty(entropy, byzantine_fraction)
        else:
            difficulty = self.pow_engine.base_difficulty

        # Check energy budget
        estimated_energy = self.pow_engine.estimate_energy_cost(difficulty)
        if not self.energy_budget.check_budget(self.node_id, estimated_energy):
            logger.warning(f"Node {self.node_id}: Insufficient energy budget")
            return None

        # Mine the state
        try:
            state = self.pow_engine.create_pow_state(state_value, self.node_id, difficulty)

            # Consume energy budget
            self.energy_budget.consume_budget(self.node_id, state.energy)

            logger.info(f"Node {self.node_id}: Proposed state with energy {state.energy:.6f}J")
            return state

        except RuntimeError as e:
            logger.error(f"Node {self.node_id}: Failed to mine state: {e}")
            return None

    def receive_state(self, state: ConsensusState) -> bool:
        """
        Receive and validate a state from another node.

        Args:
            state: Consensus state from peer

        Returns:
            True if state is valid and accepted
        """
        # Verify Proof-of-Work
        if not self.pow_engine.verify_pow(state):
            logger.warning(f"Node {self.node_id}: Invalid PoW from {state.proposer_id}")
            return False

        # Add to ensemble
        self.current_ensemble.add_state(state)
        logger.debug(f"Node {self.node_id}: Accepted state from {state.proposer_id}")
        return True

    def run_consensus_round(
        self, max_annealing_steps: int = 100, filter_byzantine: bool = True
    ) -> Tuple[np.ndarray, Dict]:
        """
        Run a complete consensus round.

        This is the main consensus algorithm:
        1. Filter Byzantine states (optional)
        2. Run annealing to converge ensemble
        3. Extract consensus state
        4. Compute metrics

        Args:
            max_annealing_steps: Maximum annealing iterations
            filter_byzantine: Enable Byzantine filtering

        Returns:
            Tuple of (consensus_state, metrics)
        """
        self.round_number += 1
        start_time = time.time()

        logger.info(f"Node {self.node_id}: Starting consensus round {self.round_number}")

        # Check if we have states
        if len(self.current_ensemble.states) == 0:
            logger.warning(f"Node {self.node_id}: No states in ensemble")
            return np.array([]), {"error": "no_states"}

        # Filter Byzantine states
        if filter_byzantine:
            original_count = len(self.current_ensemble.states)
            self.current_ensemble = self.current_ensemble.filter_byzantine_states(
                threshold=self.byzantine_threshold
            )
            filtered_count = original_count - len(self.current_ensemble.states)
            if filtered_count > 0:
                logger.info(f"Node {self.node_id}: Filtered {filtered_count} Byzantine states")

        # Run annealing
        if self.annealer.use_parallel_tempering:
            converged_ensemble, anneal_metrics = self.annealer.converge_with_tempering(
                self.current_ensemble,
                max_steps=max_annealing_steps,
                convergence_threshold=self.convergence_threshold,
            )
        else:
            converged_ensemble, anneal_metrics = self.annealer.converge(
                self.current_ensemble,
                max_steps=max_annealing_steps,
                convergence_threshold=self.convergence_threshold,
            )

        # Extract consensus state (energy-weighted)
        beta = 1.0 / (converged_ensemble.temperature + 1e-10)
        consensus_state = converged_ensemble.compute_weighted_consensus(beta)

        # Compute final metrics
        final_variance = converged_ensemble.compute_variance()
        final_temperature = converged_ensemble.compute_temperature()
        final_entropy = converged_ensemble.compute_entropy()

        elapsed_time = time.time() - start_time

        # Compile metrics
        metrics = {
            "round": self.round_number,
            "n_states": len(self.current_ensemble.states),
            "n_filtered": filtered_count if filter_byzantine else 0,
            "final_variance": final_variance,
            "final_temperature": final_temperature,
            "final_entropy": final_entropy,
            "converged": anneal_metrics["converged"],
            "annealing_steps": anneal_metrics["steps"],
            "total_time": elapsed_time,
            "consensus_state": consensus_state,
        }

        # Record history
        self.consensus_history.append(metrics)

        # Check consensus
        if final_variance < self.convergence_threshold:
            logger.info(
                f"Node {self.node_id}: Consensus achieved! "
                f"Variance={final_variance:.6f}, Temp={final_temperature:.6f}°C"
            )
        else:
            logger.warning(
                f"Node {self.node_id}: Consensus not achieved. " f"Variance={final_variance:.6f}"
            )

        return consensus_state, metrics

    def reset_ensemble(self):
        """Reset the current ensemble for a new round."""
        self.current_ensemble = ThermodynamicEnsemble()
        logger.debug(f"Node {self.node_id}: Reset ensemble")

    def _estimate_byzantine_fraction(self) -> float:
        """
        Estimate the fraction of Byzantine nodes based on entropy.

        High entropy indicates potential Byzantine activity.

        Returns:
            Estimated Byzantine fraction (0.0 to 1.0)
        """
        if len(self.current_ensemble.states) < 2:
            return 0.0

        entropy = self.current_ensemble.compute_entropy()

        # Heuristic: entropy > log2(n) suggests Byzantine activity
        n = len(self.current_ensemble.states)
        expected_entropy = np.log2(n) if n > 1 else 0.0

        if entropy > expected_entropy:
            # Estimate fraction based on excess entropy
            excess = entropy - expected_entropy
            fraction = min(excess / expected_entropy, 0.5)  # Cap at 50%
            return fraction

        return 0.0

    def get_status(self) -> Dict:
        """
        Get current protocol status.

        Returns:
            Status dictionary
        """
        return {
            "node_id": self.node_id,
            "round": self.round_number,
            "ensemble_size": len(self.current_ensemble.states),
            "current_temperature": self.current_ensemble.compute_temperature(),
            "current_entropy": self.current_ensemble.compute_entropy(),
            "current_variance": self.current_ensemble.compute_variance(),
            "energy_budget_remaining": self.energy_budget.get_remaining_budget(self.node_id),
            "total_rounds": len(self.consensus_history),
        }

    def create_genesis(self, genesis_value: np.ndarray) -> ConsensusState:
        """
        Create genesis state for network bootstrap.

        Args:
            genesis_value: Initial state value

        Returns:
            Genesis consensus state
        """
        genesis = create_genesis_state(genesis_value, self.node_id)
        self.current_ensemble.add_state(genesis)
        logger.info(f"Node {self.node_id}: Created genesis state")
        return genesis

    def get_consensus_metrics(self) -> Dict:
        """
        Get comprehensive consensus metrics.

        Returns:
            Metrics dictionary
        """
        if not self.consensus_history:
            return {}

        # Aggregate metrics across rounds
        variances = [r["final_variance"] for r in self.consensus_history]
        temperatures = [r["final_temperature"] for r in self.consensus_history]
        entropies = [r["final_entropy"] for r in self.consensus_history]
        times = [r["total_time"] for r in self.consensus_history]

        return {
            "total_rounds": len(self.consensus_history),
            "avg_variance": np.mean(variances),
            "avg_temperature": np.mean(temperatures),
            "avg_entropy": np.mean(entropies),
            "avg_time": np.mean(times),
            "convergence_rate": sum(r["converged"] for r in self.consensus_history)
            / len(self.consensus_history),
            "history": self.consensus_history,
        }
