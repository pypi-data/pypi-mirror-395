"""
Metrics calculation for detection and performance evaluation.

Provides quantitative evaluation of detection algorithms and system performance.
"""

from typing import Tuple

import numpy as np


class MetricsCalculator:
    """
    Computes detection and performance metrics.

    Provides static methods for computing TPR, FPR, ROC curves, and consensus error.
    """

    @staticmethod
    def compute_detection_metrics(
        predictions: set[str], ground_truth: dict[str, bool]
    ) -> dict[str, float]:
        """
        Compute TPR, FPR, precision, recall, F1.

        Args:
            predictions: Set of flagged UAV IDs
            ground_truth: Mapping of UAV ID to is_legitimate flag

        Returns:
            Dictionary with metric values
        """
        # True Positives: Spoofed UAVs correctly flagged
        tp = sum(1 for uid in predictions if not ground_truth.get(uid, True))

        # False Positives: Legitimate UAVs incorrectly flagged
        fp = sum(1 for uid in predictions if ground_truth.get(uid, True))

        # False Negatives: Spoofed UAVs missed
        fn = sum(
            1
            for uid, is_legit in ground_truth.items()
            if not is_legit and uid not in predictions
        )

        # True Negatives: Legitimate UAVs correctly not flagged
        tn = sum(
            1
            for uid, is_legit in ground_truth.items()
            if is_legit and uid not in predictions
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
            "tp": tp,
            "fp": fp,
            "tn": tn,
            "fn": fn,
        }

    @staticmethod
    def compute_roc_curve(
        confidence_scores: dict[str, float],
        ground_truth: dict[str, bool],
        num_points: int = 100,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute ROC curve points by varying threshold.

        Args:
            confidence_scores: Anomaly score per UAV (higher = more anomalous)
            ground_truth: True labels (legitimate=True, spoofed=False)
            num_points: Number of threshold points to evaluate

        Returns:
            Tuple of (fpr_array, tpr_array)
        """
        # Get all confidence scores
        scores = list(confidence_scores.values())

        if not scores:
            return np.array([0.0, 1.0]), np.array([0.0, 1.0])

        # Generate thresholds from min to max score
        min_score = min(scores)
        max_score = max(scores)
        thresholds = np.linspace(min_score, max_score, num_points)

        fpr_list = []
        tpr_list = []

        for threshold in thresholds:
            # Flag UAVs above threshold
            predictions = {
                uid for uid, score in confidence_scores.items() if score >= threshold
            }

            # Compute TPR and FPR
            metrics = MetricsCalculator.compute_detection_metrics(
                predictions, ground_truth
            )
            fpr_list.append(metrics["fpr"])
            tpr_list.append(metrics["tpr"])

        # Add corner points
        fpr_array = np.array([0.0] + fpr_list + [1.0])
        tpr_array = np.array([0.0] + tpr_list + [1.0])

        return fpr_array, tpr_array

    @staticmethod
    def compute_consensus_error(values: np.ndarray, true_average: float) -> float:
        """
        Compute L2 norm of consensus error.

        Args:
            values: Current consensus values per UAV
            true_average: True average without attack

        Returns:
            Consensus error magnitude (L2 distance from true average)
        """
        error_vector = values - true_average
        return float(np.linalg.norm(error_vector))

    @staticmethod
    def compute_auc(fpr: np.ndarray, tpr: np.ndarray) -> float:
        """
        Compute Area Under the ROC Curve (AUC).

        Args:
            fpr: False positive rates
            tpr: True positive rates

        Returns:
            AUC value (0.0 to 1.0)
        """
        # Sort by FPR
        sorted_indices = np.argsort(fpr)
        fpr_sorted = fpr[sorted_indices]
        tpr_sorted = tpr[sorted_indices]

        # Compute area using trapezoidal rule
        auc = np.trapz(tpr_sorted, fpr_sorted)

        return float(auc)
