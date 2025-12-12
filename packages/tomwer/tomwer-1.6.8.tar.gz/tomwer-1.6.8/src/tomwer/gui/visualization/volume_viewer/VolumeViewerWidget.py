from __future__ import annotations

import logging
import numpy
import pint
from functools import partial
from silx.gui.plot.items.axis import Axis
from silx.gui import qt

from tomoscan.volumebase import SliceTuple
from tomoscan.identifier import VolumeIdentifier

from tomoscan.esrf.volume.singleframebase import VolumeSingleFrameBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume import HDF5Volume
from tomwer.gui.visualization.fullscreenplot import FullScreenPlot2D
from tomwer.gui.visualization.TomoPlot2D import TomoPlot2D as _TomoPlot2D

from .GeometryOrMetadataWidget import GeometryOrMetadataWidget
from ._TomoPlot2DSlices import TomoPlot2DSlices
from ._CrossHairs import CrossHairs


_logger = logging.getLogger(__name__)
_ureg = pint.get_application_registry()


class VolumeViewerWidget(qt.QWidget):
    """
    A window displaying slices side by side along the three direction with a 'geometric reference'.
    """

    _HANDLE_WIDTH = 10  # px

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setLayout(qt.QVBoxLayout())
        self._verticalSplitter = qt.QSplitter(qt.Qt.Vertical)
        self._verticalSplitter.setHandleWidth(self._HANDLE_WIDTH)
        self.layout().addWidget(self._verticalSplitter)

        # horizontal top splitter
        self._horizontalTopSplitter = qt.QSplitter(qt.Qt.Horizontal)
        self._horizontalTopSplitter.setHandleWidth(self._HANDLE_WIDTH)
        self._XYPlot2D = TomoPlot2DSlices(
            parent=self,
            title="XY",
            color="red",
            image="3D_coordinate_system_XY",
            axis=0,
        )
        self._horizontalTopSplitter.addWidget(self._XYPlot2D)

        self._YZPlot2D = TomoPlot2DSlices(
            parent=self,
            title="YZ",
            color="blue",
            image="3D_coordinate_system_YZ",
            axis=2,
        )
        self._horizontalTopSplitter.addWidget(self._YZPlot2D)
        self._verticalSplitter.addWidget(self._horizontalTopSplitter)

        # vertical bottom splitter
        self._horizontalBottomSplitter = qt.QSplitter(qt.Qt.Horizontal)
        self._horizontalBottomSplitter.setHandleWidth(self._HANDLE_WIDTH)
        self._geometryOrMetadataWidget = GeometryOrMetadataWidget(parent=self)
        self._horizontalBottomSplitter.addWidget(self._geometryOrMetadataWidget)
        self._XZPlot2D = TomoPlot2DSlices(
            parent=self,
            title="XZ",
            color="green",
            image="3D_coordinate_system_XZ",
            axis=1,
        )
        self._horizontalBottomSplitter.addWidget(self._XZPlot2D)
        self._verticalSplitter.addWidget(self._horizontalBottomSplitter)

        # define size policy
        self._YZPlot2D.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self._XZPlot2D.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self._XYPlot2D.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self._geometryOrMetadataWidget.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding
        )

        self._crossHairs = CrossHairs(
            XYPlot=self._XYPlot2D,
            XZPlot=self._XZPlot2D,
            YZPlot=self._YZPlot2D,
        )

        # connect signal / slot
        for plot in (
            self._YZPlot2D,
            self._XZPlot2D,
            self._XYPlot2D,
        ):
            plot.displayFullScreen.connect(
                partial(
                    self._popUpImageFullScreen,
                    plot,
                )
            )
            plot._sliceIndexSelection.valueChanged.connect(self._updateCrossHairs)

    def initVolumePreview(self, volume: TomwerVolumeBase, message: str | None):
        """
        Set display for a new volume before the full volume or slices are loaded.

        For HDF5 and VolumeSingleFrame it will allow users to browse the dataset before the full volume or slices subset are loaded.
        Else we notify the user that some loading is on-going.
        """
        self._geometryOrMetadataWidget.setVolumeIdentifier(volume.get_identifier())
        if isinstance(volume, (HDF5Volume, VolumeSingleFrameBase)):
            # Z is the fast read axis for most file format. So we allow users to access it directly.
            _logger.info(f"Set {volume.get_identifier()} for preview.")
            self._XYPlot2D.setVolume(volume)

            vol_shape = volume.get_volume_shape()
            if vol_shape:
                self.setVolumeShape(shape=vol_shape)
                self._XYPlot2D.setCurrentIndex(vol_shape[0] // 2)
        elif isinstance(volume, TomwerVolumeBase):
            _logger.debug(f"No preview available for {volume.get_identifier()}.")
            self._XYPlot2D.setLoadingMessage(message)
            self._XYPlot2D.setLoading(True)
        else:
            raise TypeError(f"type not handled: {type(volume)}")
        for plot in (self._XZPlot2D, self._YZPlot2D):
            plot.setLoadingMessage(message)
            plot.clearActiveImage()
            plot.setLoading(True)

    def setVolume(self, volume: TomwerVolumeBase):
        """
        Defines the volume. Expects to be loaded in memory to avoid freezing the GUI when browsing slices.
        """
        self._XYPlot2D.setVolume(volume)
        self._XZPlot2D.setVolume(volume)
        self._YZPlot2D.setVolume(volume)

    def stopPreview(self):
        for plot in self._window.getPlots():
            plot.setLoading(False)

    def getPlots(self) -> dict[str, _TomoPlot2D]:
        return {
            "XY": self._XYPlot2D.getPlot(),
            "YZ": self._YZPlot2D.getPlot(),
            "XZ": self._XZPlot2D.getPlot(),
        }

    def extendPlot(self, plot_name: str | None):
        """
        Extend the requested plot to take most of the space in the widget.
        If None 'reset' the view to equally space the plots and metadata

        :param plot_name: None for reset else should be in ('XY', 'XZ', 'YZ')
        """
        # warning: the bottom slides are using 3 values because we expect to have the
        # ColorbarWidget defined by the VolumeReconstructionSummaryWindow
        # reset splitters
        if plot_name is None:
            self._horizontalTopSplitter.setSizes([1, 1])
            self._horizontalBottomSplitter.setSizes([2, 4, 6])
            self._verticalSplitter.setSizes([1, 1])
        elif plot_name == "XY":
            self._verticalSplitter.setSizes([1, 0])
            self._horizontalTopSplitter.setSizes([1, 0])
        elif plot_name == "YZ":
            self._verticalSplitter.setSizes([1, 0])
            self._horizontalTopSplitter.setSizes([0, 1])
        elif plot_name == "XZ":
            self._verticalSplitter.setSizes([0, 1])
            self._horizontalBottomSplitter.setSizes([0, 0, 1])
        else:
            raise ValueError(f"{plot_name!r} not handle.")

    def clear(self) -> None:
        self._YZPlot2D.clear()
        self._XZPlot2D.clear()
        self._XYPlot2D.clear()
        self._geometryOrMetadataWidget.clear()

    def setLoading(self, loading: bool):
        self._YZPlot2D.setLoading(loading)
        self._XZPlot2D.setLoading(loading)
        self._XYPlot2D.setLoading(loading)

    def setSlices(self, slices: dict[SliceTuple, numpy.ndarray]):
        for axis, plot in {
            0: self._XYPlot2D,
            1: self._YZPlot2D,
            2: self._XZPlot2D,
        }.items():
            plot.setSlices(
                dict(
                    filter(
                        lambda item: item[0].axis == axis,
                        slices.items(),
                    )
                )
            )

    def setVolumeShape(self, shape: tuple[int]) -> None:
        self._XYPlot2D.setSliceRange(0, shape[0] - 1)
        self._XZPlot2D.setSliceRange(0, shape[1] - 1)
        self._YZPlot2D.setSliceRange(0, shape[2] - 1)

    def getVolumeShape(self) -> tuple[int]:
        return (
            self._XYPlot2D.getSliceRange()[1] + 1,
            self._XZPlot2D.getSliceRange()[1] + 1,
            self._YZPlot2D.getSliceRange()[1] + 1,
        )

    def setVolumeMetadata(self, metadata: dict, volume_shape: tuple[int]):
        """
        Warning: as the call might change the scale it must be called once the data is set.
        """
        self._geometryOrMetadataWidget.setMetadata(metadata=metadata)
        self._updatePlotAxes(metadata=metadata, volume_shape=volume_shape)

    def _updatePlotAxes(self, metadata: dict, volume_shape: tuple[int]):
        """
        Define axes limits and labels according to the volume metadata (when possible)
        """
        reconstruction_metadata = metadata.get("processing_options", {}).get(
            "reconstruction", {}
        )
        position_m = reconstruction_metadata.get("position", None)
        voxel_size_cm = reconstruction_metadata.get("voxel_size_cm", None)

        labels = ("Z", "Y", "X")
        if position_m is not None and voxel_size_cm is not None:
            voxel_size = numpy.array(voxel_size_cm) * _ureg.centimeter
        else:
            _logger.info("Missing metadata from volume. Cannot set axis values")
            voxel_size = [None] * 3
        # Note: pixel size must be a scalar. So we arbitrarly choice one of the two values. Voxel are expected to be squares
        self._XYPlot2D.setVoxelSize(voxel_size[2])
        self._XZPlot2D.setVoxelSize(voxel_size[2])
        self._YZPlot2D.setVoxelSize(voxel_size[1])

        map_silx_axis_to_index_axis: {Axis, int} = {
            self._XYPlot2D.getPlot().getXAxis(): 1,
            self._XYPlot2D.getPlot().getYAxis(): 2,
            self._YZPlot2D.getPlot().getXAxis(): 1,
            self._YZPlot2D.getPlot().getYAxis(): 0,
            self._XZPlot2D.getPlot().getXAxis(): 2,
            self._XZPlot2D.getPlot().getYAxis(): 0,
        }
        for silx_axis, axis_index in map_silx_axis_to_index_axis.items():
            silx_axis.setLabel(labels[axis_index])

    def _popUpImageFullScreen(self, plot: TomoPlot2DSlices):
        new_plot = FullScreenPlot2D()
        active_image = plot.getPlot().getActiveImage()
        if active_image is None or active_image.getData(copy=False) is None:
            return

        window_title = f"Plot of {plot.getTitle()}"

        new_plot.setWindowTitle(window_title)

        # add the current image
        new_plot.addImage(
            active_image.getData(copy=False), colormap=active_image.getColormap()
        )

        new_plot.showFullScreen()

    def getMasterPlot(self) -> _TomoPlot2D:
        """
        To apply the same colormap to the three plot we need to have a master / driver one.
        It has been decided arbitrarily to use the
        """
        return self._YZPlot2D.getPlot()

    def getCrossHairs(self) -> CrossHairs:
        return self._crossHairs

    def resetZooms(self):
        for plot in self.getPlots().values():
            plot.resetZoom()

    def setVolumeIdentifier(self, volume_identifier: VolumeIdentifier):
        self._geometryOrMetadataWidget.setVolumeIdentifier(volume_identifier)

    def _updateCrossHairs(self, *args, **kwargs):
        self._crossHairs.updateMarkers(
            XYIndex=self._XYPlot2D.getCurrentSliceIndex(),
            XZIndex=self._XZPlot2D.getCurrentSliceIndex(),
            YZIndex=self._YZPlot2D.getCurrentSliceIndex(),
        )
