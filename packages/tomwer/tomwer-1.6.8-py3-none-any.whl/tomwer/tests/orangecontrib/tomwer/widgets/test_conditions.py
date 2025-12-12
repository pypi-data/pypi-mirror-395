# coding: utf-8
from __future__ import annotations

import gc
import logging
import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt

from orangecontrib.tomwer.widgets.control.FilterOW import NameFilterOW
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo

logging.disable(logging.INFO)


class NameFilterOWCI(NameFilterOW):
    sigScanReady = qt.Signal(str)
    """signal emitted when a scan is ready; Parameter is folder path of the
    scan"""

    def _signalScanReady(self, scan):
        self.sigScanReady.emit(scan.path)


class TestFilterWidget(TestCaseQt):
    """class testing the DarkRefWidget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self.widget = NameFilterOWCI(parent=None)

        self.tmpdir = tempfile.mkdtemp()
        # create hdf5 dataset
        self._hdf5with_mytotodir = MockNXtomo(
            scan_path=os.path.join(self.tmpdir, "mytotodir120"), n_proj=10
        ).scan
        self._hdf5without_mytotodir = MockNXtomo(
            scan_path=os.path.join(self.tmpdir, "totodir120"), n_proj=10
        ).scan
        # create edf dataset
        mockEDF1 = MockEDF(
            scan_path=os.path.join(self.tmpdir, "mytotodir20"), n_radio=10
        )
        self.edfwith_mytotodir = EDFTomoScan(scan=mockEDF1.scan_path)

        mockEDF2 = MockEDF(scan_path=os.path.join(self.tmpdir, "dir120"), n_radio=10)
        self.edfwithout_mytotodir = EDFTomoScan(scan=mockEDF2.scan_path)

        # add a signal listener
        self.signalListener = SignalListener()
        self.widget.sigScanReady.connect(self.signalListener)

        # define the unix file pattern
        self.widget.setPattern("*mytotodir*")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        gc.collect()

    def testEDF(self):
        """Make sure filtering works with EDF"""
        self.assertEqual(self.signalListener.callCount(), 0)
        self.widget.applyfilter(self.edfwith_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 1)
        self.widget.applyfilter(self.edfwithout_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 1)

    def testHDF5(self):
        """Make sure filtering works with HDF5"""
        self.assertEqual(self.signalListener.callCount(), 0)
        self.widget.applyfilter(self._hdf5without_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 0)
        self.widget.applyfilter(self._hdf5with_mytotodir)
        self.qapp.processEvents()
        self.assertEqual(self.signalListener.callCount(), 1)
