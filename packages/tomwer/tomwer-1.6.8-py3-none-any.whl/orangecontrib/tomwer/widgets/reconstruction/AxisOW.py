# coding: utf-8
from __future__ import annotations

import copy
import functools
import logging

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output

from processview.core import helpers as pv_helpers
from processview.core.manager import DatasetState
from processview.gui.processmanager import ProcessManager

from silx.gui import qt

import tomwer.core.process.reconstruction.axis
from orangecontrib.tomwer.orange.managedprocess import SuperviseOW
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from tomwer.core import settings
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.core.process.reconstruction.axis import AxisTask
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.process.reconstruction.params_cache import (
    save_reconstruction_parameters_to_cache,
)
from tomwer.core.scan.scanbase import TomwerScanBase, _TomwerBaseDock
from tomwer.gui.reconstruction.axis import AxisMainWindow
from tomwer.synctools.axis import QAxisRP
from tomwer.synctools.stacks.reconstruction.axis import AxisProcessStack

from ..utils import WidgetLongProcessing

logger = logging.getLogger(__name__)


class AxisOW(SuperviseOW, WidgetLongProcessing):
    """
    Widget used to defined the center of rotation axis to be used for a
    reconstruction.

    :param _connect_handler: True if we want to store the modifications
                      on the setting. Need for unit test since
                      keep alive qt widgets.
    """

    name = "center of rotation finder"
    id = "orange.widgets.tomwer.axis"
    description = "use to compute the center of rotation"
    icon = "icons/axis.png"
    priority = 14
    keywords = [
        "tomography",
        "axis",
        "tomwer",
        "reconstruction",
        "rotation",
        "position",
        "center of position",
    ]

    ewokstaskclass = tomwer.core.process.reconstruction.axis.AxisTask

    want_main_area = True
    resizing_enabled = True

    settingsHandler = CallbackSettingsHandler()

    sigScanReady = qt.Signal(TomwerScanBase)
    """Signal emitted when a scan is ready"""

    _ewoks_default_inputs = Setting({"data": None, "axis_params": None, "gui": None})

    class Inputs:
        data = Input(
            name="data",
            type=TomwerScanBase,
            doc="one scan to be process",
            multiple=True,
        )
        data_recompute_axis = Input(
            name="change recons params",
            type=_TomwerBaseDock,
            doc="recompute delta / beta",
        )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")

    def __init__(self, parent=None, axis_params: QAxisRP | None = None):
        """

        :param parent: QWidget parent or None
        :param _connect_handler: used for CI, because if connected fails CI
        :param axis_params: reconstruction parameters
        """
        if axis_params is not None:
            if not isinstance(axis_params, QAxisRP):
                raise TypeError(
                    f"axis_params should be an instance of QAxisRP. Not {type(axis_params)}"
                )
        self._axis_params = axis_params or QAxisRP()

        # handle settings
        #  axis params settings
        axis_params_settings = self._ewoks_default_inputs.get("axis_params", None)
        if axis_params_settings not in (None, dict()):
            try:
                self._axis_params.load_from_dict(axis_params_settings)
            except Exception as e:
                logger.error(f"fail to load reconstruction settings: {e}")

        #  gui settings
        gui_settings = self._ewoks_default_inputs.get("gui", {})
        if gui_settings is None:
            gui_settings = {}

        original_mode = self._axis_params.mode
        if original_mode is AxisMode.manual:
            original_cor = self._axis_params.relative_cor_value
        else:
            original_cor = None

        self.__lastAxisProcessParamsCache = None
        # used to memorize the last (reconstruction parameters, scan)
        self.__scan = None
        self.__skip_exec = False
        self._n_skip = 0
        self._patches = []
        """patches for processing"""

        WidgetLongProcessing.__init__(self)
        SuperviseOW.__init__(self, parent)
        self._processingStack = AxisProcessStack(
            axis_params=self._axis_params, process_id=self.process_id
        )

        self._widget = AxisMainWindow(parent=self, axis_params=self._axis_params)

        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._widget)

        # load settings
        try:
            if "mode_is_lock" in gui_settings:
                mode_lock = gui_settings["mode_is_lock"]
                # if the mode is manual or read ignore lock
                if not (
                    mode_lock is True
                    and self.getMode() in (AxisMode.manual, AxisMode.read)
                ):
                    self._setModeLockFrmSettings(mode_lock)

            if "value_is_lock" in gui_settings:
                if gui_settings["value_is_lock"] is True:
                    self._setValueLockFrmSettings(bool(gui_settings["value_is_lock"]))

            auto_update_estimated_cor = gui_settings.get(
                "auto_update_estimated_cor", True
            )
            self._widget.setAutoUpdateEstimatedCor(auto_update_estimated_cor)
            self._widget.setYAxisInverted(gui_settings.get("y_axis_inverted", False))

        except Exception as e:
            logger.warning(f"Fail to load settings. Error is {str(e)}")

        # expose API
        self._applyBut = self._widget._controlWidget._applyBut
        # connect Signal / Slot
        self._widget.sigComputationRequested.connect(self.__compute)
        self._widget.sigApply.connect(self.__validate)
        self._widget.sigAxisEditionLocked.connect(self.__lockReconsParams)
        self._processingStack.sigComputationStarted.connect(self._processingStart)
        self._processingStack.sigComputationEnded.connect(self._scanProcessed)

        self._axis_params.sigChanged.connect(self._updateSettingsVals)
        self._widget._axisWidget._settingsWidget._mainWidget._calculationWidget.sigUpdateXRotAxisPixelPosOnNewScan.connect(
            self._updateSettingsVals
        )
        self._widget.sigAxisEditionLocked.connect(self._updateSettingsVals)
        self._widget.sigModeChanged.connect(self._updateSettingsVals)
        self._widget.sigLockModeChanged.connect(self._updateSettingsVals)

        self._widget._axisWidget._settingsWidget._mainWidget._calculationWidget._estimatedCorWidget.sigValueChanged.connect(
            self._updateSettingsVals
        )

        # handle special case of the manual mode
        # force axis to manual because not handled by the widget setup directly
        if original_mode in (
            AxisMode.manual,
            AxisMode.read,
        ):
            self._axis_params.mode = original_mode
            if original_cor is not None:
                self._axis_params.set_relative_value(original_cor)

            self.setMode(original_mode)
            # force gui update
            self._widget.sigModeChanged.emit("manual")
            # hard fix, but this widget has to be redone and rework anyway
            self._widget._axisWidget._settingsWidget._mainWidget._calculationWidget._modeChanged()
            if original_cor is not None:
                self._widget._controlWidget._positionInfo.setPosition(
                    relative_cor=original_cor, abs_cor=None
                )

    def __new__(cls, *args, **kwargs):
        # ensure backward compatibility with 'static_input'
        static_input = kwargs.get("stored_settings", {}).get("static_input", None)
        if static_input not in (None, {}):
            logger.warning(
                "static_input has been deprecated. Will be replaced by _ewoks_default_inputs in the workflow file. Please save the workflow to apply modifications"
            )
            kwargs["stored_settings"]["_ewoks_default_inputs"] = static_input
        return super().__new__(cls, *args, **kwargs)

    def _processingStart(self, *args, **kwargs):
        WidgetLongProcessing._startProcessing(self)

    def _scanProcessed(self, scan, future_tomo_obj):
        assert isinstance(scan, TomwerScanBase)
        WidgetLongProcessing._endProcessing(self, scan)
        if self.isValueLock() or self.isModeLocked():
            self.__scan = scan
            self.__validate()
        else:
            pm = ProcessManager()
            # handle previous scan if not validated yey: skip it
            if (
                self.__scan is not None
                and pm.get_dataset_state(dataset=self.__scan, process=self)
                != DatasetState.SUCCEED
            ):
                pm.notify_dataset_state(
                    dataset=self.__scan,
                    process=self,
                    state=DatasetState.SKIPPED,
                    details="Scan was waiting for validation. Has been replaced by another scan. No scan stack on Axis process",
                )

            # handle the new scan
            # retrieve details to keep them in `memory`
            self.__scan = scan
            details = pm.get_dataset_details(dataset=self.__scan, process=self)
            details = "Wait for user validation. " + details
            pm.notify_dataset_state(
                dataset=self.__scan,
                process=self,
                state=DatasetState.WAIT_USER_VALIDATION,
                details=details,
            )
            self.activateWindow()
            self.raise_()
            self.show()

    def __compute(self):
        if self.__scan:
            dict_for_cache = self._axis_params.to_dict().copy()
            dict_for_cache.pop("POSITION_VALUE")
            params_cache = (
                dict_for_cache,
                str(self.__scan),
            )
            # check mode is not locked or manual and value is still here
            if (
                params_cache == self.__lastAxisProcessParamsCache
            ) and self._processingStack.is_computing():
                logger.error(
                    "Parameters and scan are the same as last request. Please wait until the processing is done."
                )
            else:
                self.__lastAxisProcessParamsCache = params_cache
                callback = functools.partial(self._updatePosition, self.__scan)
                self._processingStack.add(
                    data=self.__scan,
                    configuration=self._axis_params.to_dict(),
                    callback=callback,
                )

    def __validate(self):
        """Validate the current scan and move the scan to the next process.
        The Axis will process the next scan in the stack.
        """
        if self.__scan:
            if self.getMode() is AxisMode.manual:
                # when value is set from manual mode we need to retrieve it from the GUI `_axis_param`. Else it has already been set
                # to the scan `_axis_params`
                if (
                    self.__scan._axis_params.frame_width is None
                    and self.__scan.dim_1 is not None
                ):
                    self.__scan._axis_params.frame_width = self.__scan.dim_1

                self.__scan._axis_params.set_relative_value(
                    self._axis_params.relative_cor_value
                )
                relative_cor_value = self.__scan.axis_params.relative_cor_value
                save_reconstruction_parameters_to_cache(scan=self.__scan)
                pv_helpers.notify_succeed(
                    process=self,
                    dataset=self.__scan,
                    details=f"axis calculation defined for {self.__scan.path}: {relative_cor_value} (using manual)",
                )
            # validate the center of rotation
            pm = ProcessManager()
            # retrieve details to keep them in memory
            details = pm.get_dataset_details(dataset=self.__scan, process=self)
            state = pm.get_dataset_state(dataset=self.__scan, process=self)
            if state in (DatasetState.ON_GOING, DatasetState.WAIT_USER_VALIDATION):
                # update the state to SUCCEED
                ProcessManager().notify_dataset_state(
                    dataset=self.__scan,
                    process=self,
                    state=DatasetState.SUCCEED,
                    details=details,
                )
            self.accept()
            self.scan_ready(scan=self.__scan)
        self.hide()

    def __lockReconsParams(self, lock):
        self.lock_position_value(lock)

    def scan_ready(self, scan):
        assert isinstance(scan, TomwerScanBase)
        self.Outputs.data.send(scan)
        self.sigScanReady.emit(scan)

    def _informNoProjFound(self, scan):
        msg = qt.QMessageBox(self)
        msg.setIcon(qt.QMessageBox.Warning)
        text = (
            "Unable to find url to compute the axis of `%s`" % scan.path
            or "no path given"
        )
        text += ", please select them from the `axis input` tab"
        msg.setText(text)
        msg.exec()

    def _updateSettingsVals(self):
        # remove rp setting to the advantage of 'static_input'
        self._ewoks_default_inputs = {
            "data": None,
            "axis_params": self._axis_params.to_dict(),
            "gui": {
                "mode_is_lock": self.isModeLocked(),
                "value_is_lock": self.isValueLock(),
                "auto_update_estimated_cor": self._widget.getAutoUpdateEstimatedCor(),
                "y_axis_inverted": self._widget.isYAxisInverted(),
            },
        }

    def _skip_exec(self, b):
        """util function used for unit test. If activate, skip the call to
        self.exec() in process"""
        self.__skip_exec = b

    @property
    def recons_params(self):
        return self._axis_params

    def _lock_axis_controls(self, lock):
        """

        :param lock: lock the axis controls to avoid modification of the
                          requested options, method... of the axis calculation
                          when this value is under calculation.
        """
        self._widget.setLocked(lock)

    def isValueLock(self):
        """
        Check if the cor value has been lock. If so we simply copy the cor
        value and move to the next scan
        """
        return self._widget.isValueLock()

    def isModeLocked(self):
        """
        Check if the mode has been lock or not. If lock then call the
        algorithm and does not wait for any user feedback
        """
        return self._widget.isModeLock()

    @Inputs.data
    def new_data_in(self, scan, *args, **kwargs):
        if scan is None:
            return
        scan_ = copy.copy(scan)
        if not (
            settings.isOnLbsram(scan) and is_low_on_memory(settings.get_lbsram_path())
        ):
            set_position = False  # avoid shift reset
            self._widget.setScan(scan=scan_, set_position=set_position)
        elif scan_.axis_params is None:
            scan_.axis_params = QAxisRP()
        self.process(scan=scan_)

    def process(self, scan):
        if scan is None:
            return
        self.__scan = scan
        self._axis_params.frame_width = scan.dim_1
        if (
            settings.isOnLbsram(scan)
            and is_low_on_memory(settings.get_lbsram_path()) is True
        ):
            self._updatePosition(scan=scan)
            self.scan_ready(scan=scan)
        elif self.__skip_exec:
            self._n_skip += 1
            if self.isValueLock():
                scan._axis_params.set_relative_value(
                    self._axis_params.relative_cor_value
                )
                cor = scan._axis_params.relative_cor_value
                save_reconstruction_parameters_to_cache(scan=scan)
                ap = AxisTask(
                    process_id=self.process_id,
                    inputs={
                        "data": None,
                    },
                )
                ProcessManager().notify_dataset_state(
                    dataset=scan,
                    process=ap,
                    state=DatasetState.SUCCEED,
                )
            else:
                processing_class = AxisTask(
                    inputs={
                        "axis_params": self._axis_params,
                        "data": self.__scan,
                        "serialize_output_data": False,
                    }
                )
                processing_class.run()
            self._updatePosition(scan=self.__scan)
            if self.isModeLocked() or self.isValueLock():
                self.scan_ready(scan=scan)

        elif self.isValueLock():
            cor = self._axis_params.relative_cor_value
            scan.axis_params.set_relative_value(cor)
            save_reconstruction_parameters_to_cache(scan=scan)
            scan._axis_params.mode = "manual"
            ProcessManager().notify_dataset_state(
                dataset=scan,
                process=AxisTask(
                    process_id=self.process_id,
                    inputs={
                        "data": None,
                        "serialize_output_data": False,
                    },
                ),
                state=DatasetState.SUCCEED,
            )
            self.scan_ready(scan=scan)

        elif self.isModeLocked():
            callback = functools.partial(self._updatePosition, scan)
            self._processingStack.add(
                data=scan, configuration=self._axis_params.to_dict(), callback=callback
            )
        else:
            self.activateWindow()
            self.raise_()
            self.show()

    def _updatePosition(self, scan):
        if scan.axis_params is not None:
            self._widget.setPosition(relative_value=scan.axis_params.relative_cor_value)

    @Inputs.data_recompute_axis
    def reprocess(self, scan):
        """Recompute the axis for scan"""
        if scan is not None:
            # for now The behavior for reprocessing is the sama as for processing
            if hasattr(scan, "instance"):
                self.process(scan.instance)
            else:
                self.process(scan)

    def close(self):
        self._processingStack.stop()
        self._processingStack.wait_computation_finished()
        self._widget = None
        self._processingStack = None
        super().close()

    def patch_calc_method(self, mode, function):
        self._patches.append((mode, function))

    def keyPressEvent(self, event):
        """The event has to be filtered since we have some children
        that can be edited using the 'enter' key as defining the cor manually
        (see #481)). As we are in a dialog this automatically trigger
        'accepted'. See https://forum.qt.io/topic/5080/preventing-enter-key-from-triggering-ok-in-qbuttonbox-in-particular-qlineedit-qbuttonbox/5
        """
        if event.key() != qt.Qt.Key_Enter:
            super().keyPressEvent(event)

    # expose API
    def setMode(self, mode):
        self._widget.setMode(mode=mode)

    def getMode(self):
        return self._widget.getMode()

    def getEstimatedCor(self):
        return self._widget.getEstimatedCor()

    def setEstimatedCor(self, value):
        self._widget.setEstimatedCor(value=value)

    def getAxisParams(self):
        return self._widget.getAxisParams()

    def setValueLock(self, lock: bool):
        self._widget.setValueLock(lock=lock)

    def _setModeLockFrmSettings(self, lock: bool):
        self._widget._setModeLockFrmSettings(lock=lock)

    def _setValueLockFrmSettings(self, lock: bool):
        self._widget._setValueLockFrmSettings(lock=lock)
