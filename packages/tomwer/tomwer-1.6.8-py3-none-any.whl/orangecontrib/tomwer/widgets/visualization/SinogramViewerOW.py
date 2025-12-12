# coding: utf-8
from __future__ import annotations

import logging

from orangewidget import gui, widget
from orangewidget.widget import Input

import tomwer.core.process.visualization.sinogramviewer
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.visualization.sinogramviewer import SinogramViewer

from ..utils import WidgetLongProcessing

logger = logging.getLogger(__name__)


class SinogramViewerOW(WidgetLongProcessing, widget.OWBaseWidget, openclass=True):
    """
    This widget can be used to compute and display a specific sinogram from an
    acquisition.
    """

    name = "sinogram viewer"
    id = "orange.widgets.tomwer.visualization.sinogramviewer"
    description = (
        "This widget can be used to compute and display a "
        "specific sinogram from an acquisition."
    )

    icon = "icons/sinogramviewer.png"
    priority = 5
    keywords = ["tomography", "sinogram", "radio"]

    ewokstaskclass = (
        tomwer.core.process.visualization.sinogramviewer._SinogramViewerPlaceHolder
    )

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    class Inputs:
        data = Input(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        widget.OWBaseWidget.__init__(self, parent)
        WidgetLongProcessing.__init__(self)
        self._box = gui.vBox(self.mainArea, self.name)
        self._viewer = SinogramViewer(parent=self)
        self._box.layout().addWidget(self._viewer)

        # connect signal / slot
        self._viewer.sigSinoLoadStarted.connect(self._startProcessing)
        self._viewer.sigSinoLoadEnded.connect(self._endProcessing)

    @Inputs.data
    def addLeafScan(self, scanID):
        if scanID is None:
            return
        self._viewer.setScan(scanID)

    def close(self):
        self._viewer.close()
        super().close()
