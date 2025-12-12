import os
import pickle
import shutil
import tempfile

import numpy

from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.stitching.ZStitchingConfigOW import ZStitchingConfigOW
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.core.volume.hdf5volume import HDF5Volume


class TestScansZStitchingConfigOW(TestCaseQt):
    """
    Test stitching with scans
    """

    def setUp(self):
        super().setUp()
        self._widget = ZStitchingConfigOW()
        self._tmp_dir = tempfile.mkdtemp()
        self._scans = []
        for i_scan in range(3):
            scan = MockNXtomo(
                scan_path=os.path.join(self._tmp_dir, f"scan_{i_scan}.nx"),
                n_ini_proj=20,
                n_proj=20,
                n_alignement_proj=2,
                dim=10,
            ).scan
            self._scans.append(scan)
        self._widget.setConfiguration(
            {
                "inputs": {
                    "input_datasets": [
                        scan.get_identifier().to_str() for scan in self._scans
                    ],
                },
                "stitching": {
                    "type": "z-preproc",
                    "stitching_strategy": "closest",
                    "alignment_axis_1": "center",
                    "alignment_axis_2": "center",
                    "pad_mode": "constant",
                },
                "preproc": {
                    "data_path": "myentry",
                    "location": "/path/to/mynexusfile.nx",
                },
            }
        )
        self.qapp.processEvents()

    def test_get_configuration(self):
        """Make sure the set configuration will be the get configuration"""
        config = self._widget.getConfiguration()
        assert config == {
            "inputs": {
                "input_datasets": list(
                    [scan.get_identifier().to_str() for scan in self._scans]
                ),
                "slices": "",
            },
            "stitching": {
                "stitching_strategy": "cosinus weights",
                "type": "z-preproc",
                "axis_0_pos_px": [0] * len(self._scans),
                "axis_0_params": "overlap_size=;img_reg_method=nabu-fft;window_size=400",
                "axis_1_pos_px": [0] * len(self._scans),
                "axis_1_params": "img_reg_method=None;window_size=400",
                "flipud": False,
                "fliplr": False,
                "avoid_data_duplication": False,
                "rescale_frames": False,
                "rescale_params": "rescale_min_percentile=0;rescale_max_percentile=100",
                "alignment_axis_1": "center",
                "alignment_axis_2": "center",
                "pad_mode": "constant",
            },
            "preproc": {
                "data_path": "myentry",
                "location": "/path/to/mynexusfile.nx",
            },
            "output": {
                "overwrite_results": True,
            },
            "normalization_by_sample": {
                "active": False,
                "margin": 0,
                "method": "median",
                "side": "left",
                "width": 30,
            },
        }
        # test setting some metadata for stitching
        for i_scan, scan in enumerate(
            self._widget.widget._widget._mainWidget.getTomoObjs()
        ):
            scan.stitching_metadata.setPxPos(-i_scan, axis=0)
            scan.stitching_metadata.setPxPos(-i_scan * 10, axis=1)
        self.qapp.processEvents()
        config = self._widget.getConfiguration()
        assert config == {
            "inputs": {
                "input_datasets": list(
                    [scan.get_identifier().to_str() for scan in self._scans]
                ),
                "slices": "",
            },
            "stitching": {
                "type": "z-preproc",
                "stitching_strategy": "cosinus weights",
                "axis_0_pos_px": [0, -1, -2],
                "axis_0_params": "overlap_size=;img_reg_method=nabu-fft;window_size=400",
                "axis_1_pos_px": [0, -10, -20],
                "axis_1_params": "img_reg_method=None;window_size=400",
                "flipud": False,
                "fliplr": False,
                "avoid_data_duplication": False,
                "rescale_frames": False,
                "rescale_params": "rescale_min_percentile=0;rescale_max_percentile=100",
                "alignment_axis_1": "center",
                "alignment_axis_2": "center",
                "pad_mode": "constant",
            },
            "preproc": {
                "data_path": "myentry",
                "location": "/path/to/mynexusfile.nx",
            },
            "output": {
                "overwrite_results": True,
            },
            "normalization_by_sample": {
                "active": False,
                "margin": 0,
                "method": "median",
                "side": "left",
                "width": 30,
            },
        }
        config["stitching"]["axis_1_pos_px"] = [0, -1, -2]
        config["output"]["overwrite_results"] = False
        self._widget.setConfiguration(config)
        assert self._widget.getConfiguration() == config

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        shutil.rmtree(self._tmp_dir)

    def test_serializing(self):
        pickle.dumps(self._widget.getConfiguration())

    def test_literal_dumps(self):
        literal_dumps(self._widget.getConfiguration())


class TestVolumesZStitchingConfigOW(TestCaseQt):
    """
    Test ZStitchingConfigOW with volumes
    """

    def setUp(self):
        super().setUp()
        self._widget = ZStitchingConfigOW()
        self._tmp_dir = tempfile.mkdtemp()
        self._volumes = []
        for i_volumes in range(4):
            volume = HDF5Volume(
                file_path=os.path.join(self._tmp_dir, f"volume_{i_volumes}.hdf5"),
                data_path="entry0000",
                data=numpy.ones(shape=(10, 20, 30)),
                metadata={},
            )
            volume.save()
            self._volumes.append(volume)

        self.output_volume = HDF5Volume(
            file_path=os.path.join(self._tmp_dir, "result.hdf5"),
            data_path="stitched",
        )
        self._widget.setConfiguration(
            {
                "inputs": {
                    "input_datasets": [
                        volume.get_identifier().to_str() for volume in self._volumes
                    ],
                },
                "stitching": {
                    "type": "z-postproc",
                    "stitching_strategy": "closest",
                    "alignment_axis_1": "center",
                    "alignment_axis_2": "center",
                    "pad_mode": "constant",
                },
                "postproc": {
                    "output_volume": self.output_volume.get_identifier().to_str(),
                },
            }
        )
        self.qapp.processEvents()

    def test_get_configuration(self):
        """Make sure the set configuration will be the get configuration"""
        config = self._widget.getConfiguration()
        assert config == {
            "inputs": {
                "input_datasets": list(
                    [scan.get_identifier().to_str() for scan in self._volumes]
                ),
                "slices": "",
            },
            "stitching": {
                "stitching_strategy": "cosinus weights",
                "type": "z-postproc",
                "axis_0_pos_px": [0] * len(self._volumes),
                "axis_0_params": "overlap_size=;img_reg_method=nabu-fft;window_size=400",
                "axis_1_pos_px": [0] * len(self._volumes),
                "axis_1_params": "img_reg_method=None;window_size=400",
                "flipud": False,
                "fliplr": False,
                "avoid_data_duplication": False,
                "rescale_frames": False,
                "rescale_params": "rescale_min_percentile=0;rescale_max_percentile=100",
                "alignment_axis_1": "center",
                "alignment_axis_2": "center",
                "pad_mode": "constant",
            },
            "postproc": {
                "output_volume": self.output_volume.get_identifier().to_str(),
            },
            "output": {
                "overwrite_results": True,
            },
            "normalization_by_sample": {
                "active": False,
                "margin": 0,
                "method": "median",
                "side": "left",
                "width": 30,
            },
        }
        # test setting some metadata for stitching
        for i_scan, scan in enumerate(
            self._widget.widget._widget._mainWidget.getTomoObjs()
        ):
            scan.stitching_metadata.setPxPos(-i_scan, axis=0)
            scan.stitching_metadata.setPxPos(-i_scan * 10, axis=1)
        self.qapp.processEvents()
        config = self._widget.getConfiguration()
        assert config == {
            "inputs": {
                "input_datasets": list(
                    [scan.get_identifier().to_str() for scan in self._volumes]
                ),
                "slices": "",
            },
            "stitching": {
                "stitching_strategy": "cosinus weights",
                "type": "z-postproc",
                "axis_0_pos_px": [0, -1, -2, -3],
                "axis_0_params": "overlap_size=;img_reg_method=nabu-fft;window_size=400",
                "axis_1_pos_px": [0, -10, -20, -30],
                "axis_1_params": "img_reg_method=None;window_size=400",
                "flipud": False,
                "fliplr": False,
                "avoid_data_duplication": False,
                "rescale_frames": False,
                "rescale_params": "rescale_min_percentile=0;rescale_max_percentile=100",
                "alignment_axis_1": "center",
                "alignment_axis_2": "center",
                "pad_mode": "constant",
            },
            "postproc": {
                "output_volume": self.output_volume.get_identifier().to_str(),
            },
            "output": {
                "overwrite_results": True,
            },
            "normalization_by_sample": {
                "active": False,
                "margin": 0,
                "method": "median",
                "side": "left",
                "width": 30,
            },
        }
        # update some field to enhance test
        config["stitching"]["axis_1_pos_px"] = [0, -100, -200, -300]
        config["stitching"]["rescale_frames"] = True
        config["stitching"][
            "rescale_params"
        ] = "rescale_min_percentile=10;rescale_max_percentile=35"
        config["output"]["overwrite_results"] = False
        self._widget.setConfiguration(config)
        assert self._widget.getConfiguration() == config

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        shutil.rmtree(self._tmp_dir)

    def test_serializing(self):
        pickle.dumps(self._widget.getConfiguration())

    def test_literal_dumps(self):
        literal_dumps(self._widget.getConfiguration())
