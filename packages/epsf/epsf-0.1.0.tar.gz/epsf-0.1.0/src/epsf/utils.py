import os
from pathlib import Path

import numpy as np
from astropy.io import fits
from photutils.centroids import centroid_quadratic


def get_epsf_data_path() -> Path:
    """Get the EPSF data directory path

    Returns EPSF_PATH env var if set, otherwise ~/.local/share/epsf

    :return: Path to EPSF data directory
    """
    epsf_path = os.environ.get("EPSF_PATH")
    if epsf_path:
        return Path(epsf_path)
    else:
        return Path.home() / ".local/share/epsf"


def seppa2radec(
    sep: float | np.ndarray, pa: float | np.ndarray
) -> tuple[float | np.ndarray]:
    """Convert separation and position angle (PA) to RA and Dec

    PA = 0 is along the Y axis (north) and RA increases to the left (east)

    :param sep: Separation in mas
    :param pa: Position angle in deg
    :return: RA and Dec in mas
    """
    pa_rad = np.deg2rad(pa)

    # PA = 0 is along the Y axis (North)
    ddec = sep * np.cos(pa_rad)
    # RA increases to the left (East)
    dra = sep * np.sin(pa_rad)

    return dra, ddec


def radec2seppa(
    ra: float | np.ndarray, dec: float | np.ndarray
) -> tuple[float | np.ndarray]:
    """Convert RA and Dec to separation and position angle (PA)

    PA = 0 is along the Y axis (north) and RA increases to the left (east)

    :param ra: RA in mas
    :param dec: Dec in mas
    :return: Separation and PA in mas and deg, respectively
    """
    sep = np.sqrt(ra**2 + dec**2)
    # RA is like y, dec like x
    pa = np.rad2deg(np.arctan2(ra, dec))

    return sep, pa


def get_cutout(img: np.ndarray, pos: tuple[int, int], half_size: int) -> np.ndarray:
    """
    Get a cutout from an image around a given position.

    :param img: Array to take a cutout from with shape ``(Ny, Nx)``
    :param pos: indices of the x and y positions around which to take a cutout
    :param half_size: Half-size of the cutout to extract
    :return: Returns a copy of the desired cutout from the original image
    """
    x, y = pos
    crop_ind = np.s_[y - half_size : y + half_size, x - half_size : x + half_size]
    img_cut = img[crop_ind].copy()
    return img_cut


def get_final_img(
    img: np.ndarray, final_size: int, pos_int: tuple[int] | None = None
) -> np.ndarray:
    """
    Get a cutout with size ``final_size`` around a given position in an image.
    This is very similar to ``get_cutout()``.
    ``get_cutout()`` was written to extract a wider array from a full-frame image while this function was written to extract the final, small cutout from a single-PSF image.

    Concretely, the main differences are that ``get_cutout()`` requires a position and an ``half_size``, while here we use the final size of the image and take the middle pixel by default.

    :param img: Array to take a cutout from with shape ``(Ny, Nx)``
    :param final_size: Final size of the cutout, in pixels
    :param pos: indices of the x and y positions around which to take a cutout. Take the central pixel if None. Defaults to None.
    :return: Returns a copy of the desired cutout from the original image.
    """
    if pos_int is None:
        pos_int = img.shape[1] // 2, img.shape[0] // 2
    x_int, y_int = pos_int
    start, end = final_size // 2, final_size // 2 + final_size % 2
    x1, x2, y1, y2 = x_int - start, x_int + end, y_int - start, y_int + end
    img = img[y1:y2, x1:x2].copy()
    return img


def open_jwst_image(
    path: Path,
    pos_cut: tuple[int, int] | None = None,
    half_size_cut: int | None = None,
    final_size: int | None = None,
    recenter: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Open a JWST image with uncertainties

    :param path: Path to a JWST cal file (output of the stage 2 image pipeline).
    :param pos_cut: Rough position of the target in the full-frame image. Used to center a first cutout.
    :param half_size: Half size of the first cutout taken from the full-frame image in pixels.
    :param final_size: Size of the final image to return in pixels.
    :param recenter: Refine the centroid after the first cutout if True. Uses ``photutils.centroids.centroid_quadratic()``.
    :return: Science image and associated uncertainties (``SCI`` and ``ERR`` extensions).
    """
    with fits.open(path) as hdul:
        img = hdul["SCI"].data
        err = hdul["ERR"].data
    if half_size_cut is not None:
        if pos_cut is None:
            pos_cut = img.shape[1] // 2, img.shape[0] // 2
        img = get_cutout(img, pos=pos_cut, half_size=half_size_cut)
        err = get_cutout(err, pos=pos_cut, half_size=half_size_cut)
    elif pos_cut is not None:
        raise TypeError("pos_cut is not None but half_size cut is None")

    if recenter:
        xy_centroid = centroid_quadratic(img, mask=np.isnan(img))
        pos_int = np.round(xy_centroid).astype(int)
    else:
        pos_int = None

    if final_size is not None:
        img = get_final_img(img, final_size, pos_int=pos_int)
        err = get_final_img(err, final_size, pos_int=pos_int)

    return img, err


def download_jwst1pass(overwrite: bool = False):
    """Download all FITS files from JWST1PASS library

    Downloads to EPSF_PATH/jwst1pass if EPSF_PATH env var is set, otherwise to ~/.local/share/epsf/jwst1pass

    :param overwrite: If True, use timestamping to update existing files. If False, skip existing files.
    """
    import subprocess

    base_url = "https://www.stsci.edu/~jayander/JWST1PASS/LIB/PSFs/STDPSFs/"

    download_dir = get_epsf_data_path() / "jwst1pass"

    download_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading FITS files to {download_dir}...")

    wget_args = [
        "wget",
        "--recursive",
        "--no-parent",
        "--no-directories",
        "--accept",
        "*.fits",
        "--reject",
        "index.html*",
        "--directory-prefix",
        str(download_dir),
    ]

    if overwrite:
        wget_args.append("--timestamping")
    else:
        wget_args.append("--no-clobber")

    wget_args.append(base_url)

    subprocess.run(wget_args, check=True)

    print(f"Download complete. FITS files saved to {download_dir}/")
