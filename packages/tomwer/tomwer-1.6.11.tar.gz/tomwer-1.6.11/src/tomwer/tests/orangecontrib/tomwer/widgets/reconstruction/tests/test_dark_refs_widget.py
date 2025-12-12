import gc
import logging
import os
import pickle
import tempfile

import numpy
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW import (
    DarkRefAndCopyOW,
)
from tomwer.core.utils.scanutils import MockNXtomo

logging.disable(logging.INFO)


class TestDarkRefWidget(TestCaseQt):
    """class testing the DarkRefWidget"""

    def setUp(self):
        self._tmp_path = tempfile.mkdtemp()
        scan_folder_with_raw = os.path.join(self._tmp_path, "test_dir_1")
        scan_folder_without_raw = os.path.join(self._tmp_path, "test_dir_2")
        for my_dir in (scan_folder_with_raw, scan_folder_without_raw):
            os.makedirs(my_dir)

        self._scan_with_raw = MockNXtomo(
            scan_path=scan_folder_with_raw,
            create_ini_dark=True,
            create_ini_flat=True,
            create_final_flat=False,
            n_proj=10,
            n_ini_proj=10,
            dim=12,
        ).scan
        self._scan_without_raw = MockNXtomo(
            scan_path=scan_folder_without_raw,
            create_ini_dark=False,
            create_ini_flat=False,
            create_final_flat=False,
            n_proj=10,
            n_ini_proj=10,
            dim=12,
        ).scan

        self.widget = DarkRefAndCopyOW()
        return super().setUp()

    def tearDown(self):
        # shutil.rmtree(self._tmp_path)
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        gc.collect()

    def test_serializing(self):
        self.widget._updateSettingsVals()
        pickle.dumps(self.widget._ewoks_default_inputs)

    def test_literal_dumps(self):
        self.widget._updateSettingsVals()
        literal_dumps(self.widget._ewoks_default_inputs)

    def test_copy(self):
        self.widget.setCopyActive(True)
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        assert len(os.listdir(self.widget._processing_stack._save_dir)) == 0

        self.widget.process(self._scan_with_raw)
        self.widget._processing_stack.wait_computation_finished()
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        assert self._scan_with_raw.load_reduced_darks() not in (None, {})
        assert self._scan_with_raw.load_reduced_flats() not in (None, {})
        assert len(os.listdir(self.widget._processing_stack._save_dir)) == 1
        assert len(os.listdir(self.widget._processing_stack._save_dir)) == 1

        self.widget.setCopyActive(False)
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        self.widget.process(self._scan_without_raw)
        self.widget._processing_stack.wait_computation_finished()
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        assert self._scan_without_raw.load_reduced_darks() in (None, {})
        assert self._scan_without_raw.load_reduced_flats() in (None, {})

        self.widget.setCopyActive(True)
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        self.widget.process(self._scan_without_raw)
        self.widget._processing_stack.wait_computation_finished()
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        assert self._scan_without_raw.load_reduced_darks() not in (None, {})
        assert self._scan_without_raw.load_reduced_flats() not in (None, {})

    def test_set_darks_and_flats(self):
        """
        Test settings darks and flats.
        """
        self.widget.setCopyActive(True)

        assert len(os.listdir(self.widget._processing_stack._save_dir)) == 0
        self.widget.setReducedFlats(
            {
                "0.0r": numpy.linspace(12, 12 + 12 * 12, 12 * 12).reshape(12, 12),
                "1.0r": numpy.linspace(24, 24 + 12 * 12, 12 * 12).reshape(12, 12),
            }
        )
        self.widget.setReducedDarks(
            {
                "0.0r": numpy.linspace(0, 12 * 12, 12 * 12).reshape(12, 12),
            }
        )
        self.widget.process(self._scan_without_raw)
        self.widget._processing_stack.wait_computation_finished()
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()

        loaded_reduced_darks = self._scan_without_raw.load_reduced_darks()
        assert tuple(loaded_reduced_darks.keys()) == (0,)
        numpy.testing.assert_allclose(
            loaded_reduced_darks[0],
            numpy.linspace(0, 12 * 12, 12 * 12).reshape(12, 12),
        )

        loaded_reduced_flats = self._scan_without_raw.load_reduced_flats()
        assert tuple(loaded_reduced_flats.keys()) == (0, 9)
        numpy.testing.assert_allclose(
            loaded_reduced_flats[9],
            numpy.linspace(24, 24 + 12 * 12, 12 * 12).reshape(12, 12),
        )
