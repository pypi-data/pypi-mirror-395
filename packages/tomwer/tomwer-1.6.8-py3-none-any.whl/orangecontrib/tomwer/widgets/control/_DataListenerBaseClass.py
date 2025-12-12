from __future__ import annotations

from orangewidget import gui, settings, widget
from orangewidget.widget import Output
from silx.gui import qt
import os

from orangecontrib.tomwer.widgets.utils import WidgetLongProcessing
from tomwer.core.process.control.datalistener import DataListener
from tomwer.core.process.control.nxtomomill import H5ToNxProcess
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.control.datalistener import DataListenerWidget
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.synctools.stacks.control.datalistener import DataListenerProcessStack
from tomwer.utils import docstring

from nxtomomill.models.h52nx import H52nxModel

import logging
import signal
from typing import Iterable

logger = logging.getLogger(__name__)


class DataListenerBaseClass(
    widget.OWBaseWidget,
    WidgetLongProcessing,
    DataListener,
    openclass=True,
):
    """
    This widget is a mix-in class for widgets listening a scan.
    Scan decovery can come from `bliss-tomo tomoSync<https://gitlab.esrf.fr/tomo/bliss-tomo/-/blob/main/tomo_listener/TomoSynch.py>`
    or from `bliss data <https://gitlab.esrf.fr/bliss/blissdata>`
    """

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _blissConfiguration = settings.Setting(dict())
    # to keep backward compatibility

    _nxtomo_cfg_file = settings.Setting(str())
    # to keep backward compatibility

    _static_input = settings.Setting(dict())

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")

    def __init__(self, host_discovery: str | None, parent=None, uses_rpc: bool = False):
        widget.OWBaseWidget.__init__(self, parent)
        WidgetLongProcessing.__init__(self)
        DataListener.__init__(self)
        self._processingStack = DataListenerProcessStack()
        self._processingStack.sigComputationEnded.connect(self._signal_scan_ready)
        self._widget = DataListenerWidget(parent=self, host_discovery=host_discovery)
        self._mock = False
        self._is_using_rpc = uses_rpc

        self._box = gui.vBox(self.mainArea, self.name)
        layout = self._box.layout()
        layout.addWidget(self._widget)

        # signal / slot connection
        self._widget.sigActivate.connect(self._activated)
        self._widget.sigDeactivate.connect(self._deactivated)
        self._widget.sigConfigurationChanged.connect(self._jsonRPCConfigChanged)
        self._widget.sigCFGFileChanged.connect(self._nxtomoFileChanged)
        self._widget.sigAcquisitionEnded.connect(self._process_bliss_file_frm_tuple)
        self._widget.sigServerStopped.connect(self._serverStopped)
        self._widget.sigMechanicalFlipsChanged.connect(self._mechanicalFlipHaveChanged)

        # set up
        self._loadSettings()

        # for convenience start the listener when create it.
        # ONLY if 'BEACON_HOST' is defined or using json-rpc
        if self._is_using_rpc or bool(os.environ.get("BEACON_HOST", "")):
            self.activate(True, is_using_rpc=self._is_using_rpc)

    def _loadSettings(self):
        if "bliss_server_configuration" in self._static_input:  # pylint: disable=E1135
            bliss_configuration = self._static_input[  # pylint: disable=E1136
                "bliss_server_configuration"
            ]
        else:
            bliss_configuration = self._blissConfiguration
        if bliss_configuration != {}:
            self._widget.setBlissServerConfiguration(bliss_configuration)
        if "nxtomomill_cfg_file" in self._static_input:  # pylint: disable=E1135
            nxtomo_cfg_file = self._static_input[  # pylint: disable=E1136
                "nxtomomill_cfg_file"
            ]
        else:
            nxtomo_cfg_file = self._nxtomo_cfg_file
        self._widget.setCFGFilePath(nxtomo_cfg_file)
        if "output_dir" in self._static_input:  # pylint: disable=E1135
            self._widget.setOutputFolder(
                self._static_input["output_dir"]  # pylint: disable=E1136
            )
        mechanical_flips = self._static_input.get("mechanical_flips")
        if mechanical_flips is not None:  # pylint: disable=E1135
            lr_flip, ud_flip = mechanical_flips
            with block_signals(self._widget):
                self._widget.setMechanicalFlips(
                    left_right_flip=lr_flip, up_down_flip=ud_flip
                )

    def getNXTomomillConfiguration(self):
        cfg_file = self._widget.getCFGFilePath()

        def create_default_config():
            configuration = H52nxModel()
            configuration.bam_single_file = True
            configuration.no_master_file = True
            return configuration

        if cfg_file in (None, ""):
            config = create_default_config()
        else:
            try:
                config = H52nxModel.from_cfg_file(cfg_file)
            except Exception as e:
                logger.warning(f"Fail to load configuration file. Error is {e}")
                config = create_default_config()
        # apply mechanical flip
        config.mechanical_lr_flip, config.mechanical_ud_flip = (
            self._widget.getMechanicalFlips()
        )
        return config

    def _process_bliss_file_frm_tuple(self, t):
        master_file, entry, proposal_file, saving_file, success = t
        bliss_scan = BlissScan(
            master_file=master_file,
            entry=str(entry) + ".1",
            proposal_file=proposal_file,
            saving_file=saving_file,
        )
        configuration = self.getNXTomomillConfiguration()
        # overwrite output file
        configuration.output_file = H5ToNxProcess.deduce_output_file_path(
            bliss_scan.master_file,
            output_dir=self._widget.getOutputFolder(),
            scan=bliss_scan,
        )
        if success:
            self._processingStack.add(data=bliss_scan, configuration=configuration)
        else:
            pass

    def activate(self, activate=True, is_using_rpc: bool = False):

        with block_signals(self._widget):
            self.set_configuration(self._widget.getBlissServerConfiguration())
            self._widget.activate(activate=activate)
            super().activate(activate=activate, is_using_rpc=is_using_rpc)
            self.processing_state(activate, info="listener active")

    def _activated(self):
        self.activate(True, is_using_rpc=self._is_using_rpc)

    def _deactivated(self):
        self.activate(False, is_using_rpc=self._is_using_rpc)

    def _mechanicalFlipHaveChanged(self):
        self._static_input["mechanical_flips"] = self._widget.getMechanicalFlips()

    def _serverStopped(self):
        """
        Callback when the server is stopped
        """
        self.activate(False, is_using_rpc=self._is_using_rpc)

    def _signal_scan_ready(self, scan, future_tomo_obj):
        if scan is None:
            return
        assert isinstance(scan, Iterable)
        for s in scan:
            assert isinstance(s, TomwerScanBase)
            self.Outputs.data.send(s)

    def _ask_user_for_overwritting(self, file_path):
        msg = qt.QMessageBox(self)
        msg.setIcon(qt.QMessageBox.Question)
        types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
        msg.setStandardButtons(types)

        text = "NXtomomill will overwrite: \n %s. Do you agree ?" % file_path
        msg.setText(text)
        return msg.exec() == qt.QMessageBox.Ok

    def _jsonRPCConfigChanged(self):
        self._blissConfiguration = self._widget.getBlissServerConfiguration()
        self._static_input["bliss_server_configuration"] = (  # pylint: disable=E1137
            self._widget.getBlissServerConfiguration()
        )
        self._static_input["output_dir"] = (  # pylint: disable=E1137
            self._widget.getOutputFolder()
        )
        if self.is_active():
            self.activate(False, is_using_rpc=True)
            self.activate(True, is_using_rpc=True)

    def _nxtomoFileChanged(self, cfg_file):
        self._nxtomo_cfg_file = cfg_file
        self._static_input["nxtomomill_cfg_file"] = cfg_file  # pylint: disable=E1137

    def setMock(self, mock, acquisitions):
        self._mock = mock
        self._mock_acquisitions = acquisitions

    @docstring(DataListenerWidget.getHost)
    def getHost(self):
        return self._widget.getHost()

    @docstring(DataListenerWidget.getPort)
    def getPort(self):
        return self._widget.getPort()

    def close(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.activate(False)
        super().close()

    def _get_n_scan_observe(self):
        return self._widget._observationWidget.observationTable.model().rowCount()

    def _get_n_scan_finished(self):
        return self._widget._historyWindow.scanHistory.model().rowCount()
