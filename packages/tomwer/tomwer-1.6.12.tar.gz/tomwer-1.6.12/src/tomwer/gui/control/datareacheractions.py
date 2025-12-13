# coding: utf-8
from __future__ import annotations

from silx.gui import qt

from tomwer.gui import icons as tomwericons


class HistoryAction(qt.QAction):
    """
    Action displaying the history of finished scans
    """

    def __init__(self, parent):
        icon = tomwericons.getQIcon("history")
        qt.QAction.__init__(self, icon, "history", parent)
        self.setCheckable(True)


class ConfigurationAction(qt.QAction):
    """
    Action to show the configuration dialog
    """

    def __init__(self, parent):
        icon = tomwericons.getQIcon("parameters")
        qt.QAction.__init__(self, icon, "configuration", parent)
        self.setCheckable(True)


class ObservationAction(qt.QAction):
    """
    Action to show the observation dialog
    """

    def __init__(self, parent):
        icon = tomwericons.getQIcon("loop")
        qt.QAction.__init__(self, icon, "observations", parent)
        self.setCheckable(True)


class ControlAction(qt.QAction):
    """
    Action to control the datawatcher (see status and select folder)
    """

    def __init__(self, parent):
        icon = tomwericons.getQIcon("health")
        qt.QAction.__init__(self, icon, "control", parent)
        self.setCheckable(True)
