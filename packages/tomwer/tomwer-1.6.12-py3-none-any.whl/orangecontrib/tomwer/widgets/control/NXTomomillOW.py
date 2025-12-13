from __future__ import annotations

import logging
import os
from copy import copy

from nxtomomill.models.h52nx import H52nxModel
from orangewidget import gui
from orangewidget.settings import Setting

from silx.gui import qt
from silx.gui.utils import blockSignals

from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack
from orangecontrib.tomwer.widgets.control.NXTomomillMixIn import NXTomomillMixIn
from tomwer.core.process.control.nxtomomill import H5ToNxProcess
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.nxtomoscan import NXtomoScan, NXtomoScanIdentifier
from tomwer.gui.control.datalist import BlissHDF5DataListMainWindow
from tomwer.gui.control.nxtomomill import NXTomomillInput, OverwriteMessage
from tomwer.core.process.output import ProcessDataOutputDirMode
from ewoksorange.bindings.owwidgets import invalid_data


logger = logging.getLogger(__name__)


class NXTomomillOW(
    TomwerWithStackStack,
    NXTomomillMixIn,
    ewokstaskclass=H5ToNxProcess,
):
    """
    Widget to allow user to pick some bliss files and that will convert them
    to HDF5scan.
    """

    name = "nxtomomill h52nx (bliss-HDF5)"
    id = "orange.widgets.tomwer.control.NXTomomillOW.NXTomomillOW"
    description = (
        "Read a bliss .h5 file and extract from it all possible"
        "NxTomo. When validated create a TomwerBaseScan for each "
        "file and entry"
    )
    icon = "icons/nxtomomill.svg"
    priority = 120
    keywords = [
        "hdf5",
        "nexus",
        "tomwer",
        "file",
        "convert",
        "NXTomo",
        "tomography",
        "nxtomomill",
        "h52nx",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    CONFIG_CLS = H52nxModel

    LOGGER = logger

    _ewoks_inputs_to_hide_from_orange = (
        "h5_to_nx_configuration",
        "progress",
        "serialize_output_data",
    )

    _detector_mechanical_flips = Setting(tuple([False, False]))

    def __init__(self, parent=None):
        TomwerWithStackStack.__init__(self, parent=parent)
        NXTomomillMixIn.__init__(self)
        _layout = gui.vBox(self.mainArea, self.name).layout()

        self.widget = BlissHDF5DataListMainWindow(parent=self)
        _layout.addWidget(self.widget)
        self.__request_input = True
        # do we ask the user for input if missing
        self._inputGUI = None
        """Gui with cache for missing field in files to be converted"""
        self._canOverwriteOutputs = False
        """Cache to know if we have to ask user permission for overwriting"""

        # expose API
        self.n_scan = self.widget.n_scan
        # alias used for the 'simple workflow' for now
        self.start = self._sendAll

        # connect signal / slot
        self.widget._sendSelectedButton.clicked.connect(self._sendSelected)
        self.widget.sigNXTomoCFGFileChanged.connect(self._saveNXTomoCfgFile)
        self.widget.sigUpdated.connect(self._updateSettings)

        # set default configuration is no existing configuration file defined in the settings
        # note: historically the model was a 'nested one'. Let's keep it as it is for now
        # to avoid any breaking modification
        default_config = H52nxModel().to_nested_model()
        default_config = {
            key.upper(): value for key, value in default_config.model_dump().items()
        }
        self.update_default_inputs(
            h5_to_nx_configuration=default_config,
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
        self._scans = []
        for scan in self.widget.datalist._myitems:
            # kept for backward compatibility since 0.11. To be removed on the future version.
            if "@" in scan:
                entry, file_path = scan.split("@")
                nxtomo_scan = NXtomoScan(entry=entry, scan=file_path)
                self.add(nxtomo_scan)
            else:
                self._scans.append(scan)
        output_dir = self.widget.getOutputFolder()
        if isinstance(output_dir, ProcessDataOutputDirMode):
            output_dir = output_dir.value
        self._ewoks_default_inputs["output_dir"] = output_dir  # pylint: disable=E1137
        self._detector_mechanical_flips = self.widget._dialog.getMechanicalFlips()

    @property
    def request_input(self):
        return self.__request_input

    @request_input.setter
    def request_input(self, request):
        self.__request_input = request

    def get_task_inputs(self):
        return {
            "h5_to_nx_configuration": self.__configuration_cache.to_dict(),
            "serialize_output_data": False,
        }

    def handleNewSignals(self) -> None:
        """Invoked by the workflow signal propagation manager after all
        signals handlers have been called.
        """
        # for now we want to avoid propagation any processing.
        # task will be executed only when the user validates the dialog
        bliss_scan = super().get_task_inputs().get("bliss_scan", None)
        if bliss_scan is not None:
            if not isinstance(bliss_scan, BlissScan):
                raise TypeError("bliss_scan is expected to be an instance of BlissScan")
            self.add(bliss_scan.master_file)

    def _convertAndSend(self, bliss_url: str):
        """

        :param bliss_url: string at entry@file format
        """
        logger.processStarted(f"Start translate {bliss_url} to NXTomo")
        self.__configuration_cache = H52nxModel.from_dict(
            copy(self.get_default_input_values()["h5_to_nx_configuration"])
        )

        identifier = NXtomoScanIdentifier.from_str(bliss_url)
        bliss_scan = BlissScan(
            master_file=identifier.file_path,
            entry=identifier.data_path,
            proposal_file=None,
        )

        output_file_path = H5ToNxProcess.deduce_output_file_path(
            bliss_scan.master_file,
            output_dir=self.widget.getOutputFolder(),
            scan=bliss_scan,
        )

        self.__configuration_cache.input_file = bliss_scan.master_file
        self.__configuration_cache.output_file = output_file_path
        self.__configuration_cache.entries = (bliss_scan.entry,)
        self.__configuration_cache.single_file = False
        self.__configuration_cache.overwrite = True
        self.__configuration_cache.request_input = self.request_input
        self.__configuration_cache.file_extension = ".nx"
        (
            self.__configuration_cache.mechanical_lr_flip,
            self.__configuration_cache.mechanical_ud_flip,
        ) = self.widget._dialog.getMechanicalFlips()

        self._processBlissScan(bliss_scan)

    def _userAgreeForOverwrite(self, file_path):
        if self._canOverwriteOutputs:
            return True
        else:
            msg = OverwriteMessage(self)
            text = "NXtomomill will overwrite \n %s. Do you agree ?" % file_path
            msg.setText(text)
            if msg.exec():
                self._canOverwriteOutputs = msg.canOverwriteAll()
                return True
            else:
                return False

    def _processBlissScan(self, bliss_scan):
        if bliss_scan is None:
            return
        output_file_path = H5ToNxProcess.deduce_output_file_path(
            bliss_scan.master_file,
            output_dir=self.widget.getOutputFolder(),
            scan=bliss_scan,
        )
        # check user has rights to write on the folder
        dirname = os.path.dirname(output_file_path)
        if os.path.exists(dirname) and not os.access(dirname, os.W_OK):
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Warning)
            text = f"You don't have write rights on '{dirname}'. Unable to generate the nexus file associated to {str(bliss_scan)}"
            msg.setWindowTitle("No rights to write")
            msg.setText(text)
            msg.show()
            return
        # check if need to overwrite the file
        elif os.path.exists(output_file_path):
            if not self._userAgreeForOverwrite(output_file_path):
                return

        # keep 'h5_to_nx_configuration' up to date according to input folder and output_file updates
        self.update_default_inputs(
            h5_to_nx_configuration=self.__configuration_cache.to_dict()
        )
        try:
            self._execute_ewoks_task(  # pylint: disable=E1123
                propagate=True,
                log_missing_inputs=False,
            )
        except Exception:
            self._execute_ewoks_task(propagate=True)  # pylint: disable=E1123, E1120

    def _loadSettings(self):
        with blockSignals(self.widget):
            for scan in self._scans:
                assert isinstance(scan, str)
                try:
                    self.widget.add(scan)
                except Exception as e:
                    logger.error(f"Fail to add {scan}. Error is {e}")
                else:
                    logger.warning(f"{scan} is an invalid link to a file")
            if (
                "nxtomomill_cfg_file" in self._ewoks_default_inputs
            ):  # pylint: disable=E1135
                nxtomo_cfg_file = self._ewoks_default_inputs[  # pylint: disable=E1136
                    "nxtomomill_cfg_file"
                ]
                self.widget.setCFGFilePath(nxtomo_cfg_file)
            if "output_dir" in self._ewoks_default_inputs:  # pylint: disable=E1135
                self.widget.setOutputFolder(
                    self._ewoks_default_inputs["output_dir"]  # pylint: disable=E1136
                )
            if len(self._detector_mechanical_flips) == 2:
                self.widget._dialog.setMechanicalFlips(*self._detector_mechanical_flips)

    def _saveNXTomoCfgFile(self, cfg_file):
        super()._saveNXTomoCfgFile(cfg_file, keyword="h5_to_nx_configuration")

    def _sendSelected(self):
        """Send a signal for selected scans found to the next widget"""
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist.selectedItems():
            data = bliss_url.data(qt.Qt.UserRole)
            assert isinstance(data, NXtomoScan)
            identifier = data.get_identifier()
            self._inputGUI.setBlissScan(
                entry=identifier.data_path, file_path=identifier.file_path
            )
            self._convertAndSend(identifier.to_str())

    def _sendAll(self):
        """Send a signal for each scan found to the next widget"""
        self._inputGUI = NXTomomillInput()
        # reset the GUI for input (reset all the cache for answers)
        self._canOverwriteOutputs = False
        for bliss_url in self.widget.datalist._myitems.values():
            data = bliss_url.data(qt.Qt.UserRole)
            identifier = data.get_identifier()
            assert isinstance(data, NXtomoScan)
            self._inputGUI.setBlissScan(
                entry=identifier.data_path, file_path=identifier.file_path
            )
            self._convertAndSend(identifier.to_str())

    def _notify_state(self):
        try:
            task_executor = self.sender()
            task_suceeded = task_executor.succeeded
            config = task_executor.current_task.inputs.h5_to_nx_configuration
            config = H52nxModel.from_dict(config)
            scan = task_executor.current_task.outputs.data
            if task_suceeded:
                self.notify_succeed(scan=scan)
            else:
                self.notify_failed(scan=scan)
        except Exception as e:
            logger.error(f"failed to handle task finished callback. Reason is {e}")

    def trigger_downstream(self) -> None:
        for ewoksname, var in self.get_task_outputs().items():
            # note: for now we want to trigger 'data' for each items of 'datas'
            if ewoksname == "series" and not (
                invalid_data.is_invalid_data(var.value) or var.value is None
            ):
                for data in var.value:
                    data_channel = self._get_output_signal("data")
                    data_channel.send(data)
                serie_channel = self._get_output_signal("series")
                # then send the list of value / series (also know as datas)
                serie_channel.send(var.value)
            elif ewoksname == "data" and not (
                invalid_data.is_invalid_data(var.value) or var.value is None
            ):
                pass  # handle by 'series' in this case

    def keyPressEvent(self, event):
        # forward Ctrl+A to the list as the shift ease selection of all
        modifiers = event.modifiers()
        key = event.key()
        if key == qt.Qt.Key_A and modifiers == qt.Qt.KeyboardModifier.ControlModifier:
            self.widget._widget.datalist.keyPressEvent(event)
        super().keyPressEvent(event)
