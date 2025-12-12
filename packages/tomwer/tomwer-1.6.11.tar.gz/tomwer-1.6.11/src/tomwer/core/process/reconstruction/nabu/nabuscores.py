from __future__ import annotations

try:
    from nabu.pipeline.fullfield.reconstruction import (  # noqa F401
        FullFieldReconstructor,
    )
except (ImportError, OSError):
    try:
        from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
            ChunkedReconstructor,
        )
    except (ImportError, OSError):
        # import of cufft library can bring an OSError if cuda not install
        has_nabu = False
    else:
        has_nabu = True
else:
    has_nabu = True
import logging
import os
import sys
from copy import deepcopy
import subprocess
from typing import Iterable
import numpy
from tqdm import tqdm

from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from processview.core.manager.manager import ProcessManager
from sluurp.job import SBatchScriptJob
from sluurp.executor import submit as submit_to_slurm_cluster

from tomoscan.utils.io import filter_esrf_mounting_points

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.process.reconstruction.nabu.nabuslices import (
    SingleSliceRunner,
    _NabuBaseReconstructor,
    generate_nabu_configfile,
)
from tomwer.core.process.reconstruction.nabu.utils import (
    slice_index_to_int,
    get_nabu_multicor_file_prefix,
)
from tomwer.core.process.reconstruction.utils.cor import (
    relative_pos_to_absolute,
    absolute_pos_to_relative,
)
from tomwer.core.process.reconstruction.nabu.target import Target
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.slurm import get_slurm_script_name, is_slurm_available
from tomwer.utils import docstring
from tomwer.core.process.reconstruction.nabu.utils import nabu_std_err_has_error
from tomwer.core.process.reconstruction.nabu.plane import NabuPlane

from ..nabu import settings as nabu_settings
from . import utils, settings
from .nabucommon import ResultsLocalRun, ResultSlurmRun, ResultsWithStd, ResultsRun

_logger = logging.getLogger(__name__)


def run_nabu_one_slice_several_config(
    scan: TomwerScanBase,
    nabu_configs: list | tuple,
    cluster_config: dict | None,
    dry_run: bool,
    slice_index: int | str,
    file_format: str,
    axis: NabuPlane,
    advancement: tqdm | None = None,
    process_id: int | None = None,
    instantiate_classes_only: bool = False,
    output_file_prefix_pattern=None,
) -> tuple:
    """
    Run several reconstruction of a specific slice.

    :param scan: dataset
    :param nabu_configs: set of nabu configurations to be run
    :param dry_run:
    :param slice_index: slice index to reconstruct or "middle"
    :param advancement: optional class to display advancement
    :param process_id: id of the process requesting this computation
    :param cluster_config: cluster configuration if
    :return: success, recons_urls (list of output urls), tuple of outs, tuples of errs, dict future_scans (key is cor, value is future_scan)
             if `instantiate_classes_only` set to True then return a list of :class:`_Reconstructor`
    """
    if cluster_config in (None, {}):
        target = Target.LOCAL
    elif isinstance(cluster_config, dict):
        if not is_slurm_available():
            raise RuntimeError("Slurm computation requested but unvailable")
        target = Target.SLURM
    else:
        raise TypeError(
            f"cluster_config should be None or a dict not {type(cluster_config)}"
        )

    if process_id is not None:
        try:
            process_name = ProcessManager().get_process(process_id=process_id).name
        except KeyError:
            process_name = "unknow"
    else:
        process_name = ""

    reconstructor = _Reconstructor(
        scan=scan,
        nabu_configs=nabu_configs,
        advancement=advancement,
        slice_index=slice_index,
        target=target,
        dry_run=dry_run,
        file_format=file_format,
        cluster_config=cluster_config,
        process_name=process_name,
        output_file_prefix_pattern=output_file_prefix_pattern,
        axis=axis,
    )
    if instantiate_classes_only:
        return (reconstructor,)

    try:
        results = reconstructor.run()
    except TimeoutError as e:
        _logger.error(e)
        return None
    else:
        assert isinstance(
            results, dict
        ), "results should be a dictionary with var_value as key and urls as value"
        success = True
        recons_urls = {}
        std_outs = []
        std_errs = []
        future_tomo_objs = {}
        for var_value, res in results.items():
            success = success and res.success
            if isinstance(res, ResultsWithStd):
                std_outs.append(res.std_out)
                std_errs.append(res.std_err)
            if isinstance(res, ResultsLocalRun):
                recons_urls[var_value] = res.results_identifiers
            if isinstance(res, ResultSlurmRun):
                future_tomo_obj = FutureTomwerObject(
                    tomo_obj=scan,
                    process_requester_id=process_id,
                    futures=res.future_slurm_jobs,
                )
                future_tomo_objs[var_value] = future_tomo_obj
        return success, recons_urls, std_outs, std_errs, future_tomo_objs


def run_nabu_multicor(
    scan: TomwerScanBase,
    nabu_config: dict,
    cors: tuple,
    cluster_config: dict | None,
    dry_run: bool,
    slice_index: int | str,
    file_format: str,
    process_id: int | None = None,
    instantiate_classes_only: bool = False,
    output_file_prefix_pattern=None,
):
    if cluster_config in (None, {}):
        target = Target.LOCAL
    elif isinstance(cluster_config, dict):
        if not is_slurm_available():
            raise RuntimeError("Slurm computation requested but unvailable")
        target = Target.SLURM
    else:
        raise TypeError(
            f"cluster_config should be None or a dict not {type(cluster_config)}"
        )

    if process_id is not None:
        try:
            process_name = ProcessManager().get_process(process_id=process_id).name
        except KeyError:
            process_name = "unknow"
    else:
        process_name = ""

    # TODO: FIXME small hack to make sure the configuration will be accepted when valie
    # for now even if the cor values are given from a dedicated parameter nabu is still
    # checking the value provided in the config file. If this value is invalid for
    # half acquisition it will be refused
    nabu_config["reconstruction"]["rotation_axis_position"] = numpy.mean(cors)

    axis = nabu_config["reconstruction"].get("slice_plane", "XY")

    reconstructor = _ReconstructorMultiCor(
        scan=scan,
        nabu_config=nabu_config,
        cors=cors,
        slice_index=slice_index,
        target=target,
        dry_run=dry_run,
        file_format=file_format,
        cluster_config=cluster_config,
        process_name=process_name,
        axis=axis,
        output_file_prefix_pattern=output_file_prefix_pattern,
    )
    if instantiate_classes_only:
        return reconstructor

    try:
        result = reconstructor.run()
    except TimeoutError as e:
        _logger.error(e)
        return None
    else:
        recons_urls = {}
        std_outs = []
        std_errs = []
        future_tomo_obj = None

        success = result.success
        if isinstance(result, ResultsWithStd):
            std_outs.append(result.std_out)
            std_errs.append(result.std_err)
        if isinstance(result, ResultsLocalRun):
            recons_urls = result.results_identifiers
        if isinstance(result, ResultSlurmRun):
            future_tomo_obj = FutureTomwerObject(
                tomo_obj=scan,
                process_requester_id=process_id,
                futures=result.future_slurm_jobs,
            )
        return success, recons_urls, (future_tomo_obj,), std_outs, std_errs


class _Reconstructor(_NabuBaseReconstructor):
    def __init__(
        self,
        scan: TomwerScanBase,
        nabu_configs: Iterable,
        advancement: tqdm | None,
        slice_index: int | str,
        axis: str | NabuPlane,
        target: Target,
        dry_run: bool,
        file_format: str,
        cluster_config: dict | None,
        process_name: str,
        output_file_prefix_pattern=None,
    ) -> None:
        """
        :param scan: scan to reconstruct
        :param nabu_configs: all the configuration to run
        :param advancement: Progress object to notify advancement
        :param slice_index: index of the slice to reconstruct.
        :param axis: axis over which we want to do the reconstruction
        :param target: is the reconstruction is to made locally or remotly
        :param file_format: reconstructed volume file format
        :param cluster_config: cluster configuration in the case of a remote execution
        :param extra_output_file_pattern: possible extra file name pattern like for cor we want to add 'cor_' as prefix and cor value as suffix.
                                              To make the file name unique. For delta/beta it is already forseen to be unique. For now keywords are:
                                              * file_name: default file name according to db values and dataset name
                                              * value: value of the nabu_configs keys
        """
        super().__init__(
            scan=scan,
            dry_run=dry_run,
            target=target,
            cluster_config=cluster_config,
            process_name=process_name,
            axis=axis,
        )
        if not isinstance(slice_index, (int, str)):
            raise TypeError(
                f"slice_index should be an int or a string not {type(slice_index)}"
            )
        self.advancement = advancement
        self.slice_index = slice_index
        self.nabu_configs = nabu_configs
        self.file_format = file_format
        self._output_file_prefix_pattern = output_file_prefix_pattern

    @docstring(_NabuBaseReconstructor)
    def run(self) -> Iterable:
        self.slice_index = slice_index_to_int(
            slice_index=self.slice_index, scan=self.scan
        )

        results = {}
        if self.advancement is not None:
            self.advancement.total = len(self.nabu_configs)
        for var_value, config in self.nabu_configs.items():
            if self._cancelled:
                break
            config, conf_file = self.preprocess_config(deepcopy(config), var_value)

            # add some tomwer metadata and save the configuration
            # note: for now the section is ignored by nabu but shouldn't stay that way
            with utils.TomwerInfo(config) as config_to_dump:
                generate_nabu_configfile(
                    conf_file,
                    nabu_fullfield_default_config,
                    config=config_to_dump,
                    options_level="advanced",
                )

            results[var_value] = self._process_config(
                config_to_dump=config_to_dump,
                config_file=conf_file,
                file_format=self.file_format,
                info="nabu slice reconstruction",
                process_name=self.process_name,
            )
            # specific treatment for cor: rename output files
            if self.advancement is not None:
                self.advancement.update()
        return results

    def _format_file_prefix(self, file_prefix, value):
        if self._output_file_prefix_pattern is None:
            return file_prefix

        keywords = {
            "file_name": file_prefix,
            "value": value,
        }

        # filter necessary keywords
        def get_necessary_keywords():
            import string

            formatter = string.Formatter()
            return [
                field
                for _, field, _, _ in formatter.parse(self._output_file_prefix_pattern)
                if field
            ]

        requested_keywords = get_necessary_keywords()

        def keyword_needed(pair):
            keyword, _ = pair
            return keyword in requested_keywords

        keywords = dict(filter(keyword_needed, keywords.items()))
        return self._output_file_prefix_pattern.format(**keywords)

    def treateOutputConfig(self, _config, value):
        """
        - add or overwrite some parameters of the dictionary
        - create the output directory if does not exist
        """
        pag = False
        ctf = False
        db = None
        if "phase" in _config:
            phase_method = _config["phase"].get("method", "").lower()
            if phase_method in ("pag", "paganin"):
                pag = True
            elif phase_method in ("ctf",):
                ctf = True

            if "delta_beta" in _config["phase"]:
                db = round(float(_config["phase"]["delta_beta"]))
        if "output" in _config:
            file_prefix = SingleSliceRunner.get_file_basename_reconstruction(
                scan=self.scan,
                slice_index=self.slice_index,
                pag=pag,
                db=db,
                ctf=ctf,
                axis=self.axis,
            )
            file_prefix = self._format_file_prefix(file_prefix=file_prefix, value=value)
            _config["output"]["file_prefix"] = file_prefix
            assert _config["output"]["location"] not in ("", None)
            if not os.path.isdir(_config["output"]["location"]):
                os.makedirs(_config["output"]["location"])

        if "reconstruction" not in _config:
            _config["reconstruction"] = {}
        if self.axis is NabuPlane.YZ:
            _config["reconstruction"]["start_x"] = self.slice_index
            _config["reconstruction"]["end_x"] = self.slice_index
        elif self.axis is NabuPlane.XZ:
            _config["reconstruction"]["start_y"] = self.slice_index
            _config["reconstruction"]["end_y"] = self.slice_index
        elif self.axis is NabuPlane.XY:
            _config["reconstruction"]["start_z"] = self.slice_index
            _config["reconstruction"]["end_z"] = self.slice_index
        else:
            raise ValueError(
                f"self.axis has an invalid value: {self.axis} when expected to be in {[item.value for item in NabuPlane]}"
            )
        return _config, file_prefix

    def preprocess_config(self, config, value) -> tuple:
        dataset_params = self.scan.get_nabu_dataset_info()
        if "dataset" in config:
            dataset_params.update(config["dataset"])
        config["dataset"] = dataset_params

        config["resources"] = config.get("resources", {})
        config["resources"]["method"] = "local"

        # force overwrite results
        if "output" not in config:
            config["output"] = {}
        config["output"].update({"overwrite_results": 1})

        config, file_prefix = self.treateOutputConfig(config, value=value)
        # the policy is to save nabu .cfg file at the same location as the
        # force overwrite results

        cfg_folder = os.path.join(
            config["output"]["location"],
            nabu_settings.NABU_CFG_FILE_FOLDER,
        )
        os.makedirs(cfg_folder, exist_ok=True)

        conf_file = os.path.join(
            cfg_folder, file_prefix + nabu_settings.NABU_CONFIG_FILE_EXTENSION
        )
        return config, conf_file


class _ReconstructorMultiCor(_NabuBaseReconstructor):
    def __init__(
        self,
        nabu_config: dict,
        axis: str | NabuPlane,
        cors: tuple,
        file_format,
        slice_index: int | str = "middle",
        output_file_prefix_pattern=None,
        *args,
        **kwargs,
    ):
        if not isinstance(cors, tuple):
            raise TypeError(
                f"cors are expected to be an instance of tuple. Get {type(cors)} instead"
            )
        self.__cors = cors
        self.__slice_index = slice_index
        self.__nabu_config = nabu_config
        self.file_format = file_format
        self._output_file_prefix_pattern = output_file_prefix_pattern

        super().__init__(*args, **kwargs)

    @property
    def cors(self) -> tuple:
        return self.__cors

    @property
    def slice_index(self) -> int | str:
        return self.__slice_index

    @property
    def nabu_config(self) -> dict:
        return self.__nabu_config

    def _process_config(
        self,
        config_to_dump: dict,
        config_file: str,
        file_format: str,
        info: str | None,
        process_name: str,
    ):
        """
        process provided configuration

        :param info:
        """
        if self.dry_run is True or self.only_create_config_file():
            return ResultsRun(
                success=True,
                config=config_to_dump,
            )
        elif self.target is Target.LOCAL:
            _logger.info(f"run {info} for {self.scan} with {config_to_dump}")
            return self._run_nabu_multicor_locally(
                conf_file=config_file,
                file_format=file_format,
                config_to_dump=config_to_dump,
            )
        elif self.target is Target.SLURM:
            _logger.info(
                f"run {info} on slurm for {self.scan.path} with {config_to_dump}"
            )
            return self._run_nabu_multicor_on_slurm(
                conf_file=config_file,
                config_to_dump=config_to_dump,
                cluster_config=self.cluster_config.to_dict(),
                process_name=process_name,
                info=info,
            )
        else:
            raise ValueError(f"{self.target} is not recognized as a valid target")

    def _run_nabu_multicor_locally(
        self,
        conf_file: str,
        file_format: str,
        config_to_dump: dict,
    ) -> ResultsLocalRun:
        """
        run locally nabu for a single configuration file.

        :param conf_file: path to the nabu .cfg file
        :param file_format: format of the generated file
        :param config_to_dump: configuration saved in the .cfg as a dictionary
        :return: results of the local run
        """
        if not has_nabu:
            raise ImportError("Fail to import nabu")
        slice_index = slice_index_to_int(self.slice_index, scan=self.scan)

        cor_in_nabu_ref = tuple(
            [
                relative_pos_to_absolute(relative_pos=cor, det_width=self.scan.dim_1)
                for cor in self.cors
            ]
        )
        cor_in_nabu_ref = ",".join([str(cor) for cor in cor_in_nabu_ref])
        command = " ".join(
            (
                sys.executable,
                "-m",
                settings.NABU_MULTICOR_PATH,
                f"'{conf_file}'",  # input file
                f"{slice_index}",  # slice
                f"{cor_in_nabu_ref}",  # cor
            )
        )
        _logger.info(f'call nabu from "{command}"')

        self._process = subprocess.Popen(
            command,
            shell=True,
            cwd=self.scan.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            outs, errs = self._process.communicate()
        except (TimeoutError, KeyboardInterrupt):
            self._process.kill()
            outs, errs = self._process.communicate()

        file_prefix = get_nabu_multicor_file_prefix(self.scan)

        recons_vol_identifiers = utils.get_multi_cor_recons_volume_identifiers(
            slice_index=slice_index,
            location=config_to_dump["output"]["location"],
            file_prefix=file_prefix,
            scan=self.scan,
            file_format=file_format,
            cors=[
                relative_pos_to_absolute(relative_pos=cor, det_width=self.scan.dim_1)
                for cor in self.cors
            ],
        )
        # convert back from abs ref to rel ref
        recons_vol_identifiers = {
            absolute_pos_to_relative(
                absolute_pos=cor, det_width=self.scan.dim_1
            ): identifiers
            for cor, identifiers in recons_vol_identifiers.items()
        }
        return ResultsLocalRun(
            success=not nabu_std_err_has_error(errs),
            results_identifiers=recons_vol_identifiers.values(),
            std_out=outs,
            std_err=errs,
            config=config_to_dump,  # config_slices,
        )

    def _run_nabu_multicor_on_slurm(
        self,
        conf_file: str,
        config_to_dump: dict,
        cluster_config: dict,
        process_name: str,
        info: str,
    ) -> ResultSlurmRun:
        """
        Run a nabu reconstruction on slurm of a single configuration

        :return: results of the slurm run
        """
        if not isinstance(conf_file, str):
            raise TypeError(f"conf_file is expected to be a strg not {type(conf_file)}")
        if not isinstance(config_to_dump, dict):
            raise TypeError(
                f"config_to_dump is expected to be a strg not {type(config_to_dump)}"
            )
        if not is_slurm_available():
            raise RuntimeError("slurm not available")
        if not isinstance(cluster_config, dict):
            raise ValueError(
                f"cluster config is expected to be a dict not {type(cluster_config)}"
            )

        # create slurm cluster
        project_name = cluster_config.get(
            "job_name", "tomwer_{scan}_-_{process}_-_{info}"
        )
        project_name = project_name.format(
            scan=str(self.scan), process=process_name, info=info
        )
        # project name should not contain any spaces as it will be integrated in a script and interpreted.
        project_name = project_name.replace(" ", "_")
        cluster_config["job_name"] = project_name

        slice_index = slice_index_to_int(self.slice_index, scan=self.scan)
        cor_in_nabu_ref = tuple(
            [
                relative_pos_to_absolute(relative_pos=cor, det_width=self.scan.dim_1)
                for cor in self.cors
            ]
        )
        cor_in_nabu_ref = ",".join([str(cor) for cor in cor_in_nabu_ref])

        # submit job
        script_name = get_slurm_script_name(prefix="nabu")
        # for now force job name
        cluster_config["job_name"] = f"tomwer-nabu {conf_file}"
        job = SBatchScriptJob(
            slurm_config=cluster_config,
            script=(
                f"python3 -m {settings.NABU_MULTICOR_PATH} {conf_file} {slice_index} {cor_in_nabu_ref}",
            ),
            script_path=filter_esrf_mounting_points(
                os.path.join(self.scan.resolved_path, "slurm_scripts", script_name)
            ),
            clean_script=False,
            working_directory=filter_esrf_mounting_points(
                str(self.scan.working_directory.resolve())
            ),
        )
        future_slurm_job = submit_to_slurm_cluster(job)

        callbacks = self._get_futures_slurm_callback(config_to_dump)
        assert isinstance(
            callbacks, tuple
        ), f"callbacks is expected to an instance of tuple and not {type(callbacks)}"
        for callback in callbacks:
            future_slurm_job.add_done_callback(callback.process)

        return ResultSlurmRun(
            success=True,
            config=config_to_dump,
            future_slurm_jobs=(future_slurm_job,),
            std_out=None,
            std_err=None,
            job_id=job.job_id,
        )

    def preprocess_config(self, config):
        dataset_params = self.scan.get_nabu_dataset_info()
        if "dataset" in config:
            dataset_params.update(config["dataset"])
        config["dataset"] = dataset_params

        config["resources"] = config.get("resources", {})
        config["resources"]["method"] = "local"

        # force overwrite results
        if "output" not in config:
            config["output"] = {}
        config["output"].update({"overwrite_results": 1})

        cfg_folder = os.path.join(
            config["output"]["location"],
            nabu_settings.NABU_CFG_FILE_FOLDER,
        )
        os.makedirs(cfg_folder, exist_ok=True)

        cfg_folder = os.path.join(
            self.nabu_config["output"]["location"],
            nabu_settings.NABU_CFG_FILE_FOLDER,
        )
        os.makedirs(cfg_folder, exist_ok=True)

        conf_file = os.path.join(
            cfg_folder,
            f"{self.scan.get_dataset_basename()}_multi_cor"
            + nabu_settings.NABU_CONFIG_FILE_EXTENSION,
        )
        return config, conf_file

    def run(self) -> Iterable:
        nabu_config, conf_file = self.preprocess_config(deepcopy(self.nabu_config))

        # the policy is to save nabu .cfg file at the same location as the
        # force overwrite results

        # add some tomwer metadata and save the configuration
        # note: for now the section is ignored by nabu but shouldn't stay that way
        with utils.TomwerInfo(nabu_config) as config_to_dump:
            generate_nabu_configfile(
                conf_file,
                nabu_fullfield_default_config,
                config=config_to_dump,
                options_level="advanced",
            )

        results = self._process_config(
            config_to_dump=nabu_config,
            config_file=conf_file,
            file_format=self.file_format,
            info="nabu sa-axis reconstruction",
            process_name=self.process_name,
        )

        return results
