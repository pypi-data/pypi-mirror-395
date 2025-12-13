from __future__ import annotations

import h5py
from silx.gui import qt
from silx.io.utils import open as open_hdf5

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui import icons


class NXtomoProxyWarmer(qt.QWidget):
    """
    Widget to warm in the case the NXtomo entry is a SoftLink or an ExternalLink (so editing it will modify another file).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(qt.QHBoxLayout())
        # icon
        # warning about requires parameters from a nabu slice reconstruction
        self._warningIcon = qt.QLabel(
            "It seems this entry points to a soft link. Be carreful. Editing metadata will affect another file",
            parent=self,
        )
        self._warningIcon.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self._warningIcon.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        warning_icon = icons.getQIcon("warning")
        self._warningIcon.setPixmap(warning_icon.pixmap(20, 20))
        self.layout().addWidget(self._warningIcon)
        # label
        self._warningLabel = qt.QLabel(
            "It seems the NXtomo you are editing is pointing to another dataset.",
            parent=self,
        )
        self._warningLabel.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self._warningLabel.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        font = self._warningLabel.font()
        font.setBold(True)
        font.setPixelSize(10)
        self._warningLabel.setFont(font)
        self.layout().addWidget(self._warningLabel)
        # set up
        self.setScan(None)

    def setScan(self, scan: NXtomoScan | None):
        if scan is None:
            self._activateWarning(False)
        elif isinstance(scan, NXtomoScan):
            with open_hdf5(scan.master_file) as h5f:
                entry = h5f.get(
                    name=scan.entry, getclass=True, getlink=True, default=None
                )
                self._activateWarning(entry in (h5py.ExternalLink, h5py.SoftLink))
        else:
            raise TypeError(f"{scan} is expected to be an instance of {NXtomoScan}")

    def _activateWarning(self, activate: bool):
        self._warningIcon.setVisible(activate)
        self._warningLabel.setVisible(activate)
