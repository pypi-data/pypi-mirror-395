from __future__ import annotations

import logging

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output, OWBaseWidget
from silx.gui import qt

import tomwer.core.process.control.scanselector
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.control.scanselectorwidget import ScanSelectorWidget

logger = logging.getLogger(__name__)


class DataSelectorOW(OWBaseWidget, openclass=True):
    name = "scan selector"
    id = "orange.widgets.tomwer.scanselector"
    description = (
        "List all received scan. Then user can select a specific"
        "scan to be passed to the next widget."
    )
    icon = "icons/scanselector.svg"
    priority = 42
    keywords = ["tomography", "selection", "tomwer", "scan", "data"]

    ewokstaskclass = tomwer.core.process.control.scanselector._ScanSelectorPlaceHolder

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _scanIDs = Setting(list())

    class Inputs:
        data = Input(name="data", type=TomwerScanBase, multiple=True)

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        """ """
        super().__init__(parent)

        self.widget = ScanSelectorWidget(parent=self)
        self.widget.setWindowFlags(qt.Qt.Widget)
        self._loadSettings()

        self.widget.sigUpdated.connect(self._updateSettings)
        self.widget.sigSelectionChanged.connect(self.changeSelection)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)

    @Inputs.data
    def addScan(self, scan, *args, **kwargs):
        self.add(scan)

    def add(self, scan):
        if scan is not None:
            self.widget.add(scan=scan)

    def changeSelection(self, list_objs):
        if list_objs is None:
            return
        for obj_id in list_objs:
            item = self.widget.dataList._myitems.get(obj_id, None)
            if item:
                tomo_obj = item.data(qt.Qt.UserRole)
                assert isinstance(tomo_obj, TomwerScanBase)
                self.Outputs.data.send(tomo_obj)
            else:
                logger.error("%s not found in scan ids" % obj_id)

    def send(self):
        """send output signals for each selected items"""
        sItem = self.widget.dataList.selectedItems()
        if sItem and len(sItem) >= 1:
            selection = [
                _item.data(qt.Qt.UserRole).get_identifier().to_str() for _item in sItem
            ]
            self.changeSelection(list_objs=selection)

    def _loadSettings(self):
        for scan in self._scanIDs:
            assert isinstance(scan, str)
            # kept for backward compatibility since 0.11. To be removed on the future version.
            if "@" in scan:
                entry, file_path = scan.split("@")
                nxtomo_scan = NXtomoScan(entry=entry, scan=file_path)
                self.addScan(nxtomo_scan)
            else:
                self.addScan(scan)

    def _updateSettings(self):
        self._scanIDs = []
        for scan in self.widget.dataList._myitems:
            self._scanIDs.append(scan)

    def keyPressEvent(self, event):
        """
        Forward:
        * delete key (shortcut orange and make sure the `delete` key will be interpreted we need to overwrite this function)
        * Ctrl + A to select all the scan
        """
        modifiers = event.modifiers()
        key = event.key()

        if key == qt.Qt.Key_A and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self.widget.dataList.keyPressEvent(event)

        if key == qt.Qt.Key_Delete:
            self.widget.removeSelectedDatasets()
        else:
            super().keyPressEvent(event)

    # expose API
    def setActiveScan(self, data):
        self.widget.setActiveData(data=data)

    def selectAll(self):
        return self.widget.selectAll()

    def n_scan(self):
        return self.widget.n_scan()
