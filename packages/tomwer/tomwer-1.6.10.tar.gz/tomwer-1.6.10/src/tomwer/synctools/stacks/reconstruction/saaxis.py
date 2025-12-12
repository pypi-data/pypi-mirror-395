# coding: utf-8
from __future__ import annotations


import functools
import logging

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt

from tomwer.core.process.reconstruction.saaxis import SAAxisTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.synctools.axis import QAxisRP
from tomwer.synctools.saaxis import QSAAxisParams

from ..processingstack import FIFO, ProcessingThread

_logger = logging.getLogger(__name__)


class SAAxisProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisTask` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, saaxis_params, process_id=None):
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)
        assert saaxis_params is not None
        self._dry_run = False
        self._process_fct = None

    def patch_processing(self, process_fct):
        self._computationThread.patch_processing(process_fct)

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def _process(self, data, configuration, callback=None):
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )
        _logger.processStarted(f"start saaxis {data}")
        assert isinstance(data, TomwerScanBase)
        if data.axis_params is None:
            data.axis_params = QAxisRP()
        if data.saaxis_params is None:
            data.saaxis_params = QSAAxisParams()
        self._data_currently_computed = data
        saaxis_params = QSAAxisParams.from_dict(configuration)
        saaxis_params.frame_width = data.dim_1
        if isOnLbsram(data) and is_low_on_memory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = f"low memory, skip saaxis calculation {data.path}"
            ProcessManager().notify_dataset_state(
                dataset=data, process=self._process_id, state=DatasetState.SKIPPED
            )
            _logger.processSkipped(mess)
            data.axis_params.set_relative_value(None)
            if callback is not None:
                callback()
            self.scan_ready(scan=data)
        else:
            self._data_currently_computed = data
            self._computationThread.init(data=data, saaxis_params=saaxis_params)
            # need to manage connect before starting it because
            fct_callback = functools.partial(self._end_threaded_computation, callback)
            self._computationThread.finished.connect(fct_callback)
            self._computationThread.start()

    def _end_computation(self, data, future_tomo_obj, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        assert isinstance(data, TomwerScanBase)
        FIFO._end_computation(
            self, data=data, future_tomo_obj=future_tomo_obj, callback=callback
        )

    def _end_threaded_computation(self, callback=None):
        self._computationThread.finished.disconnect()
        if callback:
            callback()
        FIFO._end_threaded_computation(self)

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        return _ProcessingThread(process_id=process_id)


class _ProcessingThread(ProcessingThread, SuperviseProcess):
    """
    Thread use to execute the processing of the axis position
    """

    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        try:
            ProcessingThread.__init__(self, process_id=process_id)
        except TypeError:
            ProcessingThread.__init__(self)
        self.center_of_rotation = None
        self._dry_run = False
        self._scan = None
        self._saaxis_params = None
        self._patch_process_fct = None
        """function pointer to know which function to call for the axis
        calculation"""
        self._current_processing = None
        # processing currently runned. As we want to be able to cancel processing we need to keep a pointer on the
        # 'activate' nabu processing to stop process if requested
        self._task = None
        # ewoks task for reconstruction

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def patch_processing(self, process_fct):
        self._patch_process_fct = process_fct

    def init(self, data, saaxis_params: dict):
        self._scan = data
        self._saaxis_params = saaxis_params

    def run(self):
        self.sigComputationStarted.emit()
        if self._patch_process_fct:
            scores = {}
            for cor in self._saaxis_params.cors:
                scores[cor] = self._patch_process_fct(cor)
            self._scan.saaxis_params.scores = scores
            SAAxisTask.autofocus(scan=self._scan)
            self.center_of_rotation = self._scan.saaxis_params.autofocus
        else:
            self._task = SAAxisTask(
                process_id=self.process_id,
                inputs={
                    "dump_process": False,
                    "data": self._scan,
                    "dry_run": self._dry_run,
                    "sa_axis_params": self._saaxis_params.to_dict(),
                    "serialize_output_data": False,
                },
            )

            self._task.run()
            self.center_of_rotation = self._task.outputs.best_cor

    def cancel(self):
        if self._task is not None:
            self._task.cancel()
        self.quit()
