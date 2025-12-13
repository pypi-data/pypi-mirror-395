# coding: utf-8
from __future__ import annotations

import shutil
import tempfile
import unittest

from tomwer.core.process.conditions.filters import (
    FileNameFilterTask,
    RegularExpressionFilter,
)
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import MockEDF


class TestConditionalFilter(unittest.TestCase):
    """
    Small unit test for the core.conditions
    """

    def testPattern1(self):
        filter_ = RegularExpressionFilter("name10")
        self.assertTrue(filter_.isFiltered("toto") is True)
        self.assertTrue(filter_.isFiltered("name10") is False)
        self.assertTrue(filter_.isFiltered("name100") is False)

    def testInputOutput(self):
        pass


class TestConditionIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()
        self.scan = MockEDF.mockScan(
            scanID=self.scan_folder, nRadio=10, nRecons=1, nPagRecons=4, dim=10
        )

    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        for input_type in (dict, TomwerScanBase):
            for serialize_output_data in (True, False):
                with self.subTest(
                    return_dict=serialize_output_data,
                    input_type=input_type,
                ):
                    input_obj = self.scan
                    if input_type is dict:
                        input_obj = self.scan.to_dict()
                    filter_process = FileNameFilterTask(
                        inputs={
                            "pattern": "*",
                            "serialize_output_data": serialize_output_data,
                            "data": input_obj,
                        }
                    )
                    filter_process.run()
                    out = filter_process.outputs.data
                    if serialize_output_data:
                        self.assertTrue(isinstance(out, dict))
                    else:
                        self.assertTrue(isinstance(out, TomwerScanBase))
