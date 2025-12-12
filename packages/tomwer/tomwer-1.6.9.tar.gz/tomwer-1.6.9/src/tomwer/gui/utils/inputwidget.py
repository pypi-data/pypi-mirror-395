from __future__ import annotations

import logging
import os

import numpy
from nxtomomill.models.h52nx import H52nxModel
from nxtomomill.models.edf2nx import EDF2nxModel

from silx.gui import qt

from tomoscan.identifier import BaseIdentifier

from tomwer.gui import icons
from tomwer.gui.qlefilesystem import QLFileSystem
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.io.utils import get_default_directory
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.process.output import ProcessDataOutputDirMode

from tomwer.core.volume import (
    EDFVolume,
    HDF5Volume,
    JP2KVolume,
    RawVolume,
    TIFFVolume,
    MultiTIFFVolume,
)

_logger = logging.getLogger(__name__)


class SelectionLineEdit(qt.QWidget):
    """Line edit with several type of selection possible:

    * a single value
    * a range of value on the type min:max:step
    * a list of value: val1, val2, ...
    """

    # SINGLE_MODE = 'single'
    RANGE_MODE = "range"
    LIST_MODE = "list"

    # SELECTION_MODES = (SINGLE_MODE, RANGE_MODE, LIST_MODE)
    SELECTION_MODES = (RANGE_MODE, LIST_MODE)

    _DEFAULT_SELECTION = LIST_MODE

    def __init__(self, text=None, parent=None, allow_negative_indices=False):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self._qLineEdit = qt.QLineEdit(parent=self)
        if allow_negative_indices:
            fpm = "\\-?\\d*\\.?\\d+"  # float or int matching
        else:
            fpm = "\\d*\\.?\\d+"  # float or int matching
        qRegExp = qt.QRegularExpression(
            "(" + fpm + "[;]?[,]?[ ]?){1,}" + "|" + ":".join((fpm, fpm, fpm))
        )
        self._qLineEdit.setValidator(qt.QRegularExpressionValidator(qRegExp))
        self.layout().addWidget(self._qLineEdit)
        self._button = SelectionModeButton(parent=self)
        self.layout().addWidget(self._button)

        # QObject signal connections
        self._qLineEdit.textChanged.connect(self._checkIfModeChanged)
        self._button.sigModeChanged.connect(self._modeChanged)

        # expose API
        self.setText = self._qLineEdit.setText
        self.editingFinished = self._qLineEdit.editingFinished
        self.textChanged = self._qLineEdit.textChanged
        self.text = self._qLineEdit.text

        if text is not None:
            self._qLineEdit.setText(str(text))
        # update place holders
        self._modeChanged(self._button.mode)

    def getMode(self):
        return self._button.mode

    @property
    def selection(self):
        if self._qLineEdit.hasAcceptableInput():
            if self._button.mode == self.RANGE_MODE:
                _from, _to, _step = self._qLineEdit.text().split(":")
                _from, _to, _step = float(_from), float(_to), float(_step)
                if _from > _to:
                    _logger.warning(f"to > from, invert {_from} and {_to}")
                    tmp = _to
                    _to = _from
                    _from = tmp
                num = int((_to - _from) / _step)
                return tuple(
                    numpy.linspace(start=_from, stop=_to, num=num, endpoint=True)
                )
            else:
                vals = self._qLineEdit.text().replace(" ", "")
                vals = vals.replace(";", ",").split(",")
                res = []
                [res.append(float(val)) for val in vals]
                if len(res) == 1:
                    return res[0]
                else:
                    return tuple(res)
        else:
            _logger.warning("Wrong input, invalid selection")
            return None

    def _checkIfModeChanged(self, _str):
        with block_signals(self._button):
            if _str.count(":") > 0:
                self._button.mode = self.RANGE_MODE
            else:
                self._button.mode = self.LIST_MODE

    def _modeChanged(self, mode):
        if mode == self.RANGE_MODE:
            text = "from:to:step"
        elif mode == self.LIST_MODE:
            text = "val1; val2; ..."
        else:
            raise ValueError("unknown mode")

        with block_signals(self._qLineEdit):
            self._qLineEdit.setPlaceholderText(text)


class SelectionModeButton(qt.QToolButton):
    """Base class for Selection QAction.

    :param mode: the mode of selection of the action.
    :param text: The name of this action to be used for menu label
    :param tooltip: The text of the tooltip
    :param triggered: The callback to connect to the action's triggered
                      signal or None for no callback.
    """

    sigModeChanged = qt.Signal(str)
    """signal emit when the mode is changed"""

    def __init__(self, parent=None, tooltip=None, triggered=None):
        qt.QToolButton.__init__(self, parent)
        self._states = {}
        self._mode = None
        for mode in SelectionLineEdit.SELECTION_MODES:
            icon = icons.getQIcon("_".join([mode, "selection"]))
            self._states[mode] = (icon, self._getTooltip(mode))

        self._rangeAction = RangeSelAction(parent=self)
        self._listAction = ListSelAction(parent=self)
        for _action in (self._rangeAction, self._listAction):
            _action.sigModeChanged.connect(self._modeChanged)

        menu = qt.QMenu(self)
        menu.addAction(self._rangeAction)
        menu.addAction(self._listAction)
        self.setMenu(menu)
        self.setPopupMode(qt.QToolButton.InstantPopup)
        self.mode = SelectionLineEdit.LIST_MODE

    def _getTooltip(self, mode):
        # if mode == SelectionLineEdit.SINGLE_MODE:
        #     return 'Define only one value for this parameter'
        if mode == SelectionLineEdit.LIST_MODE:
            return (
                "Define a single value or a list of values for this "
                "parameter (va1; val2)"
            )
        elif mode == SelectionLineEdit.RANGE_MODE:
            return "Define a range of value for this parameter (from:to:step)"
        else:
            raise ValueError("unknown mode")

    def _modeChanged(self, mode):
        self.mode = mode

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        assert mode in SelectionLineEdit.SELECTION_MODES
        if mode != self._mode:
            self._mode = mode
            self.setIcon(icons.getQIcon("_".join([mode, "selection"])))
            self.setToolTip(self._getTooltip(mode))
            self.sigModeChanged.emit(self._mode)


class SelectionAction(qt.QAction):
    """
    Base class of the several selection mode
    """

    sigModeChanged = qt.Signal(str)
    """emit when the mode change"""

    def __init__(self, mode, parent, text):
        icon = icons.getQIcon("_".join([mode, "selection"]))
        qt.QAction.__init__(self, icon, text, parent)
        self.setIconVisibleInMenu(True)
        self._mode = mode
        self.triggered.connect(self._modeChanged)

    def _modeChanged(self, *args, **kwargs):
        self.sigModeChanged.emit(self._mode)


class RangeSelAction(SelectionAction):
    """
    Action to select a range of element on the scheme from:to:step
    """

    def __init__(self, parent=None):
        SelectionAction.__init__(
            self,
            mode=SelectionLineEdit.RANGE_MODE,
            parent=parent,
            text="range selection",
        )


class ListSelAction(SelectionAction):
    """
    Action to select a list of element on the scheme elmt1, elmt2, ...
    """

    def __init__(self, parent=None):
        SelectionAction.__init__(
            self, mode=SelectionLineEdit.LIST_MODE, parent=parent, text="list selection"
        )


class NXTomomillOutputDirSelector(qt.QWidget):
    sigChanged = qt.Signal()
    """Signal emit when the output directory of the nx file change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self.__buttonGroup = qt.QButtonGroup(self)
        self.__buttonGroup.setExclusive(True)

        tooltip = """Define the output directory of the nexus (.nx) file. Options are:
        \n - same folder as scan: create the NXtomos at the same level as the bliss input file or spec folder
        \n - 'PROCESSED_DATA' folder: create NXtomos on the default 'PROCESSED_DATA' folder (bliss default folder, nearby the 'raw' folder).
        \n - user defined folder: users can provide their own folders using keywords for string formatting such as 'scan_dir_name', 'scan_basename' or 'scan_parent_dir_basename', 'scan_file_name' and 'scan_entry'
        """

        # output dir is the folder containing the .nx file
        self._inScanFolder = qt.QRadioButton("same folder as scan", self)
        self._inScanFolder.setToolTip(tooltip)
        self.layout().addWidget(self._inScanFolder, 0, 0, 1, 1)
        self.__buttonGroup.addButton(self._inScanFolder)
        # output dir is the default 'reduced'folder
        self._processedDataFolderRB = qt.QRadioButton("'PROCESSED_DATA' folder", self)
        self._processedDataFolderRB.setToolTip(tooltip)
        self.layout().addWidget(self._processedDataFolderRB, 1, 0, 1, 1)
        self.__buttonGroup.addButton(self._processedDataFolderRB)
        # manual
        self._manualRB = qt.QRadioButton("custom output directory", self)
        self._manualRB.setToolTip(tooltip)
        self.layout().addWidget(self._manualRB, 3, 0, 1, 1)
        self._outputFolderQLE = QLFileSystem("", self)
        self.layout().addWidget(self._outputFolderQLE, 3, 1, 1, 1)
        self._selectButton = qt.QPushButton("", self)
        style = qt.QApplication.style()
        icon_opendir = style.standardIcon(qt.QStyle.SP_DirOpenIcon)
        self._selectButton.setIcon(icon_opendir)
        self._selectButton.setToolTip("select output directory")
        self.layout().addWidget(self._selectButton, 3, 2, 1, 1)
        self.__buttonGroup.addButton(self._manualRB)

        # connect signal / slot
        self._selectButton.released.connect(self._selectOutpuFolder)
        self.__buttonGroup.buttonReleased.connect(self._updateVisiblity)
        self._inScanFolder.toggled.connect(self.sigChanged)
        self._processedDataFolderRB.toggled.connect(self.sigChanged)
        self._manualRB.toggled.connect(self.sigChanged)
        self._outputFolderQLE.editingFinished.connect(self.sigChanged)

        # set up
        self._processedDataFolderRB.setChecked(True)
        self._updateVisiblity()

    def _updateVisiblity(self, *args, **kwargs):
        self._selectButton.setVisible(self._manualRB.isChecked())
        self._outputFolderQLE.setVisible(self._manualRB.isChecked())

    def _selectOutpuFolder(self):  # pragma: no cover
        defaultDirectory = self._outputFolderQLE.text()
        if os.path.isdir(defaultDirectory):
            defaultDirectory = get_default_directory()

        dialog = qt.QFileDialog(self, directory=defaultDirectory)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec():
            dialog.close()
            return

        self._outputFolderQLE.setText(dialog.selectedFiles()[0])
        self.sigChanged.emit()

    def getOutputFolder(self) -> str | ProcessDataOutputDirMode:
        if self._manualRB.isChecked():
            return self._outputFolderQLE.text()
        elif self._processedDataFolderRB.isChecked():
            return ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER
        elif self._inScanFolder.isChecked():
            return ProcessDataOutputDirMode.IN_SCAN_FOLDER
        else:
            raise RuntimeError("Use case - h52nx output dir - not handled")

    def setOutputFolder(self, output_folder: str):
        with block_signals(self):
            self._manualRB.setChecked(output_folder is not None)
            try:
                default_output = ProcessDataOutputDirMode.from_value(output_folder)
            except ValueError:
                self._outputFolderQLE.setText(output_folder)
                self._manualRB.setChecked(True)
            else:
                if default_output is ProcessDataOutputDirMode.IN_SCAN_FOLDER:
                    self._inScanFolder.setChecked(True)
                elif default_output is ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER:
                    self._processedDataFolderRB.setChecked(True)
                else:
                    raise ValueError(f"default output not handled ({default_output})")
            finally:
                self._updateVisiblity()


class _ConfigFileSelector(qt.QWidget):
    """Widget used to select a configuration file. Originally used for
    NXtomomill"""

    sigConfigFileChanged = qt.Signal(str)
    """signal emitted when the edition of the file path is finished"""

    def __init__(self, parent=None, try_load_cfg: bool = True):
        """
        :param try_load_cfg: If True then when a file path is provided will try to load the configuration using '_load_config' and display error if the file is malformed
        """
        super().__init__(parent)
        self._try_load_cfg = try_load_cfg
        self.setLayout(qt.QHBoxLayout())
        self._lineEdit = QLFileSystem("", self)
        self.layout().addWidget(self._lineEdit)
        self._selectButton = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectButton)
        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        self._clearButton = qt.QPushButton(self)
        self._clearButton.setIcon(icon)
        self.layout().addWidget(self._clearButton)

        # connect signal / slot button
        self._clearButton.released.connect(self._clearFilePath)
        self._selectButton.released.connect(self._selectCFGFile)
        self._lineEdit.editingFinished.connect(self._editedFinished)

    def _clearFilePath(self):
        self._lineEdit.clear()

    def _selectCFGFile(self):  # pragma: no cover
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.ExistingFile)

        if not dialog.exec():
            dialog.close()
            return
        if len(dialog.selectedFiles()) > 0:
            file_path = dialog.selectedFiles()[0]
            self.setCFGFilePath(file_path)

    def _editedFinished(self):
        # try to convert the file and inform the use if this fails
        cfg_file = self.getCFGFilePath()
        if cfg_file not in (None, ""):
            if self._try_load_cfg:
                try:
                    self._load_config_file(cfg_file)
                except Exception as e:
                    mess = f"Fail to load nxtomomill configuration from {cfg_file}. Error is {e}"
                    _logger.warning(mess)
                    qt.QMessageBox.warning(
                        self, "Unable to read configuration from file", mess
                    )
                else:
                    _logger.info(f"Will use {cfg_file} as input configuration file.")
        self.sigConfigFileChanged.emit(cfg_file)

    def getCFGFilePath(self):
        return self._lineEdit.text()

    def setCFGFilePath(self, cfg_file):
        self._lineEdit.setText(cfg_file)
        self._lineEdit.editingFinished.emit()

    def _load_config_file(self, cfg_file: str):
        raise NotImplementedError("Base class")


class HDF5ConfigFileSelector(_ConfigFileSelector):
    def _load_config_file(self, cfg_file: str):
        H52nxModel.from_cfg_file(cfg_file)


class EDFConfigFileSelector(_ConfigFileSelector):
    def _load_config_file(self, cfg_file: str):
        EDF2nxModel.from_cfg_file(cfg_file)


class OutputVolumeDefinition(qt.QWidget):
    DEFAULT_DATA_PATH = "stitched_volume"

    _OUTPUT_FILE_PATH_TXT = "output file"

    _OUTPUT_FOLDER_PATH_TXT = "output folder"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())
        # define format
        self._formatLabel = qt.QLabel("format", self)
        self.layout().addWidget(self._formatLabel, 0, 0, 1, 1)
        self._outputFileFormatCB = qt.QComboBox(parent=self)
        self._outputFileFormatCB.addItem("hdf5")
        for volume in (EDFVolume, JP2KVolume, RawVolume, TIFFVolume):
            self._outputFileFormatCB.addItem(volume.DEFAULT_DATA_EXTENSION)
        self.layout().addWidget(self._outputFileFormatCB, 0, 1, 1, 2)

        # output file or folder
        self._outputFileLabel = qt.QLabel("", self)
        self.layout().addWidget(self._outputFileLabel, 1, 0, 1, 1)
        self._outputFileQLE = QLFileSystem(
            os.path.join(
                os.getcwd(),
                "stitched_volume.hdf5",
            ),
            parent=None,
        )
        self.layout().addWidget(self._outputFileQLE, 1, 1, 1, 1)
        self._selectPB = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectPB, 1, 2, 1, 1)

        # output data path
        self._outputDataPathLabel = qt.QLabel("output path", self)
        self.layout().addWidget(self._outputDataPathLabel, 2, 0, 1, 1)
        self._outputDataPathQLE = qt.QLineEdit(self.DEFAULT_DATA_PATH, self)
        self.layout().addWidget(self._outputDataPathQLE, 2, 1, 1, 2)

        # connect signal / path
        self._selectPB.released.connect(self._selectCurrentFileFormatOutputPath)
        self._outputFileFormatCB.currentIndexChanged.connect(self._fileFormatChanged)

        # set up
        self.setOuputVolumeFormat("hdf5")
        # force label update
        self._fileFormatChanged()

    def _fileFormatChanged(self, *args, **kwargs):
        extension = self.getOutputVolumeFormat()
        self._outputDataPathLabel.setVisible(extension == "hdf5")
        self._outputDataPathQLE.setVisible(extension == "hdf5")
        if extension == "hdf5":
            self._outputFileLabel.setText(self._OUTPUT_FILE_PATH_TXT)
        else:
            self._outputFileLabel.setText(self._OUTPUT_FOLDER_PATH_TXT)

    def _selectCurrentFileFormatOutputPath(self):
        extension = self.getOutputVolumeFormat()
        if extension == "hdf5":
            return self.selectOutputFile(
                extensions=[
                    "HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                    "Nexus files (*.nx *.nxs *.nexus)",
                    "Any files (*)",
                ]
            )
        else:
            return self.selectOutputFolder()

    def selectOutputFile(self, extensions) -> str | None:
        dialog = qt.QFileDialog(self)
        dialog.setNameFilters(extensions)
        dialog.setAcceptMode(qt.QFileDialog.AcceptSave)

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
            return None
        else:
            return dialog.selectedFiles()

    def selectOutputFolder(self) -> str | None:
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)
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

        return dialog.selectedFiles()

    def getOutputVolumeFormat(self) -> str:
        return self._outputFileFormatCB.currentText()

    def setOuputVolumeFormat(self, file_format: str):
        idx = self._outputFileFormatCB.findText(file_format)
        if idx >= 0:
            self._outputFileFormatCB.setCurrentIndex(idx)

    def getOutputDataPath(self) -> str:
        return self._outputDataPathQLE.text()

    def setOutputDataPath(self, data_path: str):
        self._outputDataPathQLE.setText(data_path)

    def getOutputFilePath(self) -> str:
        return self._outputFileQLE.text()

    def setOutputFilePath(self, file_path: str):
        self._outputFileQLE.setText(file_path)

    def getOutputVolumeIdentifier(self) -> BaseIdentifier:
        volume_format = self.getOutputVolumeFormat()
        file_path = self.getOutputFilePath()

        if volume_format in ("hdf5", "h5", "hdf", "nx"):
            data_path = self.getOutputDataPath()
            if data_path == "":
                data_path = self.DEFAULT_DATA_PATH
            return HDF5Volume(
                file_path=file_path,
                data_path=data_path,
            ).get_identifier()
        elif volume_format == EDFVolume.DEFAULT_DATA_EXTENSION:
            return EDFVolume(
                folder=file_path,
            ).get_identifier()
        elif volume_format == JP2KVolume.DEFAULT_DATA_EXTENSION:
            return JP2KVolume(
                folder=file_path,
            ).get_identifier()
        elif volume_format == RawVolume.DEFAULT_DATA_EXTENSION:
            return RawVolume(
                file_path=file_path,
            ).get_identifier()
        elif volume_format == TIFFVolume.DEFAULT_DATA_EXTENSION:
            return TIFFVolume(
                folder=file_path,
            ).get_identifier()
        else:
            raise RuntimeError(f"format {volume_format} is not handled")

    def setOutputVolumeIdentifier(self, url):
        volume = VolumeFactory.create_tomo_object_from_identifier(url)

        file_format = (
            "hdf5" if isinstance(volume, HDF5Volume) else volume.DEFAULT_DATA_EXTENSION
        )
        self.setOuputVolumeFormat(file_format=file_format)
        if isinstance(volume, HDF5Volume):
            self.setOutputDataPath(volume.data_path)
            self.setOutputFilePath(volume.file_path)
        elif isinstance(
            volume, (EDFVolume, TIFFVolume, JP2KVolume, RawVolume, MultiTIFFVolume)
        ):
            self.setOutputFilePath(volume.data_url.file_path())
        else:
            raise ValueError(f"volume type ({type(volume)}) is not handled")
