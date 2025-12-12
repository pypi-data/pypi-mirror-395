"""contain the SADeltaBetaProcess. Half automatic best delta / beta finder"""

from __future__ import annotations

import logging
import os
from copy import copy, deepcopy

import h5py
import numpy
from multiprocessing import Pool
from tqdm import tqdm

from nabu.pipeline.config import get_default_nabu_config
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from tomoscan.esrf.scan.utils import get_data
from tomoscan.io import HDF5File
from silx.io.utils import h5py_read_dataset

import tomwer.version
from tomwer.core.process.reconstruction.nabu.nabucommon import (
    ResultsLocalRun,
    ResultSlurmRun,
    ResultsWithStd,
)
from tomwer.core.process.reconstruction.nabu.nabuslices import SingleSliceRunner
from tomwer.core.process.reconstruction.utils.cor import relative_pos_to_absolute
from tomwer.core.process.reconstruction.scores import (
    ComputedScore,
    ScoreMethod,
    apply_roi,
    compute_score,
    get_disk_mask_radius,
)
from tomwer.core.process.task import Task
from tomwer.core.process import utils as core_utils
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils import logconfig
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.io.utils import format_stderr_stdout
from tomwer.io.utils.h5pyutils import EntryReader
from tomwer.core.process.reconstruction.nabu.nabuscores import (
    run_nabu_one_slice_several_config,
)
from tomwer.core.futureobject import FutureTomwerObject

from silx.io.url import DataUrl
from silx.utils.deprecation import deprecated, deprecated_warning

from ..nabu import utils as nabu_utils
from .params import SADeltaBetaParams

_logger = logging.getLogger(__name__)


DEFAULT_RECONS_FOLDER = "multi_delta_beta_results"


def one_slice_several_db(
    scan: TomwerScanBase,
    configuration: dict | SADeltaBetaParams,
    process_id: int | None = None,
) -> tuple:
    """
    Run a slice reconstruction using nabu per Center Of Rotation (cor) provided
    Then for each compute a score (quality) of the center of rotation

    :param scan:
    :param configuration:
    :return: cor_reconstructions, outs, errs
             cor_reconstructions is a dictionary of cor as key and a tuple
             (url, score) as value
    """
    if isinstance(configuration, SADeltaBetaParams):
        configuration = configuration.to_dict()

    task = SADeltaBetaTask(
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


class SADeltaBetaTask(
    Task,
    SuperviseProcess,
    input_names=("data", "sa_delta_beta_params"),
    output_names=("data", "best_db"),
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
    """

    DEFAULT_POOL_SIZE = 10

    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        SuperviseProcess.__init__(self, process_id=process_id)
        self._dry_run = inputs.get("dry_run", False)
        self._dump_process = inputs.get("dump_process", True)
        self._dump_roi = inputs.get("dump_roi", False)
        self._sa_delta_beta_params = inputs.get("sa_delta_beta_params", None)
        self._std_outs = tuple()
        self._std_errs = tuple()
        self._cancelled = False

    @property
    def dump_roi(self):
        return self._dump_roi

    @dump_roi.setter
    def dump_roi(self, dump):
        self._dump_roi = dump

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

    @deprecated(replacement="ewoks task inputs.sa_delta_beta_params")
    def set_configuration(self, configuration: dict) -> None:
        if isinstance(configuration, SADeltaBetaParams):
            self._settings = configuration.to_dict()
        elif isinstance(configuration, dict):
            self._settings = configuration
        else:
            raise TypeError(
                "configuration should be an instance of dict or " "SAAxisParams"
            )

    @staticmethod
    def autofocus(scan) -> float | None:
        scores = scan.sa_delta_beta_params.scores
        if scores is None:
            return
        score_method = scan.sa_delta_beta_params.score_method
        best_db, best_score = None, 0
        for cor, (_, score_cls) in scores.items():
            if score_cls is None:  # if score calculation failed
                continue
            score = score_cls.get(score_method)
            if score is None:
                continue
            if score > best_score:
                best_db, best_score = cor, score
        scan.sa_delta_beta_params.autofocus = best_db
        scan.sa_delta_beta_params.value = best_db
        return best_db

    def get_output_dir(self, params: SADeltaBetaParams, scan: TomwerScanBase):
        output_dir = params.output_dir or None

        if params.output_dir is None:
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
            self.outputs.data = scan
            return
        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed")

        config = copy(self.inputs.sa_delta_beta_params)
        axis = config.get("reconstruction", {}).get("slice_plane", "XY")
        params = SADeltaBetaParams.from_dict(config)

        # insure scan contains some parameter regarding sa delta / beta
        if scan.sa_delta_beta_params is None:
            scan.sa_delta_beta_params = params

        # insure it also contains some axis_params
        if scan.axis_params is None:
            from tomwer.core.process.reconstruction.axis import AxisRP

            scan.axis_params = AxisRP()

        # create dir if does not exists
        params.output_dir = self.get_output_dir(params=params, scan=scan)
        if not os.path.exists(params.output_dir):
            os.makedirs(params.output_dir)

        slice_index = self._preprocess_slice_index(params.slice_indexes)
        delta_beta_s = params.delta_beta_values
        # TODO: check: dry run should only be settable at one location
        dry_run = self._dry_run or params.dry_run
        cluster_config = params.cluster_config
        nabu_config = params.nabu_recons_params

        # step one: complete nabu configuration(s)
        configs = self._config_preprocessing(
            scan=scan,
            config=nabu_config,
            delta_beta_s=delta_beta_s,
            output_dir=params.output_dir,
        )
        # step 2: run reconstructions
        advancement = tqdm(
            desc=f"sa-delta-beta - slice {slice_index} of {scan.get_identifier().short_description()}"
        )

        dbs_res = {}
        rois = {}

        try:
            (
                _,
                dbs_res,
                future_tomo_objs,
                self._std_outs,
                self._std_errs,
            ) = self._run_one_slice_several_db(
                scan=scan,
                configs=configs,
                advancement=advancement,
                slice_index=slice_index,
                dry_run=dry_run,
                cluster_config=cluster_config,
                axis=axis,
            )
        except Exception as e:
            _logger.error(e)
            mess = f"sa-delta-beta -nabu- computation for {str(scan)} failed."
            state = DatasetState.FAILED
        else:
            # step 3: wait for future if any
            self._resolve_futures(
                scan=scan,
                nabu_config=next(iter(configs.items()))[
                    1
                ],  # db is not used but paganin and other parameters are. Take the first nabu configuration available
                slice_index=slice_index,
                db_reconstructions=dbs_res,
                future_tomo_objs=future_tomo_objs,
                axis=axis,
            )

            # step 4: run post processing (compute score for each slice)
            if self.get_input_value("compute_scores", True):
                try:
                    dbs_res, rois = self._post_processing(
                        scan=scan,
                        db_reconstructions=dbs_res,
                    )
                except Exception as e:
                    _logger.error(e)
                    mess = f"sa-delta-beta -post-processing- computation for {str(scan)} failed."
                    state = DatasetState.FAILED
                    dbs_res = {}
                else:
                    state = DatasetState.WAIT_USER_VALIDATION
                    self.delta_beta_s = scan.sa_delta_beta_params.autofocus
                    mess = "sa-delta-beta computation succeeded"
            else:
                dbs_res = {}
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

        scan.sa_delta_beta_params.scores = dbs_res
        best_db = self.autofocus(scan=scan)
        # store nabu recons parameters to be used within the nabu volume for example.

        sc_config = get_default_nabu_config(nabu_fullfield_default_config)
        sc_config.update(nabu_config)
        if best_db is not None:
            sc_config["phase"]["delta_beta"] = (
                best_db,
            )  # warning: at this tage delta_beta expects a list of value
        # store used reconstruction parameters - to be used later on
        scan.nabu_recons_params = sc_config

        # end processing
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan
        self.outputs.best_db = best_db

        self._process_end(scan=scan, db_res=dbs_res, score_rois=rois)

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

    def _config_preprocessing(self, scan, config, delta_beta_s, output_dir) -> dict:
        config.get("phase", {}).pop("beam_shape", None)
        if (
            scan.axis_params is not None
            and scan.axis_params.relative_cor_value is not None
        ):
            if "reconstruction" in config:
                cor_nabu_ref = relative_pos_to_absolute(
                    relative_pos=scan.axis_params.relative_cor_value,
                    det_width=scan.dim_1,
                )
                config["reconstruction"]["rotation_axis_position"] = str(cor_nabu_ref)

        _logger.info(f"set nabu reconstruction parameters to {scan}")
        scan.nabu_recons_params = config
        res = {}
        for db in delta_beta_s:
            l_config = deepcopy(config)
            if "output" not in config:
                l_config["output"] = {}
            if output_dir is None:
                l_config["output"]["location"] = os.path.join(
                    scan.path, DEFAULT_RECONS_FOLDER
                )
            else:
                l_config["output"]["location"] = output_dir
            # TODO: allow file format modifications
            l_config["output"]["file_format"] = "hdf5"
            if "phase" not in config:
                l_config["phase"] = {}
            l_config["phase"]["delta_beta"] = db
            l_config["phase"]["method"] = "Paganin"
            res[db] = l_config
        return res

    def _run_one_slice_several_db(
        self,
        scan,
        configs,
        slice_index,
        advancement,
        dry_run,
        axis,
        cluster_config: dict | None,
    ):
        future_tomo_objs = {}
        success = True
        recons_urls = {}
        std_outs = []
        std_errs = []

        if not isinstance(cluster_config, (dict, type(None))):
            raise TypeError(
                f"'cluster_config' is expected to be a dict or None. Get {type(cluster_config)} instead."
            )

        runners = run_nabu_one_slice_several_config(
            nabu_configs=configs,
            scan=scan,
            slice_index=slice_index,
            dry_run=dry_run,
            file_format="hdf5",
            advancement=advancement,
            cluster_config=cluster_config,
            process_id=self.process_id,
            instantiate_classes_only=True,
            output_file_prefix_pattern=None,
            axis=axis,
        )

        for runner in runners:
            if self._cancelled:
                break

            self._current_processing = runner
            try:
                results = runner.run()
            except TimeoutError as e:
                _logger.error(e)
            else:
                assert isinstance(
                    results, dict
                ), "results should be a dictionary with delta-beta as key and urls as value"

                for db, res in results.items():
                    success = success and res.success
                    if isinstance(res, ResultsWithStd):
                        std_outs.append(res.std_out)
                        std_errs.append(res.std_err)
                    if (
                        isinstance(res, ResultsLocalRun)
                        and len(res.results_identifiers) > 0
                    ):
                        assert (
                            len(res.results_identifiers) == 1
                        ), "only one slice expected"
                        recons_urls[db] = res.results_identifiers[0]
                    if isinstance(res, ResultSlurmRun):
                        future_tomo_obj = FutureTomwerObject(
                            tomo_obj=scan,
                            process_requester_id=self.process_id,
                            futures=res.future_slurm_jobs,
                        )
                        future_tomo_objs[db] = future_tomo_obj

            if advancement is not None:
                advancement.update()

        return success, recons_urls, future_tomo_objs, std_outs, std_errs

    def _post_processing(
        self,
        scan,
        db_reconstructions,
    ):
        post_processing = _PostProcessing(
            scan=scan,
            db_reconstructions=db_reconstructions,
            pool_size=self.get_input_value("pool_size", self.DEFAULT_POOL_SIZE),
        )
        post_processing._cancelled = self._cancelled
        self._current_processing = post_processing
        return post_processing.run()

    def _resolve_futures(
        self,
        scan,
        nabu_config: dict,
        db_reconstructions,
        slice_index,
        axis,
        future_tomo_objs: dict,
    ):
        assert isinstance(nabu_config, dict)
        pag = False
        ctf = False
        if "phase" in nabu_config:
            phase_method = nabu_config["phase"].get("method", "").lower()
            if phase_method in ("pag", "paganin"):
                pag = True
            elif phase_method in ("ctf",):
                ctf = True

        # treat future.
        for db, future_tomo_obj in future_tomo_objs.items():
            if self._cancelled:
                break

            future_tomo_obj.results()
            if future_tomo_obj.cancelled() or future_tomo_obj.exceptions():
                continue
            file_prefix = SingleSliceRunner.get_file_basename_reconstruction(
                scan=scan,
                slice_index=slice_index,
                pag=pag,
                db=int(db) if db is not None else None,
                ctf=ctf,
                axis=axis,
            )
            # retrieve url
            volume_identifier = nabu_utils.get_recons_volume_identifier(
                file_prefix=file_prefix,
                location=nabu_config["output"]["location"],
                file_format=nabu_config.get("file_format", "hdf5"),
                scan=scan,
                slice_index=None,
                axis=axis,
            )

            assert len(volume_identifier) <= 1, "only one slice expected"
            if len(volume_identifier) == 1:
                db_reconstructions[db] = volume_identifier[0]
            else:
                _logger.warning(
                    f"something went wrong with reconstruction of {db} from {str(scan)}"
                )

    @staticmethod
    def _preprocess_slice_index(slice_index):
        if isinstance(slice_index, str):
            if not slice_index == "middle":
                raise ValueError(f"slice index {slice_index} not recognized")
            else:
                return slice_index
        elif not len(slice_index) == 1:
            raise ValueError("only manage one slice")
        else:
            return list(slice_index.values())[0]

    def _process_end(self, scan, db_res, score_rois):
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
                slice_index = self.inputs.sa_delta_beta_params.get("slice_index", None)

                if db_res is None:
                    info = f"fail to compute delta/beta scores of slice {slice_index} for scan {scan}."
                    _logger.processFailed(info, extra=extra)
                    ProcessManager().notify_dataset_state(
                        dataset=scan,
                        process=self,
                        state=DatasetState.FAILED,
                        details=info,
                    )
                else:
                    info = f"delta/beta scores of slice {slice_index} for scan {scan} computed."
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
    def dump_rois(scan, score_rois: dict):
        if not isinstance(score_rois, dict):
            raise TypeError("score_rois is expected to be a dict")

        if score_rois is None or len(score_rois) == 0:
            return

        if scan.saaxis_params.scores in (None, {}):
            return

        sa_delta_beta_results_url = SADeltaBetaTask.get_results_url(scan=scan)

        # save it to the file
        with HDF5File(sa_delta_beta_results_url.file_path(), mode="a") as h5f:
            nx_process = h5f.require_group(sa_delta_beta_results_url.data_path())
            score_roi_grp = nx_process.require_group("score_roi")
            for db, roi in score_rois.items():
                score_roi_grp[str(db)] = roi
                score_roi_grp[str(db)].attrs["interpretation"] = "image"

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "semi-automatic delta/beta finder"

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
                os.path.join(DEFAULT_RECONS_FOLDER, "tomwer_sadelta_beta.h5")
            ),
            data_path=scan.entry or "entry",
            scheme="silx",
        )

    @staticmethod
    def save_results_to_disk(scan):
        if scan.saaxis_params.scores in (None, {}):
            return

        results_url = SADeltaBetaTask.get_results_url(scan=scan)
        # save it to the file
        with HDF5File(results_url.file_path(), mode="w") as h5f:
            nx_process = h5f.require_group(results_url.data_path())
            if "NX_class" not in nx_process.attrs:
                nx_process.attrs["NX_class"] = "NXprocess"

            results = nx_process.require_group("results")

            for cor, (url, score) in scan.sa_delta_beta_params.scores.items():
                results_db = results.require_group(str(cor))
                for method in ScoreMethod:
                    if method is ScoreMethod.TOMO_CONSISTENCY:
                        continue
                    results_db[method.value] = score.get(method)

                link_path = os.path.relpath(
                    url.file_path(),
                    os.path.dirname(results_url.file_path()),
                )
                results_db["reconstructed_slice"] = h5py.ExternalLink(
                    link_path, url.data_path()
                )

    @staticmethod
    def load_results_from_disk(scan):
        results_url = SADeltaBetaTask.get_results_url(scan=scan)
        process_file = results_url.file_path()

        if process_file is None or not os.path.exists(process_file):
            _logger.warning(
                "Unable to find process file. Unable to read " "existing processing"
            )
            return None, None

        try:
            with EntryReader(results_url) as h5f_entry_node:
                scores = core_utils.get_scores(h5f_entry_node)
                if (
                    "results" in h5f_entry_node
                    and "delta_beta" in h5f_entry_node["results"]
                ):
                    selected = h5py_read_dataset(
                        h5f_entry_node["results"]["delta_beta"]
                    )
                else:
                    _logger.warning(f"no results found for {scan}")
                    selected = None
            return scores, selected
        except ValueError:
            _logger.warning(f"Data path ({results_url.data_path()}) not found")
            return None, None

    def cancel(self):
        """
        stop current processing
        """
        if self._current_processing is not None:
            self._cancelled = True
            self._current_processing.cancel()


class _PostProcessing:
    """class used to run SA-delta-beta post-processing on reconstructed slices"""

    DEFAULT_POOL_SIZE = 10

    def __init__(self, db_reconstructions, scan, pool_size) -> None:
        self._db_reconstructions = db_reconstructions
        self._scan = scan
        self._cancelled = False
        self.pool_size = pool_size

    @staticmethod
    def compute_score(item: tuple):
        db, (url, data), mask_disk_radius, cancelled = item
        if data is None:
            score = None
            data_roi = None
        else:
            assert data.ndim == 2
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
            )
        return {db: (url, score)}, {db: data_roi}

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
        db, volume_identifier = item
        slice_url = None
        # in case the try processing fails
        try:
            volume = VolumeFactory.create_tomo_object_from_identifier(volume_identifier)
            volumes_urls = tuple(volume.browse_data_urls())
            if len(volumes_urls) > 1:
                _logger.warning(
                    f"found a volume with mode that one url ({volumes_urls})"
                )
            slice_url = volumes_urls[0]
            data = get_data(slice_url)
        except Exception as e:
            _logger.error(
                f"Fail to compute a score for {volume_identifier}. Reason is {e}"
            )
            return {db: (slice_url, None)}
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
                raise ValueError(f"Data is expected to be 2D. Not {data.ndim}D")

            return {db: (slice_url, data)}

    def load_datasets(self):
        with Pool(self.pool_size) as pool:
            res = pool.map(
                self._load_dataset,
                self._db_reconstructions.items(),
            )
        datasets_ = {}
        for mydict in res:
            datasets_.update(mydict)

        return datasets_

    def cancel(self):
        self._cancelled = True


class SADeltaBetaProcess(SADeltaBetaTask):
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
            name="tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta.SADeltaBetaProcess",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="SADeltaBetaTask",
        )
        super().__init__(process_id, varinfo, inputs, node_id, node_attrs, execinfo)
