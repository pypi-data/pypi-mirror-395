from __future__ import annotations

import logging
import weakref
import h5py

import numpy

import os
import silx
from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.data.DataViewerFrame import DataViewerFrame
from silx.gui.data.DataViews import IMAGE_MODE, DataViewHooks
from silx.gui.dialog.ColormapDialog import ColormapDialog

from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.visualization.reconstructionparameters import ReconstructionParameters
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.resourcemanager import BaseResourceObserver, HDF5VolumeManager
from tomoscan.identifier import VolumeIdentifier

from silx.gui.widgets.WaitingOverlay import WaitingOverlay

_logger = logging.getLogger(__name__)


class _ScanInfo(qt.QWidget):
    """Display information about the reconstruction currently displayed"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QFormLayout())
        self._scanQLE = qt.QLineEdit("", self)
        self._scanQLE.setReadOnly(True)
        self.layout().addRow("scan", self._scanQLE)

        self._volumeQLE = qt.QLineEdit("", self)
        self._volumeQLE.setReadOnly(True)
        self.layout().addRow("volume", self._volumeQLE)

    def setScan(self, scan: None | TomwerScanBase):
        if scan is None:
            self._scanQLE.clear()
        else:
            assert isinstance(
                scan, TomwerScanBase
            ), f"scan should be an instance of {TomwerScanBase}. Got {type(scan)}"
            self._scanQLE.setText(str(scan))
            self.setVolumes(volumes=scan.latest_vol_reconstructions)

    def setVolumes(self, volumes: tuple[str | VolumeIdentifier | TomwerVolumeBase]):
        """
        Display volume metadata. At the moment only display the identifier of the first reconstructed volume
        """
        self._volumeQLE.clear()
        if len(volumes) > 0:
            volume = volumes[0]
            if not isinstance(volume, TomwerVolumeBase):
                volume = VolumeFactory.create_tomo_object_from_identifier(volume)
            self._volumeQLE.setText(str(volume))
            self._volumeQLE.setToolTip(volume.data_url.file_path())

    def clear(self):
        self.setScan(None)


class _TomoApplicationContext(DataViewHooks):
    """
    Store the context of the application

    It overwrites the DataViewHooks to custom the use of the DataViewer for
    the silx view application.

    - Create a single colormap shared with all the views
    - Create a single colormap dialog shared with all the views
    """

    def __init__(self, parent, settings=None):
        self.__parent = weakref.ref(parent)
        self.__defaultColormap = Colormap(name="gray")
        self.__defaultColormapDialog = None
        self.__settings = settings
        self.__recentFiles = []

    def getSettings(self) -> qt.QSettings:
        """Returns actual application settings."""
        return self.__settings

    def restoreLibrarySettings(self):
        """Restore the library settings, which must be done early"""
        settings = self.__settings
        if settings is None:
            return
        settings.beginGroup("library")
        plotBackend = settings.value("plot.backend", "")
        plotImageYAxisOrientation = settings.value("plot-image.y-axis-orientation", "")
        settings.endGroup()

        if plotBackend != "":
            silx.config.DEFAULT_PLOT_BACKEND = plotBackend
        if plotImageYAxisOrientation != "":
            silx.config.DEFAULT_PLOT_IMAGE_Y_AXIS_ORIENTATION = (
                plotImageYAxisOrientation
            )

    def restoreSettings(self):
        """Restore the settings of all the application"""
        settings = self.__settings
        if settings is None:
            return
        parent = self.__parent()
        parent.restoreSettings(settings)

        settings.beginGroup("colormap")
        byteArray = settings.value("default", None)
        if byteArray is not None:
            try:
                colormap = Colormap()
                colormap.restoreState(byteArray)
                self.__defaultColormap = colormap
            except Exception:
                _logger.debug("Backtrace", exc_info=True)
        settings.endGroup()

        self.__recentFiles = []
        settings.beginGroup("recent-files")
        for index in range(1, 10 + 1):
            if not settings.contains("path%d" % index):
                break
            filePath = settings.value("path%d" % index)
            self.__recentFiles.append(filePath)
        settings.endGroup()

    def saveSettings(self):
        """Save the settings of all the application"""
        settings = self.__settings
        if settings is None:
            return
        parent = self.__parent()
        parent.saveSettings(settings)

        if self.__defaultColormap is not None:
            settings.beginGroup("colormap")
            settings.setValue("default", self.__defaultColormap.saveState())
            settings.endGroup()

        settings.beginGroup("library")
        settings.setValue("plot.backend", silx.config.DEFAULT_PLOT_BACKEND)
        settings.setValue(
            "plot-image.y-axis-orientation",
            silx.config.DEFAULT_PLOT_IMAGE_Y_AXIS_ORIENTATION,
        )
        settings.endGroup()

        settings.beginGroup("recent-files")
        for index in range(0, 11):
            key = "path%d" % (index + 1)
            if index < len(self.__recentFiles):
                filePath = self.__recentFiles[index]
                settings.setValue(key, filePath)
            else:
                settings.remove(key)
        settings.endGroup()

    def getRecentFiles(self) -> list[str]:
        """Returns the list of recently opened files.

        The list is limited to the last 10 entries. The newest file path is
        in first.
        """
        return self.__recentFiles

    def pushRecentFile(self, filePath: str):
        """Push a new recent file to the list.

        If the file is duplicated in the list, all duplications are removed
        before inserting the new filePath.

        If the list becan bigger than 10 items, oldest paths are removed.

        :param filePath: File path to push
        """
        # Remove old occurencies
        self.__recentFiles[:] = (f for f in self.__recentFiles if f != filePath)
        self.__recentFiles.insert(0, filePath)
        while len(self.__recentFiles) > 10:
            self.__recentFiles.pop()

    def clearRencentFiles(self):
        """Clear the history of the recent files."""
        self.__recentFiles[:] = []

    def getColormap(self, view) -> Colormap:
        """Returns a default colormap.

        Override from DataViewHooks
        """
        if self.__defaultColormap is None:
            self.__defaultColormap = Colormap(name="viridis")
        return self.__defaultColormap

    def getColormapDialog(self, view) -> ColormapDialog:
        """Returns a shared color dialog as default for all the views.

        Override from DataViewHooks
        """
        if self.__defaultColormapDialog is None:
            parent = self.__parent()
            if parent is None:
                return None
            dialog = ColormapDialog(parent=parent)
            dialog.setModal(False)
            self.__defaultColormapDialog = dialog
        return self.__defaultColormapDialog


class VolumeViewer(qt.QMainWindow, BaseResourceObserver):
    def __init__(self, parent):
        super().__init__(parent)

        self._volume_loaded_in_background = (None, None)
        # store the volume loaded in the background and the thread used for it as (volume_identifier, thread)
        self._centralWidget = DataViewerFrame(parent=self)
        self.__context = _TomoApplicationContext(self)
        self._centralWidget.setGlobalHooks(self.__context)
        self._centralWidget.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding
        )
        self.setCentralWidget(self._centralWidget)
        # waiter overlay to notify user loading is on-going
        self._waitingOverlay = WaitingOverlay(self._centralWidget)
        self._waitingOverlay.setIconSize(qt.QSize(30, 30))
        self._waitingOverlay.hide()

        # display scan information when possible
        self._infoWidget = _ScanInfo(parent=self)

        # top level dock widget to display information regarding the scan
        # and volume
        self._dockInfoWidget = qt.QDockWidget(parent=self)
        self._dockInfoWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._dockInfoWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._dockInfoWidget.setWidget(self._infoWidget)
        self.addDockWidget(qt.Qt.TopDockWidgetArea, self._dockInfoWidget)

        # add dock widget for reconstruction parameters
        self._reconsInfoDockWidget = qt.QDockWidget(parent=self)
        self._reconsWidgetScrollArea = qt.QScrollArea(self)
        self._reconsWidgetScrollArea.setWidgetResizable(True)
        self._reconsWidget = ReconstructionParameters(self)
        self._reconsWidgetScrollArea.setWidget(self._reconsWidget)
        self._reconsInfoDockWidget.setWidget(self._reconsWidgetScrollArea)
        self._reconsInfoDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._reconsInfoDockWidget)

        self._h5_file = None
        """pointer to the hdf5 file since we want to set the HDF5Dataset for
        loading data on the fly and avoid loading everything into memory for
        hdf5."""
        self.__last_mode = None
        # register the viewer as observer of the HDF5 volume (handle resource conflict)
        HDF5VolumeManager.register(self)

    def _close_h5_file(self):
        if self._h5_file is not None:
            self._h5_file.close()
        self._h5_file = None

    def close(self):
        HDF5VolumeManager.unregister(self)
        self._close_h5_file()
        super().close()

    def release_resource(self, resource: str):
        if self._h5_file is not None and resource in (
            self._h5_file.filename,
            os.path.abspath(self._h5_file.filename),
        ):
            _logger.warning(
                f"{resource} about to be overwrite. Closing resource and cleaning plot."
            )
            self._close_h5_file()
            self.clear()

    def setScan(self, scan):
        self.clear()
        if scan is None:
            return

        elif len(scan.latest_vol_reconstructions) == 0:
            _logger.warning(f"No reconstructed volume for {scan}")
            self._infoWidget.setScan(scan)
        else:
            self._set_volumes(volumes=scan.latest_vol_reconstructions)
            self._infoWidget.setScan(scan)

    def setVolume(self, volume):
        self.clear(clear_infos=False)
        if volume is None:
            return
        self._set_volumes(volumes=(volume,))
        self._infoWidget.setVolumes((volume,))

    def _get_data_volume(self, volume: TomwerVolumeBase):
        """
        load the data of the requested volume.
        :return: (data: str | None, state: str) state can be "loaded", "loading" or "failed"
        """
        if not isinstance(volume, TomwerVolumeBase):
            raise TypeError(
                f"volume is expected to be an instance of {TomwerVolumeBase}. Not {type(volume)}"
            )

        self._close_h5_file()
        if isinstance(volume, HDF5Volume):
            try:
                self._h5_file = h5py.File(volume.data_url.file_path(), mode="r")
            except OSError:
                self._h5_file = h5py.File(
                    volume.data_url.file_path(),
                    mode="r",
                    libver="latest",
                    swmr=True,
                )
            if volume.data_url.data_path() in self._h5_file:
                data = self._h5_file[volume.data_url.data_path()]
                state = "loaded"
            else:
                data = None
                state = "failed"
        elif volume.data is not None:
            data = volume.data
            state = "loaded"
        else:
            volume_id, _ = self._volume_loaded_in_background
            if volume_id == volume.get_identifier().to_str():
                # special case if the user send several time the volume which is currently loading
                # in this case we just want to ignore the request to avoid reloading the volume
                # can happen in the case of a large volume that take some time to be loaded.
                pass
            else:
                _logger.warning(
                    "Attempt to set a non HDF5 volume to the viewer. This requires to load all the data in memory. This can take a while"
                )
                self._stopExistingLoaderThread()
                self._loadAndDisplay(volume)
            state = "loading"
            data = None

        return data, state

    def _loaderThreadFinished(self):
        """Callback activated when a VolumeLoader thread is finished"""
        sender = self.sender()
        if not isinstance(sender, VolumeLoader):
            raise TypeError("sender is expected to be a VolumeLoader")

        self._stopExistingLoaderThread()
        if sender.volume.data is None:
            _logger.error(f"Failed to load volume {sender.volume.get_identifier()}")
        elif sender.volume is not None:
            self.setVolume(sender.volume)

    def _loadAndDisplay(self, volume):
        """Load a thread and add a callback when loading is done"""
        loader_thread = VolumeLoader(volume=volume)
        self._volume_loaded_in_background = (
            volume.get_identifier().to_str(),
            loader_thread,
        )
        loader_thread.finished.connect(self._loaderThreadFinished)
        loader_thread.start()

    def _stopExistingLoaderThread(self):
        """Will stop any existing loader thread. Make sure we load one volume at most at the time"""
        _, loader_thread = self._volume_loaded_in_background
        if loader_thread is not None:
            loader_thread.finished.disconnect(self._loaderThreadFinished)
            if loader_thread.isRunning():
                loader_thread.quit()
            self._volume_loaded_in_background = (None, None)

    def _set_volumes(self, volumes: tuple):
        self.clear()
        # for now handle a single volume
        if len(volumes) == 0:
            pass
        else:
            if len(volumes) > 1:
                _logger.warning(
                    "Only one volume can be displayed. Will display the first one"
                )
            volume = volumes[0]
            if isinstance(volume, (str, VolumeIdentifier)):
                volume = VolumeFactory.create_tomo_object_from_identifier(volume)
            elif isinstance(volume, TomwerVolumeBase):
                pass
            else:
                raise TypeError(
                    f"Volume should be an instance of a Volume, a VolumeIdentifier or a string refering to a VolumeIdentifier. {type(volume)} provided"
                )

            # warning: load metadata before data because can get some conflict with the HDF5 reader flag if done after
            try:
                # warning: limitation expected for .vol as it gets two configuration file. The default one is vol.info and does not contains
                # any of the metadata 'distance', 'pixel size'... but it is here for backward compatiblity
                self._reconsWidget.setVolumeMetadata(
                    volume.metadata or volume.load_metadata()
                )
            except Exception as e:
                _logger.info(
                    f"Unable to set reconstruction parameters from {volume.data_url}. Not handled for pyhst reconstructions. Error is {e}"
                )

            data, state = self._get_data_volume(volume)
            # set volume dataset
            if state == "loading":
                self._waitingOverlay.show()
            elif state == "loaded":
                self._waitingOverlay.hide()
                if data is not None:
                    self._set_volume(data)

            elif state == "failed":
                _logger.warning(
                    f"Failed to load data from {volume.get_identifier().to_str()}"
                )
                return

    def _set_volume(self, volume: numpy.ndarray | h5py.Dataset):
        self._centralWidget.setData(volume)
        self._centralWidget.setDisplayMode(self.__last_mode or IMAGE_MODE)

    def clear(self, clear_infos=True):
        if self._centralWidget.displayMode():
            self.__last_mode = self._centralWidget.displayMode()
        self._close_h5_file()
        if clear_infos:
            self._infoWidget.clear()
        self._centralWidget.setData(None)
        # if clear stop loading any volume
        self._stopExistingLoaderThread()

    def sizeHint(self):
        return qt.QSize(600, 600)


class VolumeLoader(qt.QThread):
    """
    simple thread that load a volume in memory
    """

    def __init__(self, volume: TomwerVolumeBase) -> None:
        super().__init__()
        if not isinstance(volume, TomwerVolumeBase):
            raise TypeError()
        self.__volume = volume

    def run(self):
        self.__volume.load_data(store=True)

    @property
    def volume(self):
        return self.__volume
