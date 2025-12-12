"""
gRPC Server Implementation for ThermoTruth Nodes

Handles incoming network requests from peer nodes.
"""

import grpc
from concurrent import futures
import logging
import numpy as np
from typing import Optional

from . import thermo_protocol_pb2 as pb2
from . import thermo_protocol_pb2_grpc as pb2_grpc
from ..core.protocol import ThermodynamicTruth
from ..core.state import ConsensusState

logger = logging.getLogger(__name__)


class ThermoNodeServicer(pb2_grpc.ThermoNodeServicer):
    """
    gRPC servicer implementing the ThermoNode service.

    This handles all incoming RPC calls from peer nodes.
    """

    def __init__(self, protocol: ThermodynamicTruth):
        """
        Initialize servicer with protocol instance.

        Args:
            protocol: ThermodynamicTruth protocol instance
        """
        self.protocol = protocol
        logger.info(f"Initialized ThermoNode servicer for {protocol.node_id}")

    def ProposeState(self, request: pb2.StateProposal, context) -> pb2.StateResponse:
        """
        Handle incoming state proposal from a peer.

        Args:
            request: StateProposal message
            context: gRPC context

        Returns:
            StateResponse indicating acceptance
        """
        try:
            # Deserialize state vector
            state_vector = np.frombuffer(request.state_vector, dtype=np.float64)

            # Create ConsensusState object
            state = ConsensusState(
                state_vector=state_vector,
                energy=request.energy,
                timestamp=request.timestamp,
                proposer_id=request.proposer_id,
                nonce=request.nonce,
                difficulty=request.difficulty,
                metadata=dict(request.metadata),
            )

            # Validate and add to ensemble
            accepted = self.protocol.receive_state(state)

            # Get current metrics
            status = self.protocol.get_status()

            return pb2.StateResponse(
                accepted=accepted,
                message="State accepted" if accepted else "State rejected (invalid PoW)",
                current_temperature=status["current_temperature"],
                current_entropy=status["current_entropy"],
                ensemble_size=status["ensemble_size"],
            )

        except Exception as e:
            logger.error(f"Error in ProposeState: {e}")
            return pb2.StateResponse(
                accepted=False,
                message=f"Error: {str(e)}",
                current_temperature=0.0,
                current_entropy=0.0,
                ensemble_size=0,
            )

    def RequestStates(self, request: pb2.StateRequest, context) -> pb2.StateBundle:
        """
        Handle request for current states.

        Args:
            request: StateRequest message
            context: gRPC context

        Returns:
            StateBundle with current ensemble states
        """
        try:
            # Get states from current ensemble
            states = self.protocol.current_ensemble.states

            # Limit number of states if requested
            max_states = request.max_states if request.max_states > 0 else len(states)
            states_to_send = states[:max_states]

            # Convert to protobuf messages
            state_proposals = []
            for state in states_to_send:
                proposal = pb2.StateProposal(
                    state_vector=state.state_vector.tobytes(),
                    energy=state.energy,
                    timestamp=state.timestamp,
                    proposer_id=state.proposer_id,
                    nonce=state.nonce,
                    difficulty=state.difficulty,
                    metadata=state.metadata,
                )
                state_proposals.append(proposal)

            return pb2.StateBundle(
                states=state_proposals,
                round_number=self.protocol.round_number,
                provider_id=self.protocol.node_id,
            )

        except Exception as e:
            logger.error(f"Error in RequestStates: {e}")
            return pb2.StateBundle(states=[], round_number=0, provider_id=self.protocol.node_id)

    def AnnounceConsensus(
        self, request: pb2.ConsensusAnnouncement, context
    ) -> pb2.AcknowledgeResponse:
        """
        Handle consensus announcement from a peer.

        Args:
            request: ConsensusAnnouncement message
            context: gRPC context

        Returns:
            AcknowledgeResponse
        """
        try:
            logger.info(
                f"Received consensus announcement from {request.announcer_id} "
                f"for round {request.round_number}: "
                f"variance={request.final_variance:.6f}, "
                f"temp={request.final_temperature:.6f}°C"
            )

            return pb2.AcknowledgeResponse(acknowledged=True, message="Consensus acknowledged")

        except Exception as e:
            logger.error(f"Error in AnnounceConsensus: {e}")
            return pb2.AcknowledgeResponse(acknowledged=False, message=f"Error: {str(e)}")

    def Ping(self, request: pb2.PingRequest, context) -> pb2.PongResponse:
        """
        Handle ping request (health check).

        Args:
            request: PingRequest message
            context: gRPC context

        Returns:
            PongResponse with node status
        """
        try:
            status = self.protocol.get_status()

            return pb2.PongResponse(
                responder_id=self.protocol.node_id,
                timestamp=request.timestamp,
                current_round=status["round"],
                ensemble_size=status["ensemble_size"],
                temperature=status["current_temperature"],
            )

        except Exception as e:
            logger.error(f"Error in Ping: {e}")
            return pb2.PongResponse(
                responder_id=self.protocol.node_id,
                timestamp=request.timestamp,
                current_round=0,
                ensemble_size=0,
                temperature=0.0,
            )

    def SyncState(self, request: pb2.SyncRequest, context) -> pb2.SyncResponse:
        """
        Handle state synchronization request.

        Args:
            request: SyncRequest message
            context: gRPC context

        Returns:
            SyncResponse with consensus history
        """
        try:
            # Get consensus history
            history = self.protocol.consensus_history

            # Filter history after last known round
            relevant_history = [h for h in history if h["round"] > request.last_known_round]

            # Convert to protobuf messages
            consensus_announcements = []
            for h in relevant_history:
                announcement = pb2.ConsensusAnnouncement(
                    round_number=h["round"],
                    consensus_state=h["consensus_state"].tobytes(),
                    final_variance=h["final_variance"],
                    final_temperature=h["final_temperature"],
                    final_entropy=h["final_entropy"],
                    announcer_id=self.protocol.node_id,
                    timestamp=h.get("timestamp", 0.0),
                )
                consensus_announcements.append(announcement)

            # Get pending states
            pending_states = []
            for state in self.protocol.current_ensemble.states:
                proposal = pb2.StateProposal(
                    state_vector=state.state_vector.tobytes(),
                    energy=state.energy,
                    timestamp=state.timestamp,
                    proposer_id=state.proposer_id,
                    nonce=state.nonce,
                    difficulty=state.difficulty,
                    metadata=state.metadata,
                )
                pending_states.append(proposal)

            return pb2.SyncResponse(
                current_round=self.protocol.round_number,
                consensus_history=consensus_announcements,
                pending_states=pending_states,
            )

        except Exception as e:
            logger.error(f"Error in SyncState: {e}")
            return pb2.SyncResponse(
                current_round=self.protocol.round_number, consensus_history=[], pending_states=[]
            )


class ThermoNodeServer:
    """
    gRPC server for ThermoTruth node.

    Manages the server lifecycle and handles incoming connections.
    """

    def __init__(self, protocol: ThermodynamicTruth, port: int = 50051, max_workers: int = 10):
        """
        Initialize server.

        Args:
            protocol: ThermodynamicTruth protocol instance
            port: Port to listen on
            max_workers: Maximum number of worker threads
        """
        self.protocol = protocol
        self.port = port
        self.max_workers = max_workers
        self.server: Optional[grpc.Server] = None

        logger.info(f"Initialized ThermoNode server on port {port}")

    def start(self):
        """Start the gRPC server."""
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))

        # Add servicer to server
        servicer = ThermoNodeServicer(self.protocol)
        pb2_grpc.add_ThermoNodeServicer_to_server(servicer, self.server)

        # Bind to port
        self.server.add_insecure_port(f"[::]:{self.port}")

        # Start server
        self.server.start()
        logger.info(f"ThermoNode server started on port {self.port}")

    def stop(self, grace_period: int = 5):
        """
        Stop the gRPC server.

        Args:
            grace_period: Grace period for shutdown (seconds)
        """
        if self.server:
            self.server.stop(grace_period)
            logger.info("ThermoNode server stopped")

    def wait_for_termination(self):
        """Block until the server is terminated."""
        if self.server:
            self.server.wait_for_termination()
