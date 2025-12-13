from __future__ import annotations

import logging
import numpy

from silx.gui import qt

from tomwer.core.process.reconstruction.utils.cor import (
    absolute_pos_to_relative,
    relative_pos_to_absolute,
)
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.settings import EDITING_BACKGROUND_COLOR
from tomwer.synctools.axis import QAxisRP

_logger = logging.getLogger(__file__)


class ControlWidget(qt.QWidget):
    """
    Widget to lock, compute or validate the cor position and display it value as absolute or relative
    This is the widget displayed at the bottom of the AxisOW
    """

    sigComputationRequest = qt.Signal()
    """Signal emitted when user request a computation from the settings"""

    sigValidateRequest = qt.Signal()
    """Signal emitted when user validate the current settings"""

    sigLockCORValueChanged = qt.Signal(bool)
    """Signal emitted when the user lock the cor value. Param: True if lock"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())

        # display 'center' information
        self._positionInfo = _PositionInfoWidget(parent=self)
        self.layout().addWidget(self._positionInfo)

        self._buttons = qt.QWidget(parent=self)
        self._buttons.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._buttons)

        self._lockBut = PadlockButton(parent=self)
        self._lockBut.setAutoDefault(False)
        self._lockBut.setDefault(False)

        self._buttons.layout().addWidget(self._lockBut)
        self._lockLabel = qt.QLabel("lock cor value", parent=self)
        self._buttons.layout().addWidget(self._lockLabel)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._buttons.layout().addWidget(spacer)

        self._computeBut = qt.QPushButton("compute", parent=self)
        self._buttons.layout().addWidget(self._computeBut)
        style = qt.QApplication.style()
        applyIcon = style.standardIcon(qt.QStyle.SP_DialogApplyButton)
        self._applyBut = qt.QPushButton(applyIcon, "validate", parent=self)
        self._buttons.layout().addWidget(self._applyBut)
        self.layout().addWidget(self._buttons)

        # set up
        self._positionInfo.setPosition(None, None)

        # make connection
        self._computeBut.pressed.connect(self._needComputation)
        self._applyBut.pressed.connect(self._validate)
        self._lockBut.sigLockChanged.connect(self._lockValueChanged)

    def hideLockButton(self) -> None:
        self._lockLabel.hide()
        self._lockBut.hide()

    def hideApplyButton(self) -> None:
        self._applyBut.hide()

    def _lockValueChanged(self):
        self.sigLockCORValueChanged.emit(self._lockBut.isLocked())
        self._computeBut.setEnabled(not self._lockBut.isLocked())

    def _needComputation(self, *arg, **kwargs):
        """callback when the radio line changed"""
        self.sigComputationRequest.emit()

    def _validate(self):
        self.sigValidateRequest.emit()

    def setPosition(self, relative_cor, abs_cor):
        self._positionInfo.setPosition(relative_cor=relative_cor, abs_cor=abs_cor)

    def _updateAbsolutePosition(self, width):
        self._positionInfo._updateAbsolutePosition(width=width)

    def _updateRelativePosition(self, width):
        self._positionInfo._updateRelativePosition(width=width)

    def isValueLock(self):
        return self._lockBut.isLocked()

    def setValueLock(self, lock):
        self._lockBut.setLock(lock)


class _PositionInfoValidator(qt.QDoubleValidator):
    def validate(self, a0: str, a1: int):
        if "..." in a0 or a0 == "?":
            return (qt.QDoubleValidator.Acceptable, a0, a1)
        else:
            return super().validate(a0, a1)


class _PositionInfoWidget(qt.QWidget):
    """Widget used to display information relative to the current position"""

    sigRelativeValueSet = qt.Signal(float)
    """Emit when the user define manually the relative value"""
    sigAbsolueValueSet = qt.Signal(float)
    """Emit when the user define manually the absolute value"""

    def __init__(self, parent, axis=None):
        self._axis_params = None
        self._defaultBackgroundColor = None
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        centerLabel = qt.QLabel("center", parent=self)
        centerLabel.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        font = centerLabel.font()
        font.setBold(True)
        centerLabel.setFont(font)

        self.layout().addWidget(centerLabel, 0, 0, 1, 1)
        self.layout().addWidget(qt.QLabel(" (relative):"), 0, 1, 1, 1)

        self._relativePositionQLE = qt.QLineEdit("", parent=self)
        self._positionValidator = _PositionInfoValidator(self)
        self._relativePositionQLE.setValidator(self._positionValidator)
        self._relativePositionQLE.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum
        )
        self._relativePositionQLE.setStyleSheet("color: red")
        self.layout().addWidget(self._relativePositionQLE, 0, 2, 1, 1)

        centerLabel = qt.QLabel("center", parent=self)
        centerLabel.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        font = centerLabel.font()
        font.setBold(False)
        centerLabel.setFont(font)

        self.layout().addWidget(centerLabel, 1, 0, 1, 1)
        self.layout().addWidget(qt.QLabel(" (absolute):"), 1, 1, 1, 1)
        self._absolutePositionQLE = qt.QLineEdit("", parent=self)
        self._absolutePositionQLE.setValidator(self._positionValidator)
        self._absolutePositionQLE.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum
        )
        self._absolutePositionQLE.setStyleSheet("color: #ff8c00")
        self.layout().addWidget(self._absolutePositionQLE, 1, 2, 1, 1)

        if axis:
            self.setAxisParams(axis)

        # connect signal / slot
        self._relativePositionQLE.textEdited.connect(
            self._userStartEditingRelativePosition
        )
        self._relativePositionQLE.editingFinished.connect(
            self._userUpdatedRelativePosition
        )
        self._absolutePositionQLE.textEdited.connect(
            self._userStartEditingAbsolutePosition
        )

        self._absolutePositionQLE.editingFinished.connect(
            self._userUpdatedAbsolutePosition
        )

    def _getDefaultBackgroundColor(self):
        if self._defaultBackgroundColor is None:
            self._defaultBackgroundColor = self.palette().color(
                self._absolutePositionQLE.backgroundRole()
            )
        return self._defaultBackgroundColor

    def _userStartEditingRelativePosition(self, *args, **kwargs):
        palette = self.palette()
        palette.setColor(
            self._relativePositionQLE.backgroundRole(), EDITING_BACKGROUND_COLOR
        )
        self._relativePositionQLE.setPalette(palette)

    def _userStartEditingAbsolutePosition(self, *args, **kwargs):
        palette = self.palette()
        palette.setColor(
            self._absolutePositionQLE.backgroundRole(), EDITING_BACKGROUND_COLOR
        )
        self._absolutePositionQLE.setPalette(palette)

    def _userUpdatedRelativePosition(self, *args, **kwargs):
        palette = self.palette()
        palette.setColor(
            self._relativePositionQLE.backgroundRole(),
            self._getDefaultBackgroundColor(),
        )
        self._relativePositionQLE.setPalette(palette)
        if self._relativePositionQLE.text().startswith((".", "?")):
            return
        else:
            value = float(self._relativePositionQLE.text())
            # make sure we only emit the signal if the value changed (and when the Qline has been edited).
            if isinstance(self._axis_params.relative_cor_value, (type(None), str)) or (
                self._axis_params is not None
                and not numpy.isclose(
                    value, self._axis_params.relative_cor_value, atol=1e-3
                )
            ):
                self.sigRelativeValueSet.emit(value)

    def _userUpdatedAbsolutePosition(self, *args, **kwargs):
        palette = self.palette()
        palette.setColor(
            self._absolutePositionQLE.backgroundRole(),
            self._getDefaultBackgroundColor(),
        )
        self._absolutePositionQLE.setPalette(palette)
        if self._absolutePositionQLE.text().startswith((".", "?")):
            return
        else:
            value = float(self._absolutePositionQLE.text())
            # make sure we only emit the signal if the value changed (and when the Qline has been edited).
            if self._axis_params.absolute_cor_value is None or (
                self._axis_params is not None
                and not numpy.isclose(
                    value, self._axis_params.absolute_cor_value, atol=1e-3
                )
            ):
                self.sigAbsolueValueSet.emit(value)

    def setAxisParams(self, axis):
        assert isinstance(axis, QAxisRP)
        if axis == self._axis_params:
            return
        self._axis_params = axis

    def getPosition(self):
        return float(self._relativePositionQLE.text())

    def setPosition(self, relative_cor: float | None, abs_cor: float | None):
        if relative_cor is None:
            self._relativePositionQLE.setText("?")
        elif isinstance(relative_cor, str):
            self._relativePositionQLE.setText(relative_cor)
        else:
            self._relativePositionQLE.setText(f"{relative_cor:.3f}")
        if abs_cor is None:
            self._absolutePositionQLE.setText("?")
        else:
            self._absolutePositionQLE.setText(f"{abs_cor:.3f}")

    def _updateAbsolutePosition(self, width):
        if width is not None:
            try:
                rel_value = float(self._relativePositionQLE.text())
            except Exception:
                return
            else:
                abs_value = relative_pos_to_absolute(
                    relative_pos=float(rel_value), det_width=width
                )
                self._absolutePositionQLE.setText(str(abs_value))

    def _updateRelativePosition(self, width):
        if width is not None:
            try:
                abs_value = float(self._absolutePositionQLE.text())
            except Exception:
                return
            else:
                rel_value = absolute_pos_to_relative(
                    absolute_pos=float(abs_value), det_width=width
                )
                self._relativePositionQLE.setText(str(rel_value))
