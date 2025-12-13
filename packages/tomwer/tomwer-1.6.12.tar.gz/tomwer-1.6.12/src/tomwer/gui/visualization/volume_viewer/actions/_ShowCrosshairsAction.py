from __future__ import annotations

from silx.gui import qt

from tomwer.gui import icons


class ShowCrosshairsAction(qt.QAction):
    """
    QAction to show / hide the plots crosshairs
    """

    sigVisibilityChanged = qt.Signal()

    def __init__(self, parent=None):
        icon = icons.getQIcon("crosshairs")
        text = "Toggle Crosshairs"
        super().__init__(parent=parent, icon=icon, text=text)

        self.setToolTip("Toggle Slice Plots Crosshairs")
        self.setCheckable(True)
        self.setChecked(True)

        self.triggered[bool].connect(self.sigVisibilityChanged)
