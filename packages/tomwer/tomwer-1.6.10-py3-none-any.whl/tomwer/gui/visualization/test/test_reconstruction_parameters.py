# coding: utf-8
from __future__ import annotations


import pytest
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.gui.visualization.reconstructionparameters import ReconstructionParameters

from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.parametrize("phase_method", ("", "CTF", "Paganin"))
def test_ReconstructionParameters(qtapp, phase_method):  # noqa F401
    window = ReconstructionParameters()
    volume = HDF5Volume(
        file_path="test.hdf5",
        data_path="data",
        data=None,
        metadata={
            "nabu_config": {
                "reconstruction": {
                    "method": "FBP",
                },
                "phase": {
                    "method": phase_method,
                    "delta_beta": 110.0,
                },
            },
            "processing_options": {
                "reconstruction": {
                    "voxel_size_cm": (0.2, 0.2, 0.2),
                    "rotation_axis_position": 104,
                    "enable_halftomo": True,
                    "fbp_filter_type": "Hilbert",
                    "sample_detector_dist": 0.4,
                },
                "take_log": {
                    "log_min_clip": 1.0,
                    "log_max_clip": 10.0,
                },
            },
        },
    )
    window.setVolumeMetadata(metadata=volume.metadata)

    assert window._methodQLE.text() == "FBP"
    assert window._paganinQLE.text() == phase_method
    assert window._deltaBetaQLE.text() == "110.0"
    assert window._sampleDetectorDistanceInMeterQLE.text() == "0.004"
    assert window._voxelSizeInMicronQLE.text() == "2e+03x2e+03x2e+03"
    assert window._corQLE.text() == "104.00"
    assert window._halfTomoCB.isChecked()
    assert window._fbpFilterQLE.text() == "Hilbert"
    assert window._minLogClipQLE.text() == "1.0"
    assert window._maxLogClipQLE.text() == "10.0"

    window.setVolumeMetadata(metadata=None)
