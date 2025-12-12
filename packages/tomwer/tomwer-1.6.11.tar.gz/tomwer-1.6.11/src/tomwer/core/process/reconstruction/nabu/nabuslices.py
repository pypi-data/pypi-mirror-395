from __future__ import annotations

import copy
import functools
import logging
import os
import gc
from collections.abc import Callable
from tomwer.io.utils import format_stderr_stdout
from silx.utils.deprecation import deprecated, deprecated_warning
from silx.io.utils import open as open_hdf5

from processview.core.manager.manager import ProcessManager, DatasetState

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.utils.slurm import is_slurm_available
from tomwer.core.process.reconstruction.nabu.utils import (
    update_nabu_config_for_tiff_3d,
    from_nabu_config_to_file_format,
)
from tomwer.core.process.reconstruction.nabu.plane import NabuPlane
from tomwer.core.process.reconstruction.nabu.utils import slice_index_to_int
from tomwer.core.process.reconstruction.utils.cor import relative_pos_to_absolute
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_RECONSTRUCTED_SLICES,
)

try:
    from nabu.pipeline.fullfield.reconstruction import (  # noqa F401
        FullFieldReconstructor,
    )
except (ImportError, OSError) as e:
    _err_import_nabu = e
    try:
        from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
            ChunkedReconstructor,
        )
    except (ImportError, OSError):
        # import of cufft library can bring an OSError if cuda not install
        has_nabu = False
    else:
        has_nabu = True
        _err_import_nabu = None
else:
    has_nabu = True
    _err_import_nabu = None

from typing import Iterable

from nabu import version as nabu_version
from nabu.pipeline.config import (
    _extract_nabuconfig_keyvals,
    generate_nabu_configfile,
    get_default_nabu_config,
)
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from processview.core.superviseprocess import SuperviseProcess
from enum import Enum as _Enum

from tomwer.core.process.task import Task
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.utils import docstring

from . import settings as nabu_settings
from . import utils
from .nabucommon import (
    ResultsLocalRun,
    ResultSlurmRun,
    ResultsRun,
    _NabuBaseReconstructor,
)
from .target import Target

_logger = logging.getLogger(__name__)
if not has_nabu:
    _logger.error(_err_import_nabu)


def run_slices_reconstruction(
    scan: TomwerScanBase,
    config: dict,
    dry_run: bool = False,
    advancement=None,
    process_id: int | None = None,
    instantiate_classes_only: bool = False,
    invalid_slice_callback: Callable[[str], None] | None = None,
) -> tuple:
    """
    call nabu for a reconstruction on scan with the given configuration

    :param scan: scan to reconstruct
    :param config: configuration to run the reconstruction.
                        Contains nabu reconstruction parameters and slurm cluster
                        configuration if requested (key: `slurm-cluster`).
    :param dry_run: do we want to run dry
    :param local: do we want to run a local reconstruction
    :param stderr: file to redirect stderr
    :param stdout: file to redirect stdout
    :param advancement: optional Progress class to display advancement
    :param process_id: optional process id
    :param instantiate_class_only: if we don't want to run the SingleSliceRunner but only return them. Use case: we want to keep a hand on processing and it can be cancelled

    :return: (all_succeed, stdouts, stderrs, final_configs, future_scan)
        * all_succeed: bool, True if all the reconstruction succeed or if all job request succeed.
        * stdouts: list of stdout of job reconstruction or job requests
        * stderrs: list of stderr of job reconstruction or job requests
        * final_configs: list of configurations submits to nabu
        * future_scan: FutureTomwerScan | None future scan containing futures pointing to job submited to the cluster. None if local reconstruction

    Behavior: will clear the last slices reconstructed
    """
    # TODO: remove the local parameter
    _logger.info(f"start reconstruction of {scan}")

    cluster_config = config.pop("cluster_config", None)
    if cluster_config == {}:
        cluster_config = None
    is_cluster_job = cluster_config is not None
    if is_cluster_job and not is_slurm_available():
        raise ValueError(
            "job on cluster requested but no access to slurm cluster found"
        )

    # beam shape is not directly used by nabu (uses ctf_geometry directly)
    config.get("phase", {}).pop("beam_shape", None)

    # if scan contains some center of position copy it to nabu
    if scan.axis_params is not None and scan.axis_params.relative_cor_value is not None:
        if "reconstruction" in config:
            # move the cor value to the nabu reference
            cor_nabu_ref = relative_pos_to_absolute(
                relative_pos=scan.axis_params.relative_cor_value,
                det_width=scan.dim_1,
            )
            config["reconstruction"]["rotation_axis_position"] = str(cor_nabu_ref)
    _logger.info(f"set nabu reconstruction parameters to {scan}")

    # update nabu recons_params used
    sc_config = get_default_nabu_config(nabu_fullfield_default_config)
    sc_config.update(config)
    scan.nabu_recons_params = sc_config

    # handle special cases like several db...
    nabu_configurations = interpret_tomwer_configuration(
        config, scan=scan, invalid_slice_callback=invalid_slice_callback
    )
    output_urls = []
    stderrs = []
    stdouts = []
    final_configs = []
    futures = []
    instantiated_classes = []
    all_succeed = True
    if advancement is not None:
        advancement.total = len(nabu_configurations)
    scan.clear_latest_reconstructions()
    for nabu_configuration in nabu_configurations:
        l_config, slice_index = nabu_configuration
        result = run_single_slice_reconstruction(
            nabu_config=l_config,
            cluster_config=cluster_config,
            scan=scan,
            slice_index=slice_index,
            dry_run=dry_run,
            instantiate_class_only=instantiate_classes_only,
            axis=config.get("reconstruction", {}).get("slice_plane", "XY"),
        )

        # specific treatments of results
        if result is None:
            # in case of timeout or another issue. Log should already have been provided
            pass
        elif instantiate_classes_only:
            instantiated_classes.append(result)
            continue
        if slice_index is None:
            continue
        elif isinstance(result, ResultsLocalRun):
            assert not is_cluster_job, "cluster job should not return ResultsLocalRun"
            stderrs.append(result.std_err)
            stdouts.append(result.std_out)
            output_urls.extend(result.results_identifiers)
            # if slice_index is None this mean that we are simply creating the
            # .cfg file for nabu full volume.
        elif isinstance(result, ResultSlurmRun):
            assert (
                is_cluster_job
            ), "local reconstruction should not return ResultSlurmRun"
            stderrs.append(result.std_err)
            stdouts.append(result.std_out)
            futures.extend(result.future_slurm_jobs)
        elif not isinstance(result, ResultsRun):
            raise ValueError(
                f"result is expected to be an instance of {ResultsRun} not {type(result)}"
            )

        # common treatments of results
        if result is not None:
            final_configs.append(result.config)
            all_succeed = all_succeed and result.success

        if advancement is not None:
            advancement.update()

    if instantiate_classes_only:
        return instantiated_classes
    if is_cluster_job:
        future_tomo_obj = FutureTomwerObject(
            tomo_obj=scan,
            futures=tuple(futures),
            process_requester_id=process_id,
        )
        scan.set_latest_reconstructions(output_urls)
        return all_succeed, stdouts, stderrs, final_configs, future_tomo_obj
    else:
        # tag latest reconstructions
        scan.set_latest_reconstructions(output_urls)
        return all_succeed, stdouts, stderrs, final_configs, None


class NabuSlicesTask(
    Task,
    SuperviseProcess,
    input_names=(
        "data",
        "nabu_params",
    ),
    optional_input_names=(
        "dry_run",
        "serialize_output_data",
        "invalid_slice_callback",
    ),
    output_names=("data", "nabu_params", "future_tomo_obj"),
):
    """
    Definition of the nabu reconstruction volume reconstruction process
    """

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
        self._dry_run = inputs.get("dry_run", False)
        self._current_processing = None
        # we can sometime call several time a nabu subprocess. The idea is to keep track of it
        # if we want to stop the processing

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        configuration = self.inputs.nabu_params

        self.outputs.nabu_params = None
        if scan is None:
            self.outputs.data = None
            return
        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed" "")
        assert isinstance(configuration, dict), "configuration is expected to be a dict"

        output_urls = []
        stderrs = []
        stdouts = []
        final_configs = []
        futures = []
        all_succeed = True
        is_cluster_job = configuration.get("cluster_config", None) is not None
        # loop is required for distributed since version 2021
        try:
            single_slice_runner_instances = run_slices_reconstruction(
                config=configuration,
                scan=scan,
                dry_run=self._dry_run,
                process_id=self.process_id,
                instantiate_classes_only=True,
                invalid_slice_callback=self.get_input_value(
                    "invalid_slice_callback", None
                ),
            )
        except Exception as e:
            mess = f"Fail to instantiate slice reconstructor for {str(scan)}. Reason is {e}."
            _logger.processFailed(mess)
            ProcessManager().notify_dataset_state(
                dataset=scan,
                process=self,
                state=DatasetState.FAILED,
                details=mess,
            )
            self.outputs.future_tomo_obj = None
            return

        for slice_runner in single_slice_runner_instances:
            self._current_processing = slice_runner
            result = self._current_processing.run()[
                0
            ]  # we are expecting a single slice per run in this configuration
            if result is None:
                # in case of timeout or another issue. Log should already have been provided
                pass
            elif isinstance(result, ResultsLocalRun):
                assert (
                    not is_cluster_job
                ), "cluster job should not return ResultsLocalRun"
                stderrs.append(result.std_err)
                stdouts.append(result.std_out)
                output_urls.extend(result.results_identifiers)
                # if slice_index is None this mean that we are simply creating the
                # .cfg file for nabu full volume.
            elif isinstance(result, ResultSlurmRun):
                assert (
                    is_cluster_job
                ), "local reconstruction should not return ResultSlurmRun"
                stderrs.append(result.std_err)
                stdouts.append(result.std_out)
                futures.extend(result.future_slurm_jobs)
            elif not isinstance(result, ResultsRun):
                raise ValueError(
                    f"result is expected to be an instance of {ResultsRun} not {type(result)}"
                )

            # common treatments of results
            if result is not None:
                final_configs.append(result.config)
                all_succeed = all_succeed and result.success

        # update future object and scan latest reconstructions
        self._current_processing = None
        if not self._cancelled and is_cluster_job:
            future_tomo_obj = FutureTomwerObject(
                tomo_obj=scan,
                futures=tuple(futures),
                process_requester_id=self.process_id,
            )
            scan.set_latest_reconstructions(output_urls)
        else:
            # tag latest reconstructions
            scan.set_latest_reconstructions(output_urls)
            future_tomo_obj = None

        volume_urls = []
        for rec_identifier in scan.latest_reconstructions:
            volume_urls.extend(
                VolumeFactory.from_identifier_to_vol_urls(rec_identifier)
            )

        # update processes information / registration
        gc.collect()

        # TODO: check output files with the tomoscan validator ?
        if self._cancelled:
            state = DatasetState.CANCELLED
            details = "cancelled by user"
            future_tomo_obj = None
            _logger.info(f"Slices computation for {scan} cancelled")
        else:
            if not all_succeed:
                mess = f"Slices computation for {scan} failed."
                state = DatasetState.FAILED
                _logger.processFailed(mess)
            else:
                state = DatasetState.SUCCEED
                mess = f"Slices computed for {scan}."
                _logger.processSucceed(mess)
            elmts = [
                format_stderr_stdout(stderr=stderr, stdout=stdout)
                for stderr, stdout in zip(stderrs, stdouts)
            ]
            elmts.insert(0, mess)
            details = "\n".join(elmts)

        ProcessManager().notify_dataset_state(
            dataset=scan,
            process=self,
            state=state,
            details=details,
        )

        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan
        self.outputs.nabu_params = scan.nabu_recons_params
        self.outputs.future_tomo_obj = future_tomo_obj

    def set_configuration(self, configuration: dict) -> None:
        Task.set_configuration(self, configuration=configuration)
        if "dry_run" in configuration:
            self.set_dry_run(bool(configuration["dry_run"]))

    @staticmethod
    def program_name():
        return "nabu-slices"

    @staticmethod
    def program_version():
        return nabu_version

    @deprecated(replacement="provide dry_run to the task inputs", since_version="1.2")
    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    @property
    @deprecated(replacement="Task.inputs.dry_run", since_version="1.2")
    def dry_run(self):
        return self._dry_run

    def cancel(self):
        """
        stop current processing
        """
        self._cancelled = True
        if self._current_processing is not None:
            self._current_processing.cancel()


def interpret_tomwer_configuration(
    config: dict,
    scan: TomwerScanBase | None,
    invalid_slice_callback: Callable[[str], None] | None = None,
) -> tuple:
    """
    tomwer can 'mock' the nabu reconstruction to request more feature.
    Typical use case is that we can ask for reconstruction of several
    slices and not only the volume

    :param config: tomwer configuration for nabu
    :param scan: requested if we want to get slices
    :return: tuple of tuples (nabu configuration, is slice)
    """
    if not isinstance(config, dict):
        raise TypeError("config is expected to be a dict")

    def get_nabu_config(config):
        nabu_config = copy.deepcopy(config)
        if "tomwer_slices" in nabu_config:
            del nabu_config["tomwer_slices"]
        return nabu_config

    if "tomwer_slices" in config and scan is not None:
        reconstruction_axis = NabuPlane.from_value(
            config.get("reconstruction", {}).get("slice_plane", "XY")
        )
        slices = list(
            NabuSliceMode.getSlices(
                config["tomwer_slices"],
                scan=scan,
                axis=reconstruction_axis,
            )
        )

        def filter_slice(slice_index: int, axis: NabuPlane):
            """remove slices that 'cannot' be reconstructed (out of bounds)"""
            if axis is NabuPlane.XY:
                index_max = scan.dim_2
            elif axis in (NabuPlane.XZ, NabuPlane.YZ):
                index_max = scan.dim_1
            else:
                raise ValueError

            if index_max is None:
                return True

            index_max = index_max - 1

            if slice_index > index_max:
                error_message = f"{scan.get_identifier().short_description()}\n\nCannot reconstruct slice {slice_index} along plane {axis.value}. Must be in [0-{index_max}]"
                _logger.error(error_message)
                if invalid_slice_callback is not None:
                    invalid_slice_callback(error_message)
                return False
            return True

        slices = list(
            filter(
                lambda slice_index: filter_slice(
                    int(slice_index), axis=reconstruction_axis
                ),
                slices,
            )
        )

    else:
        slices = []

    if "phase" in config and "delta_beta" in config["phase"]:
        pag_dbs = config["phase"]["delta_beta"]
        if isinstance(pag_dbs, str):
            pag_dbs = utils.retrieve_lst_of_value_from_str(pag_dbs, type_=float)
        if len(pag_dbs) == 0:
            pag_dbs = (None,)
    else:
        pag_dbs = (None,)

    # by default add the slice 'None' which is the slice for the volume
    slices.append(None)
    nabu_config = get_nabu_config(config=config)
    res = []
    for slice_ in slices:
        for pag_db in pag_dbs:
            local_config = copy.deepcopy(nabu_config)
            if pag_db is not None:
                local_config["phase"]["delta_beta"] = str(pag_db)
            res.append((local_config, slice_))
    return tuple(res)


class SingleSliceRunner(_NabuBaseReconstructor):
    def __init__(
        self,
        scan: TomwerScanBase,
        config: dict,
        dry_run: bool,
        slice_index: int | str | None,
        axis: NabuPlane,
        target: Target,
        cluster_config: dict | None,
        process_name: str,
        add_to_latest_reconstructions: bool = True,
    ) -> None:
        super().__init__(
            scan=scan,
            dry_run=dry_run,
            target=target,
            cluster_config=cluster_config,
            process_name=process_name,
            axis=axis,
        )
        self._slice_index = slice_index
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dictionary not {type(dict)}")
        self._config = config
        self._add_to_latest_reconstructions = add_to_latest_reconstructions

    @property
    def slice_index(self):
        return self._slice_index

    @property
    def config(self):
        return self._config

    @property
    def add_to_latest_reconstructions(self):
        return self._add_to_latest_reconstructions

    @property
    def processed_data_folder_name(self):
        """return the specific processed folder name associated to this type of reconstruction."""
        return PROCESS_FOLDER_RECONSTRUCTED_SLICES

    @docstring(_NabuBaseReconstructor)
    def only_create_config_file(self):
        return self.slice_index is None

    @docstring(_NabuBaseReconstructor)
    def run(self) -> Iterable:
        """
        If the target is local will wait for the reconstruction to be finish to return

        :raise: TIMEOUT_SLURM_JOB_SUBMISSION if not all workers spwan
        """
        if isinstance(self.slice_index, str):
            self._slice_index = slice_index_to_int(
                slice_index=self.slice_index,
                scan=self.scan,
                axis=self.axis,
            )
        elif (
            isinstance(self.slice_index, float)
            and int(self.slice_index) == self.slice_index
        ):
            self._slice_index = int(self.slice_index)
        elif not isinstance(self.slice_index, (int, type(None))):
            raise TypeError(
                f"slice index is expected to an int or 'middle' or None and not {type(self.slice_index)}"
            )
        config_complete = _extract_nabuconfig_keyvals(nabu_fullfield_default_config)
        config_complete["dataset"] = self.scan.get_nabu_dataset_info()
        for key in config_complete.keys():
            if key in self.config:
                config_complete[key].update(self.config[key])
        config = config_complete

        config["resources"] = config.get("resources", {})
        config["resources"]["method"] = "local"

        # force overwrite results
        if "output" not in config:
            config["output"] = {}

        config["output"].update({"overwrite_results": 1})

        config, cfg_folder = self._treateOutputSliceConfig(config)
        # the policy is to save nabu .cfg file at the same location as the
        # force overwrite results
        if self.slice_index is not None:
            if self.axis is NabuPlane.YZ:
                config["reconstruction"]["start_x"] = self.slice_index
                config["reconstruction"]["end_x"] = self.slice_index
            elif self.axis is NabuPlane.XZ:
                config["reconstruction"]["start_y"] = self.slice_index
                config["reconstruction"]["end_y"] = self.slice_index
            elif self.axis is NabuPlane.XY:
                config["reconstruction"]["start_z"] = self.slice_index
                config["reconstruction"]["end_z"] = self.slice_index
            else:
                raise ValueError(
                    f"self.axis has an invalid value: {self.axis} when expected to be in {[item.value for item in NabuPlane]}"
                )

        if self.slice_index is not None:
            os.makedirs(config["output"]["location"], exist_ok=True)

        name = (
            config["output"]["file_prefix"] + nabu_settings.NABU_CONFIG_FILE_EXTENSION
        )
        if not isinstance(self.scan, EDFTomoScan):
            name = "_".join((self.scan.entry.lstrip("/"), name))
        conf_file = os.path.join(cfg_folder, name)

        _logger.info(f"{self.scan}: create {conf_file}")
        file_format = config["output"]["file_format"]
        update_nabu_config_for_tiff_3d(config)
        # add some tomwer metadata and save the configuration
        # note: for now the section is ignored by nabu but shouldn't stay that way
        with utils.TomwerInfo(config) as config_to_dump:
            generate_nabu_configfile(
                conf_file,
                nabu_fullfield_default_config,
                config=config_to_dump,
                options_level="advanced",
            )

        return tuple(
            [
                self._process_config(
                    config_to_dump=config_to_dump,
                    config_file=conf_file,
                    info="nabu slice reconstruction",
                    file_format=file_format,
                    process_name=self.process_name,
                ),
            ]
        )

    @docstring(_NabuBaseReconstructor)
    def _get_futures_slurm_callback(self, config_to_dump):
        if self.add_to_latest_reconstructions:
            # add callback to set slices reconstructed urls
            class CallBack:
                # we cannot create a future directly because distributed enforce
                # the callback to have a function signature with only the future
                # as single parameter.
                def __init__(self, f_partial, scan) -> None:
                    self.f_partial = f_partial
                    self.scan = scan

                def process(self, fn):
                    if fn.done() and not (fn.cancelled() or fn.exception()):
                        # update reconstruction urls only if processing succeed.
                        recons_urls = self.f_partial()
                        self.scan.add_latest_reconstructions(recons_urls)

            file_format = from_nabu_config_to_file_format(config_to_dump)
            callback = functools.partial(
                utils.get_recons_volume_identifier,
                file_prefix=config_to_dump["output"]["file_prefix"],
                location=config_to_dump["output"]["location"],
                file_format=file_format,
                scan=self.scan,
                slice_index=None,
                axis=self.axis,
            )

            return (CallBack(callback, self.scan),)
        else:
            return super()._get_futures_slurm_callback(config_to_dump)

    @staticmethod
    def get_file_basename_reconstruction(
        scan,
        pag,
        ctf,
        db,
        slice_index: str | int,
        axis: NabuPlane,
    ):
        axis = NabuPlane.from_value(axis)
        if pag:
            assert db is not None, "if paganin defined, db should not be None"
        if slice_index is not None:
            slice_index = slice_index_to_int(slice_index, scan=scan, axis=axis)

        assert type(db) in (int, type(None))
        if isinstance(scan, NXtomoScan):
            basename, _ = os.path.splitext(scan.master_file)
            basename = os.path.basename(basename)
            try:
                with open_hdf5(scan.master_file) as h5f:
                    if len(h5f.keys()) > 1:
                        # if there is more than one entry in the file append the entry name to the file basename
                        basename = "_".join((basename, scan.entry.lstrip("/")))
            except Exception:
                pass
        else:
            basename = os.path.basename(scan.path)
        if slice_index is None:
            if pag:
                return "_".join((basename + "pag", "db" + str(db).zfill(4)))
            elif ctf:
                return "_".join((basename + "ctf", "db" + str(db).zfill(4)))
            else:
                return basename
        else:
            if pag:
                return "_".join(
                    (
                        basename + "slice_pag",
                        str(slice_index).zfill(6),
                        "db" + str(db).zfill(4),
                        "plane",
                        axis.value,
                    )
                )
            elif ctf:
                return "_".join(
                    (
                        basename + "slice_ctf",
                        str(slice_index).zfill(6),
                        "db" + str(db).zfill(4),
                        "plane",
                        axis.value,
                    )
                )
            else:
                return "_".join(
                    (
                        basename + "slice",
                        str(slice_index).zfill(6),
                        "plane",
                        axis.value,
                    )
                )

    @docstring(_NabuBaseReconstructor)
    def _get_file_basename_reconstruction(self, pag, db, ctf, axis):
        """

        :param pag: is it a paganin reconstruction
        :param db: delta / beta parameter
        :return: basename of the file reconstructed (without any extension)
        """
        return self.get_file_basename_reconstruction(
            scan=self.scan,
            db=db,
            pag=pag,
            slice_index=self.slice_index,
            ctf=ctf,
            axis=axis,
        )


def run_single_slice_reconstruction(
    scan,
    nabu_config,
    dry_run,
    slice_index: int | str | None,
    process_id: int | None = None,
    cluster_config: dict | None = None,
    add_to_latest_reconstructions=True,
    instantiate_class_only=False,
    axis: NabuPlane = NabuPlane.XY,
) -> ResultsRun | None:
    """
    # TODO: might need something like a context or an option "keep" slice in memory

    :param scan:
    :param nabu_config: configuration of nabu process
    :param cluster_config: configuration of cluster (slurm-cluster only for now)
    :param dry_run:
    :param slice_index: slice index to reconstruct.
                                             If str should be "middle"
    :param local:
    :param stdout: file to redirect stdout
    :param stderr: file to redirect stderr
    :param add_to_latest_reconstructions: if true add reconstructed slice to the latest reconstruction.
                                               We wan't to avoid this treatment for saaxis and sadeltebeta for example
    :param instantiate_class_only: if we don't want to run the SingleSliceRunner but only return them. Use case: we want to keep a hand on processing and it can be cancelled
    :return: result of the slice reconstruction if succeed to launch it.
    """
    # TODO: remove local from the function signature
    target = Target.SLURM if cluster_config not in ({}, None) else Target.LOCAL
    axis = NabuPlane.from_value(axis)
    # FIXEME: nabu fails if outer_circle activated and if the axis != z
    if axis != NabuPlane.XY and nabu_config.get("reconstruction", {}).get(
        "clip_outer_circle", False
    ):
        nabu_config["reconstruction"]["clip_outer_circle"] = False

    if process_id is not None:
        try:
            process_name = ProcessManager().get_process(process_id=process_id).name
        except KeyError:
            process_name = "unknow"
    else:
        process_name = ""

    slice_reconstructor = SingleSliceRunner(
        scan=scan,
        config=nabu_config,
        dry_run=dry_run,
        slice_index=slice_index,
        axis=axis,
        target=target,
        cluster_config=cluster_config,
        add_to_latest_reconstructions=add_to_latest_reconstructions,
        process_name=process_name,
    )
    if instantiate_class_only:
        return slice_reconstructor

    try:
        results = slice_reconstructor.run()
    except TimeoutError as e:
        _logger.error(e)
        return None
    else:
        assert len(results) == 1, "only one slice should be reconstructed"
        return results[0]


class NabuSliceMode(_Enum):
    MIDDLE = "middle"
    OTHER = "other"

    @staticmethod
    def getSlices(slices, scan, axis=NabuPlane.XY) -> tuple:
        res = []
        try:
            mode = NabuSliceMode(slices)
        except ValueError:
            try:
                res = utils.retrieve_lst_of_value_from_str(slices, type_=int)
            except Exception:
                pass
        else:
            if mode == mode.MIDDLE:
                axis = NabuPlane(axis)
                if axis is NabuPlane.XY:
                    n_slice = scan.dim_2 or 2048
                elif axis in (NabuPlane.YZ, NabuPlane.XZ):
                    n_slice = scan.dim_1 or 2048
                else:
                    raise NotImplementedError(f"unknow axis {axis}")
                res.append(n_slice // 2)
            else:
                raise ValueError(
                    "there should be only two ways of defining "
                    "slices: middle one or other, by giving "
                    "an unique value or a list or a tuple"
                )
        return tuple(res)


class NabuSlices(NabuSlicesTask):
    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        deprecated_warning(
            name="tomwer.core.process.reconstruction.nabu.nabuslices.Nabuslices",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="NabuSlicesTask",
        )
        super().__init__(process_id, varinfo, inputs, node_id, node_attrs, execinfo)
