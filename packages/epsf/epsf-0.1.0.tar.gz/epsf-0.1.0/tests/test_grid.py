import glob

import numpy as np
import pytest

from epsf.grid import EPSFGrid


def get_jwst1pass_cases():
    jwst1pass_files = glob.glob("src/epsf/data/jwst1pass/*.fits")
    cases = []
    for jwst1pass_file in jwst1pass_files:
        grid = EPSFGrid.from_fits(jwst1pass_file)
        grid_points = np.stack(np.meshgrid(grid.x, grid.y)).reshape(2, -1).T
        for i, (x, y) in enumerate(grid_points):
            cases.append((grid, x, y, i))
    return cases


cases = get_jwst1pass_cases()


@pytest.mark.parametrize("grid,x,y,i", cases)
def test_interp_point(grid, x, y, i):
    np.testing.assert_allclose(grid(x, y).array, grid.grid[i])


def test_from_params():
    EPSFGrid.from_params("NIRISS", "F480M")
    EPSFGrid.from_params("NIRCAM", "F480M", detector="NRCAL")
    EPSFGrid.from_params("NIRCAM", "F150W", detector="NRCB1")
    with pytest.raises(FileNotFoundError):
        EPSFGrid.from_params("NIRCAM", "F480M", detector="NRCB1")
    with pytest.raises(TypeError):
        EPSFGrid.from_params("NIRCAM", "F150W")
    with pytest.raises(ValueError):
        EPSFGrid.from_params("NIRCAM", "F150W", detector="NRCAA")
