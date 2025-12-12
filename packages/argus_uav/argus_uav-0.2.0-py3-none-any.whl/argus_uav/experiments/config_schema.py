"""
Experiment configuration schema with Pydantic validation.

Defines the structure and validation rules for experiment configurations.
"""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from argus_uav.attacks import AttackScenario


class ExperimentConfig(BaseModel):
    """
    Complete configuration for a reproducible experiment.

    Attributes:
        experiment_name: Human-readable identifier
        random_seed: Seed for reproducibility
        swarm_size: Number of legitimate UAVs
        comm_range: Communication range in meters
        simulation_duration: Total simulation time in seconds
        update_frequency: State update rate in Hz
        attack_scenario: Attack configuration (optional)
        enable_crypto: Whether to use Ed25519 signing
        detection_methods: List of detectors to run
        output_dir: Where to save results
    """

    experiment_name: str
    random_seed: int = 42
    swarm_size: int = Field(ge=10, le=200)
    comm_range: float = Field(gt=0)
    simulation_duration: float = Field(gt=0)
    update_frequency: float = Field(gt=0)
    attack_scenario: Optional[AttackScenario] = None
    enable_crypto: bool = False
    detection_methods: list[str] = []
    output_dir: Path = Path("results")

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True

    def validate_detectors(self) -> bool:
        """
        Validate that detection method names are recognized.

        Returns:
            True if all detector names are valid
        """
        valid_detectors = {"spectral", "centrality", "node2vec", "crypto"}
        invalid = set(self.detection_methods) - valid_detectors

        if invalid:
            raise ValueError(
                f"Invalid detection methods: {invalid}. "
                f"Valid options: {valid_detectors}"
            )

        return True

    def get_output_path(self, filename: str) -> Path:
        """
        Get full path for an output file.

        Args:
            filename: Name of output file

        Returns:
            Full path in output directory
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir / filename
