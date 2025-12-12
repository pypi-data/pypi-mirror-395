import pytest

from tomwer.gui.stitching.config.axisparams import StitcherAxisParams
from tomwer.tests.conftest import qtapp  # noqa F401


def test_StitcherAxisParams(
    qtapp,  # noqa F811
):
    """test the StitcherAxisParams widget"""
    with pytest.raises(TypeError):
        widget = StitcherAxisParams(axis="toto")
    widget = StitcherAxisParams(axis=0)
    assert widget.getConfiguration() == {
        "stitching": {
            "axis_0_params": "img_reg_method=nabu-fft;window_size=400",
        }
    }
    new_config = {
        "stitching": {
            "axis_0_params": "img_reg_method=skimage;window_size=50",
        },
    }
    widget.setConfiguration(new_config)
    assert widget.getConfiguration() == new_config
