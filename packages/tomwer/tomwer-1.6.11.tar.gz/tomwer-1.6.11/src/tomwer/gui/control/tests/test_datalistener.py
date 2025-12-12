# coding: utf-8
from __future__ import annotations

import pytest
from silx.gui.utils.testutils import SignalListener

from tomwer.gui.control.datalistener import ConfigurationWidget
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.tests.utils import skip_gui_test
from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_TestDataListenerConfiguration(
    qtapp,  # noqa F811
):
    configWidget = ConfigurationWidget(parent=None, enable_host_pinging=False)
    sig_listener = SignalListener()
    configWidget.sigConfigurationChanged.connect(sig_listener)
    with block_signals(configWidget):
        configWidget.setHost("localhost")

    assert configWidget.getConfiguration() == {"host": "localhost", "port": 4000}
    with block_signals(configWidget):
        configWidget.setPort(0)
    with block_signals(configWidget):
        configWidget.setHost("toto")
    assert configWidget.getConfiguration() == {"host": "toto", "port": 0}
    assert sig_listener.callCount() == 0
