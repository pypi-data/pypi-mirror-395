# coding: utf-8
from __future__ import annotations

import gc
import os
import pickle
import tempfile
import time

import numpy
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.reconstruction.CastNabuVolumeOW import (
    CastNabuVolumeOW,
)
from tomwer.core.volume.rawvolume import RawVolume


class TestCastVolumeOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._window = CastNabuVolumeOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def test_serializing(self):
        pickle.dumps(self._window.getConfiguration())

    def test_literal_dumps(self):
        literal_dumps(self._window.getConfiguration())

    def test_cast_volume(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_dir = os.path.join(tmp_dir, "input")
            os.makedirs(input_dir)

            volume = RawVolume(
                file_path=os.path.join(input_dir, "vol_file.vol"),
                data=numpy.linspace(0, 10, 100 * 100 * 3, dtype=numpy.float32).reshape(
                    3, 100, 100
                ),
            )
            volume.save()

            self._window.process_volume(volume)
            while self._window._processingStack.is_computing():
                time.sleep(0.1)
                self.qapp.processEvents()
