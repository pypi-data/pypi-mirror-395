from __future__ import annotations

from silx.gui import qt

from tomwer.core.process.reconstruction.axis.mode import AxisMode, AXIS_MODE_METADATAS
from tomwer.synctools.axis import QAxisRP
from tomwer.core.process.reconstruction.axis.params import AxisCalculationInput
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel, QSpinBoxIgnoreWheel
from tomwer.core.process.reconstruction.axis.params import (
    DEFAULT_CMP_N_SUBSAMPLING_Y,
    DEFAULT_CMP_OVERSAMPLING,
    DEFAULT_CMP_TAKE_LOG,
    DEFAULT_CMP_THETA,
)


class AxisOptionsWidget(qt.QWidget):
    """
    GUI to define (advanced) option of the AxisTask

    Used as a tab of the AxisSettingsTabWidget
    """

    sigChanged = qt.Signal()
    """Emit when the options changed"""

    def __init__(self, parent, axis_params):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis_params, QAxisRP)
        self._axis_params = axis_params
        self.setLayout(qt.QVBoxLayout())

        # cor_options
        self._corOptsWidget = qt.QWidget(self)
        self._corOptsWidget.setLayout(qt.QFormLayout())
        self._corOpts = qt.QLineEdit(self)
        self._corOpts.setToolTip(
            "Options for methods finding automatically the rotation axis position. 'side', 'near_pos' and 'near_width' are already provided by dedicated interface. The parameters are separated by commas and passed as 'name=value'. Mind the semicolon separator (;)."
        )
        self._corOpts.setPlaceholderText("low_pass=1; high_pass=20")
        self._corOptsWidget.layout().addRow("cor advanced options", self._corOpts)
        self.layout().addWidget(self._corOptsWidget)

        # padding option
        self._padding_widget = qt.QGroupBox("padding mode")
        self._padding_widget.setCheckable(True)
        self.layout().addWidget(self._padding_widget)
        self._padding_widget.setLayout(qt.QHBoxLayout())

        self._qbPaddingMode = QComboBoxIgnoreWheel(self._padding_widget)
        for _mode in (
            "constant",
            "edge",
            "linear_ramp",
            "maximum",
            "mean",
            "median",
            "minimum",
            "reflect",
            "symmetric",
            "wrap",
        ):
            self._qbPaddingMode.addItem(_mode)
        def_index = self._qbPaddingMode.findText("edge")
        self._qbPaddingMode.setCurrentIndex(def_index)
        self._padding_widget.layout().addWidget(self._qbPaddingMode)

        # define common options
        self._commonOpts = qt.QWidget(parent=self)
        self._commonOpts.setLayout(qt.QFormLayout())

        self._qcbDataMode = qt.QComboBox(parent=self)
        for data_mode in AxisCalculationInput:
            # paganin is not managed for sinogram
            self._qcbDataMode.addItem(data_mode.name(), data_mode)
        self._qcbDataMode.hide()

        self.layout().addWidget(self._commonOpts)

        # composite method advanced options
        self._compositeOptsGroup = CompositeOptsGroup(
            parent=self, axis_params=axis_params
        )
        self.layout().addWidget(self._compositeOptsGroup)

        # set up
        self.setCalculationInputType(self._axis_params.calculation_input_type)
        self._compositeOptsGroup.setVisible(
            self._axis_params.mode in (AxisMode.near, AxisMode.composite_coarse_to_fine)
        )

        # connect signal / slot
        self._corOpts.editingFinished.connect(self._updateAdvancedCorOptions)
        self._qcbDataMode.currentIndexChanged.connect(self._updateInputType)
        self._axis_params.sigChanged.connect(self._axis_params_changed)
        self._qbPaddingMode.currentIndexChanged.connect(self._paddingModeChanged)
        self._padding_widget.toggled.connect(self._paddingModeChanged)
        self._compositeOptsGroup.sigChanged.connect(self.sigChanged)

    def _axis_params_changed(self):
        with block_signals(self):
            # update according to AxisCalculationInput
            index = self._qcbDataMode.findText(
                self._axis_params.calculation_input_type.name()
            )
            if index >= 0:
                self._qcbDataMode.setCurrentIndex(index)
            # update advanced cor options visibility (not relevant if mode is manual or read)
            axis_mode = self._axis_params.mode
            self._corOptsWidget.setVisible(
                axis_mode
                not in (
                    AxisMode.manual,
                    AxisMode.read,
                )
            )
            # update cor options value
            self.setCorOptions(self._axis_params.extra_cor_options)
            self.setPaddingMode(self._axis_params.padding_mode)
            self._padding_widget.setVisible(
                AXIS_MODE_METADATAS[axis_mode].allows_padding
            )

    def _updateInputType(self, *arg, **kwargs):
        self._axis_params.calculation_input_type = self.getCalculationInputType()
        self.sigChanged.emit()

    def _paddingModeChanged(self, *args, **kwargs):
        self._axis_params.padding_mode = self.getPaddingMode()
        self.sigChanged.emit()

    def getPaddingMode(self):
        if self._padding_widget.isChecked():
            return self._qbPaddingMode.currentText()
        else:
            return None

    def setPaddingMode(self, mode):
        index = self._qbPaddingMode.findText(mode)
        if index >= 0:
            self._qbPaddingMode.setCurrentIndex(index)
        self._paddingModeChanged()

    def _updateAdvancedCorOptions(self, *args, **kwargs):
        self._axis_params.extra_cor_options = self.getCorOptions()
        self.sigChanged.emit()

    def getCalculationInputType(self, *arg, **kwargs):
        return AxisCalculationInput.from_value(self._qcbDataMode.currentText())

    def setCalculationInputType(self, calculation_type):
        calculation_type = AxisCalculationInput.from_value(calculation_type)
        index_dm = self._qcbDataMode.findText(calculation_type.name())
        self._qcbDataMode.setCurrentIndex(index_dm)

    def setAxisParams(self, axis):
        self._axis_params = axis
        with block_signals(self):
            index = self._qcbDataMode.findText(axis.calculation_input_type.name())
            self._qcbDataMode.setCurrentIndex(index)
            self._compositeOptsGroup.setAxisParams(axis)

    def getCorOptions(self):
        return self._corOpts.text()

    def setCorOptions(self, opts: str | None):
        with block_signals(self._axis_params):
            self._corOpts.clear()
            if opts:
                self._corOpts.setText(opts)
                self._updateAdvancedCorOptions()

    def setMode(self, mode: AxisMode):
        composite_opts_visible = AxisMode.from_value(mode) in (
            AxisMode.composite_coarse_to_fine,
            AxisMode.near,
        )
        self._compositeOptsGroup.setVisible(composite_opts_visible)


class CompositeOptsGroup(qt.QGroupBox):
    """Group box dedicated to the composite algorithms"""

    sigChanged = qt.Signal()
    """Emit when the options changed"""

    def __init__(self, title="composite options", parent=None, axis_params=None):
        self._axis_params = axis_params
        super().__init__(title, parent)
        ## options for the composite mode
        self.setLayout(qt.QFormLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._thetaSB = QSpinBoxIgnoreWheel(self)
        self._thetaSB.setRange(0, 360)
        self._thetaSB.setValue(DEFAULT_CMP_THETA)
        self._thetaSB.setToolTip("a radio will be picked each theta degrees")
        self._thetaLabel = qt.QLabel("angle interval (in degree)", self)
        self._thetaLabel.setToolTip(
            "algorithm will take one projection each 'angle interval'. Also know as 'theta'"
        )
        self.layout().addRow(self._thetaLabel, self._thetaSB)

        self._oversamplingSB = QSpinBoxIgnoreWheel(self)
        self._oversamplingSB.setRange(1, 999999)
        self._oversamplingSB.setValue(DEFAULT_CMP_OVERSAMPLING)
        self._oversamplingSB.setToolTip("sinogram oversampling")
        self.layout().addRow("oversampling", self._oversamplingSB)

        self._nearWidthSB = QSpinBoxIgnoreWheel(self)
        self._nearWidthSB.setRange(1, 999999)
        self._nearWidthSB.setValue(0)
        self._nearWidthSB.setToolTip("position to be used with near option")
        self._nearWidthLabel = qt.QLabel("near width", self)
        self._nearWidthLabel.setToolTip("position to be used with near option")
        self.layout().addRow(self._nearWidthLabel, self._nearWidthSB)

        self._subsamplingYSB = QSpinBoxIgnoreWheel(self)
        self._subsamplingYSB.setRange(1, 999999)
        self._subsamplingYSB.setValue(DEFAULT_CMP_N_SUBSAMPLING_Y)
        self._subsamplingYSB.setToolTip("sinogram number of subsampling along y")
        self.layout().addRow("n_subsampling_y", self._subsamplingYSB)

        self._takeLogCB = qt.QCheckBox(self)
        self._takeLogCB.setToolTip("Take logarithm")
        self._takeLogCB.setChecked(DEFAULT_CMP_TAKE_LOG)
        self._takeTheLogLabel = qt.QLabel("linearisation (-log(I/I0))")
        self._takeTheLogLabel.setToolTip(
            "take (-log(I/I0)) as input. Also know as 'take_log' option"
        )
        self.layout().addRow(self._takeTheLogLabel, self._takeLogCB)

        # connect signal / slot
        self._thetaSB.valueChanged.connect(self._changed)
        self._oversamplingSB.valueChanged.connect(self._changed)
        self._subsamplingYSB.valueChanged.connect(self._changed)
        self._nearWidthSB.valueChanged.connect(self._changed)
        self._takeLogCB.toggled.connect(self._changed)

    def setAxisParams(self, axis_params):
        with block_signals(self):
            self.setConfiguration(axis_params.composite_options)
        self._axis_params = axis_params

    def _changed(self):
        if self._axis_params is not None:
            self._axis_params.composite_options = self.getConfiguration()
        self.sigChanged.emit()

    def getTheta(self) -> int:
        return self._thetaSB.value()

    def setTheta(self, theta: int) -> None:
        self._thetaSB.setValue(theta)

    def getOversampling(self) -> int:
        return self._oversamplingSB.value()

    def setOversampling(self, oversampling: int) -> None:
        self._oversamplingSB.setValue(oversampling)

    def getNearWidth(self) -> int:
        return self._nearWidthSB.value()

    def setNearWidth(self, value) -> int:
        return self._nearWidthSB.setValue(value)

    def getSubSamplingY(self) -> int:
        return self._subsamplingYSB.value()

    def setSubSamplingY(self, subsampling: int) -> None:
        self._subsamplingYSB.setValue(subsampling)

    def getTakeLog(self) -> bool:
        return self._takeLogCB.isChecked()

    def setTakeLog(self, log: bool) -> None:
        self._takeLogCB.setChecked(log)

    def getConfiguration(self) -> dict:

        return {
            "theta": self.getTheta(),
            "oversampling": self.getOversampling(),
            "n_subsampling_y": self.getSubSamplingY(),
            "take_log": self.getTakeLog(),
            "near_width": self.getNearWidth(),
        }

    def setConfiguration(self, opts: dict) -> None:
        if not isinstance(opts, dict):
            raise TypeError("opts should be an instance of dict")
        # theta
        theta = opts.get("theta", None)
        if theta is not None:
            self.setTheta(theta=theta)
        # oversampling
        oversampling = opts.get("oversampling", None)
        if oversampling is not None:
            self.setOversampling(oversampling)
        # n subsampling y
        n_subsampling_y = opts.get("n_subsampling_y", None)
        if n_subsampling_y is not None:
            self.setSubSamplingY(n_subsampling_y)
        # near_width
        near_width = opts.get("near_width", None)
        if near_width is not None:
            self.setNearWidth(near_width)
        # take log
        take_log = opts.get("take_log", None)
        if take_log is not None:
            self.setTakeLog(take_log)
