# coding: utf-8
from __future__ import annotations

import os
import shutil
import tempfile

import h5py
import numpy.random
import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui.reconstruction.axis import AxisMainWindow
from tomwer.gui.reconstruction.axis.ManualFramesSelection import ManualFramesSelection
from tomwer.synctools.axis import QAxisRP
from tomwer.tests.datasets import TomwerCIDatasets
from tomwer.tests.utils import skip_gui_test
from tomwer.core.utils.scanutils import MockNXtomo


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestWindowAxis(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.recons_params = QAxisRP()
        self._window = AxisMainWindow(axis_params=self.recons_params)
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tempdir, "nx_tomo.nx"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=20,
            energy=12.3,
        ).scan
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()

    def testSetImagesNumpyArray(self):
        """Test the setImages function"""
        radio_axis = self._window._axisWidget
        radio_axis_plot = self._window._axisWidget.getPlot()
        numpy.testing.assert_array_equal(
            radio_axis_plot.getPlot().getActiveImage().getData(), numpy.empty((0, 0, 4))
        )
        imgA = numpy.random.random((100, 100))
        imgB = numpy.random.random((100, 100))
        radio_axis.setImages(imgA=imgA, imgB=imgB, flipB=True)
        self.qapp.processEvents()
        # make sur the image has been set
        assert radio_axis_plot.getPlot().getImage(legend="image1").getData().shape == (
            100,
            100,
        )

    def testSetScan(self):
        """Test the setScan function"""
        radio_axis_plot = self._window._axisWidget.getPlot()
        numpy.testing.assert_array_equal(
            radio_axis_plot.getPlot().getActiveImage().getData(), numpy.empty((0, 0, 4))
        )
        self._window.setScan(self.scan)
        self.qapp.processEvents()
        # make sur the image has been set
        assert radio_axis_plot.getPlot().getImage(legend="image1").getData().shape == (
            20,
            20,
        )

    def testShiftButtons(self):
        """Test that the 'left', 'right', ... buttons and the shift steps are
        correctly working"""
        imgA = numpy.random.random((100, 100))
        imgB = numpy.random.random((100, 100))
        radio_axis = self._window._axisWidget
        radio_axis.setImages(imgA=imgA, imgB=imgB, flipB=False)
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == 0)
        self.assertTrue(
            radio_axis.getShiftStep() == 1.0,
            f"shift is {radio_axis.getShiftStep()} when 1.0 expected",
        )
        radio_axis._settingsWidget._shiftControl._leftButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == -1)
        self.assertTrue(radio_axis.getYShift() == 0)
        radio_axis._settingsWidget._shiftControl._rightButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == 0)
        radio_axis._settingsWidget._displacementSelector._fineButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getShiftStep() == 0.1)
        radio_axis._settingsWidget._shiftControl._topButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == 0.1)
        radio_axis.setShiftStep(0.2)
        self.assertTrue(radio_axis.getShiftStep() == 0.2)
        radio_axis._settingsWidget._shiftControl._bottomButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == -0.1)

    def testAxisObjectGlobal(self):
        """Test that the GUI change according to the Axis object"""
        axis_obj = QAxisRP()
        self._window.setReconsParams(axis_obj)
        self.qapp.processEvents()
        self.assertEqual(self._window._axisWidget.getMode(), axis_obj.mode)
        # TODO: change the mode to see if the object is modify

    def testAxisObjectManual(self):
        """Test that the GUI change according to the Axis object"""
        axis_params = QAxisRP()
        axis_params.mode = AxisMode.manual
        axis_params.set_relative_value(-6.0)
        # note : for now only the xshift is managed !
        self._window.setReconsParams(axis_params)
        radio_axis = self._window._axisWidget
        self.assertEqual(radio_axis.getXShift(), -6.0)
        self.assertEqual(radio_axis.getYShift(), 0.0)


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestWindowsAxisSetScan(TestCaseQt):
    """Test that updates are correctly done in the case scan has some
    knowledge on"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self.recons_params = QAxisRP()
        self.widget = AxisMainWindow(axis_params=self.recons_params)
        self.scan_dir = tempfile.mkdtemp()
        # create dataset
        self.master_file = os.path.join(self.scan_dir, "frm_edftomomill_twoentries.nx")
        shutil.copyfile(
            TomwerCIDatasets.get_dataset(
                "h5_datasets/frm_edftomomill_twoentries.nx",
            ),
            self.master_file,
        )
        self.scan = NXtomoScan(scan=self.master_file, entry="entry0000")

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None

    def patch_fov(self, value: str):
        with h5py.File(self.scan.master_file, mode="a") as h5s:
            for entry in ("entry0000", "entry0001"):
                entry_node = h5s[entry]
                if "instrument/detector/field_of_view" in entry_node:
                    del entry_node["instrument/detector/field_of_view"]
                entry_node["instrument/detector/field_of_view"] = value


def test__getClosestAssociatedAngle():
    """
    test _getClosestAssociatedAngle function
    """
    assert (
        ManualFramesSelection._getClosestAssociatedAngle(angle=12.3, angles=(12.3,))
        == 12.3
    )
    assert (
        ManualFramesSelection._getClosestAssociatedAngle(
            angle=12.3, angles=(2.06, 10.3, 100.6)
        )
        == 10.3
    )
    assert (
        ManualFramesSelection._getClosestAssociatedAngle(
            angle=100.2, angles=(2.06, 10.3, 100.6)
        )
        == 100.6
    )
    assert (
        ManualFramesSelection._getClosestAssociatedAngle(angle=12.3, angles=()) is None
    )
    assert (
        ManualFramesSelection._getClosestAssociatedAngle(
            angle=300.2, angles=(2.06, 10.3, 100.6)
        )
        == 100.6
    )
    assert (
        ManualFramesSelection._getClosestAssociatedAngle(
            angle=-12, angles=(2.06, 10.3, 100.6)
        )
        == 2.06
    )
