#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to edit several entries of a NXtomo"""

import argparse
import logging
import signal
import sys

from silx.gui import qt

from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.process.edit.nxtomoeditor import NXtomoEditorTask
from tomwer.gui.edit.nxtomoeditor import NXtomoEditorDialog as _NXtomoEditorDialog
from tomwer.gui.utils.splashscreen import getMainSplashScreen

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


class NXtomoEditorDialog(_NXtomoEditorDialog):
    def __init__(self) -> None:
        super().__init__()

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Ok).released.connect(self._triggerTask)

    def getScan(self):
        return self.mainWidget.getScan()

    def _triggerTask(self, *args, **kwargs):
        task = NXtomoEditorTask(
            inputs={
                "data": self.getScan(),
                "configuration": self.getConfigurationForTask(),
            }
        )
        task.run()
        print("edition finished")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan_path", help="nexus file (HDF5 file) to edit.")
    parser.add_argument(
        "entry",
        help="path to the file where starts the NXtomo. Usually named 'entry', or 'entryXXXX'",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )

    options = parser.parse_args(argv[1:])

    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication([])
    splash = getMainSplashScreen()
    qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    app.processEvents()

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler

    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    try:
        scan = ScanFactory.create_scan_object(
            scan_path=options.scan_path, entry=options.entry
        )
    except Exception as e:
        _logger.error(
            f"Fail to find a NXtomo from {options.scan_path} at {options.entry}. Error is {e}"
        )
        return

    dialog = NXtomoEditorDialog()
    dialog.setWindowFlags(qt.Qt.Window)

    dialog.setScan(scan)
    dialog.show()
    splash.finish(dialog)

    qt.QApplication.restoreOverrideCursor()
    app.exec()


def getinputinfo():
    return "tomwer nxtomo-editor [scanDir]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    main(sys.argv)
