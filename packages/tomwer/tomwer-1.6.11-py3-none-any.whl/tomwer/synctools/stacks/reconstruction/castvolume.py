# coding: utf-8
from __future__ import annotations

import functools
import logging

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt

from tomwer.core.process.reconstruction.nabu.castvolume import CastVolumeTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory

from ..processingstack import FIFO, ProcessingThread

_logger = logging.getLogger(__name__)


class CastVolumeProcessStack(FIFO, qt.QObject):
    def __init__(self, process_id=None):
        qt.QObject.__init__(self)
        FIFO.__init__(self, process_id=process_id)
        self._dry_run = False

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def _process(self, data, configuration, callback=None):
        ProcessManager().notify_dataset_state(
            dataset=data,
            process=self,
            state=DatasetState.ON_GOING,
        )
        _logger.processStarted(
            f"start cast volume {str(data.get_identifier())} with parameters {configuration}"
        )

        if isinstance(data, TomwerVolumeBase):
            if data.data_url is not None:
                path = data.data_url.file_path()
            else:
                path = None
        elif isinstance(data, TomwerScanBase):
            path = data.path
        else:
            raise ValueError(
                f"data is expected to be an instance of {TomwerScanBase} or {TomwerVolumeBase}. {type(data)} provided"
            )

        if (
            path is not None
            and isOnLbsram(path)
            and is_low_on_memory(get_lbsram_path()) is True
        ):
            # if computer is running into low memory on lbsram skip it
            mess = f"low memory, skip volume cast {data}"
            ProcessManager().notify_dataset_state(
                dataset=data, process=self, state=DatasetState.SKIPPED
            )
            _logger.processSkipped(mess)
            if callback is not None:
                callback()
                self._end_computation(data=data, future_tomo_obj=None, callback=None)
        else:
            self._data_currently_computed = data
            try:
                self._computationThread.init(data=data, configuration=configuration)
            except ValueError as e:
                # initialization can fail (for example for cast volume is there is no volume or be case this will raise an error)
                # then we want to keep the thread active
                self._data_currently_computed = None
                ProcessManager().notify_dataset_state(
                    dataset=data, process=self, state=DatasetState.FAILED
                )
                _logger.processFailed(f"thread initialization failed. Error is {e}")
                if callback is not None:
                    callback()
                self._end_computation(data=data, future_tomo_obj=None, callback=None)
            else:
                # need to manage connect before starting it because
                fct_callback = functools.partial(
                    self._end_threaded_computation, callback
                )
                self._computationThread.finished.connect(fct_callback)
                self._computationThread.start()

    def _end_computation(self, data, future_tomo_obj, callback):
        """
        callback when the computation thread is finished

        :param scan: pass if no call to '_computationThread is made'
        """
        assert isinstance(data, TomwerObject)
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
        self._dry_run = False
        self._scan = None
        self._future_tomo_obj = None
        self._volume = None
        self._configuration = None

    @property
    def future_tomo_obj(self):
        return self._future_tomo_obj

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    def init(self, data, configuration):
        if isinstance(data, TomwerVolumeBase):
            self._scan = None
            self._volume = data
        else:
            self._scan = data
            if len(data.latest_vol_reconstructions) < 1:
                raise ValueError(
                    "No reconstructed volume found. did you run the 'nabu volume reconstruction' process ?"
                )
            volume_identifier = data.latest_vol_reconstructions[0]
            self._volume = VolumeFactory.create_tomo_object_from_identifier(
                volume_identifier
            )
        self._data = data
        self._configuration = configuration

    def run(self):
        self.sigComputationStarted.emit()
        cast_volume_task = CastVolumeTask(
            process_id=self.process_id,
            varinfo=None,
            inputs={
                "volume": self._volume,
                "configuration": self._configuration,
                "scan": self._scan,
            },
        )
        try:
            cast_volume_task.run()
        except Exception as e:
            _logger.error(str(e))
            if self._scan is not None:
                # if scan is provided update status because otherwise only the volume state is updated
                ProcessManager().notify_dataset_state(
                    dataset=self._scan,
                    process=self,
                    state=DatasetState.FAILED,
                )
        else:
            if self._scan is not None:
                self._scan.cast_volume = cast_volume_task.outputs.volume
            if cast_volume_task.outputs.future_tomo_obj is not None:
                self._future_tomo_obj = cast_volume_task.outputs.future_tomo_obj
