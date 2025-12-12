from silx.gui import qt

from tomwer.core.process.stitching.metadataholder import (
    StitchingMetadata as _StitchingMetadata,
)


class QStitchingMetadata(qt.QObject, _StitchingMetadata):
    """
    overload of a TomoObject to register metadata set by the user on positions
    """

    sigChanged = qt.Signal()
    """
    emit when some parameter changed
    """

    def __init__(self, parent=None, tomo_obj=None) -> None:
        super().__init__(parent)
        _StitchingMetadata.__init__(self=self, tomo_obj=tomo_obj)

    def setPixelOrVoxelSize(self, value, axis):
        super().setPixelOrVoxelSize(value=value, axis=axis)
        self.sigChanged.emit()

    def setPxPos(self, value, axis):
        super().setPxPos(value=value, axis=axis)
        self.sigChanged.emit()

    def setMetricPos(self, value, axis):
        super().setMetricPos(value=value, axis=axis)
        self.sigChanged.emit()
