# coding: utf-8
from __future__ import annotations

import gc

import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.edit.ImageKeyEditorOW import ImageKeyEditorOW
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestImageKeyEditor(TestCaseQt):
    """Test that the ImageKeyEditorOW widget work correctly (at least launched)"""

    def setUp(self):
        super().setUp()
        self._window = ImageKeyEditorOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)
