# coding: utf-8
from __future__ import annotations


import functools
from collections import OrderedDict

from silx.gui import qt

from tomwer.core.futureobject import FutureTomwerObject

try:
    from processview.gui.utils.qitem_model_resetter import qitem_model_resetter
except ImportError:
    from tomwer.third_part.qitem_model_resetter import qitem_model_resetter


class FutureTomwerScanObserverWidget(qt.QWidget):
    """Widget used to observe a set of :class:`FutureTomwerScan`"""

    sigConversionPolicyChanged = qt.Signal()
    """Signal emit when the user change rule for converting finished scan"""

    sigConversionRequested = qt.Signal(object)
    """signal emit when a conversion is requested. Parameter is the future scan"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        # filter widget
        self.filterWidget = FilterWidget(parent=self)
        self.layout().setContentsMargins(4, 4, 4, 4)
        self.layout().setSpacing(4)
        self.filterWidget.layout().setSpacing(4)
        self.layout().addWidget(self.filterWidget)
        # observation table
        self.observationTable = ObservationTable(self)
        self.layout().addWidget(self.observationTable)
        self.observationTable.setModel(
            _DatasetProcessModel(parent=self.observationTable, header=tuple())
        )
        self.observationTable.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.observationTable.resizeColumnsToContents()
        self.observationTable.setSortingEnabled(True)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        # converter option
        self._commandWidget = qt.QWidget(self)
        self.layout().addWidget(self._commandWidget)
        self._commandWidget.setLayout(qt.QGridLayout())
        self._commandWidget.setContentsMargins(0, 0, 0, 0)
        spacer = qt.QWidget(self._commandWidget)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._commandWidget.layout().addWidget(spacer, 0, 0, 1, 1)
        self._convertWhenFinished = qt.QCheckBox(
            "convert back to 'data' when finished", self
        )
        self._commandWidget.layout().addWidget(self._convertWhenFinished, 0, 1, 1, 2)
        self._convertSelectedPB = qt.QPushButton(self)
        self._convertSelectedPB.setText("convert selected")
        self._commandWidget.layout().addWidget(self._convertSelectedPB, 1, 2, 1, 1)
        self._cancelSelectedPB = qt.QPushButton(self)
        self._cancelSelectedPB.setText("cancel selected")
        style = qt.QApplication.style()
        stopIcon = style.standardIcon(qt.QStyle.SP_BrowserStop)
        self._cancelSelectedPB.setIcon(stopIcon)
        self._commandWidget.layout().addWidget(self._cancelSelectedPB, 1, 1, 1, 1)

        # set up
        self._convertWhenFinished.setChecked(True)

        # connect signal / slot
        self.filterWidget.sigChanged.connect(self._filterUpdated)
        self._convertWhenFinished.toggled.connect(self._conversionPolicyChanged)
        self._convertSelectedPB.released.connect(self._convertSelected)
        self._cancelSelectedPB.released.connect(self._cancelSelected)

    def _convertSelected(self, *args, **kwargs):
        for cell in self.observationTable.selectionModel().selectedRows():
            future_tomo_obj = self.observationTable.model().futureTomoObjs.get(
                cell.row(), None
            )
            if future_tomo_obj is not None:
                self.sigConversionRequested.emit(future_tomo_obj)
        self.observationTable.model().updateIndices()
        self.observationTable.model().layoutChanged.emit()

    def _cancelSelected(self, *args, **kwargs):
        for cell in self.observationTable.selectionModel().selectedRows():
            future_tomo_obj = self.observationTable.model().futureTomoObjs.get(
                cell.row(), None
            )
            if future_tomo_obj is not None:
                future_tomo_obj.cancel()
        self.observationTable.model().layoutChanged.emit()

    def addFutureTomoObj(self, future_tomo_obj: FutureTomwerObject):
        self.observationTable.model().addFutureTomoObj(future_tomo_obj)

    def removeFutureTomoObj(self, future_tomo_obj: FutureTomwerObject):
        self.observationTable.model().removeFutureTomoObj(future_tomo_obj)

    def _filterUpdated(self):
        with qitem_model_resetter(self.observationTable.model()):
            self.observationTable.model().filtered_status = (
                self.filterWidget.getFilteredStatus()
            )

    def updateView(self):
        """
        Update scan view and each future scan status
        """
        self.observationTable.model().updateStatusAllFutureTomoObjs()
        self.observationTable.model().layoutChanged.emit()

    def convertWhenFinished(self):
        return self._convertWhenFinished.isChecked()

    def _conversionPolicyChanged(self, *args, **kwargs):
        self.sigConversionPolicyChanged.emit()

    def futureTomoObjs(self):
        return self.observationTable.model().futureTomoObjs

    def setConvertWhenFinished(self, convert):
        self._convertWhenFinished.setChecked(convert)


class _DatasetProcessModel(qt.QAbstractTableModel):
    sigStatusUpdated = qt.Signal(object, str)
    """Signal emit when the status of scan changes"""

    def __init__(self, parent, header, *args):
        qt.QAbstractTableModel.__init__(self, parent, *args)
        self.header = header
        self.futureTomoObjs = OrderedDict()
        # key is index, value is scan
        self._filteredFutureTomoObjs = OrderedDict()
        # key is index, value is scan but only for the scan we want to display
        self._tomoObjStatus = dict()
        # key is the future scan, value is the status of the scan
        self._filteredStatus = tuple()
        # list of status to filter
        """FutureTomwerScan with this status will be hide"""
        self._headers = {
            0: "start-time",
            1: "dataset",
            2: "status",
            3: "requester",
            4: "slurm-job",
            5: "info",
        }
        self._headersI = {v: k for k, v in self._headers.items()}
        assert len(self._headers) == len(self._headersI), "insure values are unique"

    def is_filtered(self, future_scan):
        return future_scan.status in self._filteredStatus

    def _computeUnfilteredFutureTomoObjs(self):
        i_row = 0
        self._filteredFutureTomoObjs = OrderedDict()

        for _, scan in self.futureTomoObjs.items():
            if not self.is_filtered(scan):
                self._filteredFutureTomoObjs[i_row] = scan
                i_row += 1
        return self._filteredFutureTomoObjs

    def endResetModel(self, *args, **kwargs):
        self._computeUnfilteredFutureTomoObjs()
        super().endResetModel(*args, **kwargs)

    def addFutureTomoObj(self, future_tomo_obj):
        if not isinstance(future_tomo_obj, FutureTomwerObject):
            raise TypeError(
                f"future_tomo_obj is expected to be an instance of {FutureTomwerObject} and not {type(future_tomo_obj)}"
            )
        self.futureTomoObjs[len(self.futureTomoObjs)] = future_tomo_obj
        self._tomoObjStatus[future_tomo_obj] = "pending"
        for future in future_tomo_obj.futures:
            callback = functools.partial(
                self._updateStatus,
                future_tomo_obj=future_tomo_obj,
            )

            # TODO: remove this since we are not using distributed anymore...
            class CallBack:
                # we cannot create a future directly because distributed enforce
                # the callback to have a function signature with only the future
                # as single parameter.
                def __init__(self, f_partial) -> None:
                    self.f_partial = f_partial

                def process(self, fn):
                    self.f_partial()

            future.add_done_callback(CallBack(callback).process)
        obj_index = len(self._filteredFutureTomoObjs)

        if not self.is_filtered(future_tomo_obj):
            self._filteredFutureTomoObjs[obj_index] = future_tomo_obj

        self.dataChanged.emit(
            self.createIndex(obj_index, 0),
            self.createIndex(obj_index, len(self._headers) - 1),
        )
        self.layoutChanged.emit()

    def updateStatusAllFutureTomoObjs(self):
        for future_tomo_obj in self._tomoObjStatus:
            self._tomoObjStatus[future_tomo_obj] = future_tomo_obj.status

    def _updateStatus(self, future_tomo_obj):
        if future_tomo_obj is None:
            return
        status = future_tomo_obj.status

        trigger_update = (
            future_tomo_obj not in self._tomoObjStatus
            or status != self._tomoObjStatus[future_tomo_obj]
            or status
            in (
                "finished",
                "completed",
            )  # hack: when several finish at the same time, ensure the conversion is done :()
        )
        if trigger_update:
            self._tomoObjStatus[future_tomo_obj] = status
            obj_index = list(self._tomoObjStatus.keys()).index(future_tomo_obj)
            try:
                self.sigStatusUpdated.emit(future_tomo_obj, status)
            except Exception:
                pass
            else:
                self.dataChanged.emit(
                    self.createIndex(obj_index, 0),
                    self.createIndex(obj_index, len(self._headers) - 1),
                )

    def removeFutureTomoObj(self, future_tomo_obj):
        for container in (self.futureTomoObjs, self._filteredFutureTomoObjs):
            futureTomoObjsI = {v: k for k, v in container.items()}
            idx = futureTomoObjsI.get(future_tomo_obj, None)
            if idx is not None:
                del container[idx]
        if future_tomo_obj in self._tomoObjStatus:
            del self._tomoObjStatus[future_tomo_obj]
        self.layoutChanged.emit()

    def updateIndices(self):
        """
        Update tomo object indices when a tomo object has been removed (during a convertion for example)
        """
        tomo_objs = list(self.futureTomoObjs.values())
        self.futureTomoObjs.clear()
        for i_tomo_obj, tomo_obj in enumerate(tomo_objs):
            self.futureTomoObjs[i_tomo_obj] = tomo_obj
        self._computeUnfilteredFutureTomoObjs()

    def getUnfilteredFutureTomoObjs(self):
        return self._filteredFutureTomoObjs

    @property
    def filtered_status(self):
        return self._filteredStatus

    @filtered_status.setter
    def filtered_status(self, filters):
        self._filteredStatus = filters
        self.layoutChanged.emit()

    def clear(self):
        self.futureTomoObjs = OrderedDict()
        self._filteredFutureTomoObjs = OrderedDict()
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.getUnfilteredFutureTomoObjs())

    def columnCount(self, parent=None):
        return len(self._headers)

    def headerData(self, col, orientation, role):
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            if col < len(self._headers):
                return self._headers[col]
            else:
                return None

    def data(self, index, role):
        if not index.isValid():
            return None

        if role not in (qt.Qt.DisplayRole, qt.Qt.ToolTipRole, qt.Qt.BackgroundRole):
            return None

        key = list(self._filteredFutureTomoObjs.keys())[index.row()]
        f_scan = self._filteredFutureTomoObjs[key]

        if role == qt.Qt.BackgroundRole:
            if index.column() in (self._headersI["status"],):
                # color are the same as the one defined by the process manager

                if f_scan.status == "error":
                    return qt.QColor("#f52718")
                elif f_scan.status == "pending":
                    return qt.QColor("#609ab3")
                elif f_scan.status == "cancelled":
                    return qt.QColor("#fcba03")
                elif f_scan.status == "running":
                    return qt.QColor("#839684")
                elif f_scan.status in ("finished", "completed"):
                    return qt.QColor("#068c0c")

        elif role == qt.Qt.DisplayRole:
            col_type = self._headers[index.column()]
            if col_type == "start-time":
                return f_scan.start_time.strftime("%H:%M:%S")
            elif col_type == "dataset":
                return str(f_scan.tomo_obj.get_identifier())
            elif col_type == "requester":
                from processview.core.manager import ProcessManager

                id_ = f_scan.process_requester_id
                process = ProcessManager().get_process(id_)
                if process is not None:
                    return process.name
                else:
                    return "unknown"
            elif col_type == "status":
                return f_scan.status
            elif col_type == "slurm-job":
                infos_job = ",".join(
                    [
                        str(future.job_id) if hasattr(future, "job_id") else ""
                        for future in f_scan.futures
                    ]
                )
                return infos_job


class ObservationTable(qt.QTableView):
    def sizeHintForColumn(self, column):
        # warning: to be called we need to call resizeColumnsToContents upper
        if column == 1:  # dataset column
            return 400
        elif column in (
            0,
            2,
            3,
            4,
        ):  # start-time, status, requester, slurm-job
            return 55
        elif column == 5:
            return 200
        else:
            return super().sizeHintForColumn(column)


class FilterWidget(qt.QGroupBox):
    """
    Interface to define which future to be displayed
    """

    sigChanged = qt.Signal()
    """signal emit when filter change"""

    def __init__(self, parent=None):
        super().__init__("show job with status", parent)
        self.setLayout(qt.QHBoxLayout())
        # spacer
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(spacer)

        # pending
        self._pending = qt.QCheckBox("pending", self)
        self.layout().addWidget(self._pending)
        # running
        self._running = qt.QCheckBox("running", self)
        self.layout().addWidget(self._running)
        # finished
        self._finished = qt.QCheckBox("finished", self)
        self.layout().addWidget(self._finished)
        # error
        self._error = qt.QCheckBox("error", self)
        self.layout().addWidget(self._error)
        # cancelled
        self._cancelled = qt.QCheckBox("cancelled", self)
        self.layout().addWidget(self._cancelled)

        # set up
        self._pending.setChecked(True)
        self._cancelled.setChecked(True)
        self._running.setChecked(True)
        self._finished.setChecked(True)
        self._error.setChecked(True)

        # connect signal / slot
        self._pending.toggled.connect(self._updated)
        self._cancelled.toggled.connect(self._updated)
        self._running.toggled.connect(self._updated)
        self._finished.toggled.connect(self._updated)
        self._error.toggled.connect(self._updated)

    def _updated(self):
        self.sigChanged.emit()

    def getFilteredStatus(self):
        filters = []
        cbs_filter = {
            "pending": self._pending,
            "cancelled": self._cancelled,
            "running": self._running,
            "finished": self._finished,
            "error": self._error,
        }
        for status, status_cb in cbs_filter.items():
            if not status_cb.isChecked():
                filters.append(status)
        return tuple(filters)
