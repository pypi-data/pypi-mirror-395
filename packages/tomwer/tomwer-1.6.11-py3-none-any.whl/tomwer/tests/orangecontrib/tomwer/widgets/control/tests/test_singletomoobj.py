import gc
import os
import pickle
import shutil
import tempfile

import numpy
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.SingleTomoObjOW import SingleTomoObjOW
from tomwer.core.volume.hdf5volume import HDF5Volume


class TestSingleTomoObjOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.window = SingleTomoObjOW()
        self.folder = tempfile.mkdtemp()
        self.volume_1 = HDF5Volume(
            file_path=os.path.join(self.folder, "vol_file.hdf5"),
            data_path="entry0000",
            data=numpy.linspace(0, 10, 100 * 100 * 3).reshape(3, 100, 100),
        )
        self.volume_1.save()

    def tearDown(self):
        self.window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.window.close()
        self.window = None
        shutil.rmtree(self.folder)
        gc.collect()

    def test(self):
        self.window.show()
        self.window.widget.setTomoObject(self.volume_1)
        # test serialization
        pickle.dumps(self.window._tomo_obj_setting)
        literal_dumps(self.window._tomo_obj_setting)
