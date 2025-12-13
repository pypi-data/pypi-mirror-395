"""Some widget construction to check if a sample moved"""

from __future__ import annotations

import logging

import sys
import h5py
from silx.gui import qt
from silx.io.url import DataUrl

from .metadataloader import VolumeMetadataLoader
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.io.utils.tomoobj import get_tomo_objs_instances
from tomwer.gui.dialog.QDataDialog import QDataDialog
from tomwer.gui.stackplot import QImageFileStackPlot
from tomwer.gui.utils.loadingmode import LoadingModeToolButton, LoadingMode

_logger = logging.getLogger(__name__)


class _ImageStack(qt.QMainWindow):
    """
    Base class to :class:`SliceStack` and :class:`RadioStack` classes.
    Define the common layout and interaction.
    """

    METADATA_LOADER_CLASS = None

    SHOW_SCAN_OVERVIEW = True

    SHOW_VOLUME_METADATA_OVERVIEW = True

    sigMetadataLoaded = qt.Signal()

    def __init__(self, parent=None, backend=None):

        super().__init__(parent)

        self.setWindowFlags(qt.Qt.Widget)
        self._viewer = QImageFileStackPlot(
            parent=self, backend=backend, show_overview=self.SHOW_SCAN_OVERVIEW
        )
        if not self.SHOW_VOLUME_METADATA_OVERVIEW:
            self._viewer._reconsInfoDockWidget.hide()
        self.setCentralWidget(self._viewer)

        self._actionsToolbar = qt.QToolBar()
        self.addToolBar(qt.Qt.RightToolBarArea, self._actionsToolbar)

        self._clearAction = _ClearAction(parent=self._actionsToolbar)
        self._actionsToolbar.addAction(self._clearAction)
        self._clearAction.triggered.connect(self.clear)

        self._addTomoObjAction = _AddTomoObjectAction(parent=self._actionsToolbar)
        self._actionsToolbar.addAction(self._addTomoObjAction)
        self._addTomoObjAction.triggered.connect(self._callbackAddNewTomoObjFrmDialog)

        self._loadingMode = LoadingModeToolButton(parent=self)
        self._actionsToolbar.addWidget(self._loadingMode)

        # connect signal / slot
        self.sigMetadataLoaded.connect(self._viewer._updateUrlInfos)
        self._loadingMode.sigLoadModeChanged.connect(self.setLoadingMode)

    def addTomoObj(self, tomo_obj: TomwerObject | str):
        raise NotImplementedError

    def _callbackAddNewTomoObjFrmDialog(self) -> None:

        dialog = QDataDialog(self, multiSelection=True)
        dialog.setNameFilters(
            [
                "Any files (*)",
                "HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                "Nexus files (*.nx *.nxs *.nexus)",
            ]
        )

        if not dialog.exec():
            dialog.close()
            return

        self._addTomoObjectsFromStrList(dialog.files_selected())

    def _addTomoObjectsFromStrList(self, str_list: list[str]) -> None:
        tomo_objects, _ = get_tomo_objs_instances(str_list)
        for tomo_obj in tomo_objects:
            self.addTomoObj(tomo_obj)

    def clear(self):
        self._viewer.reset()

    def close(self) -> None:
        # clearing free the loading thread. Safer to remove them when closing
        self.clear()
        super().close()

    def setLoadingMode(self, mode: LoadingMode | str) -> None:
        mode = LoadingMode(mode)
        if mode is LoadingMode.LAZY_LOADING:
            # set to the default N_PRELOAD value
            n_prefetch = self._viewer.N_PRELOAD
        else:
            n_prefetch = sys.maxsize
        self._viewer.setNPrefetch(n_prefetch)


class _ClearAction(qt.QAction):
    def __init__(self, parent):
        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        qt.QAction.__init__(self, icon, "Clear", parent)


class _AddTomoObjectAction(qt.QAction):
    def __init__(self, parent):
        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_DirIcon)
        qt.QAction.__init__(self, icon, "Add tomo object", parent)


class SliceStack(_ImageStack):
    """
    Widget displaying all slices contained in a list of acquisition folder
    """

    SHOW_SCAN_OVERVIEW = False

    SHOW_VOLUME_METADATA_OVERVIEW = True

    METADATA_LOADER_CLASS = VolumeMetadataLoader

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)
        self._loadingMetadataThreads = []
        "list of thread processing metadata loading"
        self._volume_id_to_urls: dict[str, tuple[DataUrl]] = {}
        # allow user to edit the list (user can remove an url)
        url_list = self._viewer._urlsTable._urlsTable
        url_list.setEditable(True)
        # allow multiple selection (more convenient when users want to remove a set of url)
        # not for now: seems to have a bug on it
        # url_list.setSelectionMode(qt.QAbstractItemView.MultiSelection)

    @property
    def url_to_volume_id(self, volume_id) -> str | None:
        urls_to_volume_id = {
            (value, key) for key, value in self._volume_id_to_urls.items()
        }
        return urls_to_volume_id.get(volume_id, None)

    def getImagesUrls(self) -> dict[str, dict]:
        """
        Parse all self._scans and find the images to be displayed on the widget

        :return: images to display for each scan. Key is the volume identifier, value is a dict
                 with index as key and DataUrl as value
        """
        slices = {}
        for volume in self._tomoObjects.values():
            assert isinstance(volume, TomwerVolumeBase)
            slices[volume.get_identifier().to_str()] = tuple(volume.browse_data_urls())
        return slices

    def __tomoObjIdToInstance(self, tomo_obj: TomwerObject | str) -> TomwerObject:
        """Convert a tomo obj to it TomwerObject"""
        if isinstance(tomo_obj, str):
            try:
                tomo_obj = VolumeFactory.create_tomo_object_from_identifier(tomo_obj)
            except (ValueError, TypeError) as e1:
                try:
                    tomo_obj = ScanFactory.create_tomo_object_from_identifier(tomo_obj)
                except (ValueError, TypeError) as e2:
                    raise ValueError(
                        f"Unable to create a tomo object from {tomo_obj}. Errors are {e1}, {e2}"
                    )
        return tomo_obj

    def addTomoObj(self, tomo_obj: TomwerObject | str):
        tomo_obj = self.__tomoObjIdToInstance(tomo_obj=tomo_obj)

        if isinstance(tomo_obj, TomwerScanBase):
            reconstructed_volumes = (
                tomo_obj.latest_reconstructions or tomo_obj.get_reconstructed_slices()
            )
            for volume_id in reconstructed_volumes:
                if isinstance(volume_id, str):
                    volume_id_as_str = volume_id
                elif isinstance(volume_id, TomwerVolumeBase):
                    volume_id_as_str = volume_id.get_identifier().to_str()
                else:
                    volume_id_as_str = volume_id.to_str()
                self.addTomoObj(tomo_obj=volume_id_as_str)
        elif isinstance(tomo_obj, TomwerVolumeBase):
            self._addVolume(volume=tomo_obj)
            # set the latest slice as the active one
            try:
                active_url = next(tomo_obj.browse_data_urls())
            except StopIteration:
                pass
            else:
                try:
                    self._viewer.setCurrentUrl(active_url)
                except Exception:
                    # the url might not exist or might have been removed.
                    # Because each tome we add an object the urls are reset
                    # FIXME: in this case the urls must be updated instead of resetting
                    pass
        else:
            raise TypeError(f"tomo obj type is not handled ({type(tomo_obj)})")

    def _addVolume(self, volume: TomwerVolumeBase):
        new_urls = [url.path() for url in volume.browse_data_urls()]
        self._volume_id_to_urls[volume.get_identifier().to_str()] = tuple(new_urls)
        self._loadMetadata(volume)

        # work around. See issue: TODO add silx issue
        if self._viewer._urlIndexes is None:
            current_urls = tuple()
        else:
            current_urls = self._viewer.getUrls() or tuple()
        updated_urls = {*new_urls} | {*current_urls}
        updated_urls = tuple([DataUrl(path=url_path) for url_path in updated_urls])
        self._viewer.setUrls(updated_urls)

    def setCurrentUrl(self, url: DataUrl):
        if url in ("", None):
            url = None
        elif isinstance(url, str):
            url = DataUrl(path=url)
        elif not isinstance(url, DataUrl):
            raise TypeError
        if url is None:
            pass
            # FIXME: add a function to clear the metadata widget
        super().setCurrentUrl(url)

    # metadata loading
    def _load(self, url: DataUrl):
        # load the frame
        super()._load()
        # load metadata
        url_path = url.path()
        volume_id = self.url_to_volume_id(url_path)
        if volume_id is None:
            _logger.warning(f"Failed to find volume associated to {url_path}")
            return

        volume = VolumeFactory.create_tomo_object_from_identifier(volume_id)
        if volume not in self._loadingMetadataThreads:
            # if a thread is already loading metadata for this volume avoid launching another thread for it
            self._loadMetadata(tomo_obj=volume)

    def _loadMetadata(self, tomo_obj: TomwerObject):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"volume should be an instance of {TomwerObject}. Got {type(tomo_obj)} instead"
            )
        loader = self.METADATA_LOADER_CLASS(
            tomo_obj_identifier=tomo_obj.get_identifier().to_str(), parent=self
        )
        loader.finished.connect(self._metadataLoaded, qt.Qt.QueuedConnection)
        self._loadingMetadataThreads.append(loader)
        loader.start()

    def _metadataLoaded(self):
        sender = self.sender()
        if sender in self._loadingMetadataThreads:
            self._loadingMetadataThreads.remove(sender)
        self._viewer.updateSliceMetadata(
            {url.path(): sender.metadata for url in sender.volume.browse_data_urls()}
        )
        self.sigMetadataLoaded.emit()

    def _freeMetadataLoadingThreads(self):
        for thread in self._loadingMetadataThreads:
            thread.blockSignals(True)
            thread.wait(50)
        self._loadingMetadataThreads.clear()

    def close(self):
        # clearing free the loading thread. Safer to remove them when closing
        self._freeMetadataLoadingThreads()
        super().close()

    def clear(self):
        self._volume_id_to_urls.clear()
        self._freeMetadataLoadingThreads()
        super().clear()


class RadioStack(_ImageStack):
    """
    Widget displaying all radio contained in a list of acquisition folder
    """

    SHOW_SCAN_OVERVIEW = True

    SHOW_VOLUME_METADATA_OVERVIEW = False

    def getImagesUrls(self) -> dict:
        """
        Parse all self._scans and find the images to be displayed on the widget

        :return: images to display for each scan
        """
        slices = {}
        for scan in self._tomoObjects.values():
            # manage hdf5
            if isinstance(scan, TomwerScanBase):
                imgs = scan.projections
                if len(imgs) > 0:
                    slices[str(scan)] = imgs
            elif h5py.is_hdf5(scan):
                try:
                    scans = ScanFactory.create_scan_objects(scan_path=scan)
                except Exception as e:
                    _logger.warning(e)
                else:
                    for scan_ in scans:
                        imgs = scan_.projections
                        if len(imgs) > 0:
                            slices[str(scan_)] = imgs
            else:
                # manage edf
                try:
                    scan_ = ScanFactory.create_scan_object(scan_path=scan)
                except ValueError:
                    pass
                else:
                    imgs = scan_.projections
                    if len(imgs) > 0:
                        slices[scan] = imgs
        return slices

    def addTomoObj(self, tomo_obj: TomwerScanBase | str):
        if isinstance(tomo_obj, str):
            try:
                tomo_obj = ScanFactory.create_tomo_object_from_identifier(tomo_obj)
            except (ValueError, TypeError) as e:
                _logger.error(
                    f"Fail to create a scan object from {tomo_obj}. Error is {e}"
                )
        if not isinstance(tomo_obj, TomwerScanBase):
            raise TypeError(
                f"tomo_obj should be an instance of {TomwerScanBase}. Get {type(tomo_obj)}"
            )
        self._addScan(scan=tomo_obj)
        self._viewer.updateScanToUrl(
            {url.path(): tomo_obj for url in tomo_obj.projections.values()}
        )

    def _addScan(self, scan: TomwerScanBase):
        new_urls = tuple([url.path() for url in scan.projections.values()])

        # work around. See issue: TODO add silx issue
        if self._viewer._urlIndexes is None:
            current_urls = tuple()
        else:
            current_urls = self._viewer.getUrls() or tuple()
        updated_urls = {*new_urls} | {*current_urls}
        updated_urls = tuple([DataUrl(path=url_path) for url_path in updated_urls])
        self._viewer.setUrls(updated_urls)
