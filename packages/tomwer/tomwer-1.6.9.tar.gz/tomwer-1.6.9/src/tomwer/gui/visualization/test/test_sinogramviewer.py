# coding: utf-8
from __future__ import annotations

import logging
import os
import shutil
import tempfile
import time
import unittest

from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt

from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.gui.visualization import sinogramviewer

logging.disable(logging.INFO)


class TestSinogramViewer(TestCaseQt):
    """unit test for the :class:_ImageStack widget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._widget = sinogramviewer.SinogramViewer()
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.tmp_dir = tempfile.mkdtemp()
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan

        # listen to the 'sigSinoLoadEnded' signal from the sinogram viewer
        self.signalListener = SignalListener()
        self._widget.sigSinoLoadEnded.connect(self.signalListener)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        self._widget.close()
        self._widget = None
        unittest.TestCase.tearDown(self)

    def test(self):
        """Make sur the addLeaf and clear functions are working"""
        self._widget.setScan(self.scan)
        timeout = 10
        while timeout >= 0 and self.signalListener.callCount() < 1:
            timeout -= 0.1
            time.sleep(0.1)
        if timeout >= 0:
            raise TimeoutError("widget never emitted the sigSinogramLoaded " "signal")
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        self.qapp.processEvents()
        self.assertTrue(self._widget.getActiveImage() is not None)
