from __future__ import annotations

import logging

from silx.gui import qt
from silx.gui.utils import blockSignals

from tomwer.core.process.reconstruction.nabu.castvolume import (
    DEFAULT_OUTPUT_DIR,
    RESCALE_MAX_PERCENTILE,
    RESCALE_MIN_PERCENTILE,
)
from tomwer.core.process.reconstruction.output import NabuOutputFileFormat
from tomwer.gui.qlefilesystem import QLFileSystem
from tomwer.gui.reconstruction.nabu.nabuconfig.output import QNabuFileFormatComboBox
from nxtomomill.models.utils import convert_str_to_tuple

_logger = logging.getLogger(__name__)


class CastVolumeWidget(qt.QWidget):
    sigConfigChanged = qt.Signal()
    """Signal emit when the configuration changed"""

    DEFAULT_OUTPUT_DATA_TYPE = "uint16"

    AVAILABLE_OUTPUT_DATA_TYPE = ("uint8", "uint16", "float32", "float64")

    assert DEFAULT_OUTPUT_DATA_TYPE in AVAILABLE_OUTPUT_DATA_TYPE

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        self.setLayout(qt.QGridLayout())

        # output data size
        self._castToLabel = qt.QLabel("cast to", self)
        self._castToLabel.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.layout().addWidget(self._castToLabel, 0, 0, 1, 1)
        self._outputDataTypeCB = qt.QComboBox(self)
        for data_type in self.AVAILABLE_OUTPUT_DATA_TYPE:
            self._outputDataTypeCB.addItem(data_type)
        self.layout().addWidget(self._outputDataTypeCB, 0, 1, 1, 3)
        # output file format
        self._outputFileformatLabel = qt.QLabel("output file format", self)
        self.layout().addWidget(self._outputFileformatLabel, 1, 0, 1, 1)
        # for now cast to vol is not handle to better remove it from the list
        self._outputFileformatCB = QNabuFileFormatComboBox(
            self, filter_formats=("vol",)
        )

        self.layout().addWidget(self._outputFileformatCB, 1, 1, 1, 3)

        # let the user provide min and max manually
        self._minMaxLabel = qt.QLabel("min max values")
        self.layout().addWidget(self._minMaxLabel, 2, 0, 1, 1)
        self._minMaxAuto = qt.QCheckBox("auto with rescale from percentiles")
        self._minMaxAuto.setChecked(True)
        self._minMaxAuto.setToolTip(
            "If set to auto will try to get min/max pixel values from nabu histogram else will compute it. Otherwise will values provided by the user"
        )
        self.layout().addWidget(self._minMaxAuto, 2, 1, 1, 1)

        self._minPixValue = qt.QLineEdit("0.0", self)
        self._minPixValue.setPlaceholderText("min")
        self._maxPixValue = qt.QLineEdit("0.0", self)
        self._maxPixValue.setPlaceholderText("max")
        validator = qt.QDoubleValidator(self)
        validator.setNotation(qt.QDoubleValidator.ScientificNotation)
        self._minPixValue.setValidator(validator)
        self._maxPixValue.setValidator(validator)
        self.layout().addWidget(self._minPixValue, 4, 2, 1, 1)
        self.layout().addWidget(self._maxPixValue, 4, 3, 1, 1)
        self._minPixValue.setVisible(False)
        self._maxPixValue.setVisible(False)
        # or from percentiles
        self._percentilesLabel = qt.QLabel("rescale percentiles")
        self.layout().addWidget(self._percentilesLabel, 3, 1, 1, 1)
        self._lowPercentileQSB = qt.QSpinBox(self)
        self._lowPercentileQSB.setRange(0, 100)
        self._lowPercentileQSB.setPrefix("min:")
        self._lowPercentileQSB.setSuffix("%")
        self._lowPercentileQSB.setValue(RESCALE_MIN_PERCENTILE)
        self.layout().addWidget(self._lowPercentileQSB, 3, 2, 1, 1)
        self._highPercentileQSB = qt.QSpinBox(self)
        self._highPercentileQSB.setRange(0, 100)
        self._highPercentileQSB.setPrefix("max:")
        self._highPercentileQSB.setSuffix("%")
        self._highPercentileQSB.setValue(RESCALE_MAX_PERCENTILE)
        self.layout().addWidget(self._highPercentileQSB, 3, 3, 1, 1)
        # compression ratios for JP2K
        self._cRatiosLabel = qt.QLabel("compression ratios", self)
        self.layout().addWidget(self._cRatiosLabel, 5, 0, 1, 1)
        self._cRatiosQLE = qt.QLineEdit(self)
        fpm = "\\d*\\.?\\d+"  # float or int matching
        qRegExp = qt.QRegularExpression(
            "(" + fpm + "[;]?[,]?[ ]?){1,}" + "|" + ":".join((fpm, fpm, fpm))
        )
        self._cRatiosQLE.setValidator(qt.QRegularExpressionValidator(qRegExp))
        self._cRatiosQLE.setPlaceholderText(
            "l1 compression rate, l2 compression rate..."
        )
        self._cRatiosQLE.setToolTip(
            "Optional list of int values defining the quality of the different layer. For example '20, 10, 1' will create 3 layers. The first one with a compression factor of 20, the second of 10 and the last will be lossless"
        )
        self.layout().addWidget(self._cRatiosQLE, 5, 1, 1, 3)
        # save dir
        self._saveDirLabel = qt.QLabel("output directory", self)
        self.layout().addWidget(self._saveDirLabel, 15, 0, 1, 1)
        self._useDefaultSaveDirQCB = qt.QCheckBox("default", self)
        self._useDefaultSaveDirQCB.setToolTip(
            f"Default directory is: {DEFAULT_OUTPUT_DIR}"
        )
        self._useDefaultSaveDirQCB.setSizePolicy(
            qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum
        )
        self._useDefaultSaveDirQCB.setChecked(True)
        self.layout().addWidget(self._useDefaultSaveDirQCB, 15, 1, 1, 1)
        self._saveDirQLE = QLFileSystem(text=DEFAULT_OUTPUT_DIR, parent=self)
        # force text because this is not a valid path
        self._saveDirQLE.setText(DEFAULT_OUTPUT_DIR)
        self._saveDirQLE.setToolTip(
            """
            can contains pattern / keywords. Those should be provided as '{keyword}'. Here are pattern currently handled:
            \n - 'volume_data_parent_folder': returns basename of the directory containing the volume (this will be the parent folder for edf, jp2k...)"
            """
        )
        self._saveDirQLE.setVisible(False)
        self.layout().addWidget(self._saveDirQLE, 15, 2, 1, 2)
        # overwrite
        self._overwriteCB = qt.QCheckBox("overwrite", self)
        self._overwriteCB.setChecked(True)
        self.layout().addWidget(self._overwriteCB, 16, 0, 1, 2)
        # remove input volume
        self._removeInputvolumeCB = qt.QCheckBox("remove input volume", self)
        self._removeInputvolumeCB.setChecked(False)
        self.layout().addWidget(self._removeInputvolumeCB, 17, 0, 1, 2)
        # spacer
        self._spacer = qt.QWidget(self)
        self._spacer.setSizePolicy(
            qt.QSizePolicy.MinimumExpanding, qt.QSizePolicy.Expanding
        )
        self.layout().addWidget(self._spacer, 99, 0, 1, 3)

        # set up
        self._outputDataTypeCB.setCurrentText(self.DEFAULT_OUTPUT_DATA_TYPE)
        self._updateCRatiosVis()

        # connect signal / slot
        self._outputFileformatCB.currentIndexChanged.connect(self._configChanged)
        self._outputFileformatCB.currentIndexChanged.connect(self._updateCRatiosVis)
        self._outputDataTypeCB.currentIndexChanged.connect(self._configChanged)
        self._saveDirQLE.editingFinished.connect(self._configChanged)
        self._useDefaultSaveDirQCB.toggled.connect(self._configChanged)
        self._overwriteCB.toggled.connect(self._configChanged)
        self._useDefaultSaveDirQCB.toggled.connect(self._updateOutputDirVis)
        self._minMaxAuto.toggled.connect(self._configChanged)
        self._minMaxAuto.toggled.connect(self._updatePixMinMaxVis)
        self._minPixValue.textChanged.connect(self._configChanged)
        self._maxPixValue.textChanged.connect(self._configChanged)
        self._lowPercentileQSB.valueChanged.connect(self._configChanged)
        self._highPercentileQSB.valueChanged.connect(self._configChanged)
        self._removeInputvolumeCB.toggled.connect(self._configChanged)

    def _updateCRatiosVis(self, *args, **kwargs):
        self._cRatiosLabel.setVisible(
            self.getOutputFileFormat() == NabuOutputFileFormat.JP2K
        )
        self._cRatiosQLE.setVisible(
            self.getOutputFileFormat() == NabuOutputFileFormat.JP2K
        )

    def getOutputDataType(self) -> str:
        return self._outputDataTypeCB.currentText()

    def setOutputDataType(self, data_type) -> None:
        if hasattr(data_type, "value"):
            data_type = data_type.value
        idx = self._outputDataTypeCB.findText(data_type)
        if idx >= 0:
            self._outputDataTypeCB.setCurrentIndex(idx)

    def getOutputDir(self) -> str:
        if self._useDefaultSaveDirQCB.isChecked():
            return DEFAULT_OUTPUT_DIR
        else:
            return self._saveDirQLE.text()

    def setOutputDir(self, output_dir: str) -> None:
        self._useDefaultSaveDirQCB.setChecked(output_dir == DEFAULT_OUTPUT_DIR)
        self._saveDirQLE.setText(output_dir)

    def getOutputFileFormat(self) -> NabuOutputFileFormat:
        return NabuOutputFileFormat.from_value(self._outputFileformatCB.currentText())

    def setOutputFileformat(self, file_format: str) -> None:
        file_format = NabuOutputFileFormat.from_value(file_format)
        idx = self._outputFileformatCB.findText(file_format.value)
        if idx >= 0:
            self._outputFileformatCB.setCurrentIndex(idx)

    def getOverwrite(self) -> bool:
        return self._overwriteCB.isChecked()

    def setOverwrite(self, remove) -> None:
        self._overwriteCB.setChecked(remove)

    def isRemoveInputVolume(self) -> bool:
        return self._removeInputvolumeCB.isChecked()

    def setRemoveInputVolume(self, remove: bool) -> None:
        self._removeInputvolumeCB.setChecked(remove)

    def getDataMin(self) -> float | None:
        if (
            self._minMaxAuto.isChecked()
            or self._minPixValue.text().replace(" ", "") == ""
        ):
            return None
        else:
            return float(self._minPixValue.text())

    def setDataMin(self, value: float | None) -> None:
        with blockSignals(self._minMaxAuto):
            self._minMaxAuto.setChecked(value is None)
        if value is not None:
            with blockSignals(self._minPixValue):
                self._minPixValue.setText(str(value))
        self._updatePixMinMaxVis()

    def getDataMax(self) -> float | None:
        if (
            self._minMaxAuto.isChecked()
            or self._maxPixValue.text().replace(" ", "") == ""
        ):
            return None
        else:
            return float(self._maxPixValue.text())

    def setDataMax(self, value: float | None) -> None:
        with blockSignals(self._minMaxAuto):
            self._minMaxAuto.setChecked(value is None)
        if value is not None:
            with blockSignals(self._maxPixValue):
                self._maxPixValue.setText(str(value))
        self._updatePixMinMaxVis()

    def setCompressionRatios(self, c_ratios: list | None):
        if c_ratios in (None, tuple(), list()):
            c_ratios = ""
        self._cRatiosQLE.setText(str(c_ratios))

    def getCompressionRatios(self) -> tuple:
        if self.getOutputFileFormat() is NabuOutputFileFormat.JP2K:
            # for now the compression ratios are only handled for JP2K
            return tuple(
                [int(value) for value in convert_str_to_tuple(self._cRatiosQLE.text())]
            )
        else:
            return None

    def getRescalePercentiles(self) -> tuple[int | None, int | None]:
        if self._minMaxAuto.isChecked():
            return self._lowPercentileQSB.value(), self._highPercentileQSB.value()
        else:
            return None, None

    def setRescalePercentiles(self, low: int | None, high: int | None) -> tuple:
        if low is not None:
            with blockSignals(self._minMaxAuto):
                self._minMaxAuto.setChecked(True)
                self._lowPercentileQSB.setValue(low)
        if high is not None:
            with blockSignals(self._minMaxAuto):
                self._minMaxAuto.setChecked(True)
                self._highPercentileQSB.setValue(high)
        self._updatePixMinMaxVis()

    def getConfiguration(self) -> dict:
        rescale_min_percentile, rescale_max_percentile = self.getRescalePercentiles()
        if (rescale_min_percentile, rescale_max_percentile) == (None, None):
            data_min, data_max = self.getDataMin(), self.getDataMax()
        else:
            data_min, data_max = None, None
        return {
            "output_data_type": self.getOutputDataType(),
            "output_file_format": self.getOutputFileFormat().value,
            "output_dir": self.getOutputDir(),
            "overwrite": self.getOverwrite(),
            "rescale_min_percentile": rescale_min_percentile,
            "rescale_max_percentile": rescale_max_percentile,
            "data_min": data_min,
            "data_max": data_max,
            "compression_ratios": self.getCompressionRatios(),
            "remove_input_volume": self.isRemoveInputVolume(),
        }

    def setConfiguration(self, config: dict) -> None:
        output_data_type = config.get("output_data_type", None)
        if output_data_type is not None:
            self.setOutputDataType(output_data_type)
        output_file_format = config.get("output_file_format", None)
        if output_file_format is not None:
            self.setOutputFileformat(output_file_format)
        output_dir = config.get("output_dir", None)
        if output_dir is not None:
            self.setOutputDir(output_dir)
        overwrite = config.get("overwrite", None)
        if overwrite is not None:
            self.setOverwrite(overwrite)
        rescale_min_percentile = config.get("rescale_min_percentile", None)
        rescale_max_percentile = config.get("rescale_max_percentile", None)

        self.setRescalePercentiles(rescale_min_percentile, rescale_max_percentile)
        if "data_min" in config:
            self.setDataMin(config["data_min"])
        if "data_max" in config:
            self.setDataMax(config["data_max"])
        if "compression_ratios" in config:
            self.setCompressionRatios(config["compression_ratios"])
        remove_input_volume = config.get("remove_input_volume", None)
        if remove_input_volume is not None:
            self.setRemoveInputVolume(remove=remove_input_volume)

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def _updateOutputDirVis(self, *args, **kwargs):
        self._saveDirQLE.setVisible(not self._useDefaultSaveDirQCB.isChecked())

    def _updatePixMinMaxVis(self, *args, **kwargs):
        self._minPixValue.setVisible(not self._minMaxAuto.isChecked())
        self._maxPixValue.setVisible(not self._minMaxAuto.isChecked())
        self._percentilesLabel.setVisible(self._minMaxAuto.isChecked())
        self._lowPercentileQSB.setVisible(self._minMaxAuto.isChecked())
        self._highPercentileQSB.setVisible(self._minMaxAuto.isChecked())
