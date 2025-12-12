from __future__ import annotations

import functools
import logging

from orangewidget import gui, settings
from orangewidget.widget import Input, Output
from processview.core.manager import DatasetState, ProcessManager
from silx.gui import qt

import tomwer.core.process.control.scantransfer
from orangecontrib.tomwer.orange.managedprocess import SuperviseOW
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from tomwer.core.process.control.scantransfer import ScanTransferTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.control.datatransfert import DataTransfertSelector
from tomwer.utils import docstring

logger = logging.getLogger(__name__)


class DataTransfertOW(SuperviseOW):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """

    name = "data transfer"
    id = "orange.widgets.tomwer.foldertransfert"
    description = "This widget insure data transfer of the received data "
    description += "to the given directory"
    icon = "icons/folder-transfert.svg"
    priority = 30
    keywords = [
        "tomography",
        "transfert",
        "cp",
        "copy",
        "move",
        "file",
        "tomwer",
        "folder",
    ]

    ewokstaskclass = tomwer.core.process.control.scantransfer.ScanTransferTask

    settingsHandler = CallbackSettingsHandler()

    want_main_area = True
    resizing_enabled = True

    dest_dir_settings = settings.Setting(str())
    """Parameters directly editabled from the TOFU interface"""

    scanready = qt.Signal(TomwerScanBase)
    """emit when scan ready"""

    class Inputs:
        data = Input(name="data", type=TomwerScanBase)

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._destDir = None
        self._forceSync = False
        self._threads = []

        # define GUI
        self._widget = DataTransfertSelector(
            parent=self,
            rnice_option=True,
            default_root_folder=ScanTransferTask.getDefaultOutputDir(),
        )
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.addWidget(self._widget)

        # signal / SLOT connection
        self.settingsHandler.addCallback(self._updateSettingsVals)
        self._widget.sigSelectionChanged.connect(self._updateDestDir)

        # setting configuration
        if self.dest_dir_settings != "":
            self._widget.setFolder(self.dest_dir_settings)

    def _requestFolder(self):  # pragma: no cover
        """Launch a QFileDialog to ask the user the output directory"""
        dialog = qt.QFileDialog(self)
        dialog.setWindowTitle("Destination folder")
        dialog.setModal(1)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec():
            dialog.close()
            return None

        return dialog.selectedFiles()[0]

    def transfertDoneCallback(self, output_scan):
        if output_scan is None:
            return
        self.Outputs.data.send(output_scan)
        self.scanready.emit(output_scan)

    def _updateDestDir(self):
        self._destDir = self._widget.getFolder()

    def _updateSettingsVals(self):
        """function used to update the settings values"""
        self.dest_dir_settings = self._destDir

    @Inputs.data
    def process(self, scan):
        self._process(data=scan)

    def _process(self, data, move=False, force=True, noRsync=False):
        if data is None:
            return
        elif not isinstance(data, TomwerScanBase):
            raise TypeError("data is expected to be an instance of TomwerScanBase")

        inputs = {
            "data": data,
            "move": move,
            "overwrite": force,
            "noRsync": noRsync,
            "dest_dir": self._destDir,
            "block": self._forceSync,
            "serialize_output_data": False,
        }
        thread = ThreadDataTransfer(
            inputs=inputs,
            data=data,
            process=self,
        )
        try:
            process = ScanTransferTask(inputs=inputs)
        except Exception as e:
            logger.error(e)
        else:
            dest_dir = process.getDestinationDir(data.path, ask_for_output=False)
            if dest_dir is not None:
                thread.finished.connect(
                    functools.partial(
                        self.transfertDoneCallback,
                        data._deduce_transfert_scan(
                            process.getDestinationDir(data.path)
                        ),
                    )
                )
                thread.start()
            self._threads.append(thread)

    @docstring(SuperviseOW)
    def reprocess(self, dataset):
        self.process(dataset)

    def setDestDir(self, dest_dir):
        self._destDir = dest_dir

    def setForceSync(self, sync):
        self._forceSync = sync

    def isCopying(self):
        # for now only move file is handled
        return False


class ThreadDataTransfer(qt.QThread):
    def __init__(self, data, inputs, process) -> None:
        super().__init__()
        self._inputs = inputs
        self._data = data
        self._process = process

    def run(self):
        try:
            process = ScanTransferTask(inputs=self._inputs)
            process.run()
        except Exception as e:
            logger.error(f"data transfer failed. Reason is {e}")
            ProcessManager().notify_dataset_state(
                dataset=self._data,
                process=self._process,
                state=DatasetState.FAILED,
                details=str(e),
            )
        else:
            ProcessManager().notify_dataset_state(
                dataset=self._data,
                process=self._process,
                state=DatasetState.SUCCEED,
            )
