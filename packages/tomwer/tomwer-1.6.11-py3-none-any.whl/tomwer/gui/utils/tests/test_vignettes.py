"""
test vignettes
"""

import time
import numpy
import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.process.reconstruction.scores.scores import ComputedScore, ScoreMethod
from tomwer.gui.utils.vignettes import VignettesQDialog
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestVignettes(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._window = VignettesQDialog(
            value_name="cor",
            score_name="score",
        )

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        super().tearDown()

    def test(self):
        self._window.setScores(
            scores={
                "3": (numpy.ones((100, 100)), ComputedScore(tv=2.0, std=3.2)),
                "7": (numpy.zeros((100, 100)), ComputedScore(tv=25, std=0.6)),
            },
            score_method="standard deviation",
        )
        self._window.show()
        self.qWaitForWindowExposed(self._window)

        def assert_scores_are_equal(scores_1, scores_2):
            assert scores_1.keys() == scores_2.keys()
            for key, (data_1, computed_score_1) in scores_1.items():
                data_2, computed_score_2 = scores_2[key]
                numpy.testing.assert_array_almost_equal(data_1, data_2)
                assert computed_score_1 == computed_score_2

        scores, score_method = self._window._vignettesWidget.getScores()
        assert_scores_are_equal(
            scores_1=scores,
            scores_2={
                "3": (numpy.ones((100, 100)), ComputedScore(std=3.2, tv=None)),
                "7": (numpy.zeros((100, 100)), ComputedScore(std=0.6, tv=None)),
            },
        )
        assert score_method is ScoreMethod.STD

        self._window.setNbColumn(4)
        self._window.setNbColumn(2)
        with pytest.raises(ValueError):
            self._window.setNbColumn(20)
        self._window.setNbColumn("auto")

        self._window.resize(qt.QSize(400, 400))
        self.qapp.processEvents()
        time.sleep(VignettesQDialog.RESIZE_MAX_TIME * 2 / 1000)
        self.qapp.processEvents()
