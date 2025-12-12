from __future__ import annotations


import functools
import numpy
from silx.gui import qt
from enum import Enum as _Enum

from tomwer.core.tomwer_object import TomwerObject
from tomwer.gui import icons
from tomwer.gui.stitching.axisorderedlist import AxisOrderedTomoObjsModel
from tomwer.gui.utils.step import StepSizeSelectorWidget
from tomwer.gui.utils.qt_utils import block_signals


class PosEditorOverOneAxis(qt.QWidget):
    """keep it ordered along one axis"""

    def __init__(
        self, parent, axis_edited: int, axis_order=None, *args, **kwargs
    ) -> None:
        assert axis_edited in (0, 1, 2)
        super().__init__(parent, *args, **kwargs)
        self._axisEdited = axis_edited
        # the axis we are editing
        self._axisOrder = axis_order if axis_order is not None else axis_edited
        # the axis along which the tomo obj are ordered
        self._tomoObjtoTomoObjPosWidget = {}
        # list of `_TomoObjPosition` to edit the position over the axis. Key is the tomo object, value is the `_TomoObjPosition`
        self.__tomoObjPosWidgetCallbacks = {}
        self.setLayout(qt.QVBoxLayout())
        # widget to define step size
        self._stepSizeWidget = StepSizeSelectorWidget(
            self,
            fine_value=1,
            medium_value=5,
            rough_value=25,
            dtype=int,
        )
        self.layout().addWidget(self._stepSizeWidget)

        # widget to define edition mode and reset
        self._editionOptionsWidget = _EditionOptions()
        self.layout().addWidget(self._editionOptionsWidget)

        # table with the different Tomo objects
        self._tomoObjsTableView = qt.QTableView(parent=self)
        model = EditableAxisOrderedTomoObjsModel(axis=axis_edited)
        self._tomoObjsTableView.setModel(model)

        self.layout().addWidget(self._tomoObjsTableView)

        # connect signal / slot
        self._stepSizeWidget.valueChanged.connect(self._updateStepSize)
        self._editionOptionsWidget.sigReset.connect(self._resetPositions)

        # tune table view
        self._tomoObjsTableView.setColumnWidth(0, 45)
        self._tomoObjsTableView.setColumnWidth(2, _TomoObjPosition.WIDGET_WIDTH)
        self._tomoObjsTableView.horizontalHeader().setSectionResizeMode(
            1, qt.QHeaderView.Stretch
        )
        self.setStepSize(1)

    def _updateStepSize(self):
        step_size = self.getStepSize()
        for sb in self._tomoObjtoTomoObjPosWidget.values():
            sb.setSingleStep(step_size)

    def setStepSize(self, step_size: int):
        self._stepSizeWidget.setStepSize(step_size)
        self._updateStepSize()

    def getStepSize(self) -> int:
        return self._stepSizeWidget.getStepSize()

    def getTomoObjs(self) -> tuple[TomwerObject]:
        return self._tomoObjsTableView.model().getTomoObjs()

    def addTomoObj(self, tomo_obj):
        if tomo_obj is None:
            return
        else:
            self._tomoObjsTableView.model().addTomoObj(tomo_obj)
            # register tomo obj metadata modification to make sure we keel the z ordered list up to data
            tomo_obj.stitching_metadata.sigChanged.connect(
                self._orderedMightHaveChanged
            )
            self._createTomoObjPosition(tomo_obj=tomo_obj)
            self._orderedMightHaveChanged()

    def _createTomoObjPosition(self, tomo_obj, original_value: float | None = None):
        """
        :param original_value: original_value of the tomo_obj along the edited axis. Used when the widget is delete and recreate
        """
        widget = _TomoObjPosition(
            tomo_obj=tomo_obj,
            axis_edited=self._axisEdited,
            original_value=original_value,
            parent=self,
        )
        widget.setSingleStep(self.getStepSize())

        identifier_as_str = tomo_obj.get_identifier().to_str()
        self._tomoObjtoTomoObjPosWidget[identifier_as_str] = widget
        # connect signal / slot
        callback = functools.partial(
            self._tomoObjPosChanged, spin_box=widget, tomo_obj_to_update=tomo_obj
        )
        self.__tomoObjPosWidgetCallbacks[identifier_as_str] = callback
        widget.sigValueChanged.connect(callback)
        return widget

    def _deleteTomoObjPosition(self, tomo_obj):
        identifier_as_str = tomo_obj.get_identifier().to_str()
        if identifier_as_str in self._tomoObjtoTomoObjPosWidget:
            spinBox = self._tomoObjtoTomoObjPosWidget.pop(  # noqa F841
                identifier_as_str
            )
            # indeed this should be called once 'self.__tomoObjPosWidgetCallbacks' disconnected.
            # never the less forcing deletion triggers issue 1457 (see https://gitlab.esrf.fr/tomotools/tomwer/-/issues/1457)
            # spinBox.deleteLater()
        if identifier_as_str in self.__tomoObjPosWidgetCallbacks:
            del self.__tomoObjPosWidgetCallbacks[identifier_as_str]

    def removeTomoObj(self, tomo_obj):
        self._deleteTomoObjPosition(tomo_obj)
        self._tomoObjsTableView.model().removeTomoObj(tomo_obj)
        tomo_obj.stitching_metadata.sigChanged.disconnect(self._orderedMightHaveChanged)

    def _tomoObjPosChanged(
        self,
        old_pos_value: int,
        new_pos_value: int,
        tomo_obj_to_update,
        *args,
        **kwargs,
    ):
        tomo_obj_to_update.stitching_metadata.setPxPos(
            new_pos_value, axis=self._axisEdited
        )
        # edit upstream or downstream nodes according to the edit mode
        shift = new_pos_value - old_pos_value
        if shift == 0:
            return

        edition_mode = self._editionOptionsWidget.getEditionMode()
        if edition_mode is _EditionMode.FREE:
            tomo_objs_to_update = ()
        elif edition_mode is _EditionMode.DOWNSTREAM:
            tomo_objs_to_update = self._get_downstream_tomo_obj(
                position=old_pos_value, tomo_obj_to_filter=tomo_obj_to_update
            )
        elif edition_mode is _EditionMode.UPSTREAM:
            tomo_objs_to_update = self._get_upstream_tomo_obj_pos_widgets(
                position=old_pos_value, tomo_obj_to_filter=tomo_obj_to_update
            )
        else:
            raise NotImplementedError(f"edition mode ({edition_mode}) is not handled")
        with block_signals(self):
            for tomo_obj_to_update in tomo_objs_to_update:
                associated_widget = self._tomoObjtoTomoObjPosWidget[
                    tomo_obj_to_update.get_identifier().to_str()
                ]
                current_value = associated_widget.getValue()
                assert (
                    current_value == associated_widget.getValue()
                ), "incoherent value between tomo object and widget"
                new_value = current_value + shift
                with block_signals(associated_widget):
                    associated_widget.setValue(new_value)
                with block_signals(tomo_obj_to_update.stitching_metadata):
                    tomo_obj_to_update.stitching_metadata.setPxPos(
                        value=new_value, axis=self._axisEdited
                    )
        self._orderedMightHaveChanged()

    def setTomoObjs(self, tomo_objs: tuple) -> None:
        """
        replace current list of object by the given list
        """
        self._tomoObjsTableView.model().clearTomoObjs()
        for tomo_obj in tomo_objs:
            self.addTomoObj(tomo_obj)

    def clean(self):
        tomo_objs = self._tomoObjsTableView.model().getTomoObjs()
        for tomo_obj in tomo_objs:
            self.removeTomoObj(tomo_obj=tomo_obj)

    def setSeries(self):
        raise NotImplementedError

    def _resetPositions(self):
        tomo_objs = self.getTomoObjs()

        with block_signals(self):
            for tomo_obj in tomo_objs:
                widget = self._tomoObjtoTomoObjPosWidget[
                    tomo_obj.get_identifier().to_str()
                ]
                with block_signals(widget):
                    widget.resetOriginalValue()
                    tomo_obj.stitching_metadata.setPxPos(
                        value=widget.getOriginalValue(), axis=self._axisEdited
                    )
        self._orderedMightHaveChanged()

    def _get_upstream_tomo_obj_pos_widgets(
        self, position: float, tomo_obj_to_filter: TomwerObject | None = None
    ) -> tuple[TomwerObject]:
        return tuple(
            filter(
                lambda tomo_obj: (
                    tomo_obj.stitching_metadata.get_abs_position_px(
                        axis=self._axisEdited
                    )
                    >= position
                )
                and (tomo_obj is not tomo_obj_to_filter),
                self.getTomoObjs(),
            )
        )

    def _get_downstream_tomo_obj(
        self, position: float, tomo_obj_to_filter: TomwerObject | None = None
    ) -> tuple[TomwerObject]:
        return tuple(
            filter(
                lambda tomo_obj: (
                    tomo_obj.stitching_metadata.get_abs_position_px(
                        axis=self._axisEdited
                    )
                    <= position
                )
                and (tomo_obj is not tomo_obj_to_filter),
                self.getTomoObjs(),
            )
        )

    def _orderedMightHaveChanged(self, force_sb_update=False):
        # add index widget
        self._tomoObjsTableView.model().reorder_objs()
        self._tomoObjsTableView.model().layoutChanged.emit()

        ordered_objs = self._tomoObjsTableView.model()._axis_decreasing_ordered_objs

        # start update position widgets
        # check if we need to update one widget. Has this is designed if we need to update one then we need to update them all...
        needs_to_update_widget = force_sb_update
        for i_pos, tomo_obj in enumerate(ordered_objs):
            identifier_as_str = tomo_obj.get_identifier().to_str()
            widget = self._tomoObjtoTomoObjPosWidget[identifier_as_str]
            model_index = self._tomoObjsTableView.model().createIndex(i_pos, 2)
            if self._tomoObjsTableView.indexWidget(model_index) not in (None, widget):
                needs_to_update_widget = True
                break

        for i_pos, tomo_obj in enumerate(ordered_objs):
            identifier_as_str = tomo_obj.get_identifier().to_str()
            widget = self._tomoObjtoTomoObjPosWidget[identifier_as_str]
            model_index = self._tomoObjsTableView.model().createIndex(i_pos, 2)
            if needs_to_update_widget:
                # if items have been reordered then we must recreated `TomoObjPosWidget` otherwise if we try
                # to change order then Qt will end up with a seg fault which seems to come from
                # overwriting the cell and trying to reuse them
                original_value = widget.getOriginalValue()
                self._deleteTomoObjPosition(tomo_obj=tomo_obj)
                widget = self._createTomoObjPosition(
                    tomo_obj=tomo_obj, original_value=original_value
                )
            self._tomoObjsTableView.setIndexWidget(model_index, widget)

    # expose API
    def getEditionMode(self) -> _EditionMode:
        return self._editionOptionsWidget.getEditionMode()

    def setEditionMode(self, edition_mode: _EditionMode) -> _EditionMode:
        self._editionOptionsWidget.setEditionMode(edition_mode=edition_mode)


class EditableAxisOrderedTomoObjsModel(AxisOrderedTomoObjsModel):
    def __init__(self, axis: int, parent=None) -> None:
        super().__init__(axis, parent)
        self._headers = ["index", "tomo obj", f"axis {axis} pos (px)"]


class _TomoObjPosition(qt.QWidget):
    """
    Widget used to define tomo object position over one axis (and reset if needed)

    :param original_value: original_value of the tomo_obj along the edited axis. Used when the widget is delete and recreate
    """

    WIDGET_WIDTH = 120

    RESET_BUTTON_WIDTH = 25

    DEFAULT_VALUE_WHEN_MISSING = 0

    sigValueChanged = qt.Signal(int, int)
    """emit when the value is changed. Parameters are (old value, new value)"""

    def __init__(
        self,
        tomo_obj,
        axis_edited: int,
        parent: qt.QWidget | None = None,
        original_value: float | None = None,
    ) -> None:
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        # create spin box object
        self._spinBox = qt.QSpinBox(self)
        self._spinBox.setRange(
            numpy.iinfo(numpy.int32).min, numpy.iinfo(numpy.int32).max
        )
        self._spinBox.setSuffix("px")
        currentPos = (
            tomo_obj.stitching_metadata.get_abs_position_px(axis=axis_edited)
            or self.DEFAULT_VALUE_WHEN_MISSING
        )
        self.__originalValue = original_value or currentPos
        self.__lastValue = self.__originalValue
        self._spinBox.setValue(currentPos)
        self._spinBox.setFixedWidth(self.WIDGET_WIDTH - self.RESET_BUTTON_WIDTH)
        self.layout().addWidget(self._spinBox)

        # create option to reset value
        self._resetValueQPB = qt.QPushButton(parent=self)
        self._resetValueQPB.setFixedWidth(self.RESET_BUTTON_WIDTH)
        style = qt.QApplication.style()
        resetIcon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        self._resetValueQPB.setIcon(resetIcon)
        self.layout().addWidget(self._resetValueQPB)

        # connect signal / slot
        self._spinBox.editingFinished.connect(self._sbEditingFinished)
        self._resetValueQPB.clicked.connect(self.resetOriginalValue)

    def _sbEditingFinished(self):
        sender = self.sender()
        assert isinstance(sender, qt.QSpinBox)
        new_value = sender.value()
        self._valueChanged(new_value=new_value)

    def _valueChanged(self, new_value):
        self.sigValueChanged.emit(
            self.__lastValue,
            new_value,
        )
        self.__lastValue = new_value

    def getOriginalValue(self) -> float:
        return self.__originalValue

    def setOriginalValue(self, value: float) -> None:
        self.__originalValue = value

    def resetOriginalValue(self) -> None:
        self._spinBox.setValue(self.getOriginalValue())
        self._positionChanged()

    def _positionChanged(self):
        self._valueChanged(self._spinBox.value())

    def setValue(self, value: float, emit_editing_finished: bool = False) -> None:
        self._spinBox.setValue(value)
        if emit_editing_finished:
            self._spinBox.editingFinished.emit()
        self.__lastValue = value

    def getValue(self) -> float:
        return self._spinBox.value()

    # expose API
    def setSingleStep(self, val: int):
        self._spinBox.setSingleStep(val)


class _EditionMode(_Enum):
    FREE = "free"
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"

    @staticmethod
    def get_icon(cls):
        if cls == cls.UPSTREAM:
            return icons.getQIcon("edit_upstream")
        elif cls == cls.DOWNSTREAM:
            return icons.getQIcon("edit_downstream")
        elif cls == cls.FREE:
            return icons.getQIcon("free_edition")
        else:
            raise ValueError()


class _EditionOptions(qt.QWidget):

    sigReset = qt.Signal()
    sigModeChanged = qt.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())

        self._editionModeLabel = qt.QLabel("edition mode", self)
        self.layout().addWidget(self._editionModeLabel)

        self._editionModeCB = qt.QComboBox(self)
        for mode in _EditionMode:
            self._editionModeCB.addItem(
                _EditionMode.get_icon(mode),
                mode.value,
            )
        self.layout().addWidget(self._editionModeCB)
        self._editionModeCB.setFixedHeight(30)

        self._spacer = qt.QSpacerItem(
            20, 40, qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum
        )
        self.layout().addItem(self._spacer)

        style = qt.QApplication.style()
        reset_icon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        self._resetButton = qt.QPushButton(
            parent=self, text="reset all positions", icon=reset_icon
        )
        self._resetButton.setToolTip("reset all position to initial positions")
        self.layout().addWidget(self._resetButton)

        # connect signal / slot
        self._editionModeCB.currentIndexChanged.connect(self.sigModeChanged)
        self._resetButton.released.connect(self.sigReset)

    def getEditionMode(self) -> _EditionMode:
        return _EditionMode(self._editionModeCB.currentText())

    def setEditionMode(self, edition_mode: _EditionMode | str):
        self._editionModeCB.setCurrentText(_EditionMode(edition_mode).value)
