"""Synthetic 3D signed-distance field (SDF) surface factory utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from .rng import numpy_rng

__all__ = [
    "SDFNode",
    "Sphere",
    "Box",
    "Union",
    "Intersection",
    "Difference",
    "Synthetic3DSurfaceFactory",
    "Torus",
    "make_asteroid_field",
    "make_cave_network",
    "make_canal_maze",
    "make_torus",
]


def _as_point(vec: Sequence[float]) -> np.ndarray:
    arr = np.asarray(vec, dtype=float)
    if arr.shape != (3,):  # pragma: no cover - guardrail
        raise ValueError("Expected a 3D vector")
    return arr


def _normalize(vecs: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms = np.clip(norms, eps, None)
    return vecs / norms


class SDFNode:
    """Abstract base class for SDF primitives and composite nodes."""

    def phi(self, points: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def gradient(self, points: np.ndarray, eps: float = 1e-4) -> np.ndarray:
        if points.size == 0:
            return np.zeros((0, 3), dtype=float)
        offsets = np.eye(3, dtype=float) * eps
        grads = []
        for offset in offsets:
            grads.append((self.phi(points + offset) - self.phi(points - offset)) / (2.0 * eps))
        return np.stack(grads, axis=1)


@dataclass(slots=True)
class Sphere(SDFNode):
    center: np.ndarray
    radius: float

    def __init__(self, *, center: Sequence[float] = (0.0, 0.0, 0.0), radius: float = 1.0) -> None:
        self.center = _as_point(center)
        self.radius = float(radius)

    def phi(self, points: np.ndarray) -> np.ndarray:  # type: ignore[override]
        diff = points - self.center
        return np.linalg.norm(diff, axis=1) - self.radius

    def gradient(self, points: np.ndarray, eps: float = 1e-4) -> np.ndarray:  # type: ignore[override]
        diff = points - self.center
        return _normalize(diff)


@dataclass(slots=True)
class Box(SDFNode):
    center: np.ndarray
    half_sizes: np.ndarray

    def __init__(self, *, center: Sequence[float] = (0.0, 0.0, 0.0), size: Sequence[float] = (1.0, 1.0, 1.0)) -> None:
        self.center = _as_point(center)
        self.half_sizes = 0.5 * np.asarray(size, dtype=float)
        if np.any(self.half_sizes <= 0):
            raise ValueError("Box size components must be positive")

    def phi(self, points: np.ndarray) -> np.ndarray:  # type: ignore[override]
        q = np.abs(points - self.center) - self.half_sizes
        outside = np.maximum(q, 0.0)
        outside_norm = np.linalg.norm(outside, axis=1)
        inside = np.minimum(np.maximum.reduce(q, axis=1), 0.0)
        return outside_norm + inside


class Union(SDFNode):
    def __init__(self, *nodes: SDFNode) -> None:
        if not nodes:
            raise ValueError("Union requires at least one node")
        self.nodes = nodes

    def phi(self, points: np.ndarray) -> np.ndarray:  # type: ignore[override]
        values = np.stack([node.phi(points) for node in self.nodes], axis=0)
        return np.min(values, axis=0)

    def gradient(self, points: np.ndarray, eps: float = 1e-4) -> np.ndarray:  # type: ignore[override]
        values = np.stack([node.phi(points) for node in self.nodes], axis=0)
        winners = np.argmin(values, axis=0)
        grads = np.stack([node.gradient(points, eps=eps) for node in self.nodes], axis=0)
        selected = np.take_along_axis(grads, winners[np.newaxis, :, np.newaxis], axis=0)[0]
        return _normalize(selected)


class Intersection(SDFNode):
    def __init__(self, *nodes: SDFNode) -> None:
        if not nodes:
            raise ValueError("Intersection requires at least one node")
        self.nodes = nodes

    def phi(self, points: np.ndarray) -> np.ndarray:  # type: ignore[override]
        values = np.stack([node.phi(points) for node in self.nodes], axis=0)
        return np.max(values, axis=0)

    def gradient(self, points: np.ndarray, eps: float = 1e-4) -> np.ndarray:  # type: ignore[override]
        values = np.stack([node.phi(points) for node in self.nodes], axis=0)
        winners = np.argmax(values, axis=0)
        grads = np.stack([node.gradient(points, eps=eps) for node in self.nodes], axis=0)
        selected = np.take_along_axis(grads, winners[np.newaxis, :, np.newaxis], axis=0)[0]
        return _normalize(selected)


class Difference(SDFNode):
    def __init__(self, a: SDFNode, b: SDFNode) -> None:
        self.a = a
        self.b = b

    def phi(self, points: np.ndarray) -> np.ndarray:  # type: ignore[override]
        pa = self.a.phi(points)
        pb = self.b.phi(points)
        return np.maximum(pa, -pb)

    def gradient(self, points: np.ndarray, eps: float = 1e-4) -> np.ndarray:  # type: ignore[override]
        pa = self.a.phi(points)
        pb = self.b.phi(points)
        grad_a = self.a.gradient(points, eps=eps)
        grad_b = -self.b.gradient(points, eps=eps)
        mask = pa >= -pb
        selected = np.where(mask[:, None], grad_a, grad_b)
        return _normalize(selected)


@dataclass(slots=True)
class Torus(SDFNode):
    """Torus aligned with the z-axis."""

    major_radius: float
    minor_radius: float
    center: np.ndarray

    def __init__(
        self,
        *,
        major_radius: float = 0.8,
        minor_radius: float = 0.25,
        center: Sequence[float] = (0.0, 0.0, 0.0),
    ) -> None:
        if major_radius <= 0 or minor_radius <= 0:
            raise ValueError("Torus radii must be positive")
        self.major_radius = float(major_radius)
        self.minor_radius = float(minor_radius)
        self.center = _as_point(center)

    def phi(self, points: np.ndarray) -> np.ndarray:  # type: ignore[override]
        shifted = points - self.center
        xy_norm = np.linalg.norm(shifted[:, :2], axis=1)
        inner = np.sqrt((xy_norm - self.major_radius) ** 2 + shifted[:, 2] ** 2)
        return inner - self.minor_radius

    def gradient(self, points: np.ndarray, eps: float = 1e-9) -> np.ndarray:  # type: ignore[override]
        shifted = points - self.center
        xy_norm = np.linalg.norm(shifted[:, :2], axis=1)
        xy_safe = np.clip(xy_norm, eps, None)
        inner = np.sqrt((xy_safe - self.major_radius) ** 2 + shifted[:, 2] ** 2)
        inner = np.clip(inner, eps, None)

        grad = np.zeros_like(shifted)
        radial_term = (xy_safe - self.major_radius) / inner
        grad[:, 0] = shifted[:, 0] * radial_term / xy_safe
        grad[:, 1] = shifted[:, 1] * radial_term / xy_safe
        grad[:, 2] = shifted[:, 2] / inner
        return _normalize(grad)


@dataclass(slots=True)
class Synthetic3DSurfaceFactory:
    root: SDFNode
    bounds: tuple[np.ndarray, np.ndarray]
    name: str = "custom"

    def __post_init__(self) -> None:
        low, high = self.bounds
        self.bounds = (_as_point(low), _as_point(high))
        if np.any(self.bounds[0] >= self.bounds[1]):
            raise ValueError("Invalid bounds: low must be strictly less than high")

    def evaluate(self, points: np.ndarray, *, with_normals: bool = False) -> tuple[np.ndarray, np.ndarray | None]:
        phi = self.root.phi(points)
        normals = None
        if with_normals:
            normals = _normalize(self.root.gradient(points))
        return phi, normals

    def sample_uniform(self, n_samples: int, *, seed: int | None = None, with_normals: bool = False) -> pd.DataFrame:
        if n_samples <= 0:
            raise ValueError("n_samples must be positive")
        rng = numpy_rng(seed, namespace="synthetic3d.uniform")
        low, high = self.bounds
        points = rng.uniform(low, high, size=(n_samples, 3))
        phi = self.root.phi(points)
        data = {
            "x": points[:, 0],
            "y": points[:, 1],
            "z": points[:, 2],
            "phi": phi,
        }
        if with_normals:
            normals = _normalize(self.root.gradient(points))
            data.update({
                "nx": normals[:, 0],
                "ny": normals[:, 1],
                "nz": normals[:, 2],
            })
        return pd.DataFrame(data)

    def sample_surface_band(
        self,
        n_samples: int,
        *,
        band_width: float = 0.15,
        oversample_factor: int = 6,
        seed: int | None = None,
        with_normals: bool = True,
        max_attempts: int = 12,
    ) -> pd.DataFrame:
        if n_samples <= 0:
            raise ValueError("n_samples must be positive")
        if band_width <= 0:
            raise ValueError("band_width must be positive")
        rng = numpy_rng(seed, namespace="synthetic3d.surface_band")
        low, high = self.bounds
        collected_pts: list[np.ndarray] = []
        collected_phi: list[np.ndarray] = []
        n_collected = 0
        attempts = 0
        while n_collected < n_samples and attempts < max_attempts:
            attempts += 1
            remaining = max(n_samples - n_collected, 1)
            batch_size = max(oversample_factor * remaining, remaining)
            batch = rng.uniform(low, high, size=(batch_size, 3))
            phi = self.root.phi(batch)
            mask = np.abs(phi) <= band_width
            if np.any(mask):
                collected_pts.append(batch[mask])
                collected_phi.append(phi[mask])
                n_collected += np.count_nonzero(mask)
        if not collected_pts or n_collected < n_samples:
            raise RuntimeError(
                "Unable to sample near-surface points; consider increasing band_width or oversample_factor"
            )
        points = np.concatenate(collected_pts, axis=0)[:n_samples]
        phi_vals = np.concatenate(collected_phi, axis=0)[:n_samples]
        data = {
            "x": points[:, 0],
            "y": points[:, 1],
            "z": points[:, 2],
            "phi": phi_vals,
        }
        if with_normals:
            normals = _normalize(self.root.gradient(points))
            data.update({
                "nx": normals[:, 0],
                "ny": normals[:, 1],
                "nz": normals[:, 2],
            })
        return pd.DataFrame(data)


def _build_sphere_union(
    rng: np.random.Generator,
    *,
    count: int,
    radius_range: tuple[float, float],
    spread: float,
) -> tuple[list[Sphere], list[Sphere]]:
    cores: list[Sphere] = []
    subtractions: list[Sphere] = []
    r_min, r_max = radius_range
    for _ in range(count):
        radius = rng.uniform(r_min, r_max)
        center = rng.normal(scale=spread, size=3)
        cores.append(Sphere(center=center, radius=radius))
        if rng.uniform() < 0.4:
            direction = rng.normal(size=3)
            direction = direction / np.linalg.norm(direction)
            crater_center = center + direction * radius * rng.uniform(0.45, 0.85)
            crater_radius = radius * rng.uniform(0.25, 0.45)
            subtractions.append(Sphere(center=crater_center, radius=crater_radius))
    return cores, subtractions


def make_asteroid_field(
    *,
    count: int = 10,
    radius_range: tuple[float, float] = (0.4, 1.2),
    spread: float = 2.5,
    seed: int | None = None,
) -> Synthetic3DSurfaceFactory:
    rng = numpy_rng(seed, namespace="synthetic3d.asteroid")
    cores, subtractions = _build_sphere_union(rng, count=count, radius_range=radius_range, spread=spread)
    core_union: SDFNode = Union(*cores) if len(cores) > 1 else cores[0]
    if subtractions:
        caverns = Union(*subtractions) if len(subtractions) > 1 else subtractions[0]
        root: SDFNode = Difference(core_union, caverns)
    else:
        root = core_union
    max_r = radius_range[1]
    bound = spread * 2.5 + max_r * 1.5
    low = np.full(3, -bound)
    high = np.full(3, bound)
    return Synthetic3DSurfaceFactory(root=root, bounds=(low, high), name="asteroid-field")


def make_cave_network(
    *,
    cavern_radius: float = 5.0,
    cavity_count: int = 12,
    tunnel_count: int = 6,
    seed: int | None = None,
) -> Synthetic3DSurfaceFactory:
    rng = numpy_rng(seed, namespace="synthetic3d.cave")
    base = Sphere(center=(0.0, 0.0, 0.0), radius=cavern_radius)
    cavities = []
    for _ in range(cavity_count):
        offset = rng.normal(scale=cavern_radius * 0.6, size=3)
        amp = rng.uniform(0.4, 0.8)
        cavities.append(Sphere(center=offset, radius=cavern_radius * 0.25 * amp))
    tunnels = []
    for _ in range(tunnel_count):
        start = rng.normal(scale=cavern_radius * 0.7, size=3)
        axis = rng.normal(size=3)
        axis = axis / np.linalg.norm(axis)
        end = start + axis * rng.uniform(cavern_radius * 0.8, cavern_radius * 1.4)
        mid = 0.5 * (start + end)
        length = np.linalg.norm(end - start)
        direction = axis
        size = np.array([cavern_radius * 0.25, cavern_radius * 0.25, length + cavern_radius * 0.4])
        rot = _orthonormal_basis(direction)
        tunnels.append(_oriented_box(center=mid, size=size, rotation=rot))
    subtractors: list[SDFNode] = []
    if cavities:
        subtractors.append(Union(*cavities) if len(cavities) > 1 else cavities[0])
    if tunnels:
        subtractors.append(Union(*tunnels) if len(tunnels) > 1 else tunnels[0])
    if subtractors:
        root: SDFNode = Difference(base, Union(*subtractors) if len(subtractors) > 1 else subtractors[0])
    else:
        root = base
    bound = cavern_radius * 1.25
    low = np.full(3, -bound)
    high = np.full(3, bound)
    return Synthetic3DSurfaceFactory(root=root, bounds=(low, high), name="cave-network")


def make_canal_maze(
    *,
    span: float = 8.0,
    height: float = 2.5,
    channel_width: float = 0.9,
    grid: int = 4,
    seed: int | None = None,
) -> Synthetic3DSurfaceFactory:
    rng = numpy_rng(seed, namespace="synthetic3d.canal")
    base = Box(center=(0.0, 0.0, 0.0), size=(span * 2, span * 2, height))
    channels: list[SDFNode] = []
    step = (2 * span) / grid
    for i in range(grid + 1):
        offset = -span + i * step
        channels.append(Box(center=(offset, 0.0, 0.0), size=(channel_width, span * 2.2, height * 0.9)))
        channels.append(Box(center=(0.0, offset, 0.0), size=(span * 2.2, channel_width, height * 0.9)))
    for _ in range(grid // 2):
        centre = rng.normal(scale=span * 0.5, size=2)
        channels.append(Box(center=(centre[0], centre[1], 0.0), size=(channel_width * 0.75, channel_width * 0.75, height * 1.1)))
    subtractor = Union(*channels)
    root: SDFNode = Difference(base, subtractor)
    bound = span * 1.05
    low = np.array([-bound, -bound, -height * 0.6])
    high = np.array([bound, bound, height * 0.6])
    return Synthetic3DSurfaceFactory(root=root, bounds=(low, high), name="canal-maze")


def make_torus(
    *,
    major_radius: float = 0.8,
    minor_radius: float = 0.25,
    bounds: tuple[Sequence[float], Sequence[float]] | None = None,
    padding: float = 0.4,
) -> Synthetic3DSurfaceFactory:
    """Convenience factory for a z-aligned torus."""

    root = Torus(major_radius=major_radius, minor_radius=minor_radius)
    if bounds is None:
        span_xy = major_radius + minor_radius + padding
        span_z = minor_radius + padding
        low = np.array([-span_xy, -span_xy, -span_z], dtype=float)
        high = np.array([span_xy, span_xy, span_z], dtype=float)
    else:
        low = _as_point(bounds[0])
        high = _as_point(bounds[1])
    return Synthetic3DSurfaceFactory(root=root, bounds=(low, high), name="torus")


def _orthonormal_basis(direction: np.ndarray) -> np.ndarray:
    direction = direction / np.linalg.norm(direction)
    if abs(direction[0]) < 0.5:
        other = np.array([1.0, 0.0, 0.0])
    else:
        other = np.array([0.0, 1.0, 0.0])
    v1 = other - np.dot(other, direction) * direction
    v1 /= np.linalg.norm(v1)
    v2 = np.cross(direction, v1)
    return np.stack((v1, v2, direction), axis=1)


def _oriented_box(*, center: np.ndarray, size: np.ndarray, rotation: np.ndarray) -> SDFNode:
    local_box = Box(center=(0.0, 0.0, 0.0), size=size)

    class _TransformedBox(SDFNode):
        def phi(self, points: np.ndarray) -> np.ndarray:  # type: ignore[override]
            local = (points - center) @ rotation
            return local_box.phi(local)

        def gradient(self, points: np.ndarray, eps: float = 1e-4) -> np.ndarray:  # type: ignore[override]
            local = (points - center) @ rotation
            grads = local_box.gradient(local, eps=eps) @ rotation.T
            return _normalize(grads)

    return _TransformedBox()
