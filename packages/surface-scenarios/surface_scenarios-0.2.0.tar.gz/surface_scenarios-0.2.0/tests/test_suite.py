from survi_scenarios.suite import ScenarioSuite
from survi_scenarios.loaders import _default_suite_manifest


def test_load_suite_and_names():
    suite = ScenarioSuite.load_manifest(str(_default_suite_manifest()))
    names = suite.names()
    assert "flat_rect_small" in names
    scenario = suite.get(names[0])
    mat = scenario.materialize()
    assert not mat.master_points.empty
    assert not mat.grid_with_z.empty
