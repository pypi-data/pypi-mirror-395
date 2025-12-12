import gc
import os
import pickle
import shutil
import tempfile

import numpy
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.VolumeSelector import VolumeSelectorOW
from tomwer.core.volume.hdf5volume import HDF5Volume


class TestVolumeSelectorOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self.window = VolumeSelectorOW()
        self.folder = tempfile.mkdtemp()
        self.volume_1 = HDF5Volume(
            file_path=os.path.join(self.folder, "vol_file.hdf5"),
            data_path="entry0000",
            data=numpy.linspace(0, 10, 100 * 100 * 3).reshape(3, 100, 100),
        )
        self.volume_1.save()
        self.volume_2 = HDF5Volume(
            file_path=os.path.join(self.folder, "vol_file2.hdf5"),
            data_path="entry0001",
            data=numpy.linspace(60, 120, 100 * 100 * 5).reshape(5, 100, 100),
        )
        self.volume_2.save()

    def tearDown(self):
        self.window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.window.close()
        self.window = None
        shutil.rmtree(self.folder)
        gc.collect()

    def test(self):
        self.window.show()
        # check adding one volume
        self.window.addVolume(self.volume_1)
        assert self.window.widget.dataList.n_data() == 1
        # check behavior adding the same volume
        self.window.addVolume(self.volume_1)
        assert self.window.widget.dataList.n_data() == 1
        # check adding another volume
        self.window.addVolume(self.volume_2)
        assert self.window.widget.dataList.n_data() == 2
        # check removing volume(s)
        self.window.removeVolume(self.volume_1)
        assert self.window.widget.dataList.n_data() == 1
        self.window.removeVolume(self.volume_1)
        assert self.window.widget.dataList.n_data() == 1
        self.window.removeVolume(self.volume_2)
        assert self.window.widget.dataList.n_data() == 0

        # and adding them back
        self.window.addVolume(self.volume_1)
        self.window.addVolume(self.volume_2)
        assert self.window.widget.dataList.n_data() == 2

        # test serialization
        self.window._updateSettings()
        assert len(self.window._scanIDs) == 2
        pickle.dumps(self.window._scanIDs)
        literal_dumps(self.window._scanIDs)
