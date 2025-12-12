import os
from tomoscan.series import Series
import pickle

from ewoksorange.bindings.qtapp import QtEvent

from orangecanvas.scheme.readwrite import literal_dumps

from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.core.utils.scanutils import MockNXtomo

from orangecontrib.tomwer.widgets.control.NXtomoConcatenate import NXtomoConcatenateOW


def test_NabuHelicalPrepareWeightsDoubleOW(
    qtapp,  # noqa F811
    tmp_path,
):
    """simple test of the _DeltaBetaSelectorDialog"""
    widget = NXtomoConcatenateOW()
    widget._loadSettings()
    # test settings serialization
    pickle.dumps(widget._ewoks_default_inputs)
    literal_dumps(widget._ewoks_default_inputs)

    scan_1 = MockNXtomo(
        scan_path=os.path.join(tmp_path, "scan1"),
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=20,
        energy=12.3,
    ).scan
    scan_2 = MockNXtomo(
        scan_path=os.path.join(tmp_path, "scan2"),
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=20,
        energy=12.3,
    ).scan

    output_scan_file = os.path.join(tmp_path, "concatenation.nx")
    assert not os.path.exists(output_scan_file)

    widget.widget.setConfiguration(
        {
            "output_file": output_scan_file,
        }
    )

    # process task
    finished = QtEvent()

    def finished_callback():
        finished.set()

    executor = widget.task_executor_queue
    executor.sigComputationEnded.connect(finished_callback)
    widget._process_series(series=Series(iterable=[scan_1, scan_2]))

    # wait until processing is finished
    assert finished.wait(timeout=10)
    assert os.path.exists(output_scan_file)
