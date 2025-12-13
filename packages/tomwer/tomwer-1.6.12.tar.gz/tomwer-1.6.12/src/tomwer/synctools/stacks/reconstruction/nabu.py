# coding: utf-8
from __future__ import annotations


import logging

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess

from silx.gui import qt
from silx.gui.utils import blockSignals

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.core.process.reconstruction.nabu.nabuslices import NabuSlicesTask
from tomwer.core.process.reconstruction.nabu.nabuvolume import NabuVolumeTask

from ..processingstack import FIFO, ProcessingThread

_logger = logging.getLogger(__name__)


class NabuSliceProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisTask` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, parent=None, process_id=None):
        qt.QObject.__init__(self, parent=parent)
        FIFO.__init__(self, process_id=process_id)
        self._dry_run = False

    def _process(self, data, configuration, callback=None):
        _logger.info(f"Nabu slice stack is processing {data}")
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )

        self._data_currently_computed = data
        assert isinstance(data, TomwerScanBase)
        self._computationThread.finished.connect(self._end_threaded_computation)

        if isOnLbsram(data) and is_low_on_memory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = f"low memory, skip nabu reconstruction for {data.path}"
            _logger.processSkipped(mess)
            ProcessManager().notify_dataset_state(
                dataset=data,
                process=self,
                state=DatasetState.SKIPPED,
            )
            self._end_threaded_computation()
        else:
            self._computationThread.init(data=data, configuration=configuration)
            self._computationThread.setDryRun(self._dry_run)
            # need to manage connect before starting it because
            self._computationThread.start()

    def _end_threaded_computation(self, callback=None):
        self._computationThread.finished.disconnect(self._end_threaded_computation)
        super()._end_threaded_computation(callback=callback)

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        return _SliceProcessingThread(process_id=process_id)

    def setDryRun(self, dry_run):
        self._dry_run = dry_run

    def cancel(self):
        if self._computationThread.isRunning():
            with blockSignals(self._computationThread):
                self._computationThread.cancel()
                # stop stack
                super().stop()
                # emit next
                self.sigComputationEnded.emit(None, None)


class NabuVolumeProcessStack(NabuSliceProcessStack):
    """Implementation of the `.AxisTask` but having a stack for treating
    scans and making computation in threads"""

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        return _VolumeProcessingThread(process_id=process_id)


class _SliceProcessingThread(ProcessingThread, SuperviseProcess):
    """
    Thread use to execute the processing of nabu reconstruction
    """

    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        try:
            ProcessingThread.__init__(self, process_id=process_id)
        except TypeError:
            ProcessingThread.__init__(self)
        self._scan = None
        self._future_tomo_obj = None
        self._configuration = None
        self._dry_run = False
        self._current_processing = None
        # processing currently runned. As we want to be able to cancel processing we need to keep a pointer on the
        # 'activate' nabu processing to stop process if requested
        self._task = None
        # ewoks task for reconstruction

    @property
    def future_tomo_obj(self):
        return self._future_tomo_obj

    def setDryRun(self, dry_run):
        self._dry_run = dry_run

    def init(self, data, configuration):
        self._scan = data
        self._configuration = configuration
        self._task = None

    def run(self):
        # note: now rnu does a processing close to the 'run_slices_reconstruction' except that we keep a trace on the
        # current nabu subprocess runned. The goal is to be able to cancel / stop processing when asked
        self.sigComputationStarted.emit()
        mess = f"Start nabu slice(s) reconstruction of {self._scan}"
        _logger.processStarted(mess)
        ProcessManager().notify_dataset_state(
            dataset=self._scan,
            process=self,
            state=DatasetState.ON_GOING,
            details=mess,
        )

        self._task = NabuSlicesTask(
            process_id=self.process_id,
            inputs={
                "data": self._scan,
                "nabu_params": self._configuration,
                "dry_run": self._dry_run,
                "serialize_output_data": False,
                "invalid_slice_callback": self.showErrorSliceInvalid,
            },
        )
        self._task.run()
        self._future_tomo_obj = self._task.outputs.future_tomo_obj

    def cancel(self):
        if self._task is not None:
            self._task.cancel()
        self.quit()

    def showErrorSliceInvalid(self, error_message):
        self.sigError.emit(error_message)


class _VolumeProcessingThread(_SliceProcessingThread):
    """
    Thread use to execute the processing of nabu reconstruction
    """

    def run(self):
        self.sigComputationStarted.emit()
        mess = f"Start nabu volume reconstruction of {self._scan}"
        _logger.processStarted(mess)
        ProcessManager().notify_dataset_state(
            dataset=self._scan,
            process=self,
            state=DatasetState.ON_GOING,
            details=mess,
        )

        self._task = NabuVolumeTask(
            process_id=self.process_id,
            inputs={
                "data": self._scan,
                "nabu_params": self._scan.nabu_recons_params,
                "nabu_extra_params": self._configuration,
                "process_id": self.process_id,
                "dry_run": self._dry_run,
                "serialize_output_data": False,  # avoid spending time on serialization / deserialization
            },
        )
        self._task.run()
        self._future_tomo_obj = self._task.outputs.future_tomo_obj
