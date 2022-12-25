"""
Low resolution Mandlebrot set images program.
"""

import logging

import dotsi  # type: ignore

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
