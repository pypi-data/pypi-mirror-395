# survi-scenarios

Standalone synthetic elevation and 3D SDF scenario library extracted from the Survi project. Bundles the original synthetic datasets and generators, with a slim API for listing and loading scenarios, plus analytic truth functions for evaluation.

## Status
Work in progress: early extraction from Survi. Surface generators and manifests are present; adapters are being slimmed down to remove Survi-specific dependencies.

## Environment overrides
- `SURVI_SCENARIO_MANIFEST`: custom path for the elevation suite manifest.
- `SURVI_SDF_MANIFEST`: custom path for the SDF manifest.

## Usage (planned)
```python
from survi_scenarios import list_elevation_scenarios, load_elevation_scenario

names = list_elevation_scenarios()
dataset = load_elevation_scenario(names[0])
print(dataset.samples.head())
```

## Tests
```
PYTHONPATH=src pytest tests -q
```

## Install
```
pip install surface-scenarios
```
