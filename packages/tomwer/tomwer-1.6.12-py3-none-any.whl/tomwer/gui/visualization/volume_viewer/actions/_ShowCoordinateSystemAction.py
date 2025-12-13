from __future__ import annotations

import weakref
from silx.gui import qt

from tomwer.gui import icons


class ShowCoordinateSystemAction(qt.QAction):
    """
    QAction to show / hide the coordinate system vignette of the plots
    """

    STATE = None
    """Lazy loaded states used to feed the coordinate system"""

    def __init__(self, plots: tuple, parent=None):
        icon = icons.getQIcon("show_3D_coordinate_system")
        text = "Toggle 3D coordinate system"
        super().__init__(parent=parent, icon=icon, text=text)

        self.setToolTip("Toggle 3D coordinate system of slice plots")
        self.setCheckable(True)
        self.setChecked(True)

        self._plots = [weakref.ref(plot) for plot in plots]

        self.triggered[bool].connect(self._updateCoordinateSystemVisibility)

    def _updateCoordinateSystemVisibility(self, visible):
        """Handle Plot set keep aspect ratio signal"""
        for ref_plot in self._plots:
            plot = ref_plot()
            if plot:
                plot.setCoordinateSystemVisible(visible)
