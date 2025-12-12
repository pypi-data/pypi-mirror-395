import pytest
from orangewidget import gui, widget
from orangewidget.widget import Input

from silx.gui import qt

import tomwer.core.process.visualization.volumeviewer
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from ._volume_viewer import VolumeViewer


@pytest.mark.skip("Fail on CI")
class VolumeViewerOW(widget.OWBaseWidget, openclass=True):
    """a viewer to display the last volume reconstructed using silx plot3d
    viewer.

    :param parent: the parent widget
    """

    name = "volume viewer"
    id = "orange.widgets.tomwer.deprecated.VolumeViewerOW.VolumeViewerOW"
    description = "display the last volume reconstructed"
    icon = "icons/deprecated_volume_viewer.svg"
    priority = 80
    keywords = ["tomography", "file", "tomwer", "acquisition", "validation"]

    ewokstaskclass = (
        tomwer.core.process.visualization.volumeviewer._VolumeViewerPlaceHolder
    )

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    class Inputs:
        data = Input(name="data", type=TomwerScanBase)
        volume = Input(name="volume", type=TomwerVolumeBase, multiple=True)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self.viewer = VolumeViewer(parent=self)
        self._layout.addWidget(self.viewer)

    @Inputs.data
    def addScan(self, scan, *args, **kwargs):
        if scan is None:
            return
        self.viewer.setScan(scan)

    @Inputs.volume
    def _volumeReceived(self, volume, *args, **kwargs):
        self.addVolume(volume)

    def addVolume(self, volume):
        if volume is None:
            return
        self.viewer.setVolume(volume)

    def sizeHint(self):
        return qt.QSize(400, 500)
