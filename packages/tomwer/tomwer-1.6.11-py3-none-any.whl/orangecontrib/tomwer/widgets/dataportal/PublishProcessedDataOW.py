from __future__ import annotations

import weakref
from silx.gui import qt
from ewoksorange.bindings.owwidgets import OWEwoksWidgetOneThreadPerRun
from ewoksorange.gui.orange_imports import Input
from orangewidget import gui
from orangewidget.settings import Setting
from orangecontrib.tomwer.widgets.utils import WidgetLongProcessing

from tomwer.core.settings import TOMO_BEAMLINES
import tomwer.core.process.drac.publish
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.dataportal.publish import PublishProcessedDataWindow, has_ewoksnotify

from processview.core.superviseprocess import SuperviseProcess


class PublishProcessedDataOW(
    OWEwoksWidgetOneThreadPerRun,
    SuperviseProcess,
    WidgetLongProcessing,
    ewokstaskclass=tomwer.core.process.drac.publish.PublishICatDatasetTask,
):
    """
    This widget can receive 'data' (scan) and but some screenshot to be pushed on GALLERY.
    """

    name = "Data Portal Publishing"
    id = "orangecontrib.widgets.tomwer.dataportal.PublishProcessedDataOW.PublishProcessedDataOW"
    description = "Publish processed data to the (ESRF) data portal. \n To execute this you need to be inside the ESRF network"
    icon = "icons/publish_processed_data.svg"
    priority = 64
    keywords = [
        "tomography",
        "tomwer",
        "tomo_obj",
        "processed data",
        "PROCESSED_DATA",
        "publish",
        "icat",
        "icatplus",
        "pyicatplus",
        "pyicat-plus",
        "drac",
        "data portal",
        "dataportal",
        "portal",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _ewoks_default_inputs = Setting({})

    _ewoks_inputs_to_hide_from_orange = (
        "__process__",
        "beamline",
        "proposal",
        "dataset",
        "dry_run",
        "path",
    )

    class Inputs:
        # redefine the input to allow multiple and default
        data_portal_processed_datasets = Input(
            name="data_portal_processed_datasets",
            type=tuple,
            doc="data portal processed data to be saved",
            multiple=True,
            default=True,
        )

    def __init__(self, parent=None):
        super().__init__(parent)
        SuperviseProcess.__init__(self)
        WidgetLongProcessing.__init__(self)
        if not has_ewoksnotify:
            raise RuntimeError(
                "ewoksnotify not installed. Cannot define the PublishProcessedDataOW"
            )
        self.__on_going_task: int = 0
        """used to know how many tasks are on-going (as they are processed in parallel). Used to display processing wheel and processing"""

        self._window = PublishProcessedDataWindow(
            parent=self,
            beamlines=TOMO_BEAMLINES,
        )
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self._window)
        self._scan = None

        # load settings
        self._window.setConfiguration(self._ewoks_default_inputs)

        # connect signal / slot
        self._window.centralWidget().sigConfigChanged.connect(self._updateSettings)

    def _updateSettings(self):
        self._ewoks_default_inputs = self._window.getConfiguration()

    def setScan(self, scan: TomwerScanBase):
        self._scan = weakref.ref(scan)
        self._window.setScan(scan=scan)

    def getScan(self) -> TomwerScanBase | None:
        if self._scan is None:
            return None
        else:
            return self._scan()

    def _getScanFromIcatProcessedData(self) -> TomwerScanBase:
        """Return the associated scan to the latest set 'data_portal_processed_datasets'"""
        data_portal_processed_datasets = self.get_task_input_value(
            "data_portal_processed_datasets", None
        )
        if (
            data_portal_processed_datasets is None
            or len(data_portal_processed_datasets) == 0
        ):
            return None
        else:
            return data_portal_processed_datasets[0].source_scan

    def handleNewSignals(self) -> None:
        """Invoked by the workflow signal propagation manager after all
        signals handlers have been called.
        """
        # update the widget when receive the scan (proposal, dataset...)
        scan = self._getScanFromIcatProcessedData()
        # update processing wheel if necessary
        if self.__on_going_task == 0:
            self._startProcessing()
        self.__on_going_task += 1

        if scan is None:
            return

        if scan != self.getScan():
            self._window.setScan(scan)
        super().handleNewSignals()

    @Inputs.data_portal_processed_datasets
    def add(self, data_portal_processed_datasets, signal_id=None):
        # required because today ewoksorange is not handling multiple inputs
        self.set_dynamic_input(
            "data_portal_processed_datasets", data_portal_processed_datasets
        )

    def task_output_changed(self):
        # update processing wheel if necessary
        # task_output_changed is called when the ewoks task is finished from __ewoks_task_finished
        # call once even if there is 0..n outputs
        self.__on_going_task -= 1
        if self.__on_going_task == 0:
            self._endProcessing()
        return super().task_output_changed()

    def get_task_inputs(self):
        task_inputs = super().get_task_inputs()
        configuration = self._window.getConfiguration()

        task_inputs["beamline"] = configuration["beamline"]
        task_inputs["proposal"] = configuration["proposal"]
        task_inputs["__process__"] = weakref.ref(self)

        return task_inputs

    def sizeHint(self):
        return qt.QSize(500, 200)
