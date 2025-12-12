"""Lightweight geometry and sampling utilities used by the scenario suite."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon

try:  # optional speed-up
    from scipy.spatial import cKDTree  # type: ignore

    _HAVE_SCIPY = True
except Exception:  # pragma: no cover - optional dependency missing
    _HAVE_SCIPY = False


@dataclass(slots=True)
class SurveyArea:
    polygon: Polygon

    def __post_init__(self) -> None:
        if not self.polygon.is_valid:
            raise ValueError("SurveyArea.polygon must be a valid polygon")


@dataclass(slots=True)
class SamplingParams:
    shift_x: float = 0.0
    shift_y: float = 0.0
    rotation_deg: float = 0.0
    grid_spacing: float = 3.0
    edge_exclusion: float = 1.5


def _rotate(points: np.ndarray, theta: float, origin: tuple[float, float]) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return (points - origin) @ R.T + origin


def make_grid(area: SurveyArea, params: SamplingParams) -> pd.DataFrame:
    """Axis-aligned grid optionally rotated and clipped to polygon minus buffer."""

    minx, miny, maxx, maxy = area.polygon.bounds
    xs = np.arange(minx + params.shift_x, maxx, params.grid_spacing)
    ys = np.arange(miny + params.shift_y, maxy, params.grid_spacing)
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    grid = np.column_stack([xx.ravel(), yy.ravel()])

    if params.rotation_deg:
        grid = _rotate(grid, math.radians(params.rotation_deg), area.polygon.centroid.coords[0])

    clip_poly = area.polygon.buffer(-params.edge_exclusion)
    inside = np.fromiter(
        (clip_poly.contains(Point(float(x), float(y))) for x, y in grid),
        dtype=bool,
        count=len(grid),
    )
    grid = grid[inside]

    return pd.DataFrame({
        "x": grid[:, 0],
        "y": grid[:, 1],
        "point_id": np.arange(len(grid), dtype=int),
    })


def nearest_surface_values(
    surface_df: pd.DataFrame,
    query_df: pd.DataFrame,
    *,
    max_dist: float | None = 0.10,
) -> pd.DataFrame:
    """Nearest-neighbour z lookup for query points.

    Uses SciPy cKDTree when available, otherwise falls back to a NumPy brute-force
    search (acceptable for the modest scenario grid sizes).
    """

    xyz = surface_df[["x", "y"]].to_numpy()
    qxy = query_df[["x", "y"]].to_numpy()

    if _HAVE_SCIPY:
        tree = cKDTree(xyz)
        dists, idx = tree.query(qxy, k=1)
    else:
        d2 = np.sum((qxy[:, None, :] - xyz[None, :, :]) ** 2, axis=-1)
        idx = np.argmin(d2, axis=1)
        dists = np.sqrt(d2[np.arange(len(qxy)), idx])

    z_nearest = surface_df["z"].to_numpy()[idx]
    out = query_df.copy().reset_index(drop=True)
    out["z_nn"] = z_nearest
    out["dist"] = dists

    if max_dist is not None and np.any(dists > max_dist):
        bad = np.flatnonzero(dists > max_dist)
        raise ValueError(
            f"{len(bad)} query point(s) further than {max_dist:.3f} m from the surface grid."
        )

    return out


__all__ = ["SurveyArea", "SamplingParams", "make_grid", "nearest_surface_values"]
