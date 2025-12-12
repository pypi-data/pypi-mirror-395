from __future__ import annotations

import weakref
import logging
import numpy

from tomoscan.tomoobject import TomoObject
from tomoscan.scanbase import TomoScanBase
from tomoscan.volumebase import VolumeBase

_logger = logging.getLogger(__name__)


class StitchingMetadata:
    """
    overload of a TomoObject to register metadata set by the user on positions
    """

    KEY_PIXEL_OR_VOXEL_SIZE = "pixel_or_voxel_size"
    KEY_PIXEL_POSITION = "position_px"
    KEY_METRIC_POSITION = "position_m"

    def __init__(self, tomo_obj) -> None:
        super().__init__()
        if tomo_obj is None:
            self._tomo_obj = None
        else:
            self._tomo_obj = weakref.ref(tomo_obj)
        self._pixel_or_voxel_size = [None, None, None]
        self._pos_as_px = [None, None, None]
        self._pos_as_m = [None, None, None]

    @property
    def tomo_obj(self) -> TomoObject:
        if self._tomo_obj is None:
            return None
        else:
            return self._tomo_obj()

    def setPixelOrVoxelSize(self, value, axis):
        if value is not None and not isinstance(
            value, (float, numpy.float32, numpy.float64)
        ):
            raise TypeError(f"Invalid type for value. Got {type(value)}")
        self._pixel_or_voxel_size[axis] = value

    def setPxPos(self, value, axis):
        if value is not None and not isinstance(value, (int, numpy.int32)):
            raise TypeError(f"Invalid type for value. Got {type(value)}")
        self._pos_as_px[axis] = value

    def setMetricPos(self, value, axis):
        if value is not None and not isinstance(
            value, (int, numpy.float32, numpy.float64, float)
        ):
            raise TypeError(f"Invalid type for value. Got {type(value)}")
        self._pos_as_m[axis] = value

    def get_raw_position_m(self, axis):
        if self.tomo_obj is None:
            return
        bb = self.tomo_obj.get_bounding_box(axis)
        return (bb.max - bb.min) / 2 + bb.min

    def get_abs_position_px(self, axis, warn=True) -> int | None:
        if axis not in (0, 1, 2):
            raise ValueError("axis is expected to be in (0, 1, 2)")
        # if user registered position as pixels
        if self._pos_as_px[axis] is not None:
            return int(self._pos_as_px[axis])
        else:
            # get position as m from the user input
            pos_as_m = self._pos_as_m[axis]
            # or from metadata if not provided
            if pos_as_m is None:
                try:
                    pos_as_m = self.get_raw_position_m(axis=axis)
                except Exception as e:
                    if warn:
                        _logger.warning(
                            f"Fail to get bounding box of {self.tomo_obj}. Error is {e}"
                        )
                    return None
            # else if user registered position as meter
            pixel_or_voxel_size = self.get_pixel_or_voxel_size(axis=axis)
            if pixel_or_voxel_size is None:
                if warn:
                    if isinstance(self.tomo_obj, TomoScanBase):
                        missing = "pixel"
                    else:
                        missing = "voxel"
                    _logger.warning(
                        f"Unable to get {missing} from {self.tomo_obj}. Please provide it manually"
                    )
                return None
            else:
                return int(pos_as_m / pixel_or_voxel_size)

    def reset(self):
        self._pixel_or_voxel_size = [None, None, None]
        self._pos_as_px = [None, None, None]
        self._pos_as_m = [None, None, None]

    def get_pixel_or_voxel_size(self, axis) -> float | None:
        """
        return value provided by the user if any else return the value contained in metadata
        """
        if self.tomo_obj is None:
            return
        if self._pixel_or_voxel_size[axis] is not None:
            return self._pixel_or_voxel_size[axis]
        elif isinstance(self.tomo_obj, TomoScanBase):
            if axis == 0:
                return self.tomo_obj.sample_y_pixel_size
            elif axis in (1, 2):
                return self.tomo_obj.sample_x_pixel_size
            else:
                raise TypeError(f"axis is expected to be in (0, 1, 2). {axis} provided")
        elif isinstance(self.tomo_obj, VolumeBase):
            voxel_size = self.tomo_obj.voxel_size
            if voxel_size is None:
                return None
            else:
                return voxel_size[axis]
        else:
            raise NotImplementedError

    def to_dict(self) -> dict:
        def cast_values(values):
            return ",".join(["" if val is None else str(val) for val in values])

        return {
            self.KEY_PIXEL_OR_VOXEL_SIZE: cast_values(self._pixel_or_voxel_size),
            self.KEY_PIXEL_POSITION: cast_values(self._pos_as_px),
            self.KEY_METRIC_POSITION: cast_values(self._pos_as_m),
        }

    @staticmethod
    def from_dict(ddict, tomo_obj):
        res = StitchingMetadata(tomo_obj=tomo_obj)
        res.load_from_dict(ddict)
        return res

    def load_from_dict(self, ddict) -> dict:
        def cast_str(my_str: str, expected_type):
            return list(
                [
                    None if part_ == "" else expected_type(part_)
                    for part_ in my_str.split(",")
                ]
            )

        if self.KEY_METRIC_POSITION in ddict:
            self._pos_as_m = cast_str(
                ddict[self.KEY_METRIC_POSITION], expected_type=float
            )
        if self.KEY_PIXEL_POSITION in ddict:
            self._pos_as_px = cast_str(
                ddict[self.KEY_PIXEL_POSITION], expected_type=int
            )
        if self.KEY_PIXEL_OR_VOXEL_SIZE in ddict:
            self._pixel_or_voxel_size = cast_str(
                ddict[self.KEY_PIXEL_OR_VOXEL_SIZE], expected_type=float
            )

    def __eq__(self, __o: object) -> bool:
        return (
            self._pixel_or_voxel_size == __o._pixel_or_voxel_size
            and self._pos_as_px == __o._pos_as_px
            and self._pos_as_m == __o._pos_as_m
        )

    def __str__(self) -> str:
        metadatas = {
            "pixel_or_voxel_size": self._pixel_or_voxel_size,
            "metric position (m)": self._pos_as_m,
            "pixel position (px)": self._pos_as_px,
        }
        metadata_str = "\n -".join(
            [f"{key}: {value}" for key, value in metadatas.items()]
        )
        tomo_obj = self.tomo_obj or "?"
        return (
            f"user override stitching metadata for {tomo_obj} metadata: \n"
            + metadata_str
        )
