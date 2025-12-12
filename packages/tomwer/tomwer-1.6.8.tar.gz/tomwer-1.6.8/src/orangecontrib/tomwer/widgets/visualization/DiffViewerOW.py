# coding: utf-8
from __future__ import annotations

import logging

from orangewidget import gui, widget
from orangewidget.widget import Input

from silx.gui import qt

import tomwer.core.process.visualization.diffviewer
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.visualization.diffviewer import DiffFrameViewer

_logger = logging.getLogger(__name__)


class DiffViewerOW(widget.OWBaseWidget, openclass=True):
    """
    Associate TomoScanBase with the silx's ComparaImage tool.
    Allows to compare two random frame.
    """

    name = "diff frame viewer"
    id = "orangecontrib.tomwer.widgets.visualization.diffviewerow"
    description = "Allows comparison between two random frame from a scan"
    icon = "icons/diff.png"
    priority = 107
    keywords = ["tomography", "diff", "tomwer", "compare", "comparison"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    ewokstaskclass = tomwer.core.process.visualization.diffviewer._DiffViewerPlaceHolder

    class Inputs:
        data = Input(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        widget.OWBaseWidget.__init__(self, parent)
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self.viewer = DiffFrameViewer(parent=self)
        self._layout.addWidget(self.viewer)

    @Inputs.data
    def addScan(self, scan):
        if scan is None:
            return
        self.viewer.addScan(scan)

    def sizeHint(self):
        return qt.QSize(500, 700)
