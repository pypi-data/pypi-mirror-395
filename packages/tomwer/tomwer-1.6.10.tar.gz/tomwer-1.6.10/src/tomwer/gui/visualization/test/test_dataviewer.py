# coding: utf-8
from __future__ import annotations

import unittest

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.visualization.dataviewer import DataViewer, ImageStack


class TestImageStack(TestCaseQt):
    """Test that the ImageStackWidget can be load and remove without any issue"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._widget = ImageStack(None)

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        self.qapp.processEvents()
        unittest.TestCase.tearDown(self)

    def test(self):
        pass


class TestDataViewer(TestCaseQt):
    """Test that the data viewer can be load and remove without any issue"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._widget = DataViewer(None)

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        self.qapp.processEvents()
        unittest.TestCase.tearDown(self)

    def test(self):
        pass
