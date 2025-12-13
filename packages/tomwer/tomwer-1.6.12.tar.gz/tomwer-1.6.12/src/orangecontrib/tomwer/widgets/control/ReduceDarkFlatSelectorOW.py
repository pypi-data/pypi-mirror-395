from __future__ import annotations

import logging

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output, OWBaseWidget

from tomwer.gui.control.reducedarkflatselector import ReduceDarkFlatSelectorDialog

logger = logging.getLogger(__name__)


class ReduceDarkFlatSelectorOW(OWBaseWidget, openclass=True):
    name = "reduce dark-flat selector"
    id = "orangecontrib.widgets.tomwer.control.ReduceDarkFlatSelectorOW.ReduceDarkFlatSelectorOW"
    description = "Allow user to select one or several reduced dark / flat"
    icon = "icons/reduced_darkflat_selector.svg"
    priority = 242
    keywords = [
        "tomography",
        "selection",
        "tomwer",
        "scan",
        "data",
        "reduce",
        "dark",
        "flat",
        "reduced",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _configuration = Setting(tuple())

    class Inputs:
        in_reduced_frames = Input(
            name="reduced frames",
            type=dict,
            doc="dict of containing reduced frames (either dark or flat)",
            multiple=True,
        )

    class Outputs:
        out_reduced_darks = Output(
            name="reduced dark(s)",
            doc="dict of containing reduced darks(s)",
            type=dict,
        )
        out_reduced_flats = Output(
            name="reduced flat(s)",
            type=dict,
            doc="dict of containing reduced flat(s)",
        )

    def __init__(self, parent=None):
        """ """
        super().__init__(parent)

        self._dialog = ReduceDarkFlatSelectorDialog(parent=self)
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.addWidget(self._dialog)

        self._dialog.setConfiguration(self._configuration)

        # connect signal / slot
        self._dialog.sigSelectActiveAsDarks.connect(self._sendDarks)
        self._dialog.sigSelectActiveAsFlats.connect(self._sendFlats)
        self._dialog.sigUpdated.connect(self._updateConfiguration)

    def _updateConfiguration(self):
        self._configuration = self.getConfiguration()

    def _sendDarks(self, darks: dict):
        self.Outputs.out_reduced_darks.send(darks)

    def _sendFlats(self, flats: dict):
        self.Outputs.out_reduced_flats.send(flats)

    @Inputs.in_reduced_frames
    def addReduceFrames(self, reduce_frames: dict | None, *args, **kwargs):
        if reduce_frames is not None:
            self._dialog.addReduceFrames(reduce_frames)

    # expose API
    def getConfiguration(self) -> tuple:
        return self._dialog.getConfiguration()

    def setConfiguration(self, configuration: tuple) -> None:
        if configuration is None:
            return
        return self._dialog.setConfiguration(configuration)
