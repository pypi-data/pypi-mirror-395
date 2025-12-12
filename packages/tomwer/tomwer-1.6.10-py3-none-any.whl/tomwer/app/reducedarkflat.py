#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to compute reduced darks and flats for a given scan"""

import argparse
import logging
import signal
import sys

from silx.gui import qt

from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefsTask
from tomwer.core.process.reconstruction.darkref.params import DKRFRP, ReduceMethod
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.gui.reconstruction.darkref.darkrefwidget import DarkRefWidget
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.synctools.darkref import QDKRFRP

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


def getinputinfo():
    return "tomwer darkref [scanDir]"


def _exec_without_interaction(scan, dark_method, flat_method, overwrite):
    recons_params = DKRFRP()
    recons_params.overwrite_dark = overwrite
    recons_params.overwrite_ref = overwrite
    recons_params.dark_calc_method = dark_method
    recons_params.flat_calc_method = flat_method
    dark_ref = DarkRefsTask(
        inputs={
            "data": scan,
            "dark_ref_params": recons_params,
            "serialize_output_data": False,
        }
    )
    _logger.info(f"Start processing of {scan}")
    dark_ref.run()
    _logger.info(f"End processing of {scan}")
    return 0


def _exec_with_interaction(scan, dark_method, flat_method, overwrite):
    class ProcessingThread(qt.QThread):
        """
        Thread used to run the processing
        """

        def __init__(self, inputs: dict) -> None:
            super().__init__()
            self._inputs = inputs

        def run(self):
            process = DarkRefsTask(inputs=self._inputs)
            process.run()

    class _DarkRefWidgetRunnable(DarkRefWidget):
        sigScanReady = qt.Signal(str)
        """emit when scan ready"""

        def __init__(self, scan, parent=None):
            self.__scan = scan
            self.__darkref_rp = QDKRFRP()
            DarkRefWidget.__init__(self, parent=parent, reconsparams=self.__darkref_rp)
            buttonExec = qt.QPushButton("execute", parent=self)
            buttonExec.setAutoDefault(True)
            # needed to be used as an application to return end only when the
            # processing thread is needed
            self._forceSync = True
            self.layout().addWidget(buttonExec)
            buttonExec.pressed.connect(self._process)
            self.setWindowIcon(icons.getQIcon("tomwer"))
            self._processingThread = None

        def _notifyEnd(self, *args, **kwargs):
            self._processingThread.finished.disconnect(self._notifyEnd)
            print(f"computation of {self.__scan} reduced dark and flat done.")
            self._processingThread = None

        def _process(self):
            if self._processingThread is not None:
                print("processing already on-going...")
            else:
                self._processingThread = ProcessingThread(
                    inputs={
                        "data": self.__scan,
                        "dark_ref_params": self.__darkref_rp,
                        "force_sync": self._forceSync,
                    }
                )
                self._processingThread.finished.connect(self._notifyEnd)
                print(f"start reducing dark and flat of {self.__scan} ...")
                self._processingThread.start()

    def sigintHandler(*args):
        """Handler for the SIGINT signal."""
        qt.QApplication.quit()

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

    widget = _DarkRefWidgetRunnable(scan)
    # set up
    widget.recons_params.overwrite_dark = overwrite
    widget.recons_params.overwrite_flat = overwrite
    widget.recons_params.dark_calc_method = dark_method
    widget.recons_params.flat_calc_method = flat_method
    splash.finish(widget)
    widget.show()
    return app.exec()


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_path", help="Data file to show (h5 file, edf files, spec files)"
    )
    parser.add_argument(
        "--entry",
        help="an entry can be specify in case of hdf5 the master file",
        default=None,
    )
    parser.add_argument(
        "--dark-method",
        help="Define the method to be used for computing dark",
        default=ReduceMethod.MEAN,
    )
    parser.add_argument(
        "--flat-method",
        help="Define the method to be used for computing flat",
        default=ReduceMethod.MEDIAN,
    )
    parser.add_argument(
        "--no-gui",
        help="Will run directly the dark and ref without any interaction",
        dest="run",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        default=False,
        help="Overwrite dark/flats if exists",
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

    increase_max_number_file()

    scan = ScanFactory.create_scan_object(options.scan_path, entry=options.entry)

    dark_method = ReduceMethod(options.dark_method)
    flat_method = ReduceMethod(options.flat_method)

    if options.run:
        exit(
            _exec_without_interaction(
                scan=scan,
                dark_method=dark_method,
                flat_method=flat_method,
                overwrite=options.overwrite,
            )
        )
    else:
        exit(
            _exec_with_interaction(
                scan=scan,
                dark_method=dark_method,
                flat_method=flat_method,
                overwrite=options.overwrite,
            )
        )


if __name__ == "__main__":
    main(sys.argv)
