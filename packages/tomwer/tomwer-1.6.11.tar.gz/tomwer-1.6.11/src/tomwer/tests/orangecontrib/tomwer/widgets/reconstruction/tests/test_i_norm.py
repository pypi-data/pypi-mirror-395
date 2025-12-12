# coding: utf-8
from __future__ import annotations

import logging
import os
import pickle

from orangecanvas.scheme.readwrite import literal_dumps
from processview.core.manager import DatasetState, ProcessManager
from silx.gui import qt

from orangecontrib.tomwer.widgets.reconstruction.SinoNormOW import (
    SinoNormOW as _SinoNormOW,
)
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.tests.conftest import qtapp  # noqa F401

logger = logging.getLogger(__name__)


class SinoNormOW(_SinoNormOW):
    def __init__(self, parent=None):
        self._scans_finished = []
        super().__init__(parent)

    def processing_finished(self, scan):
        self._scans_finished.append(scan)

    def wait_processing(self, wait_time):
        self._window._processing_stack._computationThread.wait(wait_time)

    @property
    def scans_finished(self):
        return self._scans_finished

    def compute(self):
        self._window._processCurrentScan()

    def setROI(self, start_x, end_x, start_y, end_y):
        self._window.setROI(start_x=start_x, end_x=end_x, start_y=start_y, end_y=end_y)

    def close(self):
        self._scans_finished = {}
        super().close()


FRAME_DIM = 100


def create_scan(folder_name):
    return MockNXtomo(
        scan_path=folder_name,
        n_ini_proj=20,
        n_proj=20,
        n_alignement_proj=2,
        create_final_flat=False,
        create_ini_dark=True,
        create_ini_flat=True,
        n_refs=1,
        dim=FRAME_DIM,
    ).scan


def test_SinoNormOW(
    qtapp,  # noqa F811
    tmp_path,
):
    source_dir = tmp_path / "source"
    source_dir.mkdir()

    # create scans
    scan_1 = create_scan(os.path.join(source_dir, "scan_1"))
    scan_2 = create_scan(os.path.join(source_dir, "scan_2"))
    scan_3 = create_scan(os.path.join(source_dir, "scan_3"))
    process_manager = ProcessManager()

    widget = SinoNormOW()
    widget.show()

    # test serialization
    pickle.dumps(widget.getConfiguration())

    # test literal dumps
    widget._updateSettings()
    literal_dumps(widget._ewoks_default_inputs)

    # test behavior when the widget is unlocked
    """Test result when used with some interaction"""
    widget.setLocked(False)

    def process_scalar_manually():
        widget.setCurrentMethod("division")
        widget.setCurrentSource("manual ROI")

        qt.QApplication.processEvents()
        widget.setROI(start_x=0, end_x=10, start_y=0, end_y=10)
        qt.QApplication.processEvents()
        widget.compute()
        widget.wait_processing(5000)
        qt.QApplication.processEvents()

    widget.process(scan_1)
    process_scalar_manually()
    assert (
        process_manager.get_dataset_state(
            dataset_id=scan_1.get_identifier(),
            process=widget,
        )
        == DatasetState.WAIT_USER_VALIDATION
    )

    widget.process(scan_2)
    process_scalar_manually()
    assert len(widget.scans_finished) == 0
    assert (
        process_manager.get_dataset_state(
            dataset_id=scan_1.get_identifier(),
            process=widget,
        )
        == DatasetState.SKIPPED
    )
    assert (
        process_manager.get_dataset_state(
            dataset_id=scan_2.get_identifier(),
            process=widget,
        )
        == DatasetState.WAIT_USER_VALIDATION
    )

    widget.process(scan_3)
    process_scalar_manually()
    widget.validateCurrentScan()
    assert (
        process_manager.get_dataset_state(
            dataset_id=scan_3.get_identifier(),
            process=widget,
        )
        == DatasetState.SUCCEED
    )

    # test behavior when the widget is locked

    widget.setLocked(True)
    for scan in (scan_1, scan_2, scan_3):
        widget.process(scan)
        widget.wait_processing(5000)
        qt.QApplication.processEvents()

    for scan in (scan_1, scan_2, scan_3):
        # test status is SUCCEED
        assert (
            process_manager.get_dataset_state(
                dataset_id=scan.get_identifier(),
                process=widget,
            )
            == DatasetState.SUCCEED
        )
