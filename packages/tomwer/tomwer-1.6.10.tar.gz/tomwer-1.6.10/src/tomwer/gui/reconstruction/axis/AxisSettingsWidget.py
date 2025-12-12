from __future__ import annotations

import enum
import logging

from silx.gui import qt

from tomwer.core.process.reconstruction.axis import mode as axis_mode
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.utils.step import StepSizeSelectorWidget
from tomwer.synctools.axis import QAxisRP
from tomwer.gui.settings import EDITING_BACKGROUND_COLOR

from .AxisOptionsWidget import AxisOptionsWidget
from .CalculationWidget import CalculationWidget
from .InputWidget import InputWidget


_logger = logging.getLogger(__name__)


@enum.unique
class ShiftMode(enum.Enum):
    x_only = 0
    y_only = 1
    x_and_y = 2


class AxisSettingsWidget(qt.QWidget):
    """
    Widget to define settings for COR search (which algorithm to use...)
    """

    sigShiftChanged = qt.Signal(float, float)
    """Signal emitted when requested shift changed. Parameter is x, y"""

    sigModeLockChanged = qt.Signal(bool)
    """Signal emitted when the mode is lock or unlock"""

    sigResetZoomRequested = qt.Signal()
    """Signal emitted when request a zoom reset from the plot"""

    sigSubSamplingChanged = qt.Signal()
    """Signal emitted when sub-sampling change"""

    sigUrlChanged = qt.Signal()
    """Signal emit when frames urls changed"""

    sigModeChanged = qt.Signal(str)
    """Signal emit when mode (algorithm) is changed"""

    sigRoiChanged = qt.Signal(object)
    """Signal emitted when the ROI changed"""

    sigAuto = qt.Signal()
    """Signal emitted when the auto button is activated"""

    def __init__(self, parent, reconsParams):
        assert isinstance(reconsParams, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self._xShift = 0
        self._yShift = 0
        self._recons_params = reconsParams
        self._axisParams = None

        self.setLayout(qt.QVBoxLayout())

        self._manualSelectionWidget = ManualAxisSelectionWidget(
            parent=self, shift_mode=ShiftMode.x_only
        )
        self._manualSelectionWidget.layout().setContentsMargins(0, 0, 0, 0)

        self._displacementSelector = self._manualSelectionWidget._displacementSelector
        self._shiftControl = self._manualSelectionWidget._shiftControl
        self._roiControl = self._manualSelectionWidget._roiControl
        self._imgOpts = self._manualSelectionWidget._imgOpts

        self._mainWidget = AxisSettingsTabWidget(
            parent=self,
            recons_params=self._recons_params,
        )
        # append the Manual selection to the AxisTabWidget to have all widget related to axis settings together
        self._mainWidget._calculationWidget.layout().addWidget(
            self._manualSelectionWidget
        )

        self.layout().addWidget(self._mainWidget)

        # signal / slot connection
        self._shiftControl.sigShiftLeft.connect(self._incrementLeftShift)
        self._shiftControl.sigShiftRight.connect(self._incrementRightShift)
        self._shiftControl.sigShiftTop.connect(self._incrementTopShift)
        self._shiftControl.sigShiftBottom.connect(self._incrementBottomShift)
        self._shiftControl.sigReset.connect(self._resetShift)
        self._shiftControl.sigShiftChanged.connect(self._setShiftAndSignal)
        self._mainWidget.sigLockModeChanged.connect(self._modeLockChanged)
        self._manualSelectionWidget.sigResetZoomRequested.connect(
            self._requestZoomReset
        )
        self._imgOpts.sigSubSamplingChanged.connect(self.sigSubSamplingChanged)
        self._mainWidget.sigUrlChanged.connect(self.sigUrlChanged)
        self._roiControl.sigRoiChanged.connect(self.sigRoiChanged)
        self._shiftControl.sigAuto.connect(self.sigAuto)
        self._mainWidget.sigModeChanged.connect(self.sigModeChanged)

        # set up interface
        self.setAxisParams(self._recons_params)

    def setScan(self, scan):
        self._mainWidget.setScan(scan=scan)
        self._roiControl.setScan(scan=scan)

    def manual_uses_full_image(self, value):
        self._roiControl.manual_uses_full_image(value)

    def _incrementLeftShift(self):
        self._incrementShift("left")

    def _incrementRightShift(self):
        self._incrementShift("right")

    def _incrementTopShift(self):
        self._incrementShift("top")

    def _incrementBottomShift(self):
        self._incrementShift("bottom")

    def _setShiftAndSignal(self, x, y):
        if x == self._xShift and y == self._yShift:
            return
        self.setShift(x, y)
        self._shiftControl._updateShiftInfo(x=x, y=y)
        self.sigShiftChanged.emit(x, y)

    def setAxisParams(self, axis):
        if axis == self._axisParams:
            return
        assert isinstance(axis, QAxisRP)
        with block_signals(self):
            if self._axisParams:
                self._axisParams.sigChanged.disconnect(self._updateAxisView)
            self._axisParams = axis
            self.setXShift(self._axisParams.relative_cor_value)
            self._mainWidget.setAxisParams(self._axisParams)
            self._updateAxisView()
            self._axisParams.sigChanged.connect(self._updateAxisView)

    def _modeLockChanged(self, lock):
        self.sigModeLockChanged.emit(lock)

    def setMode(self, mode):
        with block_signals(self._axisParams):
            self._axisParams.mode = mode
            self._mainWidget._calculationWidget.setMode(mode)
            self._mainWidget._optionsWidget.setMode(mode)
            self._updateAxisView()
        self._axisParams.sigChanged.emit()

    def _updateAxisView(self):
        with block_signals(self._axisParams):
            if self._axisParams.relative_cor_value not in (None, "..."):
                self.setXShift(self._axisParams.relative_cor_value)

        self._manualSelectionWidget.setVisible(
            self._axisParams.mode is axis_mode.AxisMode.manual
        )

    def getAxisParams(self):
        return self._axisParams

    def _incrementShift(self, direction):
        assert direction in ("left", "right", "top", "bottom")
        if direction == "left":
            self.setXShift(self._xShift - self.getShiftStep())
        elif direction == "right":
            self.setXShift(self._xShift + self.getShiftStep())
        elif direction == "top":
            self.setYShift(self._yShift + self.getShiftStep())
        else:
            self.setYShift(self._yShift - self.getShiftStep())

        self._shiftControl._updateShiftInfo(x=self._xShift, y=self._yShift)

    def _resetShift(self):
        with block_signals(self._axisParams):
            self.setXShift(0)
            self.setYShift(0)
            self._shiftControl._updateShiftInfo(x=self._xShift, y=self._yShift)

        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def getXShift(self):
        if self._xShift == "...":
            return 0
        return self._xShift

    def getYShift(self):
        if self._yShift == "...":
            return 0
        return self._yShift

    def setXShift(self, x: float):
        self.setShift(x=x, y=self._yShift)

    def setYShift(self, y):
        self.setShift(x=self._xShift, y=y)

    def setShift(self, x, y):
        if x == self._xShift and y == self._yShift:
            return
        self._xShift = x if x is not None else 0.0
        self._yShift = y if y is not None else 0.0
        if self._axisParams:
            with block_signals(self._axisParams):
                self._axisParams.set_relative_value(x)
        self._shiftControl._updateShiftInfo(x=self._xShift, y=self._yShift)
        if not isinstance(self._xShift, str):
            # filter `...` and `?` values (used for issues or processing)
            self.sigShiftChanged.emit(self._xShift, self._yShift)

    def reset(self):
        with block_signals(self):
            self.setShift(0, 0)
        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def setLocked(self, locked):
        self._mainWidget.setEnabled(not locked)

    def _requestZoomReset(self):
        self.sigResetZoomRequested.emit()

    # expose API

    def setEstimatedCor(self, value):
        self._mainWidget.setEstimatedCorValue(value=value)

    def updateXRotationAxisPixelPositionOnNewScan(self) -> bool:
        return self._mainWidget.updateXRotationAxisPixelPositionOnNewScan()

    def setUpdateXRotationAxisPixelPositionOnNewScan(self, update: bool):
        self._mainWidget.setUpdateXRotationAxisPixelPositionOnNewScan(update=update)

    def getEstimatedCor(self):
        return self._mainWidget.getEstimatedCor()

    def getROIDims(self):
        return self._roiControl.getROIDims()

    def getShiftStep(self):
        return self._displacementSelector.getStepSize()

    def setShiftStep(self, value):
        self._displacementSelector.setStepSize(value=value)

    def getROIOrigin(self):
        return self._roiControl.getROIOrigin()

    def getImgSubSampling(self):
        return self._imgOpts.getSubSampling()

    def getMode(self):
        return self._mainWidget.getMode()

    def isModeLock(self):
        return self._mainWidget.isModeLock()

    def setModeLock(self, mode):
        return self._mainWidget.setModeLock(mode=mode)

    def isYAxisInverted(self) -> bool:
        return self._mainWidget.isYAxisInverted()

    def setYAxisInverted(self, checked: bool):
        return self._mainWidget.setYAxisInverted(checked=checked)


class ManualAxisSelectionWidget(qt.QWidget):
    sigResetZoomRequested = qt.Signal()
    """Signal emitted when a zoom request is necessary (when change to full
    image)"""

    def __init__(self, parent, shift_mode):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._displacementSelector = StepSizeSelectorWidget(
            parent=self,
            fine_value=0.1,
            medium_value=1.0,
            rough_value=None,
            dtype=float,
        )
        self.layout().addWidget(self._displacementSelector)

        self._shiftControl = _ShiftControl(parent=self, shift_mode=shift_mode)
        self.layout().addWidget(self._shiftControl)

        self._roiControl = _ROIControl(parent=self)
        self.layout().addWidget(self._roiControl)

        self._imgOpts = _ImgOpts(parent=self)
        self.layout().addWidget(self._imgOpts)

        # connect signal / slot
        self._roiControl.sigResetZoomRequested.connect(self.sigResetZoomRequested)


class _ROIControl(qt.QGroupBox):
    """
    Widget used to define the ROI on images to compare
    """

    sigRoiChanged = qt.Signal(object)
    """Signal emitted when the ROI changed"""
    sigResetZoomRequested = qt.Signal()
    """Signal emitted when a zoom request is necessary (when change to full
    image)"""

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, "ROI selection", parent)
        self.setLayout(qt.QVBoxLayout())

        self._buttonGrp = qt.QButtonGroup(parent=self)
        self._buttonGrp.setExclusive(True)

        self._roiWidget = qt.QWidget(parent=self)
        self._roiWidget.setLayout(qt.QHBoxLayout())
        self._roiWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._fullImgButton = qt.QRadioButton("full image", parent=self)
        self._buttonGrp.addButton(self._fullImgButton)
        self.layout().addWidget(self._fullImgButton)
        self._roiButton = qt.QRadioButton("ROI", parent=self._roiWidget)
        self._roiWidget.layout().addWidget(self._roiButton)
        self._buttonGrp.addButton(self._roiButton)
        self._roiDefinition = _ROIDefinition(parent=self)
        self._roiWidget.layout().addWidget(self._roiDefinition)
        self.layout().addWidget(self._roiWidget)

        # connect signal / Slot
        self._roiButton.toggled.connect(self._roiDefinition.setEnabled)
        self._fullImgButton.toggled.connect(self.sigResetZoomRequested)
        self._roiButton.toggled.connect(self.sigResetZoomRequested)
        self._roiDefinition.sigRoiChanged.connect(self.sigRoiChanged)

        # setup for full image
        self._fullImgButton.setChecked(True)

    def getROIDims(self):
        if self._roiButton.isChecked():
            return self._roiDefinition.getROIDims()
        else:
            return None

    def manual_uses_full_image(self, activate):
        if activate:
            self._fullImgButton.setChecked(True)
        else:
            self._roiButton.setChecked(True)

    # expose API
    def getROIOrigin(self):
        return self._roiDefinition.getROIOrigin()

    def setLimits(self, width, height):
        self._roiDefinition.setLimits(width=width, height=height)

    def setScan(self, scan):
        self._roiDefinition.setScan(scan=scan)


class _ROIDefinition(qt.QWidget):
    """
    Widget used to define ROI width and height.

    :note: emit ROI == None if setDisabled
    """

    sigRoiChanged = qt.Signal(object)
    """Signal emitted when the ROI changed"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self._already_set = False

        # width & height
        self.layout().addWidget(qt.QLabel("dims", self), 0, 0)
        self._widthSB = qt.QSpinBox(parent=self)
        self._widthSB.setSingleStep(2)
        self._widthSB.setMaximum(10000)
        self._widthSB.setSuffix(" px")
        self._widthSB.setPrefix("w: ")
        self._widthSB.setToolTip("ROI width")
        self.layout().addWidget(self._widthSB, 0, 1)
        self._heightSB = qt.QSpinBox(parent=self)
        self._heightSB.setSingleStep(2)
        self._heightSB.setSuffix(" px")
        self._heightSB.setPrefix("h: ")
        self._heightSB.setToolTip("ROI height")
        self._heightSB.setMaximum(10000)
        self.layout().addWidget(self._heightSB, 0, 2)

        # origin x and y position
        self.layout().addWidget(qt.QLabel("origin", self), 1, 0)
        self._xOriginSB = qt.QSpinBox(parent=self)
        self._xOriginSB.setSingleStep(10)
        self._xOriginSB.setMaximum(10000)
        self._xOriginSB.setPrefix("x: ")
        self.layout().addWidget(self._xOriginSB, 1, 1)
        self._yOriginSB = qt.QSpinBox(parent=self)
        self._yOriginSB.setSingleStep(10)
        self._yOriginSB.setPrefix("y: ")
        self._yOriginSB.setMaximum(10000)
        self.layout().addWidget(self._yOriginSB, 1, 2)

        # Signal / Slot connection
        self._widthSB.editingFinished.connect(self.__roiChanged)
        self._heightSB.editingFinished.connect(self.__roiChanged)
        self._xOriginSB.editingFinished.connect(self.__roiChanged)
        self._yOriginSB.editingFinished.connect(self.__roiChanged)

    def __roiChanged(self, *args, **kwargs):
        self.sigRoiChanged.emit((self.getROIDims(), self.getROIOrigin()))

    def setLimits(self, width, height):
        """

        :param x: width maximum value
        :param height: height maximum value
        """
        for spinButton in (self._widthSB, self._heightSB):
            spinButton.blockSignals(True)
        assert type(width) is int
        assert type(height) is int
        valueChanged = False
        if self._widthSB.value() > width:
            self._widthSB.setValue(width)
            valueChanged = True
        if self._heightSB.value() > height:
            self._heightSB.setValue(height)
            valueChanged = True

        # if this is the first limit definition, propose default width and
        # height
        if self._widthSB.value() == 0:
            self._widthSB.setValue(min(256, width))
            valueChanged = True
        if self._heightSB.value() == 0:
            self._heightSB.setValue(min(256, height))
            valueChanged = True

        # define minimum / maximum
        self._widthSB.setRange(1, width)
        self._heightSB.setRange(1, height)
        for spinButton in (self._widthSB, self._heightSB):
            spinButton.blockSignals(False)
        if valueChanged is True:
            self.__roiChanged()

    def getROIDims(self) -> tuple | None:
        """

        :return: (width, height) or None
        """
        if self.isEnabled():
            return (self._widthSB.value(), self._heightSB.value())
        else:
            return None

    def getROIOrigin(self):
        return (self._xOriginSB.value(), self._yOriginSB.value())

    def setEnabled(self, *arg, **kwargs):
        qt.QWidget.setEnabled(self, *arg, **kwargs)
        self.__roiChanged()

    def setScan(self, scan):
        if not self._already_set:
            self._already_set = True
            try:
                x_origin = scan.dim_1 // 2
                y_origin = scan.dim_2 // 2
                self._xOriginSB.setValue(x_origin)
                self._yOriginSB.setValue(y_origin)
            except Exception:
                _logger.warning(f"unable to determine origin for {scan}")


class AxisSettingsTabWidget(qt.QTabWidget):
    """
    TabWidget containing all the settings of the AxisTask
    """

    sigLockModeChanged = qt.Signal(bool)
    """signal emitted when the mode lock change"""

    sigUrlChanged = qt.Signal()
    """Signal emit when frames urls changed"""

    sigModeChanged = qt.Signal(str)
    """Signal emit when mode (algorithm) is changed"""

    sigUpdateXRotAxisPixelPosOnNewScan = qt.Signal()

    def __init__(
        self,
        recons_params: QAxisRP | None,
        parent=None,
    ):
        """

        :param recons_params: reconstruction parameters edited by the widget
        """
        qt.QTabWidget.__init__(self, parent)
        assert recons_params is not None
        # first tab 'calculation widget'
        self._calculationWidget = CalculationWidget(
            parent=self, axis_params=recons_params
        )

        # second tab: options
        self._optionsWidget = AxisOptionsWidget(parent=self, axis_params=recons_params)
        self._inputWidget = InputWidget(parent=self, axis_params=recons_params)

        for widget in self._calculationWidget, self._optionsWidget:
            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
            widget.layout().addWidget(spacer)

        self.addTab(self._calculationWidget, "calculation")
        self.addTab(self._optionsWidget, "options")
        # simplify set up. Hide options
        self.addTab(self._inputWidget, "input")

        # set up
        self.setAxisParams(recons_params)
        self._updatePossibleInput()

        # connect signal / slot
        self._calculationWidget.sigLockModeChanged.connect(self.sigLockModeChanged)
        self.sigModeChanged.connect(self._updatePossibleInput)
        self.sigModeChanged.connect(self._updatePossibleOptions)
        self._inputWidget._sigUrlChanged.connect(self._urlChanged)
        self._calculationWidget.sigModeChanged.connect(self.sigModeChanged)
        self._calculationWidget.sigUpdateXRotAxisPixelPosOnNewScan.connect(
            self.sigUpdateXRotAxisPixelPosOnNewScan
        )

    def _urlChanged(self):
        self.sigUrlChanged.emit()

    def setScan(self, scan):
        if scan is not None:
            self._calculationWidget.setScan(scan)
            self._inputWidget.setScan(scan)

    def setAxisParams(self, axis):
        with block_signals(self):
            self._calculationWidget.setAxisParams(axis)
            self._optionsWidget.setAxisParams(axis)
            self._inputWidget.setAxisParams(axis)

    def _updatePossibleInput(self):
        """Update Input tab according to the current mode"""
        current_mode = self.getMode()
        valid_inputs = axis_mode.AXIS_MODE_METADATAS[current_mode].valid_inputs
        if valid_inputs is None:
            self._inputWidget.setEnabled(False)
        else:
            self._inputWidget.setEnabled(True)
            self._inputWidget.setValidInputs(valid_inputs)

    def _updatePossibleOptions(self):
        mode = self.getMode()
        self._optionsWidget.setMode(mode)

    # expose API
    def isModeLock(self) -> bool:
        return self._calculationWidget.isModeLock()

    def setModeLock(self, mode):
        self._calculationWidget.setModeLock(mode=mode)

    def setEstimatedCorValue(self, value):
        self._calculationWidget.setEstimatedCorValue(value=value)

    def getEstimatedCor(self):
        return self._calculationWidget.getEstimatedCor()

    def updateXRotationAxisPixelPositionOnNewScan(self) -> bool:
        return self._calculationWidget.updateXRotationAxisPixelPositionOnNewScan()

    def setUpdateXRotationAxisPixelPositionOnNewScan(self, update: bool):
        self._calculationWidget.setUpdateXRotationAxisPixelPositionOnNewScan(
            update=update
        )

    def getMode(self):
        """Return algorithm to use for axis calculation"""
        return self._calculationWidget.getMode()

    def isYAxisInverted(self) -> bool:
        return self._calculationWidget._estimatedCorWidget.isYAxisInverted()

    def setYAxisInverted(self, checked: bool):
        return self._calculationWidget._estimatedCorWidget.setYAxisInverted(
            checked=checked
        )


class _ShiftControl(qt.QWidget):
    """
    Widget to control the shift step we want to apply
    """

    sigShiftLeft = qt.Signal()
    """Signal emitted when the left button is activated"""
    sigShiftRight = qt.Signal()
    """Signal emitted when the right button is activated"""
    sigShiftTop = qt.Signal()
    """Signal emitted when the top button is activated"""
    sigShiftBottom = qt.Signal()
    """Signal emitted when the bottom button is activated"""
    sigReset = qt.Signal()
    """Signal emitted when the reset button is activated"""
    sigAuto = qt.Signal()
    """Signal emitted when the auto button is activated"""
    sigShiftChanged = qt.Signal(float, float)
    """Signal emitted ony when xLE and yLE edition is finished"""

    def __init__(self, parent, shift_mode: ShiftMode):
        """

        :param parent: qt.QWidget
        :param shift_mode: what are the shift we want to control
        """
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._leftButton = qt.QPushButton("left", parent=self)
        self.layout().addWidget(self._leftButton, 1, 0)

        self._rightButton = qt.QPushButton("right", parent=self)
        self.layout().addWidget(self._rightButton, 1, 3)

        self._shiftInfo = _ShiftInformation(parent=self)
        self.layout().addWidget(self._shiftInfo, 1, 1)
        self._shiftInfo._updateShiftInfo(x=0.0, y=0.0)

        self._topButton = qt.QPushButton("top", parent=self)
        self.layout().addWidget(self._topButton, 0, 1)

        self._bottomButton = qt.QPushButton("bottom", parent=self)
        self.layout().addWidget(self._bottomButton, 2, 1)

        self._resetButton = qt.QPushButton("reset", parent=self)
        self.layout().addWidget(self._resetButton, 3, 2, 3, 4)

        self._autoButton = qt.QPushButton("auto", parent=self)
        self.layout().addWidget(self._autoButton, 3, 0, 3, 2)
        self._autoButton.hide()

        # Signal / Slot connection
        self._leftButton.pressed.connect(self.sigShiftLeft.emit)
        self._rightButton.pressed.connect(self.sigShiftRight.emit)
        self._topButton.pressed.connect(self.sigShiftTop.emit)
        self._bottomButton.pressed.connect(self.sigShiftBottom.emit)
        self._resetButton.pressed.connect(self.sigReset.emit)
        self._autoButton.pressed.connect(self.sigAuto.emit)
        self._shiftInfo.sigShiftChanged.connect(self.sigShiftChanged.emit)

        # expose API
        self._updateShiftInfo = self._shiftInfo._updateShiftInfo

        self.setShiftMode(shift_mode)

    def setShiftMode(self, shift_mode):
        show_x_shift = shift_mode in (ShiftMode.x_only, ShiftMode.x_and_y)
        show_y_shift = shift_mode in (ShiftMode.y_only, ShiftMode.x_and_y)
        self._leftButton.setVisible(show_x_shift)
        self._rightButton.setVisible(show_x_shift)
        self._topButton.setVisible(show_y_shift)
        self._bottomButton.setVisible(show_y_shift)
        self._shiftInfo._xLE.setVisible(show_x_shift)
        self._shiftInfo._xLabel.setVisible(show_x_shift)
        self._shiftInfo._yLE.setVisible(show_y_shift)
        self._shiftInfo._yLabel.setVisible(show_y_shift)


class _ImgOpts(qt.QGroupBox):
    sigSubSamplingChanged = qt.Signal()
    """Signal emitted when the sub sampling change"""

    def __init__(self, parent, title="Image Option"):
        super().__init__(title, parent)
        self.setLayout(qt.QFormLayout())
        self._subSamplingQSpinBox = qt.QSpinBox(self)
        self.layout().addRow("sub-sampling:", self._subSamplingQSpinBox)
        self._subSamplingQSpinBox.setMinimum(1)

        # set up
        self._subSamplingQSpinBox.setValue(1)

        # connect signal / slot
        self._subSamplingQSpinBox.valueChanged.connect(self._subSamplingChanged)

    def _subSamplingChanged(self):
        self.sigSubSamplingChanged.emit()

    def getSubSampling(self):
        return self._subSamplingQSpinBox.value()

    def setSubSampling(self, value):
        return self._subSamplingQSpinBox.setValue(int(value))


class _ShiftInformation(qt.QWidget):
    """
    Widget displaying information about the current x and y shift.
    Both x shift and y shift are editable.
    """

    class _ShiftLineEdit(qt.QLineEdit):
        def __init__(self, *args, **kwargs):
            qt.QLineEdit.__init__(self, *args, **kwargs)
            self._defaultBackgroundColor = None
            # validator
            validator = qt.QDoubleValidator(parent=self, decimals=2)
            self.setValidator(validator)
            self._getDefaultBackgroundColor()
            # connect signal / slot
            self.textEdited.connect(self._userEditing)
            self.editingFinished.connect(self._userEndEditing)

        def sizeHint(self):
            return qt.QSize(40, 10)

        def _getDefaultBackgroundColor(self):
            if self._defaultBackgroundColor is None:
                self._defaultBackgroundColor = self.palette().color(
                    self.backgroundRole()
                )
            return self._defaultBackgroundColor

        def _userEditing(self, *args, **kwargs):
            palette = self.palette()
            palette.setColor(self.backgroundRole(), EDITING_BACKGROUND_COLOR)
            self.setPalette(palette)

        def _userEndEditing(self, *args, **kwargs):
            palette = self.palette()
            palette.setColor(
                self.backgroundRole(),
                self._getDefaultBackgroundColor(),
            )
            self.setPalette(palette)

    sigShiftChanged = qt.Signal(float, float)
    """Signal emitted ony when xLE and yLE edition is finished"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self._xLabel = qt.QLabel("x=", parent=self)
        self.layout().addWidget(self._xLabel)
        self._xLE = _ShiftInformation._ShiftLineEdit("", parent=self)
        self.layout().addWidget(self._xLE)

        self._yLabel = qt.QLabel("y=", parent=self)
        self.layout().addWidget(self._yLabel)
        self._yLE = _ShiftInformation._ShiftLineEdit("", parent=self)
        self.layout().addWidget(self._yLE)

        # connect Signal / Slot
        self._xLE.editingFinished.connect(self._shiftChanged)
        self._yLE.editingFinished.connect(self._shiftChanged)

    def _updateShiftInfo(self, x, y):
        with block_signals(self):
            if x is None:
                x = 0.0
            if y is None:
                y = 0.0
            x_text = x
            if x_text != "...":
                x_text = "%.1f" % float(x)
            y_text = y
            if y_text != "...":
                y_text = "%.1f" % float(y)
            self._xLE.setText(x_text)
            self._yLE.setText(y_text)

    def _shiftChanged(self, *args, **kwargs):
        self.sigShiftChanged.emit(float(self._xLE.text()), float(self._yLE.text()))
