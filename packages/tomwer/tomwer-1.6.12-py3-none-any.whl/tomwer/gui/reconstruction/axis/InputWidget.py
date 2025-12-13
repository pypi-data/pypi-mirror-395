from __future__ import annotations

import logging

from silx.gui import qt

from tomwer.core.process.reconstruction.axis import mode as axis_mode
from tomwer.core.process.reconstruction.axis.anglemode import CorAngleMode
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.synctools.axis import QAxisRP
from .ManualFramesSelection import ManualFramesSelection

_logger = logging.getLogger(__name__)


class InputWidget(qt.QWidget):
    """
    Widget used to define the radios or the sinogram to be used for computing the cor
    Used as a tab of the AxisSettingsTabWidget
    """

    sigChanged = qt.Signal()
    """Signal emitted when input changed"""

    _sigUrlChanged = qt.Signal()
    """Signal emit when url to be used changed"""

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        self._blockUpdateAxisParams = False
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        # radio input
        self._radioGB = qt.QGroupBox(self)
        self._radioGB.setTitle("radios")
        self._radioGB.setLayout(qt.QVBoxLayout())
        self._radioGB.setCheckable(True)
        self.layout().addWidget(self._radioGB)
        ## angle mode
        self._angleModeWidget = _AngleSelectionWidget(
            parent=self, axis_params=axis_params
        )
        self._radioGB.layout().addWidget(self._angleModeWidget)
        self._axis_params = axis_params

        # sinogram input
        self._sinogramGB = qt.QGroupBox(self)
        self._sinogramGB.setLayout(qt.QFormLayout())

        self._sinogramGB.setTitle("sinogram")
        self._sinogramGB.setCheckable(True)
        self.layout().addWidget(self._sinogramGB)
        ##  sinogram line
        self._sinogramLineSB = _SliceSelector(self)
        self._sinogramGB.layout().addRow("line", self._sinogramLineSB)
        ##  sinogram subsampling
        self._sinogramSubsampling = qt.QSpinBox(self)
        self._sinogramSubsampling.setRange(1, 1000)
        self._sinogramSubsampling.setValue(10)
        self._sinogramGB.layout().addRow("subsampling", self._sinogramSubsampling)

        self._spacer = qt.QWidget(self)
        self._spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self._spacer)

        # set up
        self._sinogramGB.setChecked(False)

        # connect signal / slot
        self._sinogramGB.toggled.connect(self._sinogramChecked)
        self._radioGB.toggled.connect(self._radiosChecked)
        self._sinogramSubsampling.valueChanged.connect(self._changed)
        self._sinogramLineSB.sigChanged.connect(self._changed)
        self._angleModeWidget.sigChanged.connect(self._sigUrlChanged)

    def setScan(self, scan: TomwerScanBase):
        if scan is not None:
            self._angleModeWidget.setScan(scan)
            self._angleModeWidget.setScanRange(scan.scan_range)

    def setAxisParams(self, axis_params):
        with block_signals(axis_params):
            with block_signals(self._axis_params):
                self._blockUpdateAxisParams = True

                if axis_params is not None:
                    assert isinstance(axis_params, QAxisRP)
                    with block_signals(self._sinogramGB):
                        self._sinogramChecked(
                            axis_params.mode.requires_sinogram_index(), on_load=True
                        )
                    self._sinogramLineSB.setSlice(axis_params.sinogram_line)
                    self._sinogramSubsampling.setValue(axis_params.sinogram_subsampling)
                self._angleModeWidget.setAxisParams(axis_params)
                self._axis_params = axis_params

        self._blockUpdateAxisParams = False

    def getSinogramLine(self) -> str | int:
        return self._sinogramLineSB.getSlice()

    def getSinogramSubsampling(self) -> int:
        return self._sinogramSubsampling.value()

    def _sinogramChecked(self, checked, on_load=False):
        with block_signals(self._radioGB):
            with block_signals(self._sinogramGB):
                if checked:
                    self._radioGB.setChecked(False)
                    self._sinogramGB.setChecked(True)
                elif self._radioGB.isEnabled():
                    self._radioGB.setChecked(not checked)
                elif on_load:
                    self._sinogramGB.setChecked(checked)
                else:
                    # ignore it if radio disabled
                    self._sinogramGB.setChecked(True)
        self._changed()

    def _radiosChecked(self, checked, on_load=False):
        with block_signals(self._radioGB):
            with block_signals(self._sinogramGB):
                if checked:
                    self._sinogramGB.setChecked(False)
                    self._radioGB.setChecked(True)
                elif self._sinogramGB.isEnabled():
                    self._sinogramGB.setChecked(not checked)
                elif on_load:
                    self._radioGB.setChecked(checked)
                else:
                    # ignore it if sinogram disabled
                    self._radioGB.setChecked(True)
        self._changed()

    def _changed(self, *args, **kwargs):
        self._updateAxisParams()
        self.sigChanged.emit()

    def _updateAxisParams(self):
        if not self._blockUpdateAxisParams:
            self._axis_params.sinogram_line = self.getSinogramLine()
            self._axis_params.sinogram_subsampling = self.getSinogramSubsampling()

    def setValidInputs(self, modes: list | tuple):
        """
        Define possible inputs.

        :raises: ValueError if modes are invalid
        """
        modes = set(modes)
        for mode in modes:
            try:
                axis_mode._InputType(mode)
            except ValueError:
                raise ValueError(
                    f"mode {mode} should be an instance of {axis_mode._InputType}"
                )
        if len(modes) == 2:
            self._sinogramGB.setEnabled(True)
            self._radioGB.setEnabled(True)
        elif len(modes) > 2:
            raise ValueError(f"invalid input {modes}")
        elif len(modes) < 0:
            raise ValueError("modes is empty")
        else:
            mode = axis_mode._InputType(modes.pop())
            if mode is axis_mode._InputType.SINOGRAM:
                self._sinogramGB.setEnabled(True)
                self._radioGB.setEnabled(False)
                self._sinogramGB.setChecked(True)
            elif mode is axis_mode._InputType.RADIOS_X2:
                self._radioGB.setEnabled(True)
                self._sinogramGB.setEnabled(False)
                self._radioGB.setChecked(True)
            elif mode is axis_mode._InputType.COMPOSITE:
                # those mode are neither sinogram neither radio. Now one of the two will be checked but without any much meaning
                self._radioGB.setEnabled(False)
                self._sinogramGB.setEnabled(False)
            else:
                raise ValueError(f"Nothing implemented for {mode.value}")


class _AngleSelectionWidget(qt.QWidget):
    """Group box to select the angle to used for cor calculation
    (0-180, 90-270 or manual)"""

    sigChanged = qt.Signal()
    """signal emitted when the selected angle changed"""

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(
            self,
            parent=parent,
        )
        self.setLayout(qt.QVBoxLayout())
        self._groupBoxMode = qt.QGroupBox(
            self, title="Angles to use for axis calculation"
        )
        self._groupBoxMode.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._groupBoxMode)

        self._corButtonsGps = qt.QButtonGroup(parent=self)
        self._corButtonsGps.setExclusive(True)
        self._qrbCOR_0_180 = qt.QRadioButton("0-180", parent=self)
        self._groupBoxMode.layout().addWidget(self._qrbCOR_0_180)
        self._qrbCOR_90_270 = qt.QRadioButton("90-270", parent=self)
        self._qrbCOR_90_270.setToolTip(
            "pick radio closest to angles 90° and "
            "270°. If disable mean that the scan "
            "range is 180°"
        )
        self._groupBoxMode.layout().addWidget(self._qrbCOR_90_270)
        self._qrbCOR_manual = qt.QRadioButton("other", parent=self)
        self._qrbCOR_manual.setVisible(True)
        self._groupBoxMode.layout().addWidget(self._qrbCOR_manual)
        # add all button to the button group
        for b in (self._qrbCOR_0_180, self._qrbCOR_90_270, self._qrbCOR_manual):
            self._corButtonsGps.addButton(b)

        self.setAxisParams(axis_params)

        self._manualFrameSelection = ManualFramesSelection(self)
        self.layout().addWidget(self._manualFrameSelection)
        self._manualFrameSelection.setVisible(False)

        # connect signal / Slot
        self._corButtonsGps.buttonClicked.connect(self._angleModeChanged)
        self._manualFrameSelection.sigChanged.connect(self._changed)

    def setScan(self, scan: TomwerScanBase):
        if scan is not None:
            self.setScanRange(scan.scan_range)
        self._manualFrameSelection.setScan(scan=scan)

    def setScanRange(self, scanRange):
        if scanRange == 180:
            self._qrbCOR_90_270.setEnabled(False)
            # force using 0-180 if was using 90-270
            if self._qrbCOR_90_270.isChecked():
                self._qrbCOR_0_180.setChecked(True)
                self._axis_params.angle_mode = CorAngleMode.use_0_180
        else:
            self._qrbCOR_90_270.setEnabled(True)

    def setAngleMode(self, mode):
        """

        :param mode: mode to use (can be manual , 90-270 or 0-180)
        """
        assert isinstance(mode, CorAngleMode)
        if mode == CorAngleMode.use_0_180:
            self._qrbCOR_0_180.setChecked(True)
        elif mode == CorAngleMode.use_90_270:
            self._qrbCOR_90_270.setChecked(True)
        else:
            self._qrbCOR_manual.setChecked(True)

    def getAngleMode(self) -> CorAngleMode:
        """

        :return: the angle to use for the axis calculation
        """
        if self._qrbCOR_90_270.isChecked():
            return CorAngleMode.use_90_270
        elif self._qrbCOR_0_180.isChecked():
            return CorAngleMode.use_0_180
        else:
            return CorAngleMode.manual_selection

    def setAxisParams(self, axis_params):
        with block_signals(self):
            self._axis_params = axis_params
            # set up
            self.setAngleMode(axis_params.angle_mode)

    def _angleModeChanged(self, *args, **kwargs):
        self._axis_params.angle_mode = self.getAngleMode()
        if self.getAngleMode() is CorAngleMode.manual_selection:
            self._axis_params.angle_mode_extra = (
                self._manualFrameSelection.getFramesUrl()
            )
        else:
            self._axis_params.angle_mode_extra = None
        self._manualFrameSelection.setVisible(
            self.getAngleMode() is CorAngleMode.manual_selection
        )
        self._changed()

    def _changed(self):
        self.sigChanged.emit()


class _SliceSelector(qt.QWidget):
    sigChanged = qt.Signal()
    """signal emit when the selected slice change"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._modeCB = QComboBoxIgnoreWheel(self)
        self._modeCB.addItem("middle")
        self._modeCB.addItem("other")
        self.layout().addWidget(self._modeCB)
        self._otherSB = qt.QSpinBox(self)
        self._otherSB.setRange(0, 10000)
        self.layout().addWidget(self._otherSB)

        # connect signal / slot
        self._otherSB.valueChanged.connect(self._valueChanged)
        self._modeCB.currentIndexChanged.connect(self._modeChanged)
        # set up
        self._modeChanged()

    def getSlice(self) -> int | str:
        "return a specific slice index or 'middle'"
        if self.getMode() == "middle":
            return "middle"
        else:
            return self._otherSB.value()

    def setSlice(self, slice_):
        if slice_ is None:
            return
        if slice_ == "middle":
            idx = self._modeCB.findText("middle")
            self._modeCB.setCurrentIndex(idx)
        else:
            idx = self._modeCB.findText("other")
            self._modeCB.setCurrentIndex(idx)
            self._otherSB.setValue(slice_)
        self.sigChanged.emit()

    def getMode(self):
        return self._modeCB.currentText()

    def _valueChanged(self):
        self.sigChanged.emit()

    def _modeChanged(self, *args, **kwargs):
        self._otherSB.setVisible(self.getMode() == "other")
        self._valueChanged()
