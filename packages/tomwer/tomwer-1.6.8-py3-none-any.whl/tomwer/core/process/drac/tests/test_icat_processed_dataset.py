from __future__ import annotations

import os
import pytest
import numpy

from tomwer.core.process.drac.processeddataset import DracReconstructedVolumeDataset
from tomwer.tests.conftest import nxtomo_scan_180  # noqa F811
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.volume.edfvolume import EDFVolume


@pytest.mark.parametrize(
    "output_dir_use_case", ("default", "change_name", "change_dir")
)
@pytest.mark.parametrize("MetaVolumeClass", (HDF5Volume, EDFVolume))
def test_IcatReconstructedVolumeDataset(
    output_dir_use_case: str, nxtomo_scan_180, MetaVolumeClass, tmp_path  # noqa F811
):

    if output_dir_use_case == "default":
        output_dir = os.path.join(
            os.path.dirname(nxtomo_scan_180.master_file), "reconstructed_volumes"
        )
    elif output_dir_use_case == "change_name":
        output_dir = os.path.join(
            os.path.dirname(nxtomo_scan_180.master_file), "my_vols"
        )
    elif output_dir_use_case == "change_dir":
        output_dir = tmp_path / "test" / "reconstructed_volumes"
        output_dir.mkdir(parents=True)

    if MetaVolumeClass is HDF5Volume:
        volume = MetaVolumeClass(
            file_path=os.path.join(output_dir, "test.hdf5"),
            data_path="data",
        )
    elif MetaVolumeClass is EDFVolume:
        volume = MetaVolumeClass(folder=os.path.join(output_dir, "folder"))
    else:
        raise NotImplementedError
    volume.data = numpy.random.random((10, 10, 10))
    volume.save()

    icat_dataset = DracReconstructedVolumeDataset(
        tomo_obj=volume, source_scan=nxtomo_scan_180
    )
    gallery_dir = icat_dataset.get_gallery_dir()
    assert gallery_dir == os.path.join(output_dir, "gallery")
    assert not os.path.exists(gallery_dir)
    assert icat_dataset.get_slices_to_extract() == (
        (0, 2),
        (0, 5),
        (0, 8),
        (1, 2),
        (1, 5),
        (1, 8),
        (2, 2),
        (2, 5),
        (2, 8),
    )
    icat_dataset.build_gallery()
    assert os.path.exists(gallery_dir)
    # make sure we have three slice over each direction
    assert len(os.listdir(gallery_dir)) == 3
    assert "XY" in os.listdir(gallery_dir)
    if MetaVolumeClass is HDF5Volume:
        assert "test_capture_XY_000008.png" in os.listdir(
            os.path.join(gallery_dir, "XY")
        )
        assert "test_capture_YZ_000002.png" in os.listdir(
            os.path.join(gallery_dir, "YZ")
        )
    elif MetaVolumeClass is EDFVolume:
        assert "folder_capture_XY_000008.png" in os.listdir(
            os.path.join(gallery_dir, "XY")
        )
        assert "folder_capture_YZ_000002.png" in os.listdir(
            os.path.join(gallery_dir, "YZ")
        )
