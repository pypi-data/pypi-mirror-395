"""Lightweight synthetic scenario library extracted from Survi.

Public API keeps compatibility with Survi's scenario loaders while avoiding
Survi-specific container types. Functions return pandas DataFrames and simple
truth callables.
"""

from .loaders import (
    list_elevation_scenarios,
    load_elevation_scenario,
    list_sdf_scenarios,
    load_sdf_scenario,
)
from .synthetic import SurfaceParams, RippleSpec, BumpSpec, make_surface_df
from .synthetic_3d import (
    Synthetic3DSurfaceFactory,
    make_asteroid_field,
    make_canal_maze,
    make_cave_network,
    make_torus,
)
from .types import ElevationSurface, SDFSurface

__all__ = [
    "list_elevation_scenarios",
    "load_elevation_scenario",
    "list_sdf_scenarios",
    "load_sdf_scenario",
    "SurfaceParams",
    "RippleSpec",
    "BumpSpec",
    "make_surface_df",
    "Synthetic3DSurfaceFactory",
    "make_asteroid_field",
    "make_canal_maze",
    "make_cave_network",
    "make_torus",
    "ElevationSurface",
    "SDFSurface",
]

__version__ = "0.2.0"
