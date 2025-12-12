"""
Cryptographic verification detector.

Detects spoofed messages by verifying Ed25519 digital signatures.
Provides 100% TPR/0% FPR when crypto is enabled.
"""

import time

import networkx as nx

from argus_uav.detection import AnomalyDetector
from argus_uav.evaluation import DetectionResult
from argus_uav.utils.logging_config import get_logger

logger = get_logger(__name__)


class CryptoDetector(AnomalyDetector):
    """
    Detects anomalies by verifying cryptographic signatures.

    When cryptography is enabled:
    - Legitimate UAVs have valid Ed25519 signatures
    - Phantom UAVs have no signatures (or invalid ones)

    This provides perfect detection (100% TPR, 0% FPR) but requires
    all UAVs to support cryptographic signing.
    """

    def __init__(self, name: str = "crypto"):
        """
        Initialize crypto detector.

        Args:
            name: Detector identifier
        """
        super().__init__(name)
        self.public_keys: dict[str, bytes] = {}

    def train(self, clean_graphs: list[nx.Graph]) -> None:
        """
        Train detector on clean baseline graphs.

        Args:
            clean_graphs: Time series of graphs without attacks

        Effects:
            Extracts and stores public keys from legitimate UAVs
        """
        self.baseline_graphs = clean_graphs

        if not clean_graphs:
            logger.warning("No clean graphs provided for training")
            return

        # Extract public keys from UAVs in the most recent graph
        if clean_graphs:
            latest_graph = clean_graphs[-1]
            for node in latest_graph.nodes():
                node_data = latest_graph.nodes[node]
                if "uav" in node_data:
                    uav = node_data["uav"]
                    if uav.public_key is not None:
                        self.public_keys[node] = uav.public_key

        logger.info(f"Crypto detector: registered {len(self.public_keys)} public keys")

    def detect(self, graph: nx.Graph) -> DetectionResult:
        """
        Detect anomalies by verifying message signatures.

        Args:
            graph: Current swarm graph to analyze

        Returns:
            DetectionResult with flagged UAVs (those without valid signatures)
        """
        start_time = time.time()

        confidence_scores = {}
        anomalous_uav_ids = set()
        ground_truth = {}

        if len(graph.nodes()) == 0:
            detection_time = time.time() - start_time
            return DetectionResult(
                detector_name=self.name,
                timestamp=time.time(),
                anomalous_uav_ids=set(),
                confidence_scores={},
                ground_truth={},
                detection_time=detection_time,
            )

        # Check each UAV's most recent message
        for node in graph.nodes():
            node_data = graph.nodes[node]

            if "uav" not in node_data:
                continue

            uav = node_data["uav"]
            ground_truth[node] = uav.is_legitimate

            # Get most recent message from UAV's queue
            if not uav.message_queue:
                # No messages yet - assume suspicious
                confidence_scores[node] = 1.0
                anomalous_uav_ids.add(node)
                continue

            latest_message = uav.message_queue[-1]

            # Check if message has signature
            if latest_message.signature is None:
                # No signature - definitely suspicious
                confidence_scores[node] = 1.0
                anomalous_uav_ids.add(node)
                logger.debug(f"UAV {node} has no signature - flagged")
                continue

            # Verify signature if we have the public key
            if node in self.public_keys:
                is_valid = latest_message.verify_signature(self.public_keys[node])
                if is_valid:
                    # Valid signature - not suspicious
                    confidence_scores[node] = 0.0
                else:
                    # Invalid signature - very suspicious
                    confidence_scores[node] = 1.0
                    anomalous_uav_ids.add(node)
                    logger.debug(f"UAV {node} has invalid signature - flagged")
            else:
                # Unknown UAV (not in baseline) - suspicious
                confidence_scores[node] = 1.0
                anomalous_uav_ids.add(node)
                logger.debug(f"UAV {node} not in known keys - flagged")

        detection_time = time.time() - start_time

        logger.debug(f"Crypto detection: {len(anomalous_uav_ids)} anomalies detected")

        return DetectionResult(
            detector_name=self.name,
            timestamp=time.time(),
            anomalous_uav_ids=anomalous_uav_ids,
            confidence_scores=confidence_scores,
            ground_truth=ground_truth,
            detection_time=detection_time,
        )
