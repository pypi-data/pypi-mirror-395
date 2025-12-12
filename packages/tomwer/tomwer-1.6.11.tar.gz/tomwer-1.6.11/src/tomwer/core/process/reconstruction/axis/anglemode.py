# coding: utf-8

from enum import Enum as _Enum


class CorAngleMode(_Enum):
    use_0_180 = "0-180"
    use_90_270 = "90-270"
    manual_selection = "manual"

    @classmethod
    def from_value(cls, value):
        # TODO: back compatibility if is int
        if value == 0:
            return CorAngleMode.use_0_180
        elif value == 1:
            return CorAngleMode.use_90_270
        elif value == 2:
            return CorAngleMode.manual_selection
        else:
            return CorAngleMode(value=value)
