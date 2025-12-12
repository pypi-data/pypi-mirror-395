# coding: utf-8
from __future__ import annotations


import gc
import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.visualization.DiffViewerOW import DiffViewerOW
from tomwer.core.utils.scanutils import MockNXtomo


class TestDiffViewerOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        os.makedirs(self.tmp_dir, exist_ok=True)
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan
        self.widget = DiffViewerOW()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        self.qapp.processEvents()
        shutil.rmtree(self.tmp_dir)
        gc.collect()

    def test(self):
        self.widget.addScan(self.scan)
