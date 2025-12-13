from __future__ import annotations

from copy import copy
import os
import numpy
import logging

from silx.gui import qt
from silx.gui.plot import Plot2D
from silx.io.dictdump import h5todict
from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5
from silx.gui.dialog.DataFileDialog import DataFileDialog

from tomoscan.esrf.scan.utils import cwd_context
from tomoscan.framereducer.target import REDUCER_TARGET

from tomwer.io.utils import get_default_directory

_logger = logging.getLogger(__name__)


class ReduceDarkFlatSelectorTableWidget(qt.QWidget):
    """
    Table widget used to register and select a list of reduces frames
    """

    sigActiveChanged = qt.Signal(object)
    """Signal emit when the active frame changed (the one to be displayed)"""

    sigUpdated = qt.Signal()
    """Signal emit when the table is updated"""

    def __init__(self, parent: qt.QWidget | None = None) -> None:
        super().__init__(parent)
        self._iDict = 0
        self._dicts = {}
        # key are 'dict name', value are dict of the reduced frame (acquisition index as key, 2D numpy array as value).
        self.setLayout(qt.QVBoxLayout())
        self._tree = qt.QTreeWidget(self)
        self._tree.setHeaderLabels(("reduce frames", "acq index", "select"))
        self._tree.header().setStretchLastSection(False)
        self._tree.header().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        self._tree.setColumnWidth(1, 80)
        self._tree.setColumnWidth(2, 50)
        self.layout().addWidget(self._tree)

        self.setAcceptDrops(True)

        # connect signal / slot
        self._tree.currentItemChanged.connect(self._updateActiveChanged)

    def _updateActiveChanged(self, item, column: int):
        frame = item.data(0, qt.Qt.UserRole)
        self.sigActiveChanged.emit(frame)

    def popDictIndex(self) -> int:
        self._iDict = self._iDict + 1
        return self._iDict - 1

    def addReduceFrames(self, reduced_frames: dict, selected: tuple = ()):
        """
        Add the reduced frames in the interface.

        :param reduced_frames: frame index as key and numpy.ndarray as value
        :param selected: if the frame index is in selected tuple then this item will be automatically selected
        """
        reduced_frames = copy(reduced_frames)
        dict_key = (
            reduced_frames.pop("reduce_frames_name", None)
            or f"reduced frames #{self.popDictIndex()}"
        )
        # if the key already exists: remove it (avoid )
        if dict_key in self._dicts:
            self._removeReduceFramesByLabel(dict_key)
        self._dicts[dict_key] = reduced_frames

        topLevelItem = qt.QTreeWidgetItem(self._tree)
        topLevelItem.setText(0, dict_key)

        for frame_index, frame in reduced_frames.items():
            if not isinstance(frame, numpy.ndarray):
                _logger.error(
                    f"frame are expected to be numpy.ndarray. Get {type(frame)} instead - will not add it"
                )
                continue
            if frame.ndim != 2:
                _logger.error(f"frame are expected to be 2D. Get {frame.shape} instead")
                continue

            # frame info
            frameInfo = qt.QTreeWidgetItem(topLevelItem)
            frameInfo.setText(0, f"shape: {frame.shape}, dtype {frame.dtype}")
            frameInfo.setData(0, qt.Qt.UserRole, frame)
            # frame index
            indexItem = qt.QLineEdit(self._tree)
            # index can be provided as absolute indexes (integers)
            validator = qt.QRegularExpressionValidator(
                qt.QRegularExpression(r"([+-]?([0-9]*[.])?[0-9]+)*[r]"), self
            )
            indexItem.setValidator(validator)
            indexItem.setText(str(frame_index))
            self._tree.setItemWidget(frameInfo, 1, indexItem)
            indexItem.setToolTip(
                "Index of the reduced frames in the acquisition. Value can be provided as an absolute value - integer or as a relative value. In this case we expect users to provide a value between [0 and 1.0[ and postfix by 'r'"
            )
            # item selection
            selectCB = qt.QCheckBox(self._tree)
            selectCB.setChecked(frame_index in selected)
            self._tree.setItemWidget(frameInfo, 2, selectCB)
        self.sigUpdated.emit()

    def clear(self):
        self._dicts.clear()
        self._tree.clear()
        self.sigUpdated.emit()

    def getConfiguration(self) -> tuple:
        """
        return configuration as a tuple of 'reduced frames'. Each reduced_frames are provided with the following:
        * 'reduce_frames_name': str: name of the reduced frame
        * 'reduce_frames': tuple of dict for each reduce frame. This second dict contains:

            * index: index of this frame in the acquisition
            * data: the reduce frame as a 2D array
            * selected: is the frame selected by the user

        """
        config = []
        for i_child in range(self._tree.topLevelItemCount()):
            child = self._tree.topLevelItem(i_child)
            reduce_frames_infos = []
            for j_child in range(child.childCount()):
                sub_child = child.child(j_child)
                reduce_frames_infos.append(
                    {
                        "data": sub_child.data(0, qt.Qt.UserRole),
                        "index": self._get_reduce_frame_index(
                            self._tree.itemWidget(sub_child, 1).text()
                        ),
                        "selected": self._tree.itemWidget(sub_child, 2).isChecked(),
                    }
                )
            config.append(
                {
                    "reduce_frames_name": child.text(0),
                    "reduce_frames": reduce_frames_infos,
                }
            )
        return tuple(config)

    def setConfiguration(self, config: tuple | None):
        if config is None:
            return
        self.clear()
        for reduce_frames in config:
            frames_dict = {
                "reduce_frames_name": reduce_frames.get("reduce_frames_name", None)
            }
            selected = []
            for reduce_frame in reduce_frames["reduce_frames"]:
                assert isinstance(
                    reduce_frame, dict
                ), f"reduce_frames is expected to contain a list of dict. Get {type(reduce_frame)} instead"
                frame_index = reduce_frame["index"]
                assert isinstance(frame_index, int) or (
                    isinstance(frame_index, str) and frame_index.endswith("r")
                ), f"frame index should be an int or a str ending by 'r', get {type(frame_index)}"
                frames_dict[frame_index] = reduce_frame["data"]
                if reduce_frame["selected"]:
                    selected.append(reduce_frame["index"])
            self.addReduceFrames(frames_dict, selected)
        self.sigUpdated.emit()

    @staticmethod
    def _get_reduce_frame_index(index_as_str):
        """
        simple util to return expected frame index depending if the index is provided as relative or as absolute.
        """
        if index_as_str.endswith("r"):
            return index_as_str
        else:
            return int(index_as_str)

    def getSelectedReduceFrames(self) -> dict:
        """
        Return the selected reduced frame as dict
        """
        reduce_frames = {}
        for i_child in range(self._tree.topLevelItemCount()):
            child = self._tree.topLevelItem(i_child)
            for j_child in range(child.childCount()):
                sub_child = child.child(j_child)
                is_selected = self._tree.itemWidget(sub_child, 2).isChecked()
                if not is_selected:
                    continue

                frame_index = self._get_reduce_frame_index(
                    self._tree.itemWidget(sub_child, 1).text()
                )
                data = sub_child.data(0, qt.Qt.UserRole)
                assert isinstance(
                    data, numpy.ndarray
                ), f"frame are expected to be numpy.ndarray. Get {type(data)} instead"
                assert (
                    data.ndim == 2
                ), f"frame are expected to be 2D. Get {data.shape} instead"
                if frame_index in reduce_frames:
                    _logger.error(
                        f"frame index {frame_index} defined twice. Ignore last one"
                    )
                reduce_frames[frame_index] = data
        return reduce_frames

    def clearSelection(self):
        """
        Uncheck any check Combobox found
        """
        for i_child in range(self._tree.topLevelItemCount()):
            child = self._tree.topLevelItem(i_child)
            for j_child in range(child.childCount()):
                sub_child = child.child(j_child)
                if self._tree.itemWidget(sub_child, 2).isChecked():
                    self._tree.itemWidget(sub_child, 2).setChecked(False)

    def _removeSelected(self):
        # note: simplest way to remove item it to reset the configuration
        configuration = self.getConfiguration()
        configuration = filter_unselected_reduced_frames(configuration=configuration)
        self.setConfiguration(configuration)
        self.sigUpdated.emit()

    def _removeReduceFramesByLabel(self, label: str):
        """
        remove the label named 'label' if exists.
        The simplest way to remove reduced frames are by reseting the configuration for now
        """
        configuration = list(self.getConfiguration())
        new_configuration = tuple(
            filter(
                lambda my_dict: my_dict.get("reduce_frames_name", None) != label,
                configuration,
            ),
        )

        if len(configuration) != len(new_configuration):
            self.setConfiguration(new_configuration)

    def _guessReduceFramesFromFile(self, file_path: str) -> tuple:
        if not os.path.exists(file_path):
            _logger.error(f"file doesn't exists ({file_path})")

        with open_hdf5(file_path) as h5f:
            entries = tuple(h5f.keys())

        res = []
        for entry in entries:
            res.extend(
                self.get_reduce_frames(
                    DataUrl(
                        file_path=file_path,
                        data_path=entry,
                    )
                )
            )
        return tuple(res)

    @staticmethod
    def get_reduce_frames(url: DataUrl) -> tuple:
        """
        try to guess location of darks / flats according to provided url.
        The idea is to be more robust if the user provide a file or an higher level data path

        :warning: Return a tuple and not a dict. Because in the case the user provide an entry which contains
                  a 'darks' and a flats' groups we want to return both reduced_frames.
                  And we cannot return them as a dict as they can have the same index - used as dict key
        """
        if not isinstance(url, DataUrl):
            raise TypeError(f"url is expected to be a DataUrl. Get {type(url)} instead")
        if not os.path.exists(url.file_path()):
            _logger.error(f"file doesn't exists ({url.file_path()})")
            return tuple()

        result = []
        with cwd_context(url.file_path()):
            reduced_info_dict = h5todict(
                h5file=url.file_path(),
                path=url.data_path(),
            )
            for target in REDUCER_TARGET:
                if target.value in reduced_info_dict:
                    reduced_frames = reduced_info_dict[target.value]
                    reduced_frames["reduce_frames_name"] = (
                        f"{target.value} from {url.data_path()}@{os.path.basename(url.file_path())}"
                    )
                    result.append(reduced_frames)

            if len(reduced_frames) == 0:
                # else we consider the data_path is the valid one
                reduced_frames["reduce_frames_name"] = (
                    f"{url.data_path()}@{os.path.basename(url.file_path())}"
                )
                result.append(reduced_frames)

        return tuple(result)

    # drag / drop handling

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            for url in event.mimeData().urls():
                reduced_frames_list = self._guessReduceFramesFromFile(
                    file_path=url.path()
                )
                for reduced_frames in reduced_frames_list:
                    self.addReduceFrames(reduced_frames)

    def supportedDropActions(self):
        """Inherited method to redefine supported drop actions."""
        return qt.Qt.CopyAction | qt.Qt.MoveAction

    def dragEnterEvent(self, event):
        if hasattr(event, "mimeData") and event.mimeData().hasFormat("text/uri-list"):
            event.accept()
            event.setDropAction(qt.Qt.CopyAction)
        else:
            try:
                qt.QListWidget.dragEnterEvent(self, event)
            except TypeError:
                pass

    def dragMoveEvent(self, event):
        if hasattr(event, "mimeDatamyitems") and event.mimeDatamyitems().hasFormat(
            "text/uri-list"
        ):
            event.setDropAction(qt.Qt.CopyAction)
            event.accept()
        else:
            try:
                qt.QListWidget.dragMoveEvent(self, event)
            except TypeError:
                pass


class ReduceDarkFlatSelectorWidget(qt.QSplitter):
    """
    Widget combining ReduceDarkFlatSelectorTableWidget and plot of the active item
    """

    sigUpdated = qt.Signal()
    """Signal emmit when the table is updated"""

    def __init__(self, parent: qt.QWidget | None = None) -> None:
        super().__init__(parent)
        self._first_display = True
        self._plot = Plot2D(self)
        self.addWidget(self._plot)
        self._table = ReduceDarkFlatSelectorTableWidget(parent=self)
        self.addWidget(self._table)

        # connect signal / slot
        self._table.sigActiveChanged.connect(self._updatePlot)
        self._table.sigUpdated.connect(self._tableUpdated)

    def _tableUpdated(self, *args, **kwargs):
        self.sigUpdated.emit()

    def _updatePlot(self, obj: numpy.ndarray | None):
        if obj is None:
            self._plot.clear()
        else:
            self._plot.addImage(
                data=obj,
                replace=True,
                resetzoom=self._first_display,
            )
            self._first_display = False

    # expose API
    def addReduceFrames(self, *args, **kwargs):
        self._table.addReduceFrames(*args, **kwargs)

    def getConfiguration(self) -> tuple:
        return self._table.getConfiguration()

    def setConfiguration(self, *args, **kwargs):
        self._table.setConfiguration(*args, **kwargs)

    def getSelectedReduceFrames(self) -> dict:
        return self._table.getSelectedReduceFrames()

    def clearSelection(self) -> None:
        self._table.clearSelection()

    def _removeSelected(self) -> None:
        self._table._removeSelected()

    def clear(self) -> None:
        self._table.clear()


class ReduceDarkFlatSelectorDialog(qt.QDialog):
    """
    'Final' dialog to select reduce frames
    """

    sigClearSelection = qt.Signal()
    """emit when user ask for the selection to be cleared"""
    sigSelectActiveAsDarks = qt.Signal(dict)
    """emit when user select the darks to be activated"""
    sigSelectActiveAsFlats = qt.Signal(dict)
    """emit when user select the flats to be activated"""

    sigUpdated = qt.Signal()
    """Signal emmit when the table is updated"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setLayout(qt.QVBoxLayout())
        # add list
        self._widget = ReduceDarkFlatSelectorWidget()
        self.layout().addWidget(self._widget)
        # add buttons
        self._buttons = qt.QDialogButtonBox(parent=self)
        # select reduce flats
        self._selectAsFlatButton = qt.QPushButton(
            "Select as reduce flat(s)", parent=self
        )
        self._buttons.addButton(
            self._selectAsFlatButton, qt.QDialogButtonBox.AcceptRole
        )
        # select reduce darks
        self._selectAsDarkButton = qt.QPushButton(
            "Select as reduce dark(s)", parent=self
        )
        self._buttons.addButton(
            self._selectAsDarkButton, qt.QDialogButtonBox.AcceptRole
        )
        # clear
        self._clearSelectionButton = qt.QPushButton("clear selection", parent=self)
        self._buttons.addButton(
            self._clearSelectionButton, qt.QDialogButtonBox.ResetRole
        )
        # remove selected
        self._removeSelectionButton = qt.QPushButton("remove selection", parent=self)
        self._buttons.addButton(
            self._removeSelectionButton, qt.QDialogButtonBox.ActionRole
        )
        # remove selected
        self._addButton = qt.QPushButton("add", parent=self)
        self._buttons.addButton(self._addButton, qt.QDialogButtonBox.ActionRole)
        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._selectAsFlatButton.released.connect(self._flatSelected)
        self._selectAsDarkButton.released.connect(self._darkSelected)
        self._clearSelectionButton.released.connect(self._clearSelection)
        self._removeSelectionButton.released.connect(self._removeSelected)
        self._addButton.released.connect(self._addFromFileSelection)
        self._widget.sigUpdated.connect(self._tableUpdated)

    def _tableUpdated(self, *args, **kwargs):
        self.sigUpdated.emit()

    def _flatSelected(self):
        self.sigSelectActiveAsFlats.emit(
            self._widget.getSelectedReduceFrames(),
        )

    def _darkSelected(self):
        self.sigSelectActiveAsDarks.emit(
            self._widget.getSelectedReduceFrames(),
        )

    def _clearSelection(self):
        self._widget.clearSelection()

    def _removeSelected(self):
        self._widget._removeSelected()

    def _addFromFileSelection(self):
        dialog = DataFileDialog()
        dialog.setDirectory(get_default_directory())
        if dialog.exec():
            url = dialog.selectedUrl()
            reduced_frames_tuple = ReduceDarkFlatSelectorTableWidget.get_reduce_frames(
                DataUrl(path=url)
            )
            for reduced_frames in reduced_frames_tuple:
                try:
                    self.addReduceFrames(reduced_frames)
                except Exception as e:
                    _logger.error(e)

    # expose API
    def addReduceFrames(self, *args, **kwargs):
        self._widget.addReduceFrames(*args, **kwargs)

    def getConfiguration(self) -> tuple:
        self._widget.getConfiguration()

    def setConfiguration(self, configuration: tuple) -> None:
        self._widget.setConfiguration(configuration)


def filter_selected_reduced_frames(configuration: tuple):
    """
    remove all the frames not 'selected' from the configuration.
    If a reduce frame set becomes empty it will also be removed

    :param configuration: configuration of the reduced frames
    """
    return _filter_reduced_frames(configuration=configuration, filter_selected=True)


def filter_unselected_reduced_frames(configuration: tuple):
    """
    remove all the frames 'selected' from the configuration.
    If a reduce frame set becomes empty it will also be removed

    :param configuration: configuration of the reduced frames
    """
    return _filter_reduced_frames(configuration=configuration, filter_selected=False)


def _filter_reduced_frames(configuration: tuple, filter_selected: bool):
    assert isinstance(
        configuration, (tuple, list, set)
    ), f"configuration is expected to be a tuple. Get {type(configuration)}"
    result = []
    for reduce_group in configuration:
        reduce_frames = reduce_group.get("reduce_frames", tuple())
        reduce_group_name = reduce_group.get("reduce_frames_name", None)
        res_set = tuple(
            filter(
                lambda my_dict: my_dict["selected"] == filter_selected,
                reduce_frames,
            )
        )
        if len(res_set) > 0:
            result_group = {}
            if reduce_group_name is not None:
                result_group["reduce_frames_name"] = reduce_group_name
            result_group["reduce_frames"] = res_set

            result.append(result_group)

    return tuple(result)
