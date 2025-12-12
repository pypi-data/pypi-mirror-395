#!/usr/bin/env python3
"""
ThermoTruth Client CLI

Command-line tool for interacting with ThermoTruth nodes.
"""

import argparse
import sys
import json
import numpy as np

sys.path.insert(0, "/home/ubuntu/thermo-truth-proto/src")

from thermodynamic_truth.network.client import ThermoNodeClient


def cmd_ping(args):
    """Ping a node."""
    client = ThermoNodeClient(args.node)
    status = client.ping(args.sender_id or "client")

    if status:
        print(f"✓ Node {status['responder_id']} is alive")
        print(f"  Round: {status['current_round']}")
        print(f"  Ensemble Size: {status['ensemble_size']}")
        print(f"  Temperature: {status['temperature']:.6f}°C")
    else:
        print(f"✗ Failed to ping {args.node}")
        sys.exit(1)


def cmd_status(args):
    """Get node status."""
    client = ThermoNodeClient(args.node)
    status = client.ping(args.sender_id or "client")

    if status:
        print(json.dumps(status, indent=2))
    else:
        print(f"✗ Failed to get status from {args.node}")
        sys.exit(1)


def cmd_request_states(args):
    """Request states from a node."""
    client = ThermoNodeClient(args.node)
    states = client.request_states(
        requester_id=args.sender_id or "client",
        round_number=args.round or 0,
        max_states=args.max_states or 100,
    )

    print(f"Received {len(states)} states from {args.node}")

    if args.verbose:
        for i, state in enumerate(states):
            print(f"\nState {i+1}:")
            print(f"  Proposer: {state.proposer_id}")
            print(f"  Energy: {state.energy:.6f}J")
            print(f"  Difficulty: {state.difficulty}")
            print(f"  Vector: {state.state_vector}")


def cmd_sync(args):
    """Synchronize with a node."""
    client = ThermoNodeClient(args.node)
    current_round, history, pending = client.sync_state(
        requester_id=args.sender_id or "client", last_known_round=args.last_round or 0
    )

    print(f"Synchronized with {args.node}")
    print(f"  Current Round: {current_round}")
    print(f"  History Items: {len(history)}")
    print(f"  Pending States: {len(pending)}")

    if args.verbose and history:
        print("\nConsensus History:")
        for item in history:
            print(f"  Round {item['round']}:")
            print(f"    Variance: {item['final_variance']:.6f}")
            print(f"    Temperature: {item['final_temperature']:.6f}°C")
            print(f"    Entropy: {item['final_entropy']:.6f}")


def main():
    """Main entry point for client CLI."""
    parser = argparse.ArgumentParser(
        description="ThermoTruth Client Tool", formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Ping command
    ping_parser = subparsers.add_parser("ping", help="Ping a node")
    ping_parser.add_argument("node", help="Node address (host:port)")
    ping_parser.add_argument("--sender-id", help="Sender identifier")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get node status")
    status_parser.add_argument("node", help="Node address (host:port)")
    status_parser.add_argument("--sender-id", help="Sender identifier")

    # Request states command
    request_parser = subparsers.add_parser("request-states", help="Request states from node")
    request_parser.add_argument("node", help="Node address (host:port)")
    request_parser.add_argument("--sender-id", help="Sender identifier")
    request_parser.add_argument("--round", type=int, help="Round number")
    request_parser.add_argument("--max-states", type=int, help="Maximum states to request")
    request_parser.add_argument("--verbose", action="store_true", help="Verbose output")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Synchronize with node")
    sync_parser.add_argument("node", help="Node address (host:port)")
    sync_parser.add_argument("--sender-id", help="Sender identifier")
    sync_parser.add_argument("--last-round", type=int, help="Last known round")
    sync_parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == "ping":
        cmd_ping(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "request-states":
        cmd_request_states(args)
    elif args.command == "sync":
        cmd_sync(args)


if __name__ == "__main__":
    main()
