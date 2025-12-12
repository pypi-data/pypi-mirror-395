import pathlib

import numpy as np
import pytest
import xarray as xr

from pywrb.xarray import xarray_from_wrb, xarray_to_wrb

xarray = pytest.importorskip("xarray")


def test_engine_registration():
    ds = xr.open_dataset(pathlib.Path(__file__).parent / "fixtures/real_world.wrb", engine="pywrb")
    assert isinstance(ds, xr.Dataset)

    other_ds = xarray_from_wrb(pathlib.Path(__file__).parent / "fixtures/real_world.wrb")
    xarray.testing.assert_allclose(ds, other_ds)


def test_extension_registration(tmp_path):
    ds = xarray_from_wrb(pathlib.Path(__file__).parent / "fixtures/real_world.wrb")
    ds.pywrb.to_wrb(tmp_path / "test.wrb")

    other_ds = xarray_from_wrb(tmp_path / "test.wrb")
    xarray.testing.assert_allclose(ds, other_ds)


def test_real_wrb_to_xarray():
    ds = xarray_from_wrb(pathlib.Path(__file__).parent / "fixtures/real_world.wrb")

    assert ds["elevation"].dims == ("y", "x")
    assert ds["roughness_length"].dims == ("y", "x")
    assert ds["weibull_scale"].dims == ("heights", "directions", "y", "x")
    assert ds["weibull_shape"].dims == ("heights", "directions", "y", "x")
    assert ds["power"].dims == ("heights", "y", "x")
    assert ds["probability"].dims == ("heights", "directions", "y", "x")
    assert ds["inflow_angle"].dims == ("heights", "directions", "y", "x")


def test_generate_wrb(tmp_path):
    dst = tmp_path / "test.wrb"

    n_x, n_y, n_directions, n_wind_speed, n_heights = 128, 128, 12, 10, 3

    ds = xr.Dataset(
        data_vars=dict(
            weibull_scale=(["x", "y", "directions", "heights"], np.random.randn(n_x, n_y, n_directions, n_heights)),
            weibull_shape=(["x", "y", "directions", "heights"], np.random.randn(n_x, n_y, n_directions, n_heights)),
            wind_shear_exponent=(["x", "y", "directions"], np.random.randn(n_x, n_y, n_directions)),
            inflow_angle=(["x", "y", "directions", "heights"], np.random.randn(n_x, n_y, n_directions, n_heights)),
            turbulence_intensity=(
                ["x", "y", "directions", "wind_speeds", "heights"],
                np.random.randn(n_x, n_y, n_directions, n_wind_speed, n_heights),
            ),
            elevation=(["x", "y"], np.ones((n_x, n_y))),
            roughness_length=(["x", "y"], np.ones((n_x, n_y))),
            probability=(
                ["x", "y", "directions", "wind_speeds", "heights"],
                (lambda a: a / np.linalg.norm(a))(np.random.rand(n_x, n_y, n_directions, n_wind_speed, n_heights)),
            ),
        ),
        coords=dict(
            x=(["x"], np.arange(n_x)),
            y=(["y"], np.arange(n_y)),
            directions=(["directions"], np.linspace(0, 360, n_directions, endpoint=False)),
            wind_speeds=(["wind_speeds"], np.linspace(6, 15, n_wind_speed)),
            heights=(["heights"], [100, 150, 200]),
        ),
    )
    ds = ds.rio.write_crs("epsg:4326")

    xarray_to_wrb(ds, dst)

    new_ds = xarray_from_wrb(dst)

    ds = ds.transpose(*new_ds["turbulence_intensity"].dims)
    xr.testing.assert_allclose(ds, new_ds)
