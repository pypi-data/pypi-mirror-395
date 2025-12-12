"""contain the SAAxisProcess. Half automatic center of rotation calculation"""

from __future__ import annotations

import logging
import os
import h5py

import numpy
from multiprocessing import Pool
from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.io.url import DataUrl
from silx.io.utils import h5py_read_dataset

from tomwer.core.utils.deprecation import deprecated_warning
from tomoscan.io import HDF5File

import tomwer.version
from tomwer.core.process.reconstruction.axis import AxisRP
from tomwer.core.process.reconstruction.nabu.nabuscores import (
    run_nabu_multicor,
)
from tomwer.core.process.reconstruction.nabu.nabuslices import (
    interpret_tomwer_configuration,
)
from tomwer.core.process.reconstruction.scores import (
    ComputedScore,
    apply_roi,
    compute_score,
    get_disk_mask_radius,
)
from tomwer.core.process.reconstruction.scores.params import ScoreMethod
from tomwer.core.process.reconstruction.utils.cor import relative_pos_to_absolute
from tomwer.core.process.task import Task
from tomwer.core.process import utils as core_utils
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils import logconfig
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.utils.slurm import is_slurm_available
from tomwer.core.process.reconstruction.nabu.utils import update_nabu_config_for_tiff_3d

from tomwer.io.utils.h5pyutils import EntryReader
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.io.utils.utils import get_slice_data
from tomwer.io.utils import format_stderr_stdout
from tomwer.core.process.reconstruction.nabu.nabucommon import (
    ResultsLocalRun,
    ResultSlurmRun,
    ResultsWithStd,
)
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.process.reconstruction.saaxis.params import ReconstructionMode
from tomwer.core.process.reconstruction.nabu.utils import (
    get_multi_cor_recons_volume_identifiers,
    get_nabu_multicor_file_prefix,
)

from .params import SAAxisParams

_logger = logging.getLogger(__name__)


DEFAULT_RECONS_FOLDER = "multi_cor_results"


def one_slice_several_cor(
    scan,
    configuration: dict,
    process_id: int | None = None,
) -> tuple:
    """
    Run a slice reconstruction using nabu per Center Of Rotation (cor) provided
    Then for each compute a score (quality) of the center of rotation

    .. warning:: if target if the slurm cluster this will wait for the processing to be done to return the result.
                 as this function is returning the result of the score process on reconstructed slices

    :param scan:
    :param configuration: nabu reconstruction parameters (can include 'slurm-cluster' key defining the slurm configuration)
    :param process_id: process id
    :return: cor_reconstructions, outs, errs
             cor_reconstructions is a dictionary of cor as key and a tuple
             (url, score) as value
    """
    task = SAAxisTask(
        process_id=process_id,
        inputs={
            "data": scan,
            "sa_axis_params": configuration,
            "serialize_output_data": False,
        },
    )
    task.run()
    return (
        task.outputs.scores,
        task.outputs.std_out,
        task.outputs.std_err,
        task.outputs.rois,
    )


class SAAxisTask(
    Task,
    SuperviseProcess,
    input_names=("data", "sa_axis_params"),
    output_names=("data", "best_cor"),
    optional_input_names=(
        "dry_run",
        "dump_roi",
        "dump_process",
        "serialize_output_data",
        "compute_scores",  # for GUI we want to post pone the score calculation
        "pool_size",
    ),
):
    """
    Main process to launch several reconstruction of a single slice with
    several Center Of Rotation (cor) values

    As the saaxis is integrating the score calculation we will never get a future_tomo_scan as output
    """

    DEFAULT_POOL_SIZE = 10

    def __init__(
        self, process_id=None, inputs=None, varinfo=None, node_attrs=None, execinfo=None
    ):
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        SuperviseProcess.__init__(self, process_id=process_id)
        self._dry_run = inputs.get("dry_run", False)
        self._dump_process = inputs.get("dump_process", True)
        self._dump_roi = inputs.get("dump_roi", False)
        self._std_outs = tuple()
        self._std_errs = tuple()
        self._current_processing = None
        self._cancelled = False

    @property
    def std_outs(self):
        return self._std_outs

    @property
    def std_errs(self):
        return self._std_errs

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    @property
    def dry_run(self):
        return self._dry_run

    @property
    def dump_roi(self):
        return self._dump_roi

    @dump_roi.setter
    def dump_roi(self, dump):
        self._dump_roi = dump

    @staticmethod
    def autofocus(scan) -> float | None:
        scores = scan.saaxis_params.scores
        if scores is None:
            return
        score_method = scan.saaxis_params.score_method
        best_cor, best_score = None, 0
        for cor, (_, score_cls) in scores.items():
            if score_cls is None:  # if score calculation failed
                continue
            score = score_cls.get(score_method)
            if score is None:
                continue
            if score > best_score:
                best_cor, best_score = cor, score
        scan.saaxis_params.autofocus = best_cor
        if scan.axis_params is None:
            # create parameter if needed because will set it once he find the best cor
            scan.axis_params = AxisRP()
        scan.axis_params.frame_width = scan.dim_1
        scan.axis_params.set_relative_value(best_cor)
        return best_cor

    def _config_preprocessing(
        self, scan, config, file_format, output_dir, cluster_config
    ):
        """convert general configuration to nabu - single reconstruction - configuration"""
        nabu_configurations = interpret_tomwer_configuration(config, scan=None)
        if len(nabu_configurations) == 0:
            raise RuntimeWarning(
                "Unable to get a valid nabu configuration for " "reconstruction."
            )
        elif len(nabu_configurations) > 1:
            _logger.warning(
                "Several configuration found for nabu (you probably "
                "ask for several delta/beta value or several slices). "
                "Picking the first one."
            )

        # work on file name...
        if output_dir is None:
            output_dir = os.path.join(scan.path, DEFAULT_RECONS_FOLDER)

        nabu_configuration = nabu_configurations[0][0]
        if cluster_config == {}:
            cluster_config = None
        is_cluster_job = cluster_config is not None
        if is_cluster_job and not is_slurm_available():
            raise ValueError(
                "job on cluster requested but no access to slurm cluster found"
            )

        # handle reconstruction section
        if "reconstruction" not in nabu_configuration:
            nabu_configuration["reconstruction"] = {}
        nabu_configuration["reconstruction"]["rotation_axis_position"] = ""
        # handle output section
        if "output" not in nabu_configuration:
            nabu_configuration["output"] = {}
        nabu_configuration["output"]["location"] = output_dir
        nabu_configuration["output"]["file_format"] = file_format
        update_nabu_config_for_tiff_3d(nabu_configuration)

        # handle resources section
        nabu_configuration["resources"] = nabu_configuration.get("resources", {})
        nabu_configuration["resources"]["method"] = "local"

        return nabu_configuration

    def _run_nabu_multicor(
        self,
        scan,
        nabu_config,
        cors,
        slice_index,
        file_format,
        cluster_config: dict | None,
        dry_run=False,
    ):
        if not (cluster_config is None or isinstance(cluster_config, dict)):
            raise TypeError(
                f"cluster_config is expected to be a dict. Get {type(cluster_config)} instead."
            )
        runner = run_nabu_multicor(
            nabu_config=nabu_config,
            scan=scan,
            cors=cors,
            slice_index=slice_index,
            dry_run=dry_run,
            file_format=file_format,
            cluster_config=cluster_config if cluster_config is not None else None,
            process_id=self.process_id,
            instantiate_classes_only=True,
            output_file_prefix_pattern="cor_{file_name}_{value}",  # as the cor is evolving, create different files to make sure the name will be unique
        )

        future_tomo_obj = None
        recons_urls = dict()
        std_outs = []
        std_errs = []

        self._current_processing = runner
        try:
            result = runner.run()
        except TimeoutError as e:
            _logger.error(e)
        else:
            success = result.success
            if isinstance(result, ResultsWithStd):
                std_outs.append(result.std_out)
                std_errs.append(result.std_err)
            if isinstance(result, ResultsLocalRun):
                recons_urls = {
                    cor: recons for cor, recons in zip(cors, result.results_identifiers)
                }
            if isinstance(result, ResultSlurmRun):
                future_tomo_obj = FutureTomwerObject(
                    tomo_obj=scan,
                    process_requester_id=self.process_id,
                    futures=result.future_slurm_jobs,
                )
        return success, recons_urls, (future_tomo_obj,), std_outs, std_errs

    def _resolve_futures(
        self,
        scan,
        nabu_config,
        slice_index,
        file_format,
        cors,
        cor_reconstructions,
        future_tomo_objs: dict,
        output_dir,
    ):
        """
        in case the task is launching jobs over slurm wait for them to be finished before resuming 'standard processing'
        """
        if output_dir is None:
            output_dir = os.path.join(scan.path, DEFAULT_RECONS_FOLDER)

        file_prefix = get_nabu_multicor_file_prefix(scan)

        for future_tomo_obj in future_tomo_objs:
            if self._cancelled:
                break

            if future_tomo_obj is None:
                continue

            future_tomo_obj.results()
            if future_tomo_obj.cancelled() or future_tomo_obj.exceptions():
                continue

            for cor in cors:
                cor_nabu_ref = relative_pos_to_absolute(
                    relative_pos=cor,
                    det_width=scan.dim_1,
                )
                volume_identifiers = get_multi_cor_recons_volume_identifiers(
                    scan=scan,
                    slice_index=slice_index,
                    location=nabu_config["output"]["location"],
                    file_prefix=file_prefix,
                    file_format=file_format,
                    cors=(cor_nabu_ref,),
                )
                volume_identifier = volume_identifiers.get(cor_nabu_ref, None)
                if volume_identifier is None:
                    _logger.warning(
                        f"failed to load volume for {cor}. Something went wrong on slurm submission job"
                    )
                cor_reconstructions[cor] = volume_identifier

    def _post_processing(self, scan, slice_index, cor_reconstructions: dict):
        """
        compute score along the different slices

        :param cor_reconstructions: key is expected to be a float with the cor value and the value is expected to be a volume identifier (volume with a single frame)
        """
        post_processing = _PostProcessing(
            slice_index=slice_index,
            scan=scan,
            cor_reconstructions=cor_reconstructions,
            pool_size=self.get_input_value("pool_size", self.DEFAULT_POOL_SIZE),
        )
        post_processing._cancelled = self._cancelled
        self._current_processing = post_processing
        return post_processing.run()

    def _compute_mess_details(self, mess=""):
        """
        util to join a message and nabu std err and std out
        """
        nabu_logs = []
        for std_err, std_out in zip(self._std_errs, self.std_outs):
            nabu_logs.append(format_stderr_stdout(stdout=std_out, stderr=std_err))
        self._nabu_log = nabu_logs
        nabu_logs.insert(0, mess)
        return "\n".join(nabu_logs)

    @staticmethod
    def _preprocess_slice_index(slice_index, mode: ReconstructionMode):
        if isinstance(slice_index, str):
            if not slice_index == "middle":
                raise ValueError(f"slice index {slice_index} not recognized")
            else:
                return slice_index
        elif not len(slice_index) == 1:
            raise ValueError(f"{mode.value} mode only manage one slice")
        else:
            return list(slice_index.values())[0]

    def get_output_dir(self, params: SAAxisParams, scan: TomwerScanBase):
        output_dir = params.output_dir or None
        if output_dir is None:
            output_dir = (
                params.nabu_recons_params.get("output", {}).get("location", None)
                or None
            )
            if output_dir is None:
                output_dir = os.path.join(scan.path, DEFAULT_RECONS_FOLDER)
        return output_dir

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            self.outputs.data = None
            return
        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed")
        # TODO: look and update if there is some nabu reconstruction
        # or axis information to be used back
        configuration = self.inputs.sa_axis_params
        params = SAAxisParams.from_dict(configuration)
        # insure output dir is created
        params.output_dir = self.get_output_dir(params=params, scan=scan)
        if not os.path.exists(params.output_dir):
            os.makedirs(params.output_dir)

        # try to find an estimated cor
        #  from a previously computed cor
        if params.estimated_cor is None and scan.axis_params is not None:
            relative_cor = scan.axis_params.relative_cor_value
            if relative_cor is not None and numpy.issubdtype(
                type(relative_cor), numpy.number
            ):
                params.estimated_cor = relative_cor
                _logger.info(
                    f"{scan}: set estimated cor from previously computed cor ({params.estimated_cor})"
                )
        #  from scan.x_rotation_axis_pixel_position
        if (
            params.estimated_cor is None
            and scan.x_rotation_axis_pixel_position is not None
        ):
            params.estimated_cor = scan.x_rotation_axis_pixel_position
            _logger.info(
                f"{scan}: set estimated cor from motor position ({params.estimated_cor})"
            )
        if scan.dim_1 is not None:
            params.image_width = scan.dim_1
        scan.saaxis_params = params

        mode = ReconstructionMode(params.mode)
        if mode is not ReconstructionMode.VERTICAL:
            raise ValueError(f"{mode} is not handled for now")

        nabu_config = configuration.get("nabu_params", {})
        nabu_output_config = configuration.get("output", {})
        file_format = nabu_output_config.get("file_format", "hdf5")
        slice_index = self._preprocess_slice_index(
            params.slice_indexes,
            mode=mode,
        )
        cluster_config = params.cluster_config
        dry_run = self._dry_run

        # step one: complete nabu configuration(s)
        nabu_config = self._config_preprocessing(
            scan=scan,
            config=nabu_config,
            file_format=file_format,
            output_dir=params.output_dir,
            cluster_config=cluster_config,
        )
        # step 2: run reconstructions
        cors_res = {}
        rois = {}

        try:
            (
                _,
                cor_reconstructions,
                future_tomo_objs,
                self._std_outs,
                self._std_errs,
            ) = self._run_nabu_multicor(
                scan=scan,
                nabu_config=nabu_config,
                cors=tuple(params.cors),
                slice_index=slice_index,
                file_format=file_format,
                cluster_config=cluster_config,
                dry_run=dry_run,
            )
        except Exception as e:
            _logger.error(e)
            mess = f"sa-axis -nabu- computation for {str(scan)} failed."
            state = DatasetState.FAILED
        else:
            # step 3: wait for future if any
            self._resolve_futures(
                scan=scan,
                nabu_config=nabu_config,
                slice_index=slice_index,
                file_format=file_format,
                cor_reconstructions=cor_reconstructions,
                cors=tuple(params.cors),
                future_tomo_objs=future_tomo_objs,
                output_dir=params.output_dir,
            )

            # step 4: run post processing (compute score for each slice)
            if self.get_input_value("compute_scores", True):
                try:
                    cors_res, rois = self._post_processing(
                        scan=scan,
                        slice_index=slice_index,
                        cor_reconstructions=cor_reconstructions,
                    )
                except Exception as e:
                    _logger.error(e)
                    mess = (
                        f"sa-axis -post-processing- computation for {str(scan)} failed."
                    )
                    state = DatasetState.FAILED
                    cors_res = {}
                else:
                    state = DatasetState.WAIT_USER_VALIDATION
                    mess = "sa-axis computation succeeded"
            else:
                cors_res = {}
                state = DatasetState.FAILED
                mess = "couldn't find 'compute_scores'"

        if self._cancelled:
            state = DatasetState.CANCELLED
            mess = "scan cancelled by the user"

        ProcessManager().notify_dataset_state(
            dataset=scan,
            process=self,
            state=state,
            details=self._compute_mess_details(mess),
        )

        scan.saaxis_params.scores = cors_res
        best_relative_cor = self.autofocus(scan=scan)

        if best_relative_cor is not None:
            scan.axis_params.set_relative_value(best_relative_cor)

        self._process_end(scan=scan, cors_res=cors_res, score_rois=rois)

        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan
        self.outputs.best_cor = best_relative_cor

    def _process_end(self, scan, cors_res, score_rois):
        assert isinstance(scan, TomwerScanBase)
        state = ProcessManager().get_dataset_state(
            dataset_id=scan.get_identifier(), process=self
        )
        if state not in (
            DatasetState.CANCELLED,
            DatasetState.FAILED,
            DatasetState.SKIPPED,
        ):
            try:
                extra = {
                    logconfig.DOC_TITLE: self._scheme_title,
                    logconfig.SCAN_ID: str(scan),
                }
                slice_index = self.inputs.sa_axis_params.get("slice_index", None)

                if cors_res is None:
                    info = f"fail to compute cor scores of slice {slice_index} for scan {scan}."
                    _logger.processFailed(info, extra=extra)
                    ProcessManager().notify_dataset_state(
                        dataset=scan,
                        process=self,
                        state=DatasetState.FAILED,
                        details=info,
                    )
                else:
                    info = (
                        f"cor scores of slice {slice_index} for scan {scan} computed."
                    )
                    _logger.processSucceed(info, extra=extra)
                    ProcessManager().notify_dataset_state(
                        dataset=scan,
                        process=self,
                        state=DatasetState.WAIT_USER_VALIDATION,
                        details=info,
                    )
            except Exception as e:
                _logger.error(e)
            else:
                if self._dump_process:
                    self.save_results_to_disk(scan=scan)
                    if self.dump_roi:
                        self.dump_rois(scan, score_rois=score_rois)

    @staticmethod
    def dump_rois(scan, score_rois):
        if scan.saaxis_params.scores in (None, {}):
            return

        process_url = SAAxisTask.get_results_url(scan=scan)

        with HDF5File(process_url.file_path(), mode="w") as h5f:
            nx_process = h5f.require_group(process_url.data_path())
            score_roi_grp = nx_process.require_group("score_roi")
            for cor, roi in score_rois.items():
                score_roi_grp[str(cor)] = roi
                score_roi_grp[str(cor)].attrs["interpretation"] = "image"

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "semi-automatic axis"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "Semi automatic center of rotation / axis calculation"

    @staticmethod
    def get_results_url(scan):
        return DataUrl(
            file_path=scan.get_relative_file(
                os.path.join(DEFAULT_RECONS_FOLDER, "tomwer_saaxis.h5")
            ),
            data_path=scan.entry or "entry",
            scheme="silx",
        )

    @staticmethod
    def save_results_to_disk(scan):
        if scan.saaxis_params.scores in (None, {}):
            return

        saaxis_results_url = SAAxisTask.get_results_url(scan=scan)

        if not os.path.exists(saaxis_results_url.file_path()):
            _logger.error("no result saved")
            return

        # save it to the file
        with HDF5File(saaxis_results_url.file_path(), mode="a") as h5f:
            nx_process = h5f.require_group(saaxis_results_url.data_path())
            if "NX_class" not in nx_process.attrs:
                nx_process.attrs["NX_class"] = "NXprocess"

            results = nx_process.require_group("results")
            for cor, (url, score) in scan.saaxis_params.scores.items():
                results_cor = results.require_group(str(cor))
                for method in ScoreMethod:
                    method_score = score.get(method)
                    if method_score is None:
                        results_cor[method.value] = "None"
                    else:
                        results_cor[method.value] = method_score

                link_path = os.path.relpath(
                    url.file_path(),
                    os.path.dirname(saaxis_results_url.file_path()),
                )
                results_cor["reconstructed_slice"] = h5py.ExternalLink(
                    link_path, url.data_path()
                )

    @staticmethod
    def load_results_from_disk(scan):
        saaxis_results_url = SAAxisTask.get_results_url(scan=scan)

        if saaxis_results_url.file_path() is None or not os.path.exists(
            saaxis_results_url.file_path()
        ):
            _logger.warning(
                "Unable to find process file. Unable to read " "existing processing"
            )
            return None, None

        try:
            with EntryReader(saaxis_results_url) as h5f_entry_node:
                scores = core_utils.get_scores(h5f_entry_node)
                if (
                    "results" in h5f_entry_node
                    and "center_of_rotation" in h5f_entry_node["results"]
                ):
                    selected = h5py_read_dataset(
                        h5f_entry_node["results"]["center_of_rotation"]
                    )
                else:
                    _logger.warning(f"no results found for {scan}")
                    selected = None
                return scores, selected
        except ValueError:
            _logger.warning(f"Data path ({saaxis_results_url.data_path()}) not found")
            return None, None

    def cancel(self):
        """
        stop current processing
        """
        if self._current_processing is not None:
            self._cancelled = True
            self._current_processing.cancel()


class _PostProcessing:
    """class used to run SA-axis post-processing on reconstructed slices"""

    def __init__(self, cor_reconstructions, slice_index, scan, pool_size) -> None:
        self._cor_reconstructions = cor_reconstructions
        self._slice_index = slice_index
        self._scan = scan
        self._cancelled = False
        self.pool_size = pool_size

    @staticmethod
    def compute_score(item: tuple):
        cor, (url, data), mask_disk_radius, cancelled = item
        if cancelled:
            return (None, None), None

        if data is None:
            score = None
            data_roi = None
        else:
            if not isinstance(data, numpy.ndarray):
                raise TypeError(
                    f"data should be a numpy array. Get {type(data)} instead"
                )
            assert data.ndim == 2, f"data should be 2D. Get {data.ndim} instead"
            data_roi = apply_roi(data=data, radius=mask_disk_radius, url=url)

            # move data_roi to [0-1] range
            #  preprocessing: get percentile 0 and 99 from image and
            #  "clean" highest and lowest pixels from it
            min_p, max_p = numpy.percentile(data_roi, (1, 99))
            data_roi_int = data_roi[...]
            data_roi_int[data_roi_int < min_p] = min_p
            data_roi_int[data_roi_int > max_p] = max_p
            data_roi_int = (data_roi_int - min_p) / (max_p - min_p)

            score = ComputedScore(
                tv=compute_score(data=data_roi_int, method=ScoreMethod.TV),
                std=compute_score(data=data_roi_int, method=ScoreMethod.STD),
                tomo_consistency=None,
            )
        return {cor: (url, score)}, {cor: data_roi}

    def run(self):
        datasets = self.load_datasets()
        assert isinstance(datasets, dict)
        mask_disk_radius = get_disk_mask_radius(datasets)
        with Pool(self.pool_size) as pool:
            res = pool.map(
                self.compute_score,
                [
                    (
                        *item,
                        mask_disk_radius,
                        self._cancelled,
                    )
                    for item in datasets.items()
                ],
            )
        scores = {}
        rois = {}
        for mydict in res:
            myscores, myrois = mydict
            scores.update(myscores)
            rois.update(myrois)
        return scores, rois

    @staticmethod
    def _load_dataset(item: tuple):
        cor, volume_identifier = item
        if volume_identifier is None:
            return {cor: (None, None)}

        volume = VolumeFactory.create_tomo_object_from_identifier(volume_identifier)
        urls = tuple(volume.browse_data_urls())
        if len(urls) == 0:
            _logger.error(
                f"volume {volume.get_identifier().to_str()} has no url / slices. Unable to load any data."
            )
            return {cor: (None, None)}
        if len(urls) != 1:
            _logger.error(
                f"volume is expected to have at most one url (single slice volume). get {len(urls)} - most likely nabu reconstruction failed. Do you have GPU ? Are the requested COR values valid ? - Especially for Half-acquisition"
            )
        url = urls[0]
        if not isinstance(url, (DataUrl, str)):
            raise TypeError(f"url is expected to be a str or DataUrl not {type(url)}")

        try:
            data = get_slice_data(url=url)
        except Exception as e:
            _logger.error(f"Fail to compute a score for {url.path()}. Reason is {e}")
            return {cor: (url, None)}
        else:
            if data.ndim == 3:
                if data.shape[0] == 1:
                    data = data.reshape(data.shape[1], data.shape[2])
                elif data.shape[2] == 1:
                    data = data.reshape(data.shape[0], data.shape[1])
                else:
                    raise ValueError(f"Data is expected to be 2D. Not {data.ndim}D")
            elif data.ndim == 2:
                pass
            else:
                raise ValueError("Data is expected to be 2D. Not {data.ndim}D")
            return {cor: (url, data)}

    def load_datasets(self):
        with Pool(self.pool_size) as pool:
            res = pool.map(
                self._load_dataset,
                self._cor_reconstructions.items(),
            )
        datasets_ = {}
        for mydict in res:
            datasets_.update(mydict)
        return datasets_

    def cancel(self):
        self._cancelled = True


class SAAxisProcess(SAAxisTask):
    def __init__(
        self, process_id=None, inputs=None, varinfo=None, node_attrs=None, execinfo=None
    ):
        deprecated_warning(
            name="tomwer.core.process.reconstruction.saaxis.SAAxisProcess",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="SAAxisTask",
        )
        super().__init__(process_id, inputs, varinfo, node_attrs, execinfo)
