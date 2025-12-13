#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to browse a given scan"""

import argparse
import logging
import signal
import sys

from silx.gui import qt

from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui.visualization.dataviewer import DataViewer

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_path",
        help="For EDF acquisition: provide folder path, for HDF5 / nexus "
        "provide the master file",
        default=None,
    )
    parser.add_argument(
        "entry",
        help="For Nexus files: entry in the master file",
        default=None,
        nargs="?",
    )
    parser.add_argument(
        "--use-opengl-plot",
        "--opengl-backend",
        help="Use OpenGL for plots (instead of matplotlib)",
        action="store_true",
        default=False,
    )

    options = parser.parse_args(argv[1:])

    scan = ScanFactory.create_scan_object(
        scan_path=options.scan_path, entry=options.entry
    )

    import silx

    if options.use_opengl_plot:
        silx.config.DEFAULT_PLOT_BACKEND = "gl"
    else:
        silx.config.DEFAULT_PLOT_BACKEND = "matplotlib"

    increase_max_number_file()

    global app  # QApplication must be global to avoid seg fault on quit

    app = qt.QApplication.instance() or qt.QApplication(["tomwer"])
    splash = getMainSplashScreen()
    qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    qt.QApplication.processEvents()

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler

    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    window = DataViewer(parent=None)
    window.setDisplayMode("projections-radios")
    window.setWindowTitle("tomwer: scan-viewer")
    window.setWindowIcon(icons.getQIcon("tomwer"))
    window.setScan(scan)
    splash.finish(window)
    window.show()

    qt.QApplication.restoreOverrideCursor()
    app.aboutToQuit.connect(window.close)
    exit(app.exec())


def getinputinfo():
    return "tomwer scan-viewer [file_path] [[file_entry]]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.closeAllWindows()  # needed because get a waiting thread behind
    qt.QApplication.quit()


if __name__ == "__main__":
    main(sys.argv)
