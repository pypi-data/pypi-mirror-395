"""Define some processing stack"""

from __future__ import annotations

from collections import deque
from tomwer.core.tomwer_object import TomwerObject
from silx.gui.utils import blockSignals

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt


class ProcessingThread(qt.QThread):
    """Class for running some processing"""

    sigComputationStarted = qt.Signal()
    """Signal emitted when a computation is started"""

    sigError = qt.Signal(str)
    """Error found during processing. Parameter is the error raised"""


class FIFO(SuperviseProcess):
    """Processing Queue with a First In, First Out behavior"""

    sigComputationStarted = qt.Signal(object)
    """Signal emitted when a computation is started"""
    sigComputationEnded = qt.Signal(object, object)
    """Signal emitted when a computation is ended. First parameter is mandatory and
    is the scan computed. Second one is an optional FutureTomwerScan"""

    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        self._errors: list[qt.QErrorMessage] = []
        self._deque = deque()
        self._computationThread = self._create_processing_thread(process_id=process_id)
        assert isinstance(self._computationThread, ProcessingThread)

        """scan process by the thread"""
        self._data_currently_computed = None
        """Scan computed currently"""
        self._processing = False

        # connect signal / slot
        self._computationThread.sigComputationStarted.connect(
            self._start_threaded_computation
        )
        self._computationThread.sigError.connect(self._displayError)

    @property
    def data_currently_computed(self) -> TomwerObject | None:
        return self._data_currently_computed

    def add(self, data, configuration=None, callback=None):
        """
        add a scan to process

        :param data: data to process
        :param configuration: configuration of the process
        :param callback: function to call once the processing is Done
        """
        try:
            if self.process_id not in (None, -1):
                ProcessManager().notify_dataset_state(
                    dataset=data,
                    process=self,
                    state=DatasetState.PENDING,
                )
        except Exception:
            pass

        self.append((data, configuration, callback))
        if self.can_process_next():
            self._process_next()

    def _process(self, data, configuration, callback):
        raise NotImplementedError("Virtual class")

    def _process_next(self):
        if len(self) == 0:
            return

        self._processing = True
        data, configuration, callback = self.pop()
        self._process(data=data, configuration=configuration or {}, callback=callback)

    def can_process_next(self):
        """
        :return: True if the computation thread is ready to compute a new axis position
        """
        return not self._processing

    def _end_computation(self, data, future_tomo_obj, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        if callback is not None:
            callback()
        sender = self.sender()  # pylint: disable=E1101
        if hasattr(sender, "future_tomo_obj"):
            future_tomo_obj = sender.future_tomo_obj
        else:
            future_tomo_obj = None

        self.sigComputationEnded.emit(data, future_tomo_obj)
        self._processing = False
        if self.can_process_next():
            self._process_next()

    def _create_processing_thread(self, process_id=None) -> ProcessingThread:
        raise NotImplementedError("Virtual class")

    def is_computing(self):
        """Return True if processing thread is running (mean that computation
        is on going)"""
        return self._processing

    def wait_computation_finished(self):
        """
        Wait until the computation is finished
        """
        if self._processing:
            self._computationThread.wait()

    def _start_threaded_computation(self, *args, **kwargs):
        self.sigComputationStarted.emit(self._data_currently_computed)

    def _end_threaded_computation(self, callback=None):
        sender = self.sender()  # pylint: disable=E1101
        if hasattr(sender, "future_tomo_obj"):
            future_tomo_obj = sender.future_tomo_obj
        else:
            future_tomo_obj = None
        self._end_computation(
            data=self._data_currently_computed,
            callback=callback,
            future_tomo_obj=future_tomo_obj,
        )

    def cancel(self):
        if self._computationThread.isRunning():
            with blockSignals(self._computationThread):
                self._computationThread.cancel()
                # stop stack
                self.stop()
                # emit next
                self.sigComputationEnded.emit(None, None)

    def stop(self):
        self._computationThread.wait()
        self._processing = False
        self._data_currently_computed = None

    def _displayError(self, error_msg: str):
        err = qt.QMessageBox()
        err.setText(error_msg)
        err.setIcon(qt.QMessageBox.Warning)
        self._errors.append(err)
        err.setModal(False)
        err.show()

    # expose deque API
    def append(self, value):
        self._deque.append(value)

    def clear(self):
        self._deque.clear()

    def pop(self):
        return self._deque.pop()

    def remove(self, value):
        return self._deque.remove(value)

    def __len__(self):
        return len(self._deque)

    def __contains__(self, value):
        return value.get_identifier().to_str() in [
            scan.get_identifier().to_str() for scan in self._deque
        ]
