"""
Unit test for application name checker.
This is an inital unit test to check build scripts.
"""

import dotsi  # type: ignore

from mandlebrot.app_settings import load as load_aerrings

def test_app_name():

    # Load application settings.
    _settings = dotsi.Dict(load_aerrings("./mandlebrot/settings.yaml"))

    # Simple test to check app name is 'right'.
    assert _settings.app.APP_NAME == "mandlebrot"
