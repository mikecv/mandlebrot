"""
Low resolution Mandlebrot set images program.
"""

import logging
from typing import Any

import dotsi  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

# Ignore numpy warnings from overflow in iterations.
# Needed as not checking for diverging point to speed things up.
# Test without ignoring errors then comment out.
np.seterr(all="ignore")

from mandlebrot import app_settings
from mandlebrot.app_logging import setup_logging

log = logging.getLogger(__name__)


class LowResMandlebrot:
    """
    Main Class the low res Mandlebrot set images application.
    """

    def __init__(self):
        """
        Low resolution Mandlebrot set images initialisation.
        """

        # Load application settings.
        self._settings = dotsi.Dict(app_settings.load("./mandlebrot/settings.yaml"))

        # Initialise app name and version from settings.
        self._app_name = self._settings.app.APP_NAME
        self._app_version = self._settings.app.APP_VERSION

        # Setup the application logger.
        setup_logging(self._app_name)

        log.info(f"Starting application: {self._app_name}, version: {self._app_version}")

        # Generate complex array of numbers (pixels in image).
        c_pts = complex_matrix(
            self._settings.lres.DEF_XMIN,
            self._settings.lres.DEF_XMAX,
            self._settings.lres.DEF_YMIN,
            self._settings.lres.DEF_YMAX,
            self._settings.lres.DEF_PIXELS,
        )
        # Determine pixels in the Mandlebrot set (not divergent).
        members = get_members(c_pts, self._settings.lres.DEF_ITERATIONS)

        # Do simple Mandlebrot scatter plot.
        plt.scatter(members.real, members.imag, color="black", marker=",", s=1)
        plt.gca().set_aspect("equal")
        plt.axis("off")
        plt.tight_layout()
        plt.show()


def complex_matrix(xmin: float, xmax: float, ymin: float, ymax: float, pixel_density: int) -> np.ndarray:
    """
    Constructs complex array of points for image.

    Args:
        xmin:           minimum x value (real)
        xmax:           maximum x value (real)
        ymin:           minimum y value (imaginary)
        ymax:           maximum y value (imaginary)
        pixel_density:  Number of pixels (points) in x and y ranges.

    Returns:
        Array of complex points making up image space.
    """
    # Construct real and imaginary arrays.
    re_part = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im_part = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))

    # Construct and return arracy of complex points for image.
    return re_part[np.newaxis, :] + im_part[:, np.newaxis] * 1j


def get_members(c_pts: np.ndarray, num_iterations: int) -> np.ndarray:
    """
    Returns complex points that are stable, that is,
    don't diverge at maximum iterations.
    Args:
        c_pts:          Array of complex points in image.
        num_iterations: Number of iterations to check for divergence
    Retutns:
        Returns array of complex points that are stable.
    """
    mask = is_stable(c_pts, num_iterations)  # type: ignore[arg-type]
    return c_pts[mask]


def is_stable(c_pt: int, num_iterations: int) -> bool:
    """
    Checks if point is stable, i.e. reaches iteration limit
    without diverging.
    Args:
        c_pt:           Complex point (component) in image to test.
        num_iterations: Number of iterations to check for divergence.
    Returns:
        Returns true if not diverging at max iterations.
    """
    z_pt = 0
    for _ in range(num_iterations):
        z_pt = z_pt**2 + c_pt
    return abs(z_pt) <= 2


def run() -> None:
    """
    Poetry calls this to get the application up and running.
    Assumes a python script as follows:

    [tool.poetry.scripts]
    low-res-go = "mandlebrot.low_res_app:run"
    """

    LowResMandlebrot()


if __name__ == "__main__":
    run()
