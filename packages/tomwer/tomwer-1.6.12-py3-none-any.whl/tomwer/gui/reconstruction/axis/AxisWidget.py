from __future__ import annotations

import logging

import numpy
import scipy.signal
from silx.gui import qt

from tomwer.core.process.reconstruction.axis import mode as axis_mode
from tomwer.core.process.reconstruction.axis.anglemode import CorAngleMode
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils import image
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.synctools.axis import QAxisRP

from .CompareImages import CompareImages
from .AxisSettingsWidget import AxisSettingsWidget

_logger = logging.getLogger(__name__)


class AxisWidget(qt.QMainWindow):
    """
    Main widget for the computing the rotation axis.

    It contains:
    * CompareImages widget as the central widget to display two opposite radios once shifted (and flip) with the cor found
    * A control widget on the left to select the algorithm to be applied, algorithm options...

    :raises ValueError: given axis is not an instance of _QAxisRP
    """

    sigAxisEditionLocked = qt.Signal(bool)
    """Signal emitted when the status of the reconstruction parameters edition
    change"""

    sigLockModeChanged = qt.Signal(bool)
    """signal emitted when the lock on the mode change"""

    sigPositionChanged = qt.Signal(tuple)
    """signal emitted when the center of rotation center change"""

    def __init__(self, axis_params, parent=None, backend=None):
        super().__init__(parent)
        if isinstance(axis_params, QAxisRP):
            self.__recons_params = axis_params
        else:
            raise TypeError("axis should be an instance of _QAxisRP")

        self._imgA = None
        self._imgB = None
        self._shiftedImgA = None
        self._flipB = True
        """Option if we want to flip the image B"""
        self._scan = None
        self._axis_params = None
        self._lastManualFlip = None
        """Cache for the last user entry for manual flip"""
        self._lastXShift = None
        # cache to know if the x shift has changed since
        self._lastYShift = None
        # cache to know if the y shift has changed
        self._lastXOrigin = None
        # cache to know if the x origin has changed since
        self._lastYOrigin = None
        # cache to know if the y origin has changed since

        self.setWindowFlags(qt.Qt.Widget)
        self._plot = CompareImages(parent=self, backend=backend)
        self._plot.setAutoResetZoom(False)
        _mode = CompareImages.VisualizationMode.COMPOSITE_A_MINUS_B
        self._plot.setVisualizationMode(_mode)
        self._plot.setAlignmentMode(CompareImages.AlignmentMode.STRETCH)
        self.setCentralWidget(self._plot)

        self._dockWidgetCtrl = qt.QDockWidget(parent=self)
        self._dockWidgetCtrl.layout().setContentsMargins(0, 0, 0, 0)
        self._dockWidgetCtrl.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._settingsWidget = AxisSettingsWidget(
            parent=self, reconsParams=self.__recons_params
        )
        self._settingsWidgetScrollArea = qt.QScrollArea(self)
        self._settingsWidgetScrollArea.setWidgetResizable(True)
        self._settingsWidgetScrollArea.setWidget(self._settingsWidget)
        self._dockWidgetCtrl.setWidget(self._settingsWidgetScrollArea)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._dockWidgetCtrl)

        # signal / slot connection
        self._settingsWidget.sigShiftChanged.connect(self._updateShift)
        self._settingsWidget.sigShiftChanged.connect(self._corChanged)
        self._settingsWidget.sigRoiChanged.connect(self._updateShift)
        self._settingsWidget.sigAuto.connect(self._updateAuto)
        self._settingsWidget.sigModeChanged.connect(self.setMode)
        self._settingsWidget.sigModeLockChanged.connect(self._modeLockChanged)
        self._settingsWidget.sigResetZoomRequested.connect(self._resetZoomPlot)
        self._settingsWidget.sigSubSamplingChanged.connect(self._updateSubSampling)
        self._settingsWidget.sigUrlChanged.connect(self._urlChanged)
        self._plot.sigCropImagesChanged.connect(self._updateShift)

        # adapt gui to the axis value
        self.setReconsParams(axis=self.__recons_params)
        self.getPlot().getPlot().setAxesDisplayed(True)

    def manual_uses_full_image(self, value):
        self._settingsWidget.manual_uses_full_image(value)

    def _modeLockChanged(self, lock):
        self.sigLockModeChanged.emit(lock)

    def _corChanged(self):
        self.sigPositionChanged.emit((self.getXShift(), self.getYShift()))

    def getPlot(self):
        return self._plot

    def _resetZoomPlot(self):
        self._plot.getPlot().resetZoom()

    def setMode(self, mode):
        """
        Define the mode to use for radio axis

        :param mode:
        :return:
        """
        mode = axis_mode.AxisMode.from_value(mode)
        with block_signals(self._settingsWidget):
            with block_signals(self._axis_params):
                self._settingsWidget.setMode(mode)
                if mode is axis_mode.AxisMode.manual:
                    self._setModeLockFrmSettings(False)

    def setEstimatedCor(self, value):
        self._settingsWidget.setEstimatedCor(value=value)

    def getEstimatedCor(self):
        return self._settingsWidget.getEstimatedCor()

    def updateXRotationAxisPixelPositionOnNewScan(self) -> bool:
        return self._settingsWidget.updateXRotationAxisPixelPositionOnNewScan()

    def _setModeLockFrmSettings(self, lock: bool):
        # only lock the push button
        with block_signals(self):
            self._settingsWidget._mainWidget._calculationWidget._lockMethodPB.setLock(
                lock
            )

    def getROIDims(self):
        if self.getMode() == axis_mode.AxisMode.manual:
            return self._settingsWidget.getROIDims()
        else:
            return None

    def getROIOrigin(self):
        if self.getMode() == axis_mode.AxisMode.manual:
            return self._settingsWidget.getROIOrigin()
        else:
            return None

    def getImgSubSampling(self):
        return self._settingsWidget.getImgSubSampling()

    def _computationRequested(self):
        self.sigComputationRequested.emit()

    def setLocked(self, locked):
        with block_signals(self):
            if self._axis_params.mode not in (axis_mode.AxisMode.manual,):
                self._axis_params.mode = axis_mode.AxisMode.manual
            self._settingsWidget.setLocked(locked)

        self.sigAxisEditionLocked.emit(locked)

    def isModeLock(self):
        return self._settingsWidget.isModeLock()

    def _validated(self):
        """callback when the validate button is activated"""
        self.sigApply.emit()

    def _setRadio2Flip(self, checked):
        self._plot.setRadio2Flip(checked)

    def _flipChanged(self, checked):
        if self.getMode() == axis_mode.AxisMode.manual:
            self._lastManualFlip = self._plot.isRadio2Flip()

        if checked == self._flipB:
            return
        else:
            self._flipB = checked
            self._updatePlot()

    def setReconsParams(self, axis: QAxisRP):
        """

        :param axis: axis to edit
        :return:
        """
        assert isinstance(axis, QAxisRP)
        self._axis_params = axis
        with block_signals(self):
            self.resetShift()
            self._settingsWidget.setAxisParams(axis)

    def setScan(self, scan):
        """
        Update the interface concerning the given scan. Try to display the
        radios for angle 0 and 180.

        :param scan: scan for which we want the axis updated.
        """
        self.clear()
        _scan = scan
        if type(scan) is str:
            try:
                _scan = ScanFactory.create_scan_object(scan)
            except ValueError:
                raise ValueError("Fail to discover a valid scan in %s" % scan)
        elif not isinstance(_scan, TomwerScanBase):
            raise ValueError(
                f"type of {scan} ({type(scan)}) is invalid, scan should be a file/dir path or an instance of ScanBase"
            )
        assert isinstance(_scan, TomwerScanBase)

        if _scan.axis_params is None:
            _scan.axis_params = QAxisRP()

        if self._scan is not None:
            self._scan.axis_params.sigAxisUrlChanged.disconnect(self._updatePlot)
        update_x_rotation_axis_pixel_position = (
            self._settingsWidget._mainWidget.updateXRotationAxisPixelPositionOnNewScan()
        )
        if (
            update_x_rotation_axis_pixel_position
            and scan.x_rotation_axis_pixel_position is not None
        ):
            self.setEstimatedCor(scan.x_rotation_axis_pixel_position)

        # update visualization
        self._scan = _scan
        self._scan.axis_params.sigAxisUrlChanged.connect(self._updatePlot)
        self._settingsWidget.setScan(scan=self._scan)
        self._updatePlot()
        self.getPlot().getPlot().resetZoom()

    def _updatePlot(self):
        if self._scan is None:
            return
        self._urlChanged()

    def _urlChanged(self):
        with block_signals(self):
            coreAngleMode = CorAngleMode.from_value(self.__recons_params.angle_mode)
            if self._scan is None:
                return
            axis_rp = self._scan.axis_params
            if coreAngleMode is CorAngleMode.manual_selection:
                manual_sel_widget = (
                    self._settingsWidget._mainWidget._inputWidget._angleModeWidget._manualFrameSelection
                )
                urls = manual_sel_widget.getFramesUrl(as_txt=False)
                axis_rp.axis_url_1, axis_rp.axis_url_2 = urls
                axis_rp.flip_lr = manual_sel_widget.isFrame2LRFLip()
            else:
                axis_rp.flip_lr = True
                res = self._scan.get_opposite_projections(mode=coreAngleMode)
                axis_rp.axis_url_1 = res[0]
                axis_rp.axis_url_2 = res[1]

            if axis_rp.n_url() < 2:
                _logger.error("Fail to detect radio for axis calculation")
            elif axis_rp.axis_url_1.url:
                # if necessary normalize data
                axis_rp.axis_url_1.normalize_data(self._scan, log_=False)
                axis_rp.axis_url_2.normalize_data(self._scan, log_=False)

                paganin = self.__recons_params.paganin_preproc
                # check if normed
                if paganin:
                    imgA = axis_rp.axis_url_1.normalized_data_paganin
                    imgB = axis_rp.axis_url_2.normalized_data_paganin
                else:
                    imgA = axis_rp.axis_url_1.normalized_data
                    imgB = axis_rp.axis_url_2.normalized_data
                assert imgA is not None
                assert imgB is not None
                self.setImages(imgA=imgA, imgB=imgB, flipB=axis_rp.flip_lr)
            else:
                _logger.error(
                    "fail to find radios for angle 0 and 180. Unable to update axis gui"
                )

    def clear(self):
        if self._scan is not None:
            self._scan.axis_params.sigAxisUrlChanged.disconnect(self._updatePlot)
        self._scan = None

    def setImages(self, imgA: numpy.array, imgB: numpy.array, flipB: bool):
        """

        :warning: does not reset the shift when change images

        :param imgA: first image to compare. Will be the one shifted
        :param imgB: second image to compare
        :param flipB: True if the image B has to be flipped
        """
        assert imgA is not None
        assert imgB is not None
        _imgA = imgA
        _imgB = imgB

        if _imgA.shape != _imgB.shape:
            _logger.error(
                "The two provided images have incoherent shapes "
                f"({_imgA.shape} vs {_imgB.shape})"
            )
        elif _imgA.ndim != 2:
            _logger.error("Image shape are not 2 dimensional")
        else:
            self._imgA = _imgA
            self._imgB = _imgB
            self._flipB = flipB

            self._settingsWidget._roiControl.setLimits(
                width=self._imgA.shape[1], height=self._imgA.shape[0]
            )
            self._updateShift()

    def _updateSubSampling(self):
        self._updateShift()
        self.getPlot().getPlot().resetZoom()

    def _updateShift(self, xShift=None, yShift=None):
        if self._imgA is None or self._imgB is None:
            return
        xShift = xShift or self.getXShift()
        yShift = yShift or self.getYShift()

        # TODO: we might avoid flipping image at each new x_shift...
        _imgA, _imgB = self._getRawImages()
        # apply shift
        if xShift == 0.0 and yShift == 0.0:
            self._shiftedImgA = _imgA
            self._shiftedImgB = _imgB
        else:
            try:
                cval_imgA = _imgA.min()
                cval_imgB = _imgB.min()
            except ValueError:
                _logger.warning("enable to retrieve imgA.min() and / or" "imgB.min().")
                cval_imgA = 0
                cval_imgB = 0
            try:
                x_shift = self.getXShift() / self.getImgSubSampling()
                y_shift = self.getYShift() / self.getImgSubSampling()
                self._shiftedImgA = image.shift_img(
                    data=_imgA,
                    dx=-x_shift,
                    dy=y_shift,
                    cval=cval_imgA,
                )
                self._shiftedImgB = image.shift_img(
                    data=_imgB,
                    dx=x_shift,
                    dy=y_shift,
                    cval=cval_imgB,
                )
                crop = self.getPlot().cropComparedImages()

                if not crop:
                    # handling of the crop:
                    # 1. we will concatenate the shifted array with the unshifted to avoid crop
                    # 2. in order to handled properly the shift and overlaps we need to add an empty array
                    abs_x_shift = abs(int(x_shift))
                    buffer_array_img_A = numpy.full(
                        shape=(self._shiftedImgA.shape[0], abs_x_shift),
                        fill_value=cval_imgA,
                    )
                    buffer_array_img_B = numpy.full(
                        shape=(self._shiftedImgB.shape[0], abs_x_shift),
                        fill_value=cval_imgB,
                    )
                    if x_shift == 0:
                        pass
                    elif x_shift > 0:
                        self._shiftedImgA = numpy.concatenate(
                            (
                                _imgA[:, :abs_x_shift],
                                self._shiftedImgA,
                                buffer_array_img_A,
                            ),
                            axis=1,
                        )
                        self._shiftedImgB = numpy.concatenate(
                            (
                                buffer_array_img_B,
                                self._shiftedImgB,
                                _imgB[:, -abs_x_shift:],
                            ),
                            axis=1,
                        )
                    else:
                        self._shiftedImgA = numpy.concatenate(
                            (
                                buffer_array_img_A,
                                self._shiftedImgA,
                                _imgA[:, :abs_x_shift],
                            ),
                            axis=1,
                        )
                        self._shiftedImgB = numpy.concatenate(
                            (
                                _imgB[:, :abs_x_shift],
                                self._shiftedImgB,
                                buffer_array_img_B,
                            ),
                            axis=1,
                        )
            except ValueError as e:
                _logger.error(e)
                self._shiftedImgA = _imgA
                self._shiftedImgB = _imgB

        with block_signals(self):
            try:
                self._plot.setData(
                    image1=self._shiftedImgA,
                    image2=self._shiftedImgB,
                )
            except ValueError:
                _logger.warning(
                    "Unable to set images. Maybe there is some "
                    "incomplete dataset or an issue with "
                    "normalization."
                )
            roi_origin = self.getROIOrigin()
            if roi_origin is not None:
                x_origin, y_origin = roi_origin
            else:
                x_origin = y_origin = None
            self._lastXShift = xShift
            self._lastYShift = yShift
            self._lastXOrigin = x_origin
            self._lastYOrigin = y_origin

    def _getRawImages(self):
        def selectROI(data, width, height, x_origin, y_origin, subsampling):
            assert subsampling > 0
            x_min = x_origin - width // 2
            x_max = x_origin + width // 2
            y_min = y_origin - height // 2
            y_max = y_origin + height // 2
            return data[y_min:y_max:subsampling, x_min:x_max:subsampling]

        # get images and apply ROI if any
        _roi_dims = self.getROIDims()
        _origin = self.getROIOrigin()
        subsampling = self.getImgSubSampling()
        _imgA = self._imgA
        _imgB = self._imgB
        # flip image B
        _imgB = numpy.fliplr(_imgB) if self._flipB else _imgB
        if _roi_dims is not None:
            assert type(_roi_dims) is tuple, f"invalide roi value {_roi_dims}"
            _imgA = selectROI(
                _imgA,
                width=_roi_dims[0],
                height=_roi_dims[1],
                x_origin=_origin[0],
                y_origin=_origin[1],
                subsampling=subsampling,
            )
            _imgB = selectROI(
                _imgB,
                width=_roi_dims[0],
                height=_roi_dims[1],
                x_origin=_origin[0],
                y_origin=_origin[1],
                subsampling=subsampling,
            )
        return _imgA, _imgB

    def _updateAuto(self):
        _imgA, _imgB = self._getRawImages()
        correlation = scipy.signal.correlate2d(in1=_imgA, in2=_imgB)
        y, x = numpy.unravel_index(numpy.argmax(correlation), correlation.shape)
        self._setShift(x=x, y=y)

    def resetShift(self):
        with block_signals(self._settingsWidget):
            self._settingsWidget.reset()
        if self._imgA is not None and self._imgB is not None:
            self.setImages(imgA=self._imgA, imgB=self._imgB, flipB=self._flipB)

    # expose API

    def getXShift(self):
        return self._settingsWidget.getXShift()

    def setXShift(self, x):
        self._settingsWidget.setXShift(x=x)

    def getYShift(self):
        return self._settingsWidget.getYShift()

    def setYShift(self, y):
        self._settingsWidget.setYShift(y=y)

    def _setShift(self, x, y):
        self._settingsWidget.setShift(x, y)

    def getShiftStep(self):
        return self._settingsWidget.getShiftStep()

    def setShiftStep(self, value):
        self._settingsWidget.setShiftStep(value=value)

    def getAxisParams(self):
        return self._settingsWidget.getAxisParams()

    def getMode(self):
        return self._settingsWidget.getMode()

    def setModeLock(self, mode):
        return self._settingsWidget.setModeLock(mode=mode)

    def isYAxisInverted(self) -> bool:
        return self._settingsWidget.isYAxisInverted()

    def setYAxisInverted(self, checked: bool):
        return self._settingsWidget.setYAxisInverted(checked=checked)
