from __future__ import annotations

import os
import numpy
import pytest

from tomwer.core.volume.tiffvolume import TIFFVolume

from tomoscan.esrf.volume.tiffvolume import has_tifffile
from tomoscan.volumebase import VolumeBase, SliceTuple

from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.tasks.visualization.volume_viewer import VolumeViewerTask


volume_constructors = [
    EDFVolume,
    HDF5Volume,
]
if has_tifffile:
    volume_constructors.append(TIFFVolume)


@pytest.mark.parametrize("volume_input_as", (VolumeBase, str))
@pytest.mark.parametrize("volume_constructor", volume_constructors)
def test_volume_viewer(tmp_path, volume_constructor, volume_input_as):
    volume_data = numpy.ones((10, 20, 30))
    volume_metadata = {
        "nabu_config": {
            "reconstruction": {
                "method": "FBP",
            },
            "phase": {
                "method": "paganin",
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
    }
    if volume_constructor is HDF5Volume:
        volume = HDF5Volume(
            data=volume_data,
            metadata=volume_metadata,
            file_path=os.path.join(tmp_path, "output_file.h5"),
            data_path="my_volume",
        )
    else:
        vol_basename = "my_vol"
        volume = volume_constructor(
            data=volume_data,
            metadata=volume_metadata,
            folder=os.path.join(tmp_path, vol_basename),
            volume_basename=vol_basename,
        )
    volume.save()

    if volume_input_as is VolumeBase:
        input_volume = volume
    elif volume_input_as is str:
        input_volume = volume.get_identifier().to_str()
    else:
        raise TypeError(f"'volume_input_as' should be [{str}, {VolumeBase}]")

    task = VolumeViewerTask(
        inputs={
            "volume": input_volume,
            "load_volume": True,
        }
    )
    task.execute()

    slices = task.get_output_value("slices")
    assert len(slices) == 9
    for slice_ in slices:
        assert isinstance(slice_, SliceTuple)
    assert isinstance(task.get_output_value("volume_metadata"), dict)
    loaded_volume = task.get_output_value("loaded_volume")
    assert isinstance(loaded_volume.data, numpy.ndarray)
