from __future__ import annotations

import numpy
from silx.gui import qt
from silx.gui.utils import concurrent

from silx.gui.widgets.WaitingOverlay import WaitingOverlay
import logging

from tomoscan.volumebase import SliceTuple

from tomwer.gui import icons as tomwer_icons
from tomwer.gui.visualization.TomoPlot2D import TomoPlot2D as _TomoPlot2D

from tomwer.core.volume.volumebase import TomwerVolumeBase

from ._HorizontalSliderWithBrowser import HorizontalSliderWithBrowser
from .CoordinateSystemOverlay import CoordinateSystemOverlay
from ._ProcessingOverlay import ProcessingOverlay
from ._SliceLoader import SliceLoader

_logger = logging.getLogger(__name__)


class TomoPlot2DSlices(qt.QWidget):
    """
    A composition of a TomoPlot2D, a QLabel (with a colored frame) and a set of radio buttons for the user to select the index to be displayed

    :param title: plot title.
    :param color: color associated to the plot.
    :param image: image to associate for the overlay coordinate system.
    :param axis: Axis associated to the plot (determine how to read from the raw volume).
    """

    displayFullScreen = qt.Signal()

    def __init__(self, title: str, color: str, image: str, axis: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if axis not in (0, 1, 2):
            raise ValueError(f"'axis' should be in (0, 1, 2). Got {type(axis)}")
        self._axis = axis
        self.__sliceLoader: SliceLoader | None = None
        # thread used to load a slice when not part of the 'slices' and when the volume data is not in memory.
        # avoid any deadlock or GUI lag.

        self.setLayout(qt.QVBoxLayout())
        self.layout().setContentsMargins(2, 2, 2, 2)
        self.layout().setSpacing(2)

        self._slices: dict[SliceTuple, numpy.ndarray] = {}
        # sub set of slice easily accessible
        self._volume: TomwerVolumeBase | None = None
        # optional volume from which we can read slices.
        # The volume is expected to be loaded or reading is expected to be done on the 'fast' axis.

        self._plot = _TomoPlot2D(parent=self)
        self._plot.getColorBarWidget().hide()
        self._plot.getOutputToolBar().hide()
        self._plot.getColormapAction().setVisible(False)
        self._plot.getColorBarAction().setVisible(False)
        self._plot.getMaskAction().setVisible(False)
        self._plot.getInteractiveModeToolBar().hide()
        self.layout().addWidget(self._plot)

        self._coordinateSystemOverlay = CoordinateSystemOverlay(
            parent=self._plot.getWidgetHandle(),
            img=image,
            img_size=qt.QSize(50, 50),
        )
        self._coordinateSystemOverlay.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignBottom)
        self._coordinateSystemOverlay.setAlignmentOffsets((-10, -10))

        self._title = qt.QLabel(title, parent=self)
        self._title.setAlignment(qt.Qt.AlignCenter)
        self.layout().addWidget(self._title)

        self._sliceIndexSelection = HorizontalSliderWithBrowser()
        self.layout().addWidget(self._sliceIndexSelection)

        # set the color to the title frame (simplest)
        self._title.setStyleSheet(
            f"border: 2px solid {color}",
        )

        # overlay to signal some loading is on-going.
        self._messageOverlayWidget = WaitingOverlay(self._plot)
        self._messageOverlayWidget.setStyleSheet(
            "QPushButton { background-color: rgba(150, 150, 150, 40); border: 0px; border-radius: 10px; }"
        )
        self._messageOverlayWidget.setIconSize(qt.QSize(30, 30))

        # Overlay to notify during fast axis reading
        self._fastReadingIndicator = ProcessingOverlay(
            self._plot, img_size=qt.QSize(5, 6)
        )
        self._fastReadingIndicator.setAlignmentOffsets((-10, 10))
        self._fastReadingIndicator.setVisible(False)

        # create the new toolbar
        # full screen action
        self._extraToolbar = qt.QToolBar(self)
        self._plot.addToolBar(self._extraToolbar)
        fullScreenIcon = tomwer_icons.getQIcon("full_screen")
        self._fullScreenAction = qt.QAction(fullScreenIcon, "pop up full screen")
        self._extraToolbar.addAction(self._fullScreenAction)

        self._toolbars = (
            self._plot.toolBar(),
            self._plot.getProfileToolbar(),
            self._extraToolbar,
        )

        # set up
        self.setCoordinateSystemLabelVisible(False)
        self.setToolBarsVisible(False)
        self.setLoading(False)

        # connect signal / slot
        self._fullScreenAction.triggered.connect(self.displayFullScreen)
        self._sliceIndexSelection.valueChanged.connect(self._updatePlot)

    def _indicateFastReading(self, value: bool):
        """
        At the moment the fast-reading axis can become load in the case of hdf5. At the moment we simply notify it to the user.
        """
        self._fastReadingIndicator.setVisible(value)

    def setLoadingMessage(self, message: str):
        self._messageOverlayWidget.setText(message)

    def setLoading(self, loading: bool) -> None:
        self._messageOverlayWidget.setVisible(loading)

    def isLoading(self) -> bool:
        return self._messageOverlayWidget.isVisible()

    def setCoordinateSystemVisible(self, visible):
        self._coordinateSystemOverlay.setVisible(visible)

    def setCoordinateSystemLabelVisible(self, visible: bool):
        self._title.setVisible(visible)

    def setSliceSelectionVisible(self, visible: bool):
        self._sliceIndexSelection.setVisible(visible)

    def setToolBarsVisible(self, visible: bool):
        for toolbar in self._toolbars:
            toolbar.setVisible(visible)

    def getTitle(self) -> str:
        return self._title

    def clearActiveImage(self) -> None:
        """
        Remove the active image from the plot.

        .. note:: Other items (e.g., markers) may still be present in the widget.
        """
        img = self._plot.getImage()
        if img is not None:
            self._plot.remove(img)

    def setVolume(self, volume: TomwerVolumeBase | None):
        """
        Set the volume. So user can browse through it in addition to the slices.
        """
        if not isinstance(volume, (TomwerVolumeBase, type(None))):
            raise TypeError(
                f"'volume' is expected to be instance of {TomwerVolumeBase} or {None}. Got {type(volume)}."
            )
        self._volume = volume
        if volume is not None:
            # avoid updating the range (and the slice index) when possible
            range = 0, self._volume.get_volume_shape()[self._axis] - 1
            if range != self._sliceIndexSelection.getRange():
                self._sliceIndexSelection.setRange(*range)
        self._sliceIndexSelection.setSliceBrowsingEnabled(self._volume is not None)

    @staticmethod
    def _determinePreferredSliceIndex(slice_indices: tuple[int]) -> int:
        """Return the index to display if None provided during construction"""
        if len(slice_indices) == 0:
            return -1
        return slice_indices[len(slice_indices) // 2]

    def setSlices(
        self, slices: dict[SliceTuple, numpy.ndarray], update_index: bool = True
    ):
        self._slices = {
            slice_tuple.index: value for slice_tuple, value in slices.items()
        }
        # update to the new one
        slice_indices = tuple(self._slices.keys())
        self._sliceIndexSelection.setSliceIndices(slices=slice_indices)
        if update_index:
            self._sliceIndexSelection.setValue(
                self._determinePreferredSliceIndex(slice_indices=slice_indices)
            )

        self._updatePlot(slice_index=self._sliceIndexSelection.value())

    def setSliceRange(self, first, last):
        self._sliceIndexSelection.setRange(first, last)

    def getSliceRange(self):
        return self._sliceIndexSelection.getRange()

    def _updatePlot(self, slice_index: int | None):
        if slice_index is None:
            self._plot.clear()
            return

        image = self._slices.get(slice_index, None)
        loading_delegated = False
        if image is None and self._volume is not None:
            if self._volume.data is None:
                loading_delegated = self.__delegateSliceLoading(slice_index=slice_index)
            else:
                image = self._volume.get_slice(
                    index=slice_index,
                    axis=self._axis,
                )

        if loading_delegated:
            return

        if image is None:
            _logger.error(f"Fail to load slice index {slice_index}")
            return

        self._plot.addImage(image, resetzoom=False)

    def __delegateSliceLoading(self, slice_index: int) -> bool:
        """Delegate slice loading to a dedicated thread"""
        if self.__sliceLoader is not None:
            self.__sliceLoader.finished.disconnect(self.__delegatedSliceLoadingFinished)
            # TODO: fix me: avoid some segfault having several thread reading and being destroyed without owner.
            # wait for the previous loading to be done.
            # This avoid having several thread and ensure a 'clean' loading of the data.
            # Remember that we are on the 'fast' reading axis.
            # self.__sliceLoader.wait()
        self._indicateFastReading(True)
        self.__sliceLoader = SliceLoader(
            parent=self,
            volume=self._volume,
            slice_index=slice_index,
            axis=self._axis,
        )
        self.__sliceLoader.finished.connect(self.__delegatedSliceLoadingFinished)
        self.__sliceLoader.start()
        return True

    def __delegatedSliceLoadingFinished(self):
        if self.sender() != self.__sliceLoader:
            # slice to be loaded has been changed
            return

        self._indicateFastReading(False)
        self.__sliceLoader.finished.disconnect(self.__delegatedSliceLoadingFinished)
        data = self.__sliceLoader.data
        slice_index = self.__sliceLoader.slice_index

        if data is not None:
            if slice_index == self.getCurrentSliceIndex():
                concurrent.submitToQtMainThread(
                    self._plot.addImage,
                    data,
                    resetzoom=False,
                )
            else:
                # can happen if not being responsive enough (volume being load, user browsing the fast axis and the loading of slices along the fast axis not being so fast...)
                pass
        else:
            _logger.warning(f"Failed to load slice {self.__sliceLoader.slice_index}")
        self.__sliceLoader = None

    def getPlot(self):
        return self._plot

    # expose API
    def clear(self):
        self._plot.clear()

    def setVoxelSize(self, size_m: float | None):
        self._plot.setVoxelSize(size=size_m)

    def setCurrentIndex(self, index: int):
        self._sliceIndexSelection.setValue(index)

    def getCurrentSliceIndex(self) -> int:
        return self._sliceIndexSelection.value()
