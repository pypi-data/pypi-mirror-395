# coding: utf-8
from __future__ import annotations

import os

import numpy
import pytest

from tomwer.core.process.reconstruction.nabu.castvolume import CastVolumeTask
from tomwer.core.process.reconstruction.output import NabuOutputFileFormat
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.volume.tiffvolume import TIFFVolume


def test_cast_volume_32bitstiff_to_16bits_tiff(tmp_path):
    """test 32 bits tiffs to 16 bits works"""
    dir_test = tmp_path / "test_dir"
    dir_test.mkdir()
    save_dir = tmp_path / "output_dir"
    save_dir.mkdir()

    vol_data = numpy.random.random(20 * 100 * 100) * 3600.4
    vol_data = vol_data.reshape(20, 100, 100)
    vol_data = vol_data.astype(numpy.float32)
    volume = TIFFVolume(
        folder=dir_test,
        volume_basename="test_dir_vol_",
        data=vol_data,
    )
    volume.save()

    # test with output datadir as None
    with pytest.raises(ValueError):
        CastVolumeTask(
            inputs={
                "volume": volume,
                "configuration": {
                    "output_file_path": None,
                    "output_file_format": NabuOutputFileFormat.EDF,
                    "output_data_type": numpy.uint16,
                },
            },
        ).run()

    # test providing save dir and tiff
    assert len(os.listdir(save_dir)) == 0
    task = CastVolumeTask(
        inputs={
            "volume": volume,
            "configuration": {
                "output_dir": str(save_dir),
                "output_file_format": NabuOutputFileFormat.EDF,
                "output_data_type": numpy.uint16,
            },
        }
    )
    task.run()

    assert len(os.listdir(save_dir)) == 20, "no files have been generated"
    assert task.outputs.volume.load_data().shape == (20, 100, 100)
    assert task.outputs.volume.load_data().dtype == numpy.uint16

    # test providing save dir, a scan and hdf5
    scan = NXtomoScan(scan=os.sep.join([str(tmp_path), "scan"]), entry="entry0000")
    task = CastVolumeTask(
        inputs={
            "volume": volume,
            "configuration": {
                "output_dir": str(save_dir),
                "output_file_format": NabuOutputFileFormat.HDF5,
                "output_data_type": numpy.float32,
            },
            "scan": scan,
        },
    )
    task.run()
    assert task.outputs.volume.load_data().shape == (20, 100, 100)
    assert task.outputs.volume.load_data().dtype == numpy.float32

    # test providing a volume as output volume
    output_volume = HDF5Volume(
        file_path=os.path.join(str(tmp_path), "my_volume.hdf5"), data_path="entry0002"
    )
    task = CastVolumeTask(
        inputs={
            "volume": volume,
            "configuration": {
                "output_dir": str(save_dir),
                "output_file_format": NabuOutputFileFormat.HDF5,
                "output_data_type": numpy.uint8,
            },
            "output_volume": output_volume,
        },
    )
    task.run()
    assert task.outputs.volume.load_data().shape == (20, 100, 100)
    assert task.outputs.volume.load_data().dtype == numpy.uint8

    # test providing a volume us as output volume
    output_volume = EDFVolume(folder=os.path.join(str(tmp_path), "my_edf_vol"))
    task = CastVolumeTask(
        inputs={
            "volume": volume,
            "configuration": {
                "output_dir": str(save_dir),
                "output_file_format": NabuOutputFileFormat.HDF5,
                "output_data_type": numpy.int16,
                "remove_input_volume": True,
            },
            "output_volume": output_volume.get_identifier().to_str(),
        },
    )
    task.run()
    assert task.outputs.volume.load_data().shape == (20, 100, 100)
    assert task.outputs.volume.load_data().dtype == numpy.int16
    assert not os.path.exists(volume.data_url.file_path())
