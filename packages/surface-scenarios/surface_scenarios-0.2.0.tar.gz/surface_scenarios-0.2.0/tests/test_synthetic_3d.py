import numpy as np
from survi_scenarios.synthetic_3d import Sphere, Torus, Union


def test_sphere_phi_and_gradient():
    sphere = Sphere(center=(0.0, 0.0, 0.0), radius=1.0)
    pts = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    phi = sphere.phi(pts)
    assert phi[0] == 0.0  # on surface
    assert phi[1] == -1.0
    grad = sphere.gradient(pts)
    np.testing.assert_allclose(grad[0], [1.0, 0.0, 0.0])


def test_torus_phi_signs():
    torus = Torus(major_radius=0.8, minor_radius=0.25)
    pts = np.array([[1.3, 0.0, 0.0], [0.8, 0.0, 0.0]])
    phi = torus.phi(pts)
    assert phi[0] > 0  # outside
    assert phi[1] < 0  # inside


def test_union_selects_min():
    a = Sphere(center=(0, 0, 0), radius=1)
    b = Sphere(center=(2, 0, 0), radius=1)
    u = Union(a, b)
    pts = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    phi = u.phi(pts)
    assert phi[2] == 0.0  # mid-point lies on both surfaces
    assert phi[0] == -1.0
    assert phi[1] == -1.0
