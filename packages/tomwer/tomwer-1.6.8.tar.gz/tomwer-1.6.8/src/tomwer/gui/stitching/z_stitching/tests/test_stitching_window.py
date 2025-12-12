from __future__ import annotations

import os
import shutil
import tempfile
import pint

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.stitching.tests.utils import create_scans_z_series
from tomwer.gui.stitching.StitchingWindow import ZStitchingWindow


_ureg = pint.get_application_registry()


class TestZStichingWindow(TestCaseQt):
    """
    Test high level z stitching definition
    """

    def setUp(self):
        super().setUp()
        self._tmp_path = tempfile.mkdtemp()
        self.scans = create_scans_z_series(
            os.path.join(self._tmp_path, "case1"),
            z_positions_m=(0.200, 0.205, 0.210),
            sample_pixel_size=0.001,
            raw_frame_width=100,
        )

        self._widget = ZStitchingWindow()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        shutil.rmtree(self._tmp_path)

    @staticmethod
    def checkNbReceivers(scan, nb_receivers):
        return (
            scan.stitching_metadata.receivers(scan.stitching_metadata.sigChanged)
            == nb_receivers
        )

    def test(self):
        self._widget.show()
        # fill the widget with scans

        for scan in self.scans:
            self._widget.addTomoObj(scan)
            # note: add the sigChanged to the z ordered list 'update z' slot
