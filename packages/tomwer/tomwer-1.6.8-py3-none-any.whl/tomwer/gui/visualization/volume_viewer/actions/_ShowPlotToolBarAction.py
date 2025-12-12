from __future__ import annotations

import weakref
from silx.gui import qt

from tomwer.gui import icons
from silx.gui.plot import PlotWidget


class ShowPlotToolBarAction(qt.QAction):
    """
    QAction opening the ColorBarWidget of the specified plot.
    It was not possible to inherit the one from silx because it inherit from a PlotAction which is not the case of this one (n plots...)
    """

    def __init__(self, plots: tuple[PlotWidget], parent=None):
        icon = icons.getQIcon("show_plot_toolbars")
        text = "show plot toolbars"
        super().__init__(parent=parent, icon=icon, text=text)

        self.setToolTip("Show/Hide plot toolbars")
        self.setCheckable(True)
        self.setChecked(True)

        self._plots = [weakref.ref(plot) for plot in plots]

        self.triggered[bool].connect(self._actionTriggered)

    def _actionTriggered(self, checked=False):
        """Create a cmap dialog and update active image and default colormap."""
        for ref_plot in self._plots:
            plot = ref_plot()
            if plot:
                plot.setToolBarsVisible(checked)
