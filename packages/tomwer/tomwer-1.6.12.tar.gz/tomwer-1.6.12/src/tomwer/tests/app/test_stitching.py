import pytest

from nabu.stitching.config import StitchingType
from nabu.stitching.tests import test_y_preprocessing_stitching
from nabu.stitching.tests import test_z_preprocessing_stitching
from nabu.stitching.tests import test_z_postprocessing_stitching

from tomwer.app.stitching.common import MainWindow
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.volume.volumefactory import VolumeFactory
from tomoscan.esrf.volume import HDF5Volume as _tomoscan_HDF5Volume
from tomwer.tests.conftest import qtapp  # noqa F401


def _create_objects_for_stitching(stitching_type: StitchingType, output_dir) -> tuple:
    """
    create tomo object (scans or volumes) and return them with there position along the axis to stitch
    """

    def cast_tomoscan_scans_to_tomwer_scans(scans: tuple) -> tuple:
        return tuple(
            [NXtomoScan(scan=scan.master_file, entry=scan.entry) for scan in scans]
        )

    def cast_tomoscan_volumes_to_tomwer_volumes(volumes: tuple) -> tuple:
        return tuple(
            [
                VolumeFactory.create_tomo_object_from_identifier(
                    volume.get_identifier().to_str()
                )
                for volume in volumes
            ]
        )

    stitching_type = StitchingType(stitching_type)
    if stitching_type is StitchingType.Y_PREPROC:
        nxtomos, positions, _ = test_y_preprocessing_stitching.build_nxtomos(
            output_dir=output_dir, flip_lr=False, flip_ud=False
        )
        return cast_tomoscan_scans_to_tomwer_scans(nxtomos), positions
    elif stitching_type is StitchingType.Z_PREPROC:
        nxtomos, positions, _ = test_z_preprocessing_stitching.build_nxtomos(
            output_dir=output_dir
        )
        return cast_tomoscan_scans_to_tomwer_scans(nxtomos), positions
    elif stitching_type is StitchingType.Z_POSTPROC:
        volumes, positions, _ = test_z_postprocessing_stitching.build_volumes(
            output_dir=output_dir, volume_class=_tomoscan_HDF5Volume
        )
        return cast_tomoscan_volumes_to_tomwer_volumes(volumes), positions
    else:
        raise NotImplementedError()


@pytest.mark.parametrize("stitching_type", StitchingType)
def test_stitching_on_projections(stitching_type, tmp_path, qtapp):  # noqa F401
    if stitching_type in (StitchingType.Z_PREPROC, StitchingType.Z_POSTPROC):
        axis = 0
    elif stitching_type is StitchingType.Y_PREPROC:
        axis = 1
    else:
        raise NotImplementedError

    widget = MainWindow(axis=axis)
    output_dir = tmp_path / "input_objs"
    output_dir.mkdir()
    tomo_objects, positions = _create_objects_for_stitching(stitching_type, output_dir)
    positions_dict = {}
    for tomo_object, position in zip(tomo_objects, positions):
        widget.addTomoObj(tomo_object)
        positions_dict[tomo_object.get_identifier().to_str()] = position

    pos_widget = (
        widget._mainWindow._stitchingConfigWindow._editTomoObjFirstAxisPositionsWidget._tomoObjtoTomoObjPosWidget
    )
    # make sure the position over the axis to stitch are valid
    for tomo_obj, w in pos_widget.items():
        assert positions_dict[tomo_obj] == w.getOriginalValue()

    stitching_configuration = widget.getStitchingConfiguration()
    second_axis = widget._mainWindow._stitchingConfigWindow.second_axis

    # only the axis of the stitching is defined. When launching the widget we don't know if this is pre-processing or post-processing
    assert stitching_configuration["stitching"]["type"][0] == stitching_type.value[0]
    assert len(stitching_configuration["inputs"]["input_datasets"]) == len(tomo_objects)
    assert stitching_configuration["stitching"][f"axis_{axis}_pos_px"] == sorted(
        positions, reverse=True
    )
    # at the moment the 'overlap' size is only handled and provided for the 'main axis (stitching axis)
    assert "overlap_size" in stitching_configuration["stitching"][f"axis_{axis}_params"]
    assert (
        "overlap_size"
        not in stitching_configuration["stitching"][f"axis_{second_axis}_params"]
    )
    assert "axis_2_params" not in stitching_configuration["stitching"]
