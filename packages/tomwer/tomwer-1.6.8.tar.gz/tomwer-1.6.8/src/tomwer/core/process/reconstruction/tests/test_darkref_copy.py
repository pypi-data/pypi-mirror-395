import os

import numpy
import pytest
from silx.io.dictdump import dicttoh5

from tomwer.core.process.reconstruction.darkref.darkrefscopy import DarkRefsCopy
from tomwer.core.utils.scanutils import MockNXtomo


@pytest.mark.parametrize(
    "process_only_copy_scan_without_raw, process_only_dkrf_scan_without_raw",
    ((False, False), (True, False), (False, True), (True, True)),
)
@pytest.mark.parametrize(
    "process_only_copy_scan_with_raw, process_only_dkrf_scan_with_raw",
    ((False, False), (True, False), (False, True), (True, True)),
)
def test_register_and_copy_darks_and_flats(
    tmp_path,
    process_only_copy_scan_with_raw,
    process_only_dkrf_scan_with_raw,
    process_only_copy_scan_without_raw,
    process_only_dkrf_scan_without_raw,
):
    """
    Test registration and copy of darks and flats
    """
    scan_folder_with_raw = tmp_path / "test_dir_1"
    scan_folder_without_raw = tmp_path / "test_dir_2"
    save_dir = tmp_path / "save_dir"
    for my_dir in (save_dir, scan_folder_with_raw, scan_folder_without_raw):
        os.makedirs(my_dir)

    scan_with_raw = MockNXtomo(
        scan_path=scan_folder_with_raw,
        create_ini_dark=True,
        create_ini_flat=True,
        create_final_flat=False,
        n_proj=10,
        n_ini_proj=10,
        dim=12,
    ).scan
    scan_without_raw = MockNXtomo(
        scan_path=scan_folder_without_raw,
        create_ini_dark=False,
        create_ini_flat=False,
        create_final_flat=False,
        n_proj=10,
        n_ini_proj=10,
        dim=12,
    ).scan

    # get task ready
    process_with_raw = DarkRefsCopy(
        inputs={
            "data": scan_with_raw,
            "save_dir": save_dir,
            "process_only_copy": process_only_copy_scan_with_raw,
            "process_only_dkrf": process_only_dkrf_scan_with_raw,
            "serialize_output_data": False,
        }
    )
    # test processing with flat and dark materials
    process_with_raw.run()
    if process_only_copy_scan_with_raw:
        assert scan_with_raw.load_reduced_darks() in (None, {})
        assert scan_with_raw.load_reduced_flats() in (None, {})
    else:
        assert scan_with_raw.load_reduced_darks() not in (None, {})
        assert scan_with_raw.load_reduced_flats() not in (None, {})

    # test processing without flat and dark materials (where copy can happen)
    process_without_raw = DarkRefsCopy(
        inputs={
            "data": scan_without_raw,
            "save_dir": save_dir,
            "process_only_copy": process_only_copy_scan_without_raw,
            "process_only_dkrf": process_only_dkrf_scan_without_raw,
            "serialize_output_data": False,
        }
    )

    process_without_raw.run()
    if process_only_copy_scan_with_raw or process_only_dkrf_scan_without_raw:
        assert scan_without_raw.load_reduced_darks() in (None, {})
        assert scan_without_raw.load_reduced_flats() in (None, {})
    elif process_only_dkrf_scan_without_raw:
        assert scan_without_raw.load_reduced_darks() not in (None, {})
        assert scan_without_raw.load_reduced_flats() not in (None, {})


def test_save_reduced_frames_to_be_copied(tmp_path):
    """
    test save_flats_to_be_copied and save_darks_to_be_copied functions
    """
    # create raw data
    from silx.io.url import DataUrl
    from tomoscan.scanbase import ReducedFramesInfos

    raw_data = tmp_path / "raw_data"
    raw_data.mkdir()
    dark_file_path = os.path.join(raw_data, "darks.h5")
    darks_dict = {
        "0": numpy.linspace(0, 100, 10000).reshape(100, 100),
        ReducedFramesInfos.COUNT_TIME_KEY: numpy.array(
            [
                0.2,
            ]
        ),
        ReducedFramesInfos.MACHINE_ELECT_CURRENT_KEY: numpy.array(
            [
                12.2,
            ]
        ),
        ReducedFramesInfos.LR_FLIP: True,
        ReducedFramesInfos.UD_FLIP: True,
    }

    dicttoh5(
        darks_dict,
        h5file=dark_file_path,
        h5path="entry0000/darks",
        update_mode="modify",
        mode="a",
    )

    flat_file_path = os.path.join(raw_data, "flats.hdf5")
    flats_dict = {
        "0": numpy.linspace(0, 100, 10000).reshape(100, 100),
        "200": numpy.ones((100, 100)).reshape(100, 100),
        ReducedFramesInfos.COUNT_TIME_KEY: numpy.array([0.2, 0.3]),
        ReducedFramesInfos.MACHINE_ELECT_CURRENT_KEY: numpy.array([12.2, 12.1]),
        ReducedFramesInfos.LR_FLIP: True,
        ReducedFramesInfos.UD_FLIP: True,
    }

    dicttoh5(
        flats_dict,
        h5file=flat_file_path,
        h5path="entry0000/flats",
        update_mode="modify",
        mode="a",
    )

    raw_darks_url_1 = DataUrl(
        file_path=dark_file_path,
        data_path="entry0000",
    )
    raw_darks_url_2 = DataUrl(
        file_path=dark_file_path,
        data_path="entry0000/darks",
    )
    raw_darks_url_3 = DataUrl(
        file_path=dark_file_path,
        data_path="",
    )

    assert (
        DarkRefsCopy.get_reduced_frame_data(
            url=raw_darks_url_1, reduced_target="darks"
        ).keys()
        == darks_dict.keys()
    )
    assert (
        DarkRefsCopy.get_reduced_frame_data(
            url=raw_darks_url_2, reduced_target="darks"
        ).keys()
        == darks_dict.keys()
    )
    assert (
        DarkRefsCopy.get_reduced_frame_data(
            url=raw_darks_url_3, reduced_target="darks"
        ).keys()
        != darks_dict.keys()
    )

    flat_darks_url_1 = DataUrl(
        file_path=flat_file_path,
        data_path="entry0000",
    )
    flat_darks_url_2 = DataUrl(
        file_path=flat_file_path,
        data_path="entry0000/flats",
    )
    flat_darks_url_3 = DataUrl(
        file_path=flat_file_path,
        data_path="",
    )

    assert (
        DarkRefsCopy.get_reduced_frame_data(
            url=flat_darks_url_1, reduced_target="flats"
        ).keys()
        == flats_dict.keys()
    )
    assert (
        DarkRefsCopy.get_reduced_frame_data(
            url=flat_darks_url_2, reduced_target="flats"
        ).keys()
        == flats_dict.keys()
    )
    assert (
        DarkRefsCopy.get_reduced_frame_data(
            url=flat_darks_url_3, reduced_target="flats"
        ).keys()
        != flats_dict.keys()
    )
