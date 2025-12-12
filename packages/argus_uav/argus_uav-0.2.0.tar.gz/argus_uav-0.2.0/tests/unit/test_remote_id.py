"""
Unit tests for RemoteIDMessage class.

Tests message creation, serialization, and validation.
"""

import time

import pytest

from argus_uav.core.remote_id import RemoteIDMessage


@pytest.mark.unit
def test_remote_id_message_creation():
    """Test RemoteIDMessage initializes correctly."""
    msg = RemoteIDMessage(
        uav_id="UAV-001",
        timestamp=time.time(),
        latitude=37.7749,
        longitude=-122.4194,
        altitude=100.0,
        velocity=(5.0, 3.0, 0.0),
    )

    assert msg.uav_id == "UAV-001"
    assert msg.latitude == pytest.approx(37.7749)
    assert msg.longitude == pytest.approx(-122.4194)
    assert msg.altitude == 100.0
    assert msg.velocity == (5.0, 3.0, 0.0)
    assert msg.signature is None
    assert msg.is_spoofed is False


@pytest.mark.unit
def test_remote_id_latitude_validation():
    """Test latitude validation rejects invalid values."""
    with pytest.raises(ValueError, match="Latitude.*out of range"):
        RemoteIDMessage(
            uav_id="UAV-001",
            timestamp=time.time(),
            latitude=95.0,  # Invalid: > 90
            longitude=-122.0,
            altitude=100.0,
            velocity=(0.0, 0.0, 0.0),
        )


@pytest.mark.unit
def test_remote_id_longitude_validation():
    """Test longitude validation rejects invalid values."""
    with pytest.raises(ValueError, match="Longitude.*out of range"):
        RemoteIDMessage(
            uav_id="UAV-001",
            timestamp=time.time(),
            latitude=37.0,
            longitude=-185.0,  # Invalid: < -180
            altitude=100.0,
            velocity=(0.0, 0.0, 0.0),
        )


@pytest.mark.unit
def test_remote_id_altitude_validation():
    """Test altitude validation rejects negative values."""
    with pytest.raises(ValueError, match="Altitude.*must be >= 0"):
        RemoteIDMessage(
            uav_id="UAV-001",
            timestamp=time.time(),
            latitude=37.0,
            longitude=-122.0,
            altitude=-10.0,  # Invalid: negative
            velocity=(0.0, 0.0, 0.0),
        )


@pytest.mark.unit
def test_remote_id_serialization():
    """Test message serialization and deserialization."""
    original = RemoteIDMessage(
        uav_id="UAV-TEST",
        timestamp=12345.678,
        latitude=37.7749,
        longitude=-122.4194,
        altitude=100.0,
        velocity=(5.0, 3.0, 0.0),
    )

    # Serialize
    msg_bytes = original.to_bytes()
    assert isinstance(msg_bytes, bytes)
    assert len(msg_bytes) > 0

    # Deserialize
    restored = RemoteIDMessage.from_bytes(msg_bytes)

    assert restored.uav_id == original.uav_id
    assert restored.timestamp == pytest.approx(original.timestamp)
    assert restored.latitude == pytest.approx(original.latitude)
    assert restored.longitude == pytest.approx(original.longitude)
    assert restored.altitude == pytest.approx(original.altitude)


@pytest.mark.unit
def test_remote_id_signature_validation():
    """Test signature field must be exactly 64 bytes."""
    with pytest.raises(ValueError, match="Signature must be exactly 64 bytes"):
        RemoteIDMessage(
            uav_id="UAV-001",
            timestamp=time.time(),
            latitude=37.0,
            longitude=-122.0,
            altitude=100.0,
            velocity=(0.0, 0.0, 0.0),
            signature=b"short",  # Invalid: not 64 bytes
        )
