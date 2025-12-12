"""Evaluation modules for metrics and visualization."""

from dataclasses import dataclass


@dataclass
class DetectionResult:
    """
    Output of a detection algorithm.

    Attributes:
        detector_name: Name of detection algorithm used
        timestamp: When detection was performed
        anomalous_uav_ids: UAVs flagged as suspicious
        confidence_scores: Anomaly score per UAV (0-1)
        ground_truth: True labels (legitimate=True, spoofed=False)
        detection_time: Algorithm execution time in seconds
    """

    detector_name: str
    timestamp: float
    anomalous_uav_ids: set[str]
    confidence_scores: dict[str, float]
    ground_truth: dict[str, bool]
    detection_time: float

    def compute_metrics(self) -> dict[str, float]:
        """
        Compute TPR, FPR, precision, recall, F1.

        Returns:
            Dictionary with metric values

        Metrics:
            - tpr (True Positive Rate / Recall): TP / (TP + FN)
            - fpr (False Positive Rate): FP / (FP + TN)
            - precision: TP / (TP + FP)
            - recall: Same as TPR
            - f1: Harmonic mean of precision and recall
            - detection_time: Time taken for detection
        """
        # True Positives: Spoofed UAVs correctly flagged
        tp = sum(
            1 for uid in self.anomalous_uav_ids if not self.ground_truth.get(uid, True)
        )

        # False Positives: Legitimate UAVs incorrectly flagged
        fp = sum(
            1 for uid in self.anomalous_uav_ids if self.ground_truth.get(uid, True)
        )

        # False Negatives: Spoofed UAVs missed
        fn = sum(
            1
            for uid, is_legit in self.ground_truth.items()
            if not is_legit and uid not in self.anomalous_uav_ids
        )

        # True Negatives: Legitimate UAVs correctly not flagged
        tn = sum(
            1
            for uid, is_legit in self.ground_truth.items()
            if is_legit and uid not in self.anomalous_uav_ids
        )

        # Compute rates
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tpr
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        return {
            "tpr": tpr,
            "fpr": fpr,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "detection_time": self.detection_time,
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn,
        }


__all__ = ["DetectionResult"]
