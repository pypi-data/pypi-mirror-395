# coding: utf-8
from __future__ import annotations

import gc

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.NotifierOW import NotifierWidgetOW


class TestTimerOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.widget = NotifierWidgetOW()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        gc.collect()

    def test(self):
        self.widget.show()
