#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import sys

from silx.gui import qt

from tomwer.core.process.reconstruction.normalization import SinoNormalizationTask
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.gui import icons
from tomwer.gui.reconstruction.normalization.intensity import (
    SinoNormWindow as _SinoNormWindow,
)
from tomwer.gui.utils.splashscreen import getMainSplashScreen

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


class IntensityNormalizationThread(qt.QThread):
    """
    Thread to call the normalization process when needed (to avoid gui freeze)
    """

    def __init__(self, *args, **kwargs):
        qt.QThread.__init__(self, *args, **kwargs)
        self._result = None

    @property
    def result(self):
        return self._result

    def init(self, data, configuration):
        if not isinstance(configuration, dict):
            raise TypeError("Configuration is expected to be a dict")
        if not isinstance(data, TomwerScanBase):
            raise TypeError("Scan is expected to be an instance of " "TomwerScanBase")
        self.scan = data
        self._configuration = configuration
        self._result = None

    def run(self) -> None:
        process = SinoNormalizationTask(
            process_id=None,
            inputs={
                "data": self.scan,
                "configuration": self._configuration,
                "serialize_output_data": False,
            },
            varinfo=None,
        )
        process.run()
        self._result = self.scan.intensity_normalization.tomwer_processing_res


class NormIntensityWindow(_SinoNormWindow):
    def __init__(self, parent=None):
        _SinoNormWindow.__init__(self, parent)
        self._processingThread = IntensityNormalizationThread()
        self._hideLockButton()

        # connect signal / slot
        self._optsWidget.sigProcessingRequested.connect(self._launchProcessing)
        self._processingThread.finished.connect(self._threadedProcessEnded)

    def _validated(self):
        self.close()

    def _launchProcessing(self):
        self.clear()
        if self._processingThread.isRunning():
            _logger.error(
                "a calculation is already launch. You must wait for "
                "it to end prior to launch a new one"
            )
        else:
            qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
            self._processingThread.init(
                data=self.getScan(),
                configuration=self.getConfiguration(),
            )
            self._processingThread.start()

    def _threadedProcessEnded(self):
        qt.QApplication.restoreOverrideCursor()

    def close(self) -> None:
        self._stopProcessingThread()
        super().close()

    def _stopProcessingThread(self):
        if self._processingThread:
            self._processingThread.terminate()
            self._processingThread.wait(500)
            self._processingThread = None

    def stop(self):
        self._stopProcessingThread()
        super().stop()


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_path",
        help="For EDF acquisition: provide folder path, for HDF5 / nexus"
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

    if options.scan_path is not None:
        if os.path.isdir(options.scan_path):
            options.scan_path = options.scan_path.rstrip(os.path.sep)
            scan = ScanFactory.create_scan_object(scan_path=options.scan_path)
        else:
            if not os.path.isfile(options.scan_path):
                raise ValueError(
                    "scan path should be a folder containing an"
                    " EDF acquisition or an hdf5 - nexus "
                    "compliant file"
                )
            if options.entry is None:
                raise ValueError("entry in the master file should be specify")
            scan = NXtomoScan(scan=options.scan_path, entry=options.entry)
    else:
        scan = ScanFactory.mock_scan()
    # define the process_index is any tomwer_processes_existing
    if options.debug:
        _logger.setLevel(logging.DEBUG)

    window = NormIntensityWindow(parent=None)

    window.setWindowTitle("sinogram-norm-intensity")
    window.setWindowIcon(icons.getQIcon("tomwer"))
    window.setScan(scan)

    splash.finish(window)
    window.show()
    qt.QApplication.restoreOverrideCursor()
    app.aboutToQuit.connect(window.stop)
    app.exec()


def getinputinfo():
    return "tomwer intensity normalization [scanDir entry]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    main(sys.argv)
