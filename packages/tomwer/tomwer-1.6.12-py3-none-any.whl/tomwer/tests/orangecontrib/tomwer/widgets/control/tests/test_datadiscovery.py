# coding: utf-8
from __future__ import annotations

import gc
import os
import pickle
import tempfile

from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt

from orangecontrib.tomwer.widgets.control.DataDiscoveryOW import DataDiscoveryOW
from tomwer.core.scan.scantype import ScanType
from tomwer.core.utils.scanutils import MockBlissAcquisition
from tomoscan.esrf.scan.mock import MockNXtomo, MockEDF


class TestDataDiscovery(TestCaseQt):
    WAIT_TIME = 5000  # thread processing wait time in ms

    def setUp(self):
        super().setUp()
        self.widget = DataDiscoveryOW()
        self.widget.setConfiguration(self.default_settings)
        self.signal_listener = SignalListener()
        self.widget.getProcessingThread().sigDataFound.connect(self.signal_listener)

    def tearDown(self):
        self.widget.getProcessingThread().sigDataFound.disconnect(self.signal_listener)
        self.signal_listener = None
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        gc.collect()

    @property
    def default_settings(self):
        return {
            "start_folder": "/my/folder",
            "file_filter": "*.h5",
            "scan_type_searched": ScanType.NX_TOMO,
        }

    def testSerialization(self):
        """make sure pickling works for the settings"""
        pickle.dumps(self.widget.getConfiguration())

    def testLiteralDumps(self):
        """make sure literal dumps (from orangecanvas) works for the settings"""
        literal_dumps(self.widget.getConfiguration())

    def testProcessingNXtomo(self):
        """Test the widget can find NXtomos"""
        n_scan = 3
        with tempfile.TemporaryDirectory() as root_dir:
            for i_scan in range(n_scan):
                MockNXtomo(
                    scan_path=os.path.join(root_dir, f"sub_folder_{i_scan}", "scan"),
                    n_proj=10,
                    n_ini_proj=10,
                    dim=10,
                )
            self.widget.setFolderObserved(root_dir)
            self.widget.start_discovery(wait=self.WAIT_TIME)
            while self.qapp.hasPendingEvents():
                self.qapp.processEvents()

            assert self.signal_listener.callCount() == n_scan

    def testProcessingBlissRawScan(self):
        """Test the widget can find bliss raw scans"""
        with tempfile.TemporaryDirectory() as root_dir:
            n_scan = 2
            for i_scan in range(n_scan):
                MockBlissAcquisition(
                    n_sample=1,
                    n_sequence=1,
                    n_scan_per_sequence=1,
                    n_darks=1,
                    n_flats=1,
                    with_nx=True,
                    output_dir=os.path.join(root_dir, f"sub_folder_{i_scan}", "scan"),
                )

            self.widget.setFilePattern("*.edf")
            self.widget.setSearchScanType(ScanType.BLISS)
            self.widget.setFolderObserved(root_dir)
            self.widget.start_discovery(wait=self.WAIT_TIME)
            while self.qapp.hasPendingEvents():
                self.qapp.processEvents()

            assert (
                self.signal_listener.callCount() == 0
            )  # because of the filtering on files
            self.widget.setFilePattern(None)
            self.widget.start_discovery(wait=self.WAIT_TIME)
            while self.qapp.hasPendingEvents():
                self.qapp.processEvents()

            assert self.signal_listener.callCount() == n_scan

    def testProcessingSpecScan(self):
        """Test the widget can find bliss raw scans"""
        with tempfile.TemporaryDirectory() as root_dir:
            n_scan = 4
            for i_scan in range(n_scan):
                MockEDF(
                    n_radio=4,
                    n_ini_radio=4,
                    scan_path=os.path.join(root_dir, f"sub_folder_{i_scan}", "scan"),
                )

            self.widget.setSearchScanType(ScanType.BLISS)
            self.widget.setFilePattern(None)
            self.widget.setFolderObserved(root_dir)
            self.widget.start_discovery(wait=self.WAIT_TIME)
            while self.qapp.hasPendingEvents():
                self.qapp.processEvents()

            assert (
                self.signal_listener.callCount() == 0
            )  # because of the scan type searched
            self.widget.setSearchScanType(ScanType.SPEC)
            self.widget.setFilePattern(None)
            self.widget.start_discovery(wait=self.WAIT_TIME)
            while self.qapp.hasPendingEvents():
                self.qapp.processEvents()
            assert self.signal_listener.callCount() == n_scan
