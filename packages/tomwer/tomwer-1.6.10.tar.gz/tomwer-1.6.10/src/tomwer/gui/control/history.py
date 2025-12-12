# coding: utf-8
from __future__ import annotations


from operator import itemgetter

from silx.gui import qt

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase


class ScanHistory(qt.QWidget):
    """Widget used to display the lastest discovered scans"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)

        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(qt.QLabel(""))

        self.scanHistory = qt.QTableView(parent=parent)
        self.scanHistory.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.scanHistory.setModel(
            _FoundScanModel(
                parent=self.scanHistory, header=("time", "type", "scan ID"), mlist={}
            )
        )
        self.scanHistory.resizeColumnsToContents()
        self.scanHistory.setSortingEnabled(True)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

        self.layout().addWidget(self.scanHistory)
        header = self.scanHistory.horizontalHeader()
        header.setSectionResizeMode(0, qt.QHeaderView.Fixed)
        header.setSectionResizeMode(1, qt.QHeaderView.Fixed)
        header.setSectionResizeMode(2, qt.QHeaderView.Stretch)
        header.setStretchLastSection(True)

    def update(self, scans):
        self.scanHistory.setModel(
            _FoundScanModel(
                parent=self, header=("time", "type", "scan ID"), mlist=scans
            )
        )
        self.scanHistory.resizeColumnsToContents()


class _FoundScanModel(qt.QAbstractTableModel):
    """
    Model for :class:_ScanHistory

    :param mlist: list of tuple (scan, time stamp)
    """

    def __init__(self, parent, header, mlist: list[tuple], *args):
        qt.QAbstractTableModel.__init__(self, parent, *args)
        self.header = header
        self.myList = mlist

    def rowCount(self, parent=None):
        if self.myList is None:
            return 0
        else:
            return len(self.myList)

    def columnCount(self, parent=None):
        return 3

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        if self.myList is None:
            return
        self.myList = sorted(list(self.myList), key=itemgetter(col))
        if order == qt.Qt.DescendingOrder:
            self.myList = list(reversed(sorted(list(self.myList), key=itemgetter(col))))

        self.layoutChanged.emit()

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != qt.Qt.DisplayRole:
            return None
        if index.column() == 0:
            return self.myList[index.row()][1].strftime("%a %m - %d - %Y   - %H:%M:%S")
        elif index.column() == 1:
            path = self.myList[index.row()][0]
            if isinstance(path, TomwerScanBase):
                return path.type
            elif isinstance(path, str) and path.startswith("hdf5 scan"):
                return "hdf5"
            elif NXtomoScan.directory_contains_scan(path) or "@" in path:
                return "hdf5"
            else:
                return "edf"
        elif index.column() == 2:
            return self.myList[index.row()][0]

    def headerData(self, col, orientation, role):
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            return self.header[col]
        return None
