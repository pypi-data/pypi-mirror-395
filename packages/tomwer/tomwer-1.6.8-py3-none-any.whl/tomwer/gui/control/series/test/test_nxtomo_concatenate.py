from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.control.series.nxtomoconcatenate import NXtomoConcatenateWidget


def test_NXtomoConcatenateWidget(
    qtapp,  # noqa F811
):
    """simple test of the NXtomoConcatenateWidget"""
    widget = NXtomoConcatenateWidget()
    assert widget.getConfiguration() == {
        "output_file": "{common_path}/concatenate.nx",
        "output_entry": "entry0000",
        "overwrite": False,
    }
    config = {
        "output_file": "helical.hdf5",
        "output_entry": "my_entry",
        "overwrite": True,
    }
    widget.setConfiguration(config=config)
    assert widget.getConfiguration() == config
