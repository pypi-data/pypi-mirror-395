from __future__ import annotations

import logging
from contextlib import AbstractContextManager
from typing import Iterable

from silx.gui import qt
from silx.gui.utils import blockSignals
from enum import Enum as _Enum
from tomoscan.series import Series

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.gui.control.datalist import TomoObjList
from tomwer.gui.dialog.QDataDialog import QDataDialog
from tomwer.gui.visualization.tomoobjoverview import TomoObjOverview

_logger = logging.getLogger(__name__)


class SeriesWidgetDialog(qt.QDialog):
    sigSeriesSelected = qt.Signal(Series)
    """
    emit when a series is selected / triggered by the user
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setLayout(qt.QVBoxLayout())
        # add list
        self._widget = SeriesWidget()
        self.layout().addWidget(self._widget)
        # add buttons
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._selectButton = qt.QPushButton("Select (active) series", parent=self)
        self._buttons.addButton(self._selectButton, qt.QDialogButtonBox.ActionRole)
        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._selectButton.released.connect(self._seriesSelected)

    def getSelectedSeries(self) -> Series | None:
        return self._widget.getSelectedSeries()

    def _seriesSelected(self, *args, **kwargs):
        series = self.getSelectedSeries()
        if series is not None:
            self.sigSeriesSelected.emit(series)

    # expose API
    def add(self, tomo_obj):
        self._widget.add(tomo_obj=tomo_obj)


class SeriesWidget(qt.QTabWidget):
    sigCurrentSeriesChanged = qt.Signal()
    """signal emit when the current series changes"""

    sigHistoryChanged = qt.Signal()
    """signal emit when the history changed (a series has been added or removed"""

    sigSeriesSend = qt.Signal(Series)
    """Signal emit when a series has been send"""

    _HISTORY_MODE = "history"
    _DEFINITION_MODE = "series definition"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("series of scans")
        self._seriesDefinitionWidget = SeriesDefinition(parent=self)
        self.addTab(self._seriesDefinitionWidget, self._DEFINITION_MODE)
        self._historyWidget = SeriesHistoryDialog(parent=self)
        self._historyWidget.setWindowFlags(qt.Qt.Widget)
        self.addTab(self._historyWidget, self._HISTORY_MODE)

        # connect signal / slot
        self._historyWidget.sigEditSeries.connect(self._seriesEditionRequested)
        self._historyWidget.sigSeriesSend.connect(self.sigSeriesSend)
        self._historyWidget.sigHistoryUpdated.connect(self._repeatHistoryUpdated)
        self._seriesDefinitionWidget.sigSeriesChanged.connect(self._repeatSeriesChanged)
        self._seriesDefinitionWidget.sigSeriesSend.connect(self.sigSeriesSend)
        self._seriesDefinitionWidget.sigSeriesSend.connect(
            self._historyWidget.addSeries
        )

    def getHistoryWidget(self):
        return self._historyWidget

    def getDefinitionWidget(self):
        return self._seriesDefinitionWidget

    def getSelectedSeries(self) -> Series | None:
        return self._seriesDefinitionWidget.getSelectedSeries()

    def setMode(self, mode: str, definition_mode: str | None = None):
        valid_modes = (self._HISTORY_MODE, self._DEFINITION_MODE)
        if mode == self._HISTORY_MODE:
            self.setCurrentWidget(self._historyWidget)
        elif mode == self._DEFINITION_MODE:
            self.setCurrentWidget(self._seriesDefinitionWidget)
            self._seriesDefinitionWidget.setMode(definition_mode)
        else:
            raise ValueError(
                f"mode {mode} is no recognized. Valid modes are {valid_modes}"
            )

    def _seriesEditionRequested(self, series: Series):
        if not isinstance(series, Series):
            raise TypeError(f"series is expected to be a series not {type(series)}")
        self.setMode("series definition", "manual")
        self.getDefinitionWidget().getManualDefinitionWidget().setSeries(series)

    def _repeatSeriesChanged(self, *args, **kwargs):
        self.sigCurrentSeriesChanged.emit()

    def _repeatHistoryUpdated(self, *args, **kwargs):
        self.sigHistoryChanged.emit()

    def add(self, tomo_obj):
        return self._seriesDefinitionWidget.addTomoObj(tomo_obj)


class _SeriesDefinitionMode(_Enum):
    MANUAL = "manual"
    AUTO = "auto"


class SeriesDefinition(qt.QWidget):
    sigSeriesChanged = qt.Signal()
    """signal emit when a the series defined manually changed"""

    sigSeriesSend = qt.Signal(Series)
    """Signal emited when a series has been send"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())

        self._modeLabel = qt.QLabel("Mode", self)
        self.layout().addWidget(self._modeLabel, 0, 0, 1, 1)

        self._modeCB = qt.QComboBox(self)
        for mode in _SeriesDefinitionMode:
            self._modeCB.addItem(mode.value)
        self.layout().addWidget(self._modeCB, 0, 1, 1, 1)

        self._manualDefWidget = SeriesManualFromTomoObj(parent=self)
        self.layout().addWidget(self._manualDefWidget, 1, 0, 1, 2)
        self._manualDefWidget.setWindowFlags(qt.Qt.Widget)

        self._automaticDefWidget = SeriesAutomaticDefinitionWidget(parent=self)
        self.layout().addWidget(self._automaticDefWidget, 2, 0, 1, 2)

        # connect signal / slot
        self._modeCB.currentIndexChanged.connect(self._updateVisibility)
        self._manualDefWidget._newSeriesWidget.sigUpdated.connect(self.sigSeriesChanged)

        # set up
        self._updateVisibility()

    def getSelectedSeries(self) -> Series | None:
        if self.getMode() == _SeriesDefinitionMode.MANUAL:
            return self._manualDefWidget.getSeries()
        else:
            raise ValueError(f"mode {self.getMode()} is not handled yet")

    def getMode(self) -> str:
        return _SeriesDefinitionMode(self._modeCB.currentText())

    def setMode(self, mode: str):
        mode = _SeriesDefinitionMode(mode)
        idx = self._modeCB.findText(mode.value)
        self._modeCB.setCurrentIndex(idx)

    def _updateVisibility(self):
        self._manualDefWidget.setVisible(self.getMode() == _SeriesDefinitionMode.MANUAL)
        self._automaticDefWidget.setVisible(
            self.getMode() == _SeriesDefinitionMode.AUTO
        )

    def getManualDefinitionWidget(self):
        return self._manualDefWidget

    def getAutoDefinitionWidget(self):
        return self._automaticDefWidget

    def createManualSeries(self):
        self._manualDefWidget.createSeries()

    def addTomoObj(self, tomo_obj: TomwerObject):
        self._manualDefWidget.addTomoObj(tomo_obj=tomo_obj)

    def setSeriesName(self, name: str):
        self._manualDefWidget.setSeriesName(name=name)


class _SeriesDefinitionTree(qt.QWidget):
    """
    Tree used to define manually series of scan.
    Drag and drop of files is handled
    """

    sigUpdated = qt.Signal()
    """Signal emit when the series is updated"""

    class SignalBlocker(AbstractContextManager):
        """Simple context manager to hide / show button dialogs"""

        def __init__(self, serie_definition_widget) -> None:
            super().__init__()
            self.serie_definition_widget = serie_definition_widget

        def __enter__(self):
            self.old_widget = self.serie_definition_widget.blockSignals(True)
            self.old_tree = self.serie_definition_widget._tree.blockSignals(True)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.serie_definition_widget.blockSignals(self.old_widget)
            self.serie_definition_widget._tree.blockSignals(self.old_tree)

    def __init__(self, parent=None, serie_name="my_serie") -> None:
        self._tomo_objs = {}
        # associated serie name (key) to tuple (serie, QTreeWidgetItem)
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._tree = qt.QTreeWidget(self)
        self._tree.setSelectionMode(qt.QAbstractItemView.MultiSelection)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("series", "scan ids"))
        self._tree.setItemsExpandable(False)
        self.layout().addWidget(self._tree)

        # set up the tree with the serie name that will stay during the entire
        # life time of the tree
        self._seriesItem = qt.QTreeWidgetItem(self._tree)
        self._seriesItem.setFlags(self._seriesItem.flags() | qt.Qt.ItemIsEditable)
        self._seriesItem.setExpanded(True)

        self.setAcceptDrops(True)

        # connect signal / slot
        self._tree.itemChanged.connect(self._updated)

        # set up
        self.setSeriesName(name=serie_name)

        # expose API
        self.itemChanged = self._tree.itemChanged

    @property
    def rootItem(self):
        return self._seriesItem

    def setSeriesName(self, name: str):
        with self.SignalBlocker(self):
            self._seriesItem.setText(0, name)
        self.sigUpdated.emit()

    def getSeriesName(self):
        return self._seriesItem.text(0)

    def addTomoObj(self, tomo_obj: TomwerObject):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"{tomo_obj} is expected to be an instance of {TomwerObject} not {type(tomo_obj)}"
            )
        identifier = tomo_obj.get_identifier().to_str()
        if identifier in self._tomo_objs:
            _logger.warning(f"scan {identifier} already part of the serie")
            return

        with self.SignalBlocker(self):
            tomo_obj_item = qt.QTreeWidgetItem(self.rootItem)
            tomo_obj_item.setText(1, identifier)
            tomo_obj_item.setFlags(tomo_obj_item.flags() | qt.Qt.ItemIsUserCheckable)
            self._tomo_objs[identifier] = (tomo_obj, tomo_obj_item)
        self.sigUpdated.emit()

    def removeTomoObj(self, tomo_obj: TomwerObject):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"{tomo_obj} is expected to be an instance of {TomwerObject} not {type(tomo_obj)}"
            )

        with self.SignalBlocker(self):
            identifier = tomo_obj.get_identifier().to_str()
            if identifier not in self._tomo_objs:
                _logger.warning(f"{identifier} is not in the serie")
            else:
                _, tomo_obj_item = self._tomo_objs.pop(identifier)
                root = self._tree.invisibleRootItem()
                root.removeChild(tomo_obj_item)
        self.sigUpdated.emit()

    @property
    def n_tomo_objs(self):
        return len(self._tomo_objs)

    def setSeries(self, series: Series) -> None:
        if not isinstance(series, Series):
            raise TypeError(
                f"serie is expected to be an instance of {Series} not {type(series)}"
            )

        with self.SignalBlocker(self):
            self.clearTomoObjs()
            self.setSeriesName(series.name)
            for tomo_obj in series:
                if isinstance(tomo_obj, str):
                    try:
                        tomo_obj = ScanFactory.create_tomo_object_from_identifier(
                            identifier=tomo_obj
                        )
                    except Exception:
                        try:
                            tomo_obj = VolumeFactory.create_tomo_object_from_identifier(
                                identifier=tomo_obj
                            )
                        except Exception:
                            _logger.warning(f"Fail to recreate scan from {tomo_obj}.")
                            return
                elif not isinstance(tomo_obj, TomwerObject):
                    raise TypeError(
                        f"tomo_obj is expected to be an instance of {TomwerObject}. Not {type(tomo_obj)}"
                    )
                self.addTomoObj(tomo_obj)
        self.sigUpdated.emit()

    def getSeries(self, use_identifiers=False) -> Series:
        scans = [scan for scan, _ in self._tomo_objs.values()]
        return Series(
            name=self.getSeriesName(),
            iterable=scans,
            use_identifiers=use_identifiers,
        )

    def clearTomoObjs(self):
        with self.SignalBlocker(self):
            keys = list(self._tomo_objs.keys())
            for key in keys:
                _, scan_item = self._tomo_objs.pop(key)
                root = self._tree.invisibleRootItem()
                root.removeChild(scan_item)
        self.sigUpdated.emit()

    def setSelectedTomoObjs(self, objs):
        self.clearSelection()
        for scan in objs:
            scan_item = self._getTomoObjItem(scan)
            if scan_item is not None:
                scan_item.setSelected(True)

    def _getTomoObjItem(self, tomo_obj: TomwerObject) -> qt.QTreeWidgetItem | None:
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"scan is expected to be an instance of {TomwerObject} not {type(tomo_obj)}"
            )
        return self._tomo_objs.get(tomo_obj.get_identifier().to_str(), (None, None))[1]

    def getSelectedTomoObjs(self) -> tuple():
        """return selected scans"""
        selected = []
        for _, (scan, item) in self._tomo_objs.items():
            if item.isSelected():
                selected.append(scan)
        return tuple(selected)

    def removeSelectedTomoObjs(self) -> None:
        with self.SignalBlocker(self):
            for tomo_obj in self.getSelectedTomoObjs():
                self.removeTomoObj(tomo_obj)

    def _updated(self, *args, **kwargs):
        self.sigUpdated.emit()

    def clearSelection(self) -> None:
        self._tree.selectionModel().clearSelection()

    def addScanFromNxFile(self, file_: str, entry: str | None = None):
        try:
            if entry is None:
                scans = ScanFactory.create_scan_objects(scan_path=file_)
            else:
                scans = [ScanFactory.create_scan_object(scan_path=file_, entry=entry)]
        except Exception as e:
            _logger.error(f"cannot create scan instances from {file_}. Error is {e}")
        else:
            changed = False
            with self.SignalBlocker(self):
                for scan in scans:
                    if scan is not None:
                        try:
                            self.addTomoObj(tomo_obj=scan)
                        except TypeError:
                            _logger.error(
                                f"fail to add scan {scan}. Invalid type encountered ({type(scan)})"
                            )
                        else:
                            changed = True
            if changed:
                self.sigUpdated.emit()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            for url in event.mimeData().urls():
                self.addScanFromNxFile(file_=str(url.path()), entry=None)

    def supportedDropActions(self):
        """Inherited method to redefine supported drop actions."""
        return qt.Qt.CopyAction | qt.Qt.MoveAction

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.accept()
            event.setDropAction(qt.Qt.CopyAction)
        else:
            qt.QListWidget.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.setDropAction(qt.Qt.CopyAction)
            event.accept()
        else:
            qt.QListWidget.dragMoveEvent(self, event)


class SeriesManualControlDialog(qt.QDialog):
    """
    Same as the :class:`SeriesManualDefinitionDialog` but with control of the serie.
    This include a `create series` and a `create series and clear button`
    """

    sigSeriesSend = qt.Signal(Series)
    """Signal emit when a series has been send"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._mainWidget = SeriesManualDefinitionDialog(parent=self)
        self._mainWidget.setWindowFlags(qt.Qt.Widget)
        self.layout().addWidget(self._mainWidget)

        self._buttons = qt.QDialogButtonBox(parent=self)
        self._createButton = qt.QPushButton("create serie", parent=self)
        self._buttons.addButton(self._createButton, qt.QDialogButtonBox.ActionRole)

        # connect signal / slot
        self._createButton.clicked.connect(self._sendSeries)
        self.layout().addWidget(self._buttons)

        # expose API
        self.sigUpdated = self._mainWidget.sigUpdated

    def _sendSeries(self):
        self.sigSeriesSend.emit(self._mainWidget.getSeries())

    @property
    def n_tomo_objs(self):
        return self._mainWidget.n_tomo_objs

    def setSeriesName(self, name: str):
        self._mainWidget.setSeriesName(name=name)

    def getSeriesName(self) -> str:
        return self._mainWidget.getSeriesName()

    def setSeries(self, series: Series) -> None:
        self._mainWidget.setSeries(series)

    def getSeries(self, *args, **kwargs) -> Series:
        return self._mainWidget.getSeries(*args, **kwargs)

    def addScanFromNxFile(self, file_: str, entry: str | None = None):
        return self._mainWidget.addScanFromNxFile(file_=file_, entry=entry)

    def removeSelectedScans(self) -> None:
        return self._mainWidget.removeSelectedTomoObjs()

    def getSelectedScans(self) -> tuple:
        return self._mainWidget.getSelectedTomoObjs()

    def setSelectedScans(self, scans: Iterable) -> None:
        self._mainWidget.setSelectedTomoObjs(scans=scans)

    def addScan(self, scan: TomwerScanBase) -> None:
        self._mainWidget.addTomoObj(scan=scan)

    def removeScan(self, scan: TomwerScanBase) -> None:
        self._mainWidget.removeTomoObj(scan=scan)

    def clearSeries(self) -> None:
        self._mainWidget.clearSeries()

    def createSeries(self):
        self.sigSeriesSend.emit(self.getSeries())


class SeriesManualFromTomoObj(qt.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        style = qt.QApplication.style()
        self.setLayout(qt.QGridLayout())

        # tomo objs list
        self._tomoObjList = TomoObjList(self)
        self._tomoObjList.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding
        )
        self._tomoObjListScrollArea = qt.QScrollArea(self)
        self._tomoObjListScrollArea.setWidgetResizable(True)
        self._tomoObjListScrollArea.setWidget(self._tomoObjList)
        self.layout().addWidget(self._tomoObjListScrollArea, 0, 0, 4, 2)

        # right arrow
        self._rightArrowButton = qt.QPushButton(self)
        rightArrowIcon = style.standardIcon(qt.QStyle.SP_ArrowRight)
        self._rightArrowButton.setIcon(rightArrowIcon)
        self._rightArrowButton.setFixedWidth(30)
        self.layout().addWidget(self._rightArrowButton, 1, 2, 1, 1)

        # left arrow
        self._leftArrowButton = qt.QPushButton(self)
        leftArrowIcon = style.standardIcon(qt.QStyle.SP_ArrowLeft)
        self._leftArrowButton.setIcon(leftArrowIcon)
        self._leftArrowButton.setFixedWidth(30)
        self.layout().addWidget(self._leftArrowButton, 2, 2, 1, 1)

        # new series
        self._newSeriesWidget = NewSeriesWidget(self)
        self._newSerieWidgetScrollArea = qt.QScrollArea(self)
        self._newSerieWidgetScrollArea.setWidgetResizable(True)
        self._newSerieWidgetScrollArea.setWidget(self._newSeriesWidget)
        self.layout().addWidget(self._newSerieWidgetScrollArea, 0, 3, 4, 2)

        # tomo obj details
        self._tomoObjInfos = TomoObjOverview(self)
        self._tomoObjInfos.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._tomoObjInfos, 4, 0, 2, 2)

        # connect signals / slot
        self._leftArrowButton.released.connect(self._removeSelectedObjs)
        self._rightArrowButton.released.connect(self._addSelectedObjs)
        self._tomoObjList.selectionModel().selectionChanged.connect(
            self._updateTomoObjInfos
        )

    def selectedTomoObjects(self) -> tuple:
        """
        :return: tuple of tomo object selected on the list
        """
        items = self._tomoObjList.selectedItems()
        return [item.data(qt.Qt.UserRole) for item in items]

    def _removeSelectedObjs(self, *args, **kwargs):
        for tomo_obj in self.selectedTomoObjects():
            self._newSeriesWidget.removeTomoObjToCurrentSeries(tomo_obj)

    def _addSelectedObjs(self, *args, **kwargs):
        for tomo_obj in self.selectedTomoObjects():
            self._newSeriesWidget.addTomoObjToCurrentSeries(tomo_obj)

    def _updateTomoObjInfos(self, *args, **kwargs):
        # should
        select_objs = self._tomoObjList.selectedItems()
        if select_objs and len(select_objs) > 0:
            tomo_obj = select_objs[0].data(qt.Qt.UserRole)
            self._tomoObjInfos.setTomoObj(tomo_obj)
        else:
            self._tomoObjInfos.setTomoObj(None)

    # expose API
    def setSeries(self, series: Series):
        self._newSeriesWidget.setSeries(series=series)

    def getSeries(self, *args, **kwargs) -> Series:
        return self._newSeriesWidget.getSeries(*args, **kwargs)

    def addTomoObj(self, tomo_obj):
        self._tomoObjList.add(tomo_obj)

    def addToCurrentSeries(self, tomo_obj):
        self._newSeriesWidget.addTomoObjToCurrentSeries(tomo_obj)

    def setSeriesName(self, name: str):
        self._newSeriesWidget.setSeriesName(name=name)


class NewSeriesWidget(qt.QWidget):
    sigNameChanged = qt.Signal()
    """Emit when serie name changed"""

    sigUpdated = qt.Signal()
    """
    Emit when the serie has been updated by the tree
    """

    DEFAULT_SERIES_NAME = "my_series"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self._nameWidget = qt.QWidget(self)
        self._nameWidget.setLayout(qt.QHBoxLayout())
        self._nameWidget.layout().addWidget(qt.QLabel("series name", self))
        self._nameQLE = qt.QLineEdit(self.DEFAULT_SERIES_NAME, self)
        self._nameWidget.layout().addWidget(self._nameQLE)
        self.layout().addWidget(self._nameWidget)

        self._serieTree = _SeriesDefinitionTree(
            self, serie_name=self.DEFAULT_SERIES_NAME
        )
        self.layout().addWidget(self._serieTree)

        # Signal / slot connection
        self._serieTree.itemChanged.connect(self._handleItemUpdate)
        self._serieTree.sigUpdated.connect(self.sigUpdated)
        self._nameQLE.textChanged.connect(self._nameChangedOnQLE)

    def setSeries(self, series: Series) -> None:
        with blockSignals(self._nameQLE):
            self._nameQLE.setText(series.name)
        self._serieTree.setSeries(series=series)

    def getSeries(self, *args, **kwargs) -> Series:
        return self._serieTree.getSeries(*args, **kwargs)

    def _nameChangedOnQLE(self, name):
        with blockSignals(self._serieTree):
            self._serieTree.setSeriesName(name)
        self.sigNameChanged.emit()

    def _handleItemUpdate(self, item, column):
        if item == self._serieTree.rootItem:
            old = self.blockSignals(True)
            self._nameQLE.setText(self._serieTree.rootItem.text(0))
            self.blockSignals(old)
        self.sigUpdated.emit()

    def addTomoObjToCurrentSeries(self, tomo_obj: TomwerObject):
        assert isinstance(
            tomo_obj, TomwerObject
        ), f"invalid type {type(tomo_obj)}. {TomwerObject} expected"
        self._serieTree.addTomoObj(tomo_obj)

    def removeTomoObjToCurrentSeries(self, tomo_obj: TomwerObject):
        assert isinstance(
            tomo_obj, TomwerObject
        ), f"invalid type {type(tomo_obj)}. {TomwerObject} expected"
        self._serieTree.removeTomoObj(tomo_obj)

    def getSeriesName(self) -> str:
        return self._serieTree.getSeriesName()

    def setSeriesName(self, name: str):
        self._serieTree.setSeriesName(name=name)


class SeriesManualDefinitionDialog(qt.QDialog):
    """Dialog to define a serie manually"""

    sigUpdated = qt.Signal()
    """emit when serie is updated"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self._newSeriesWidget = NewSeriesWidget(self)

        self._buttons = qt.QDialogButtonBox(parent=self)

        self._addScanButton = qt.QPushButton("Add scan to the serie", parent=self)
        self._buttons.addButton(self._addScanButton, qt.QDialogButtonBox.ActionRole)

        self._removeSelectedButton = qt.QPushButton(
            "Remove selected scans", parent=self
        )
        self._buttons.addButton(
            self._removeSelectedButton, qt.QDialogButtonBox.ActionRole
        )

        self._clearButton = qt.QPushButton("Clear", parent=self)
        self._buttons.addButton(self._clearButton, qt.QDialogButtonBox.ActionRole)

        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._newSeriesWidget.sigNameChanged.connect(self._nameChanged)
        self._newSeriesWidget.sigUpdated.connect(self.sigUpdated)
        self._addScanButton.clicked.connect(self.addScanFromFileDialog)
        self._removeSelectedButton.clicked.connect(self.removeSelectedTomoObjs)
        self._clearButton.clicked.connect(self.clearSeries)

    @property
    def n_tomo_objs(self):
        serieTree = self._newSeriesWidget._serieTree
        return serieTree.n_tomo_objs

    def _nameChanged(self, new_name):
        serieTree = self._newSeriesWidget._serieTree
        with blockSignals(self._serieTree):
            serieTree.setSeriesName(name=new_name)
        self.sigUpdated.emit()

    def setSeriesName(self, name: str):
        self._newSeriesWidget.setSeriesName(name=name)

    def getSeriesName(self) -> str:
        return self._newSeriesWidget.getSeriesName()

    def setSeries(self, series: Series) -> None:
        self._newSeriesWidget.setSeries(series)

    def getSeries(self, *args, **kwargs) -> Series:
        return self._newSeriesWidget.getSeries(*args, **kwargs)

    def addScanFromFileDialog(self) -> None:
        dialog = QDataDialog(self, multiSelection=True)

        if not dialog.exec():
            dialog.close()
            return

        foldersSelected = dialog.files_selected()
        for folder in foldersSelected:
            self.addScanFromNxFile(file_=folder, entry=None)

    def addScanFromNxFile(self, file_: str, entry: str | None = None):
        serieTree = self._newSeriesWidget._serieTree
        return serieTree.addScanFromNxFile(file_=file_, entry=entry)

    def removeSelectedTomoObjs(self) -> None:
        serieTree = self._newSeriesWidget._serieTree
        return serieTree.removeSelectedTomoObjs()

    def getSelectedTomoObjs(self) -> tuple:
        serieTree = self._newSeriesWidget._serieTree
        return serieTree.getSelectedTomoObjs()

    def setSelectedTomoObjs(self, scans: Iterable) -> None:
        serieTree = self._newSeriesWidget._serieTree
        serieTree.setSelectedTomoObjs(objs=scans)

    def addTomoObj(self, scan: TomwerScanBase) -> None:
        serieTree = self._newSeriesWidget._serieTree
        return serieTree.addTomoObj(tomo_obj=scan)

    def removeTomoObj(self, scan: TomwerScanBase) -> None:
        serieTree = self._newSeriesWidget._serieTree
        serieTree.removeTomoObj(tomo_obj=scan)

    def clearSeries(self) -> None:
        serieTree = self._newSeriesWidget._serieTree
        serieTree.clearTomoObjs()


class SeriesAutomaticDefinitionWidget(qt.QWidget):
    pass


class SeriesTree(qt.QWidget):
    """
    Widget used to define a scan series from a list of scans.
    """

    def __init__(self, parent=None, scans=tuple()) -> None:
        self._series = {}
        # associated series name (key) to tuple (series, QTreeWidgetItem)
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._tree = qt.QTreeWidget(self)
        self._tree.setSelectionMode(qt.QAbstractItemView.MultiSelection)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("series", "scan ids"))
        self.layout().addWidget(self._tree)

        # set up
        [self.addSeries(scan) for scan in scans]

    def addSeries(self, series: Series):
        if not isinstance(series, Series):
            raise TypeError(
                f"{series} is expected to be an instance of {Series} not {type(series)}"
            )
        if series.name in self._series:
            self.removeSeries(self._series[series.name][0])

        root_item = qt.QTreeWidgetItem(self._tree)
        root_item.setText(0, series.name)
        self._series[series.name] = (series, root_item)
        for obj in series:
            scan_item = qt.QTreeWidgetItem(root_item)
            if isinstance(obj, TomwerObject):
                text = obj.get_identifier().to_str()
            else:
                text = obj
            scan_item.setText(1, text)
            scan_item.setFlags(qt.Qt.NoItemFlags)

    def removeSeries(self, series: Series):
        if not isinstance(series, Series):
            raise TypeError(
                f"{series} is expected to be an instance of {Series} not {type(series)}"
            )
        if series.name in self._series:
            _, serie_item = self._series.pop(series.name)
            root = self._tree.invisibleRootItem()
            root.removeChild(serie_item)

    @property
    def n_series(self):
        return len(self._series)

    def series(self) -> tuple:
        series = []
        [series.append(serie) for serie, _ in self._series.values()]
        return tuple(series)

    def clearSelection(self):
        self._tree.selectionModel().clearSelection()

    def setSelectedSeries(self, series):
        self.clearSelection()
        for serie in series:
            serie_item = self._getSeriesItem(serie)
            if serie_item is not None:
                serie_item.setSelected(True)

    def _getSeriesItem(self, series: Series) -> qt.QTreeWidgetItem | None:
        if not isinstance(series, Series):
            raise TypeError(
                f"serie is expected to be an instance of {Series} not {type(series)}"
            )
        return self._series.get(series.name, (None, None))[1]

    def getSelectedSeries(self) -> tuple():
        """return selected series"""
        selected = []
        for _, (series, item) in self._series.items():
            if item.isSelected():
                selected.append(series)
        return tuple(selected)

    def removeSelected(self) -> None:
        for series in self.getSelectedSeries():
            self.removeSeries(series)


class SeriesHistoryDialog(qt.QDialog):
    sigSeriesSend = qt.Signal(Series)
    """signal emit when a serie has been selected by the user"""

    sigEditSeries = qt.Signal(Series)
    """Signal emit when user request to edit a serie"""

    sigHistoryUpdated = qt.Signal()
    """Signal emit when the history has been modified"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self._serieList = SeriesTree(self)
        self.layout().addWidget(self._serieList)

        self._buttons = qt.QDialogButtonBox(parent=self)

        self._editButton = qt.QPushButton("Edit", parent=self)
        self._buttons.addButton(self._editButton, qt.QDialogButtonBox.ActionRole)

        self._sendButton = qt.QPushButton("Resend", parent=self)
        self._buttons.addButton(self._sendButton, qt.QDialogButtonBox.ActionRole)

        self._removeButton = qt.QPushButton("Remove", parent=self)
        self._buttons.addButton(self._removeButton, qt.QDialogButtonBox.ActionRole)

        self._clearButton = qt.QPushButton("Clear", parent=self)
        self._buttons.addButton(self._clearButton, qt.QDialogButtonBox.ActionRole)

        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._sendButton.clicked.connect(self.sendSelected)
        self._removeButton.clicked.connect(self.removeSelected)
        self._clearButton.clicked.connect(self.clearSelection)
        self._editButton.clicked.connect(self.editSelected)

    def addSeries(self, serie: Series):
        old = self.blockSignals(True)
        self._serieList.addSeries(serie)
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def removeSeries(self, serie: Series):
        old = self.blockSignals(True)
        self._serieList.removeSeries(serie)
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def getSelectedSeries(self):
        return self._serieList.getSelectedSeries()

    def setSelectedSeries(self, series):
        old = self.blockSignals(True)
        self._serieList.setSelectedSeries(series)
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def sendSelected(self):
        for serie in self.getSelectedSeries():
            self.sigSeriesSend.emit(serie)

    def editSelected(self):
        selected = self.getSelectedSeries()
        if len(selected) == 0:
            return
        if len(selected) > 1:
            _logger.warning(
                "more than one serie selected for edition. Will only edit the first one"
            )
        self.sigEditSeries.emit(selected[0])

    def removeSelected(self):
        old = self.blockSignals(True)
        self._serieList.removeSelected()
        self.blockSignals(old)
        self.sigHistoryUpdated.emit()

    def clearSelection(self):
        self._serieList.clearSelection()

    def series(self) -> tuple:
        return self._serieList.series()
