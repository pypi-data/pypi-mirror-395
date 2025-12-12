# coding: utf-8
from __future__ import annotations

import logging
import os
import shutil
import tempfile
import unittest

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.gui.visualization.diffviewer import DiffFrameViewer

logging.disable(logging.INFO)


class TestDiffViewer(TestCaseQt):
    """unit test for the :class:_ImageStack widget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._widget = DiffFrameViewer()
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.tmp_dir = tempfile.mkdtemp()
        self.scan1 = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan

        self.scan2 = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        self._widget.close()
        self._widget = None
        unittest.TestCase.tearDown(self)

    def test(self):
        """Make sur the addLeaf and clear functions are working"""
        self._widget.addScan(self.scan1)
        self._widget.addScan(self.scan2)
        self._widget.getLeftScan()

        # test shift
        shift_widgets = self._widget.getShiftsWidget()
        relShiftWidget = shift_widgets.getRelativeShiftWidget()
        relShiftWidget.setShiftStep(0.1)
        relShiftWidget.move("left")
        self.qapp.processEvents()
        relShiftWidget.setShiftStep(0.3)
        relShiftWidget.move("right")
        self.qapp.processEvents()
        relShiftWidget.setShiftStep(10)
        relShiftWidget.move("up")
        self.qapp.processEvents()
        relShiftWidget.setShiftStep(33)
        relShiftWidget.move("down")
        self.qapp.processEvents()
        # for the frame A y is expected to be always 0
        assert relShiftWidget.getFrameAShift() == (0.2, 0)
        # for the frame B y is expected to be the shift. And x is supposed to be the opposite of the A.x shift
        assert relShiftWidget.getFrameBShift() == (-0.2, -23)
