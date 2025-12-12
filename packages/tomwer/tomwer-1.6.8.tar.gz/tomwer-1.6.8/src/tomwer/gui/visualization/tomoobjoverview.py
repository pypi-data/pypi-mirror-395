from __future__ import annotations

from silx.gui import qt

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.volume.volumebase import TomwerVolumeBase

from .scanoverview import ScanOverviewWidget
from .volumeoverview import VolumeOverviewWidget


class TomoObjOverview(qt.QWidget):
    """
    Dummy widget to show ScanOverviewWidget if the object is a scan or VolumeOverviewWidget if the object is a Volume
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self._scanOverview = ScanOverviewWidget(self)
        self.layout().addWidget(self._scanOverview)

        self._volumeOverview = VolumeOverviewWidget(self)
        self.layout().addWidget(self._volumeOverview)

        self._scanOverview.setVisible(False)
        self._volumeOverview.setVisible(False)

    def setTomoObj(self, tomo_obj: TomwerObject | None):
        """
        update sub widgets according to the type of tomo_obj
        """
        if tomo_obj is not None and not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"tomo_obj is expected to be an instance of {TomwerObject} and not {type(tomo_obj)}"
            )
        # handle visibility
        self._volumeOverview.setVisible(isinstance(tomo_obj, TomwerVolumeBase))
        self._scanOverview.setVisible(isinstance(tomo_obj, TomwerScanBase))

        if isinstance(tomo_obj, TomwerVolumeBase):
            self._scanOverview.setScan(None)
            self._volumeOverview.setVolume(tomo_obj)
        elif isinstance(tomo_obj, TomwerScanBase):
            self._scanOverview.setScan(tomo_obj)
            self._volumeOverview.setVolume(None)
        elif tomo_obj is None:
            self._volumeOverview.setVolume(None)
            self._scanOverview.setScan(None)
        else:
            raise RuntimeError(f"TomwerObject of type {type(tomo_obj)} is not handled")
