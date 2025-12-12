import weakref

from silx.gui import qt
from enum import Enum as _Enum

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.gui.settings import Y_AXIS_DOWNWARD
from tomwer.gui.visualization.imagestack import ImageStack


class DataViewer(qt.QMainWindow):
    """
    Widget used to browse through data and reconstructed slices
    """

    sigConfigChanged = qt.Signal()
    """Signal emitted when the settings (display mode, options...) changed. """

    def __init__(self, parent, show_overview=True, backend=None):
        super().__init__(parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._scan = None
        # viewer
        self._viewer = ImageStack(
            parent=self, show_overview=show_overview, backend=backend
        )
        self._viewer.getPlotWidget().getMaskAction().setVisible(False)
        self._viewer.getPlotWidget().setYAxisInverted(Y_AXIS_DOWNWARD)
        # set an UrlLoader managing .npy and .vol
        self._viewer.getPlotWidget().setKeepDataAspectRatio(True)
        self.setCentralWidget(self._viewer)

        # display control
        self._controls = DisplayControl(parent=self)
        self._controlsDW = qt.QDockWidget(self)
        self._controlsDW.setWidget(self._controls)
        self._controlsDW.setWindowTitle("infos")
        self.addDockWidget(qt.Qt.TopDockWidgetArea, self._controlsDW)
        self._controlsDW.setTitleBarWidget(qt.QWidget(self))
        self._controlsDW.setFloating(False)

        # connect signal / slot
        self._controls.sigDisplayModeChanged.connect(self._updateDisplay)
        self._controls.sigDisplayModeChanged.connect(self.sigConfigChanged)

        # upgrade of the slider (see details in '__sliderPressed' docstring).
        horizontal_slider = self._viewer._slider
        horizontal_slider._slider.sliderReleased.connect(self.__sliderReleased)
        horizontal_slider._slider.sliderPressed.connect(self.__sliderPressed)

    def __sliderPressed(self):
        """
        today each time the slider value is modified it will load the frame and display it
        but in our case we cannot afford it as it will take too much memory.
        So we will disconnect the callback (self._viewer.setCurrentUrlIndex) until the slider is active
        and reactivate it afterwards

        """
        self._viewer._slider.sigCurrentUrlIndexChanged.disconnect(
            self._viewer.setCurrentUrlIndex
        )

    def __sliderReleased(self):
        """
        See details in '__sliderPressed'
        """
        horizontal_slider = self._viewer._slider
        self._viewer._slider.sigCurrentUrlIndexChanged.connect(
            self._viewer.setCurrentUrlIndex
        )
        # set the url with the latest value to display the requested frame
        self._viewer.setCurrentUrlIndex(horizontal_slider.value())

    def getPlotWidget(self):
        return self._viewer.getPlotWidget()

    def getCurrentUrl(self):
        return self._viewer.getCurrentUrl()

    def setScanInfoVisible(self, visible: bool):
        self._controls.setScanInfoVisible(visible=visible)

    def setDisplayModeVisible(self, visible: bool):
        self._controls.setDisplayModeVisible(visible=visible)

    def setScanOverviewVisible(self, visible: bool) -> None:
        self._viewer.setScanOverviewVisible(visible=visible)

    def getUrlListDockWidget(self):
        return self._viewer.getUrlListDockWidget()

    def close(self):
        self.stop()
        self._viewer.close()
        self._viewer = None
        super().close()

    def getScan(self):
        if self._scan:
            return self._scan()

    def setScan(self, scan):
        if scan is not None:
            self._scan = weakref.ref(scan)
        else:
            self._scan = None
        # update scan name
        self._viewer.setScan(scan=scan)
        self._controls.setScanName(str(scan))
        self._updateDisplay()
        # has the display is post pone we can only set expected dimensions
        # for the viewer
        self._viewer.setResetZoomOnNextIteration(True)

    def getDisplayMode(self):
        return self._controls.getDisplayMode()

    def setDisplayMode(self, mode):
        self._controls.setDisplayMode(mode)

    def getRadioOption(self):
        return self._controls.getRadioOption()

    def setRadioOption(self, opt):
        self._controls.setRadioOption(opt)

    def getSliceOption(self):
        return self._controls.getSliceOption()

    def setSliceOption(self, opt):
        self._controls.setSliceOption(opt)

    def _updateDisplay(self):
        """Update display of the viewer"""
        self._viewer.setSliceReconsParamsVisible(
            self.getDisplayMode() is _DisplayMode.SLICES
        )
        self._viewer.setScanOverviewVisible(
            self.getDisplayMode() is not _DisplayMode.SLICES
        )
        if self._scan is None or self._scan() is None:
            self._viewer.reset()
            return

        assert isinstance(self._scan(), TomwerScanBase)
        slices_metadata = {}
        if self.getDisplayMode() is _DisplayMode.RADIOS:
            # update the normalization function from the viewer if needed
            if self.getRadioOption() is _RadioMode.NORMALIZED:
                url_to_index = {
                    v.path(): k for k, v in self._scan().projections.items()
                }
                self._viewer.setNormalizationFct(
                    self._scan().data_flat_field_correction,
                    url_indexes=url_to_index,
                )
            else:
                self._viewer.setNormalizationFct(None)

            slices = self._scan().projections
        elif self.getDisplayMode() is _DisplayMode.SLICES:
            self._viewer.setNormalizationFct(None)
            if self.getSliceOption() is _SliceMode.LATEST:
                slices = self._scan().latest_reconstructions
            else:
                slices = self._scan().get_reconstructed_slices()
            # convert volumes identifiers to DataUrl
            slices_urls = []
            for identifier in slices:
                if isinstance(identifier, TomwerVolumeBase):
                    volume = identifier
                else:
                    volume = VolumeFactory.create_tomo_object_from_identifier(
                        identifier=identifier
                    )
                urls = list(volume.browse_data_urls())
                try:
                    metadata = volume.metadata or volume.load_metadata()
                except Exception:
                    metadata = None
                slices_urls.extend(urls)
                slices_metadata.update({url.path(): metadata for url in urls})

            slices = slices_urls

        elif self.getDisplayMode() is _DisplayMode.DARKS:
            self._viewer.setNormalizationFct(None)
            slices = self._scan().darks
        elif self.getDisplayMode() is _DisplayMode.FLATS:
            self._viewer.setNormalizationFct(None)
            slices = self._scan().flats
        elif self.getDisplayMode() is _DisplayMode.REDUCED_DARKS:
            self._viewer.setNormalizationFct(None)
            slices = self._scan().load_reduced_darks(return_as_url=True)
        elif self.getDisplayMode() is _DisplayMode.REDUCED_FLATS:
            self._viewer.setNormalizationFct(None)
            slices = self._scan().load_reduced_flats(return_as_url=True)
        else:
            raise ValueError("DisplayMode should be RADIOS or SLICES")

        if isinstance(slices, dict):
            slices = [
                value for key, value in sorted(slices.items(), key=lambda item: item[0])
            ]
        if slices is not None and len(slices) > 0:
            # warning: 'setUrls' will clean metadata so we need to first set the urls
            self._viewer.setUrls(slices)
            self._viewer.setSliceMetadata(slices_metadata)
        else:
            self._viewer.reset()
        self._viewer._filterUrlList()

    def clear(self):
        self._scan = None
        self._viewer.reset()
        self._viewer.setUrls(list())
        self._controls.clear()

    def stop(self):
        # insure we call self._viewer._freeLoadingThreads()
        self._viewer.reset()


class _DisplayMode(_Enum):
    RADIOS = "projections-radios"
    SLICES = "slices"
    DARKS = "raw darks"
    FLATS = "raw flats"
    REDUCED_DARKS = "reduced darks"
    REDUCED_FLATS = "reduced flats"


class _RadioMode(_Enum):
    NORMALIZED = "normalized"
    RAW = "raw"


class _SliceMode(_Enum):
    LATEST = "latest"
    ALL = "all"


class DisplayControl(qt.QWidget):
    """
    Widget used to define what we want to display from the viewer
    """

    sigDisplayModeChanged = qt.Signal()
    """Signal emitted when the configuration of the display change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._lastConfig = None, None
        self.setLayout(qt.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # scan information
        self._scanLab = qt.QLabel("scan:", self)
        self._scanLab.setFixedWidth(40)
        self._scanLab.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._scanLab, 0, 0, 1, 1)
        self._scanQLE = qt.QLineEdit("", self)
        self._scanQLE.setReadOnly(True)
        self.layout().addWidget(self._scanQLE, 0, 1, 1, 3)

        # display information
        self._displayLab = qt.QLabel("display:", self)
        self._displayLab.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._displayLab, 1, 0, 1, 1)
        self._displayMode = qt.QComboBox(self)
        for mode in _DisplayMode:
            self._displayMode.addItem(mode.value)
        self.layout().addWidget(self._displayMode, 1, 1, 1, 1)

        # option information
        self._modeLab = qt.QLabel("mode:", self)
        self._modeLab.setFixedWidth(60)
        self._modeLab.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._modeLab, 1, 2, 1, 1)
        self._widget_options = qt.QWidget(self)
        self._widget_options.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._widget_options, 1, 3, 1, 1)

        self._radioMode = qt.QComboBox(self)
        for mode in _RadioMode:
            self._radioMode.addItem(mode.value)
        self._widget_options.layout().addWidget(self._radioMode)

        self._sliceMode = qt.QComboBox(self)
        for mode in _SliceMode:
            self._sliceMode.addItem(mode.value)
        self._widget_options.layout().addWidget(self._sliceMode)

        # set up
        # by default propose slices to avoid useless processing on radios
        idx = self._displayMode.findText(_DisplayMode.SLICES.value)
        self._displayMode.setCurrentIndex(idx)
        self._updateOptions()

        # connect signal and slot
        self._displayMode.currentTextChanged.connect(self._updateOptions)
        self._radioMode.currentTextChanged.connect(self._updateOptions)
        self._sliceMode.currentTextChanged.connect(self._updateOptions)

    def setScanInfoVisible(self, visible):
        self._scanLab.setVisible(visible)
        self._scanQLE.setVisible(visible)

    def setDisplayModeVisible(self, visible):
        self._displayLab.setVisible(visible)
        self._displayMode.setVisible(visible)

    def getDisplayMode(self) -> _DisplayMode:
        """

        :return: selected mode: display slices or radios
        """
        return _DisplayMode(self._displayMode.currentText())

    def setDisplayMode(self, mode):
        mode = _DisplayMode(mode)
        idx = self._displayMode.findText(mode.value)
        self._displayMode.setCurrentIndex(idx)

    def getRadioOption(self) -> _RadioMode:
        return _RadioMode(self._radioMode.currentText())

    def setRadioOption(self, opt):
        opt = _RadioMode(opt)
        idx = self._radioMode.findText(opt.value)
        self._radioMode.setCurrentIndex(idx)

    def getSliceOption(self) -> _SliceMode:
        return _SliceMode(self._sliceMode.currentText())

    def setSliceOption(self, opt):
        opt = _SliceMode(opt)
        idx = self._sliceMode.findText(opt.value)
        self._sliceMode.setCurrentIndex(idx)

    def _updateOptions(self, *args, **kwargs):
        mode = self.getDisplayMode()
        self._radioMode.setVisible(mode == _DisplayMode.RADIOS)
        self._sliceMode.setVisible(mode == _DisplayMode.SLICES)
        self._modeLab.setVisible(mode in (_DisplayMode.RADIOS, _DisplayMode.SLICES))
        if mode is _DisplayMode.RADIOS:
            config = mode, self.getRadioOption()
        elif mode is _DisplayMode.SLICES:
            config = mode, self.getSliceOption()
        elif mode in (
            _DisplayMode.DARKS,
            _DisplayMode.FLATS,
            _DisplayMode.REDUCED_DARKS,
            _DisplayMode.REDUCED_FLATS,
        ):
            config = mode, None
        else:
            raise ValueError("mode should be RADIOS or SLICES")
        if config != self._lastConfig:
            self._lastConfig = config
            self.sigDisplayModeChanged.emit()

    def setScanName(self, scan_name: str):
        self._scanQLE.setText(scan_name)

    def clear(self):
        self._scanQLE.clear()
