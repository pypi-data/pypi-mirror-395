#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to reconstruct a slice with Paganin for a set of delta/beta values."""

from __future__ import annotations

import argparse
import logging
import signal
import sys
import time

import silx
from silx.gui import qt

from tomwer.core.process.reconstruction.axis.axis import AxisTask, NoAxisUrl
from tomwer.core.process.reconstruction.darkref.darkrefs import (
    requires_reduced_dark_and_flat,
)
from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
    SADeltaBetaTask,
)
from tomwer.core.process.reconstruction.utils.cor import (
    relative_pos_to_absolute,
    absolute_pos_to_relative,
)
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.gui.reconstruction.saaxis.saaxis import NabuAutoCorDiag
from tomwer.gui.reconstruction.sadeltabeta.saadeltabeta import (
    SADeltaBetaWindow as _SADeltaBetaWindow,
)
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.synctools.axis import QAxisRP
from tomwer.synctools.sadeltabeta import QSADeltaBetaParams

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


class SADeltaBetaThread(qt.QThread):
    """
    Thread to call nabu and reconstruct one slice with several cor value
    """

    def init(self, data, configuration, dump_roi):
        self.scan = data
        self._configuration = configuration
        self._dump_roi = dump_roi

    def run(self) -> None:
        process = SADeltaBetaTask(
            process_id=None,
            inputs={
                "scan": self.scan,
                "serialize_output_data": False,
            },
        )
        process.set_configuration(self._configuration)
        process.dump_roi = self._dump_roi
        t0 = time.time()
        process.run()
        print(f"execution time is {time.time() - t0}")


class SADeltaBetaWindow(_SADeltaBetaWindow):
    def __init__(self, parent=None, dump_roi=False, backend=None):
        self._scan = None
        super().__init__(parent, backend=backend)
        self._insert_cor_gui()
        # thread for computing cors
        self._processingThread = SADeltaBetaThread()
        self._processingThread.finished.connect(self._threadedProcessEnded)
        # thread to compute the COR
        self._dump_roi = dump_roi

        # hide the validate button
        self._sadbControl._applyBut.hide()
        self.hideAutoFocusButton()

    def _insert_cor_gui(self):
        self._imageWidth = None
        self._automaticCorWidget = None
        self._qaxis_rp = QAxisRP()
        # dialog used to compute automatically the cor

        widget = self._tabWidget._deltaBetaSelectionWidget
        self._corGB = qt.QGroupBox(self)
        self._corGB.setTitle("center of rotation")
        self._corGB.setLayout(qt.QFormLayout())
        # auto cor calculation
        self._autoPB = qt.QPushButton("auto", self)
        self._corGB.layout().addRow(self._autoPB)

        # relative position
        self._relativeCORValueQLE = qt.QDoubleSpinBox(self)
        self._relativeCORValueQLE.setRange(-99999999, 99999999)
        self._corGB.layout().addRow("cor relative position", self._relativeCORValueQLE)
        # absolute position
        self._absoluteCORValueQLE = qt.QDoubleSpinBox(self)
        self._corGB.layout().addRow("cor absolute position", self._absoluteCORValueQLE)
        self._absoluteCORValueQLE.setRange(0, 99999999)
        widget.layout().insertWidget(2, self._corGB)

        # connect signal / slot
        self._relativeCORValueQLE.editingFinished.connect(self._relativeValueEdited)
        self._absoluteCORValueQLE.editingFinished.connect(self._absolueValueEdited)
        self._autoPB.pressed.connect(self._autoCorRequested)

    def _autoCorRequested(self):
        window = self.getAutomaticCorWindow()
        window.activateWindow()
        window.raise_()
        window.show()

    def getAutomaticCorWindow(self):
        if self._automaticCorWidget is None:
            self._automaticCorWidget = NabuAutoCorDiag(self, qarixrp=self._qaxis_rp)
            self._automaticCorWidget.setWindowTitle(
                "compute estimated center of rotation"
            )
            auto_cor_icon = icons.getQIcon("a")
            self._automaticCorWidget.setWindowIcon(auto_cor_icon)
            self._automaticCorWidget.sigRequestAutoCor.connect(
                self._computeEstimatedCor
            )
        return self._automaticCorWidget

    def setScan(self, scan):
        self._imageWidth = scan.dim_1
        # force update of the cor value
        self._relativeCORValueQLE.editingFinished.emit()
        super().setScan(scan=scan)

    def _relativeValueEdited(self):
        old = self._absoluteCORValueQLE.blockSignals(True)
        value = relative_pos_to_absolute(
            relative_pos=self._relativeCORValueQLE.value(), det_width=self._imageWidth
        )
        self._absoluteCORValueQLE.setValue(value)
        self._absoluteCORValueQLE.blockSignals(old)

    def _absoluteValueEdited(self):
        old = self._relativeCORValueQLE.blockSignals(True)
        value = absolute_pos_to_relative(
            absolute_pos=self._absoluteCORValueQLE.value(), det_width=self._imageWidth
        )
        self._relativeCORValueQLE.setValue(value)
        self._relativeCORValueQLE.blockSignals(old)

    def setRelativeCorPosition(self, value):
        self._relativeCORValueQLE.setValue(value)
        self._relativeCORValueQLE.editingFinished.emit()

    def getAbsoluteCorPosition(self):
        return self._absoluteCORValueQLE.value()

    def _launchReconstructions(self):
        if self._processingThread.isRunning():
            _logger.error(
                "a calculation is already launch. You must wait for "
                "it to end prior to launch a new one"
            )
        else:
            qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
            self._processingThread.init(
                configuration=self.getConfiguration(),
                data=self.getScan(),
                dump_roi=self._dump_roi,
            )
            self._processingThread.start()

    def getConfiguration(self) -> dict:
        config = super().getConfiguration()
        # insert rotation_axis_position
        if "reconstruction" not in config["nabu_params"]:
            config["nabu_params"]["reconstruction"] = {}
        config["nabu_params"]["reconstruction"][
            "rotation_axis_position"
        ] = self.getAbsoluteCorPosition()
        return config

    def _threadedProcessEnded(self):
        sa_delta_beta_params = self._processingThread.scan.sa_delta_beta_params
        if sa_delta_beta_params is None:
            scores = None
        else:
            scores = sa_delta_beta_params.scores
        scan = self.getScan()
        assert scan is not None, "scan should have been set"
        self.setDBScores(
            scores, img_width=scan.dim_1, score_method=self.getScoreMethod()
        )
        if scan.sa_delta_beta_params.autofocus is not None:
            self.setCurrentDeltaBetaValue(scan.sa_delta_beta_params.autofocus)
        qt.QApplication.restoreOverrideCursor()
        self.showResults()

    def _stopProcessingThread(self):
        if self._processingThread:
            self._processingThread.terminate()
            self._processingThread.wait(500)
            self._processingThread = None

    def stop(self):
        self._stopProcessingThread()

    def _computeEstimatedCor(self) -> float | None:
        scan = self.getScan()
        if scan is None:
            return
        _cor_estimation_process = AxisTask(
            inputs={
                "data": scan,
                "axis_params": self._qaxis_rp,
                "serialize_output_data": False,
            }
        )

        _logger.info(f"{scan} - start cor estimation for")
        qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
        try:
            _cor_estimation_process.compute(scan=scan, wait=True)
        except NoAxisUrl:
            qt.QApplication.restoreOverrideCursor()
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Warning)
            text = (
                "Unable to find url to compute the axis, please select them "
                "from the `axis input` tab"
            )
            msg.setText(text)
            msg.exec()
            return None
        else:
            self.setRelativeCorPosition(
                value=scan.axis_params.relative_cor_value,
            )
            qt.QApplication.restoreOverrideCursor()
            self.getAutomaticCorWindow().hide()
            return scan.axis_params.relative_cor_value


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_path",
        help="For EDF acquisition: provide folder path, for HDF5 / nexus "
        "provide the master file",
        default=None,
    )
    parser.add_argument(
        "--entry",
        help="For Nexus files: entry in the master file",
        default=None,
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )
    parser.add_argument(
        "--read-existing",
        dest="read_existing",
        action="store_true",
        default=False,
        help="Load latest sa-delta-beta processing from *_tomwer_processes.h5 "
        "if exists",
    )
    parser.add_argument(
        "--dump-roi",
        dest="dump_roi",
        action="store_true",
        default=False,
        help="Save roi where the score is computed on the .hdf5",
    )
    parser.add_argument(
        "--use-opengl-plot",
        "--opengl-backend",
        help="Use OpenGL for plots (instead of matplotlib)",
        action="store_true",
        default=False,
    )
    options = parser.parse_args(argv[1:])

    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    if options.use_opengl_plot:
        silx.config.DEFAULT_PLOT_BACKEND = "gl"
    else:
        silx.config.DEFAULT_PLOT_BACKEND = "matplotlib"

    increase_max_number_file()
    scan = ScanFactory.create_scan_object(
        scan_path=options.scan_path, entry=options.entry
    )
    requires_reduced_dark_and_flat(scan=scan, logger_=_logger)

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication([])
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

    window = SADeltaBetaWindow(dump_roi=options.dump_roi)
    window.setWindowTitle("sa-delta-beta")
    window.setWindowIcon(icons.getQIcon("tomwer"))
    if not hasattr(scan, "sa_delta_beta_params") or scan.sa_delta_beta_params is None:
        scan.sa_delta_beta_params = QSADeltaBetaParams()
    window.setScan(scan)
    if options.read_existing is True:
        scores, selected = SADeltaBetaTask.load_results_from_disk(scan)
        if scores is not None:
            window.setDBScores(scores, score_method="standard deviation")
            if selected not in (None, "-"):
                window.setCurrentDeltaBetaValue(selected)

    splash.finish(window)
    window.show()
    qt.QApplication.restoreOverrideCursor()
    app.aboutToQuit.connect(window.stop)
    app.exec()


def getinputinfo():
    return "tomwer saaxis [scanDir]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    main(sys.argv)
