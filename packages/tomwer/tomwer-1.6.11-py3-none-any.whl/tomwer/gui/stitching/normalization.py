from __future__ import annotations
from silx.gui import qt
from nabu.stitching.sample_normalization import (
    SampleSide as _SampleSide,
    Method as _SampleNormalizationMethod,
)
from nabu.stitching import config as _config_stitching
from tomwer.gui.utils.qt_utils import block_signals


class NormalizationBySampleGroupBox(qt.QGroupBox):
    """
    Widget to define the normalization to apply to frames"""

    sigConfigChanged = qt.Signal()
    """Emit when the configuration is changed"""

    def __init__(self, title: str = "normalization by sample", parent=None):
        # FIXME: add a way to the user for requesting a view of the region picked ???
        super().__init__(title, parent)
        self.setCheckable(True)
        self.setLayout(qt.QFormLayout())

        # method
        self._methodCB = qt.QComboBox(self)
        self._methodCB.addItems([item.value for item in _SampleNormalizationMethod])
        self._methodCB.setCurrentText(_SampleNormalizationMethod.MEDIAN.value)
        self.layout().addRow("method", self._methodCB)

        # side
        self._sideCB = qt.QComboBox(self)
        self._sideCB.addItems([item.value for item in _SampleSide])
        self._sideCB.setCurrentText(_SampleSide.LEFT.value)
        self.layout().addRow("sampling side", self._sideCB)

        # width
        self._widthSB = qt.QSpinBox(self)
        self._widthSB.setRange(1, 9999999)
        self._widthSB.setValue(30)
        self._widthSB.setSingleStep(10)
        self._widthSB.setSuffix("px")
        self.layout().addRow("sampling width", self._widthSB)

        # margin
        self._marginSB = qt.QSpinBox(self)
        self._marginSB.setRange(0, 999999)
        self._marginSB.setValue(0)
        self.layout().addRow("sampling margin", self._marginSB)

        # connect signal / slot
        self._methodCB.currentIndexChanged.connect(self._configChanged)
        self._sideCB.currentIndexChanged.connect(self._configChanged)
        self._widthSB.valueChanged.connect(self._configChanged)
        self._marginSB.valueChanged.connect(self._configChanged)

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getMethod(self) -> _SampleNormalizationMethod:
        return _SampleNormalizationMethod(self._methodCB.currentText())

    def setMethod(self, method: _SampleNormalizationMethod | str):
        method = _SampleNormalizationMethod(method)
        self._methodCB.setCurrentText(method.value)

    def getSide(self) -> _SampleSide:
        return _SampleSide(self._sideCB.currentText())

    def setSide(self, side: _SampleSide):
        side = _SampleSide(side)
        self._sideCB.setCurrentText(side.value)

    def getMargin(self) -> int:
        return self._marginSB.value()

    def setMargin(self, margin: int):
        self._marginSB.setValue(int(margin))

    def getWidth(self) -> int:
        return self._widthSB.value()

    def setWidth(self, width: int):
        self._widthSB.setValue(int(width))

    def getConfiguration(self) -> dict:
        return {
            _config_stitching.NORMALIZATION_BY_SAMPLE_ACTIVE_FIELD: self.isChecked(),
            _config_stitching.NORMALIZATION_BY_SAMPLE_METHOD: self.getMethod().value,
            _config_stitching.NORMALIZATION_BY_SAMPLE_SIDE: self.getSide().value,
            _config_stitching.NORMALIZATION_BY_SAMPLE_MARGIN: self.getMargin(),
            _config_stitching.NORMALIZATION_BY_SAMPLE_WIDTH: self.getWidth(),
        }

    def setConfiguration(self, config: dict) -> None:
        with block_signals(self):
            method = config.get(_config_stitching.NORMALIZATION_BY_SAMPLE_METHOD, None)
            if method is not None:
                self.setMethod(method=method)

            side = config.get(_config_stitching.NORMALIZATION_BY_SAMPLE_SIDE, None)
            if side is not None:
                self.setSide(side=side)

            margin = config.get(_config_stitching.NORMALIZATION_BY_SAMPLE_MARGIN, None)
            if margin is not None:
                self.setMargin(margin=margin)

            width = config.get(_config_stitching.NORMALIZATION_BY_SAMPLE_WIDTH, None)
            if width is not None:
                self.setWidth(width=width)

            active = config.get(
                _config_stitching.NORMALIZATION_BY_SAMPLE_ACTIVE_FIELD, None
            )
            if active is not None:
                self.setChecked(active in (True, 1, "1", "True"))

        self._configChanged()
