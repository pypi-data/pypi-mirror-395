from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.reconstruction.nabu.helical import HelicalPrepareWeightsDouble


def test_DeltaBetaSelector(
    qtapp,  # noqa F811
):
    """simple test of the _DeltaBetaSelectorDialog"""
    widget = HelicalPrepareWeightsDouble()
    assert widget.getConfiguration() == {
        "processes_file": "{scan_parent_dir_basename}/{scan_dir_name}/map_and_doubleff.hdf5",
        "transition_width_vertical": 50.0,
        "transition_width_horizontal": 50.0,
    }
    config = {
        "processes_file": "test.hdf5",
        "transition_width_vertical": 12.5,
        "transition_width_horizontal": 11.5,
    }
    widget.setConfiguration(config=config)
    assert widget.getConfiguration() == config
