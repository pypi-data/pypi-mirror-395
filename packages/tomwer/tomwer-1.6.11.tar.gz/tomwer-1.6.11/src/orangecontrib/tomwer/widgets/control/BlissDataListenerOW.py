from __future__ import annotations

import logging

from ._DataListenerBaseClass import DataListenerBaseClass
from tomwer.core.process.control.datalistener import DataListener
from tomwer.synctools.bliss_sync.blissdata_listener import BlissDataListenerQThread


_logger = logging.getLogger(__name__)


class BlissDataListenerOW(DataListenerBaseClass):
    """
    This widget is used to listen to blissdata at a specific BEACON_HOST
    """

    name = "Blissdata Listener"
    id = "orangecontrib.widgets.tomwer.control.BlissDataListenerOW.BlissDataListenerOW"
    description = (
        "The widget will listen to bliss data in order to retrieve on-going (tomo) bliss-sequence.\n"
        "It must ne started **before** the bliss scan starts.\n"
        "Once the bliss sequence is finished it will be converted to NXtomo(s)"
    )
    icon = "icons/blissdata_listener.svg"
    priority = 10
    keywords = [
        "bliss data",
        "blissdata",
        "tomography",
        "tomwer",
        "listener",
        "datalistener",
        "hdf5",
        "NXtomo",
    ]

    def __init__(self, host_discovery="BEACON_HOST", parent=None):
        super().__init__(host_discovery=host_discovery, parent=parent, uses_rpc=False)
        self._widget.setHostAndPortToolTip(
            "Host and port must be defined from the 'BEACON_HOST' environment before launching the canvas.\nLike for example: `export BEACON_HOST=id00:25000`"
        )

    def delete_listening_thread(self):
        if self._listening_thread is not None:
            self._listening_thread.sigAcquisitionStarted.disconnect(
                self._widget._acquisitionStarted
            )
            self._listening_thread.sigAcquisitionEnded.disconnect(
                self._widget._acquisitionEnded
            )
        DataListener.delete_listening_thread(self)

    def create_listening_thread(self):
        try:
            thread = BlissDataListenerQThread(
                host=self.getHost(), port=self.getPort(), acquisitions=None
            )
        except ConnectionRefusedError:
            _logger.error(self._getErrorMsg(ConnectionRefusedError))
            return None
        except TimeoutError:
            _logger.error(self._getErrorMsg(TimeoutError))
            return None

        # connect thread
        thread.sigAcquisitionStarted.connect(self._widget._acquisitionStarted)
        thread.sigAcquisitionEnded.connect(self._widget._acquisitionEnded)

        return thread

    def _getErrorMsg(self, exception_type):
        return f"Unable to create Blissdata Listener widget. - {exception_type}. Please check that the host and the port are correct from the BEACON_HOST environment variable"
