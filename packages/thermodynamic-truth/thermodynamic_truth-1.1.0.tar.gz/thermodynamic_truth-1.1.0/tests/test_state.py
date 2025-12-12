"""
Unit tests for thermodynamic_truth.core.state module

Tests cover:
- ConsensusState creation and validation
- ThermodynamicEnsemble operations
- Temperature, entropy, and free energy calculations
- Boltzmann weighting
- Byzantine filtering
- Edge cases and error handling
"""

import pytest
import numpy as np
import sys

sys.path.insert(0, "/home/ubuntu/thermo-truth-proto/src")

from thermodynamic_truth.core.state import (
    ConsensusState,
    ThermodynamicEnsemble,
    create_genesis_state,
)


class TestConsensusState:
    """Test ConsensusState class."""

    def test_create_state(self):
        """Test basic state creation."""
        state_vector = np.array([1.0, 2.0, 3.0])
        state = ConsensusState(
            state_vector=state_vector,
            energy=0.5,
            timestamp=1234567890.0,
            proposer_id="node_0",
            nonce=42,
            difficulty=2.0,
        )

        assert np.array_equal(state.state_vector, state_vector)
        assert state.energy == 0.5
        assert state.timestamp == 1234567890.0
        assert state.proposer_id == "node_0"
        assert state.nonce == 42
        assert state.difficulty == 2.0

    def test_state_with_metadata(self):
        """Test state with metadata."""
        state = ConsensusState(
            state_vector=np.array([1.0]),
            energy=0.1,
            timestamp=0.0,
            proposer_id="test",
            nonce=0,
            difficulty=1.0,
            metadata={"key": "value"},
        )

        assert state.metadata == {"key": "value"}

    def test_state_vector_storage(self):
        """Test that state vector is properly stored."""
        original = np.array([1.0, 2.0, 3.0])
        state = ConsensusState(
            state_vector=original,
            energy=0.0,
            timestamp=0.0,
            proposer_id="test",
            nonce=0,
            difficulty=0.0,
        )

        # State vector should be stored
        np.testing.assert_array_equal(state.state_vector, original)


class TestThermodynamicEnsemble:
    """Test ThermodynamicEnsemble class."""

    def test_empty_ensemble(self):
        """Test empty ensemble creation."""
        ensemble = ThermodynamicEnsemble()

        assert len(ensemble.states) == 0
        assert ensemble.compute_temperature() == 0.0
        assert ensemble.compute_entropy() == 0.0

    def test_add_state(self):
        """Test adding states to ensemble."""
        ensemble = ThermodynamicEnsemble()

        state = ConsensusState(
            state_vector=np.array([1.0, 2.0]),
            energy=0.5,
            timestamp=0.0,
            proposer_id="node_0",
            nonce=0,
            difficulty=1.0,
        )

        ensemble.add_state(state)
        assert len(ensemble.states) == 1
        assert ensemble.states[0] == state

    def test_compute_mean_state(self):
        """Test mean state computation."""
        ensemble = ThermodynamicEnsemble()

        # Add three states
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0, 2.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([2.0, 4.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([3.0, 6.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n2",
                nonce=0,
                difficulty=0.0,
            )
        )

        mean = ensemble.compute_mean_state()
        expected = np.array([2.0, 4.0])

        np.testing.assert_array_almost_equal(mean, expected)

    def test_compute_variance(self):
        """Test variance computation."""
        ensemble = ThermodynamicEnsemble()

        # Add states with known variance
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([0.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )

        variance = ensemble.compute_variance()

        # Variance of [0, 1] is 0.25
        assert abs(variance - 0.25) < 1e-6

    def test_compute_temperature(self):
        """Test temperature computation (T = 2σ²/3k)."""
        ensemble = ThermodynamicEnsemble()

        # Add states
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([0.0, 0.0, 0.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0, 1.0, 1.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )

        temperature = ensemble.compute_temperature()
        variance = ensemble.compute_variance()

        # T = (2/3) * variance (with k_B = 1)
        expected_temp = (2.0 / 3.0) * variance

        assert abs(temperature - expected_temp) < 1e-6

    def test_compute_entropy(self):
        """Test Shannon entropy computation."""
        ensemble = ThermodynamicEnsemble()

        # Add states with different energies
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([2.0]),
                energy=1.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )

        entropy = ensemble.compute_entropy()

        # Entropy should be positive for non-uniform distribution
        assert entropy >= 0.0

    def test_compute_free_energy(self):
        """Test Helmholtz free energy computation (F = U - TS)."""
        ensemble = ThermodynamicEnsemble()

        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0]),
                energy=2.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([2.0]),
                energy=3.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )

        free_energy = ensemble.compute_free_energy()

        # F = U - TS (should be a real number)
        assert isinstance(free_energy, float)

    def test_boltzmann_weights(self):
        """Test Boltzmann weight computation."""
        ensemble = ThermodynamicEnsemble()

        # Add states with different energies
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([2.0]),
                energy=1.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )

        weights = ensemble.compute_boltzmann_weights(beta=1.0)

        # Weights should sum to 1
        assert abs(np.sum(weights) - 1.0) < 1e-6

        # Lower energy should have higher weight
        assert weights[0] > weights[1]

    def test_weighted_consensus(self):
        """Test weighted consensus computation."""
        ensemble = ThermodynamicEnsemble()

        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([3.0]),
                energy=10.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )

        consensus = ensemble.compute_weighted_consensus(beta=1.0)

        # Should be closer to low-energy state
        assert consensus[0] < 2.0  # Closer to 1.0 than 3.0

    def test_filter_byzantine_states(self):
        """Test Byzantine state filtering."""
        ensemble = ThermodynamicEnsemble()

        # Add honest states (clustered)
        for i in range(10):
            ensemble.add_state(
                ConsensusState(
                    state_vector=np.array([1.0 + np.random.randn() * 0.01]),
                    energy=0.0,
                    timestamp=0.0,
                    proposer_id=f"honest_{i}",
                    nonce=0,
                    difficulty=0.0,
                )
            )

        # Add Byzantine outlier
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([100.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="byzantine",
                nonce=0,
                difficulty=0.0,
            )
        )

        filtered = ensemble.filter_byzantine_states(threshold=3.0)

        # Byzantine state should be filtered out
        assert len(filtered.states) == 10
        assert all("honest" in s.proposer_id for s in filtered.states)


class TestGenesisState:
    """Test genesis state creation."""

    def test_create_genesis(self):
        """Test genesis state creation."""
        genesis_value = np.array([0.0, 0.0, 0.0])
        genesis = create_genesis_state(genesis_value, node_id="genesis_node")

        np.testing.assert_array_equal(genesis.state_vector, genesis_value)
        assert genesis.energy == 0.0
        assert genesis.proposer_id == "genesis_node"
        assert genesis.difficulty == 0.0


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_single_state_variance(self):
        """Test variance with single state."""
        ensemble = ThermodynamicEnsemble()
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )

        variance = ensemble.compute_variance()
        assert variance == 0.0

    def test_zero_energy_states(self):
        """Test ensemble with all zero-energy states."""
        ensemble = ThermodynamicEnsemble()

        for i in range(5):
            ensemble.add_state(
                ConsensusState(
                    state_vector=np.array([float(i)]),
                    energy=0.0,
                    timestamp=0.0,
                    proposer_id=f"n{i}",
                    nonce=0,
                    difficulty=0.0,
                )
            )

        weights = ensemble.compute_boltzmann_weights(beta=1.0)

        # All weights should be equal for zero energy
        assert np.allclose(weights, 1.0 / 5.0)

    def test_high_beta_boltzmann(self):
        """Test Boltzmann weights with high beta (low temperature)."""
        ensemble = ThermodynamicEnsemble()

        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([1.0]),
                energy=0.0,
                timestamp=0.0,
                proposer_id="n0",
                nonce=0,
                difficulty=0.0,
            )
        )
        ensemble.add_state(
            ConsensusState(
                state_vector=np.array([2.0]),
                energy=1.0,
                timestamp=0.0,
                proposer_id="n1",
                nonce=0,
                difficulty=0.0,
            )
        )

        weights = ensemble.compute_boltzmann_weights(beta=100.0)

        # At high beta, low-energy state should dominate
        assert weights[0] > 0.99


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
