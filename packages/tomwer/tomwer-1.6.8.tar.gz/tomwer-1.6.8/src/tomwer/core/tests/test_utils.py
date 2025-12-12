# coding: utf-8
from __future__ import annotations

import os
import shutil
import tempfile
import unittest

import numpy

from tomwer.core.utils import spec as spec_utils
from tomwer.core.utils.normalization import flatFieldCorrection
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo
from tomwer.tests.datasets import TomwerCIDatasets


class TestGetClosestEnergy(unittest.TestCase):
    def setUp(self):
        self.topSrcFolder = tempfile.mkdtemp()
        self.dataSetID = "scan_3_"
        self.dataDir = TomwerCIDatasets.get_dataset(
            f"edf_datasets/{self.dataSetID}",
        )
        self.sourceS3 = os.path.join(self.topSrcFolder, self.dataSetID)
        shutil.copytree(src=os.path.join(self.dataDir), dst=self.sourceS3)

        self.sourceT01 = os.path.join(self.topSrcFolder, "test01")
        shutil.copytree(
            src=TomwerCIDatasets.get_dataset(
                "edf_datasets/test01",
            ),
            dst=self.sourceT01,
        )
        self.S3XMLFile = os.path.join(self.sourceS3, "scan_3_.xml")
        self.S3Ref0000 = os.path.join(self.sourceS3, "ref0000_0000.edf")
        self.S3Ref0010 = os.path.join(self.sourceS3, "ref0000_0010.edf")

    def tearDown(self):
        shutil.rmtree(self.topSrcFolder)

    def testEnergyFromEDF(self):
        os.remove(self.S3XMLFile)
        self.assertTrue(
            spec_utils.getClosestEnergy(scan=self.sourceS3, refFile=self.S3Ref0000)
            == 61
        )
        self.assertTrue(
            spec_utils.getClosestEnergy(scan=self.sourceS3, refFile=self.S3Ref0010)
            == 61
        )

    def testEnergyFromXML(self):
        os.remove(self.S3Ref0000)
        os.remove(self.S3Ref0010)
        self.assertTrue(
            spec_utils.getClosestEnergy(scan=self.sourceS3, refFile=self.S3Ref0000)
            == 10
        )
        self.assertTrue(
            spec_utils.getClosestEnergy(scan=self.sourceS3, refFile=self.S3Ref0010)
            == 10
        )

    def testEnergyFromInfo(self):
        self.assertTrue(
            spec_utils.getClosestEnergy(scan=self.sourceT01, refFile=None) == 19
        )

    def testDefaultEnergy(self):
        os.remove(self.S3XMLFile)
        os.remove(self.S3Ref0000)
        os.remove(self.S3Ref0010)
        self.assertTrue(
            spec_utils.getClosestEnergy(scan=self.sourceS3, refFile=self.S3Ref0000)
            is None
        )
        self.assertTrue(
            spec_utils.getClosestEnergy(scan=self.sourceS3, refFile=self.S3Ref0010)
            is None
        )


class TestGetClosestSREnergy(unittest.TestCase):
    def setUp(self):
        self.topSrcFolder = tempfile.mkdtemp()
        self.dataSetID = "test10"
        self.dataDir = TomwerCIDatasets.get_dataset(
            f"edf_datasets/{self.dataSetID}",
        )
        self.sourceT10 = os.path.join(self.topSrcFolder, self.dataSetID)
        shutil.copytree(src=os.path.join(self.dataDir), dst=self.sourceT10)
        self.T10XMLFile = os.path.join(self.sourceT10, "test10.xml")
        self.T10InfoFile = os.path.join(self.sourceT10, "test10.info")
        self.T10Ref0000 = os.path.join(self.sourceT10, "ref0000_0000.edf")

    def tearDown(self):
        shutil.rmtree(self.topSrcFolder)


class TestMockEDFScan(unittest.TestCase):
    """Test that mock scan are adapted to other unit test"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.scan_id = os.path.join(self.tmpdir, "myscan")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def testScanEvolution360(self):
        """Test get scan evolution from a mock scan with a 360 range and no
        extra radio"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=5,
            nRecons=1,
            nPagRecons=1,
            dim=10,
            scan_range=360,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 5)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0002.edf"),
        )
        self.assertTrue(360 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[360].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0004.edf"),
        )

    def testScanEvolution180(self):
        """Test get scan evolution from a mock scan with a 180 range and no
        extra radio"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=8,
            nRecons=0,
            nPagRecons=0,
            dim=10,
            scan_range=180,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 8)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0007.edf"),
        )
        self.assertFalse(360 in scan_dynamic)

    def testScanEvolution360Extra4(self):
        """Test get scan evolution from a mock scan with a 360 range and 4
        extra radio"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=21,
            nRecons=0,
            nPagRecons=0,
            dim=10,
            scan_range=360,
            n_extra_radio=4,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 21 + 4)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0010.edf"),
        )
        self.assertTrue(360 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[360].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0020.edf"),
        )
        extra_angles = (0, 90, 180, 270)  # note: 0(1) is the last file acquire
        for iAngle, angle in enumerate(extra_angles):
            angle_id = str(angle) + "(1)"
            self.assertTrue(angle_id in scan_dynamic)
            file_name = os.path.join(
                self.tmpdir, "myscan", "myscan_%04d.edf" % (21 + 4 - 1 - iAngle)
            )
            self.assertEqual(scan_dynamic[angle_id].file_path(), file_name)

    def testScanEvolution180Extra2(self):
        """Test get scan evolution from a mock scan with a 360 range and 3
        extra radios"""
        scan = MockEDF.mockScan(
            scanID=self.scan_id,
            nRadio=4,
            nRecons=2,
            nPagRecons=2,
            dim=10,
            scan_range=180,
            n_extra_radio=2,
        )
        scan_dynamic = scan.get_proj_angle_url()
        self.assertEqual(len(scan_dynamic), 4 + 2)
        self.assertTrue(0 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[0].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0000.edf"),
        )
        self.assertTrue(180 in scan_dynamic)
        self.assertEqual(
            scan_dynamic[180].file_path(),
            os.path.join(self.tmpdir, "myscan", "myscan_0003.edf"),
        )
        self.assertTrue(360 not in scan_dynamic)
        extra_angles = (0, 90)  # note: 0(1) is the last file acquire
        for iAngle, angle in enumerate(extra_angles):
            angle_id = str(angle) + "(1)"
            self.assertTrue(angle_id in scan_dynamic)
            file_name = os.path.join(
                self.tmpdir, "myscan", "myscan_%04d.edf" % (4 + 2 - 1 - iAngle)
            )
            self.assertEqual(scan_dynamic[angle_id].file_path(), file_name)


class TestMockNXtomo(unittest.TestCase):
    """Test MockNXtomo to check that the file produced is valid"""

    def setUp(self) -> None:
        self._folder = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self._folder)

    def testSimpleMockCreationOneCall(self):
        """Test mock of an acquisition starting by one dark, then 10 ref,
        then 20 radios, then 10 'final' ref and 2 alignment radio"""
        mock = MockNXtomo(
            scan_path=self._folder,
            n_proj=20,
            n_ini_proj=20,
            n_alignement_proj=2,
            create_ini_dark=True,
            create_ini_flat=True,
            create_final_flat=True,
            n_refs=10,
        )
        self.assertTrue(0 in mock.scan.darks.keys())
        self.assertTrue(1 in mock.scan.flats.keys())
        self.assertTrue(10 in mock.scan.flats.keys())


def test_flat_field_normalization():
    """test flatFieldCorrection function"""
    f = numpy.ones((10, 10))
    d = numpy.ones((10, 10))
    imgs = {
        0: numpy.random.random((10, 10)),
        12: numpy.random.random((10, 10)),
    }
    flatFieldCorrection(imgs, d, f)
