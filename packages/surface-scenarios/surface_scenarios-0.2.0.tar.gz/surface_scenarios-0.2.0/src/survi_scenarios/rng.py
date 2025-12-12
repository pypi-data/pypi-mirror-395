"""Minimal RNG helper mirroring Survi's deterministic-friendly wrapper."""
from __future__ import annotations

import hashlib
import os
import numpy as np

_DEFAULT_NAMESPACE = "survi-scenarios"


def _hash_namespace(seed: int, namespace: str | None) -> int:
    label = namespace or _DEFAULT_NAMESPACE
    digest = hashlib.blake2b(f"{seed}:{label}".encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def base_seed() -> int:
    """Return base seed from SURVI_SEED (defaults to 0)."""

    raw = os.getenv("SURVI_SEED")
    try:
        return int(raw) if raw is not None else 0
    except (TypeError, ValueError):
        return 0


def numpy_rng(seed: int | None = None, *, namespace: str | None = None) -> np.random.Generator:
    """Return a NumPy Generator. If SURVI_DETERMINISTIC=1, derive seeds from SURVI_SEED and namespace."""

    deterministic = os.getenv("SURVI_DETERMINISTIC", "0").lower() in {"1", "true", "yes", "on"}
    if seed is not None:
        resolved = int(seed)
    elif deterministic:
        resolved = _hash_namespace(base_seed(), namespace)
    else:
        resolved = None
    return np.random.default_rng(resolved)

__all__ = ["numpy_rng", "base_seed"]
