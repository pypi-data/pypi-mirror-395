from __future__ import annotations

from silx.gui import qt
from tomwer.gui import icons

try:
    from silx.gui.widgets.OverlayMixIn import OverlayMixIn as _OverlayMixIn
except ImportError:
    from tomwer.third_part.OverlayMixIn import OverlayMixIn as _OverlayMixIn


class ProcessingOverlay(_OverlayMixIn, qt.QLabel):
    """
    Small widget overlay that will display a red dot when some processing are on-going.

    Use case: when loading a frame on the fast axis we cannot clear the plot and add a message else it will
    do some blinking.
    But in some cases loading can take some time (when loading already a full volume in hdf5 for example).
    And we need to notify the user that something is on-going.
    """

    def __init__(self, parent, img_size, *args, **kwargs):
        qt.QLabel.__init__(self, parent=parent)
        _OverlayMixIn.__init__(self, parent=parent, *args, **kwargs)
        self.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignTop)
        self._imageQIcon = icons.getQIcon("red_dot")

        self.setPixmap(self._imageQIcon.pixmap(img_size))
