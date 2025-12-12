#!/usr/bin/env python3
"""
ThermoTruth Benchmark CLI

Tool for running real performance benchmarks on the protocol.
"""

import argparse
import sys
import time
import numpy as np
import json
from typing import List, Dict

sys.path.insert(0, "/home/ubuntu/thermo-truth-proto/src")

from thermodynamic_truth.core.protocol import ThermodynamicTruth
from thermodynamic_truth.core.state import ConsensusState


def benchmark_latency(n_nodes: int, n_rounds: int = 10) -> Dict:
    """
    Benchmark consensus latency vs number of nodes.

    Args:
        n_nodes: Number of simulated nodes
        n_rounds: Number of consensus rounds

    Returns:
        Benchmark results
    """
    print(f"Running latency benchmark: {n_nodes} nodes, {n_rounds} rounds")

    # Create protocol instance
    protocol = ThermodynamicTruth(
        node_id="benchmark_node",
        pow_difficulty=1.0,  # Lower difficulty for faster benchmarking
        use_parallel_tempering=True,
    )

    latencies = []
    variances = []

    for round_num in range(n_rounds):
        # Simulate states from n nodes
        for i in range(n_nodes):
            state_value = np.random.randn(3) * 0.1
            state = protocol.propose_state(state_value, adaptive_difficulty=False)
            if state:
                protocol.current_ensemble.add_state(state)

        # Run consensus and measure time
        start_time = time.time()
        consensus_state, metrics = protocol.run_consensus_round(
            max_annealing_steps=100, filter_byzantine=False
        )
        latency = time.time() - start_time

        latencies.append(latency)
        variances.append(metrics["final_variance"])

        protocol.reset_ensemble()

        print(
            f"  Round {round_num+1}/{n_rounds}: {latency:.3f}s, variance={metrics['final_variance']:.6f}"
        )

    return {
        "n_nodes": n_nodes,
        "n_rounds": n_rounds,
        "avg_latency": np.mean(latencies),
        "std_latency": np.std(latencies),
        "min_latency": np.min(latencies),
        "max_latency": np.max(latencies),
        "avg_variance": np.mean(variances),
        "latencies": latencies,
        "variances": variances,
    }


def benchmark_throughput(duration: int = 60) -> Dict:
    """
    Benchmark transaction throughput.

    Args:
        duration: Benchmark duration in seconds

    Returns:
        Benchmark results
    """
    print(f"Running throughput benchmark: {duration}s duration")

    protocol = ThermodynamicTruth(
        node_id="benchmark_node",
        pow_difficulty=1.0,
        use_parallel_tempering=False,  # Faster for throughput
    )

    start_time = time.time()
    transactions = 0
    rounds = 0

    while time.time() - start_time < duration:
        # Propose states (simulate transactions)
        for i in range(10):  # 10 nodes
            state_value = np.random.randn(3) * 0.1
            state = protocol.propose_state(state_value, adaptive_difficulty=False)
            if state:
                protocol.current_ensemble.add_state(state)
                transactions += 1

        # Run consensus
        consensus_state, metrics = protocol.run_consensus_round(
            max_annealing_steps=50, filter_byzantine=False  # Fewer steps for throughput
        )
        rounds += 1

        protocol.reset_ensemble()

    elapsed = time.time() - start_time
    tps = transactions / elapsed

    print(f"  Transactions: {transactions}")
    print(f"  Rounds: {rounds}")
    print(f"  TPS: {tps:.2f}")

    return {"duration": elapsed, "transactions": transactions, "rounds": rounds, "tps": tps}


def benchmark_byzantine_resilience(
    n_nodes: int, byzantine_fraction: float, n_rounds: int = 10
) -> Dict:
    """
    Benchmark resilience under Byzantine attacks.

    Args:
        n_nodes: Number of simulated nodes
        byzantine_fraction: Fraction of Byzantine nodes (0.0 to 1.0)
        n_rounds: Number of consensus rounds

    Returns:
        Benchmark results
    """
    print(
        f"Running Byzantine resilience benchmark: {n_nodes} nodes, {byzantine_fraction:.0%} Byzantine"
    )

    protocol = ThermodynamicTruth(
        node_id="benchmark_node", pow_difficulty=2.0, use_parallel_tempering=True
    )

    n_byzantine = int(n_nodes * byzantine_fraction)
    n_honest = n_nodes - n_byzantine

    variances = []
    filtered_counts = []

    for round_num in range(n_rounds):
        # Honest nodes propose near-consensus states
        honest_center = np.array([1.0, 2.0, 3.0])
        for i in range(n_honest):
            state_value = honest_center + np.random.randn(3) * 0.05
            state = protocol.propose_state(state_value, adaptive_difficulty=False)
            if state:
                protocol.current_ensemble.add_state(state)

        # Byzantine nodes propose far-off states
        for i in range(n_byzantine):
            state_value = np.random.randn(3) * 10.0  # Large deviation
            state = protocol.propose_state(state_value, adaptive_difficulty=False)
            if state:
                protocol.current_ensemble.add_state(state)

        # Run consensus with Byzantine filtering
        consensus_state, metrics = protocol.run_consensus_round(
            max_annealing_steps=100, filter_byzantine=True
        )

        variances.append(metrics["final_variance"])
        filtered_counts.append(metrics["n_filtered"])

        protocol.reset_ensemble()

        print(
            f"  Round {round_num+1}/{n_rounds}: variance={metrics['final_variance']:.6f}, "
            f"filtered={metrics['n_filtered']}/{n_nodes}"
        )

    return {
        "n_nodes": n_nodes,
        "n_byzantine": n_byzantine,
        "byzantine_fraction": byzantine_fraction,
        "n_rounds": n_rounds,
        "avg_variance": np.mean(variances),
        "avg_filtered": np.mean(filtered_counts),
        "variances": variances,
        "filtered_counts": filtered_counts,
    }


def benchmark_scaling(max_nodes: int = 100, step: int = 10) -> List[Dict]:
    """
    Benchmark scalability across different network sizes.

    Args:
        max_nodes: Maximum number of nodes to test
        step: Step size for node count

    Returns:
        List of benchmark results
    """
    print(f"Running scaling benchmark: up to {max_nodes} nodes")

    results = []

    for n_nodes in range(step, max_nodes + 1, step):
        result = benchmark_latency(n_nodes, n_rounds=5)
        results.append(result)
        print(f"✓ {n_nodes} nodes: {result['avg_latency']:.3f}s avg latency\n")

    return results


def main():
    """Main entry point for benchmark CLI."""
    parser = argparse.ArgumentParser(
        description="ThermoTruth Performance Benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="benchmark", help="Benchmark to run")

    # Latency benchmark
    latency_parser = subparsers.add_parser("latency", help="Benchmark consensus latency")
    latency_parser.add_argument("--nodes", type=int, default=10, help="Number of nodes")
    latency_parser.add_argument("--rounds", type=int, default=10, help="Number of rounds")

    # Throughput benchmark
    throughput_parser = subparsers.add_parser("throughput", help="Benchmark transaction throughput")
    throughput_parser.add_argument("--duration", type=int, default=60, help="Duration in seconds")

    # Byzantine resilience benchmark
    byzantine_parser = subparsers.add_parser("byzantine", help="Benchmark Byzantine resilience")
    byzantine_parser.add_argument("--nodes", type=int, default=10, help="Number of nodes")
    byzantine_parser.add_argument("--fraction", type=float, default=0.33, help="Byzantine fraction")
    byzantine_parser.add_argument("--rounds", type=int, default=10, help="Number of rounds")

    # Scaling benchmark
    scaling_parser = subparsers.add_parser("scaling", help="Benchmark scalability")
    scaling_parser.add_argument("--max-nodes", type=int, default=100, help="Maximum nodes")
    scaling_parser.add_argument("--step", type=int, default=10, help="Step size")

    # Output options
    parser.add_argument("--output", help="Output file for results (JSON)")

    args = parser.parse_args()

    if not args.benchmark:
        parser.print_help()
        sys.exit(1)

    # Run benchmark
    if args.benchmark == "latency":
        results = benchmark_latency(args.nodes, args.rounds)
    elif args.benchmark == "throughput":
        results = benchmark_throughput(args.duration)
    elif args.benchmark == "byzantine":
        results = benchmark_byzantine_resilience(args.nodes, args.fraction, args.rounds)
    elif args.benchmark == "scaling":
        results = benchmark_scaling(args.max_nodes, args.step)

    # Print summary
    print(f"\n{'='*60}")
    print("Benchmark Results")
    print(f"{'='*60}")
    print(json.dumps(results, indent=2, default=str))

    # Save to file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n✓ Results saved to {args.output}")


if __name__ == "__main__":
    main()
