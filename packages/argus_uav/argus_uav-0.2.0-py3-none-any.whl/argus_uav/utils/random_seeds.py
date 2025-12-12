"""
Random seed management for reproducible experiments.

Uses NumPy's modern random API (numpy.random.Generator) for better statistical
properties and reproducibility.
"""

from typing import Optional

import numpy as np

# Global random generator instance
_global_rng: Optional[np.random.Generator] = None
_global_seed: Optional[int] = None


def set_global_seed(seed: int) -> None:
    """
    Set the global random seed for all Argus modules.

    Args:
        seed: Integer seed value for reproducibility

    Example:
        >>> set_global_seed(42)
        >>> rng = get_rng()
        >>> values = rng.uniform(0, 1, size=10)
    """
    global _global_rng, _global_seed
    _global_seed = seed
    _global_rng = np.random.default_rng(seed)


def get_rng(seed: Optional[int] = None) -> np.random.Generator:
    """
    Get a NumPy random generator instance.

    Args:
        seed: Optional seed. If None, uses global seed or creates unseeded generator.

    Returns:
        NumPy Generator instance

    Example:
        >>> rng = get_rng(seed=42)
        >>> positions = rng.uniform(low=0, high=1000, size=(10, 3))
    """
    if seed is not None:
        return np.random.default_rng(seed)

    global _global_rng
    if _global_rng is None:
        # No global seed set, create unseeded generator
        _global_rng = np.random.default_rng()

    return _global_rng


def get_current_seed() -> Optional[int]:
    """
    Get the current global seed value.

    Returns:
        Current seed or None if not set
    """
    return _global_seed
