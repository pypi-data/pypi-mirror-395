from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.control.datadiscovery import DataDiscoveryWidget
from tomwer.core.scan.scantype import ScanType


def test_data_discovery_widget(qtapp):  # noqa F811
    widget = DataDiscoveryWidget()
    pass
    widget.show()
    configuration = widget.getConfiguration()

    assert isinstance(configuration, dict)
    assert configuration == {
        "start_folder": "",
        "file_filter": None,
        "scan_type_searched": ScanType.NX_TOMO.value,
    }

    new_config = {
        "start_folder": "/my/folder",
        "file_filter": "*.nx",
        "scan_type_searched": ScanType.BLISS.value,
    }

    widget.setConfiguration(new_config)
    assert widget.getConfiguration() == new_config
    widget = None
