from __future__ import annotations

from silx.gui.plot import Plot2D
from tomwer.gui.utils.buttons import TapeMeasureToolButton
from tomwer.gui.settings import Y_AXIS_DOWNWARD


class TomoPlot2D(Plot2D):
    """Plot set up for tomography and to display reconstructed slices"""

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)
        self.setYAxisInverted(Y_AXIS_DOWNWARD)
        self.setKeepDataAspectRatio(True)
        self.setAxesDisplayed(False)

        self._tapeMeasureButton = TapeMeasureToolButton(parent=self, plot=self)
        self._tapeMeasureButton.setCheckable(True)

        self.toolBar().addWidget(self._tapeMeasureButton)

    def setVoxelSize(self, size: float | None):
        """set the pixel size to be used by the ruler"""
        self._tapeMeasureButton.setPixelSize(pixel_size=size)

    def setToolbarVisible(self, visible):
        self.toolBar().setVisible(visible)
