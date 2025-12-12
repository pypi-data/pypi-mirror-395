# coding: utf-8
from __future__ import annotations

import os
import shutil
import tempfile

import numpy
import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.volume import EDFVolume, HDF5Volume
from tomwer.gui.control.volumeselectorwidget import VolumeSelectorWidget
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestVolumeSelector(TestCaseQt):
    """
    Simple test for the VolumeSelector
    """

    def setUp(self):
        super().setUp()
        self.folder = tempfile.mkdtemp()

        self.volume_1 = HDF5Volume(
            file_path=os.path.join(self.folder, "my_volume.hdf5"),
            data_path="entry0000",
            data=numpy.linspace(start=1, stop=100, num=300).reshape((3, 10, 10)),
        )
        self.volume_1.save()

        self.volume_2 = HDF5Volume(
            file_path=os.path.join(self.folder, "my_volume.hdf5"),
            data_path="entry0001",
            data=numpy.linspace(start=1, stop=100, num=400).reshape((4, 10, 10)),
        )
        self.volume_2.save()

        self.volume_3 = EDFVolume(
            folder=os.path.join(self.folder, "vol"),
            data=numpy.linspace(start=1, stop=100, num=500).reshape((5, 10, 10)),
        )
        self.volume_3.save()

        self.widget = VolumeSelectorWidget(parent=None)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.folder)
        super().tearDown()

    def test(self):
        for volume in (self.volume_1, self.volume_2, self.volume_3):
            self.widget.add(volume)

        # self.widget.show()
        # self.qapp.exec()
        self.assertEqual(self.widget.dataList.n_data(), 3)
        self.widget.remove(self.volume_2)
        self.assertEqual(self.widget.dataList.n_data(), 2)
        self.widget.remove(self.volume_3)
        self.assertEqual(self.widget.dataList.n_data(), 1)
        assert self.widget.dataList.rowCount() == 1
