from orangewidget import gui, widget
from orangewidget.widget import Input, Output
from silx.gui import qt

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.visualization.nxtomometadata import NXtomoMetadataViewer


class NXtomoMetadataViewerOW(widget.OWBaseWidget, openclass=True):
    """
    Widget to siplay NXtomo metadata
    """

    name = "nxtomo-metadata-viewer"
    id = "orange.widgets.tomwer.visualization.NXtomoMetadataViewerOW.NXtomoMetadataViewerOW"
    description = "Interface to display some metadata of a NXtomo"
    icon = "icons/nx_tomo_metadata_viewer.svg"
    priority = 13
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "visualize",
        "visualization",
        "display",
        "NXTomo",
        "editor",
        "energy",
        "distance",
        "pixel size",
    ]

    class Inputs:
        data = Input(name="data", type=TomwerScanBase)

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)

    want_main_area = True
    resizing_enabled = True

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = NXtomoMetadataViewer(parent=self)
        _layout.addWidget(self.widget)

    def _validateScan(self, scan):
        self.Outputs.data.send(scan)
        super().hide()

    @Inputs.data
    def setScan(self, scan):
        if scan is None:
            pass
        elif not isinstance(scan, NXtomoScan):
            raise TypeError(
                f"expect to have an instance of {NXtomoScan}. {type(scan)} provided."
            )
        else:
            self.widget.setScan(scan)
            self.show()
            self.raise_()

    def sizeHint(self):
        return qt.QSize(400, 500)
