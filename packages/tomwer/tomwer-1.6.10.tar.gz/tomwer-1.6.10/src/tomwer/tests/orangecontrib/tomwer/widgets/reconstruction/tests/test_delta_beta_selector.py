import numpy

from orangecontrib.tomwer.widgets.reconstruction.NabuVolumeOW import (
    _DeltaBetaSelectorDialog,
)
from tomwer.tests.conftest import qtapp  # noqa F401


def test_DeltaBetaSelector(
    qtapp,  # noqa F811
):
    """simple test of the _DeltaBetaSelectorDialog"""
    dialog = _DeltaBetaSelectorDialog(values=(12, 45))
    dialog.show()
    assert numpy.isscalar(dialog.getSelectedValue())
