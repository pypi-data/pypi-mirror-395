from __future__ import annotations

import logging
from collections import OrderedDict
from typing import Iterable

import numpy
from silx.gui import qt
from silx.gui.plot import PlotWidget

logger = logging.getLogger(__name__)


class QSliceSelectorDialog(qt.QDialog):
    """
    The dialog used to select some slice indexes from a radio

    :param QWidget parent: parent widget
    :param n_required_slice: number of required slice we expect the user to select
    """

    def __init__(self, parent, n_required_slice: int | None = None):
        qt.QDialog.__init__(self, parent=parent)
        self.setLayout(qt.QVBoxLayout())
        self.setWindowTitle("select slices on radio")

        self.mainWidget = QLineSelector(parent=self, n_required_slice=n_required_slice)
        self.layout().addWidget(self.mainWidget)

        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        # connect signal / slots
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.Cancel).clicked.connect(self.reject)

        # expose API
        self.setData = self.mainWidget.setData

    def setSelection(self, selection: Iterable):
        """

        :param rows: define the selection
        """
        if self.nRequiredSlice() is not None and len(selection) > self.nRequiredSlice():
            raise ValueError(
                f"you provide a selection of {len(selection)} elements when the user should select {self._n_required_slice}"
            )
        if type(selection) is str:
            selection = selection.replace("(", "")
            selection = selection.replace(")", "")
            selection = selection.replace(" ", "")
            selection = selection.replace(",", ";")
            try:
                selection = [int(item) for item in selection.split(";")]
            except Exception as e:
                logger.error(f"Fail to set selection. Error is {e}")
        self.mainWidget.setSelection(selection)

    def getSelection(self) -> tuple:
        """

        :return: the selection of slices to use
        """
        return self.mainWidget.getSelection()

    def exec_(self):
        if not self.mainWidget._has_data:
            mess = "no data set, can't use the selection tool"
            logger.warning(mess)
            qt.QMessageBox.warning(self, "Selection tool not available", mess)
            self.reject()
        else:
            return qt.QDialog.exec(self)

    def nRequiredSlice(self) -> int | None:
        return self.mainWidget.nRequiredSlice()


class QLineSelector(qt.QWidget):
    """Widget to select a set of slices from a plot"""

    def __init__(self, parent=None, n_required_slice=None):
        self._n_required_slice = n_required_slice
        qt.QWidget.__init__(self, parent)
        self._plot = PlotWidget()
        # invert y axis
        self._plot.setYAxisInverted(True)
        self.__selection = OrderedDict()
        # dict of markers from the user selection. Keys are item legend, value
        # are items
        self._has_data = False
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._plot)
        # connect signal / slot
        self._plot.sigPlotSignal.connect(self._plotDrawEvent)

    def nRequiredSlice(self) -> int | None:
        return self._n_required_slice

    def setData(self, data: numpy.ndarray):
        """
        Define the data from which we can select slices

        :param data: data to plot
        """
        self._has_data = True
        self._plot.addImage(data)
        assert self._plot.getActiveImage(just_legend=True) is not None

    def getSelection(self) -> tuple:
        """

        :return: the selection of slices to use
        """
        res = []
        for _, marker in self.__selection.items():
            res.append(int(marker.getPoints()[0][1]))
        return tuple(sorted(res))

    def _clear(self):
        if len(self.__selection) > 0:
            self.removeSlice(list(self.__selection.keys())[0])
            self._clear()

    def nSelected(self) -> int:
        """Return the number of slice selected"""
        return len(self.__selection)

    def setSelection(self, rows: Iterable) -> None:
        """

        :param rows: define the selection
        """
        assert type(rows) is not str
        self._clear()
        if rows is not None:
            for row in rows:
                self.addSlice(row)

    def addSlice(self, row: float | int) -> None:
        """
        Add the requested slice to the selection

        :param row:
        """
        row_n = round(float(row))

        if self._plot.getActiveImage(just_legend=True) is not None:
            data_bounds = self._plot.getActiveImage(just_legend=False).getBounds()
            if not (data_bounds[0] <= row_n < data_bounds[1]):
                logger.warning("requested slice out of the data, ignored")
                return

        # remove the n first selected point if needed
        n_selected = len(self.getSelection())
        n_required_slice = self.nRequiredSlice()
        if (n_required_slice is not None) and (n_selected >= n_required_slice):
            n_slice_to_rm = n_required_slice - n_selected + 1
            # +1 because we are about to add a slice
            markers = tuple(self.__selection.values())
            idx_to_rm = [
                int(marker.getPoints()[0][1]) for marker in markers[0:n_slice_to_rm]
            ]
            for slice_idx in idx_to_rm:
                self.removeSlice(slice_idx)

        inf = 10000
        legend = self._getLegend(row_n=row_n)
        self._plot.addShape(
            xdata=numpy.array((-inf, -inf, inf, inf)),
            ydata=numpy.array((row_n, row_n + 1, row_n + 1, row_n)),
            shape="polygon",
            linewidth=1,
            color="pink",
            linestyle="-",
            fill=True,
            legend=legend,
        )
        self.__selection[legend] = self._plot._getItem(kind="item", legend=legend)

    def _getLegend(self, row_n) -> str:
        return str(round(float(row_n)))

    def removeSlice(self, row: float | int) -> None:
        """
        remove the requested slice from the selection

        :param row: row containing the slice to be removed
        """
        legend = self._getLegend(row_n=row)
        if legend in self.__selection:
            self._plot.remove(legend=legend, kind="item")
            del self.__selection[legend]

    def _plotDrawEvent(self, event):
        if "event" in event and event["event"] == "mouseClicked":
            row = event["y"] - 0.5

            if qt.QApplication.keyboardModifiers() & qt.Qt.ControlModifier:
                self.removeSlice(row=row)
            else:
                self.addSlice(row=row)
