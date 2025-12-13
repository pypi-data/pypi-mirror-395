import logging

from silx.gui import qt

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output, OWBaseWidget
from tomoscan.series import Series

from tomwer.core.tomwer_object import TomwerObject
from tomwer.gui.stitching.StitchingWindow import ZStitchingWindow

_logger = logging.getLogger(__name__)


class ZStitchingConfigOW(OWBaseWidget):
    """
    Widget to create a stitching configuration to be used with nabu-stitching
    """

    name = "z-stitching config"
    id = "orange.widgets.tomwer.stitching.ZStitchingConfigOW.ZStitchingConfigOW"
    description = (
        "Interface to create / edit a z-stitching to be used with nabu-stitching"
    )
    icon = "icons/zstitching_icon.svg"
    priority = 60
    keywords = [
        "hdf5",
        "tomwer",
        "NXTomo",
        "stitching",
        "z-stitching",
        "z-series",
        "zseries",
        "pre-processing",
        "radios",
        "projections",
    ]

    want_main_area = True
    resizing_enabled = True
    want_control_area = False

    _ewoks_default_inputs = Setting({})

    class Inputs:
        tomo_obj = Input(
            name="tomo_obj",
            type=TomwerObject,
            doc="one scan to be process",
            default=True,
            multiple=True,
        )

        series = Input(
            "series",
            type=Series,
            doc="series of scan or volumes to be stitched together",
            default=False,
            multiple=False,
        )

    class Outputs:
        stitching_config = Output(
            name="stitching configuration",
            type=dict,
            doc="configuration to stitch together tomo object as a dictionary",
        )

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = ZStitchingWindow(parent=self)
        _layout.addWidget(self.widget)

        # connect signal / slot
        self.widget.sigChanged.connect(self._storeSettings)

        # load settings
        self.setConfiguration(self._ewoks_default_inputs)

    def setConfiguration(self, config: dict) -> None:
        self.widget.setConfiguration(config=config)

    def getConfiguration(self) -> dict:
        return self.widget.getConfiguration()

    def _storeSettings(self):
        self._ewoks_default_inputs = self.widget.getConfiguration()

    @Inputs.tomo_obj
    def addTomoObj(self, tomo_obj, *args, **kwargs):
        self.widget.addTomoObj(tomo_obj)

    @Inputs.series
    def setSeries(self, series, *args, **kwargs):
        self.widget.setSeries(series)
        self._storeSettings()

    def validate(self):
        config = self.widget.getConfiguration()
        assert isinstance(config, dict)
        self.Outputs.stitching_config.send(config)

    def keyPressEvent(self, event):
        """
        To shortcut orange and make sure the `F5` <=> refresh stitching preview
        """
        if event.key() == qt.Qt.Key_F5:
            self.widget._trigger_update_preview()
        else:
            super().keyPressEvent(event)

    def close(self):
        self.widget.close()
        super().close()
