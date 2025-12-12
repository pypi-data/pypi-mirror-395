# coding: utf-8
from __future__ import annotations

import unittest

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.control.datavalidator import DataValidator


class TestValidatorGUI(TestCaseQt):
    """Test that the ImageStackWidget can be load and remove without any issue"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._widget = DataValidator(None)

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        unittest.TestCase.tearDown(self)

    def test(self):
        """Make sur the addLeaf and clear functions are working"""
        pass
