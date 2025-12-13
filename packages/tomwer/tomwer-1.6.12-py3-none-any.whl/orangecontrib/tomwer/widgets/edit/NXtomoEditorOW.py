from __future__ import annotations

import logging

from orangewidget import gui
from orangewidget.settings import Setting
from silx.gui import qt
from ewokscore.missing_data import MISSING_DATA

from ...orange.managedprocess import TomwerWithStackStack

from tomwer.core.scan.nxtomoscan import NXtomoScan
import tomwer.core.process.edit.nxtomoeditor
from tomwer.gui.edit.nxtomoeditor import NXtomoEditorDialog as _NXtomoEditorDialog

from ...orange.managedprocess import _SuperviseMixIn

_logger = logging.getLogger(__name__)


class NXtomoEditorDialog(_NXtomoEditorDialog):

    def __init__(self, parent, *args, **kwargs) -> None:
        assert isinstance(parent, _SuperviseMixIn)
        super().__init__(parent, *args, **kwargs)


class NXtomoEditorOW(
    TomwerWithStackStack,
    ewokstaskclass=tomwer.core.process.edit.nxtomoeditor.NXtomoEditorTask,
):
    """
    Widget to edit manually a NXtomo
    """

    name = "nxtomo-editor"
    id = "orange.widgets.tomwer.edit.NXtomoEditorOW.NXtomoEditorOW"
    description = "Interface to edit manually a NXtomo"
    icon = "icons/nx_tomo_editor.svg"
    priority = 10
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "edition",
        "NXTomo",
        "editor",
        "energy",
        "distance",
        "pixel size",
    ]
    _ewoks_inputs_to_hide_from_orange = ("configuration",)

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    sigScanReady = qt.Signal(str)
    """emit when scan ready. Used for test only"""

    settings = Setting(dict())

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = NXtomoEditorDialog(parent=self, hide_lockers=False)
        _layout.addWidget(self.widget)
        self.widget.mainWidget.sigEditingFinished.connect(self._updateSettings)

        # load settings
        self.widget.setConfiguration(self.settings)

        # connect signal / slot
        self.widget._buttons.button(qt.QDialogButtonBox.Ok).released.connect(
            self.execute_ewoks_task
        )

    def _updateSettings(self):
        self.settings = self.getConfiguration()

    def handleNewSignals(self) -> None:
        scan = self.get_task_input_value("data", MISSING_DATA)
        if scan not in (MISSING_DATA, None):
            self._setScan(scan=scan)
        # return super().handleNewSignals() do not call to make sure the processing is not triggered

    def setScan(self, scan: NXtomoScan | None):
        self.set_dynamic_input("data", scan)
        self._setScan(scan=scan)

    def _setScan(self, scan: NXtomoScan | None):
        if not isinstance(scan, NXtomoScan):
            raise TypeError(
                f"expect to have an instance of {NXtomoScan}. {type(scan)} provided."
            )

        self.widget.setScan(scan)
        if self.widget.hasLockField():
            super().execute_ewoks_task()
        else:
            self.show()
            self.raise_()

    def task_output_changed(self) -> None:
        self.sigScanReady.emit(str(self.get_task_output_value("data")))
        super().task_output_changed()

    def get_task_inputs(self):
        task_inputs = super().get_task_inputs()
        task_inputs.update(
            {
                "configuration": self.widget.getConfigurationForTask(),
            }
        )
        return task_inputs

    def sizeHint(self):
        return qt.QSize(400, 500)

    # expose API
    def getConfiguration(self) -> dict:
        return self.widget.getConfiguration()

    def setConfiguration(self, config: dict):
        self.widget.setConfiguration(config)
