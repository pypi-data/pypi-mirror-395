import gc
import pickle
import shutil
import tempfile
import time
import os

import pytest
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.reconstruction.AxisOW import AxisOW
from tomwer.core.utils.lbsram import mock_low_memory
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.settings import mock_lsbram
from tomwer.core.utils.scanutils import MockNXtomo, MockEDF
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestOWAxis(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        self._window = AxisOW()
        self.recons_params = self._window.recons_params
        self.tempdir = tempfile.mkdtemp()
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tempdir, "nx_tomo.nx"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=20,
            energy=12.3,
        ).scan

        self._window.getAxisParams().mode = AxisMode.centered
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        gc.collect()

    def testAxisLock(self):
        """Test behavior when locking the axis position. Could not be included
        in the tomwer/gui because the lock action is only available for the OW
        """
        assert self._window.getAxisParams().mode in (
            AxisMode.centered,
            AxisMode.global_,
        )
        radio_axis = self._window._widget._axisWidget
        main_widget = self._window._widget
        self.assertFalse(main_widget._controlWidget._lockBut.isLocked())
        self.assertTrue(radio_axis._settingsWidget._mainWidget.isEnabled())
        self.mouseClick(main_widget._controlWidget._lockBut, qt.Qt.LeftButton)
        self.qapp.processEvents()
        self.assertTrue(main_widget._controlWidget._lockBut.isLocked())
        # when the lock button is activated we should automatically switch to
        # the manual mode
        self.assertTrue(self._window.getAxisParams().mode is AxisMode.manual)
        self.assertFalse(radio_axis._settingsWidget._mainWidget.isEnabled())

    def test_serializing(self):
        pickle.dumps(self._window.recons_params.to_dict())

    def test_literal_dumps(self):
        literal_dumps(self._window.recons_params.to_dict())


class TestWindowAxisComputation(TestCaseQt):
    @staticmethod
    def _long_computation(scan):
        time.sleep(5)
        return -1

    """Test that the axis widget work correctly"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self.tempdir = tempfile.mkdtemp()
        self._mainWindow = AxisOW()
        self.recons_params = self._mainWindow.recons_params
        self._window = self._mainWindow._widget
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tempdir, "nx_tomo.nx"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=20,
            energy=12.3,
        ).scan
        self._mainWindow.show()
        self.qWaitForWindowExposed(self._mainWindow)
        self._mainWindow.setMode("manual")

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        self._mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._mainWindow.close()
        self._mainWindow = None
        self._window = None
        gc.collect()

    def testComputationSucceed(self):
        """Test gui if the axis position is correctly computed"""
        self.recons_params.mode = AxisMode.manual
        radio_axis = self._window._axisWidget
        self.assertEqual(radio_axis.getMode(), AxisMode.manual)
        radio_axis.setXShift(2.345)
        self._mainWindow.process(self.scan)
        self.qapp.processEvents()
        self.assertEqual(radio_axis.getMode(), AxisMode.manual)
        self.assertEqual(self.recons_params.relative_cor_value, 2.345)
        position_info_widget = self._window._controlWidget._positionInfo
        self.assertEqual(position_info_widget._relativePositionQLE.text(), "2.345")


global _computation_res
_computation_res = 0


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestAxisStack(TestCaseQt):
    """Test axis computation of a stack of scan"""

    @staticmethod
    def _test_computation(scan):
        global _computation_res
        _computation_res += 1
        return _computation_res

    def setUp(self):
        # not working due to OW
        TestCaseQt.setUp(self)
        self._scan1 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._scan2 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._scan3 = MockEDF.mockScan(scanID=tempfile.mkdtemp())
        self._mainWindow = AxisOW()
        self.recons_params = self._mainWindow._axis_params
        self._mainWindow._skip_exec(True)

        global _computation_res
        _computation_res = 0

        self._mainWindow.patch_calc_method(
            AxisMode.centered, TestAxisStack._test_computation
        )
        self.recons_params.mode = AxisMode.centered

        self._mainWindow.show()
        self.qWaitForWindowExposed(self._mainWindow)

    def tearDown(self):
        mock_low_memory(False)
        mock_lsbram(False)
        self._mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._mainWindow.close()
        self._mainWindow = None
        self._recons_params = None
        self.qapp.processEvents()
        for scan in (self._scan1, self._scan2, self._scan3):
            shutil.rmtree(scan.path)
        gc.collect()

    def testLowMemory(self):
        """Make sure the axis computation will be skip if we are in low memory"""
        mock_low_memory(True)
        mock_lsbram(True)
        for scan in (self._scan1, self._scan2, self._scan3):
            self.qapp.processEvents()
            self._mainWindow.new_data_in(scan)

        self.assertEqual(self._scan1.axis_params, None)
        self.assertEqual(self._scan2.axis_params, None)
        self.assertEqual(self._scan3.axis_params, None)

    def testLockStack(self):
        """Check that axis position will be simply copy if we are in a lock
        stack"""
        self.recons_params.mode = AxisMode.manual
        position_value = 0.36
        self.recons_params.set_relative_value(position_value)

        for scan in (self._scan1, self._scan2, self._scan3):
            self._mainWindow.process(scan)

        for i in range(5):
            self.qapp.processEvents()
            time.sleep(0.2)
            self.qapp.processEvents()

        self.assertEqual(self._scan1.axis_params.relative_cor_value, position_value)
        self.assertEqual(self._scan2.axis_params.relative_cor_value, position_value)
        self.assertEqual(self._scan3.axis_params.relative_cor_value, position_value)
