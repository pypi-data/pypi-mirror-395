from __future__ import annotations

import weakref
from silx.gui import qt

from silx.gui import icons as silx_icons


class ColorBarAction(qt.QAction):
    """
    QAction opening the ColorBarWidget of the specified plot.
    It was not possible to inherit the one from silx because it inherit from a PlotAction which is not the case of this one (n plots...)
    """

    def __init__(self, colorbar, parent=None):
        icon = silx_icons.getQIcon("colorbar")
        text = "Colorbar"
        super().__init__(parent=parent, icon=icon, text=text)

        self.setToolTip("Show/Hide the colorbar")
        self.setCheckable(True)

        self.triggered[bool].connect(self._actionTriggered)
        colorbar.sigVisibleChanged.connect(self._widgetVisibleChanged)
        self._colorBar = weakref.ref(colorbar)

    def _widgetVisibleChanged(self, isVisible):
        """Callback when the colorbar `visible` property change."""
        if self.isChecked() == isVisible:
            return
        self.setChecked(isVisible)

    def _actionTriggered(self, checked=False):
        """Create a cmap dialog and update active image and default colormap."""

        colorBar = self._colorBar()
        if colorBar is None:
            return
        if not colorBar.isHidden() == checked:
            return

        colorBar.setVisible(checked)
