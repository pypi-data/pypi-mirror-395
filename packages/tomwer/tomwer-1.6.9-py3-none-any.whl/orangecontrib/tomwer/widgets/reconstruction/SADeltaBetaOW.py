# coding: utf-8
from __future__ import annotations


import functools
import logging

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output
from processview.core import helpers as pv_helpers
from processview.core.manager import DatasetState, ProcessManager
from silx.gui import qt

import tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta
from orangecontrib.tomwer.orange.managedprocess import SuperviseOW
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from tomwer.core import settings
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.core.cluster import SlurmClusterConfiguration
from tomwer.core.scan.scanbase import TomwerScanBase, _TomwerBaseDock
from tomwer.gui.reconstruction.sadeltabeta import (
    SADeltaBetaWindow as _SADeltaBetaWindow,
)
from tomwer.synctools.axis import QAxisRP
from tomwer.synctools.sadeltabeta import QSADeltaBetaParams
from tomwer.synctools.stacks.reconstruction.sadeltabeta import SADeltaBetaProcessStack

from ..utils import WidgetLongProcessing

_logger = logging.getLogger(__name__)


class SADeltaBetaWindow(_SADeltaBetaWindow):
    def __init__(self, Outputs, parent=None, process_id=None):
        _SADeltaBetaWindow.__init__(self, parent=parent)

        self.Outputs = Outputs
        self._sa_delta_beta_params = QSADeltaBetaParams()
        self._processing_stack = SADeltaBetaProcessStack(
            sa_delta_beta_params=self._sa_delta_beta_params, process_id=process_id
        )
        self._clusterConfig = None

    def setClusterConfig(self, cluster_config: dict):
        if not isinstance(
            cluster_config, (dict, type(None), SlurmClusterConfiguration)
        ):
            raise TypeError(
                f"cluster config is expected to be None, dict, {SlurmClusterConfiguration} not {type(cluster_config)}"
            )
        self._clusterConfig = cluster_config

    def _launchReconstructions(self):
        """callback when we want to launch the reconstruction of the
        slice for n cor value"""
        scan = self.getScan()
        if scan is None:
            return
        # step1: if isAutoFocus: validate automatically the scan
        # step2: update the interface if the current scan is the one displayed
        # else skip it
        callback = functools.partial(
            self._mightUpdateResult, scan, self.isAutoFocusLock()
        )
        self._processing_stack.add(
            data=scan, configuration=self.getConfiguration(), callback=callback
        )

    def _validate(self):
        self.validateCurrentScan()

    def _mightUpdateResult(self, scan: TomwerScanBase, validate: bool):
        if not isinstance(scan, TomwerScanBase):
            raise TypeError("scan is expected to be an instance of TomwerScanBase")
        if not isinstance(validate, bool):
            raise TypeError("validate is expected to be a boolean")
        if scan == self.getScan():
            self.setDBScores(
                scan.sa_delta_beta_params.scores,
                score_method=scan.sa_delta_beta_params.score_method,
            )
            if scan.sa_delta_beta_params.autofocus is not None:
                self.setCurrentDeltaBetaValue(scan.sa_delta_beta_params.autofocus)

            pm = ProcessManager()
            details = pm.get_dataset_details(
                dataset_id=scan.get_identifier(), process=self._processing_stack
            )
            current_state = ProcessManager().get_dataset_state(
                dataset_id=scan.get_identifier(), process=self._processing_stack
            )
            if current_state not in (
                DatasetState.CANCELLED,
                DatasetState.FAILED,
                DatasetState.SKIPPED,
            ):
                ProcessManager().notify_dataset_state(
                    dataset=scan,
                    process=self._processing_stack,
                    details=details,
                    state=DatasetState.WAIT_USER_VALIDATION,
                )
        if validate:
            self.validateScan(scan)

    def wait_processing(self, wait_time):
        self._processing_stack._computationThread.wait(wait_time)

    def validateCurrentScan(self):
        return self.validateScan(self.getScan())

    def validateScan(self, scan):
        if scan is None:
            return
        assert isinstance(scan, TomwerScanBase)
        selected_db_value = (
            self.getCurrentDeltaBetaValue() or scan.sa_delta_beta_params.autofocus
        )
        if selected_db_value is None:
            infos = f"no selected delta / beta value. {scan} skip SADeltaBetaParams"
            _logger.warning(infos)
            scan.sa_delta_beta_params.set_db_selected_value(None)
            pv_helpers.notify_skip(
                process=self._processing_stack, dataset=scan, details=infos
            )
        else:
            scan.sa_delta_beta_params.set_db_selected_value(selected_db_value)
            if scan.nabu_recons_params is not None:
                if "phase" not in scan.nabu_recons_params:
                    scan.nabu_recons_params["phase"] = {}
                scan.nabu_recons_params["phase"]["delta_beta"] = (selected_db_value,)
            _db_value = scan.sa_delta_beta_params.value
            infos = f"delta / beta selected for {scan}: {_db_value}"
            pv_helpers.notify_succeed(
                process=self._processing_stack, dataset=scan, details=infos
            )
        self.Outputs.data.send(scan)

    def getConfiguration(self) -> dict:
        config = super().getConfiguration()
        config["cluster_config"] = self._clusterConfig
        return config

    def setConfiguration(self, config: dict):
        # ignore slurm cluster. Defined by the upper widget
        config.pop("cluster_config", None)
        return super().setConfiguration(config)


class SADeltaBetaOW(SuperviseOW, WidgetLongProcessing):
    """
    Widget for semi-automatic delta / beta calculation

    behavior within a workflow:

    * no delta / beta value will be loaded even if an "axis" window exists on
      the upper stream.

    * if autofocus option is lock:

        * launch the series of reconstruction (with research width defined)
          and the estimated center of rotation if defined. Once the
          reconstruction is ended and if the autofocus button is still lock
          it will select the cor with the highest
          value and mode to workflow downstream.

    * hint: you can define a "multi-step" half-automatic center of rotation
      research by creating several "sa_delta_beta" widget and reducing the
      research width.

    Details about :ref:`sadeltabeta score calculation`
    """

    name = "multi-pag (sa-delta/beta calculation)"
    id = "orange.widgets.tomwer.sa_delta_beta"
    description = "Reconstruct a slice with several delta / beta values."
    icon = "icons/delta_beta_range.png"
    priority = 22
    keywords = [
        "multi",
        "multi-pag",
        "tomography",
        "semi automatic",
        "half automatic",
        "axis",
        "delta-beta",
        "delta/beta",
        "delta",
        "beta",
        "tomwer",
        "reconstruction",
        "position",
        "center of rotation",
        "sadeltabetaaxis",
        "sa_delta_beta_axis",
        "sa_delta_beta",
        "sadeltabeta",
    ]

    ewokstaskclass = (
        tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta.SADeltaBetaTask
    )

    want_main_area = True
    resizing_enabled = True

    settingsHandler = CallbackSettingsHandler()

    sigScanReady = qt.Signal(TomwerScanBase)
    """Signal emitted when a scan is ready"""

    _ewoks_default_inputs = Setting({"data": None, "sa_delta_beta_params": None})

    class Inputs:
        data = Input(name="data", type=TomwerScanBase, default=True, multiple=False)
        data_recompute = Input(
            name="change recons params",
            type=_TomwerBaseDock,
            doc="recompute delta / beta",
        )
        cluster_in = Input(
            name="cluster_config",
            type=SlurmClusterConfiguration,
            doc="slurm cluster to be used",
            multiple=False,
        )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        """

        :param parent: QWidget parent or None
        """
        SuperviseOW.__init__(self, parent)
        WidgetLongProcessing.__init__(self)

        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._widget = SADeltaBetaWindow(
            Outputs=self.Outputs, parent=self, process_id=self.process_id
        )
        self._layout.addWidget(self._widget)

        sa_delta_beta_params = self._ewoks_default_inputs.get(
            "sa_delta_beta_params", None
        )
        self.setConfiguration(sa_delta_beta_params or {})

        # connect signal / slot
        self._widget.sigConfigurationChanged.connect(self._updateSettings)
        self._widget._processing_stack.sigComputationStarted.connect(
            self._startProcessing
        )
        self._widget._processing_stack.sigComputationEnded.connect(self._endProcessing)
        # expose API
        self.wait_processing = self._widget.wait_processing

    def __new__(cls, *args, **kwargs):
        # ensure backward compatibility with 'static_input'
        static_input = kwargs.get("stored_settings", {}).get("static_input", None)
        if static_input not in (None, {}):
            _logger.warning(
                "static_input has been deprecated. Will be replaced by _ewoks_default_inputs in the workflow file. Please save the workflow to apply modifications"
            )
            kwargs["stored_settings"]["_ewoks_default_inputs"] = static_input
        return super().__new__(cls, *args, **kwargs)

    def setConfiguration(self, configuration):
        if "workflow" in configuration:
            autofocus_lock = configuration["workflow"].get("autofocus_lock", None)
            if autofocus_lock is not None:
                self._widget.lockAutofocus(autofocus_lock)
            del configuration["workflow"]
        self._widget.setConfiguration(configuration)

    def getCurrentCorValue(self):
        return self._widget.getCurrentCorValue()

    def load_sinogram(self):
        self._widget.loadSinogram()

    def compute(self):
        self._widget.compute()

    def lockAutofocus(self, lock):
        self._widget.lockAutofocus(lock=lock)

    def isAutoFocusLock(self):
        return self._widget.isAutoFocusLock()

    @Inputs.data
    def process(self, scan):
        if scan is None:
            return
        if scan.axis_params is None:
            scan.axis_params = QAxisRP()
        if scan.sa_delta_beta_params is None:
            scan.sa_delta_beta_params = QSADeltaBetaParams()
        self._skipCurrentScan(new_scan=scan)

        if settings.isOnLbsram(scan) and is_low_on_memory(settings.get_lbsram_path()):
            self.notify_skip(
                scan=scan,
                details=f"sa-delta-beta has been skiped for {scan} because of low space in lbsram",
            )
            self.Outputs.data.send(scan)
        else:
            self._widget.setScan(scan=scan)
            self.notify_pending(scan)
            self.activateWindow()
            if self.isAutoFocusLock():
                self.compute()
            else:
                self.raise_()
                self.show()

    def _skipCurrentScan(self, new_scan):
        scan = self._widget.getScan()
        # if the same scan has been run several scan
        if scan is None or str(scan) == str(new_scan):
            return
        current_scan_state = ProcessManager().get_dataset_state(
            dataset_id=scan.get_identifier(), process=self
        )
        if current_scan_state in (
            DatasetState.PENDING,
            DatasetState.WAIT_USER_VALIDATION,
        ):
            details = "Was pending and has been replaced by another scan."
            self.notify_skip(scan=scan, details=details)
            self.Outputs.data.send(scan)

    @Inputs.data_recompute
    def reprocess(self, dataset):
        self.lockAutofocus(False)
        self.process(dataset)

    @Inputs.cluster_in
    def setCluster(self, cluster):
        self._widget.setClusterConfig(cluster_config=cluster)

    def validateCurrentScan(self):
        self._widget.validateCurrentScan()

    def _updateSettings(self):
        config = self._widget.getConfiguration()
        config.pop("cluster_config", None)
        self._ewoks_default_inputs = {
            "data": None,
            "sa_delta_beta_params": self._widget.getConfiguration(),
        }
        self._ewoks_default_inputs["sa_delta_beta_params"]["workflow"] = {
            "autofocus_lock": self._widget.isAutoFocusLock(),
        }

    def getConfiguration(self):
        return self._widget.getConfiguration()

    def cancel(self, scan):
        if scan is None:
            return
        if scan in self._widget._processing_stack:
            self._widget._processing_stack.remove(scan)
        if (
            self._widget._processing_stack._data_currently_computed.get_identifier().to_str()
            == scan.get_identifier().to_str()
        ):
            # stop current processing
            self._widget._processing_stack.cancel()
            # if possible process next
            if self._widget._processing_stack.can_process_next():
                self._widget._processing_stack._process_next()

    def getWaitingOverlay(self):
        return self._widget._tabWidget._resultsViewer._plot.getWaiterOverlay()

    def _startProcessing(self, *args, **kwargs):
        self.getWaitingOverlay().show()
        super()._startProcessing()

    def _endProcessing(self, *args, **kwargs):
        self.getWaitingOverlay().hide()
        super()._endProcessing()
