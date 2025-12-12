from __future__ import annotations

import logging

from orangewidget import gui
from orangewidget.settings import Setting
from silx.io.url import DataUrl

import tomwer.core.process.edit.darkflatpatch
from tomwer.gui.edit.dkrfpatch import DarkRefPatchWidget

from ...orange.managedprocess import TomwerWithStackStack

_logger = logging.getLogger(__name__)


class DarkFlatPatchOW(
    TomwerWithStackStack,
    ewokstaskclass=tomwer.core.process.edit.darkflatpatch.DarkFlatPatchTask,
):
    """
    Widget to define on the fly the image_key of a NXtomoScan
    """

    name = "dark-flat-patch"
    id = "orange.widgets.tomwer.edit.DarkFlatPatchOW.DarkFlatPatchOW"
    description = "Interface to patch dark and flat to an existing NXTomo" "entry"
    icon = "icons/patch_dark_flat.svg"
    priority = 25
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "edition",
        "NXTomo",
        "editor",
        "dark",
        "patch",
        "ref",
        "flat",
    ]

    want_main_area = True
    resizing_enabled = True

    _urlsSetting = Setting(dict())
    _ewoks_inputs_to_hide_from_orange = ("configuration", "serialize_output_data")

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = gui.vBox(self.mainArea, self.name).layout()

        self.widget = DarkRefPatchWidget(parent=self)
        layout.addWidget(self.widget)

        self.setConfiguration(self._urlsSetting)

        # connect signal / slot
        self.task_executor_queue.sigComputationStarted.connect(self._startProcessing)
        self.task_executor_queue.sigComputationEnded.connect(self._endProcessing)
        self.widget.sigConfigurationChanged.connect(self._updateSettings)
        if isinstance(self.task_output_changed_callbacks, set):
            self.task_output_changed_callbacks.add(self._notify_state)
        elif isinstance(self.task_output_changed_callbacks, list):
            self.task_output_changed_callbacks.append(self._notify_state)
        else:
            raise NotImplementedError

    def reprocess(self, dataset):
        self.set_default_input(
            "data",
            dataset,
        )

    def get_task_inputs(self) -> dict:
        task_inputs = super().get_task_inputs()
        task_inputs.update(
            {
                "configuration": self.getConfiguration(),
                "serialize_output_data": False,  # avoid serializing when using orange
            }
        )
        return task_inputs

    def getConfiguration(self):
        def cast_url_to_str(url: DataUrl | None):
            if url is None:
                return None
            elif not isinstance(url, DataUrl):
                raise TypeError(
                    f"url is expected to be an optional DataUrl. {type(url)} provided instead"
                )
            else:
                return url.path()

        return {
            "darks_start": cast_url_to_str(self.widget.getStartDarkUrl()),
            "flats_start": cast_url_to_str(self.widget.getStartFlatUrl()),
            "darks_end": cast_url_to_str(self.widget.getEndDarkUrl()),
            "flats_end": cast_url_to_str(self.widget.getEndFlatUrl()),
        }

    def setConfiguration(self, config):
        if config is None:
            return
        self.widget.clear()
        url_keys = ("darks_start", "flats_start", "darks_end", "flats_end")
        url_index_keys = (
            "darks_start_index",
            "flats_start_index",
            "darks_end_index",
            "flats_end_index",
        )
        setters = (
            self.widget.setStartDarkUrl,
            self.widget.setStartFlatUrl,
            self.widget.setEndDarkUrl,
            self.widget.setEndFlatUrl,
        )
        for url_key, url_idx_key, setter in zip(url_keys, url_index_keys, setters):
            if url_key in config:
                index = config.get(url_idx_key, 0)
                url = config[url_key]
                if isinstance(url, str):
                    url = DataUrl(path=url)
                if url not in (None, ""):
                    assert isinstance(
                        url, DataUrl
                    ), "url is expected to be an url. Either as a str or as an instance of DataUrl"
                    try:
                        setter(url=url, series_index=index)
                    except Exception as e:
                        _logger.error(e)

    def _updateSettings(self):
        self._urlsSetting = self.getConfiguration()
        self._urlsSetting.update(
            {
                "darks_start_index": self.widget.getStartDarkIndex(),
                "flats_start_index": self.widget.getStartFlatIndex(),
                "darks_end_index": self.widget.getEndDarkIndex(),
                "flats_end_index": self.widget.getEndFlatIndex(),
            }
        )

    def _notify_state(self):
        try:
            task_executor = self.sender()
            task_suceeded = task_executor.succeeded
            scan = task_executor.current_task.inputs.data
            if task_suceeded:
                self.notify_succeed(scan=scan)
            else:
                self.notify_failed(scan=scan)
        except Exception as e:
            _logger.error(f"failed to handle task finished callback. Reason is {e}")
