from __future__ import annotations

import gc
import pickle

import pytest
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.cluster.SlurmClusterOW import SlurmClusterOW
from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSlurmClusterOW(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        super().setUp()
        self._window = SlurmClusterOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)
        configuration = self._window.getConfiguration()
        assert isinstance(configuration, SlurmClusterConfiguration)

    def test_serializing(self):
        pickle.dumps(self._window.getConfiguration().to_dict())

    def test_literal_dumps(self):
        literal_dumps(self._window.getConfiguration().to_dict())
