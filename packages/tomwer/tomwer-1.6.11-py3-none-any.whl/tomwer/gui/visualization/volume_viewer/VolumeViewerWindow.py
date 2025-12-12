from __future__ import annotations

import logging
import numpy
from functools import partial

from silx.gui import qt
from silx.gui.plot.ColorBar import ColorBarWidget as _ColorBarWidget

from tomoscan.volumebase import SliceTuple
from tomwer.gui.utils.qt_utils import block_signals

from .VolumeViewerWidget import VolumeViewerWidget
from .toolbar import ToolBar
from silx.gui.colors import Colormap

_logger = logging.getLogger(__name__)


class ColorBarWidget(_ColorBarWidget):
    def _activeImageChanged(self, previous, legend):
        # we are force to overwrite this function to avoid resetting the colormap when
        # image changes. Somehow just disconnection from `_disconnectPlot` is not enough
        pass


class VolumeViewerWindow(qt.QMainWindow):
    """
    Window dedicated to the volume reconstruction summary.
    It add a toolbar common to the three plots.
    """

    sigLoadVolume = qt.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._window = VolumeViewerWidget()
        self._slicesSet = False

        # main widget
        self.setCentralWidget(self._window)

        # colormap
        self._colormap = Colormap(name="gray", vmin=None, vmax=None)
        for plot in self._window.getPlots().values():
            plot.setDefaultColormap(self._colormap)
            plot.sigActiveImageChanged.connect(self._onSliceLoaded)

        # colorbar
        self._colorbarWidget = ColorBarWidget(
            plot=self._window.getMasterPlot(), parent=self._window
        )
        # Make colorbar background white
        self._colorbarWidget.setAutoFillBackground(True)
        self._colorbarWidget.layout().setSizeConstraint(qt.QLayout.SetNoConstraint)
        self._window._horizontalBottomSplitter.insertWidget(0, self._colorbarWidget)

        # window toolbar
        self._toolbar = ToolBar(
            master_plot=self._window.getMasterPlot(),
            parent=self._window.getMasterPlot(),
            colorbar=self._colorbarWidget,
            plots=self._window.getPlots().values(),
        )
        self.addToolBar(self._toolbar)

        # set up
        self._toolbar.showCoordinatesSystemLabel.setChecked(False)
        self._toolbar.showToolbar.setChecked(False)

        # connect signal / slot
        self._toolbar._loadVolumeWidget.toggled.connect(self.sigLoadVolume)
        self._toolbar.getExtendXYPlotAction().triggered.connect(
            partial(self.extendPlot, "XY")
        )
        self._toolbar.getExtendXZPlotAction().triggered.connect(
            partial(self.extendPlot, "XZ")
        )
        self._toolbar.getExtendYZPlotAction().triggered.connect(
            partial(self.extendPlot, "YZ")
        )
        self._toolbar.getResetDisplayAction().triggered.connect(
            partial(self.extendPlot, None)
        )
        self._toolbar.getCrosshairsAction().sigVisibilityChanged.connect(
            self._updateCrosshairsVisibility
        )

    def setSlicesAndMetadata(
        self,
        slices: dict[SliceTuple, numpy.ndarray],
        metadata: dict,
        volume_shape: tuple[int],
    ):
        self._slicesSet = len(slices) > 0
        self._colorbarWidget.setColormap(
            self._colormap, data=numpy.concatenate(tuple(slices.values()))
        )
        self._window.setVolumeShape(shape=volume_shape)
        self._window.setSlices(slices=slices)
        self._window.setVolumeMetadata(metadata=metadata, volume_shape=volume_shape)
        # required, especially because silx has known issues with it when keeping aspect ration
        self._window.resetZooms()
        self._updateCrosshairsVisibility()

    def _updateCrosshairsVisibility(self):
        plotXYMarkersVisible = (
            self._toolbar.getCrosshairsAction().isChecked()
            and not self._window._XYPlot2D.isLoading()
        )
        plotXZMarkersVisible = (
            self._toolbar.getCrosshairsAction().isChecked()
            and not self._window._XZPlot2D.isLoading()
        )
        plotYZMarkersVisible = (
            self._toolbar.getCrosshairsAction().isChecked()
            and not self._window._YZPlot2D.isLoading()
        )
        self._window.getCrossHairs().setVisible(
            plotXYMarkersVisible=plotXYMarkersVisible,
            plotXZMarkersVisible=plotXZMarkersVisible,
            plotYZMarkersVisible=plotYZMarkersVisible,
        )

    def setLoading(self, loading: bool):
        """Function to interrupt loading - when finished or failed."""
        self._window.setLoading(loading)
        self._updateCrosshairsVisibility()

    # expose API
    def getDefaultColormap(self) -> Colormap:
        return self._colormap

    def clear(self):
        self._slicesSet = False
        self._window.clear()

    def isLoadingVolume(self) -> bool:
        return self._toolbar._loadVolumeWidget.isChecked()

    def setLoadingVolume(self, loading_volume: bool) -> None:
        with block_signals(self):
            self._toolbar._loadVolumeWidget.setChecked(loading_volume)

    def setLoadingVolumeOptionVisible(self, visible) -> None:
        self._toolbar.getLoadVolumeAction().setVisible(visible)

    def initVolumePreview(self, *args, **kwargs):
        # reset colormap range to be able to update it when the first slice is displayed
        # (and before the full colormap is loaded in memory)
        self._colormap.setVRange(None, None)
        self._window.initVolumePreview(*args, **kwargs)
        self._updateCrosshairsVisibility()

    def _onSliceLoaded(self, previous, legend):
        """
        When a new slice is loaded and when the colormap min/max have not been set already we want to update the range
        from the current slice values
        """
        if not self._slicesSet:
            data = self.sender().getImage(legend).getData()
            vMin, vMax = self._colormap._computeAutoscaleRange(data=data)
            self._colormap.setVRange(vMin, vMax)
            with block_signals(self._colormap):
                self._colormap.setVRange(None, None)

    def extendPlot(self, plot_name):
        # FIXME: we are force to hide / show the colorbar else
        # when calling the `setSizes` function this class
        # messup with the layout / resizing... couldn't find the origin of it.
        visible = self._colorbarWidget.isVisible()
        self._colorbarWidget.setVisible(False)
        self._window.extendPlot(plot_name)
        self._colorbarWidget.setVisible(visible)

    def setVolume(self, volume):
        self._window.setVolume(volume=volume)
