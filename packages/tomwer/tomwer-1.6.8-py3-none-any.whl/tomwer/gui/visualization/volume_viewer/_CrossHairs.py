from __future__ import annotations

from ._TomoPlot2DSlices import _TomoPlot2D
from silx.gui.plot.items import XMarker, YMarker
from silx.gui import qt


class CrossHairs:
    """
    A class to manage and group markers within the VolumeViewerWidget.

    This class provides an API to:
    - Show or hide markers.
    - Update marker positions dynamically.
    """

    XYColor = qt.QColor(255, 0, 0, 180)
    YZColor = qt.QColor(0, 0, 255, 180)
    XZColor = qt.QColor(0, 255, 0, 180)

    def __init__(self, XYPlot: _TomoPlot2D, XZPlot: _TomoPlot2D, YZPlot: _TomoPlot2D):
        self._XYPlot = XYPlot.getPlot()
        self._XZPlot = XZPlot.getPlot()
        self._YZPlot = YZPlot.getPlot()

        self._XYPlot_XMarker = YMarker()
        # Warning about naming: the pattern is '_XYPlot_[X|Y|Z]Marker'. In this case, the marker drawing the Y axis happens to be a XMarker.
        self._XYPlot_XMarker.setColor(CrossHairs.YZColor)
        self._XYPlot.addItem(self._XYPlot_XMarker)
        self._XYPlot_YMarker = XMarker()
        self._XYPlot_YMarker.setColor(CrossHairs.XZColor)
        self._XYPlot.addItem(self._XYPlot_YMarker)

        self._XZPlot_ZMarker = YMarker()
        self._XZPlot.addItem(self._XZPlot_ZMarker)
        self._XZPlot_ZMarker.setColor(CrossHairs.XYColor)
        self._XZPlot_XMarker = XMarker()
        self._XZPlot.addItem(self._XZPlot_XMarker)
        self._XZPlot_XMarker.setColor(CrossHairs.YZColor)

        self._YZPlot_ZMarker = YMarker()
        self._YZPlot.addItem(self._YZPlot_ZMarker)
        self._YZPlot_ZMarker.setColor(CrossHairs.XYColor)
        self._YZPlot_YMarker = XMarker()
        self._YZPlot.addItem(self._YZPlot_YMarker)
        self._YZPlot_YMarker.setColor(CrossHairs.XZColor)

    def getMarkers(self) -> dict[str, XMarker | YMarker]:
        return {
            "XYPlot": {
                "YMarker": self._XYPlot_YMarker,
                "XMarker": self._XYPlot_XMarker,
            },
            "XZPlot": {
                "XMarker": self._XZPlot_XMarker,
                "ZMarker": self._XZPlot_ZMarker,
            },
            "YZPlot": {
                "YMarker": self._YZPlot_YMarker,
                "ZMarker": self._YZPlot_ZMarker,
            },
        }

    def setVisible(
        self,
        plotXYMarkersVisible: bool,
        plotXZMarkersVisible: bool,
        plotYZMarkersVisible: bool,
    ):
        self._XYPlot_XMarker.setVisible(plotXYMarkersVisible)
        self._XYPlot_YMarker.setVisible(plotXYMarkersVisible)

        self._XZPlot_XMarker.setVisible(plotXZMarkersVisible)
        self._XZPlot_ZMarker.setVisible(plotXZMarkersVisible)

        self._YZPlot_YMarker.setVisible(plotYZMarkersVisible)
        self._YZPlot_ZMarker.setVisible(plotYZMarkersVisible)

    def updateMarkers(self, XYIndex: int, XZIndex: int, YZIndex: int):
        """
        Update marker positions according to the different XY, XZ, YZ positions
        """
        self._XYPlot_YMarker.setPosition(XZIndex, 0)
        self._XYPlot_XMarker.setPosition(0, YZIndex)

        self._XZPlot_XMarker.setPosition(YZIndex, 0)
        self._XZPlot_ZMarker.setPosition(0, XYIndex)

        self._YZPlot_ZMarker.setPosition(0, XYIndex)
        self._YZPlot_YMarker.setPosition(XZIndex, 0)
