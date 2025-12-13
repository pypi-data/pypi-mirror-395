from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.reconstruction.nabu.castvolume import CastVolumeWidget


def test_CastVolumeWidget(qtapp):  # noqa F811
    """simple test of the CastVolumeWidget"""
    widget = CastVolumeWidget(parent=None)
    assert widget.getConfiguration() == {
        "compression_ratios": None,
        "data_max": None,
        "data_min": None,
        "output_data_type": "uint16",
        "output_dir": "{volume_data_parent_folder}/cast_volume",
        "output_file_format": "tiff",
        "overwrite": True,
        "rescale_max_percentile": 90,
        "rescale_min_percentile": 10,
        "remove_input_volume": False,
    }

    widget._minMaxAuto.setChecked(False)
    assert widget.getConfiguration() == {
        "compression_ratios": None,
        "data_max": 0.0,
        "data_min": 0.0,
        "output_data_type": "uint16",
        "output_dir": "{volume_data_parent_folder}/cast_volume",
        "output_file_format": "tiff",
        "overwrite": True,
        "rescale_max_percentile": None,
        "rescale_min_percentile": None,
        "remove_input_volume": False,
    }

    widget.setDataMin(1.0)
    widget.setDataMax(10.0)

    assert widget.getConfiguration() == {
        "compression_ratios": None,
        "data_max": 10.0,
        "data_min": 1.0,
        "output_data_type": "uint16",
        "output_dir": "{volume_data_parent_folder}/cast_volume",
        "output_file_format": "tiff",
        "overwrite": True,
        "rescale_max_percentile": None,
        "rescale_min_percentile": None,
        "remove_input_volume": False,
    }
    widget.setOutputFileformat("edf")
    assert widget.getConfiguration() == {
        "compression_ratios": None,
        "data_max": 10.0,
        "data_min": 1.0,
        "output_data_type": "uint16",
        "output_dir": "{volume_data_parent_folder}/cast_volume",
        "output_file_format": "edf",
        "overwrite": True,
        "rescale_max_percentile": None,
        "rescale_min_percentile": None,
        "remove_input_volume": False,
    }
    widget.setOverwrite(False)
    assert widget.getConfiguration() == {
        "compression_ratios": None,
        "data_max": 10.0,
        "data_min": 1.0,
        "output_data_type": "uint16",
        "output_dir": "{volume_data_parent_folder}/cast_volume",
        "output_file_format": "edf",
        "overwrite": False,
        "rescale_max_percentile": None,
        "rescale_min_percentile": None,
        "remove_input_volume": False,
    }
    widget.setOutputDataType("float32")
    assert widget.getConfiguration() == {
        "compression_ratios": None,
        "data_max": 10.0,
        "data_min": 1.0,
        "output_data_type": "float32",
        "output_dir": "{volume_data_parent_folder}/cast_volume",
        "output_file_format": "edf",
        "overwrite": False,
        "rescale_max_percentile": None,
        "rescale_min_percentile": None,
        "remove_input_volume": False,
    }
    widget.setRemoveInputVolume(True)
    assert widget.getConfiguration() == {
        "compression_ratios": None,
        "data_max": 10.0,
        "data_min": 1.0,
        "output_data_type": "float32",
        "output_dir": "{volume_data_parent_folder}/cast_volume",
        "output_file_format": "edf",
        "overwrite": False,
        "rescale_max_percentile": None,
        "rescale_min_percentile": None,
        "remove_input_volume": True,
    }
