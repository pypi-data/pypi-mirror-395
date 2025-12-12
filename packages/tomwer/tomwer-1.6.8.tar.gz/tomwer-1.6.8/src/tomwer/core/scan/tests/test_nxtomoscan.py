import os
import shutil
import numpy

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.tests.datasets import TomwerCIDatasets
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_RECONSTRUCTED_SLICES,
)
from nxtomomill.converter.hdf5.utils import PROCESSED_DATA_DIR_NAME, RAW_DATA_DIR_NAME


def test_scan_dir(tmp_path):
    """test result of NxtomoScan.scan_dir_name is correct"""
    tmp_dir = tmp_path / "frm_edftomomill_twoentries_dataset"
    tmp_dir.mkdir()
    tmp_dir = str(tmp_dir)
    dataset_file = os.path.join(tmp_dir, "frm_edftomomill_twoentries.nx")
    shutil.copyfile(
        TomwerCIDatasets.get_dataset(
            "h5_datasets/frm_edftomomill_twoentries.nx",
        ),
        dataset_file,
    )
    assert os.path.isfile(dataset_file)
    scan = NXtomoScan(scan=dataset_file, entry="entry0000")
    assert scan.scan_dir_name() == tmp_dir.split(os.sep)[-1]


def test_flat_field_interval(tmp_path):
    """test the call to ff_interval"""
    tmp_dir = tmp_path / "test_flat_field_interval"
    scan_path = os.path.join(tmp_dir, "my_scan_1")
    scan_1 = MockNXtomo(
        scan_path=scan_path,
        n_ini_proj=20,
        n_proj=20,
        n_alignement_proj=2,
        create_final_flat=True,
        create_ini_dark=True,
        create_ini_flat=True,
        n_refs=5,
    ).scan
    numpy.testing.assert_equal(scan_1.ff_interval, 20)

    scan_path2 = os.path.join(tmp_dir, "my_scan_2")
    scan_2 = MockNXtomo(
        scan_path=scan_path2,
        n_ini_proj=10,
        n_proj=10,
        n_alignement_proj=2,
        create_final_flat=False,
        create_ini_dark=True,
        create_ini_flat=True,
        n_refs=1,
    ).scan
    numpy.testing.assert_equal(scan_2.ff_interval, 0)


def test_working_directory():
    """test behavior of the working directory function"""
    scan = NXtomoScan(scan=None, entry="my_entry")
    assert scan.working_directory is None
    scan = NXtomoScan(scan="/full/path/my_file.sh", entry="my_entry")
    assert str(scan.working_directory) == os.path.abspath("/full/path")
    scan = NXtomoScan(scan="my_file.sh", entry="my_entry")
    assert str(scan.working_directory) == os.path.abspath(".")


def test_get_reconstructions_slices(tmp_path):
    """test NXtomoscan.get_reconstruction_urls and make sure all related scan can be found from a scan
    (as long as they are stored at a 'searched' location)
    """
    test_dir = tmp_path / "test_get_reconstructions_urls"
    test_dir.mkdir()
    raw_data_dir = test_dir / RAW_DATA_DIR_NAME / "frm_edftomomill_twoentries"
    raw_data_dir.mkdir(parents=True)
    processed_data_dir = (
        test_dir / PROCESSED_DATA_DIR_NAME / "frm_edftomomill_twoentries"
    )
    processed_data_dir.mkdir(parents=True)
    third_path_dir = test_dir / "third_part"
    third_path_dir.mkdir(parents=True)

    output_file_path = os.path.join(raw_data_dir, "frm_edftomomill_twoentries.nx")
    shutil.copyfile(
        TomwerCIDatasets.get_dataset(
            "h5_datasets/frm_edftomomill_twoentries.nx",
        ),
        output_file_path,
    )
    scan = NXtomoScan(
        scan=output_file_path,
        entry="entry0000",
    )
    assert str(scan.working_directory) == str(raw_data_dir)
    assert os.path.exists(output_file_path)

    # create a edf volume in PROCESSED_DATA
    data = numpy.linspace(start=0, stop=100, num=100).reshape(  # pylint: disable=E1121
        1, 10, 10
    )
    edf_volume = EDFVolume(
        folder=os.path.join(
            raw_data_dir,
            PROCESS_FOLDER_RECONSTRUCTED_SLICES,
        ),
        volume_basename="frm_edftomomill_twoentries_slice",
        data=data,
    )
    edf_volume.save()

    # create an hdf5 volume in RAW_DATA
    hdf5_volume = HDF5Volume(
        file_path=os.path.join(
            processed_data_dir,
            PROCESS_FOLDER_RECONSTRUCTED_SLICES,
            "frm_edftomomill_twoentries_slice.h5",
        ),
        data_path="/entry0000",
        data=data,
    )
    hdf5_volume.save()

    # create a third hdf5 volume in 'third_part_dir'
    third_part_volume = HDF5Volume(
        file_path=os.path.join(
            third_path_dir,
            PROCESS_FOLDER_RECONSTRUCTED_SLICES,
            "frm_edftomomill_twoentries_slice.h5",
        ),
        data_path="entry0000",
        data=data,
    )
    third_part_volume.save()

    reconstructions_urls = scan.get_reconstructed_slices()
    assert len(reconstructions_urls) == 2
    assert edf_volume.get_identifier().to_str() in reconstructions_urls
    assert hdf5_volume.get_identifier().to_str() in reconstructions_urls
