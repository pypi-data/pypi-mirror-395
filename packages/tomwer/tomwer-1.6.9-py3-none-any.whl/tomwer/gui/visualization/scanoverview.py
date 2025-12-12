# coding: utf-8
from __future__ import annotations


import logging
import weakref

from silx.gui import qt
from nxtomo.nxobject.nxdetector import FOV

from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.char import DEGREE_CHAR

_logger = logging.getLogger(__name__)


class ScanOverviewWidget(qt.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scan = None
        self.setLayout(qt.QVBoxLayout())
        self._tree = qt.QTreeWidget(self)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("entry", "value"))
        self.layout().addWidget(self._tree)

        # 1: define instrument
        self._instrument = qt.QTreeWidgetItem(self._tree)
        self._instrument.setText(0, "instrument")
        # 1.1 define beam
        self._beam = qt.QTreeWidgetItem(self._instrument)
        self._beam.setText(0, "beam")
        self._energy = qt.QTreeWidgetItem(self._beam)
        self._energy.setText(0, "energy")
        # 1.1 define detector
        self._frames = qt.QTreeWidgetItem(self._instrument)
        self._frames.setText(0, "frames")
        self._projections = qt.QTreeWidgetItem(self._frames)
        self._projections.setText(0, "projections")
        self._darks = qt.QTreeWidgetItem(self._frames)
        self._darks.setText(0, "darks")
        self._flats = qt.QTreeWidgetItem(self._frames)
        self._flats.setText(0, "flats")
        self._alignments = qt.QTreeWidgetItem(self._frames)
        self._alignments.setText(0, "alignments")
        self._estimatedCOR = qt.QTreeWidgetItem(self._frames)
        self._estimatedCOR.setText(0, "estimated cor")

        self._detector_x_pixel_size = qt.QTreeWidgetItem(self._instrument)
        self._detector_x_pixel_size.setText(0, "x pixel size")
        self._detector_y_pixel_size = qt.QTreeWidgetItem(self._instrument)
        self._detector_y_pixel_size.setText(0, "y pixel size")

        # 2: define sample
        self._sample = qt.QTreeWidgetItem(self._tree)
        self._sample.setText(0, "sample")
        self._sample_name = qt.QTreeWidgetItem(self._sample)
        self._sample_name.setText(0, "name")

        self._sample_x_pixel_size = qt.QTreeWidgetItem(self._sample)
        self._sample_x_pixel_size.setText(0, "x pixel size")
        self._sample_y_pixel_size = qt.QTreeWidgetItem(self._sample)
        self._sample_y_pixel_size.setText(0, "y pixel size")

        # 3: other hight level items
        self._startTime = qt.QTreeWidgetItem(self._tree)
        self._startTime.setText(0, "start_time")
        self._endTime = qt.QTreeWidgetItem(self._tree)
        self._endTime.setText(0, "end_time")
        self._title = qt.QTreeWidgetItem(self._tree)
        self._title.setText(0, "title")
        self._scanRangeQLE = qt.QTreeWidgetItem(self._tree)
        self._scanRangeQLE.setText(0, "scan range")

        # set up
        self._instrument.setExpanded(True)
        self._frames.setExpanded(True)
        self._sample.setExpanded(True)
        self._beam.setExpanded(True)

    def setScan(self, scan):
        if scan is None:
            self._scan = scan
        elif not isinstance(scan, TomwerScanBase):
            raise TypeError(f"{scan} is expected to be an instance of {TomwerScanBase}")
        else:
            self._scan = weakref.ref(scan)
        if scan is not None:
            self.update_tree(scan=scan)

    def getScan(self):
        if self._scan is None or self._scan() is None:
            return None
        else:
            return self._scan()

    def update_tree(self, scan: TomwerScanBase):
        parts = {
            "instrument": self._updateInstrument,
            "times": self._updateTimes,
            "names": self._updateNames,
            "scan-range": self._updateScanRange,
            "sample": self._updateSample,
        }
        for part_name, fct in parts.items():
            try:
                fct(scan=scan)
            except Exception:
                _logger.error(f"Failed to update '{part_name}'.", stack_info=True)
        self._tree.resizeColumnToContents(0)

    def _updateInstrument(self, scan: TomwerScanBase):
        self._updateFrames(scan=scan)
        self._updateEnergy(scan=scan)
        self._updateDetectorPixelSize(scan=scan)

    def _setColoredTxt(
        self, item, text, column=1, hightlight_red=False, hightlight_orange=False
    ):
        if text in (None, str(None)):
            text = "?"
        if hightlight_red:
            bkg_color = qt.QColor(220, 0, 0, 200)
        elif hightlight_orange:
            bkg_color = qt.QColor(200, 160, 0, 150)
        else:
            bkg_color = qt.QColor(0, 220, 0, 50)

        item.setText(column, text)
        item.setBackground(0, qt.QBrush(bkg_color))

    def _updateSample(self, scan: TomwerScanBase):
        x_pixel_size = scan.sample_x_pixel_size
        y_pixel_size = scan.sample_y_pixel_size
        self._setColoredTxt(
            item=self._sample_x_pixel_size,
            text=f"{x_pixel_size} (m)",
            hightlight_red=x_pixel_size in (None, 0.0, 1.0),
        )
        self._setColoredTxt(
            item=self._sample_y_pixel_size,
            text=f"{y_pixel_size} (m)",
            hightlight_red=y_pixel_size in (None, 0.0, 1.0),
        )

    def _updateTimes(self, scan: TomwerScanBase):
        self._startTime.setText(1, str(scan.start_time))
        self._endTime.setText(1, str(scan.end_time))

    def _updateFrames(self, scan: TomwerScanBase):
        assert isinstance(scan, TomwerScanBase)
        # frames
        n_frames = len(scan.frames)
        self._setColoredTxt(
            item=self._frames,
            text=str(n_frames),
            hightlight_red=(n_frames in (0, None)),
        )
        # projections
        n_proj = len(scan.projections)
        self._setColoredTxt(
            item=self._projections,
            text=str(n_proj),
            hightlight_red=(n_proj in (0, None)),
        )
        # darks
        n_darks = len(scan.darks)
        self._setColoredTxt(
            item=self._darks,
            text=str(n_darks),
            hightlight_red=(n_darks in (0, None)),
        )

        # flats
        n_flats = len(scan.flats)
        self._setColoredTxt(
            item=self._flats,
            text=str(n_flats),
            hightlight_red=(n_flats in (0, None)),
        )
        # align
        n_alignment = len(scan.alignment_projections)
        self._setColoredTxt(
            item=self._alignments,
            text=str(n_alignment),
        )

        if scan.field_of_view == FOV.HALF:
            if scan.x_rotation_axis_pixel_position is None:
                self._estimatedCOR.setText(1, "???")
            else:
                self._estimatedCOR.setText(1, str(scan.x_rotation_axis_pixel_position))
        else:
            self._estimatedCOR.setText(1, "only for half")

    def _updateEnergy(self, scan: TomwerScanBase):
        assert isinstance(scan, TomwerScanBase)
        energy = scan.energy
        self._setColoredTxt(
            item=self._energy,
            text=f"{energy} (kev)",
            hightlight_red=energy in (0, None),
        )

    def _updateNames(self, scan: TomwerScanBase):
        assert isinstance(scan, TomwerScanBase)
        sample_name = scan.sample_name
        sequence_name = scan.sequence_name
        self._title.setText(1, sequence_name)
        self._sample_name.setText(1, sample_name)

    def _updateTomoN(self, scan: TomwerScanBase):
        assert isinstance(scan, TomwerScanBase)
        tomo_n = scan.tomo_n
        self._setColoredTxt(
            item=self._tomoNQLE,
            text=str(tomo_n),
        )

    def _updateScanRange(self, scan: TomwerScanBase):
        assert isinstance(scan, TomwerScanBase)
        scan_range = scan.scan_range
        if scan_range is None:
            scan_range = "???"
        else:
            scan_range = f"{scan_range}{DEGREE_CHAR}"
        self._setColoredTxt(
            item=self._scanRangeQLE,
            text=str(scan_range),
        )

    def _updateDetectorPixelSize(self, scan: TomwerScanBase):
        assert isinstance(scan, TomwerScanBase)
        if isinstance(scan, EDFTomoScan):
            x_pixel_size = y_pixel_size = scan.pixel_size
        else:
            x_pixel_size = scan.detector_x_pixel_size
            y_pixel_size = scan.detector_y_pixel_size
        self._setColoredTxt(
            item=self._detector_x_pixel_size,
            text=f"{x_pixel_size} (m)",
            hightlight_red=x_pixel_size in (None, 0.0, 1.0),
        )
        self._setColoredTxt(
            item=self._detector_y_pixel_size,
            text=f"{y_pixel_size} (m)",
            hightlight_red=y_pixel_size in (None, 0.0, 1.0),
        )

    def clear(self):
        self._tree.clear()
