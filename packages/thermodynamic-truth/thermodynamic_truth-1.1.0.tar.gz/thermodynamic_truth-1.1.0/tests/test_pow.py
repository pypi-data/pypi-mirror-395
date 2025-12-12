"""
Unit tests for thermodynamic_truth.core.pow module

Tests cover:
- Proof-of-Work mining and validation
- Adaptive difficulty adjustment
- Energy budget management
- Hash computation and verification
- Edge cases and security
"""

import pytest
import numpy as np
import sys

sys.path.insert(0, "/home/ubuntu/thermo-truth-proto/src")

from thermodynamic_truth.core.pow import ProofOfWork, EnergyBudget


class TestProofOfWork:
    """Test ProofOfWork class."""

    def test_create_pow_engine(self):
        """Test PoW engine creation."""
        pow_engine = ProofOfWork(base_difficulty=2.0)

        assert pow_engine.base_difficulty == 2.0
        assert pow_engine.energy_per_hash > 0

    def test_mine_with_zero_difficulty(self):
        """Test mining with zero difficulty (should succeed immediately)."""
        pow_engine = ProofOfWork(base_difficulty=0.0)

        state_vector = np.array([1.0, 2.0, 3.0])
        nonce, energy, hash_val, timestamp = pow_engine.mine(
            state_vector, "test_node", difficulty=0.0
        )

        assert nonce >= 0
        assert energy >= 0
        assert isinstance(hash_val, str)
        assert timestamp > 0

    def test_mine_with_low_difficulty(self):
        """Test mining with low difficulty."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        state_vector = np.array([1.0])
        nonce, energy, hash_val, timestamp = pow_engine.mine(
            state_vector, "test_node", difficulty=1.0, max_attempts=10000
        )

        assert nonce >= 0
        assert energy > 0
        assert hash_val.startswith("0")

    def test_create_pow_state(self):
        """Test creating a state with PoW."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        state_vector = np.array([1.0, 2.0])
        state = pow_engine.create_pow_state(state_vector, "test_node", difficulty=1.0)

        assert np.array_equal(state.state_vector, state_vector)
        assert state.energy > 0
        assert state.proposer_id == "test_node"
        assert state.difficulty == 1.0

    def test_verify_pow(self):
        """Test PoW verification."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        state_vector = np.array([1.0, 2.0])
        state = pow_engine.create_pow_state(state_vector, "test_node", difficulty=1.0)

        # Verification should succeed (state was created with valid PoW)
        is_valid = pow_engine.verify_pow(state)

        # Debug: print hash to see what's happening
        if not is_valid:
            hash_val = pow_engine.compute_hash(
                state.state_vector, state.timestamp, state.proposer_id, state.nonce
            )
            print(f"Hash: {hash_val}, Difficulty: {state.difficulty}, Nonce: {state.nonce}")

        assert is_valid

    def test_verify_invalid_state(self):
        """Test verification with invalid state."""
        from thermodynamic_truth.core.state import ConsensusState

        pow_engine = ProofOfWork(base_difficulty=2.0)

        # Create state with invalid nonce
        state = ConsensusState(
            state_vector=np.array([1.0]),
            energy=0.0,
            timestamp=0.0,
            proposer_id="test",
            nonce=0,
            difficulty=2.0,
        )

        # Should fail (unless extremely lucky)
        is_valid = pow_engine.verify_pow(state)
        assert not is_valid

    def test_adaptive_difficulty(self):
        """Test adaptive difficulty calculation."""
        pow_engine = ProofOfWork(base_difficulty=1.0)
        pow_engine.adaptive_enabled = True

        # Low entropy should give low difficulty
        low_entropy = 0.1
        diff_low = pow_engine.compute_adaptive_difficulty(low_entropy)

        # High entropy should give higher difficulty
        high_entropy = 5.0
        diff_high = pow_engine.compute_adaptive_difficulty(high_entropy)

        assert diff_high > diff_low

    def test_difficulty_formula(self):
        """Test difficulty formula: d = base + log(1 + H)."""
        pow_engine = ProofOfWork(base_difficulty=1.0)
        pow_engine.adaptive_enabled = True

        entropy = 2.718  # e - 1
        difficulty = pow_engine.compute_adaptive_difficulty(entropy)

        # d = 1.0 + log(1 + 2.718) ≈ 1.0 + log(3.718) ≈ 1.0 + 1.31 ≈ 2.31
        assert 2.0 < difficulty < 3.0

    def test_energy_estimation(self):
        """Test energy cost estimation."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        difficulty = 1.0
        estimated_energy = pow_engine.estimate_energy_cost(difficulty)

        # Should be 16^1 * energy_per_hash
        expected = 16 * pow_engine.energy_per_hash
        assert abs(estimated_energy - expected) < 1e-12

    def test_hash_computation(self):
        """Test hash computation."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        state_vector = np.array([1.0, 2.0, 3.0])
        hash_val = pow_engine.compute_hash(state_vector, 12345.0, "test_node", 42)

        assert isinstance(hash_val, str)
        assert len(hash_val) == 64  # SHA-256 hex length

    def test_hash_deterministic(self):
        """Test that hash computation is deterministic."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        state_vector = np.array([1.0, 2.0, 3.0])
        timestamp = 12345.0
        proposer_id = "test_node"
        nonce = 42

        # Compute hash twice
        hash1 = pow_engine.compute_hash(state_vector, timestamp, proposer_id, nonce)
        hash2 = pow_engine.compute_hash(state_vector, timestamp, proposer_id, nonce)

        assert hash1 == hash2

    def test_different_inputs_different_hashes(self):
        """Test that different inputs produce different hashes."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        vector1 = np.array([1.0])
        vector2 = np.array([2.0])

        hash1 = pow_engine.compute_hash(vector1, 0.0, "test", 0)
        hash2 = pow_engine.compute_hash(vector2, 0.0, "test", 0)

        assert hash1 != hash2


class TestEnergyBudget:
    """Test EnergyBudget class."""

    def test_create_budget(self):
        """Test energy budget creation."""
        budget = EnergyBudget(budget_per_epoch=1000.0)

        assert budget.budget_per_epoch == 1000.0
        assert budget.epoch_duration > 0

    def test_check_budget(self):
        """Test checking energy budget."""
        budget = EnergyBudget(budget_per_epoch=100.0)

        # First check should pass
        has_budget = budget.check_budget("node_0", 50.0)
        assert has_budget

    def test_consume_budget(self):
        """Test consuming energy budget."""
        budget = EnergyBudget(budget_per_epoch=100.0)

        # Consume some energy
        success = budget.consume_budget("node_0", 50.0)
        assert success

        # Check remaining budget
        has_budget = budget.check_budget("node_0", 60.0)
        assert not has_budget  # Only 50 left

        has_budget = budget.check_budget("node_0", 40.0)
        assert has_budget  # 40 is within remaining 50

    def test_exceed_budget(self):
        """Test exceeding energy budget."""
        budget = EnergyBudget(budget_per_epoch=100.0)

        # Consume most of budget
        budget.consume_budget("node_0", 90.0)

        # Try to consume more than remaining
        success = budget.consume_budget("node_0", 20.0)
        assert not success

    def test_multiple_nodes(self):
        """Test budget tracking for multiple nodes."""
        budget = EnergyBudget(budget_per_epoch=100.0)

        # Each node has independent budget
        budget.consume_budget("node_0", 50.0)
        budget.consume_budget("node_1", 50.0)

        # Both should have 50 remaining
        assert budget.check_budget("node_0", 50.0)
        assert budget.check_budget("node_1", 50.0)

    def test_epoch_reset(self):
        """Test epoch reset."""
        budget = EnergyBudget(budget_per_epoch=100.0, epoch_duration=0.1)

        # Consume budget
        budget.consume_budget("node_0", 90.0)

        # Wait for epoch to expire
        import time

        time.sleep(0.15)

        # Budget should be reset
        has_budget = budget.check_budget("node_0", 100.0)
        assert has_budget


class TestPoWIntegration:
    """Integration tests for PoW system."""

    def test_pow_with_budget(self):
        """Test PoW mining with energy budget."""
        pow_engine = ProofOfWork(base_difficulty=1.0)
        budget = EnergyBudget(budget_per_epoch=1000.0)

        state_vector = np.array([1.0, 2.0])
        nonce, energy, hash_val, timestamp = pow_engine.mine(
            state_vector, "test_node", difficulty=1.0
        )

        # Check budget before consuming
        has_budget = budget.check_budget("test_node", energy)
        assert has_budget

        # Consume energy
        success = budget.consume_budget("test_node", energy)
        assert success

    def test_multiple_mining_operations(self):
        """Test multiple mining operations with budget."""
        pow_engine = ProofOfWork(base_difficulty=0.5)
        budget = EnergyBudget(budget_per_epoch=1000.0)

        for i in range(5):
            state_vector = np.array([float(i)])
            nonce, energy, hash_val, timestamp = pow_engine.mine(
                state_vector, "test_node", difficulty=0.5
            )

            has_budget = budget.check_budget("test_node", energy)
            if has_budget:
                budget.consume_budget("test_node", energy)


class TestEdgeCases:
    """Test edge cases and security."""

    def test_max_attempts_limit(self):
        """Test that mining respects max attempts."""
        pow_engine = ProofOfWork(base_difficulty=10.0)

        state_vector = np.array([1.0])

        # Should raise RuntimeError when max_attempts is too low
        with pytest.raises(RuntimeError):
            pow_engine.mine(state_vector, "test_node", difficulty=10.0, max_attempts=10)

    def test_zero_difficulty_mining(self):
        """Test mining with zero difficulty."""
        pow_engine = ProofOfWork(base_difficulty=0.0)

        state_vector = np.array([1.0])
        nonce, energy, hash_val, timestamp = pow_engine.mine(
            state_vector, "test_node", difficulty=0.0
        )

        # Should succeed immediately
        assert nonce == 0
        assert energy == 0.0

    def test_adaptive_difficulty_disabled(self):
        """Test adaptive difficulty when disabled."""
        pow_engine = ProofOfWork(base_difficulty=2.0)
        pow_engine.adaptive_enabled = False

        difficulty = pow_engine.compute_adaptive_difficulty(entropy=10.0)

        # Should return base difficulty
        assert difficulty == 2.0

    def test_byzantine_difficulty_adjustment(self):
        """Test difficulty adjustment under Byzantine attack."""
        pow_engine = ProofOfWork(base_difficulty=1.0)

        # No Byzantine activity
        diff_normal = pow_engine.compute_adaptive_difficulty(entropy=1.0, byzantine_fraction=0.0)

        # With Byzantine activity
        diff_attack = pow_engine.compute_adaptive_difficulty(entropy=1.0, byzantine_fraction=0.3)

        # Difficulty should increase under attack
        assert diff_attack > diff_normal


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
