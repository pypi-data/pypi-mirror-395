from __future__ import annotations

import os
import time
import logging

import numpy
import numpy.lib.npyio

from silx.gui import qt
from silx.gui.dialog.ColormapDialog import DisplayMode
from silx.gui.plot.ImageStack import ImageStack as _ImageStack
from silx.gui.plot.ImageStack import UrlLoader
from silx.io.url import DataUrl
from tomwer.core.utils.ftseriesutils import get_vol_file_shape
from tomwer.gui import icons
from tomwer.gui.visualization.fullscreenplot import FullScreenPlot2D
from tomwer.gui.visualization.reconstructionparameters import ReconstructionParameters
from tomwer.gui.visualization.scanoverview import ScanOverviewWidget
from tomwer.io.utils.utils import get_slice_data
from tomwer.core.scan.scanbase import TomwerScanBase

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    has_PIL = False  # pragma: no cover
else:
    has_PIL = True

_logger = logging.getLogger(__name__)


class ImageStack(_ImageStack):
    """
    Image stack dedicated to data display.

    It deal for example with data normalization...
    """

    def __init__(self, parent, show_overview=True, backend=None):
        self._sliceMetadata: dict[str, dict] = {}
        # metadata associated to the slice. Key is the url (as str) and value is the dict containing metadata
        self._urlToScan: dict[str, TomwerScanBase] = {}
        # dict to link each slice to a scan id (in the case slices are raw projections - to set _scanOverviewDockerWidget)

        self._normFct = None
        self._url_indexes = None
        super().__init__(parent)
        self.getPlotWidget().setBackend(backend)
        self.getPlotWidget().setKeepDataAspectRatio(True)

        # tune colormap dialog to have histogram by default
        colormapAction = self.getPlotWidget().getColormapAction()
        colormapDialog = colormapAction.getColormapDialog()
        colormapDialog.getHistogramWidget().setDisplayMode(DisplayMode.HISTOGRAM)
        colormapAction.setColormapDialog(colormapDialog)

        self.setUrlLoaderClass(_TomwerUrlLoader)
        # hide axis to be display
        self._plot.setAxesDisplayed(False)
        self._loadSliceParams = False
        self._resetZoom = True

        # add dock widget for reconstruction parameters
        self._reconsInfoDockWidget = qt.QDockWidget(parent=self)
        self._reconsWidgetScrollArea = qt.QScrollArea(self)
        self._reconsWidgetScrollArea.setWidgetResizable(True)
        self._reconsWidget = ReconstructionParameters(self)
        self._reconsWidgetScrollArea.setWidget(self._reconsWidget)
        self._reconsInfoDockWidget.setWidget(self._reconsWidgetScrollArea)
        self._reconsInfoDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._reconsInfoDockWidget)

        # add scan overview dock widget
        if show_overview:
            self._scanOverviewDockerWidget = qt.QDockWidget(parent=self)
            self._scanOverviewDockerWidget.setMaximumHeight(300)
            self._scanOverviewWidget = ScanOverviewWidget(self)
            self._scanOverviewDockerWidget.setWidget(self._scanOverviewWidget)
            self._scanOverviewDockerWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
            self.addDockWidget(
                qt.Qt.RightDockWidgetArea, self._scanOverviewDockerWidget
            )
        else:
            self._scanOverviewWidget = None
            self._scanOverviewDockerWidget = None

        # add search
        self._searchWidget = qt.QLineEdit(parent=self)
        self._searchWidget.setPlaceholderText("search")
        search_icon = icons.getQIcon("search")
        self._searchWidget.addAction(search_icon, qt.QLineEdit.LeadingPosition)
        # reorder urlsTable (include search QLineEdit)
        container = qt.QWidget()
        container_layout = qt.QGridLayout(container)

        container_layout.addWidget(self._searchWidget, 0, 1, 1, 2)
        container_layout.addWidget(self._urlsTable._toggleButton, 1, 2, 1, 1)
        container_layout.addWidget(self._urlsTable, 1, 1, 1, 2)
        self._urlsTable._urlsTable.model()
        self._tableDockWidget.setWidget(container)

        # for now hide the "control"
        self._urlsTable._toggleButton.hide()

        # add an action to plot the url-image 'full size'
        fullScreenIcon = icons.getQIcon("full_screen")
        self._fullScreenAction = qt.QAction(fullScreenIcon, "pop up full screen")
        self.getPlotWidget().toolBar().addAction(self._fullScreenAction)
        self._fullScreenAction.triggered.connect(self._popCurrentImageFullScreen)

        # set up
        self.setAutoResetZoom(False)

        # connect signal / slot
        self.sigCurrentUrlChanged.connect(self.updateAllMetadataDisplayed)
        self._searchWidget.textChanged.connect(self._filterUrlList)

    def _filterUrlList(self, *args, **kwargs):
        """Filter the url list according to the 'searchWidget'"""
        url_list = self._urlsTable._urlsTable
        filter_str = self._searchWidget.text()
        filter_str = filter_str.lstrip(" ").rstrip(" ")
        for item_index in range(url_list.count()):
            item = url_list.item(item_index)
            item.setHidden(filter_str not in item.text())

    def _popCurrentImageFullScreen(self, *args, **kwargs):
        new_plot = FullScreenPlot2D()
        active_image = self.getPlotWidget().getActiveImage()
        if active_image is None or active_image.getData(copy=False) is None:
            return
        url = self.getCurrentUrl()
        window_title = f"Plot of {url.path()}" if url is not None else "Image Plot"

        new_plot.setWindowTitle(window_title)
        # reuse the same colormap for convenience (user modification on it will be applied everywhere)
        new_plot.setDefaultColormap(self.getPlotWidget().getDefaultColormap())

        # add the current image
        new_plot.addImage(active_image.getData(copy=True))

        new_plot.showFullScreen()

    def setScan(self, scan):
        if self._scanOverviewWidget is not None:
            self._scanOverviewWidget.setScan(scan=scan)

    def getUrlListDockWidget(self):
        return self._tableDockWidget

    def resetZoom(self):
        self._plot.resetZoom()

    def setLimits(self, x_min, x_max, y_min, y_max):
        self._plot.setLimits(xmin=x_min, ymin=y_min, xmax=x_max, ymax=y_max)

    def getLimits(self):
        limits = []
        limits.extend(self._plot.getGraphXLimits())
        limits.extend(self._plot.getGraphYLimits())
        return tuple(limits)

    def setSliceReconsParamsVisible(self, visible):
        """show or not information regarding the slice reconstructed"""
        self._reconsInfoDockWidget.setVisible(visible)
        self._loadSliceParams = visible

    def setScanOverviewVisible(self, visible):
        """show or not overview of the scan"""
        if self._scanOverviewDockerWidget is not None:
            self._scanOverviewDockerWidget.setVisible(visible)

    def setNormalizationFct(self, fct, url_indexes=None):
        self._normFct = fct
        self._url_indexes = url_indexes

    def _urlLoaded(self) -> None:
        """

        :param url: result of DataUrl.path() function
        :return:
        """
        sender = self.sender()
        url = sender.url.path()
        if self._urlIndexes is not None and url in self._urlIndexes:
            data = sender.data
            if data is None:
                _logger.warning("no data found (is the url valid ?) " + url)
                return

            if data.ndim != 2:
                if data.ndim == 3:
                    if data.shape[0] == 1:
                        # if reconstruction along z
                        data = data.reshape((data.shape[1], data.shape[2]))
                    elif data.shape[1] == 1:
                        # if reconstruction along y
                        data = data.reshape((data.shape[0], data.shape[2]))
                    elif data.shape[2] == 1:
                        # if reconstruction along z
                        data = data.reshape((data.shape[0], data.shape[1]))
                    else:
                        _logger.warning(f"Image Stack only manage 2D data. Url: {url}")
                        return
                else:
                    _logger.warning(f"Image Stack only manage 2D data. Url: {url}")
                    return
            if self._normFct is None:
                self._urlData[url] = data
            else:
                norm_data = self._normFct(data, index=self._urlIndexes[url])
                self._urlData[url] = norm_data

            if self.getCurrentUrl().path() == url:
                self._plot.addImage(self._urlData[url])
                if hasattr(self, "getWaiterOverlay"):
                    self.getWaiterOverlay().hide()
                else:
                    self._waitingOverlay.hide()
                if self._resetZoom:
                    self._resetZoom = False
                    self._plot.resetZoom()

            if sender in self._loadingThreads:
                self._loadingThreads.remove(sender)
            self.sigLoaded.emit(url)

    def setResetZoomOnNextIteration(self, reset):
        self._resetZoom = reset

    def setCurrentUrl(self, url: DataUrl):
        if url in ("", None):
            url = None
        elif isinstance(url, str):
            url = DataUrl(path=url)
        elif not isinstance(url, DataUrl):
            raise TypeError
        if url is None:
            pass
        elif self._loadSliceParams:
            try:
                self.setCurrentSliceMetadata(self._metadata.get(url.path(), None))
            except Exception:
                _logger.info(f"Failed to find any metadata for {url.path()}.")
        super().setCurrentUrl(url)

    def setUrls(self, urls: list):
        self.clearSliceMetadata()
        _ImageStack.setUrls(self, urls)
        listWidget = self._urlsTable._urlsTable
        items = []
        for i in range(listWidget.count()):
            # TODO: do this on the fly
            item = listWidget.item(i)
            try:
                url = DataUrl(path=item.text())
            except Exception:
                _logger.info(
                    f"fail to deduce data of last modification for {item.text()}"
                )
            else:
                if os.path.exists(url.file_path()):
                    lst_m = time.ctime(os.path.getmtime(url.file_path()))
                    item.setToolTip(f"last modification : {lst_m}")
            items.append(listWidget.item(i))

    def updateAllMetadataDisplayed(self):
        # update widget related to image metadata.
        current_url = self.getCurrentUrl()
        if current_url is not None:
            current_url = current_url.path()

        self.setCurrentSliceMetadata(self._sliceMetadata.get(current_url, None))
        current_scan = self._urlToScan.get(current_url, None)
        if self._scanOverviewWidget:
            self._scanOverviewWidget.setScan(current_scan)

    def clearSliceMetadata(self):
        self._sliceMetadata.clear()

    def setCurrentSliceMetadata(self, metadata: dict | None) -> None:
        self._reconsWidget.setVolumeMetadata(metadata)

    def setSliceMetadata(self, metadata: dict[str, dict]) -> None:
        self._sliceMetadata = metadata
        self.updateAllMetadataDisplayed()

    def updateSliceMetadata(self, metadata: dict[str, dict]) -> None:
        self._sliceMetadata.update(metadata)
        self.updateAllMetadataDisplayed()

    def updateScanToUrl(self, scan_to_url: dict):
        self._urlToScan.update(scan_to_url)
        self.updateAllMetadataDisplayed()

    # scan metadata loading
    def reset(self):
        super().reset()
        self.clearSliceMetadata()
        self._urlToScan.clear()

    def _freeLoadingThreads(self):
        # overwrite it because the default waiting time seems very low
        # and make the CI fails
        for thread in self._loadingThreads:
            thread.blockSignals(True)
            thread.wait(100)
        self._loadingThreads.clear()


class _TomwerUrlLoader(UrlLoader):
    """
    Thread use to load DataUrl
    """

    def run(self):
        if self.url.file_path().endswith(".vol"):
            self.data = self._load_vol()
        elif self.url.scheme() == "tomwer":
            if has_PIL:
                self.data = numpy.array(Image.open(self.url.file_path()))
                if self.url.data_slice() is not None:
                    self.data = self.data[self.url.data_slice()]
            else:
                _logger.warning(
                    "need to install Pillow to read file " + self.url.file_path()
                )
                self.data = None
        else:
            try:
                self.data = get_slice_data(self.url)
            except IOError:
                self.data = None
            except ValueError:
                self.data = None
                _logger.warning(
                    f"Fail to open {self.url.path()}. Maybe the reconstruction failed."
                )
            except Exception as e:
                self.data = None
                _logger.error(
                    "Fail to load data from %s. Error is %s",
                    self.url.path(),
                    e,
                )

    def _load_vol(self):
        """
        load a .vol file
        """
        if self.url.file_path().lower().endswith(".vol.info"):
            info_file = self.url.file_path()
            raw_file = self.url.file_path().replace(".vol.info", ".vol")
        else:
            assert self.url.file_path().lower().endswith(".vol")
            raw_file = self.url.file_path()
            info_file = self.url.file_path().replace(".vol", ".vol.info")

        if not os.path.exists(raw_file):
            data = None
            mess = f"Can't find raw data file {raw_file} associated with {info_file}"
            _logger.warning(mess)
        elif not os.path.exists(info_file):
            mess = f"Can't find info file {info_file} associated with {raw_file}"
            _logger.warning(mess)
            data = None
        else:
            shape = get_vol_file_shape(info_file)
            if None in shape:
                _logger.warning(f"Fail to retrieve data shape for {info_file}.")
                data = None
            else:
                try:
                    numpy.zeros(shape)
                except MemoryError:
                    data = None
                    _logger.warning(
                        f"Raw file %s is too large for being read {raw_file}"
                    )
                else:
                    data = numpy.fromfile(
                        raw_file, dtype=numpy.float32, count=-1, sep=""
                    )
                    try:
                        data = data.reshape(shape)
                    except ValueError:
                        _logger.warning(
                            f"unable to fix shape for raw file {raw_file}. Look for information in {info_file}"
                        )
                        try:
                            sqr = int(numpy.sqrt(len(data)))
                            shape = (1, sqr, sqr)
                            data = data.reshape(shape)
                        except ValueError:
                            _logger.info(
                                f"deduction of shape size for {raw_file} failed"
                            )
                            data = None
                        else:
                            _logger.warning(
                                f"try deducing shape size for {raw_file} might be an incorrect interpretation"
                            )
        if self.url.data_slice() is None:
            return data
        else:
            return data[self.url.data_slice()]
