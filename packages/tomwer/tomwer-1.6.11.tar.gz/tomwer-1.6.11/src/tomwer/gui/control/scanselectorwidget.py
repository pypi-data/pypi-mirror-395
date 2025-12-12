# coding: utf-8
from __future__ import annotations


import logging

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.control.datalist import GenericScanList
from tomwer.gui.dialog.QDataDialog import QDataDialog

from .selectorwidgetbase import _SelectorWidget

logger = logging.getLogger(__name__)


class ScanSelectorWidget(_SelectorWidget):
    """Widget used to select a scan on a list"""

    def _buildDataList(self):
        return GenericScanList(parent=self)

    def n_scan(self) -> int:
        return super().n_data()

    def _callbackAddData(self):
        dialog = QDataDialog(self, multiSelection=True)

        if not dialog.exec():
            dialog.close()
            return

        for folder in dialog.files_selected():
            tomo_objs = self.add(folder)
            self.setMySelection(tomo_objs)
        self.sigUpdated.emit()

    def setActiveData(self, data):
        if isinstance(data, TomwerScanBase):
            data = data.path
        super().setActiveData(data)
