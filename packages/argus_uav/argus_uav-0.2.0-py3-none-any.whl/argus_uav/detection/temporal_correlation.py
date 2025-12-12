"""
Temporal correlation detector for coordinated attacks.

Detects coordinated behavior by analyzing:
- Velocity correlation between UAVs
- Synchronized trajectory patterns
- Group movement anomalies
- Temporal behavior consistency
"""

import time
from collections import deque

import networkx as nx
import numpy as np
from scipy.stats import pearsonr

from argus_uav.detection import AnomalyDetector
from argus_uav.evaluation import DetectionResult
from argus_uav.utils.logging_config import get_logger

logger = get_logger(__name__)


class TemporalCorrelationDetector(AnomalyDetector):
    """
    Detects coordinated attacks via temporal correlation analysis.

    Monitors:
    - Velocity correlation: UAVs moving in sync
    - Trajectory similarity: Similar movement patterns
    - Group formation: Suspicious clustering
    - Behavioral consistency: Deviation from normal patterns

    Coordinated attacks exhibit high inter-UAV correlation that differs
    from legitimate swarm behavior.
    """

    def __init__(
        self,
        name: str = "temporal_correlation",
        threshold: float = 0.9,
        history_size: int = 15,
        correlation_threshold: float = 0.80,
        warmup_steps: int = 5,
    ):
        """
        Initialize temporal correlation detector.

        Args:
            name: Detector identifier
            threshold: Anomaly threshold (lower = more sensitive, default: 0.9 for coordinated attacks)
            history_size: Number of timesteps to track for correlation (default: 15)
            correlation_threshold: Minimum correlation for suspicious behavior (default: 0.80)
            warmup_steps: Number of initial steps to skip for warmup (default: 5)
        """
        super().__init__(name)
        self.threshold = threshold
        self.history_size = history_size
        self.correlation_threshold = correlation_threshold
        self.warmup_steps = warmup_steps
        self.detection_count = 0

        # Historical data storage
        self.position_history: dict[str, deque] = {}
        self.velocity_history: dict[str, deque] = {}
        self.timestamp_history: deque = deque(maxlen=history_size)

        # Baseline statistics
        self.baseline_velocity_corr_mean: float = 0.0
        self.baseline_velocity_corr_std: float = 0.0
        self.baseline_position_variance: float = 0.0
        self.baseline_group_size_mean: float = 0.0
        self.baseline_group_size_std: float = 0.0

    def train(self, clean_graphs: list[nx.Graph]) -> None:
        """
        Train detector on clean baseline graphs.

        Args:
            clean_graphs: Time series of graphs without attacks

        Effects:
            Computes baseline temporal correlation statistics
        """
        self.baseline_graphs = clean_graphs

        if not clean_graphs or len(clean_graphs) < 2:
            logger.warning("Need at least 2 graphs for temporal training")
            return

        # Collect velocity correlations and group statistics
        all_correlations = []
        all_group_sizes = []

        for i in range(1, len(clean_graphs)):
            prev_graph = clean_graphs[i - 1]
            curr_graph = clean_graphs[i]

            # Get UAVs present in both timesteps
            common_uavs = set(prev_graph.nodes()) & set(curr_graph.nodes())

            if len(common_uavs) < 2:
                continue

            # Extract velocities
            velocities = []
            for uav_id in common_uavs:
                curr_data = curr_graph.nodes[uav_id]

                if "uav" in curr_data:
                    velocity = curr_data["uav"].velocity
                    velocities.append(velocity)

            if len(velocities) < 2:
                continue

            # Compute pairwise velocity correlations
            velocities = np.array(velocities)
            for j in range(len(velocities)):
                for k in range(j + 1, len(velocities)):
                    v1 = velocities[j]
                    v2 = velocities[k]

                    # Correlation in velocity magnitude and direction
                    if np.linalg.norm(v1) > 0.1 and np.linalg.norm(v2) > 0.1:
                        # Cosine similarity for direction
                        cosine_sim = np.dot(v1, v2) / (
                            np.linalg.norm(v1) * np.linalg.norm(v2)
                        )
                        all_correlations.append(cosine_sim)

            # Detect groups (connected components with high density)
            if len(curr_graph.edges()) > 0:
                components = list(nx.connected_components(curr_graph))
                for component in components:
                    if len(component) > 1:
                        all_group_sizes.append(len(component))

        # Compute baseline statistics
        if all_correlations:
            self.baseline_velocity_corr_mean = np.mean(all_correlations)
            self.baseline_velocity_corr_std = np.std(all_correlations)

        if all_group_sizes:
            self.baseline_group_size_mean = np.mean(all_group_sizes)
            self.baseline_group_size_std = np.std(all_group_sizes)

        logger.info(f"Temporal detector trained on {len(clean_graphs)} graphs")
        logger.debug(
            f"  Baseline velocity correlation: {self.baseline_velocity_corr_mean:.3f} "
            f"± {self.baseline_velocity_corr_std:.3f}"
        )
        logger.debug(
            f"  Baseline group size: {self.baseline_group_size_mean:.1f} "
            f"± {self.baseline_group_size_std:.1f}"
        )

    def detect(self, graph: nx.Graph) -> DetectionResult:
        """
        Detect coordinated attacks using temporal correlation.

        Args:
            graph: Current swarm graph to analyze

        Returns:
            DetectionResult with flagged UAVs and confidence scores
        """
        start_time = time.time()

        confidence_scores = {}
        anomalous_uav_ids = set()

        if len(graph.nodes()) < 2:
            detection_time = time.time() - start_time
            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=set(),
                confidence_scores={uid: 0.0 for uid in graph.nodes()},
                ground_truth={},
                detection_time=detection_time,
            )

        # Increment detection count
        self.detection_count += 1

        # Update history with current graph
        current_timestamp = time.time()
        self.timestamp_history.append(current_timestamp)

        # Extract current positions and velocities
        for node in graph.nodes():
            node_data = graph.nodes[node]
            if "uav" in node_data:
                uav = node_data["uav"]

                # Initialize history if needed
                if node not in self.position_history:
                    self.position_history[node] = deque(maxlen=self.history_size)
                    self.velocity_history[node] = deque(maxlen=self.history_size)

                self.position_history[node].append(uav.position)
                self.velocity_history[node].append(uav.velocity)

        # Skip detection during warmup period
        if self.detection_count <= self.warmup_steps:
            detection_time = time.time() - start_time
            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=set(),
                confidence_scores={uid: 0.0 for uid in graph.nodes()},
                ground_truth={},
                detection_time=detection_time,
            )

        # Analyze coordinated behavior
        uav_nodes = [node for node in graph.nodes() if "uav" in graph.nodes[node]]

        if len(uav_nodes) < 2:
            detection_time = time.time() - start_time
            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=set(),
                confidence_scores={uid: 0.0 for uid in graph.nodes()},
                ground_truth={},
                detection_time=detection_time,
            )

        # 1. Compute velocity correlations
        velocity_correlation_matrix = self._compute_velocity_correlations(uav_nodes)

        # 2. Detect suspicious groups (high correlation clusters)
        suspicious_groups = self._detect_suspicious_groups(
            uav_nodes, velocity_correlation_matrix
        )

        # 3. Compute trajectory deviation scores
        trajectory_scores = self._compute_trajectory_scores(graph)

        # 4. Combine scores
        for node in graph.nodes():
            score = 0.0

            # Score from velocity correlation
            if node in uav_nodes:
                avg_correlation = np.mean(
                    [
                        velocity_correlation_matrix[uav_nodes.index(node)][
                            uav_nodes.index(other)
                        ]
                        for other in uav_nodes
                        if other != node
                    ]
                )

                # Z-score: high correlation is suspicious
                if self.baseline_velocity_corr_std > 0:
                    corr_z_score = abs(
                        avg_correlation - self.baseline_velocity_corr_mean
                    ) / (self.baseline_velocity_corr_std + 1e-10)
                    score += 0.4 * corr_z_score

            # Score from group membership
            in_suspicious_group = any(node in group for group in suspicious_groups)
            if in_suspicious_group:
                score += 1.5  # Strong indicator

            # Score from trajectory deviation
            if node in trajectory_scores:
                score += 0.4 * trajectory_scores[node]

            confidence_scores[node] = float(score)

            # Flag if above threshold
            if score > self.threshold:
                anomalous_uav_ids.add(node)

        # Get ground truth
        ground_truth = {}
        for node in graph.nodes():
            node_data = graph.nodes[node]
            if "uav" in node_data:
                uav = node_data["uav"]
                ground_truth[node] = uav.is_legitimate
            else:
                ground_truth[node] = True

        detection_time = time.time() - start_time

        logger.debug(
            f"Temporal correlation detection: {len(anomalous_uav_ids)} anomalies, "
            f"{len(suspicious_groups)} suspicious groups"
        )

        return DetectionResult(
            detector_name=self.name,
            timestamp=time.time(),
            anomalous_uav_ids=anomalous_uav_ids,
            confidence_scores=confidence_scores,
            ground_truth=ground_truth,
            detection_time=detection_time,
        )

    def _compute_velocity_correlations(self, uav_nodes: list[str]) -> np.ndarray:
        """
        Compute pairwise velocity correlation matrix.

        Args:
            uav_nodes: List of UAV node IDs

        Returns:
            N×N correlation matrix
        """
        n = len(uav_nodes)
        corr_matrix = np.zeros((n, n))

        for i, node1 in enumerate(uav_nodes):
            for j, node2 in enumerate(uav_nodes):
                if i == j:
                    corr_matrix[i][j] = 1.0
                    continue

                if (
                    node1 not in self.velocity_history
                    or node2 not in self.velocity_history
                ):
                    continue

                # Get velocity histories
                v1_history = list(self.velocity_history[node1])
                v2_history = list(self.velocity_history[node2])

                if len(v1_history) < 2 or len(v2_history) < 2:
                    continue

                # Compute correlation based on velocity magnitudes
                v1_mags = [np.linalg.norm(v) for v in v1_history]
                v2_mags = [np.linalg.norm(v) for v in v2_history]

                # Pearson correlation
                min_len = min(len(v1_mags), len(v2_mags))
                if min_len >= 2:
                    try:
                        corr, _ = pearsonr(v1_mags[-min_len:], v2_mags[-min_len:])
                        corr_matrix[i][j] = corr if not np.isnan(corr) else 0.0
                    except Exception:
                        corr_matrix[i][j] = 0.0

        return corr_matrix

    def _detect_suspicious_groups(
        self, uav_nodes: list[str], correlation_matrix: np.ndarray
    ) -> list[set[str]]:
        """
        Detect groups with suspiciously high correlation.

        Args:
            uav_nodes: List of UAV node IDs
            correlation_matrix: N×N correlation matrix

        Returns:
            List of suspicious groups (sets of UAV IDs)
        """
        suspicious_groups = []
        n = len(uav_nodes)

        if n < 2:
            return suspicious_groups

        # Build graph of high-correlation pairs
        corr_graph = nx.Graph()
        for i in range(n):
            for j in range(i + 1, n):
                corr = correlation_matrix[i][j]
                if corr > self.correlation_threshold:
                    corr_graph.add_edge(uav_nodes[i], uav_nodes[j], weight=corr)

        # Find connected components (groups)
        if len(corr_graph.nodes()) > 0:
            components = list(nx.connected_components(corr_graph))

            for component in components:
                # Group is suspicious if:
                # 1. Size is unusual (z-score test)
                # 2. Average correlation is very high

                group_size = len(component)

                if self.baseline_group_size_std > 0:
                    size_z_score = abs(group_size - self.baseline_group_size_mean) / (
                        self.baseline_group_size_std + 1e-10
                    )

                    # Anomalous if group size deviates significantly
                    if size_z_score > 2.0:
                        suspicious_groups.append(component)

        return suspicious_groups

    def _compute_trajectory_scores(self, graph: nx.Graph) -> dict[str, float]:
        """
        Compute trajectory deviation scores for UAVs.

        Args:
            graph: Current swarm graph

        Returns:
            Mapping of UAV ID to deviation score
        """
        scores = {}

        for node in graph.nodes():
            if node not in self.position_history:
                scores[node] = 0.0
                continue

            pos_history = list(self.position_history[node])

            if len(pos_history) < 3:
                scores[node] = 0.0
                continue

            # Compute trajectory smoothness (acceleration changes)
            accelerations = []
            for i in range(2, len(pos_history)):
                p0 = np.array(pos_history[i - 2])
                p1 = np.array(pos_history[i - 1])
                p2 = np.array(pos_history[i])

                # Approximate acceleration
                v1 = p1 - p0
                v2 = p2 - p1
                accel = v2 - v1
                accelerations.append(np.linalg.norm(accel))

            if accelerations:
                # High variance in acceleration = erratic movement
                accel_variance = np.var(accelerations)
                scores[node] = float(accel_variance / 100.0)  # Normalize
            else:
                scores[node] = 0.0

        return scores

    def reset_history(self) -> None:
        """Clear temporal history (useful for new simulations)."""
        self.position_history.clear()
        self.velocity_history.clear()
        self.timestamp_history.clear()
        logger.info("Temporal correlation history reset")
