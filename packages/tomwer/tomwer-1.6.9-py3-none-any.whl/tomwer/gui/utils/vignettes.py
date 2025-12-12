"""
contains gui to select a slice in a volume
"""

from __future__ import annotations

import logging
from typing import Iterable

import numpy
from silx.gui import qt
from silx.gui.plot import PlotWindow
from silx.gui.plot.utils.axis import SyncAxes
from silx.io.url import DataUrl
from tomoscan.esrf.scan.utils import get_data
from math import floor

from tomwer.core.process.reconstruction.scores.scores import ComputedScore, ScoreMethod

_logger = logging.getLogger(__name__)


class VignettesQDialog(qt.QDialog):
    """ """

    SIZE_HINT = qt.QSize(820, 820)

    AUTO_NB_COLUMN = "auto"

    COLUMN_VALUES = (AUTO_NB_COLUMN, 1, 2, 3, 4, 5, 6, 8, 10)

    RESIZE_MAX_TIME = 500

    def __init__(
        self,
        value_name,
        score_name,
        parent=None,
        value_format=None,
        score_format=None,
        colormap=None,
    ):
        qt.QDialog.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._scan = None
        self._selectedValue = None
        self.setLayout(qt.QVBoxLayout())

        self._nbColumnCB = qt.QComboBox(self)
        for nb_column in self.COLUMN_VALUES:
            self._nbColumnCB.addItem(str(nb_column))

        self._columnWidget = qt.QWidget(self)
        # needed intermediary widget because the 'setWidgetResizable' fails with QFormLayout on PyQt 5.14.1 and will want to keep compatiblity for now
        self._columnWidget.setLayout(qt.QFormLayout())
        self._columnWidget.layout().addRow("number of column", self._nbColumnCB)
        self.layout().addWidget(self._columnWidget)

        self._mainWidget = qt.QScrollArea(self)
        self._mainWidget.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
        self._mainWidget.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAsNeeded)
        self._vignettesWidget = VignettesWidget(
            self,
            with_spacer=True,
            value_name=value_name,
            score_name=score_name,
            score_format=score_format,
            value_format=value_format,
            colormap=colormap,
        )
        self._mainWidget.setWidget(self._vignettesWidget)
        self.layout().addWidget(self._mainWidget)
        self._mainWidget.setWidgetResizable(True)

        # buttons
        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self._buttons.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(self._buttons)

        # connect signal slot
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self._nbColumnCB.currentIndexChanged.connect(self._updateNbColumn)

        self._resizeCallback = None
        self._firstResizeEvent = True

    def sizeHint(self):
        """Return a reasonable default size for usage in :class:`PlotWindow`"""
        return self.SIZE_HINT

    def setScores(self, scores: dict, score_method: ScoreMethod):
        """
        Expect a dictionary with possible values to select as key and
        (2D numpy.array, score) as value.
        Where the 2D numpy.array is the frame to display and the score if the
        "indicator" score to display with the frame.
        :param scores: with score as key and a tuple (url|numpy array, ComputedScore) as value
        :param ScoreMethod score_method: score kind to be display
        """
        self._vignettesWidget.setScores(scores=scores, score_method=score_method)

    def selectedValue(self):
        if self._vignettesWidget is None:
            return self._selectedValue
        else:
            return self._vignettesWidget.selectedValue()

    def acccept(self):
        self._selectedValue = self._vignettesWidget.selectedValue()
        self._vignettesWidget.close()
        super().accept()

    def reject(self):
        self._selectedValue = self._vignettesWidget.selectedValue()
        self._vignettesWidget.close()
        super().reject()

    def getNColumn(self) -> int | None:
        n_column = self._nbColumnCB.currentText()
        if n_column == self.AUTO_NB_COLUMN:
            return None
        else:
            return int(n_column)

    def setNbColumn(self, value: int | str):
        if value not in self.COLUMN_VALUES:
            raise ValueError(
                f"Unhandled number of column requested ({value}). Valid values are {self.COLUMN_VALUES}"
            )
        idx = self._nbColumnCB.findText(str(value))
        self._nbColumnCB.setCurrentIndex(idx)

    @staticmethod
    def computeOptimalNColumn(window_width, vignette_width):
        n = floor(window_width / vignette_width)
        # To check with Jerome; He seems to have work on the topic.
        # might have some method for a smart way to do it
        return max(1, n)

    def _updateNbColumn(self, force_update=False):
        n_colum = self.getNColumn()
        if n_colum is None:
            n_colum = self.computeOptimalNColumn(
                window_width=self.width(),
                vignette_width=400,
            )
        self._vignettesWidget.setNElementsPerRow(n_colum, force_update=force_update)

    def resizeEvent(self, event):
        if self._firstResizeEvent:
            # cheap way to filter the first resize and avoid updating it
            self._firstResizeEvent = False
        else:
            # print("resize event received...", event)
            if self._resizeCallback is not None:
                self._resizeCallback.timeout.disconnect(self._updateNbColumn)
                self._resizeCallback.stop()
                self._resizeCallback.deleteLater()
                self._resizeCallback = None
            self._resizeCallback = qt.QTimer(self)
            self._resizeCallback.setSingleShot(True)
            self._resizeCallback.timeout.connect(self._updateNbColumn)
            self._resizeCallback.start(self.RESIZE_MAX_TIME)

        super().resizeEvent(event)


class VignettesWidget(qt.QWidget):
    """
    Widget to display all the frames.

    :param parent:
    :param value_name: name of the values for which we are looking for the
                           best one
    :param score_name: name of the score computed
    :param score_format: None or str that can be formatted to display the
                         score
    :param value_format: None or str that can be formatted to display the
                         value
    """

    DEFAULT_PLOT_PER_ROW = 2
    MAX_NB_COLUMN = 999999

    def __init__(
        self,
        parent=None,
        value_name="value",
        score_name="score",
        with_spacer=True,
        value_format=None,
        score_format=None,
        colormap=None,
    ):
        qt.QWidget.__init__(self, parent)
        self._valueName = value_name
        self._scoreName = score_name
        self._nPlotPerRow = VignettesWidget.DEFAULT_PLOT_PER_ROW
        self._withSpacer = with_spacer
        self._vignettesGroup = qt.QButtonGroup()
        self.__constraintXAxis = None
        self.__constraintYAxis = None
        self._valueFormat = value_format
        self._scoreFormat = score_format
        self._colormap = colormap
        self._vignettes = []
        self.__score_method = None

        self.setLayout(qt.QGridLayout())

    def close(self):
        for vignette in self._vignettes:
            vignette.close()
        super().close()

    def selectedValue(self):
        sel_vignette = self._vignettesGroup.checkedButton()
        if sel_vignette is not None:
            return sel_vignette.getScoreValue()
        else:
            return None

    def setNElementsPerRow(self, n: int, force_update):
        assert isinstance(n, int), "number of column must be an int"
        if self._nPlotPerRow != n:
            self._nPlotPerRow = n
            self.__update()
        elif force_update:
            self.__update()

    def __update(self):
        scores, score_method = self.getScores()
        self.setScores(scores, score_method)
        # raise NotImplementedError

    def getNElementsPerRow(self):
        return self._nPlotPerRow

    def getScores(self) -> tuple:
        """
        Return currently displayed scores as (scores, scores_method)
        """
        scores = {}
        scores_method = self.__score_method
        for vignette in self._vignettes:
            assert isinstance(vignette, Vignette)
            if scores_method in (ScoreMethod.STD, ScoreMethod.STD_INVERSE):
                compute_score_args = {
                    "std": vignette.getScoreValue(),
                    "tv": None,
                }
            elif scores_method in (ScoreMethod.TV, ScoreMethod.TV_INVERSE):
                compute_score_args = {
                    "std": None,
                    "tv": vignette.getScoreValue(),
                }
            elif scores_method in (ScoreMethod.TOMO_CONSISTENCY):
                compute_score_args = {
                    "std": None,
                    "tv": None,
                    "tomo_consitency": vignette.getScoreValue(),
                }
            else:
                raise ValueError(f"score method unhandled: {scores_method.value}")

            scores[vignette.getValue()] = (
                vignette.getData(),
                ComputedScore(**compute_score_args),
            )
        return scores, scores_method

    def clearVignettes(self):
        for vignette in self._vignettes:
            self.layout().removeWidget(vignette)
            vignette.setParent(None)
            self._vignettesGroup.removeButton(vignette)
            # vignette.deleteLater()
        self._vignettes = []

    def setScores(self, scores: dict, score_method: ScoreMethod):
        """
        Expect a dictionary with possible values to select as key and
        (2D numpy.array, score) as value.
        Where the 2D numpy.array is the frame to display and the score if the
        "indicator" score to display with the frame.
        :param scores: with score as key and a tuple (url|numpy array, ComputedScore) as value
        :param ScoreMethod score_method: score kind to be display
        """
        if len(scores) < 1:
            return

        self.clearVignettes()

        i_row = 0
        scores_values = []
        for i_score, (value, (data, score_cls)) in enumerate(scores.items()):
            if not isinstance(score_cls, ComputedScore):
                raise TypeError(
                    f"score is expected to be a dict with values as (v1: numpy.ndarray, v2: ComputedScore). v2 type Found: {type(score_cls)}"
                )
            scores_values.append(score_cls.get(score_method))
        self.__score_method = ScoreMethod(score_method)
        highest_score_indices = numpy.nanargmax(scores_values)
        self._vignettesGroup = qt.QButtonGroup(self)
        self._vignettesGroup.setExclusive(True)

        if not isinstance(highest_score_indices, Iterable):
            highest_score_indices = (highest_score_indices,)

        xAxis = []
        yAxis = []

        for i_score, (value, (data, score_cls)) in enumerate(scores.items()):
            score = score_cls.get(score_method)
            i_column = i_score % self.getNElementsPerRow()
            # TODO: instead of having a binary color we could use
            # colormap from green (good score) to red (bad score score)
            if i_score == highest_score_indices or i_score in highest_score_indices:
                frame_color = qt.Qt.green
            else:
                frame_color = qt.Qt.lightGray
            widget = Vignette(
                parent=self,
                value_name=self._valueName,
                score_name=self._scoreName,
                value=value,
                data=data,
                score=score,
                frame_color=frame_color,
                value_format=self._valueFormat,
                score_format=self._scoreFormat,
                colormap=self._colormap,
            )
            widget.setAttribute(qt.Qt.WA_DeleteOnClose)
            xAxis.append(widget.getPlotWidget().getXAxis())
            yAxis.append(widget.getPlotWidget().getYAxis())

            self.layout().addWidget(widget, i_row, i_column)
            if i_column == self.getNElementsPerRow() - 1:
                i_row += 1
            if i_score == 0:
                # we cannot request all widget to keep the aspect ratio
                widget.setKeepDataAspectRatio(True)
            self._vignettesGroup.addButton(widget)
            self._vignettes.append(widget)

        if self._withSpacer:
            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
            # to simplify we add a spacer at the end. We do not expect to have more than 999999 column
            self.layout().addWidget(spacer, i_row + 1, self.MAX_NB_COLUMN)

        # constrain axis synchronization
        self.__constraintXAxis = SyncAxes(
            xAxis,
            syncLimits=False,
            syncScale=True,
            syncDirection=True,
            syncCenter=True,
            syncZoom=True,
        )
        self.__constraintYAxis = SyncAxes(
            yAxis,
            syncLimits=False,
            syncScale=True,
            syncDirection=True,
            syncCenter=True,
            syncZoom=True,
        )


class _PlotForVignette(PlotWindow):
    def __init__(self, parent=None):
        PlotWindow.__init__(
            self,
            parent=parent,
            yInverted=True,
            copy=False,
            save=False,
            print_=False,
            control=False,
            mask=False,
        )
        self.setKeepDataAspectRatio(False)
        self.setAxesDisplayed(False)
        self.toolBar().hide()
        self.getInteractiveModeToolBar().hide()
        self.getOutputToolBar().hide()
        self.setInteractiveMode("zoom", zoomOnWheel=False)

    def close(self) -> bool:
        super().close()


class Vignette(qt.QToolButton):
    """Widget to display a vignette"""

    FRAME_WIDTH = 2

    def __init__(
        self,
        parent,
        value,
        value_name: str,
        score_name: str,
        data: DataUrl | numpy.array,
        score: float,
        frame_color: qt.QColor,
        score_format=None,
        value_format=None,
        colormap=None,
    ):
        self._value = value
        self._scoreName = score_name
        self._valueName = value_name
        qt.QToolButton.__init__(self, parent)
        self.setCheckable(True)
        self.setLayout(qt.QVBoxLayout())
        self._plot = _PlotForVignette(parent=self)
        self._plot.setDefaultColormap(colormap=colormap)

        self.layout().addWidget(self._plot)
        self._valueLabel = ValueLabel(
            self,
            value=value,
            score=score,
            score_name=self._scoreName,
            value_name=self._valueName,
            value_format=value_format,
            score_format=score_format,
        )
        self.layout().addWidget(self._valueLabel)
        self.setFixedSize(400, 400)
        self._frameColor = frame_color
        self._selectedFrameColor = qt.Qt.black

        if isinstance(data, DataUrl):
            data = get_data(data)
        if data.ndim == 3 and data.shape[0] == 1:
            data = data.reshape(data.shape[1:])
        self._plot.addImage(data)

    def setKeepDataAspectRatio(self, keep):
        self._plot.setKeepDataAspectRatio(keep)

    def getPlotWidget(self):
        return self._plot

    def getValue(self):
        return self._value

    def getData(self) -> numpy.ndarray:
        return self._plot.getImage().getData()

    def getScoreValue(self):
        return self._valueLabel.score

    def getScoreName(self):
        return self._scoreName

    def getValueName(self):
        return self._valueName

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = qt.QPainter(self)
        half_h_width = self.FRAME_WIDTH // 2
        rect = qt.QRect(
            half_h_width,
            half_h_width,
            self.width() - self.FRAME_WIDTH,
            self.height() - self.FRAME_WIDTH,
        )
        pen = qt.QPen()
        pen.setWidth(Vignette.FRAME_WIDTH)
        pen.setColor(self._frameColor)
        painter.setPen(pen)
        painter.drawRect(rect)
        if self.isChecked():
            pen.setColor(self._selectedFrameColor)
            pen.setStyle(qt.Qt.DashLine)
            pen.setDashOffset(0.2)
            painter.setPen(pen)
            painter.drawRect(rect)

    def close(self):
        self._plot.clear()
        self._plot.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._plot.close()
        self._plot = None


class ValueLabel(qt.QWidget):
    """Display the value and the associated score"""

    def __init__(
        self, parent, value, score, value_name, score_name, value_format, score_format
    ):
        qt.QWidget.__init__(self, parent)
        self._score = score
        self.setLayout(qt.QHBoxLayout())
        if value_format is not None:
            str_value = value_format.format(value)
        else:
            str_value = str(value)
        txt = f"{value_name}: {str_value}"
        self._valueLabel = qt.QLabel(txt, self)
        self.layout().addWidget(self._valueLabel)
        if score_format is not None:
            str_score = score_format.format(score)
        else:
            str_score = str(score)
        txt = f"({score_name}: {str_score})"
        self._scoreLabel = qt.QLabel(txt, self)
        self.layout().addWidget(self._scoreLabel)

    @property
    def score(self):
        return self._score
