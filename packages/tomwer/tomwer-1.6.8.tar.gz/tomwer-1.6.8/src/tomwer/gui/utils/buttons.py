"""
Button of general usage.
"""

from __future__ import annotations

import pint
import numpy
import logging
from silx.gui import qt
from silx.gui.plot.tools.roi import RegionOfInterestManager
from silx.gui.plot.items.roi import LineROI
from silx.gui.plot.PlotToolButtons import PlotToolButton

from tomwer.gui import icons

_logger = logging.getLogger(__file__)

_ureg = pint.get_application_registry()


class PadlockButton(qt.QPushButton):
    """Simple button to define a button with PadLock icons"""

    sigLockChanged = qt.Signal(bool)
    """signal emitted when the lock status change"""

    def __init__(self, parent):
        qt.QPushButton.__init__(self, parent)
        self._lockIcon = icons.getQIcon("locked")
        self._unlockIcon = icons.getQIcon("unlocked")
        self.setIcon(self._unlockIcon)
        self.setCheckable(True)

        # connect signals
        self.toggled.connect(self._updateDisplay)

    def setLock(self, lock: bool):
        self.setChecked(lock)
        self._updateDisplay(lock)

    def _updateDisplay(self, checked):
        _icon = self._lockIcon if checked else self._unlockIcon
        self.setIcon(_icon)
        self.sigLockChanged.emit(checked)

    def isLocked(self) -> bool:
        return self.isChecked()


class TabBrowsersButtons(qt.QWidget):
    """Simple widget containing buttons to go to 'next' or 'previous'"""

    sigPreviousReleased = qt.Signal()
    """emitted when the previous button is released"""
    sigNextReleased = qt.Signal()
    """emitted when the next button is released"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        # define gui
        style = qt.QApplication.style()
        self._previousButton = qt.QPushButton("previous", self)
        previous_icon = style.standardIcon(qt.QStyle.SP_ArrowLeft)
        self._previousButton.setIcon(previous_icon)
        self.layout().addWidget(self._previousButton)

        self._nextButton = qt.QPushButton("next", self)
        next_icon = style.standardIcon(qt.QStyle.SP_ArrowRight)
        self._nextButton.setIcon(next_icon)
        self.layout().addWidget(self._nextButton)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(spacer)

        # connect signal / slot
        self._previousButton.released.connect(self._previousReleased)
        self._nextButton.released.connect(self._nextReleased)

    def _previousReleased(self, *args, **kwargs):
        self.sigPreviousReleased.emit()

    def _nextReleased(self, *args, **kwargs):
        self.sigNextReleased.emit()


class TapeMeasureToolButton(PlotToolButton):
    """Button to active measurement between two point of the plot"""

    def __init__(self, parent=None, plot=None, pixel_size: pint.Quantity | None = None):
        super().__init__(parent=parent, plot=plot)
        self._roiManager = None
        self._lastRoiCreated = None
        self._pixel_size: pint.Quantity | None = pixel_size
        self.setIcon(icons.getQIcon("ruler"))
        self.setToolTip("measure distance between two pixels")
        self.toggled.connect(self._callback)
        self._connectPlot(plot)

    def setPlot(self, plot):
        return super().setPlot(plot)

    def setPixelSize(self, pixel_size: tuple[pint.Quantity, pint.Quantity] | None):
        self._pixel_size = pixel_size

    def _callback(self, toggled):
        if not self._roiManager:
            return
        if self._lastRoiCreated is not None:
            self._lastRoiCreated.setVisible(self.isChecked())
        if self.isChecked():
            self._roiManager.start(
                TapeMeasureROI,
                self,
            )
            self.__interactiveModeStarted(self._roiManager)
        else:
            source = self._roiManager.getInteractionSource()
            if source is self:
                self._roiManager.stop()

    def __interactiveModeStarted(self, roiManager):
        roiManager.sigInteractiveModeFinished.connect(self.__interactiveModeFinished)

    def __interactiveModeFinished(self):
        roiManager = self._roiManager
        if roiManager is not None:
            roiManager.sigInteractiveModeFinished.disconnect(
                self.__interactiveModeFinished
            )
        self.setChecked(False)

    def _connectPlot(self, plot):
        """
        Called when the plot is connected to the widget
        :param plot: :class:`.PlotWidget` instance
        """
        if plot is None:
            return
        self._roiManager = RegionOfInterestManager(plot)
        self._roiManager.setColor("yellow")  # Set the color of ROI
        self._roiManager.sigRoiAdded.connect(self._registerCurrentROI)

    def _disconnectPlot(self, plot):
        if plot and self._lastRoiCreated is not None:
            self._roiManager.removeRoi(self._lastRoiCreated)
            self._lastRoiCreated = None
        return super()._disconnectPlot(plot)

    def _registerCurrentROI(self, currentRoi):
        if self._lastRoiCreated is None:
            self._lastRoiCreated = currentRoi
            self._lastRoiCreated.setPixelSize(self._pixel_size)
        elif currentRoi != self._lastRoiCreated and self._roiManager is not None:
            self._roiManager.removeRoi(self._lastRoiCreated)
            self._lastRoiCreated = currentRoi
            self._lastRoiCreated.setPixelSize(self._pixel_size)


class TapeMeasureROI(LineROI):
    """ROI dedicated to tape measure"""

    def __init__(self, parent=None, pixel_size: pint.Quantity | None = None):
        super().__init__(parent)
        self._pixel_size: pint.Quantity | None = None
        self.setPixelSize(pixel_size)

    def setEndPoints(self, startPoint, endPoint):
        distance_px = numpy.linalg.norm(endPoint - startPoint)
        super().setEndPoints(startPoint=startPoint, endPoint=endPoint)
        if self._pixel_size is None:
            self._updateText(f"{distance_px :.1f}px")
        else:
            distance_m = distance_px * self._pixel_size
            value = self.cast_metric_to_best_unit(distance_m)
            self._updateText(f"{value:.4f~P}")

    def setPixelSize(self, pixel_size: tuple[pint.Quantity]):
        if isinstance(pixel_size, (tuple, list)):
            assert (
                len(pixel_size) == 2
            ), "expects at most two pixel size values (x and y values)"
            if not numpy.isclose(
                pixel_size[0].to_base_units(), pixel_size[1].to_base_units()
            ):
                value = self.cast_metric_to_best_unit(pixel_size[0])
                _logger.warning(
                    f"TapeMeasure is only handling square pixels for now. Will consider the pixel is {value:.4f~P}x{value:.4f~P}"
                )
            pixel_size = pixel_size[0]
        self._pixel_size = pixel_size

    @staticmethod
    def cast_metric_to_best_unit(value: pint.Quantity) -> pint.Quantity:
        value = value.to_base_units()
        if value < (1.0 * _ureg.micrometer):
            return value.to(_ureg.nanometer)
        elif value < (0.1 * _ureg.millimeter):  # prefer mm to um
            return value.to(_ureg.micrometer)
        elif value < (1.0 * _ureg.centimeter):
            return value.to(_ureg.millimeter)
        elif value < (1.0 * _ureg.meter):
            return value.to(_ureg.centimeter)
        else:
            return value.to(_ureg.meter)
