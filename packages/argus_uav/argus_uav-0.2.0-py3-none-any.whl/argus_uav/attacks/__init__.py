"""Attack injection modules for spoofing scenarios."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from argus_uav.core.swarm import Swarm


class AttackType(Enum):
    """Types of Remote ID spoofing attacks."""

    PHANTOM = "phantom"
    POSITION_FALSIFICATION = "position"
    COORDINATED = "coordinated"


@dataclass
class AttackScenario:
    """
    Configuration for attack injection.

    Attributes:
        attack_type: Type of attack to inject
        start_time: When to start attack (seconds)
        duration: Attack duration (seconds)
        intensity: Attack intensity (0.0 to 1.0)
        target_uav_ids: Specific UAVs to target (None = random)
        phantom_count: Number of phantom UAVs for PHANTOM attack
        falsification_magnitude: Position offset in meters for POSITION attack
        coordination_pattern: Movement pattern for COORDINATED attack
    """

    attack_type: AttackType
    start_time: float
    duration: float
    intensity: float = 0.1
    target_uav_ids: Optional[list[str]] = None
    phantom_count: int = 0
    falsification_magnitude: float = 0.0
    coordination_pattern: Optional[str] = None

    def is_active(self, current_time: float) -> bool:
        """
        Check if attack is currently active.

        Args:
            current_time: Current simulation time

        Returns:
            True if attack is active, False otherwise
        """
        return self.start_time <= current_time < self.start_time + self.duration


class AttackInjector(ABC):
    """
    Base class for attack injection strategies.

    All attack injectors must implement inject() and get_ground_truth().
    """

    def __init__(self):
        """Initialize attack injector."""
        self.ground_truth: dict[str, bool] = {}

    @abstractmethod
    def inject(
        self, swarm: "Swarm", scenario: AttackScenario, current_time: float
    ) -> None:
        """
        Inject attack into swarm simulation.

        Args:
            swarm: Target swarm to attack
            scenario: Attack configuration
            current_time: Current simulation time

        Effects:
            Modifies swarm state (adds phantoms, alters positions, etc.)
        """
        pass

    @abstractmethod
    def get_ground_truth(self) -> dict[str, bool]:
        """
        Returns ground truth labels for all UAVs.

        Returns:
            Mapping of UAV ID to is_legitimate flag
        """
        pass


__all__ = [
    "AttackType",
    "AttackScenario",
    "AttackInjector",
]
