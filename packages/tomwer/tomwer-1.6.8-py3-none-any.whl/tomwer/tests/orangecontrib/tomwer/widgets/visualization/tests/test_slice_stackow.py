# coding: utf-8
from __future__ import annotations

import gc

import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.visualization.SliceStackOW import SlicesStackOW
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skip("Fail on CI")
@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSliceStackOW(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        super().setUp()
        self._window = SlicesStackOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)
