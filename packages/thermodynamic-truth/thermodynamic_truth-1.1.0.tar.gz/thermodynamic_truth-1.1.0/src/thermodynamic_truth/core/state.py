"""
Thermodynamic State Representation

This module implements the core thermodynamic state representation for consensus.
States are represented as vectors in configuration space, with thermodynamic
properties (temperature, entropy, energy) computed from the ensemble.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import hashlib
import time


@dataclass
class ConsensusState:
    """
    Represents a proposed consensus state with thermodynamic properties.

    In the thermodynamic framework:
    - state_vector: The actual consensus value (e.g., transaction hash, data)
    - energy: Proof-of-Work energy expenditure (Joules equivalent)
    - timestamp: When the state was proposed
    - proposer_id: Node that proposed this state
    - nonce: Proof-of-Work nonce
    - difficulty: PoW difficulty level
    """

    state_vector: np.ndarray
    energy: float
    timestamp: float
    proposer_id: str
    nonce: int = 0
    difficulty: float = 1.0
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self):
        """Ensure state_vector is a numpy array."""
        if not isinstance(self.state_vector, np.ndarray):
            self.state_vector = np.array(self.state_vector, dtype=np.float64)

    def compute_hash(self) -> str:
        """Compute cryptographic hash of the state."""
        data = (
            self.state_vector.tobytes()
            + str(self.timestamp).encode()
            + str(self.proposer_id).encode()
            + str(self.nonce).encode()
        )
        return hashlib.sha256(data).hexdigest()

    def verify_pow(self) -> bool:
        """
        Verify that the Proof-of-Work satisfies the difficulty requirement.

        Returns:
            True if hash has required number of leading zeros
        """
        state_hash = self.compute_hash()
        required_zeros = int(self.difficulty)
        return state_hash.startswith("0" * required_zeros)


@dataclass
class ThermodynamicEnsemble:
    """
    Represents an ensemble of consensus states with thermodynamic properties.

    This is the core data structure for thermodynamic consensus:
    - states: Collection of proposed states from nodes
    - temperature: Measure of consensus error (variance)
    - entropy: Measure of state multiplicity (disorder)
    - free_energy: Helmholtz free energy (U - TS)
    """

    states: List[ConsensusState] = field(default_factory=list)
    temperature: float = 1.0  # Kelvin (or consensus error units)
    boltzmann_constant: float = 1.38e-23  # J/K (can be rescaled)

    def add_state(self, state: ConsensusState):
        """Add a new state to the ensemble."""
        self.states.append(state)

    def compute_mean_state(self) -> np.ndarray:
        """
        Compute the mean state vector (center of mass).

        Returns:
            Mean state vector across all proposals
        """
        if not self.states:
            return np.array([])

        state_vectors = np.array([s.state_vector for s in self.states])
        return np.mean(state_vectors, axis=0)

    def compute_variance(self) -> float:
        """
        Compute variance of state vectors (consensus error).

        This is the key thermodynamic quantity: variance maps to temperature.

        Returns:
            Variance (squared deviation from mean)
        """
        if len(self.states) < 2:
            return 0.0

        mean_state = self.compute_mean_state()
        deviations = np.array(
            [np.linalg.norm(s.state_vector - mean_state) ** 2 for s in self.states]
        )
        return np.mean(deviations)

    def compute_temperature(self) -> float:
        """
        Compute thermodynamic temperature from consensus variance.

        From equipartition theorem: <E> = (3/2) k T
        We map variance σ² to energy: T = (2/3k) σ²

        Returns:
            Temperature in Kelvin (or consensus error units)
        """
        variance = self.compute_variance()
        # Rescale to avoid numerical issues (use effective k)
        k_eff = 1.0  # Effective Boltzmann constant (dimensionless)
        self.temperature = (2.0 / 3.0) * variance / k_eff
        return self.temperature

    def compute_entropy(self) -> float:
        """
        Compute Shannon entropy of the state distribution.

        H = -Σ p_i log(p_i)

        We discretize the state space and compute probabilities.

        Returns:
            Shannon entropy (bits)
        """
        if len(self.states) < 2:
            return 0.0

        # Discretize states by hashing
        state_hashes = [s.compute_hash() for s in self.states]
        unique_hashes, counts = np.unique(state_hashes, return_counts=True)

        # Compute probabilities
        probabilities = counts / len(state_hashes)

        # Shannon entropy
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy

    def compute_total_energy(self) -> float:
        """
        Compute total internal energy (sum of PoW energies).

        Returns:
            Total energy in Joules (or equivalent units)
        """
        return sum(s.energy for s in self.states)

    def compute_free_energy(self) -> float:
        """
        Compute Helmholtz free energy: F = U - TS

        This is the quantity minimized at equilibrium.

        Returns:
            Free energy
        """
        U = self.compute_total_energy()
        T = self.compute_temperature()
        S = self.compute_entropy()

        # Use effective k for dimensionless entropy
        k_eff = 1.0
        F = U - T * S * k_eff
        return F

    def compute_partition_function(self, beta: float = 1.0) -> float:
        """
        Compute partition function: Z = Σ exp(-β E_i)

        Args:
            beta: Inverse temperature (1/kT)

        Returns:
            Partition function Z
        """
        if not self.states:
            return 1.0

        energies = np.array([s.energy for s in self.states])
        Z = np.sum(np.exp(-beta * energies))
        return Z

    def compute_boltzmann_weights(self, beta: float = 1.0) -> np.ndarray:
        """
        Compute Boltzmann weights for each state: w_i = exp(-β E_i) / Z

        Args:
            beta: Inverse temperature (1/kT)

        Returns:
            Array of weights (probabilities)
        """
        if not self.states:
            return np.array([])

        energies = np.array([s.energy for s in self.states])
        Z = self.compute_partition_function(beta)

        weights = np.exp(-beta * energies) / Z
        return weights

    def compute_weighted_consensus(self, beta: float = 1.0) -> np.ndarray:
        """
        Compute energy-weighted consensus state.

        States with lower energy (more PoW) have higher weight.

        Args:
            beta: Inverse temperature (1/kT)

        Returns:
            Weighted mean state vector
        """
        if not self.states:
            return np.array([])

        weights = self.compute_boltzmann_weights(beta)
        state_vectors = np.array([s.state_vector for s in self.states])

        weighted_state = np.average(state_vectors, axis=0, weights=weights)
        return weighted_state

    def filter_byzantine_states(self, threshold: float = 2.5) -> "ThermodynamicEnsemble":
        """
        Filter out Byzantine (outlier) states using robust statistical detection.

        Uses Median Absolute Deviation (MAD) instead of mean/std, which is
        resistant to outlier contamination. This prevents Byzantine nodes
        from inflating the std_dev and evading detection.

        MAD = median(|X_i - median(X)|)
        Modified Z-score = 0.6745 * (X_i - median(X)) / MAD

        Args:
            threshold: Modified Z-score threshold (default 2.5 ≈ 3σ for normal data)

        Returns:
            New ensemble with Byzantine states removed
        """
        if len(self.states) < 3:
            return self

        # Compute median state (robust central tendency)
        state_vectors = np.array([s.state_vector for s in self.states])
        median_state = np.median(state_vectors, axis=0)

        # Compute MAD (robust scale estimator)
        deviations = np.array([np.linalg.norm(s.state_vector - median_state) 
                               for s in self.states])
        mad = np.median(deviations)

        # Avoid division by zero
        if mad < 1e-10:
            # All states are identical (or near-identical)
            return self

        # Compute modified Z-scores (robust outlier detection)
        # Factor 0.6745 makes MAD comparable to std for normal distributions
        modified_z_scores = 0.6745 * deviations / mad

        # Filter states within threshold
        filtered_states = []
        for i, state in enumerate(self.states):
            if modified_z_scores[i] <= threshold:
                filtered_states.append(state)

        # Create new ensemble
        new_ensemble = ThermodynamicEnsemble(
            states=filtered_states,
            temperature=self.temperature,
            boltzmann_constant=self.boltzmann_constant,
        )
        return new_ensemble

    def get_consensus_metrics(self) -> Dict[str, float]:
        """
        Get all thermodynamic metrics for monitoring.

        Returns:
            Dictionary of metrics
        """
        return {
            "n_states": len(self.states),
            "temperature": self.compute_temperature(),
            "entropy": self.compute_entropy(),
            "variance": self.compute_variance(),
            "total_energy": self.compute_total_energy(),
            "free_energy": self.compute_free_energy(),
            "partition_function": self.compute_partition_function(),
        }


def create_genesis_state(state_value: np.ndarray, node_id: str) -> ConsensusState:
    """
    Create a genesis (initial) consensus state.

    Args:
        state_value: Initial state vector
        node_id: ID of the genesis node

    Returns:
        Genesis consensus state
    """
    return ConsensusState(
        state_vector=state_value,
        energy=0.0,  # Genesis has no PoW requirement
        timestamp=time.time(),
        proposer_id=node_id,
        nonce=0,
        difficulty=0.0,
        metadata={"genesis": True},
    )
