from __future__ import annotations


import os
import pint
import tempfile

from tomoscan.series import Series

from tomwer.gui.stitching.StitchingWindow import ZStitchingWindow
from tomwer.gui.stitching.tests.utils import create_scans_z_series
from tomwer.tests.conftest import qtapp  # noqa F401


_ureg = pint.get_application_registry()


def test_ZStitchingWindow(
    qtapp,  # noqa F811
    tmp_path,
):
    """
    Test ZStitchingWindow

    * adding tom objects
    * saving and loading settings (nabu-stitching configuration)
    * editing tomo objects positions over stitching axis
    * reset tomo objects positions
    """

    window = ZStitchingWindow()

    axis_0_positions = (90, 0.0, -90.0)
    axis_2_positions = (0.0, 0.0, 0.0)
    pixel_size = 1.0

    input_dir = os.path.join(tmp_path, "input")

    scans = create_scans_z_series(
        output_dir=input_dir,
        z_positions_m=axis_0_positions,
        x_positions_m=axis_2_positions,
        shifts=((0.0, 0.0), (-90.0, 0.0), (-180.0, 0.0)),
        sample_pixel_size=pixel_size,
        raw_frame_width=280,
        final_frame_width=100,
    )
    series = Series("z-series", scans)

    window.show()
    for scan in scans:
        window.addTomoObj(scan)
    window.clean()
    window.setSeries(series)

    # test dumping and loading configuration to a file
    with tempfile.TemporaryDirectory() as dump_dir:
        config_file = os.path.join(dump_dir, "configuration.cfg")
        window._saveSettings(file_path=config_file)
        assert os.path.exists(config_file)
        window._loadSettings(config_file)
        # remove configuration
        window.clean()
        assert len(window._widget._mainWidget.getTomoObjs()) == 0
        # reload it
        window._loadSettings(file_path=config_file)
        assert len(window._widget._mainWidget.getTomoObjs()) == len(series)

    assert window.getConfiguration()["stitching"]["axis_0_pos_px"] == [90, 0, -90]

    # test editing axis position
    widget_tomo_obj_0 = (
        window._editTomoObjFirstAxisPositionsWidget._tomoObjtoTomoObjPosWidget[
            scans[0].get_identifier().to_str()
        ]
    )

    window._editTomoObjFirstAxisPositionsWidget.setEditionMode("free")
    widget_tomo_obj_0.setValue(10, emit_editing_finished=True)
    assert window.getConfiguration()["stitching"]["axis_0_pos_px"] == [10, 0, -90]
    window._editTomoObjFirstAxisPositionsWidget.setEditionMode("downstream")
    widget_tomo_obj_0.setValue(30, emit_editing_finished=True)
    assert window.getConfiguration()["stitching"]["axis_0_pos_px"] == [30, 20, -70]
    window._editTomoObjFirstAxisPositionsWidget.setEditionMode("upstream")
    widget_tomo_obj_2 = (
        window._editTomoObjFirstAxisPositionsWidget._tomoObjtoTomoObjPosWidget[
            scans[2].get_identifier().to_str()
        ]
    )
    widget_tomo_obj_2.setValue(-120, emit_editing_finished=True)
    assert window.getConfiguration()["stitching"]["axis_0_pos_px"] == [-20, -30, -120]

    # test reset positions to initial positions
    window._editTomoObjFirstAxisPositionsWidget._resetPositions()
    assert window.getConfiguration()["stitching"]["axis_0_pos_px"] == [90, 0, -90]
