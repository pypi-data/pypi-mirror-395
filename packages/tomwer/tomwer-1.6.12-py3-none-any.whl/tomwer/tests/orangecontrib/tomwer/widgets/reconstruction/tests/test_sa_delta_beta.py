import logging
import os
import pickle

import numpy
from orangecanvas.scheme.readwrite import literal_dumps
from processview.core.manager import DatasetState, ProcessManager
from silx.io.url import DataUrl
from silx.gui import qt

from orangecontrib.tomwer.widgets.reconstruction.SADeltaBetaOW import (
    SADeltaBetaOW as _SADeltaBetaOW,
)
from tomwer.core.process.reconstruction.scores import ComputedScore
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.tests.conftest import qtapp  # noqa F401

logger = logging.getLogger(__name__)


class SADeltaBetaOW(_SADeltaBetaOW):
    """class saving scan finished to keep a trace on those."""

    def __init__(self, parent=None):
        self._scans_finished = []
        super().__init__(parent)

    def processing_finished(self, scan):
        self._scans_finished.append(scan)

    @property
    def scans_finished(self):
        return self._scans_finished

    def close(self):
        self._scans_finished = {}
        super().close()


FRAME_DIM = 100


def create_scan(output_dir):
    return MockNXtomo(
        scan_path=output_dir,
        n_ini_proj=20,
        n_proj=20,
        n_alignement_proj=2,
        create_final_flat=False,
        create_ini_dark=True,
        create_ini_flat=True,
        n_refs=1,
        dim=FRAME_DIM,
    ).scan


def patch_score(*args, **kwargs):
    """Function to save some result"""
    return DataUrl(
        file_path="/no_existing/path.hdf5",
        data_path="/no_existing_data_path",
        scheme="silx",
    ), ComputedScore(
        tv=numpy.random.random(),
        std=numpy.random.random(),
    )


def test_SADeltaBetaOW(
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

    widget = SADeltaBetaOW()
    widget.show()

    widget._widget._processing_stack.patch_processing(patch_score)

    # make sure the configuration is serializable
    pickle.dumps(widget.getConfiguration())

    # make sure this is compatible with 'literal dumps'
    literal_dumps(widget.getConfiguration())

    # test behavior when 'autofocus' is lock. (in this case we expect to take the dataset with the higher score) and continue
    widget.lockAutofocus(False)

    def manual_processing():
        widget.compute()
        qt.QApplication.processEvents()
        widget.wait_processing(5000)
        qt.QApplication.processEvents()

    widget.process(scan_1)
    manual_processing()
    assert (
        process_manager.get_dataset_state(
            dataset_id=scan_1.get_identifier(),
            process=widget,
        )
        == DatasetState.WAIT_USER_VALIDATION
    )

    widget.process(scan_2)
    manual_processing()
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
    manual_processing()
    widget.validateCurrentScan()
    assert (
        process_manager.get_dataset_state(
            dataset_id=scan_3.get_identifier(),
            process=widget,
        )
        == DatasetState.SUCCEED
    )

    # ensure a cor has been registered
    assert scan_3.sa_delta_beta_params.selected_delta_beta_value is not None
