# coding: utf-8
from __future__ import annotations

import copy
import logging

import tomoscan.esrf.scan.utils
from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output
from processview.core.manager import DatasetState, ProcessManager
from silx.gui import qt

import tomwer.core.process.reconstruction.darkref.darkrefscopy
from orangecontrib.tomwer.orange.managedprocess import SuperviseOW
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.reconstruction.darkref.darkrefcopywidget import DarkRefAndCopyWidget
from tomwer.synctools.darkref import QDKRFRP
from tomwer.synctools.stacks.reconstruction.dkrefcopy import DarkRefCopyProcessStack
from tomwer.utils import docstring

from ..utils import WidgetLongProcessing

_logger = logging.getLogger(__name__)


class DarkRefAndCopyOW(SuperviseOW, WidgetLongProcessing):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """

    # note of this widget should be the one registered on the documentation
    name = "reduced darks and flats"
    id = "orange.widgets.tomwer.darkrefs"
    description = (
        "This widget will generate reduced darks and flats for a received scan "
    )
    icon = "icons/darkref.svg"
    priority = 15
    keywords = ["tomography", "dark", "darks", "ref", "refs", "flat", "flats"]

    want_main_area = True
    resizing_enabled = True

    _ewoks_default_inputs = Setting({"data": None, "dark_ref_params": None})

    sigScanReady = qt.Signal(TomwerScanBase)
    """Signal emitted when a scan is ready"""

    ewokstaskclass = (
        tomwer.core.process.reconstruction.darkref.darkrefscopy.DarkRefsCopy
    )

    class Inputs:
        data = Input(
            name="data",
            type=TomwerScanBase,
            doc="one scan to be process",
            multiple=True,
        )
        reduced_darks = Input(
            name="reduced dark(s)",
            type=dict,
            doc="dict containing reduced dark(s)",
            multiple=False,
        )
        reduced_flats = Input(
            name="reduced flat(s)",
            type=dict,
            doc="dict of containing reduced flat(s)",
            multiple=False,
        )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")
        reduced_darks = Output(
            name="reduced dark(s)",
            type=dict,
            doc="DataUrl of the reduced dark. Key is the relative position, value is the reduced dark",
        )
        reduced_flats = Output(
            name="reduced flat(s)",
            type=dict,
            doc="DataUrl of the reduced flat. Key is the relative position, value is the reduced flat",
        )

    def __init__(self, parent=None, reconsparams: QDKRFRP | None = None):
        """

        :param reconsparams: reconstruction parameters
        """
        SuperviseOW.__init__(self, parent)
        WidgetLongProcessing.__init__(self)
        recons_params = reconsparams or QDKRFRP()
        self._processing_stack = DarkRefCopyProcessStack(process_id=self.process_id)

        dark_ref_params = self._ewoks_default_inputs.get("dark_ref_params", None)
        if dark_ref_params not in ({}, None):
            try:
                recons_params.dkrf.load_from_dict(dark_ref_params)
            except Exception:
                _logger.warning("fail to load reconstruction settings")

        self.widget = DarkRefAndCopyWidget(
            save_dir=self._processing_stack._save_dir,
            parent=self,
            reconsparams=recons_params,
            process_id=self.process_id,
        )
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.addWidget(self.widget)
        self.setForceSync = self.widget.setForceSync

        # expose API
        self.setModeAuto = self.widget.set_mode_auto
        self.setRefsFromScan = self.widget.setRefsFromScan
        self.setCopyActive = self.widget.setCopyActive

        # connect signal / slot
        self.widget.sigProcessingStart.connect(self._startProcessing)
        self.widget.sigProcessingEnd.connect(self._endProcessing)
        self.widget.sigScanReady.connect(self.signalReady)
        self.widget.recons_params.sigChanged.connect(self._updateSettingsVals)
        self.widget.sigModeAutoChanged.connect(self._updateSettingsVals)
        self.widget.sigCopyActivationChanged.connect(self._updateSettingsVals)
        self.widget.sigClearCache.connect(self._processing_stack.clear_cache)
        self._processing_stack.sigComputationStarted.connect(self._startProcessing)
        self._processing_stack.sigComputationEnded.connect(self._endProcessing)
        self._processing_stack.sigRefSetted.connect(self.widget.setRefSetBy)

        # load some other copy parameters
        if dark_ref_params not in ({}, None):
            try:
                if "activate" in dark_ref_params:
                    self.widget.setCopyActive(dark_ref_params.pop("activate"))
                if "auto" in dark_ref_params:
                    auto_mode = dark_ref_params.pop("auto")
                    # insure backward compatibility. Has beem saved as a tuple (this was a typo)
                    if isinstance(auto_mode, tuple) and isinstance(auto_mode[0], bool):
                        auto_mode = auto_mode[0]
                    self.widget.setModeAuto(auto_mode)
            except Exception:
                _logger.warning("fail to load reconstruction settings")

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
    def process(self, scanID, *args, **kwargs):
        if scanID is None:
            return
        assert isinstance(scanID, TomwerScanBase)
        ProcessManager().notify_dataset_state(
            dataset=scanID, process=self, state=DatasetState.PENDING
        )
        configuration = self.widget.recons_params.to_dict()
        configuration["process_only_copy"] = False  # we never only do copy from the gui
        configuration["process_only_dkrf"] = not self.widget.isCopyActive()
        configuration["mode_auto"] = self.widget.isOnModeAuto()

        self._processing_stack.add(copy.copy(scanID), configuration=configuration)

    @Inputs.reduced_darks
    def received_reduced_darks(self, reduced_darks: dict):
        # we consider if the darks are provided then the user want to use those and don't copy them manually
        self.setModeAuto(False)
        reduced_darks.pop("reduce_frames_name", None)
        self.setReducedDarks(reduced_darks)

    @Inputs.reduced_flats
    def received_reduced_flats(self, reduced_flats: dict):
        # we consider if the darks are provided then the user want to use those and don't copy them manually
        self.setModeAuto(False)
        reduced_flats.pop("reduce_frames_name", None)
        self.setReducedFlats(reduced_flats)

    @docstring(SuperviseOW)
    def reprocess(self, dataset):
        self.process(dataset)

    def signalReady(self, scanID):
        assert isinstance(scanID, TomwerScanBase)
        self.Outputs.data.send(scanID)
        self.sigScanReady.emit(scanID)

    def _updateSettingsVals(self):
        self._ewoks_default_inputs = {
            "data": None,
            "dark_ref_params": self.widget.recons_params.to_dict(),
        }
        self._ewoks_default_inputs["dark_ref_params"][
            "auto"
        ] = self.widget.isOnModeAuto()
        self._ewoks_default_inputs["dark_ref_params"][
            "activate"
        ] = self.widget.isCopyActive()

    @property
    def recons_params(self):
        return self.widget.recons_params

    def close(self):
        self.widget.close()
        super(DarkRefAndCopyOW, self).close()

    def _endProcessing(self, scan):
        WidgetLongProcessing._endProcessing(self, scan)
        self.Outputs.data.send(scan)
        self.sigScanReady.emit(scan)
        if scan.reduced_darks not in (None, {}):
            # we want to send those in relative position to have something generic. This is a convention for now
            reduced_darks = scan.reduced_darks
            reduced_darks.pop("reduce_frames_name", None)
            self.Outputs.reduced_darks.send(
                tomoscan.esrf.scan.utils.from_absolute_reduced_frames_to_relative(
                    reduced_frames=reduced_darks, scan=scan
                )
            )
        if scan.reduced_flats not in (None, {}):
            # we want to send those in relative position to have something generic. This is a convention for now
            reduced_flats = scan.reduced_flats
            reduced_flats.pop("reduce_frames_name", None)
            self.Outputs.reduced_flats.send(
                tomoscan.esrf.scan.utils.from_absolute_reduced_frames_to_relative(
                    reduced_frames=reduced_flats, scan=scan
                )
            )
        _logger.info(f"{scan} ended")

    def setReducedDarks(self, darks: dict):
        self.widget._refCopyWidget.save_darks_to_be_copied(darks)

    def setReducedFlats(self, flats: dict):
        self.widget._refCopyWidget.save_flats_to_be_copied(flats)
