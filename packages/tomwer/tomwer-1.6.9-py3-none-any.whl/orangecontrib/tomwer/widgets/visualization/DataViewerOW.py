# coding: utf-8
from __future__ import annotations

import logging

from orangewidget import gui, settings, widget
from orangewidget.widget import Input
from silx.gui import qt

import tomwer.core.process.visualization.dataviewer
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui import icons, utils
from tomwer.gui.visualization.dataviewer import DataViewer

_logger = logging.getLogger(__name__)


class DataViewerOW(widget.OWBaseWidget, openclass=True):
    """a data viewer able to:

    - display slices (latest reconstructed if any)
    - display radios with or without normalization

    :param parent: the parent widget
    """

    name = "data viewer"
    id = "orange.widgets.tomwer.dataviewer"
    description = "allow user too browse through data"
    icon = "icons/eye.png"
    priority = 70
    keywords = ["tomography", "file", "tomwer", "acquisition", "validation"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    ewokstaskclass = tomwer.core.process.visualization.dataviewer._DataViewerPlaceHolder

    _viewer_config = settings.Setting(dict())

    class Inputs:
        data = Input(
            name="data",
            type=TomwerScanBase,
            multiple=True,
        )

    def __init__(self, parent=None):
        super().__init__(parent)
        self._imagejThreads = []
        # threads used to open frames with image j
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self.viewer = DataViewer(parent=self)
        self.viewer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self._layout.addWidget(self.viewer)
        self._setSettings(settings=self._viewer_config)

        # open with ImageJ button
        types = qt.QDialogButtonBox.Apply
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self._buttonOpenImageJ = self._buttons.button(qt.QDialogButtonBox.Apply)
        self._buttonOpenImageJ.setText("open with ImageJ")
        self._buttonOpenImageJ.setIcon(icons.getQIcon("Imagej_icon"))
        self.layout().addWidget(self._buttons)

        # connect signal / slot
        self.viewer.sigConfigChanged.connect(self._updateSettings)
        self._buttonOpenImageJ.released.connect(self._openCurrentInImagej)

    def _openCurrentInImagej(self):
        current_url = self.viewer.getCurrentUrl()

        if current_url is None:
            _logger.warning("No active image defined")
        else:
            try:
                self._imagejThreads.append(utils.open_url_with_image_j(current_url))
            except OSError as e:
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Warning)
                msg.setWindowTitle("Unable to open image in imagej")
                msg.setText(str(e))
                msg.exec()

    @Inputs.data
    def addScan(self, scan, *args, **kwargs):
        if scan is None:
            return
        self.viewer.setScan(scan)

    def sizeHint(self):
        return qt.QSize(400, 500)

    def _updateSettings(self):
        self._viewer_config["mode"] = (  # pylint: disable=E1137
            self.viewer.getDisplayMode().value
        )
        self._viewer_config["slice_opt"] = (  # pylint: disable=E1137
            self.viewer.getSliceOption().value
        )
        self._viewer_config["radio_opt"] = (  # pylint: disable=E1137
            self.viewer.getRadioOption().value
        )

    def _setSettings(self, settings):
        old_state = self.viewer.blockSignals(True)
        if "mode" in settings:
            self.viewer.setDisplayMode(settings["mode"])
        if "slice_opt" in settings:
            self.viewer.setSliceOption(settings["slice_opt"])
        if "radio_opt" in settings:
            self.viewer.setRadioOption(settings["radio_opt"])
        self.viewer.blockSignals(old_state)

    def close(self):
        [thread.quit() for thread in self._imagejThreads]
        self.viewer.close()
        self.viewer = None
        super().close()
