from __future__ import annotations

import functools
import logging

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output
from processview.core.manager import DatasetState, ProcessManager
from silx.gui import qt

import tomwer.core.process.control.timer
from orangecontrib.tomwer.orange.managedprocess import SuperviseOW
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.utils import docstring
from tomwer.core.utils.deprecation import deprecated_warning

_logger = logging.getLogger(__name__)


class _TimerWidget(qt.QWidget):
    def __init__(self, parent, _time=None):
        if _time is not None:
            assert type(_time) is int
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        self.layout().addWidget(qt.QLabel("time to wait (in sec):", parent=self), 0, 0)
        self._timeLE = qt.QSpinBox(parent=self)
        self._timeLE.setMinimum(0)
        self._timeLE.setValue(_time or 1)
        self.layout().addWidget(self._timeLE, 0, 1)

        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 1, 0)

        # expose API
        self.timeChanged = self._timeLE.valueChanged


class TimerOW(SuperviseOW):
    name = "timer"
    id = "orange.widgets.tomwer.filterow"
    description = (
        "Simple widget which wait for a defined amont of time and" "release the data"
    )
    icon = "icons/time.png"
    priority = 200
    keywords = ["control", "timer", "wait", "data"]

    want_main_area = True
    resizing_enabled = True
    _waiting_time = Setting(int(1))

    ewokstaskclass = tomwer.core.process.control.timer.TimerTask

    class Inputs:
        data = Input(name="data", type=TomwerScanBase, multiple=True)

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        """ """
        SuperviseOW.__init__(self, parent)
        deprecated_warning(
            type_="class",
            name="orangecontrib.tomwer.widgets.control.TimerOW",
            replacement="orangecontrib.ewoksnotify.WaiterOW",
            reason="moved to ewoksnotify (pip install ewoksnotify[full] to get the orange widget)",
            since_version="1.4",
        )
        self._widget = _TimerWidget(parent=self, _time=self._waiting_time)
        self._widget.setContentsMargins(0, 0, 0, 0)

        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self._widget)

        self._widget.timeChanged.connect(self._updateTime)

    @Inputs.data
    def process(self, scan, *args, **kwargs):
        if scan is None:
            return

        ProcessManager().notify_dataset_state(
            dataset=scan,
            process=self,
            state=DatasetState.ON_GOING,
        )

        callback = functools.partial(self._get_out, scan)
        _timer = qt.QTimer(self)
        _timer.singleShot(self._waiting_time * 1000, callback)

    def _updateTime(self, newTime):
        self._waiting_time = newTime

    def _get_out(self, scan):
        ProcessManager().notify_dataset_state(
            dataset=scan,
            process=self,
            state=DatasetState.SUCCEED,
        )
        self.Outputs.data.send(scan)

    @docstring(SuperviseOW)
    def reprocess(self, dataset):
        self.process(dataset)
