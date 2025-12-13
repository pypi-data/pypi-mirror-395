from collections.abc import Iterable
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar
from matplotlib.colors import LogNorm, SymLogNorm
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from simpple.model import Model


def plot_mosaic(
    cube: np.ndarray | list[np.ndarray],
    nrows: int,
    ncols: int,
    titles: list[str] | None = None,
    ytitles: list[str] | None = None,
    xtitles: list[str] | None = None,
    colorbar: bool = True,
    imshow_kwargs: dict | None = None,
) -> tuple[Figure, Axes]:
    """
    Plot an image cube in a mosaic display.

    :param cube: Image cube with shape ``(Nimg, Ny, Nx)``
    :param nrows: Number of rows in the mosaic
    :param cols: Number of rows in the mosaic
    :param titles: List of titles to use
    :param xtitles: List of titles for each column.
    :param ytitles: List of titles for each row.
    :param colorbar: Show a colorbar for each panel if ``True``.
    :param imshow_kwargs: Keyword arguments passed to imshow for all panels.
    :return: Figure and Axes used to create the plot.
    """
    if nrows / ncols > 4.0:
        height_factor = 1.5
    elif nrows / ncols >= 1.5:
        height_factor = nrows / ncols
    else:
        height_factor = 1.0
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(4 * ncols / height_factor, 4 * nrows),
        dpi=100,
        squeeze=False,
        sharex=True,
        sharey=True,
    )
    assert axes.size >= len(cube), "There are less axes in grid than datasets in cube"

    for i, img in enumerate(cube):
        ax = axes[np.unravel_index(i, axes.shape)]
        # Symlog avoids having blank pixels when slightly < 0
        default_kwargs = {"norm": "symlog"}
        if imshow_kwargs is not None:
            imshow_kwargs = default_kwargs | imshow_kwargs
        else:
            imshow_kwargs = default_kwargs
        im = ax.imshow(img, **imshow_kwargs, origin="lower")
        # Ticks clutter the figure and we don't really need them here
        ax.set_xticks([])
        ax.set_yticks([])
        if titles is not None:
            ax.set_title(titles[i])

        if colorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            cb = fig.colorbar(im, cax=cax)
            cb.formatter = lambda x, _: f"{x:.2f}"
    if ytitles is not None:
        assert len(ytitles) == nrows
        for i, ax in enumerate(axes[:, 0]):
            ax.set_ylabel(ytitles[i], size=rcParams["axes.titlesize"])
    if xtitles is not None:
        assert len(xtitles) == ncols
        for i, ax in enumerate(axes[0]):
            ax.set_title(xtitles[i])

    for i in range(len(cube), axes.size):
        ax = axes[np.unravel_index(i, axes.shape)]
        fig.delaxes(ax)

    return fig, axes


def plot_image(
    img: np.ndarray,
    scale: str = "log",
    ax: Optional[Axes] = None,
    fig: Optional[Figure] = None,
    color_label: Optional[str] = None,
    return_colorbar: bool = False,
    **kwargs,
) -> tuple[Figure, Axes] | tuple[Figure, Axes, Colorbar]:
    """Plot an image with a given scaling and axes

    Simple wrapper to handle proper scaling, colorbar and axis names

    :param img: Image array
    :param scale: Scale to apply. If a "norm" kwarg is present, it will override this setting. Symlog uses a treshold of 1e-3 of the max.
    :param ax: Axis. Current axis (`plt.gca()`) is used if None.
    :param fig: Figure. Current figure (`plt.gcf()`) is used if None.
    :return: Figure and axis
    """
    if fig is None:
        fig = plt.gcf()
    if ax is None:
        ax = plt.gca()

    if "norm" in kwargs:
        norm = kwargs.pop("norm")
    elif scale == "log":
        norm = LogNorm(vmin=kwargs.pop("vmin", None), vmax=kwargs.pop("vmax", None))
    elif scale == "symlog":
        norm = SymLogNorm(
            linthresh=np.nanmax(img) * 1e-3,
            vmin=kwargs.pop("vmin", None),
            vmax=kwargs.pop("vmax", None),
        )
    else:
        norm = None

    im = ax.imshow(img, norm=norm, origin="lower", **kwargs)
    ax.set_xlabel("X [pix]")
    ax.set_ylabel("Y [pix]")
    cb = fig.colorbar(im, ax=ax, label=color_label)
    if return_colorbar:
        return fig, ax, cb
    return fig, ax


def plot_with_diff(
    img1: np.ndarray,
    img2: np.ndarray,
    scale: Union[str, list] = "log",
    fig: Optional[Figure] = None,
    axes: Optional[Axes] = None,
) -> tuple[Figure, Axes]:
    """Simple 3-panel plot with two images and their difference

    If fig or axes is passed, the current figure will be

    :param img1: First image
    :param img2: Second image
    :param scale: Scale to use. Log will automatically use symlog for the diff. Pass a list to override per-panel.
    :param fig: Figure to use. 3-panel figure created if None.
    :param axes: Axes to use. Indices 0-2 will be used. Make sure they exist.
    :return: Tuple with figure and axes
    """
    img_res = img1 - img2

    if scale == "log":
        scales = ["log", "log", "symlog"]
    elif isinstance(scale, str) or not isinstance(scale, Iterable):
        scales = [scale] * 3
    else:
        scales = scale

    if fig is not None:
        if axes is None:
            axes = []
            for i in range(3):
                axes.append(fig.add_subplot(1, 3, i + 1))
    elif axes is not None:
        fig = axes[0].get_figure()
    else:
        fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(16, 4))

    plot_image(img1, ax=axes[0], scale=scales[0], fig=fig)
    plot_image(img2, ax=axes[1], scale=scales[1], fig=fig)
    plot_image(img_res, ax=axes[2], scale=scales[2], fig=fig)

    return fig, axes


def plot_flat_samples(
    img: np.ndarray,
    err: np.ndarray,
    samples: np.ndarray,
) -> tuple[Figure, Axes]:
    fig, axs = plt.subplots(2, 1, gridspec_kw={"height_ratios": (3, 1)})
    x_img = np.arange(img.size)
    axd, axr = axs
    res_samples = samples - img

    axd.errorbar(
        x_img,
        img.ravel(),
        yerr=err.ravel(),
        fmt="k.",
        capsize=2,
        label="Image data",
        mfc="w",
    )
    for i, ypred in enumerate(samples):
        axd.plot(
            x_img,
            ypred.ravel(),
            ".",
            color="C0",
            alpha=0.1,
            label="Posterior samples" if i == 0 else None,
        )
    axd.set_ylabel("Count rate [DN/s]")

    axr.fill_between(
        x_img,
        -err.ravel(),
        err.ravel(),
        alpha=0.5,
        color="k",
        zorder=10000,
        label="Uncertainty envelope",
    )
    axr.axhline(0.0, linestyle="--", color="k")
    axr.set_ylabel("Samples - Data [DN/s]")
    for res in res_samples:
        axr.plot(x_img, res.ravel(), ".", color="C0", alpha=0.1)
    axr.set_xlabel("Pixel")
    fig.legend()
    return fig, axs
