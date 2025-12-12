# coding: utf-8
"""
contains utils for inputs and outputs
"""

from __future__ import annotations

import os

import h5py
import numpy
from silx.io.url import DataUrl
from tomoscan.io import HDF5File

from tomwer.core.utils import scanutils
from tomwer.io.utils import (
    get_default_directory,
    get_linked_files_with_entry,
    get_slice_data,
)


def test_get_linked_files_with_entry(tmp_path):
    """test get_linked_files_with_entry function"""
    dir_test = tmp_path / "sub"
    dir_test.mkdir()

    layout = h5py.VirtualLayout(shape=(4, 10, 10), dtype="i4")
    for i_file in range(4):
        file_name = os.path.join(dir_test, f"file_{i_file}.hdf5")
        with HDF5File(file_name, "w") as h5s:
            h5s.create_dataset("data", (10, 10), "i4", numpy.ones((10, 10)))
            vsource = h5py.VirtualSource(file_name, "data", shape=(10, 10))
            layout[i_file] = vsource

    test_with_vds = os.path.join(dir_test, "file_with_vds")
    with HDF5File(test_with_vds, "w") as h5s:
        h5s.create_virtual_dataset("vdata", layout, fillvalue=-1)

    assert len(get_linked_files_with_entry(test_with_vds, "vdata")) == 4


def test_get_default_directory():
    get_default_directory()


def test_get_slice_data_vol(tmp_path):
    """test load of a .vol file"""
    dir_test = tmp_path / "test_vol"
    dir_test.mkdir()
    vol_file_path = os.path.join(dir_test, "volume.vol")
    vol_info_file_path = os.path.join(dir_test, "volume.vol.info")

    shape = (4, 50, 20)
    data = numpy.ones(shape)
    data.astype(numpy.float32).tofile(vol_file_path)
    scanutils.MockEDF._createVolInfoFile(
        filePath=vol_info_file_path,
        shape=shape,
    )

    vol = get_slice_data(DataUrl(file_path=vol_file_path))
    assert vol is not None
    assert vol.shape == shape
    vol = get_slice_data(DataUrl(file_path=vol_info_file_path))
    assert vol is not None
    assert vol.shape == shape
