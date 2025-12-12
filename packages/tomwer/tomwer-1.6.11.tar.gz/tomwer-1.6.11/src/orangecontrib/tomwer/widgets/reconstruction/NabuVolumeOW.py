# coding: utf-8
from __future__ import annotations

import copy
import functools
import logging
from typing import Iterable
from contextlib import AbstractContextManager

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output
from silx.gui import qt
from tomoscan.identifier import VolumeIdentifier

import tomwer.core.process.reconstruction.nabu.nabuvolume
from orangecontrib.tomwer.widgets.utils import WidgetLongProcessing
from tomwer.core.process.reconstruction.params_cache import (
    load_reconstruction_parameters_from_cache,
)
from tomwer.core import settings
from tomwer.core.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.process.drac.processeddataset import (
    DracReconstructedVolumeDataset,
)
from tomwer.core.process.reconstruction.nabu import utils as nabu_utils
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.char import BETA_CHAR, DELTA_CHAR
from tomwer.core.utils.scanutils import format_output_location
from tomwer.core.process.reconstruction.nabu.utils import update_nabu_config_for_tiff_3d
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.gui.reconstruction.nabu.volume import NabuVolumeWindow
from tomwer.synctools.stacks.reconstruction.nabu import NabuVolumeProcessStack
from tomwer.utils import docstring

from ...orange.managedprocess import SuperviseOW

_logger = logging.getLogger(__name__)


class NabuVolumeOW(WidgetLongProcessing, SuperviseOW):
    """
    A simple widget managing the copy of an incoming folder to an other one

    :param parent: the parent widget
    """

    # note of this widget should be the one registered on the documentation
    name = "nabu volume reconstruction"
    id = "orange.widgets.tomwer.reconstruction.NabuVolumeOW.NabuVolumeOW"
    description = (
        "This widget will call nabu for running a reconstruction " "on a volume"
    )
    icon = "icons/nabu_3d.svg"
    priority = 15
    keywords = ["tomography", "nabu", "reconstruction", "volume"]

    ewokstaskclass = tomwer.core.process.reconstruction.nabu.nabuvolume.NabuVolumeTask

    want_main_area = True
    resizing_enabled = True

    _ewoks_default_inputs = Setting(
        {"data": None, "nabu_volume_params": None, "nabu_params": None}
    )

    sigScanReady = qt.Signal(TomwerScanBase)
    "Signal emitted when a scan is ended"

    TIMEOUT = 30

    class Inputs:
        data = Input(
            name="data",
            type=TomwerScanBase,
            doc="one scan to be process",
            default=True,
            multiple=False,
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
        volume = Output(
            name="volume",
            type=TomwerVolumeBase,
            doc="volume(s) created",
        )
        volume_urls = Output(
            name="volume urls", type=tuple, doc="url of the volume(s) reconstructed"
        )
        data_portal_processed_datasets = Output(
            name="data_portal_processed_datasets",
            type=tuple,
            doc="data portal processed data to be saved",
        )

    class DialogCM(AbstractContextManager):
        """Simple context manager to hide / show button dialogs"""

        def __init__(self, dialogButtonsBox):
            self._dialogButtonsBox = dialogButtonsBox

        def __enter__(self):
            self._dialogButtonsBox.show()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._dialogButtonsBox.hide()

    def __init__(self, parent=None, *args, **kwargs):
        SuperviseOW.__init__(self, parent)
        WidgetLongProcessing.__init__(self)
        self._slurmCluster = None
        # processing tool
        self._processingStack = NabuVolumeProcessStack(self, process_id=self.process_id)

        _layout = gui.vBox(self.mainArea, self.name).layout()
        # main widget
        self._nabuWidget = NabuVolumeWindow(parent=self)
        _layout.addWidget(self._nabuWidget)
        # add button to validate when change reconstruction parameters is called
        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        _layout.addWidget(self._buttons)

        # set up
        self._buttons.hide()

        # load settings
        nabu_volume_params = self._ewoks_default_inputs.get("nabu_volume_params", None)

        if nabu_volume_params not in (dict(), None):
            try:
                self.setConfiguration(nabu_volume_params)
            except Exception:
                _logger.warning("fail to load reconstruction settings")

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
    def process(self, scan: TomwerScanBase):
        assert isinstance(scan, (TomwerScanBase, type(None)))
        if scan is None:
            return
        scan_ = copy.copy(scan)
        scan_.clear_latest_vol_reconstructions()

        # insure we are able to reconstruct
        if scan.nabu_recons_params in ({}, None):
            _logger.error(
                f"No reconstruction parameters found from nabu slices for {scan}. "
                "You should first run slice reconstruction prior to volume reconstruction"
            )
            self.Outputs.data.send(scan)
            self.sigScanReady.emit(scan)
            return

        config = scan.nabu_recons_params
        # update output format if requested
        nabuSettingsWidget = self._nabuWidget._mainWidget._nabuSettingsWidget
        if nabuSettingsWidget.redefineNabuFileFormat():
            config["output"]["file_format"] = nabuSettingsWidget.getNabuFileFormat()
            update_nabu_config_for_tiff_3d(config)
        # update output location if requested
        if nabuSettingsWidget.redefineOutputLocation():
            location = nabuSettingsWidget.getNabuOutputLocation()
            if location is not None:
                location = format_output_location(location=location, scan=scan)
            config["output"]["location"] = location
            config["output"][
                "output_dir_mode"
            ] = nabuSettingsWidget._outputLocationWidget.getOutputDirMode().value

        if "phase" in config and "delta_beta" in config["phase"]:
            pag_dbs = config["phase"]["delta_beta"]
            if isinstance(pag_dbs, str):
                try:
                    pag_dbs = nabu_utils.retrieve_lst_of_value_from_str(
                        config["phase"]["delta_beta"], type_=float
                    )
                except Exception:
                    pass
            if len(pag_dbs) > 1:
                _logger.warning(
                    f"Several value found for {DELTA_CHAR} / {BETA_CHAR}. Volume reconstruction take one at most."
                )
                timeout = NabuVolumeOW.TIMEOUT if settings.isOnLbsram(scan) else None
                self._dialogDB = _DeltaBetaSelectorDialog(
                    values=pag_dbs, parent=None, timeout=timeout
                )
                self._dialogDB.setModal(False)
                self._callbackDB = functools.partial(
                    self._updateDB, scan, self._dialogDB
                )
                self._dialogDB.accepted.connect(self._callbackDB)
                self._callbackTimeout = functools.partial(self._skipProcessing, scan)
                self._dialogDB.timeoutReached.connect(self._callbackTimeout)
                self._dialogDB.show()
                return

        self._processingStack.add(scan_, self.getConfiguration())

    @docstring(SuperviseOW)
    def reprocess(self, dataset):
        if (
            dataset.axis_params is None
            or dataset.axis_params.relative_cor_value is None
        ):
            # try to retrieve last computed cor value from nabu process
            if dataset.axis_params is None:
                from tomwer.synctools.axis import QAxisRP

                dataset.axis_params = QAxisRP()
            load_reconstruction_parameters_from_cache(scan=dataset)

        self.process(dataset)

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
    def setCluster(self, cluster):
        self._slurmCluster = cluster

    def _updateDB(self, scan, dialog):
        db = dialog.getSelectedValue()
        if db is not None:
            try:
                scan.nabu_recons_params["phase"]["delta_beta"] = (db,)
            except Exception as e:
                logging.error(e)
            else:
                self.process(scan=scan)

    def _endProcessing(self, scan, future_tomo_obj):
        WidgetLongProcessing._endProcessing(self, scan)
        if scan is not None:
            # send scan
            self.Outputs.data.send(scan)
            self.sigScanReady.emit(scan)

            # send volume urls
            volume_urls = []
            for volume_id in scan.latest_vol_reconstructions:
                assert isinstance(volume_id, VolumeIdentifier)
                volume_urls.extend(VolumeFactory.from_identifier_to_vol_urls(volume_id))
            if len(volume_urls) > 0:
                self.Outputs.volume_urls.send(tuple(volume_urls))

            # send volume identifier(s) and associated IcatDataBase objects
            n_rec_volumes = len(scan.latest_vol_reconstructions)
            drac_processed_datasets = []
            if n_rec_volumes > 0:
                if n_rec_volumes > 1:
                    _logger.warning(
                        f"{n_rec_volumes} volume reconstructed when at most one expected"
                    )
                try:
                    volume = VolumeFactory.create_tomo_object_from_identifier(
                        scan.latest_vol_reconstructions[0]
                    )
                except Exception as e:
                    _logger.error(
                        f"Failed to retrieve volume from {volume_id}. Error is {e}"
                    )
                else:
                    self.Outputs.volume.send(volume)

                    icatReconstructedDataset = DracReconstructedVolumeDataset(
                        tomo_obj=volume,
                        source_scan=scan,
                    )
                    drac_processed_datasets.append(icatReconstructedDataset)

            if len(drac_processed_datasets) > 0:
                self.Outputs.data_portal_processed_datasets.send(
                    drac_processed_datasets
                )

        if future_tomo_obj is not None:
            self.Outputs.future_out.send(future_tomo_obj)

    def setDryRun(self, dry_run):
        self._processingStack.setDryRun(dry_run)

    def _ciExec(self):
        self.activateWindow()
        self.raise_()
        self.show()

    def _updateSettingsVals(self):
        self._ewoks_default_inputs = {
            "data": None,
            "nabu_volume_params": self.getConfiguration(),
            "nabu_params": None,
        }

    def _skipProcessing(self, scan):
        self.Outputs.data.send(scan)
        self.sigScanReady.emit(scan)

    def getConfiguration(self):
        config = self._nabuWidget.getConfiguration()
        config["cluster_config"] = self._slurmCluster
        return config

    def setConfiguration(self, config):
        # ignore slurm cluster. Defined by the upper widget
        config.pop("cluster_config", None)
        self._nabuWidget.setConfiguration(config=config)


class _DeltaBetaSelectorDialog(qt.QDialog):
    timeoutReached = qt.Signal()

    def __init__(self, values, parent=None, timeout=None):
        """

        :param values:
        :param parent:
        :param timeout: if a timeout is provided once reach this will
                        automatically reject the delta / beta selection.
                        This is needed when on lbsram to avoid 'locking'
                        a reconstruction. In sec.
        """
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())

        self.mainWidget = _DeltaBetaSelector(parent=self, values=values)
        self.layout().addWidget(self.mainWidget)

        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)
        self._timeout = timeout
        if self._timeout is None:
            self.setWindowTitle(f"Select one value for {DELTA_CHAR} / {BETA_CHAR}")
        else:
            self.setWindowTitle(
                f"Select one value for {DELTA_CHAR} / {BETA_CHAR}. (close automatically in {self._timeout} sec.)"
            )

        # connect signal / slot
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        # expose API
        self.getSelectedValue = self.mainWidget.getSelectedValue

        # add timers
        if timeout is not None:
            self._timer = qt.QTimer()
            self._timer.timeout.connect(self.reject)
            self._timer.start(timeout * 1000)
            self._displayTimer = qt.QTimer()
            self._displayTimer.timeout.connect(self._updateTitle)
            self._displayTimer.start(1000)
        else:
            self._timer = None

    def reject(self):
        if self._timer:
            self._timer.stop()
            self._timer.timeout.disconnect(self.reject)
            self._displayTimer.stop()
            self._displayTimer.timeout.disconnect(self._updateTitle)
            self._timer = None

        qt.QDialog.reject(self)

    def _updateTitle(self):
        self._timeout = self._timeout - 1
        if self._timeout <= 0:
            self.timeoutReached.emit()
            self.reject()
        else:
            self.setWindowTitle(
                f"Select one value for {DELTA_CHAR} / {BETA_CHAR}. (close automatically in {self._timeout} sec.)"
            )
            self._displayTimer.start(1000)


class _DeltaBetaSelector(qt.QTableWidget):
    """Widget used to select a value of delta beta if several provided"""

    def __init__(self, values, parent=None):
        qt.QTableWidget.__init__(self, parent)
        self.setSelectionMode(qt.QAbstractItemView.SingleSelection)
        self.setHorizontalHeaderLabels([DELTA_CHAR + " / " + BETA_CHAR])
        self.setRowCount(0)
        self.setColumnCount(1)
        self.verticalHeader().hide()
        if hasattr(self.horizontalHeader(), "setSectionResizeMode"):  # Qt5
            self.horizontalHeader().setSectionResizeMode(0, qt.QHeaderView.Stretch)
        else:  # Qt4
            self.horizontalHeader().setResizeMode(0, qt.QHeaderView.Stretch)
        self.setAcceptDrops(False)

        # set up
        self.setValues(values=values)

    def setValues(self, values: Iterable):
        self.setHorizontalHeaderLabels([DELTA_CHAR + " / " + BETA_CHAR])
        self.setRowCount(len(values))
        self.setColumnCount(1)
        for i_value, value in enumerate(values):
            _item = qt.QTableWidgetItem()
            _item.setText(str(value))
            _item.setFlags(qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            self.setItem(i_value, 0, _item)
            _item.setSelected(i_value == 0)

    def getSelectedValue(self):
        sel = None
        for item in self.selectedItems():
            sel = item.text()
        return sel
