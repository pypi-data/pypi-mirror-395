from __future__ import annotations

import logging
from orangecontrib.tomwer.orange.managedprocess import TomwerUnsupervisedOneThreadPerRun

from orangewidget import gui

from ewokscore.missing_data import is_missing_data

from tomwer.tasks.visualization.volume_viewer import VolumeViewerTask
from tomwer.gui.visualization.volume_viewer.VolumeViewerWindow import (
    VolumeViewerWindow,
)


_logger = logging.getLogger(__name__)


class VolumeViewerOW(
    TomwerUnsupervisedOneThreadPerRun,
    ewokstaskclass=VolumeViewerTask,
):
    """
    Widget embedding a viewer to display reconstructed volume.

    Several views are possible. One per axis or an 'overall' view (displaying the three axis in parallel).

    By default this widget allow users to browse the volume along the 'fast axis' and will sample 3 slices along each axis that could be displayed.
    If users agrees on loading the full volume then browsing can be done along any direction.
    """

    name = "volume viewer"
    id = "orange.widgets.tomwer.visualization.VolumeViewerOW.VolumeViewerOW"
    description = "Widget for browsing reconstructed volume."

    icon = "icons/volumeviewer.svg"
    priority = 31
    keywords = [
        "tomography",
        "volume",
        "tomwer",
        "reconstruction",
        "summary",
        "slices",
        "axis",
    ]

    _ewoks_inputs_to_hide_from_orange = ("load_volume",)

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._window = VolumeViewerWindow()
        self._box = gui.vBox(self.mainArea, self.name)
        self._box.layout().addWidget(self._window)
        self.loadSettings()

        # make sure 'load_volume' is defined.
        self.set_default_input("load_volume", self._window.isLoadingVolume())

        self._window.sigLoadVolume.connect(self._loadVolumeHasChanged)

    def handleNewSignals(self):
        volume = self.get_task_input_value("volume")
        if not is_missing_data(volume):
            self._startProcessing()
            self._window.initVolumePreview(volume=volume, message="Loading slices")

        super().handleNewSignals()

    def _loadVolumeHasChanged(self, load: bool):
        self.set_default_input("load_volume", load)

    def loadSettings(self):
        load_volume = self.get_default_input_value("load_volume", None)
        if load_volume is not None:
            self._window.setLoadingVolume(loading_volume=load_volume)

    def task_output_changed(self):
        slices = self.get_task_output_value("slices")
        volume_metadata = self.get_task_output_value("volume_metadata")
        volume_shape = self.get_task_output_value("volume_shape")
        loaded_volume = self.get_task_output_value("loaded_volume")

        if (not is_missing_data(slices)) and (not is_missing_data(volume_metadata)):
            self._window.setSlicesAndMetadata(
                slices=slices,
                metadata=volume_metadata,
                volume_shape=volume_shape,
            )

            if not is_missing_data(loaded_volume) and loaded_volume is not None:
                self._window.setVolume(loaded_volume)
        else:
            _logger.warning("Fail to load slices / metadata")
        self._window.setLoading(False)

        self._endProcessing()
        super().task_output_changed()
