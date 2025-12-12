from __future__ import annotations

import logging

from orangewidget import gui, widget
from processview.gui.processmanager import ProcessManagerWindow

logger = logging.getLogger(__name__)


class AdvancementOW(widget.OWBaseWidget, openclass=True):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """

    # note of this widget should be the one registred on the documentation
    name = "advancement"
    id = "orangecontrib.widgets.tomwer.control.AdvancementOW.AdvancementOW"
    description = "This widget can display advancement of processes and scans"
    icon = "icons/advancement.svg"
    priority = 5
    keywords = ["tomography", "process", "advancement"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    def __init__(self, parent=None):
        widget.OWBaseWidget.__init__(self, parent)

        self._widget = ProcessManagerWindow(parent=self)

        self._box = gui.vBox(self.mainArea, self.name)
        layout = self._box.layout()
        layout.addWidget(self._widget)
