# coding: utf-8

from __future__ import annotations

import copy
import logging
from contextlib import AbstractContextManager

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output
from silx.gui import qt

from tomwer.core.process.reconstruction.params_cache import (
    load_reconstruction_parameters_from_cache,
    save_reconstruction_parameters_to_cache,
)
import tomwer.core.process.reconstruction.nabu.nabuslices
from tomwer.core.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.scan.scanbase import TomwerScanBase, _TomwerBaseDock
from tomwer.core.volume.volumefactory import VolumeFactory

from tomwer.gui.reconstruction.nabu.slices import NabuWindow
from tomwer.synctools.stacks.reconstruction.nabu import NabuSliceProcessStack

from ...orange.managedprocess import SuperviseOW
from ..utils import WidgetLongProcessing

_logger = logging.getLogger(__name__)


class NabuOW(WidgetLongProcessing, SuperviseOW):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """

    # note of this widget should be the one registered on the documentation
    name = "nabu slice reconstruction"
    id = "orange.widgets.tomwer.reconstruction.NabuOW.NabuOW"
    description = "This widget will call nabu for running a reconstruction "
    icon = "icons/nabu_2d.svg"
    priority = 12
    keywords = ["tomography", "nabu", "reconstruction", "FBP", "filter"]

    want_main_area = True
    resizing_enabled = True

    _ewoks_default_inputs = Setting({"data": None, "nabu_params": None})

    ewokstaskclass = tomwer.core.process.reconstruction.nabu.nabuslices.NabuSlicesTask

    sigScanReady = qt.Signal(TomwerScanBase)
    "Signal emitted when a scan is ended"

    class Inputs:
        reprocess = Input(
            name="change recons params",
            type=_TomwerBaseDock,
            doc="reconpute slice with different parameters",
        )
        data = Input(
            name="data",
            type=TomwerScanBase,
            doc="one scan to be process",
            default=True,
            multiple=True,
        )
        cluster_in = Input(
            name="cluster_config",
            type=SlurmClusterConfiguration,
            doc="slurm cluster to be used",
            multiple=False,
        )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")

        future_out = Output(
            name="future_tomo_obj",
            type=FutureTomwerObject,
            doc="data with some remote processing",
        )

        slice_urls = Output(name="slice urls", type=tuple, doc="tuple of urls created")

    class DialogCM(AbstractContextManager):
        """Simple context manager to hide / show button dialogs"""

        def __init__(self, dialogButtonsBox):
            self._dialogButtonsBox = dialogButtonsBox

        def __enter__(self):
            self._dialogButtonsBox.show()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._dialogButtonsBox.hide()

    def __init__(self, parent=None):
        SuperviseOW.__init__(self, parent)
        WidgetLongProcessing.__init__(self)
        self._slurmCluster = None
        self.__exec_for_ci = False
        # processing tool
        self._processingStack = NabuSliceProcessStack(self, process_id=self.process_id)

        _layout = gui.vBox(self.mainArea, self.name).layout()
        # main widget
        self._nabuWidget = NabuWindow(parent=self)
        _layout.addWidget(self._nabuWidget)
        # add button to validate when change reconstruction parameters is
        # called
        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        _layout.addWidget(self._buttons)

        # set up
        self._buttons.hide()

        # load settings
        nabu_params = self._ewoks_default_inputs.get("nabu_params", None)
        if nabu_params not in (dict(), None):
            try:
                self._nabuWidget.setConfiguration(nabu_params)
            except Exception:
                _logger.warning("fail to load reconstruction settings")

        # expose API
        self.getMode = self._nabuWidget.getMode
        self.setMode = self._nabuWidget.setMode

        # connect signal / slot
        self._processingStack.sigComputationStarted.connect(self._startProcessing)
        self._processingStack.sigComputationEnded.connect(self._endProcessing)
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._nabuWidget.sigConfigChanged.connect(self._updateSettingsVals)

    def __new__(cls, *args, **kwargs):
        # ensure backward compatibility with 'static_input'
        static_input = kwargs.get("stored_settings", {}).get("static_input", None)
        if static_input not in (None, {}):
            _logger.warning(
                "static_input has been deprecated. Will be replaced by _ewoks_default_inputs in the workflow file. Please save the workflow to apply modifications"
            )
            kwargs["stored_settings"]["_ewoks_default_inputs"] = static_input
        return super().__new__(cls, *args, **kwargs)

    @Inputs.data
    def process(self, scan, *args, **kwargs):
        assert isinstance(scan, (TomwerScanBase, type(None)))
        if scan is None:
            return
        scan_ = copy.copy(scan)
        scan_.clear_latest_reconstructions()

        _logger.info(f"add {scan} to the stack")
        # update the reconstruction mode if possible
        self._nabuWidget.setScan(scan_)
        self._processingStack.add(scan_, self.getConfiguration())

    @Inputs.reprocess
    def reprocess(self, scan):
        """Recompute nabu with different parameters"""
        # wait for user to tune the reconstruction
        if scan is None:
            return

        self._nabuWidget.setScan(scan)

        if scan.axis_params is None or scan.axis_params.relative_cor_value is None:
            # try to retrieve last computed cor value from nabu process
            if scan.axis_params is None:
                from tomwer.synctools.axis import QAxisRP

                scan.axis_params = QAxisRP()
            load_reconstruction_parameters_from_cache(scan=scan)

        self.show()
        with NabuOW.DialogCM(self._buttons):
            if self.__exec_for_ci is True:
                self._ciExec()
            else:
                if self.exec():
                    # for now The behavior for reprocessing is the sama as for processing
                    if hasattr(scan, "instance"):
                        self.process(scan.instance)
                    else:
                        self.process(scan)

    def cancel(self, scan):
        if scan is None:
            return
        if scan in self._processingStack:
            self._processingStack.remove(scan)
        if (
            self._processingStack._data_currently_computed.get_identifier().to_str()
            == scan.get_identifier().to_str()
        ):
            # stop current processing
            self._processingStack.cancel()
            # if possible process next
            if self._processingStack.can_process_next():
                self._processingStack._process_next()

    @Inputs.cluster_in
    def setCluster(self, slurm_cluster: SlurmClusterConfiguration | None):
        assert isinstance(
            slurm_cluster, (type(None), SlurmClusterConfiguration)
        ), f"Expect None of SlurmClusterConfiguration. Not {type(slurm_cluster)}"
        self._slurmCluster = slurm_cluster

    def _endProcessing(self, scan, future_tomo_obj):
        WidgetLongProcessing._endProcessing(self, scan)
        if scan is not None:
            save_reconstruction_parameters_to_cache(scan=scan)
            # send scan
            self.Outputs.data.send(scan)
            # send slice urls
            slice_urls = []
            for rec_identifier in scan.latest_reconstructions:
                slice_urls.extend(
                    VolumeFactory.from_identifier_to_vol_urls(rec_identifier)
                )
            if len(slice_urls) > 0:
                slice_urls = tuple(slice_urls)
                # provide list of reconstructed slices
                self.Outputs.slice_urls.send(slice_urls)

            self.sigScanReady.emit(scan)
        if future_tomo_obj is not None:
            # send future scan
            self.Outputs.future_out.send(future_tomo_obj)

    def setDryRun(self, dry_run):
        self._processingStack.setDryRun(dry_run)

    def _ciExec(self):
        self.activateWindow()
        self.raise_()
        self.show()

    def _replaceExec_(self):
        """used for CI, replace the exec_ call ny"""
        self.__exec_for_ci = True

    def _updateSettingsVals(self):
        self._ewoks_default_inputs = {
            "data": None,
            "nabu_params": self.getConfiguration(),
        }

    def getConfiguration(self):
        config = self._nabuWidget.getConfiguration()
        config["cluster_config"] = self._slurmCluster
        return config

    def setConfiguration(self, config):
        # ignore slurm cluster. Defined by the upper widget
        config.pop("cluster_config", None)
        self._nabuWidget.setConfiguration(config=config)

    def keyPressEvent(self, event):
        """The event has to be filtered since we have some children
        that can be edited using the 'enter' key as defining the cor manually
        (see #481)). As we are in a dialog this automatically trigger
        'accepted'. See https://forum.qt.io/topic/5080/preventing-enter-key-from-triggering-ok-in-qbuttonbox-in-particular-qlineedit-qbuttonbox/5
        """
        if event.key() not in (qt.Qt.Key_Enter, qt.Qt.Key_Return):
            super().keyPressEvent(event)
