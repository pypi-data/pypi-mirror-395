"""
Byzantine Threshold Test - REAL Protocol Execution
Tests ThermoTruth's resilience at 30%, 33%, 40%, 50% Byzantine ratios
"""

import sys
sys.path.insert(0, '/home/ubuntu/thermo-truth-proto/src')

import numpy as np
import time
import json
from thermodynamic_truth.core.protocol import ThermodynamicTruth
from thermodynamic_truth.core.pow import ProofOfWork
from thermodynamic_truth.core.state import ConsensusState

def run_byzantine_test(n_nodes=20, byz_fraction=0.33, n_rounds=5):
    """
    Run real Byzantine threshold test.
    
    Args:
        n_nodes: Total number of nodes
        byz_fraction: Fraction of Byzantine nodes (0.0-1.0)
        n_rounds: Number of consensus rounds to test
    
    Returns:
        dict with consensus errors, convergence status, timing
    """
    n_byzantine = int(n_nodes * byz_fraction)
    n_honest = n_nodes - n_byzantine
    
    print(f"\n{'='*60}")
    print(f"Byzantine Test: {n_nodes} nodes, {byz_fraction*100:.0f}% Byzantine ({n_byzantine} malicious)")
    print(f"{'='*60}")
    
    results = {
        'n_nodes': n_nodes,
        'byz_fraction': byz_fraction,
        'n_byzantine': n_byzantine,
        'n_honest': n_honest,
        'rounds': [],
        'avg_error': 0.0,
        'avg_time_ms': 0.0,
        'converged_count': 0
    }
    
    # True consensus value (what honest nodes agree on)
    true_value = 42.0
    
    for round_num in range(n_rounds):
        protocol = ThermodynamicTruth(node_id=f'validator_{round_num}')
        
        # Honest nodes propose near true value
        for i in range(n_honest):
            state_vec = np.array([true_value + np.random.randn() * 0.05])  # Small noise
            state = protocol.propose_state(state_vec)
            if state:
                protocol.receive_state(state)  # Add to ensemble
        
        # Byzantine nodes propose random garbage
        for i in range(n_byzantine):
            # Byzantine attack: random values far from consensus
            attack_value = true_value + np.random.randn() * 10.0  # Large deviation
            state_vec = np.array([attack_value])
            state = protocol.propose_state(state_vec)
            if state:
                protocol.receive_state(state)  # Add to ensemble
        
        # Run consensus
        start = time.time()
        consensus_vec, metrics = protocol.run_consensus_round()
        elapsed_ms = (time.time() - start) * 1000
        
        # Calculate error from true value
        consensus_value = consensus_vec[0] if len(consensus_vec) > 0 else 0.0
        error = abs(consensus_value - true_value)
        converged = metrics.get('converged', False)
        
        round_result = {
            'round': int(round_num + 1),
            'consensus_value': float(consensus_value),
            'error': float(error),
            'variance': float(metrics.get('final_variance', 0.0)),
            'temperature': float(metrics.get('final_temperature', 0.0)),
            'entropy': float(metrics.get('final_entropy', 0.0)),
            'n_states': int(metrics.get('n_states', 0)),
            'n_filtered': int(metrics.get('n_filtered', 0)),
            'time_ms': float(elapsed_ms),
            'converged': bool(converged)
        }
        
        results['rounds'].append(round_result)
        
        print(f"Round {round_num+1}: Error={error:.4f}, Var={round_result['variance']:.4f}, "
              f"T={round_result['temperature']:.6f}, Time={elapsed_ms:.2f}ms, "
              f"States={round_result['n_states']}/{round_result['n_states']+round_result['n_filtered']}, "
              f"Converged={'✓' if converged else '✗'}")
    
    # Aggregate results
    results['avg_error'] = np.mean([r['error'] for r in results['rounds']])
    results['avg_variance'] = np.mean([r['variance'] for r in results['rounds']])
    results['avg_time_ms'] = np.mean([r['time_ms'] for r in results['rounds']])
    results['converged_count'] = sum(1 for r in results['rounds'] if r['converged'])
    results['convergence_rate'] = results['converged_count'] / n_rounds
    
    print(f"\nAggregate Results:")
    print(f"  Avg Error: {results['avg_error']:.4f}")
    print(f"  Avg Variance: {results['avg_variance']:.4f}")
    print(f"  Avg Time: {results['avg_time_ms']:.2f}ms")
    print(f"  Convergence Rate: {results['convergence_rate']*100:.0f}%")
    
    return results

def main():
    """Run Byzantine threshold tests at multiple fractions"""
    
    print("\n" + "="*80)
    print("ThermoTruth Byzantine Threshold Test - REAL PROTOCOL EXECUTION")
    print("="*80)
    
    test_fractions = [0.30, 0.33, 0.40, 0.50]
    all_results = []
    
    for frac in test_fractions:
        result = run_byzantine_test(n_nodes=20, byz_fraction=frac, n_rounds=5)
        all_results.append(result)
        time.sleep(0.5)  # Brief pause between tests
    
    # Save results
    output_file = '/home/ubuntu/thermo-truth-proto/validation/byzantine_results.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*80}")
    print("SUMMARY TABLE")
    print(f"{'='*80}")
    print(f"{'Byz %':<10} {'Avg Error':<15} {'Avg Var':<15} {'Conv Rate':<15} {'Status':<10}")
    print(f"{'-'*80}")
    
    for result in all_results:
        byz_pct = result['byz_fraction'] * 100
        status = "✓ HELD" if result['avg_error'] < 0.5 else "✗ BROKE"
        print(f"{byz_pct:<10.0f} {result['avg_error']:<15.4f} {result['avg_variance']:<15.4f} "
              f"{result['convergence_rate']*100:<15.0f}% {status:<10}")
    
    print(f"\nResults saved to: {output_file}")
    print("\n✦ VALIDATION COMPLETE ✦")

if __name__ == '__main__':
    main()
