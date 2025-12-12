# coding: utf-8
from __future__ import annotations


import gc
import os
import shutil
import tempfile

from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.visualization.DataViewerOW import DataViewerOW
from tomwer.core.utils.scanutils import MockNXtomo


class TestDataViewerOW(TestCaseQt):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan
        self.widget = DataViewerOW()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.tmp_dir)
        self.qapp.processEvents()
        gc.collect()

    def test(self):
        self.widget.addScan(self.scan)
        for mode in (
            "projections-radios",
            "slices",
            "raw darks",
            "raw flats",
            "reduced darks",
            "reduced flats",
        ):
            self.widget.viewer.setDisplayMode(mode)
            self.qapp.processEvents()

    def test_literal_dumps(self):
        """
        test settings are correcly dump to literals (and load)
        """
        self.widget._updateSettings()
        config = self.widget._viewer_config
        literal_dumps(config)
        self.widget._setSettings(config)
