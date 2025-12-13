from tomwer.gui.stitching.normalization import NormalizationBySampleGroupBox

from tomwer.tests.conftest import qtapp  # noqa F401


def test_FrameNormalizationWidget(
    qtapp,  # noqa F811
):
    widget = NormalizationBySampleGroupBox()
    assert widget.getConfiguration() == {
        "active": True,
        "side": "left",
        "method": "median",
        "width": 30,
        "margin": 0,
    }

    new_config = {
        "active": False,
        "side": "left",
        "method": "median",
        "width": 30,
        "margin": 0,
    }

    widget.setConfiguration(new_config)
    assert widget.getConfiguration() == new_config
