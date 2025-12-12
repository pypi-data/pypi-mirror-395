"""
Argus: A UAV Remote ID Spoofing Defense System

A research framework for simulating UAV swarms, injecting spoofing attacks,
and evaluating graph-theoretic and cryptographic defense mechanisms.
"""

# Expose main classes for convenient imports
from argus_uav.core.remote_id import RemoteIDMessage
from argus_uav.core.swarm import Swarm
from argus_uav.core.uav import UAV

__all__ = [
    "Swarm",
    "UAV",
    "RemoteIDMessage",
    "__version__",
]
