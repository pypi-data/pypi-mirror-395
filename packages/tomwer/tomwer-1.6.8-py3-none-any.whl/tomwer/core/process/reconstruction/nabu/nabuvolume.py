from __future__ import annotations

import copy
import functools
import logging
import os
from typing import Iterable

from nabu import version as nabu_version
from nabu.pipeline.config import generate_nabu_configfile
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from processview.core.manager.manager import ProcessManager, DatasetState
from processview.core.superviseprocess import SuperviseProcess

from silx.io.utils import open as open_hdf5
from tomwer.core.utils.deprecation import deprecated_warning

from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.process.reconstruction.nabu.plane import NabuPlane
from tomwer.core.process.reconstruction.nabu.utils import (
    from_nabu_config_to_file_format,
    update_nabu_config_for_tiff_3d,
)
from tomwer.core.process.task import Task
from tomwer.core.process.drac.processeddataset import DracReconstructedVolumeDataset
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.dictutils import concatenate_dict
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.utils import docstring
from tomwer.io.utils import format_stderr_stdout
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_RECONSTRUCTED_VOLUMES,
)

from . import settings, utils
from .nabucommon import ResultsLocalRun, ResultSlurmRun, _NabuBaseReconstructor
from .target import Target

_logger = logging.getLogger(__name__)


def run_volume_reconstruction(
    scan: TomwerScanBase,
    config: dict,
    dry_run: bool,
    process_id: int | None = None,
) -> tuple:
    """
    Run a volume reconstruction. Scan need to have reconstruction parameters for nabu.

    Behavior: will clear link to the last volume reconstructed

    :param process_id: optional process id

    :return: succeed, stdouts, stderrs, configs, future_scan
    """

    if scan.nabu_recons_params in ({}, None):
        raise ValueError(
            "no configuration provided. You should run a "
            "reconstruction from nabuslices first."
        )
    cluster_config = config.pop("cluster_config", None)
    if cluster_config == {}:
        cluster_config = None
    elif isinstance(cluster_config, SlurmClusterConfiguration):
        cluster_config = cluster_config.to_dict()

    if cluster_config is None:
        target = Target.LOCAL
    else:
        target = Target.SLURM

    # # beam shape is not directly used by nabu (uses ctf_geometry directly)
    # config.get("phase", {}).pop("beam_shape", None)

    # config_volume = copy.copy(config)
    # config_nabu_slices = copy.deepcopy(scan.nabu_recons_params)
    # if "tomwer_slices" in config_nabu_slices:
    #     del config_nabu_slices["tomwer_slices"]

    # if "phase" in config_nabu_slices and "delta_beta" in config_nabu_slices["phase"]:
    #     pag_dbs = config_nabu_slices["phase"]["delta_beta"]
    #     if isinstance(pag_dbs, str):
    #         pag_dbs = utils.retrieve_lst_of_value_from_str(pag_dbs, type_=float)
    #     if len(pag_dbs) > 1:
    #         raise ValueError(
    #             "Several value of delta / beta found for volume reconstruction"
    #         )
    # scan.clear_latest_vol_reconstructions()

    if process_id is not None:
        try:
            process_name = ProcessManager().get_process(process_id=process_id).name
        except KeyError:
            process_name = "unknow"
    else:
        process_name = ""

    volume_reconstructor = VolumeRunner(
        scan=scan,
        config_nabu=config,
        cluster_config=cluster_config,
        dry_run=dry_run,
        target=target,
        process_name=process_name,
    )
    try:
        results = volume_reconstructor.run()
    except TimeoutError as e:
        _logger.error(e)
        return None
    else:
        assert len(results) == 1, "only one volume should be reconstructed"
        res = results[0]
        # tag latest reconstructions
        if isinstance(res, ResultsLocalRun) and res.results_identifiers is not None:
            scan.set_latest_vol_reconstructions(res.results_identifiers)
        # create future if needed
        if isinstance(res, ResultSlurmRun):
            future_tomo_obj = FutureTomwerObject(
                tomo_obj=scan,
                futures=tuple(res.future_slurm_jobs),
                process_requester_id=process_id,
            )

        else:
            future_tomo_obj = None
        succeed = res.success
        stdouts = (
            [
                res.std_out,
            ]
            if hasattr(res, "std_out")
            else []
        )
        stderrs = (
            [
                res.std_err,
            ]
            if hasattr(res, "std_err")
            else []
        )
        configs = (
            [
                res.config,
            ]
            if res is not None
            else []
        )

        return succeed, stdouts, stderrs, configs, future_tomo_obj


class VolumeRunner(_NabuBaseReconstructor):
    """
    Class used to reconstruct a full volume with Nabu.
    Locally or on a cluster.
    """

    EXPECTS_SINGLE_SLICE = False

    def __init__(
        self,
        scan: TomwerScanBase,
        config_nabu,
        cluster_config: dict | None,
        dry_run: bool,
        target: Target,
        process_name: str,
    ) -> None:
        super().__init__(
            scan=scan,
            dry_run=dry_run,
            target=target,
            cluster_config=cluster_config,
            process_name=process_name,
        )
        self._config = config_nabu

    @property
    def configuration(self):
        return self._config

    @property
    def processed_data_folder_name(self):
        """return the specific processed folder name associated to this type of reconstruction."""
        return PROCESS_FOLDER_RECONSTRUCTED_VOLUMES

    @docstring(_NabuBaseReconstructor)
    def run(self) -> Iterable:
        dataset_params = self.scan.get_nabu_dataset_info()
        if "dataset" in self.configuration:
            dataset_params.update(self.configuration["dataset"])
        self.configuration["dataset"] = dataset_params

        self.configuration["resources"] = self.configuration.get("resources", {})
        self.configuration["resources"]["method"] = "local"

        # force overwrite results
        if "output" not in self.configuration:
            self.configuration["output"] = {}
        config_slices, cfg_folder = self._treateOutputConfig(self.configuration)

        # force overwriting results
        config_slices["output"].update({"overwrite_results": 1})

        # check and clamp `start_z` and `end_z`
        if "reconstruction" in self.configuration:
            for key in ("start_z", "end_z"):
                value = config_slices["reconstruction"].get(key)
                if value is None:
                    continue

                value = int(value)
                if self.scan.dim_2 is not None and value >= self.scan.dim_2:
                    _logger.warning(
                        f"{key} > max_size (radio height: {self.scan.dim_2}). Set it to -1 (maximum)"
                    )
                    value = -1
                config_slices["reconstruction"][key] = value

        name = (
            config_slices["output"]["file_prefix"] + settings.NABU_CONFIG_FILE_EXTENSION
        )
        if not isinstance(self.scan, EDFTomoScan):
            name = "_".join((self.scan.entry.lstrip("/"), name))
        conf_file = os.path.join(cfg_folder, name)
        _logger.info(f"{self.scan}: create {conf_file}")

        # make sure output location exists
        os.makedirs(config_slices["output"]["location"], exist_ok=True)

        file_format = config_slices["output"]["file_format"]
        update_nabu_config_for_tiff_3d(config_slices)
        # add some tomwer metadata and save the configuration
        # note: for now the section is ignored by nabu but shouldn't stay that way
        with utils.TomwerInfo(config_slices) as config_to_dump:
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
                        info="nabu volume reconstruction",
                        file_format=file_format,
                        process_name=self.process_name,
                    )
                ]
            )

    @docstring(_NabuBaseReconstructor)
    def _get_futures_slurm_callback(self, config_to_dump) -> tuple:
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
                    recons_identifiers = self.f_partial()
                    self.scan.add_latest_vol_reconstructions(recons_identifiers)

        file_format = from_nabu_config_to_file_format(config_to_dump)

        callback = functools.partial(
            utils.get_recons_volume_identifier,
            file_prefix=config_to_dump["output"]["file_prefix"],
            location=config_to_dump["output"]["location"],
            file_format=file_format,
            scan=self.scan,
            slice_index=None,
            axis=NabuPlane.XY,  # for volume we always reconstruct along XY plane
        )

        return (CallBack(callback, self.scan),)

    def _treateOutputConfig(self, config) -> tuple:
        """

        :return: (nabu config dict, nabu extra options)
        """
        config = copy.deepcopy(config)
        config, nabu_cfg_folder = super()._treateOutputSliceConfig(config)
        os.makedirs(config["output"]["location"], exist_ok=True)

        # adapt config_s to specific volume treatment
        if "postproc" in config:
            config["postproc"] = config["postproc"]

        # make sure start_[x] and end_[x] come from config
        for key in ("start_x", "end_x", "start_y", "end_y", "start_z", "end_z"):
            if key in config:
                config["reconstruction"][key] = config[key]
                del config[key]

        return config, nabu_cfg_folder

    @docstring(_NabuBaseReconstructor)
    def _get_file_basename_reconstruction(self, pag, db, ctf, axis):
        """

        :param pag: is it a Paganin reconstruction
        :param db: delta / beta parameter
        :param axis: axis over which the reconstruction goes. For volume always expected to be z. So ignored in the function
        :return: basename of the file reconstructed (without any extension)
        """
        assert type(db) in (int, type(None))
        assert not pag == ctf == True, "cannot ask for both pag and ctf active"
        if isinstance(self.scan, NXtomoScan):
            basename, _ = os.path.splitext(self.scan.master_file)
            basename = os.path.basename(basename)
            try:
                # if there is more than one entry in the file append the entry name to the file basename
                with open_hdf5(self.scan.master_file) as h5f:
                    if len(h5f.keys()) > 1:
                        basename = "_".join((basename, self.scan.entry.strip("/")))
            except Exception:
                pass
        else:
            basename = os.path.basename(self.scan.path)

        if pag:
            return "_".join((basename + "pag", "db" + str(db).zfill(4), "vol"))
        elif ctf:
            return "_".join((basename + "ctf", "db" + str(db).zfill(4), "vol"))
        else:
            return "_".join((basename, "vol"))


class NabuVolumeTask(
    Task,
    SuperviseProcess,
    input_names=("data", "nabu_params"),
    output_names=(
        "data",
        "volumes",
        "future_tomo_obj",
        "data_portal_processed_datasets",
    ),
    optional_input_names=(
        "dry_run",
        "nabu_extra_params",  # some parameter that must update 'nabu_params' before launching the reconstruction. Such as z range...
        "serialize_output_data",
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
        self._dry_run = inputs.get("dry_run", False)
        self._current_processing = None

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            self.outputs.data = None
            return

        # update scan reconstruction parameters used
        nabu_params = concatenate_dict(
            copy.deepcopy(self.inputs.nabu_params),
            self.get_input_value("nabu_extra_params", dict()),
        )
        scan.nabu_recons_params = nabu_params
        scan.clear_latest_vol_reconstructions()

        cluster_config = nabu_params.pop("cluster_config", None)
        if cluster_config == {}:
            cluster_config = None
        elif isinstance(cluster_config, SlurmClusterConfiguration):
            cluster_config = cluster_config.to_dict()

        if "tomwer_slices" in nabu_params:
            del nabu_params["tomwer_slices"]

        if "phase" in nabu_params and "delta_beta" in nabu_params["phase"]:
            pag_dbs = nabu_params["phase"]["delta_beta"]
            if isinstance(pag_dbs, str):
                pag_dbs = utils.retrieve_lst_of_value_from_str(pag_dbs, type_=float)
            if len(pag_dbs) > 1:
                raise ValueError(
                    "Several value of delta / beta found for volume reconstruction"
                )

        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(f"input type {scan} is not managed")

        if cluster_config is None:
            target = Target.LOCAL
        else:
            target = Target.SLURM

        state = None
        details = None
        try:
            self._current_processing = VolumeRunner(
                scan=scan,
                config_nabu=nabu_params,
                cluster_config=cluster_config,
                dry_run=self._dry_run,
                target=target,
                process_name=self.program_name,
            )
            res = self._current_processing.run()[0]
        except Exception as e:
            _logger.error(f"Failed to process {scan}. Error is {e}")
            state = DatasetState.FAILED
            details = None
            future_tomo_obj = None
        else:
            # tag latest reconstructions
            if isinstance(res, ResultsLocalRun) and res.results_identifiers is not None:
                scan.set_latest_vol_reconstructions(res.results_identifiers)
            # create future if needed
            if isinstance(res, ResultSlurmRun):
                future_tomo_obj = FutureTomwerObject(
                    tomo_obj=scan,
                    futures=tuple(res.future_slurm_jobs),
                    process_requester_id=self.process_id,
                )

            else:
                future_tomo_obj = None

            if self._cancelled:
                state = DatasetState.CANCELLED
                details = "cancelled by user"
                _logger.info(f"Slices computation for {scan} cancelled")
            else:
                succeed = res.success
                stdouts = (
                    [
                        res.std_out,
                    ]
                    if hasattr(res, "std_out")
                    else []
                )
                stderrs = (
                    [
                        res.std_err,
                    ]
                    if hasattr(res, "std_err")
                    else []
                )

                if not succeed:
                    mess = f"Volume computed for {scan} failed."
                    _logger.processFailed(mess)
                    state = DatasetState.FAILED
                else:
                    mess = f"Volume computed for {scan}."
                    _logger.processSucceed(mess)
                    state = DatasetState.SUCCEED

                # format stderr and stdout
                elmts = [
                    format_stderr_stdout(stderr=stderr, stdout=stdout)
                    for stderr, stdout in zip(stderrs, stdouts)
                ]
                elmts.insert(0, mess)
                details = "\n".join(elmts)
        finally:
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
        self.outputs.volumes = scan.latest_vol_reconstructions
        self.outputs.future_tomo_obj = future_tomo_obj

        # build screenshots
        data_portal_processed_datasets = []
        if scan.latest_vol_reconstructions is not None:
            for volume_id in scan.latest_vol_reconstructions:
                try:
                    volume = VolumeFactory.create_tomo_object_from_identifier(
                        identifier=volume_id
                    )
                except Exception as e:
                    _logger.error(
                        f"Fail to build volume from {volume_id}. Error is {e}"
                    )
                else:
                    icatReconstructedDataset = DracReconstructedVolumeDataset(
                        tomo_obj=volume,
                        source_scan=scan,
                    )
                    data_portal_processed_datasets.append(icatReconstructedDataset)

        self.outputs.data_portal_processed_datasets = tuple(
            data_portal_processed_datasets
        )

    def set_configuration(self, configuration: dict) -> None:
        Task.set_configuration(self, configuration=configuration)
        if "dry_run" in configuration:
            self.set_dry_run(bool(configuration["dry_run"]))

    @staticmethod
    def program_name():
        return "nabu-volume"

    @staticmethod
    def program_version():
        return nabu_version

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    @property
    def dry_run(self):
        return self._dry_run

    def cancel(self):
        """
        stop current processing
        """
        self._cancelled = True
        if self._current_processing is not None:
            self._current_processing.cancel()


class NabuVolume(NabuVolumeTask):
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
            name="tomwer.core.process.reconstruction.nabu.nabuvolume.NabuVolume",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="NabuVolumeTask",
        )
        super().__init__(process_id, varinfo, inputs, node_id, node_attrs, execinfo)
