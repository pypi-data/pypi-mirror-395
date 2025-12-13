# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "14/10/2021"


import time

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output, OWBaseWidget
from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt
from silx.gui.utils.concurrent import submitToQtMainThread

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.gui.cluster.supervisor import (
    FutureTomwerScanObserverWidget as _FutureTomwerScanObserverWidget,
)
from tomwer.core.process.drac.processeddataset import DracReconstructedVolumeDataset
from tomwer.core.volume.volumefactory import VolumeFactory


class FutureSupervisorOW(OWBaseWidget, openclass=True):
    """
    Orange widget to define a slurm cluster as input of other
    widgets (based on nabu for now)
    """

    name = "future supervisor"
    id = "orange.widgets.tomwer.cluster.FutureSupervisorOW.FutureSupervisorOW"
    description = "Observe slurm job registered."
    icon = "icons/slurmobserver.svg"
    priority = 22
    keywords = [
        "tomography",
        "tomwer",
        "slurm",
        "observer",
        "cluster",
        "job",
        "sbatch",
        "supervisor",
        "future",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _ewoks_default_inputs = Setting(dict())

    class Inputs:
        future_in = Input(
            name="future_tomo_obj",
            type=FutureTomwerObject,
            doc="data with some remote processing",
            multiple=True,
            default=True,
        )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase)
        volume = Output(name="volume", type=TomwerVolumeBase)
        data_portal_processed_datasets = Output(
            name="data_portal_processed_datasets",
            type=tuple,
            doc="data portal processed data to be saved",
        )

    def __init__(self, parent=None):
        super().__init__(parent)
        # gui
        layout = gui.vBox(self.mainArea, self.name).layout()
        self._widget = FutureTomwerObjectObserverWidget(
            parent=self, name=self.windowTitle()
        )
        layout.addWidget(self._widget)

        # connect signal / slot
        self._widget.observationTable.model().sigStatusUpdated.connect(
            self._convertBackAutomatically
        )
        self._widget.sigConversionRequested.connect(self._convertBack)

    def convertWhenFinished(self):
        return self._widget.convertWhenFinished()

    def _convertBackAutomatically(self, future_tomo_obj, status):
        if not isinstance(future_tomo_obj, FutureTomwerObject):
            raise TypeError(
                f"future_tomo_obj is expected to be an instance of {FutureTomwerObject} and not {type(future_tomo_obj)}"
            )
        if status in ("finished", "completed") and self.convertWhenFinished():
            self._convertBack(future_tomo_obj)

    def _convertBack(self, future_tomo_obj):
        if not isinstance(future_tomo_obj, FutureTomwerObject):
            raise TypeError(
                f"future_tomo_obj is expected to be an instance of {FutureTomwerObject} and not {type(future_tomo_obj)}"
            )
        self._futureHasBeenConverted(future_tomo_obj, future_tomo_obj.tomo_obj)

    @Inputs.future_in
    def add(self, future_tomo_obj, signal_id=None):
        if future_tomo_obj is not None:
            self._widget.addFutureTomoObj(future_tomo_obj=future_tomo_obj)

    def _futureHasBeenConverted(self, future_tomo_obj, tomo_obj):
        # clean client to free resources
        self._widget.removeFutureTomoObj(future_tomo_obj=future_tomo_obj)
        if tomo_obj is not None:
            if isinstance(tomo_obj, TomwerScanBase):
                self.Outputs.data.send(tomo_obj)

                def build_drac_dataset(vol_id):
                    volume = VolumeFactory.create_tomo_object_from_identifier(vol_id)
                    return DracReconstructedVolumeDataset(
                        tomo_obj=volume,
                        source_scan=tomo_obj,
                    )

                self.Outputs.data_portal_processed_datasets.send(
                    tuple(
                        [
                            build_drac_dataset(vol_id=vol_id)
                            for vol_id in tomo_obj.latest_vol_reconstructions
                        ]
                    )
                )

                if len(tomo_obj.latest_vol_reconstructions) > 0:
                    rec_volume = VolumeFactory.create_tomo_object_from_identifier(
                        tomo_obj.latest_vol_reconstructions[0]
                    )
                    self.Outputs.volume.send(rec_volume)

            elif isinstance(tomo_obj, TomwerVolumeBase):
                self.Outputs.volume.send(tomo_obj)


class FutureTomwerObjectObserverWidget(
    _FutureTomwerScanObserverWidget, SuperviseProcess
):
    """add dataset state notification (ProcessManager) to the original FutureTomwerScanObserverWidget"""

    REFRESH_FREQUENCE = 10
    """time between call to updateView"""

    def __init__(self, name, parent=None):
        super().__init__(parent=parent)
        self.name = name
        self._updateThread = _RefreshThread(
            callback=self.updateView, refresh_frequence=self.REFRESH_FREQUENCE
        )
        self.destroyed.connect(self.stopRefresh)
        self._updateThread.start()

    def stopRefresh(self):
        if self._updateThread is not None:
            self._updateThread.stop()
            self._updateThread.wait(self.REFRESH_FREQUENCE + 1)
            self._updateThread = None

    def close(self):
        self.stopRefresh()
        super().close()

    def addFutureTomoObj(self, future_tomo_obj: FutureTomwerObject):
        super().addFutureTomoObj(future_tomo_obj)
        self._updateTomoObjSupervisor(future_tomo_obj)

    def removeFutureTomoObj(self, future_tomo_obj: FutureTomwerObject):
        self._updateTomoObjSupervisor(future_tomo_obj)
        super().removeFutureTomoObj(future_tomo_obj)

    def _updateTomoObjSupervisor(self, future_tomo_obj):
        r_id = future_tomo_obj.process_requester_id
        if r_id is not None:
            requester_name = ProcessManager().get_process(r_id).name
        else:
            requester_name = "unknow"
        details = f"job spawn by {requester_name}"
        if future_tomo_obj is None:
            return
        elif future_tomo_obj.status == "error":
            state = DatasetState.FAILED
            if future_tomo_obj.job_id is None:
                details = "Job submission to Slurm has failed. This is likely due to an invalid configuration request, such as requesting a GPU on a partition that does not support GPUs. Please review your configuration and try again."
        elif future_tomo_obj.status == "pending":
            details = "\n".join([details, "pending"])
            state = DatasetState.PENDING
        elif future_tomo_obj.status in ("finished", "completed"):
            details = future_tomo_obj.logs or "no log found"
            state = DatasetState.SUCCEED
        elif future_tomo_obj.status == "running":
            details = "\n".join([details, "running"])
            state = DatasetState.ON_GOING
        elif future_tomo_obj.status == "cancelled":
            details = "\n".join([details, "job cancelled"])
            state = DatasetState.SKIPPED
        elif future_tomo_obj.status is None:
            return
        else:
            raise ValueError(
                f"future scan status '{future_tomo_obj.status}' is not managed, {type(future_tomo_obj.status)}"
            )
        ProcessManager().notify_dataset_state(
            dataset=future_tomo_obj.tomo_obj,
            process=self,
            state=state,
            details=details,
        )

    def _updateStatus(self, future_tomo_obj):
        self._updateTomoObjSupervisor(future_tomo_obj)
        super()._updateStatus(future_tomo_obj)


class _RefreshThread(qt.QThread):
    """Simple thread to call a refresh callback each refresh_frequence (seconds)"""

    TIME_BETWEEN_LOOP = 1.0

    def __init__(self, callback, refresh_frequence) -> None:
        super().__init__()
        self._callback = callback
        self._refresh_frequence = refresh_frequence
        self._stop = False

    def stop(self):
        self._stop = True
        self._callback = None

    def run(self):
        w_t = self._refresh_frequence + self.TIME_BETWEEN_LOOP

        while not self._stop:
            if w_t <= 0:
                if self._callback is not None:
                    try:
                        submitToQtMainThread(self._callback)
                    except AttributeError:
                        # can happen when closing
                        pass
                w_t = self._refresh_frequence + self.TIME_BETWEEN_LOOP
            w_t -= self.TIME_BETWEEN_LOOP
            time.sleep(self.TIME_BETWEEN_LOOP)
