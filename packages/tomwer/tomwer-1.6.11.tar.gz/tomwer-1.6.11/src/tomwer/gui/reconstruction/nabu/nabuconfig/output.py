# coding: utf-8
from __future__ import annotations


import logging
import os

from silx.gui import qt

from tomwer.core.process.reconstruction.output import NabuOutputFileFormat
from tomwer.core.process.reconstruction.nabu.utils import _NabuStages
from tomwer.core.process.reconstruction.output import ProcessDataOutputDirMode
from tomwer.gui.qlefilesystem import QLFileSystem
from tomwer.gui.reconstruction.nabu.nabuconfig.base import _NabuStageConfigBase
from tomwer.io.utils import get_default_directory

try:
    import glymur  # noqa #F401 needed for later possible lazy loading
except ImportError:
    has_glymur = False
else:
    has_glymur = True

_logger = logging.getLogger(__name__)


class QNabuFileFormatComboBox(qt.QComboBox):
    def __init__(self, parent: qt.QWidget | None = ..., filter_formats=tuple()) -> None:
        """
        :param filter_format: if provided the given file format won't have an item on the ComboBox
        """
        super().__init__(parent=parent)
        if not isinstance(filter_formats, tuple):
            raise TypeError(
                f"filter_format should be a tuple. Get {type(filter_formats)} instead"
            )
        filter_formats = [
            NabuOutputFileFormat.from_value(file_format)
            for file_format in filter_formats
        ]

        for ff in NabuOutputFileFormat:
            if ff in filter_formats:
                continue
            if ff is NabuOutputFileFormat.JP2K:
                if not has_glymur:
                    _logger.warning(
                        "could not load jp2k format, glymur and OpenJPEG requested"
                    )
                else:
                    from glymur import version

                    if version.openjpeg_version < "2.3.0":
                        _logger.warning(
                            "You must have at least version 2.3.0 of OpenJPEG "
                            "in order to write jp2k images."
                        )
                    else:
                        self.addItem(ff.value)
            else:
                self.addItem(ff.value)


class QNabuFileFormatComboBoxIgnoreWheel(QNabuFileFormatComboBox):
    def wheelEvent(self, e: qt.QWheelEvent) -> None:
        pass


class NabuOutputLocationWidget(qt.QGroupBox):
    sigOutputChanged = qt.Signal()
    """Emit when location changed"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(title="output folder", *args, **kwargs)
        self.setLayout(qt.QGridLayout())

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # in scan folder
        self._inScanFolderRB = qt.QRadioButton(
            ProcessDataOutputDirMode.IN_SCAN_FOLDER.value, self
        )
        self._inScanFolderRB.setToolTip(
            "Reconstruction will be saved at the same level as the acquisition folder. (near the NXtomo file (.nx) or under the spec acquisition folder)"
        )
        self.layout().addWidget(self._inScanFolderRB, 1, 0, 1, 1)
        # in processed data dir
        self._processedDataDirRB = qt.QRadioButton(
            ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER.value, self
        )
        self._inScanFolderRB.setToolTip(
            "Reconstruction will be saved under the PROCESSED_DATA/dataset folder. if exists else under the scan folder."
        )
        self.layout().addWidget(self._processedDataDirRB, 2, 0, 1, 1)
        # other dir
        self._otherDirRB = qt.QRadioButton(ProcessDataOutputDirMode.OTHER.value, self)
        self._otherDirRB.setToolTip(
            "Reconstruction will be saved under user provided folder."
        )
        self.layout().addWidget(self._otherDirRB, 4, 0, 1, 1)
        self._outputDirQLE = QLFileSystem(
            "", self, filters=qt.QDir.NoDotAndDotDot | qt.QDir.Dirs
        )
        self.layout().addWidget(self._outputDirQLE, 4, 1, 1, 1)
        style = qt.QApplication.style()
        icon_opendir = style.standardIcon(qt.QStyle.SP_DirOpenIcon)
        self._selectOutputPB = qt.QPushButton(icon_opendir, "", self)
        self._selectOutputPB.setIcon(icon_opendir)
        general_tooltip = (
            "You can enter a string with some keywords like {my_keyword}. Those will be interpreted during runtime according to scan metadata. Possible keywords are:"
            + "\n - 'scan_dir_name': returns name of the directory containing the acquisition (! not a path !)"
            + "\n - 'scan_basename': returns basename of the directory containing the acquisition"
            + "\n - 'scan_parent_dir_basename': returns basename of the PARENT directory containing the acquisition"
            + "\n - 'scan_file_name': for NXtomo scans only. Return the name of the file containing the NXtomo"
            + "\n - 'scan_entry': for NXtomo scans only. Return the name of the entry containing the NXtomo"
        )

        self._selectOutputPB.setToolTip(general_tooltip)
        self._outputDirQLE.setToolTip(general_tooltip)
        self.layout().addWidget(self._selectOutputPB, 4, 2, 1, 1)

        # set up:
        self._inScanFolderRB.setChecked(True)

        # connect signal / slot
        self._inScanFolderRB.toggled.connect(self._outputModeChanged)
        self._processedDataDirRB.toggled.connect(self._outputModeChanged)
        self._otherDirRB.toggled.connect(self._outputModeChanged)
        self._selectOutputPB.released.connect(self._selectOutput)
        self._inScanFolderRB.setChecked(True)
        self._outputModeChanged()

    def getOutputDirMode(self) -> ProcessDataOutputDirMode:
        if self._inScanFolderRB.isChecked():
            return ProcessDataOutputDirMode.IN_SCAN_FOLDER
        elif self._processedDataDirRB.isChecked():
            return ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER
        elif self._otherDirRB.isChecked():
            return ProcessDataOutputDirMode.OTHER

    def setOutputDirMode(self, mode: ProcessDataOutputDirMode | str) -> None:
        mode = ProcessDataOutputDirMode.from_value(mode)
        if mode is ProcessDataOutputDirMode.IN_SCAN_FOLDER:
            self._inScanFolderRB.setChecked(True)
        elif mode is ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER:
            self._processedDataDirRB.setChecked(True)
        elif mode is ProcessDataOutputDirMode.OTHER:
            self._otherDirRB.setChecked(True)

    def _outputModeChanged(self, *args, **kwargs):
        outputMode = self.getOutputDirMode()
        self._outputDirQLE.setVisible(outputMode is ProcessDataOutputDirMode.OTHER)
        self._selectOutputPB.setVisible(outputMode is ProcessDataOutputDirMode.OTHER)
        self.sigOutputChanged.emit()

    def _selectOutput(self):  # pragma: no cover
        defaultDirectory = self._outputDirQLE.text()
        if not os.path.isdir(defaultDirectory):
            defaultDirectory = get_default_directory()

        dialog = qt.QFileDialog(self, directory=defaultDirectory)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec():
            dialog.close()
            return

        self._outputDirQLE.setText(dialog.selectedFiles()[0])

    def getOutputDir(self):
        """

        :return: None if the default output directory is selected else
                 return path to the directory
        """
        if self._otherDirRB.isChecked():
            return self._outputDirQLE.text()
        else:
            return None

    def setOutputDir(self, output_dir):
        if output_dir in (None, ""):
            pass
        else:
            self._outputDirQLE.setText(output_dir)


class _NabuOutputConfig(_NabuStageConfigBase, qt.QWidget):
    """
    Widget to define the output configuration of nabu
    """

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent):
        _NabuStageConfigBase.__init__(self, stage=_NabuStages.POST)
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        # output dir
        self._output_dir_widget = NabuOutputLocationWidget(parent=self)
        self.layout().addWidget(self._output_dir_widget, 0, 0, 1, 4)
        self.registerWidget(self._output_dir_widget, "advanced")

        # file format
        self._outputFileFormatLabel = qt.QLabel("output file format:", self)
        self.layout().addWidget(self._outputFileFormatLabel, 1, 0, 1, 1)
        self._fileFormatCB = QNabuFileFormatComboBoxIgnoreWheel(self)
        self.layout().addWidget(self._fileFormatCB, 1, 2, 1, 2)
        self.registerWidget(self._outputFileFormatLabel, "optional")
        self.registerWidget(self._fileFormatCB, "optional")

        # file per group
        self._filePerGroupLabel = qt.QLabel("frame per group:", self)
        self.layout().addWidget(self._filePerGroupLabel, 2, 0, 1, 1)
        self._framePerGroup = qt.QSpinBox(self)
        self._framePerGroup.setMinimum(100)
        self._framePerGroup.setSingleStep(50)
        self._framePerGroup.setMaximum(10000)
        # not managed for now so hide
        self._filePerGroupLabel.hide()
        self._framePerGroup.hide()
        self.layout().addWidget(self._framePerGroup, 2, 2, 1, 2)

        # spacer for style
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 200, 0, 1, 1)

        # set up
        self.setFramePerGroup(100)
        self.setFileformat("hdf5")

        # connect signal / slot
        self._output_dir_widget._outputDirQLE.editingFinished.connect(
            self._outputDirChanged
        )
        self._output_dir_widget.sigOutputChanged.connect(self._outputDirChanged)
        self._fileFormatCB.currentTextChanged.connect(self._fileFormatChanged)
        self._framePerGroup.valueChanged.connect(self._framePerGroupChanged)

    def _outputDirChanged(self):
        self.sigConfChanged.emit("location")

    def _fileFormatChanged(self):
        self.sigConfChanged.emit("file_format")

    def _framePerGroupChanged(self):
        self.sigConfChanged.emit("frames_per_group")

    def getOutputDir(self):
        return self._output_dir_widget.getOutputDir()

    def setOutputDir(self, dir):
        return self._output_dir_widget.setOutputDir(dir)

    def getOutputdirMode(self):
        return self._output_dir_widget.getOutputDirMode()

    def setOutputdirMode(self, mode):
        return self._output_dir_widget.setOutputDirMode(mode=mode)

    def getFileFormat(self) -> NabuOutputFileFormat:
        return NabuOutputFileFormat.from_value(self._fileFormatCB.currentText())

    def setFileformat(self, file_format):
        file_format = NabuOutputFileFormat.from_value(file_format)
        index = self._fileFormatCB.findText(file_format.value)
        self._fileFormatCB.setCurrentIndex(index)

    def getFramePerGroup(self):
        return self._framePerGroup.value()

    def setFramePerGroup(self, n_frames):
        self._framePerGroup.setValue(n_frames)

    def getConfiguration(self):
        return {
            "file_format": self.getFileFormat().value,
            "location": self.getOutputDir() or "",
            "output_dir_mode": self.getOutputdirMode().value,
            # 'frames_per_group': self.getFramePerGroup(),
        }

    def setConfiguration(self, config):
        if "file_format" in config:
            self.setFileformat(config["file_format"])
        location = config.get("location", None)
        if location == "":
            location = None
        if location is not None:
            self.setOutputDir(location)
        if "frames_per_group" in config:
            self.setFramePerGroup(int(config["frames_per_group"]))

        # definition of default_output_dir_mode ensure backward compatibility
        default_output_dir_mode = (
            None if location is None else ProcessDataOutputDirMode.OTHER
        )
        output_dir_mode = config.get("output_dir_mode", default_output_dir_mode)
        if output_dir_mode is not None:
            self.setOutputdirMode(output_dir_mode)
