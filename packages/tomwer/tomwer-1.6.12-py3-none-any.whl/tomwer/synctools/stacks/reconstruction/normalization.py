# coding: utf-8
from __future__ import annotations


import functools
import logging

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt

from tomwer.core.process.reconstruction.normalization import SinoNormalizationTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils.lbsram import is_low_on_memory

from ..processingstack import FIFO, ProcessingThread

_logger = logging.getLogger(__name__)


class INormalizationProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisTask` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, process_id=None):
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)

    def _process(self, data, configuration, callback=None):
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )
        _logger.processStarted(f"start intensity normalization {data}")
        assert isinstance(data, TomwerScanBase)
        if isOnLbsram(data) and is_low_on_memory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = "low memory, skip intensity normalization", data.path
            ProcessManager().notify_dataset_state(
                dataset=data, process=self._process_id, state=DatasetState.SKIPPED
            )
            _logger.processSkipped(mess)
            if callback is not None:
                callback()
            self.scan_ready(scan=data)
        else:
            self._data_currently_computed = data
            self._computationThread.init(data=data, i_norm_params=configuration)
            # need to manage connect before starting it because
            fct_callback = functools.partial(self._end_threaded_computation, callback)
            self._computationThread.finished.connect(fct_callback)
            self._computationThread.start()

    def _end_threaded_computation(self, callback=None):
        assert self._data_currently_computed is not None
        self._computationThread.finished.disconnect()
        if callback:
            callback()
        FIFO._end_threaded_computation(self)

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        return _ProcessingThread(process_id=process_id)


class _ProcessingThread(ProcessingThread, SuperviseProcess):
    """
    Thread use to execute the processing of intensity normalization
    (mostly load io and compute the mean / median on it)
    """

    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        ProcessingThread.__init__(self, process_id=process_id)
        self.center_of_rotation = None
        self._dry_run = False
        self._scan = None
        self._i_norm_params = None

    def init(self, data, i_norm_params):
        self._scan = data
        self._i_norm_params = i_norm_params

    def run(self):
        self.sigComputationStarted.emit()
        norm_process = SinoNormalizationTask(
            process_id=self.process_id,
            varinfo=None,
            inputs={
                "data": self._scan,
                "configuration": self._i_norm_params,
                "serialize_output_data": False,
            },
        )
        try:
            norm_process.run()
        except Exception as e:
            _logger.error(str(e))
            mess = f"Intensity normalization computation for {self._scan} failed."
            state = DatasetState.FAILED
        else:
            mess = f"Intensity normalization computation for {self._scan} succeed."
            state = DatasetState.WAIT_USER_VALIDATION

        ProcessManager().notify_dataset_state(
            dataset=self._scan,
            process=self,
            state=state,
            details=mess,
        )
