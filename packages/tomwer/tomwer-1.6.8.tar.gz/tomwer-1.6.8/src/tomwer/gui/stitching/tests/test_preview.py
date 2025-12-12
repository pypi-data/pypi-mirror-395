from __future__ import annotations

import os
import pint
import numpy
import pytest
from nabu.stitching.config import PreProcessedZStitchingConfiguration
from nabu.stitching.z_stitching import PreProcessZStitcher
from tomwer.tests.conftest import qtapp  # noqa F401

from silx.image.phantomgenerator import PhantomGenerator

from tomwer.gui.stitching.stitching_preview import PreviewStitchingPlot
from tomwer.gui.stitching.tests.utils import create_scans_z_series

_ureg = pint.get_application_registry()


@pytest.mark.parametrize("flip_lr", (True, False))
@pytest.mark.parametrize("flip_ud", (True, False))
def test_preview(tmp_path, flip_lr, flip_ud, qtapp):  # noqa F401
    axis_0_positions = (90, 0.0, -90.0)
    axis_2_positions = (0.0, 0.0, 0.0)
    sample_pixel_size = 1.0

    output_file_path = os.path.join(str(tmp_path), "output", "stitched.nx")
    input_dir = os.path.join(tmp_path, "input")

    scans = create_scans_z_series(
        output_dir=input_dir,
        z_positions_m=axis_0_positions,
        x_positions_m=axis_2_positions,
        shifts=((0.0, 0.0), (-90.0, 0.0), (-180.0, 0.0)),
        sample_pixel_size=sample_pixel_size,
        raw_frame_width=280,
        final_frame_width=100,
        flip_lr=flip_lr,
        flip_ud=flip_ud,
    )
    stitching_config = PreProcessedZStitchingConfiguration(
        output_file_path=output_file_path,
        output_data_path="entry_stitched",
        overwrite_results=True,
        slurm_config=None,
        axis_0_pos_mm=numpy.array(axis_0_positions) * 1000,
        axis_2_pos_mm=numpy.array(axis_2_positions) * 1000,
        axis_0_pos_px=None,
        axis_1_pos_px=None,
        axis_2_pos_px=None,
        input_scans=scans,
        pixel_size=sample_pixel_size,
    )
    widget = PreviewStitchingPlot(axis=0)
    widget._backGroundAction.toggle()

    stitcher = PreProcessZStitcher(configuration=stitching_config)
    stitched_id = stitcher.stitch(store_composition=True)
    assert stitched_id is not None
    composition = stitcher.frame_composition
    assert composition is not None

    widget.setStitchedTomoObj(tomo_obj_id=stitched_id.to_str(), composition=composition)
    assert widget.stitched_image is not None
    assert widget.composition_background is not None

    numpy.testing.assert_almost_equal(
        widget.stitched_image,
        PhantomGenerator.get2DPhantomSheppLogan(n=280).astype(numpy.float32) * 256.0,
    )

    widget._backGroundAction.toggle()
