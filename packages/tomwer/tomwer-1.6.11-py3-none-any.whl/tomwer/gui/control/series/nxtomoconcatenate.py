from silx.gui import qt


class NXtomoConcatenateWidget(qt.QWidget):
    """
    Widget to define setting of a concatenation of NXtomo.
    User need to provide entry name (data_path), output file path (a default option is possible) and if they want to overwrite any existing file / entry if necessary
    """

    sigConfigChanged = qt.Signal()
    """Emitted on configuration modifications"""

    class OutputWidget(qt.QWidget):
        def __init__(self, parent=None, *args, **kwargs) -> None:
            super().__init__(parent, *args, **kwargs)
            self.setLayout(qt.QFormLayout())
            self.layout().setContentsMargins(0, 0, 0, 0)
            self._outputFilePathQLE = qt.QLineEdit("{common_path}/concatenate.nx", self)
            self._outputFilePathQLE.setToolTip(
                """location of the concatenation. Possible keywords are: \n
                - 'common_path': common path of all the scans to concatenate
                """
            )
            self.layout().addRow("output file path", self._outputFilePathQLE)
            self._outputDataPathQLE = qt.QLineEdit("entry0000", self)
            self.layout().addRow("output entry", self._outputDataPathQLE)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setLayout(qt.QVBoxLayout())
        # output widget
        self._outputWidget = self.OutputWidget(parent=self)
        self.layout().addWidget(self._outputWidget)
        # overwrite option
        self._overwriteCB = qt.QCheckBox("overwrite", parent)
        self.layout().addWidget(self._overwriteCB)
        # spacer
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        # conenct signal / slot
        self._outputWidget._outputFilePathQLE.textEdited.connect(self._changed)
        self._outputWidget._outputDataPathQLE.textEdited.connect(self._changed)
        self._overwriteCB.toggled.connect(self._changed)

    def _changed(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getConfiguration(self) -> dict:
        return {
            "overwrite": self._overwriteCB.isChecked(),
            "output_file": self.getOutputFilePath(),
            "output_entry": self.getOutputEntry(),
        }

    def setConfiguration(self, config: dict) -> None:
        overwrite = config.get("overwrite", None)
        if overwrite is not None:
            self._overwriteCB.setChecked(overwrite in (True, "True", "1", "true"))

        output_file = config.get("output_file", None)
        if output_file is not None:
            self._outputWidget._outputFilePathQLE.setText(output_file)

        output_entry = config.get("output_entry", None)
        if output_entry is not None:
            self._outputWidget._outputDataPathQLE.setText(output_entry)

    # expose API
    def getOutputFilePath(self) -> str:
        return self._outputWidget._outputFilePathQLE.text()

    def getOutputEntry(self) -> str:
        return self._outputWidget._outputDataPathQLE.text()
