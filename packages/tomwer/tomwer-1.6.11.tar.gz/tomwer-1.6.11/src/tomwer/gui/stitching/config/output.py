import logging

from nabu.stitching import config as stitching_config
from nabu.stitching.config import StitchingType
from nxtomomill.models.utils import convert_str_to_bool
from silx.gui import qt

from tomwer.core.scan.nxtomoscan import NXtomoScan, NXtomoScanIdentifier
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.gui.utils.inputwidget import OutputVolumeDefinition
from tomwer.gui.qlefilesystem import QLFileSystem
from silx.io.url import DataUrl

_logger = logging.getLogger(__name__)


class _PreProcessingOutput(qt.QWidget):
    """
    Define output settings for the pre processing z stitching
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())
        # TODO: check if the widget with output .nx file exists somewhere
        # output file
        self._outputFile = QLFileSystem("", self)
        self._outputFileLabel = qt.QLabel("output nexus file")
        self.layout().addWidget(self._outputFileLabel, 0, 0, 1, 1)
        self.layout().addWidget(self._outputFile, 0, 1, 1, 1)
        self._selectPB = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectPB, 0, 2, 1, 1)

        self._outputDataPathLabel = qt.QLabel("output data path")
        self.layout().addWidget(self._outputDataPathLabel, 1, 0, 2, 1)
        self._outputDataPath = qt.QLineEdit("", self)
        self._outputDataPath.setToolTip("Location of the dataset **inside** the file.")
        self.layout().addWidget(self._outputDataPath, 1, 1, 1, 2)

        # connect signal / slot
        self._selectPB.released.connect(self._selectNxTomoFile)

    def getUrl(self) -> str:
        return NXtomoScanIdentifier(
            object=NXtomoScan,
            hdf5_file=self._outputFile.text(),
            entry=self._outputDataPath.text(),
        )

    def setUrl(self, url: str):
        try:
            identifier = NXtomoScanIdentifier.from_str(url)
        except Exception as e:
            _logger.warning(f"Fail to create an identifier from {url}. Error is {e}")
        else:
            self._outputFile.setText(identifier.file_path)
            self._outputDataPath.setText(identifier.data_path)

    def _selectNxTomoFile(self):
        dialog = qt.QFileDialog(self)
        dialog.setNameFilters(
            [
                "Any files (*)",
                "HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                "Nexus files (*.nx *.nxs *.nexus)",
            ]
        )
        if not dialog.exec():
            dialog.close()
        elif len(dialog.selectedFiles()) == 0:
            return
        else:
            self._outputFile.setText(dialog.selectedFiles()[0])


class _PostProcessingOutput(OutputVolumeDefinition):
    """
    Define output settings for the post processing z stitching
    """

    def getUrl(self) -> str:
        return self.getOutputVolumeIdentifier().to_str()

    def setUrl(self, url: str):
        self.setOutputVolumeIdentifier(url)


class StitchingOutput(qt.QWidget):
    """
    Defines the output of the stitching
    """

    sigChanged = qt.Signal()
    """emit when stithcing output change"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.__stitching_type = None
        self.setLayout(qt.QVBoxLayout())
        self._preProcOutput = _PreProcessingOutput(parent=self)
        self.layout().addWidget(self._preProcOutput)
        self._postProcOutput = _PostProcessingOutput(parent=self)
        self.layout().addWidget(self._postProcOutput)
        self._overwritePB = qt.QCheckBox("Overwrite", self)
        self._overwritePB.setChecked(True)
        self.layout().addWidget(self._overwritePB)

        # add a vertical spacer for display
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        self._updateOutputForStitchingType(StitchingType.Z_PREPROC)

    def _updateOutputForStitchingType(self, stitching_type):
        self.__stitching_type = StitchingType(stitching_type)
        self._preProcOutput.setVisible(self.__stitching_type is StitchingType.Z_PREPROC)
        self._postProcOutput.setVisible(
            self.__stitching_type is StitchingType.Z_POSTPROC
        )

    def getConfiguration(self) -> dict:
        config = {
            stitching_config.OUTPUT_SECTION: {
                stitching_config.OVERWRITE_RESULTS_FIELD: self._overwritePB.isChecked()
            },
        }
        if self.__stitching_type is StitchingType.Z_POSTPROC:
            config.update(
                {
                    stitching_config.POST_PROC_SECTION: {
                        stitching_config.OUTPUT_VOLUME: self._postProcOutput.getUrl()
                    },
                }
            )
            return config

        elif self.__stitching_type is StitchingType.Z_PREPROC:
            url = self._preProcOutput.getUrl()
            try:
                scan = ScanFactory.create_tomo_object_from_identifier(url)
            except Exception:
                scan = None

            if not isinstance(scan, NXtomoScan):
                _logger.warning("Failed to create an HDF5Tomoscan from url")
                pass
            else:
                config.update(
                    {
                        stitching_config.PRE_PROC_SECTION: {
                            stitching_config.DATA_FILE_FIELD: scan.master_file,
                            stitching_config.DATA_PATH_FIELD: scan.entry,
                        },
                    }
                )
            return config
        else:
            raise NotImplementedError

    def setConfiguration(self, config: dict):
        stitching_type = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.STITCHING_TYPE_FIELD, None
        )
        if stitching_type is not None:
            self._updateOutputForStitchingType(stitching_type)

        output_volume = config.get(stitching_config.POST_PROC_SECTION, {}).get(
            stitching_config.OUTPUT_VOLUME, None
        )
        if output_volume:
            self._postProcOutput.setUrl(output_volume)

        location = config.get(stitching_config.PRE_PROC_SECTION, {}).get(
            stitching_config.DATA_FILE_FIELD, None
        )
        data_path = config.get(stitching_config.PRE_PROC_SECTION, {}).get(
            stitching_config.DATA_PATH_FIELD, None
        )
        if location is not None:
            identifier = NXtomoScanIdentifier(
                object=NXtomoScan, hdf5_file=location, entry=data_path
            )
            self._preProcOutput.setUrl(identifier.to_str())

        overwrite = config.get(stitching_config.OUTPUT_SECTION, {}).get(
            stitching_config.OVERWRITE_RESULTS_FIELD, None
        )
        if overwrite is not None:
            overwrite = convert_str_to_bool(overwrite)
            self._overwritePB.setChecked(overwrite)

    # expose API
    def setPreProcessingOutput(self, identifier: str) -> None:
        self._preProcOutput.setUrl(identifier)

    def setPostProcessingOutput(self, identifier: DataUrl) -> None:
        self._postProcOutput.setUrl(identifier)
