from __future__ import annotations

from silx.gui import qt

from ._ReconstructionParameters import ReconstructionParameters
from tomwer.gui.utils.illustrations import _IllustrationWidget


class GeometryOrMetadataWidget(qt.QTabWidget):
    """Simple widget that display either esrf geometric reference or volume metadata"""

    def __init__(self, parent=...):
        super().__init__(parent)

        # reconstruction parameters
        self._metadataWidget = ReconstructionParameters()
        self._metadataScrollArea = qt.QScrollArea(self)
        self._metadataScrollArea.setWidgetResizable(True)
        self._metadataScrollArea.setWidget(self._metadataWidget)

        self.addTab(self._metadataScrollArea, "volume metadata")

        # coordinate system illustration
        self._geometricRefLabel = _IllustrationWidget(self, img="3D_coordinate_system")
        self.addTab(self._geometricRefLabel, "geometry")

    # expos API
    def setVolumeIdentifier(self, *args, **kwargs):
        self._metadataWidget.setVolumeIdentifier(*args, **kwargs)

    def setMetadata(self, metadata: dict):
        self._metadataWidget.setVolumeMetadata(metadata=metadata)

    def sizeHint(self) -> qt.QSize:
        # size hint to match the plot2D one and have equal initial size
        return qt.QSize(500, 534)
