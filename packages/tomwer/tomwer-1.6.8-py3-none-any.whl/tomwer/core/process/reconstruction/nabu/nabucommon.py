"""contain utils for score process"""

from __future__ import annotations

import logging
import os
import subprocess
import uuid
from typing import Iterable
import signal
import psutil
import sys

import numpy
from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5
from silx.gui.utils import concurrent

from sluurp.executor import submit as submit_to_slurm_cluster
from sluurp.job import SBatchScriptJob
from tomoscan.io import HDF5File
from tomoscan.normalization import Method as INormMethod
from tomoscan.identifier import VolumeIdentifier
from tomoscan.utils.io import filter_esrf_mounting_points

from tomwer.core.process.reconstruction.nabu.plane import NabuPlane
from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.core.process.reconstruction.nabu.target import Target
from tomwer.core.process.reconstruction.nabu.utils import (
    _NabuPhaseMethod,
    nabu_std_err_has_error,
)
from tomwer.core.process.reconstruction.output import (
    ProcessDataOutputDirMode,
    get_output_folder_from_scan,
    NabuOutputFileFormat,
)
from tomwer.core.process.reconstruction.normalization.params import (
    _ValueSource as INormSource,
)
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.slurm import get_slurm_script_name, is_slurm_available
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.resourcemanager import HDF5VolumeManager
from tomwer.core.volume.hdf5volume import HDF5VolumeIdentifier

from . import settings, utils

_logger = logging.getLogger(__name__)
try:
    from nabu.pipeline.fullfield.reconstruction import (  # noqa F401
        FullFieldReconstructor,
    )
except (ImportError, OSError) as e:
    try:
        from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
            ChunkedReconstructor,
        )
    except (ImportError, OSError):
        # import of cufft library can bring an OSError if cuda not install
        _logger.error(e)
        has_nabu = False
    else:
        has_nabu = True
else:
    has_nabu = True


class ResultsRun:
    """
    Base class of results for nabu
    """

    def __init__(self, success, config) -> None:
        self.__success = success
        self.__config = config

    @property
    def success(self) -> bool:
        return self.__success

    @property
    def config(self) -> dict:
        return self.__config

    def __str__(self) -> str:
        return f"result from nabu run: {'succeed' if self.success else 'failed'} with \n - config:{self.config} \n"


class ResultsWithStd(ResultsRun):
    """Nabu result with std"""

    def __init__(self, std_out, std_err, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__std_err = std_err
        self.__std_out = std_out

    @property
    def std_out(self) -> str:
        return self.__std_out

    @property
    def std_err(self) -> str:
        return self.__std_err

    def __str__(self) -> str:
        res = super().__str__()
        res += f"\n {self.std_out} \n {self.std_err}"
        return res


class ResultsLocalRun(ResultsWithStd):
    """Nabu result when run locally.
    If this is the case we should be able to retrieve directly the results urls"""

    def __init__(
        self,
        results_identifiers: tuple,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if not isinstance(results_identifiers, Iterable):
            raise TypeError(
                f"results_urls is expected to be an Iterable not {type(results_identifiers)}"
            )

        # check all identifiers
        def check_identifier(identifier):
            if isinstance(identifier, str):
                vol = VolumeFactory.create_tomo_object_from_identifier(
                    identifier=identifier
                )
                return vol.get_identifier()
            elif not isinstance(identifier, VolumeIdentifier):
                raise TypeError(
                    f"identifiers are expected to be VolumeIdentifier. Get {type(identifier)} instead."
                )
            else:
                return identifier

        self.__results_identifiers = tuple(
            [
                check_identifier(identifier=identifier)
                for identifier in results_identifiers
            ]
        )

    @property
    def results_identifiers(self) -> tuple:
        return self.__results_identifiers

    def __str__(self) -> str:
        res = super().__str__()
        res += f"\n - result urls: {self.results_identifiers}"
        return res


class ResultSlurmRun(ResultsWithStd):
    """Nabu result when run on slurm. on this case we expect to get a future and a distributed client"""

    def __init__(
        self,
        future_slurm_jobs: tuple,
        job_id: int | None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.__future_slurm_jobs = future_slurm_jobs
        self.__job_id = job_id

    @property
    def future_slurm_jobs(self):
        return self.__future_slurm_jobs

    @property
    def job_id(self) -> int | None:
        return self.__job_id

    def __str__(self) -> str:
        res = super().__str__()
        res += f"\n - future job slurms: {self.future_slurm_jobs} \n"
        return res


class _NabuBaseReconstructor:
    """
    Base class to submit a job to nabu
    """

    TIMEOUT_SLURM_JOB_SUBMISSION = 30
    """Timeout when submit a job to slurm cluster. In second"""

    EXPECTS_SINGLE_SLICE = True

    def __init__(
        self,
        scan: TomwerScanBase,
        dry_run: bool,
        target: Target,
        cluster_config: dict | SlurmClusterConfiguration | None,
        process_name: str,
        axis: NabuPlane = NabuPlane.XY,
    ) -> None:
        self._scan = scan
        self._target = Target(target)
        self._dry_run = dry_run
        self._process_name = process_name
        self._process = None
        self._cancelled = False
        self._axis = NabuPlane.from_value(axis)
        # nabu subprocess if run locally
        if isinstance(cluster_config, SlurmClusterConfiguration):
            self._cluster_config = cluster_config
        elif isinstance(cluster_config, dict):
            self._cluster_config = SlurmClusterConfiguration.from_dict(cluster_config)
        elif cluster_config is None:
            self._cluster_config = None
        else:
            raise TypeError(
                f"cluster config is expected to be a dict or an instance of {SlurmClusterConfiguration}. Not {type(cluster_config)}"
            )

    @property
    def scan(self):
        return self._scan

    @property
    def target(self):
        return self._target

    @property
    def cluster_config(self):
        return self._cluster_config

    @property
    def dry_run(self):
        return self._dry_run

    @property
    def process_name(self):
        return self._process_name

    @property
    def axis(self) -> NabuPlane:
        return self._axis

    @property
    def processed_data_folder_name(self) -> str:
        """return the specific processed folder name associated to this type of reconstruction."""
        raise NotImplementedError("Base class")

    def only_create_config_file(self):
        """Should we run the reconstruction or only create the configuration file"""
        return False

    def run(self) -> Iterable:
        """
        run the requested slices.

        :return: Iterable of ResultsRun.
        """
        raise NotImplementedError("Base class")

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
        elif self.target in (Target.LOCAL, Target.SLURM):
            axis = config_to_dump["reconstruction"].get("slice_plane", "XY")
            if file_format in ("hdf5", "h5", "hdf"):
                vol_identifiers = utils.get_recons_volume_identifier(
                    file_prefix=config_to_dump["output"]["file_prefix"],
                    location=config_to_dump["output"]["location"],
                    slice_index=None,
                    scan=self.scan,
                    file_format=file_format,
                    axis=axis,
                )
                # release potential resource lockers (like the HDF5 volume viewer)
                for vol_identifier in vol_identifiers:
                    if isinstance(vol_identifier, HDF5VolumeIdentifier):
                        concurrent.submitToQtMainThread(
                            HDF5VolumeManager.release_resource,
                            vol_identifier.file_path,
                        )
            if self.target is Target.LOCAL:
                _logger.info(f"run {info} for {self.scan} with {config_to_dump}")
                return self._run_nabu_locally(
                    conf_file=config_file,
                    file_format=file_format,
                    config_to_dump=config_to_dump,
                    axis=axis,
                )
            elif self.target is Target.SLURM:
                _logger.info(
                    f"run {info} on slurm for {self.scan.path} with {config_to_dump}"
                )
                return self._run_nabu_on_slurm(
                    conf_file=config_file,
                    config_to_dump=config_to_dump,
                    cluster_config=self.cluster_config.to_dict(),
                    process_name=process_name,
                    info=info,
                )
        else:
            raise ValueError(f"{self.target} is not recognized as a valid target")

    @staticmethod
    def _get_gpu_and_cpu_mem_fraction(config_to_dump: dict):
        gpu_mem_fraction = config_to_dump.get("resources", {}).get(
            "gpu_mem_fraction", config_to_dump.get("gpu_mem_fraction", 0.9)
        )
        assert gpu_mem_fraction <= 1
        cpu_mem_fraction = config_to_dump.get("resources", {}).get(
            "cpu_mem_fraction", config_to_dump.get("cpu_mem_fraction", 0.9)
        )
        assert cpu_mem_fraction <= 1
        return gpu_mem_fraction, cpu_mem_fraction

    def _run_nabu_locally(
        self,
        axis: NabuPlane,
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
        assert isinstance(config_to_dump, dict)
        gpu_mem_fraction, cpu_mem_fraction = self._get_gpu_and_cpu_mem_fraction(
            config_to_dump
        )

        command = " ".join(
            (
                sys.executable,
                "-m",
                settings.NABU_FULL_FIELD_APP_PATH,
                f"'{conf_file}'",  # adding ' around file name allows to handle config file with spaces
                "--gpu_mem_fraction",
                str(gpu_mem_fraction),
                "--cpu_mem_fraction",
                str(cpu_mem_fraction),
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

        recons_vol_identifiers = utils.get_recons_volume_identifier(
            file_prefix=config_to_dump["output"]["file_prefix"],
            location=config_to_dump["output"]["location"],
            slice_index=None,
            scan=self.scan,
            file_format=file_format,
            axis=axis,
        )
        return ResultsLocalRun(
            success=not nabu_std_err_has_error(errs),
            results_identifiers=recons_vol_identifiers,
            std_out=outs,
            std_err=errs,
            config=config_to_dump,  # config_slices,
        )

    def _run_nabu_on_slurm(
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
            raise TypeError(
                f"conf_file is expected to be a string not {type(conf_file)}"
            )
        if not isinstance(config_to_dump, dict):
            raise TypeError(
                f"config_to_dump is expected to be a string not {type(config_to_dump)}"
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

        # extract gpu_mem_fraction and cpu_mem_fraction
        assert isinstance(config_to_dump, dict)
        gpu_mem_fraction, cpu_mem_fraction = self._get_gpu_and_cpu_mem_fraction(
            config_to_dump
        )

        # submit job
        script_name = get_slurm_script_name(prefix="nabu")
        # for now force job name
        cluster_config["job_name"] = f"tomwer-nabu {conf_file}"
        job = SBatchScriptJob(
            slurm_config=cluster_config,
            script=(
                f"python3 -m {settings.NABU_FULL_FIELD_APP_PATH} '{conf_file}' --gpu_mem_fraction {gpu_mem_fraction} --cpu_mem_fraction {cpu_mem_fraction}",
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

    def _get_futures_slurm_callback(self, config_to_dump) -> tuple:
        """Return a tuple a potential callback to be launch once the future is done"""
        return tuple()

    def _treateOutputSliceConfig(self, config) -> tuple:
        """
        - add or overwrite some parameters of the dictionary
        - create the output directory if does not exist

        :return: (config: dict, nabu_cfg_folder: str)
        """
        # handle phase
        pag = False
        ctf = False
        db = None
        if "phase" in config:
            pag = (
                "method" in config["phase"]
                and config["phase"]["method"] == _NabuPhaseMethod.PAGANIN.value
            )
            ctf = (
                "method" in config["phase"]
                and config["phase"]["method"] == _NabuPhaseMethod.CTF.value
            )
            if pag or ctf:
                if "delta_beta" in config["phase"]:
                    if not numpy.isscalar(config["phase"]["delta_beta"]):
                        if len(config["phase"]["delta_beta"]) > 1:
                            raise ValueError(
                                "expects at most one value for 'delta_beta'"
                            )
                        else:
                            config["phase"]["delta_beta"] = config["phase"][
                                "delta_beta"
                            ][0]
                    db = round(float(config["phase"]["delta_beta"]))
        # retrieve axis used
        axis = config.get("reconstruction", {}).get("slice_plane", "XY")

        # handle output
        if "output" in config:
            _file_name = self._get_file_basename_reconstruction(
                pag=pag, db=db, ctf=ctf, axis=axis
            )
            config["output"]["file_prefix"] = _file_name
            location, location_cfg_files = get_output_folder_from_scan(
                mode=ProcessDataOutputDirMode.from_value(
                    config["output"].get(
                        "output_dir_mode", ProcessDataOutputDirMode.OTHER
                    )
                ),
                nabu_location=config["output"].get("location", None),
                scan=self.scan,
                file_basename=_file_name,
                file_format=config["output"].get(
                    "file_format", NabuOutputFileFormat.HDF5
                ),
                processed_data_folder_name=self.processed_data_folder_name,
            )
            # add reconstruction path to the list. scan `reconstruction_paths` register all the existing path where
            # reconstruction are saved in order to be able to browse them all
            self.scan.add_reconstruction_path(location)
            config["output"]["location"] = location
        else:
            # don't think this could ever happen
            location_cfg_files = self.scan.path
        # handle preproc
        if "preproc" not in config:
            config["preproc"] = {}
        if self.scan.intensity_normalization.method is INormMethod.NONE:
            config["preproc"]["sino_normalization"] = ""
        else:
            config["preproc"][
                "sino_normalization"
            ] = self.scan.intensity_normalization.method.value

        extra_infos = self.scan.intensity_normalization.get_extra_infos()

        nabu_cfg_folder = os.path.join(
            location_cfg_files, settings.NABU_CFG_FILE_FOLDER
        )
        os.makedirs(nabu_cfg_folder, exist_ok=True)

        # configuration file and nabu_tomwer_serving_hatch must be in the same folder
        serving_hatch_file = os.path.join(
            nabu_cfg_folder, settings.NABU_TOMWER_SERVING_HATCH
        )

        source = extra_infos.get("source", INormSource.NONE)
        source = INormSource(source)

        if source is INormSource.NONE:
            pass
        elif source is INormSource.MANUAL_SCALAR:
            if "value" not in extra_infos:
                raise KeyError(
                    "value should be provided in extra)infos for scalar defined manually"
                )
            else:
                # check if the dataset has already been saved once and if we can reuse it
                dataset_url = extra_infos.get("dataset_created_by_tomwer", None)
                if dataset_url is not None:
                    # if an url exists insure we can access it
                    dataset_url = DataUrl(path=dataset_url)
                    if os.path.exists(dataset_url.file_path()):
                        with open_hdf5(dataset_url.file_path()) as h5f:
                            if dataset_url.data_path() not in h5f:
                                dataset_url = None
                    else:
                        dataset_url = None
                # if unable toi reuse an existing url them dump the value
                if dataset_url is None:
                    value = extra_infos["value"]
                    if isinstance(value, (tuple, list)):
                        value = numpy.asarray(value)
                    dataset_url = dump_normalization_array_for_nabu(
                        scan=self.scan,
                        array=value,
                        output_file=serving_hatch_file,
                    )
                    extra_infos.update(
                        {"dataset_created_by_tomwer": dataset_url.path()}
                    )
                    self.scan.intensity_normalization.set_extra_infos(extra_infos)

                config["preproc"]["sino_normalization_file"] = dataset_url.path()
        elif source is INormSource.DATASET:
            url = extra_infos["dataset_url"]
            if isinstance(url, DataUrl):
                config["preproc"]["sino_normalization_file"] = url.path()
            elif isinstance(url, str):
                config["preproc"]["sino_normalization_file"] = url
            else:
                raise TypeError(
                    f"dataset_url is expected to be an instance of DataUrl or str representing a DataUrl. Not {type(url)}"
                )
        else:
            raise NotImplementedError(f"source type {source.value} is not handled")
        return config, nabu_cfg_folder

    def _get_file_basename_reconstruction(self, pag, db, ctf, axis):
        """return created file base name"""
        raise NotImplementedError("Base class")

    def cancel(self):
        self._cancelled = True
        if self._process:
            # kill childs processes
            try:
                parent = psutil.Process(self._process.pid)
            except psutil.NoSuchProcess:
                pass
            else:
                # TODO: see with Pierre. But from my point of view this
                # might be handled by nabu it self....
                childrens = parent.children(recursive=True)
                for child in childrens:
                    try:
                        child.send_signal(signal.SIGKILL)
                    except psutil.NoSuchProcess:
                        pass
                    else:
                        child.wait()
                self._process.kill()
                self._process.wait()
            finally:
                self._process = None


def dump_normalization_array_for_nabu(
    scan: TomwerScanBase, output_file: str, array: numpy.ndarray | float | int
) -> DataUrl:
    if not isinstance(array, (numpy.ndarray, float, int)):
        raise TypeError(
            f"array is expected to be a numpy array or a scalar and not {type(array)}"
        )
    # save the value to a dedicated path in "nabu_tomwer_serving_hatch"
    if isinstance(scan, NXtomoScan):
        entry_path = scan.entry
    elif isinstance(scan, EDFTomoScan):
        entry_path = "entry"
    else:
        raise TypeError
    with HDF5File(output_file, mode="a") as h5f:
        serving_hatch_data_path = None
        # create a unique dataset path to avoid possible conflicts
        while serving_hatch_data_path is None or serving_hatch_data_path in h5f:
            serving_hatch_data_path = "/".join([entry_path, str(uuid.uuid1())])
        # adapt value to what nabues expects.
        if isinstance(array, (float, int)) or (
            isinstance(array, numpy.ndarray) and array.ndim == 1 and len(array) == 1
        ):
            dim_1 = scan.dim_1
            array = numpy.asarray(
                numpy.asarray([array] * len(scan.projections) * dim_1)
            )
            array = array.reshape(len(scan.projections), dim_1)
        elif isinstance(array, numpy.ndarray) and array.ndim == 1:
            dim_1 = scan.dim_1
            array = numpy.repeat(array, dim_1).reshape(len(array), dim_1)

        h5f[serving_hatch_data_path] = array
    file_path = os.path.join(
        settings.NABU_CFG_FILE_FOLDER, settings.NABU_TOMWER_SERVING_HATCH
    )
    return DataUrl(
        file_path=file_path,
        data_path=serving_hatch_data_path,
        scheme="silx",
    )
