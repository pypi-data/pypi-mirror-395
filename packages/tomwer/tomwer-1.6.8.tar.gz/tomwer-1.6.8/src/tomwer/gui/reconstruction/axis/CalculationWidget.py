from __future__ import annotations

import logging

from silx.gui import qt

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.process.reconstruction.axis import mode as axis_mode
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.synctools.axis import QAxisRP
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel
from tomwer.gui.reconstruction.axis.EstimatedCORWidget import EstimatedCORWidget

_logger = logging.getLogger(__name__)


class CalculationWidget(qt.QWidget):
    """
    Main widget to select the algorithm to use for COR calculation
    Used as a tab of the AxisSettingsTabWidget
    """

    sigModeChanged = qt.Signal(str)
    """signal emitted when the algorithm for computing COR changed"""

    sigLockModeChanged = qt.Signal(bool)
    """signal emitted when the mode has been lock or unlock"""
    sigUpdateXRotAxisPixelPosOnNewScan = qt.Signal()
    sigYAxisInvertedChanged = qt.Signal(bool)

    def __init__(self, parent, axis_params):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self._axis_params = None
        self.setLayout(qt.QVBoxLayout())

        # algorithm
        self._modeWidget = qt.QWidget(parent=self)
        self._modeWidget.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._modeWidget)

        self.__rotAxisSelLabel = qt.QLabel("algorithm to compute cor")
        self._modeWidget.layout().addWidget(self.__rotAxisSelLabel)
        self._qcbPosition = QComboBoxIgnoreWheel(self)

        algorithm_groups = (
            # radio group
            (
                axis_mode.AxisMode.centered,
                axis_mode.AxisMode.global_,
                axis_mode.AxisMode.growing_window_radios,
                axis_mode.AxisMode.sliding_window_radios,
                axis_mode.AxisMode.octave_accurate_radios,
            ),
            # sino group
            (
                axis_mode.AxisMode.growing_window_sinogram,
                axis_mode.AxisMode.sino_coarse_to_fine,
                axis_mode.AxisMode.sliding_window_sinogram,
                axis_mode.AxisMode.fourier_angles,
            ),
            # composite coarse to fine
            (
                axis_mode.AxisMode.composite_coarse_to_fine,
                axis_mode.AxisMode.near,
            ),
            # read
            (axis_mode.AxisMode.read,),
            # manual
            (axis_mode.AxisMode.manual,),
        )
        current_pos = 0
        for i_grp, algorithm_group in enumerate(algorithm_groups):
            if i_grp != 0:
                self._qcbPosition.insertSeparator(current_pos)
                current_pos += 1
            for cor_algorithm in algorithm_group:
                self._qcbPosition.addItem(cor_algorithm.value)
                idx = self._qcbPosition.findText(cor_algorithm.value)
                self._qcbPosition.setItemData(
                    idx,
                    axis_mode.AXIS_MODE_METADATAS[cor_algorithm].tooltip,
                    qt.Qt.ToolTipRole,
                )
                current_pos += 1

        self._modeWidget.layout().addWidget(self._qcbPosition)

        # method lock button
        self._lockMethodPB = PadlockButton(parent=self._modeWidget)
        self._lockMethodPB.setToolTip(
            "Lock the method to compute the cor. \n"
            "This will automatically call the "
            "defined algorithm each time a scan is received."
        )
        self._modeWidget.layout().addWidget(self._lockMethodPB)

        # estimated cor
        self._estimatedCorWidget = EstimatedCORWidget(self, axis_params=axis_params)
        self.layout().addWidget(self._estimatedCorWidget)

        # connect signal / slot
        self._qcbPosition.currentIndexChanged.connect(self._modeChanged)
        self._lockMethodPB.sigLockChanged.connect(self.lockMode)
        self._estimatedCorWidget.sigUpdateXRotAxisPixelPosOnNewScan.connect(
            self.sigUpdateXRotAxisPixelPosOnNewScan
        )
        self._estimatedCorWidget.sigYAxisInvertedChanged.connect(
            self.sigYAxisInvertedChanged
        )

        # set up interface
        self._estimatedCorWidget._updateVisibleSides(mode=self.getMode())
        self.setAxisParams(axis_params)

    def getMethodLockPB(self) -> qt.QPushButton:
        return self._lockMethodPB

    def setEstimatedCorValue(self, value):
        self._estimatedCorWidget.setEstimatedCor(value=value)
        # note: force to update the side values.
        self._estimatedCorWidget._updateVisibleSides(mode=self.getMode())

    def getEstimatedCor(self):
        return self._estimatedCorWidget.getEstimatedCor()

    def updateXRotationAxisPixelPositionOnNewScan(self) -> bool:
        return self._estimatedCorWidget.updateXRotationAxisPixelPositionOnNewScan()

    def setUpdateXRotationAxisPixelPositionOnNewScan(self, update: bool):
        self._estimatedCorWidget.setUpdateXRotationAxisPixelPositionOnNewScan(
            update=update
        )

    def _modeChanged(self, *args, **kwargs):
        mode = self.getMode()
        with block_signals(self._qcbPosition):
            with block_signals(self._axis_params):
                self._estimatedCorWidget._updateVisibleSides(mode)
                self._axis_params.mode = mode.value
            self._axis_params.changed()
            self.sigModeChanged.emit(mode.value)

    def isModeLock(self):
        return self._lockMethodPB.isLocked()

    def setModeLock(self, mode=None):
        """set a specific mode and lock it.

        :param mode: mode to lock. If None then keep the current mode
        """
        if mode is not None:
            mode = axis_mode.AxisMode.from_value(mode)
        if mode is None and axis_mode.AXIS_MODE_METADATAS[self.getMode()].is_lockable():
            raise ValueError(
                "Unable to lock the current mode is not an automatic algorithm"
            )
        elif (
            mode != self.getMode() and axis_mode.AXIS_MODE_METADATAS[mode].is_lockable()
        ):
            raise ValueError("Unable to lock %s this is not a lockable mode")

        if mode is not None:
            self.setMode(mode)
        if not self._lockMethodPB.isLocked():
            with block_signals(self._lockMethodPB):
                self._lockMethodPB.setLock(True)
        self.lockMode(True)

    def lockMode(self, lock):
        with block_signals(self._lockMethodPB):
            self._lockMethodPB.setLock(lock)
            self._qcbPosition.setEnabled(not lock)

        self.sigLockModeChanged.emit(lock)

    def getMode(self):
        """Return algorithm to use for axis calculation"""
        return axis_mode.AxisMode.from_value(self._qcbPosition.currentText())

    def setMode(self, mode: axis_mode.AxisMode):
        with block_signals(self._qcbPosition):
            index = self._qcbPosition.findText(mode.value)
            if index >= 0:
                self._qcbPosition.setCurrentIndex(index)
            else:
                raise ValueError("Unable to find mode", mode)
            self._lockMethodPB.setVisible(mode not in (axis_mode.AxisMode.manual,))
            mode_metadata = axis_mode.AXIS_MODE_METADATAS[mode]
            estimated_cor_widget_visible = (
                mode_metadata.allows_estimated_cor_as_numerical_value
                or len(mode_metadata.valid_sides) > 0
            )
            self._estimatedCorWidget.setVisible(estimated_cor_widget_visible)
            self._estimatedCorWidget._updateVisibleSides(mode=mode)

    def setAxisParams(self, axis):
        with block_signals(self):
            if self._axis_params is not None:
                self._axis_params.sigChanged.disconnect(self._axis_params_changed)
            self._axis_params = axis
            if self._axis_params.mode in (axis_mode.AxisMode.manual,):
                # those mode cannot be handled by the auto calculation dialog
                self._axis_params.mode = axis_mode.AxisMode.growing_window_radios
            self._axis_params.sigChanged.connect(self._axis_params_changed)
            self._axis_params_changed()

    def _axis_params_changed(self, *args, **kwargs):
        if self._axis_params.mode != self.getMode():
            # setMode will force to update visible side. So avoid to reset it if not necessary
            self.setMode(self._axis_params.mode)

    def setScan(self, scan: TomwerScanBase | None):
        self._estimatedCorWidget.setPixelSize(pixel_size_m=scan.sample_x_pixel_size)
        self._estimatedCorWidget.setImageWidth(image_width=scan.dim_1)
