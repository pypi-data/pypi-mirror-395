"""
Position falsification attack.

Falsifies GPS positions in Remote ID messages while maintaining true positions
for graph topology (simulating spoofed broadcasts vs actual location).
"""

from typing import TYPE_CHECKING

from argus_uav.attacks import AttackInjector, AttackScenario
from argus_uav.utils.logging_config import get_logger

if TYPE_CHECKING:
    from argus_uav.core.swarm import Swarm

logger = get_logger(__name__)


class PositionFalsifier(AttackInjector):
    """
    Falsifies GPS positions in Remote ID messages.

    Target UAVs report incorrect positions in their Remote ID broadcasts
    while maintaining their true positions for movement and graph connectivity.
    This simulates GPS spoofing or malicious position reporting.
    """

    def __init__(self):
        """Initialize position falsifier."""
        super().__init__()
        self.target_uav_ids: set[str] = set()
        self.position_offsets: dict[str, tuple[float, float, float]] = {}
        self.injected = False

    def inject(
        self, swarm: "Swarm", scenario: AttackScenario, current_time: float
    ) -> None:
        """
        Modify reported positions of target UAVs.

        Args:
            swarm: Target swarm to attack
            scenario: Attack configuration
            current_time: Current simulation time

        Effects:
            - Selects target UAVs (random or specified)
            - Generates position offsets for falsification
            - Stores mappings for broadcast interception

        Note:
            Actual position falsification happens during message broadcasting.
            This method sets up the attack parameters.
        """
        # Only inject once at attack start
        if self.injected:
            return

        # Select target UAVs
        if scenario.target_uav_ids is not None:
            # Use specified targets
            self.target_uav_ids = set(scenario.target_uav_ids)
        else:
            # Random selection based on intensity
            all_legitimate_uavs = [
                uav_id for uav_id, uav in swarm.uavs.items() if uav.is_legitimate
            ]
            num_targets = max(1, int(len(all_legitimate_uavs) * scenario.intensity))
            self.target_uav_ids = set(
                swarm.rng.choice(all_legitimate_uavs, size=num_targets, replace=False)
            )

        # Generate random position offsets for each target
        magnitude = scenario.falsification_magnitude
        for uav_id in self.target_uav_ids:
            # Random direction with fixed magnitude
            offset = (
                float(swarm.rng.uniform(-magnitude, magnitude)),
                float(swarm.rng.uniform(-magnitude, magnitude)),
                float(
                    swarm.rng.uniform(-magnitude / 2, magnitude / 2)
                ),  # Less vertical
            )
            self.position_offsets[uav_id] = offset

            logger.info(
                f"Target UAV {uav_id} will report falsified position "
                f"with offset {offset}"
            )

        # Mark targeted UAVs as compromised (for ground truth)
        for uav_id in self.target_uav_ids:
            if uav_id in swarm.uavs:
                swarm.uavs[uav_id].is_legitimate = False

        # Update ground truth
        self._update_ground_truth(swarm)

        self.injected = True
        logger.info(
            f"Position falsification attack: {len(self.target_uav_ids)} "
            f"UAVs compromised with magnitude {magnitude}m"
        )

    def _update_ground_truth(self, swarm: "Swarm") -> None:
        """Update ground truth labels for all UAVs."""
        self.ground_truth = {
            uav_id: uav.is_legitimate for uav_id, uav in swarm.uavs.items()
        }

    def get_ground_truth(self) -> dict[str, bool]:
        """
        Returns ground truth labels for all UAVs.

        Returns:
            Mapping of UAV ID to is_legitimate flag
        """
        return self.ground_truth.copy()

    def apply_falsification(
        self, uav_id: str, true_position: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        """
        Apply position falsification to a UAV's reported position.

        Args:
            uav_id: UAV identifier
            true_position: True position (x, y, z)

        Returns:
            Falsified position with offset applied
        """
        if uav_id not in self.position_offsets:
            return true_position

        offset = self.position_offsets[uav_id]
        falsified = (
            true_position[0] + offset[0],
            true_position[1] + offset[1],
            true_position[2] + offset[2],
        )
        return falsified

    def restore_positions(self, swarm: "Swarm") -> None:
        """
        Restore legitimate status to compromised UAVs.

        Args:
            swarm: Swarm to restore
        """
        for uav_id in self.target_uav_ids:
            if uav_id in swarm.uavs:
                swarm.uavs[uav_id].is_legitimate = True

        self.target_uav_ids.clear()
        self.position_offsets.clear()
        self.injected = False
        logger.info("Position falsification removed, UAVs restored to legitimate")
