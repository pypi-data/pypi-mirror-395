# coding: utf-8
from __future__ import annotations

import logging

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output, OWBaseWidget
from silx.gui import qt

import tomwer.core.process.control.volumeselector
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.gui.control.volumeselectorwidget import VolumeSelectorWidget

logger = logging.getLogger(__name__)


class VolumeSelectorOW(OWBaseWidget, openclass=True):
    name = "volume selector"
    id = "orange.widgets.tomwer.volumeselector"
    description = (
        "List all received volumes. Then user can select a specific"
        "volume to be passed to the next widget."
    )
    icon = "icons/volumeselector.svg"
    priority = 62
    keywords = ["tomography", "selection", "tomwer", "volume"]

    ewokstaskclass = (
        tomwer.core.process.control.volumeselector._VolumeSelectorPlaceHolder
    )

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _scanIDs = Setting(list())

    class Inputs:
        volume = Input(name="volume", type=TomwerVolumeBase, multiple=True)

    class Outputs:
        volume = Output(name="volume", type=TomwerVolumeBase)

    def __init__(self, parent=None):
        """ """
        super().__init__(parent)

        self.widget = VolumeSelectorWidget(parent=self)
        self._loadSettings()

        self.widget.sigUpdated.connect(self._updateSettings)
        self.widget.sigSelectionChanged.connect(self.changeSelection)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        # expose API
        self.setActiveScan = self.widget.setActiveData
        self.selectAll = self.widget.selectAll
        self.add = self.widget.add

    @Inputs.volume
    def _volumeReceived(self, volume, *args, **kwargs):
        self.addVolume(volume)

    def addVolume(self, volume):
        if volume is not None:
            self.widget.add(volume)

    def removeVolume(self, volume):
        if volume is not None:
            self.widget.remove(volume)

    def changeSelection(self, list_volume):
        if list_volume:
            for volume_id in list_volume:
                volume = self.widget.dataList.getVolume(volume_id, None)
                if volume is not None:
                    assert isinstance(volume, TomwerVolumeBase)
                    self.Outputs.volume.send(volume)
                else:
                    logger.error(f"{volume_id} not found the list")

    def send(self):
        """send output signals for each selected items"""
        sItem = self.widget.dataList.selectedItems()
        if sItem and len(sItem) >= 1:
            selection = [_item.text() for _item in sItem]
            self.changeSelection(list_volume=selection)

    def _loadSettings(self):
        for scan in self._scanIDs:
            assert isinstance(scan, str)
            # kept for backward compatibility since 0.11. To be removed on the future version.
            if "@" in scan:
                entry, file_path = scan.split("@")
                nxtomo_scan = NXtomoScan(entry=entry, scan=file_path)
                self.addVolume(nxtomo_scan)
            else:
                self.addVolume(scan)

    def _updateSettings(self):
        self._scanIDs = []
        for scan in self.widget.dataList._myitems:
            self._scanIDs.append(scan)

    def keyPressEvent(self, event):
        """
        To shortcut orange and make sure the `delete` key will be interpreted we need to overwrite this function
        """
        modifiers = event.modifiers()
        key = event.key()

        if key == qt.Qt.Key_A and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self.widget.dataList.keyPressEvent(event)

        if key == qt.Qt.Key_Delete:
            self.widget._callbackRemoveSelectedDatasets()
        else:
            super().keyPressEvent(event)
