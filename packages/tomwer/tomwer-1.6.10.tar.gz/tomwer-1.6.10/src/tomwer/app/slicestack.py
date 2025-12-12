#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to display findable reconstructed slice of a scan (as a stack).
reconstructed slices can be added by hand or as input(s) of the command line.
"""

import argparse
import logging
import signal
import sys
import os

import silx
from silx.gui import qt

from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.gui.stacks import SliceStack
from tomwer.gui.utils.splashscreen import getMainSplashScreen

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


def getinputinfo():
    return "tomwer slice-stack [scanDir]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "volume_paths",
        help="Volumes to be added to the slice stack visualization. Warning: volumes should be single slice volumes.",
        nargs="*",
    )
    parser.add_argument(
        "--use-opengl-plot",
        "--opengl-backend",
        help="Use OpenGL for plots (instead of matplotlib)",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )

    options = parser.parse_args(argv[1:])

    if options.use_opengl_plot:
        silx.config.DEFAULT_PLOT_BACKEND = "gl"
    else:
        silx.config.DEFAULT_PLOT_BACKEND = "matplotlib"

    increase_max_number_file()

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication(["tomwer"])

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catched
    timer.timeout.connect(lambda: None)

    splash = getMainSplashScreen()
    widget = SliceStack()
    widget.setWindowIcon(icons.getQIcon("tomwer"))
    widget._addTomoObjectsFromStrList(
        [os.path.abspath(volume_path) for volume_path in options.volume_paths]
    )

    splash.finish(widget)
    widget.show()
    app.exec()


if __name__ == "__main__":
    main(sys.argv)
