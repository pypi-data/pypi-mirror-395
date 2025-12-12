"""
contains gui relative to semi-automatic axis calculation
"""

from __future__ import annotations

import pint
from typing import Iterable

from silx.gui import qt
from tomwer.gui.utils.qt_utils import block_signals

_ureg = pint.get_application_registry()


class DimensionWidget(qt.QGroupBox):
    """
    Simple widget to display value over 3 dimensions

    :param parent:
    :param title: QGroupBox title
    :param dims_name: name of the dimension. If set will be store in each
                      QDoubleLine prefix
    :param dims_colors: color associated to the three dimensions if any
    """

    valuesChanged = qt.Signal()
    """Signal emitted when a value change"""

    def __init__(
        self, parent=None, title=None, dims_name=None, dims_colors=None, title_size=10
    ):
        qt.QGroupBox.__init__(self, parent)
        self.setFont(qt.QFont("Arial", title_size))
        assert title is not None
        assert dims_name is None or (
            isinstance(dims_name, Iterable) and len(dims_name) == 3
        )
        assert dims_colors is None or (
            isinstance(dims_colors, Iterable) and len(dims_colors) == 3
        )
        self._displayUnit = _ureg.millimeter
        self._dim0Value: pint.Quantity = 1.0 * self._displayUnit
        self._dim1Value: pint.Quantity = 1.0 * self._displayUnit
        self._dim2Value: pint.Quantity = 1.0 * self._displayUnit
        # defined unit to display values. Always stored in m (International
        # System)
        ## set GUI
        self.setTitle(title)
        self.setLayout(qt.QHBoxLayout())
        # dim 0
        self._dim0ValueQLE = qt.QDoubleSpinBox(self)
        if dims_name is not None:
            self._dim0ValueQLE.setPrefix(dims_name[0])
        self._dim0ValueQLE.setRange(0, 999999999999)
        self._dim0ValueQLE.setDecimals(10)
        self._dim0ValueQLE.setSingleStep(0.0001)
        self._dim0ValueQLE.setValue(self._dim0Value.magnitude)
        if dims_colors is not None:
            stylesheet = f"background-color: {dims_colors[0]}"
            self._dim0ValueQLE.setStyleSheet(stylesheet)
        self.layout().addWidget(self._dim0ValueQLE)
        # dim 1
        self._dim1ValueQLE = qt.QDoubleSpinBox(self)
        if dims_name is not None:
            self._dim1ValueQLE.setPrefix(dims_name[1])
        self._dim1ValueQLE.setRange(0, 999999999999)
        self._dim1ValueQLE.setDecimals(10)
        self._dim1ValueQLE.setSingleStep(0.0001)
        self._dim1ValueQLE.setValue(self._dim1Value.magnitude)
        if dims_colors is not None:
            stylesheet = f"background-color: {dims_colors[1]}"
            self._dim1ValueQLE.setStyleSheet(stylesheet)
        self.layout().addWidget(self._dim1ValueQLE)
        # dim 2
        self._dim2ValueQLE = qt.QDoubleSpinBox(self)
        if dims_name is not None:
            self._dim2ValueQLE.setPrefix(dims_name[2])
        self._dim2ValueQLE.setRange(0, 999999999999)
        self._dim2ValueQLE.setDecimals(10)
        self._dim2ValueQLE.setSingleStep(0.0001)
        self._dim2ValueQLE.setValue(self._dim2Value.magnitude)
        if dims_colors is not None:
            stylesheet = f"background-color: {dims_colors[2]}"
            self._dim2ValueQLE.setStyleSheet(stylesheet)
        self.layout().addWidget(self._dim2ValueQLE)

        # set up
        self.setUnit(self._displayUnit)

        # connect signal / slot
        self._dim0ValueQLE.editingFinished.connect(self._userSetDim0)
        self._dim1ValueQLE.editingFinished.connect(self._userSetDim1)
        self._dim2ValueQLE.editingFinished.connect(self._userSetDim2)

    def setUnit(self, unit: pint.Unit):
        """
        define with which unit we should display the size
        :param unit: metric to be used for display. Internally this is always stored using the international metric system
        """
        if not isinstance(unit, pint.Unit):
            raise TypeError(
                f"unit is expected be an instance of {pint.Unit}. Got {type(unit)}"
            )
        for widget in (self._dim0ValueQLE, self._dim1ValueQLE, self._dim2ValueQLE):
            widget.setSuffix(f"{self._displayUnit:.4f~P}")
        # convert current values
        self._dim0Value = self._dim0Value.magnitude * self._displayUnit
        self._dim1Value = self._dim1Value.magnitude * self._displayUnit
        self._dim2Value = self._dim2Value.magnitude * self._displayUnit
        # update displayed values
        with block_signals(self):
            self._dim0ValueQLE.setValue(self._dim0Value.magnitude)
            self._dim1ValueQLE.setValue(self._dim1Value.magnitude)
            self._dim2ValueQLE.setValue(self._dim2Value.magnitude)

    def setQuantities(
        self,
        dim0: pint.Quantity,
        dim1: pint.Quantity,
        dim2: pint.Quantity,
    ) -> None:
        """

        :param dim0: value to dim0
        :param dim1: value to dim1
        :param dim2: value to dim2
        :param unit: unit used for the provided values
        """
        with block_signals(self):
            self.setDim0Quantity(value=dim0)
            self.setDim1value(value=dim1)
            self.setDim2Quantity(value=dim2)
        self.valuesChanged.emit()

    def getQuantities(
        self, cast_unit_to: None | pint.Unit = None
    ) -> tuple[pint.Quantity]:
        """
        :param cast_unit_to: if given will cast the quantities to the requested unit

        :return: (dim0 value, dim1 value, dim2 value)
        """
        if cast_unit_to is None:
            return (
                self.getDim0Quantity(),
                self.getDim1Quantity(),
                self.getDim2Quantity(),
            )
        else:
            return (
                self.getDim0Quantity().to(cast_unit_to),
                self.getDim1Quantity().to(cast_unit_to),
                self.getDim2Quantity().to(cast_unit_to),
            )

    def getDim0Quantity(self) -> tuple:
        """Return Dim 0 value and unit. Unit is always meter"""
        return self._dim0Value

    def setDim0Quantity(self, value: pint.Quantity):
        """

        :param value: value to set to dim 0.
        :return:
        """
        assert isinstance(value, pint.Quantity)
        self._dim0Value = value
        with block_signals(self):
            self._dim0ValueQLE.setValue(self._dim0Value.magnitude)
        self.valuesChanged.emit()

    def getDim1Quantity(self) -> pint.Quantity:
        """Return Dim 1 Quantity"""
        return self._dim1Value

    def setDim1value(self, value: pint.Quantity):
        """

        :param value: value to set to dim 1.
        :return:
        """
        assert isinstance(value, pint.Quantity)
        self._dim1Value = value
        with block_signals(self):
            self._dim1ValueQLE.setValue(self._dim1Value.magnitude)
        self.valuesChanged.emit()

    def getDim2Quantity(self) -> pint.Quantity:
        """Return Dim 2 value and unit. Unit is always meter"""
        return self._dim2Value

    def setDim2Quantity(self, value: pint.Quantity):
        """

        :param value: value to set to dim 2.
        :return:
        """
        assert isinstance(value, pint.Quantity)
        self._dim2Value = value
        with block_signals(self):
            self._dim2ValueQLE.setValue(self._dim2Value.magnitude)
        self.valuesChanged.emit()

    def _valuesChanged(self, *args, **kwargs):
        self.valuesChanged.emit()

    def _userSetDim0(self):
        """callback when the user modify the dim 0 QDSP"""
        with block_signals(self):
            self._dim0Value = self._dim0ValueQLE.value() * self._displayUnit
        self.valuesChanged.emit()

    def _userSetDim1(self):
        """callback when the user modify the dim 1 QDSP"""
        with block_signals(self):
            self._dim1Value = self._dim1ValueQLE.value() * self._displayUnit
        self.valuesChanged.emit()

    def _userSetDim2(self):
        """callback when the user modify the dim 2 QDSP"""
        with block_signals(self):
            self._dim2Value = self._dim2ValueQLE.value() * self._displayUnit
        self.valuesChanged.emit()
