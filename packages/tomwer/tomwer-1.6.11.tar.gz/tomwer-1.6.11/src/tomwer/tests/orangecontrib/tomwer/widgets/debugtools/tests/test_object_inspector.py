# coding: utf-8
from __future__ import annotations


import gc
import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.debugtools.ObjectInspectorOW import ObjectInspectorOW
from tomwer.core.utils.scanutils import MockNXtomo


class TestObjectInspectorOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        gc.collect()

    def test(self):
        widget = ObjectInspectorOW()
        widget.setObject(self.scan)
        widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        widget.close()
