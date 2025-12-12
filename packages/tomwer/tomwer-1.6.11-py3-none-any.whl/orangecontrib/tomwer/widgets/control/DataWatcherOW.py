from __future__ import annotations

import functools
import logging

from orangewidget import gui, widget
from orangewidget.settings import Setting
from orangewidget.widget import Output

import tomwer.core.process.control.datawatcher.datawatcher
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.control.datawatcher import DataWatcherWidget

from ..utils import WidgetLongProcessing

logger = logging.getLogger(__name__)


class DataWatcherOW(widget.OWBaseWidget, WidgetLongProcessing, openclass=True):
    """
    This widget is used to observe a selected folder and his sub-folders to
    detect if they are containing valid-finished acquisitions.
    """

    name = "scan watcher"
    id = "orangecontrib.widgets.tomwer.datawatcherwidget.DataWatcherOW"
    description = (
        "The widget will observe folder and sub folders of a given"
        " path and waiting for acquisition to be ended."
        " The widget will infinitely wait until an acquisition is "
        "ended. If an acquisition is ended then a signal "
        "containing the folder path is emitted."
    )
    icon = "icons/datawatcher.svg"
    priority = 12
    keywords = ["tomography", "file", "tomwer", "observer", "datawatcher"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    folderObserved = Setting(str())

    acquisitionMethod = Setting(tuple())

    linuxFilePatternSetting = Setting(str())

    DEFAULT_DIRECTORY = "/lbsram/data/visitor"

    ewokstaskclass = (
        tomwer.core.process.control.datawatcher.datawatcher.DataWatcherEwoksTask
    )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)
        bliss_scan = Output(
            name="bliss data", type=BlissScan, doc="bliss scan to be process"
        )

    def __init__(self, parent=None, displayAdvancement=True):
        """Simple class which will check advancement state of the acquisition
        for a specific folder

        :param parent: the parent widget
        """
        widget.OWBaseWidget.__init__(self, parent)
        WidgetLongProcessing.__init__(self)
        self._widget = DataWatcherWidget(parent=self)
        self._widget.setFolderObserved(self.folderObserved)

        self._box = gui.vBox(self.mainArea, self.name)
        layout = self._box.layout()
        layout.addWidget(self._widget)

        # signal / slot connection
        self._widget.sigFolderObservedChanged.connect(self._updateSettings)
        self._widget.sigObservationModeChanged.connect(self._updateSettings)
        self._widget.sigObservationModeChanged.connect(self._setObsMethod)
        self._widget.sigFilterFileNamePatternChanged.connect(
            self._saveFilterLinuxPattern
        )
        self._widget.sigFilterFileNamePatternChanged.connect(
            self._widget.setLinuxFilePattern
        )
        self._widget.sigScanReady.connect(self._sendSignal)
        callback_start = functools.partial(self.processing_state, True, "watching on")
        self._widget.sigObservationStart.connect(callback_start)
        callback_end = functools.partial(self.processing_state, False, "watching off")
        self._widget.sigObservationEnd.connect(callback_end)
        self._loadSettings()

    def _loadSettings(self):
        if self.acquisitionMethod != tuple():
            self.widget.getConfigWindow().setMode(self.acquisitionMethod)
        if self.folderObserved != str():
            self.widget.setFolderObserved(self.folderObserved)
        if self.linuxFilePatternSetting != str():
            # for the GUI
            self.widget._filterQLE.setText(self.linuxFilePatternSetting)
            # for providing it to the processing thread. Bad design but this widget shouldn't be used that
            # much and modifying internals is not the priority.
            self.widget.setLinuxFilePattern(self.linuxFilePatternSetting)

    def _updateSettings(self):
        self.folderObserved = self.widget.getFolderObserved()
        mode = self.widget.getConfigWindow().getMode()
        if mode is not None:
            self.acquisitionMethod = mode
        self.linuxFilePatternSetting = self.widget.getLinuxFilePattern()

    def _saveFilterLinuxPattern(self, *args, **kwargs):
        linuxFilePattern = self.widget.getFilterLinuxFileNamePattern()
        if linuxFilePattern is None:
            self.linuxFilePatternSetting = ""
        else:
            self.linuxFilePatternSetting = linuxFilePattern

    def _setObsMethod(self, mode):
        self.widget.setObsMethod(mode)

    @property
    def widget(self):
        return self._widget

    @property
    def currentStatus(self):
        return self._widget.currentStatus

    @property
    def sigTMStatusChanged(self):
        return self._widget.sigTMStatusChanged

    def resetStatus(self):
        self._widget.resetStatus()

    def _sendSignal(self, scan):
        if scan is None:
            pass
        elif isinstance(scan, TomwerScanBase):
            self.Outputs.data.send(scan)
        elif isinstance(scan, BlissScan):
            self.Outputs.bliss_scan.send(scan)
        else:
            raise TypeError(
                f"output is expected to be a {TomwerScanBase} or a {BlissScan}"
            )

    def setFolderObserved(self, path):
        self.widget.setFolderObserved(path)

    def setObservation(self, b):
        self._widget.setObservation(b)

    def setTimeBreak(self, val):
        """
        Set the time break between two loop observation
        :param val: time (in sec)
        """
        self._widget.setWaitTimeBtwLoop(val)

    def startObservation(self):
        try:
            self.processing_info("processing")
        except Exception:
            pass
        self._widget.start()

    def stopObservation(self, succes=False):
        self.widget.stop(succes)
        try:
            self.Processing.clear()
        except Exception:
            pass

    def close(self):
        self.widget.close()
        super().close()
