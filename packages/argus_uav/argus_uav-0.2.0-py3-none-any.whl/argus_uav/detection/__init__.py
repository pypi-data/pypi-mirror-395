"""Detection algorithm modules for anomaly identification."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import networkx as nx

if TYPE_CHECKING:
    from argus_uav.evaluation import DetectionResult


class AnomalyDetector(ABC):
    """
    Base class for anomaly detection algorithms.

    All detectors must implement train() and detect() methods.
    """

    def __init__(self, name: str):
        """
        Initialize detector.

        Args:
            name: Detector identifier for logging and results
        """
        self.name = name
        self.baseline_graphs: list[nx.Graph] = []

    @abstractmethod
    def train(self, clean_graphs: list[nx.Graph]) -> None:
        """
        Train detector on clean baseline graphs.

        Args:
            clean_graphs: Time series of graphs without attacks

        Effects:
            Stores baseline statistics for comparison
        """
        pass

    @abstractmethod
    def detect(self, graph: nx.Graph) -> "DetectionResult":
        """
        Detect anomalies in graph.

        Args:
            graph: Current swarm graph to analyze

        Returns:
            DetectionResult with flagged UAVs and confidence scores
        """
        pass


__all__ = ["AnomalyDetector", "TemporalCorrelationDetector"]

# Import concrete detectors for convenience
try:
    from argus_uav.detection.temporal_correlation import TemporalCorrelationDetector
except ImportError:
    pass
