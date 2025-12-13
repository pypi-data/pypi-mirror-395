"""widgets to perform a z-sttiching in pre processing (from projections) or post processing (from reconstructed volumes)"""

from __future__ import annotations


import logging

from nabu.stitching import config as _nabu_stitching_config
from nabu.stitching.config import StitchingType
from nabu.stitching.overlap import OverlapStitchingStrategy
from nabu.stitching.utils import ShiftAlgorithm as _NabuShiftAlgorithm
from silx.gui import qt

_logger = logging.getLogger(__name__)


class Axis_N_Params(qt.QGroupBox):
    """
    widget to edit the option for image registration along a specific axe
    """

    def __init__(self, title, parent=None) -> None:
        super().__init__(title, parent)
        self.setLayout(qt.QFormLayout())

        # img registration method
        self._imageRegMethodCB = qt.QComboBox(self)
        for method in _NabuShiftAlgorithm:
            self._imageRegMethodCB.addItem(method.value)
        self._imageRegMethodCB.setToolTip(
            "method to use in order to affine positions provided by the user"
        )
        self.layout().addRow("image registration method", self._imageRegMethodCB)

        # set up
        self._imageRegMethodCB.setCurrentText(_NabuShiftAlgorithm.NONE.value)

    def getCurrentMethod(self):
        return _NabuShiftAlgorithm(self._imageRegMethodCB.currentText())

    def setCurrentMethod(self, method):
        self._imageRegMethodCB.setCurrentText(_NabuShiftAlgorithm(method).value)

    def getOptsLine(self) -> str:
        current_method = self.getCurrentMethod()
        line_ = f"{_nabu_stitching_config.KEY_IMG_REG_METHOD}={current_method.value}"
        return line_

    def setOptsLine(self, opt_line: str) -> None:
        opt_line = opt_line.replace(",", ";")
        opt_line = opt_line.replace(" ", "")
        opts = {}
        for key_value in filter(None, opt_line.split(";")):
            key, value = key_value.split("=")
            opts[key] = value

        window_size = opts.get(_nabu_stitching_config.KEY_WINDOW_SIZE, None)
        if window_size is not None:
            try:
                self.setWindowSize(int(window_size))
            except Exception as e:
                _logger.error(e)

        img_reg_exp_method = opts.get(_nabu_stitching_config.KEY_IMG_REG_METHOD, None)
        if img_reg_exp_method is not None:
            try:
                self.setCurrentMethod(img_reg_exp_method)
            except Exception as e:
                _logger.error(e)


class AutoRefineWidget(qt.QWidget):
    """
    widget grouping information not specific to objects (output file, stitching strategy...)
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setLayout(qt.QVBoxLayout())

        self._globalOpts = qt.QWidget(self)
        self.layout().addWidget(self._globalOpts)
        self._globalOpts.setLayout(qt.QFormLayout())

        # stitching strategy
        self._stitchingStrategyCG = qt.QComboBox(parent=self)
        for strategy in OverlapStitchingStrategy:
            self._stitchingStrategyCG.addItem(strategy.value)
        self._globalOpts.layout().addRow(
            "stitching strategy", self._stitchingStrategyCG
        )
        # slice for cross correlation
        self._sliceForCorrelation = qt.QLineEdit("middle", self)
        self._globalOpts.layout().addRow(
            "slice for cross correlation", self._sliceForCorrelation
        )
        self._overwritePB = qt.QCheckBox("overwrite", self)
        self._globalOpts.layout().addRow(self._overwritePB)

        # pre processing options
        self._preProcGroup = qt.QGroupBox("pre-processing option", self)
        self.layout().addWidget(self._preProcGroup)
        self._preProcGroup.setLayout(qt.QFormLayout())
        # TODO: check if the widget with output .nx file exists somewhere
        self._outputFile = qt.QLineEdit("", self)
        self._preProcGroup.layout().addRow("output nexus file", self._outputFile)
        self._outputDataPath = qt.QLineEdit("entry0000", self)
        self._preProcGroup.layout().addRow("output data path", self._outputDataPath)

        # post processing options
        self._postProcGroup = qt.QGroupBox("post-processing option", self)
        self._postProcGroup.setLayout(qt.QFormLayout())
        self.layout().addWidget(self._preProcGroup)
        self._outputVolumeIdentifier = qt.QLineEdit("", self)
        self._postProcGroup.layout().addRow(
            "output identifier", self._outputVolumeIdentifier
        )
        self.layout().addWidget(self._postProcGroup)
        # spacer
        self._spacer = qt.QWidget(parent=self)
        self._spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self._spacer)

        # set up
        self._stitchingStrategyCG.setCurrentText(
            OverlapStitchingStrategy.COSINUS_WEIGHTS.value
        )

    def getConfiguration(self) -> dict:
        raise NotImplementedError

    def setConfiguration(self, config: dict):
        raise NotImplementedError

    def updateStitchingType(self, mode: StitchingType):
        mode = StitchingType(mode)
        self._preProcGroup.setVisible(mode is StitchingType.Z_PREPROC)
        self._postProcGroup.setVisible(mode is StitchingType.Z_POSTPROC)

    def getSliceForPreview(self) -> int | str:
        slice = self._sliceForPreview.text()
        try:
            return int(slice)
        except Exception:
            return slice


class ManualRefineWidget(qt.QWidget):
    pass


class _RefineEstimationTabWidget(qt.QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._autoRefine = AutoRefineWidget(parent=self)
        self.addTab(self._autoRefine, "automatique")
        self._manualRefine = ManualRefineWidget(parent=self)
        self.addTab(self._manualRefine, "manual")


class _SliceGetter(qt.QLineEdit):
    class Validator(qt.QIntValidator):
        def validate(self, a0: str, a1: int):
            if a0 in ("first", "middle", "last"):
                return (qt.QValidator.Acceptable, a0, a1)
            elif a0 in (
                "f",
                "fi",
                "fir",
                "firs",
                "m",
                "mi",
                "mid",
                "midd",
                "middl",
                "l",
                "la",
                "las",
            ):
                # dummy hack to avoid letting users write non-sense.
                return (qt.QValidator.Intermediate, a0, a1)
            else:
                return super().validate(a0, a1)

    def __init__(self, contents, parent=None):
        super().__init__(contents, parent)
        self.setValidator(self.Validator(parent=self))


class RefineEstimationCtrlWidget(qt.QWidget):
    sigSlicePreviewChanged = qt.Signal(str)
    """emit when the slice preview has changed"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # main widget
        self.setLayout(qt.QGridLayout())
        self._widget = _RefineEstimationTabWidget(parent=self)
        self.layout().addWidget(self._widget, 0, 0, 3, 3)
        # slice to be used for preview
        self._previewedSliceQLE = _SliceGetter("middle", parent=self)
        self.layout().addWidget(self._previewedSliceQLE, 4, 1, 2, 1)
        # auto update preview
        self._updateAutoPreviewCB = qt.QCheckBox("auto update preview", self)
        self.layout().addWidget(self._updateAutoPreviewCB, 5, 1, 1, 2)

    def isPreviewAuto(self):
        return self._updateAutoPreviewCB.isChecked()

    def setPreviewAuto(self, auto: bool):
        self._updateAutoPreviewCB.setChecked(auto)

    def getSliceForPreview(self) -> str:
        return self._previewedSliceQLE.text()

    def setSliceForPreview(self, slice: str):
        self._previewedSliceQLE.setText(str(slice))
