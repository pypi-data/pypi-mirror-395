from nabu.stitching.utils import ShiftAlgorithm as _NabuShiftAlgorithm
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.stitching.z_stitching.fineestimation import Axis_N_Params


class TestAxis_N_Params(TestCaseQt):
    """
    Test definition of an axis shift research parameters
    """

    def setUp(self):
        super().setUp()
        self._widget = Axis_N_Params("axis n", None)

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()

    def test(self):
        self._widget.show()
        assert self._widget.getCurrentMethod() == _NabuShiftAlgorithm.NONE
        opts1 = self._widget.getOptsLine()
        assert opts1 == "img_reg_method=None"
        self._widget.setCurrentMethod(_NabuShiftAlgorithm.NABU_FFT)
        opts2 = self._widget.getOptsLine()
        assert opts2 == "img_reg_method=nabu-fft"
        self._widget.setOptsLine(opts1)
        assert self._widget.getOptsLine() == opts1
        self._widget.setOptsLine(opts2)
        assert self._widget.getOptsLine() == opts2
