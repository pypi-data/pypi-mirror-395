from __future__ import annotations

import fnmatch
import logging
import os

import h5py
from orangewidget import gui, widget
from orangewidget.widget import Output
from silx.gui import qt
from orangewidget.settings import Setting

import tomwer.core.process.control.datadiscovery
from orangecontrib.tomwer.widgets.utils import WidgetLongProcessing
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.scan.scantype import ScanType
from tomwer.gui.control.datadiscovery import DataDiscoveryWidget

logger = logging.getLogger(__name__)


class DataDiscoveryOW(widget.OWBaseWidget, WidgetLongProcessing, openclass=True):
    """
    This widget will browse a folder and sub folder to find valid tomo scan project.
    Contrary to the scan watcher it will parse all folder / sub folders then stop.
    """

    name = "scan discovery"
    id = "orangecontrib.widgets.tomwer.control.DataDiscoveryOW.DataDiscoveryOW"
    description = (
        "This widget will browse a folder and sub folder to find valid tomo scan project. \n"
        "Contrary to the scan watcher it will parse all folder / sub folders then stop."
    )
    icon = "icons/datadiscover.svg"
    priority = 11
    keywords = [
        "tomography",
        "tomwer",
        "datadiscovery",
        "data",
        "discovery",
        "search",
        "research",
        "hdf5",
        "NXtomo",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    ewokstaskclass = tomwer.core.process.control.datadiscovery._DataDiscoveryPlaceHolder

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")

    settings = Setting(dict())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = DataDiscoveryWidget(parent=self)

        self._box = gui.vBox(self.mainArea, self.name)
        layout = self._box.layout()
        layout.addWidget(self._widget)

        self._widget.setConfiguration(self.settings)

        # getting ready for processing
        self._processingThread = _DiscoverThread()

        # connect signal / slot
        self._processingThread.sigDataFound.connect(self._sendData)
        self._processingThread.finished.connect(self._endProcessing)
        self._widget.widget.controlWidget._qpbstartstop.released.connect(
            self._switchObservation
        )
        # dedicated one for settings
        self._widget.widget.controlWidget._filterQLE.editingFinished.connect(
            self._updatesettings
        )
        self._widget.widget.controlWidget._qteFolderSelected.editingFinished.connect(
            self._updatesettings
        )
        self._widget.widget.configWidget.sigScanTypeChanged.connect(
            self._updatesettings
        )

    def _updatesettings(self):
        self.settings = self.getConfiguration()

    # expose some API
    def getConfiguration(self) -> dict:
        return self._widget.getConfiguration()

    def setConfiguration(self, config: dict):
        self._widget.setConfiguration(config)

    def getProcessingThread(self) -> qt.QThread:
        return self._processingThread

    def setFolderObserved(self, dir_: str):
        self._widget.widget.setFolderObserved(dir_)

    def setSearchScanType(self, scan_type):
        self._widget.widget.setSearchScanType(scan_type)

    def setFilePattern(self, pattern: str | None):
        self._widget.widget.setLinuxFilePattern(pattern)

    def _switchObservation(self, *args, **kwargs):
        """stop or start the disceovery according to the thread state"""
        thread = self.getProcessingThread()
        if thread.isRunning():
            thread.quit()
            self._endProcessing()
        else:
            self.start_discovery()

    def start_discovery(self, wait: int | None = None):
        """start the discovery of scans
        :param wait: optional waiting time in second
        """
        thread = self.getProcessingThread()
        if thread.isRunning():
            logger.warning("Discovery is already running")
            return
        self._startProcessing()
        thread.setConfiguration(self.getConfiguration())
        thread.start()
        if wait is not None:
            thread.wait(wait)

    def _sendData(self, data):
        if data is not None:
            self.Outputs.data.send(data)

    def _startProcessing(self, *args, **kwargs):
        self._widget.widget.controlWidget._qpbstartstop.setText("stop discovery")
        return super()._startProcessing(*args, **kwargs)

    def _endProcessing(self, *args, **kwargs):
        self._widget.widget.controlWidget._qpbstartstop.setText("start discovery")
        return super()._endProcessing(*args, **kwargs)


class _DiscoverThread(qt.QThread):
    """
    Thread to browse folder and sub folder and looking for some scan
    """

    sigDataFound = qt.Signal(object)
    """emit each time a new dataset is found"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._root_dir = None
        self._research_type = None
        self._file_filter = None
        self._look_for_hdf5 = False

    def setConfiguration(self, config: dict):
        self._root_dir = config.get("start_folder", None)
        self._research_type = ScanType(config["scan_type_searched"])
        self._file_filter = config.get("file_filter", None)
        self._look_for_hdf5 = self._research_type in (
            ScanType.BLISS,
            ScanType.NX_TOMO,
        )

    def run(self):
        if self._research_type is None:
            logger.error("No reserach type defined. Cannot research scan")
        elif not os.path.isdir(self._root_dir):
            logger.error(f"{self._root_dir} is not a directory")
        else:
            self.discover_scan(file_path=self._root_dir)

    def discover_scan(self, file_path):
        if (
            os.path.isfile(file_path)
            and self._look_for_hdf5
            and h5py.is_hdf5(file_path)
        ) or (os.path.isdir(file_path) and not self._look_for_hdf5):
            try:
                name_match = self._file_filter is None or fnmatch.fnmatch(
                    os.path.basename(file_path), self._file_filter
                )
            except Exception as e:
                logger.error(f"fnmatch fail. Error is {e}")
                name_match = True
            if name_match:
                self._treat_path(file_path)
        if os.path.isdir(file_path):
            [
                self.discover_scan(file_path=os.path.join(file_path, file_))
                for file_ in os.listdir(file_path)
            ]

    def _treat_path(self, folder_path: str):
        """treat file / folder at a specific location"""
        try:
            scan_objs = ScanFactory.create_scan_objects(
                scan_path=folder_path,
                accept_bliss_scan=(self._research_type == ScanType.BLISS),
            )
        except Exception as e:
            logger.info(f"Fail to treat {folder_path}. Error is {e}")
        else:
            for scan in scan_objs:
                if (
                    isinstance(scan, BlissScan)
                    and self._research_type is ScanType.BLISS
                ):
                    self.sigDataFound.emit(scan)
                elif (
                    isinstance(scan, NXtomoScan)
                    and self._research_type is ScanType.NX_TOMO
                ):
                    self.sigDataFound.emit(scan)
                elif (
                    isinstance(scan, EDFTomoScan)
                    and self._research_type is ScanType.SPEC
                ):
                    self.sigDataFound.emit(scan)
                else:
                    raise NotImplementedError("case not handled", self._research_type)
