# coding: utf-8
from __future__ import annotations

import enum

from tomoscan.framereducer.method import ReduceMethod

from tomwer.core.process.reconstruction.darkref.settings import (
    DARKHST_PREFIX,
    REFHST_PREFIX,
)
from tomwer.core.process.reconstruction.paramsbase import _ReconsParam
from tomwer.core.utils.deprecation import deprecated


# TODO: those classes (when, method) should be linked / embedded in the DarkRef
# method
@enum.unique
class When(enum.Enum):
    never = (0,)
    before = (1,)
    after = (2,)


def _from_value_reduce_method_backward_compatibility(value) -> ReduceMethod:
    if value in ("none", 0, (0,)):
        return ReduceMethod.NONE
    elif value in ("average", 1, (1,)):
        return ReduceMethod.MEAN
    elif value in ("median", 2, (2,)):
        return ReduceMethod.MEDIAN
    elif value in ("first", 10, (10,)):
        return ReduceMethod.FIRST
    elif value in ("last", 11, (11,)):
        return ReduceMethod.FIRST
    else:
        return ReduceMethod(value)


class DKRFRP(_ReconsParam):
    """Settings for the calculation of dark and flat fields mean or median"""

    def __init__(self):
        _ReconsParam.__init__(self)
        self.__do_when = When.before
        self.__dark_calc = ReduceMethod.MEAN
        self.__overwrite_dark = False
        self.__remove_dark = False
        self.__dark_pattern = "darkend[0-9]{3,4}"
        self.__flat_calc = ReduceMethod.MEDIAN
        self.__overwrite_flat = False
        self.__remove_flats = False
        self.__flat_pattern = "ref*.*[0-9]{3,4}_[0-9]{3,4}"
        self.__dark_prefix = DARKHST_PREFIX
        self.__ref_prefix = REFHST_PREFIX

        self._managed_params = {
            "DOWHEN": self.__class__.do_when,
            "DARKCAL": self.__class__.dark_calc_method,
            "DARKOVE": self.__class__.overwrite_dark,
            "DARKRMV": self.__class__.remove_dark,
            "DKFILE": self.__class__.dark_pattern,
            "REFSCAL": self.__class__.flat_calc_method,
            "REFSOVE": self.__class__.overwrite_flat,
            "REFSRMV": self.__class__.remove_raw_flats,
            "RFFILE": self.__class__.flat_pattern,
        }

    @property
    def do_when(self):
        """When should we process calculation. Should be removed now that DKRF
        process exists. Was needed for fastomo3"""
        return self.__do_when

    @do_when.setter
    def do_when(self, when):
        assert isinstance(when, (int, When))
        when = When(when)
        if when != self.__do_when:
            self.__do_when = when
            self.changed()

    @property
    def dark_calc_method(self):
        """Dark calculation Method"""
        return self.__dark_calc

    @dark_calc_method.setter
    def dark_calc_method(self, method):
        assert isinstance(method, (int, ReduceMethod, str))
        _dark_calc = _from_value_reduce_method_backward_compatibility(method)

        if self.__dark_calc != _dark_calc:
            self.__dark_calc = _dark_calc
            self.changed()

    @property
    def overwrite_dark(self):
        """Overwrite Dark results if already exists"""
        return self.__overwrite_dark

    @overwrite_dark.setter
    def overwrite_dark(self, overwrite):
        assert isinstance(overwrite, (int, bool, float))
        _overwrite_dark = bool(overwrite)
        if self.__overwrite_dark != _overwrite_dark:
            self.__overwrite_dark = _overwrite_dark
            self.changed()

    @property
    def remove_dark(self):
        """Remove original Darks files when done"""
        return self.__remove_dark

    @remove_dark.setter
    def remove_dark(self, remove):
        assert isinstance(remove, (int, bool, float))
        _remove_dark = bool(remove)
        if _remove_dark != self.__remove_dark:
            self.__remove_dark = _remove_dark
            self.changed()

    @property
    def dark_pattern(self):
        """File pattern to detect edf Dark field"""
        return self.__dark_pattern

    @dark_pattern.setter
    def dark_pattern(self, pattern):
        _dark_pattern = pattern
        if self.__dark_pattern != _dark_pattern:
            self.__dark_pattern = _dark_pattern
            self.changed()

    @property
    def flat_calc_method(self):
        """Dark calculation method (None, Average, Median)"""
        return self.__flat_calc

    @flat_calc_method.setter
    def flat_calc_method(self, method):
        assert isinstance(method, (int, ReduceMethod, str))
        _ref_calc = _from_value_reduce_method_backward_compatibility(method)
        if self.__flat_calc != _ref_calc:
            self.__flat_calc = _ref_calc
            self.changed()

    @property
    @deprecated(replacement="overwrite_flat", since_version="0.9")
    def overwrite_ref(self):
        return self.overwrite_flat

    @overwrite_ref.setter
    @deprecated(replacement="overwrite_flat", since_version="0.9")
    def overwrite_ref(self, overwrite):
        self.overwrite_flat = overwrite

    @property
    def overwrite_flat(self):
        """Overwrite Dark results if already exists"""
        return self.__overwrite_flat

    @overwrite_flat.setter
    def overwrite_flat(self, overwrite):
        assert isinstance(overwrite, (int, bool, float))
        _overwrite_flat = bool(overwrite)
        if self.__overwrite_flat != _overwrite_flat:
            self.__overwrite_flat = _overwrite_flat
            self.changed()

    @property
    def remove_raw_flats(self):
        """Remove original flat / ref files when done (for EDF only)"""
        return self.__remove_flats

    @remove_raw_flats.setter
    def remove_raw_flats(self, remove):
        # TODO: float should be removed, but this is a legacy from fastomo3
        assert isinstance(remove, (int, bool, float))
        _remove_flats = remove
        if self.__remove_flats != _remove_flats:
            self.__remove_flats = _remove_flats
            self.changed()

    @property
    def flat_pattern(self):
        """File pattern to detect EDF flats files"""
        return self.__flat_pattern

    @flat_pattern.setter
    def flat_pattern(self, pattern):
        if pattern != self.__flat_pattern:
            self.__flat_pattern = pattern
            self.changed()

    @property
    def flat_prefix(self):
        """flat prefix for EDF"""
        return self.__ref_prefix

    @flat_prefix.setter
    def flat_prefix(self, prefix):
        if prefix != self.__ref_prefix:
            self.__ref_prefix = prefix
            self.changed()

    @property
    def dark_prefix(self):
        """dark prefix for EDF"""
        return self.__dark_prefix

    @dark_prefix.setter
    def dark_prefix(self, prefix):
        if prefix != self.__dark_prefix:
            self.__dark_prefix = prefix
            self.changed()

    def _set_remove_opt(self, rm):
        self.remove_raw_flats = rm
        self.remove_dark = rm

    def _set_skip_if_exist(self, skip):
        self.overwrite_flat = not skip
        self.overwrite_dark = not skip

    def to_dict(self):
        _dict = {
            "DOWHEN": self.do_when.name,
            "DARKCAL": self.dark_calc_method.value,
            "DARKOVE": int(self.overwrite_dark),
            "DARKRMV": int(self.remove_dark),
            "DKFILE": self.dark_pattern,
            "REFSCAL": self.flat_calc_method.value,
            "REFSOVE": int(self.overwrite_flat),
            "REFSRMV": int(self.remove_raw_flats),
            "RFFILE": self.flat_pattern,
        }
        _dict.update(self.unmanaged_params)
        return _dict

    @staticmethod
    def from_dict(_dict):
        params = DKRFRP()
        params.load_from_dict(_dict)
        return params

    def load_from_dict(self, _dict):
        # Convert managed keys to upper case
        _dict = {
            key.upper() if key.upper() in self.managed_params else key: value
            for key, value in _dict.items()
        }

        self._load_unmanaged_params(_dict=_dict)
        if "DOWHEN" in _dict:
            self.do_when = getattr(When, _dict["DOWHEN"])
        if "DARKCAL" in _dict:
            self.dark_calc_method = _dict["DARKCAL"]
        if "DARKOVE" in _dict:
            self.overwrite_dark = _dict["DARKOVE"]
        if "DARKRMV" in _dict:
            self.remove_dark = _dict["DARKRMV"]
        if "DKFILE" in _dict:
            self.dark_pattern = _dict["DKFILE"]
        if "REFSCAL" in _dict:
            self.flat_calc_method = _dict["REFSCAL"]
        if "REFSOVE" in _dict:
            self.overwrite_flat = _dict["REFSOVE"]
        if "REFSRMV" in _dict:
            self.remove_raw_flats = _dict["REFSRMV"]
        if "RFFILE" in _dict:
            self.flat_pattern = _dict["RFFILE"]
