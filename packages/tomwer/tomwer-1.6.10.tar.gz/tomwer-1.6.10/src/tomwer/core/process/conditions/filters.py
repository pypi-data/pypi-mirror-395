# coding: utf-8
"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""
from __future__ import annotations


import fnmatch
import logging
import os
import re

import tomwer.version
from tomwer.core.process.task import Task
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory

from tomwer.core.utils.deprecation import deprecated_warning

_logger = logging.getLogger(__name__)


class BaseFilter(object):
    """
    Apply a filter to an object
    """

    def description(self):
        pass

    def isFiltered(self, value):
        """
        Return True if the value not filtered

        """
        raise NotImplementedError("Base class")


class _PatternBaseFilter(BaseFilter):
    """Filter based on a pattern"""

    def __init__(self, pattern):
        BaseFilter.__init__(self)
        self.setPattern(pattern)

    def setPattern(self, pattern):
        """
        compile th filter for the given pattern
        :param pattern:
        """
        self._pattern = pattern

    def getPattern(self):
        return self._pattern


class RegularExpressionFilter(_PatternBaseFilter):
    """Filter a string based on a defined pattern"""

    def __init__(self, pattern):
        _PatternBaseFilter.__init__(self, pattern=pattern)

    def setPattern(self, pattern):
        """
        compile th filter for the given pattern
        :param pattern:
        """
        super().setPattern(pattern)
        if self._pattern is not None:
            try:
                self._filter = re.compile(self._pattern)
            except re.error as e:
                self.unvalidPatternDefinition(self, self._pattern, e)
                _logger.error(e)

    def description(self):
        return "Filter a string base on a regular expression"

    def isFiltered(self, value):
        try:
            match = self._filter.match(value) is None
        except Exception:
            return False
        else:
            return match

    def unvalidPatternDefinition(self, cls, pattern, error):
        _logger.error(f"{cls} {pattern} is not a valid pattern. Error is {error}")


class UnixFileNamePatternFilter(_PatternBaseFilter):
    """Filter a string based on 'fnmatch' module (unix filename pattern
    matching)"""

    def __init__(self, pattern):
        _PatternBaseFilter.__init__(self, pattern)

    def description(self):
        return "Filter a string base on a glob (unix style pathname)"

    def isFiltered(self, value):
        try:
            match = fnmatch.fnmatch(value, self._pattern)
        except Exception:
            match = False
        return not match


class FileNameFilterTask(
    _PatternBaseFilter,
    Task,
    input_names=("data", "pattern"),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """
    Task to filter a scan according to his name and a 'unix file name pattern' or a 'regular expression'
    """

    UNIX_PATTERN_FILTER = "unix file name pattern"

    REGULAR_EXP_FILTER = "regular expression"

    FILTER_TYPES = UNIX_PATTERN_FILTER, REGULAR_EXP_FILTER

    _DEFAULT_FILTER_TYPE = FILTER_TYPES[0]

    _FILTER_CONSTR = {
        UNIX_PATTERN_FILTER: UnixFileNamePatternFilter,
        REGULAR_EXP_FILTER: RegularExpressionFilter,
    }

    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        pattern = inputs.get("pattern", None)
        if pattern is None:
            raise ValueError("'pattern' should be provided")
        filter_type = inputs.get("filter_type", self._DEFAULT_FILTER_TYPE)
        self._invert = inputs.get("invert_result", False)

        self._filter = self._FILTER_CONSTR[filter_type](pattern)

        _PatternBaseFilter.__init__(self, pattern)

    @property
    def invert_result(self):
        return self._invert

    @property
    def filter(self):
        return self._filter

    def isFiltered(self, value):
        result = self._filter.isFiltered(value)
        if self.invert_result:
            return not result
        else:
            return result

    def run(self):
        scan = self.inputs.data
        if scan is None:
            raise ValueError("'data' should be provided")
        if isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        if scan is None:
            return False
        assert isinstance(scan, TomwerScanBase)

        if not self.isFiltered(os.path.basename(scan.path)):
            if self.get_input_value("serialize_output_data", True):
                self.outputs.data = scan.to_dict()
            else:
                self.outputs.data = scan
        else:
            self.outputs.data = None

    @staticmethod
    def program_name():
        return "scan filter"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "filter a scan according to his name"


class FileNameFilter(FileNameFilterTask):
    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        deprecated_warning(
            name="tomwer.core.process.conditions.filters.FileNameFilter",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="FileNameFilterTask",
        )
        super().__init__(varinfo, inputs, node_id, node_attrs, execinfo)
