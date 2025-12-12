import gc
import pickle
import numpy

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.ReduceDarkFlatSelectorOW import (
    ReduceDarkFlatSelectorOW,
)
from orangecanvas.scheme.readwrite import literal_dumps


class TestEmailOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.widget = ReduceDarkFlatSelectorOW()
        self.widget._dialog.addReduceFrames(
            {
                "reduce_frames_name": "new dict",
                -1: numpy.random.random(100 * 100).reshape(100, 100),
                2: numpy.random.random(100 * 100).reshape(100, 100),
            },
            selected=(-1, 2),
        )

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        gc.collect()

    def test(self):
        self.widget.show()

    def test_serializing(self):
        pickle.dumps(self.widget.getConfiguration())

    def test_literal_dumps(self):
        literal_dumps(self.widget.getConfiguration())
