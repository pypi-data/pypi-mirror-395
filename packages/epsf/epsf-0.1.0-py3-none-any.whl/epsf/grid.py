from itertools import product
from pathlib import Path

from astropy.io import fits
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
from scipy.interpolate import RegularGridInterpolator

from epsf.utils import get_epsf_data_path
from epsf.plot import plot_mosaic
from epsf.epsf import EPSF


class EPSFGrid:
    """Object to store an effective PSF Grid

    An ePSF grid consists of a set of PSFs with their corresponding detector coordinates.
    It can then be called at the desired detector coordinate to generate an interpolated PSF.

    To create a grid from a ``JWST1PASS`` FITS file, see ``EPSFGrid.from_fits()``.

    :param x_grid: x coordinates of the ePSF grid. Should be 1D with shape ``(Npsf,)``.
    :param y_grid: y coordinates of the ePSF grid. Should be 1D with shape ``(Npsf,)``.
    :param grid: Array containing the grid of ePSF. Should be 3D with shape ``(Npsf, Npix, Npix)``.
    """

    def __init__(self, x_grid: np.ndarray, y_grid: np.ndarray, grid: np.ndarray):
        self.x = x_grid
        self.y = y_grid
        self.grid = grid

        self.file = None

        self.npsf = self.grid.shape[0]

        assert len(self.x) * len(self.y) == self.npsf

        # Use scipy linear interpolation
        # Fairly easy to write by hand but more trouble
        # Reshape grid so scipy understands x and y coordinates
        # (requires swaping 0 and 1 because numpy's first axis is y)
        # We want x to be passed first so the interpolator is not confusing
        self.interpolator = RegularGridInterpolator(
            (self.x, self.y),
            self.grid.reshape(self.y.size, self.x.size, *self.grid.shape[1:]).swapaxes(
                0, 1
            ),
        )

    def __repr__(self) -> str:
        base = f"EPSFGrid with {self.npsf} PSFs"
        if self.file is not None:
            base += f" from file {self.file}"
        return base

    @classmethod
    def from_params(
        cls, inst: str, filt: str, detector: str | None = None
    ) -> "EPSFGrid":
        inst = inst.upper()
        filt = filt.upper()
        if detector is not None:
            detector = detector.upper()
        if inst == "NIRISS":
            if detector is None or detector == "NIS":
                detector = "NIRISS"
            else:
                raise ValueError(
                    f"Unexpected detector name {detector} for instrument {inst}"
                )
        elif inst == "NIRCAM":
            allowed_detectors = (
                [f"NRCA{i}" for i in range(1, 5)]
                + [f"NRCB{i}" for i in range(1, 5)]
                + ["NRCAL", "NRCBL"]
            )
            if detector is None:
                raise TypeError(f"A detector name is rquired for instrument {inst}")
            elif detector not in allowed_detectors:
                raise ValueError(
                    f"Unexpected detector name {detector} for instrument {inst}"
                )
        else:
            raise ValueError(
                f"Instrument {inst} not available. Only NIRCam and NIRISS are."
            )

        epsf_filename = f"STDPSF_{detector}_{filt}.fits"
        jwst1pass_dir = get_epsf_data_path() / "jwst1pass"
        epsf_path = jwst1pass_dir / epsf_filename

        if epsf_path.is_file():
            return cls.from_fits(epsf_path)

        available_files = list(jwst1pass_dir.glob("STDPSF_*.fits"))
        raise FileNotFoundError(
            f"File {epsf_filename} not found. Available epsf files are {available_files}"
        )

    @classmethod
    def from_fits(cls, epsf_path: str | Path) -> "EPSFGrid":
        """Create EPSFGrid from a ``JWST1PASS`` FITS file.

        The fits file should ave a single extension with the PSF grid as data.
        The grid positions should be stored in IPSFX0i and JPSFY0j where i and j are the x and y indices for each position.

        :param epsf_path: Path to the ``JWST1PASS`` ePSF grid.
        """
        epsf_path = Path(epsf_path)
        with fits.open(epsf_path) as hdul:
            hdr = hdul[0].header
            grid = hdul[0].data

        # X and Y positions are stored in header
        x_grid = np.array([hdr[f"IPSFX0{i + 1}"] for i in range(5)])
        y_grid = np.array([hdr[f"JPSFY0{i + 1}"] for i in range(5)])

        epsf_grid = cls(x_grid, y_grid, grid)
        epsf_grid.file = epsf_path
        return epsf_grid

    def __call__(self, x: float, y: float, *args, **kwargs) -> EPSF:
        """
        Generate an EPSF object at the provided detector position.

        :param x: x cordinate on the detector
        :param x: y cordinate on the detector
        """
        xy_star = np.array([x, y])

        epsf = self.interpolator(xy_star)[0]
        return EPSF(epsf, *args, **kwargs)

    def plot(self) -> tuple[Figure, Axes]:
        """
        Plot the ePSF grid as a mosaic.

        Calls ``epsf.plot.plot_mosaic()``.

        :return: Figure and Axes objects e plot
        """
        titles = [f"({c[1]}, {c[0]})" for c in product(self.x, self.y)]
        fig, axs = plot_mosaic(
            self.grid,
            self.x.size,
            self.y.size,
            imshow_kwargs={"vmax": np.quantile(self.grid, 0.95)},
            titles=titles,
        )
        fig.suptitle("ePSF grid with positions on the detector")
        return fig, axs
