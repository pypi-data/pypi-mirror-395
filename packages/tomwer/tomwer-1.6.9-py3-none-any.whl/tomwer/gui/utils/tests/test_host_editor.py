from tomwer.gui.utils.host_editor import HostEditor
from tomwer.tests.conftest import qtapp  # noqa F401


def test_HostEditor(
    qtapp,  # noqa F811
):
    # Note: host pinging is not compliant with CI
    widget = HostEditor(name=None, enable_host_pinging=False)
    widget.setCurrentText("tata")
    widget.setPort(26)

    assert widget.currentText() == "tata"
