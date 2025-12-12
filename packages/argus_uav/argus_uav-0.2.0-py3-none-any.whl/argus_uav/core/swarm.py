"""
UAV Swarm simulation with dynamic graph topology.

Orchestrates UAV movements, Remote ID broadcasting, and graph connectivity.
"""

import networkx as nx
import numpy as np

from argus_uav.core.uav import UAV
from argus_uav.utils.logging_config import get_logger

logger = get_logger(__name__)


class Swarm:
    """
    UAV swarm simulator with dynamic graph topology.

    Manages a collection of UAVs, updates their positions, maintains
    network connectivity graph, and handles Remote ID message broadcasting.

    Attributes:
        num_uavs: Number of legitimate UAVs in swarm
        comm_range: Communication range in meters
        bounds: Simulation space boundaries (x_max, y_max, z_max)
        rng: NumPy random generator for reproducibility
        uavs: Dictionary mapping UAV IDs to UAV objects
        graph: NetworkX graph representing network topology
        simulation_time: Current simulation time in seconds
    """

    def __init__(
        self,
        num_uavs: int,
        comm_range: float,
        bounds: tuple[float, float, float],
        rng: np.random.Generator,
        enable_crypto: bool = False,
    ):
        """
        Initialize swarm with N UAVs in 3D space.

        Args:
            num_uavs: Number of legitimate UAVs
            comm_range: Communication range in meters
            bounds: Simulation space dimensions (x, y, z)
            rng: NumPy random generator for reproducibility
            enable_crypto: If True, generate Ed25519 keys for all UAVs
        """
        self.num_uavs = num_uavs
        self.comm_range = comm_range
        self.bounds = bounds
        self.rng = rng
        self.simulation_time = 0.0
        self.enable_crypto = enable_crypto

        # Initialize graph
        self.graph = nx.Graph()

        # Create UAVs with random positions and velocities
        self.uavs: dict[str, UAV] = {}
        self._initialize_uavs()

        # Build initial topology
        self._update_topology()

        crypto_status = "crypto enabled" if enable_crypto else "no crypto"
        logger.info(
            f"Swarm initialized: {num_uavs} UAVs, comm_range={comm_range}m, "
            f"bounds={bounds}, {crypto_status}"
        )

    def _initialize_uavs(self) -> None:
        """Create UAVs with random positions and velocities."""
        max_speed = 15.0  # m/s (reasonable for UAVs)

        for i in range(self.num_uavs):
            uav_id = f"UAV-{i:03d}"

            # Random position within bounds
            position = (
                float(self.rng.uniform(0, self.bounds[0])),
                float(self.rng.uniform(0, self.bounds[1])),
                float(self.rng.uniform(0, self.bounds[2])),
            )

            # Random velocity
            velocity = (
                float(self.rng.uniform(-max_speed, max_speed)),
                float(self.rng.uniform(-max_speed, max_speed)),
                float(
                    self.rng.uniform(-max_speed / 2, max_speed / 2)
                ),  # Less vertical movement
            )

            uav = UAV(
                uav_id=uav_id, position=position, velocity=velocity, is_legitimate=True
            )

            # Generate Ed25519 keys if crypto enabled
            if self.enable_crypto:
                from argus_uav.crypto.ed25519_signer import Ed25519Signer

                private_key, public_key = Ed25519Signer.generate_keypair()
                uav.private_key = private_key
                uav.public_key = public_key

            self.uavs[uav_id] = uav
            self.graph.add_node(uav_id, uav=uav)

    def _distance(
        self, pos1: tuple[float, float, float], pos2: tuple[float, float, float]
    ) -> float:
        """
        Compute Euclidean distance between two 3D positions.

        Args:
            pos1: First position (x, y, z)
            pos2: Second position (x, y, z)

        Returns:
            Distance in meters
        """
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        return np.sqrt(dx**2 + dy**2 + dz**2)

    def _update_topology(self) -> None:
        """
        Rebuild graph edges based on current UAV positions.

        Two UAVs are connected if their distance <= comm_range.
        """
        # Clear existing edges
        self.graph.clear_edges()

        # Build new edges based on distances
        uav_ids = list(self.uavs.keys())

        for i in range(len(uav_ids)):
            for j in range(i + 1, len(uav_ids)):
                uav_i = self.uavs[uav_ids[i]]
                uav_j = self.uavs[uav_ids[j]]

                dist = self._distance(uav_i.position, uav_j.position)

                if dist <= self.comm_range:
                    self.graph.add_edge(uav_ids[i], uav_ids[j], distance=dist)

    def step(self, dt: float) -> None:
        """
        Advance simulation by time delta.

        Args:
            dt: Time step in seconds

        Effects:
            - Updates UAV positions
            - Rebuilds graph topology
            - Broadcasts Remote ID messages (signed if crypto enabled)
        """
        # Move all UAVs
        for uav in self.uavs.values():
            uav.move(dt, self.bounds)

        # Update graph topology
        self._update_topology()

        # Broadcast Remote ID messages
        for uav in self.uavs.values():
            message = uav.broadcast_remote_id(self.simulation_time)

            # Sign message if crypto enabled and UAV has private key
            if self.enable_crypto and uav.private_key is not None:
                uav.sign_message(message)

        # Increment simulation time
        self.simulation_time += dt

    def get_graph(self) -> nx.Graph:
        """
        Returns current swarm graph (read-only copy).

        Returns:
            NetworkX Graph with current topology
        """
        return self.graph.copy()

    def get_uavs(self) -> dict[str, UAV]:
        """
        Returns UAV mapping (read-only access).

        Returns:
            Dictionary of UAV ID to UAV object
        """
        return self.uavs.copy()

    def add_uav(self, uav: UAV) -> None:
        """
        Add a UAV to the swarm (used for attack injection).

        Args:
            uav: UAV object to add
        """
        self.uavs[uav.uav_id] = uav
        self.graph.add_node(uav.uav_id, uav=uav)
        logger.debug(f"Added UAV {uav.uav_id} to swarm")

    def remove_uav(self, uav_id: str) -> None:
        """
        Remove a UAV from the swarm.

        Args:
            uav_id: ID of UAV to remove
        """
        if uav_id in self.uavs:
            del self.uavs[uav_id]
            self.graph.remove_node(uav_id)
            logger.debug(f"Removed UAV {uav_id} from swarm")

    def get_statistics(self) -> dict:
        """
        Get current swarm statistics.

        Returns:
            Dictionary with swarm metrics
        """
        return {
            "num_uavs": len(self.uavs),
            "num_edges": self.graph.number_of_edges(),
            "avg_degree": sum(dict(self.graph.degree()).values()) / len(self.uavs)
            if self.uavs
            else 0,
            "is_connected": nx.is_connected(self.graph)
            if len(self.uavs) > 0
            else False,
            "simulation_time": self.simulation_time,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        stats = self.get_statistics()
        return (
            f"Swarm(uavs={stats['num_uavs']}, edges={stats['num_edges']}, "
            f"connected={stats['is_connected']}, t={stats['simulation_time']:.1f}s)"
        )
