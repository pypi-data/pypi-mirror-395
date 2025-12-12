from silx.gui import qt
from tomwer.gui.qlefilesystem import QLFileSystem


class HelicalPrepareWeightsDouble(qt.QWidget):
    sigConfigChanged = qt.Signal()
    """emit when the configuration has changed"""

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.setLayout(qt.QGridLayout())
        # TODO: optional outptu file path. Default or set by the user
        self._outputFilePathLabel = qt.QLabel("output file", self)
        self.layout().addWidget(self._outputFilePathLabel, 0, 0, 1, 1)
        self._outputFilePathQLE = QLFileSystem(
            text="{scan_parent_dir_basename}/{scan_dir_name}/map_and_doubleff.hdf5",
            parent=self,
        )
        self._outputFilePathQLE.setToolTip(
            "location of the output file. Which will contain the weight map."
        )
        self.layout().addWidget(self._outputFilePathQLE, 0, 2, 1, 1)

        # transition_width_vertical
        self._verticalTransitionWidthQDSP = qt.QLabel("transition width", self)
        self.layout().addWidget(self._verticalTransitionWidthQDSP, 1, 0, 1, 1)
        self._verticalTransitionWidthQDSP = qt.QDoubleSpinBox(self)
        self._verticalTransitionWidthQDSP.setRange(0.0, 99999999)
        self._verticalTransitionWidthQDSP.setValue(50.0)
        self._verticalTransitionWidthQDSP.setToolTip(
            "the transition width is used to determine how the weights are apodised near the upper and lower border"
        )
        # TODO: improve tooltip of this
        self.layout().addWidget(self._verticalTransitionWidthQDSP, 1, 1, 1, 2)

        # transition_width_vertical
        self._horizontalTransitionWidthQDSP = qt.QLabel("transition width", self)
        self.layout().addWidget(self._horizontalTransitionWidthQDSP, 1, 0, 1, 1)
        self._horizontalTransitionWidthQDSP = qt.QDoubleSpinBox(self)
        self._horizontalTransitionWidthQDSP.setRange(0.0, 99999999)
        self._horizontalTransitionWidthQDSP.setValue(50.0)
        self._horizontalTransitionWidthQDSP.setToolTip(
            "the transition width is used to determine how the weights are apodised near the upper and lower border"
        )
        self.layout().addWidget(self._horizontalTransitionWidthQDSP, 1, 1, 1, 2)

        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 100, 0, 1, 3)

        # connect signal / slot
        self._outputFilePathQLE.editingFinished.connect(self._changed)
        self._verticalTransitionWidthQDSP.valueChanged.connect(self._changed)
        self._horizontalTransitionWidthQDSP.valueChanged.connect(self._changed)

    def _changed(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getConfiguration(self) -> dict:
        return {
            "processes_file": self._outputFilePathQLE.text(),
            "transition_width_vertical": self._verticalTransitionWidthQDSP.value(),
            "transition_width_horizontal": self._horizontalTransitionWidthQDSP.value(),
        }

    def setConfiguration(self, config: dict):
        processes_file = config.get("processes_file", None)
        if processes_file is not None:
            self._outputFilePathQLE.setText(processes_file)

        transition_width = config.get("transition_width_vertical", None)
        if transition_width is not None:
            self._verticalTransitionWidthQDSP.setValue(float(transition_width))

        transition_width = config.get("transition_width_horizontal", None)
        if transition_width is not None:
            self._horizontalTransitionWidthQDSP.setValue(float(transition_width))
