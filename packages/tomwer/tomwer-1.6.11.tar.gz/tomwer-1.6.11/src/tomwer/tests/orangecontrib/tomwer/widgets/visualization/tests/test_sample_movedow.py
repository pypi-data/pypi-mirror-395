# coding: utf-8
from __future__ import annotations

import gc
import tempfile

import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.visualization.SampleMovedOW import SampleMovedOW
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSampleMoved(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        super().setUp()
        self._window = SampleMovedOW()
        self._tmp_path = tempfile.mkdtemp()

        self._scan = MockNXtomo(
            scan_path=self._tmp_path,
            create_ini_dark=True,
            create_ini_flat=True,
            create_final_flat=False,
            n_proj=10,
            n_ini_proj=10,
            dim=12,
        ).scan

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)

        self._window.updateScan(self._scan)
        self.qapp.processEvents()
