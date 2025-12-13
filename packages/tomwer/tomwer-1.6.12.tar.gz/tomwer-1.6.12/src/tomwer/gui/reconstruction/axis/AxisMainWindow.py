"""
contains gui relative to axis calculation using sinogram
"""

from __future__ import annotations

import logging

from silx.gui import qt
from tomwer.gui.utils.qt_utils import block_signals

from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.process.reconstruction.utils.cor import (
    absolute_pos_to_relative,
    relative_pos_to_absolute,
)
from tomwer.core.scan.scanbase import TomwerScanBase

from ...utils.scandescription import ScanNameLabelAndShape
from .AxisWidget import AxisWidget
from .ControlWidget import ControlWidget

_logger = logging.getLogger(__file__)


class AxisMainWindow(qt.QMainWindow):
    """
    Main window for the center of rotation search.
    It displays:
    * scan information
    * AxisWidget
    * allows to set the cor value as absolute and relative and edit it
    """

    sigComputationRequested = qt.Signal()
    """emit when the user request for computation"""

    sigApply = qt.Signal()
    """emit when the user validate the axis value"""

    sigLockCORValueChanged = qt.Signal(bool)
    """bool: True if locked"""

    sigLockModeChanged = qt.Signal()
    """Signal emitted when the lock mode on the mode change"""

    sigModeChanged = qt.Signal(str)
    """signal emit when the mode is changed"""

    sigSinogramReady = qt.Signal()
    """signal emit when the sinogram load is complete and processing ready"""

    sigAxisEditionLocked = qt.Signal(bool)
    """Signal emitted when the status of the reconstruction parameters edition
    change"""

    def __init__(self, axis_params, parent=None, backend=None):
        super().__init__(parent)

        self._mainWidget = qt.QWidget(self)
        self._mainWidget.setLayout(qt.QVBoxLayout())

        # add scan name
        self._scan_label = ScanNameLabelAndShape(parent=self)
        self._mainWidget.layout().addWidget(self._scan_label)

        self.setDockOptions(qt.QMainWindow.AnimatedDocks)

        # Axis Widget
        self._axis_params = axis_params
        self._axisWidget = AxisWidget(
            parent=self, axis_params=axis_params, backend=backend
        )
        self._mainWidget.layout().addWidget(self._axisWidget)
        self.setCentralWidget(self._mainWidget)

        # append cor editor to the radio axis widget
        self._controlWidget = ControlWidget(parent=self)
        self._controlWidget.setSizePolicy(
            qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum
        )
        self._controlDockWidget = qt.QDockWidget(parent=self)
        self._controlDockWidget.setSizePolicy(
            qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum
        )
        self._controlDockWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._controlDockWidget.layout().setSpacing(0)
        self._controlDockWidget.setMaximumHeight(150)
        self._controlDockWidget.setWidget(self._controlWidget)
        self._controlDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._axisWidget.addDockWidget(
            qt.Qt.RightDockWidgetArea, self._controlDockWidget
        )

        # set up
        if self._axis_params.mode is AxisMode.manual:
            self._controlWidget.setPosition(
                self._axis_params.relative_cor_value,
                self._axis_params.absolute_cor_value,
            )
        self._controlWidget._positionInfo.setAxisParams(self._axis_params)

        # connect signal / slots
        self._controlWidget.sigComputationRequest.connect(self.sigComputationRequested)
        self._controlWidget.sigValidateRequest.connect(self.sigApply)
        self._controlWidget.sigLockCORValueChanged.connect(self._CORValueLocked)
        self._axisWidget.sigLockModeChanged.connect(self.sigLockModeChanged)
        self._axisWidget.sigPositionChanged.connect(self._setPositionFrmTuple)
        self._controlWidget._positionInfo.sigRelativeValueSet.connect(
            self._forceRelativePosition
        )
        self._controlWidget._positionInfo.sigAbsolueValueSet.connect(
            self._forceAbsolutePosition
        )

    def _forceRelativePosition(self, value: float):
        self.setMode(AxisMode.manual)
        self.setPosition(
            relative_value=value,
            absolute_value=None,
        )

    def _forceAbsolutePosition(self, value: float):
        self.setMode(AxisMode.manual)
        self.setPosition(
            relative_value=None,
            absolute_value=value,
        )

    def setAutoUpdateEstimatedCor(self, value):
        self._axisWidget._settingsWidget._mainWidget.setUpdateXRotationAxisPixelPositionOnNewScan(
            value
        )

    def manual_uses_full_image(self, value):
        self._axisWidget.manual_uses_full_image(value)

    def _modeChanged(self):
        self.getAxisParams().mode = self.getMode()

    def _CORValueLocked(self, lock):
        if lock:
            self.setMode(AxisMode.manual)
        self.setModeLock(lock)
        self.sigLockCORValueChanged.emit(lock)

    def _setPositionFrmTuple(self, value):
        self.setPosition(relative_value=value[0])

    def setPosition(self, relative_value: float, absolute_value: float = None) -> None:
        if (
            absolute_value is None
            and self._axis_params.frame_width is not None
            and relative_value is not None
        ):
            try:
                absolute_value = relative_pos_to_absolute(
                    relative_pos=relative_value, det_width=self._axis_params.frame_width
                )
            except TypeError:
                absolute_value = None
        if (
            relative_value is None
            and self._axis_params.frame_width is not None
            and absolute_value is not None
        ):
            try:
                relative_value = absolute_pos_to_relative(
                    absolute_pos=absolute_value, det_width=self._axis_params.frame_width
                )
            except TypeError:
                relative_value = None
        self._controlWidget.setPosition(
            relative_cor=relative_value, abs_cor=absolute_value
        )
        if relative_value is not None:
            self._axisWidget.setXShift(relative_value)
        else:
            self._axisWidget.resetShift()

    def getAxisParams(self):
        return self._axis_params

    def setScan(self, scan: TomwerScanBase, set_position: bool = False):
        """
        set the gui for this scan

        :param scan:
        """
        self._axisWidget.setScan(scan=scan)
        if set_position is True and scan.axis_params is not None:
            self.setPosition(
                scan.axis_params.relative_cor_value, scan.axis_params.relative_cor_value
            )
        elif set_position is False:
            if scan.dim_1 is not None:
                # if absolute position is know and relative position not (in the case the user already define absolute position only):
                has_absolute_val_already = not self._controlWidget._positionInfo._absolutePositionQLE.text().startswith(
                    (".", "?")
                )
                has_relative_val_already = not self._controlWidget._positionInfo._relativePositionQLE.text().startswith(
                    (".", "?")
                )
                if (
                    self.getMode() is AxisMode.manual
                    and has_absolute_val_already
                    and not has_relative_val_already
                ):
                    self._controlWidget._updateRelativePosition(width=scan.dim_1)
                else:
                    self._controlWidget._updateAbsolutePosition(width=scan.dim_1)

    def _computationRequested(self) -> None:
        self.sigComputationRequested.emit()

    def _setModeLockFrmSettings(self, lock):
        with block_signals(self):
            self._axisWidget._setModeLockFrmSettings(lock)

    def _setValueLockFrmSettings(self, lock):
        with block_signals(self):
            self.setValueLock(lock)

    def setModeLock(self, lock):
        assert type(lock) is bool
        self._axisWidget.setLocked(lock)

    def isModeLock(self):
        return self._axisWidget.isModeLock()

    def isValueLock(self):
        return self._controlWidget.isValueLock()

    def setValueLock(self, lock):
        self._controlWidget.setValueLock(lock)

    def setReconsParams(self, recons_params):
        self._axis_params = recons_params
        self._axisWidget.setReconsParams(axis=recons_params)
        if recons_params.mode is AxisMode.manual:
            self._controlWidget.setPosition(
                self._axis_params.relative_cor_value,
                self._axis_params.absolute_cor_value,
            )

    # expose API
    def hideLockButton(self) -> None:
        self._controlWidget.hideLockButton()

    def hideApplyButton(self) -> None:
        self._controlWidget.hideApplyButton()

    def setMode(self, mode):
        mode = AxisMode.from_value(mode)
        self._axisWidget.setMode(mode)
        self._axis_params.mode = mode
        self.sigModeChanged.emit(mode.value)

    def getMode(self):
        return self._axisWidget.getMode()

    def getEstimatedCor(self) -> float:
        return self._axisWidget.getEstimatedCor()

    def setEstimatedCor(self, value: float):
        self._axisWidget.setEstimatedCor(value=value)

    def getAutoUpdateEstimatedCor(self):
        return self._axisWidget.updateXRotationAxisPixelPositionOnNewScan()

    def isYAxisInverted(self) -> bool:
        return self._axisWidget.isYAxisInverted()

    def setYAxisInverted(self, checked: bool):
        return self._axisWidget.setYAxisInverted(checked=checked)
