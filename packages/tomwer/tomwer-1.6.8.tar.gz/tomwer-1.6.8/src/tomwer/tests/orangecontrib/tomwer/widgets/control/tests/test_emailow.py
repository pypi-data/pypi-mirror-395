import gc
import pickle

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.EmailOW import EmailOW
from orangecanvas.scheme.readwrite import literal_dumps


class TestEmailOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.widget = EmailOW()

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
