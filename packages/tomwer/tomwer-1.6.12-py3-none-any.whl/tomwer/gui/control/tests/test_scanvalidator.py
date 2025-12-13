# coding: utf-8
from __future__ import annotations


import logging
import os
import shutil
import tempfile
import time

import pytest
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core import settings
from tomwer.core.utils.lbsram import mock_low_memory, is_low_on_memory
from tomwer.core.process.control.scanvalidator import ScanValidatorP
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.scanutils import MockEDF
from tomwer.gui.utils.waiterthread import QWaiterThread
from tomwer.tests.utils import skip_gui_test

logging.disable(logging.INFO)


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestScanValidator(TestCaseQt):
    """
    Simple test to make sure the timeout of data watcher is working properly
    """

    LOOP_MEM_RELEASER_DURATION = 0.2
    NB_SCANS = 2

    def tearDown(self):
        mock_low_memory(False)

    @classmethod
    def setUpClass(cls):
        settings.mock_lsbram(True)

        cls.scanValidator = ScanValidatorP(memoryReleaser=QWaiterThread(0.5))

        cls.scans = []

        for _ in range(cls.NB_SCANS):
            scanID = tempfile.mkdtemp()
            MockEDF.mockScan(scanID=scanID, nRadio=10, nRecons=2, nPagRecons=0, dim=10)
            cls.scans.append(scanID)

    @classmethod
    def tearDownClass(cls):
        settings.mock_lsbram(False)

        for f in cls.scans:
            if os.path.isdir(f):
                shutil.rmtree(f)

    @pytest.mark.skipif(
        (settings.isOnLbsram() and is_low_on_memory(settings.get_lbsram_path())),
        reason="Lbsram already overloaded",
    )
    def testMemoryReleaseLoop(self):
        """
        Make sure the internal loop of the scan validator is active if we are
        on lbsram.
        """

        def add_all_scans():
            for scan in self.scans:
                self.scanValidator.addScan(EDFTomoScan(scan))
            self.assertEqual(len(self.scanValidator._scans), self.NB_SCANS)

        def my_wait():
            for _ in range(3):
                while self.qapp.hasPendingEvents():
                    self.qapp.processEvents()
                time.sleep(self.LOOP_MEM_RELEASER_DURATION * 2)

        add_all_scans()
        mock_low_memory(True)
        my_wait()
        self.assertEqual(len(self.scanValidator._scans), 0)

        mock_low_memory(False)
        add_all_scans()
        my_wait()
        self.assertEqual(len(self.scanValidator._scans), self.NB_SCANS)
        self.scanValidator.clear()
        my_wait()
        self.assertEqual(len(self.scanValidator._scans), 0)
