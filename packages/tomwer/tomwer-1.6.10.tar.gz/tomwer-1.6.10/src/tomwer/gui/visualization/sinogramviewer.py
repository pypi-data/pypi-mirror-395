# coding: utf-8
"""
contains gui relative to axis calculation using sinogram
"""
from __future__ import annotations


import logging
import weakref

from silx.gui import qt
from silx.gui.plot import Plot2D
from silx.gui.widgets.WaitingOverlay import WaitingOverlay
from tomwer.gui.settings import Y_AXIS_DOWNWARD

_logger = logging.getLogger(__name__)


class SinogramViewer(qt.QMainWindow):
    """
    Widget to display a sinogram
    """

    sigSinoLoadStarted = qt.Signal()
    """Signal emitted when some computation is started. For this widget
    some computation can be time consuming when creating the sinogram"""
    sigSinoLoadEnded = qt.Signal()
    """Signal emitted when a computation is ended"""

    def __init__(
        self,
        parent=None,
        scan=None,
        opts_orientation=qt.Qt.Vertical,
        backend=None,
    ):
        qt.QMainWindow.__init__(self, parent)
        self._scan = None
        self._sinoInfoCache = None
        # used to memorize sinogram properties when load it.
        # Contains (str(scan), line, oversampling)

        self._plot = Plot2D(parent=self)
        self._plotWaiter = WaitingOverlay(self._plot)
        self._plotWaiter.hide()
        self._plotWaiter.setIconSize(qt.QSize(30, 30))

        self._plot.getMaskAction().setVisible(False)
        self._plot.setYAxisInverted(Y_AXIS_DOWNWARD)
        self._plot.getDefaultColormap().setVRange(None, None)
        self._plot.setAxesDisplayed(False)
        self._plot.setKeepDataAspectRatio(True)
        self._dockOpt = qt.QDockWidget(self)
        self._options = SinogramOpts(parent=self, orientation=opts_orientation)
        self._dockOpt.setWidget(self._options)

        self.setCentralWidget(self._plot)
        self._dockOpt.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._dockOpt)

        # prepare processing
        self._loadingThread = _LoadSinoThread()

        # connect signal / slot
        self._options.sigUpdateRequested.connect(self.updateSinogram)
        self._loadingThread.finished.connect(self._sinogram_loaded)

        # expose API
        self.getActiveImage = self._plot.getActiveImage

        # set up
        if scan is not None:
            self.setScan(scan=scan)

    def getOptionsDockWidget(self):
        return self._dockOpt

    def setReconsParams(self, axis):
        self._axis_params = axis
        # TODO: update according to axis paramters

    def setScan(self, scan, update=True):
        if self._scan is None or self._scan() != scan:
            self._scan = weakref.ref(scan)
            self._options.setScan(scan)
            if update:
                self.updateSinogram()
            else:
                self.clear()

    def setLine(self, line: int):
        """

        :param line: define the line we want to compute
        """
        self._options.setRadioLine(line)

    def getLine(self):
        return self._options.getRadioLine()

    def setSubsampling(self, value):
        self._options.setSubsampling(value)

    def _updatePlot(self, sinogram):
        self._plot.addImage(data=sinogram)
        self._plot.replot()

    def _sinogram_loaded(self):
        """callback when the sinogram is loaded"""
        self._plotWaiter.hide()
        if self._scan is None or self._scan() is None:
            return
        assert self._sinoInfoCache is not None

        scan_id, line, subsampling = self._sinoInfoCache
        # if the scan changed since the load started, skip this update
        if scan_id != str(self._scan()):
            return

        # note: cache avoid reading data twice here.
        sinogram = self._scan().get_normed_sinogram(line=line, subsampling=subsampling)
        self._updatePlot(sinogram=sinogram)
        self.sigSinoLoadEnded.emit()
        self._options.setEnabled(True)

    def updateSinogram(self):
        if self._scan is None or self._scan() is None:
            return
        if self._loadingThread.isRunning():
            _logger.warning(
                "a sinogram is already beeing computing, please wait until it" " ends"
            )
            return
        # update scan
        self._plotWaiter.show()
        self.sigSinoLoadStarted.emit()
        self._sinoInfoCache = (
            str(self._scan()),
            self._options.getRadioLine(),
            self._options.getSubsampling(),
        )
        self._loadingThread.init(
            data=self._scan(),
            line=self._options.getRadioLine(),
            subsampling=int(self._options.getSubsampling()),
        )
        self._loadingThread.start()

    def clear(self):
        self._plot.clear()

    def close(self):
        self._plotWaiter.hide()
        self._plot.close()
        self._plot = None
        super().close()


class _LoadSinoThread(qt.QThread):
    def init(self, data, line, subsampling):
        self._scan = data
        self._line = line
        self._subsampling = subsampling

    def run(self):
        try:
            self._scan.get_normed_sinogram(
                line=self._line, subsampling=self._subsampling
            )
        except ValueError as e:
            _logger.error(e)


class SinogramOpts(qt.QDialog):
    """
    Define the options to compute and display the sinogram
    """

    sigUpdateRequested = qt.Signal()
    """signal emitted when an update of the sinogram (with different
    parameters) is requested"""

    def __init__(self, parent, orientation=qt.Qt.Vertical):
        qt.QDialog.__init__(self, parent)
        if orientation is qt.Qt.Vertical:
            self.setLayout(qt.QVBoxLayout())
        elif orientation is qt.Qt.Horizontal:
            self.setLayout(qt.QHBoxLayout())
        else:
            raise TypeError(
                "orientation should be either qt.Qt.Vertical or " "qt.Qt.Horizontal"
            )
        self._scan = None

        # add line
        self._lineSelWidget = qt.QWidget(parent=self)
        self._lineSelWidget.setLayout(qt.QHBoxLayout())
        self._lineSelWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._lineSB = qt.QSpinBox(parent=self)
        self._lineSB.setMaximum(999999)
        self._lineSelWidget.layout().addWidget(qt.QLabel("radio line", self))
        self._lineSelWidget.layout().addWidget(self._lineSB)
        self.layout().addWidget(self._lineSelWidget)

        # add subsampling option
        self._subsamplingWidget = qt.QWidget(parent=self)
        self._subsamplingWidget.setLayout(qt.QHBoxLayout())
        self._subsamplingWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._subsamplingSB = qt.QSpinBox(parent=self)
        self._subsamplingSB.setMinimum(1)
        self._subsamplingSB.setValue(4)
        self._subsamplingSB.setMaximum(100)
        self._subsamplingLabel = qt.QLabel("subsampling", self)
        self._subsamplingWidget.layout().addWidget(self._subsamplingLabel)
        self._subsamplingWidget.setToolTip(
            "if you like you can only take a "
            "subsample of the sinogram to "
            "speed up process"
        )
        self._subsamplingWidget.layout().addWidget(self._subsamplingSB)
        self.layout().addWidget(self._subsamplingWidget)

        # add spacer
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        types = qt.QDialogButtonBox.Apply
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)

        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Apply).clicked.connect(
            self.sigUpdateRequested
        )

    def setLineSelectionVisible(self, visible):
        self._lineSelWidget.setVisible(visible)

    def setScan(self, scan):
        old = self.blockSignals(True)
        # update line max and value
        n_line = scan.dim_2
        if n_line is None:
            n_line = 0
        self._lineSB.setMaximum(n_line)
        self.blockSignals(old)

    def getRadioLine(self):
        return self._lineSB.value()

    def setRadioLine(self, line):
        self._lineSB.setValue(line)

    def getSubsampling(self):
        return self._subsamplingSB.value()

    def setSubsampling(self, value):
        self._subsamplingSB.setValue(value)
