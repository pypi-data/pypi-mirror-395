from __future__ import annotations

import logging

from nabu.stitching.config import StitchingType
from nabu.stitching.config import identifiers_as_str_to_instances

from nxtomomill.models.utils import convert_str_to_tuple as _convert_str_to_tuple
from silx.gui import qt
from tomoscan.series import Series
from tomoscan.scanbase import TomoScanBase as _TomoScanBase
from tomoscan.volumebase import VolumeBase as _VolumeBase

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.tomwer_object import TomwerObject
from tomwer.gui.stitching.stitching_preview import PreviewStitchingPlot
from tomwer.gui.stitching.stitching_raw import RawStitchingPlot
from tomwer.gui.stitching.axisorderedlist import EditableOrderedTomoObjWidget
from .singleaxis import _SingleAxisMixIn

_logger = logging.getLogger(__name__)


def convert_str_to_tuple(input_str, none_if_empty):
    if input_str is None:
        return None
    elif isinstance(input_str, (tuple, list)):
        return tuple(input_str)
    else:
        return _convert_str_to_tuple(input_str=input_str, none_if_empty=none_if_empty)


class SingleAxisStitchingWidget(qt.QWidget, _SingleAxisMixIn):
    """
    Main widget for (single axis) stitching. It contains display and options definition.
    """

    sigStitchingTypeChanged = qt.Signal(str)
    """emit when stitching type changes"""
    sigTomoObjsLoaded = qt.Signal(tuple)
    """Signal emit when during setting a configuration this trigger some addition of tomo object"""

    def __init__(self, axis: int, parent=None) -> None:
        super().__init__(parent)
        assert axis in (0, 1, 2)
        self._axis = axis  # used from _SingleAxisMixIn interface
        self.setLayout(qt.QGridLayout())

        self._stitchingTypeCB = qt.QComboBox(parent=self)

        # filter stitching types that does belong to the axis (GUI is specific to a given axis. The other have no sense at this level)
        stitching_types = filter(
            lambda s_type: s_type.lower().startswith(self.axis_alias(axis).lower()),
            [item.value for item in StitchingType],
        )
        for mode in stitching_types:
            self._stitchingTypeCB.addItem(mode)
        self._stitchingTypeCB.currentIndexChanged.connect(self._stitchingTypeChanged)
        self.layout().addWidget(qt.QLabel("stitching method:"), 0, 0, 1, 1)
        self.layout().addWidget(self._stitchingTypeCB, 0, 1, 1, 1)

        self._mainWidget = _SingleAxisStitchingCentralTabWidget(parent=self, axis=axis)
        self.layout().addWidget(self._mainWidget, 1, 0, 4, 4)

        # set up
        self.setStitchingType(self.getStitchingType())
        self._mainWidget.setCurrentWidget(self._mainWidget._previewPlot)

        # connect signal / slot
        self._stitchingTypeCB.currentIndexChanged.connect(self._stitchingTypeChanged)

    def close(self):
        self._mainWidget.close()
        # requested for the waiting plot update
        super().close()

    def clean(self):
        self._mainWidget.clean()

    def _stitchingTypeChanged(self, *args, **kwargs):
        self.sigStitchingTypeChanged.emit(self.getStitchingType().value)

    def getStitchingType(self):
        return StitchingType(self._stitchingTypeCB.currentText())

    def setStitchingType(self, mode):
        mode = StitchingType(mode)
        idx = self._stitchingTypeCB.findText(mode.value)
        if idx >= 0:
            self._stitchingTypeCB.setCurrentIndex(idx)

    def get_available_pre_processing_stitching_mode(self):
        pre_proc_modes: tuple[str] = tuple(
            filter(
                lambda mode: "preproc" in mode,
                [
                    self._stitchingTypeCB.itemText(i_item)
                    for i_item in range(self._stitchingTypeCB.count())
                ],
            )
        )
        return tuple([StitchingType(mode) for mode in pre_proc_modes])

    def get_available_post_processing_stitching_mode(self):
        post_proc_modes: tuple[str] = tuple(
            filter(
                lambda mode: "postproc" in mode,
                [
                    self._stitchingTypeCB.itemText(i_item)
                    for i_item in range(self._stitchingTypeCB.count())
                ],
            )
        )
        return tuple([StitchingType(mode) for mode in post_proc_modes])

    def addTomoObj(self, tomo_obj: TomwerObject):
        self._mainWidget.addTomoObj(tomo_obj)
        self._updatePreviewPixelSize()

    def getTomoObjs(self) -> tuple:
        return self._mainWidget.getTomoObjs()

    def removeTomoObj(self, tomo_obj: TomwerObject):
        self._mainWidget.removeTomoObj(tomo_obj)
        self._updatePreviewPixelSize()

    def _updatePreviewPixelSize(self):
        """update the pixel size of the preview from existing tomo obj"""

        def get_pixel_size():
            tomo_objs = self._mainWidget.getTomoObjs()
            for tomo_obj in tomo_objs:
                if (
                    isinstance(tomo_obj, NXtomoScan)
                    and tomo_obj.sample_x_pixel_size is not None
                    and tomo_obj.sample_y_pixel_size is not None
                ):
                    return tomo_obj.sample_x_pixel_size, tomo_obj.sample_y_pixel_size
                elif (
                    isinstance(tomo_obj, TomwerVolumeBase)
                    and tomo_obj.voxel_size is not None
                ):
                    # warning: axis are inverted between the volume and the voxel_size. voxel_size are given as (x, y, z) instead of (z, y, x)
                    return (
                        tomo_obj.voxel_size[2 - self.first_axis],
                        tomo_obj.voxel_size[2 - self.first_axis],
                    )
            return None, None

        pixel_size = get_pixel_size()
        self._mainWidget._previewPlot.setPixelSize(pixel_size_m=pixel_size)

    def getConfiguration(self) -> dict:
        # missing parameters:
        # * overwrite
        # * slices
        # * slurm stuff...

        tomo_objs = self._mainWidget.getTomoObjs()

        def filter_empty_list_and_cast_as_int(elmts):
            new_list = [int(elmt) for elmt in elmts if elmt is not None]
            if len(new_list) == 0:
                return None
            else:
                return elmts

        first_axis_pos_px = filter_empty_list_and_cast_as_int(
            [
                obj.stitching_metadata.get_abs_position_px(axis=self.first_axis) or 0
                for obj in tomo_objs
            ]
        )
        second_axis_pos_px = filter_empty_list_and_cast_as_int(
            [
                obj.stitching_metadata.get_abs_position_px(axis=self.second_axis) or 0
                for obj in tomo_objs
            ]
        )
        return {
            "stitching": {
                "type": self.getStitchingType().value,
                f"axis_{self.first_axis}_pos_px": (
                    "" if first_axis_pos_px is None else first_axis_pos_px
                ),
                f"axis_{self.second_axis}_pos_px": (
                    "" if second_axis_pos_px is None else second_axis_pos_px
                ),
            },
            "inputs": {
                "input_datasets": [obj.get_identifier().to_str() for obj in tomo_objs],
            },
        }

    def setConfiguration(self, config: dict) -> None:
        stitching_type = config.get("stitching", {}).get("type", None)
        if stitching_type is not None:
            self.setStitchingType(stitching_type)
        tomo_obj_ids = config.get("inputs", {}).get("input_datasets", None)
        tomo_obj_ids = identifiers_as_str_to_instances(tomo_obj_ids)
        first_axis_pos = convert_str_to_tuple(
            config.get("stitching", {}).get(f"axis_{self.first_axis}_pos_px", None),
            none_if_empty=True,
        )
        second_axis_pos = convert_str_to_tuple(
            config.get("stitching", {}).get(f"axis_{self.second_axis}_pos_px", None),
            none_if_empty=True,
        )
        if tomo_obj_ids is not None:
            self._mainWidget.clearTomoObjs()
            if first_axis_pos is None:
                first_axis_pos = [None] * len(tomo_obj_ids)
            if second_axis_pos is None:
                second_axis_pos = [None] * len(tomo_obj_ids)
            if len(first_axis_pos) != len(tomo_obj_ids):
                _logger.error(
                    f"incoherent axis {self.first_axis} position compared to the number of input datasets. Will ignore those"
                )
                first_axis_pos = [None] * len(tomo_obj_ids)
            if len(second_axis_pos) != len(tomo_obj_ids):
                _logger.error(
                    f"incoherent axis {self.second_axis} position compared to the number of input datasets. Will ignore those"
                )
                second_axis_pos = [None] * len(tomo_obj_ids)

            new_tomo_objs = []
            for tomo_obj_id, first_axis_v, second_axis_v in zip(
                tomo_obj_ids, first_axis_pos, second_axis_pos
            ):
                if isinstance(tomo_obj_id, TomwerObject):
                    tomo_obj = tomo_obj_id
                elif isinstance(tomo_obj_id, _TomoScanBase):
                    # for now we need to convert it back because object are not the same
                    tomo_obj = ScanFactory.create_tomo_object_from_identifier(
                        tomo_obj_id.get_identifier().to_str()
                    )
                elif isinstance(tomo_obj_id, _VolumeBase):
                    tomo_obj = VolumeFactory.create_tomo_object_from_identifier(
                        tomo_obj_id.get_identifier().to_str()
                    )
                else:
                    tomo_obj = ScanFactory.create_tomo_object_from_identifier(
                        tomo_obj_id
                    )
                self.addTomoObj(tomo_obj=tomo_obj)
                # set metadata information if any
                for axis, axis_value in zip((0, 1), (first_axis_v, second_axis_v)):
                    if axis_value is not None:
                        tomo_obj.stitching_metadata.setPxPos(int(axis_value), axis=axis)
                new_tomo_objs.append(tomo_obj)
            self.sigTomoObjsLoaded.emit(tuple(new_tomo_objs))
            self._mainWidget._axisOrderedList._orderMightHaveChanged()

    # expose API
    def setAddTomoObjCallbacks(self, *args, **kwargs):
        self._mainWidget.setAddTomoObjCallbacks(*args, **kwargs)

    def setRemoveTomoObjCallbacks(self, *args, **kwargs):
        self._mainWidget.setRemoveTomoObjCallbacks(*args, **kwargs)


class _SingleAxisStitchingCentralTabWidget(qt.QTabWidget):
    """
    Tab widget containing:
    * preview interface of the stitching
    * ordered list of the scan / volume position over the main stitching axis
    """

    def __init__(self, axis: int, parent=None) -> None:
        super().__init__(parent)
        assert axis in (0, 1, 2)
        self._seriesName = None
        self._axisOrderedList = EditableOrderedTomoObjWidget(parent=self, axis=axis)
        self.addTab(self._axisOrderedList, f"axis {axis} ordered list")
        self._previewPlot = PreviewStitchingPlot(parent=self, axis=axis)
        self.addTab(self._previewPlot, "stitching preview")
        # TODO: add a raw display to print frame from raw position z positions ...
        self._rawDisplayPlot = RawStitchingPlot(
            parent=self,
            aspectRatio=True,
            logScale=False,
            copy=False,
            save=False,
            print_=False,
            grid=False,
            curveStyle=False,
            mask=False,
            alpha_values=True,
        )
        self._rawDisplayPlot.setKeepDataAspectRatio(True)
        self._rawDisplayPlot.setAxesDisplayed(False)
        self.addTab(self._rawDisplayPlot, "raw display")
        # add an option to activate / deactivate auto update of the raw display as it can be time consuming.
        raw_display_idx = self.indexOf(self._rawDisplayPlot)
        self._rawDisplayCB = qt.QCheckBox(self)
        self.tabBar().setTabButton(
            raw_display_idx,
            qt.QTabBar.LeftSide,
            self._rawDisplayCB,
        )
        self.setTabToolTip(
            raw_display_idx,
            "If toggled will keep the raw display up to date from axis 0 modifications",
        )
        # set up: turn overlay one by default
        self._previewPlot._backGroundAction.setChecked(True)

    def _handleRawDisplayConnection(self, toggled: bool):
        if toggled:
            self._connectRawDisplayConnection()
        else:
            self._disconnectRawDisplayConnection()

    def setSeries(self, series: Series):
        for elmt in series:
            self._axisOrderedList.addTomoObj(elmt)
        self.setSeriesName(series.name)

    def addTomoObj(self, tomo_obj: TomwerObject):
        self._axisOrderedList.addTomoObj(tomo_obj)

    def removeTomoObj(self, tomo_obj: TomwerObject):
        self._axisOrderedList.removeTomoObj(tomo_obj=tomo_obj)

    def getSeriesName(self) -> str:
        return self._seriesName

    def setSeriesName(self, name: str):
        self._seriesName = name

    def getTomoObjs(self) -> tuple:
        return self._axisOrderedList.getTomoObjsAxisOrdered()

    def clearTomoObjs(self):
        self._axisOrderedList.clearTomoObjs()

    def clean(self) -> None:
        self.clearTomoObjs()
        self._previewPlot.clear()

    def close(self):
        self._previewPlot.close()
        # requested for the waiting plot update
        super().close()

    def setAddTomoObjCallbacks(self, *args, **kwargs):
        self._axisOrderedList.setAddTomoObjCallbacks(*args, **kwargs)

    def setRemoveTomoObjCallbacks(self, *args, **kwargs):
        self._axisOrderedList.setRemoveTomoObjCallbacks(*args, **kwargs)
