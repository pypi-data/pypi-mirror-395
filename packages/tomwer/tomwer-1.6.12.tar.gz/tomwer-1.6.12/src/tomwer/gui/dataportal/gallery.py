from __future__ import annotations

from silx.gui import qt
from tomwer.core.process.drac.output import OutputFormat
from tomwer.gui import icons

from tomwer.core.process.drac.binning import Binning


class GalleryOptionsAction(qt.QAction):
    def __init__(self, parent):
        icon = icons.getQIcon("icat_gallery_opts")
        qt.QAction.__init__(self, icon, "Icat gallery options", parent)


class GalleryWidget(qt.QWidget):
    """Widget to let the user define the output location of the screenshots"""

    sigConfigChanged = qt.Signal()
    """emit when the configuration has changed"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(qt.QFormLayout())

        # screenshot precision
        self._precisionQCB = qt.QComboBox(self)
        self._precisionQCB.addItem("uint8")
        self.layout().addRow("precision", self._precisionQCB)
        # binning
        self._binningQCB = qt.QComboBox(self)
        self._binningQCB.addItems([item.value for item in Binning])
        self.layout().addRow("binning", self._binningQCB)
        self._binningQCB.setCurrentText(Binning.SIXTEEN_BY_SIXTEEN.value)
        self._binningQCB.setToolTip(
            "To speed up display of the gallery at the data portal side it is highly recommended to bin screenshots"
        )  # recommended size: 5ko for the entire gallery
        # output format
        self._outputFormat = qt.QComboBox(self)
        self._outputFormat.addItems([item.value for item in OutputFormat])
        self.layout().addRow("output format", self._outputFormat)
        # overwrite
        self._overwriteCB = qt.QCheckBox("overwrite", self)
        self._overwriteCB.setChecked(True)
        self.layout().addRow(self._overwriteCB)
        # connect signal / slot
        self._outputFormat.currentIndexChanged.connect(self._configChanged)
        self._overwriteCB.toggled.connect(self._configChanged)
        self._binningQCB.currentIndexChanged.connect(self._configChanged)

    def getOutputFormat(self) -> OutputFormat:
        return OutputFormat(self._outputFormat.currentText())

    def setOutputFormat(self, format: OutputFormat):
        format = OutputFormat(format)
        self._outputFormat.setCurrentText(format.value)

    def getBinning(self) -> Binning:
        return Binning(self._binningQCB.currentText())

    def setBinning(self, binning: Binning):
        binning = Binning(binning)
        self._binningQCB.setCurrentText(binning.value)

    def overwrite(self) -> bool:
        return self._overwriteCB.isChecked()

    def setOverwrite(self, overwrite: bool) -> None:
        return self._overwriteCB.setChecked(overwrite)

    def getConfiguration(self):
        return {
            "output_format": self.getOutputFormat().value,
            "overwrite": self.overwrite(),
            "binning": self.getBinning().value,
        }

    def setConfiguration(self, config: dict):
        if not isinstance(config, dict):
            raise TypeError(f"config is a expected to be a dict. got {type(config)}")
        output_format = config.get("output_format", None)
        if output_format is not None:
            self.setOutputFormat(output_format)

        overwrite = config.get("overwrite", None)
        if overwrite is not None:
            overwrite = overwrite in (True, "True", 1)
            self.setOverwrite(overwrite=overwrite)

        binning = config.get("binning", None)
        if binning is not None:
            self.setBinning(binning=binning)

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()


class GalleryDialog(qt.QDialog):
    def __init__(self, parent: qt.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._widget = GalleryWidget()
        self.layout().addWidget(self._widget)

        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

    # expose API
    def setConfiguration(self, gallery_options: dict) -> None:
        self._widget.setConfiguration(gallery_options)

    def getConfiguration(self) -> dict:
        return self._widget.getConfiguration()

    def getOutputFormat(self) -> OutputFormat:
        return self._widget.getOutputFormat()

    def setOutputFormat(self, format: OutputFormat):
        return self._widget.setOutputFormat(format=format)

    def getBinning(self) -> Binning:
        return self._widget.getBinning()

    def setBinning(self, binning: Binning):
        self._widget.setBinning(binning=binning)

    def overwrite(self) -> bool:
        return self._widget.overwrite

    def setOverwrite(self, overwrite: bool) -> None:
        self._widget.setOverwrite(overwrite=overwrite)
