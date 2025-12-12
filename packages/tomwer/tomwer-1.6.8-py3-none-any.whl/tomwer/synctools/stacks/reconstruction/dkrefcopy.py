# coding: utf-8
from __future__ import annotations


import functools
import logging
import shutil
import tempfile
import os

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt

from tomwer.core.process.reconstruction.darkref.darkrefscopy import DarkRefsCopy
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils.lbsram import is_low_on_memory

from ..processingstack import FIFO, ProcessingThread

_logger = logging.getLogger(__name__)


class DarkRefCopyProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisTask` but having a stack for treating
    scans and making computation in threads"""

    sigRefSetted = qt.Signal(str)
    """Signal emit when dark or flat are set by a scan. str is the scan identifier"""

    def __init__(self, process_id=None):
        try:
            self._save_dir = tempfile.mkdtemp()
        except Exception as e:
            _logger.warning(
                f"unable to create save dir. Error is {e}. Won't be able to copy any dark or flat"
            )
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)

    @property
    def save_dir(self):
        return self._save_dir

    def __del__(self):
        try:
            shutil.rmtree(self._save_dir)
        except Exception as e:
            _logger.error(e)

    def _process(self, data, configuration: dict, callback=None):
        if not isinstance(data, TomwerScanBase):
            raise TypeError(f"{data} is expected to be an instance of {TomwerScanBase}")
        if not isinstance(configuration, dict):
            raise TypeError(f"{configuration} is expected to be an instance of {dict}")
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )
        _logger.processStarted(f"dk-flat-copy {data}")
        assert isinstance(data, TomwerScanBase)
        self._data_currently_computed = data
        if isOnLbsram(data) and is_low_on_memory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = "low memory, skip dk-flat-copy", data.path
            try:
                ProcessManager().notify_dataset_state(
                    dataset=data, process=self, state=DatasetState.SKIPPED
                )
                _logger.processSkipped(mess)
                if callback is not None:
                    callback()
            except Exception as e:
                _logger.error(e)
            try:
                FIFO._end_threaded_computation(self)
            except Exception as e:
                _logger.error(e)
        else:
            self._data_currently_computed = data
            self._computationThread.init(data=data, inputs=configuration)
            # need to manage connect before starting it because
            fct_callback = functools.partial(self._end_threaded_computation, callback)
            self._computationThread.finished.connect(fct_callback)
            self._computationThread.sigRefSetted.connect(self.sigRefSetted)
            self._computationThread.start()

    def _end_computation(self, data, future_tomo_obj, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        if not isinstance(data, TomwerScanBase):
            raise TypeError(f"data is {type(data)} when {TomwerScanBase} expected.")
        super()._end_computation(
            data=data, future_tomo_obj=future_tomo_obj, callback=callback
        )

    def _end_threaded_computation(self, callback=None):
        assert self._data_currently_computed is not None
        self._computationThread.finished.disconnect()
        if callback:
            callback()
        FIFO._end_threaded_computation(self)

    def _create_processing_thread(self, process_id=None) -> qt.QThread:
        return _ProcessingThread(process_id=process_id, save_dir=self._save_dir)

    def clear_cache(self):
        """
        remove the file used to cache the reduced darks / flats.
        This can be used in the case it contain unrelevant data. Like frame with another shape...
        """
        cache_file = DarkRefsCopy.get_save_file(self._save_dir)
        if os.path.exists(cache_file):
            os.remove(cache_file)


class _ProcessingThread(ProcessingThread, SuperviseProcess):
    """
    Thread use to execute the processing of the axis position
    """

    sigRefSetted = qt.Signal(str)
    """Signal emit when dark or flat are set by a scan. str is the scan identifier"""

    def __init__(self, save_dir, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        try:
            ProcessingThread.__init__(self, process_id=process_id)
        except TypeError:
            ProcessingThread.__init__(self)
        self._save_dir = save_dir
        self._data = None
        self._inputs = None

    def init(self, data, inputs):
        self._data = data
        self._inputs = inputs

    def run(self):
        self.sigComputationStarted.emit()
        inputs = self._inputs
        inputs["data"] = self._data
        inputs["save_dir"] = self._save_dir
        inputs["serialize_output_data"] = False
        process = DarkRefsCopyWithSig(
            parent=self.parent(), inputs=inputs, process_id=self.process_id
        )
        process.sigRefSetted.connect(self.sigRefSetted)
        try:
            process.run()
        except Exception as e:
            _logger.warning(e)


class DarkRefsCopyWithSig(qt.QObject, DarkRefsCopy):
    sigRefSetted = qt.Signal(str)
    """Signal emit when dark or flat are set by a scan. str is the scan identifier"""

    def __init__(self, parent=None, *args, **kwargs) -> None:
        qt.QObject.__init__(self, parent)
        DarkRefsCopy.__init__(self, *args, **kwargs)

    def _ref_has_been_set(self, scan):
        self.sigRefSetted.emit(scan.get_identifier().to_str())
