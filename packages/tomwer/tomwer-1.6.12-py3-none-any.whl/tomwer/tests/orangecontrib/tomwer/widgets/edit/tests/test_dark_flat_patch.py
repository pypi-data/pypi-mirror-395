# coding: utf-8
from __future__ import annotations

import gc
import os
import pickle
import tempfile

import h5py
import numpy
import pytest
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from silx.io.url import DataUrl

from orangecontrib.tomwer.widgets.edit.DarkFlatPatchOW import DarkFlatPatchOW
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestDarkFlatPatch(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        super().setUp()
        self._window = DarkFlatPatchOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def test_serialiazation(self):
        with tempfile.TemporaryDirectory() as tmp_path:
            file_path = os.path.join(tmp_path, "darks.hdf5")
            with h5py.File(file_path, mode="w") as h5f:
                h5f.require_group("darks")["0"] = numpy.ones((10, 10))
            dark_url = DataUrl(file_path=file_path, data_path="darks/0")
            self._window.widget.setStartDarkUrl(url=dark_url)
            config = self._window.getConfiguration()
            pickle.dumps(config)
            literal_dumps(config)

            self._window.setConfiguration(config)
