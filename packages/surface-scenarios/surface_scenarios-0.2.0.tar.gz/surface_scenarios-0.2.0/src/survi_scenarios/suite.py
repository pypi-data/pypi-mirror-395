"""Scenario manifest plumbing (adapted from Survi, sans heavy dependencies)."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping

import numpy as np
import pandas as pd
from shapely.geometry import Polygon, Point

from .geom import SamplingParams, SurveyArea, make_grid, nearest_surface_values
from .rng import numpy_rng
from .synthetic import BumpSpec, RippleSpec, SurfaceParams, make_surface_df, make_rectangle, make_l_shape, rotate_polygon
from .units import Unit


class PolygonKind(str, Enum):
    RECT = "rect"
    ROTATED_RECT = "rotated_rect"
    L_SHAPE = "lshape"
    RANDOM_CONVEX = "random_convex"


@dataclass(frozen=True)
class GridSpec:
    grid_spacing: float = 3.0
    edge_exclusion: float = 1.5
    rotation_deg: float = 0.0
    shift_x: float = 0.0
    shift_y: float = 0.0

    def to_params(self) -> SamplingParams:
        return SamplingParams(
            shift_x=self.shift_x,
            shift_y=self.shift_y,
            rotation_deg=self.rotation_deg,
            grid_spacing=self.grid_spacing,
            edge_exclusion=self.edge_exclusion,
        )


@dataclass(frozen=True)
class ScenarioConfig:
    name: str
    surface: SurfaceParams
    polygon_kind: PolygonKind = PolygonKind.RECT
    polygon_params: Mapping[str, Any] | None = None
    grid: GridSpec = GridSpec()
    master_seed: int = 0
    model_unit: Unit = Unit.METERS

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ScenarioConfig":
        poly_kind = PolygonKind(str(payload.get("polygon_kind", "rect")))
        grid = GridSpec(**(payload.get("grid") or {}))
        surface_raw = payload.get("surface") or {}
        # hydrate nested ripple/bump specs
        if surface_raw.get("ripples") is not None:
            surface_raw = dict(surface_raw)
            surface_raw["ripples"] = [RippleSpec(**r) for r in surface_raw.get("ripples")]
        if surface_raw.get("bump_specs") is not None:
            surface_raw = dict(surface_raw)
            surface_raw["bump_specs"] = [BumpSpec(**b) for b in surface_raw.get("bump_specs")]
        surface = SurfaceParams(**surface_raw)
        return cls(
            name=str(payload["name"]),
            surface=surface,
            polygon_kind=poly_kind,
            polygon_params=payload.get("polygon_params") or {},
            grid=grid,
            master_seed=int(payload.get("master_seed", 0)),
            model_unit=Unit(payload.get("model_unit", Unit.METERS.value)),
        )

    def to_dict(self) -> dict[str, Any]:
        out = {
            "name": self.name,
            "surface": asdict(self.surface),
            "polygon_kind": self.polygon_kind.value,
            "polygon_params": dict(self.polygon_params or {}),
            "grid": asdict(self.grid),
            "master_seed": int(self.master_seed),
            "model_unit": self.model_unit.value,
        }
        return out


@dataclass(frozen=True)
class ScenarioMaterialized:
    name: str
    master_points: pd.DataFrame
    area: SurveyArea
    grid_xy: pd.DataFrame
    grid_with_z: pd.DataFrame


class Scenario:
    def __init__(self, cfg: ScenarioConfig):
        self.cfg = cfg

    # deterministic polygon builder
    def _make_polygon(self, rng: np.random.Generator) -> Polygon:
        p = self.cfg
        if p.polygon_kind == PolygonKind.RECT:
            return make_rectangle(p.surface.width, p.surface.length)
        if p.polygon_kind == PolygonKind.ROTATED_RECT:
            base = make_rectangle(p.surface.width, p.surface.length)
            deg = float(p.polygon_params.get("rotation_deg", 0.0))
            rot = rotate_polygon(base, deg)
            return rot.intersection(base)
        if p.polygon_kind == PolygonKind.L_SHAPE:
            notch = float(p.polygon_params["notch"])
            return make_l_shape(p.surface.width, p.surface.length, notch=notch)
        if p.polygon_kind == PolygonKind.RANDOM_CONVEX:
            from .synthetic import random_convex_polygon  # reuse
            centre = tuple(p.polygon_params.get("centre", (p.surface.width/2, p.surface.length/2)))
            radius = float(p.polygon_params.get("radius", min(p.surface.width, p.surface.length)/3))
            vertices = int(p.polygon_params.get("vertices", 10))
            seed = int(p.polygon_params.get("seed", rng.integers(0, 2**31-1)))
            poly = random_convex_polygon(centre=centre, radius=radius, vertices=vertices, seed=seed)
            deg = float(p.polygon_params.get("rotation_deg", 0.0))
            return rotate_polygon(poly, deg) if deg else poly
        raise ValueError(f"Unknown polygon_kind {p.polygon_kind}")

    @staticmethod
    def _infer_half_diag(df: pd.DataFrame) -> float | None:
        xs = np.unique(df["x"].to_numpy())
        ys = np.unique(df["y"].to_numpy())
        if xs.size < 2 or ys.size < 2:
            return None
        dx = np.min(np.diff(xs)) if xs.size > 1 else None
        dy = np.min(np.diff(ys)) if ys.size > 1 else None
        if dx is None or dy is None or not np.isfinite(dx) or not np.isfinite(dy):
            return None
        return 0.5 * float(np.hypot(dx, dy))

    def materialize(self) -> ScenarioMaterialized:
        rng = numpy_rng(self.cfg.master_seed, namespace="suite.materialize")
        df = make_surface_df(self.cfg.surface)
        poly = self._make_polygon(rng)
        area = SurveyArea(polygon=poly)

        grid_xy = make_grid(area, params=self.cfg.grid.to_params())

        # auto max_dist from inferred spacing
        half_diag = self._infer_half_diag(df)
        maxd = 1.01 * half_diag if half_diag is not None else None

        nn = nearest_surface_values(df, grid_xy, max_dist=maxd)
        grid_with_z = grid_xy.copy()
        grid_with_z["z"] = nn["z_nn"]

        return ScenarioMaterialized(
            name=self.cfg.name,
            master_points=df,
            area=area,
            grid_xy=grid_xy,
            grid_with_z=grid_with_z,
        )

    def sample_surface(
        self,
        materialized: ScenarioMaterialized,
        strategy: "SamplingStrategy",
        *,
        nearest_max_dist: float | Literal["auto"] | None = "auto",
    ) -> pd.DataFrame:
        qp = strategy.sample(materialized.area, self.cfg.master_seed)
        if nearest_max_dist == "auto":
            half_diag = self._infer_half_diag(materialized.master_points)
            maxd = 1.01 * half_diag if half_diag is not None else None
        else:
            maxd = nearest_max_dist

        nn = nearest_surface_values(materialized.master_points, qp, max_dist=maxd)
        out = qp.copy()
        out["z"] = nn["z_nn"]
        return out


class SamplingStrategy:
    def sample(self, area: SurveyArea, seed: int) -> pd.DataFrame:
        raise NotImplementedError


class RandomUniform(SamplingStrategy):
    def __init__(self, n: int):
        self.n = int(n)

    def sample(self, area: SurveyArea, seed: int) -> pd.DataFrame:
        rng = numpy_rng(seed, namespace="suite.random_uniform")
        minx, miny, maxx, maxy = area.polygon.bounds
        xs: list[float] = []
        ys: list[float] = []
        while len(xs) < self.n:
            x = rng.uniform(minx, maxx)
            y = rng.uniform(miny, maxy)
            if area.polygon.contains(Point(float(x), float(y))):
                xs.append(float(x)); ys.append(float(y))
        return pd.DataFrame({"x": xs, "y": ys, "point_id": np.arange(self.n, dtype=int)})


class UniformGridWithJitter(SamplingStrategy):
    def __init__(
        self,
        spacing: float,
        jitter: float = 0.0,
        rotation_deg: float = 0.0,
        edge_exclusion: float = 0.0
    ):
        self.spacing = float(spacing)
        self.jitter = float(jitter)
        self.rotation_deg = float(rotation_deg)
        self.edge_exclusion = float(edge_exclusion)

    def sample(self, area: SurveyArea, seed: int) -> pd.DataFrame:
        base = make_grid(area, params=SamplingParams(
            grid_spacing=self.spacing,
            edge_exclusion=self.edge_exclusion,
            rotation_deg=self.rotation_deg
        ))
        if self.jitter <= 0:
            return base
        rng = numpy_rng(seed, namespace="suite.uniform_jitter")
        jx = rng.uniform(-self.jitter, self.jitter, size=len(base))
        jy = rng.uniform(-self.jitter, self.jitter, size=len(base))
        df = base.copy()
        df["x"] = df["x"] + jx
        df["y"] = df["y"] + jy
        # keep those that stay inside
        inside = [area.polygon.contains(Point(float(x), float(y))) for x, y in zip(df["x"], df["y"])]
        df = df.loc[inside].reset_index(drop=True)
        df["point_id"] = np.arange(len(df), dtype=int)
        return df


@dataclass
class ScenarioSuite:
    items: list[ScenarioConfig]

    def save_manifest(self, path: str) -> None:
        import json
        payload = {"items": [cfg.to_dict() for cfg in self.items]}
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load_manifest(cls, path: str) -> "ScenarioSuite":
        import json
        payload = json.loads(Path(path).read_text())
        items_raw = payload.get("items")
        if not isinstance(items_raw, Iterable):
            raise ValueError("Manifest must contain an 'items' list")
        items = [ScenarioConfig.from_dict(item) for item in items_raw]
        return cls(items)

    def names(self) -> list[str]:
        return [c.name for c in self.items]

    def get(self, name: str) -> Scenario:
        for c in self.items:
            if c.name == name:
                return Scenario(c)
        raise KeyError(name)


__all__ = [
    "ScenarioConfig",
    "ScenarioSuite",
    "Scenario",
    "ScenarioMaterialized",
    "RandomUniform",
    "UniformGridWithJitter",
    "GridSpec",
    "PolygonKind",
]
