import gc
import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.DataValidatorOW import DataValidatorOW
from tomwer.core.utils.scanutils import MockNXtomo


class TestDataValidatorOW(TestCaseQt):
    """
    simple test on the DataValidatorOW widget
    """

    def setUp(self):
        super().setUp()
        self.window = DataValidatorOW()
        self.folder = tempfile.mkdtemp()
        self.scan_1 = MockNXtomo(
            scan_path=os.path.join(self.folder, "scan_1"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan
        self.scan_2 = MockNXtomo(
            scan_path=os.path.join(self.folder, "scan_2"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan

    def tearDown(self):
        self.window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.window.close()
        self.window = None
        shutil.rmtree(self.folder)
        gc.collect()

    def test(self):
        def wait_processing():
            while self.qapp.hasPendingEvents():
                self.qapp.processEvents()

        assert self.window.getNScanToValidate() == 0
        self.window.addScan(self.scan_1)
        wait_processing()
        self.window.addScan(self.scan_2)
        wait_processing()
        assert self.window.getNScanToValidate() == 2
        self.window._widget.validateCurrentScan()
        wait_processing()
        assert self.window.getNScanToValidate() == 1
