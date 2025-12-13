# coding: utf-8
from __future__ import annotations

import logging
import os

from orangewidget import gui, widget
from orangewidget.widget import Input

from silx.gui import qt

import tomwer.core.process.visualization.samplemoved
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.samplemoved import SampleMovedWidget

logger = logging.getLogger(__name__)


class SampleMovedOW(widget.OWBaseWidget, openclass=True):
    """
    Simple widget exposing two images side by side to see if a sample moved
    during the acquisition.

    :param parent: the parent widget
    """

    name = "sample moved"
    id = "orange.widgets.tomwer.samplemoved"
    description = (
        "This widget is used to display two scan side by side "
        "to know if a sample moved during the acquisition by "
        "simple observation."
    )
    icon = "icons/sampleMoved.svg"
    priority = 85
    keywords = ["tomography", "sample", "moved", "visualization"]

    ewokstaskclass = (
        tomwer.core.process.visualization.samplemoved._SampleMovedPlaceHolder
    )

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    class Inputs:
        data = Input(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = gui.vBox(self.mainArea, self.name).layout()

        self._widgetScanPath = qt.QWidget(parent=self)
        self._widgetScanPath.setLayout(qt.QHBoxLayout())
        self._widgetScanPath.layout().addWidget(
            qt.QLabel("scan: ", parent=self._widgetScanPath)
        )
        self._scanNameQLabel = qt.QLabel("", parent=self._widgetScanPath)
        self._widgetScanPath.layout().addWidget(self._scanNameQLabel)
        spacer = qt.QWidget(parent=self._widgetScanPath)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._widgetScanPath.layout().addWidget(spacer)
        layout.addWidget(self._widgetScanPath)

        self._mainWidget = SampleMovedWidget(parent=self)
        layout.addWidget(self._mainWidget)

    def sizeHint(self):
        return qt.QSize(400, 200)

    @Inputs.data
    def updateScan(self, scan):
        if scan is None:
            return

        assert isinstance(scan, TomwerScanBase)
        if os.path.isdir(scan.path):
            self._scanNameQLabel.setText(os.path.basename(scan.path))
            rawSlices = scan.get_proj_angle_url()

            self._mainWidget.clearOnLoadActions()
            self._mainWidget.setImages(rawSlices)
            self._mainWidget.setScan(scan)
            self._mainWidget.setOnLoadAction(scan.flat_field_correction)

    def clear(self):
        self._scanNameQLabel.setText("")
        self._mainWidget.clear()
