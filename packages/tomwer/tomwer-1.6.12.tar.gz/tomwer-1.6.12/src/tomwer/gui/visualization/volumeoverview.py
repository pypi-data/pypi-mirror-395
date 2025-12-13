from __future__ import annotations

import logging

from silx.gui import qt
from tomoscan.identifier import VolumeIdentifier

from tomwer.core.volume.volumebase import TomwerVolumeBase

_logger = logging.getLogger(__name__)


class VolumeOverviewWidget(qt.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._volumeIdentifier = None
        self.setLayout(qt.QVBoxLayout())
        self._tree = qt.QTreeWidget(self)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("metadata", "value"))
        self.layout().addWidget(self._tree)

        # 1: define translations
        self._x_position = qt.QTreeWidgetItem(self._tree)
        self._x_position.setText(0, "x position")
        self._y_position = qt.QTreeWidgetItem(self._tree)
        self._y_position.setText(0, "y position")
        self._z_position = qt.QTreeWidgetItem(self._tree)
        self._z_position.setText(0, "z position")

        # 2. define pixel size
        self._x_pixel_size = qt.QTreeWidgetItem(self._tree)
        self._x_pixel_size.setText(0, "x pixel size")
        self._y_pixel_size = qt.QTreeWidgetItem(self._tree)
        self._y_pixel_size.setText(0, "y pixel size")

    def setVolume(self, volume: TomwerVolumeBase | None):
        if volume is None:
            self._x_position.setText(1, "")
            self._y_position.setText(1, "")
            self._z_position.setText(1, "")
            self._x_pixel_size.setText(1, "")
            self._y_pixel_size.setText(1, "")
        elif not isinstance(volume, TomwerVolumeBase):
            raise TypeError(
                f"volume is expected to be a {TomwerVolumeBase} or a {VolumeIdentifier}. Not ({type(volume)}) "
            )
        else:
            try:
                x_pos, y_pos, z_pos = volume.position()
            except Exception:
                self._x_position.setText(1, "?")
                self._y_position.setText(1, "?")
                self._z_position.setText(1, "?")
            else:
                self._x_position.setText(1, x_pos)
                self._y_position.setText(1, y_pos)
                self._z_position.setText(1, z_pos)

            try:
                x_size, y_size = volume.pixel_size
            except Exception:
                self._x_pixel_size.setText(1, "?")
                self._y_pixel_size.setText(1, "?")
            else:
                self._x_pixel_size.setText(1, x_size)
                self._y_pixel_size.setText(1, y_size)
