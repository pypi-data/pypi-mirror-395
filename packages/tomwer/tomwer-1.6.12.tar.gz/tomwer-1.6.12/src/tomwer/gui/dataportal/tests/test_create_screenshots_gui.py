from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.dataportal.createscreenshots import CreateRawDataScreenshotsWidget


def test_CreateRawDataScreenshotsWidget(qtapp):  # noqa F811
    widget = CreateRawDataScreenshotsWidget()

    assert widget.getConfiguration() == {
        "raw_projections_required": True,
        "raw_projections_each": 90,
        "raw_darks_required": True,
        "raw_flats_required": True,
    }

    new_config = {
        "raw_projections_required": True,
        "raw_projections_each": 26,
        "raw_darks_required": False,
        "raw_flats_required": False,
    }
    widget.setConfiguration(new_config)

    assert widget.getConfiguration() == new_config
