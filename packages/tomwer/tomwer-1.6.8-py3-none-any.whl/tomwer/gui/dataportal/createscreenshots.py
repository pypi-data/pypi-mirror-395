from __future__ import annotations

from silx.gui import qt


class CreateRawDataScreenshotsWidget(qt.QWidget):
    """
    Widget to allow the user define the screenshot to make of the raw data
    """

    sigConfigChanged = qt.Signal()
    """emit when the configuration change"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(qt.QFormLayout())
        # projections
        self._projectionsCB = qt.QCheckBox("raw projections each", self)
        self._projectionsSB = qt.QSpinBox(parent)
        self._projectionsSB.setSuffix("°")
        self.layout().addRow(self._projectionsCB, self._projectionsSB)
        # flat field
        self._flatFieldCB = qt.QCheckBox("first raw flat")
        self.layout().addRow(self._flatFieldCB)
        # dark field
        self._darkFieldCB = qt.QCheckBox("first raw dark")
        self.layout().addRow(self._darkFieldCB)

        # set up
        self._projectionsCB.setChecked(True)
        self._flatFieldCB.setChecked(True)
        self._darkFieldCB.setChecked(True)

        # connect signal / slot
        self._projectionsCB.toggled.connect(self._changed)
        self._projectionsSB.valueChanged.connect(self._changed)
        self._projectionsSB.setRange(0, 360)
        self._projectionsSB.setValue(90)
        self._flatFieldCB.toggled.connect(self._changed)
        self._darkFieldCB.toggled.connect(self._changed)

    def _changed(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getConfiguration(self) -> dict:
        return {
            "raw_projections_required": self._projectionsCB.isChecked(),
            "raw_projections_each": self._projectionsSB.value(),
            "raw_darks_required": self._darkFieldCB.isChecked(),
            "raw_flats_required": self._flatFieldCB.isChecked(),
        }

    def setRawProjections(self, required: bool, each_proj: int | None):
        self._projectionsCB.setChecked(required)
        if each_proj is not None:
            self._projectionsSB.setValue(int(each_proj))

    def setFlatFieldRequired(self, required: bool):
        self._flatFieldCB.setChecked(required)

    def setDarkFieldRequired(self, required: bool):
        self._darkFieldCB.setChecked(required)

    def setConfiguration(self, configuration: dict):
        assert isinstance(configuration, dict)
        # handle raw projections
        raw_projections_required = configuration.get(
            "raw_projections_required", self._projectionsCB.isChecked()
        )
        raw_projections_each = configuration.get("raw_projections_each", None)
        self.setRawProjections(
            required=raw_projections_required, each_proj=raw_projections_each
        )
        # handle flat field
        flat_field_required = configuration.get("raw_flats_required", None)
        if flat_field_required is not None:
            self.setFlatFieldRequired(flat_field_required)
        # handle flat field
        dark_field_required = configuration.get("raw_darks_required", None)
        if dark_field_required is not None:
            self.setDarkFieldRequired(dark_field_required)
