# coding: utf-8
from __future__ import annotations


import os
import shutil
import tempfile

import fabio
import numpy
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefsTask
from tomwer.core.process.reconstruction.darkref.params import DKRFRP, ReduceMethod
from tomwer.core.utils.scanutils import MockEDF
from tomwer.tests.datasets import TomwerCIDatasets


class TestDarkRefsBehavior(TestCaseQt):
    """Test that the Darks and reference are correctly computed from the
    DarksRefs class
    """

    def setUp(self):
        TestCaseQt.setUp(self)
        self.datasetsID = "test10"
        self.tmpDir = tempfile.mkdtemp()
        self.thRef = {}
        """number of theoretical ref file the algorithm should create"""
        self.thDark = {}
        """number of theoretical dark file the algorithm should create"""
        self.dataset_folder = os.path.join(self.tmpDir, self.datasetsID)

        dataDir = TomwerCIDatasets.get_dataset(
            f"edf_datasets/{self.datasetsID}",
        )
        shutil.copytree(dataDir, self.dataset_folder)
        files = os.listdir(self.dataset_folder)
        for _f in files:
            if _f.startswith(("refHST", "darkHST", "dark.edf")):
                os.remove(os.path.join(self.dataset_folder, _f))

        self.recons_params = DKRFRP()
        self.recons_params._set_remove_opt(False)

    def tearDown(self):
        self.qapp.processEvents()
        self.darkRef = None
        shutil.rmtree(self.tmpDir)

    def testDarkCreation(self):
        """Test that the dark is correctly computed"""
        self.recons_params.flat_calc_method = ReduceMethod.NONE
        self.recons_params.dark_calc_method = ReduceMethod.MEDIAN

        dar_ref_process = DarkRefsTask(
            inputs={
                "dark_ref_params": self.recons_params,
                "force_sync": True,
                "darkhst_prefix": "darkHST",
                "data": self.dataset_folder,
                "serialize_output_data": False,
            }
        )
        dar_ref_process.run()
        self.qapp.processEvents()
        if os.path.basename(self.dataset_folder) == "test10":
            self.assertTrue("darkend0000.edf" in os.listdir(self.dataset_folder))
            self.assertTrue("dark.edf" in os.listdir(self.dataset_folder))
            self.assertEqual(
                len(
                    dar_ref_process.getDarkHSTFiles(
                        self.dataset_folder, prefix=self.recons_params.dark_prefix
                    )
                ),
                1,
            )
            self.assertEqual(
                len(
                    dar_ref_process.getRefHSTFiles(
                        self.dataset_folder, prefix=self.recons_params.flat_prefix
                    )
                ),
                0,
            )

    def testRefCreation(self):
        """Test that the dark is correctly computed"""
        self.recons_params.flat_calc_method = ReduceMethod.MEDIAN
        self.recons_params.dark_calc_method = ReduceMethod.NONE

        dar_ref_process = DarkRefsTask(
            inputs={
                "dark_ref_params": self.recons_params,
                "force_sync": True,
                "darkhst_prefix": "darkHST",
                "data": self.dataset_folder,
                "serialize_output_data": False,
            }
        )

        dar_ref_process.run()
        self.qapp.processEvents()
        self.assertTrue("darkend0000.edf" in os.listdir(self.dataset_folder))
        self.assertFalse("dark0000.edf" in os.listdir(self.dataset_folder))
        self.assertTrue("refHST0000.edf" in os.listdir(self.dataset_folder))
        self.assertTrue("refHST0020.edf" in os.listdir(self.dataset_folder))
        self.assertTrue("ref0000_0000.edf" in os.listdir(self.dataset_folder))
        self.assertTrue("ref0000_0020.edf" in os.listdir(self.dataset_folder))
        self.assertTrue("ref0001_0000.edf" in os.listdir(self.dataset_folder))
        self.assertTrue("ref0001_0020.edf" in os.listdir(self.dataset_folder))


class TestRefCalculationOneSerie(TestCaseQt):
    """
    Make sure the calculation is correct for the dark and flat field
    according to the method used.
    """

    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        n_scans = 5
        n_info = 1
        n_xml = 1
        MockEDF.fastMockAcquisition(self.tmp_dir, n_radio=n_scans)
        reFiles = {}
        data1 = numpy.zeros((20, 10))
        data2 = numpy.zeros((20, 10)) + 100
        reFiles["ref0000_0000.edf"] = data1
        reFiles["ref0001_0000.edf"] = data2
        reFiles["ref0002_0000.edf"] = data2
        reFiles["ref0003_0000.edf"] = data2
        for refFile in reFiles:
            file_desc = fabio.edfimage.EdfImage(data=reFiles[refFile])
            file_desc.write(os.path.join(self.tmp_dir, refFile))
        assert len(os.listdir(self.tmp_dir)) is (
            len(reFiles) + n_scans + n_xml + n_info
        )

        self.recons_params = DKRFRP()
        self.darkRef = DarkRefsTask(
            inputs={
                "dark_ref_params": self.recons_params,
                "data": self.tmp_dir,
                "serialize_output_data": False,
            }
        )
        self.darkRef.setForceSync(True)
        self.recons_params.flat_pattern = "ref*.*[0-9]{3,4}_[0-9]{3,4}"

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        super().tearDown()

    def testRefMedianCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.MEDIAN
        self.recons_params.dark_calc_method = ReduceMethod.NONE
        self.darkRef.run()
        refHST = os.path.join(self.tmp_dir, "refHST0000.edf")
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 100)
        )

    def testRefMeanCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.MEAN
        self.recons_params.dark_calc_method = ReduceMethod.NONE
        self.darkRef.run()
        refHST = os.path.join(self.tmp_dir, "refHST0000.edf")
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 75)
        )


class TestRefCalculationThreeSerie(TestCaseQt):
    """
    Make sure the calculation is correct for the dark and flat field
    according to the method used.
    """

    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        MockEDF.fastMockAcquisition(folder=self.tmp_dir, n_radio=1)
        reFiles = {}
        self.seriesList = (0, 10, 200)
        for series in self.seriesList:
            data1 = numpy.zeros((20, 10)) + series
            data2 = numpy.zeros((20, 10)) + 100 + series
            reFiles["ref0000_" + str(series).zfill(4) + ".edf"] = data1
            reFiles["ref0001_" + str(series).zfill(4) + ".edf"] = data2
            reFiles["ref0002_" + str(series).zfill(4) + ".edf"] = data2
            reFiles["ref0003_" + str(series).zfill(4) + ".edf"] = data2
            for refFile in reFiles:
                file_desc = fabio.edfimage.EdfImage(data=reFiles[refFile])
                file_desc.write(os.path.join(self.tmp_dir, refFile))

        self.recons_params = DKRFRP()
        self.darkRef = DarkRefsTask(
            inputs={
                "dark_ref_params": self.recons_params,
                "data": self.tmp_dir,
                "force_sync": True,
                "serialize_output_data": False,
            }
        )
        self.recons_params.flat_pattern = "ref*.*[0-9]{3,4}_[0-9]{3,4}"

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        super().tearDown()

    def testRefMedianCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.MEDIAN
        self.recons_params.dark_calc_method = ReduceMethod.NONE
        self.darkRef.run()
        for serie in self.seriesList:
            refHST = os.path.join(self.tmp_dir, "refHST" + str(serie).zfill(4) + ".edf")
            self.assertTrue(os.path.isfile(refHST))
            self.assertTrue(
                numpy.array_equal(
                    fabio.open(refHST).data, numpy.zeros((20, 10)) + 100 + serie
                )
            )

    def testRefMeanCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.MEAN
        self.recons_params.dark_calc_method = ReduceMethod.NONE
        self.darkRef.run()
        for series in self.seriesList:
            refHST = os.path.join(
                self.tmp_dir, "refHST" + str(series).zfill(4) + ".edf"
            )
            self.assertTrue(os.path.isfile(refHST))
            self.assertTrue(
                numpy.array_equal(
                    fabio.open(refHST).data, numpy.zeros((20, 10)) + 75 + series
                )
            )


class TestDarkCalculationOneFrame(TestCaseQt):
    """Make sure computation of the Dark is correct"""

    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        n_scan = 1
        n_info = 1
        n_xml = 1
        MockEDF.fastMockAcquisition(self.tmp_dir, n_radio=n_scan)
        file_desc = fabio.edfimage.EdfImage(data=numpy.zeros((20, 10)) + 10)

        file_desc.write(os.path.join(self.tmp_dir, "darkend0000.edf"))
        assert len(os.listdir(self.tmp_dir)) is (1 + n_scan + n_info + n_xml)
        self.recons_params = DKRFRP()
        self.darkRef = DarkRefsTask(
            inputs={
                "dark_ref_params": self.recons_params,
                "force_sync": True,
                "data": self.tmp_dir,
                "serialize_output_data": False,
            }
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        super().tearDown()

    def testDarkMeanCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.NONE
        self.recons_params.dark_calc_method = ReduceMethod.MEAN

        self.darkRef.run()
        refHST = os.path.join(self.tmp_dir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 10)
        )

    def testDarkMedianCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.NONE
        self.recons_params.dark_calc_method = ReduceMethod.MEDIAN

        self.darkRef.run()
        refHST = os.path.join(self.tmp_dir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 10)
        )


class TestDarkCalculation(TestCaseQt):
    """Make sure computation of the Dark is correct"""

    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        n_scan = 1
        n_xml = 1
        n_info = 1
        MockEDF.fastMockAcquisition(os.path.join(self.tmp_dir), n_radio=n_scan)

        file_desc = fabio.edfimage.EdfImage(data=numpy.zeros((20, 10)))
        file_desc.append_frame(data=(numpy.zeros((20, 10)) + 100))
        file_desc.append_frame(data=(numpy.zeros((20, 10)) + 100))
        file_desc.append_frame(data=(numpy.zeros((20, 10)) + 100))

        file_desc.write(os.path.join(self.tmp_dir, "darkend0000.edf"))
        assert len(os.listdir(self.tmp_dir)) is (1 + n_scan + n_xml + n_info)
        self.recons_params = DKRFRP()
        self.darkRef = DarkRefsTask(
            inputs={
                "data": self.tmp_dir,
                "dark_ref_params": self.recons_params,
                "force_sync": True,
                "serialize_output_data": False,
            }
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        super().tearDown()

    def testDarkMeanCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.NONE
        self.recons_params.dark_calc_method = ReduceMethod.MEAN

        self.darkRef.run()
        refHST = os.path.join(self.tmp_dir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 75)
        )

    def testDarkMedianCalculation(self):
        self.recons_params.flat_calc_method = ReduceMethod.NONE
        self.recons_params.dark_calc_method = ReduceMethod.MEDIAN

        self.darkRef.run()
        refHST = os.path.join(self.tmp_dir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 100)
        )


class TestDarkAccumulation(TestCaseQt):
    """
    Make sure computation for dark in accumulation are correct
    """

    def setUp(self):
        super().setUp()
        self.dataset = "bone8_1_"
        dataDir = TomwerCIDatasets.get_dataset(
            f"edf_datasets/{self.dataset}",
        )
        self.outputdir = tempfile.mkdtemp()
        shutil.copytree(src=dataDir, dst=os.path.join(self.outputdir, self.dataset))
        self.darkFile = os.path.join(self.outputdir, self.dataset, "dark.edf")
        # create a single 'bone8_1_' to be a valid acquisition directory
        MockEDF.fastMockAcquisition(os.path.join(self.outputdir, self.dataset))
        assert os.path.isfile(self.darkFile)
        with fabio.open(self.darkFile) as dsc:
            self.dark_reference = dsc.data
        # remove dark file
        os.remove(self.darkFile)

        self.recons_params = DKRFRP()
        self.recons_params.flat_calc_method = ReduceMethod.NONE
        self.recons_params.dark_calc_method = ReduceMethod.MEDIAN
        self.recons_params.dark_pattern = "darkend*"
        self.recons_params.dark_prefix = "dark.edf"

    def tearDown(self):
        shutil.rmtree(self.outputdir)
        super().tearDown()

    def testComputation(self):
        """Test data `bone8_1_` from id16b containing dark.edf of reference
        and darkend"""
        dark_ref_process = DarkRefsTask(
            inputs={
                "data": os.path.join(self.outputdir, self.dataset),
                "force_sync": True,
                "serialize_output_data": False,
            }
        )

        dark_ref_process.run()
        self.assertTrue(os.path.isfile(self.darkFile))
        with fabio.open(self.darkFile) as dsc:
            self.computed_dark = dsc.data
        self.assertTrue(numpy.array_equal(self.computed_dark, self.dark_reference))
