import numpy as np
from scipy.interpolate import RectBivariateSpline

class EPSF:
    """Effective point spread function

    Python object to store an empirical PSF function.
    Once created, the Python object can be called to generate a PSF with the desired offset in pixels.

    :param epsf: Array with the (oversampled) epsf pixel values
    :param true_size: Size (in pixels) of the output images from the epsf.
    :param oversampling: Oversampling factor between the epsf pixel and the detector pixels.
    """
    def __init__(self, epsf: np.ndarray, true_size: int = 11, oversampling: int = 4):
        self.ny, self.nx = epsf.shape
        x = np.arange(self.nx)  # axis that goes to the right with origin=lower
        y = np.arange(self.ny)  # axis that goes up with origin=lower
        self.array = epsf
        self.spl = RectBivariateSpline(x, y, epsf)
        self.true_size = true_size
        self.oversampling = oversampling

    def __repr__(self):
        return f"EPSF(true_size={self.true_size}, oversampling={self.oversampling})"

    def __call__(self, x: float, y: float) -> np.ndarray:
        """Generate a PSF at the ``(x, y)`` detector coordinates

        :param x: x coordinate on the detector
        :param y: y coordinate on the detector
        """

        # Hardcoded for a 11x11 cutout
        start = - (self.true_size // 2)
        end = self.true_size // 2 + self.true_size % 2
        dx_grid = np.arange(start, end) - x
        dy_grid = np.arange(start, end) - y

        # These assume the 4x oversampled 101x101 grid from Jay Anderson's jwst1pass
        x_grid = self.nx // 2 + self.oversampling * dx_grid
        y_grid = self.ny // 2 + self.oversampling * dy_grid

        psf = self.spl(x_grid, y_grid)
        return psf / np.sum(psf)
