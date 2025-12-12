# Synthetic 2.5D surface generators extracted from Survi
from __future__ import annotations
from dataclasses import dataclass, fields
import math
import numpy as np
import pandas as pd
from shapely.affinity import rotate as _rotate_poly
from shapely.geometry import Polygon
from shapely.ops import unary_union

from .units import Unit, convert_unit
from .rng import numpy_rng


# ────────────────────────────────────────────────────────────────────────────
#  New components
# ────────────────────────────────────────────────────────────────────────────

@dataclass(slots=True)
class RippleSpec:
    """One sinusoidal ripple component."""
    amp: float = 0.0               # meters
    angle_deg: float = 0.0         # CCW from +x axis
    wavelength: float | None = None  # meters (preferred)
    cycles_across_diag: float | None = None  # dimensionless alternative

@dataclass(slots=True)
class BumpSpec:
    """One Gaussian bump or hollow."""
    amp: float                      # meters, sign controls bump (+) or hollow (-)
    radius: float                   # meters (1 sigma)
    center: tuple[float, float] | None = None  # (x,y). If None, RNG picks.

# ────────────────────────────────────────────────────────────────────────────
#  Surface synthesis
# ────────────────────────────────────────────────────────────────────────────

@dataclass(slots=True)
class SurfaceParams:
    width: float = 10.0
    length: float = 10.0
    spacing: float = 0.10
    slope_mag: float = 0.0
    slope_angle_deg: float = 0.0
    # legacy single ripple (kept for back compat)
    ripple_amp: float = 0.0
    ripple_freq: float = 1.0
    # legacy uniform bumps (kept for back compat)
    bumps: int = 0
    bump_amp: float = 0.0
    bump_radius: float = 0.5
    # new flexible components
    ripples: list[RippleSpec] | None = None
    bump_specs: list[BumpSpec] | None = None

    noise_mean: float = 0.0
    noise_std: float = 0.0
    seed: int | None = None
    unit: Unit = Unit.METERS

    def __post_init__(self):
        if self.unit == Unit.METERS:
            return
        cf = convert_unit(1.0, self.unit, Unit.METERS)  # to meters

        distance_fields = {
            "width", "length", "spacing", "ripple_amp", "bump_amp",
            "bump_radius", "noise_mean", "noise_std"
        }
        inverse_distance_fields = {"ripple_freq"}  # cycles per diag length proxy

        for f in fields(self):
            name = f.name; val = getattr(self, name)
            if val is None:
                continue
            if name in distance_fields:
                setattr(self, name, val * cf)
            elif name in inverse_distance_fields:
                setattr(self, name, val / cf)

        # nested conversions
        if self.ripples:
            for r in self.ripples:
                r.amp *= cf
                if r.wavelength is not None:
                    r.wavelength *= cf
        if self.bump_specs:
            for b in self.bump_specs:
                b.amp *= cf
                b.radius *= cf
                if b.center is not None:
                    b.center = (b.center[0] * cf, b.center[1] * cf)

        self.unit = Unit.METERS

def make_surface_df(p: SurfaceParams) -> pd.DataFrame:
    """Return a validated-like DataFrame with (x,y,z)."""
    rng = numpy_rng(p.seed, namespace="synthetic.surface")

    nx = int(math.floor(p.width / p.spacing)) + 1
    ny = int(math.floor(p.length / p.spacing)) + 1

    xs = np.linspace(0, p.width, nx)
    ys = np.linspace(0, p.length, ny)
    X, Y = np.meshgrid(xs, ys, indexing="xy")

    # slope
    theta = math.radians(p.slope_angle_deg)
    Z = p.slope_mag * (X * math.cos(theta) + Y * math.sin(theta))

    # new: multiple ripples
    if p.ripples:
        diag = math.hypot(p.width, p.length)
        for r in p.ripples:
            ang = math.radians(r.angle_deg)
            s = X * math.cos(ang) + Y * math.sin(ang)  # coordinate along direction
            if r.wavelength and r.wavelength > 0:
                Z += r.amp * np.sin(2 * math.pi * s / r.wavelength)
            elif r.cycles_across_diag and diag > 0:
                wl = diag / r.cycles_across_diag
                Z += r.amp * np.sin(2 * math.pi * s / wl)
    else:
        # legacy single ripple (unchanged semantics)
        if p.ripple_amp:
            diag = math.hypot(p.width, p.length)
            if diag > 0:
                Z += p.ripple_amp * np.sin(2 * math.pi * p.ripple_freq * (X + Y) / diag)

    # new: flexible bumps
    if p.bump_specs:
        for b in p.bump_specs:
            if b.center is None:
                cx = rng.uniform(0, p.width)
                cy = rng.uniform(0, p.length)
            else:
                cx, cy = b.center
            r2 = (X - cx) ** 2 + (Y - cy) ** 2
            Z += b.amp * np.exp(-r2 / (b.radius ** 2))
    else:
        # legacy uniform bumps
        for _ in range(p.bumps):
            cx = rng.uniform(0, p.width)
            cy = rng.uniform(0, p.length)
            amp = rng.uniform(-p.bump_amp, p.bump_amp)
            r2 = (X - cx) ** 2 + (Y - cy) ** 2
            Z += amp * np.exp(-r2 / (p.bump_radius ** 2))

    if p.noise_std > 0:
        Z += rng.normal(loc=p.noise_mean, scale=p.noise_std, size=Z.shape)

    return pd.DataFrame({"x": X.ravel(), "y": Y.ravel(), "z": Z.ravel()})

# polygon helpers (unchanged)
def make_rectangle(width: float, length: float) -> Polygon:
    return Polygon([(0, 0), (width, 0), (width, length), (0, length)])

def make_l_shape(width: float, length: float, notch: float) -> Polygon:
    if notch <= 0 or notch >= min(width, length):
        raise ValueError("`notch` must be positive and smaller than both sides")
    outer = Polygon([(0, 0), (width, 0), (width, length), (0, length)])
    notch_poly = Polygon([(width-notch, 0), (width, 0), (width, notch), (width-notch, notch)])
    poly = unary_union(outer.difference(notch_poly))
    if not poly.is_valid or poly.geom_type != "Polygon":
        raise RuntimeError("L-shape generation failed")
    return poly

def random_convex_polygon(
    centre: tuple[float, float],
    radius: float,
    vertices: int = 8,
    angle_jitter: float = 0.15,
    seed: int | None = None,
) -> Polygon:
    """
    Generate a random (roughly) convex polygon around `centre` with
    `vertices` points and average radius `radius`.
    """
    rng = numpy_rng(seed, namespace="synthetic.random_polygon")
    angles = np.linspace(0, 2 * math.pi, vertices, endpoint=False)
    angles += rng.uniform(-angle_jitter, angle_jitter, size=vertices)
    rng.shuffle(angles)

    pts = [
        (
            centre[0] + radius * rng.uniform(0.85, 1.15) * math.cos(a),
            centre[1] + radius * rng.uniform(0.85, 1.15) * math.sin(a),
        )
        for a in angles
    ]
    poly = Polygon(pts).convex_hull
    if not poly.is_valid:
        poly = poly.buffer(0)  # fix self-intersections if any
    return poly

def rotate_polygon(poly: Polygon, deg: float, origin: tuple[float, float] | str = "centroid") -> Polygon:
    return _rotate_poly(poly, deg, origin=origin, use_radians=False)

__all__ = [
    "SurfaceParams",
    "RippleSpec",
    "BumpSpec",
    "make_surface_df",
    "make_rectangle",
    "make_l_shape",
    "random_convex_polygon",
    "rotate_polygon",
]
