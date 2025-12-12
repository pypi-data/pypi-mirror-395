# coding: utf-8
from __future__ import annotations

import numpy
import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.utils import inputwidget
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class SelectionLineEditTest(TestCaseQt):
    """Test the SelectionLineEdit"""

    def setUp(self):
        super().setUp()
        self.widget = inputwidget.SelectionLineEdit(parent=None)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        super().tearDown()

    def testListSelection(self):
        self.widget.mode = inputwidget.SelectionLineEdit.LIST_MODE
        self.widget.setText("1.0, 2.0; 6.3")
        self.assertTrue(self.widget.selection == (1.0, 2.0, 6.3))
        self.widget.setText("1.0:3.6:0.2")
        self.assertTrue(
            self.widget.selection == tuple(numpy.linspace(1.0, 3.6, num=int(2.6 / 0.2)))
        )
        self.assertTrue(
            self.widget.getMode() == inputwidget.SelectionLineEdit.RANGE_MODE
        )
        self.widget.setText("1.0")
        self.assertTrue(self.widget.selection == 1.0)

    def testRangeSelection(self):
        self.widget.mode = inputwidget.SelectionLineEdit.RANGE_MODE
        self.widget.setText("1.0:3.6:0.2")
        self.assertTrue(
            self.widget.selection == tuple(numpy.linspace(1.0, 3.6, num=int(2.6 / 0.2)))
        )
        self.widget.setText("1.0")
        self.assertTrue(self.widget.selection == 1.0)
        self.widget.setText("1.0, 2.0, 6.3")
        self.assertTrue(
            self.widget.getMode() == inputwidget.SelectionLineEdit.LIST_MODE
        )
        self.assertTrue(self.widget.selection == (1.0, 2.0, 6.3))
