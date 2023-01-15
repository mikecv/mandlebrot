"""
High resolution Mandlebrot set images program.
"""

import logging

import dotsi  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

# Ignore numpy warnings from overflow in iterations.
# Needed as not checking for diverging point to speed things up.
# Test without ignoring errors then comment out.
np.seterr(all="ignore")

from mandlebrot import app_settings
from mandlebrot.app_logging import setup_logging
from mandlebrot.process_utils import complex_matrix, is_stable

log = logging.getLogger(__name__)


class HighResMandlebrot:
    """
    Main Class the high res Mandlebrot set images application.
    """

    def __init__(self):
        """
        High resolution Mandlebrot set images initialisation.
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
            self._settings.hres.DEF_XMIN,
            self._settings.hres.DEF_XMAX,
            self._settings.hres.DEF_YMIN,
            self._settings.hres.DEF_YMAX,
            self._settings.hres.DEF_PIXELS,
        )

        # Do image plot of stable (non-divergent) Mandlebrot points.
        # Plot using the Matplotlib colour map in settings.
        plt.imshow(is_stable(c_pts, num_iterations=self._settings.hres.DEF_ITERATIONS), cmap=self._settings.hres.COL_MAP)
        plt.gca().set_aspect("equal")
        plt.axis("off")
        plt.tight_layout()
        plt.show()


def run() -> None:
    """
    Poetry calls this to get the application up and running.
    Assumes a python script as follows:

    [tool.poetry.scripts]
    high-res-go = "mandlebrot.high_res_app:run"
    """

    HighResMandlebrot()


if __name__ == "__main__":
    run()
