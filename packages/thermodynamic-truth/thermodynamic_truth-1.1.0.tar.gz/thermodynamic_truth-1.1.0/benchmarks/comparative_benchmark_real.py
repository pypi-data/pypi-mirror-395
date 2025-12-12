"""
Real Comparative Benchmark: Thermodynamic Truth Performance

This benchmark runs the ACTUAL ThermoTruth protocol and measures real performance.
Unlike the original mock benchmark, this provides verifiable experimental results.
"""

import sys
sys.path.insert(0, '/home/ubuntu/thermo-truth-proto/src')

import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import json
import os
from dataclasses import dataclass
from typing import List, Dict

from thermodynamic_truth.core.protocol import ThermodynamicTruth


@dataclass
class BenchmarkResult:
    protocol: str
    n_nodes: int
    latency_ms: float
    throughput_tps: float
    consensus_error: float
    converged: bool


def run_thermodynamic_truth_benchmark(n_nodes: int, n_rounds: int = 5) -> BenchmarkResult:
    """
    Run actual ThermoTruth protocol and measure performance.
    
    Args:
        n_nodes: Number of simulated nodes
        n_rounds: Number of consensus rounds to average
    
    Returns:
        BenchmarkResult with measured metrics
    """
    protocol = ThermodynamicTruth(
        node_id=f"bench_node_{n_nodes}",
        pow_difficulty=1.0,  # Reduced for benchmarking
        use_parallel_tempering=True,
        n_replicas=4
    )
    
    latencies = []
    variances = []
    converged_count = 0
    
    for round_num in range(n_rounds):
        # Simulate states from n nodes
        for i in range(n_nodes):
            state_value = np.random.randn(3) * 0.1
            state = protocol.propose_state(state_value, adaptive_difficulty=False)
            if state:
                protocol.current_ensemble.add_state(state)
        
        # Measure consensus time
        start_time = time.time()
        consensus_state, metrics = protocol.run_consensus_round(
            max_annealing_steps=100,
            filter_byzantine=False
        )
        latency = time.time() - start_time
        
        latencies.append(latency)
        variances.append(metrics['final_variance'])
        if metrics['converged']:
            converged_count += 1
        
        protocol.reset_ensemble()
    
    # Compute metrics
    avg_latency_ms = np.mean(latencies) * 1000
    avg_variance = np.mean(variances)
    
    # Throughput: transactions per second
    # Assume each node proposes 1 transaction per round
    tps = n_nodes / np.mean(latencies)
    
    return BenchmarkResult(
        protocol="ThermoTruth",
        n_nodes=n_nodes,
        latency_ms=avg_latency_ms,
        throughput_tps=tps,
        consensus_error=avg_variance,
        converged=(converged_count == n_rounds)
    )


def run_benchmark():
    """Run comprehensive benchmark across different network sizes."""
    results = []
    node_counts = [4, 9, 16, 25, 36, 49, 64, 100]
    
    print("="*70)
    print("REAL ThermoTruth Performance Benchmark")
    print("="*70)
    print(f"{'Nodes':<8} | {'Latency (ms)':<15} | {'Throughput (TPS)':<18} | {'Variance':<12} | {'Status'}")
    print("-"*70)
    
    for n in node_counts:
        print(f"Testing {n} nodes...", end=' ', flush=True)
        
        result = run_thermodynamic_truth_benchmark(n, n_rounds=5)
        results.append(result)
        
        status = "✓ Converged" if result.converged else "✗ No consensus"
        print(f"\r{n:<8} | {result.latency_ms:<15.2f} | {result.throughput_tps:<18.0f} | {result.consensus_error:<12.6f} | {status}")
    
    print("="*70)
    return results


def analyze_scaling(results: List[BenchmarkResult]):
    """Analyze scaling behavior."""
    print("\nScaling Analysis:")
    print("-"*70)
    
    nodes = [r.n_nodes for r in results]
    latencies = [r.latency_ms for r in results]
    
    # Fit linear model: latency = a * n + b
    A = np.vstack([nodes, np.ones(len(nodes))]).T
    a, b = np.linalg.lstsq(A, latencies, rcond=None)[0]
    
    print(f"Latency Model: L(n) = {a:.4f}*n + {b:.4f}")
    print(f"Scaling: O(n) with coefficient {a:.4f} ms/node")
    
    # Compute R²
    ss_res = np.sum((np.array(latencies) - (a * np.array(nodes) + b)) ** 2)
    ss_tot = np.sum((np.array(latencies) - np.mean(latencies)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print(f"R² = {r_squared:.4f} (goodness of fit)")
    
    # Check if sub-second at 100 nodes
    latency_100 = results[-1].latency_ms if results[-1].n_nodes == 100 else None
    if latency_100:
        if latency_100 < 1000:
            print(f"✓ Sub-second finality at 100 nodes: {latency_100:.2f}ms")
        else:
            print(f"✗ Exceeds 1s at 100 nodes: {latency_100:.2f}ms")
    
    print("-"*70)


def plot_results(results: List[BenchmarkResult]):
    """Generate performance plots."""
    nodes = [r.n_nodes for r in results]
    latencies = [r.latency_ms for r in results]
    throughputs = [r.throughput_tps for r in results]
    variances = [r.consensus_error for r in results]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Latency vs Nodes
    axes[0, 0].plot(nodes, latencies, 'g-o', linewidth=2, markersize=8)
    axes[0, 0].set_xlabel('Number of Nodes', fontsize=12)
    axes[0, 0].set_ylabel('Latency (ms)', fontsize=12)
    axes[0, 0].set_title('Consensus Latency (Real Measurements)', fontsize=14, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Add linear fit
    z = np.polyfit(nodes, latencies, 1)
    p = np.poly1d(z)
    axes[0, 0].plot(nodes, p(nodes), "r--", alpha=0.5, label=f'Linear fit: {z[0]:.3f}n + {z[1]:.3f}')
    axes[0, 0].legend()
    
    # Throughput vs Nodes
    axes[0, 1].plot(nodes, throughputs, 'b-s', linewidth=2, markersize=8)
    axes[0, 1].set_xlabel('Number of Nodes', fontsize=12)
    axes[0, 1].set_ylabel('Throughput (TPS)', fontsize=12)
    axes[0, 1].set_title('Transaction Throughput', fontsize=14, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Consensus Error (Variance)
    axes[1, 0].plot(nodes, variances, 'r-^', linewidth=2, markersize=8)
    axes[1, 0].set_xlabel('Number of Nodes', fontsize=12)
    axes[1, 0].set_ylabel('Consensus Error (Variance)', fontsize=12)
    axes[1, 0].set_title('Consensus Accuracy', fontsize=14, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=0.05, color='orange', linestyle='--', label='Target threshold (0.05)')
    axes[1, 0].legend()
    
    # Scaling Efficiency
    efficiency = [throughputs[0] * nodes[0] / (t * n) for t, n in zip(throughputs, nodes)]
    axes[1, 1].plot(nodes, efficiency, 'm-d', linewidth=2, markersize=8)
    axes[1, 1].set_xlabel('Number of Nodes', fontsize=12)
    axes[1, 1].set_ylabel('Scaling Efficiency', fontsize=12)
    axes[1, 1].set_title('Parallel Efficiency', fontsize=14, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axhline(y=1.0, color='green', linestyle='--', label='Ideal (1.0)')
    axes[1, 1].legend()
    
    plt.tight_layout()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/thermodynamic_truth_real_benchmark.png', dpi=150)
    print("\n✓ Saved plot: results/thermodynamic_truth_real_benchmark.png")


def save_results(results: List[BenchmarkResult]):
    """Save results to JSON."""
    data = [vars(r) for r in results]
    
    os.makedirs('results', exist_ok=True)
    with open('results/real_benchmark_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✓ Saved data: results/real_benchmark_data.json")


if __name__ == "__main__":
    print("\nRunning REAL ThermoTruth benchmarks...")
    print("This measures actual protocol performance, not mock simulations.\n")
    
    results = run_benchmark()
    analyze_scaling(results)
    plot_results(results)
    save_results(results)
    
    print("\n" + "="*70)
    print("Benchmark Complete!")
    print("="*70)
    print("\nKey Findings:")
    print(f"  • Tested network sizes: 4 to 100 nodes")
    print(f"  • Latency at 100 nodes: {results[-1].latency_ms:.2f}ms")
    print(f"  • Throughput at 100 nodes: {results[-1].throughput_tps:.0f} TPS")
    print(f"  • Average consensus error: {np.mean([r.consensus_error for r in results]):.6f}")
    print(f"  • Convergence rate: {sum(1 for r in results if r.converged)}/{len(results)}")
    print("\nThese are REAL measurements from the actual protocol implementation.")
    print("="*70 + "\n")
