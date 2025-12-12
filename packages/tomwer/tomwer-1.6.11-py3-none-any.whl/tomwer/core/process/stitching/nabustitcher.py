import logging

from tqdm import tqdm
from ewokscore.missing_data import is_missing_data

from sluurp.executor import submit as submit_to_slurm_cluster

from nabu.stitching.config import (
    dict_to_config_obj,
    PreProcessedZStitchingConfiguration,
    PostProcessedZStitchingConfiguration,
    SlurmConfig,
    StitchingConfiguration,
    StitchingType,
)
from nabu.stitching.z_stitching import z_stitching
from nabu.stitching.y_stitching import y_stitching

from nabu.stitching.utils.post_processing import (
    StitchingPostProcAggregation as _StitchingPostProcAggregation,
)
from nabu.stitching.slurm_utils import split_stitching_configuration_to_slurm_job

from processview.core.superviseprocess import SuperviseProcess

from tomwer.core.process.task import Task
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.volume.volumefactory import VolumeFactory


_logger = logging.getLogger(__name__)


class StitcherTask(
    Task,
    SuperviseProcess,
    input_names=("stitching_config",),
    optional_input_names=(
        "cluster_config",
        "progress",
        "serialize_output_data",
    ),
    output_names=(
        "data",
        "future_tomo_obj",
        "volume",
    ),
):
    def __init__(self, process_id=None, *args, **kwargs):
        SuperviseProcess.__init__(self, process_id=process_id)
        super().__init__(*args, **kwargs)

    def run(self):
        cluster_config = self.inputs.cluster_config
        assert cluster_config is None or isinstance(cluster_config, dict)
        stitching_config = self.inputs.stitching_config
        assert isinstance(stitching_config, dict)

        config = dict_to_config_obj(stitching_config)
        config.slurm_config = SlurmConfig.from_dict(cluster_config)
        if cluster_config in ({}, None):
            # opt1: run locally
            config.slurm_config = SlurmConfig.from_dict(cluster_config)

            progress = (
                None if is_missing_data(self.inputs.progress) else self.inputs.progress
            )

            if config.stitching_type in (
                StitchingType.Z_PREPROC,
                StitchingType.Y_PREPROC,
            ):
                if config.stitching_type is StitchingType.Z_PREPROC:
                    stitched_identifier = z_stitching(
                        configuration=config, progress=progress
                    )
                else:
                    stitched_identifier = y_stitching(
                        configuration=config, progress=progress
                    )

                nx_tomo = ScanFactory.create_tomo_object_from_identifier(
                    stitched_identifier.to_str()
                )
                if self.get_input_value("serialize_output_data", True):
                    self.outputs.data = nx_tomo.to_dict()
                else:
                    self.outputs.data = nx_tomo
                self.outputs.volume = None
                self.outputs.future_tomo_obj = None
            elif config.stitching_type is StitchingType.Z_POSTPROC:
                stitched_identifier = z_stitching(
                    configuration=config, progress=progress
                )
                volume = VolumeFactory.create_tomo_object_from_identifier(
                    stitched_identifier.to_str()
                )
                self.outputs.volume = volume
                self.outputs.data = None
                self.outputs.future_tomo_obj = None
            else:
                raise NotImplementedError()
        else:
            # opt2: run remotely and aggregate locally
            futures = {}

            # 2.1 launch jobs
            # TODO: refactor: nabu.app.stitching could be called or something like that...
            slurm_job_progress_bars: dict = {}
            for i_job, (job, sub_config) in enumerate(
                split_stitching_configuration_to_slurm_job(
                    config, yield_configuration=True
                )
            ):
                _logger.info(f"submit job nb {i_job}: handles {sub_config.slices}")
                output_tomo_obj = (
                    sub_config.get_output_object().get_identifier().to_str()
                )
                futures[output_tomo_obj] = submit_to_slurm_cluster(job, timeout=999999)
                # note on total=100: we only consider percentage in this case (providing advancement from slurm jobs)
                slurm_job_progress_bars[job] = tqdm(
                    total=100,
                    position=i_job + 1,
                    desc=f"   part {str(i_job).ljust(3)}",
                    delay=0.5,  # avoid to mess with terminal and (near) future logs
                    bar_format="{l_bar}{bar}",  # avoid using 'r_bar' as 'total' is set to 100 (percentage)
                    leave=False,
                )

            # handle post processing
            data_aggregation = StitchingPostProcAggregation(
                futures=futures,
                stitching_config=config,
                progress_bars=slurm_job_progress_bars,
            )
            # will wait and provide feedback until the stitching is completed.
            data_aggregation.process()

            if config.stitching_type is StitchingType.Z_PREPROC:
                output_nx_tomo_file = config.output_file_path
                output_nx_tomo_entry = config.output_data_path
                self.outputs.data = NXtomoScan(
                    scan=output_nx_tomo_file, entry=output_nx_tomo_entry
                )
                self.outputs.future_tomo_obj = None
                self.outputs.volume = None

            elif config.stitching_type is StitchingType.Z_POSTPROC:
                tomwer_volume = VolumeFactory.create_tomo_object_from_identifier(
                    config.output_volume.get_identifier().to_str()
                )
                self.outputs.future_tomo_obj = None
                self.outputs.volume = tomwer_volume
                self.outputs.data = None


class StitchingPostProcAggregation(_StitchingPostProcAggregation):
    """
    once stitching is done remotly we need to 'aggregate' the different part in the correct order
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if isinstance(self.stitching_config, dict):
            stitching_type = StitchingType(self.stitching_config["stitching"]["type"])
            if stitching_type is StitchingType.Z_PREPROC:
                self._stitching_config = PreProcessedZStitchingConfiguration.from_dict(
                    self.stitching_config
                )
            elif stitching_type is StitchingType.Z_POSTPROC:
                self._stitching_config = PostProcessedZStitchingConfiguration.from_dict(
                    self.stitching_config
                )
            else:
                raise NotImplementedError("stitching type not handled")
        elif not isinstance(self.stitching_config, StitchingConfiguration):
            raise TypeError(
                f"stitching_config is expected to be an instance of {StitchingConfiguration}. {type(self.stitching_config)} provided instead"
            )

    def process(self):
        super().process()
        _logger.info("Stitching finished.")
