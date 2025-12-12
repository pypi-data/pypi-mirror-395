# coding: utf-8
from __future__ import annotations


import gc
import os
import pickle
import shutil
import tempfile
from time import sleep

from nabu.pipeline.config import get_default_nabu_config
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.reconstruction.NabuVolumeOW import NabuVolumeOW
from tomwer.core.utils.scanutils import MockNXtomo


class TestNabuVolumeOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        self.scan = MockNXtomo(
            scan_path=os.path.join(self.tmp_dir, "myscan"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan
        self.widget = NabuVolumeOW()
        self.widget._processingStack.setDryRun(True)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.tmp_dir)
        self.qapp.processEvents()
        gc.collect()

    def test_serializing(self):
        pickle.dumps(self.widget.getConfiguration())

    def test_literal_dumps(self):
        literal_dumps(self.widget.getConfiguration())

    def test_scan_as_None(self):
        "test if scan is None"
        self.widget.process(None)

    def test_scan_un_preprocessed(self):
        "test when scan is unconfigured (No nabu_recons_params defined)"
        assert self.scan.nabu_recons_params is None
        self.widget.process(self.scan)

    def test_scan_ready_to_be_processed(self):
        "test if scan has valid reconstruction parameters to be runned"
        self.scan.nabu_recons_params = get_default_nabu_config(
            nabu_fullfield_default_config
        )
        self.widget.process(self.scan)
        timeout = 3
        loop_sleep_time = 0.05
        while not self.widget._processingStack.can_process_next():
            self.qapp.processEvents()
            timeout -= loop_sleep_time
            if timeout <= 0.0:
                raise TimeoutError("volume not process within expected time")
            else:
                sleep(loop_sleep_time)
