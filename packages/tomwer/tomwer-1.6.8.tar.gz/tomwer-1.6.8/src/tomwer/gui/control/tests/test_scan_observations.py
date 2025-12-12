from silx.gui import qt
from tomwer.gui.control.observations import ScanObservation
from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.tests.conftest import nxtomo_scan_180  # noqa F401


def test_ScanObservation(qtapp, nxtomo_scan_180):  # noqa F811
    widget = ScanObservation(parent=None)
    widget.addObservation(
        scan=nxtomo_scan_180,
    )

    model = widget.observationTable.model()
    # check time stamp
    assert len(model.data(model.createIndex(0, 0), qt.Qt.DisplayRole)) == 8
    # check type
    assert model.data(model.createIndex(0, 1), qt.Qt.DisplayRole) == "hdf5"
    # check n projections
    assert model.data(model.createIndex(0, 2), qt.Qt.DisplayRole) == 0
    # check status
    assert model.data(model.createIndex(0, 3), qt.Qt.DisplayRole) == "starting"
    # check identifier
    assert "NXtomo" in model.data(model.createIndex(0, 4), qt.Qt.DisplayRole)
