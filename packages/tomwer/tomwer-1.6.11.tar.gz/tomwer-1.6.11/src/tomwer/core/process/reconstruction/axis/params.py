from __future__ import annotations

import logging
from collections import namedtuple

import numpy
from silx.io.url import DataUrl
from enum import Enum as _Enum
from tomoscan.esrf.scan.utils import get_data

from tomwer.core.process.reconstruction.utils.cor import relative_pos_to_absolute
from tomwer.core.process.reconstruction.axis.side import Side
from tomwer.core.scan.scanbase import TomwerScanBase

from .anglemode import CorAngleMode
from .mode import AxisMode, AXIS_MODE_METADATAS
from .projectiontype import ProjectionType

from nabu.preproc.phase import PaganinPhaseRetrieval


_logger = logging.getLogger(__name__)


_calculation_conf = namedtuple(
    "_calculation_conf", ["projection_type", "paganin"]
)  # noqa

_WITH_PAG = "withpag"
_NO_PAG = "nopag"


DEFAULT_CMP_THETA = 5
DEFAULT_CMP_N_SUBSAMPLING_Y = 40
DEFAULT_CMP_NEAR_POS = 0
DEFAULT_CMP_NEAR_WIDTH = 40
DEFAULT_CMP_OVERSAMPLING = 4
DEFAULT_CMP_TAKE_LOG = True


class AxisCalculationInput(_Enum):
    """Define the different mode of input the user can have for axis calculation"""

    emission = _calculation_conf(ProjectionType.absorption, False)
    transmission = _calculation_conf(ProjectionType.transmission, False)
    transmission_pag = _calculation_conf(ProjectionType.transmission, True)

    def name(self):  # pylint: disable=E0102
        if self.value.paganin is True:
            return " ".join((self.value.projection_type.value, "paganin"))
        else:
            return self.value.projection_type.value

    def to_dict(self):
        pag_text = _WITH_PAG if self.value.paganin is True else _NO_PAG
        return "_".join((self.value.projection_type.value, pag_text))

    @classmethod
    def from_value(cls, value):
        if type(value) is str and len(value.split("_")) == 2:
            proj_type, pag = value.split("_")
            value_pag = True if pag == _WITH_PAG else False
            value_proj = ProjectionType(proj_type)
            return cls(_calculation_conf(value_proj, value_pag))
        elif isinstance(value, cls):
            return value
        else:
            for member in cls:
                if value in (member.value, member.name()):
                    return member
            raise ValueError(f"Cannot convert: {value}")


class AxisResource(object):
    """Helper for axis file relative stuff"""

    _PAGANIN_CONFIG = {"distance": 100e-3, "energy": 35, "delta_beta": 1e3}
    """Paganin configuration for axis calculation. To simplify we have only one
    static configuration for now. Otherwise complicate stuff"""

    def __init__(self, url: None | DataUrl, angle: float | None = None):
        assert url is None or isinstance(url, DataUrl)
        assert url is None or url.is_valid()
        self.__url = url
        self.__raw_data = None
        self.__norme_data = None
        self.__norm_paganin = None
        self.__angle = angle

    def __str__(self):
        return f"{type(self)}, url: {self.__url.path() if self.__url else None}"

    @property
    def url(self):
        return self.__url

    @property
    def data(self):
        """

        :return: 2D numpy.array
        """
        if self.__url is None:
            return None
        if self.__raw_data is None:
            self.__raw_data = get_data(self.url)
        return self.__raw_data

    @data.setter
    def data(self, data):
        self.__raw_data = data

    @property
    def normalized_data(self):
        return self.__norme_data

    @normalized_data.setter
    def normalized_data(self, data):
        self.__norme_data = data

    @property
    def angle(self) -> float | None:
        return self.__angle

    def normalize_data(self, scan, log_):
        """Normalize data for axis calculation"""
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"scan is expected to be an instance of {TomwerScanBase}. {type(scan)} provided"
            )
        if self.__url is None:
            return None
        else:
            self.__norme_data = scan.data_flat_field_correction(data=self.data)
            if log_ is True:
                self.__norme_data[numpy.isnan(self.__norme_data)] = (
                    self.__norme_data.max()
                )
                if self.__norme_data.max() < 0:
                    _logger.error("max data value < 0 unable to compute log")
                else:
                    try:
                        data = self.__norme_data
                        data[data <= 1] = 1
                        self.__norme_data = -numpy.log(data)
                    except Exception as e:
                        _logger.error("Fail to apply log on radio" + e)
            else:
                self.__norme_data[numpy.isnan(self.__norme_data)] = (
                    self.__norme_data.min()
                )

        return self.__norme_data

    @property
    def normalized_data_paganin(self):
        """

        :return: data processed by the Pagagin phase retrieval
        """
        if self.__url is None:
            return None
        if self.__norm_paganin is None:
            if self.normalized_data is None:
                raise ValueError("data should be normalized before applying " "paganin")
            else:
                data = self.normalized_data
                phase_retrieval = PaganinPhaseRetrieval(
                    data.shape, **AxisResource._PAGANIN_CONFIG
                )
                self.__norm_paganin = phase_retrieval.apply_filter(data)
        return self.__norm_paganin

    @normalized_data_paganin.setter
    def normalized_data_paganin(self, data):
        self.__norm_paganin = data

    def __eq__(self, other):
        if not isinstance(other, AxisResource):
            return False
        if self.url is None and other.url is None:
            return True
        elif self.url is None or other.url is None:
            return False
        else:
            return self.url == other.url


class AxisRP:
    """
    Configuration class for a tomwer :class:`AxisTask`

    note: every modification on the parameters will process a call fo changed
    except `axis_url_1` and `axis_url_2` which will produce a call to the
    dedicated axis_url_changed
    """

    AXIS_POSITION_PAR_KEY = "ROTATION_AXIS_POSITION"
    """Key used for the axis position in par files"""

    _MANAGED_KEYS = (
        "MODE",
        "POSITION_VALUE",
        "CALC_INPUT_TYPE",
        "USE_SINOGRAM",
        "ANGLE_MODE",
        "SINOGRAM_LINE",
        "AXIS_URL_1",
        "AXIS_URL_2",
        "LOOK_AT_STDMAX",
        "NEAR_WX",
        "FINE_STEP_X",
        "SCALE_IMG2_TO_IMG1",
        "NEAR_POSITION",
        "MOTOR_OFFSET",
        "X_ROTATION_AXIS_PIXEL_POSITION",
        "SINOGRAM_SUBSAMPLING",
        "PADDING_MODE",
        "FLIP_LR",
        "COMPOSITE_OPTS",
        "COR_OPTIONS",
    )

    def __init__(self):
        self.__mode = AxisMode.manual
        """Mode used for defining the COR (center of rotation)"""
        self.__relative_value = None
        """Value of the center of rotation in [0; image_width].
        None is not processing.
        This value is on the *raw* frames referential as expected by nabu. It means it doesn't take into account
        possible detector flips.
        """
        self.__absolute_value = None
        """
        Value of the center of rotation in [-image_width/2; image_width/2].
        None is not processing.
        This value is on the *raw* frames referential as expected by nabu. It means it doesn't take into account
        possible detector flips.
        """
        self.__angle_mode = CorAngleMode.use_0_180
        """Angle to use for radios"""
        self.__x_rotation_axis_pixel_position = None
        """rotation axis position obtained from motor. In the **raw** frame referential."""
        self.__x_rotation_axis_pos_px_offset = 0.0
        """motor offset to be used to compute the 'estimated_cor' from 'x_rotation_axis_pixel_position'"""
        self.__estimated_cor = 0.0
        """Estimated position of the center of rotation. Given by the user or computed from 'x_rotation_axis_pixel_position' and 'pixel_offset'.
        In the **raw** frame referential.
        """
        self.__axis_url_1 = AxisResource(url=None)
        """first data url to use for axis cor calculation"""
        self.__axis_url_2 = AxisResource(url=None)
        """second data url to use for axis cor calculation"""
        self.__calculation_input_type = AxisCalculationInput.transmission
        """Type of input (emission, absorption, with or without paganin)"""
        self.__sinogram_line = "middle"
        """Line of the radios to use for getting the sinogram"""
        self.__sinogram_subsampling = 10
        """if use sinogram activate, we can use a subsampling to reduce
        computation time"""
        self.__look_at_stdmax = False
        """do the near search at X position which as the max Y column standard
        deviation"""
        self.__composite_window_size = 5
        """do the near search in an X window of size +-near_wx"""
        self.__composite_fine_step = 0.1
        """shift step x for fine shifting image"""
        self.__scale_img2_to_img1 = False
        """do image scaling"""
        self.__padding_mode = None
        self.__frame_width = None
        self.__flip_lr = True
        self.__composite_options = {
            "theta": DEFAULT_CMP_THETA,
            "n_subsampling_y": DEFAULT_CMP_N_SUBSAMPLING_Y,
            "oversampling": DEFAULT_CMP_OVERSAMPLING,
            "take_log": DEFAULT_CMP_TAKE_LOG,
            "near_pos": DEFAULT_CMP_NEAR_POS,
            "near_width": DEFAULT_CMP_NEAR_WIDTH,
        }
        """specific options for composite cor search"""
        self.__extra_cor_options = ""
        """Automatic cor options as str. side, near_pos and near_width are provided independantly"""

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = AxisMode.from_value(mode)
        self.changed()

    @property
    def frame_width(self) -> float | None:
        return self.__frame_width

    @frame_width.setter
    def frame_width(self, value):
        if not isinstance(value, (type(None), float, int)):
            raise TypeError(
                f"Value is expected to be None or a float. Not {type(value)}"
            )
        if value is None:
            self.__frame_width = value
        else:
            self.__frame_width = float(value)

    @property
    def angle_mode(self):
        return self.__angle_mode

    @angle_mode.setter
    def angle_mode(self, mode):
        if type(mode) is str:
            mode = CorAngleMode.from_value(mode)

        if self.__angle_mode != mode:
            self.__angle_mode = mode
            self.changed()

    @property
    def relative_cor_value(self):
        return self.__relative_value

    @property
    def absolute_cor_value(self):
        return self.__absolute_value

    def set_relative_value(self, value):
        if not isinstance(value, (int, float, str, type(None))):
            raise TypeError(
                f"value is expected to be an instance of {int}, {float}, {str}, or {None}. {type(value)} provided"
            )
        if value is None:
            changed = self.__relative_value is not None
        elif isinstance(value, str) and value == "...":
            changed = self.__relative_value != "..."
        else:
            changed = self.__relative_value != float(value)
        if changed:
            if value is None or (isinstance(value, str) and value == "..."):
                self.__relative_value = value
                self.__absolute_value = value
            else:
                self.__relative_value = float(value)
                if self.frame_width is not None:
                    self.__absolute_value = relative_pos_to_absolute(
                        relative_pos=self.__relative_value, det_width=self.frame_width
                    )
            self.changed()

    @property
    def estimated_cor(self) -> Side | float | None:
        return self.__estimated_cor

    @estimated_cor.setter
    def estimated_cor(self, value: Side | float | None):
        try:
            value = Side(value)
        except ValueError:
            pass
        if self.__estimated_cor != value:
            self.__estimated_cor = value
            self.changed()

    @property
    def x_rotation_axis_pos_px_offset(self) -> float:
        return self.__x_rotation_axis_pos_px_offset

    @x_rotation_axis_pos_px_offset.setter
    def x_rotation_axis_pos_px_offset(self, value: float):
        assert isinstance(
            value, float
        ), f"x_rotation_axis_pos_px_offset should be a float. Got {type(value)}"
        self.__x_rotation_axis_pos_px_offset = value

    @property
    def x_rotation_axis_pixel_position(self) -> float | None:
        return self.__x_rotation_axis_pixel_position

    @x_rotation_axis_pixel_position.setter
    def x_rotation_axis_pixel_position(self, value: float | None):
        assert isinstance(
            value, (float, type(None))
        ), f"x_rotation_axis_pixel_position should be None or a float. Got{type(value)}"
        self.__x_rotation_axis_pixel_position = value

    @property
    def axis_url_1(self):
        """the first file to be used for the axis calculation"""
        return self.__axis_url_1

    def _get_rsrc_frm_url(self, old_resource, new_url_):
        """
        Util function to compare new resource / url with an existing one.
        """
        new_resource = None
        changed = False
        if isinstance(new_url_, AxisResource):
            if old_resource != new_url_:
                changed = True
                new_resource = new_url_
        elif isinstance(new_url_, str):
            if new_url_ == "":
                new_resource = AxisResource(None)
            else:
                new_resource = AxisResource(DataUrl(path=new_url_))
            if old_resource != new_resource:
                changed = True
        else:
            assert isinstance(new_url_, DataUrl) or new_url_ is None
            new_resource = AxisResource(new_url_)
            if old_resource != new_resource:
                changed = True
        return new_resource, changed

    @axis_url_1.setter
    def axis_url_1(self, url_):
        new_resource, changed = self._get_rsrc_frm_url(
            old_resource=self.__axis_url_1, new_url_=url_
        )
        if changed is True:
            self.__axis_url_1 = new_resource
            self.axis_urls_changed()

    @property
    def axis_url_2(self):
        """the second file to be used for the axis calculation"""
        return self.__axis_url_2

    @axis_url_2.setter
    def axis_url_2(self, url_):
        new_resource, changed = self._get_rsrc_frm_url(
            old_resource=self.__axis_url_2, new_url_=url_
        )
        if changed is True:
            self.__axis_url_2 = new_resource
            self.axis_urls_changed()

    @property
    def flip_lr(self):
        return self.__flip_lr

    @flip_lr.setter
    def flip_lr(self, flip: bool):
        if not isinstance(flip, bool):
            raise TypeError("flip should be a boolean")
        self.__flip_lr = flip

    @property
    def projection_type(self):
        return self.__calculation_input_type.value.projection_type

    @property
    def paganin_preproc(self):
        return self.__calculation_input_type.value.paganin

    @property
    def calculation_input_type(self):
        return self.__calculation_input_type

    @calculation_input_type.setter
    def calculation_input_type(self, type_):
        assert isinstance(type_, AxisCalculationInput)
        value = AxisCalculationInput.from_value(type_)
        if value != self.__calculation_input_type:
            self.__calculation_input_type = type_
            self.changed()

    @property
    def sinogram_line(self):
        return self.__sinogram_line

    @sinogram_line.setter
    def sinogram_line(self, line):
        if line == "":
            if self.__sinogram_line is not None:
                self.__sinogram_line = None
                self.changed()
        else:
            if line == "middle":
                line = line
            elif line is not None:
                line = int(line)
            if self.__sinogram_line != line:
                self.__sinogram_line = line
                self.changed()

    @property
    def sinogram_subsampling(self) -> int:
        """Subsample radio to speed up processing of the sinogram generation"""
        return self.__sinogram_subsampling

    @sinogram_subsampling.setter
    def sinogram_subsampling(self, subsampling: int) -> None:
        subsampling = int(subsampling)
        if subsampling != self.__sinogram_subsampling:
            self.__sinogram_subsampling = subsampling
            self.changed()

    @property
    def look_at_stdmax(self):
        return self.__look_at_stdmax

    @look_at_stdmax.setter
    def look_at_stdmax(self, stdmax):
        self.__look_at_stdmax = stdmax

    @property
    def composite_window_size(self):
        return self.__composite_window_size

    @composite_window_size.setter
    def composite_window_size(self, width):
        if self.__composite_window_size != width:
            self.__composite_window_size = width
            self.changed()

    @property
    def composite_fine_step(self):
        """Fine step along x axis"""
        return self.__composite_fine_step

    @composite_fine_step.setter
    def composite_fine_step(self, step_size):
        if self.__composite_fine_step != step_size:
            self.__composite_fine_step = step_size
            self.changed()

    @property
    def scale_img2_to_img1(self):
        return self.__scale_img2_to_img1

    @scale_img2_to_img1.setter
    def scale_img2_to_img1(self, scale):
        if self.__scale_img2_to_img1 != scale:
            self.__scale_img2_to_img1 = scale
            self.changed()

    @property
    def extra_cor_options(self) -> str:
        return self.__extra_cor_options

    @extra_cor_options.setter
    def extra_cor_options(self, cor_options: str):
        if not isinstance(cor_options, str):
            raise TypeError(f"{type(cor_options)} provided when {str} expected")
        else:
            clean_opts_str = (
                cor_options.replace(" ", "").strip(";").rstrip(";").replace(";", " ; ")
            )
            self.__extra_cor_options = clean_opts_str
            self.changed()

    @property
    def composite_options(self) -> dict:
        """return specific options for composite cor search"""
        return self.__composite_options

    @composite_options.setter
    def composite_options(self, opts: dict) -> None:
        """
        :param opts: options to use for the composite COR search
        :raises:
            * KeyError if some provided keys are not handled
            * TypeError if opts is not an instance of dictionary
        """
        if not isinstance(opts, dict):
            raise TypeError(
                f"opts is expected to be an instance of dict not {type(opts)}"
            )
        # insure backward compatibility
        if "subsampling_y" in opts:
            opts["n_subsampling_y"] = opts.pop("subsampling_y")
        for key in opts.keys():
            if key not in (
                "theta",
                "oversampling",
                "n_subsampling_y",
                "take_log",
                "near_pos",
                "near_width",
            ):
                raise KeyError(f"{key} is not recognized")
        self.__composite_options = opts

    @property
    def padding_mode(self):
        return self.__padding_mode

    @padding_mode.setter
    def padding_mode(self, mode):
        if self.__padding_mode != mode:
            self.__padding_mode = mode
            self.changed()

    def changed(self):
        """callback to overwrite when the parameter value changed"""
        pass

    def n_url(self):
        """

        :return: number of available url from url_1, url_2
        """
        n_url = 0
        if self.axis_url_1 and self.axis_url_1.url:
            n_url += 1
        if self.axis_url_2 and self.axis_url_2.url:
            n_url += 1
        return n_url

    def to_dict(self):
        # keep octave compatibility
        axis_urls_1 = self.axis_url_1.url
        if axis_urls_1 is None:
            axis_urls_1 = ""
        else:
            axis_urls_1 = axis_urls_1.path()
        axis_urls_2 = self.axis_url_2.url
        if axis_urls_2 is None:
            axis_urls_2 = ""
        else:
            axis_urls_2 = axis_urls_2.path()

        _dict = {
            "MODE": self.mode.value,
            "POSITION_VALUE": self.relative_cor_value,
            "CALC_INPUT_TYPE": self.calculation_input_type.to_dict(),
            "ANGLE_MODE": self.angle_mode.value,
            "SINOGRAM_LINE": (
                self.sinogram_line if self.mode.requires_sinogram_index() else ""
            ),
            "SINOGRAM_SUBSAMPLING": self.sinogram_subsampling,
            "AXIS_URL_1": axis_urls_1,
            "AXIS_URL_2": axis_urls_2,
            "LOOK_AT_STDMAX": self.look_at_stdmax,
            "NEAR_WX": self.composite_window_size,
            "FINE_STEP_X": self.composite_fine_step,
            "SCALE_IMG2_TO_IMG1": self.scale_img2_to_img1,
            "NEAR_POSITION": (
                self.estimated_cor.value
                if isinstance(self.estimated_cor, Side)
                else self.estimated_cor
            ),
            "PADDING_MODE": self.padding_mode,
            "FLIP_LR": self.flip_lr,
            "COMPOSITE_OPTS": self.composite_options,
            "COR_OPTIONS": self.extra_cor_options,
            "MOTOR_OFFSET": self.x_rotation_axis_pos_px_offset,
            "X_ROTATION_AXIS_PIXEL_POSITION": self.x_rotation_axis_pixel_position,
        }
        return _dict

    @staticmethod
    def from_dict(_dict):
        axis = AxisRP()
        axis.load_from_dict(_dict=_dict)
        return axis

    def load_from_dict(self, _dict):
        # Convert managed keys to upper case
        _dict = {
            key.upper() if key.upper() in self._MANAGED_KEYS else key: value
            for key, value in _dict.items()
        }

        if "MODE" in _dict:
            self.mode = _dict["MODE"]
        if "POSITION_VALUE" in _dict:
            self.set_relative_value(_dict["POSITION_VALUE"])
        if "CALC_INPUT_TYPE" in _dict:
            self.calculation_input_type = AxisCalculationInput.from_value(
                _dict["CALC_INPUT_TYPE"]
            )
        if "ANGLE_MODE" in _dict:
            self.angle_mode = CorAngleMode.from_value(_dict["ANGLE_MODE"])
        if "SINOGRAM_LINE" in _dict:
            self.sinogram_line = _dict["SINOGRAM_LINE"]
        if "AXIS_URL_1" in _dict:
            self.axis_url_1 = _dict["AXIS_URL_1"]
        if "AXIS_URL_2" in _dict:
            self.axis_url_2 = _dict["AXIS_URL_2"]
        if "LOOK_AT_STDMAX" in _dict:
            self.look_at_stdmax = _dict["LOOK_AT_STDMAX"]
        if "NEAR_WX" in _dict:
            self.composite_window_size = _dict["NEAR_WX"]
        if "FINE_STEP_X" in _dict:
            self.composite_fine_step = _dict["FINE_STEP_X"]
        if "SCALE_IMG2_TO_IMG1" in _dict:
            self.scale_img2_to_img1 = _dict["SCALE_IMG2_TO_IMG1"]
        if "NEAR_POSITION" in _dict:
            self.estimated_cor = _dict["NEAR_POSITION"]
        if "SINOGRAM_SUBSAMPLING" in _dict:
            self.sinogram_subsampling = _dict["SINOGRAM_SUBSAMPLING"]
        if "PADDING_MODE" in _dict:
            self.padding_mode = _dict["PADDING_MODE"]
        if "FLIP_LR" in _dict:
            self.flip_lr = bool(_dict["FLIP_LR"])
        if "COMPOSITE_OPTS" in _dict:
            self.composite_options = _dict["COMPOSITE_OPTS"]
        self.extra_cor_options = _dict.get("COR_OPTIONS", "")

    def copy(self, axis_params, copy_axis_url=True, copy_flip_lr=True):
        assert isinstance(axis_params, AxisRP)
        self.mode = axis_params.mode
        self.frame_width = axis_params.frame_width
        self.set_relative_value(axis_params.relative_cor_value)
        self.calculation_input_type = axis_params.calculation_input_type
        self.angle_mode = axis_params.angle_mode
        self.sinogram_line = axis_params.sinogram_line
        self.sinogram_subsampling = axis_params.sinogram_subsampling
        self.look_at_stdmax = axis_params.look_at_stdmax
        self.composite_window_size = axis_params.composite_window_size
        self.composite_fine_step = axis_params.composite_fine_step
        self.scale_img2_to_img1 = axis_params.scale_img2_to_img1
        self.estimated_cor = axis_params.estimated_cor
        self.x_rotation_axis_pixel_position = axis_params.x_rotation_axis_pixel_position
        self.x_rotation_axis_pos_px_offset = axis_params.x_rotation_axis_pos_px_offset
        self.padding_mode = axis_params.padding_mode
        self.composite_options = axis_params.composite_options
        self.extra_cor_options = axis_params.extra_cor_options
        if copy_axis_url:
            self.axis_url_1 = axis_params.axis_url_1
            self.axis_url_2 = axis_params.axis_url_2
        if copy_flip_lr:
            self.flip_lr = axis_params.flip_lr

    def __str__(self):
        return str(self.to_dict())

    def axis_urls_changed(self):
        """Callback when the axis url change"""
        pass

    def get_simple_str(self):
        """
        special information as a str for mode able to handle both sinogram and radios
        """
        results = f"{self.mode.value}"
        if self.mode in (
            AxisMode.growing_window_radios,
            AxisMode.growing_window_sinogram,
            AxisMode.sliding_window_radios,
            AxisMode.sliding_window_sinogram,
        ):
            extra_info = f"side: {self.estimated_cor}"
            results = ", ".join((results, extra_info))
        return results

    def get_nabu_cor_options_as_dict(self) -> str:
        options = {}
        # provide side. Scalar if a first guess is provided else a value in ('left', 'right', 'center', 'all')
        if (
            isinstance(self.estimated_cor, Side)
            and AXIS_MODE_METADATAS[self.mode].valid_sides
        ):
            options["side"] = self.estimated_cor.value
        elif AXIS_MODE_METADATAS[self.mode].allows_estimated_cor_as_numerical_value:
            options["side"] = self.estimated_cor

        if self.mode in (AxisMode.composite_coarse_to_fine, AxisMode.near):
            options["near_width"] = self.composite_options.get(
                "near_width", DEFAULT_CMP_NEAR_WIDTH
            )
            options["theta_interval"] = self.composite_options.get(
                "theta_interval", DEFAULT_CMP_THETA
            )
            options["oversampling"] = self.composite_options.get(
                "oversampling", DEFAULT_CMP_OVERSAMPLING
            )
            options["n_subsampling_y"] = self.composite_options.get(
                "n_subsampling_y", DEFAULT_CMP_N_SUBSAMPLING_Y
            )
            options["take_log"] = self.composite_options.get(
                "take_log", DEFAULT_CMP_TAKE_LOG
            )

        # provide radio indices or sinogram index
        if self.mode.requires_radio_indices:
            # warning: nabu expect radio angles to be in rad, in nxtomo and tomwer they are in degrees
            options["radio_angles"] = (
                numpy.deg2rad(self.axis_url_1.angle or 0.0),
                numpy.deg2rad(self.axis_url_2.angle or 180.0),
            )
        if self.mode.requires_sinogram_index:
            options["slice_idx"] = self.sinogram_line

        # append "extra_cor_options" to already handled cor options
        # expected values: low_pass, high_pass
        extra_cor_options = self.extra_cor_options.replace(" ", "")

        if extra_cor_options != "":
            for opt in self.extra_cor_options.replace(" ", "").split(";"):
                if len(opt.split("=")) == 2:
                    key, value = opt.split("=")
                    if key in ("low_pass", "high_pass"):
                        value = float(value)
                        options[key] = value
                    else:
                        _logger.warning(
                            f"key {key} is not recognized by nabu. Ignore it."
                        )
                else:
                    _logger.info(f"ignore option {opt}. Invalid syntax")
        return options
