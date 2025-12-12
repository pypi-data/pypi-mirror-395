# coding: utf-8

"""
This module is dedicated to cast of volume from one file format to the other.
"""
from __future__ import annotations


import logging
import os

import numpy
import pathlib

from nabu.io.cast_volume import RESCALE_MAX_PERCENTILE, RESCALE_MIN_PERCENTILE
from nabu.io.cast_volume import cast_volume as _nabu_cast_volume
from nabu.io.cast_volume import get_default_output_volume
from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from sluurp.executor import submit as submit_to_slurm_cluster
from sluurp.job import SBatchScriptJob
from tomoscan.volumebase import VolumeBase
from tomoscan.utils.io import filter_esrf_mounting_points

from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.process.reconstruction.nabu import settings
from tomwer.core.process.output import NabuOutputFileFormat
from tomwer.core.process.reconstruction.nabu.utils import (
    get_default_output_volume_for_tiff_3d,
)
from tomwer.core.process.task import Task
from tomwer.core.utils.scanutils import (
    format_output_location as format_scan_output_location,
)
from tomwer.core.utils.slurm import get_slurm_script_name
from tomwer.core.utils.volumeutils import volume_identifier_to_volume
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.process.drac.processeddataset import (
    DracReconstructedVolumeDataset,
)

_logger = logging.getLogger(__name__)

CAST_VOLUME_WORKING_SUB_DIRECTORY = "cast_volume"

DEFAULT_OUTPUT_DIR = (
    "{volume_data_parent_folder}" f"/{CAST_VOLUME_WORKING_SUB_DIRECTORY}"
)


class CastVolumeTask(
    Task,
    SuperviseProcess,
    input_names=(
        "volume",
        "configuration",
    ),
    optional_input_names=("scan", "output_volume"),
    output_names=(
        "volume",
        "future_tomo_obj",
        "data_portal_processed_datasets",
    ),
):
    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        SuperviseProcess.__init__(self, process_id=process_id)
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        self._cluster_config = None

    def run(self):
        input_volume = volume_identifier_to_volume(self.inputs.volume)
        if not isinstance(input_volume, VolumeBase):
            raise TypeError(
                f"input_volume is a {type(input_volume)} when {VolumeBase} expected"
            )
        configuration = self.inputs.configuration
        self._cluster_config = configuration.pop("cluster_config", None)
        if isinstance(self._cluster_config, SlurmClusterConfiguration):
            self._cluster_config = self._cluster_config.to_dict()

        if self.inputs.scan:
            scan = self.inputs.scan
        else:
            scan = None

        if self.inputs.output_volume:
            output_volume = self.inputs.output_volume
            if not isinstance(output_volume, TomwerVolumeBase):
                output_volume = VolumeFactory.create_tomo_object_from_identifier(
                    output_volume
                )
        else:
            output_file_format = configuration.get(
                "output_file_format", None
            )  # expects values like hdf5, edf ...
            output_dir = configuration.get("output_dir", None)
            if output_file_format is None or output_dir is None:
                mess = "'output_volume' or ('output_file_format' and 'output_dir' from configuration) should be provided."
                _logger.processFailed(f"volume cast of {str(input_volume)} failed")
                ProcessManager().notify_dataset_state(
                    dataset=scan or input_volume,
                    process=self,
                    state=DatasetState.FAILED,
                )
                raise ValueError(mess)

            try:
                output_dir = TomwerVolumeBase.format_output_location(
                    location=output_dir,
                    volume=input_volume,
                )
            except KeyError:
                pass

            if scan:
                try:
                    output_dir = format_scan_output_location(
                        location=output_dir,
                        scan=scan,
                    )
                except KeyError:
                    pass
            output_file_format = NabuOutputFileFormat.from_value(output_file_format)
            if output_file_format is NabuOutputFileFormat.TIFF_3D:
                output_volume = get_default_output_volume_for_tiff_3d(
                    input_volume=input_volume,
                    output_dir=output_dir,
                )
            else:
                output_volume = get_default_output_volume(
                    input_volume=input_volume,
                    output_type=output_file_format.value,
                    output_dir=output_dir,
                )
            # convert from tomoscan volume to tomwer volume
            output_volume = VolumeFactory.create_tomo_object_from_identifier(
                output_volume.get_identifier().to_str()
            )

        # build output volume object
        overwrite = configuration.get("overwrite", False)
        remove_input_volume = configuration.get("remove_input_volume", False)
        output_volume.overwrite = overwrite
        cratios = configuration.get("compression_ratios", None)
        if cratios is not None:
            output_volume.cratios = cratios

        output_data_type = numpy.dtype(
            configuration.get("output_data_type")
        )  # expects values like numpy uint8, unint16...

        rescale_min_percentile = configuration.get(
            "rescale_min_percentile", RESCALE_MIN_PERCENTILE
        )
        rescale_max_percentile = configuration.get(
            "rescale_max_percentile", RESCALE_MAX_PERCENTILE
        )
        data_min = configuration.get("data_min", None)
        data_max = configuration.get("data_max", None)

        # run volume cast locally
        if self._cluster_config is None:
            try:
                _nabu_cast_volume(
                    input_volume=input_volume,
                    output_volume=output_volume,
                    output_data_type=output_data_type,
                    data_min=data_min,
                    data_max=data_max,
                    scan=scan,
                    rescale_min_percentile=rescale_min_percentile,
                    rescale_max_percentile=rescale_max_percentile,
                    save=True,
                    store=False,
                    remove_input_volume=remove_input_volume,
                )
            except Exception as e:
                mess = f"volume cast of {str(input_volume)} failed. Reason is {str(e)}"
                _logger.processFailed(mess)
                state = DatasetState.FAILED
            else:
                mess = f"volume cast of {str(input_volume)} succeed"
                _logger.processSucceed(mess)
                state = DatasetState.SUCCEED

            ProcessManager().notify_dataset_state(
                dataset=scan or input_volume,
                process=self,
                state=state,
                details=mess,
            )
            self.outputs.future_tomo_obj = None
            self.outputs.volume = output_volume
            if scan is not None:
                scan.cast_volume = output_volume.get_identifier()
            else:
                input_volume.cast_volume = output_volume.get_identifier()
            self.outputs.data_portal_processed_datasets = tuple()
        # run volume cast remotely
        else:

            def get_command():
                command = f"python3 -m {settings.NABU_CAST_APP_PATH} '{input_volume.get_identifier().to_str()}'"
                command += (
                    f" --output_volume='{output_volume.get_identifier().to_str()}'"
                )
                if overwrite:
                    command += " --overwrite"
                command += f" --output-data-type={str(output_data_type)}"
                if data_min is not None:
                    command += f" --data_min={data_min}"
                if data_max is not None:
                    command += f" --data_max={data_max}"
                if rescale_min_percentile is not None:
                    command += f" --rescale_min_percentile={rescale_min_percentile}"
                if rescale_max_percentile is not None:
                    command += f" --rescale_max_percentile={rescale_max_percentile}"
                if remove_input_volume:
                    command += " --remove-input-volume"
                return command

            script_name = get_slurm_script_name(prefix="nabu_cast")
            if scan is not None:
                working_directory = scan.working_directory.resolve()
                script_path = os.path.join(
                    scan.resolved_path, "slurm_scripts", script_name
                )
            else:
                working_directory = os.path.dirname(input_volume.data_url.file_path())
                working_directory = str(pathlib.Path(working_directory).resolve())
                script_path = os.path.join(
                    working_directory, "slurm_scripts", script_name
                )
            # for now force job name
            self._cluster_config["job_name"] = (
                f"tomwer-cast-volume {input_volume.get_identifier().to_str()} to {output_volume.get_identifier().to_str()}"
            )
            job = SBatchScriptJob(
                slurm_config=self._cluster_config,
                script=(get_command(),),
                script_path=filter_esrf_mounting_points(script_path),
                clean_script=False,
                working_directory=filter_esrf_mounting_points(working_directory),
            )
            future_slurm_job = submit_to_slurm_cluster(job)
            if scan is not None:
                future_obj = scan
            else:
                future_obj = output_volume
            self.outputs.future_tomo_obj = FutureTomwerObject(
                tomo_obj=future_obj,
                futures=(future_slurm_job,),
                process_requester_id=self.process_id,
            )
            self.outputs.volume = output_volume

            if scan is not None:
                drac_reconstructed_dataset = DracReconstructedVolumeDataset(
                    tomo_obj=output_volume,
                    source_scan=scan,
                )
                self.outputs.data_portal_processed_datasets = (
                    drac_reconstructed_dataset,
                )
            # for now at the task level we consider this is succeed if it has been submitted
            ProcessManager().notify_dataset_state(
                dataset=scan or input_volume,
                process=self,
                state=DatasetState.SUCCEED,
                details="cast has been correctly submitted to slurm",
            )
