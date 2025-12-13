# coding: utf-8
from __future__ import annotations


from silx.gui import qt

from tomwer.core.process.control.scantransfer import (
    ScanTransferTask as FolderTransfertP,
)
from tomwer.core.scan.scanbase import TomwerScanBase


class ScanTransfer(qt.QObject, FolderTransfertP):
    scanready = qt.Signal(TomwerScanBase)
    """emit when scan ready"""

    def __init__(self, parent=None, inputs=None, varinfo=None):
        qt.QObject.__init__(self, parent)
        FolderTransfertP.__init__(self, varinfo=varinfo, inputs=inputs)
