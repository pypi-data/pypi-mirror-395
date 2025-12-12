from __future__ import annotations

from silx.gui import qt
from tomwer.gui import icons

try:
    from silx.gui.widgets.OverlayMixIn import OverlayMixIn as _OverlayMixIn
except ImportError:
    from tomwer.third_part.OverlayMixIn import OverlayMixIn as _OverlayMixIn


class CoordinateSystemOverlay(_OverlayMixIn, qt.QLabel):
    "Widget to be display an image on one of the four widget corner"

    def __init__(self, parent, img, img_size, *args, **kwargs):
        qt.QLabel.__init__(self, parent=parent)
        _OverlayMixIn.__init__(self, parent=parent, *args, **kwargs)
        self._imageQIcon = icons.getQIcon(img)

        self.setPixmap(self._imageQIcon.pixmap(img_size))
