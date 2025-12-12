"""
Average consensus algorithm for UAV swarm coordination.

Implements distributed averaging where all UAVs converge to the mean
of their initial values through local communication.
"""

from typing import Optional

import networkx as nx
import numpy as np

from argus_uav.utils.logging_config import get_logger

logger = get_logger(__name__)


class AverageConsensus:
    """
    Distributed average consensus algorithm.

    Each UAV updates its state by averaging with its neighbors.
    Converges to the global average if the network is connected.

    Update rule:
        x_i(t+1) = x_i(t) + ε × Σ_{j∈N_i} (x_j(t) - x_i(t))

    Where:
        x_i(t) = state of UAV i at time t
        N_i = neighbors of UAV i (connected in graph)
        ε = step size (typically 1/max_degree for guaranteed convergence)
    """

    def __init__(self, step_size: Optional[float] = None):
        """
        Initialize consensus algorithm.

        Args:
            step_size: Consensus step size (if None, uses 1/max_degree)
        """
        self.step_size = step_size
        self.states: dict[str, float] = {}
        self.initial_states: dict[str, float] = {}
        self.true_average: float = 0.0

    def initialize(self, graph: nx.Graph, rng: np.random.Generator) -> None:
        """
        Initialize consensus states with random values.

        Args:
            graph: Swarm graph
            rng: Random number generator
        """
        # Assign random initial values to each UAV
        for node in graph.nodes():
            initial_value = float(rng.uniform(0, 100))
            self.states[node] = initial_value
            self.initial_states[node] = initial_value

        # Compute true average
        if self.states:
            self.true_average = np.mean(list(self.states.values()))

        logger.info(
            f"Consensus initialized: {len(self.states)} nodes, "
            f"true average = {self.true_average:.2f}"
        )

    def step(self, graph: nx.Graph) -> None:
        """
        Perform one consensus update step.

        Args:
            graph: Current swarm graph topology
        """
        if not self.states:
            logger.warning("Consensus not initialized")
            return

        # Determine step size
        if self.step_size is None:
            # Use 1/max_degree for guaranteed convergence
            degrees = dict(graph.degree())
            max_degree = max(degrees.values()) if degrees else 1
            epsilon = 1.0 / max(max_degree, 1)
        else:
            epsilon = self.step_size

        # Compute new states
        new_states = {}

        for node in graph.nodes():
            if node not in self.states:
                # New node (e.g., phantom) - initialize with current average
                current_avg = np.mean(list(self.states.values()))
                self.states[node] = current_avg
                self.initial_states[node] = current_avg

            current_value = self.states[node]

            # Get neighbors
            neighbors = list(graph.neighbors(node))

            if not neighbors:
                # Isolated node - no update
                new_states[node] = current_value
                continue

            # Average with neighbors
            neighbor_sum = sum(
                self.states.get(neighbor, current_value) for neighbor in neighbors
            )
            neighbor_avg = neighbor_sum / len(neighbors)

            # Consensus update
            new_value = current_value + epsilon * (neighbor_avg - current_value)
            new_states[node] = new_value

        # Update states
        self.states = new_states

    def get_consensus_error(self) -> float:
        """
        Compute L2 norm of consensus error.

        Returns:
            Distance from current states to true average
        """
        if not self.states:
            return 0.0

        values = np.array(list(self.states.values()))
        errors = values - self.true_average

        return float(np.linalg.norm(errors))

    def get_states(self) -> dict[str, float]:
        """
        Get current consensus states.

        Returns:
            Dictionary mapping UAV IDs to current state values
        """
        return self.states.copy()

    def has_converged(self, tolerance: float = 0.01) -> bool:
        """
        Check if consensus has converged.

        Args:
            tolerance: Convergence threshold

        Returns:
            True if all states are within tolerance of true average
        """
        if not self.states:
            return False

        values = np.array(list(self.states.values()))
        max_error = np.max(np.abs(values - self.true_average))

        return max_error < tolerance

    def get_statistics(self) -> dict:
        """
        Get consensus statistics.

        Returns:
            Dictionary with consensus metrics
        """
        if not self.states:
            return {}

        values = np.array(list(self.states.values()))

        return {
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "true_average": self.true_average,
            "error": self.get_consensus_error(),
            "converged": self.has_converged(),
        }
