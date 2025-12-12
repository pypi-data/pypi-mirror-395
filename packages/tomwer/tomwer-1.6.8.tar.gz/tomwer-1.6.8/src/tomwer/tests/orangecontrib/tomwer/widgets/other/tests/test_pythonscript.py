import gc
import logging

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.other.PythonScriptOW import OWPythonScript
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.volume.hdf5volume import HDF5Volume

logging.disable(logging.INFO)


class TestEDFDarkRefWidget(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)
        self.widget = OWPythonScript()
        self._scan = NXtomoScan("my_file.hdf5", entry="entry0000")
        self._volume = HDF5Volume(file_path="my_volume.hdf5", data_path="volume")

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        gc.collect()

    def test_handle_data(self):
        self.widget.handle_input(self._scan, (1,), "data")

    def test_handle_volume(self):
        self.widget.handle_input(self._volume, (1,), "volume")
