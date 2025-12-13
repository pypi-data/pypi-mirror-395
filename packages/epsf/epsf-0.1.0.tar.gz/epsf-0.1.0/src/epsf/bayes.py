from epsf.epsf import EPSF
import numpy as np
from simpple.model import ForwardModel


# TODO: Could the model classes be simplified/joined?
class EPSFModel(ForwardModel):
    expected_keys = []
    optional_keys = []

    def __init__(self, parameters):
        super().__init__(parameters)
        all_keys = self.expected_keys + self.optional_keys
        for k in self.expected_keys:
            assert k in parameters, f"Expected parameter {k} in SingleModel"
        for pname in parameters:
            assert pname in all_keys, (
                f"Unexpected parameter {pname} found in SingleModel"
            )

    def _log_likelihood(self, p: dict, img: np.ndarray, err: np.ndarray):
        img_mod = self._forward(p)
        s2 = (p.get("fnoise", 1.0) * err) ** 2 + p.get("sigma", 0) ** 2
        return -0.5 * np.nansum(np.log(2 * np.pi * s2) + (img - img_mod) ** 2 / s2)


class SingleModel(EPSFModel):
    expected_keys = ["flux", "x0", "y0"]
    optional_keys = ["bkg", "sigma", "fnoise"]

    def __init__(self, parameters: dict, psf: EPSF):
        super().__init__(parameters)
        self.epsf = psf

    def _forward(self, p: dict):
        return p["flux"] * self.epsf(p["x0"], p["y0"]) + p.get("bkg", 0)


class SingleModelMulti(EPSFModel):
    expected_keys = ["flux"]
    optional_keys = ["bkg", "sigma", "fnoise"]

    def __init__(self, parameters, psf_list: list[EPSF]):
        self.epsf_list = psf_list
        self.npsf = len(psf_list)
        for i in range(self.npsf):
            self.expected_keys += [f"x0{i}", f"y0{i}"]
        super().__init__(parameters)

    def _forward(self, p: dict):
        # Assumes all epsfs have the same true size
        out = np.empty(
            (self.npsf, self.epsf_list[0].true_size, self.epsf_list[0].true_size)
        )
        # TODO: Bkg shared vs multi
        for i in range(self.npsf):
            out[i] = p["flux"] * self.epsf_list[i](p[f"x0{i}"], p[f"y0{i}"]) + p.get(
                "bkg", 0
            )
        return out


class BinaryModel(EPSFModel):
    expected_keys = ["flux", "x0", "y0", "sep", "pa", "cr"]
    optional_keys = ["bkg", "sigma", "fnoise"]

    def __init__(self, parameters, psf: EPSF):
        super().__init__(parameters)
        self.epsf = psf

    def _forward(self, p: dict):
        x0, y0, flux = p["x0"], p["y0"], p["flux"]
        sep, pa, cr = p["sep"], p["pa"], p["cr"]
        bkg = p.get("bkg", 0)
        dx = sep * np.cos(np.radians(pa))
        dy = sep * np.sin(np.radians(pa))
        primary_psf = self.epsf(x0, y0)
        secondary_psf = self.epsf(x0 + dx, y0 + dy)
        return flux * (primary_psf + cr * secondary_psf) + bkg


class BinaryModelMulti(EPSFModel):
    expected_keys = ["flux", "sep", "pa", "cr"]
    optional_keys = ["bkg", "sigma", "fnoise"]

    def __init__(self, parameters, psf_list: list[EPSF]):
        self.epsf_list = psf_list
        self.npsf = len(psf_list)
        for i in range(self.npsf):
            self.expected_keys += [f"x0{i}", f"y0{i}"]

        super().__init__(parameters)

    def _forward(self, p: dict):
        # Assumes all epsfs have the same true size
        out = np.empty(
            (self.npsf, self.epsf_list[0].true_size, self.epsf_list[0].true_size)
        )
        flux = p["flux"]
        sep, pa, cr = p["sep"], p["pa"], p["cr"]
        # TODO: Bkg shared vs multi
        bkg = p.get("bkg", 0)
        dx = sep * np.cos(np.radians(pa))
        dy = sep * np.sin(np.radians(pa))
        for i in range(self.npsf):
            x0, y0 = p[f"x0{i}"], p[f"y0{i}"]
            primary_psf = self.epsf_list[i](x0, y0)
            secondary_psf = self.epsf_list[i](x0 + dx, y0 + dy)
            out[i] = flux * (primary_psf + cr * secondary_psf) + bkg
        return out
