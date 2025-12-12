import pytest
from ewoksorange.bindings import owsconvert
from tomwer.tests.datasets import TomwerCIDatasets


ows_files_to_convert = ("from_nxtomo_to_volume.ows",)


@pytest.mark.parametrize("orange_file_name", ows_files_to_convert)
def test_conversion(orange_file_name):
    """test orange file can be converted to ewoks Graph"""
    scheme_file = TomwerCIDatasets.get_dataset(f"workflows/{orange_file_name}")
    graph = owsconvert.ows_to_ewoks(scheme_file)
    # make sure settings where correctly saved
    assert len(graph.graph.nodes) == 7
    assert len(graph.graph.edges) == 6
    # make sure the settings are properly loaded
    for node in graph.graph.nodes.values():
        assert node["task_type"] == "class"
        assert node["task_identifier"].startswith("tomwer")
    # check settings of some specific nodes
    # dark and flat
    dark_flat_node = graph.graph.nodes["1"]
    assert (
        dark_flat_node["task_identifier"]
        == "tomwer.core.process.reconstruction.darkref.darkrefscopy.DarkRefsCopy"
    )
    assert "default_inputs" in dark_flat_node

    def fileter_dark_ref_params(my_dict):
        return my_dict["name"] == "dark_ref_params"

    dark_ref_params_settings = tuple(
        filter(fileter_dark_ref_params, dark_flat_node["default_inputs"])
    )
    assert len(dark_ref_params_settings) == 1
    dark_ref_params_as_dict = dark_ref_params_settings[0]["value"]

    assert "DOWHEN" in dark_ref_params_as_dict
    assert "DARKCAL" in dark_ref_params_as_dict
    assert "DKFILE" in dark_ref_params_as_dict

    # axis
    axis_node = graph.graph.nodes["2"]
    assert (
        axis_node["task_identifier"]
        == "tomwer.core.process.reconstruction.axis.axis.AxisTask"
    )
    assert "default_inputs" in axis_node
    assert len(axis_node["default_inputs"]) == 2  # axis_params + gui metadata

    def filter_axis_params(my_dict):
        return my_dict["name"] == "axis_params"

    axis_params_settings = tuple(
        filter(filter_axis_params, axis_node["default_inputs"])
    )
    assert len(axis_params_settings) == 1
    axis_params_as_dict = axis_params_settings[0]["value"]

    assert "MODE" in axis_params_as_dict
    assert "POSITION_VALUE" in axis_params_as_dict
    assert "SINOGRAM_LINE" in axis_params_as_dict

    # nabu slice
    nabu_slice_node = graph.graph.nodes["3"]
    assert (
        nabu_slice_node["task_identifier"]
        == "tomwer.core.process.reconstruction.nabu.nabuslices.NabuSlicesTask"
    )
    assert "default_inputs" in axis_node

    def filter_nabu_params(my_dict):
        return my_dict["name"] == "nabu_params"

    nabu_params_settings = tuple(
        filter(filter_nabu_params, nabu_slice_node["default_inputs"])
    )
    assert len(nabu_params_settings) == 1
    nabu_params_as_dict = nabu_params_settings[0]["value"]

    assert "preproc" in nabu_params_as_dict
    assert "phase" in nabu_params_as_dict
    assert "tomwer_slices" in nabu_params_as_dict

    # nabu volume
    nabu_volume_node = graph.graph.nodes["4"]
    assert (
        nabu_volume_node["task_identifier"]
        == "tomwer.core.process.reconstruction.nabu.nabuvolume.NabuVolumeTask"
    )
    assert "default_inputs" in axis_node

    def filter_nabu_volume_params(my_dict):
        return my_dict["name"] == "nabu_volume_params"

    nabu_volume_params_settings = tuple(
        filter(filter_nabu_volume_params, nabu_volume_node["default_inputs"])
    )
    assert len(nabu_volume_params_settings) == 1
    nabu_volume_params_as_dict = nabu_volume_params_settings[0]["value"]

    assert "start_z" in nabu_volume_params_as_dict
    assert "end_z" in nabu_volume_params_as_dict
