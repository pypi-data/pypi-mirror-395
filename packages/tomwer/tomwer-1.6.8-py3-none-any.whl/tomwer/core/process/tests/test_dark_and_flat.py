# coding: utf-8
from __future__ import annotations


import os
import shutil
import tempfile
import unittest

import numpy
from tomoscan.esrf.scan.utils import get_data

from tomwer.core.process.reconstruction.darkref.params import DKRFRP
from tomwer.core.process.reconstruction.darkref.params import ReduceMethod as cMethod
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo
from tomwer.tests.datasets import TomwerCIDatasets

from ..reconstruction.darkref.darkrefs import DarkRefsTask
from ..reconstruction.darkref.darkrefscopy import DarkRefsCopy


class TestDarkRefIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()

        self.scan_edf = MockEDF.mockScan(
            scanID=self.scan_folder, nRadio=10, nRecons=1, nPagRecons=4, dim=10
        )
        self.mock_hdf5 = MockNXtomo(
            scan_path=self.scan_folder, n_proj=10, n_pag_recons=0
        )
        self.scan_hdf5 = self.mock_hdf5.scan

        self.recons_params = DKRFRP()

    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        for scan, scan_type in zip(
            (self.scan_edf, self.scan_hdf5), ("edf scan", "hdf5 scan")
        ):
            for input_type in (dict, TomwerScanBase):
                for serialize_output_data in (True, False):
                    with self.subTest(
                        return_dict=serialize_output_data,
                        input_type=input_type,
                        scan_type=scan_type,
                    ):
                        input_obj = scan
                        if input_obj is dict:
                            input_obj = input_obj.to_dict()
                        process = DarkRefsTask(
                            inputs={
                                "dark_ref_params": self.recons_params,
                                "data": input_obj,
                                "serialize_output_data": serialize_output_data,
                            }
                        )
                        process.run()
                        out = process.outputs.data
                        if serialize_output_data:
                            self.assertTrue(isinstance(out, dict))
                        else:
                            self.assertTrue(isinstance(out, TomwerScanBase))


class TestDarkRefCopyIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()

        self.scan_edf = MockEDF.mockScan(
            scanID=self.scan_folder, nRadio=10, nRecons=1, nPagRecons=4, dim=10
        )
        self.scan_hdf5 = MockNXtomo(
            scan_path=self.scan_folder, n_proj=10, n_pag_recons=0
        ).scan
        self.recons_params = DKRFRP()
        self._save_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.scan_folder)

    def testInputOutput(self):
        for scan, scan_type in zip(
            (self.scan_edf, self.scan_hdf5), ("edf scan", "hdf5 scan")
        ):
            for input_type in (dict, TomwerScanBase):
                for serialize_output_data in (True, False):
                    with self.subTest(
                        return_dict=serialize_output_data,
                        input_type=input_type,
                        scan_type=scan_type,
                    ):
                        input_obj = scan
                        if input_obj is dict:
                            input_obj = input_obj.to_dict()
                        dkrf_process = DarkRefsCopy(
                            inputs={
                                "dark_ref_params": self.recons_params,
                                "data": input_obj,
                                "serialize_output_data": serialize_output_data,
                                "save_dir": self._save_dir,
                            }
                        )
                        dkrf_process.run()
                        out = dkrf_process.outputs.data
                        if serialize_output_data:
                            self.assertTrue(isinstance(out, dict))
                        else:
                            self.assertTrue(isinstance(out, TomwerScanBase))


class TestDarkRefEdf(unittest.TestCase):
    """
    Test dark ref is correctly processing with h5 refs
    """

    def setUp(self) -> None:
        self.scan_folder = tempfile.mkdtemp()
        self.dark_data = numpy.array(  # pylint: disable=E1121
            numpy.random.random(4 * 200 * 200) * 100,
            dtype=numpy.uint16,
        ).reshape(4, 200, 200)
        self.flat_data = numpy.array(  # pylint: disable=E1121
            numpy.random.random(4 * 200 * 200) * 100,
            dtype=numpy.uint32,
        ).reshape(4, 200, 200)
        self.scan = MockEDF.mockScan(
            scanID=self.scan_folder,
            nRadio=10,
            nRecons=1,
            nPagRecons=4,
            dim=200,
            start_dark=True,
            start_flat=True,
            start_dark_data=self.dark_data,
            start_flat_data=self.flat_data,
        )
        self.recons_params = DKRFRP()
        self.recons_params.overwrite_dark = True
        self.recons_params.overwrite_ref = True

    def tearDown(self) -> None:
        shutil.rmtree(self.scan_folder)

    def testDark(self):
        """
        Test darks are computed when only dark are requested
        """
        method_to_test = (
            cMethod.MEDIAN,
            cMethod.MEAN,
            cMethod.FIRST,
            cMethod.LAST,
        )
        th_results = (
            numpy.median(self.dark_data, axis=0),
            numpy.mean(self.dark_data, axis=0),
            self.dark_data[0],
            self.dark_data[-1],
        )
        for method, th_res in zip(method_to_test, th_results):
            with self.subTest(method=method):
                process = DarkRefsTask(
                    inputs={
                        "dark_ref_params": self.recons_params,
                        "data": self.scan,
                        "serialize_output_data": False,
                    }
                )

                self.recons_params.dark_calc_method = method
                self.recons_params.flat_calc_method = cMethod.NONE
                process.run()
                numpy.testing.assert_array_almost_equal(
                    self.scan.reduced_darks[0], th_res.astype(numpy.uint16)
                )

    def testFlat(self):
        """
        Test flats are computed when only flat are requested
        """
        method_to_test = (
            cMethod.MEDIAN,
            cMethod.MEAN,
            cMethod.FIRST,
            cMethod.LAST,
        )
        th_results = (
            numpy.median(self.flat_data, axis=0),
            numpy.mean(self.flat_data, axis=0),
            self.flat_data[0],
            self.flat_data[-1],
        )
        for method, th_res in zip(method_to_test, th_results):
            with self.subTest(method=method):
                self.recons_params.dark_calc_method = cMethod.NONE
                self.recons_params.flat_calc_method = method
                process = DarkRefsTask(
                    inputs={
                        "dark_ref_params": self.recons_params,
                        "data": self.scan,
                        "serialize_output_data": False,
                    }
                )
                process.run()
                numpy.testing.assert_array_almost_equal(
                    self.scan.reduced_flats[0], th_res.astype(numpy.uint16)
                )


class TestDarkRefNx(unittest.TestCase):
    """
    Test dark ref is correctly processing with h5 refs
    """

    def setUp(self) -> None:
        super().setUp()
        dataset_name = "frm_edftomomill_twoentries.nx"
        self.scan_folder = tempfile.mkdtemp()
        self._file_path = os.path.join(self.scan_folder, dataset_name)
        shutil.copyfile(
            src=TomwerCIDatasets.get_dataset(f"h5_datasets/{dataset_name}"),
            dst=self._file_path,
        )
        self.scan = NXtomoScan(scan=self._file_path, entry="entry0000")
        self.recons_params = DKRFRP()
        self.recons_params.overwrite_dark = True
        self.recons_params.overwrite_ref = True

    def tearDown(self) -> None:
        shutil.rmtree(self.scan_folder)
        super().tearDown()

    def testDark(self):
        """
        Test darks are computed when only dark are requested
        """
        darks = self.scan.darks
        self.assertEqual(len(darks), 1)

        method_to_test = (cMethod.MEAN, cMethod.MEDIAN, cMethod.FIRST, cMethod.LAST)
        for method in method_to_test:
            with self.subTest(method=method):
                self.recons_params.dark_calc_method = method
                self.recons_params.flat_calc_method = cMethod.NONE
                process = DarkRefsTask(
                    inputs={
                        "dark_ref_params": self.recons_params,
                        "data": self.scan,
                        "serialize_output_data": False,
                    }
                )
                process.run()
                flats = self.scan.load_reduced_flats()
                self.assertEqual(len(flats), 0)
                darks = self.scan.load_reduced_darks()
                self.assertEqual(len(darks), 1)

    def testFlat(self):
        """
        Test flats are computed when only flat are requested
        """
        flats = self.scan.flats
        self.assertEqual(len(flats), 42)
        url_flat_serie_1 = [flats[index] for index in range(1, 22)]
        url_flat_serie_2 = [flats[index] for index in range(1521, 1542)]
        assert len(url_flat_serie_1) == 21
        assert len(url_flat_serie_2) == 21
        data_flat_serie_1 = [get_data(url) for url in url_flat_serie_1]
        data_flat_serie_2 = [get_data(url) for url in url_flat_serie_2]

        self.recons_params.overwrite_dark = True
        self.recons_params.overwrite_ref = True

        method_to_test = (cMethod.MEAN, cMethod.MEDIAN, cMethod.FIRST, cMethod.LAST)
        for method in method_to_test:
            with self.subTest(method=method):
                if method is cMethod.MEDIAN:
                    expected_res_s1 = numpy.median(data_flat_serie_1, axis=0)
                    expected_res_s2 = numpy.median(data_flat_serie_2, axis=0)
                elif method is cMethod.MEAN:
                    expected_res_s1 = numpy.mean(data_flat_serie_1, axis=0)
                    expected_res_s2 = numpy.mean(data_flat_serie_2, axis=0)
                elif method is cMethod.FIRST:
                    expected_res_s1 = data_flat_serie_1[0]
                    expected_res_s2 = data_flat_serie_2[0]
                elif method is cMethod.LAST:
                    expected_res_s1 = data_flat_serie_1[-1]
                    expected_res_s2 = data_flat_serie_2[-1]
                else:
                    raise ValueError("method not managed")

                self.recons_params.dark_calc_method = cMethod.NONE
                self.recons_params.flat_calc_method = method
                process = DarkRefsTask(
                    inputs={
                        "dark_ref_params": self.recons_params,
                        "data": self.scan,
                        "serialize_output_data": False,
                    }
                )
                process.run()

                darks = self.scan.load_reduced_darks()
                self.assertEqual(len(darks), 0)
                flats = self.scan.load_reduced_flats()
                self.assertEqual(len(flats), 2)
                self.assertTrue(1 in flats)
                self.assertTrue(1521 in flats)
                self.assertTrue(numpy.allclose(flats[1], expected_res_s1))
                self.assertTrue(numpy.allclose(flats[1521], expected_res_s2))

    def testDarkAndFlat(self):
        """
        Test darks and flats are computed when both are requested
        """
        flats = self.scan.flats
        self.assertEqual(len(flats), 42)
        url_flat_serie_1 = [flats[index] for index in range(1, 22)]
        url_flat_serie_2 = [flats[index] for index in range(1521, 1542)]
        assert len(url_flat_serie_1) == 21
        assert len(url_flat_serie_2) == 21
        data_flat_serie_1 = [get_data(url) for url in url_flat_serie_1]
        data_flat_serie_2 = [get_data(url) for url in url_flat_serie_2]

        self.recons_params.dark_calc_method = cMethod.MEAN
        self.recons_params.flat_calc_method = cMethod.MEDIAN
        darks = self.scan.darks
        self.assertEqual(len(darks), 1)
        dark_data = get_data(list(darks.values())[0])

        expected_flats_s1 = numpy.median(data_flat_serie_1, axis=0)
        expected_flats_s2 = numpy.median(data_flat_serie_2, axis=0)
        process = DarkRefsTask(
            inputs={
                "dark_ref_params": self.recons_params,
                "data": self.scan,
                "serialize_output_data": False,
            }
        )
        process.run()
        darks = self.scan.load_reduced_darks()
        flats = self.scan.load_reduced_flats()
        self.assertEqual(len(darks), 1)
        self.assertEqual(len(flats), 2)
        self.assertTrue(0 in darks)
        self.assertTrue(1 in flats)
        self.assertTrue(1521 in flats)
        self.assertTrue(numpy.allclose(flats[1], expected_flats_s1))
        self.assertTrue(numpy.allclose(flats[1521], expected_flats_s2))
        self.assertTrue(numpy.allclose(darks[0], dark_data))
