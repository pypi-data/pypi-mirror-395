# coding: utf-8
from __future__ import annotations


from silx.gui import qt

from tomwer.core.process.control.datalistener import DataListener
from tomwer.core.scan.blissscan import BlissScan
from nxtomomill.models.h52nx import H52nxModel

from ..processingstack import FIFO, ProcessingThread

import logging

_logger = logging.getLogger(__name__)


class DataListenerProcessStack(FIFO, qt.QObject):
    """Stack of file conversion once received by the data-listener
    from a bliss file and a specific entry"""

    def __init__(self, parent=None):
        qt.QObject.__init__(self, parent=parent)
        FIFO.__init__(self, process_id=-1)
        self._results = {}

    def _process(self, data, configuration, callback=None):
        assert isinstance(data, BlissScan)
        assert isinstance(configuration, H52nxModel)
        _logger.info(f"DataListenerProcessStack is processing {data}")
        self._data_currently_computed = data
        self._computationThread.finished.connect(self._end_threaded_computation)

        self._computationThread.init(data=data, configuration=configuration)
        # need to manage connect before starting it because
        self._computationThread.start()

    def _end_threaded_computation(self, callback=None):
        self._computationThread.finished.disconnect(self._end_threaded_computation)
        super()._end_threaded_computation(callback=callback)

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        thread = _DataListenerConverterThread()
        thread.setParent(self)
        return thread

    def _end_computation(self, data, future_tomo_obj, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        if callback is not None:
            callback()
        if data in self._results:
            nx_scan = self._results[data]
            del self._results[data]
        else:
            nx_scan = None
        self.sigComputationEnded.emit(nx_scan, None)
        self._processing = False
        if self.can_process_next():
            self._process_next()

    def register_result(self, bliss_scan, nx_scan):
        self._results[bliss_scan] = nx_scan


class _DataListenerConverterThread(ProcessingThread):
    """
    Thread use to execute the processing of nxtomomill
    """

    def __init__(self):
        ProcessingThread.__init__(self)
        self._scan = None
        self._configuration = None

    def init(self, data, configuration):
        if not isinstance(data, BlissScan):
            raise TypeError(f"Only manage BlissScan. {type(data)} is not managed")
        assert isinstance(configuration, H52nxModel)
        self._scan = data
        self._configuration = configuration

    def run(self):
        self.sigComputationStarted.emit()
        _logger.processStarted(f"Start conversion of bliss scan {self._scan}")

        data_listener = DataListener()
        data_listener.set_configuration(self._configuration or {})
        try:
            scans = data_listener.process_sample_file(
                sample_file=self._scan.master_file,
                entry=self._scan.entry,
                proposal_file=self._scan.proposal_file,
                master_sample_file=self._scan.saving_file,
            )
        except Exception as e:
            _logger.processFailed(
                f"Conversion of bliss scan {self._scan}. Reason is {e}"
            )
            scans = None
        else:
            _logger.processSucceed(f"Conversion of bliss scan {self._scan}.")
        self.parent().register_result(self._scan, scans)
