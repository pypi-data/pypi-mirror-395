"""
Proof-of-Work Mechanism

Implements thermodynamic Proof-of-Work as an energy cost function for Sybil resistance.
Unlike Bitcoin's lottery-based PoW, this is used as a cost barrier and energy metric
for thermodynamic weighting.
"""

import hashlib
import time
from typing import Tuple, Optional
import numpy as np
from .state import ConsensusState


class ProofOfWork:
    """
    Thermodynamic Proof-of-Work engine.

    This implements PoW as an energy expenditure mechanism rather than a lottery.
    The difficulty is adaptive based on network entropy and Byzantine activity.
    """

    def __init__(self, base_difficulty: float = 2.0, energy_per_hash: float = 1e-9):
        """
        Initialize PoW engine.

        Args:
            base_difficulty: Base difficulty level (number of leading zeros)
            energy_per_hash: Energy cost per hash attempt (Joules)
        """
        self.base_difficulty = base_difficulty
        self.energy_per_hash = energy_per_hash
        self.adaptive_enabled = True

    def compute_hash(
        self, state_vector: np.ndarray, timestamp: float, proposer_id: str, nonce: int
    ) -> str:
        """
        Compute SHA-256 hash of state data.

        Args:
            state_vector: State data
            timestamp: Timestamp
            proposer_id: Node ID
            nonce: Proof-of-work nonce

        Returns:
            Hexadecimal hash string
        """
        data = (
            state_vector.tobytes()
            + str(timestamp).encode()
            + str(proposer_id).encode()
            + str(nonce).encode()
        )
        return hashlib.sha256(data).hexdigest()

    def verify_pow(self, state: ConsensusState) -> bool:
        """
        Verify that a state satisfies PoW requirements.

        Args:
            state: Consensus state to verify

        Returns:
            True if PoW is valid
        """
        state_hash = self.compute_hash(
            state.state_vector, state.timestamp, state.proposer_id, state.nonce
        )

        required_zeros = int(state.difficulty)
        return state_hash.startswith("0" * required_zeros)

    def mine(
        self,
        state_vector: np.ndarray,
        proposer_id: str,
        difficulty: Optional[float] = None,
        max_attempts: int = 1000000,
        timestamp: Optional[float] = None,
    ) -> Tuple[int, float, str, float]:
        """
        Mine a valid nonce for the given state.

        Args:
            state_vector: State data to mine
            proposer_id: Node ID
            difficulty: Target difficulty (uses base if None)
            max_attempts: Maximum mining attempts
            timestamp: Timestamp to use (generates new if None)

        Returns:
            Tuple of (nonce, energy_spent, final_hash, timestamp)
        """
        if difficulty is None:
            difficulty = self.base_difficulty

        if timestamp is None:
            timestamp = time.time()

        required_zeros = int(difficulty)
        target_prefix = "0" * required_zeros

        nonce = 0
        attempts = 0

        while attempts < max_attempts:
            state_hash = self.compute_hash(state_vector, timestamp, proposer_id, nonce)

            if state_hash.startswith(target_prefix):
                # Found valid nonce
                energy_spent = attempts * self.energy_per_hash
                return nonce, energy_spent, state_hash, timestamp

            nonce += 1
            attempts += 1

        # Failed to find valid nonce
        raise RuntimeError(f"Failed to mine valid nonce after {max_attempts} attempts")

    def compute_adaptive_difficulty(self, entropy: float, byzantine_fraction: float = 0.0) -> float:
        """
        Compute adaptive difficulty based on network conditions.

        From the whitepaper: d = log(1 + H) where H is entropy.
        We also increase difficulty if Byzantine activity is detected.

        Args:
            entropy: Shannon entropy of state distribution
            byzantine_fraction: Estimated fraction of Byzantine nodes

        Returns:
            Adaptive difficulty level
        """
        if not self.adaptive_enabled:
            return self.base_difficulty

        # Entropy-based adjustment
        entropy_difficulty = np.log(1 + entropy) if entropy > 0 else 0.0

        # Byzantine adjustment (increase difficulty under attack)
        byzantine_multiplier = 1.0 + 2.0 * byzantine_fraction

        # Combined difficulty
        adaptive_difficulty = self.base_difficulty + entropy_difficulty * byzantine_multiplier

        # Clamp to reasonable range
        adaptive_difficulty = max(1.0, min(adaptive_difficulty, 10.0))

        return adaptive_difficulty

    def estimate_energy_cost(self, difficulty: float) -> float:
        """
        Estimate expected energy cost for given difficulty.

        Expected attempts = 16^difficulty (for hex leading zeros)

        Args:
            difficulty: Target difficulty

        Returns:
            Expected energy in Joules
        """
        expected_attempts = 16**difficulty
        expected_energy = expected_attempts * self.energy_per_hash
        return expected_energy

    def create_pow_state(
        self, state_vector: np.ndarray, proposer_id: str, difficulty: Optional[float] = None
    ) -> ConsensusState:
        """
        Create a consensus state with valid Proof-of-Work.

        Args:
            state_vector: State data
            proposer_id: Node ID
            difficulty: Target difficulty (uses base if None)

        Returns:
            ConsensusState with valid PoW
        """
        if difficulty is None:
            difficulty = self.base_difficulty

        # Mine the state
        nonce, energy, state_hash, timestamp = self.mine(state_vector, proposer_id, difficulty)

        # Create state object with the SAME timestamp used in mining
        state = ConsensusState(
            state_vector=state_vector,
            energy=energy,
            timestamp=timestamp,
            proposer_id=proposer_id,
            nonce=nonce,
            difficulty=difficulty,
            metadata={"hash": state_hash},
        )

        return state


class EnergyBudget:
    """
    Manages energy budgets for nodes to prevent spam.

    Each node has a limited energy budget per epoch. This prevents
    Sybil attacks by making it expensive to create many identities.
    """

    def __init__(self, budget_per_epoch: float = 1000.0, epoch_duration: float = 60.0):
        """
        Initialize energy budget manager.

        Args:
            budget_per_epoch: Maximum energy per node per epoch (Joules)
            epoch_duration: Duration of an epoch (seconds)
        """
        self.budget_per_epoch = budget_per_epoch
        self.epoch_duration = epoch_duration
        self.node_budgets = {}  # node_id -> remaining_energy
        self.epoch_start = time.time()

    def reset_epoch(self):
        """Reset all budgets for a new epoch."""
        self.node_budgets = {}
        self.epoch_start = time.time()

    def check_budget(self, node_id: str, required_energy: float) -> bool:
        """
        Check if a node has sufficient energy budget.

        Args:
            node_id: Node identifier
            required_energy: Energy required for operation

        Returns:
            True if node has sufficient budget
        """
        # Reset epoch if needed
        if time.time() - self.epoch_start > self.epoch_duration:
            self.reset_epoch()

        # Get current budget
        used_energy = self.node_budgets.get(node_id, 0.0)
        remaining = self.budget_per_epoch - used_energy

        return remaining >= required_energy

    def consume_budget(self, node_id: str, energy: float) -> bool:
        """
        Consume energy budget for a node.

        Args:
            node_id: Node identifier
            energy: Energy to consume

        Returns:
            True if consumption successful, False if insufficient budget
        """
        if not self.check_budget(node_id, energy):
            return False

        current_used = self.node_budgets.get(node_id, 0.0)
        self.node_budgets[node_id] = current_used + energy
        return True

    def get_remaining_budget(self, node_id: str) -> float:
        """
        Get remaining energy budget for a node.

        Args:
            node_id: Node identifier

        Returns:
            Remaining energy budget
        """
        used_energy = self.node_budgets.get(node_id, 0.0)
        return self.budget_per_epoch - used_energy

    def get_budget_fraction(self, node_id: str) -> float:
        """
        Get fraction of budget remaining.

        Args:
            node_id: Node identifier

        Returns:
            Fraction remaining (0.0 to 1.0)
        """
        remaining = self.get_remaining_budget(node_id)
        return remaining / self.budget_per_epoch
