import numpy

from tomwer.gui.utils.lineselector.lineselector import QSliceSelectorDialog
from tomwer.tests.conftest import qtapp  # noqa F401


def test_line_selector(
    qtapp,  # noqa F811
):
    dialog = QSliceSelectorDialog(parent=None)
    dialog.setData(
        numpy.ones((100, 100)),
    )
    dialog.mainWidget.addSlice(2)
    dialog.mainWidget.addSlice(12)
    assert dialog.getSelection() == (2, 12)
    dialog.mainWidget.removeSlice(12)
    assert dialog.getSelection() == (2,)
    dialog.setSelection((12, 23))
    assert dialog.getSelection() == (12, 23)
    assert dialog.mainWidget.nSelected() == 2
