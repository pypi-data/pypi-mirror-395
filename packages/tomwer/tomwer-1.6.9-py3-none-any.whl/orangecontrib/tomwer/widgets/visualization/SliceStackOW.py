# coding: utf-8
from __future__ import annotations


import logging

from orangewidget import gui, widget
from orangewidget.widget import Input

from silx.gui import qt

import tomwer.core.process.visualization.slicestack
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.stacks import SliceStack

logger = logging.getLogger(__name__)


class SlicesStackOW(widget.OWBaseWidget, openclass=True):
    """
    This widget will make copy or virtual link to all received *slice* files
    in order to group them all in one place and be able to browse those
    (using the image stack of view in orange or a third software as silx view)

    Options are:
       - copy files or create sym link (set to sym link)
       - overwrite if existing (set to False)

    Behavior:
        When the process receives a new data path ([scanPath]/[scan]) and if
        no output folder has been defined manually them it will try to create
        the folder [scanPath]/slices if not existing in order to redirect
        the slices files.
        If fails will ask for a directory.
        If the output folder is already existing then move directly to the
        copy.
    """

    name = "slice stack"
    id = "orange.widgets.tomwer.slicesstack.slicesstack"
    description = (
        "This widget will save all scan path given to here "
        "and extract received *slice* files with there shortest"
        "unique basename to be able to browse them"
    )

    icon = "icons/slicesstack.svg"
    priority = 26
    keywords = ["tomography", "slices", "tomwer", "stack", "group"]

    ewokstaskclass = tomwer.core.process.visualization.slicestack._SliceStackPlaceHolder

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
        self._viewer = SliceStack(parent=self)
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
