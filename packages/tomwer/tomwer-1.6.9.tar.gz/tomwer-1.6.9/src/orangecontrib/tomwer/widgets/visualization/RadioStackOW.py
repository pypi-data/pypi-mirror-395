# coding: utf-8
from __future__ import annotations

import logging

from orangewidget import gui, widget
from orangewidget.widget import Input

from silx.gui import qt

import tomwer.core.process.visualization.radiostack
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.stacks import RadioStack

logger = logging.getLogger(__name__)


class RadioStackOW(widget.OWBaseWidget, openclass=True):
    """
    This widget will make stack radios incoming and allow user to browse into
    it.
    """

    name = "radio stack"
    id = "orange.widgets.tomwer.slicesstack.radiostack"
    description = (
        "This widget will save all scan path given to here "
        "and extract received radio files with there shortest"
        "unique basename to be able to browse them"
    )

    icon = "icons/radiosstack.svg"
    priority = 27
    keywords = ["tomography", "radio", "tomwer", "stack", "group"]

    ewokstaskclass = tomwer.core.process.visualization.radiostack._RadioStackPlaceHolder

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    class Inputs:
        data = Input(
            name="data",
            type=TomwerScanBase,
            multiple=True,
        )

    def __init__(self, parent=None):
        widget.OWBaseWidget.__init__(self, parent)
        self._box = gui.vBox(self.mainArea, self.name)
        self._viewer = RadioStack(parent=self)
        self._box.layout().addWidget(self._viewer)

    @Inputs.data
    def addLeafScan(self, scanID, *args, **kwargs):
        if scanID is None:
            return
        self._viewer.addTomoObj(scanID)

    def keyPressEvent(self, e):
        # TODO: fixme
        # here we want to avoid loading imageJ when enter is pressed.
        # the correct way would be to install an event filer
        # but this is ignored because the KeyPressEvent goes other it.
        # I don't really see why too annoyed at the point to look deeper
        if e.key() in (qt.Qt.Key_Enter, qt.Qt.Key_Return):
            pass
        else:
            super().keyPressEvent(e)
