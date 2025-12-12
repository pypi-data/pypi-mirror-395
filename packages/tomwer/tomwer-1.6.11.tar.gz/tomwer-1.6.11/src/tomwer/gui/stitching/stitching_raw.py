from __future__ import annotations

import logging
import weakref
import numpy
from typing import Any
from contextlib import AbstractContextManager

from silx.gui import qt
from silx.gui.plot import PlotWindow
from nxtomo.nxobject.nxdetector import ImageKey
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.tomwer_object import TomwerObject
from tomwer.gui.stitching.metadataholder import QStitchingMetadata
from tomwer.gui import icons as tomwer_icons

_logger = logging.getLogger(__name__)


class RawStitchingPlot(PlotWindow):
    """
    Plot displaying the different TomwerObject (volume or scan) at the specify position.
    This widget is used to help users find initial positions for stitching over anspecific axis.

    It will display a single slice or projection.

    The design is that it will keep up to date with TomwerObject if the widget is "active".
    Else it will wait for either a manual update (calling updateImages) or to be activated.

    tomo objects are weakref and stitching metadata will always be connected. But ignore if not activated.
    Activation mecanism is here because this can be memory consuming and we want by default to avoid this mecanism

    Warning: for now the interface expects to have frames homogeneous space. So if a scan / volume gets invertions (y downward)... we expect all
    scans / volumes to have the same. This is the same at nabu level.
    """

    class ActivateContext(AbstractContextManager):
        """
        simple context to turn off : turn on image update
        """

        def __init__(self, rawStitchingPlot, activate) -> None:
            super().__init__()
            self._rawStitchingPlot = rawStitchingPlot
            self._activate = activate

        def __enter__(self) -> Any:
            self._activateStatus = self._rawStitchingPlot.isActive()
            self._rawStitchingPlot.setActive(self._activate)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._rawStitchingPlot.setActive(self._activateStatus)

    def __init__(self, parent=None, alpha_values=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._activated = True
        self._tomo_objs = dict({})
        self._slice_for_preview = "middle"
        self._scan_reading_order = {}
        # for each scan store if the rotation angles are store in increasing order or decreasing.
        # this way we can try to know if the order is inverted between different scans.
        self._flipudFrames = False
        # should we flip up / down frame (once management of metadata is done). For scan we can get fliplr and flip ud information already
        # but not for volumes
        self._fliplrFrames = False
        self._firstDisplay = True
        # bool to know if we are currently displaying the BW mode
        self._blackAndWhiteCompositeMode = False
        # result of the B&W composite mode
        self._BWImage = None
        self._compositeOffset = None, None

        # add alpha values widget
        if alpha_values:
            self._alphaValuesWidget = AlphaValuesTableWidget(self, plot=self)
            self._alphaValuesWidgetDockWidget = qt.QDockWidget(self)
            self._alphaValuesWidgetDockWidget.setWidget(self._alphaValuesWidget)
            self.addDockWidget(
                qt.Qt.BottomDockWidgetArea, self._alphaValuesWidgetDockWidget
            )
        else:
            self._alphaValuesWidget = None

        # composite  B&W mode
        self._modeToolbar = qt.QToolBar("display mode", self)

        icon = tomwer_icons.getQIcon("compare_mode_a_minus_b")
        self._substractAction = qt.QAction(icon, "Subtract in BW mode", self)
        self._substractAction.setCheckable(True)
        self._substractAction.setChecked(False)
        self._substractAction.toggled.connect(self.__displayModeChanged)
        self._modeToolbar.addAction(self._substractAction)
        self._modeToolbar.setVisible(
            False
        )  # for now this mode is a proto. Complex to do to keep some performances.

        self.addToolBar(self._modeToolbar)

    def __displayModeChanged(self):
        self._blackAndWhiteCompositeMode = self._substractAction.isChecked()
        self._updateImages()

    def setFlipLRFrames(self, flip: bool) -> None:
        if flip != self._fliplrFrames:
            self._fliplrFrames = flip
            self._updateImages()

    def setFlipUDFrames(self, flip: bool):
        if flip != self._flipudFrames:
            self._flipudFrames = flip
            self._updateImages()

    def setSliceForPreview(self, slice_for_preview: str | int):
        if self._slice_for_preview != slice_for_preview:
            self._slice_for_preview = slice_for_preview
            self._updateImages()

    def setActive(self, active: bool):
        if active == self._activated:
            # avoid any update if not necessary
            return
        self._activated = active
        if active:
            # if has been activated update plot to be up to date
            self._updateImages()

    def isActive(self) -> bool:
        return self._activated

    @staticmethod
    def getMinAxisPosition(tomo_obj: TomwerObject | None, axis):
        if tomo_obj is None or tomo_obj.stitching_metadata is None:
            return 0
        else:
            return tomo_obj.stitching_metadata.get_abs_position_px(axis=axis) or 0

    @staticmethod
    def getRotationAngleDirection(scan: TomwerScanBase):
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"scan is expected to be an instance of {TomwerScanBase} instead of {type(scan)}"
            )

        rotation_angle_ref = numpy.array(scan.rotation_angle)
        return rotation_angle_ref[
            numpy.asarray(scan.image_key_control) == ImageKey.PROJECTION.value
        ]

    def addTomoObj(self, tomo_obj: TomwerObject):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"tomo_obj is expected to be an instance of {TomwerObject}. {type(tomo_obj)} provided"
            )
        elif tomo_obj.stitching_metadata is None:
            raise ValueError(
                "tomo obj is expected to have a stitching_metadata defined yet"
            )

        if len(self._tomo_objs) > 0:
            first_tomo_obj_id = tuple(self._tomo_objs.keys())[0]
            first_tomo_obj = self._tomo_objs[first_tomo_obj_id]()
        else:
            first_tomo_obj_id = None
            first_tomo_obj = None

        if not isinstance(first_tomo_obj, (TomwerScanBase, type(None))) and isinstance(
            tomo_obj, TomwerScanBase
        ):
            # We cannot display both scan and volumes. Especially because we need to define reading order for scan
            # and we need to keep a reference for scans (first one over the stitching axis)
            _logger.error(
                f"get instances of both {TomwerScanBase} and {TomwerVolumeBase}. Case not handled. Skip it"
            )
            return

        self._tomo_objs[tomo_obj.get_identifier().to_str()] = weakref.ref(tomo_obj)
        if isinstance(tomo_obj.stitching_metadata, QStitchingMetadata):
            tomo_obj.stitching_metadata.sigChanged.connect(
                self._tomoObjMetadataHasChanged
            )

        # reorder tomo_objs to keep it axis 0 ordered
        self._tomo_objs = dict(
            sorted(
                self._tomo_objs.items(),
                key=lambda item: self.getMinAxisPosition(item[1](), axis=0),
                reverse=True,  # scan are expected to be orderred alonx axis 0 and decreasing
            )
        )

        self._alphaValuesWidget.addTomoObj(tomo_obj)
        if isinstance(tomo_obj, TomwerScanBase):
            self._scan_reading_order[tomo_obj.get_identifier().to_str()] = (
                self.getRotationAngleDirection(tomo_obj)
            )
            if first_tomo_obj_id != tuple(self._tomo_objs.keys())[0]:
                # if the order of scans might have change we need to update the full stack (to handle reading order)
                self._updateImages()
                return

        self._updateImage(tomo_obj)

    def _tomoObjMetadataHasChanged(self, *args, **kwargs):
        sender = self.sender()
        if not isinstance(sender, QStitchingMetadata):
            _logger.error(
                "_tomoObjMetadataHasChanged is expected to be conencted with QStitchingMetadata only"
            )
        else:
            tomo_obj = sender.tomo_obj
            if tomo_obj is not None:
                self._updateImage(tomo_obj=tomo_obj)

    def removeTomoObj(self, tomo_obj: TomwerObject):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"tomo_obj is expected to be an instance of {TomwerObject}. {type(tomo_obj)} provided"
            )

        self._tomo_objs.pop(tomo_obj.get_identifier().to_str(), None)
        self._scan_reading_order.pop(tomo_obj.get_identifier().to_str(), None)

        # reorder tomo_objs to keep it axis 0 ordered
        self._tomo_objs = dict(
            sorted(
                self._tomo_objs.items(),
                key=lambda item: self.getMinAxisPosition(item[1](), axis=0),
                reverse=True,
            )
        )
        if len(self._tomo_objs) > 0:
            first_tomo_obj_id = tuple(self._tomo_objs.keys())[0]
            first_tomo_obj = self._tomo_objs[first_tomo_obj_id]()
        else:
            first_tomo_obj_id = None
            first_tomo_obj = None

        if first_tomo_obj is tomo_obj and isinstance(first_tomo_obj, TomwerScanBase):
            # if a scan has been added and if he is the first one over the axis. Then the reading order was the 'ref order'
            # and we need to update all images
            self._updateImages()
        else:
            # else we can simple remove the image it will not affect others
            self.removeImage(tomo_obj.get_identifier().to_str())

    def _updateImage(self, tomo_obj: TomwerObject, recompute_composite=True):
        if not self._activated:
            return

        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"tomo_obj is expected to be an instance of {TomwerObject}. {type(tomo_obj)} provided"
            )

        if recompute_composite:
            self._recomputeBlackAndWhiteCompositeImage()

        frame = self.getFrame(tomo_obj=tomo_obj)

        if frame is None:
            return
        frame_origin = (
            tomo_obj.stitching_metadata.get_abs_position_px(axis=2) or 0,
            tomo_obj.stitching_metadata.get_abs_position_px(axis=0) or 0,
        )
        # replace frame by the composite if needed
        if self._blackAndWhiteCompositeMode:
            frame = self._BWImage[
                self._compositeOffset[0] + frame_origin[1] : frame.shape[0],
                self._compositeOffset[1] + frame_origin[0] : frame.shape[1],
            ]

        identifier = tomo_obj.get_identifier().to_str()
        self.addImage(
            data=frame[
                ::-1
            ],  # for coherence with axis and keep frame ordered we need to invert this one
            legend=identifier,
            origin=frame_origin,
            resetzoom=self._firstDisplay,
        )
        self._firstDisplay = False
        img = self.getImage(identifier)
        img.setAlpha(0.5)  # TODO: look to be able to tune this value from interface...

    def clearTomoObjs(self):
        tomo_objs = tuple(self._tomo_objs.values())
        for tomo_obj in tomo_objs:
            self.removeTomoObj(tomo_obj())
        self._alphaValuesWidget.clearTomoObjs()

    def setTomoObjs(self, tomo_objs):
        self.clearTomoObjs()
        # avoid to update images each time
        with RawStitchingPlot.ActivateContext(self, activate=False):
            for tomo_obj in tomo_objs:
                self.addTomoObj(tomo_obj=tomo_obj)
        self._alphaValuesWidget.setTomoObjs(tomo_objs)
        self._updateImages()

    def _getReadingOrderRef(self):
        return self._scan_reading_order[tuple(self._tomo_objs.keys())[0]]

    def getFrame(self, tomo_obj):
        if isinstance(tomo_obj, TomwerVolumeBase):
            try:
                frame = tomo_obj.get_slice(index=self._slice_for_preview, axis=1)
            except IndexError:
                _logger.error(
                    f"requested slice doesn't exist (index=={self._slice_for_preview}, axis==1)"
                )
                return None

            if self._flipudFrames:
                frame = numpy.flipud(frame)
            if self._fliplrFrames:
                frame = numpy.fliplr(frame)
            return frame

        elif isinstance(tomo_obj, TomwerScanBase):
            scan = tomo_obj

            # compute flat field
            # TODO: this must be done in another thread... but sync with update might be difficult...
            try:
                reduced_darks, reduced_darks_infos = scan.load_reduced_darks(
                    return_info=True
                )
            except Exception:
                _logger.warning(
                    f"no reduced dark found for {scan}. Please compute them to get a better display."
                )
            else:
                scan.set_reduced_darks(reduced_darks, darks_infos=reduced_darks_infos)

            try:
                reduced_flats, reduced_flats_info = scan.load_reduced_flats(
                    return_info=True
                )
            except Exception:
                _logger.warning(
                    f"no reduced flat(s) found for {scan}. Please compute them to get a better display."
                )
            else:
                scan.set_reduced_flats(reduced_flats, flats_infos=reduced_flats_info)

            reading_order_ref = self._getReadingOrderRef()
            reading_order = self._scan_reading_order[scan.get_identifier().to_str()]

            invert_reading_order = not numpy.allclose(
                reading_order_ref, reading_order, atol=10e-1
            )

            slice_to_use = self._slice_for_preview
            if slice_to_use == "first":
                slice_to_use = 0
            elif slice_to_use == "last":
                slice_to_use = -1
            elif slice_to_use == "middle":
                slice_to_use = len(scan.projections) // 2

            proj_idx = sorted(scan.projections.keys(), reverse=invert_reading_order)[
                slice_to_use
            ]
            ff = scan.flat_field_correction(
                (scan.projections[proj_idx],),
                (slice_to_use,),
            )[0]

            if (scan.detector_is_lr_flip or False) ^ self._fliplrFrames:
                ff = numpy.fliplr(ff)
            if (scan.detector_is_ud_flip or False) ^ self._flipudFrames:
                ff = numpy.flipud(ff)

            return ff
        else:
            raise TypeError(f"tomo_obj of type {type(tomo_obj)} is not handled")

    def _recomputeBlackAndWhiteCompositeImage(self):
        def get_min_max(tomo_obj, axis):
            axis_pos = tomo_obj.stitching_metadata.get_abs_position_px(axis=axis) or 0
            frame_axis = 0 if axis == 0 else 1
            return (
                axis_pos,
                axis_pos + self.getFrame(tomo_obj=tomo_obj).shape[frame_axis],
            )

        import sys
        from math import ceil

        min_x = sys.float_info.max
        min_y = sys.float_info.max
        max_x = sys.float_info.min
        max_y = sys.float_info.min
        for tomo_obj in self._tomo_objs.values():
            if tomo_obj() is None:
                continue
            l_min_x, l_max_x = get_min_max(tomo_obj(), axis=2)
            l_min_y, l_max_y = get_min_max(tomo_obj(), axis=0)
            min_x = min(min_x, l_min_x)
            max_x = max(max_x, l_max_x)
            min_y = min(min_y, l_min_y)
            max_y = max(max_y, l_max_y)
        self._compositeOffset = (min_y, min_x)
        self._BWImage = numpy.zeros(
            shape=(
                ceil(max_y - min_y),
                ceil(max_x - min_x),
            ),
            dtype=numpy.float32,
        )
        # update BW image
        for tomo_obj in self._tomo_objs.values():
            if tomo_obj() is None:
                continue
            else:
                frame = self.getFrame(tomo_obj=tomo_obj())
                position_y = (
                    tomo_obj().stitching_metadata.get_abs_position_px(axis=0) or 0
                )
                position_x = (
                    tomo_obj().stitching_metadata.get_abs_position_px(axis=2) or 0
                )
                self._BWImage[
                    position_y - min_y : frame.shape[0] + position_y - min_y,
                    position_x - min_x : position_x + frame.shape[1] - min_x,
                ] -= frame

    def _updateImages(self):
        self.clearImages()
        first_display = self._firstDisplay
        if self._blackAndWhiteCompositeMode:
            self._recomputeBlackAndWhiteCompositeImage()
        for tomo_obj in self._tomo_objs.values():
            if tomo_obj() is None:
                continue
            else:
                self._updateImage(
                    tomo_obj=tomo_obj(),
                    recompute_composite=self._blackAndWhiteCompositeMode,
                )
        if first_display and len(self._tomo_objs) > 0 and self._activated:
            # work around to handle first plotting when just activated and can get several objects
            self.resetZoom()
            self._firstDisplay = False


class AlphaValuesTableWidget(qt.QTableWidget):
    """
    Widget to define alpha values of a list of tomo object.
    Meant to work with the RawPlotWidget used for stitching
    """

    COLUMNS = "legend", "alpha value"

    def __init__(self, parent=None, plot=None):
        super().__init__(parent)
        if plot is not None:
            self.__plot = weakref.ref(plot)
        self._sliders = {}

    def getPlot(self):
        if self.__plot is None:
            return None
        else:
            return self.__plot()

    def clear(self):
        for slider, label in self._sliders.items():
            slider.valueChanged.disconnect(self._alphaValueChanged)

        self._sliders.clear()
        super().clear()

    def addTomoObj(self, tomo_obj: TomwerObject):
        n_objs = self.rowCount() + 1
        self.setRowCount(n_objs)
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)
        self.horizontalHeader().setSectionResizeMode(qt.QHeaderView.ResizeToContents)
        self.verticalHeader().hide()

        _item_legend = qt.QTableWidgetItem()
        plot_legend = tomo_obj.get_identifier().to_str()
        short_descrition = tomo_obj.get_identifier().short_description()
        _item_legend.setText(short_descrition)
        self.setItem(n_objs - 1, 0, _item_legend)

        slider = AlphaValueSlider(self)
        slider.valueChanged.connect(self._alphaValueChanged)
        self.setCellWidget(n_objs - 1, 1, slider)
        self._sliders[slider] = (plot_legend, short_descrition)

    def clearTomoObjs(self):
        # disconnect sliders
        for slider in self._sliders.keys():
            slider.valueChanged.disconnect(self._alphaValueChanged)
        self._sliders.clear()
        self.setRowCount(len(self._sliders))
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)
        self.horizontalHeader().setSectionResizeMode(qt.QHeaderView.ResizeToContents)
        self.verticalHeader().hide()

    def setTomoObjs(self, tomo_objs: tuple):
        self.clearTomoObjs()
        self.clear()

        for tomo_obj in tomo_objs:
            self.addTomoObj(tomo_obj=tomo_obj)

    def _alphaValueChanged(self, *args, **kwargs):
        sender = self.sender()  # pylint: disable=E1101
        assert isinstance(
            sender, AlphaValueSlider
        ), f"sender is expected to be an instance of AlphaValueSlider. get {type(sender)}"
        legend = self._sliders.get(sender, (None, None))[0]
        if legend is not None:
            plot = self.getPlot()
            if plot is None:
                return
            else:
                image_item = plot.getImage(legend)
                if image_item is not None:
                    image_item.setAlpha(
                        sender.value() / 255
                    )  # silx define value in [0, 1.0] when AlphaValueSlider in [0, 255]


class AlphaValueSlider(qt.QTableWidget):
    """
    slider to define alpha value with a slider and top button on each side to quickly set values to boundaries
    """

    valueChanged = qt.Signal(int)
    " emit when the slider value changed"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        # `invisible` button
        invisibleIcon = tomwer_icons.getQIcon("invisible")
        self._invisibleButton = qt.QPushButton(invisibleIcon, "", self)
        self._invisibleButton.setFlat(True)
        self.layout().addWidget(self._invisibleButton)
        # `slider`
        self._slider = qt.QSlider(qt.Qt.Horizontal, self)
        self._slider.setRange(0, 255)
        self._slider.setValue(255)
        self.layout().addWidget(self._slider)

        # `visible` button
        visibleIcon = tomwer_icons.getQIcon("visible")
        self._visibleButton = qt.QPushButton(visibleIcon, "", self)
        self._visibleButton.setFlat(True)
        self.layout().addWidget(self._visibleButton)

        # connect signal / slot
        self._invisibleButton.released.connect(self._setInvisible)
        self._visibleButton.released.connect(self._setVisible)

        # expose API
        self._slider.valueChanged.connect(self.valueChanged)

    def _setInvisible(self, *args, **kwargs):
        self._slider.setValue(0)

    def _setVisible(self, *args, **kwargs):
        self._slider.setValue(255)

    def value(self) -> int:
        return self._slider.value()

    def setValue(self, value: int):
        self._slider.setValue(int(value))
