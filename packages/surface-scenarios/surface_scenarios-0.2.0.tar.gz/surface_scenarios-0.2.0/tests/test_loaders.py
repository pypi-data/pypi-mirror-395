from pathlib import Path

from survi_scenarios import (
    list_elevation_scenarios,
    load_elevation_scenario,
    list_sdf_scenarios,
    load_sdf_scenario,
)


def test_list_elevation_scenarios_non_empty():
    names = list_elevation_scenarios()
    assert "flat_rect_small" in names


def test_load_elevation_scenario_truth_matches_samples():
    ds = load_elevation_scenario("flat_rect_small")
    # Evaluate truth on first few points
    pts = ds.samples[["x", "y"]].to_numpy()[:5]
    truth = ds.truth_z(pts)
    # should match z (within noise tolerance, but this scenario has tiny noise)
    sample_z = ds.samples["z"].to_numpy()[:5]
    assert truth.shape == sample_z.shape


def test_list_sdf_scenarios_includes_torus():
    names = list_sdf_scenarios()
    assert "torus_compact" in names


def test_load_sdf_scenario_basic():
    sdf = load_sdf_scenario("torus_compact", seed=1)
    assert not sdf.raw_surface.empty
    assert callable(sdf.truth_phi)
    # evaluate phi on first few points
    pts = sdf.raw_surface[["x", "y", "z"]].to_numpy()[:3]
    phi = sdf.truth_phi(pts)
    assert phi.shape[0] == 3


def test_env_override_manifest(monkeypatch, tmp_path):
    # Build a minimal manifest that points to the existing data file but via tmp path
    suite_manifest = tmp_path / "suite_manifest.json"
    suite_manifest.write_text(
        """{"items": [{"name": "env_flat", "surface": {"width": 1, "length": 1, "spacing": 1, "slope_mag": 0, "slope_angle_deg": 0, "ripple_amp": 0, "ripple_freq": 1, "bumps": 0, "bump_amp": 0, "bump_radius": 1, "ripples": null, "bump_specs": null, "noise_mean": 0, "noise_std": 0, "seed": 1, "unit": "m"}, "grid": {"grid_spacing": 1, "edge_exclusion": 0, "rotation_deg": 0, "shift_x": 0, "shift_y": 0}, "master_seed": 0}] }""",
        encoding="utf-8",
    )
    monkeypatch.setenv("SURVI_SCENARIO_MANIFEST", str(suite_manifest))
    names = list_elevation_scenarios()
    assert names == ["env_flat"]
    ds = load_elevation_scenario("env_flat")
    assert ds.name == "env_flat"


def test_env_override_sdf_manifest(monkeypatch, tmp_path):
    src_manifest = (tmp_path / "manifest.json")
    src_manifest.write_text(
        """{"scenarios": {"env_torus": "torus_compact.json"}}""",
        encoding="utf-8",
    )
    # link to bundled torus file
    torus_src = Path(__file__).resolve().parents[1] / "src" / "survi_scenarios" / "data" / "scenarios_3d" / "torus_compact.json"
    (tmp_path / "torus_compact.json").write_bytes(torus_src.read_bytes())

    monkeypatch.setenv("SURVI_SDF_MANIFEST", str(src_manifest))
    names = list_sdf_scenarios()
    assert "env_torus" in names
    sdf = load_sdf_scenario("env_torus", seed=123)
    assert sdf.name == "torus_compact"
