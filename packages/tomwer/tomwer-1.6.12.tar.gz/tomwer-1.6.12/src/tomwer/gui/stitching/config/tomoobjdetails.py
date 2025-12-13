from __future__ import annotations

import pint
from nabu.stitching.config import StitchingType
from silx.gui import qt
from silx.gui.utils import blockSignals

from tomoscan.scanbase import TomoScanBase

from tomwer.core.process.stitching.metadataholder import StitchingMetadata
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.stitching.metadataholder import QStitchingMetadata
from tomwer.gui.utils.unitsystem import MetricEntry, PixelEntry

_ureg = pint.get_application_registry()


class _AxisPositionGroup(qt.QGroupBox):
    sigUpdate = qt.Signal()
    """Signal emit when some data have been updated"""

    def __init__(self, axis: int, parent=None):
        assert axis in (0, 1, 2)
        super().__init__(title=f"axis {axis}", parent=parent)
        self.__axis = axis
        self._stitching_metadata = None

        self.setLayout(qt.QGridLayout())

        # pixel size
        self._pixelSizeRaw = MetricEntry(
            value="unknown",
            name="pixel size",
            parent=self,
            default_unit=_ureg.millimeter,
        )
        self._pixelSizeRaw.setReadOnly(True)
        self.layout().addWidget(self._pixelSizeRaw, 0, 0, 1, 2)
        self._overridePixelSizeCB = qt.QCheckBox("overwrite", self)
        self.layout().addWidget(self._overridePixelSizeCB, 0, 2, 1, 1)
        self._pixelSizeOverride = MetricEntry(
            name="", parent=self, default_unit=_ureg.millimeter
        )
        self.layout().addWidget(self._pixelSizeOverride, 0, 3, 1, 2)

        # raw position (in meter or millimeter)
        self._rawPositionMetric = MetricEntry(
            value="unknown",
            name=f"axis {axis} position (metric unit)",
            parent=self,
            default_unit=_ureg.millimeter,
        )
        self._rawPositionMetric.setReadOnly(True)
        self.layout().addWidget(self._rawPositionMetric, 1, 0, 1, 2)
        self._overrideMetricPositionCB = qt.QCheckBox("overwrite", self)
        self.layout().addWidget(self._overrideMetricPositionCB, 1, 2, 1, 1)
        self._metricPositionOverride = MetricEntry(
            name="", parent=self, default_unit=_ureg.millimeter
        )
        self.layout().addWidget(self._metricPositionOverride, 1, 3, 1, 2)

        # raw position in pixel ...
        self._rawPxPosition = PixelEntry(name=f"axis {axis} position (pixel unit)")
        self._rawPxPosition.setReadOnly(True)
        self.layout().addWidget(self._rawPxPosition, 2, 0, 1, 2)
        self._overridePixelPositionCB = qt.QCheckBox("overwrite", self)
        self.layout().addWidget(self._overridePixelPositionCB, 2, 2, 1, 1)
        self._overridePxPosition = PixelEntry(
            name="",
            parent=self,
        )
        self.layout().addWidget(self._overridePxPosition, 2, 3, 1, 2)

        # utils to filter signals
        self._editingWidgets = (
            self._pixelSizeRaw,
            self._pixelSizeOverride,
            self._overridePixelPositionCB,
            self._overridePixelSizeCB,
            self._overrideMetricPositionCB,
            self._metricPositionOverride,
            self._rawPositionMetric,
            self._rawPxPosition,
            self._overridePxPosition,
        )

        # set up
        self._metricPositionOverride.setVisible(False)
        self._overridePxPosition.setVisible(False)
        self._pixelSizeOverride.setVisible(False)

        # connect signal / slot
        self._overrideMetricPositionCB.toggled.connect(
            self._metricPositionOverride.setVisible
        )
        self._overridePixelPositionCB.toggled.connect(
            self._overridePxPosition.setVisible
        )
        self._overridePixelSizeCB.toggled.connect(self._pixelSizeOverride.setVisible)

        self._overrideMetricPositionCB.toggled.connect(self._changed)
        self._overridePixelPositionCB.toggled.connect(self._changed)
        self._overridePixelSizeCB.toggled.connect(self._changed)
        self._metricPositionOverride.valueChanged.connect(self._changed)
        self._overridePxPosition.valueChanged.connect(self._changed)
        self._pixelSizeOverride.valueChanged.connect(self._changed)

    def _changed(self, *args, **kwargs):
        self._updateFinalPxPosition()
        self._updateTomoObjMetadata()

    def _updateTomoObjMetadata(self):
        # update the tomo obj metadata
        if self._stitching_metadata is not None:
            # disconnect the metadata signal to avoid sending several update message
            self._stitching_metadata.sigChanged.disconnect(self._loadMetadata)
            with blockSignals(self._stitching_metadata):
                self._stitching_metadata.setPixelOrVoxelSize(
                    value=self.getOverrridePixelSize(), axis=self.axis
                )
                metric_quantity = self.getOverrrideMetricPosition()
                if isinstance(metric_quantity, pint.Quantity):
                    metric_quantity = metric_quantity.to_base_units().magnitude
                self._stitching_metadata.setMetricPos(metric_quantity, axis=self.axis)
                self._stitching_metadata.setPxPos(
                    self.getOverrridePxPosition(), axis=self.axis
                )
            # make sure the signal of the tomo obj has been send (but this widget is not interested because
            # we did the update according to the widget.)
            self._stitching_metadata.sigChanged.emit()
            self._stitching_metadata.sigChanged.connect(self._loadMetadata)

    def _updateFinalPxPosition(self):
        # compute the final position
        if self._overridePixelPositionCB.isChecked():
            # if the pixel size is directly edited then ignore this one
            return None
        pixel_size_m = self.get_final_pixel_size()
        if pixel_size_m is None:
            return None

        position_m = self.get_final_metric_position()
        if position_m is None:
            return None
        position_px = int(position_m / pixel_size_m)
        self._rawPxPosition.setValue(position_px)

    @property
    def axis(self) -> int:
        return self.__axis

    def get_final_metric_position(self):
        """
        return the metric position to be used to compute the final pixel position
        """
        if self._overrideMetricPositionCB.isChecked():
            return self._metricPositionOverride.getValue()
        else:
            return self._overridePxPosition.getValue()

    def get_final_px_position(self):
        """
        return the pixel position to be used for stitching
        """
        if self._overridePixelPositionCB.isChecked():
            return self.getOverrridePxPosition()
        else:
            return self.getRawPxPosition()

    def get_final_pixel_size(self):
        if self._overridePixelPositionCB.isChecked():
            return self._pixelSizeOverride.getValue()
        else:
            return self._pixelSizeRaw.getValue()

    def setStitchingMetadata(self, stitching_metadata: QStitchingMetadata | None):
        """
        load used metadata from tomo_obj
        """
        if self._stitching_metadata is not None:
            self._stitching_metadata.sigChanged.disconnect(self._loadMetadata)
        # remove metadata because we are no more editing those
        self._stitching_metadata = None
        self.reset()
        self._stitching_metadata = stitching_metadata
        if self._stitching_metadata is not None:
            self._stitching_metadata.sigChanged.connect(self._loadMetadata)
            self._loadMetadata()

    def _loadMetadata(self):
        stitching_metadata = self._stitching_metadata
        tomo_obj = self._stitching_metadata.tomo_obj
        assert stitching_metadata is not None, "expects to have metadata"

        if isinstance(tomo_obj, TomoScanBase):
            # tODO: block all editor signal
            with blockSignals(*self._editingWidgets):
                # handle pixel size
                if self.axis == 0:
                    pixel_size = tomo_obj.sample_y_pixel_size
                else:
                    pixel_size = tomo_obj.sample_x_pixel_size
                if pixel_size is not None:
                    self.setRawPixelSize(pixel_size)
                override_pixel_size = stitching_metadata._pixel_or_voxel_size[self.axis]
                self._overridePixelSizeCB.setChecked(override_pixel_size is not None)
                if override_pixel_size is not None:
                    self.setOverrridePixelSize(override_pixel_size)
                # handle position in metric unit
                try:
                    raw_position_m = stitching_metadata.get_raw_position_m(
                        axis=self.axis
                    )
                except Exception:
                    raw_position_m = None
                if raw_position_m is not None:
                    self.setRawMetricPosition(position_m=raw_position_m)
                override_position_m = stitching_metadata._pos_as_m[self.axis]
                self._overrideMetricPositionCB.setChecked(
                    override_position_m is not None
                )
                if override_position_m is not None:
                    self.setOverrrideMetricPosition(position_m=override_position_m)

                # handle position in pixel
                l_pixel_size = override_pixel_size or pixel_size
                if raw_position_m is not None:
                    self.setRawPxPosition(int(raw_position_m / l_pixel_size))
                override_position_px = stitching_metadata._pos_as_px[self.axis]
                self._overridePixelPositionCB.setChecked(
                    override_position_px is not None
                )
                if override_position_px is not None:
                    self.setOverrridePxPosition(override_position_px)
        else:
            raise NotImplementedError(
                "loading volume metadata not handled for the moment"
            )

    def reset(self):
        self._rawPositionMetric.setValue("unknown")
        self._overrideMetricPositionCB.setChecked(False)
        self._rawPxPosition.setValue("unknown")
        self._overrideMetricPositionCB.setChecked(False)
        self._pixelSizeRaw.setValue("unknown")
        self._overridePixelSizeCB.setChecked(False)

    def getRawPxPosition(self):
        return self._rawPxPosition.getValue()

    def setRawPxPosition(self, position_px):
        self._rawPxPosition.setValue(position_px)

    def getOverrridePxPosition(self):
        if self._overridePixelPositionCB.isChecked():
            return self._overridePxPosition.getValue()
        else:
            return None

    def setOverrridePxPosition(self, position_px):
        if not self._overridePixelPositionCB.isChecked():
            with block_signals(self._overridePixelPositionCB):
                # avoid updating twice the stitching metadata value
                self._overridePixelPositionCB.setChecked(True)
        self._overridePxPosition.setValue(position_px)
        self._overridePxPosition.valueChanged.emit()

    def getOverrrideMetricPosition(self) -> pint.Quantity:
        if self._overrideMetricPositionCB.isChecked():
            return self._metricPositionOverride.getValue()
        else:
            return None

    def setOverrrideMetricPosition(self, position_m):
        if not self._overrideMetricPositionCB.isChecked():
            with block_signals(self._overrideMetricPositionCB):
                # avoid updating twice the stitching metadata value
                self._overrideMetricPositionCB.setChecked(True)
        self._metricPositionOverride.setValue(position_m)
        self._metricPositionOverride.valueChanged.emit()

    def getRawMetricPosition(self):
        return self._rawPositionMetric.getValue()

    def setRawMetricPosition(self, position_m, displayed_unit=_ureg.millimeter):
        self._rawPositionMetric.setValue(
            value_m=position_m, displayed_unit=displayed_unit
        )

    def getRawPixelSize(self):
        return self._pixelSizeRaw.getValue()

    def setRawPixelSize(self, pixel_size):
        self._pixelSizeRaw.setValue(pixel_size)

    def getOverrridePixelSize(self):
        if self._overridePixelSizeCB.isChecked():
            return self._pixelSizeOverride.getValue()
        else:
            return None

    def setOverrridePixelSize(self, pixel_size):
        if not self._overridePixelSizeCB.isChecked():
            with block_signals(self._overridePixelSizeCB):
                # avoid updating twice the stitching metadata value
                self._overridePixelSizeCB.setChecked(True)
        self._pixelSizeOverride.setValue(pixel_size)
        self._pixelSizeOverride.valueChanged.emit()


class TomoObjectPositionInfos(qt.QWidget):
    """
    Widget to define the TomoObject (scan or volume) position
    """

    def __init__(self, parent=None, stitching_metadata: StitchingMetadata = None):
        super().__init__(parent=parent)
        self._stitching_metadata = None
        self.setLayout(qt.QGridLayout())

        # axis 0 group
        self._axis_0_pos = _AxisPositionGroup(axis=0, parent=self)
        self.layout().addWidget(self._axis_0_pos, 1, 0, 1, 5)
        # axis 2 group
        self._axis_2_pos = _AxisPositionGroup(axis=2, parent=self)
        self.layout().addWidget(self._axis_2_pos, 2, 0, 1, 5)
        # spacer for style
        self._spacer = qt.QWidget(parent=self)
        self._spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self._spacer, 99, 99, 1, 1)

        # set up
        self.setStitchingMetadata(stitching_metadata)

    def getStitchingMetadata(self):
        return self._stitching_metadata

    def reset(self):
        self._axis_0_pos.reset()
        self._axis_2_pos.reset()

    def clean(self):
        self.reset()
        self._stitching_metadata = None

    def setStitchingMetadata(self, stitching_metadata: StitchingMetadata | None = None):
        if stitching_metadata is not None and not isinstance(
            stitching_metadata, StitchingMetadata
        ):
            raise TypeError(
                "stitching_metadata is expected to be an instance of {StitchingMetadata}"
            )
        else:
            self._stitching_metadata = stitching_metadata
            self._loadMetadata(stitching_metadata)

    def _loadMetadata(self, metadata: StitchingMetadata):
        self._axis_0_pos.setStitchingMetadata(metadata)
        self._axis_2_pos.setStitchingMetadata(metadata)

    def updateStitchingType(self, stitching_type: StitchingType):
        stitching_type = StitchingType(stitching_type)
        if stitching_type is StitchingType.Z_POSTPROC:
            pixel_or_voxel_label = "voxel size"
        elif stitching_type is StitchingType.Z_PREPROC:
            pixel_or_voxel_label = "pixel size"
        else:
            raise NotImplementedError
        self._axis_0_pos._pixelSizeRaw.setLabelText(pixel_or_voxel_label)
