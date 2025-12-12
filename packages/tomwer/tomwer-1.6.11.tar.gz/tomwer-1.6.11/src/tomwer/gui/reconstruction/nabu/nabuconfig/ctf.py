from __future__ import annotations

from silx.gui import qt
from silx.gui.utils import blockSignals
from enum import Enum as _Enum

from tomwer.core.process.reconstruction.nabu.utils import _NabuStages
from tomwer.gui.reconstruction.nabu.nabuconfig import base
from tomwer.gui.utils.illustrations import _IllustrationWidget
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel


def nabu_param_ligne_to_dict(str_ligne: str) -> dict:
    ddict = {}
    if "=" in str_ligne:
        for elmt in str_ligne.split(";"):
            kwv = elmt.lstrip(" ").rstrip(" ")
            key, value = kwv.split("=")
            ddict[key] = value
    return ddict


class _DoubleScientific(qt.QLineEdit):
    """
    A simple QLineEdit with a Doublevalidator with Scientific Notation
    """

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        validator = qt.QDoubleValidator(parent=self)
        validator.setNotation(qt.QDoubleValidator.ScientificNotation)
        self.setValidator(validator)

    def value(self) -> float:
        if self.text() == "":
            return 0.0
        else:
            return float(self.text())

    def setValue(self, value):
        self.setText(str(value))


class OptionalDouble(qt.QWidget):
    """
    A spin box with a Check box to handle 'None' case of the nabu CTF options
    """

    sigChanged = qt.Signal()
    """emit when the combobox of the double spin box value changed"""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())
        self._cb = qt.QCheckBox("", self)
        self.layout().addWidget(self._cb)
        self._dsb = _DoubleScientific(self)
        self.layout().addWidget(self._dsb)

        # connect signal ? slot
        self._cb.toggled.connect(self._updateVisibility)
        self._cb.toggled.connect(self._changed)
        self._dsb.textChanged.connect(self._changed)

        # set up
        self._updateVisibility()

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def value(self) -> float | None:
        if self._cb.isChecked():
            return self._dsb.value()
        else:
            return None

    def setValue(self, value: float | None):
        if value in (None, "None"):
            self._cb.setChecked(False)
        else:
            self._cb.setChecked(True)
            self._dsb.setValue(float(value))

    def setText(self, text: str):
        self._cb.setText(text)

    def _updateVisibility(self, *args, **kwargs):
        self._dsb.setVisible(self._cb.isChecked())


class _BeamShape(_Enum):
    PARALLEL = "parallel"
    CONE = "cone"


class ConeBeamOpts(qt.QGroupBox):
    """Specific settings for cone beam geometry"""

    sigConfChanged = qt.Signal()
    """emit when ctf parameters changed"""

    def __init__(self, parent=None, title="cone settings"):
        super().__init__(parent, title=title)
        self.setLayout(qt.QGridLayout())
        # z1_v
        self._z1_v = _DoubleScientific(self)
        self._z1_v.setPlaceholderText("z1_v in meter")
        self.layout().addWidget(qt.QLabel("z1_v", self), 0, 0, 1, 1)
        self.layout().addWidget(self._z1_v, 0, 1, 1, 1)
        # z1_h
        self._z1_h = _DoubleScientific(self)
        self._z1_h.setPlaceholderText("z1_h in meter")
        self.layout().addWidget(qt.QLabel("z1_h", self), 1, 0, 1, 1)
        self.layout().addWidget(self._z1_h, 1, 1, 1, 1)

        # illustration to define z1, z2
        self._ctfIllustration = _IllustrationWidget(parent=self, img="ctf_z1")
        self._ctfIllustration.setMinimumSize(qt.QSize(200, 90))
        self._ctfIllustration.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding
        )

        self._ctfIllustration.setContentsMargins(0, 0, 0, 0)
        self._ctfIllustration.layout().setSpacing(0)
        self.layout().addWidget(self._ctfIllustration, 0, 2, 2, 2)

        # connect signal / slot
        self._z1_v.textChanged.connect(self._confChanged)
        self._z1_h.textChanged.connect(self._confChanged)

    def _confChanged(self, *args, **kwargs):
        self.sigConfChanged.emit()

    def getGeometry(self) -> dict:
        return {
            "z1_v": self._z1_v.value(),
            "z1_h": self._z1_h.value(),
        }

    def setGeometry(self, config: dict) -> None:
        with blockSignals(self):
            if "z1_v" in config:
                self._z1_v.setValue(float(config["z1_v"]))
            if "z1_h" in config:
                self._z1_h.setValue(float(config["z1_h"]))


class CTFGeometry(qt.QGroupBox):
    """
    widget for the ctf_geometry parameter of nabu
    """

    sigConfChanged = qt.Signal()
    """emit when ctf parameters changed"""

    def __init__(self, parent=None, title="ctf-geometry") -> None:
        super().__init__(parent, title=title)
        self.setLayout(qt.QFormLayout())
        self._beamShapeCB = QComboBoxIgnoreWheel(self)
        for shape in _BeamShape:
            self._beamShapeCB.addItem(shape.value)
        self.layout().addRow("shape", self._beamShapeCB)

        # cone beam settings
        self._coneBeamSettings = ConeBeamOpts(self)
        self.layout().addRow(self._coneBeamSettings)

        # detector pixel size
        self._detectorPixelSize = OptionalDouble(self)
        self._detectorPixelSize.setText("overwrite")
        self._detectorPixelSize._dsb.setPlaceholderText("pixel size in meter")
        self.layout().addRow("detector pixel size", self._detectorPixelSize)
        # magnification
        self._magnification = qt.QCheckBox("magnification", self)
        self.layout().addRow(self._magnification)

        # set up
        self._magnification.setChecked(True)
        self._updateView()

        # connect signal / slot
        self._coneBeamSettings.sigConfChanged.connect(self._confChanged)
        self._detectorPixelSize.sigChanged.connect(self._confChanged)
        self._magnification.toggled.connect(self._confChanged)
        self._beamShapeCB.currentIndexChanged.connect(self._updateView)
        self._beamShapeCB.currentIndexChanged.connect(self._confChanged)

    def getBeamShape(self):
        return _BeamShape(self._beamShapeCB.currentText())

    def setBeamShape(self, shape: str | _BeamShape):
        shape = _BeamShape(shape)
        self._beamShapeCB.setCurrentText(shape.value)

    def _updateView(self, *args, **kwargs):
        self._coneBeamSettings.setVisible(self.getBeamShape() == _BeamShape.CONE)

    def _confChanged(self, *args, **kwargs):
        self.sigConfChanged.emit()

    def getConfiguration(self) -> dict:
        magnification = "True" if self._magnification.isChecked() else "False"
        beam_shape = self.getBeamShape()
        if beam_shape is _BeamShape.PARALLEL:
            z1_v = None
            z1_h = None
        elif beam_shape is _BeamShape.CONE:
            cone_params = self._coneBeamSettings.getGeometry()
            z1_v = cone_params["z1_v"]
            z1_h = cone_params["z1_h"]
        else:
            raise NotImplementedError(f"Geometry {beam_shape.value} is not handled")

        geometry = f" z1_v={z1_v}; z1_h={z1_h}; detec_pixel_size={self._detectorPixelSize.value()}; magnification={magnification}"

        return {"ctf_geometry": geometry, "beam_shape": beam_shape.value}

    def setConfiguration(self, ddict: dict) -> None:
        params = nabu_param_ligne_to_dict(ddict.get("ctf_geometry", ""))
        with blockSignals(self):
            for key, value in params.items():
                if key == "detec_pixel_size":
                    self._detectorPixelSize.setValue(value)
                elif key == "magnification":
                    self._magnification.setChecked(value.lower() == "true")

            beam_shape = ddict.get("beam_shape", None)
            if beam_shape is not None:
                if _BeamShape(beam_shape) is _BeamShape.CONE:
                    self._coneBeamSettings.setGeometry(params)
                self.setBeamShape(beam_shape)


class CTFAdvancedParams(qt.QGroupBox):
    """
    widget for the ctf_advanced_params parameter of nabu
    """

    sigConfChanged = qt.Signal()
    """emit when ctf parameters changed"""

    def __init__(self, parent=None, title="ctf-advanced-params") -> None:
        super().__init__(parent, title=title)
        self.setLayout(qt.QFormLayout())
        # length_scale
        self._length_scale = _DoubleScientific(self)
        self.layout().addRow("length_scale", self._length_scale)
        # lim1
        self._lim1 = _DoubleScientific(self)
        self._lim1Label = qt.QLabel("lim1")
        self.layout().addRow(self._lim1Label, self._lim1)
        # lim2
        self._lim2 = _DoubleScientific(self)
        self._lim2Label = qt.QLabel("lim2")
        self.layout().addRow(self._lim2Label, self._lim2)
        for w in (self._lim1, self._lim1Label, self._lim2, self._lim2Label):
            w.setToolTip(
                "parameter of the low-pass filter. Used in equation: 'lim = lim1 * r + lim2 * (1 - r)' where r is some low-pass filter (image dimensionality)"
            )

        # normalize_by_mean
        self._normalize_by_mean = qt.QCheckBox("normalize by mean", self)
        self.layout().addRow(self._normalize_by_mean)

        # set up
        self._length_scale.setText("1e-5")
        self._lim1.setText("1e-5")
        self._lim2.setText("0.2")
        self._normalize_by_mean.setChecked(True)

        # connect sginal / slot
        self._length_scale.textChanged.connect(self._confChanged)
        self._lim1.textChanged.connect(self._confChanged)
        self._lim2.textChanged.connect(self._confChanged)
        self._normalize_by_mean.toggled.connect(self._confChanged)

    def getLengthScale(self) -> str:
        if self._length_scale.text() == "":
            return "0.0"
        else:
            return self._length_scale.text()

    def _confChanged(self, *args, **kwargs):
        self.sigConfChanged.emit()

    def getConfiguration(self) -> dict:
        normalize_by_mean = "True" if self._normalize_by_mean.isChecked() else "False"
        ctf_advanced_params = f" length_scale={self._length_scale.value()}; lim1={self._lim1.value()}; lim2={self._lim2.value()}; normalize_by_mean={normalize_by_mean}"
        return {
            "ctf_advanced_params": ctf_advanced_params,
        }

    def setConfiguration(self, ddict: dict) -> None:
        params = nabu_param_ligne_to_dict(ddict.get("ctf_advanced_params", {}))
        with blockSignals(self):
            for key, value in params.items():
                if key == "length_scale":
                    self._length_scale.setText(value)
                elif key == "lim1":
                    self._lim1.setText(value)
                elif key == "lim2":
                    self._lim2.setText(value)
                elif key == "normalize_by_mean":
                    self._normalize_by_mean.setChecked(value.lower() == "true")


class CTFConfig(qt.QGroupBox, base._NabuStageConfigBase):
    """
    Widget dedicated for the CTF parameters
    """

    sigConfChanged = qt.Signal(str)
    """emit when ctf parameters changed"""

    def __init__(self, parent=None, title="ctf parameters"):
        qt.QGroupBox.__init__(self, parent, title=title, stage=_NabuStages.PHASE)
        base._NabuStageConfigBase.__init__(self, stage=_NabuStages.PHASE)

        self.setLayout(qt.QFormLayout())

        # geometry
        self._geometryWidget = CTFGeometry(parent=self, title="geometry")
        self.layout().addRow(self._geometryWidget)
        self.registerWidget(self._geometryWidget, "optional")
        # advanced parameters
        self._advancedParamsWidget = CTFAdvancedParams(
            parent=self, title="advanced parameters"
        )
        self.layout().addRow(self._advancedParamsWidget)
        self.registerWidget(self._advancedParamsWidget, "advanced")

        # connect signal / slot
        self._geometryWidget.sigConfChanged.connect(self._confChanged)
        self._advancedParamsWidget.sigConfChanged.connect(self._confChanged)

    def _confChanged(self, *args, **kwargs):
        self.sigConfChanged.emit("phase")

    def getConfiguration(self) -> dict:
        ddict = self._geometryWidget.getConfiguration()
        ddict.update(self._advancedParamsWidget.getConfiguration())
        return ddict

    def setConfiguration(self, ddict):
        self._geometryWidget.setConfiguration(ddict=ddict)
        self._advancedParamsWidget.setConfiguration(ddict=ddict)
