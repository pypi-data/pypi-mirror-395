from __future__ import annotations

from silx.gui import qt
from tomoscan.identifier import VolumeIdentifier
from tomwer.gui.visualization.reconstructionparameters import (
    ReconstructionParameters as _ReconstructionParameters,
)


class ReconstructionParameters(_ReconstructionParameters):
    """
    Add the scan identifier to the list of metadata displayed.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._volumeIdentifierQLE = qt.QLineEdit("", self)
        self._volumeIdentifierQLE.setReadOnly(True)

        self.layout().insertRow(0, "volume id", self._volumeIdentifierQLE)

    def setVolumeIdentifier(self, volume_identifier: VolumeIdentifier):
        # TODO: connect the volume to the scan and display scan information as well
        # see https://gitlab.esrf.fr/tomotools/tomwer/-/issues/1479
        self._volumeIdentifierQLE.setText(volume_identifier.to_str())
        self._volumeIdentifierQLE.setToolTip(volume_identifier.to_str())
