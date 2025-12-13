# coding: utf-8
from __future__ import annotations


import logging

from tomwer.gui.control.datalist import VolumeList
from tomwer.gui.dialog.QVolumeDialog import QVolumeDialog

from .selectorwidgetbase import _SelectorWidget

logger = logging.getLogger(__name__)


class VolumeSelectorWidget(_SelectorWidget):
    """Widget used to select a volume on a list"""

    def _buildDataList(self):
        return VolumeList(self)

    def _callbackAddData(self):
        dialog = QVolumeDialog(self)

        if not dialog.exec():
            dialog.close()
            return

        volume = dialog.getVolume()
        if volume is not None:
            added_objs = self.add(volume)
            self.setMySelection(added_objs)
        self.sigUpdated.emit()
