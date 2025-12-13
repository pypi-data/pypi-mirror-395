from __future__ import annotations

import logging
from bisect import bisect_left

from silx.gui import qt
from silx.io.url import DataUrl

from tomwer.core.scan.scanbase import TomwerScanBase

_logger = logging.getLogger(__name__)


class ManualFramesSelection(qt.QWidget):
    """Allows to select frame - angle to be used."""

    sigChanged = qt.Signal()
    """Signal emit when the frame selection changes"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._anglesAvailable = []
        # cache of the angles available from the current defined frames. Must be sorted !!!
        self.setLayout(qt.QGridLayout())
        self.layout().addWidget(qt.QLabel("frame 1", self), 0, 0, 1, 1)
        self._frame1CB = qt.QComboBox(self)
        self._frame1CB.setEditable(True)
        self.layout().addWidget(self._frame1CB, 0, 1, 1, 1)

        self.layout().addWidget(qt.QLabel("frame 2", self), 1, 0, 1, 1)
        self._frame2CB = qt.QComboBox(self)
        self._frame2CB.setEditable(True)
        self.layout().addWidget(self._frame2CB, 1, 1, 1, 1)
        self._findAssociatedAnglePB = qt.QPushButton("+180°", self)
        button_180_font = self.font()
        button_180_font.setPixelSize(10)
        self._findAssociatedAnglePB.setFont(button_180_font)
        self._findAssociatedAnglePB.setFixedWidth(30)
        self._findAssociatedAnglePB.setSizePolicy(
            qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum
        )
        self.layout().addWidget(self._findAssociatedAnglePB, 1, 2, 1, 1)
        self._flipLRCB = qt.QCheckBox("flip L-R")
        self._flipLRCB.setChecked(True)
        self.layout().addWidget(self._flipLRCB, 1, 3, 1, 1)

        self._flipLRCB.toggled.connect(self._changed)
        self._frame1CB.currentIndexChanged.connect(self._changed)
        self._frame2CB.currentIndexChanged.connect(self._changed)
        self._findAssociatedAnglePB.released.connect(self._findAssociatedAngle)

    def _findAssociatedAngle(self):
        if self._frame1CB.count() == 0 or len(self._anglesAvailable) == 0:
            _logger.warning("no angles available, unable to get '+180°' frame")
        else:
            angle = float(self._frame1CB.currentText())
            # look for the closest 'associated' angle.
            # as the angles are not limited to [0-360] we need to check for any value.
            # if the angle is on the first part of the acquisition we expect to find it near angle +180
            # if it is on the second part (for 360 degree) we expect to find it on the first part (0-180)
            closest_pls_180_angle = self._getClosestAssociatedAngle(
                angle + 180.0, self._anglesAvailable
            )
            score_add = abs(closest_pls_180_angle - angle)
            closest_minus_180_angle = self._getClosestAssociatedAngle(
                angle - 180.0, self._anglesAvailable
            )
            score_sub = abs(closest_minus_180_angle - angle)
            if score_add >= score_sub:
                closest_180_angle = closest_pls_180_angle
            else:
                closest_180_angle = closest_minus_180_angle
            item_idx = self._frame2CB.findText(self._angleToStr(closest_180_angle))
            if item_idx < 0:
                _logger.error(f"Unable to find item for angle {closest_180_angle}")
            else:
                self._frame2CB.setCurrentIndex(item_idx)

    @staticmethod
    def _getClosestAssociatedAngle(angle: float, angles: tuple) -> float:
        """
        return the angle closest angle to 'angle' from 'angles'

        :warning: angles should be already sorted !!!
        """
        if angles is None or len(angles) == 0:
            return None
        if angle in angles:
            return angle
        pos = bisect_left(angles, angle)
        if pos == 0:
            return angles[0]
        elif pos > len(angles) - 1:
            return angles[-1]
        else:
            left_angle = angles[pos - 1]
            right_angle = angles[pos]
            if abs(right_angle - angle) > abs(left_angle - angle):
                return left_angle
            else:
                return right_angle

    def _changed(self):
        self.sigChanged.emit()

    @staticmethod
    def _angleToStr(angle: float) -> str:
        return f"{float(angle):0.3f}"

    def setScan(self, scan: TomwerScanBase | None) -> None:
        self._anglesAvailable.clear()
        self._frame1CB.clear()
        self._frame2CB.clear()
        if scan is None:
            return
        current_angle1 = self._getFrame1Angle()
        current_angle2 = self._getFrame2Angle()
        for proj_angle, proj_url in scan.get_proj_angle_url().items():
            try:
                angle = self._angleToStr(proj_angle)
            except Exception:
                angle = proj_angle
            else:
                self._anglesAvailable.append(float(proj_angle))
            self._frame1CB.addItem(angle, proj_url)
            self._frame2CB.addItem(angle, proj_url)

        self._anglesAvailable.sort()

        idx = self._frame1CB.findText(current_angle1)
        if idx >= 0:
            self._frame1CB.setCurrentIndex(idx)
        if current_angle1 == current_angle2:
            # if the two current angle are close then we consider it is better to look for angleX - angleX + 180 angles
            # instead of finding back angles
            self._findAssociatedAngle()
        else:
            idx = self._frame1CB.findText(current_angle1)
            if idx >= 0:
                self._frame1CB.setCurrentIndex(idx)

            idx = self._frame2CB.findText(current_angle2)
            if idx >= 0:
                self._frame2CB.setCurrentIndex(idx)

    def getFramesUrl(self, as_txt=False) -> tuple:
        """
        Return a tuple of (frame 1 url, frame 2 url). Url can be None
        """
        if as_txt:
            return self.getFrame1Url().path(), self.getFrame2Url().path()
        else:
            return self.getFrame1Url(), self.getFrame2Url()

    def getFrame1Url(self) -> DataUrl | None:
        return self._frame1CB.currentData()

    def getFrame2Url(self) -> DataUrl | None:
        return self._frame2CB.currentData()

    def _getFrame1Angle(self) -> str | None:
        return self._frame1CB.currentText()

    def _getFrame2Angle(self) -> str | None:
        return self._frame2CB.currentText()

    def isFrame2LRFLip(self):
        return self._flipLRCB.isChecked()
