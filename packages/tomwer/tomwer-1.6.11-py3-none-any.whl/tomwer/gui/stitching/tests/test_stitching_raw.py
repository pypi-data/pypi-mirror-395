import os
import shutil
import tempfile

import numpy

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.gui.stitching.metadataholder import QStitchingMetadata
from tomwer.gui.stitching.stitching_raw import RawStitchingPlot, AlphaValuesTableWidget


def _createVolumes(axis_0_positions: tuple, root_dir: str):
    volumes = []
    for i_volume, axis_0_position in enumerate(axis_0_positions):
        data = numpy.random.random(20 * 20).reshape(1, 20, 20)
        volume = HDF5Volume(
            file_path=os.path.join(root_dir, f"volume_{i_volume}.hdf5"),
            data_path=f"entry_{i_volume}",
            data=data,
        )
        volume.stitching_metadata = QStitchingMetadata(tomo_obj=volume)
        volume.stitching_metadata.setPxPos(axis=0, value=axis_0_position)
        volumes.append(volume)
    return volumes


def _createScans(axis_0_positions: tuple, root_dir: str):
    scans = []
    for i_scan, axis_0_position in enumerate(axis_0_positions):
        scan = MockNXtomo(
            scan_path=os.path.join(root_dir, f"scan_{i_scan}"),
            n_proj=20,
            n_ini_proj=20,
            dim=10,
        ).scan
        scan.stitching_metadata = QStitchingMetadata(tomo_obj=scan)
        scan.stitching_metadata.setPxPos(axis=0, value=axis_0_position)
        scans.append(scan)
    return scans


class TestPlotRawStitching(TestCaseQt):
    """Test RawStitchingPlot widget"""

    def setUp(self):
        super().setUp()
        self._tmp_path = tempfile.mkdtemp()
        self.widget = RawStitchingPlot(alpha_values=True)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self._tmp_path)

    def testWithVolumes(self):
        axis_0_positions = (0, 12, 50)
        volumes = _createVolumes(
            axis_0_positions=axis_0_positions, root_dir=self._tmp_path
        )
        assert len(volumes) == 3
        self.widget.addTomoObj(volumes[0])
        images = self.widget.getAllImages()
        assert len(images) == 1

        self.widget.setTomoObjs(volumes)
        images = self.widget.getAllImages()
        assert len(images) == len(volumes)
        # silx is storing origins as x, y
        origins = tuple([image.getOrigin()[1] for image in images])
        assert tuple(sorted(origins)) == axis_0_positions

    def testWithScans(self):
        axis_0_positions = (0, 10, 20, 34)
        scans = _createScans(axis_0_positions=axis_0_positions, root_dir=self._tmp_path)
        self.widget.setActive(False)
        self.widget.setTomoObjs(scans)
        assert len(self.widget.getAllImages()) == 0
        self.widget.setActive(True)
        self.qapp.processEvents()
        assert len(self.widget.getAllImages()) == len(scans)


class TestAlphaValuesTableWidget(TestCaseQt):
    """test AlphaValuesTableWidget"""

    def setUp(self):
        super().setUp()
        self._tmp_path = tempfile.mkdtemp()
        self.widget = AlphaValuesTableWidget()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self._tmp_path)

    def testSettingTomoObj(self):
        self.widget.setTomoObjs(
            _createVolumes(axis_0_positions=(0, 12, 50), root_dir=self._tmp_path),
        )

        assert len(self.widget._sliders) == 3
        self.widget.setTomoObjs(
            _createScans(axis_0_positions=(89, 78), root_dir=self._tmp_path)
        )
        assert len(self.widget._sliders) == 2
