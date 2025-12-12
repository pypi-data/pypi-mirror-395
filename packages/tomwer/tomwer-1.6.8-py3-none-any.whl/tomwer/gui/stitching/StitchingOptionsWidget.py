from __future__ import annotations

from silx.gui import qt

from nabu.stitching.config import StitchingType
from nabu.stitching import config as stitching_config
from nabu.stitching.config import (
    KEY_RESCALE_MAX_PERCENTILES,
    KEY_RESCALE_MIN_PERCENTILES,
    RESCALE_FRAMES,
    RESCALE_PARAMS,
    STITCHING_SECTION,
)
from nabu.stitching.utils import ShiftAlgorithm as StitchShiftAlgorithm

from nxtomomill.models.utils import convert_str_to_bool as _convert_str_to_bool

from tomwer.gui.configuration.level import ConfigurationLevel
from tomwer.gui.stitching.config.stitchingstrategies import StitchingStrategies
from tomwer.gui.stitching.z_stitching.fineestimation import _SliceGetter
from tomwer.gui.stitching.alignment import _AlignmentGroupBox
from tomwer.gui.stitching.config.axisparams import StitcherAxisParams
from tomwer.gui.stitching.normalization import NormalizationBySampleGroupBox
from tomwer.io.utils.utils import str_to_dict

from .utils import concatenate_dict


class StitchingOptionsWidget(qt.QWidget):
    """
    Widget to let the user define the different options for z-stitching such as which algorithm to search shift,
    which stitching strategy...
    """

    sigChanged = qt.Signal()
    """Signal emit when the options change"""
    sigSliceForPreviewChanged = qt.Signal(object)
    """Signal emit when the slice requested for the preview has changed. Parameter is a str or an int"""
    sigFlipLRChanged = qt.Signal(bool)
    """Signal emit when the request to flip LR frame has changed"""
    sigFlipUDChanged = qt.Signal(bool)
    """Signal emit when the request to flip UD frame has changed"""

    def __init__(
        self, first_axis: int, second_axis: int, parent=None, *args, **kwargs
    ) -> None:
        super().__init__(parent, *args, **kwargs)
        # stitching strategy (aka stitcher behavior)
        self.setLayout(qt.QFormLayout())
        self._stitchingStrategiesWidget = StitchingStrategies(
            parent=self, axis=first_axis
        )
        self._stitchingStrategiesWidget.setObjectName("strategy")
        self.layout().addRow(self._stitchingStrategiesWidget)
        # slice for preview
        self._previewSlices = _SliceGetter("middle", parent=self)
        self._previewSlices.setPlaceholderText(
            "slice index or one of ('middle', 'first', 'last')"
        )
        self._previewSlices.setToolTip(
            "expects a slice index (int > 0) or a str in ('first', 'middle', 'last')"
        )
        self.layout().addRow("slice for preview", self._previewSlices)

        # invert frame up - down
        self._flipLR_CB = qt.QCheckBox("flip frame left-right", self)
        self._flipLR_CB.setChecked(False)
        self._flipLR_CB.setToolTip(
            "Flip frame for stitching. This is mostly for volume has no metadata are existing to specify the direction of the frame"
        )
        self.layout().addRow(self._flipLR_CB)

        # invert frame left-right
        self._flipUD_CB = qt.QCheckBox("flip frame up-down", self)
        self._flipUD_CB.setChecked(False)
        self._flipUD_CB.setToolTip(
            "Flip frame for stitching. This is mostly for volume has no metadata are existing to specify the direction of the frame"
        )
        self.layout().addRow(self._flipUD_CB)

        # avoid data duplication
        self._avoidDataDuplication_CB = qt.QCheckBox("avoid data duplication", self)
        self._avoidDataDuplication_CB.setChecked(False)
        self._avoidDataDuplication_CB.setEnabled(False)
        self._avoidDataDuplication_CB.setToolTip(
            "Avoid data duplication (only enabled for stitching on reconstructed volumes)"
        )
        self.layout().addRow(self._avoidDataDuplication_CB)

        # alignment options
        self._alignmentGroup = _AlignmentGroupBox(self)
        self.layout().addRow(self._alignmentGroup)

        # slices to be reconstructed
        self._slices = _SlicesSelector(parent=self)
        self._slices.setToolTip(
            "for pre processing stitching those are projections and for post processing stitching those are volume slices"
        )
        self.layout().addRow(self._slices)

        # axis 0 params for shift search
        self._firstAxisGroup = qt.QGroupBox(f"axis {first_axis}", self)
        self._firstAxisGroup.setLayout(qt.QVBoxLayout())
        self.layout().addRow(self._firstAxisGroup)
        self._firstAxisShiftSearchParams = StitcherAxisParams(
            axis=first_axis, parent=self
        )
        self._firstAxisShiftSearchParams.layout().setContentsMargins(0, 0, 0, 0)
        self._firstAxisShiftSearchParams.layout().setSpacing(0)
        self._firstAxisGroup.layout().addWidget(self._firstAxisShiftSearchParams)

        # axis 2 params for shift search
        self._secondAxisGroup = qt.QGroupBox(f"axis {second_axis}", self)
        self._secondAxisGroup.setLayout(qt.QVBoxLayout())
        self.layout().addRow(self._secondAxisGroup)
        self._secondAxisShiftSearchParams = StitcherAxisParams(
            axis=second_axis, parent=self
        )
        self._secondAxisShiftSearchParams.layout().setContentsMargins(0, 0, 0, 0)
        self._secondAxisShiftSearchParams.layout().setSpacing(0)
        self._secondAxisGroup.layout().addWidget(self._secondAxisShiftSearchParams)
        # by default avoid doing shift along second axis by default
        self._secondAxisShiftSearchParams.setShiftSearchMethod(
            StitchShiftAlgorithm.NONE
        )

        # frame rescaling option
        self._rescalingWidget = RescalingWidget(parent=self)
        self.layout().addRow(self._rescalingWidget)

        # normalization by sample
        self._normalizationBySampleWidget = NormalizationBySampleGroupBox(parent=self)
        self._normalizationBySampleWidget.setChecked(False)
        self.layout().addRow(self._normalizationBySampleWidget)

        # connect signal / slot
        self._stitchingStrategiesWidget.sigChanged.connect(self._updated)
        self._previewSlices.editingFinished.connect(self._sliceForPreviewHasChanged)
        self._flipLR_CB.toggled.connect(self._flipLRHasChanged)
        self._flipUD_CB.toggled.connect(self._flipUDHasChanged)

    def _sliceForPreviewHasChanged(self):
        slice_for_preview = self.getSlicesForPreview()
        try:
            slice_for_preview = int(slice_for_preview)
        except ValueError:
            pass
        self.sigSliceForPreviewChanged.emit(slice_for_preview)
        self._updated()

    def _flipLRHasChanged(self):
        self.sigFlipLRChanged.emit(self._flipLR_CB.isChecked())

    def _flipUDHasChanged(self):
        self.sigFlipUDChanged.emit(self._flipUD_CB.isChecked())

    def _updated(self, *args, **kwargs):
        self.sigChanged.emit()

    def getSlicesForPreview(self):
        return self._previewSlices.text()

    def getSlices(self):
        slices = self._slices.getSlices()
        if slices == (0, -1, 1):
            return None
        else:
            return (str(slices[0]), str(slices[1]), str(slices[2]))

    def setSlices(self, slices: tuple):
        if isinstance(slices, str):
            slices = slices.replace(" ", "").split(":")
        if len(slices) > 2:
            step = int(slices[2])
        else:
            step = None
        self._slices.setSlices(int(slices[0]), int(slices[1]), step)

    def getAvoidDataDuplication(self) -> bool:
        return (
            self._avoidDataDuplication_CB.isChecked()
            and self._avoidDataDuplication_CB.isEnabled()
        )

    def setAvoidDataDuplication(self, avoid: bool):
        self._avoidDataDuplication_CB.setChecked(avoid)

    def getConfiguration(self) -> dict:
        slices = self.getSlices()
        if slices is None:
            slices = ""
        else:
            slices = ":".join(slices)
        res = {
            stitching_config.STITCHING_SECTION: {
                stitching_config.FLIP_LR: self._flipLR_CB.isChecked(),
                stitching_config.FLIP_UD: self._flipUD_CB.isChecked(),
                stitching_config.ALIGNMENT_AXIS_1_FIELD: self._alignmentGroup.getAlignmentAxis1().value,
                stitching_config.ALIGNMENT_AXIS_2_FIELD: self._alignmentGroup.getAlignmentAxis2().value,
                stitching_config.PAD_MODE_FIELD: self._alignmentGroup.getPadMode(),
                stitching_config.AVOID_DATA_DUPLICATION_FIELD: self.getAvoidDataDuplication(),
            },
            stitching_config.INPUTS_SECTION: {
                stitching_config.STITCHING_SLICES: slices,
            },
            stitching_config.NORMALIZATION_BY_SAMPLE_SECTION: self._normalizationBySampleWidget.getConfiguration(),
        }

        for ddict in (
            self._stitchingStrategiesWidget.getConfiguration(),
            self._firstAxisShiftSearchParams.getConfiguration(),
            self._secondAxisShiftSearchParams.getConfiguration(),
            self._rescalingWidget.getConfiguration(),
        ):
            res = concatenate_dict(res, ddict)
        return res

    def setConfiguration(self, config: dict):
        self._stitchingStrategiesWidget.setConfiguration(config)
        self._firstAxisShiftSearchParams.setConfiguration(config)
        self._secondAxisShiftSearchParams.setConfiguration(config)
        self._rescalingWidget.setConfiguration(config)
        slices = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.STITCHING_SLICES, ""
        )
        # slices
        if slices == "":
            slices = None
        if slices is not None:
            self.setSlices(slices)
        # flip_lr
        flip_lr = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.FLIP_LR, None
        )
        if flip_lr is not None:
            self._flipLR_CB.setChecked(flip_lr in (True, "True", 1, "1"))
        # flip_ud
        flip_ud = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.FLIP_UD, None
        )
        if flip_ud is not None:
            self._flipUD_CB.setChecked(flip_ud in (True, "True", 1, "1"))
        # avoid data duplication
        avoid_data_duplication = config.get(
            stitching_config.AVOID_DATA_DUPLICATION_FIELD, None
        )
        if avoid_data_duplication is not None:
            self.setAvoidDataDuplication(avoid=avoid_data_duplication)
        # alignment
        alignment_axis_1 = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.ALIGNMENT_AXIS_1_FIELD, None
        )
        if alignment_axis_1 is not None:
            self._alignmentGroup.setAlignmentAxis1(alignment_axis_1)
        alignment_axis_2 = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.ALIGNMENT_AXIS_2_FIELD, None
        )
        if alignment_axis_2 is not None:
            self._alignmentGroup.setAlignmentAxis2(alignment_axis_2)
        # pad_mode
        pad_mode = config.get(stitching_config.STITCHING_SECTION, {}).get(
            stitching_config.PAD_MODE_FIELD, None
        )
        if pad_mode is not None:
            self._alignmentGroup.setPadMode(pad_mode=pad_mode)

        # normalization by sample
        normalization_by_sample = config.get(
            stitching_config.NORMALIZATION_BY_SAMPLE_SECTION, None
        )
        if normalization_by_sample is not None:
            self._normalizationBySampleWidget.setConfiguration(normalization_by_sample)

    def _stitchingTypeChanged(self, stitching_type: str):
        stitching_type = StitchingType(stitching_type)
        self._alignmentGroup.setAlignmentAxis1Enabled(
            stitching_type is StitchingType.Z_POSTPROC
        )
        self._avoidDataDuplication_CB.setEnabled(
            stitching_type is StitchingType.Z_POSTPROC
        )

    def setConfigurationLevel(self, level: ConfigurationLevel):
        self._alignmentGroup.setVisible(level >= ConfigurationLevel.ADVANCED)
        self._previewSlices.setVisible(level >= ConfigurationLevel.OPTIONAL)
        self._flipLR_CB.setVisible(level >= ConfigurationLevel.ADVANCED)
        self._flipUD_CB.setVisible(level >= ConfigurationLevel.ADVANCED)
        self._avoidDataDuplication_CB.setVisible(level >= ConfigurationLevel.OPTIONAL)
        self._rescalingWidget.setVisible(level >= ConfigurationLevel.ADVANCED)
        self._firstAxisShiftSearchParams.setConfigurationLevel(level)
        self._secondAxisShiftSearchParams.setConfigurationLevel(level)
        self._normalizationBySampleWidget.setVisible(
            level >= ConfigurationLevel.ADVANCED
        )


class _SlicesSelector(qt.QGroupBox):
    """
    Widget to determine the slices values (to be stitched)
    """

    def __init__(self, parent=None) -> None:
        super().__init__("slices", parent)
        # start interface
        self.setLayout(qt.QHBoxLayout())
        self._startSliceCB = qt.QCheckBox("start", self)
        self.layout().addWidget(self._startSliceCB)
        self._startSliceSB = qt.QSpinBox(self)
        self._startSliceSB.setMinimum(0)
        self._startSliceSB.setMaximum(9999999)
        self._startSliceSB.setValue(0)
        self.layout().addWidget(self._startSliceSB)
        # stop interface
        self._stopSliceCB = qt.QCheckBox("stop", self)
        self.layout().addWidget(self._stopSliceCB)
        self._stopSliceSB = qt.QSpinBox(self)
        self._stopSliceSB.setMinimum(-1)
        self._stopSliceSB.setMaximum(9999999)
        self._stopSliceSB.setValue(-1)
        self.layout().addWidget(self._stopSliceSB)
        # step interface
        self._stepSliceLabel = qt.QLabel("step", self)
        self.layout().addWidget(self._stepSliceLabel)
        self._stepSliceSB = qt.QSpinBox(self)
        self._stepSliceSB.setMinimum(1)
        self._stepSliceSB.setMaximum(9999999)
        self._stepSliceSB.setValue(1)
        self.layout().addWidget(self._stepSliceSB)

        # connect signal / slot
        self._startSliceCB.toggled.connect(self._startSliceSB.setDisabled)
        self._stopSliceCB.toggled.connect(self._stopSliceSB.setDisabled)

        self._startSliceCB.setChecked(True)
        self._stopSliceCB.setChecked(True)

    def getSlices(self) -> tuple:
        if self._startSliceCB.isChecked():
            start = 0
        else:
            start = self._startSliceSB.value()
        if self._stopSliceCB.isChecked():
            stop = -1
        else:
            stop = self._stopSliceSB.value()
        step = self._stepSliceSB.value()
        return (start, stop, step)

    def setSlices(self, start: int, stop: int, step: int | None = None):
        start = int(start)
        stop = int(stop)
        if start == 0:
            self._startSliceCB.setChecked(True)
        else:
            self._startSliceCB.setChecked(False)
            self._startSliceSB.setValue(start)

        if stop == -1:
            self._stopSliceCB.setChecked(True)
        else:
            self._stopSliceCB.setChecked(False)
            self._stopSliceSB.setValue(stop)

        if step is not None:
            self._stepSliceSB.setValue(int(step))


class RescalingWidget(qt.QWidget):
    DEFAULT_MIN_PERCENTILE = 0

    DEFAULT_MAX_PERCENTILE = 100

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.setLayout(qt.QHBoxLayout())
        self._activatedCB = qt.QCheckBox("rescale frames", self)
        self.layout().addWidget(self._activatedCB)

        self._minPercentileQSB = qt.QSpinBox(self)
        self._minPercentileQSB.setRange(0, 100)
        self._minPercentileQSB.setPrefix("min:")
        self._minPercentileQSB.setSuffix("%")
        self._minPercentileQSB.setValue(self.DEFAULT_MIN_PERCENTILE)
        self.layout().addWidget(self._minPercentileQSB)

        self._maxPercentileQSB = qt.QSpinBox(self)
        self._maxPercentileQSB.setRange(0, 100)
        self._maxPercentileQSB.setPrefix("max:")
        self._maxPercentileQSB.setSuffix("%")
        self._maxPercentileQSB.setValue(self.DEFAULT_MAX_PERCENTILE)
        self.layout().addWidget(self._maxPercentileQSB)

        # set up
        self._activatedCB.setChecked(False)
        self._minPercentileQSB.setEnabled(False)
        self._maxPercentileQSB.setEnabled(False)

        # connect signal / slot
        self._activatedCB.toggled.connect(self._activationChanged)
        self._activatedCB.toggled.connect(self._activationChanged)

    def _activationChanged(self):
        self._minPercentileQSB.setEnabled(self._activatedCB.isChecked())
        self._maxPercentileQSB.setEnabled(self._activatedCB.isChecked())

    def getConfiguration(self):
        return {
            STITCHING_SECTION: {
                RESCALE_FRAMES: self._activatedCB.isChecked(),
                RESCALE_PARAMS: ";".join(
                    [
                        f"{KEY_RESCALE_MIN_PERCENTILES}={self._minPercentileQSB.value()}",
                        f"{KEY_RESCALE_MAX_PERCENTILES}={self._maxPercentileQSB.value()}",
                    ]
                ),
            }
        }

    def setConfiguration(self, config: dict):
        def cast_percentile(percentile) -> int:
            if isinstance(percentile, str):
                percentile.replace(" ", "").rstrip("%")
            return int(percentile)

        stitching_config = config.get(STITCHING_SECTION, {})
        rescale_params = str_to_dict(stitching_config.get(RESCALE_PARAMS, {}))
        rescale_min_percentile = rescale_params.get(KEY_RESCALE_MIN_PERCENTILES, None)
        if rescale_min_percentile is not None:
            rescale_min_percentile = cast_percentile(rescale_min_percentile)
            self._minPercentileQSB.setValue(rescale_min_percentile)
        rescale_max_percentile = rescale_params.get(KEY_RESCALE_MAX_PERCENTILES, None)
        if rescale_max_percentile is not None:
            rescale_max_percentile = cast_percentile(rescale_max_percentile)
            self._maxPercentileQSB.setValue(rescale_max_percentile)

        rescale = stitching_config.get(RESCALE_FRAMES, None)
        if rescale is not None:
            self._activatedCB.setChecked(_convert_str_to_bool(rescale))
