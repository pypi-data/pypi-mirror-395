from __future__ import annotations

import os
import shutil
import tempfile
import pint
import numpy

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.process.stitching.metadataholder import StitchingMetadata
from tomwer.gui.stitching.metadataholder import QStitchingMetadata
from tomwer.gui.stitching.tests.utils import create_scans_z_series
from tomwer.gui.stitching.config.tomoobjdetails import TomoObjectPositionInfos
from tomwer.gui.stitching.axisorderedlist import AxisOrderedTomoObjsModel

_ureg = pint.get_application_registry()


class TestTomoObjectPositionInfos(TestCaseQt):
    """
    Test edition of the tomo object position information
    """

    def setUp(self):
        super().setUp()
        self._tmp_path = tempfile.mkdtemp()
        self._y_pixel_size = 0.002
        self._x_pixel_size = 0.001
        self.scans = create_scans_z_series(
            self._tmp_path,
            z_positions_m=(0.200, 0.205, 0.210),
            x_positions_m=(0.0, 0.0, None),
            sample_pixel_size=(self._y_pixel_size, self._x_pixel_size),
            raw_frame_width=100,
        )
        self.scan_0_metadata = QStitchingMetadata(tomo_obj=self.scans[0])
        numpy.testing.assert_almost_equal(
            self.scan_0_metadata.get_raw_position_m(axis=0), 0.20
        )

        assert self.scan_0_metadata.get_raw_position_m(axis=2) == 0.0
        self.scan_2_metadata = QStitchingMetadata(tomo_obj=self.scans[2])
        numpy.testing.assert_almost_equal(
            self.scan_2_metadata.get_raw_position_m(axis=0), 0.21
        )
        self._widget = TomoObjectPositionInfos()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        shutil.rmtree(self._tmp_path)

    def testEdition(self):
        # test QStitchingMetadata are correctly read
        self._widget.show()
        self._widget.setStitchingMetadata(self.scan_0_metadata)
        self.qapp.processEvents()
        assert self._widget._axis_0_pos.get_final_px_position() == int(0.20 / 0.002)
        assert self._widget._axis_2_pos.get_final_px_position() == 0
        self._widget.setStitchingMetadata(self.scan_2_metadata)
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        assert self._widget._axis_0_pos.get_final_px_position() == int(0.21 / 0.002)
        assert self._widget._axis_2_pos.get_final_px_position() is None
        # test editing some parameters from the GUI. Make sure GUI is updated as the underlying metadata object
        self._widget._axis_0_pos._overrideMetricPositionCB.setChecked(True)
        self._widget._axis_0_pos.setRawMetricPosition(
            position_m=0.4, displayed_unit=_ureg.nanometer
        )
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        assert self._widget._axis_0_pos.get_final_px_position() == int(
            0.4 * 10e-6 / 0.002
        )
        self._widget._axis_0_pos._overridePixelPositionCB.setChecked(True)
        self._widget._axis_0_pos.setOverrridePxPosition(position_px=120)
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        assert self._widget._axis_0_pos.get_final_px_position() == int(120)
        assert self.scan_2_metadata.get_abs_position_px(axis=0) == int(120)


class TestAxisOrderedTomoObjsModel(TestCaseQt):
    """
    test the behavior of the z ordered model used for stitching
    """

    def setUp(self):
        super().setUp()
        self._tmp_path = tempfile.mkdtemp()
        self.scans_with_pos_and_pixel_size = create_scans_z_series(
            os.path.join(self._tmp_path, "case1"),
            z_positions_m=(0.200, 0.205, 0.210),
            sample_pixel_size=0.001,
            raw_frame_width=100,
        )
        self.scans_with_pixel_size = create_scans_z_series(
            os.path.join(self._tmp_path, "case2"),
            z_positions_m=(None, None, None),
            sample_pixel_size=0.001,
            raw_frame_width=100,
        )
        self.scans_without_metadata = create_scans_z_series(
            os.path.join(self._tmp_path, "case3"),
            z_positions_m=(None, None, None),
            sample_pixel_size=None,
            raw_frame_width=100,
        )
        self._widget = qt.QTableView()
        self._widget.setModel(AxisOrderedTomoObjsModel(parent=self._widget, axis=0))

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        shutil.rmtree(self._tmp_path)

    def testWithMetadata(self):
        """
        make sure z ordering works in the best case scenario
        """
        first_expected_scan = (
            self.scans_with_pos_and_pixel_size[2].get_identifier().short_description()
        )
        # try giving it ordered
        for scan in self.scans_with_pos_and_pixel_size[::-1]:
            self._widget.model().addTomoObj(scan)
        assert (
            self._widget.model().data(
                self._widget.model().index(0, 1), qt.Qt.DisplayRole
            )
            == first_expected_scan
        )
        self._widget.model().clearTomoObjs()
        # try giving it ordered (but inverted)
        for scan in self.scans_with_pos_and_pixel_size:
            self._widget.model().addTomoObj(scan)
        assert (
            self._widget.model().data(
                self._widget.model().index(0, 1), qt.Qt.DisplayRole
            )
            == first_expected_scan
        )

    def testWithPixelSizeOnly(self):
        """
        make sure z ordering works when we are only aware about pixel size
        """
        for scan in self.scans_with_pixel_size[::-1]:
            self._widget.model().addTomoObj(scan)

        # try adding some metadata to object
        scans = self._widget.model()._objs
        scans = self._widget.model()._objs
        scans[0].stitching_metadata = StitchingMetadata(tomo_obj=scans[0])
        scans[1].stitching_metadata = QStitchingMetadata(tomo_obj=scans[1])

        scans[0].stitching_metadata._pos_as_m = (0.1, 1, 2)
        scans[1].stitching_metadata._pos_as_m = (-0.03, 1, 2)
        scans[2].stitching_metadata._pos_as_m = (0.23, 1, 2)

        self._widget.model().reorder_objs()
        self._widget.model().layoutChanged.emit()

        assert (
            self._widget.model().data(
                self._widget.model().index(0, 1), qt.Qt.DisplayRole
            )
            == scans[2].get_identifier().short_description()
        )
        assert (
            self._widget.model().data(
                self._widget.model().index(1, 1), qt.Qt.DisplayRole
            )
            == scans[0].get_identifier().short_description()
        )
        assert (
            self._widget.model().data(
                self._widget.model().index(2, 1), qt.Qt.DisplayRole
            )
            == scans[1].get_identifier().short_description()
        )

    def testWithoutMetadata(self):
        """
        make sure tomo obj are still displayed even if there is no metadata at all
        """
        for scan in self.scans_without_metadata[::-1]:
            self._widget.model().addTomoObj(scan)
        # try adding some metadata to object
        scans = self._widget.model()._objs
        scans[0].stitching_metadata = StitchingMetadata(tomo_obj=scans[0])
        scans[1].stitching_metadata = QStitchingMetadata(tomo_obj=scans[1])

        scans[0].stitching_metadata._pos_as_px = (12, None, 2)
        scans[1].stitching_metadata._pos_as_px = (-12, None, None)
        scans[2].stitching_metadata._pos_as_px = (9999, None, None)

        self._widget.model().reorder_objs()
        self._widget.model().layoutChanged.emit()

        assert (
            self._widget.model().data(
                self._widget.model().index(0, 1), qt.Qt.DisplayRole
            )
            == scans[2].get_identifier().short_description()
        )
        assert (
            self._widget.model().data(
                self._widget.model().index(1, 1), qt.Qt.DisplayRole
            )
            == scans[0].get_identifier().short_description()
        )
        assert (
            self._widget.model().data(
                self._widget.model().index(2, 1), qt.Qt.DisplayRole
            )
            == scans[1].get_identifier().short_description()
        )
