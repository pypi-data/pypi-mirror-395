from __future__ import annotations

from silx.gui import qt


class QThreadListenerBase(qt.QThread):
    """
    This class defines the API for a QThread listening to blissdata.

    Interface is defined by signals emitted and the constructor signature.
    The goal is to be able to connect it with the DataListenerWidget
    """

    sigAcquisitionStarted = qt.Signal(tuple)
    """Signal emitted when an acquisition is started. Tuple is:
    (master_file, master_entry)"""
    sigAcquisitionEnded = qt.Signal(tuple)
    """Signal emitted when an acquisition is ended. Tuple is
    (master_file, master_entry, succeed)"""
    sigScanAdded = qt.Signal(tuple)
    """Signal emitted when a scan is added to an acquisition. Tuple is
    (master_file, master_entry, scan_entry)"""
    sigServerStop = qt.Signal()
    """Signal if the rpc-server have been turn off"""

    def __init__(self, host, port, acquisitions):
        super().__init__()

    def join(self, timeout=None):
        if timeout is None:
            self.wait()
        else:
            self.wait(timeout)

    def stop(self):
        raise NotImplementedError("Base class")
