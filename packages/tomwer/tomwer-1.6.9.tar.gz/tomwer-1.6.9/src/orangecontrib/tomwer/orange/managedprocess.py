from __future__ import annotations

import functools
import logging

from ewoksorange.bindings import (
    OWEwoksWidgetWithTaskStack,
    OWEwoksWidgetOneThreadPerRun,
)
from ewoksorange.bindings.owwidgets import invalid_data
from orangewidget.widget import OWBaseWidget
from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess

from orangecontrib.tomwer.widgets.utils import WidgetLongProcessing

_logger = logging.getLogger(__name__)


class _SuperviseMixIn(SuperviseProcess):
    def __init__(self, process_id=None):
        SuperviseProcess.__init__(self, process_id=process_id)
        self.destroyed.connect(functools.partial(ProcessManager().unregister, self))

    def setCaption(self, caption):
        self.name = caption
        try:
            ProcessManager().process_renamed(process=self)
        except Exception as e:
            _logger.warning(f"Fail to update process name. Error is {e}")

    def notify_skip(self, scan, details=None):
        ProcessManager().notify_dataset_state(
            dataset=scan, process=self, state=DatasetState.SKIPPED, details=details
        )

    def notify_pending(self, scan, details=None):
        ProcessManager().notify_dataset_state(
            dataset=scan, process=self, state=DatasetState.PENDING, details=details
        )

    def notify_succeed(self, scan, details=None):
        ProcessManager().notify_dataset_state(
            dataset=scan, process=self, state=DatasetState.SUCCEED, details=details
        )

    def notify_failed(self, scan, details=None):
        ProcessManager().notify_dataset_state(
            dataset=scan, process=self, state=DatasetState.FAILED, details=details
        )

    def notify_on_going(self, scan, details=None):
        ProcessManager().notify_dataset_state(
            dataset=scan, process=self, state=DatasetState.ON_GOING, details=details
        )


class SuperviseOW(OWBaseWidget, _SuperviseMixIn, openclass=True):
    """
    A basic OWWidget but registered on the process manager
    """

    want_control_area = False

    def __init__(self, parent, process_id=None):
        OWBaseWidget.__init__(self, parent, process_id=process_id)
        _SuperviseMixIn.__init__(self, process_id=process_id)

    def setCaption(self, caption):
        OWBaseWidget.setCaption(self, caption)
        _SuperviseMixIn.setCaption(self, caption=caption)


class TomwerWithStackStack(
    OWEwoksWidgetWithTaskStack, _SuperviseMixIn, WidgetLongProcessing, openclass=True
):
    def __init__(self, parent, process_id=None, *args, **kwargs):
        OWEwoksWidgetWithTaskStack.__init__(self, parent, args, kwargs)
        _SuperviseMixIn.__init__(self, process_id=process_id)
        WidgetLongProcessing.__init__(self)

        self.task_executor_queue.sigComputationStarted.connect(self._startProcessing)
        self.task_executor_queue.sigComputationEnded.connect(self._endProcessing)

    def setCaption(self, caption):
        OWBaseWidget.setCaption(self, caption)
        _SuperviseMixIn.setCaption(self, caption=caption)

    def trigger_downstream(self) -> None:
        # for now ewoksorange send ewoks variable. This will work only if
        # all task are implemented using ewokwidget which is not the case today
        for ewoksname, var in self.get_task_outputs().items():
            channel = self._get_output_signal(ewoksname)
            if invalid_data.is_invalid_data(var.value):
                channel.send(None)  # or channel.invalidate?
            else:
                channel.send(var.value)


class TomwerUnsupervisedOneThreadPerRun(
    OWEwoksWidgetOneThreadPerRun, WidgetLongProcessing, openclass=True
):
    """EwoksOrange OWEwoksWidgetOneThreadPerRun with API to provide dataset state information"""

    pass
