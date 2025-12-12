"""
Shared pytest fixtures for Argus test suite.

Provides reusable test data and objects for unit, integration, and contract tests.
"""

import numpy as np
import pytest


@pytest.fixture
def random_seed():
    """Fixed random seed for reproducible tests."""
    return 42


@pytest.fixture
def rng(random_seed):
    """NumPy random generator with fixed seed."""
    return np.random.default_rng(seed=random_seed)


@pytest.fixture
def test_bounds():
    """Standard 3D simulation bounds for tests."""
    return (1000.0, 1000.0, 200.0)  # x, y, z in meters


@pytest.fixture
def small_swarm_size():
    """Small swarm size for fast unit tests."""
    return 10


@pytest.fixture
def medium_swarm_size():
    """Medium swarm size for integration tests."""
    return 30


@pytest.fixture
def comm_range():
    """Standard communication range in meters."""
    return 100.0


@pytest.fixture
def test_output_dir(tmp_path):
    """Temporary directory for test outputs."""
    output_dir = tmp_path / "test_results"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_uav_id():
    """Standard UAV ID for tests."""
    return "UAV-TEST-001"


@pytest.fixture
def sample_position():
    """Sample UAV position (x, y, z)."""
    return (500.0, 500.0, 100.0)


@pytest.fixture
def sample_velocity():
    """Sample UAV velocity (vx, vy, vz)."""
    return (5.0, 3.0, 0.0)


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (slower, end-to-end)"
    )
    config.addinivalue_line(
        "markers", "contract: marks tests as contract tests (interface compliance)"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance benchmarks"
    )
    config.addinivalue_line("markers", "slow: marks tests that take significant time")
