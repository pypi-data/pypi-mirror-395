from __future__ import annotations

from silx.gui import qt
from tomwer.core.process.reconstruction.axis.side import Side
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel
from tomwer.gui.utils.qt_utils import block_signals


class _EstimatedCorValidator(qt.QDoubleValidator):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDecimals(3)

    def validate(self, a0: str, a1: int):
        """validate float or string that could be part of the side values..."""
        for side in Side:
            if side.value.startswith(a0):
                return (qt.QDoubleValidator.Acceptable, a0, a1)
        return super().validate(a0, a1)


class EstimatedCorComboBox(QComboBoxIgnoreWheel):
    """
    Combobox that display the sides available according to the cor algorithm (left, right, center, all)
    and a dedicated item for cor given manually.

    This combobox is also editable and and make sure the 'estimated cor' item is up to date according to the QCombobox current value
    """

    ESTIMATED_COR_ITEM_DATA = "estimated_cor"

    sigEstimatedCorChanged = qt.Signal(object)
    """Emit when the estimated cor changed. Value can be a float (cor value) or a Side"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("0.0", self.ESTIMATED_COR_ITEM_DATA)
        for side in Side:
            self.addItem(side.value, side)

        self.setValidator(_EstimatedCorValidator())
        self.setEditable(True)

        self.setToolTip(
            """Estimated position of the center of rotation (COR) to be given to the cor algorithms. \n
            If you don't have a fair estimate you can provide only a side
            """
        )
        # connect signal / slot
        self.lineEdit().editingFinished.connect(self._corHasBeenEdited)
        self.currentIndexChanged.connect(self._corChanged)

    def _corHasBeenEdited(self):
        current_cor = self.getCurrentCorValue()
        if isinstance(current_cor, float):
            # keep the item up to date
            self._setCorItemValue(current_cor)
        self.sigEstimatedCorChanged.emit(current_cor)

    def _corChanged(self):
        self.sigEstimatedCorChanged.emit(self.getCurrentCorValue())

    def getCurrentCorValue(self) -> Side | float:
        try:
            return float(self.currentText())
        except ValueError:
            return Side(self.currentText())

    def setCurrentCorValue(self, value: float | Side):
        if isinstance(value, float):
            self._setCorItemValue(value)
        else:
            side = Side(value)
            item = self.findData(side)
            self.setCurrentIndex(item)

    def _setCorItemValue(self, value: float):
        item_index = self.findData(self.ESTIMATED_COR_ITEM_DATA)
        view = self.view()
        hidden = view.isRowHidden(item_index)
        with block_signals(self):
            self.setItemText(item_index, f"{value:.2f}")
            view.setRowHidden(item_index, hidden)

    def get_hidden_sides(self) -> tuple[Side]:
        """Return all sides currently hidden"""
        view = self.view()
        return tuple(
            filter(
                lambda side: view.isRowHidden(self.findData(side)),
                [Side(side) for side in Side],
            )
        )

    def setSidesVisible(self, sides: tuple[Side]):
        """Set side to be visible to the user"""
        sides_visibles = tuple([Side(side) for side in sides])
        view = self.view()
        for side in Side:
            item_idx = self.findData(side)
            view.setRowHidden(item_idx, side not in sides_visibles)

        need_new_current_value = self.getCurrentCorValue() in self.get_hidden_sides()
        if need_new_current_value:
            # if the current side used cannot be used fall back to the estimated cor from motor
            self.setCurrentIndex(self.findData(self.ESTIMATED_COR_ITEM_DATA))

    def setFirstGuessAvailable(self, available: bool):
        """
        For some method (only growing window at the moment) a first guess (estimated cor as a float) cannot be given
        """
        view = self.view()
        item_index = self.findData(self.ESTIMATED_COR_ITEM_DATA)
        view.setRowHidden(item_index, not available)

    def selectFirstGuess(self):
        item_index = self.findData(self.ESTIMATED_COR_ITEM_DATA)
        self.setCurrentIndex(item_index)
