from silx.gui import qt

from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.tests.conftest import qtapp  # noqa F401


def test_get_splash_screen(qtapp):  # noqa F401
    assert isinstance(getMainSplashScreen(), qt.QSplashScreen)
