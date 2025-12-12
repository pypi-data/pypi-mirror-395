# coding: utf-8
from __future__ import annotations


import os
import weakref
from collections import OrderedDict
from datetime import datetime

from silx.gui import qt

from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase

try:
    from processview.gui.utils.qitem_model_resetter import qitem_model_resetter
except ImportError:
    from tomwer.third_part.qitem_model_resetter import qitem_model_resetter


class ScanObservation(qt.QWidget):
    """
    Widget displayed the on-going observations (done by the data-listener)

    For each scan on-going we can display the following information:
    * time (when the scan has been discovered)
    * type: HDF5 or EDF
    * N projections: number of projections already acquired (a)
    * status of the scan (starting, on-going...)
    * acquisition: id of the scan (entry and data path in case of HDF5 scan)

    (a) the GUI was set up to display this information. Nevertheless this information is not provided by the rpc-call so this was never used.

    Context: when the 'data listener' gets triggered by bliss-tomo then we want to notify the user that a new scan is on-going.
    """

    HEADER = ("Time", "Type", "N Projections", "Status", "Acquisition")

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self._onGoingObservations = None
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(qt.QLabel(""))

        self.observationTable = qt.QTableView(parent=parent)
        self.observationTable.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.observationTable.setModel(
            _ObservedScanModel(parent=self.observationTable, header=self.HEADER)
        )
        self.observationTable.resizeColumnsToContents()
        self.observationTable.setSortingEnabled(True)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

        self.layout().addWidget(self.observationTable)
        header = self.observationTable.horizontalHeader()
        header.setSectionResizeMode(0, qt.QHeaderView.Fixed)
        header.setSectionResizeMode(1, qt.QHeaderView.Fixed)
        header.setSectionResizeMode(2, qt.QHeaderView.Fixed)
        header.setSectionResizeMode(3, qt.QHeaderView.Fixed)
        header.setSectionResizeMode(4, qt.QHeaderView.Stretch)
        header.setStretchLastSection(True)

        self.observationTable.setColumnWidth(0, 70)
        self.observationTable.setColumnWidth(1, 40)
        self.observationTable.setColumnWidth(2, 90)
        self.observationTable.setColumnWidth(3, 70)

    @property
    def onGoingObservations(self):
        if self._onGoingObservations:
            return self._onGoingObservations()
        else:
            return None

    def setOnGoingObservations(self, onGoingObservations):
        """
        will update the table to display the observations contained in
        onGoingObservations

        :param onGoingObservations: the obsevations observed to display
        """
        if self.onGoingObservations:
            self.onGoingObservations.sigObsAdded.disconnect(self.addObservation)
            self.onGoingObservations.sigObsRemoved.disconnect(self.removeObservation)
            self.onGoingObservations.sigObsStatusReceived.disconnect(self.update)

        self._onGoingObservations = weakref.ref(onGoingObservations)
        self.onGoingObservations.sigObsAdded.connect(self.addObservation)
        self.onGoingObservations.sigObsRemoved.connect(self.removeObservation)
        self.onGoingObservations.sigObsStatusReceived.connect(self.update)

    def update(self, scan, status):
        """

        :param scan: the updated scan
        :param status: the status of the updated scan
        """
        self.observationTable.model().update(scan, status)

    def addObservation(self, scan):
        """

        :param scan: the scan observed
        """
        self.observationTable.model().add(scan, "starting")

    def removeObservation(self, scan):
        """

        :param scan: the scan removed
        """
        self.observationTable.model().remove(scan)

    def clear(self):
        self.observationTable.model().clear()


class _ObservedScanModel(qt.QAbstractTableModel):
    def __init__(self, parent, header, *args):
        qt.QAbstractTableModel.__init__(self, parent, *args)
        self.header = header
        self.observations = OrderedDict()
        self._time_stamps = OrderedDict()
        # note: the time stamp is the time of the discovery and not of the start scan (as we don't have this information)

    def add(self, scan, status):
        with qitem_model_resetter(self):
            self.observations[scan] = status
            self._time_stamps[scan] = datetime.now()

    def remove(self, scan):
        with qitem_model_resetter(self):
            self.observations.pop(scan, None)
            self._time_stamps.pop(scan, None)

    def update(self, scan, status):
        with qitem_model_resetter(self):
            self.observations[scan] = status

    def clear(self):
        with qitem_model_resetter(self):
            self.observations = OrderedDict()
            self._time_stamps = OrderedDict()

    def rowCount(self, parent=None):
        return len(self.observations)

    def columnCount(self, parent=None):
        return len(self.header)

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        if self.observations is None:
            return

        to_order = {}
        for observation in self.observations.keys():
            to_order[str(observation)] = observation

        ordering = sorted(list(to_order.keys()))
        if order == qt.Qt.DescendingOrder:
            ordering = reversed(ordering)
        _observations = OrderedDict()
        _time_stamps = OrderedDict()
        for str_key in ordering:
            key = to_order[str_key]
            _observations[key] = self.observations[key]
            _time_stamps[key] = self._time_stamps[key]

        self.observations = _observations
        self._time_stamps = _time_stamps
        self.layoutChanged.emit()

    def data(self, index, role):
        if index.isValid() is False:
            return None

        if role not in (qt.Qt.DisplayRole, qt.Qt.ToolTipRole):
            return None

        obs = list(self.observations.keys())[index.row()]
        time_stamp = self._time_stamps.get(obs, None)
        # time stamp
        if index.column() == 0:
            if time_stamp:
                return time_stamp.strftime("%H:%M:%S")
            else:
                return "Unknown timestamp"
        # acquisition type
        elif index.column() == 1:
            if isinstance(obs, TomwerScanBase):
                return obs.type
            elif isinstance(obs, BlissScan):
                return "hdf5"
            elif NXtomoScan.directory_contains_scan(directory=obs):
                return "hdf5"
            else:
                return "edf"
        # N projections
        elif index.column() == 2:
            if isinstance(obs, TomwerScanBase):
                return obs.tomo_n or 0
            elif isinstance(obs, BlissScan):
                return f"(at least) {obs.n_acquired or '?'} over {obs.tomo_n or '?'}"
            elif os.path.exists(obs) and os.path.isdir(obs):
                return str(len(os.listdir(obs)))
            else:
                return None
        elif index.column() == 3:
            return self.observations[obs]
        # observation id
        elif index.column() == 4:
            if role == qt.Qt.ToolTipRole:
                return obs
            elif isinstance(obs, (TomwerScanBase, BlissScan)):
                return str(obs)
            else:
                return os.path.basename(obs)
        else:
            return None

    def headerData(self, col, orientation, role):
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            return self.header[col]
        return None
