from __future__ import annotations

import logging
import os
from collections import OrderedDict
from typing import Any
from nxtomomill import converter as nxtomomill_converter
from nxtomomill.io import generate_default_edf_config, generate_default_h5_config
from nxtomomill.models.h52nx import H52nxModel
from nxtomomill.models.edf2nx import EDF2nxModel

from silx.gui import qt

from tomoscan.esrf.volume.utils import guess_volumes
from tomoscan.identifier import BaseIdentifier
from tomoscan.esrf.identifier.hdf5Identifier import NXtomoScanIdentifier

from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.io.utils.tomoobj import DEFAULT_SCHEME_TO_VOL
from tomwer.gui.control.actions import CFGFileActiveLabel, NXTomomillParamsAction
from tomwer.gui.dialog.QDataDialog import QDataDialog
from tomwer.gui.dialog.QVolumeDialog import QVolumeDialog
from tomwer.gui.utils.inputwidget import (
    EDFConfigFileSelector,
    HDF5ConfigFileSelector,
    NXTomomillOutputDirSelector,
)
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.control.tomoobjdisplaymode import DisplayMode
from tomwer.gui.control.actions import TomoObjDisplayModeToolButton
from tomwer.gui import icons

logger = logging.getLogger(__name__)


class _DataListDialog(qt.QDialog):
    """A simple list of dataset path.BlissHDF5DataListDialog

    .. warning: the widget won't check for scan validity and will only
        emit the path to folders to the next widgets

    :param parent: the parent widget
    """

    sigUpdated = qt.Signal()
    """signal emitted when the list is updated"""

    def __init__(self, parent=None):
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        # add list
        self.datalist = self.createDataList()
        self.layout().addWidget(self.datalist)
        # add buttons
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._addButton = qt.QPushButton("Add", parent=self)
        self._buttons.addButton(self._addButton, qt.QDialogButtonBox.ActionRole)
        self._rmButton = qt.QPushButton("Remove", parent=self)
        self._buttons.addButton(self._rmButton, qt.QDialogButtonBox.ActionRole)
        self._rmAllButton = qt.QPushButton("Remove all", parent=self)
        self._buttons.addButton(self._rmAllButton, qt.QDialogButtonBox.ActionRole)

        self._sendSelectedButton = qt.QPushButton("Send selected", parent=self)
        self._buttons.addButton(
            self._sendSelectedButton, qt.QDialogButtonBox.AcceptRole
        )
        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self._addButton.clicked.connect(self._callbackAddPath)
        self._rmButton.clicked.connect(self._removeSelected)
        self._rmAllButton.clicked.connect(self._callbackRemoveAllFolders)

    def selectAll(self):
        return self.datalist.selectAll()

    def clear(self):
        self.datalist.clear()

    def add(self, scan) -> tuple:
        added_objs = self.datalist.add(scan)
        self.datalist.setMySelection(added_objs)
        self.sigUpdated.emit()
        return added_objs

    def remove(self, scan):
        self.datalist.remove(scan)
        self.sigUpdated.emit()

    def n_scan(self):
        return len(self.datalist._myitems)

    def _callbackAddPath(self):
        """ """
        self.sigUpdated.emit()

    def _removeSelected(self):
        """remove all selected items"""
        selected_items = self.datalist.selectedItems()
        tomwer_objs_to_remove = [item.data(qt.Qt.UserRole) for item in selected_items]
        for tomwer_obj in tomwer_objs_to_remove:
            self.remove(tomwer_obj)
        self.sigUpdated.emit()

    def _callbackRemoveAllFolders(self):
        self.datalist.selectAll()
        self._removeSelected()

    def createDataList(self):
        raise NotImplementedError("Base class")


class _NXtomomillConfigFileDialog(qt.QDialog):

    sigConfigFileChanged = qt.Signal(str)
    sigOutputdirChanged = qt.Signal()
    sigMechanicalFlipsChanged = qt.Signal()

    def __init__(
        self,
        parent,
        warning: str,
        callback_new_config_file: Any,
        ConfigFileSelectorClass: Any,
    ):
        super().__init__(parent)
        self.setLayout(qt.QFormLayout())

        self._warningLabel = qt.QLabel(warning, self)
        self._warningLabel.setWordWrap(False)
        font = self._warningLabel.font()
        font.setItalic(True)
        font.setPixelSize(12)
        self._warningLabel.setFont(font)
        self._warningLabel.setAlignment(qt.Qt.AlignLeft | qt.Qt.AlignVCenter)
        #: add left intendation + lower size + italic
        self.layout().addRow(self._warningLabel)

        # handle configuration file
        self._configurationWidget = ConfigFileSelectorClass(self, try_load_cfg=False)
        self.layout().addRow("configuration file", self._configurationWidget)

        # button to create a default configuration file
        self._cdcfWidget = qt.QWidget(self)  # widget for layout
        self._cdcfWidget.setLayout(qt.QHBoxLayout())
        self._cdcfSpacer = qt.QWidget(self._cdcfWidget)
        self._cdcfSpacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._cdcfWidget.layout().addWidget(self._cdcfSpacer)
        self._createDefaultConfigFileB = qt.QPushButton(
            "create new default configuration file", self._cdcfWidget
        )
        self._cdcfWidget.layout().addWidget(self._createDefaultConfigFileB)
        self.layout().addRow(self._cdcfWidget)

        # vline 1
        self._vLine1 = qt.QFrame()
        self._vLine1.setFrameShape(qt.QFrame.Shape.HLine)
        self._vLine1.setFrameShadow(qt.QFrame.Shadow.Sunken)
        self.layout().addRow(self._vLine1)

        # mechanical flips
        self._lrMechanicalFlipLabel = qt.QLabel()
        lr_icon = icons.getQIcon("lr_mirroring")
        self._lrMechanicalFlip = qt.QCheckBox()
        self._lrMechanicalFlip.setIcon(lr_icon)
        self._lrMechanicalFlip.setToolTip(
            "Detector image is flipped **left-right** for mechanical reasons that are not propagated with bliss-tomo hdf5 metadata (mirror,..)."
        )
        self.layout().addRow("left-right mechanical flip", self._lrMechanicalFlip)

        self._udMechanicalFlipLabel = qt.QLabel("left-right mechanical flip")
        ud_icon = icons.getQIcon("ud_mirroring")
        self._udMechanicalFlip = qt.QCheckBox()
        self._udMechanicalFlip.setIcon(ud_icon)
        self._udMechanicalFlip.setToolTip(
            "Detector image is flipped **up-down** for mechanical reasons that are not propagated with bliss-tomo hdf5 metadata (mirror,..)."
        )
        self.layout().addRow("up-down mechanical flip", self._udMechanicalFlip)

        # vline 2
        self._vLine2 = qt.QFrame()
        self._vLine2.setFrameShape(qt.QFrame.Shape.HLine)
        self._vLine2.setFrameShadow(qt.QFrame.Shadow.Sunken)
        self.layout().addRow(self._vLine2)

        # handle configuration file
        self._nxTomomillOutputWidget = NXTomomillOutputDirSelector()
        self.layout().addRow("nexus file output dir", self._nxTomomillOutputWidget)

        # buttons
        types = qt.QDialogButtonBox.Ok
        self.__buttons = qt.QDialogButtonBox(parent=self)
        self.__buttons.setStandardButtons(types)
        self.layout().addWidget(self.__buttons)

        # connect signal / slot
        self.__buttons.accepted.connect(self.accept)
        if callback_new_config_file is not None:
            self._createDefaultConfigFileB.released.connect(callback_new_config_file)
        self._configurationWidget.sigConfigFileChanged.connect(
            self.sigConfigFileChanged
        )
        self._nxTomomillOutputWidget.sigChanged.connect(self.sigOutputdirChanged)
        self._lrMechanicalFlip.toggled.connect(self.sigMechanicalFlipsChanged)
        self._udMechanicalFlip.toggled.connect(self.sigMechanicalFlipsChanged)

    def setNewconfigFileCreationCallback(self, callback):
        self._createDefaultConfigFile = callback

    def getCFGFilePath(self):
        return self._configurationWidget.getCFGFilePath()

    def setCFGFilePath(self, cfg_file):
        self._configurationWidget.setCFGFilePath(cfg_file)

    def getOutputFolder(self):
        return self._nxTomomillOutputWidget.getOutputFolder()

    def setOutputDialog(self, output_dir):
        self._nxTomomillOutputWidget.setOutputFolder(output_dir)

    def accept(self):
        self.hide()

    def _createConfigFileSelector(self):
        raise NotImplementedError

    def getMechanicalFlips(self) -> tuple[bool, bool]:
        """
        :return: mechanical flips as (left-right, up-down)
        """
        return self._lrMechanicalFlip.isChecked(), self._udMechanicalFlip.isChecked()

    def setMechanicalFlips(self, lr_flip: bool, ud_flip: bool) -> None:
        self._lrMechanicalFlip.setChecked(lr_flip)
        self._udMechanicalFlip.setChecked(ud_flip)


class BlissHDF5DataListDialog(_DataListDialog):
    """Dialog used to load .h5 files only (used for nxtomomillOW when we need to do a conversion from bliss.h5 to NXtomo)"""

    def __init__(self, parent):
        assert isinstance(parent, _RawDataListMainWindow)
        _DataListDialog.__init__(self, parent)
        self._sendSelectedButton.setText("Send selected")

    def createDataList(self):
        return BlissScanList(self)

    def _callbackAddPath(self):  # pragma: no cover
        """Open file dialog to select HDF5 files or directories, allowing multi-selection"""
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.ExistingFiles)
        dialog.setNameFilters(
            [
                "HDF5 files (*.h5 *.hdf5)",
                "Nexus files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                "Any files (*)",
            ]
        )

        # Set default directory if available
        if os.environ.get("TOMWER_DEFAULT_INPUT_DIR", None) and os.path.exists(
            os.environ["TOMWER_DEFAULT_INPUT_DIR"]
        ):
            dialog.setDirectory(os.environ["TOMWER_DEFAULT_INPUT_DIR"])
        elif dialog.directory() != os.getcwd() or str(dialog.directory()).startswith(
            "/data"
        ):
            # if the directory as already been set by the user. Avoid redefining it
            pass
        elif os.path.isdir("/data"):
            dialog.setDirectory("/data")

        if not dialog.exec():
            dialog.close()
            return

        filesSelected = dialog.selectedFiles()
        added_scans = []
        for file_ in filesSelected:
            added_scans = self.add(file_)
            if added_scans is None:
                continue
            added_scans.extend(added_scans)
        super()._callbackAddPath()
        self.datalist.setMySelection(added_scans)


class EDFDataListDialog(_DataListDialog):
    """Dialog used to load EDF directories and files for conversion"""

    def __init__(self, parent):
        assert isinstance(parent, EDFDataListMainWindow)
        _DataListDialog.__init__(self, parent)
        self._sendSelectedButton.setText("Convert and send selected")

    def createDataList(self):
        return EDFDataList(self)

    def _callbackAddPath(self):  # pragma: no cover
        """Open file dialog to select EDF directories or files"""
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        # Set default directory if available
        if os.environ.get("TOMWER_DEFAULT_INPUT_DIR", None) and os.path.exists(
            os.environ["TOMWER_DEFAULT_INPUT_DIR"]
        ):
            dialog.setDirectory(os.environ["TOMWER_DEFAULT_INPUT_DIR"])
        elif os.path.isdir("/data"):
            dialog.setDirectory("/data")

        if not dialog.exec():
            dialog.close()
            return

        filesSelected = dialog.selectedFiles()
        added_scans = []
        for file_ in filesSelected:
            added = self.add(file_)
            assert added is not None
            added_scans.extend(added)
        super()._callbackAddPath()
        self.datalist.setMySelection(added_scans)


class _RawDataListMainWindow(qt.QMainWindow):
    sigNXTomoCFGFileChanged = qt.Signal(str)
    """signal emitted when the configuration file change"""

    sigUpdated = qt.Signal()
    """signal emitted when the list of raw data to convert change"""

    def __init__(
        self, parent, DataListConstructor, ConfigClass, warning, ConfigFileSelectorClass
    ):
        super().__init__(parent)
        self._widget = DataListConstructor(self)
        self.__configConstructor = ConfigClass
        # rework BlissHDF5DataListDialog layout
        self._subWidget = qt.QWidget(self)
        self._subWidget.setLayout(qt.QVBoxLayout())
        self._subWidget.layout().addWidget(self._widget.datalist)
        self._subWidget.layout().addWidget(self._widget._buttons)
        self.setCentralWidget(self._subWidget)

        self._dialog = _NXtomomillConfigFileDialog(
            self,
            warning=warning,
            callback_new_config_file=self._createNewConfigFile,
            ConfigFileSelectorClass=ConfigFileSelectorClass,
        )
        self._dialog.setWindowTitle("Select nxtomomill configuration file")

        # add toolbar
        toolbar = qt.QToolBar(self)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(qt.Qt.TopToolBarArea, toolbar)

        # add filtering
        self._parametersAction = NXTomomillParamsAction(toolbar)
        toolbar.addAction(self._parametersAction)
        self._parametersAction.triggered.connect(self._parametersTriggered)

        # add tomo obj display mode
        self._tomoObjdisplayAction = TomoObjDisplayModeToolButton(self)
        toolbar.addWidget(self._tomoObjdisplayAction)

        # toolbar spacer
        spacer = qt.QWidget(toolbar)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        toolbar.addWidget(spacer)

        # add information if cfg file is activate or not
        self._cfgStatusLabel = CFGFileActiveLabel(toolbar)
        toolbar.addWidget(self._cfgStatusLabel)

        # expose API
        self.getCFGFilePath = self._dialog.getCFGFilePath
        self.setCFGFilePath = self._dialog.setCFGFilePath
        self._sendSelectedButton = self._widget._sendSelectedButton
        self.add = self._widget.add
        self.n_scan = self._widget.n_scan
        self.datalist = self._widget.datalist

        # connect signal / slot
        self._dialog.sigConfigFileChanged.connect(self._cfgFileChanged)
        self._dialog.sigOutputdirChanged.connect(self.sigUpdated)
        self._dialog.sigMechanicalFlipsChanged.connect(self.sigUpdated)
        self._widget.sigUpdated.connect(self.sigUpdated)
        self._tomoObjdisplayAction.sigDisplayModeChanged.connect(self.setDisplayMode)

    def setDisplayMode(self, *args, **kwargs):
        self.datalist.setDisplayMode(*args, **kwargs)

    def getOutputFolder(self):
        return self._dialog.getOutputFolder()

    def setOutputFolder(self, output_dir):
        self._dialog.setOutputDialog(output_dir)

    def _parametersTriggered(self):
        self._dialog.show()
        self._dialog.raise_()

    def _cfgFileChanged(self):
        cfg_file = self._dialog.getCFGFilePath()
        if cfg_file in (None, "") or not os.path.exists(cfg_file):
            self._cfgStatusLabel.setInactive()
        elif os.path.exists(cfg_file):
            try:
                self._load_cfg_file(cfg_file=cfg_file)
            except Exception:
                self._cfgStatusLabel.setInactive()
            else:
                self._cfgStatusLabel.setActive()
        else:
            self._cfgStatusLabel.setInactive()
        if cfg_file is None:
            cfg_file = ""
        self.sigNXTomoCFGFileChanged.emit(cfg_file)

    def _load_cfg_file(self, cfg_file):
        """The idea is to load the file before using it. This way the user can see if something is wrong with the file"""
        raise NotImplementedError("Base class")

    def getConfigInstance(self):
        """Return default HDF5Config or the one created from use input"""
        cfg_file = self._dialog.getCFGFilePath()
        if cfg_file in (None, ""):
            return self.__configConstructor()
        else:
            try:
                config = self.__configConstructor.from_cfg_file(cfg_file)
            except Exception:
                return self.__configConstructor()
            else:
                return config

    def createNXtomomillConfigFileDialog(self):  # pragma: no cover
        file_dialog = qt.QFileDialog()
        file_dialog.setAcceptMode(qt.QFileDialog.AcceptSave)
        file_dialog.setWindowTitle("Select file path to save configuration file")
        file_dialog.setNameFilters(
            [
                "Any file (*)",
                "Configuration file (*.txt *.cfg *.conf *.config)",
            ]
        )
        file_dialog.setFileMode(qt.QFileDialog.AnyFile)
        return file_dialog

    def _createNewConfigFile(self):
        """
        callback for the configuration file creation
        """
        raise NotImplementedError("Base class")


class BlissHDF5DataListMainWindow(_RawDataListMainWindow):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            DataListConstructor=BlissHDF5DataListDialog,
            ConfigClass=H52nxModel,
            warning="""Note: some parameters of the configuration file will be ignored:\n
            - input_file will be replaced from the item of the data list treated
            - output_file will be deduce from the output folder you defined""",
            ConfigFileSelectorClass=HDF5ConfigFileSelector,
            *args,
            **kwargs,
        )

    def _createNewConfigFile(self):  # pragma: no cover
        file_dialog = self.createNXtomomillConfigFileDialog()
        if file_dialog.exec():
            files_selected = file_dialog.selectedFiles()
            if len(files_selected) > 0:
                file_path = files_selected[0]
                try:
                    # nxtomomill 1.1.0a5 or higher
                    configuration = (
                        generate_default_h5_config()  # pylint: disable=E1123
                    )

                except TypeError:
                    configuration = generate_default_h5_config(  # pylint: disable=E1123
                        config_3dxrd=False
                    )
                H52nxModel.dict_to_cfg(file_path=file_path, dict_=configuration)
                # if we create a configuration file then let consider we want to use it
                self.setCFGFilePath(file_path)

    def _load_cfg_file(self, cfg_file):
        H52nxModel.from_cfg_file(cfg_file)

    def setConfiguration(self, config: dict):
        if not isinstance(config, H52nxModel):
            raise TypeError
        self.datalist.configuration = config


class EDFDataListMainWindow(_RawDataListMainWindow):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            DataListConstructor=EDFDataListDialog,
            ConfigClass=EDF2nxModel,
            warning="""Note: some parameters of the configuration file will be ignored:\n
            - input_folder will be replaced from the item of the data list treated
            - dataset_basename (if will be deduce when the input folder is provided)
            - output_file will be deduce from the output folder you defined""",
            ConfigFileSelectorClass=EDFConfigFileSelector,
            *args,
            **kwargs,
        )

    def _createNewConfigFile(self):  # pragma: no cover
        file_dialog = self.createNXtomomillConfigFileDialog()
        if file_dialog.exec():
            files_selected = file_dialog.selectedFiles()
            if len(files_selected) > 0:
                file_path = files_selected[0]
                configuration = generate_default_edf_config(level="advanced")
                EDF2nxModel.dict_to_cfg(file_path=file_path, dict_=configuration)
                # if we create a configuration file then let consider we want to use it
                self.setCFGFilePath(file_path)

    def _load_cfg_file(self, cfg_file):
        EDF2nxModel.from_cfg_file(cfg_file)


class GenericScanListDialog(_DataListDialog):
    """Dialog used to load EDFScan or HDF5 scans"""

    def createDataList(self):
        return GenericScanList(self)

    def _callbackAddPath(self):  # pragma: no cover
        """ """
        dialog = QDataDialog(self, multiSelection=True)
        dialog.setNameFilters(
            [
                "HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                "Nexus files (*.nx *.nxs *.nexus)",
                "Any files (*)",
            ]
        )

        if not dialog.exec():
            dialog.close()
            return

        files_or_folders = dialog.files_selected()
        added_scans = []
        for file_or_folder in files_or_folders:
            new_scans = self.add(file_or_folder)
            if new_scans is not None:
                added_scans.extend(new_scans)
        super()._callbackAddPath()
        self.datalist.setMySelection(added_scans)


class GenericScanListWindow(qt.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowFlags(qt.Qt.Widget)

        self._widget = GenericScanListDialog()
        self.datalist = self._widget.datalist
        self.setCentralWidget(self._widget)

        # toolbar
        toolbar = qt.QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(qt.Qt.TopToolBarArea, toolbar)

        tomoObjdisplayAction = TomoObjDisplayModeToolButton(self)
        toolbar.addWidget(tomoObjdisplayAction)

        # set up
        self.setDisplayMode(DisplayMode.SHORT)

        # expose API
        self.sigUpdated = self._widget.sigUpdated

        # connect signal / slot
        tomoObjdisplayAction.sigDisplayModeChanged.connect(self.setDisplayMode)

    def setDisplayMode(self, display_mode: DisplayMode):
        self.datalist.setDisplayMode(display_mode)

    # expose API
    def n_scan(self):
        return self._widget.n_scan()

    def add(self, *args, **kwargs):
        return self._widget.add(*args, **kwargs)


class VolumeListDialog(_DataListDialog):
    """Dialog used to load EDFScan or HEDF5 scans"""

    def createDataList(self):
        return VolumeList(self)

    def _callbackAddPath(self):  # pragma: no cover
        """ """
        dialog = QVolumeDialog(self)

        if not dialog.exec():
            dialog.close()
            return
        files_or_folders = dialog.files_selected()
        added_volumes = []
        for file_or_folder in files_or_folders:
            new_volumes = self.add(file_or_folder)
            if new_volumes is not None:
                added_volumes.extend(new_volumes)
        super()._callbackAddPath()
        self.datalist.setMySelection(added_volumes)


class _TomwerObjectList(qt.QTableWidget):
    HEADER_NAMES = ("undefined object",)

    dataReady = qt.Signal(TomwerObject)

    listChanged = qt.Signal()
    """emit when containt of the list changed"""

    def __init__(self, parent):
        self._copy_target = None
        qt.QTableWidget.__init__(self, parent)
        self.setRowCount(0)
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels(self.HEADER_NAMES)
        self.setSortingEnabled(True)
        self.verticalHeader().hide()
        if hasattr(self.horizontalHeader(), "setSectionResizeMode"):  # Qt5
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:  # Qt4
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.setAcceptDrops(True)

        self._myitems = OrderedDict()
        # key is the TomoObject identifier and value is the QTableWidgetItem.
        # Text is the identifier, QTableWidgetItem data under UserRole is the TomoObject object

        # QMenu
        self.menu = qt.QMenu(self)
        self._copyAction = qt.QAction("copy")
        self._copyAction.triggered.connect(self._copyRequested)
        self._pasteAction = qt.QAction("paste")
        self._pasteAction.triggered.connect(self._pasteRequested)
        self.menu.addAction(self._copyAction)
        self.menu.addAction(self._pasteAction)

        self.setDisplayMode(DisplayMode.SHORT)

    def setDisplayMode(self, mode: DisplayMode) -> None:
        self._displayMode = DisplayMode(mode)
        self._update()

    def n_data(self):
        return len(self._myitems)

    def remove_item(self, item):
        """Remove a given folder"""
        try:
            del self._myitems[item.data(qt.Qt.UserRole).get_identifier().to_str()]
        except RuntimeError:
            # look like this could failed on some Qt or PyQt version (see issue 802)
            # no much that we can do so ignore it.
            pass
        self._update()

    def _sendSelected(self):
        raise NotImplementedError
        for _, item in self._myitems.items():
            data = item.data(qt.Qt.UserRole)
            self.dataReady.emit(data)

    def remove(self, data: TomwerObject | str | None):
        if data is None:
            return
        if isinstance(data, str):
            data = self._getTomoObject(data, allow_several=False)
            if data is None:
                logger.warning(f"unable to get a {TomwerObject} from {data}")
                return

            identifier_as_str = data.get_identifier().to_str()
        if not isinstance(data, TomwerObject):
            raise ValueError(f"{data} is not a TomwerObject")

        identifier_as_str = data.get_identifier().to_str()

        if identifier_as_str not in self._myitems:
            logger.info(f"{identifier_as_str} not in {self._myitems}")
            return
        else:
            item = self._myitems[identifier_as_str]
            self.remove_item(item)
            self.listChanged.emit()

    def _update(self):
        tomwer_objects = [
            self._myitems[identifier_as_str].data(qt.Qt.UserRole)
            for identifier_as_str in self._myitems.keys()
        ]
        self.clear()
        with block_signals(self):
            for tomwer_object in tomwer_objects:
                self.add(tomwer_object)
        self.sortByColumn(0, self.horizontalHeader().sortIndicatorOrder())
        self.listChanged.emit()

    def _getTomoObject(self, obj: str, allow_several: bool = False):
        """
        some rules to return a TomwerObject from an object (probably a path) from children class

        :param allow_several: allow returning several objects for one input. This can be the case for example if 'obj' is a file path.
        """
        raise NotImplementedError("Base class")

    def add(self, obj: TomwerObject | BaseIdentifier | str | None) -> tuple | None:
        """add a data"""
        if obj is None:
            return
        if isinstance(obj, TomwerObject):
            # remove heavy cache obj. This could bring troubles if some processing is done.
            # but I guess this is better than keeping in memory volumes...
            # nevertheless processing using volume.data should keep a reference on the data.
            obj._clear_heavy_cache()
        elif isinstance(obj, str):
            obj = self._getTomoObject(obj, allow_several=True)
            if obj is None:
                return
            elif isinstance(obj, (tuple, list)):
                # in the case it contains in fact several objects. Related to allow_several=True
                new_objs = []
                for o in obj:
                    new_objs.extend(list(self.add(o)))
                return new_objs
            elif not isinstance(obj, TomwerObject):
                raise TypeError(
                    f"return object from _getTomoObject is not a {TomwerObject} but {type(obj)}"
                )
        elif isinstance(obj, BaseIdentifier):
            try:
                obj = ScanFactory.create_tomo_object_from_identifier(obj)
            except Exception:
                try:
                    obj = VolumeFactory.create_tomo_object_from_identifier(obj)
                except Exception:
                    raise ValueError(f"Unable to create an TomwerObject from {obj}")

        else:
            raise TypeError(
                f"is expected to be an instance of str or of {TomwerObject} but {type(obj)}"
            )

        identifier_as_str = obj.get_identifier().to_str()
        if identifier_as_str in self._myitems:
            # in this case we will update the value. Because if the same identifier already exists at launch time
            # it will create two different objects that could be an issue.
            # this is better to have it unified
            with block_signals(self):
                self.remove(self._myitems[identifier_as_str].data(qt.Qt.UserRole))

        item = qt.QTableWidgetItem()
        item.setText(self.getTextToDisplay(obj))
        item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
        item.setData(qt.Qt.UserRole, obj)

        row = self.rowCount()
        self.setRowCount(row + 1)
        self.setItem(row, 0, item)
        self._myitems[identifier_as_str] = item
        self.listChanged.emit()
        return (obj,)

    def getTextToDisplay(self, obj: TomwerObject):
        if self._displayMode is DisplayMode.SHORT:
            return obj.get_identifier().short_description()
        elif self._displayMode is DisplayMode.URL:
            return obj.get_identifier().to_str()
        else:
            raise ValueError(
                f"Requested display mode {self._displayMode} is not handled"
            )

    def setMySelection(self, datasets: tuple[str | TomwerObject]):
        if datasets is None:
            datasets = tuple()

        def convert_dataset(dataset: str | TomwerObject):
            if isinstance(dataset, TomwerObject):
                return dataset.get_identifier().to_str()
            else:
                return dataset

        datasets = tuple([convert_dataset(dataset) for dataset in datasets])
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            select_it = (
                item.data(qt.Qt.UserRole).get_identifier().to_str() in datasets
                or item.text() in datasets
            )
            item.setSelected(select_it)

    def clear(self):
        """Remove all items on the list"""
        self._myitems = OrderedDict()
        qt.QTableWidget.clear(self)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(self.HEADER_NAMES)
        if hasattr(self.horizontalHeader(), "setSectionResizeMode"):  # Qt5
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:  # Qt4
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            added_scans = set()
            with block_signals(self):
                for url in event.mimeData().urls():
                    new_scans = self.add(str(url.path()))
                    if new_scans is not None:
                        for new_scan in new_scans:
                            if not isinstance(new_scan, TomwerObject):
                                raise ValueError(
                                    f"new_scan should be an instance of {TomwerObject} and not {type(new_scan)}"
                                )
                        added_scans.update(new_scans)
            self.setMySelection(added_scans)
            self.listChanged.emit()

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

    def _datasetAt(self, point):
        item = self.itemAt(point)
        if item is not None:
            return item.data(qt.Qt.UserRole)

    def contextMenuEvent(self, event):
        self._copy_target = self._datasetAt(event.pos())
        self._copyAction.setVisible(self._copy_target is not None)
        self.menu.exec(event.globalPos())

    def _copyRequested(self):
        clipboard = qt.QGuiApplication.clipboard()

        def get_info(item):
            user_data = item.data(qt.Qt.UserRole)
            if isinstance(user_data, TomwerObject):
                return user_data.get_identifier().to_str()
            else:
                return str(user_data)

        selection = [get_info(item) for item in self.selectedItems()]
        clipboard.setText("\n".join(selection))

    def _pasteRequested(self):
        clipboard = qt.QGuiApplication.clipboard()
        identifiers = clipboard.text()
        # handle paste of several lines...
        identifiers.replace(";", "\n")
        for identifier in identifiers.split("\n"):
            try:
                self.add(identifier)
            except Exception as e:
                logger.error(f"Failed to add '{identifier}'. Error is {e}")


class GenericScanList(_TomwerObjectList):
    """Data list able to manage directories (EDF/HDF5?) or files (HDF5)"""

    HEADER_NAMES = ("dataset",)

    def _getTomoObject(self, obj: str, allow_several: bool = False):
        """
        some rules to return a TomwerObject from an object (probably a path) from children class
        """
        return self.getScanObject(obj, allow_several=allow_several)

    @staticmethod
    def getScanObject(obj, allow_several: bool = False):
        if not isinstance(obj, str):
            raise TypeError(f"obj is an instance of {type(obj)} when {str} expected")
        try:
            scan_obj = ScanFactory.create_tomo_object_from_identifier(obj)
        except ValueError as e1:
            try:
                if allow_several:
                    scan_obj = ScanFactory.create_scan_objects(obj)
                else:
                    scan_obj = ScanFactory.create_scan_object(obj)
            except Exception as e2:
                logger.warning(
                    f"Unable to create scan object from identifier ({e1}) or as a file or a folder ({e2})"
                )
                return None
            else:
                return scan_obj
        else:
            return scan_obj


class BlissScanList(_TomwerObjectList):
    """
    Widget dedicated to convert bliss entries to TomwerScanBase)
    """

    HEADER_NAMES = ("bliss scan",)

    def __init__(self, parent):
        self._configuration = H52nxModel()
        super().__init__(parent)

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, config: H52nxModel):
        assert isinstance(
            config, H52nxModel
        ), "config is expect to be an instance of dict"
        self._configuration = config

    def _update(self):
        list_data = list(self._myitems.keys())
        self.clear()
        for data in list_data:
            self.add(data)
        self.sortByColumn(0, self.horizontalHeader().sortIndicatorOrder())

    def add(self, data) -> tuple:
        """Add the path folder d in the scan list

        :param data: the path of the directory to add
        """
        possible_entries = []
        if os.path.exists(data):
            if not BlissScan.is_bliss_file(data):
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Warning)
                types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
                msg.setStandardButtons(types)

                if NXtomoScan.is_nexus_nxtomo_file(data):
                    text = (
                        f"The input file `{data}` seems to contain `NXTomo` entries. "
                        "and no valid `Bliss` valid entry. \n"
                        "This is probably not a Bliss file. Do you still want to translate ?"
                    )
                else:
                    text = (
                        f"The input file `{data}` does not seems to contain any "
                        "valid `Bliss` entry. \n"
                        "This is probably not a Bliss file. Do you still want to translate ?"
                    )
                msg.setText(text)
                if msg.exec() != qt.QMessageBox.Ok:
                    return

            try:
                for entry in nxtomomill_converter.get_bliss_tomo_entries(
                    data, self.configuration
                ):
                    possible_entries.append(entry)
            except Exception:
                logger.error(f"Faild to find entries for {data}")
                return
            else:
                file_path = data
        else:
            identifier = NXtomoScanIdentifier.from_str(data)
            possible_entries.append(identifier.data_path)
            file_path = identifier.file_path
        created_scans = []
        for entry in possible_entries:
            scan = NXtomoScan(scan=file_path, entry=entry)
            scan_objs = super().add(scan)
            if scan_objs is not None:
                for scan_obj in scan_objs:
                    created_scans.append(scan_obj)
        return created_scans


class EDFDataList(_TomwerObjectList):
    HEADER_NAMES = ("edf scan url",)

    def __init__(self, parent):
        super().__init__(parent)

    def _getTomoObject(self, obj: str, allow_several: bool = False):
        # note: allow several is not used there. No sense for EDF scan
        try:
            tomo_obj = ScanFactory.create_scan_object(obj)
        except Exception as e1:
            try:
                tomo_obj = ScanFactory.create_tomo_object_from_identifier(obj)
            except Exception as e2:
                logger.warning(
                    f"Unable to create a EDFVolume from {obj}. Error is {e1} or {e2}"
                )
                return

        if isinstance(tomo_obj, EDFTomoScan):
            return tomo_obj
        else:
            logger.warning(
                f"Unable to create a EDFVolume from {obj}. But creates a {type(tomo_obj)}. Atre you sure provided path leads to EDF acquisition ?"
            )
            return None

    def getEDFTomoScan(self, scan_id: str, default=None):
        if scan_id in self._myitems:
            return self._myitems[scan_id].data(qt.Qt.UserRole)
        else:
            return default


class VolumeList(_TomwerObjectList):
    """
    Widget dedicated to the VolumeBase object
    """

    HEADER_NAMES = ("volume url",)

    def _getTomoObject(self, obj: str, allow_several: bool = False):
        return self.getVolumeObject(obj=obj, allow_several=allow_several)

    @staticmethod
    def getVolumeObject(obj, allow_several: bool = False, warn=True):
        """
        get volume from identifier... even if not contained in the list of items (using factory)
        """
        try:
            tomo_obj = VolumeFactory.create_tomo_object_from_identifier(obj)
        except Exception as e:
            try:
                tomo_obj = guess_volumes(obj, scheme_to_vol=DEFAULT_SCHEME_TO_VOL)
            except Exception:
                if warn:
                    logger.warning(
                        f"Unable to create a volume from {obj}. Error is {e}"
                    )
                return None
            else:
                # filter potential 'nabu histogram'
                if tomo_obj is not None:

                    def is_not_histogram(vol_identifier):
                        return not (
                            hasattr(vol_identifier, "data_path")
                            and vol_identifier.data_path.endswith("histogram")
                        )

                    tomo_obj = tuple(filter(is_not_histogram, tomo_obj))

                if tomo_obj is None or len(tomo_obj) == 0:
                    logger.warning(f"Unable to create a volume from {obj}.")
                    return None
                else:
                    if len(tomo_obj) > 1 and not allow_several:
                        if warn:
                            logger.warning(
                                f"more than one volume deduce from {obj}. Will only take the first one ({tomo_obj[0]})"
                            )
                        return tomo_obj[0]
                    elif len(tomo_obj) == 1:
                        return tomo_obj[0]
                    else:
                        return tomo_obj
        else:
            return tomo_obj

    def getVolume(self, volume_id: str, default=None):
        """
        get volume from id contained in the current items, else default
        """
        if volume_id in self._myitems:
            return self._myitems[volume_id].data(qt.Qt.UserRole)
        else:
            return default


class TomoObjList(_TomwerObjectList):
    HEADER_NAMES = ("tomo object",)

    def _getTomoObject(self, obj: str, allow_several: bool = False):
        try:
            tomo_obj = VolumeList.getVolumeObject(obj=obj, allow_several=allow_several)
        except Exception:
            pass
        else:
            if tomo_obj not in (None, tuple()):
                return tomo_obj

        try:
            tomo_obj = GenericScanList.getScanObject(
                obj=obj, allow_several=allow_several
            )
        except Exception:
            return None
        else:
            return tomo_obj

    def getTextToDisplay(self, obj: TomwerObject):
        return obj.get_identifier().short_description()
