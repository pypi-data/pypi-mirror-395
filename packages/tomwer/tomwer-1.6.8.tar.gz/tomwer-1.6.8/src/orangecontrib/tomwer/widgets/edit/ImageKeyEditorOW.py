import logging
from orangewidget import gui

import tomwer.core.process.edit.imagekeyeditor
from tomwer.gui.edit.imagekeyeditor import ImageKeyDialog
from ewokscore.missing_data import MissingData

from ...orange.managedprocess import TomwerWithStackStack

_logger = logging.getLogger(__name__)


class ImageKeyEditorOW(
    TomwerWithStackStack,
    ewokstaskclass=tomwer.core.process.edit.imagekeyeditor.ImageKeyEditorTask,
):
    """
    Widget to define on the fly the image_key of a NXtomoScan
    """

    name = "image-key-editor"
    id = "orange.widgets.tomwer.control.ImageKeyEditorOW.ImageKeyEditorOW"
    description = "Interface to edit `image_key` of nexus files"
    icon = "icons/image_key_editor.svg"
    priority = 24
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "edition",
        "NXTomo",
        "editor",
        "image key editor",
        "image-key-editor",
        "image_key",
        "image_key_control",
    ]

    want_main_area = True
    resizing_enabled = True

    _ewoks_inputs_to_hide_from_orange = ("configuration", "serialize_output_data")

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._scan = None
        layout = gui.vBox(self.mainArea, self.name).layout()

        self.widget = ImageKeyDialog(parent=self)
        layout.addWidget(self.widget)

        # connect signal / slot
        self.widget.sigValidated.connect(self._validateCallback)
        self.task_executor_queue.sigComputationStarted.connect(self._startProcessing)
        self.task_executor_queue.sigComputationEnded.connect(self._endProcessing)
        if isinstance(self.task_output_changed_callbacks, set):
            self.task_output_changed_callbacks.add(self._notify_state)
        elif isinstance(self.task_output_changed_callbacks, list):
            self.task_output_changed_callbacks.append(self._notify_state)
        else:
            raise NotImplementedError

    def handleNewSignals(self) -> None:
        scan = self.get_task_input_value("data", MissingData)
        if scan not in (None, MissingData):
            if scan is not self._scan:
                self._scan = scan
                self.widget.setScan(scan)
                self.notify_pending(scan=scan)
            self.activateWindow()
            self.raise_()
            self.show()

        # warning: avoid calling "handleNewSignals" else this will trigger the processing.
        # here we want for the user to explicitly click on 'validate' to modify the image keys

    def reprocess(self, scan):
        self.set_default_input(
            "data",
            scan,
        )

    def getConfiguration(self):
        return {
            "modifications": self.widget.getModifications(),
        }

    def _validateCallback(self):
        self.update_default_inputs(configuration=self.getConfiguration())
        self.update_default_inputs(
            serialize_output_data=False
        )  # avoid serializing when using orange
        self.execute_ewoks_task()

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
