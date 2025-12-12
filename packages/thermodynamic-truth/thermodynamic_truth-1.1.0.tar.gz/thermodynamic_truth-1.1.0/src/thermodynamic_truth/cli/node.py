#!/usr/bin/env python3
"""
ThermoTruth Node CLI

Command-line interface for running a ThermoTruth consensus node.
"""

import argparse
import logging
import signal
import sys
import time
import numpy as np
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, "/home/ubuntu/thermo-truth-proto/src")

from thermodynamic_truth.core.protocol import ThermodynamicTruth
from thermodynamic_truth.network.server import ThermoNodeServer
from thermodynamic_truth.network.client import PeerManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ThermoTruthNode:
    """
    Complete ThermoTruth node with networking and consensus.
    """

    def __init__(
        self,
        node_id: str,
        port: int,
        peers: List[str],
        pow_difficulty: float = 2.0,
        is_genesis: bool = False,
    ):
        """
        Initialize node.

        Args:
            node_id: Unique node identifier
            port: Port to listen on
            peers: List of peer addresses (host:port)
            pow_difficulty: Proof-of-Work difficulty
            is_genesis: Whether this is the genesis node
        """
        self.node_id = node_id
        self.port = port
        self.is_genesis = is_genesis
        self.running = False

        # Initialize protocol
        self.protocol = ThermodynamicTruth(
            node_id=node_id,
            pow_difficulty=pow_difficulty,
            use_parallel_tempering=True,
            n_replicas=4,
        )

        # Initialize network
        self.server = ThermoNodeServer(self.protocol, port=port)
        self.peer_manager = PeerManager()

        # Add peers
        for peer_address in peers:
            self.peer_manager.add_peer(peer_address)

        logger.info(f"Initialized node {node_id} on port {port}")
        logger.info(f"Connected to {len(peers)} peers")

    def start(self):
        """Start the node."""
        # Start gRPC server
        self.server.start()

        # Create genesis if needed
        if self.is_genesis:
            logger.info("Creating genesis state...")
            genesis_value = np.array([0.0, 0.0, 0.0])  # Initial state
            genesis = self.protocol.create_genesis(genesis_value)

            # Broadcast genesis to peers
            if self.peer_manager.peers:
                logger.info("Broadcasting genesis to peers...")
                self.peer_manager.broadcast_state(genesis)

        self.running = True
        logger.info(f"Node {self.node_id} started successfully")

    def stop(self):
        """Stop the node."""
        self.running = False
        self.server.stop()
        self.peer_manager.close_all()
        logger.info(f"Node {self.node_id} stopped")

    def run_consensus_loop(self, interval: float = 10.0):
        """
        Run the main consensus loop.

        Args:
            interval: Time between consensus rounds (seconds)
        """
        round_count = 0

        while self.running:
            try:
                round_count += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"Starting consensus round {round_count}")
                logger.info(f"{'='*60}")

                # Propose a new state (simulate with random data for now)
                state_value = np.random.randn(3) * 0.1  # Small random perturbation
                state = self.protocol.propose_state(state_value, adaptive_difficulty=True)

                if state:
                    # Broadcast state to peers
                    logger.info("Broadcasting state to peers...")
                    results = self.peer_manager.broadcast_state(state)
                    accepted_count = sum(1 for accepted in results.values() if accepted)
                    logger.info(f"State accepted by {accepted_count}/{len(results)} peers")

                # Wait for states from peers
                logger.info(f"Waiting {interval}s for peer states...")
                time.sleep(interval)

                # Run consensus
                if len(self.protocol.current_ensemble.states) > 0:
                    logger.info("Running consensus algorithm...")
                    consensus_state, metrics = self.protocol.run_consensus_round(
                        max_annealing_steps=100, filter_byzantine=True
                    )

                    # Log metrics
                    logger.info(f"\nConsensus Metrics:")
                    logger.info(f"  States: {metrics['n_states']}")
                    logger.info(f"  Filtered: {metrics['n_filtered']}")
                    logger.info(f"  Variance: {metrics['final_variance']:.6f}")
                    logger.info(f"  Temperature: {metrics['final_temperature']:.6f}°C")
                    logger.info(f"  Entropy: {metrics['final_entropy']:.6f}")
                    logger.info(f"  Converged: {metrics['converged']}")
                    logger.info(f"  Time: {metrics['total_time']:.3f}s")

                    # Broadcast consensus if achieved
                    if metrics["converged"]:
                        logger.info("✓ Consensus achieved! Broadcasting...")
                        self.peer_manager.broadcast_consensus(
                            round_number=metrics["round"],
                            consensus_state=consensus_state,
                            final_variance=metrics["final_variance"],
                            final_temperature=metrics["final_temperature"],
                            final_entropy=metrics["final_entropy"],
                            announcer_id=self.node_id,
                        )

                    # Reset ensemble for next round
                    self.protocol.reset_ensemble()
                else:
                    logger.warning("No states in ensemble, skipping consensus")

            except KeyboardInterrupt:
                logger.info("Received interrupt signal")
                break
            except Exception as e:
                logger.error(f"Error in consensus loop: {e}", exc_info=True)
                time.sleep(1)

        logger.info(f"Consensus loop terminated after {round_count} rounds")

    def print_status(self):
        """Print node status."""
        status = self.protocol.get_status()
        metrics = self.protocol.get_consensus_metrics()

        print(f"\n{'='*60}")
        print(f"Node Status: {self.node_id}")
        print(f"{'='*60}")
        print(f"Round: {status['round']}")
        print(f"Ensemble Size: {status['ensemble_size']}")
        print(f"Temperature: {status['current_temperature']:.6f}°C")
        print(f"Entropy: {status['current_entropy']:.6f}")
        print(f"Variance: {status['current_variance']:.6f}")
        print(f"Energy Budget: {status['energy_budget_remaining']:.2f}J")
        print(f"Total Rounds: {status['total_rounds']}")

        if metrics:
            print(f"\nAggregate Metrics:")
            print(f"  Avg Variance: {metrics['avg_variance']:.6f}")
            print(f"  Avg Temperature: {metrics['avg_temperature']:.6f}°C")
            print(f"  Avg Entropy: {metrics['avg_entropy']:.6f}")
            print(f"  Convergence Rate: {metrics['convergence_rate']:.2%}")

        print(f"{'='*60}\n")


def main():
    """Main entry point for node CLI."""
    parser = argparse.ArgumentParser(
        description="ThermoTruth Consensus Node",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start genesis node
  python -m thermodynamic_truth.cli.node --id node0 --port 50051 --genesis
  
  # Start peer node
  python -m thermodynamic_truth.cli.node --id node1 --port 50052 --peer localhost:50051
  
  # Start with multiple peers
  python -m thermodynamic_truth.cli.node --id node2 --port 50053 \\
      --peer localhost:50051 --peer localhost:50052
        """,
    )

    parser.add_argument("--id", required=True, help="Unique node identifier")
    parser.add_argument("--port", type=int, required=True, help="Port to listen on")
    parser.add_argument(
        "--peer",
        action="append",
        default=[],
        help="Peer address (host:port), can be specified multiple times",
    )
    parser.add_argument(
        "--difficulty", type=float, default=2.0, help="Proof-of-Work difficulty (default: 2.0)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=10.0,
        help="Consensus round interval in seconds (default: 10.0)",
    )
    parser.add_argument("--genesis", action="store_true", help="Start as genesis node")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create and start node
    node = ThermoTruthNode(
        node_id=args.id,
        port=args.port,
        peers=args.peer,
        pow_difficulty=args.difficulty,
        is_genesis=args.genesis,
    )

    # Setup signal handlers
    def signal_handler(sig, frame):
        logger.info("Shutting down node...")
        node.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start node
    node.start()

    # Print initial status
    node.print_status()

    # Run consensus loop
    try:
        node.run_consensus_loop(interval=args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()


if __name__ == "__main__":
    main()
