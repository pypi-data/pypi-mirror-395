# coding: utf-8
from __future__ import annotations


import shutil
import tempfile

import pytest
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.utils.scanutils import MockEDF
from tomwer.gui.control.scanselectorwidget import ScanSelectorWidget
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestScanSelector(TestCaseQt):
    """
    Simple test for the ScanSelectorWidget
    """

    def setUp(self):
        self._folder1 = tempfile.mkdtemp()
        self._folder2 = tempfile.mkdtemp()
        self._folder3 = tempfile.mkdtemp()
        for _folder in (self._folder1, self._folder2, self._folder3):
            MockEDF.mockScan(scanID=_folder, nRadio=5, nRecons=5, nPagRecons=0, dim=10)

        self.widget = ScanSelectorWidget(parent=None)

    def tearDown(self):
        shutil.rmtree(self._folder1)
        shutil.rmtree(self._folder2)
        shutil.rmtree(self._folder3)

    def test(self):
        self.widget.add(self._folder1)
        self.widget.add(self._folder2)
        self.widget.add(self._folder3)
        self.assertEqual(self.widget.dataList.n_data(), 3)
        self.widget.remove(self._folder3)
        self.assertEqual(self.widget.dataList.n_data(), 2)
