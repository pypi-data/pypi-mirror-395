from __future__ import annotations


from silx.gui import qt
from silx.gui.plot import actions
from tomwer.gui import icons as tomwer_icons

from .actions._ColorBarAction import ColorBarAction
from .actions._ShowAxesAction import ShowAxesAction
from .actions._ShowCoordinateSystemAction import ShowCoordinateSystemAction
from .actions._ShowCoordinateSystemLabelAction import ShowCoordinateSystemLabelAction
from .actions._ShowCrosshairsAction import ShowCrosshairsAction
from .actions._ShowPlotToolBarAction import ShowPlotToolBarAction


class ToolBar(qt.QToolBar):
    """Specialized toolbar for the VolumeReconstructionSummaryWindow"""

    def __init__(self, master_plot, colorbar, plots, parent=None):
        super().__init__(parent=parent)

        # colormap action
        self._colormapAction = actions.control.ColormapAction(
            parent=self, plot=master_plot
        )
        master_plot.sigActiveImageChanged.disconnect(
            self._colormapAction._updateColormap
        )
        master_plot.sigActiveScatterChanged.disconnect(
            self._colormapAction._updateColormap
        )
        self.addAction(self._colormapAction)

        # colorbar action
        self.colorbarAction = ColorBarAction(colorbar=colorbar, parent=self)
        self.colorbarAction.setVisible(True)
        self.colorbarAction.setChecked(True)
        self.addAction(self.colorbarAction)

        # show axes
        self.showAxesAction = ShowAxesAction(parent=self, plots=plots)
        self.addAction(self.showAxesAction)

        # Toggle coordinate system
        self.showCoordinateSystem = ShowCoordinateSystemAction(
            plots=[plot.parent() for plot in plots], parent=self
        )
        self.addAction(self.showCoordinateSystem)

        # Toggle labels
        self.showCoordinatesSystemLabel = ShowCoordinateSystemLabelAction(
            plots=[plot.parent() for plot in plots], parent=self
        )
        self.addAction(self.showCoordinatesSystemLabel)

        # Toggle toolbar action
        self.showToolbar = ShowPlotToolBarAction(
            plots=[plot.parent() for plot in plots], parent=self
        )
        self.addAction(self.showToolbar)

        # separator
        self.addSeparator()

        self._showCrosshairsAction = ShowCrosshairsAction()
        self.addAction(self._showCrosshairsAction)

        # separator
        self.addSeparator()

        # load volume
        self._loadVolumeWidget = qt.QCheckBox("load volume")
        self._loadVolumeWidget.setToolTip(
            "Loading the volume in memory will allow you to browse the slices along the three dimensions. But it will consume a lot of RAM."
        )
        self._loadVolumeAction = self.addWidget(self._loadVolumeWidget)

        # separator
        self.addSeparator()

        # display a single axis
        axis0_icon = tomwer_icons.getQIcon("extend_3D_coordinate_system_XY")
        self._extendXYPlotAction = qt.QAction(axis0_icon, "extend XY plot")
        self.addAction(self._extendXYPlotAction)

        axis1_icon = tomwer_icons.getQIcon("extend_3D_coordinate_system_XZ")
        self._extendXZPlotAction = qt.QAction(axis1_icon, "extend XZ plot")
        self.addAction(self._extendXZPlotAction)

        axis2_icon = tomwer_icons.getQIcon("extend_3D_coordinate_system_YZ")
        self._extendYZPlotAction = qt.QAction(axis2_icon, "extend YZ plot")
        self.addAction(self._extendYZPlotAction)

        # equally space plots
        reset_display_icon = tomwer_icons.getQIcon("reset_3D_coordinate_system")
        self._resetDisplayAction = qt.QAction(
            reset_display_icon, "Reset plots position."
        )
        self.addAction(self._resetDisplayAction)

    # Action getters
    def getLoadVolumeAction(self):
        return self._loadVolumeAction

    def getExtendXYPlotAction(self) -> qt.QAction:
        return self._extendXYPlotAction

    def getExtendXZPlotAction(self) -> qt.QAction:
        return self._extendXZPlotAction

    def getExtendYZPlotAction(self) -> qt.QAction:
        return self._extendYZPlotAction

    def getResetDisplayAction(self) -> qt.QAction:
        return self._resetDisplayAction

    def getCrosshairsAction(self) -> ShowCrosshairsAction:
        return self._showCrosshairsAction
