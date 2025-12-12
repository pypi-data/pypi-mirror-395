# coding: utf-8

try:
    from silx.gui import qt
except ImportError:
    raise ImportError("Can't found silx modules")
import tomwer.version
from tomwer.gui import icons


def getMainSplashScreen():
    pixmap = icons.getQPixmap("tomwer")
    splash = qt.QSplashScreen(pixmap)
    splash.show()
    splash.raise_()
    _version = tomwer.version.version
    text = "version " + str(_version)
    splash.showMessage(text, qt.Qt.AlignLeft | qt.Qt.AlignBottom, qt.Qt.white)
    return splash
