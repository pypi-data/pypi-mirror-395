from __future__ import annotations

import pint
from silx.gui import qt
from processview.gui.DropDownWidget import DropDownWidget
from tomwer.synctools.axis import QAxisRP
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.reconstruction.axis.EstimatedCorComboBox import EstimatedCorComboBox
from tomwer.core.process.reconstruction.axis.side import Side
from tomwer.core.process.reconstruction.axis import mode as axis_mode
from tomwer.gui.fonts import FONT_SMALL
from tomwer.gui.utils.scrollarea import QDoubleSpinBoxIgnoreWheel

_ureg = pint.get_application_registry()


class EstimatedCORWidget(qt.QGroupBox):
    """
    Widget to define the estimated center of rotation.
    (based on the motor offset and the 'x_rotation_axis_pixel_position')
    """

    sigValueChanged = qt.Signal()
    """Emit when one of the value changed"""
    sigUpdateXRotAxisPixelPosOnNewScan = qt.Signal()
    """Emit when user want to stop / activate x rotation axis pixel position when a new scan arrives"""
    sigYAxisInvertedChanged = qt.Signal(bool)

    def __init__(self, parent, axis_params: QAxisRP):
        self._axis_params = axis_params
        self._imageWidth = None

        super().__init__(parent)
        self.setLayout(qt.QGridLayout())
        # estimated cor
        self._estimatedCORLabel = qt.QLabel("Estimated CoR (relative)", self)
        self.layout().addWidget(self._estimatedCORLabel, 0, 0, 1, 1)

        self._estimatedCORQCB = EstimatedCorComboBox(self)
        self.layout().addWidget(self._estimatedCORQCB, 0, 1, 1, 1)

        # offset calibration
        self._offsetWidgetDropdown = DropDownWidget(
            parent=self, direction=qt.Qt.LayoutDirection.RightToLeft
        )
        self._offsetWidget = _OffsetCalibration(parent=self, axis_params=axis_params)
        self.layout().addWidget(self._offsetWidgetDropdown, 1, 0, 2, 2)
        self._offsetWidgetDropdown.setWidget(self._offsetWidget)

        # set up
        self._offsetWidgetDropdown.setChecked(False)

        # connect signal / slot
        self._estimatedCORQCB.sigEstimatedCorChanged.connect(self._corChanged)
        self._offsetWidget.sigOffsetChanged.connect(
            self._updateEstimatedCorFromMotorOffsetWidget
        )
        self._offsetWidget.sigXRotationAxisPixelPositionChanged.connect(
            self._updateEstimatedCorFromMotorOffsetWidget
        )
        self._offsetWidget.sigUpdateXRotAxisPixelPosOnNewScan.connect(
            self.sigUpdateXRotAxisPixelPosOnNewScan
        )
        self._offsetWidget.sigYAxisInvertedChanged.connect(self.sigYAxisInvertedChanged)

    def getEstimatedCor(self):
        return self._estimatedCORQCB.getCurrentCorValue()

    def setEstimatedCor(
        self, value: float | Side | str, provided_with_offset: bool = False
    ):

        if isinstance(value, float):
            if self._offsetWidget.isYAxisInverted():
                value = -1.0 * value

            if provided_with_offset:
                value_with_offset = value
                value_without_offset = value - self._offsetWidget.getOffset()
            else:
                value_with_offset = value + self._offsetWidget.getOffset()
                value_without_offset = value
            with block_signals(self._offsetWidget):
                self._offsetWidget.setXRotationAxisPixelPosition(
                    value_without_offset, apply_flip=False
                )
        else:
            # case this is a side
            value_with_offset = value

        self._estimatedCORQCB.setCurrentCorValue(value_with_offset)

        with block_signals(self._axis_params):
            self._axis_params.estimated_cor = value_with_offset

    def _corChanged(self, value):
        assert value is None or isinstance(value, (float, Side, None))
        with block_signals(self._axis_params):
            self._axis_params.estimated_cor = value
        self.sigValueChanged.emit()

    def _updateVisibleSides(self, mode: axis_mode.AxisMode):
        """
        Update the visibility and selection of sides (Left, Center, Right)
        for the Estimated Center of Rotation (CoR) ComboBox based on the
        provided axis mode and a calculated CoR guess.

        This method adjusts the available sides and determines the new
        side (Left, Center, or Right) based on the position of a CoR guess
        relative to the width of the image. The image is divided into thirds:
        - Left: From -infinity to the first third.
        - Center: From the first third to the second third.
        - Right: From the second third to infinity.

        If the CoR guess is not valid or falls outside the calculated bounds,
        a default valid side is selected.

        Behavior:
        ---------
        - By default if the method allows it, the side will be the estimated CoR.
        - If the method does not allow it, it will update the visible sides in
        the Estimated CoR ComboBox based on the valid sides defined in the axis
        mode metadata and dynamically determines the new side (Left, Center, Right)
        based on the CoR guess position within the image width.

        """
        mode = axis_mode.AxisMode.from_value(mode)
        valid_sides = axis_mode.AXIS_MODE_METADATAS[mode].valid_sides
        self._estimatedCORQCB.setSidesVisible(valid_sides)
        first_guess_available = axis_mode.AXIS_MODE_METADATAS[
            mode
        ].allows_estimated_cor_as_numerical_value
        self._estimatedCORQCB.setFirstGuessAvailable(first_guess_available)

        if first_guess_available:
            # if the first guess is valid, when the sides visibility is modify we want to activate it.
            self._estimatedCORQCB.selectFirstGuess()
        elif valid_sides:
            # Proceed only if there are valid sides
            current_side = self._estimatedCORQCB.getCurrentCorValue()
            if not isinstance(current_side, Side) or current_side not in valid_sides:
                with block_signals(self._estimatedCORQCB):
                    cor_guess = self._estimatedCORQCB.getCurrentCorValue()
                    if cor_guess is not None and self._imageWidth is not None:
                        left_boundary = -float("inf")
                        right_boundary = float("inf")
                        middle_left_boundary = (
                            self._imageWidth / 3 - self._imageWidth / 2
                        )
                        middle_right_boundary = (
                            2 * self._imageWidth / 3 - self._imageWidth / 2
                        )

                        if (
                            Side.LEFT in valid_sides
                            and left_boundary <= cor_guess < middle_left_boundary
                        ):
                            new_side = Side.LEFT
                        elif (
                            Side.CENTER in valid_sides
                            and middle_left_boundary
                            <= cor_guess
                            < middle_right_boundary
                        ):
                            new_side = Side.CENTER
                        elif (
                            Side.RIGHT in valid_sides
                            and middle_right_boundary <= cor_guess <= right_boundary
                        ):
                            new_side = Side.RIGHT
                        else:
                            # Fallback to the first available valid side
                            new_side = valid_sides[0]
                    else:
                        # If no guess or boundaries are available, fallback to the first valid side
                        new_side = valid_sides[0]
                    self._estimatedCORQCB.setCurrentCorValue(new_side)
                    self._axis_params.estimated_cor = new_side

    def _updateEstimatedCorFromMotorOffsetWidget(self):
        self._estimatedCORQCB.setCurrentCorValue(self._offsetWidget.getEstimatedCor())
        self.sigValueChanged.emit()

    def setImageWidth(self, image_width: float | None):
        self._imageWidth = image_width

    # expose API
    def updateXRotationAxisPixelPositionOnNewScan(self) -> bool:
        return self._offsetWidget.updateXRotationAxisPixelPositionOnNewScan()

    def setUpdateXRotationAxisPixelPositionOnNewScan(self, update: bool):
        self._offsetWidget.setUpdateXRotationAxisPixelPositionOnNewScan(update=update)

    def setPixelSize(self, pixel_size_m: float | None) -> None:
        self._offsetWidget.setPixelSize(pixel_size_m=pixel_size_m)

    def isYAxisInverted(self) -> bool:
        return self._offsetWidget.isYAxisInverted()

    def setYAxisInverted(self, checked: bool):
        return self._offsetWidget.setYAxisInverted(checked=checked)


class _OffsetCalibration(qt.QGroupBox):

    sigOffsetChanged = qt.Signal()
    sigXRotationAxisPixelPositionChanged = qt.Signal()
    sigUpdateXRotAxisPixelPosOnNewScan = qt.Signal()
    sigYAxisInvertedChanged = qt.Signal(bool)

    def __init__(self, parent, axis_params: QAxisRP):
        super().__init__(parent)
        self._axis_params = axis_params

        self.setLayout(qt.QVBoxLayout())

        # x_rotation_axis_pixel_position
        self._xRotationAxisPixelPositionGroup = qt.QGroupBox("NXtomo metadata ")
        self._xRotationAxisPixelPositionGroup.setLayout(qt.QGridLayout())
        self.layout().addWidget(self._xRotationAxisPixelPositionGroup)
        self._xRotationAxisPixelPositionLabel = qt.QLabel(
            "x_rotation_axis_pixel_position"
        )
        self._xRotationAxisPixelPositionGroup.layout().addWidget(
            self._xRotationAxisPixelPositionLabel, 0, 0, 2, 1
        )
        self._xRotationAxisPixelPositionDSB = QDoubleSpinBoxIgnoreWheel(self)
        self._xRotationAxisPixelPositionDSB.setDecimals(2)
        self._xRotationAxisPixelPositionDSB.setRange(-float("inf"), float("inf"))
        self._xRotationAxisPixelPositionDSB.setSuffix(" px")
        self._xRotationAxisPixelPositionDSB.setEnabled(False)
        self._xRotationAxisPixelPositionGroup.layout().addWidget(
            self._xRotationAxisPixelPositionDSB, 0, 1, 2, 1
        )
        self._xRotationAxisPixelPositionKeepUpdatedCB = qt.QCheckBox(
            "Update with\n new scan"
        )
        self._xRotationAxisPixelPositionKeepUpdatedCB.setFont(FONT_SMALL)
        self._xRotationAxisPixelPositionKeepUpdatedCB.setToolTip(
            "Updates the value when a new scan arrives.\n"
            "Once updated this will change the numerical value of the estimated cor (from estimated relative cor)"
        )
        self._xRotationAxisPixelPositionGroup.layout().addWidget(
            self._xRotationAxisPixelPositionKeepUpdatedCB, 0, 2, 1, 1
        )
        self._yAxisInvertedCB = qt.QCheckBox("Y axis inverted")
        self._yAxisInvertedCB.setFont(FONT_SMALL)
        self._yAxisInvertedCB.setToolTip(
            "Sometime the y axis can be inverted (like on ID11).\nIn this case the estimation of the CoR has a flip that must be handled downstream"
        )
        self._xRotationAxisPixelPositionGroup.layout().addWidget(
            self._yAxisInvertedCB, 1, 2, 1, 1
        )

        # offset group
        self._offsetGroup = qt.QGroupBox("Custom Offset")
        self._offsetGroup.setLayout(qt.QFormLayout())
        self.layout().addWidget(self._offsetGroup)

        # offset
        self._offsetSB = QDoubleSpinBoxIgnoreWheel(self)
        self._offsetSB.setSuffix(" px")
        self._offsetSB.setDecimals(2)
        self._offsetSB.setRange(-float("inf"), float("inf"))
        self._offsetSB.setEnabled(False)
        self._offsetGroup.layout().addRow("Offset", self._offsetSB)

        # motor offset
        self._motorOffsetSB = QDoubleSpinBoxIgnoreWheel(self)
        self._motorOffsetSB.setSuffix(" mm")
        self._motorOffsetSB.setDecimals(4)
        self._motorOffsetSB.setRange(-float("inf"), float("inf"))
        self._offsetGroup.layout().addRow("Y Motor Offset", self._motorOffsetSB)

        # pixel size
        self._pixelSizeSB = QDoubleSpinBoxIgnoreWheel(self)
        self._pixelSizeSB.setSuffix(" µm")
        self._pixelSizeSB.setDecimals(3)
        self._pixelSizeSB.setRange(0, float("inf"))

        # Add a horizontal layout for the pixel size and the padlock
        pixelSizeLayout = qt.QHBoxLayout()

        # Add the spin box to the layout
        pixelSizeLayout.addWidget(self._pixelSizeSB)

        # Add a padlock button
        self._pixelSizePadlock = PadlockButton(self)
        self._pixelSizePadlock.setChecked(True)  # Default to locked
        self._pixelSizePadlock.setFixedSize(24, 24)
        self._pixelSizePadlock.setToolTip("Lock/Unlock pixel size")
        pixelSizeLayout.addWidget(self._pixelSizePadlock)

        # Add the layout to the offset group
        self._offsetGroup.layout().addRow("Pixel Size", pixelSizeLayout)

        # Initialize the spin box as disabled (locked by default)
        self._pixelSizeSB.setEnabled(False)

        # Connect signal to handle locking behavior
        self._pixelSizePadlock.toggled.connect(self._togglePixelSizeLock)

        # set up
        self._xRotationAxisPixelPositionKeepUpdatedCB.setChecked(True)
        self._yAxisInvertedCB.setChecked(False)

        # connect signal / slot
        self._offsetSB.editingFinished.connect(self._offsetEdited)
        self._xRotationAxisPixelPositionKeepUpdatedCB.toggled.connect(
            self.sigUpdateXRotAxisPixelPosOnNewScan
        )
        self._motorOffsetSB.valueChanged.connect(self._motorOffsetChanged)
        self._pixelSizeSB.valueChanged.connect(self._pixelSizeChanged)
        self._yAxisInvertedCB.toggled.connect(self._yAxisInverted)

    def getXRotationAxisPixelPosition(self) -> float:
        return self._xRotationAxisPixelPositionDSB.value()

    def updateXRotationAxisPixelPositionOnNewScan(self) -> bool:
        return self._xRotationAxisPixelPositionKeepUpdatedCB.isChecked()

    def setUpdateXRotationAxisPixelPositionOnNewScan(self, update):
        self._xRotationAxisPixelPositionKeepUpdatedCB.setChecked(update)

    def setXRotationAxisPixelPosition(
        self, value: float, apply_flip: bool = True
    ) -> float:
        """Set the 'x_rotation_axis_pixel_position' and flip it if necessary"""
        if apply_flip and self.isYAxisInverted():
            value = -1.0 * value
        self._xRotationAxisPixelPositionDSB.setValue(value)
        return value

    def getOffset(self) -> float:
        return self._offsetSB.value()

    def setOffset(self, value: float) -> None:
        self._offsetSB.setValue(value)
        self._offsetEdited()

    def _offsetEdited(self):
        with block_signals(self):
            self._axis_params.x_rotation_axis_pos_px_offset = self.getOffset()
        self.sigOffsetChanged.emit()

    def _motorOffsetChanged(self):
        """Recalculate the offset when the motor offset changes."""
        if self._pixelSizeSB.value() and self._motorOffsetSB.value():
            pixel_size = self._pixelSizeSB.value() * _ureg.micrometer
            motor_offset = self._motorOffsetSB.value() * _ureg.millimeter
            with block_signals(self):
                self.setOffset((motor_offset / pixel_size).to_base_units().magnitude)
            self.sigOffsetChanged.emit()

    def _pixelSizeChanged(self):
        """Recalculate the offset when the pixel size changes."""
        if self._pixelSizeSB.value() and self._motorOffsetSB.value():
            pixel_size = self._pixelSizeSB.value() * _ureg.micrometer
            motor_offset = self._motorOffsetSB.value() * _ureg.millimeter
            with block_signals(self):
                self.setOffset((motor_offset / pixel_size).to_base_units().magnitude)
            self.sigOffsetChanged.emit()

    def _xRotationAxisPixelPositionEdited(self):
        with block_signals(self._axis_params):
            self._axis_params.x_rotation_axis_pixel_position = (
                self.getXRotationAxisPixelPosition()
            )
        self.sigXRotationAxisPixelPositionChanged.emit()

    def _yAxisInverted(self):
        self.setXRotationAxisPixelPosition(
            value=-1.0 * self.getXRotationAxisPixelPosition(),
            apply_flip=False,
        )
        self._xRotationAxisPixelPositionEdited()

    def isYAxisInverted(self) -> bool:
        return self._yAxisInvertedCB.isChecked()

    def setYAxisInverted(self, checked: bool):
        self._yAxisInvertedCB.setChecked(checked)

    def getEstimatedCor(self) -> float:
        return self.getXRotationAxisPixelPosition() + self.getOffset()

    def setPixelSize(self, pixel_size_m: float | None):
        if pixel_size_m is None:
            self._pixelSizeSB.clear()
        else:
            self._pixelSizeSB.setValue(
                (pixel_size_m * _ureg.meter).to(_ureg.micrometer).magnitude
            )

    def _togglePixelSizeLock(self, locked: bool):
        """Lock or unlock the pixel size spin box."""
        self._pixelSizeSB.setEnabled(not locked)
