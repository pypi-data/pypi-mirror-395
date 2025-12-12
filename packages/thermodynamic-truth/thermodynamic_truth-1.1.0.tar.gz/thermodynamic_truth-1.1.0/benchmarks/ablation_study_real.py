"""
Real Ablation Study: Component Contribution Analysis

Tests the actual impact of removing protocol components.
This validates the thermodynamic necessity claims with real measurements.
"""

import sys
sys.path.insert(0, '/home/ubuntu/thermo-truth-proto/src')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os
from dataclasses import dataclass
from typing import List

from thermodynamic_truth.core.protocol import ThermodynamicTruth
from thermodynamic_truth.core.state import ConsensusState, ThermodynamicEnsemble
from thermodynamic_truth.core.annealing import ThermodynamicAnnealer, AnnealingSchedule


@dataclass
class AblationResult:
    variant: str
    attack_magnitude: float
    final_error: float
    converged: bool
    time_taken: float


def run_full_protocol(attack_magnitude: float, n_nodes: int = 10) -> AblationResult:
    """Run full protocol with all components."""
    protocol = ThermodynamicTruth(
        node_id="ablation_full",
        pow_difficulty=2.0,
        use_parallel_tempering=True,
        n_replicas=4
    )
    
    # Honest nodes
    honest_center = np.array([1.0, 2.0, 3.0])
    for i in range(n_nodes):
        state_value = honest_center + np.random.randn(3) * 0.05
        state = protocol.propose_state(state_value, adaptive_difficulty=True)
        if state:
            protocol.current_ensemble.add_state(state)
    
    # Attack: add states with large deviation
    n_attack = int(attack_magnitude / 10)  # Scale attack
    for i in range(n_attack):
        state_value = honest_center + np.random.randn(3) * attack_magnitude
        state = protocol.propose_state(state_value, adaptive_difficulty=True)
        if state:
            protocol.current_ensemble.add_state(state)
    
    # Run consensus
    import time
    start = time.time()
    consensus_state, metrics = protocol.run_consensus_round(
        max_annealing_steps=100,
        filter_byzantine=True
    )
    elapsed = time.time() - start
    
    return AblationResult(
        variant="Full Protocol",
        attack_magnitude=attack_magnitude,
        final_error=metrics['final_variance'],
        converged=metrics['converged'],
        time_taken=elapsed
    )


def run_no_energy(attack_magnitude: float, n_nodes: int = 10) -> AblationResult:
    """Run without Proof-of-Work (no energy cost)."""
    # Disable PoW by setting difficulty to 0
    protocol = ThermodynamicTruth(
        node_id="ablation_no_energy",
        pow_difficulty=0.0,  # No PoW
        use_parallel_tempering=True,
        n_replicas=4
    )
    protocol.pow_engine.adaptive_enabled = False
    
    # Honest nodes
    honest_center = np.array([1.0, 2.0, 3.0])
    for i in range(n_nodes):
        state_value = honest_center + np.random.randn(3) * 0.05
        # Manually create states without PoW
        state = ConsensusState(
            state_vector=state_value,
            energy=0.0,  # No energy
            timestamp=0.0,
            proposer_id=f"node_{i}",
            nonce=0,
            difficulty=0.0
        )
        protocol.current_ensemble.add_state(state)
    
    # Attack: spam with many low-cost states
    n_attack = int(attack_magnitude * 2)  # More attacks without PoW cost
    for i in range(n_attack):
        state_value = honest_center + np.random.randn(3) * attack_magnitude
        state = ConsensusState(
            state_vector=state_value,
            energy=0.0,
            timestamp=0.0,
            proposer_id=f"attacker_{i}",
            nonce=0,
            difficulty=0.0
        )
        protocol.current_ensemble.add_state(state)
    
    # Run consensus
    import time
    start = time.time()
    consensus_state, metrics = protocol.run_consensus_round(
        max_annealing_steps=100,
        filter_byzantine=True
    )
    elapsed = time.time() - start
    
    return AblationResult(
        variant="No Energy",
        attack_magnitude=attack_magnitude,
        final_error=metrics['final_variance'],
        converged=metrics['converged'],
        time_taken=elapsed
    )


def run_no_annealing(attack_magnitude: float, n_nodes: int = 10) -> AblationResult:
    """Run without annealing (simple averaging)."""
    protocol = ThermodynamicTruth(
        node_id="ablation_no_anneal",
        pow_difficulty=2.0,
        use_parallel_tempering=False,  # Disable tempering
        n_replicas=1
    )
    
    # Honest nodes
    honest_center = np.array([1.0, 2.0, 3.0])
    for i in range(n_nodes):
        state_value = honest_center + np.random.randn(3) * 0.05
        state = protocol.propose_state(state_value, adaptive_difficulty=False)
        if state:
            protocol.current_ensemble.add_state(state)
    
    # Attack
    n_attack = int(attack_magnitude / 10)
    for i in range(n_attack):
        state_value = honest_center + np.random.randn(3) * attack_magnitude
        state = protocol.propose_state(state_value, adaptive_difficulty=False)
        if state:
            protocol.current_ensemble.add_state(state)
    
    # Run consensus WITHOUT annealing (just use mean)
    import time
    start = time.time()
    
    # Filter Byzantine
    filtered = protocol.current_ensemble.filter_byzantine_states(threshold=3.0)
    
    # Simple mean (no annealing)
    consensus_state = filtered.compute_mean_state()
    final_variance = filtered.compute_variance()
    
    elapsed = time.time() - start
    
    return AblationResult(
        variant="No Annealing",
        attack_magnitude=attack_magnitude,
        final_error=final_variance,
        converged=(final_variance < 0.05),
        time_taken=elapsed
    )


def run_no_filtering(attack_magnitude: float, n_nodes: int = 10) -> AblationResult:
    """Run without Byzantine filtering."""
    protocol = ThermodynamicTruth(
        node_id="ablation_no_filter",
        pow_difficulty=2.0,
        use_parallel_tempering=True,
        n_replicas=4
    )
    
    # Honest nodes
    honest_center = np.array([1.0, 2.0, 3.0])
    for i in range(n_nodes):
        state_value = honest_center + np.random.randn(3) * 0.05
        state = protocol.propose_state(state_value, adaptive_difficulty=False)
        if state:
            protocol.current_ensemble.add_state(state)
    
    # Attack
    n_attack = int(attack_magnitude / 10)
    for i in range(n_attack):
        state_value = honest_center + np.random.randn(3) * attack_magnitude
        state = protocol.propose_state(state_value, adaptive_difficulty=False)
        if state:
            protocol.current_ensemble.add_state(state)
    
    # Run consensus WITHOUT filtering
    import time
    start = time.time()
    consensus_state, metrics = protocol.run_consensus_round(
        max_annealing_steps=100,
        filter_byzantine=False  # No filtering
    )
    elapsed = time.time() - start
    
    return AblationResult(
        variant="No Filtering",
        attack_magnitude=attack_magnitude,
        final_error=metrics['final_variance'],
        converged=metrics['converged'],
        time_taken=elapsed
    )


def run_ablation():
    """Run complete ablation study."""
    variants = [
        ("Full Protocol", run_full_protocol),
        ("No Energy", run_no_energy),
        ("No Annealing", run_no_annealing),
        ("No Filtering", run_no_filtering),
    ]
    
    attack_magnitudes = [1.0, 5.0, 10.0, 20.0, 50.0]
    results = []
    
    print("="*80)
    print("REAL Ablation Study: Component Contribution Analysis")
    print("="*80)
    print(f"{'Variant':<18} | {'Attack':<10} | {'Error':<12} | {'Converged':<10} | {'Time (ms)'}")
    print("-"*80)
    
    for variant_name, variant_func in variants:
        for mag in attack_magnitudes:
            print(f"Testing {variant_name} @ attack={mag}...", end=' ', flush=True)
            
            result = variant_func(mag)
            results.append(result)
            
            status = "✓" if result.converged else "✗"
            print(f"\r{variant_name:<18} | {mag:<10.1f} | {result.final_error:<12.6f} | {status:<10} | {result.time_taken*1000:.2f}")
    
    print("="*80)
    return results


def analyze_results(results: List[AblationResult]):
    """Analyze ablation results."""
    print("\nComponent Impact Analysis:")
    print("-"*80)
    
    # Group by variant
    variants = {}
    for r in results:
        if r.variant not in variants:
            variants[r.variant] = []
        variants[r.variant].append(r)
    
    # Compare to full protocol
    full_errors = [r.final_error for r in variants["Full Protocol"]]
    full_avg = np.mean(full_errors)
    
    print(f"Full Protocol avg error: {full_avg:.6f}")
    
    for variant_name, variant_results in variants.items():
        if variant_name == "Full Protocol":
            continue
        
        errors = [r.final_error for r in variant_results]
        avg_error = np.mean(errors)
        increase = (avg_error / full_avg - 1) * 100
        
        print(f"{variant_name}: {avg_error:.6f} (↑{increase:.1f}% vs Full)")
    
    print("-"*80)


def plot_ablation(results: List[AblationResult]):
    """Generate ablation plots."""
    variants = sorted(list(set(r.variant for r in results)))
    magnitudes = sorted(list(set(r.attack_magnitude for r in results)))
    
    plt.figure(figsize=(12, 7))
    
    markers = {'Full Protocol': 'o', 'No Energy': 'x', 'No Annealing': 's', 'No Filtering': '^'}
    colors = {'Full Protocol': 'g', 'No Energy': 'r', 'No Annealing': 'b', 'No Filtering': 'orange'}
    
    for variant in variants:
        variant_results = [r for r in results if r.variant == variant]
        mags = [r.attack_magnitude for r in variant_results]
        errors = [r.final_error for r in variant_results]
        
        plt.plot(mags, errors, marker=markers.get(variant, 'o'), 
                color=colors.get(variant, 'gray'), label=variant, 
                linewidth=2, markersize=8)
    
    plt.xlabel('Attack Magnitude (Deviation)', fontsize=12)
    plt.ylabel('Consensus Error (Variance)', fontsize=12)
    plt.title('Ablation Study: Component Contribution (Real Measurements)', 
             fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.yscale('log')
    
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/ablation_study_real.png', dpi=150)
    print("\n✓ Saved plot: results/ablation_study_real.png")


def save_results(results: List[AblationResult]):
    """Save results to JSON."""
    data = [vars(r) for r in results]
    
    os.makedirs('results', exist_ok=True)
    with open('results/ablation_data_real.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✓ Saved data: results/ablation_data_real.json")


if __name__ == "__main__":
    print("\nRunning REAL ablation study...")
    print("This tests actual protocol components, not mock simulations.\n")
    
    results = run_ablation()
    analyze_results(results)
    plot_ablation(results)
    save_results(results)
    
    print("\n" + "="*80)
    print("Ablation Study Complete!")
    print("="*80)
    print("\nThese are REAL measurements showing the impact of removing components.")
    print("="*80 + "\n")
