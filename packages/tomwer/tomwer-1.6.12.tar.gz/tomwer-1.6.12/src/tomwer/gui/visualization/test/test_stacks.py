import logging
import os

import numpy
import pytest
from silx.gui import qt
from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_RECONSTRUCTED_SLICES,
)
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.gui.stacks import RadioStack, SliceStack
from tomwer.tests.utils import skip_gui_test
from tomwer.tests.conftest import qtapp  # noqa F401

logging.disable(logging.INFO)


@pytest.mark.parametrize("use_identifiers", (True, False))
@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_slice_stack(
    qtapp,  # noqa F811
    tmp_path,
    use_identifiers,
):
    """
    :param use_identifiers: If true will add the different tomo object using identifiers instead of class instances.
    """
    widget = SliceStack()
    widget.setAttribute(qt.Qt.WA_DeleteOnClose)

    url_list = widget._viewer._urlsTable._urlsTable
    assert url_list.count() == 0
    n_scan = 5

    root_dir = tmp_path / "test_slice_stack"
    root_dir.mkdir()

    def create_vol_data(n_slice=1):
        return numpy.random.random(10 * 10 * n_slice).reshape(n_slice, 10, 10)

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

    # step 1: test adding some scans
    for i_scan in range(n_scan):
        scan = MockNXtomo(
            scan_path=os.path.join(root_dir, f"scan{i_scan}"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=10,
        ).scan
        volume = EDFVolume(
            folder=os.path.join(
                scan.path,
                PROCESS_FOLDER_RECONSTRUCTED_SLICES,
                f"edf_volume_scan_{i_scan}",
            ),
            volume_basename=f"edf_volume_scan_{i_scan}",
            data=create_vol_data(),
            metadata=volume_metadata,
        )
        volume.save()
        scan.set_latest_reconstructions((volume,))
        assert len(scan.latest_reconstructions) == 1
        if use_identifiers:
            widget.addTomoObj(scan.get_identifier().to_str())
        else:
            widget.addTomoObj(scan)

    last_scan_added = scan

    assert url_list.count() == n_scan
    assert len(widget._volume_id_to_urls) == n_scan

    # step 2: test adding some volumes
    n_volume = 4
    last_edf_volume_added = None
    last_hdf5_volume_added = None

    for i_vol in range(n_volume):
        volume_metadata["nabu_config"]["phase"]["delta_beta"] += i_vol
        volume_type = [EDFVolume, HDF5Volume][i_vol % 2]
        if volume_type == EDFVolume:
            volume = EDFVolume(
                folder=root_dir
                / PROCESS_FOLDER_RECONSTRUCTED_SLICES
                / f"slice_{i_vol}",
                volume_basename=f"slice_{i_vol}",
                data=create_vol_data(),
                metadata=volume_metadata,
            )
            last_edf_volume_added = volume
        elif volume_type == HDF5Volume:
            volume = HDF5Volume(
                file_path=os.path.join(
                    root_dir
                    / PROCESS_FOLDER_RECONSTRUCTED_SLICES
                    / f"my_vol_{i_vol}.hdf5"
                ),
                data_path="entry0000",
                data=create_vol_data(),
                metadata=volume_metadata,
            )
            last_hdf5_volume_added = volume
        else:
            raise TypeError
        volume.save()
        if use_identifiers:
            widget.addTomoObj(volume.get_identifier().to_str())
        else:
            widget.addTomoObj(volume)

    assert len(widget._volume_id_to_urls) == (n_scan + n_volume)
    assert len(widget._viewer.getUrls()) == (n_scan + n_volume)

    widget.clear()
    assert len(widget._volume_id_to_urls) == 0

    # check adding objects from a list of string
    assert n_volume >= 2, "following test won't be able to be correctly executed"
    widget._addTomoObjectsFromStrList(
        [
            last_hdf5_volume_added.file_path,
            last_edf_volume_added.url.file_path(),
            last_scan_added.path,
        ]
    )
    # dummy check metadata are displayed
    widget._viewer._reconsWidget._deltaBetaQLE.text().startswith("1")
    assert len(widget._volume_id_to_urls) == 3
    # try adding a non existing path
    widget._addTomoObjectsFromStrList(
        [
            "/none/existing/path",
            "/none/existing/path.hdf5",
        ]
    )

    widget.close()


@pytest.mark.parametrize("use_identifiers", (True, False))
@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_radio_stack(
    qtapp,  # noqa F811
    tmp_path,
    use_identifiers: bool,
):
    """
    :param use_identifiers: If true will add the different tomo object using identifiers instead of class instances.
    """
    widget = RadioStack()
    widget.setAttribute(qt.Qt.WA_DeleteOnClose)

    widget_urls = widget._viewer._urlsTable._urlsTable
    n_scan = 3

    root_dir = tmp_path / "test_radio_stack"
    root_dir.mkdir()
    proj_per_scan = 10

    # step 1: test adding some scans
    for i_scan in range(n_scan):
        scan = MockNXtomo(
            scan_path=os.path.join(root_dir, f"scan{i_scan}"),
            n_proj=proj_per_scan,
            n_ini_proj=proj_per_scan,
            scan_range=180,
            dim=10,
        ).scan
        if use_identifiers:
            widget.addTomoObj(scan.get_identifier().to_str())
        else:
            widget.addTomoObj(scan)
    assert widget_urls.count() == n_scan * proj_per_scan

    widget.show()
    widget.close()
