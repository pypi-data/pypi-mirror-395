# coding: utf-8
from __future__ import annotations

from silx.gui import qt
from functools import partial

from tomwer.gui import icons as tomwer_icons
from tomwer.gui.control.tomoobjdisplaymode import DisplayMode


class NXTomomillParamsAction(qt.QAction):
    """
    Action to display a window with nxtomomill configuration
    """

    def __init__(self, parent):
        icon = tomwer_icons.getQIcon("parameters")

        qt.QAction.__init__(self, icon, "filter configuration", parent)
        self.setToolTip("Open dialog to configure nxtomomill parameters")
        self.setCheckable(False)


class CFGFileActiveLabel(qt.QLabel):
    """Label used to display if the .cfg file is active or not"""

    def __init__(self, parent):
        super().__init__(parent)
        icon = tomwer_icons.getQIcon("cfg_file_inactive")
        self.setToolTip("no valid cfg file provided")
        self.setPixmap(icon.pixmap(self.width(), self.height()))

    def setActive(self, active=True):
        if active is True:
            icon = tomwer_icons.getQIcon("cfg_file_active")
            tooltip = "will use the provided .cfg file"
        else:
            icon = tomwer_icons.getQIcon("cfg_file_inactive")
            tooltip = "will use default configuration"

        self.setPixmap(icon.pixmap(self.width(), self.height()))
        self.setToolTip(tooltip)

    def setInactive(self):
        self.setActive(active=False)


class TomoObjDisplayModeToolButton(qt.QToolButton):
    """
    Button to change the way tomo object are displayed.
    Either using the full url or only a 'short' description.
    """

    sigDisplayModeChanged = qt.Signal(str)
    """signal emit when the display mode change"""

    _SHORT_DESC_TOOLTIP = "Use a short description of the tomo object. Two different scans can have the same short desciption"
    _URL_TOOLTIP = (
        "Use the full url to display the tomo object. Url is guaranted to be unique."
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._shortDescIcon = tomwer_icons.getQIcon("short_description")
        shortDescAction = qt.QAction(self._shortDescIcon, "short description", self)
        shortDescAction.setToolTip(self._SHORT_DESC_TOOLTIP)

        self._urlIcon = tomwer_icons.getQIcon("url")
        urlDescAction = qt.QAction(self._urlIcon, "url", self)
        urlDescAction.setToolTip(self._URL_TOOLTIP)

        menu = qt.QMenu(self)
        menu.addAction(shortDescAction)
        menu.addAction(urlDescAction)
        self.setMenu(menu)
        self.setPopupMode(qt.QToolButton.InstantPopup)

        # set up
        self.setDisplayMode(DisplayMode.SHORT)

        # connect signal / slot
        shortDescAction.triggered.connect(
            partial(self.setDisplayMode, DisplayMode.SHORT)
        )
        urlDescAction.triggered.connect(partial(self.setDisplayMode, DisplayMode.URL))

    def setDisplayMode(self, mode: DisplayMode):
        mode = DisplayMode(mode)
        if mode is DisplayMode.SHORT:
            self.setIcon(self._shortDescIcon)
            self.setToolTip(self._SHORT_DESC_TOOLTIP)
        elif mode is DisplayMode.URL:
            self.setIcon(self._urlIcon)
            self.setToolTip(self._URL_TOOLTIP)
        else:
            raise ValueError(f"display mode {mode} not handled")
        self.sigDisplayModeChanged.emit(mode.value)
