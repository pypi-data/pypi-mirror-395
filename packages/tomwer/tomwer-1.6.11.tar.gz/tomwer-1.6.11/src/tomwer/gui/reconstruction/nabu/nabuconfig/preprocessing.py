from __future__ import annotations

import logging

import sys
from silx.gui import qt

from tomwer.core.process.reconstruction.nabu.utils import (
    _NabuStages,
    RingCorrectionMethod,
)
from tomwer.gui.reconstruction.nabu.nabuconfig.base import _NabuStageConfigBase
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel as QComboBox
from tomwer.gui.utils.scrollarea import QDoubleSpinBoxIgnoreWheel as QDoubleSpinBox
from tomwer.gui.utils.scrollarea import QSpinBoxIgnoreWheel as QSpinBox
from tomwer.utils import docstring

_logger = logging.getLogger(__name__)


class _NabuPreProcessingConfig(_NabuStageConfigBase, qt.QWidget):
    """
    Widget to define the configuration of the nabu preprocessing
    """

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent):
        _NabuStageConfigBase.__init__(self, stage=_NabuStages.PRE)
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        # default options
        ## flat field
        self._flatFieldCB = qt.QCheckBox("flat field correction", self)
        self._flatFieldCB.setToolTip("Whether to enable flat-field " "normalization")
        self.layout().addWidget(self._flatFieldCB, 0, 0, 1, 2)
        self.registerWidget(self._flatFieldCB, "optional")

        ## double flat field
        self._dffCB = qt.QCheckBox("double flat field correction", self)
        self._dffCB.setToolTip("Whether to enable double flat field " "normalization")
        self.layout().addWidget(self._dffCB, 1, 0, 1, 2)
        self._dffSigmaLabel = qt.QLabel("sigma:", self)
        self._dffSigmaLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._dffSigmaLabel, 1, 2, 1, 1)
        self._dffSigmaQDSB = QDoubleSpinBox(parent=self)
        self._dffSigmaQDSB.setMinimum(0.0)
        self._dffSigmaQDSB.setDecimals(2)
        self._dffSigmaQDSB.setSingleStep(0.1)
        self._dffSigmaQDSB.setToolTip(
            "Sigma value to give to the double flat field unsharp mask"
        )
        self.layout().addWidget(self._dffSigmaQDSB, 1, 3, 1, 1)
        self.registerWidget(self._flatFieldCB, "required")
        self._dffOptWidgets = [
            self.registerWidget(self._dffSigmaLabel, "required"),
            self.registerWidget(self._dffSigmaQDSB, "required"),
        ]

        ## sinogram ring correction
        self._sinoRingCorrectionCB = qt.QLabel("rings removal method", self)
        self._sinoRingCorrectionCB.setToolTip("Sinogram rings removal method")
        self.layout().addWidget(self._sinoRingCorrectionCB, 2, 0, 1, 2)
        self.registerWidget(self._sinoRingCorrectionCB, "required")

        self._sinoRingCorrectionMthd = QComboBox(parent=self)
        for method in RingCorrectionMethod:
            self._sinoRingCorrectionMthd.addItem(method.value)
        ## force method to be None by default
        idx = self._sinoRingCorrectionMthd.findText(RingCorrectionMethod.NONE.value)
        self._sinoRingCorrectionMthd.setCurrentIndex(idx)

        self.layout().addWidget(self._sinoRingCorrectionMthd, 2, 2, 1, 1)
        self.registerWidget(self._sinoRingCorrectionMthd, "required")

        self._sinoRingsOpts = SinoRingsOptions(parent=self)
        self.layout().addWidget(self._sinoRingsOpts, 3, 1, 1, 3)

        ## ccd filter
        self._ccdFilterCB = qt.QCheckBox("CCD hot spot correction", self)
        self._ccdFilterCB.setToolTip("Whether to enable the CCD hotspots " "correction")
        self.layout().addWidget(self._ccdFilterCB, 4, 0, 1, 2)
        self.registerWidget(self._ccdFilterCB, "optional")

        ## ccd filter threshold
        self._ccdHotspotLabel = qt.QLabel("threshold:", self)
        self._ccdHotspotLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._ccdHotspotLabel, 5, 2, 1, 1)
        self._ccdThreshold = QDoubleSpinBox(self)
        self._ccdThreshold.setMinimum(0.0)
        self._ccdThreshold.setMaximum(999999)
        self._ccdThreshold.setSingleStep(0.01)
        self._ccdThreshold.setDecimals(6)
        tooltip = (
            "If ccd_filter_enabled = 1, a median filter is applied on "
            "the 3X3 neighborhood\nof every pixel. If a pixel value "
            "exceeds the median value more than this parameter,\nthen "
            "the pixel value is replaced with the median value."
        )
        self._ccdThreshold.setToolTip(tooltip)
        self.layout().addWidget(self._ccdThreshold, 5, 3, 1, 1)
        self._ccdOptWidgets = [
            self.registerWidget(self._ccdHotspotLabel, "optional"),
            self.registerWidget(self._ccdThreshold, "optional"),
        ]

        ## sr current normalization
        self._normalizeCurrent = qt.QCheckBox(
            "Normalize by machine electric current", self
        )
        self._normalizeCurrent.setToolTip(
            "Whether to normalize frames with Synchrotron Current. This can correct the effect of a beam refill not taken into account by flats."
        )
        self.layout().addWidget(self._normalizeCurrent, 6, 0, 1, 2)
        self.registerWidget(self._normalizeCurrent, "required")

        ## take logarithm
        self._takeLogarithmCB = qt.QCheckBox("take logarithm", self)
        self.layout().addWidget(self._takeLogarithmCB, 7, 0, 1, 2)
        self.registerWidget(self._takeLogarithmCB, "advanced")

        ## log min clip value
        self._clipMinLogValueLabel = qt.QLabel("log min clip value:", self)
        self._clipMinLogValueLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._clipMinLogValueLabel, 8, 2, 1, 1)
        self._clipMinLogValue = QDoubleSpinBox(self)
        self._clipMinLogValue.setMinimum(0.0)
        self._clipMinLogValue.setMaximum(9999999)
        self._clipMinLogValue.setSingleStep(0.01)
        self._clipMinLogValue.setDecimals(6)
        self.layout().addWidget(self._clipMinLogValue, 8, 3, 1, 1)
        self._takeLogOpt = [
            self.registerWidget(self._clipMinLogValueLabel, "optional"),
            self.registerWidget(self._clipMinLogValue, "optional"),
        ]

        ## log max clip value
        self._clipMaxLogValueLabel = qt.QLabel("log max clip value:", self)
        self._clipMaxLogValueLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._clipMaxLogValueLabel, 9, 2, 1, 1)
        self._clipMaxLogValue = QDoubleSpinBox(self)
        self._clipMaxLogValue.setMinimum(0.0)
        self._clipMaxLogValue.setMaximum(9999999)
        self._clipMaxLogValue.setSingleStep(0.01)
        self._clipMaxLogValue.setDecimals(6)
        self.layout().addWidget(self._clipMaxLogValue, 9, 3, 1, 1)
        self._takeLogOpt.extend(
            [
                self.registerWidget(self._clipMaxLogValueLabel, "optional"),
                self.registerWidget(self._clipMaxLogValue, "optional"),
            ]
        )

        ## tilt correction
        self._tiltCorrection = TiltCorrection("tilt correction", self)
        self.registerWidget(self._tiltCorrection, "advanced")
        self.layout().addWidget(self._tiltCorrection, 10, 0, 1, 4)

        # option dedicated to Helical
        ## process file
        self._processFileLabel = qt.QLabel("file containing weights maps", self)
        self.registerWidget(self._processFileLabel, "advanced")
        self.layout().addWidget(self._processFileLabel, 20, 0, 1, 1)
        self._processFileQLE = qt.QLineEdit("", self)
        self.registerWidget(self._processFileQLE, "advanced")
        self._processFileQLE.setToolTip(
            "also know as 'process_file'. If you don't have this file it can be created from the 'helical-prepare-weights' widget"
        )
        self.layout().addWidget(self._processFileQLE, 20, 1, 1, 3)

        # style

        # spacer for style
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 99, 0, 1, 1)

        # set up
        self._flatFieldCB.setChecked(True)
        self.setDFFOptVisible(False)

        self._ccdFilterCB.setChecked(False)
        self._normalizeCurrent.setChecked(False)
        self._ccdThreshold.setValue(0.04)

        self._clipMinLogValue.setValue(1e-6)
        self._clipMaxLogValue.setValue(10.0)
        self._takeLogarithmCB.setChecked(True)
        self.setCCDOptsVisible(False)
        self._sinoRingCorrectionMthd.setCurrentText("None")
        self._sinoRingsOpts.setVisible(False)
        self._tiltCorrection.setChecked(False)

        # connect signal / slot
        self._ccdFilterCB.toggled.connect(self.setCCDOptsVisible)
        self._takeLogarithmCB.toggled.connect(self.setLogClipValueVisible)
        self._flatFieldCB.toggled.connect(self._flatFieldChanged)
        self._dffCB.toggled.connect(self._dffChanged)
        self._dffCB.toggled.connect(self.setDFFOptVisible)
        self._dffSigmaQDSB.valueChanged.connect(self._dffSigmaChanged)
        self._ccdFilterCB.toggled.connect(self._ccdFilterChanged)
        self._normalizeCurrent.toggled.connect(self._normalizeCurrentChanged)
        self._ccdThreshold.editingFinished.connect(self._ccdFilterThresholdChanged)
        self._clipMinLogValue.editingFinished.connect(self._logMinClipChanged)
        self._clipMaxLogValue.editingFinished.connect(self._logMaxClipChanged)
        self._takeLogarithmCB.toggled.connect(self._takeLogarithmChanged)
        self._sinoRingCorrectionMthd.currentIndexChanged.connect(
            self._sinoRingCorrectionChanged
        )
        self._sinoRingsOpts._levelsMunch.valueChanged.connect(self._sinoRingOptsChanged)
        self._sinoRingsOpts._sigmaMunch.valueChanged.connect(self._sinoRingOptsChanged)

        self._tiltCorrection.toggled.connect(self._tiltCorrectionChanged)
        self._tiltCorrection.sigChanged.connect(self._tiltCorrectionChanged)

    def _flatFieldChanged(self, *args, **kwargs):
        self._signalConfChanged("flatfield")

    def _dffChanged(self, *args, **kwargs):
        self._signalConfChanged("double_flatfield")

    def _dffSigmaChanged(self, *args, **kwargs):
        self._signalConfChanged("dff_sigma")

    def _ccdFilterChanged(self, *args, **kwargs):
        self._signalConfChanged("ccd_filter_enabled")

    def _normalizeCurrentChanged(self, *args, **kwargs):
        self._signalConfChanged("normalize_srcurrent")

    def _ccdFilterThresholdChanged(self, *args, **kwargs):
        self._signalConfChanged("ccd_filter_threshold")

    def _logMinClipChanged(self, *args, **kwargs):
        self._signalConfChanged("log_min_clip")

    def _logMaxClipChanged(self, *args, **kwargs):
        self._signalConfChanged("log_max_clip")

    def _takeLogarithmChanged(self, *args, **kwargs):
        self._signalConfChanged("take_logarithm")

    def _sinoRingCorrectionChanged(self, *args, **kwargs):
        method = self.getSinoRingcorrectionMethod()
        if method is not RingCorrectionMethod.NONE.value:
            self._sinoRingsOpts.setVisible(True)
            self._sinoRingsOpts.setMethod(method)
        else:
            self._sinoRingsOpts.setVisible(False)

        self._signalConfChanged("sino_rings_correction")

    def _sinoRingOptsChanged(self, *args, **kwargs):
        self._signalConfChanged("sino_rings_options")

    def _tiltCorrectionChanged(self, *args, **kwargs):
        self._signalConfChanged("tilt_correction")

    def _signalConfChanged(self, param, *args, **kwargs):
        self.sigConfChanged.emit(param)

    def setDFFOptVisible(self, visible):
        for widget in self._dffOptWidgets:
            widget.setVisible(visible)

    def setCCDOptsVisible(self, visible):
        for widget in self._ccdOptWidgets:
            widget.setVisible(visible)

    def setLogClipValueVisible(self, visible):
        for widget in self._takeLogOpt:
            widget.setVisible(visible)

    def isFlatFieldActivate(self):
        return self._flatFieldCB.isChecked()

    def isDoubleFlatFieldActivate(self):
        return self._dffCB.isChecked()

    def getDFFSigma(self) -> float:
        """

        :return: double flat field sigma
        """
        return self._dffSigmaQDSB.value()

    def isCCDFilterActivate(self):
        return self._ccdFilterCB.isChecked()

    def getCCDThreshold(self) -> float:
        return float(self._ccdThreshold.text())

    def getNormalizeCurrent(self) -> bool:
        return self._normalizeCurrent.isChecked()

    def setNormalizeCurrent(self, normalize: bool) -> None:
        self._normalizeCurrent.setChecked(normalize)

    def getLogMinClipValue(self) -> float:
        return float(self._clipMinLogValue.text())

    def getLogMaxClipValue(self) -> float:
        return float(self._clipMaxLogValue.text())

    def getTakeLogarithm(self):
        return self._takeLogarithmCB.isChecked()

    def getSinoRingcorrectionMethod(self) -> str:
        return self._sinoRingCorrectionMthd.currentText()

    def getSinoRingcorrectionOptions(self) -> str:
        return " ; ".join(
            [
                f"{key}={value}"
                for key, value in self._sinoRingsOpts.getOptions().items()
            ]
        )

    def setSinoRingcorrectionOptions(self, options: str) -> None:
        opt_as_dict = {}
        for opt in options.split(";"):
            opt = opt.replace(" ", "")
            if len(opt.split("=")) == 2:
                key, value = opt.split("=")
                opt_as_dict[key] = value
            else:
                _logger.info(f"ignore option {opt}. Invalid synthax")

        self._sinoRingsOpts.setOptions(opt_as_dict)

    @docstring(_NabuStageConfigBase)
    def getConfiguration(self):
        tilt_correction, autotilt_opts = self._tiltCorrection.getTiltCorrection()
        return {
            "flatfield": int(self.isFlatFieldActivate()),
            "double_flatfield": int(self.isDoubleFlatFieldActivate()),
            "dff_sigma": self.getDFFSigma(),
            "ccd_filter_enabled": int(self.isCCDFilterActivate()),
            "ccd_filter_threshold": self.getCCDThreshold(),
            "take_logarithm": self.getTakeLogarithm(),
            "log_min_clip": self.getLogMinClipValue(),
            "log_max_clip": self.getLogMaxClipValue(),
            "sino_rings_correction": self.getSinoRingcorrectionMethod(),
            "sino_rings_options": self.getSinoRingcorrectionOptions(),
            "tilt_correction": tilt_correction,
            "autotilt_options": autotilt_opts,
            "normalize_srcurrent": int(self.getNormalizeCurrent()),
            "rotate_projections_center": self._tiltCorrection.getRotateProjectionsCenter()
            or "",
        }

    @docstring(_NabuStageConfigBase)
    def setConfiguration(self, conf):
        try:
            self._setConfiguration(conf)
        except Exception as e:
            _logger.error(e)

    def _setConfiguration(self, conf: dict):
        ff = conf.get("flatfield", None)
        if ff is not None:
            self._flatFieldCB.setChecked(bool(ff))

        dff = conf.get("double_flatfield", None)
        if dff is not None:
            self._dffCB.setChecked(bool(dff))

        dff_sigma = conf.get("dff_sigma", None)
        if dff_sigma not in (None, "", "none"):
            self._dffSigmaQDSB.setValue(float(dff_sigma))

        ccd_filter = conf.get("ccd_filter_enabled", None)
        if ccd_filter not in (None, "", "none"):
            self._ccdFilterCB.setChecked(bool(ccd_filter))

        ccd_filter_threshold = conf.get("ccd_filter_threshold", None)
        if ccd_filter_threshold not in (None, "", "none"):
            self._ccdThreshold.setValue(float(ccd_filter_threshold))

        normalize_srcurrent = conf.get("normalize_srcurrent", None)
        if normalize_srcurrent is not None:
            self.setNormalizeCurrent(bool(normalize_srcurrent))

        take_logarithm = conf.get("take_logarithm", None)
        if take_logarithm not in (None, "", "none"):
            self._takeLogarithmCB.setChecked(bool(take_logarithm))

        clip_value = conf.get("log_min_clip", None)
        if clip_value not in (None, "", "none"):
            self._clipMinLogValue.setValue(float(clip_value))

        clip_value = conf.get("log_max_clip", None)
        if clip_value not in (None, "", "none"):
            self._clipMaxLogValue.setValue(float(clip_value))

        sino_rings_correction = conf.get("sino_rings_correction", None)
        if sino_rings_correction is not None:
            if sino_rings_correction == "":
                sino_rings_correction = RingCorrectionMethod.NONE
            sino_rings_correction = RingCorrectionMethod(sino_rings_correction).value
            idx = self._sinoRingCorrectionMthd.findText(sino_rings_correction)
            if idx >= 0:
                self._sinoRingCorrectionMthd.setCurrentIndex(idx)
        sino_rings_options = conf.get("sino_rings_options", None)
        if sino_rings_options is not None:
            self.setSinoRingcorrectionOptions(options=sino_rings_options)

        tilt_correction = conf.get("tilt_correction")
        autotilt_options = conf.get("autotilt_options")
        self._tiltCorrection.setTiltCorrection(
            tilt_correction=tilt_correction, auto_tilt_options=autotilt_options
        )

        rotate_projections_center = conf.get("rotate_projections_center")
        if rotate_projections_center == "":
            rotate_projections_center = None
        self._tiltCorrection.setRotateProjectionsCenter(rotate_projections_center)


class SinoRingsOptions(qt.QWidget):
    _VO_DIMS = ("horizontaly", "horizontaly and vertically")

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._method = None
        self.setLayout(qt.QFormLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        # munch parameters
        self._sigmaMunchLabel = qt.QLabel("sigma", self)
        self._sigmaMunch = QDoubleSpinBox(self)
        self._sigmaMunch.setRange(0.0, 2147483647)
        self.layout().addRow(self._sigmaMunchLabel, self._sigmaMunch)

        self._levelsMunchLabel = qt.QLabel("levels", self)
        self._levelsMunch = QSpinBox(self)
        self._levelsMunch.setRange(0, 2147483647)
        self.layout().addRow(self._levelsMunchLabel, self._levelsMunch)

        self._paddingMunch = qt.QCheckBox("padding", self)
        self.layout().addWidget(self._paddingMunch)

        # vo parameters
        self._snrVOLabel = qt.QLabel("snr", self)
        self._snrVO = QDoubleSpinBox(self)
        self._snrVO.setMinimum(0.0)
        tooltip = "Ratio used to locate large stripes. Greater is less sensitive."
        self._snrVO.setToolTip(tooltip)
        self._snrVOLabel.setToolTip(tooltip)
        self.layout().addRow(self._snrVOLabel, self._snrVO)

        self._laSizeVOLabel = qt.QLabel("la_size", self)
        self._laSizeVO = QSpinBox(self)
        self._laSizeVO.setMinimum(0)
        tooltip = "Window size of the median filter to remove large stripes."
        self._laSizeVO.setToolTip(tooltip)
        self._laSizeVOLabel.setToolTip(tooltip)
        self.layout().addRow(self._laSizeVOLabel, self._laSizeVO)

        self._smSizeVOLabel = qt.QLabel("sm_size", self)
        self._smSizeVO = QSpinBox(self)
        self._smSizeVO.setMinimum(0)
        tooltip = "Window size of the median filter to remove small-to-medium stripes."
        self._laSizeVO.setToolTip(tooltip)
        self._smSizeVOLabel.setToolTip(tooltip)
        self.layout().addRow(self._smSizeVOLabel, self._smSizeVO)

        self._dimVOLabel = qt.QLabel("dimension", self)
        self._dimVO = QComboBox(self)
        self._dimVO.addItems(self._VO_DIMS)
        self.layout().addRow(self._dimVOLabel, self._dimVO)

        # sino mean deringer
        self._sigmaLowLabel = qt.QLabel("signal low", self)
        self._sigmaLow = QDoubleSpinBox(self)
        self._sigmaLow.setMinimum(0.0)
        self._sigmaHighLabel = qt.QLabel("signal high", self)
        self.layout().addRow(self._sigmaLowLabel, self._sigmaLow)

        self._sigmaHigh = QDoubleSpinBox(self)
        self._sigmaHigh.setMinimum(0.0)
        tooltip = (
            "sigma low and sigma high values are defining the standard deviation of "
            "gaussian(sigma_low) * (1 - gaussian(sigma_high)). \n"
            "High values of sigma mean stronger effect of associated filters."
        )
        self._sigmaHigh.setToolTip(tooltip)
        self._sigmaLow.setToolTip(tooltip)
        self.layout().addRow(self._sigmaHighLabel, self._sigmaHigh)
        # set up
        self.resetConfiguration()

    def resetConfiguration(self):
        self.setMethod(method=RingCorrectionMethod.MUNCH)
        self._levelsMunch.setValue(10)
        self._sigmaMunch.setValue(1.0)
        self._paddingMunch.setChecked(False)

        self._sigmaHigh.setValue(30.0)
        self._sigmaLow.setValue(0.0)

        self._snrVO.setValue(3.0)
        self._laSizeVO.setValue(51)
        self._smSizeVO.setValue(21)

    def getVoDim(self):
        if self._dimVO.currentText() == self._VO_DIMS[0]:
            return 1
        elif self._dimVO.currentText() == self._VO_DIMS[1]:
            return 2
        else:
            raise NotImplementedError

    def setVoDim(self, dim: int | str):
        if dim in ("1", 1, self._VO_DIMS[0]):
            self._dimVO.setCurrentText(self._VO_DIMS[0])
        elif dim in ("2", 2, self._VO_DIMS[1]):
            self._dimVO.setCurrentText(self._VO_DIMS[1])
        else:
            raise NotImplementedError(f"dim {dim} not handled")

    def getOptions(self) -> dict:
        if self.getMethod() is RingCorrectionMethod.NONE:
            return {}
        elif self.getMethod() is RingCorrectionMethod.MUNCH:
            return {
                "sigma": self._sigmaMunch.value(),
                "levels": self._levelsMunch.value(),
                "padding": self._paddingMunch.isChecked(),
            }
        elif self.getMethod() is RingCorrectionMethod.VO:
            return {
                "snr": self._snrVO.value(),
                "la_size": self._laSizeVO.value(),
                "sm_size": self._smSizeVO.value(),
                "dim": self.getVoDim(),
            }
        elif self.getMethod() in (
            RingCorrectionMethod.MEAN_DIVISION,
            RingCorrectionMethod.MEAN_SUBTRACTION,
        ):
            return {
                "filter_cutoff": (self._sigmaLow.value(), self._sigmaHigh.value()),
            }
        else:
            raise NotImplementedError

    def setOptions(self, options: dict) -> None:
        # handle munch propertoies
        if "sigma" in options:
            self._sigmaMunch.setValue(float(options["sigma"]))
        if "levels" in options:
            self._levelsMunch.setValue(int(options["levels"]))
        padding = options.get("padding")
        if padding is not None:
            self._paddingMunch.setChecked(padding in (True, 1, "1", "True"))
        # handle VO properties
        snr = options.get("snr")
        if snr is not None:
            self._snrVO.setValue(float(snr))
        la_size = options.get("la_size")
        if la_size is not None:
            self._laSizeVO.setValue(int(la_size))
        sm_size = options.get("sm_size")
        if sm_size is not None:
            self._smSizeVO.setValue(int(sm_size))
        dim = options.get("dim")
        if dim is not None:
            self.setVoDim(dim)
        # handle mean subtraction or division options
        filter_cutoff = options.get("filter_cutoff")
        if filter_cutoff is not None:
            low_pass, high_pass = filter_cutoff
            self._sigmaLow.setValue(float(low_pass))
            self._sigmaHigh.setValue(float(high_pass))

    def setMethod(self, method: RingCorrectionMethod):
        method = RingCorrectionMethod(method)
        self._method = method
        # handle munch options
        self._sigmaMunch.setVisible(method is RingCorrectionMethod.MUNCH)
        self._sigmaMunchLabel.setVisible(method is RingCorrectionMethod.MUNCH)
        self._levelsMunch.setVisible(method is RingCorrectionMethod.MUNCH)
        self._levelsMunchLabel.setVisible(method is RingCorrectionMethod.MUNCH)
        self._paddingMunch.setVisible(method is RingCorrectionMethod.MUNCH)
        # handle VO options
        self._snrVO.setVisible(method is RingCorrectionMethod.VO)
        self._snrVOLabel.setVisible(method is RingCorrectionMethod.VO)
        self._laSizeVO.setVisible(method is RingCorrectionMethod.VO)
        self._laSizeVOLabel.setVisible(method is RingCorrectionMethod.VO)
        self._smSizeVO.setVisible(method is RingCorrectionMethod.VO)
        self._smSizeVOLabel.setVisible(method is RingCorrectionMethod.VO)
        self._dimVO.setVisible(method is RingCorrectionMethod.VO)
        self._dimVOLabel.setVisible(method is RingCorrectionMethod.VO)
        # mean subtractions / division deringer
        self._sigmaLow.setVisible(
            method
            in (
                RingCorrectionMethod.MEAN_DIVISION,
                RingCorrectionMethod.MEAN_SUBTRACTION,
            )
        )
        self._sigmaLowLabel.setVisible(
            method
            in (
                RingCorrectionMethod.MEAN_DIVISION,
                RingCorrectionMethod.MEAN_SUBTRACTION,
            )
        )
        self._sigmaHigh.setVisible(
            method
            in (
                RingCorrectionMethod.MEAN_DIVISION,
                RingCorrectionMethod.MEAN_SUBTRACTION,
            )
        )
        self._sigmaHighLabel.setVisible(
            method
            in (
                RingCorrectionMethod.MEAN_DIVISION,
                RingCorrectionMethod.MEAN_SUBTRACTION,
            )
        )

    def getMethod(self) -> RingCorrectionMethod:
        return self._method


class TiltCorrection(qt.QGroupBox):
    """
    GroupBox dedicated to nabu TiltCorrection
    """

    sigChanged = qt.Signal()
    """Signal emit when parameters of the tilt options changed"""

    def __init__(self, text, parent=None, *args, **kwargs) -> None:
        super().__init__(text, parent, *args, **kwargs)
        self.setCheckable(True)
        self.setLayout(qt.QFormLayout())
        self._tiltManualRB = qt.QRadioButton("angle", self)
        self._angleValueSB = QDoubleSpinBox(self)
        self._angleValueSB.setRange(-360, 360)
        self._angleValueSB.setSuffix("°")
        self.layout().addRow(self._tiltManualRB, self._angleValueSB)

        self._autoManualRB = qt.QRadioButton("auto", self)
        self._autoModeCB = QComboBox(self)
        self._modes = {
            "1d-correlation": "auto-detect tilt with the 1D correlation method (fastest, but works best for small tilts)",
            "fft-polar": "auto-detect tilt with polar FFT method (slower, but works well on all ranges of tilts)",
        }
        for value, tooltip in self._modes.items():
            self._autoModeCB.addItem(value)
            idx = self._autoModeCB.findText(value)
            self._autoModeCB.setItemData(idx, tooltip, qt.Qt.ToolTipRole)
        self.layout().addRow(self._autoManualRB, self._autoModeCB)
        self._autoTiltOptions = qt.QLineEdit("", self)
        self._autoTiltOptions.setPlaceholderText("low_pass=1; high_pass=20 ; ...")
        self._autotiltOptsLabel = qt.QLabel("autotilt options")
        self._autotiltOptsLabel.setToolTip(
            """
        Options for methods computing automatically the detector tilt. \n
        The parameters are separated by commas and passed as 'name=value', for example: low_pass=1; high_pass=20. Mind the semicolon separator (;). \n
        For more details please see https://www.silx.org/pub/nabu/doc/apidoc/nabu.estimation.tilt.html#nabu.estimation.tilt.CameraTilt.compute_angle
        """
        )
        self.layout().addRow(self._autotiltOptsLabel, self._autoTiltOptions)
        ## `rotate_projections_center` option
        self._rotateProjectionCenter = RotateProjectionCenterWidget(self)
        self._rotateProjectionCenter.setToolTip(
            "\n".join(
                (
                    "Allows to correct detector tilt along beam orthogonal plan.",
                    "By default the center of rotation is the middle of each radio, i.e ((Nx-1)/2.0, (Ny-1)/2.0).",
                )
            )
        )
        self.layout().addRow(self._rotateProjectionCenter)

        # set up
        self._autoManualRB.setChecked(True)

        # connect signal / slot
        self._tiltManualRB.toggled.connect(self._updateVisibility)
        self._autoManualRB.toggled.connect(self._updateVisibility)

        self._tiltManualRB.toggled.connect(self._changed)
        self._autoManualRB.toggled.connect(self._changed)
        self._angleValueSB.valueChanged.connect(self._changed)

        self._updateVisibility()

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def _updateVisibility(self):
        self._angleValueSB.setEnabled(self._tiltManualRB.isChecked())
        self._autoModeCB.setEnabled(self._autoManualRB.isChecked())
        self._autotiltOptsLabel.setVisible(self._autoManualRB.isChecked())
        self._autoTiltOptions.setVisible(self._autoManualRB.isChecked())

    def getTiltCorrection(self) -> tuple:
        """
        return (tilt value, autotilt options (if any))
        """
        if not self.isChecked():
            return "", ""
        elif self._tiltManualRB.isChecked():
            return self._angleValueSB.value(), ""
        else:
            return self._autoModeCB.currentText(), self._autoTiltOptions.text()

    def setTiltCorrection(
        self, tilt_correction: str, auto_tilt_options: str | None = None
    ) -> None:
        if tilt_correction in ("", None):
            self.setChecked(False)
        elif tilt_correction in self._modes.keys():
            self.setChecked(True)
            self._autoManualRB.setChecked(True)
            idx = self._autoModeCB.findText(tilt_correction)
            self._autoModeCB.setCurrentIndex(idx)
        else:
            self.setChecked(True)
            self._tiltManualRB.setChecked(True)
            self._angleValueSB.setValue(float(tilt_correction))
        if auto_tilt_options is not None:
            self._autoTiltOptions.setText(auto_tilt_options)

    def getRotateProjectionsCenter(self):
        if self.isChecked():
            return self._rotateProjectionCenter.getRotateProjectionsCenter()
        else:
            return None

    def setRotateProjectionsCenter(self, values):
        self._rotateProjectionCenter.setRotateProjectionsCenter(values=values)


class RotateProjectionCenterWidget(qt.QWidget):

    RANGE_MIN_VALUE = -sys.float_info.max
    RANGE_MAX_VALUE = sys.float_info.max

    def __init__(self, parent: qt.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())
        self._label = qt.QLabel("rotate projections center")
        self.layout().addWidget(self._label)

        self._xQLE = QDoubleSpinBox(self)
        self._xQLE.setRange(
            RotateProjectionCenterWidget.RANGE_MIN_VALUE,
            RotateProjectionCenterWidget.RANGE_MAX_VALUE,
        )
        self._xQLE.setPrefix("x=")
        self._xQLE.setToolTip("Value should be in [-radio width, radio width]")
        self._xQLE.setSuffix("px")
        self.layout().addWidget(self._xQLE)

        self._yQLE = QDoubleSpinBox(self)
        self._yQLE.setRange(
            RotateProjectionCenterWidget.RANGE_MIN_VALUE,
            RotateProjectionCenterWidget.RANGE_MAX_VALUE,
        )
        self._yQLE.setPrefix("y=")
        self._xQLE.setToolTip("Value should be in [-radio heigh, radio heigh]")
        self._yQLE.setSuffix("px")
        self.layout().addWidget(self._yQLE)

    def getRotateProjectionsCenter(self) -> tuple | None:
        if self._xQLE.value() == 0 and self._yQLE.value() == 0:
            return None
        else:
            return (self._xQLE.value(), self._yQLE.value())

    def setRotateProjectionsCenter(self, values: tuple[float] | None):
        if values is None:
            self._xQLE.setValue(0.0)
            self._yQLE.setValue(0.0)
        elif not isinstance(values, (tuple, list)) and len(values) != 2:
            raise TypeError("values should be a tuple of two elements")
        else:
            self._xQLE.setValue(values[0])
            self._yQLE.setValue(values[1])
