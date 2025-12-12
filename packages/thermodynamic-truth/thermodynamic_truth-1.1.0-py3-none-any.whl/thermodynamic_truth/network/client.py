"""
gRPC Client Implementation for ThermoTruth Nodes

Handles outgoing network requests to peer nodes.
"""

import grpc
import logging
import numpy as np
import time
from typing import List, Optional, Tuple

from . import thermo_protocol_pb2 as pb2
from . import thermo_protocol_pb2_grpc as pb2_grpc
from ..core.state import ConsensusState

logger = logging.getLogger(__name__)


class ThermoNodeClient:
    """
    gRPC client for communicating with peer ThermoTruth nodes.
    """

    def __init__(self, peer_address: str, timeout: int = 10):
        """
        Initialize client for a peer node.

        Args:
            peer_address: Address of peer (host:port)
            timeout: Request timeout in seconds
        """
        self.peer_address = peer_address
        self.timeout = timeout
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[pb2_grpc.ThermoNodeStub] = None

        logger.info(f"Initialized client for peer {peer_address}")

    def connect(self):
        """Establish connection to peer."""
        self.channel = grpc.insecure_channel(self.peer_address)
        self.stub = pb2_grpc.ThermoNodeStub(self.channel)
        logger.debug(f"Connected to peer {self.peer_address}")

    def close(self):
        """Close connection to peer."""
        if self.channel:
            self.channel.close()
            logger.debug(f"Closed connection to peer {self.peer_address}")

    def propose_state(self, state: ConsensusState) -> Tuple[bool, dict]:
        """
        Propose a state to the peer.

        Args:
            state: ConsensusState to propose

        Returns:
            Tuple of (accepted, response_dict)
        """
        if not self.stub:
            self.connect()

        try:
            # Create proposal message
            proposal = pb2.StateProposal(
                state_vector=state.state_vector.tobytes(),
                energy=state.energy,
                timestamp=state.timestamp,
                proposer_id=state.proposer_id,
                nonce=state.nonce,
                difficulty=state.difficulty,
                metadata=state.metadata,
            )

            # Send proposal
            response = self.stub.ProposeState(proposal, timeout=self.timeout)

            return response.accepted, {
                "message": response.message,
                "temperature": response.current_temperature,
                "entropy": response.current_entropy,
                "ensemble_size": response.ensemble_size,
            }

        except grpc.RpcError as e:
            logger.error(f"RPC error proposing state to {self.peer_address}: {e}")
            return False, {"message": f"RPC error: {e}"}

    def request_states(
        self, requester_id: str, round_number: int, max_states: int = 100
    ) -> List[ConsensusState]:
        """
        Request states from the peer.

        Args:
            requester_id: ID of requesting node
            round_number: Current round number
            max_states: Maximum number of states to request

        Returns:
            List of ConsensusState objects
        """
        if not self.stub:
            self.connect()

        try:
            # Create request message
            request = pb2.StateRequest(
                requester_id=requester_id, round_number=round_number, max_states=max_states
            )

            # Send request
            response = self.stub.RequestStates(request, timeout=self.timeout)

            # Convert to ConsensusState objects
            states = []
            for proposal in response.states:
                state_vector = np.frombuffer(proposal.state_vector, dtype=np.float64)
                state = ConsensusState(
                    state_vector=state_vector,
                    energy=proposal.energy,
                    timestamp=proposal.timestamp,
                    proposer_id=proposal.proposer_id,
                    nonce=proposal.nonce,
                    difficulty=proposal.difficulty,
                    metadata=dict(proposal.metadata),
                )
                states.append(state)

            logger.debug(f"Received {len(states)} states from {self.peer_address}")
            return states

        except grpc.RpcError as e:
            logger.error(f"RPC error requesting states from {self.peer_address}: {e}")
            return []

    def announce_consensus(
        self,
        round_number: int,
        consensus_state: np.ndarray,
        final_variance: float,
        final_temperature: float,
        final_entropy: float,
        announcer_id: str,
    ) -> bool:
        """
        Announce consensus achievement to peer.

        Args:
            round_number: Consensus round number
            consensus_state: Final consensus state vector
            final_variance: Final variance
            final_temperature: Final temperature
            final_entropy: Final entropy
            announcer_id: ID of announcing node

        Returns:
            True if acknowledged
        """
        if not self.stub:
            self.connect()

        try:
            # Create announcement message
            announcement = pb2.ConsensusAnnouncement(
                round_number=round_number,
                consensus_state=consensus_state.tobytes(),
                final_variance=final_variance,
                final_temperature=final_temperature,
                final_entropy=final_entropy,
                announcer_id=announcer_id,
                timestamp=time.time(),
            )

            # Send announcement
            response = self.stub.AnnounceConsensus(announcement, timeout=self.timeout)

            return response.acknowledged

        except grpc.RpcError as e:
            logger.error(f"RPC error announcing consensus to {self.peer_address}: {e}")
            return False

    def ping(self, sender_id: str) -> Optional[dict]:
        """
        Ping the peer (health check).

        Args:
            sender_id: ID of sending node

        Returns:
            Peer status dict if successful, None otherwise
        """
        if not self.stub:
            self.connect()

        try:
            # Create ping message
            ping_request = pb2.PingRequest(sender_id=sender_id, timestamp=time.time())

            # Send ping
            response = self.stub.Ping(ping_request, timeout=self.timeout)

            return {
                "responder_id": response.responder_id,
                "timestamp": response.timestamp,
                "current_round": response.current_round,
                "ensemble_size": response.ensemble_size,
                "temperature": response.temperature,
            }

        except grpc.RpcError as e:
            logger.error(f"RPC error pinging {self.peer_address}: {e}")
            return None

    def sync_state(
        self, requester_id: str, last_known_round: int
    ) -> Tuple[int, List[dict], List[ConsensusState]]:
        """
        Synchronize state with peer.

        Args:
            requester_id: ID of requesting node
            last_known_round: Last known consensus round

        Returns:
            Tuple of (current_round, consensus_history, pending_states)
        """
        if not self.stub:
            self.connect()

        try:
            # Create sync request
            request = pb2.SyncRequest(requester_id=requester_id, last_known_round=last_known_round)

            # Send request
            response = self.stub.SyncState(request, timeout=self.timeout)

            # Parse consensus history
            consensus_history = []
            for announcement in response.consensus_history:
                consensus_state = np.frombuffer(announcement.consensus_state, dtype=np.float64)
                consensus_history.append(
                    {
                        "round": announcement.round_number,
                        "consensus_state": consensus_state,
                        "final_variance": announcement.final_variance,
                        "final_temperature": announcement.final_temperature,
                        "final_entropy": announcement.final_entropy,
                        "announcer_id": announcement.announcer_id,
                        "timestamp": announcement.timestamp,
                    }
                )

            # Parse pending states
            pending_states = []
            for proposal in response.pending_states:
                state_vector = np.frombuffer(proposal.state_vector, dtype=np.float64)
                state = ConsensusState(
                    state_vector=state_vector,
                    energy=proposal.energy,
                    timestamp=proposal.timestamp,
                    proposer_id=proposal.proposer_id,
                    nonce=proposal.nonce,
                    difficulty=proposal.difficulty,
                    metadata=dict(proposal.metadata),
                )
                pending_states.append(state)

            logger.info(
                f"Synced with {self.peer_address}: "
                f"round={response.current_round}, "
                f"history_items={len(consensus_history)}, "
                f"pending={len(pending_states)}"
            )

            return response.current_round, consensus_history, pending_states

        except grpc.RpcError as e:
            logger.error(f"RPC error syncing with {self.peer_address}: {e}")
            return 0, [], []


class PeerManager:
    """
    Manages connections to multiple peer nodes.
    """

    def __init__(self):
        """Initialize peer manager."""
        self.peers: dict[str, ThermoNodeClient] = {}
        logger.info("Initialized peer manager")

    def add_peer(self, peer_address: str) -> ThermoNodeClient:
        """
        Add a peer to the manager.

        Args:
            peer_address: Address of peer (host:port)

        Returns:
            ThermoNodeClient for the peer
        """
        if peer_address not in self.peers:
            client = ThermoNodeClient(peer_address)
            self.peers[peer_address] = client
            logger.info(f"Added peer {peer_address}")

        return self.peers[peer_address]

    def remove_peer(self, peer_address: str):
        """
        Remove a peer from the manager.

        Args:
            peer_address: Address of peer to remove
        """
        if peer_address in self.peers:
            self.peers[peer_address].close()
            del self.peers[peer_address]
            logger.info(f"Removed peer {peer_address}")

    def broadcast_state(self, state: ConsensusState) -> dict[str, bool]:
        """
        Broadcast a state to all peers.

        Args:
            state: ConsensusState to broadcast

        Returns:
            Dict mapping peer addresses to success status
        """
        results = {}
        for peer_address, client in self.peers.items():
            accepted, _ = client.propose_state(state)
            results[peer_address] = accepted

        return results

    def broadcast_consensus(
        self,
        round_number: int,
        consensus_state: np.ndarray,
        final_variance: float,
        final_temperature: float,
        final_entropy: float,
        announcer_id: str,
    ) -> dict[str, bool]:
        """
        Broadcast consensus announcement to all peers.

        Args:
            round_number: Consensus round number
            consensus_state: Final consensus state
            final_variance: Final variance
            final_temperature: Final temperature
            final_entropy: Final entropy
            announcer_id: ID of announcing node

        Returns:
            Dict mapping peer addresses to acknowledgment status
        """
        results = {}
        for peer_address, client in self.peers.items():
            acknowledged = client.announce_consensus(
                round_number,
                consensus_state,
                final_variance,
                final_temperature,
                final_entropy,
                announcer_id,
            )
            results[peer_address] = acknowledged

        return results

    def ping_all(self, sender_id: str) -> dict[str, Optional[dict]]:
        """
        Ping all peers.

        Args:
            sender_id: ID of sending node

        Returns:
            Dict mapping peer addresses to status dicts
        """
        results = {}
        for peer_address, client in self.peers.items():
            status = client.ping(sender_id)
            results[peer_address] = status

        return results

    def close_all(self):
        """Close all peer connections."""
        for client in self.peers.values():
            client.close()
        self.peers.clear()
        logger.info("Closed all peer connections")
