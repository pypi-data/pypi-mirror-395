import numpy as np
from survi_scenarios.synthetic import SurfaceParams, RippleSpec, make_surface_df


def test_surface_df_shape_and_seed():
    params = SurfaceParams(width=4.0, length=3.0, spacing=1.0, ripples=[RippleSpec(amp=0.1, wavelength=2.0)], seed=42)
    df = make_surface_df(params)
    # (length/spacing +1) * (width/spacing +1) samples
    assert len(df) == 5 * 4
    # deterministic seed
    df2 = make_surface_df(params)
    np.testing.assert_allclose(df["z"].to_numpy(), df2["z"].to_numpy())
