from __future__ import annotations

import sys
from silx.gui import qt
from tomwer.gui.utils.scrollarea import QDoubleSpinBoxIgnoreWheel as QDoubleSpinBox


class RangeWidget(qt.QWidget):
    """widget to select a range of float"""

    sigChanged = qt.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())

        # start
        self.layout().addWidget(qt.QLabel("from"))
        self._startQLE = QDoubleSpinBox(self)
        self.layout().addWidget(self._startQLE)
        self._startQLE.setRange(sys.float_info.min, sys.float_info.max)

        # stop
        self.layout().addWidget(qt.QLabel("to"))
        self._stopQLE = QDoubleSpinBox(self)
        self.layout().addWidget(self._stopQLE)
        self._stopQLE.setRange(sys.float_info.min, sys.float_info.max)

        # connect signal / slot
        self._startQLE.editingFinished.connect(self.sigChanged)
        self._stopQLE.editingFinished.connect(self.sigChanged)

    def getRange(self) -> tuple[float]:
        return (
            self._startQLE.value(),
            self._stopQLE.value(),
        )

    def setRange(self, start: float, stop: float) -> None:
        self._startQLE.setValue(float(start))
        self._stopQLE.setValue(float(stop))

    def setSuffix(self, suffix: str):
        self._startQLE.setSuffix(suffix)
        self._stopQLE.setSuffix(suffix)
