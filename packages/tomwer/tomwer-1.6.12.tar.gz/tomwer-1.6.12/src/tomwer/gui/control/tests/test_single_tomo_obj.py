import os
import tempfile

import numpy
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.gui.control.singletomoobj import SingleTomoObj


class TestSingletomoObj(TestCaseQt):
    """
    Test of SingleTomoObj interface
    """

    def setUp(self):
        super().setUp()
        self._tempdir = tempfile.mkdtemp()
        self._widget = SingleTomoObj()

        self._volume_file_path = os.path.join(self._tempdir, "volume.hdf5")
        self.volume = HDF5Volume(
            file_path=self._volume_file_path,
            data_path="my_volume",
            data=numpy.linspace(start=0, stop=200, num=200).reshape((2, 10, 10)),
        )
        self.volume.save()

        self._scan_file_path = os.path.join(self._tempdir, "scan.nx")
        self.scan_hdf5 = MockNXtomo(
            scan_path=self._scan_file_path,
            n_proj=10,
            n_ini_proj=10,
            create_ini_dark=False,
            create_ini_flat=False,
            dim=10,
        ).scan

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().tearDown()

    def test_set_volume(self):
        self._widget.setTomoObject(self.volume)
        assert (
            self._widget.getTomoObjIdentifier() == self.volume.get_identifier().to_str()
        )
        self._widget.setTomoObject("")
        assert self._widget.getTomoObjIdentifier() == ""
        self._widget.setTomoObject(self.volume.get_identifier().to_str())
        assert (
            self._widget.getTomoObjIdentifier() == self.volume.get_identifier().to_str()
        )

    def test_set_scan(self):
        self._widget.setTomoObject(self.scan_hdf5)
        assert (
            self._widget.getTomoObjIdentifier()
            == self.scan_hdf5.get_identifier().to_str()
        )
        self._widget.setTomoObject("")
        assert self._widget.getTomoObjIdentifier() == ""
        self._widget.setTomoObject(self.scan_hdf5.get_identifier().to_str())
        assert (
            self._widget.getTomoObjIdentifier()
            == self.scan_hdf5.get_identifier().to_str()
        )
