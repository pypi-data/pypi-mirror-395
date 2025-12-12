from __future__ import annotations

import logging
from copy import copy


from nxtomomill.models.edf2nx import EDF2nxModel
from orangewidget import gui
from silx.gui import qt
from silx.gui.utils import blockSignals

from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack
from orangecontrib.tomwer.widgets.control.NXTomomillMixIn import NXTomomillMixIn
from tomwer.core.process.control.nxtomomill import EDFToNxProcess
from tomwer.core.process.output import ProcessDataOutputDirMode
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui.control.datalist import EDFDataListMainWindow

logger = logging.getLogger(__name__)


class EDF2NXOW(
    TomwerWithStackStack,
    NXTomomillMixIn,
    ewokstaskclass=EDFToNxProcess,
):
    """
    Widget to allow user to pick some bliss files and that will convert them
    to HDF5scan.
    """

    name = "nxtomomill - edf2nx (Spec-EDF)"
    id = "orange.widgets.tomwer.control.NXTomomillOW.EDF2NXOW"
    description = "Convert folders with .edf to .nx"
    icon = "icons/edf2nx.svg"
    priority = 121
    keywords = [
        "edf",
        "nexus",
        "tomwer",
        "file",
        "convert",
        "NXTomo",
        "tomography",
        "edf2nx",
        "nxtomomill",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    CONFIG_CLS = EDF2nxModel

    LOGGER = logger

    _ewoks_inputs_to_hide_from_orange = (
        "edf_to_nx_configuration",
        "progress",
        "serialize_output_data",
    )

    def __init__(self, parent=None):
        self.__configuration_cache = None
        # cache updated for each folder in order to match `_execute_ewoks_task` design

        TomwerWithStackStack.__init__(self, parent=parent)
        NXTomomillMixIn.__init__(self)
        _layout = gui.vBox(self.mainArea, self.name).layout()
        self.widget = EDFDataListMainWindow(parent=self)
        _layout.addWidget(self.widget)
        # for edf default output path is still the 'near to input file'
        self.widget._dialog._nxTomomillOutputWidget._inScanFolder.setChecked(True)
        # add 'convert auto' check box
        self._convertAutoCB = qt.QCheckBox(
            "convert automatically when edf scan send through 'edf scan' channel", self
        )
        self._convertAutoCB.setChecked(True)
        _layout.addWidget(self._convertAutoCB)

        # connect signal / slot
        self.widget._sendSelectedButton.clicked.connect(self._sendSelected)
        self.widget.sigNXTomoCFGFileChanged.connect(self._saveNXTomoCfgFile)
        self.widget.sigUpdated.connect(self._updateSettings)
        self._convertAutoCB.toggled.connect(self._updateSettings)

        # set default configuration is no existing configuration file defined in the settings
        self.update_default_inputs(
            edf_to_nx_configuration=EDF2nxModel().to_nested_model().model_dump(),
        )

        if isinstance(self.task_output_changed_callbacks, set):
            self.task_output_changed_callbacks.add(self._notify_state)
        elif isinstance(self.task_output_changed_callbacks, list):
            self.task_output_changed_callbacks.append(self._notify_state)
        else:
            raise NotImplementedError

        # handle settings
        self._loadSettings()

    def _updateSettings(self):
        # keep auto conversion setting
        self._ewoks_default_inputs[  # pylint: disable=E1137
            "convert_auto_edfscan_channel"
        ] = self.convertAutoEDFScanReceivedFromChannel()
        # store scans
        self._scans = []
        for scan in self.widget.datalist._myitems:
            self._scans.append(scan)
        # store output folder
        output_dir = self.widget.getOutputFolder()
        if isinstance(output_dir, ProcessDataOutputDirMode):
            output_dir = output_dir.value
        self._ewoks_default_inputs["output_dir"] = output_dir  # pylint: disable=E1137

    def convertAutoEDFScanReceivedFromChannel(self) -> bool:
        return self._convertAutoCB.isChecked()

    def setConvertAutoEDFScanReceivedFromChannel(self, checked: bool):
        self._convertAutoCB.setChecked(checked)

    def _loadSettings(self):
        with blockSignals(self.widget):
            for scan in self._scans:  # pylint: disable=E1133
                self.widget.add(scan)
            if (
                "nxtomomill_cfg_file" in self._ewoks_default_inputs
            ):  # pylint: disable=E1135
                self._nxtomo_cfg_file = (
                    self._ewoks_default_inputs[  # pylint: disable=E1136
                        "nxtomomill_cfg_file"
                    ]
                )
                self.widget.setCFGFilePath(self._nxtomo_cfg_file)
            if "output_dir" in self._ewoks_default_inputs:  # pylint: disable=E1135
                self.widget.setOutputFolder(
                    self._ewoks_default_inputs["output_dir"]  # pylint: disable=E1136
                )
            if (
                "convert_auto_edfscan_channel"
                in self._ewoks_default_inputs  # pylint: disable=E1135
            ):
                self.setConvertAutoEDFScanReceivedFromChannel(
                    self._ewoks_default_inputs[  # pylint: disable=E1136
                        "convert_auto_edfscan_channel"
                    ]
                )

    def _convertAndSend(self, edf_scan: EDFTomoScan):
        # cache updated for each folder in order to match `_execute_ewoks_task` design
        # for edf2nx we need to update input dir from the DataList and output_dir from
        # the one requested by the user
        if not isinstance(edf_scan, EDFTomoScan):
            raise TypeError(
                f"edf_scan is expected to be a {EDFTomoScan} not {type(edf_scan)}"
            )

        self.__configuration_cache = EDF2nxModel.from_dict(
            copy(self.get_default_input_values()["edf_to_nx_configuration"])
        )

        self.__configuration_cache.input_folder = edf_scan.path
        self.__configuration_cache.dataset_basename = edf_scan.dataset_basename

        output_file = EDFToNxProcess.deduce_output_file_path(
            folder_path=edf_scan.path,
            output_dir=self.widget.getOutputFolder(),
            scan=edf_scan,
        )
        output_entry = "entry"
        self.__configuration_cache.output_file = output_file
        # keep 'edf_to_nx_configuration' up to date according to input folder and output_file updates
        self.update_default_inputs(
            edf_to_nx_configuration=self.__configuration_cache.to_dict()
        )

        self.notify_on_going(scan=NXtomoScan(output_file, output_entry))
        try:
            self._execute_ewoks_task(  # pylint: disable=E1123
                propagate=True,
                log_missing_inputs=False,
            )
        except Exception:
            self._execute_ewoks_task(propagate=True)  # pylint: disable=E1123, E1120

    def get_task_inputs(self):
        return {
            "edf_to_nx_configuration": self.__configuration_cache.to_dict(),
            "serialize_output_data": False,
        }

    def handleNewSignals(self) -> None:
        """Invoked by the workflow signal propagation manager after all
        signals handlers have been called.
        """
        # for now we want to avoid propagation any processing.
        # task will be executed only when the user validates the dialog
        edf_scan = super().get_task_inputs().get("edf_scan", None)
        if edf_scan is not None:
            if not isinstance(edf_scan, EDFTomoScan):
                raise TypeError("edf_scan is expected to be an instance of EDFTomoScan")
            self.add(edf_scan.path)
            if self.convertAutoEDFScanReceivedFromChannel():
                self._convertAndSend(edf_scan)

    def _notify_state(self):
        try:
            task_executor = self.sender()
            task_suceeded = task_executor.succeeded
            config = task_executor.current_task.inputs.edf_to_nx_configuration
            config = EDF2nxModel.from_dict(config)
            scan = NXtomoScan(
                config.output_file,
                "entry",
            )
            if task_suceeded:
                self.notify_succeed(scan=scan)
            else:
                self.notify_failed(scan=scan)
        except Exception as e:
            logger.error(f"failed to handle task finished callback. Reason is {e}")

    def _saveNXTomoCfgFile(self, cfg_file):
        super()._saveNXTomoCfgFile(cfg_file, keyword="edf_to_nx_configuration")

    def _sendSelected(self):
        """send all selected items to be converted"""
        self._canOverwriteOutputs = False
        for scan_id in self.widget.datalist._myitems:
            tomo_obj = self.widget.datalist.getEDFTomoScan(scan_id, None)
            if tomo_obj:
                self._convertAndSend(tomo_obj)

    def _sendAll(self):
        """send all items to be converted"""
        self._canOverwriteOutputs = False
        for scan_id in self.widget.datalist._myitems:
            tomo_obj = self.widget.datalist.getEDFTomoScan(scan_id, None)
            if tomo_obj:
                self._convertAndSend(tomo_obj)

    def keyPressEvent(self, event):
        # forward Ctrl+A to the list as the shift ease selection of all
        modifiers = event.modifiers()
        key = event.key()
        if key == qt.Qt.Key_A and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self.widget._widget.datalist.keyPressEvent(event)
        super().keyPressEvent(event)
