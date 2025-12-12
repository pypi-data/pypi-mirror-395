# coding: utf-8
from __future__ import annotations


import functools
import logging

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt

from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
    SADeltaBetaTask,
)
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.synctools.axis import QAxisRP
from tomwer.synctools.sadeltabeta import QSADeltaBetaParams

from ..processingstack import FIFO, ProcessingThread

_logger = logging.getLogger(__name__)


class SADeltaBetaProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisTask` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, sa_delta_beta_params, process_id=None):
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)
        assert sa_delta_beta_params is not None
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
        _logger.processStarted(f"start sa-delta-beta {data}")
        assert isinstance(data, TomwerScanBase)
        if data.axis_params is None:
            data.axis_params = QAxisRP()
        if data.sa_delta_beta_params is None:
            data.sa_delta_beta_params = QSADeltaBetaParams()
        self._data_currently_computed = data
        sa_delta_beta_params = QSADeltaBetaParams.from_dict(configuration)
        if isOnLbsram(data) and is_low_on_memory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = f"low memory, skip sa-delta-beta-axis calculation {data.path}"
            ProcessManager().notify_dataset_state(
                dataset=data, process=self._process_id, state=DatasetState.SKIPPED
            )
            _logger.processSkipped(mess)
            data.sa_delta_beta_params.set_value(None)
            if callback is not None:
                callback()
            self.scan_ready(scan=data)
        else:
            self._data_currently_computed = data
            self._computationThread.init(
                data=data, sa_delta_beta_params=sa_delta_beta_params
            )
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
        assert self._data_currently_computed is not None
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
        self.db_value = None
        self._dry_run = False
        self._scan = None
        self._sa_delta_beta_params = None
        self._patch_process_fct = None
        """function pointer to know which function to call for the axis
        calculation"""
        self._task = None
        # ewoks task for reconstruction

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def patch_processing(self, process_fct):
        self._patch_process_fct = process_fct

    def init(self, data, sa_delta_beta_params):
        self._scan = data
        self._sa_delta_beta_params = sa_delta_beta_params

    def run(self):
        self.sigComputationStarted.emit()
        if self._patch_process_fct:
            scores = {}
            for db in self._sa_delta_beta_params.delta_beta_values:
                scores[db] = self._patch_process_fct(db)
            self._scan.sa_delta_beta_params.scores = scores
            SADeltaBetaTask.autofocus(scan=self._scan)
            self.db_value = self._scan.sa_delta_beta_params.autofocus
        else:
            self._task = SADeltaBetaTask(
                inputs={
                    "dump_process": False,
                    "data": self._scan,
                    "dry_run": self._dry_run,
                    "sa_delta_beta_params": self._sa_delta_beta_params.to_dict(),
                    "serialize_output_data": False,
                },
                process_id=self.process_id,
            )

            self._task.run()
            self.db_value = self._task.outputs.best_db

    def cancel(self):
        if self._task is not None:
            self._task.cancel()
        self.quit()
