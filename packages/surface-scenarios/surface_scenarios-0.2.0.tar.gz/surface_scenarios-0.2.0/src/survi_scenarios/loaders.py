"""Public scenario loader API for the standalone library."""
from __future__ import annotations

import os
from dataclasses import dataclass, replace
from dataclasses import asdict
import json
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Callable, Iterable, Mapping, MutableMapping

import numpy as np
import pandas as pd

try:  # optional mesh support
    import trimesh  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional
    trimesh = None  # type: ignore[assignment]

from .synthetic import RippleSpec, SurfaceParams, make_surface_df
from .synthetic_3d import (
    Synthetic3DSurfaceFactory,
    make_asteroid_field,
    make_canal_maze,
    make_cave_network,
    make_torus,
)
from .suite import ScenarioSuite, Scenario
from .types import ElevationSurface, SDFSurface


FactoryBuilder = Callable[..., Synthetic3DSurfaceFactory]

_FACTORIES: dict[str, FactoryBuilder] = {
    "torus": make_torus,
    "asteroid_field": make_asteroid_field,
    "cave_network": make_cave_network,
    "canal_maze": make_canal_maze,
}

_HEIGHTFIELD_SUBDIV = 2
_HEIGHTFIELD_PADDING = 0.15


# ── Elevation scenarios ------------------------------------------------------

def _default_suite_manifest() -> Path:
    env = os.getenv("SURVI_SCENARIO_MANIFEST")
    if env:
        return Path(env)
    return Path(resources.files("survi_scenarios.data.scenarios") / "suite_manifest.json")


@lru_cache(maxsize=None)
def _load_suite(manifest_path: str) -> ScenarioSuite:
    return ScenarioSuite.load_manifest(manifest_path)


def list_elevation_scenarios(manifest_path: str | Path | None = None) -> list[str]:
    manifest = Path(manifest_path) if manifest_path is not None else _default_suite_manifest()
    if not manifest.exists():
        raise FileNotFoundError(f"Scenario manifest not found at {manifest}")
    suite = _load_suite(str(manifest.resolve()))
    return suite.names()


def _build_truth_fn(clean_df: pd.DataFrame) -> Callable[[np.ndarray], np.ndarray]:
    xs = np.unique(clean_df["x"].to_numpy())
    ys = np.unique(clean_df["y"].to_numpy())
    grid = (
        clean_df.pivot(index="y", columns="x", values="z")
        .reindex(index=ys, columns=xs)
        .to_numpy()
    )
    x_step = xs[1] - xs[0] if len(xs) > 1 else 1.0
    y_step = ys[1] - ys[0] if len(ys) > 1 else 1.0

    def truth_fn(points: np.ndarray) -> np.ndarray:
        pts = np.asarray(points, dtype=float)
        xp = np.clip((pts[:, 0] - xs[0]) / x_step, 0.0, len(xs) - 1.000001)
        yp = np.clip((pts[:, 1] - ys[0]) / y_step, 0.0, len(ys) - 1.000001)
        x0 = np.floor(xp).astype(int)
        y0 = np.floor(yp).astype(int)
        x1 = np.clip(x0 + 1, 0, len(xs) - 1)
        y1 = np.clip(y0 + 1, 0, len(ys) - 1)
        tx = xp - x0
        ty = yp - y0
        z00 = grid[y0, x0]
        z01 = grid[y1, x0]
        z10 = grid[y0, x1]
        z11 = grid[y1, x1]
        z0 = (1 - tx) * z00 + tx * z10
        z1 = (1 - tx) * z01 + tx * z11
        return (1 - ty) * z0 + ty * z1

    return truth_fn


def load_elevation_scenario(
    name: str,
    *,
    manifest_path: str | Path | None = None,
) -> ElevationSurface:
    manifest = Path(manifest_path) if manifest_path is not None else _default_suite_manifest()
    if not manifest.exists():
        raise FileNotFoundError(f"Scenario manifest not found at {manifest}")

    suite = _load_suite(str(manifest.resolve()))
    scenario = None
    try:
        scenario = suite.get(name)
    except KeyError:
        lowered = name.lower()
        for cfg in suite.items:
            if cfg.name.lower() == lowered:
                scenario = Scenario(cfg)
                break
        if scenario is None:
            raise KeyError(name) from None

    params = scenario.cfg.surface
    df = make_surface_df(params)

    params_clean = replace(params, noise_std=0.0, noise_mean=0.0)
    df_clean = make_surface_df(params_clean)

    if len(np.unique(df_clean["x"])) < 2 or len(np.unique(df_clean["y"])) < 2:
        raise ValueError(
            f"Scenario '{name}' does not provide a gridded surface; unable to build analytic interpolation."
        )

    truth_fn = _build_truth_fn(df_clean)

    metadata = {
        "scenario": scenario.cfg.name,
        "polygon_kind": scenario.cfg.polygon_kind.value,
        "grid": asdict(scenario.cfg.grid),
        "surface_params": asdict(scenario.cfg.surface),
        "model_unit": scenario.cfg.model_unit.value,
        "manifest": str(manifest.resolve()),
    }

    return ElevationSurface(
        name=scenario.cfg.name,
        samples=df,
        truth_z=truth_fn,
        description=f"Scenario '{scenario.cfg.name}' from the suite manifest.",
        metadata=metadata,
    )


# ── SDF scenarios -----------------------------------------------------------

@dataclass(slots=True)
class _SDFScenarioConfig:
    name: str
    factory_type: str
    factory_params: Mapping[str, object]
    description: str
    sampling: Mapping[str, object]
    metadata: MutableMapping[str, object]
    manifest_path: Path
    config_path: Path


def _default_sdf_manifest() -> Path:
    env = os.getenv("SURVI_SDF_MANIFEST")
    if env:
        return Path(env)
    return Path(resources.files("survi_scenarios.data.scenarios_3d") / "manifest.json")


@lru_cache(maxsize=None)
def _load_sdf_manifest(path: str) -> dict[str, Path]:
    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    scenarios = payload.get("scenarios")
    if scenarios is None:
        raise ValueError(f"Manifest {manifest_path} missing 'scenarios' section")

    base = manifest_path.parent
    mapping: dict[str, Path] = {}
    if isinstance(scenarios, dict):
        items = scenarios.items()
    elif isinstance(scenarios, Iterable):
        items = []
        for item in scenarios:
            if not isinstance(item, dict) or "name" not in item:
                raise ValueError(f"Manifest entry must be a dict with a 'name': {item}")
            rel = item.get("path") or f"{item['name']}.json"
            items.append((item["name"], rel))
    else:
        raise ValueError(f"Unsupported scenarios payload in manifest {manifest_path}")

    for name, rel_path in items:
        resolved = (base / rel_path).resolve()
        mapping[str(name)] = resolved
    return mapping


def list_sdf_scenarios(manifest_path: str | Path | None = None) -> list[str]:
    manifest = Path(manifest_path) if manifest_path is not None else _default_sdf_manifest()
    names: set[str] = set()
    try:
        mapping = _load_sdf_manifest(str(manifest.resolve()))
        names.update(mapping.keys())
    except (FileNotFoundError, ValueError):
        pass

    try:
        elevation_names = list_elevation_scenarios(manifest_path)
        names.update(elevation_names)
    except (FileNotFoundError, ValueError):
        if manifest_path is None:
            try:
                names.update(list_elevation_scenarios(None))
            except Exception:
                pass
    return sorted(names)


def _load_config(name: str, *, manifest_path: str | Path | None) -> _SDFScenarioConfig:
    manifest = Path(manifest_path) if manifest_path is not None else _default_sdf_manifest()
    mapping = _load_sdf_manifest(str(manifest.resolve()))
    try:
        cfg_path = mapping[name]
    except KeyError as exc:
        available = ", ".join(sorted(mapping))
        raise KeyError(f"Unknown SDF scenario '{name}'. Available: {available}") from exc

    with cfg_path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)

    factory_section = payload.get("factory")
    if not isinstance(factory_section, dict) or "type" not in factory_section:
        raise ValueError(f"Scenario {cfg_path} must declare a 'factory' with a 'type'")
    factory_type = str(factory_section["type"]).lower()
    factory_params = dict(factory_section.get("params") or {})

    sampling_section = payload.get("sampling") or {}
    if not isinstance(sampling_section, Mapping):
        raise ValueError(f"Scenario {cfg_path} has invalid sampling configuration: {sampling_section}")

    metadata = dict(payload.get("metadata") or {})
    description = str(payload.get("description") or f"Scenario '{name}'")
    metadata.setdefault("config_path", str(cfg_path))
    metadata.setdefault("manifest_path", str(manifest.resolve()))
    metadata.setdefault("factory_type", factory_type)

    return _SDFScenarioConfig(
        name=str(payload.get("name") or name),
        factory_type=factory_type,
        factory_params=factory_params,
        description=description,
        sampling=sampling_section,
        metadata=metadata,
        manifest_path=manifest.resolve(),
        config_path=cfg_path,
    )


def _build_factory(cfg: _SDFScenarioConfig) -> Synthetic3DSurfaceFactory:
    builder = _FACTORIES.get(cfg.factory_type)
    if builder is None:
        available = ", ".join(sorted(_FACTORIES))
        raise ValueError(f"Unsupported factory '{cfg.factory_type}'. Options: {available}")
    return builder(**cfg.factory_params)


def _sample_surface(
    factory: Synthetic3DSurfaceFactory,
    sampling: Mapping[str, object],
    *,
    seed: int,
) -> pd.DataFrame:
    strategy = str(sampling.get("strategy", "surface_band")).lower()
    draws = int(sampling.get("n_samples", 4096))
    local_seed = int(sampling.get("seed", seed))

    if strategy == "surface_band":
        band_width = float(sampling.get("band_width", 0.08))
        oversample = int(sampling.get("oversample_factor", 10))
        max_attempts = int(sampling.get("max_attempts", 12))
        with_normals = bool(sampling.get("with_normals", True))
        df = factory.sample_surface_band(
            draws,
            band_width=band_width,
            oversample_factor=oversample,
            seed=local_seed,
            with_normals=with_normals,
            max_attempts=max_attempts,
        )
    elif strategy == "uniform":
        with_normals = bool(sampling.get("with_normals", True))
        df = factory.sample_uniform(
            draws,
            seed=local_seed,
            with_normals=with_normals,
        )
    else:
        raise ValueError(f"Unknown sampling strategy '{strategy}'")

    return df.reset_index(drop=True)


def load_sdf_scenario(
    name: str,
    *,
    seed: int = 0,
    manifest_path: str | Path | None = None,
) -> SDFSurface:
    try:
        cfg = _load_config(name, manifest_path=manifest_path)
    except (FileNotFoundError, KeyError, ValueError):
        return _load_heightfield_surface(name, seed=seed, manifest_path=manifest_path)

    factory = _build_factory(cfg)
    samples = _sample_surface(factory, cfg.sampling, seed=seed)

    points = samples[["x", "y", "z"]].to_numpy(dtype=float)
    phi, normals = factory.evaluate(points, with_normals=True)

    enriched = samples.copy()
    enriched["phi"] = phi
    if "nx" not in enriched.columns or "ny" not in enriched.columns or "nz" not in enriched.columns:
        normals = normals if normals is not None else factory.root.gradient(points)
        enriched["nx"] = normals[:, 0]
        enriched["ny"] = normals[:, 1]
        enriched["nz"] = normals[:, 2]
    enriched["is_surface"] = True
    enriched["source"] = cfg.name

    low, high = factory.bounds

    def _phi_fn(query: np.ndarray) -> np.ndarray:
        pts = np.asarray(query, dtype=float)
        return factory.root.phi(pts)

    def _normals_fn(query: np.ndarray) -> np.ndarray:
        pts = np.asarray(query, dtype=float)
        return factory.root.gradient(pts)

    metadata = dict(cfg.metadata)
    metadata.setdefault("samples", len(enriched))
    metadata.setdefault("seed", int(seed))

    return SDFSurface(
        name=cfg.name,
        raw_surface=enriched,
        truth_phi=_phi_fn,
        truth_normals=_normals_fn,
        bounds=(low, high),
        description=cfg.description,
        metadata=metadata,
    )


def _heightfield_to_mesh(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    grid = (
        df.pivot_table(index="y", columns="x", values="z", aggfunc="mean")
        .sort_index()
        .sort_index(axis=1)
    )
    xs = grid.columns.to_numpy(dtype=float)
    ys = grid.index.to_numpy(dtype=float)
    Z = grid.to_numpy(dtype=float)
    ny, nx = Z.shape
    if nx < 2 or ny < 2:
        raise ValueError("Heightfield requires at least a 2x2 grid to form a mesh")

    if _HEIGHTFIELD_SUBDIV > 1:
        xs_dense = np.linspace(xs[0], xs[-1], (len(xs) - 1) * _HEIGHTFIELD_SUBDIV + 1)
        ys_dense = np.linspace(ys[0], ys[-1], (len(ys) - 1) * _HEIGHTFIELD_SUBDIV + 1)

        Z_interp_x = np.empty((ny, len(xs_dense)), dtype=float)
        for row_idx in range(ny):
            Z_interp_x[row_idx] = np.interp(xs_dense, xs, Z[row_idx])

        Z_dense = np.empty((len(ys_dense), len(xs_dense)), dtype=float)
        for col_idx in range(len(xs_dense)):
            Z_dense[:, col_idx] = np.interp(ys_dense, ys, Z_interp_x[:, col_idx])
    else:
        xs_dense = xs
        ys_dense = ys
        Z_dense = Z

    X, Y = np.meshgrid(xs_dense, ys_dense, indexing="xy")
    vertices = np.column_stack((X.ravel(), Y.ravel(), Z_dense.ravel()))
    ny_dense, nx_dense = Z_dense.shape

    faces: list[list[int]] = []
    for j in range(ny_dense - 1):
        row = j * nx_dense
        next_row = (j + 1) * nx_dense
        for i in range(nx_dense - 1):
            idx00 = row + i
            idx10 = row + i + 1
            idx01 = next_row + i
            idx11 = next_row + i + 1
            faces.append([idx00, idx10, idx11])
            faces.append([idx00, idx11, idx01])
    return vertices, np.asarray(faces, dtype=np.int64), xs_dense, ys_dense


def _load_heightfield_surface(
    name: str,
    *,
    seed: int,
    manifest_path: str | Path | None,
) -> SDFSurface:
    _ensure_trimesh()
    try:
        dataset = load_elevation_scenario(name, manifest_path=manifest_path)
    except FileNotFoundError as exc:
        raise ValueError(f"Scenario manifest not found at {manifest_path}") from exc
    except (KeyError, ValueError) as exc:
        try:
            available = list_elevation_scenarios(manifest_path)
        except Exception:
            available = list_elevation_scenarios(None)
        raise ValueError(
            f"Unknown elevation scenario '{name}'. Options: {sorted(available)}"
        ) from exc

    vertices, faces, xs_dense, ys_dense = _heightfield_to_mesh(dataset.samples)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    mesh.fix_normals()
    if mesh.face_normals.shape[0] and np.mean(mesh.face_normals[:, 2]) < 0.0:
        mesh.invert()

    vertex_normals = mesh.vertex_normals
    surface_df = pd.DataFrame(mesh.vertices, columns=["x", "y", "z"])
    surface_df["nx"] = vertex_normals[:, 0]
    surface_df["ny"] = vertex_normals[:, 1]
    surface_df["nz"] = vertex_normals[:, 2]
    surface_df["is_surface"] = True
    surface_df["source"] = f"{dataset.name}_heightfield_mesh"

    coords = surface_df[["x", "y", "z"]].to_numpy(dtype=float)
    padding = _HEIGHTFIELD_PADDING
    low = np.min(coords, axis=0) - padding
    high = np.max(coords, axis=0) + padding

    def _phi_fn(points: np.ndarray) -> np.ndarray:
        pts = np.asarray(points, dtype=float)
        closest_pts, distances, _ = trimesh.proximity.closest_point(mesh, pts)
        distances = np.asarray(distances, dtype=float)
        heights = dataset.truth_z(pts[:, :2])
        sign = np.where(pts[:, 2] >= heights, 1.0, -1.0)
        return distances * sign

    def _truth_height_fn(points: np.ndarray) -> np.ndarray:
        pts = np.asarray(points, dtype=float)
        if pts.ndim != 2:
            raise ValueError("Heightfield truth expects an (N, D) array")
        if pts.shape[1] == 3:
            xy = pts[:, :2]
        elif pts.shape[1] == 2:
            xy = pts
        else:
            raise ValueError("Heightfield truth expects 2D or 3D points")
        return dataset.truth_z(xy)

    def _normals_fn(points: np.ndarray) -> np.ndarray:
        pts = np.asarray(points, dtype=float)
        closest_pts, _, tri_idx = trimesh.proximity.closest_point(mesh, pts)
        tri_idx = np.asarray(tri_idx, dtype=int)
        normals = mesh.face_normals[np.clip(tri_idx, 0, mesh.face_normals.shape[0] - 1)].copy()
        delta = pts - closest_pts
        flip = np.sum(delta * normals, axis=1) < 0.0
        normals[flip] *= -1.0
        missing = tri_idx < 0
        if np.any(missing):
            fallback = delta[missing]
            fallback_norm = np.linalg.norm(fallback, axis=1, keepdims=True)
            normals[missing] = fallback / np.clip(fallback_norm, 1e-9, None)
        return normals

    metadata = dict(dataset.metadata)
    metadata.update({
        "dataset_mode": "scenario_heightfield",
        "scenario": dataset.name,
        "grid_shape": (int(len(ys_dense)), int(len(xs_dense))),
        "heightfield_subdivision": int(_HEIGHTFIELD_SUBDIV),
        "padding": float(padding),
        "factory_type": "heightfield",
        "seed": int(seed),
    })

    description = dataset.description or f"Heightfield scenario '{dataset.name}' repurposed as an SDF surface."

    return SDFSurface(
        name=dataset.name,
        raw_surface=surface_df,
        truth_phi=_phi_fn,
        truth_normals=_normals_fn,
        truth_height=_truth_height_fn,
        bounds=(low, high),
        description=description,
        metadata=metadata,
    )


def _ensure_trimesh() -> None:
    if trimesh is None:
        raise RuntimeError(
            "trimesh is required to sample mesh-backed SDF scenarios. Install the optional "
            "'mesh' extra (e.g. pip install survi-scenarios[mesh]) or choose an analytic scenario."
        )


__all__ = [
    "list_elevation_scenarios",
    "load_elevation_scenario",
    "list_sdf_scenarios",
    "load_sdf_scenario",
]
