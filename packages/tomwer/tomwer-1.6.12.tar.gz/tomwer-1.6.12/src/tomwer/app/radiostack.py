#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to display scan radios as a stack"""
import argparse
import logging
import os
import signal
import sys

import silx
from silx.gui import qt

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.gui.stacks import RadioStack
from tomwer.gui.utils.splashscreen import getMainSplashScreen

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


def getinputinfo():
    return "tomwer radio-stack [scanName]"


def addFolderAndSubFolder(stack, path):
    stack.addLeafScan(path)
    for f in os.listdir(path):
        _path = os.path.join(path, f)
        if os.path.isdir(_path) is True:
            addFolderAndSubFolder(stack, _path)
        elif os.path.isfile(_path) and NXtomoScan.is_nexus_nxtomo_file(_path):
            stack.addLeafScan(_path)


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root_dir", help="Root dir to browse and to extract all radio under it."
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

    increase_max_number_file()

    options = parser.parse_args(argv[1:])

    if options.use_opengl_plot:
        silx.config.DEFAULT_PLOT_BACKEND = "gl"
    else:
        silx.config.DEFAULT_PLOT_BACKEND = "matplotlib"

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication(["tomwer"])

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # cached
    timer.timeout.connect(lambda: None)

    splash = getMainSplashScreen()
    widget = RadioStack()
    widget.setWindowIcon(icons.getQIcon("tomwer"))
    options.root_dir = options.root_dir.rstrip(os.path.sep)
    addFolderAndSubFolder(stack=widget, path=options.root_dir)

    splash.finish(widget)
    widget.show()
    app.exec()


if __name__ == "__main__":
    main(sys.argv)
