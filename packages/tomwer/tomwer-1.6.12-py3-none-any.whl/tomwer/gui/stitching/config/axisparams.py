from __future__ import annotations

import logging

from nabu.stitching import config as stitching_config
from nabu.stitching.utils import ShiftAlgorithm as StitchShiftAlgorithm
from silx.gui import qt

from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.configuration.level import ConfigurationLevel
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel as QComboBox
from tomwer.gui.utils.scrollarea import QSpinBoxIgnoreWheel as QSpinBox


_logger = logging.getLogger(__name__)


class StitcherAxisParams(qt.QWidget):
    """
    Widget to define settings of shift search along one axis
    """

    sigConfigChanged = qt.Signal()
    """signal emit when the configuration is updated"""

    DEFAULT_WINDOW_SEARCH_SIZE = 400
    # default window size for shift search

    def __init__(self, axis, parent=None) -> None:
        super().__init__(parent)
        if not isinstance(axis, int):
            raise TypeError("axis is expected to be an int")
        assert axis in (0, 1, 2)
        self._axis = axis
        self.setLayout(qt.QGridLayout())
        self._shiftSearchMethodCB = QComboBox(parent=self)
        # shift algorithm
        shift_search_methods = [
            StitchShiftAlgorithm.NABU_FFT,
            StitchShiftAlgorithm.SKIMAGE,
            StitchShiftAlgorithm.ITK_IMG_REG_V4,
            StitchShiftAlgorithm.NONE,
        ]
        for method in shift_search_methods:
            self._shiftSearchMethodCB.addItem(method.value)
        self._methodLabel = qt.QLabel("shift search method", self)
        self.layout().addWidget(self._methodLabel, 0, 0, 1, 1)
        self.layout().addWidget(self._shiftSearchMethodCB, 0, 1, 1, 1)
        # stitching options
        self._windowSizeLabel = qt.QLabel("window size", self)
        self.layout().addWidget(self._windowSizeLabel, 1, 0, 1, 1)
        self._windowSizeSB = QSpinBox(self)
        self._windowSizeSB.setMinimum(1)
        self._windowSizeSB.setMaximum(9999999)
        self._windowSizeSB.setValue(self.DEFAULT_WINDOW_SEARCH_SIZE)
        self._windowSizeSB.setSuffix("px")
        self.layout().addWidget(self._windowSizeSB, 1, 1, 1, 1)
        tooltip = "size of the window to try to refine shift"
        self._windowSizeLabel.setToolTip(tooltip)
        self._windowSizeSB.setToolTip(tooltip)

        # filter options
        self._filteringGroup = _FilteringGroupBox("filter for shift search", self)
        self._filteringGroup.setCheckable(True)
        self._filteringGroup.setChecked(False)
        self._filteringGroup.setLowPassValue(1)
        self._filteringGroup.setHighPassValue(20)
        self.layout().addWidget(self._filteringGroup, 2, 0, 2, 3)

        # set up
        self._methodChanged()

        # connect signal / slot
        self._shiftSearchMethodCB.currentIndexChanged.connect(self._methodChanged)
        self._windowSizeSB.valueChanged.connect(self._notifyConfigChanged)
        self._filteringGroup.sigValueChanged.connect(self._notifyConfigChanged)

    @property
    def axis(self):
        return self._axis

    def getShiftSearchMethod(self) -> StitchShiftAlgorithm:
        return StitchShiftAlgorithm(self._shiftSearchMethodCB.currentText())

    def setShiftSearchMethod(self, method: StitchShiftAlgorithm | str) -> None:
        method = StitchShiftAlgorithm(method)
        idx = self._shiftSearchMethodCB.findText(method.value)
        self._shiftSearchMethodCB.setCurrentIndex(idx)

    def getConfiguration(self) -> dict:
        method = self.getShiftSearchMethod()
        param_opts = [
            f"{stitching_config.KEY_IMG_REG_METHOD}={method.value}",
            f"{stitching_config.KEY_WINDOW_SIZE}={self._windowSizeSB.value()}",
        ]
        if self._filteringGroup.isChecked():
            param_opts.append(
                f"{stitching_config.KEY_LOW_PASS_FILTER}='{self._filteringGroup.getLowPassValue()}'"
            )
            param_opts.append(
                f"{stitching_config.KEY_HIGH_PASS_FILTER}='{self._filteringGroup.getHighPassValue()}'"
            )

        param_as_str = ";".join(param_opts)
        return {
            stitching_config.STITCHING_SECTION: {
                f"axis_{self.axis}_params": param_as_str,
            },
        }

    def setConfiguration(self, config: dict) -> None:
        with block_signals(self):
            axis_params = config.get(stitching_config.STITCHING_SECTION, {}).get(
                f"axis_{self.axis}_params", ""
            )
            options = filter(
                lambda a: a not in (None, ""), axis_params.replace(",", ";").split(";")
            )
            for option in options:
                clean_option = option.rstrip(" ").lstrip(" ")
                opt_name, opt_value = clean_option.split("=")
                if opt_value == "":
                    continue
                if opt_name == stitching_config.KEY_IMG_REG_METHOD:
                    self.setShiftSearchMethod(opt_value)
                elif opt_name == stitching_config.KEY_WINDOW_SIZE:
                    self._windowSizeSB.setValue(int(opt_value))
                elif opt_name == stitching_config.KEY_LOW_PASS_FILTER:
                    self._filteringGroup.setLowPassValue(int(opt_value))
                    self._filteringGroup.setEnabled(True)
                elif opt_name == stitching_config.KEY_HIGH_PASS_FILTER:
                    self._filteringGroup.setHighPassValue(int(opt_value))
                    self._filteringGroup.setEnabled(True)
                elif opt_name == stitching_config.KEY_OVERLAP_SIZE:
                    pass
                else:
                    _logger.error(f"option {opt_name} is not recognized")
        self._notifyConfigChanged()

    def _methodChanged(self) -> None:
        method = self.getShiftSearchMethod()
        with block_signals(self):
            self._windowSizeSB.setVisible(method is not StitchShiftAlgorithm.NONE)
            self._windowSizeLabel.setVisible(method is not StitchShiftAlgorithm.NONE)
        self._notifyConfigChanged()

    def _notifyConfigChanged(self, *args, **kwargs) -> None:
        self.sigConfigChanged.emit()

    def setConfigurationLevel(self, level: ConfigurationLevel):
        method = self.getShiftSearchMethod()
        self._windowSizeLabel.setVisible(
            level >= ConfigurationLevel.OPTIONAL
            and method is not StitchShiftAlgorithm.NONE
        )
        self._windowSizeSB.setVisible(
            level >= ConfigurationLevel.OPTIONAL
            and method is not StitchShiftAlgorithm.NONE
        )
        self._filteringGroup.setVisible(level >= ConfigurationLevel.ADVANCED)


class _FilteringGroupBox(qt.QGroupBox):
    sigValueChanged = qt.Signal()
    """emit when one of the low or high pass value changed or when toggled"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(qt.QFormLayout())

        self._lowPassFilterSP = QSpinBox(self)
        self.layout().addRow("low pass filter", self._lowPassFilterSP)

        self._highPassFilterSP = QSpinBox(self)
        self.layout().addRow("high pass filter", self._highPassFilterSP)

        # connect signal / slot
        self.toggled.connect(self._updateEnability)
        self.toggled.connect(self._valueChanged)
        self._lowPassFilterSP.editingFinished.connect(self._valueChanged)
        self._highPassFilterSP.editingFinished.connect(self._valueChanged)

    def _updateEnability(self):
        self._lowPassFilterSP.setEnabled(self.isChecked())
        self._highPassFilterSP.setEnabled(self.isChecked())

    def getLowPassValue(self):
        return self._lowPassFilterSP.value()

    def setLowPassValue(self, value):
        self._lowPassFilterSP.setValue(value)

    def getHighPassValue(self):
        return self._highPassFilterSP.value()

    def setHighPassValue(self, value):
        self._highPassFilterSP.setValue(value)

    def _valueChanged(self, *args, **kwargs):
        self.sigValueChanged.emit()
