# coding: utf-8
from __future__ import annotations


import logging

from orangewidget import gui

import tomwer.core.process.edit.imagekeyeditor
from tomwer.gui.edit.imagekeyeditor import ImageKeyUpgraderWidget

from ...orange.managedprocess import TomwerWithStackStack

_logger = logging.getLogger(__name__)


class ImageKeyUpgraderOW(
    TomwerWithStackStack,
    ewokstaskclass=tomwer.core.process.edit.imagekeyeditor.ImageKeyUpgraderTask,
):
    """
    Widget to define upgrade all frames with some specific values of 'image_key' others values
    """

    name = "image-key-upgrader"
    id = "orange.widgets.tomwer.control.ImageKeyUpgraderOW.ImageKeyUpgraderOW"
    description = "Interface to upgrade all values of one or several specific `image_key` to a different value"
    icon = "icons/image_key_upgrader.svg"
    priority = 60
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "edition",
        "NXTomo",
        "editor",
        "image key upgrader",
        "image-key-upgrader",
        "image_key",
        "image_key_control",
    ]

    want_main_area = True
    resizing_enabled = True

    _ewoks_inputs_to_hide_from_orange = ("operations", "serialize_output_data")

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = ImageKeyUpgraderWidget(parent=self)
        _layout.addWidget(self.widget)

        # connect signal / slot
        if isinstance(self.task_output_changed_callbacks, set):
            self.task_output_changed_callbacks.add(self._notify_state)
        elif isinstance(self.task_output_changed_callbacks, list):
            self.task_output_changed_callbacks.append(self._notify_state)
        else:
            raise NotImplementedError
        self.widget.sigOperationsChanged.connect(self._update_operations_to_ewoks)

        self._updateGUIFromDefaultValues()
        # in case there is information registered and the GUI is not synchronized with the default values
        self._update_operations_to_ewoks()

    def _update_operations_to_ewoks(self):
        self.update_default_inputs(operations=self.widget.getOperations())

    def _updateGUIFromDefaultValues(self):
        try:
            operations = self.get_default_input_values()["operations"]
        except Exception:
            operations = {}
        self.widget.setOperations(operations)

    def get_task_inputs(self):
        task_inputs = super().get_task_inputs()
        task_inputs["serialize_output_data"] = False
        try:
            scan = task_inputs["data"]
        except Exception:
            pass
        else:
            self.notify_pending(scan=scan)
        return task_inputs

    def _execute_ewoks_task(self, propagate, log_missing_inputs=False):
        task_arguments = self._get_task_arguments()
        scan = task_arguments.get("inputs", {}).get("data", None)
        if scan is not None:
            self.notify_pending(scan=scan)
            super()._execute_ewoks_task(  # pylint: disable=E1123
                propagate=propagate, log_missing_inputs=log_missing_inputs
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
