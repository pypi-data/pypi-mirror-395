from __future__ import annotations

import sys
from silx.gui import qt
import functools

import signal

from ..control._DataListenerBaseClass import DataListenerBaseClass
from tomwer.core.process.control.datalistener import DataListener
from tomwer.synctools.bliss_sync.datalistener import (
    DataListenerQThread,
    MockDataListenerQThread,
)
from tomwer.gui.dialog._PortOccupyDialog import PortOccupyDialog
from tomwer.gui.utils.qt_utils import block_signals


class DataListenerOW(DataListenerBaseClass):
    """
    This widget is used to listen to a server notifying the widget when an
    acquisition is finished.
    Then the bliss file will be converted to .nx file, NXtomo compliant.
    """

    name = "Old scan listener"
    id = "orangecontrib.widgets.tomwer.deprecated.DataListenerOW.DataListenerOW"
    description = (
        "The widget will receive information from bliss acquisition "
        "and wait for acquisition to be finished. Once finished it "
        "will call nxtomomill to convert from bliss .hdf5 to "
        "NXtomo compliant .nx file"
    )
    icon = "icons/datalistener.svg"
    priority = 10
    keywords = [
        "tomography",
        "file",
        "tomwer",
        "listener",
        "datalistener",
        "hdf5",
        "NXtomo",
    ]

    def __init__(self, host_discovery=None, parent=None):
        super().__init__(host_discovery=host_discovery, parent=parent, uses_rpc=True)

        # manage server stop when delete directly the widget or stop by Ctr+C
        signal.signal(signal.SIGINT, self.handleSigTerm)
        onDestroy = functools.partial(self._stopServerBeforeClosing)
        self.destroyed.connect(onDestroy)

    def delete_listening_thread(self):
        if self._listening_thread is not None:
            self._listening_thread.sigAcquisitionStarted.disconnect(
                self._widget._acquisitionStarted
            )
            self._listening_thread.sigAcquisitionEnded.disconnect(
                self._widget._acquisitionEnded
            )
            self._listening_thread.sigScanAdded.disconnect(
                self._widget._acquisitionUpdated
            )
            self._listening_thread.sigServerStop.disconnect(self._widget._serverStopped)
        DataListener.delete_listening_thread(self)

    def create_listening_thread(self):
        if self._mock is True:
            thread = MockDataListenerQThread(
                host=self.getHost(),
                port=self.getPort(),
                acquisitions=None,
                mock_acquisitions=self._mock_acquisitions,
            )
        else:
            thread = DataListenerQThread(
                host=self.getHost(), port=self.getPort(), acquisitions=None
            )
        # connect thread
        thread.sigAcquisitionStarted.connect(
            self._widget._acquisitionStarted, qt.Qt.DirectConnection
        )
        thread.sigAcquisitionEnded.connect(
            self._widget._acquisitionEnded, qt.Qt.DirectConnection
        )
        thread.sigScanAdded.connect(
            self._widget._acquisitionUpdated, qt.Qt.DirectConnection
        )
        thread.sigServerStop.connect(
            self._widget._serverStopped, qt.Qt.DirectConnection
        )
        return thread

    def _stopServerBeforeClosing(self):
        self.activate(False)

    def handleSigTerm(self, signo, *args, **kwargs):
        if signo == signal.SIGINT:
            self._stopServerBeforeClosing()
            sys.exit()

    def activate(self, activate=True, is_using_rpc=True):
        """Overwrite the activate to notify the user in case the port is occupy"""
        if activate and not self.is_port_available():
            with block_signals(self._widget):
                self._widget.activate(activate=False)
            dialog = PortOccupyDialog(parent=self, port=self.port, host=self.host)
            dialog.setModal(False)
            if dialog.exec() == qt.QDialog.Accepted:
                if dialog.retry_connection:
                    return self.activate(activate=True, is_using_rpc=is_using_rpc)
            else:
                return

        super().activate(activate=activate, is_using_rpc=is_using_rpc)
