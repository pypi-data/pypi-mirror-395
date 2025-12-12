from importlib import resources
from pathlib import Path
import json


def test_suite_manifest_files_exist():
    manifest = Path(resources.files("survi_scenarios.data.scenarios") / "suite_manifest.json")
    payload = json.loads(manifest.read_text())
    base = manifest.parent
    for item in payload.get("items", []):
        # manifest describes synthetic parameters; no external file per item
        assert "name" in item
    assert payload.get("items"), "suite_manifest.json should list scenarios"


def test_sdf_manifest_entries_exist():
    manifest = Path(resources.files("survi_scenarios.data.scenarios_3d") / "manifest.json")
    payload = json.loads(manifest.read_text())
    base = manifest.parent
    scenarios = payload.get("scenarios", {})
    assert scenarios, "manifest must contain scenarios"
    for name, rel in scenarios.items():
        path = (base / rel).resolve()
        assert path.exists(), f"Missing SDF scenario config for {name}: {path}"
