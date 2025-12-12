#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to edit (group by group) the 'imagekey' value of a NXtomo ('imagekey' defines if a frame is a 'dark', 'flat' or a 'projection')"""

import argparse
import logging
import signal
import sys

from silx.gui import qt

from tomwer.core.process.edit.imagekeyeditor import ImageKeyUpgraderTask
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.gui.edit.imagekeyeditor import (
    ImageKeyUpgraderWidget as _ImageKeyUpgraderWidget,
)
from tomwer.gui.utils.splashscreen import getMainSplashScreen

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


class ImageKeyUpgraderDialog(qt.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scan = None

        self.setLayout(qt.QVBoxLayout())
        self._widget = _ImageKeyUpgraderWidget(self)
        self.layout().addWidget(self._widget)

        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        # signal / slot connection
        self._buttons.button(qt.QDialogButtonBox.Ok).released.connect(self.validate)
        self._buttons.button(qt.QDialogButtonBox.Cancel).released.connect(self.close)

    def setScan(self, scan):
        if not isinstance(scan, NXtomoScan):
            raise TypeError("This only manage NXtomoScan")
        self._scan = scan

    def validate(self):
        operations = self._widget.getOperations()
        task = ImageKeyUpgraderTask(
            inputs={
                "data": self._scan,
                "operations": operations,
            },
        )
        task.run()
        print("edition finished")
        self.close()


def getinputinfo():
    return "tomwer image-key-upgrader [scan_path] [entry]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    import os

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan_path", help="NXtomo to edit")
    parser.add_argument("entry", default=None, help="Entry to treat")
    options = parser.parse_args(argv[1:])

    # image key can only handle NXtomoScan for now
    scan = NXtomoScan(scan=options.scan_path, entry=options.entry)
    increase_max_number_file()

    app = qt.QApplication.instance() or qt.QApplication(["tomwer"])

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    splash = getMainSplashScreen()
    options.scan_path = options.scan_path.rstrip(os.path.sep)

    widget = ImageKeyUpgraderDialog(parent=None)
    widget.setWindowFlags(qt.Qt.Window)

    widget.setScan(scan)
    widget.setWindowTitle("Image key upgrader")
    widget.setWindowIcon(icons.getQIcon("tomwer"))
    splash.finish(widget)
    widget.show()
    app.exec()


if __name__ == "__main__":
    main(sys.argv)
