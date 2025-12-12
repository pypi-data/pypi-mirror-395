from __future__ import annotations

import signal

from silx.gui import qt
from tomwer.core.utils.process import send_signal_to_local_rpc_servers


class PortOccupyDialog(qt.QDialog):
    """Widget for the user to send a sig kill / sig term to the port listening to bliss-tomo TomoSync json-rpc code"""

    def __init__(self, parent, port, host):
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._retry = False
        self.port = port
        self.host = host

        mess = (
            f"port ({port}) of {host} already in use. \n Maybe an other "
            "instance of `datalistener` is running in this session or "
            "another tomwer session. \n As this widget is connecting with "
            "bliss we enforce it to be unique."
        )
        self.layout().addWidget(qt.QLabel(mess, self))
        self.setWindowTitle("Unable to launch two listener in parallel")

        types = qt.QDialogButtonBox.Cancel | qt.QDialogButtonBox.Retry
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        self._sendSIGTERMMsb = qt.QPushButton("send SIGTERM", self)
        self._sendSIGTERMMsb.setToolTip(
            "Try to send SIGTERM signal to the "
            "local tomwer-rpcserver if any "
            "occupies the reserved port"
        )
        self._buttons.addButton(self._sendSIGTERMMsb, qt.QDialogButtonBox.ActionRole)
        self._sendSIGKILLMsb = qt.QPushButton("send SIGKILL", self)
        self._sendSIGKILLMsb.setToolTip(
            "Try to send SIGKILL signal to the "
            "local tomwer-rpcserver if any "
            "occupies the reserved port"
        )
        self._buttons.addButton(self._sendSIGKILLMsb, qt.QDialogButtonBox.ActionRole)

        # set up
        # for now we don't want to show "send signal" feature
        self._sendSIGTERMMsb.hide()
        self._sendSIGKILLMsb.hide()

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Cancel).released.connect(self.reject)
        self._buttons.button(qt.QDialogButtonBox.Retry).released.connect(
            self._retry_connect
        )
        self._sendSIGTERMMsb.released.connect(self._emitSigterm)
        self._sendSIGKILLMsb.released.connect(self._emitSigkill)

    @property
    def retry_connection(self):
        return self._retry

    def _emitSigterm(self, *args, **kwargs):
        send_signal_to_local_rpc_servers(signal.SIGTERM, port=self.port)

    def _emitSigkill(self, *args, **kwargs):
        send_signal_to_local_rpc_servers(signal.SIGKILL, port=self.port)

    def _retry_connect(self, *args, **kargs):
        self._retry = True
        self.accept()
