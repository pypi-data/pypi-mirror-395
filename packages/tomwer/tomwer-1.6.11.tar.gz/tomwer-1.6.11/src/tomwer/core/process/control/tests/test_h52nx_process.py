import os
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.process.output import ProcessDataOutputDirMode
from tomwer.core.process.control.nxtomomill import (
    EDFToNxProcess,
    H5ToNxProcess,
    get_default_raw_data_output_file,
)
from tomwer.core.utils.scanutils import MockNXtomo, MockEDF
from nxtomomill.converter.hdf5.utils import PROCESSED_DATA_DIR_NAME, RAW_DATA_DIR_NAME


def test_h52nx_process_deduce_output_file_path(tmp_path):
    """test H5ToNxProcess.deduce_output_file_path function"""
    scan_path = str(tmp_path / "path" / RAW_DATA_DIR_NAME / "my_scan")
    os.makedirs(scan_path)

    scan = MockNXtomo(scan_path=scan_path, n_proj=0).scan

    # test H52NXDefaultOutput.PROCESSED_DATA
    assert H5ToNxProcess.deduce_output_file_path(
        master_file_name=scan.master_file,
        scan=scan,
        output_dir=ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER.value,
    ) == str(tmp_path / "path" / PROCESSED_DATA_DIR_NAME / "my_scan" / "my_scan.nx")

    # test H52NXDefaultOutput.NEAR_BLISS_FILE
    assert H5ToNxProcess.deduce_output_file_path(
        master_file_name=scan.master_file,
        scan=scan,
        output_dir=ProcessDataOutputDirMode.IN_SCAN_FOLDER.value,
    ) == str(tmp_path / "path" / RAW_DATA_DIR_NAME / "my_scan" / "my_scan.nx")

    # test providing output dir with some formatting to be done
    assert H5ToNxProcess.deduce_output_file_path(
        master_file_name=scan.master_file,
        scan=scan,
        output_dir="{scan_parent_dir_basename}/../../toto/{scan_dir_name}",
    ) == str(tmp_path / "toto" / "my_scan" / "my_scan.nx")

    # test providing output folder directly
    assert (
        H5ToNxProcess.deduce_output_file_path(
            master_file_name=scan.master_file,
            scan=scan,
            output_dir="/tmp/",
        )
        == "/tmp/my_scan.nx"
    )


def test_edf2nx_process_deduce_output_file_path(tmp_path):
    """test EDFToNxProcess.deduce_output_file_path function"""
    scan_path = str(tmp_path / "path" / RAW_DATA_DIR_NAME / "my_edf_scan")
    MockEDF(
        scan_path=scan_path,
        n_radio=10,
        n_ini_radio=10,
        n_extra_radio=0,
        dim=128,
        dark_n=1,
        flat_n=1,
    )
    scan = EDFTomoScan(scan_path)

    # test NEAR_INPUT_FILE
    assert EDFToNxProcess.deduce_output_file_path(
        folder_path=scan_path,
        output_dir=ProcessDataOutputDirMode.IN_SCAN_FOLDER.value,
        scan=scan,
    ) == os.path.join(tmp_path, "path", RAW_DATA_DIR_NAME, "my_edf_scan.nx")

    # test PROCESSED_DATA
    assert EDFToNxProcess.deduce_output_file_path(
        folder_path=scan_path,
        output_dir=ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER.value,
        scan=scan,
    ) == os.path.join(tmp_path, "path", PROCESSED_DATA_DIR_NAME, "my_edf_scan.nx")

    # test providing output dir with some formatting to be done
    assert EDFToNxProcess.deduce_output_file_path(
        folder_path=scan_path,
        output_dir="{scan_parent_dir_basename}/../../toto/",
        scan=scan,
    ) == str(tmp_path / "toto" / "my_edf_scan.nx")

    # test providing output folder directly
    assert (
        EDFToNxProcess.deduce_output_file_path(
            folder_path=scan_path,
            output_dir="/tmp/output",
            scan=scan,
        )
        == "/tmp/output/my_edf_scan.nx"
    )


def test_get_default_raw_data_output_file():
    """test 'get_default_raw_data_output_file' function"""
    assert get_default_raw_data_output_file("/tmp/path/file.h5") == "/tmp/path/file.nx"
    assert (
        get_default_raw_data_output_file(f"/tmp/{PROCESSED_DATA_DIR_NAME}/file.h5")
        == f"/tmp/{RAW_DATA_DIR_NAME}/file.nx"
    )

    assert (
        get_default_raw_data_output_file(
            f"/tmp/path/{PROCESSED_DATA_DIR_NAME}/toto/file.h5"
        )
        == f"/tmp/path/{RAW_DATA_DIR_NAME}/toto/file.nx"
    )
    # note: _RAW_DATA_DIR_NAME part of the path but not a folder
    assert (
        get_default_raw_data_output_file(f"/tmp/path_{RAW_DATA_DIR_NAME}/toto/file.h5")
        == f"/tmp/path_{RAW_DATA_DIR_NAME}/toto/file.nx"
    )

    # 2. advance test
    # 2.1 use case: '_RAW_DATA_DIR_NAME' is present twice in the path -> replace the deeper one
    assert (
        get_default_raw_data_output_file(
            f"/tmp/{PROCESSED_DATA_DIR_NAME}/path/{RAW_DATA_DIR_NAME}/toto/file.h5"
        )
        == f"/tmp/{PROCESSED_DATA_DIR_NAME}/path/{RAW_DATA_DIR_NAME}/toto/file.nx"
    )

    # 2.2 use case: contains both '_RAW_DATA_DIR_NAME' and '_PROCESSED_DATA_DIR_NAME' in the path
    assert (
        get_default_raw_data_output_file(
            f"/tmp/{PROCESSED_DATA_DIR_NAME}/path/{RAW_DATA_DIR_NAME}/toto/file.h5"
        )
        == f"/tmp/{PROCESSED_DATA_DIR_NAME}/path/{RAW_DATA_DIR_NAME}/toto/file.nx"
    )

    assert (
        get_default_raw_data_output_file(
            f"/tmp/{RAW_DATA_DIR_NAME}/path/{PROCESSED_DATA_DIR_NAME}/toto/file.h5"
        )
        == f"/tmp/{RAW_DATA_DIR_NAME}/path/{RAW_DATA_DIR_NAME}/toto/file.nx"
    )

    # 2.3 use case: expected output file is the input file. Make sure append '_nxtomo'
    assert (
        get_default_raw_data_output_file("/tmp/path/file.nx")
        == "/tmp/path/file_nxtomo.nx"
    )
