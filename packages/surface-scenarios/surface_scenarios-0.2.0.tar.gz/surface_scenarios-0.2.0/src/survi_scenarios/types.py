from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Mapping, Any

import numpy as np
import pandas as pd

ArrayLike = np.ndarray


@dataclass(slots=True)
class ElevationSurface:
    name: str
    samples: pd.DataFrame
    truth_z: Callable[[ArrayLike], ArrayLike]
    truth_gradient: Optional[Callable[[ArrayLike], ArrayLike]] = None
    description: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, object]:
        xy = self.samples[["x", "y"]].to_numpy()
        extent = np.max(xy, axis=0) - np.min(xy, axis=0)
        return {
            "points": int(len(self.samples)),
            "extent_xy": tuple(float(v) for v in extent),
            "description": self.description,
        }


@dataclass(slots=True)
class SDFSurface:
    name: str
    raw_surface: pd.DataFrame
    truth_phi: Callable[[ArrayLike], ArrayLike]
    truth_normals: Optional[Callable[[ArrayLike], ArrayLike]] = None
    truth_height: Optional[Callable[[ArrayLike], ArrayLike]] = None
    bounds: tuple[np.ndarray, np.ndarray] | None = None
    description: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, object]:
        coords = self.raw_surface[["x", "y", "z"]].to_numpy()
        extent = np.max(coords, axis=0) - np.min(coords, axis=0)
        return {
            "points": int(len(self.raw_surface)),
            "extent_xyz": tuple(float(v) for v in extent),
            "description": self.description,
        }


__all__ = ["ElevationSurface", "SDFSurface"]
