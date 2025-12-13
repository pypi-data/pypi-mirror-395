# coding: utf-8
"""module containing FutureSupervisorTask."""

from typing import Iterable

from ewokscore.task import Task as EwoksTask
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.process.drac.processeddataset import DracReconstructedVolumeDataset
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory


class FutureSupervisorTask(
    EwoksTask,
    input_names=("future_tomo_obj",),
    output_names=("data", "volume", "data_portal_processed_datasets"),
):
    """
    Task used to wait for a 'FutureTomwerObject' and convert it to original instance of:

    * TomwerScanBase (data): if the FutureTomwerObject is based on a scan instance
    * TomwerVolumeBase (volume): if the FutureTomwerObject is based on a volume instance
    * tuple of IcatReconstructedVolumeDataset (data_portal_processed_datasets): if the FutureTomwerObject is based on a volume instance
    """

    def run(self):
        future_tomo_obj = self.inputs.future_tomo_obj
        if not isinstance(future_tomo_obj, FutureTomwerObject):
            raise TypeError(
                f"future_data is expected to be an instance of {FutureTomwerObject}. Got {type(future_tomo_obj)}"
            )
        future_tomo_obj.results()

        tomo_obj = future_tomo_obj.tomo_obj

        if isinstance(tomo_obj, TomwerScanBase):
            self.outputs.data = tomo_obj

            # the volume reconstruction return an instance of 'FutureTomwerObj' with a scan.
            # so to make drac publication compatible with it we also need to send the 'data_portal_processed_datasets'
            def build_drac_dataset(vol_id):
                volume = VolumeFactory.create_tomo_object_from_identifier(vol_id)
                return DracReconstructedVolumeDataset(
                    tomo_obj=volume,
                    source_scan=tomo_obj,
                )

            assert isinstance(tomo_obj.latest_vol_reconstructions, Iterable)
            self.outputs.data_portal_processed_datasets = tuple(
                [
                    build_drac_dataset(vol_id=vol_id)
                    for vol_id in tomo_obj.latest_vol_reconstructions
                ]
            )
            if len(tomo_obj.latest_vol_reconstructions) > 0:
                # at the moment we expect at most one volume from a scan.
                # If it changes we will need to replace `volume` by `volumes`
                self.outputs.volume = VolumeFactory.create_tomo_object_from_identifier(
                    tomo_obj.latest_vol_reconstructions[0]
                )
            else:
                self.outputs.volume = None
        elif isinstance(tomo_obj, TomwerVolumeBase):
            self.outputs.volume = tomo_obj
            self.outputs.data_portal_processed_datasets = ()
            self.outputs.data = None
