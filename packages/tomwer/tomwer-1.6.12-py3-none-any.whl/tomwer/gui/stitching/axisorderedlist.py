"""widgets to perform a z-sttiching in pre processing (from projections) or post processing (from reconstructed volumes)"""

from __future__ import annotations


import logging

from silx.gui import qt
from silx.gui.utils import blockSignals
from tomoscan.scanbase import TomoScanBase
from tomoscan.series import Series

from tomwer.io.utils.tomoobj import get_tomo_objs_instances
from tomwer.core.tomwer_object import TomwerObject
from tomwer.gui.stitching.metadataholder import QStitchingMetadata
from tomwer.gui.utils.illustrations import _IllustrationWidget
from .singleaxis import _SingleAxisMixIn

_logger = logging.getLogger(__name__)


class AxisOrderedTomoObjWidget(qt.QWidget, _SingleAxisMixIn):
    """
    main widget to define configuration of a z-stitching
    """

    sigConfigChanged = qt.Signal()
    """emit when the configuration changed"""
    sigAddTomoObjRequest = qt.Signal(TomwerObject)
    """request when a file is dropped or added through the 'add button'."""
    sigRemoveObjRequest = qt.Signal(TomwerObject)
    """request when an object should be removed by calling the 'remove button'."""

    def __init__(self, axis: int, parent=None):
        super().__init__(parent=parent)
        if axis not in (0, 1, 2):
            raise ValueError(f"axis should be in (0, 1, 2). Got {axis}")
        self._axis = axis  # implement _SingleAxisMixIn interface
        self.setLayout(qt.QGridLayout())

        self._addTomoObjCallbacks = tuple()
        self._removetomoObjCallbacks = tuple()

        # left panel with arrow
        img_flow = "flow_down"
        left_panel_width = 50
        axis_label = self.axis_alias(axis)
        self._axisLabel = qt.QLabel(axis_label, parent=self)
        self._axisLabel.setToolTip(f"{axis_label} is also know as axis {axis}")
        font = self._axisLabel.font()
        font.setPixelSize(40)
        self._axisLabel.setFont(font)
        self._axisLabel.setAlignment(qt.Qt.AlignCenter)
        self._axisLabel.setFixedWidth(left_panel_width)
        self.layout().addWidget(self._axisLabel, 1, 0, 1, 1)

        self._flowIllustration = _IllustrationWidget(parent=self, img=img_flow)
        self._flowIllustration.setFixedWidth(left_panel_width)
        self._flowIllustration.setSizePolicy(
            qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding
        )
        self.layout().addWidget(self._flowIllustration, 2, 0, 1, 1)
        self._flowIllustration.setToolTip(
            f"we are first ordering tomo object along axis {axis} (aka {self.axis_alias(axis)}) position to apply stitching"
        )

        # central object list
        self._tomoObjsTableView = qt.QTableView(parent=self)
        self._tomoObjsTableView.setModel(
            AxisOrderedTomoObjsModel(parent=self._tomoObjsTableView, axis=axis)
        )
        self._tomoObjsTableView.setSelectionBehavior(qt.QAbstractItemView.SelectRows)

        self._tomoObjsTableView.horizontalHeader().setStretchLastSection(True)
        self._tomoObjsTableView.setSortingEnabled(False)
        self._tomoObjsTableView.setColumnWidth(0, 20)
        self._tomoObjsTableView.setDragEnabled(True)
        self._tomoObjsTableView.setAcceptDrops(True)

        self.layout().addWidget(self._tomoObjsTableView, 2, 1, 1, 1)

    def addTomoObj(self, tomo_obj: TomoScanBase, trigger_callbacks=False):
        if tomo_obj is None:
            return
        else:
            self._tomoObjsTableView.model().addTomoObj(tomo_obj)
            # register tomo obj metadata modification to make sure we tell the z ordered list up to data
            tomo_obj.stitching_metadata.sigChanged.connect(self._orderMightHaveChanged)
            if trigger_callbacks:
                for callback in self._addTomoObjCallbacks:
                    callback(tomo_obj)

    def removeTomoObj(self, tomo_obj, trigger_callbacks=False):
        self._tomoObjsTableView.model().removeTomoObj(tomo_obj)
        tomo_obj.stitching_metadata.sigChanged.disconnect(self._orderMightHaveChanged)
        if trigger_callbacks:
            for callback in self._removetomoObjCallbacks:
                callback(tomo_obj)

    def _orderMightHaveChanged(self):
        # when position over {axis} is updated from the GUI, make sure the {axis} ordered list of tomo object is still
        # ordered and selection is still the accurate one.
        # this case is not handled on this widget
        self._tomoObjsTableView.model().reorder_objs()

    def getTomoObjsAxisOrdered(self) -> tuple:
        return tuple(self._tomoObjsTableView.model()._axis_decreasing_ordered_objs)

    def clearTomoObjs(self):
        self._tomoObjsTableView.model().clearTomoObjs()


class AxisOrderedTomoObjsModel(qt.QAbstractTableModel):
    def __init__(self, axis: int, parent=None) -> None:
        super().__init__(parent)
        assert axis in (0, 1, 2)
        self._axis = axis
        # either we plot the tomo_obj in the list within the full identifier or with the reduce str (in this case two scans can have identical name. Identifier is unique)
        self._objs = Series(name="unordered tomo obj", use_identifiers=False)
        self._axis_decreasing_ordered_objs = []
        self._headers = ["index", "tomo obj"]
        self._tomoObjToIndex = {}
        # for each tomo object store a 'unique' id
        self._nextIndex = -1

    def supportedDragActions(self):
        return qt.Qt.CopyAction

    def supportedDropActions(self):
        return qt.Qt.CopyAction

    def getTomoObjs(self) -> tuple:
        return tuple(self._objs)

    def pop_index(self):
        self._nextIndex += 1
        return self._nextIndex

    def getTomoObjCurrentPos(self, tomo_obj):
        try:
            index = self._axis_decreasing_ordered_objs.index(tomo_obj)
        except ValueError:  # if not in the list
            return -1
        else:
            return index

    def clearTomoObjs(self):
        self._objs = Series(name="unordered tomo obj", use_identifiers=False)
        self._axis_decreasing_ordered_objs = []
        self.layoutChanged.emit()

    def reorder_objs(self):
        def get_min_axis_or_0(tomo_obj):
            # expects to find a position. If cannot set the value to infinity to be sure all tomo objects without
            # metadata (raw or from the user) are at the specific position
            return (
                tomo_obj.stitching_metadata.get_abs_position_px(axis=self._axis) or 0.0
            )

        self._axis_decreasing_ordered_objs = Series(
            "ordered tomo obj",
            sorted(self._objs[:], key=get_min_axis_or_0, reverse=True),
            use_identifiers=False,
        )

    def addTomoObj(self, obj: TomwerObject):
        if not isinstance(obj, TomwerObject):
            raise TypeError(
                f"{obj} is expected to be an instance of {TomwerObject}. {type(obj)} provided instead"
            )
        elif obj.stitching_metadata is None:
            # make sure it can contain some stitching metadata
            obj.stitching_metadata = QStitchingMetadata(tomo_obj=obj)
        elif not isinstance(obj.stitching_metadata, QStitchingMetadata):
            # if need to upgrade it to a QObject
            obj.stitching_metadata = QStitchingMetadata.from_dict(
                obj.stitching_metadata.to_dict(), tomo_obj=obj
            )
        self._objs.append(obj)
        identifier = obj.get_identifier().to_str()
        if identifier not in self._tomoObjToIndex:
            self._tomoObjToIndex[identifier] = self.pop_index()
        self.reorder_objs()
        self.layoutChanged.emit()

    def removeTomoObj(self, obj: TomwerObject):
        if not isinstance(obj, TomwerObject):
            raise TypeError(
                f"{obj} is expected to be an instance of {TomwerObject}. {type(obj)} provided instead"
            )
        self._objs.remove(obj)
        # note: we avoid removing the identifier as this is pretty small and convenient to keep
        # in case of wromg manipulation when removing an item
        self.reorder_objs()
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self._objs)

    def columnCount(self, parent=None):
        return len(self._headers)

    def headerData(self, col, orientation, role):
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            if col < len(self._headers):
                return self._headers[col]
            else:
                return None

    def getTomoObj(self, qmodelindex: qt.QModelIndex):
        index = qmodelindex.row()
        if index < len(self._axis_decreasing_ordered_objs):
            return self._axis_decreasing_ordered_objs[index]

    def data(self, index, role):
        if not index.isValid():
            return None

        if index.column() == 0:
            if role == qt.Qt.TextAlignmentRole:
                return qt.Qt.AlignLeft | qt.Qt.AlignVCenter
            elif role == qt.Qt.DisplayRole:
                obj = self._axis_decreasing_ordered_objs[index.row()]
                identifier = obj.get_identifier().to_str()
                return self._tomoObjToIndex.get(identifier, "???")
        elif index.column() == 1:
            if role == qt.Qt.TextAlignmentRole:
                return qt.Qt.AlignHCenter | qt.Qt.AlignVCenter
            elif role == qt.Qt.ToolTipRole:
                obj = self._axis_decreasing_ordered_objs[index.row()]
                return obj.get_identifier().to_str()
            elif role == qt.Qt.DisplayRole:
                obj = self._axis_decreasing_ordered_objs[index.row()]
                return obj.get_identifier().short_description()
            else:
                return None
        else:
            return None


class AxisOrderedTomoObjWidgetSingleSel(AxisOrderedTomoObjWidget):
    """
    AxisOrderedTomoObjWidget with a list that can select a single line.

    The idea is that it can be used to select the object to be edited on another widget
    """

    def __init__(self, axis: int, parent=None):
        super().__init__(axis=axis, parent=parent)
        self._tomoObjsTableView.setSelectionMode(qt.QAbstractItemView.SingleSelection)

    def removeTomoObj(self, tomo_obj):
        selected = self.getSelectedTomoObj()
        super().removeTomoObj(tomo_obj=tomo_obj)
        if selected is tomo_obj:
            self.setSelectedTomoObj(None)
        else:
            self.setSelectedTomoObj(selected)

    def getSelectedTomoObj(self):
        selection = self._tomoObjsTableView.selectedIndexes()
        if len(selection) > 0:
            return self._tomoObjsTableView.model().getTomoObj(selection[0])
        return None

    def setSelectedTomoObj(self, tomo_obj: TomwerObject | None):
        self._tomoObjsTableView.selectionModel().clearSelection()
        if tomo_obj is not None:
            model = self._tomoObjsTableView.model()
            tomo_obj_ordered_row = model.getTomoObjCurrentPos(tomo_obj=tomo_obj)

            if tomo_obj_ordered_row >= 0:
                for i_column in range(model.columnCount()):
                    selection = model.createIndex(
                        tomo_obj_ordered_row,
                        i_column,
                    )
                    self._tomoObjsTableView.selectionModel().select(
                        selection,
                        qt.QItemSelectionModel.Select,
                    )

    def _orderMightHavechanged(self):
        # when z position is updated from the GUI, make sure the z ordered list of tomo object is still
        # ordered and selection is still the accurate one.
        with blockSignals(self._tomoObjsTableView.selectionModel()):
            selectedTomoObj = self.getSelectedTomoObj()
            self._tomoObjsTableView.model().reorder_objs()
            self._tomoObjsTableView.model().layoutChanged.emit()
            self.setSelectedTomoObj(selectedTomoObj)


class EditableOrderedTomoObjWidget(AxisOrderedTomoObjWidget):
    """
    same as the ZOrderedTomoObjWidget but you can add and remove tomo obj to the list
    """

    def __init__(self, axis: int, parent=None):
        super().__init__(axis=axis, parent=parent)
        if axis not in (0, 1, 2):
            raise ValueError(f"axis must be in (0, 1, 2). Got {axis}")
        self._axis = axis
        self.setAcceptDrops(True)

        # allow multiple selection as we might want to remove several object at the same time
        self._tomoObjsTableView.setSelectionMode(qt.QAbstractItemView.MultiSelection)

        self._buttons = qt.QWidget(self)
        self._buttons.setLayout(qt.QHBoxLayout())

        # allow drag and drop of elmts

        # create buttons
        ## spacer
        self._spacer = qt.QWidget(self._buttons)
        self._spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._buttons.layout().addWidget(self._spacer)
        ## add button
        self._addButton = qt.QPushButton("Add")
        self._addButton.clicked.connect(self._callbackAddTomoObj)
        self._buttons.layout().addWidget(self._addButton)
        ## rm button
        self._rmButton = qt.QPushButton("Remove")
        self._rmButton.clicked.connect(self._callbackRemoveSelectedTomoObj)
        self._buttons.layout().addWidget(self._rmButton)

        self.layout().addWidget(self._buttons, 999, 0, 1, 2)

    @property
    def axis(self) -> int:
        return self._axis

    def removeTomoObj(self, tomo_obj, trigger_callbacks=False):
        selected = set(self.getSelectedTomoObjs())
        super().removeTomoObj(tomo_obj=tomo_obj, trigger_callbacks=trigger_callbacks)
        if tomo_obj in selected:
            selected.remove(tomo_obj)
            self.setSelectedTomoObjs(selected)

    def setSelectedTomoObjs(self, tomo_objs):
        self._tomoObjsTableView.clearSelection()

        model = self._tomoObjsTableView.model()
        for tomo_obj in tomo_objs:
            tomo_obj_ordered_row = model.getTomoObjCurrentPos(tomo_obj=tomo_obj)

            if tomo_obj_ordered_row >= 0:
                for i_column in range(model.columnCount()):
                    selection = model.createIndex(
                        tomo_obj_ordered_row,
                        i_column,
                    )
                    self._tomoObjsTableView.selectionModel().select(
                        selection,
                        qt.QItemSelectionModel.Select,
                    )

    def getSelectedTomoObjs(self):
        selection = self._tomoObjsTableView.selectedIndexes()
        return set(
            [self._tomoObjsTableView.model().getTomoObj(item) for item in selection]
        )

    def _callbackAddTomoObj(self) -> tuple[TomwerObject]:
        dialog = qt.QFileDialog()
        dialog.setFileMode(qt.QFileDialog.ExistingFiles)
        dialog.setNameFilters(
            [
                "Any file (*)",
            ]
        )

        if not dialog.exec():
            dialog.close()
            return ()
        elif len(dialog.selectedFiles()) == 0:
            return ()
        else:
            tomo_objs = []
            for file in dialog.selectedFiles():
                try:
                    new_objs = get_tomo_objs_instances(tomo_objs=(file,))[0]
                except Exception:
                    pass
                else:
                    tomo_objs.extend(new_objs)
            for tomo_obj in tomo_objs:
                self.addTomoObj(tomo_obj=tomo_obj, trigger_callbacks=True)
            return tuple(tomo_objs)

    def _callbackRemoveSelectedTomoObj(self):
        obj_to_remove = self.getSelectedTomoObjs()
        for obj in obj_to_remove:
            self.removeTomoObj(tomo_obj=obj, trigger_callbacks=True)

    def dropEvent(self, a0) -> None:
        if a0.mimeData().hasFormat("text/uri-list"):
            paths = [url.path() for url in a0.mimeData().urls()]
            tomo_objs = get_tomo_objs_instances(paths)[0]

            for tomo_obj in tomo_objs:
                assert isinstance(
                    tomo_obj, TomwerObject
                ), f"expected type is tomo_obj. Get {type(tomo_obj)}"
                self.addTomoObj(tomo_obj=tomo_obj, trigger_callbacks=True)
        else:
            return super().dropEvent(a0)

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

    def setAddTomoObjCallbacks(self, callbacks: tuple):
        """
        To synchronize the different widget we might need to notify other widget that a tomo_obj has been added
        from the dedicated interface.
        Callbacks must take a single TomwerObject as input
        """
        self._addTomoObjCallbacks = callbacks

    def setRemoveTomoObjCallbacks(self, callbacks: tuple):
        """
        To synchronize the different widget we might need to notify other widget that a tomo_obj has been removed
        from the dedicated interface.
        Callbacks must take a single TomwerObject as input
        """
        self._removetomoObjCallbacks = callbacks

    def _orderMightHavechanged(self):
        # when z position is updated from the GUI, make sure the z ordered list of tomo object is still
        # ordered and selection is still the accurate one.
        with blockSignals(self._tomoObjsTableView.selectionModel()):
            selectedTomoObjs = self.getSelectedTomoObjs()
            self._tomoObjsTableView.model().reorder_objs()
            self._tomoObjsTableView.model().layoutChanged.emit()
            self.setSelectedTomoObjs(selectedTomoObjs)
