from __future__ import annotations


import os
import shutil
import tempfile

import numpy
import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomoscan.esrf.volume.edfvolume import EDFVolume
from tomoscan.esrf.volume.hdf5volume import HDF5Volume

from tomwer.gui.dialog.QVolumeDialog import QVolumeDialog
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestVolumeDialog(TestCaseQt):
    """Test QVolumeDialog"""

    def setUp(self):
        super().setUp()
        self.tmp_dir = tempfile.mkdtemp()
        self._dialog = QVolumeDialog()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        self._dialog.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._dialog.close()
        self._dialog = None
        return super().tearDown()

    def test_provide_hdf5_volume_auto(self):
        """
        Test everything can be discovered from a single 'default' hdf5 file
        """
        self._dialog.setFullAuto(True)
        file_path = os.path.join(self.tmp_dir, "myvolume.nx")
        volume = HDF5Volume(
            file_path=file_path,
            data_path="entry",
            data=numpy.linspace(start=1, stop=10, num=300, dtype=numpy.uint8).reshape(
                (3, 10, 10)
            ),
        )
        volume.save()
        self._dialog.show()
        self._dialog.setFilePath(file_path)
        self.qapp.processEvents()
        assert self._dialog.getDataPath() in ("entry", "/entry")
        assert self._dialog.getDataExtension() == "nx"
        assert self._dialog.getVolumeBasename() in ("", None)
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_hdf5_volume_manual(self):
        """
        Test we can create a volume if everything is defined manually from hdf5 volume file
        """
        self._dialog.setFullAuto(False)
        file_path = os.path.join(self.tmp_dir, "myvolume.nx")
        volume = HDF5Volume(
            file_path=file_path,
            data_path="entry",
            data=numpy.linspace(start=1, stop=10, num=300, dtype=numpy.uint8).reshape(
                (3, 10, 10)
            ),
        )
        volume.save()

        self._dialog.setDataExtension("nx")
        assert self._dialog.getVolume() is not None
        self._dialog.setFilePath(file_path)
        self._dialog.setDataPath("entry")
        volume_defined = self._dialog.getVolume()
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_edf_volume_auto(self):
        """
        Test everything can be discovered from a single 'default' edf volume folder
        """
        self._dialog.setFullAuto(True)
        volume = EDFVolume(
            folder=self.tmp_dir,
            data=numpy.linspace(start=1, stop=10, num=300, dtype=numpy.uint8).reshape(
                (3, 10, 10)
            ),
        )
        volume.save()
        self._dialog.show()

        self._dialog.setFilePath(self.tmp_dir)
        self.qapp.processEvents()
        assert self._dialog.getDataPath() in ("", None)
        assert self._dialog.getDataExtension() == "edf"
        assert self._dialog.getVolumeBasename() == os.path.basename(self.tmp_dir)
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_edf_volume_manual(self):
        """
        Test we can create a volume if everything is defined manually from edf volume folder
        """
        self._dialog.setFullAuto(False)
        volume = EDFVolume(
            folder=self.tmp_dir,
            data=numpy.linspace(start=1, stop=10, num=300, dtype=numpy.uint8).reshape(
                (3, 10, 10)
            ),
            volume_basename="test",
        )
        volume.save()
        self._dialog.show()

        self._dialog.setFilePath(self.tmp_dir)
        self.qapp.processEvents()
        self._dialog.setDataExtension(
            ".edf"
        )  # should be edf but test works also if user add the dot
        self._dialog.setVolumeBasename("test")
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert (
            self._dialog._volumeUrlQL.text() == volume_defined.get_identifier().to_str()
        )

    def test_provide_hdf5_volume_url(self):
        """
        Test we can create a volume if the url (of a hdf5 volume) is provided by the user
        """
        file_path = os.path.join(self.tmp_dir, "myvolume.hdf")
        volume = HDF5Volume(
            file_path=file_path,
            data_path="entry",
            data=numpy.linspace(start=1, stop=10, num=300, dtype=numpy.uint8).reshape(
                (3, 10, 10)
            ),
        )
        volume.save()
        self._dialog.setVolumeUrl(volume.get_identifier().to_str())
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert self._dialog.getDataPath() in ("entry", "/entry")
        assert self._dialog.getVolumeBasename() in ("", None)
        assert self._dialog.getFilePath() == file_path
        assert self._dialog.getDataExtension() == "hdf"

    def test_provide_edf_volume_url(self):
        """
        Test we can create a volume if the url (of a EDFVolume) is provided by the user
        """
        volume = EDFVolume(
            folder=self.tmp_dir,
            data=numpy.linspace(start=1, stop=10, num=300, dtype=numpy.uint8).reshape(
                (3, 10, 10)
            ),
            volume_basename="test",
        )
        volume.save()
        self._dialog.setVolumeUrl(volume.get_identifier().to_str())
        volume_defined = self._dialog.getVolume()
        assert volume_defined is not None
        volume_defined.load()
        assert volume_defined.data is not None
        assert self._dialog.getDataPath() in ("", None)
        assert self._dialog.getVolumeBasename() == "test"
        assert self._dialog.getFilePath() == self.tmp_dir
        assert self._dialog.getDataExtension() == "edf"
