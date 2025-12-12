# coding: utf-8
from __future__ import annotations

from orangewidget import gui, widget
from orangewidget.widget import Input

from tomwer.gui.debugtools.objectinspector import ObjectInspector


class ObjectInspectorOW(widget.OWBaseWidget, openclass=True):
    """
    A simple widget to browse a TomwerScanBase object
    """

    name = "tomwer object browser"
    id = "orangecontrib.tomwer.widgets.debugtools.tomwerscanbasebrowser"
    description = "create on the fly dataset"
    icon = "icons/inspector.png"
    priority = 255
    keywords = ["tomography", "file", "tomwer", "dataset", "debug"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    class Inputs:
        data = Input(name="object", type=object)

    def __init__(self, parent=None):
        widget.OWBaseWidget.__init__(self, parent=parent)
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self.inspector = ObjectInspector(parent=self)
        self._layout.addWidget(self.inspector)

    @Inputs.data
    def setObject(self, obj):
        self.inspector.setObject(obj)
