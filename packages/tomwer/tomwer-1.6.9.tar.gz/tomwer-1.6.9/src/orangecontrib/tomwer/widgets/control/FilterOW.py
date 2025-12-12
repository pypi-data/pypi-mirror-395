from __future__ import annotations

import logging

from orangewidget import gui
from orangewidget.widget import Input, Output
from processview.core.manager import DatasetState
from silx.gui import qt

import tomwer.core.process.conditions.filters
from orangecontrib.tomwer.orange.managedprocess import SuperviseOW
from tomwer.core.process.conditions import filters
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.conditions.filter import FileNameFilterWidget
from tomwer.utils import docstring

logger = logging.getLogger(__name__)


class NameFilterOW(SuperviseOW):
    name = "scan filter"
    id = "orange.widgets.tomwer.filterow"
    description = (
        "Simple widget which filter some data directory if the name"
        "doesn't match with the pattern defined."
    )
    icon = "icons/namefilter.svg"
    priority = 106
    keywords = ["tomography", "selection", "tomwer", "folder", "filter"]

    want_main_area = True
    resizing_enabled = True

    ewokstaskclass = tomwer.core.process.conditions.filters.FileNameFilterTask

    class Inputs:
        data = Input(name="data", type=TomwerScanBase, multiple=True)

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        """ """
        super().__init__(parent)

        self.widget = FileNameFilterWidget(parent=self)
        self.widget.setContentsMargins(0, 0, 0, 0)

        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        layout.addWidget(spacer)

    @Inputs.data
    def applyfilter(self, scan, *args, **kwargs):
        if scan is None:
            return
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(f"{scan} is expected to be an instance of {TomwerScanBase}")

        process = filters.FileNameFilterTask(
            inputs={
                "data": scan,
                "pattern": self.getPattern(),
                "filter_type": self.getActiveFilter(),
                "invert_result": self.invertFilterAction(),
                "serialize_output_data": False,  # avoid spending time on scan serialization / deserialization when use orange
            }
        )
        process.run()
        out = process.outputs.data
        if out is not None:
            self.set_dataset_state(dataset=scan, state=DatasetState.SUCCEED)
            logger.processSucceed(f"{scan} pass through filter")
            self._signalScanReady(scan)
        else:
            self.set_dataset_state(dataset=scan, state=DatasetState.FAILED)
            logger.processFailed(f"{scan} NOT pass through filter")

    @docstring(SuperviseOW)
    def reprocess(self, dataset):
        self.applyfilter(dataset)

    def _signalScanReady(self, scan):
        self.Outputs.data.send(scan)

    def getPattern(self):
        return self.widget.getPattern()

    def setPattern(self, pattern):
        self.widget.setPattern(pattern)

    def getActiveFilter(self):
        return self.widget.getActiveFilter()

    def setActiveFilter(self, filter):
        self.widget.setActiveFilter(filter)

    def invertFilterAction(self):
        return self.widget.invertFilterAction()
