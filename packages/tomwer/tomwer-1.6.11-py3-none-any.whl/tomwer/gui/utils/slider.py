# coding: utf-8

"""some utils relative to PyHST"""

from __future__ import annotations

import numpy
from silx.gui import qt


class LogSlider(qt.QWidget):
    """Slider to select a value with a QSlider displayed with log scale"""

    valueChanged = qt.Signal(float)
    """signal emitted when the value changed"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        # QSlider
        self._slider = qt.QSlider(self)
        self._slider.setOrientation(qt.Qt.Horizontal)
        self.layout().addWidget(self._slider, 0, 0, 1, 1)
        # Double spin box
        self._valueQBSB = qt.QDoubleSpinBox(self)
        self.layout().addWidget(self._valueQBSB, 0, 1, 1, 1)

        # connect signal / slot
        self._slider.valueChanged.connect(self._sliderValueChanged)
        self._valueQBSB.valueChanged.connect(self._qdsbValueChanged)
        # set up
        self.setRange(1, 100)
        self.setValue(5)

    def setSuffix(self, txt):
        self._valueQBSB.setSuffix(txt)

    def setPrefix(self, txt):
        self._valueQBSB.setPrefix(txt)

    def setRange(self, min_: float, max_: float) -> None:
        """
        Define slider range

        :param min_:
        :param max_:
        """
        if min_ <= 0.0 or max_ <= 0.0:
            raise ValueError("LogSlider can only handled positive values")
        self._valueQBSB.setRange(min_, max_)
        self._slider.setRange(int(numpy.log(min_)), int(numpy.log(max_)))

    def _sliderValueChanged(self, *args, **kwargs):
        old = self._valueQBSB.blockSignals(True)
        self._valueQBSB.setValue(numpy.exp(self._slider.value()))
        self._valueQBSB.blockSignals(old)
        self.valueChanged.emit(self.value())

    def _qdsbValueChanged(self, *args, **kwargs):
        old = self._slider.blockSignals(True)
        self._slider.setValue(int(numpy.log(self._valueQBSB.value())))
        self._slider.blockSignals(old)
        self.valueChanged.emit(self.value())

    def value(self):
        return self._valueQBSB.value()

    def setValue(self, value):
        self._valueQBSB.setValue(value)
