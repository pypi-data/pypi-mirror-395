from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.dataportal.gallery import GalleryWidget


def test_GalleryWidget(
    qtapp,  # noqa F811
):
    widget = GalleryWidget()
    assert widget.getConfiguration() == {
        "output_format": "png",
        "overwrite": True,
        "binning": "16x16",
    }

    new_config = {
        "output_format": "jpg",
        "overwrite": False,
        "binning": "4x4",
    }
    widget.setConfiguration(new_config)
    assert widget.getConfiguration() == new_config
