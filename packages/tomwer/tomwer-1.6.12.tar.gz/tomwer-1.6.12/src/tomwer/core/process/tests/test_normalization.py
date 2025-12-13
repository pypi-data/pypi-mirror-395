# coding: utf-8
from __future__ import annotations


import shutil
import tempfile
import unittest

import h5py
import numpy
from tomoscan.normalization import Method

from tomwer.core.process.reconstruction.normalization import normalization, params
from tomwer.core.utils.scanutils import MockNXtomo


class TestNormalization(unittest.TestCase):
    """
    Test the normalization process
    """

    def setUp(self) -> None:
        self.tempdir = tempfile.mkdtemp()
        dim = 100
        self.scan = MockNXtomo(
            scan_path=self.tempdir,
            n_proj=2,
            n_ini_proj=2,
            scan_range=180,
            dim=dim,
            create_ini_dark=False,
            create_ini_flat=False,
            create_final_flat=False,
        ).scan

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)

    def testManualROI(self):
        # step1: rewrite the detector data to simplify result check
        with h5py.File(self.scan.master_file, mode="a") as h5f:
            dataset = h5f["/entry/instrument/detector/data"]
            assert dataset.shape == (2, 100, 100)  # pylint: disable=E1101
            del h5f["/entry/instrument/detector/data"]
            h5f["/entry/instrument/detector/data"] = numpy.arange(
                100 * 100 * 2
            ).reshape(2, 100, 100)

        process_params = normalization.SinoNormalizationParams()
        process_params.method = Method.SUBTRACTION
        process_params.source = params._ValueSource.MANUAL_ROI
        expected_results = {
            "mean": numpy.array([800.5, 10800.5]),
            "median": numpy.array([800.5, 10800.5]),
        }

        for item in params._ValueCalculationFct:
            calc_fct = item.value
            with self.subTest(calc_fct=calc_fct):
                process_params.extra_infos = {
                    "start_x": 0,
                    "end_x": 2,
                    "start_y": 8,
                    "end_y": 9,
                    "calc_fct": calc_fct,
                    "calc_area": "volume",
                }
                process = normalization.SinoNormalizationTask(
                    inputs={
                        "data": self.scan,
                        "configuration": process_params,
                        "serialize_output_data": False,
                    }
                )
                process.run()
                res = self.scan.intensity_normalization.get_extra_infos().get("value")
                if isinstance(res, numpy.ndarray):
                    numpy.testing.assert_array_equal(res, expected_results[calc_fct])
                else:
                    numpy.testing.assert_array_equal(res, expected_results[calc_fct])
