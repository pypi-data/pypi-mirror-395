# coding: utf-8
from __future__ import annotations


import logging

from silx.gui import qt
from enum import Enum as _Enum

from tomwer.core.process.reconstruction.nabu.utils import _NabuPhaseMethod, _NabuStages
from tomwer.core.utils.char import BETA_CHAR, DELTA_CHAR
from tomwer.gui.reconstruction.nabu.nabuconfig import base
from tomwer.gui.reconstruction.nabu.nabuconfig.ctf import CTFConfig
from tomwer.gui.utils.inputwidget import SelectionLineEdit
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel as QComboBox
from tomwer.gui import icons
from tomwer.utils import docstring

_logger = logging.getLogger(__name__)


class PaddingMode(_Enum):
    ZEROS = "zeros"
    MEAN = "mean"
    EDGE = "edge"
    SYMMETRIC = "symmetric"
    REFLECT = "reflect"


class _NabuPhaseConfig(qt.QWidget, base._NabuStageConfigBase):
    """
    Widget to define the configuration of the nabu preprocessing
    """

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent, stage=_NabuStages.PHASE)
        base._NabuStageConfigBase.__init__(self, stage=_NabuStages.PHASE)
        self.setLayout(qt.QGridLayout())

        # phase method
        self._methodLabel = qt.QLabel("method", self)
        self.layout().addWidget(self._methodLabel, 1, 0, 1, 1)
        self._methodCB = QComboBox(parent=self)
        for method in _NabuPhaseMethod:
            self._methodCB.addItem(method.value)
        idx_ctf = self._methodCB.findText(_NabuPhaseMethod.CTF.value)
        self._methodCB.setItemData(
            idx_ctf, "Contrast Transfer Function", qt.Qt.ToolTipRole
        )
        self.layout().addWidget(self._methodCB, 1, 1, 1, 3)
        self.registerWidget(self._methodLabel, "required")
        self.registerWidget(self._methodCB, "required")

        # paganin & ctf options
        self._paganinOpts = NabuPaganinConfig(parent=self)
        self.layout().addWidget(self._paganinOpts, 2, 0, 3, 3)

        # unsharp options
        self._unsharpOpts = NabuUnsharpConfig(parent=self)
        self.layout().addWidget(self._unsharpOpts, 6, 0, 3, 3)

        # ctf options
        self._ctfOpts = CTFConfig(parent=self)
        self.layout().addWidget(self._ctfOpts, 9, 0, 3, 4)
        self.registerWidget(self._ctfOpts, "advanced")

        # spacer for style
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 200, 1, 1, 1)

        # set up
        item_index = self._methodCB.findText(_NabuPhaseMethod.PAGANIN.value)
        assert item_index >= 0
        self._methodCB.setCurrentIndex(item_index)

        # connect signal / slot
        self._methodCB.currentIndexChanged.connect(self._methodChanged)
        self._paganinOpts.sigConfChanged.connect(self.sigConfChanged)
        self._unsharpOpts.sigConfChanged.connect(self.sigConfChanged)
        self._ctfOpts.sigConfChanged.connect(self.sigConfChanged)

        # set up
        self._paganinOpts.setEnabled(self.getMethod() is not _NabuPhaseMethod.NONE)
        self._ctfOpts.setEnabled(self.getMethod() is _NabuPhaseMethod.CTF)

    def _methodChanged(self, *args, **kwargs):
        self._paganinOpts.setEnabled(self.getMethod() is not _NabuPhaseMethod.NONE)
        self._ctfOpts.setEnabled(self.getMethod() is _NabuPhaseMethod.CTF)
        self._unsharpOpts.setDiscourageUnsharpMask(
            self.getMethod() is _NabuPhaseMethod.NONE
        )
        self._unsharpOpts._updateUnsharpMaskWarning()
        self.sigConfChanged.emit("method")

    def _signalConfChanged(self, param):
        self.sigConfChanged.emit(param)

    def getMethod(self) -> _NabuPhaseMethod:
        return _NabuPhaseMethod(self._methodCB.currentText())

    @docstring(base._NabuStageConfigBase)
    def setConfiguration(self, config) -> None:
        if "method" in config:
            method = config.get("method", _NabuPhaseMethod.NONE)
            if method == "none":
                method = _NabuPhaseMethod.NONE
            self._paganinOpts.setConfiguration(config)
            method = _NabuPhaseMethod(method)
            index_method = self._methodCB.findText(method.value)
            if index_method >= 0:
                self._methodCB.setCurrentIndex(index_method)
            else:
                _logger.warning("unable to find method {method}")
        self._unsharpOpts.setConfiguration(config)
        self._ctfOpts.setConfiguration(config)

    @docstring(base._NabuStageConfigBase)
    def getConfiguration(self) -> dict:
        configuration = {"method": self.getMethod().value}
        if self.getMethod() in (_NabuPhaseMethod.PAGANIN, _NabuPhaseMethod.CTF):
            configuration.update(self._paganinOpts.getConfiguration())
        configuration.update(self._unsharpOpts.getConfiguration())
        configuration.update(self._ctfOpts.getConfiguration())
        return configuration

    def setConfigurationLevel(self, level):
        base._NabuStageConfigBase.setConfigurationLevel(self, level)
        self._unsharpOpts.setConfigurationLevel(level=level)
        self._paganinOpts.setConfigurationLevel(level=level)

    def setDeltaBetaValue(self, value):
        self._paganinOpts.setDeltaBetaValue(value)

    def getUnsharpCoeff(self) -> float:
        return self._unsharpOpts.getUnsharpCoeff()

    def setUnsharpCoeff(self, coeff: float):
        self._unsharpOpts.setUnsharpCoeff(coeff)

    def getUnsharpSigma(self) -> float:
        return self._unsharpOpts.getUnsharpSigma()

    def setUnsharpSigma(self, sigma: float):
        self._unsharpOpts.setUnsharpSigma(sigma)

    def getPaddingType(self):
        return self._paganinOpts.getPaddingType()

    def setPaddingType(self, padding_type):
        return self._paganinOpts.setPaddingType(padding_type)


class NabuPaganinConfig(qt.QWidget, base._NabuStageConfigBase):
    """Configuration widget dedicated to the paganin options for nabu"""

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent=parent, stage=_NabuStages.PHASE)
        base._NabuStageConfigBase.__init__(self, stage=_NabuStages.PHASE)
        self.setLayout(qt.QGridLayout())

        # paganin delta / beta
        label = DELTA_CHAR + " / " + BETA_CHAR
        self._db_label = qt.QLabel(label, self)
        self.layout().addWidget(self._db_label, 0, 0, 1, 1)
        self._deltaBetaQLE = SelectionLineEdit(
            "100.0", self, allow_negative_indices=False
        )
        self.layout().addWidget(self._deltaBetaQLE, 0, 1, 1, 3)
        self.registerWidget(self._db_label, "required")
        self.registerWidget(self._deltaBetaQLE, "required")

        # paganin padding_type
        self._paddingLabel = qt.QLabel("padding", self)
        self.layout().addWidget(self._paddingLabel, 2, 0, 1, 1)
        self._paddingTypeCB = QComboBox(self)
        self._paddingTypeCB.setToolTip(
            "Padding type for the filtering step " "in Paganin/CTR."
        )
        for padding_type in (PaddingMode.ZEROS, PaddingMode.EDGE):
            self._paddingTypeCB.addItem(padding_type.value)
        self.layout().addWidget(self._paddingTypeCB, 2, 1, 1, 3)
        self.registerWidget(self._paddingLabel, "advanced")
        self.registerWidget(self._paddingTypeCB, "advanced")

        # set up
        item_index = self._paddingTypeCB.findText(PaddingMode.EDGE.value)
        self._paddingTypeCB.setCurrentIndex(item_index)

        # connect signal - slot
        self._deltaBetaQLE.editingFinished.connect(self._paganinDBChanged)
        self._paddingTypeCB.currentIndexChanged.connect(self._paganinPaddingTypeChanged)

    def _paganinDBChanged(self, *args, **kwargs):
        self.sigConfChanged.emit("delta_beta")

    def _paganinMargeChanged(self, *args, **kwargs):
        self.sigConfChanged.emit("marge")

    def _paganinPaddingTypeChanged(self, *args, **kwargs):
        self.sigConfChanged.emit("padding_type")

    def getPaddingType(self) -> PaddingMode:
        current_text = self._paddingTypeCB.currentText()
        return PaddingMode(current_text)

    def setPaddingType(self, padding_type):
        padding_type = PaddingMode(padding_type)
        item_index = self._paddingTypeCB.findText(padding_type.value)
        self._paddingTypeCB.setCurrentIndex(item_index)

    def getDeltaBeta(self) -> str:
        return self._deltaBetaQLE.text()

    def setDeltaBetaValue(self, value):
        self._deltaBetaQLE.setText(str(value))

    def getConfiguration(self):
        return {
            "delta_beta": self.getDeltaBeta(),  # this one is not cast because can contain several values
            "padding_type": self.getPaddingType().value,
        }

    def setConfiguration(self, conf):
        # delta_beta
        delta_beta = conf.get("delta_beta", None)
        if delta_beta is not None:
            self._deltaBetaQLE.setText(str(delta_beta))
        # padding_type
        padding_type = conf.get("padding_type", None)
        if padding_type is not None:
            self.setPaddingType(padding_type)


class NabuUnsharpConfig(qt.QWidget, base._NabuStageConfigBase):
    """Configuration widget dedicated to the unsharp options for nabu"""

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent=parent, stage=_NabuStages.PHASE)
        base._NabuStageConfigBase.__init__(self, stage=_NabuStages.PHASE)
        self.__discourageUnSharpMask = False
        self.setLayout(qt.QGridLayout())

        warning_icon = icons.getQIcon("warning")
        warning_unsharp_no_phase = "Warning: applying unsharp mask without phase retrieval can lead to 'noisy' reconstruction"

        # unsharp coeff
        self._unsharpCoeffCB = qt.QCheckBox("unsharp coeff", self)
        self._unsharpCoeffCB.setToolTip(
            "Unsharp mask strength. The unsharped "
            "image is equal to\n  UnsharpedImage "
            "=  (1 + coeff)*originalPaganinImage "
            "- coeff * ConvolvedImage. Setting "
            "this coefficient to zero means that "
            "no unsharp mask will be applied."
        )
        self.layout().addWidget(self._unsharpCoeffCB, 0, 0, 1, 1)
        self._unsharpCoeffQLE = qt.QLineEdit("", self)
        self._unsharpCoeffQLE.setValidator(qt.QDoubleValidator())
        self.layout().addWidget(self._unsharpCoeffQLE, 0, 1, 1, 1)
        self.registerWidget(self._unsharpCoeffCB, "optional")
        self._unsharpCoeffOpt = self.registerWidget(self._unsharpCoeffQLE, "optional")
        # unsharp coeff warning
        self._unSharpCoeffWarning = qt.QLabel("")
        self._unSharpCoeffWarning.setToolTip(warning_unsharp_no_phase)
        self._unSharpCoeffWarning.setPixmap(warning_icon.pixmap(20, state=qt.QIcon.On))
        self.layout().addWidget(self._unSharpCoeffWarning, 0, 2, 1, 1)
        self.registerWidget(self._unSharpCoeffWarning, "optional")

        # unsharp_sigma
        self._unsharpSigmaCB = qt.QCheckBox("unsharp sigma", self)
        self._unsharpSigmaCB.setToolTip(
            "Standard deviation of the Gaussian "
            "filter when applying an unsharp "
            "mask\nafter the Paganin filtering. "
            "Disabled if set to 0."
        )
        self.layout().addWidget(self._unsharpSigmaCB, 1, 0, 1, 1)
        self._unsharpSigmaQLE = qt.QLineEdit("", self)
        self._unsharpSigmaQLE.setValidator(qt.QDoubleValidator())
        self.layout().addWidget(self._unsharpSigmaQLE, 1, 1, 1, 1)
        self.registerWidget(self._unsharpSigmaCB, "optional")
        self._unsharpSigmaOpt = self.registerWidget(self._unsharpSigmaQLE, "optional")
        # unsharp coeff warning
        self._unSharpSigmaWarning = qt.QLabel("")
        self._unSharpSigmaWarning.setToolTip(warning_unsharp_no_phase)
        self._unSharpSigmaWarning.setPixmap(warning_icon.pixmap(20, state=qt.QIcon.On))
        self.layout().addWidget(self._unSharpSigmaWarning, 1, 2, 1, 1)
        self.registerWidget(self._unSharpSigmaWarning, "optional")

        # set up
        self._unsharpCoeffCB.setChecked(False)
        self._unsharpCoeffQLE.setText(str(3.0))
        self._unsharpSigmaCB.setChecked(False)
        self._unsharpSigmaQLE.setText(str(0.8))
        self._showUnsharpCoeffQLE(False)
        self._showUnsharpSigmaQLE(False)
        self._updateUnsharpMaskWarning()

        # signal / slot connection
        ## unsharp coeff
        self._unsharpCoeffCB.toggled.connect(self._showUnsharpCoeffQLE)
        self._unsharpCoeffCB.toggled.connect(self._unsharpCoeffChanged)
        self._unsharpCoeffCB.toggled.connect(self._updateUnsharpMaskWarning)
        self._unsharpCoeffQLE.editingFinished.connect(self._unsharpCoeffChanged)
        ## unsharp sigma
        self._unsharpSigmaCB.toggled.connect(self._showUnsharpSigmaQLE)
        self._unsharpSigmaCB.toggled.connect(self._unsharpSigmaChanged)
        self._unsharpSigmaCB.toggled.connect(self._updateUnsharpMaskWarning)
        self._unsharpSigmaQLE.editingFinished.connect(self._unsharpSigmaChanged)

    def _unsharpCoeffChanged(self, *args, **kwargs):
        self.sigConfChanged.emit("unsharp_coeff")

    def _unsharpSigmaChanged(self, *args, **kwargs):
        self.sigConfChanged.emit("unsharp_sigma")

    def isUnsharpCoeffActive(self):
        return self._unsharpCoeffCB.isChecked()

    def isUnsharpSigmaActive(self):
        return self._unsharpSigmaCB.isChecked()

    def _showUnsharpCoeffQLE(self, visible):
        self._unsharpCoeffOpt.setVisible(visible)

    def _showUnsharpSigmaQLE(self, visible):
        self._unsharpSigmaOpt.setVisible(visible)

    def _signalConfChanged(self, param):
        self.sigConfChanged.emit(param)

    def getUnsharpCoeff(self) -> float | int:
        if self.isUnsharpCoeffActive():
            return float(self._unsharpCoeffQLE.text())
        else:
            return 0

    def setUnsharpCoeff(self, coeff):
        if coeff == 0.0:
            self._unsharpCoeffCB.setChecked(False)
        else:
            self._unsharpCoeffCB.setChecked(True)
            self._unsharpCoeffQLE.setText(str(coeff))

    def getUnsharpSigma(self) -> float | int:
        if self.isUnsharpSigmaActive():
            return float(self._unsharpSigmaQLE.text())
        else:
            return 0

    def setUnsharpSigma(self, sigma):
        if sigma == 0.0:
            self._unsharpSigmaCB.setChecked(False)
        else:
            self._unsharpSigmaCB.setChecked(True)
            self._unsharpSigmaQLE.setText(str(sigma))

    def getConfiguration(self):
        return {
            "unsharp_coeff": self.getUnsharpCoeff(),
            "unsharp_sigma": self.getUnsharpSigma(),
        }

    def setConfiguration(self, conf):
        if "unsharp_coeff" in conf:
            self.setUnsharpCoeff(float(conf["unsharp_coeff"]))
        if "unsharp_sigma" in conf:
            self.setUnsharpSigma(float(conf["unsharp_sigma"]))

    def setDiscourageUnsharpMask(self, discourage: bool):
        """Should we discourage the user to apply unsharp mask.
        This is the case if he tries to apply an unsharp mask without phase retrieval.
        """
        self.__discourageUnSharpMask = discourage

    def _updateUnsharpMaskWarning(self):
        self._unSharpCoeffWarning.setVisible(
            self.__discourageUnSharpMask and self._unsharpCoeffCB.isChecked()
        )
        self._unSharpSigmaWarning.setVisible(
            self.__discourageUnSharpMask and self._unsharpSigmaCB.isChecked()
        )

    def setConfigurationLevel(self, level):
        super().setConfigurationLevel(level)
        # we also need to update the 'unsharp warning'
        # note: at the moment if the basic configuration level is selected, without phase and some mask
        # a warning will appear on bottom of the pahse GB. This is considered expected as this way we
        # won't hide any warning.
        self._updateUnsharpMaskWarning()
