# from __future__ import annotations

# import logging

# from orangewidget import gui
# from orangewidget.settings import Setting
# from orangewidget.widget import Input, Output
# from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack
# from silx.gui import qt
# from typing import Optional

# from tomwer.core.futureobject import FutureTomwerObject
# from tomwer.core.scan.scanbase import TomwerScanBase
# from tomwer.gui.reconstruction.nabu.helical import HelicalPrepareWeightsDouble
# from tomwer.core.process.reconstruction.nabu.helical import (
#     NabuHelicalPrepareWeightsDouble,
# )
# from tomwer.core.scan.nxtomoscan import NXtomoScan

# _logger = logging.getLogger(__name__)


# class NabuHelicalPrepareWeightsDoubleOW(
#     TomwerWithStackStack,
#     ewokstaskclass=NabuHelicalPrepareWeightsDouble,
# ):
#     """
#     widget used to call the `nabu-helical-prepare-weights-double` application on a dedicated thread. It define weights map and double flat field.

#     :param parent: the parent widget
#     """

#     # note of this widget should be the one registered on the documentation
#     name = "helical prerate weights double"
#     id = "orangecontrib.tomwer.widgets.reconstruction.NabuHelicalPrepareWeightsDoubleOW.NabuHelicalPrepareWeightsDoubleOW"
#     description = "compute map of weights requested for nabu helical reconstruction"
#     icon = "icons/nabu_prepare_weights_double.svg"
#     priority = 199
#     keywords = [
#         "tomography",
#         "nabu",
#         "reconstruction",
#         "nabu-helical",
#         "helical",
#         "weights",
#         "prepare",
#     ]

#     want_main_area = True
#     want_control_area = False
#     resizing_enabled = True

#     _ewoks_default_inputs = Setting(
#         {
#             "data": None,
#             "transition_width_vertical": 50,
#             "transition_width_horizontal": 50,
#             "processes_file": "",
#             "rotation_axis_position": 0,
#         }
#     )

#     _ewoks_inputs_to_hide_from_orange = (
#         "progress",
#         "processes_file",
#         "transition_width_vertical",
#         "transition_width_horizontal",
#         "rotation_axis_position",
#     )

#     sigScanReady = qt.Signal(TomwerScanBase)
#     "Signal emitted when a scan is ended"

#     TIMEOUT = 30

#     class Inputs:
#         data = Input(
#             name="data",
#             type=TomwerScanBase,
#             doc="one scan to be process",
#             default=True,
#             multiple=False,
#         )

#     class Outputs:
#         data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")
#         future_tomo_obj = Output(
#             name="future_tomo_obj",
#             type=FutureTomwerObject,
#             doc="future object (process remotely)",
#         )

#     LOGGER = _logger

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.__scan = None

#         # gui definition
#         _layout = gui.vBox(self.mainArea, self.name).layout()
#         self.widget = HelicalPrepareWeightsDouble(parent=self)
#         _layout.addWidget(self.widget)

#         ## connect signal / slot
#         self.widget.sigConfigChanged.connect(self._updateSettings)

#         if isinstance(self.task_output_changed_callbacks, set):
#             self.task_output_changed_callbacks.add(self._notify_state)
#         elif isinstance(self.task_output_changed_callbacks, list):
#             self.task_output_changed_callbacks.append(self._notify_state)
#         else:
#             raise NotImplementedError

#         ## handle settings
#         self._loadSettings()
#         self.task_executor_queue.sigComputationStarted.connect(self._newTaskStarted)

#     def _updateSettings(self):
#         config = self.widget.getConfiguration()
#         for key in ("transition_width", "processes_file"):
#             self._ewoks_default_inputs[key] = config[key]  # pylint: disable=E1137

#     @property
#     def request_input(self):
#         return self.__request_input

#     @request_input.setter
#     def request_input(self, request):
#         self.__request_input = request

#     def get_task_inputs(self):
#         assert self.__scan is not None
#         return {
#             "data": self.__scan,
#             "transition_width": self.widget.getConfiguration()["transition_width"],
#             "processes_file": self.widget.getConfiguration()["processes_file"],
#         }

#     def handleNewSignals(self) -> None:
#         """Invoked by the workflow signal propagation manager after all
#         signals handlers have been called.
#         """
#         # for now we want to avoid propagation any processing.
#         # task will be executed only when the user validates the dialog
#         data = super().get_task_inputs().get("data", None)
#         if data is not None:
#             if not isinstance(data, NXtomoScan):
#                 raise TypeError(
#                     f"data is expected to be an instance of NXtomoScan. {type(data)} are not handled"
#                 )
#             self.add(data.path)

#     def _loadSettings(self):
#         self.widget.setConfiguration(self._ewoks_default_inputs)

#     def _newTaskStarted(self):
#         try:
#             task_executor = self.sender()
#             scan = task_executor.current_task.inputs.data
#             self.notify_on_going(scan)
#         except Exception:
#             pass

# def _notify_state(self):
#     try:
#         task_executor = self.sender()
#         task_suceeded = task_executor.succeeded
#         scan = task_executor.current_task.outputs.data
#         if task_suceeded:
#             self.notify_succeed(scan=scan)
#         else:
#             self.notify_failed(scan=scan)
#     except Exception as e:
#         _logger.error(f"failed to handle task finished callback. Reason is {e}")

# @Inputs.data
# def process_data(self, scan: TomwerScanBase | None):
#     if scan is None:
#         return
#     else:
#         self.__scan = scan
#         self.notify_pending(scan=scan)
#         self.execute_ewoks_task()

#     def sizeHint(self) -> qt.QSize:
#         return qt.QSize(650, 60)
