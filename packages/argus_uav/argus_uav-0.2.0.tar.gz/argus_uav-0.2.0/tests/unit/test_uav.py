"""
Unit tests for UAV class.

Tests UAV initialization, movement, and message broadcasting.
"""

import time

import pytest

from argus_uav.core.uav import UAV


@pytest.mark.unit
def test_uav_initialization(sample_uav_id, sample_position, sample_velocity):
    """Test UAV initializes with correct attributes."""
    uav = UAV(uav_id=sample_uav_id, position=sample_position, velocity=sample_velocity)

    assert uav.uav_id == sample_uav_id
    assert uav.position == sample_position
    assert uav.velocity == sample_velocity
    assert uav.is_legitimate is True
    assert uav.private_key is None
    assert uav.public_key is None
    assert isinstance(uav.message_queue, list)
    assert len(uav.message_queue) == 0


@pytest.mark.unit
def test_uav_movement(sample_uav_id, test_bounds):
    """Test UAV moves correctly based on velocity."""
    uav = UAV(
        uav_id=sample_uav_id, position=(500.0, 500.0, 100.0), velocity=(10.0, 5.0, 0.0)
    )

    # Move for 1 second
    uav.move(dt=1.0, bounds=test_bounds)

    # Check new position
    assert uav.position == (510.0, 505.0, 100.0)


@pytest.mark.unit
def test_uav_boundary_reflection(sample_uav_id, test_bounds):
    """Test UAV reflects off boundaries."""
    # Start near edge moving toward boundary
    uav = UAV(
        uav_id=sample_uav_id, position=(995.0, 500.0, 100.0), velocity=(10.0, 0.0, 0.0)
    )

    # Move past boundary
    uav.move(dt=1.0, bounds=test_bounds)

    # Should reflect and reverse velocity
    assert uav.position[0] == 1000.0  # Clamped to boundary
    assert uav.velocity[0] == -10.0  # Velocity reversed


@pytest.mark.unit
def test_uav_broadcast_remote_id(sample_uav_id, sample_position, sample_velocity):
    """Test UAV broadcasts Remote ID message."""
    uav = UAV(uav_id=sample_uav_id, position=sample_position, velocity=sample_velocity)

    timestamp = time.time()
    message = uav.broadcast_remote_id(timestamp)

    assert message.uav_id == sample_uav_id
    assert message.timestamp == timestamp
    assert message.velocity == sample_velocity
    assert message.is_spoofed is False
    assert len(uav.message_queue) == 1


@pytest.mark.unit
def test_phantom_uav_flag():
    """Test phantom UAV is marked as illegitimate."""
    phantom = UAV(
        uav_id="PHANTOM-001",
        position=(0.0, 0.0, 0.0),
        velocity=(0.0, 0.0, 0.0),
        is_legitimate=False,
    )

    assert phantom.is_legitimate is False

    message = phantom.broadcast_remote_id(time.time())
    assert message.is_spoofed is True
