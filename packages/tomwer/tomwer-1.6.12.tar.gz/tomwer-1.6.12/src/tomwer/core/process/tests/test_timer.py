# coding: utf-8
from __future__ import annotations


import shutil
import tempfile
import unittest

from tomwer.core.process.control.timer import TimerTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import MockEDF


class TestTimerIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()

        self.scan = MockEDF.mockScan(
            scanID=self.scan_folder, nRadio=10, nRecons=1, nPagRecons=4, dim=10
        )

    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        """Test that io using TomoBase instance work"""
        for input_type in (dict, TomwerScanBase):
            for serialize_output_data in (True, False):
                with self.subTest(
                    return_dict=serialize_output_data,
                    input_type=input_type,
                ):
                    input_obj = self.scan
                    if input_obj is dict:
                        input_obj = input_obj.to_dict()

                    timer_process = TimerTask(
                        inputs={
                            "wait": 0.1,
                            "serialize_output_data": serialize_output_data,
                            "data": input_obj,
                        }
                    )
                    timer_process.run()
                    out = timer_process.outputs.data
                    if serialize_output_data:
                        self.assertTrue(isinstance(out, dict))
                    else:
                        self.assertTrue(isinstance(out, TomwerScanBase))
