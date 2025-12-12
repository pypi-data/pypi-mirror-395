"""
Experiment orchestration and execution.

Runs complete experiments from configuration files with automated
baseline collection, attack injection, detection, and results reporting.
"""

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np
import yaml

from argus_uav.attacks import AttackType
from argus_uav.attacks.coordinated import CoordinatedInjector
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.attacks.position_spoof import PositionFalsifier
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.crypto_detector import CryptoDetector
from argus_uav.detection.ml_detection import Node2VecDetector
from argus_uav.detection.spectral import SpectralDetector
from argus_uav.evaluation.metrics import MetricsCalculator
from argus_uav.evaluation.visualizations import Plotter
from argus_uav.experiments.config_schema import ExperimentConfig
from argus_uav.utils.logging_config import get_logger
from argus_uav.utils.random_seeds import get_rng

logger = get_logger(__name__)


@dataclass
class ExperimentResults:
    """
    Complete results from an experiment run.

    Attributes:
        experiment_name: Experiment identifier
        config: Configuration used
        detection_metrics: Metrics for each detector
        graph_snapshots: Saved graph states at key times
        output_dir: Directory where results are saved
        execution_time: Total experiment duration
    """

    experiment_name: str
    config: ExperimentConfig
    detection_metrics: dict[str, dict[str, float]]
    graph_snapshots: dict[str, Any] = field(default_factory=dict)
    output_dir: Path = Path("results")
    execution_time: float = 0.0


class ExperimentRunner:
    """
    Orchestrates complete experiment execution.

    Handles initialization, baseline collection, attack injection,
    detection, metrics computation, and visualization generation.
    """

    def __init__(self, config: ExperimentConfig):
        """
        Initialize experiment runner.

        Args:
            config: Experiment configuration
        """
        self.config = config
        self.rng = get_rng(seed=config.random_seed)
        self.swarm: Optional[Swarm] = None
        self.detectors = {}
        self.attack_injector = None

        logger.info(f"Experiment runner initialized: {config.experiment_name}")

    def run(self) -> ExperimentResults:
        """
        Execute complete experiment.

        Steps:
            1. Initialize swarm from config
            2. Collect clean baseline and train detectors
            3. Run simulation with attack injection
            4. Collect detection results
            5. Compute aggregate metrics
            6. Generate visualizations
            7. Save results to output_dir

        Returns:
            ExperimentResults with all metrics and paths
        """
        start_time = time.time()

        logger.info(f"Starting experiment: {self.config.experiment_name}")

        # Step 1: Initialize swarm
        logger.info("Step 1: Initializing swarm...")
        self.swarm = Swarm(
            num_uavs=self.config.swarm_size,
            comm_range=self.config.comm_range,
            bounds=(1000, 1000, 200),  # Default bounds
            rng=self.rng,
            enable_crypto=self.config.enable_crypto,
        )

        # Step 2: Collect baseline and train detectors
        logger.info("Step 2: Collecting baseline and training detectors...")
        baseline_duration = 20  # seconds
        baseline_graphs = []

        for t in range(baseline_duration):
            self.swarm.step(dt=1.0)
            baseline_graphs.append(self.swarm.get_graph().copy())

        # Initialize and train detectors
        self._initialize_detectors()
        for detector in self.detectors.values():
            detector.train(baseline_graphs)

        logger.info(
            f"Trained {len(self.detectors)} detectors on {len(baseline_graphs)} baseline graphs"
        )

        # Step 3: Initialize attack injector
        if self.config.attack_scenario is not None:
            logger.info("Step 3: Initializing attack injector...")
            attack_type = self.config.attack_scenario.attack_type

            if attack_type == AttackType.PHANTOM:
                self.attack_injector = PhantomInjector()
            elif attack_type == AttackType.POSITION_FALSIFICATION:
                self.attack_injector = PositionFalsifier()
            elif attack_type == AttackType.COORDINATED:
                self.attack_injector = CoordinatedInjector()

        # Step 4: Run simulation with detection
        logger.info("Step 4: Running simulation with attack and detection...")
        detection_results = []

        num_steps = int(
            self.config.simulation_duration / (1.0 / self.config.update_frequency)
        )

        for step in range(num_steps):
            current_time = step / self.config.update_frequency

            # Inject attack if configured and active
            if (
                self.attack_injector is not None
                and self.config.attack_scenario is not None
                and self.config.attack_scenario.is_active(current_time)
            ):
                if not getattr(self.attack_injector, "injected", False):
                    self.attack_injector.inject(
                        self.swarm, self.config.attack_scenario, current_time
                    )
                    logger.info(f"Attack injected at t={current_time:.1f}s")

            # Step simulation
            self.swarm.step(dt=1.0 / self.config.update_frequency)

            # Run detection every second
            if step % int(self.config.update_frequency) == 0:
                current_graph = self.swarm.get_graph()

                for detector_name, detector in self.detectors.items():
                    result = detector.detect(current_graph)
                    detection_results.append((detector_name, result))

        logger.info(f"Simulation complete: {len(detection_results)} detection runs")

        # Step 5: Aggregate metrics
        logger.info("Step 5: Computing aggregate metrics...")
        aggregated_metrics = self._aggregate_detection_results(detection_results)

        # Step 6: Generate visualizations
        logger.info("Step 6: Generating visualizations...")
        self._generate_visualizations(detection_results, aggregated_metrics)

        # Step 7: Save results
        logger.info("Step 7: Saving results...")
        self._save_results(aggregated_metrics)

        execution_time = time.time() - start_time

        logger.info(f"Experiment complete in {execution_time:.1f}s")

        return ExperimentResults(
            experiment_name=self.config.experiment_name,
            config=self.config,
            detection_metrics=aggregated_metrics,
            output_dir=self.config.output_dir,
            execution_time=execution_time,
        )

    def _initialize_detectors(self) -> None:
        """Initialize detection methods based on config."""
        for method in self.config.detection_methods:
            if method == "spectral":
                self.detectors["spectral"] = SpectralDetector(threshold=1.0)
            elif method == "centrality":
                self.detectors["centrality"] = CentralityDetector(threshold=0.9)
            elif method == "crypto":
                self.detectors["crypto"] = CryptoDetector()
            elif method == "node2vec":
                self.detectors["node2vec"] = Node2VecDetector(
                    embedding_dim=64, walk_length=20, num_walks=100
                )

    def _aggregate_detection_results(
        self, detection_results: list[tuple[str, Any]]
    ) -> dict[str, dict[str, float]]:
        """
        Aggregate detection results across all time steps.

        Args:
            detection_results: List of (detector_name, DetectionResult) tuples

        Returns:
            Dict of {detector_name: aggregated_metrics}
        """
        # Group by detector
        results_by_detector = {}
        for detector_name, result in detection_results:
            if detector_name not in results_by_detector:
                results_by_detector[detector_name] = []
            results_by_detector[detector_name].append(result)

        # Compute average metrics for each detector
        aggregated = {}
        for detector_name, results in results_by_detector.items():
            # Average metrics across all time steps
            all_metrics = [r.compute_metrics() for r in results]

            if all_metrics:
                aggregated[detector_name] = {
                    "tpr": np.mean([m["tpr"] for m in all_metrics]),
                    "fpr": np.mean([m["fpr"] for m in all_metrics]),
                    "precision": np.mean([m["precision"] for m in all_metrics]),
                    "recall": np.mean([m["recall"] for m in all_metrics]),
                    "f1": np.mean([m["f1"] for m in all_metrics]),
                    "detection_time": np.mean(
                        [m["detection_time"] for m in all_metrics]
                    ),
                }

        return aggregated

    def _generate_visualizations(
        self,
        detection_results: list[tuple[str, Any]],
        aggregated_metrics: dict[str, dict[str, float]],
    ) -> None:
        """Generate all visualization plots."""
        figures_dir = self.config.output_dir / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)

        # Use last detection result for ROC curves
        latest_results = {}
        for detector_name, result in detection_results:
            latest_results[detector_name] = result

        # Generate ROC comparison
        roc_data = {}
        for detector_name, result in latest_results.items():
            fpr, tpr = MetricsCalculator.compute_roc_curve(
                result.confidence_scores, result.ground_truth
            )
            auc = MetricsCalculator.compute_auc(fpr, tpr)
            roc_data[detector_name] = (fpr, tpr, auc)

        if roc_data:
            Plotter.plot_roc_curves_comparison(
                roc_data, figures_dir / "roc_comparison.png"
            )

        # Generate detection comparison
        if aggregated_metrics:
            Plotter.plot_detection_comparison(
                aggregated_metrics, figures_dir / "detection_comparison.png"
            )

            Plotter.plot_performance_comparison(
                aggregated_metrics, figures_dir / "performance_comparison.png"
            )

            Plotter.plot_metrics_heatmap(
                aggregated_metrics, figures_dir / "metrics_heatmap.png"
            )

        logger.info(f"Visualizations saved to {figures_dir}/")

    def _save_results(self, aggregated_metrics: dict[str, dict[str, float]]) -> None:
        """Save experiment results to disk."""
        # Save configuration
        config_dict = self.config.model_dump()
        # Convert Path to string for JSON serialization
        config_dict["output_dir"] = str(config_dict["output_dir"])

        with open(self.config.output_dir / "config.yaml", "w") as f:
            yaml.dump(config_dict, f, default_flow_style=False)

        # Save metrics
        with open(self.config.output_dir / "metrics.json", "w") as f:
            json.dump(aggregated_metrics, f, indent=2)

        # Save summary table
        Plotter.create_summary_table(
            aggregated_metrics, self.config.output_dir / "results_table.md"
        )

        logger.info(f"Results saved to {self.config.output_dir}/")

    def run_parameter_sweep(
        self, param_name: str, param_values: list[Any]
    ) -> dict[Any, ExperimentResults]:
        """
        Run experiment with varying parameter.

        Args:
            param_name: Name of parameter to sweep (e.g., 'phantom_count')
            param_values: List of values to test

        Returns:
            Mapping of parameter value to results
        """
        sweep_results = {}

        logger.info(f"Starting parameter sweep: {param_name} = {param_values}")

        for value in param_values:
            logger.info(f"Running with {param_name} = {value}")

            # Modify config for this run
            if hasattr(self.config, param_name):
                setattr(self.config, param_name, value)
            elif self.config.attack_scenario is not None and hasattr(
                self.config.attack_scenario, param_name
            ):
                setattr(self.config.attack_scenario, param_name, value)

            # Update output dir
            original_output = self.config.output_dir
            self.config.output_dir = original_output / f"{param_name}_{value}"

            # Run experiment
            results = self.run()
            sweep_results[value] = results

            # Restore output dir
            self.config.output_dir = original_output

        logger.info(f"Parameter sweep complete: {len(sweep_results)} configurations")

        return sweep_results
