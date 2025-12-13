from __future__ import annotations

from tomwer.io.utils.utils import str_to_dict

from nabu.stitching import config as stitching_config
from nabu.stitching.overlap import OverlapStitchingStrategy
from silx.gui import qt
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel as QComboBox
from tomwer.gui.utils.scrollarea import QSpinBoxIgnoreWheel as QSpinBox
from ..singleaxis import _SingleAxisMixIn


class _StitchingHeightSpinBox(qt.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())
        self._autoCB = qt.QCheckBox("max", self)
        self.layout().addWidget(self._autoCB)
        self._stitchingHeight = QSpinBox(self)
        self._stitchingHeight.setMinimum(3)
        self._stitchingHeight.setMaximum(999999)
        self._stitchingHeight.setValue(40)
        self._stitchingHeight.setSuffix("px")
        self.layout().addWidget(self._stitchingHeight)

        self._autoCB.toggled.connect(self._stitchingHeight.setDisabled)

    def getStitchingHeight(self) -> int | None:
        if self._autoCB.isChecked():
            return None
        else:
            return self._stitchingHeight.value()

    def setStitchingHeight(self, height: int | None) -> None:
        self._autoCB.setChecked(height is None)
        if height is not None:
            self._stitchingHeight.setValue(int(height))


class StitchingStrategies(qt.QWidget, _SingleAxisMixIn):
    """
    Defines algorithm and strategies to be used
    """

    DEFAULT_STITCHING_HEIGHT = None  # max value is the default

    sigChanged = qt.Signal()
    """emit when strategy change"""

    def __init__(self, axis: int, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QFormLayout())
        self._stitchingStrategyCG = QComboBox(parent=self)
        for strategy in OverlapStitchingStrategy:
            self._stitchingStrategyCG.addItem(strategy.value)
        self._stitchingStrategyCG.setToolTip(
            "stitcher behavior is also know as stitching strategy. It define the behavior to have on overlaping areas"
        )
        self.layout().addRow("stitcher behavior", self._stitchingStrategyCG)
        self._axis = axis  # needed to implement the _SingleAxisMixIn interface

        self._stitchingHeight = _StitchingHeightSpinBox(parent=self)
        self._stitchingHeight.setStitchingHeight(self.DEFAULT_STITCHING_HEIGHT)
        self.layout().addRow("stitching height", self._stitchingHeight)

        # set up
        idx = self._stitchingStrategyCG.findText(
            OverlapStitchingStrategy.COSINUS_WEIGHTS.value
        )
        self._stitchingStrategyCG.setCurrentIndex(idx)

        # connect signal / slot
        self._stitchingStrategyCG.currentIndexChanged.connect(self._changed)

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def getStitchingStrategy(self) -> OverlapStitchingStrategy:
        return OverlapStitchingStrategy(self._stitchingStrategyCG.currentText())

    def setStitchingStrategy(self, strategy: OverlapStitchingStrategy | str):
        strategy = OverlapStitchingStrategy(strategy)
        idx = self._stitchingStrategyCG.findText(strategy.value)
        if idx >= 0:
            self._stitchingStrategyCG.setCurrentIndex(idx)

    def getConfiguration(self) -> dict:
        overlap_size = self._stitchingHeight.getStitchingHeight()
        if overlap_size is None:
            overlap_size = ""
        return {
            stitching_config.STITCHING_SECTION: {
                stitching_config.STITCHING_STRATEGY_FIELD: self.getStitchingStrategy().value,
                f"axis_{self.first_axis}_params": f"overlap_size={overlap_size}",
            }
        }

    def setConfiguration(self, config: dict):
        strategy = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.STITCHING_SECTION, None
        )
        if strategy is not None:
            self.setStitchingStrategy(strategy=strategy)

        first_axis_params_dict = str_to_dict(
            config.get(stitching_config.STITCHING_SECTION, {}).get(
                f"axis_{self._axis}_params", ""
            )
        )
        stitching_height = first_axis_params_dict.get(
            stitching_config.KEY_OVERLAP_SIZE, "unknown"
        )
        if stitching_height in ("None", "", None):
            self._stitchingHeight.setStitchingHeight(None)
        elif stitching_height != "unknown":
            self._stitchingHeight.setStitchingHeight(stitching_height)
