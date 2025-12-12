"""contain the AxisTask class"""

from __future__ import annotations

import logging

from nabu.pipeline.estimators import estimate_cor
from nabu.resources.nxflatfield import update_dataset_info_flats_darks
from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess

import tomwer.version
from tomwer.core.process.reconstruction.utils.cor import absolute_pos_to_relative
from tomwer.core.process.task import Task
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils import image, logconfig
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.utils import docstring

from .mode import AxisMode
from .params import (
    DEFAULT_CMP_N_SUBSAMPLING_Y,
    DEFAULT_CMP_NEAR_POS,
    DEFAULT_CMP_NEAR_WIDTH,
    DEFAULT_CMP_OVERSAMPLING,
    DEFAULT_CMP_TAKE_LOG,
    DEFAULT_CMP_THETA,
    AxisRP,
)
from .projectiontype import ProjectionType

_logger = logging.getLogger(__name__)

# vertically, work on a window having only a percentage of the frame.
pc_height = 10.0 / 100.0
# horizontally. Global method supposes the COR is more or less in center
# % of the detector:

pc_width = 50.0 / 100.0


def _absolute_pos_to_relative_with_warning(absolute_pos: float, det_width: int | None):
    """
    nabu returns the value as absolute. tomwer needs it as relative
    Also handle the case (unlikely) the detector width cannot be found
    """
    if det_width is None:
        det_width = 2048
        _logger.warning("unable to find image width. Set width to 2048")
    else:
        det_width = det_width
    return absolute_pos_to_relative(absolute_pos=absolute_pos, det_width=det_width)


def adapt_tomwer_scan_to_nabu(scan: TomwerScanBase, do_flatfield: bool):
    """simple util to convert tomwer scan to a nabu DataAnalizer and
    updating infos regarding flat and dark if needed
    """
    dataset_infos = scan.to_nabu_dataset_analyser()
    if isinstance(scan, NXtomoScan):
        try:
            update_dataset_info_flats_darks(
                dataset_infos,
                flatfield_mode=do_flatfield,
                loading_mode="load_if_present",
            )
        except ValueError as exception:
            # nabu raise an error if no darks / flats set. But this can make sense at this stage if the NXtomo has no
            # raw dark / flat and is already normalized. In this case only fire a warning
            if (
                scan.reduced_darks is not None
                and len(scan.reduced_darks) > 0
                and scan.reduced_flats is not None
                and len(scan.reduced_flats) > 0
            ):
                raise exception
            else:
                _logger.warning(
                    "Fail to update nabu dataset info flats and darks. Expected if the dataset contains already normalized projections"
                )

    return dataset_infos


def get_composite_options(scan) -> tuple:
    theta = scan.axis_params.composite_options.get("theta", DEFAULT_CMP_THETA)
    n_subsampling_y = scan.axis_params.composite_options.get(
        "n_subsampling_y", DEFAULT_CMP_N_SUBSAMPLING_Y
    )
    oversampling = scan.axis_params.composite_options.get(
        "oversampling", DEFAULT_CMP_OVERSAMPLING
    )
    take_log = scan.axis_params.composite_options.get("take_log", DEFAULT_CMP_TAKE_LOG)

    near_pos = scan.axis_params.composite_options.get("near_pos", DEFAULT_CMP_NEAR_POS)
    near_width = scan.axis_params.composite_options.get(
        "near_width", DEFAULT_CMP_NEAR_WIDTH
    )
    return theta, n_subsampling_y, oversampling, take_log, near_pos, near_width


def read_scan_x_rotation_axis_pixel_position(scan: TomwerScanBase):
    """read center of rotation estimation from metadata"""
    if isinstance(scan, EDFTomoScan):
        raise TypeError("EDFTomoScan have not information about estimated cor position")
    else:
        res = scan.x_rotation_axis_pixel_position
        if res is None:
            _logger.error(
                f"unable to find x_rotation_axis_pixel_position from {scan.get_identifier()}"
            )
    return res


class NoAxisUrl(Exception):
    pass


class AxisTask(
    Task,
    SuperviseProcess,
    input_names=("data",),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """
    Process used to compute the center of rotation of a scan
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
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        if "recons_params" in inputs:
            raise KeyError("do not use 'recons_params' but use 'axis_params' instead")
        axis_params = inputs.get("axis_params", None)
        if isinstance(axis_params, dict):
            axis_params = AxisRP.from_dict(axis_params)
        elif not (axis_params is None or isinstance(axis_params, AxisRP)):
            raise TypeError(
                "'axis_params' is expected to be None or an instance of AxisRP or a dict"
            )

        SuperviseProcess.__init__(self, process_id=process_id)
        self._mode_calculation_fct = {}
        """dict with function pointer to call for making the mode calculation.
        Function should have only one 'scan' parameter as input"""

        self._axis_params = axis_params or AxisRP()
        """Axis reconstruction parameters to apply"""
        self._locked = False
        """Boolean used to lock reconstruction parameters edition"""
        self._recons_params_before_lock = None
        """Recons parameters register before locking the position"""

    def set_configuration(self, configuration):
        if "_rpSetting" in configuration:
            recons_params = AxisRP.from_dict(configuration["_rpSetting"])
        else:
            recons_params = AxisRP.from_dict(configuration)
        self.set_recons_params(recons_params=recons_params)

    def set_recons_params(self, recons_params):
        assert isinstance(recons_params, AxisRP)
        self._axis_params = recons_params

    def lock_position_value(self, lock=True):
        """
        lock the position currently computed or defined by the user.
        In this case we will lock the axis as defined 'fixed' with the current
        value

        :param lock: if true lock the currently existing position value
        """
        self._locked = lock
        if lock:
            self._recons_params_before_lock = self._axis_params.to_dict()
            if self._axis_params != AxisMode.manual:
                self._axis_params.mode = AxisMode.manual
        else:
            if self._recons_params_before_lock:
                self._axis_params.load_from_dict(
                    self._recons_params_before_lock
                )  # noqa

    def run(self):
        """
        Compute the position value then get ready to the next. And call

        .. note:: this simply call `compute`.
                  But this is needed for the AxisProcessThreaded class
        """
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            self.outputs.data = None
            return

        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(f"input type {scan} is not managed")

        _logger.info("start axis calculation for %s" % scan.path)
        self._axis_params.frame_width = scan.dim_1
        cor = error = None
        try:
            scan_res = self.compute(scan=scan)
        except Exception as e:
            scan_res = None
            error = e
        else:
            if isinstance(scan_res, TomwerScanBase):
                cor = scan_res.axis_params.relative_cor_value
            elif scan_res is None:
                if scan.axis_params.relative_cor_value is not None:
                    cor = scan.axis_params.relative_cor_value
            elif isinstance(scan_res, float):
                cor = scan_res
            else:
                assert isinstance(scan_res, dict)
                b_dict = scan_res
                if TomwerScanBase._DICT_AXIS_KEYS in scan_res:
                    b_dict = scan_res["axis_params"]
                cor = b_dict["POSITION_VALUE"]
        finally:
            if cor != "...":
                self._process_end(scan, cor=cor, error=error)

        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan_res.to_dict()
        else:
            self.outputs.data = scan_res

    def _process_end(self, scan, cor, error=None):
        assert isinstance(scan, TomwerScanBase)
        try:
            extra = {
                logconfig.DOC_TITLE: self._scheme_title,
                logconfig.SCAN_ID: scan.path,
            }
            if error is not None:
                info = " ".join(
                    (
                        "fail to compute axis position for scan",
                        str(scan.path),
                        "reason is ",
                        str(error),
                    )
                )
                _logger.processFailed(info, extra=extra)
                ProcessManager().notify_dataset_state(
                    dataset=scan, process=self, state=DatasetState.FAILED, details=info
                )
            elif scan.axis_params.relative_cor_value is None:
                info = " ".join(
                    ("fail to compute axis position for scan", str(scan.path))
                )
                _logger.processFailed(info, extra=extra)
                ProcessManager().notify_dataset_state(
                    dataset=scan, process=self, state=DatasetState.FAILED, details=info
                )
            else:
                info = "axis calculation defined for {}: {} (using {})".format(
                    str(scan.path),
                    str(scan.axis_params.relative_cor_value),
                    scan.axis_params.mode.value,
                )
                _logger.processSucceed(info, extra=extra)
                ProcessManager().notify_dataset_state(
                    dataset=scan, process=self, state=DatasetState.SUCCEED, details=info
                )
        except Exception as e:
            _logger.error(e)

    @staticmethod
    def get_input_radios(scan) -> tuple:
        """Make sure we have valid projections to be used for axis calculation

        :param scan: scan to check
        :raise: NoAxisUrl if fails to found
        :return: tuple of AxisResource
        """
        if (
            scan.axis_params
            and scan.axis_params.axis_url_1
            and scan.axis_params.axis_url_1.url
        ):
            return scan.axis_params.axis_url_1, scan.axis_params.axis_url_2

        return scan.get_opposite_projections(mode=scan.axis_params.angle_mode)

    @staticmethod
    def get_inputs(scan):
        assert isinstance(scan, TomwerScanBase)
        radio_1, radio_2 = AxisTask.get_input_radios(scan=scan)
        if radio_1 and radio_2:
            mess = " ".join(
                ("input radios are", radio_1.url.path(), "and", radio_2.url.path())
            )
            _logger.info(mess)
            log_ = scan.axis_params.projection_type is ProjectionType.transmission

            # if necessary normalize data
            if radio_1.normalized_data is None:
                radio_1.normalize_data(scan, log_=log_)
            if radio_2.normalized_data is None:
                radio_2.normalize_data(scan, log_=log_)

            if scan.axis_params.paganin_preproc:
                data_1 = radio_1.normalized_data_paganin
                data_2 = radio_2.normalized_data_paganin
            else:
                data_1 = radio_1.normalized_data
                data_2 = radio_2.normalized_data

            if scan.axis_params.scale_img2_to_img1:
                data_2 = image.scale_img2_to_img1(img_1=data_1, img_2=data_2)
            return data_1, data_2
        else:
            _logger.info("fail to find any inputs")
            return None, None

    def compute(self, scan, wait=True):
        """
        Compute the position value for the scan

        :param scan:
        :param wait: used for threaded process. True if we want to end the
                          computation before releasing hand.
        :return: scan as a TomoBase
        """
        assert scan is not None
        if isinstance(scan, dict):
            _logger.warning("convert scan from a dict")
            _scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            _scan = scan
        assert isinstance(_scan, TomwerScanBase)
        # if the scan has no tomo reconstruction parameters yet create them
        if _scan.axis_params is None:
            _scan.axis_params = AxisRP()

        # copy axis recons parameters. We skip the axis_url which are specific
        # to the scan
        _scan.axis_params.copy(
            self._axis_params, copy_axis_url=False, copy_flip_lr=False
        )
        assert scan.axis_params is not None
        return self._process_computation(scan=_scan)

    def scan_ready(self, scan):
        _logger.info(scan, "processed")

    def _process_computation(self, scan):
        """

        :param TomwerScanBase scan: scan for which we want to compute the axis
                              position.
        :return: scan as a TomoBase or a dict if serialize_output_data activated
        """
        _logger.info("compute center of rotation for %s" % scan.path)
        try:
            position = self.compute_axis_position(scan)
        except NotImplementedError as e:
            scan.axis_params.set_relative_value(None)
            raise e
        except ValueError as e:
            scan_name = scan.path or "undef scan"
            scan.axis_params.set_relative_value(None)
            raise Exception(
                f"Fail to compute axis position for {scan_name} reason is {e}"
            )
        else:
            scan.axis_params.set_relative_value(position)
            self._axis_params.frame_width = scan.dim_1
            self._axis_params.set_relative_value(position)
            scan_name = scan.path or "undef scan"
            r_cor_value = scan.axis_params.relative_cor_value
            mess = f"Compute axis position ({r_cor_value}) with {scan.axis_params.mode.value}"
            _logger.info(mess)
        return scan

    def setMode(self, mode, value):
        if mode is AxisMode.manual:
            self._axis_params.cor_position = value
        else:
            raise NotImplementedError("mode not implemented yet")

    def define_calculation_mode(self, mode: AxisMode, fct_pointer):
        """Register the function to call of the given mode

        :param mode: the mode to register
        :param fct_pointer: pointer to the function to call
        """
        self._mode_calculation_fct[mode] = fct_pointer

    def compute_axis_position(self, scan):
        """

        :param scan: scan for which we compute the center of rotation
        :return: position of the rotation axis. Use the `.AxisMode` defined
                 by the `.ReconsParams` of the `.AxisTask`
        """
        mode = self._axis_params.mode
        if mode is AxisMode.manual:
            # If mode is read or manual the position_value is not computed and
            # we will keep the actual one (should have been defined previously)
            res = self._axis_params.relative_cor_value
        elif mode is AxisMode.read:
            res = read_scan_x_rotation_axis_pixel_position(scan=scan)
        else:
            has_darks = scan.reduced_darks is not None and len(scan.reduced_darks) > 0
            has_flats = scan.reduced_flats is not None and len(scan.reduced_flats) > 0
            do_flatfield = has_darks and has_flats
            res = estimate_cor(
                method=mode.value,
                dataset_info=adapt_tomwer_scan_to_nabu(
                    scan=scan, do_flatfield=do_flatfield
                ),
                do_flatfield=do_flatfield,
                cor_options=scan.axis_params.get_nabu_cor_options_as_dict(),
            )
            # convert back to relative
            res = _absolute_pos_to_relative_with_warning(
                absolute_pos=res, det_width=scan.dim_1
            )

        return res

    @docstring(Task.program_name)
    @staticmethod
    def program_name():
        return "tomwer_axis"

    @docstring(Task.program_version)
    @staticmethod
    def program_version():
        return tomwer.version.version

    @docstring(Task.definition)
    @staticmethod
    def definition():
        return "Compute center of rotation"
