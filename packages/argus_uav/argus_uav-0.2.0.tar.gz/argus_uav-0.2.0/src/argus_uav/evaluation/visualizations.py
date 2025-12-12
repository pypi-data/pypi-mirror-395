"""
Visualization utilities for publication-quality plots.

Generates ROC curves, comparison charts, confusion matrices, and time series plots.
"""

# Set matplotlib backend to Qt5 for better interactive support
import matplotlib

try:
    matplotlib.use("QtAgg")
except ImportError:
    # Fall back to default if Qt5 not available
    pass

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Plotter:
    """
    Generate publication-quality plots for research papers.

    Uses matplotlib and seaborn with academic paper styling and
    colorblind-friendly palettes.
    """

    @staticmethod
    def setup_style():
        """
        Configure matplotlib for publication-quality figures.

        Sets academic paper style with colorblind-friendly colors.
        """
        # Use seaborn style for clean academic look
        plt.style.use("seaborn-v0_8-paper")

        # Set colorblind-friendly palette
        sns.set_palette("colorblind")

        # Configure font sizes for readability
        plt.rcParams.update(
            {
                "font.size": 11,
                "axes.labelsize": 12,
                "axes.titlesize": 13,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
                "figure.titlesize": 14,
                "figure.dpi": 100,
                "savefig.dpi": 300,  # High resolution for papers
                "savefig.bbox": "tight",
                "savefig.pad_inches": 0.1,
            }
        )

    @staticmethod
    def plot_roc_curve(
        fpr: np.ndarray,
        tpr: np.ndarray,
        detector_name: str,
        output_path: Path,
        auc: Optional[float] = None,
    ) -> None:
        """
        Create and save ROC curve plot.

        Args:
            fpr: False positive rates
            tpr: True positive rates
            detector_name: Name for legend
            output_path: Where to save figure (PNG and PDF)
            auc: Optional AUC value to display
        """
        Plotter.setup_style()

        fig, ax = plt.subplots(figsize=(6, 5))

        # Plot ROC curve
        label = detector_name
        if auc is not None:
            label = f"{detector_name} (AUC = {auc:.3f})"

        ax.plot(fpr, tpr, linewidth=2, label=label)

        # Plot diagonal (random classifier)
        ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="Random")

        # Labels and formatting
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title(f"ROC Curve: {detector_name}")
        ax.legend(loc="lower right")
        ax.grid(True, alpha=0.3)
        ax.set_xlim([-0.05, 1.05])
        ax.set_ylim([-0.05, 1.05])

        # Save both PNG and PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path).replace(".png", ".png"), dpi=300)
        plt.savefig(str(output_path).replace(".png", ".pdf"))
        plt.close()

    @staticmethod
    def plot_roc_curves_comparison(
        results: dict[str, tuple[np.ndarray, np.ndarray, float]], output_path: Path
    ) -> None:
        """
        Plot multiple ROC curves on same axes for comparison.

        Args:
            results: Dict of {detector_name: (fpr, tpr, auc)}
            output_path: Where to save figure
        """
        Plotter.setup_style()

        fig, ax = plt.subplots(figsize=(7, 6))

        # Plot each detector's ROC curve
        colors = sns.color_palette("colorblind", len(results))
        for (detector_name, (fpr, tpr, auc)), color in zip(results.items(), colors):
            ax.plot(
                fpr,
                tpr,
                linewidth=2.5,
                label=f"{detector_name} (AUC={auc:.3f})",
                color=color,
            )

        # Plot diagonal
        ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="Random")

        # Labels and formatting
        ax.set_xlabel("False Positive Rate", fontsize=12)
        ax.set_ylabel("True Positive Rate", fontsize=12)
        ax.set_title("ROC Curve Comparison: Detection Methods", fontsize=14)
        ax.legend(loc="lower right", frameon=True, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([-0.05, 1.05])
        ax.set_ylim([-0.05, 1.05])

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path).replace(".png", ".png"), dpi=300)
        plt.savefig(str(output_path).replace(".png", ".pdf"))
        plt.close()

    @staticmethod
    def plot_detection_comparison(
        results: dict[str, dict[str, float]], output_path: Path
    ) -> None:
        """
        Bar chart comparing detection methods across metrics.

        Args:
            results: {detector_name: {metric_name: value}}
            output_path: Where to save figure
        """
        Plotter.setup_style()

        # Extract metrics
        detectors = list(results.keys())
        metrics = ["tpr", "fpr", "precision", "f1"]
        metric_labels = ["TPR", "FPR", "Precision", "F1 Score"]

        # Create subplots for each metric
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        axes = axes.flatten()

        for idx, (metric, label) in enumerate(zip(metrics, metric_labels)):
            ax = axes[idx]

            values = [results[det].get(metric, 0.0) for det in detectors]

            # Create bar chart
            bars = ax.bar(detectors, values, alpha=0.8)

            # Color bars
            colors = sns.color_palette("colorblind", len(detectors))
            for bar, color in zip(bars, colors):
                bar.set_color(color)

            # Labels
            ax.set_ylabel(label, fontsize=11)
            ax.set_title(f"{label} by Detection Method", fontsize=12)
            ax.set_ylim([0, 1.1])
            ax.grid(True, alpha=0.3, axis="y")

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{height:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

        plt.tight_layout()

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path).replace(".png", ".png"), dpi=300)
        plt.savefig(str(output_path).replace(".png", ".pdf"))
        plt.close()

    @staticmethod
    def plot_confusion_matrix(
        confusion_matrix: np.ndarray,
        detector_name: str,
        output_path: Path,
        labels: Optional[list[str]] = None,
    ) -> None:
        """
        Heatmap of confusion matrix.

        Args:
            confusion_matrix: 2x2 array [[TN, FP], [FN, TP]]
            detector_name: Name for title
            output_path: Where to save figure
            labels: Class labels (default: ['Legitimate', 'Spoofed'])
        """
        Plotter.setup_style()

        if labels is None:
            labels = ["Legitimate", "Spoofed"]

        fig, ax = plt.subplots(figsize=(6, 5))

        # Create heatmap
        sns.heatmap(
            confusion_matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=labels,
            yticklabels=labels,
            cbar_kws={"label": "Count"},
            ax=ax,
        )

        ax.set_xlabel("Predicted Label", fontsize=12)
        ax.set_ylabel("True Label", fontsize=12)
        ax.set_title(f"Confusion Matrix: {detector_name}", fontsize=13)

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path).replace(".png", ".png"), dpi=300)
        plt.savefig(str(output_path).replace(".png", ".pdf"))
        plt.close()

    @staticmethod
    def plot_time_series(
        time: np.ndarray,
        values: np.ndarray,
        ylabel: str,
        title: str,
        output_path: Path,
        attack_window: Optional[tuple[float, float]] = None,
    ) -> None:
        """
        Plot time series with optional attack window highlighting.

        Args:
            time: Time values (x-axis)
            values: Metric values (y-axis)
            ylabel: Y-axis label
            title: Plot title
            output_path: Where to save figure
            attack_window: Optional (start_time, end_time) to highlight
        """
        Plotter.setup_style()

        fig, ax = plt.subplots(figsize=(8, 5))

        # Plot time series
        ax.plot(time, values, linewidth=2, color="steelblue", label="Metric")

        # Highlight attack window if provided
        if attack_window is not None:
            start, end = attack_window
            ax.axvspan(start, end, alpha=0.2, color="red", label="Attack Active")

        # Labels and formatting
        ax.set_xlabel("Time (seconds)", fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=13)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path).replace(".png", ".png"), dpi=300)
        plt.savefig(str(output_path).replace(".png", ".pdf"))
        plt.close()

    @staticmethod
    def plot_performance_comparison(
        results: dict[str, dict[str, float]], output_path: Path
    ) -> None:
        """
        Compare detection methods on performance metrics.

        Args:
            results: {detector_name: {'detection_time': ms, 'tpr': value, 'fpr': value}}
            output_path: Where to save figure
        """
        Plotter.setup_style()

        detectors = list(results.keys())
        detection_times = [
            results[det].get("detection_time", 0) * 1000 for det in detectors
        ]  # Convert to ms

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Plot 1: Detection time
        colors = sns.color_palette("colorblind", len(detectors))
        bars = ax1.bar(detectors, detection_times, alpha=0.8)
        for bar, color in zip(bars, colors):
            bar.set_color(color)

        ax1.set_ylabel("Detection Time (ms)", fontsize=11)
        ax1.set_title("Detection Latency Comparison", fontsize=12)
        ax1.grid(True, alpha=0.3, axis="y")
        ax1.axhline(
            y=100, color="red", linestyle="--", alpha=0.5, label="100ms requirement"
        )
        ax1.legend()

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.1f}ms",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        # Plot 2: Accuracy vs Speed scatter
        tprs = [results[det].get("tpr", 0) for det in detectors]

        for i, det in enumerate(detectors):
            ax2.scatter(
                detection_times[i],
                tprs[i],
                s=150,
                color=colors[i],
                alpha=0.7,
                label=det,
            )

        ax2.set_xlabel("Detection Time (ms)", fontsize=11)
        ax2.set_ylabel("True Positive Rate", fontsize=11)
        ax2.set_title("Accuracy vs. Speed Trade-off", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1.1])

        plt.tight_layout()

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path).replace(".png", ".png"), dpi=300)
        plt.savefig(str(output_path).replace(".png", ".pdf"))
        plt.close()

    @staticmethod
    def plot_metrics_heatmap(
        results: dict[str, dict[str, float]], output_path: Path
    ) -> None:
        """
        Heatmap showing all metrics for all detectors.

        Args:
            results: {detector_name: {metric_name: value}}
            output_path: Where to save figure
        """
        Plotter.setup_style()

        # Prepare data matrix
        detectors = list(results.keys())
        metrics = ["tpr", "fpr", "precision", "recall", "f1"]
        metric_labels = ["TPR", "FPR", "Precision", "Recall", "F1"]

        data = []
        for detector in detectors:
            row = [results[detector].get(m, 0.0) for m in metrics]
            data.append(row)

        data_array = np.array(data)

        # Create heatmap
        fig, ax = plt.subplots(figsize=(8, len(detectors) * 0.8 + 1))

        sns.heatmap(
            data_array,
            annot=True,
            fmt=".3f",
            cmap="RdYlGn",
            xticklabels=metric_labels,
            yticklabels=detectors,
            vmin=0,
            vmax=1,
            cbar_kws={"label": "Metric Value"},
            ax=ax,
        )

        ax.set_title("Detection Performance Heatmap", fontsize=13)
        plt.tight_layout()

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path).replace(".png", ".png"), dpi=300)
        plt.savefig(str(output_path).replace(".png", ".pdf"))
        plt.close()

    @staticmethod
    def create_summary_table(
        results: dict[str, dict[str, float]], output_path: Path
    ) -> str:
        """
        Generate markdown/LaTeX table of results.

        Args:
            results: {detector_name: {metric_name: value}}
            output_path: Where to save table (markdown format)

        Returns:
            Markdown table string
        """
        # Build markdown table
        table_lines = []
        table_lines.append(
            "| Detector | TPR | FPR | Precision | Recall | F1 | Detection Time (ms) |"
        )
        table_lines.append(
            "|----------|-----|-----|-----------|--------|----|--------------------|"
        )

        for detector, metrics in results.items():
            tpr = metrics.get("tpr", 0.0)
            fpr = metrics.get("fpr", 0.0)
            precision = metrics.get("precision", 0.0)
            recall = metrics.get("recall", 0.0)
            f1 = metrics.get("f1", 0.0)
            det_time = metrics.get("detection_time", 0.0) * 1000

            table_lines.append(
                f"| {detector} | {tpr:.3f} | {fpr:.3f} | {precision:.3f} | "
                f"{recall:.3f} | {f1:.3f} | {det_time:.2f} |"
            )

        table_str = "\n".join(table_lines)

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write("# Detection Performance Summary\n\n")
            f.write(table_str)
            f.write("\n")

        return table_str


# Initialize style on module import
Plotter.setup_style()
