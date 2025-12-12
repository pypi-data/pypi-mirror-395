import gc

import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.visualization.NXtomoMetadataViewerOW import (
    NXtomoMetadataViewerOW,
)
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestNXtomoMetadataViewerOW(TestCaseQt):
    """Test that the NXtomoEditorOW widget work correctly. Processing test are done in the core module. gui test are done in the tomwer.gui.edit module"""

    def setUp(self):
        super().setUp()
        self._window = NXtomoMetadataViewerOW()

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        gc.collect()

    def test(self):
        self._window.show()
        self.qWaitForWindowExposed(self._window)
