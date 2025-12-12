import h5py
from nxtomo.paths.nxtomo import get_paths as get_nexus_paths
from tomwer.core.process.reconstruction.axis import AxisTask
from tomwer.tests.conftest import nxtomo_scan_360  # noqa F811
from tomwer.core.process.reconstruction.axis import AxisRP


def test_read_x_rotation_axis_pixel_position(nxtomo_scan_360):  # noqa F811
    """
    test reading of the estimated cor from the motor using scan metadata
    """
    nexus_paths = get_nexus_paths(None)

    x_rotation_axis_pixel_position_path = "/".join(
        [
            nxtomo_scan_360.entry,
            nexus_paths.INSTRUMENT_PATH,
            nexus_paths.nx_instrument_paths.DETECTOR_PATH,
            nexus_paths.nx_detector_paths.X_ROTATION_AXIS_PIXEL_POSITION
            or nexus_paths.nx_detector_paths.ESTIMATED_COR_FRM_MOTOR_PATH,
        ]
    )
    with h5py.File(nxtomo_scan_360.master_file, mode="r") as h5f:
        assert x_rotation_axis_pixel_position_path not in h5f

    axis_params = AxisRP()
    axis_params.mode = "read"
    task = AxisTask(
        inputs={
            "data": nxtomo_scan_360,
            "axis_params": axis_params,
        }
    )
    # test the task when there is no metadata
    task.run()
    assert nxtomo_scan_360.axis_params.absolute_cor_value is None
    assert nxtomo_scan_360.axis_params.relative_cor_value is None

    # test the task when there is metadata
    with h5py.File(nxtomo_scan_360.master_file, mode="a") as h5f:
        h5f[x_rotation_axis_pixel_position_path] = 12.5

    nxtomo_scan_360.clear_cache()
    task.run()
    assert nxtomo_scan_360.axis_params.absolute_cor_value == 22.5
    assert nxtomo_scan_360.axis_params.relative_cor_value == 12.5
