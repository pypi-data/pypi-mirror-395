"""
Spectral analysis for anomaly detection.

Uses Laplacian eigenvalues to detect topological anomalies in the swarm graph.
"""

import time

import networkx as nx
import numpy as np

from argus_uav.detection import AnomalyDetector
from argus_uav.evaluation import DetectionResult
from argus_uav.utils.logging_config import get_logger

logger = get_logger(__name__)


class SpectralDetector(AnomalyDetector):
    """
    Detects anomalies via Laplacian eigenvalue analysis.

    Monitors changes in the graph Laplacian's eigenvalues, particularly:
    - Algebraic connectivity (second smallest eigenvalue λ₂)
    - Spectral gap (λₙ - λ₂)
    - Overall eigenvalue distribution shifts
    - Eigenvector residuals (subspace-based detection)
    - Position-based topology validation

    Phantom UAVs and position spoofing create topological anomalies
    that manifest as eigenvalue deviations and eigenvector perturbations.
    """

    def __init__(
        self,
        name: str = "spectral",
        threshold: float = 2.0,
        use_eigenvector_residuals: bool = True,
        enable_physics_validation: bool = True,
    ):
        """
        Initialize spectral detector.

        Args:
            name: Detector identifier
            threshold: Standard deviations for anomaly threshold (default: 2.0 for balanced performance)
            use_eigenvector_residuals: Enable subspace-based detection
            enable_physics_validation: Enable physics-based movement validation
        """
        super().__init__(name)
        self.threshold = threshold
        self.use_eigenvector_residuals = use_eigenvector_residuals
        self.enable_physics_validation = enable_physics_validation

        # Baseline statistics
        self.baseline_eigenvalues: list[np.ndarray] = []
        self.baseline_eigenvectors: list[np.ndarray] = []
        self.mean_eigenvalues: np.ndarray = None
        self.std_eigenvalues: np.ndarray = None
        self.mean_algebraic_connectivity: float = 0.0
        self.std_algebraic_connectivity: float = 0.0
        self.baseline_subspace: np.ndarray = None  # For eigenvector residuals

        # Physics validation - track previous positions and velocities
        self.previous_positions: dict[str, tuple[float, float, float]] = {}
        self.previous_velocities: dict[str, tuple[float, float, float]] = {}
        self.previous_timestamp: float = 0.0
        self.max_acceleration: float = 10.0  # m/s^2 (reasonable for UAVs)
        self.max_speed: float = 30.0  # m/s

    def train(self, clean_graphs: list[nx.Graph]) -> None:
        """
        Train detector on clean baseline graphs.

        Args:
            clean_graphs: Time series of graphs without attacks

        Effects:
            Computes and stores baseline eigenvalue statistics
        """
        self.baseline_graphs = clean_graphs

        if not clean_graphs:
            logger.warning("No clean graphs provided for training")
            return

        # Compute eigenvalues for all baseline graphs
        for graph in clean_graphs:
            if len(graph.nodes()) > 0:
                eigenvalues, eigenvectors = self._compute_spectrum(graph)
                self.baseline_eigenvalues.append(eigenvalues)
                if self.use_eigenvector_residuals and eigenvectors is not None:
                    self.baseline_eigenvectors.append(eigenvectors)

        if not self.baseline_eigenvalues:
            logger.warning("Could not compute eigenvalues for training")
            return

        # Compute statistics (pad to handle variable graph sizes)
        max_nodes = max(len(ev) for ev in self.baseline_eigenvalues)
        padded_eigenvalues = []

        for ev in self.baseline_eigenvalues:
            # Pad with zeros if needed
            if len(ev) < max_nodes:
                padded = np.pad(ev, (0, max_nodes - len(ev)), constant_values=0)
            else:
                padded = ev
            padded_eigenvalues.append(padded)

        eigenvalue_matrix = np.array(padded_eigenvalues)
        self.mean_eigenvalues = np.mean(eigenvalue_matrix, axis=0)
        self.std_eigenvalues = np.std(eigenvalue_matrix, axis=0)

        # Algebraic connectivity (λ₂) statistics
        algebraic_connectivities = [
            ev[1] if len(ev) > 1 else 0.0 for ev in self.baseline_eigenvalues
        ]
        self.mean_algebraic_connectivity = np.mean(algebraic_connectivities)
        self.std_algebraic_connectivity = np.std(algebraic_connectivities)

        # Compute baseline subspace (average eigenvector subspace)
        if self.use_eigenvector_residuals and self.baseline_eigenvectors:
            # Use first k eigenvectors for subspace
            k = min(5, min(len(ev) for ev in self.baseline_eigenvectors if len(ev) > 0))
            if k > 0:
                # Average the subspace (simplified: just use the most recent baseline)
                self.baseline_subspace = self.baseline_eigenvectors[-1][:, :k]

        logger.info(f"Spectral detector trained on {len(clean_graphs)} graphs")
        logger.debug(
            f"  Mean algebraic connectivity: {self.mean_algebraic_connectivity:.4f}"
        )
        logger.debug(
            f"  Std algebraic connectivity: {self.std_algebraic_connectivity:.4f}"
        )
        if self.use_eigenvector_residuals and self.baseline_subspace is not None:
            logger.debug(
                f"  Baseline subspace dimension: {self.baseline_subspace.shape}"
            )

    def detect(self, graph: nx.Graph) -> DetectionResult:
        """
        Detect anomalies in graph using spectral analysis.

        Args:
            graph: Current swarm graph to analyze

        Returns:
            DetectionResult with flagged UAVs and confidence scores
        """
        start_time = time.time()

        # Compute current spectrum (eigenvalues and eigenvectors)
        current_eigenvalues, current_eigenvectors = self._compute_spectrum(graph)

        # Compute anomaly scores for each node
        confidence_scores = {}
        anomalous_uav_ids = set()

        if self.mean_eigenvalues is None or len(current_eigenvalues) == 0:
            # Not trained or empty graph
            detection_time = time.time() - start_time
            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=set(),
                confidence_scores={uid: 0.0 for uid in graph.nodes()},
                ground_truth={},
                detection_time=detection_time,
            )

        # Check algebraic connectivity deviation
        algebraic_connectivity = (
            current_eigenvalues[1] if len(current_eigenvalues) > 1 else 0.0
        )
        ac_z_score = abs(algebraic_connectivity - self.mean_algebraic_connectivity) / (
            self.std_algebraic_connectivity + 1e-10
        )

        # Compute eigenvector residuals if enabled
        eigenvector_residuals = {}
        if (
            self.use_eigenvector_residuals
            and self.baseline_subspace is not None
            and current_eigenvectors is not None
        ):
            eigenvector_residuals = self._compute_eigenvector_residuals(
                graph, current_eigenvectors
            )

        # Compute per-node scores based on multiple factors
        degrees = dict(graph.degree())
        mean_degree = np.mean(list(degrees.values())) if degrees else 0
        std_degree = np.std(list(degrees.values())) if degrees else 1

        # Get positions for topology validation
        positions = {}
        for node in graph.nodes():
            node_data = graph.nodes[node]
            if "uav" in node_data:
                positions[node] = node_data["uav"].position

        for node in graph.nodes():
            # Z-score based on degree deviation
            degree = degrees.get(node, 0)
            degree_z_score = abs(degree - mean_degree) / (std_degree + 1e-10)

            # Eigenvector residual score
            ev_residual_score = eigenvector_residuals.get(node, 0.0)

            # Position-based topology score
            position_score = self._compute_position_anomaly_score(
                node, positions, graph
            )

            # Physics violation score (detects impossible movements)
            physics_score = self._compute_physics_violation_score(
                node, positions, graph, time.time()
            )

            # Combine scores with weights
            combined_score = (
                0.25 * degree_z_score  # Degree centrality
                + 0.25 * ac_z_score  # Global connectivity
                + 0.20 * ev_residual_score  # Eigenvector residual
                + 0.15 * position_score  # Position anomaly
                + 0.15 * physics_score  # Physics violations (NEW!)
            )

            confidence_scores[node] = float(combined_score)

            # Flag if above threshold
            if combined_score > self.threshold:
                anomalous_uav_ids.add(node)

        # Get ground truth from graph node attributes if available
        ground_truth = {}
        for node in graph.nodes():
            node_data = graph.nodes[node]
            if "uav" in node_data:
                uav = node_data["uav"]
                ground_truth[node] = uav.is_legitimate
            else:
                ground_truth[node] = True  # Assume legitimate if no data

        detection_time = time.time() - start_time

        logger.debug(
            f"Spectral detection: {len(anomalous_uav_ids)} anomalies detected "
            f"(AC z-score: {ac_z_score:.2f})"
        )

        return DetectionResult(
            detector_name=self.name,
            timestamp=time.time(),
            anomalous_uav_ids=anomalous_uav_ids,
            confidence_scores=confidence_scores,
            ground_truth=ground_truth,
            detection_time=detection_time,
        )

    def _compute_eigenvalues(self, graph: nx.Graph) -> np.ndarray:
        """
        Compute sorted eigenvalues of graph Laplacian.

        Args:
            graph: NetworkX graph

        Returns:
            Sorted eigenvalues (ascending order)
        """
        eigenvalues, _ = self._compute_spectrum(graph)
        return eigenvalues

    def _compute_spectrum(
        self, graph: nx.Graph
    ) -> tuple[np.ndarray, np.ndarray | None]:
        """
        Compute eigenvalues and eigenvectors of graph Laplacian.

        Args:
            graph: NetworkX graph

        Returns:
            Tuple of (eigenvalues, eigenvectors) or (eigenvalues, None)
        """
        if len(graph.nodes()) == 0:
            return np.array([]), None

        try:
            # Compute Laplacian matrix
            laplacian = nx.laplacian_matrix(graph).toarray()

            # Compute full eigendecomposition if needed
            if self.use_eigenvector_residuals:
                eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
                # Sort ascending
                sort_idx = np.argsort(eigenvalues)
                eigenvalues = eigenvalues[sort_idx]
                eigenvectors = eigenvectors[:, sort_idx]
                return eigenvalues, eigenvectors
            else:
                # Just eigenvalues
                eigenvalues = np.linalg.eigvalsh(laplacian)
                eigenvalues = np.sort(eigenvalues)
                return eigenvalues, None

        except Exception as e:
            logger.error(f"Error computing spectrum: {e}")
            return np.array([]), None

    def _compute_eigenvector_residuals(
        self, graph: nx.Graph, current_eigenvectors: np.ndarray
    ) -> dict[str, float]:
        """
        Compute eigenvector residuals for anomaly detection.

        Measures how well each node fits the baseline subspace.

        Args:
            graph: Current graph
            current_eigenvectors: Current eigenvector matrix

        Returns:
            Mapping of node ID to residual score
        """
        residuals = {}

        if self.baseline_subspace is None or current_eigenvectors is None:
            return {node: 0.0 for node in graph.nodes()}

        try:
            # Get dimensions
            n_nodes = len(graph.nodes())
            k = min(self.baseline_subspace.shape[1], current_eigenvectors.shape[1])

            if k == 0 or n_nodes != current_eigenvectors.shape[0]:
                return {node: 0.0 for node in graph.nodes()}

            # Extract first k eigenvectors
            current_subspace = current_eigenvectors[:, :k]

            # Compute subspace projection residuals for each node
            node_list = list(graph.nodes())

            for i, node in enumerate(node_list):
                # Get node's eigenvector entries
                node_vec = current_subspace[i, :]

                # Project onto baseline subspace
                if self.baseline_subspace.shape[0] > i:
                    baseline_vec = self.baseline_subspace[i, :]
                    # Compute residual (difference)
                    residual = np.linalg.norm(node_vec - baseline_vec)
                    residuals[node] = float(residual)
                else:
                    # Node not in baseline (phantom UAV)
                    residuals[node] = 10.0  # High anomaly score

        except Exception as e:
            logger.debug(f"Error computing eigenvector residuals: {e}")
            return {node: 0.0 for node in graph.nodes()}

        return residuals

    def _compute_position_anomaly_score(
        self, node: str, positions: dict[str, tuple], graph: nx.Graph
    ) -> float:
        """
        Compute position-based anomaly score.

        Detects position spoofing by checking if reported position
        is consistent with graph topology.

        Args:
            node: Node ID
            positions: Mapping of node ID to position
            graph: Current graph

        Returns:
            Anomaly score (higher = more suspicious)
        """
        if node not in positions:
            return 0.0

        node_pos = np.array(positions[node])
        neighbors = list(graph.neighbors(node))

        if not neighbors:
            # Isolated node is suspicious
            return 2.0

        # Check distance consistency
        inconsistencies = 0
        total_checks = 0

        for neighbor in neighbors:
            if neighbor not in positions:
                continue

            neighbor_pos = np.array(positions[neighbor])
            distance = np.linalg.norm(node_pos - neighbor_pos)

            # If connected but very far apart, that's suspicious
            # (Assumes communication range constraint)
            if distance > 150.0:  # Typical UAV communication range in meters
                inconsistencies += 1

            total_checks += 1

        if total_checks == 0:
            return 0.0

        # Return fraction of inconsistent connections
        return float(inconsistencies / total_checks) * 3.0  # Scale up

    def _compute_physics_violation_score(
        self,
        node: str,
        positions: dict[str, tuple],
        graph: nx.Graph,
        current_time: float,
    ) -> float:
        """
        Compute physics-based anomaly score by checking for impossible movements.

        Detects position spoofing by identifying physically impossible accelerations
        or velocities that violate UAV dynamics constraints.

        Args:
            node: Node ID
            positions: Mapping of node ID to position
            graph: Current graph
            current_time: Current timestamp

        Returns:
            Anomaly score (higher = more suspicious)
        """
        if not self.enable_physics_validation or node not in positions:
            return 0.0

        current_pos = np.array(positions[node])

        # First observation - store and return
        if node not in self.previous_positions:
            self.previous_positions[node] = positions[node]
            self.previous_timestamp = current_time
            return 0.0

        # Compute time delta
        dt = current_time - self.previous_timestamp
        if dt <= 0:
            return 0.0

        # Compute velocity
        prev_pos = np.array(self.previous_positions[node])
        displacement = current_pos - prev_pos
        current_velocity = displacement / dt
        speed = np.linalg.norm(current_velocity)

        # Check for excessive speed
        speed_violation = max(0.0, (speed - self.max_speed) / self.max_speed)

        # Check for excessive acceleration (if we have previous velocity)
        accel_violation = 0.0
        if node in self.previous_velocities:
            prev_velocity = np.array(self.previous_velocities[node])
            acceleration = (current_velocity - prev_velocity) / dt
            accel_magnitude = np.linalg.norm(acceleration)
            accel_violation = max(
                0.0, (accel_magnitude - self.max_acceleration) / self.max_acceleration
            )

        # Update tracking
        self.previous_positions[node] = positions[node]
        self.previous_velocities[node] = tuple(current_velocity)
        self.previous_timestamp = current_time

        # Combine violations
        physics_score = speed_violation * 2.0 + accel_violation * 3.0

        return min(5.0, physics_score)  # Cap at 5.0
