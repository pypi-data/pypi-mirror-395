# coding: utf-8
from __future__ import annotations


import logging
import socket

from ._QThreadListenerBase import QThreadListenerBase

_logger = logging.getLogger(__name__)

try:
    from blissdata.redis_engine.store import DataStore
    from blissdata.redis_engine.scan import ScanState
    from blissdata.beacon.data import BeaconData

    try:
        from blissdata.exceptions import NoScanAvailable
    except ImportError:
        from blissdata.redis_engine.exceptions import NoScanAvailable
except ImportError:
    _logger.warning("blissdata not installed. Cannot run the Blissdata Listener.")
    has_blissdata = False
else:
    has_blissdata = True


_logger = logging.getLogger(__name__)


class BlissDataListenerQThread(QThreadListenerBase):
    """Implementation of the _BaseDataListenerThread with a QThread.

    On this use case we use directly blissdata (requires Bliss version 2.0 or higher)

    # note: on bliss-tomo:
    # a sequence starts that triggers other scans.
    # then those scans starts and end...
    # and then only the parent sequence ends.
    # so the listener must be started before the sequence starts... which is already the case.

    ..warning:: this thread will never trigger 'sigScanAdded' or 'sigServerStop' as the first one is indeed never used at the moment and the second one is a specific feature for the json-rpc mechanism
    """

    def __init__(self, host, port, acquisitions):
        super().__init__(host=host, port=port, acquisitions=acquisitions)
        self._host = host
        self._port = port
        self._stop = False

        if not has_blissdata:
            raise RuntimeError("'blissdata' not installed. Cannot create the listener")

        try:
            self.createDataStore()
        except socket.gaierror as e:
            _logger.error(
                f"Fail to connect to host: {self._host}:{self._port}",
                exc_info=e,
                stack_info=True,
                stacklevel=3,
            )
            self._canConnect = False
        else:
            self._canConnect = True

    def createDataStore(self):
        self._beacon_client = BeaconData(host=self._host, port=self._port)
        self._redis_url = self._beacon_client.get_redis_data_db()
        self._data_store = DataStore(self._redis_url)

    def run(self):
        if not self._canConnect:
            return

        while not self._stop:
            try:
                _, key = self._data_store.get_next_scan(timeout=1)
            except (TimeoutError, NoScanAvailable):
                # not: Today the `NoScanAvailable` will be raised in case of a time out.
                continue
            except Exception as e:
                raise Exception("Failed to access next scan.") from e

            scan_sequence = self._data_store.load_scan(key)
            if not self.isBlissTomoScan(scan_sequence=scan_sequence):
                _logger.warning(
                    f"Scan {scan_sequence} is not recognized as a bliss-tomo acquisition. It will be ignored."
                )
                continue

            saving_file = scan_sequence.info["filename"]
            entry = scan_sequence.info["scan_nb"]
            proposal_file = scan_sequence.info["nexuswriter"]["masterfiles"]["proposal"]
            sample_file = scan_sequence.info["nexuswriter"]["masterfiles"][
                "dataset_collection"
            ]

            self.sigAcquisitionStarted.emit(
                (saving_file, entry, proposal_file, sample_file)
            )

            while scan_sequence.state < ScanState.CLOSED:
                if self._stop:
                    return
                scan_sequence.update()

            succeeded = scan_sequence.info["end_reason"] == "SUCCESS"
            self.sigAcquisitionEnded.emit(
                (saving_file, entry, proposal_file, sample_file, succeeded)
            )

    @staticmethod
    def isBlissTomoScan(scan_sequence) -> bool:
        """Check if the scan sequence is a bliss-tomo sequence"""
        tomo_config_group = scan_sequence.info.get("technique", {}).get(
            "tomoconfig", None
        )
        return tomo_config_group is not None

    def stop(self):
        self._stop = True
        self._beacon_client = None
        self._redis_url = None
        self._data_store = None
