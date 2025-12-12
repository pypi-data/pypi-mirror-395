# coding: utf-8
"""
data watcher classes used to define the status of an acquisition for EDF
acquisitions
"""
from __future__ import annotations

import logging

import h5py

from .datawatcherprocess import _DataWatcherProcess

_logger = logging.getLogger(__name__)


class _DataWatcherProcessHDF5(_DataWatcherProcess):
    """
    look for hdf5 information
    """

    def __init__(self, dataDir, srcPattern, destPattern):
        super(_DataWatcherProcessHDF5, self).__init__(dataDir, srcPattern, destPattern)
        if h5py.is_hdf5(dataDir):
            self._nxtomo_file = dataDir

    def _removeAcquisition(self, scanID, reason):
        _logger.warning(
            "removing acquisition is not done for hdf5 data watcher " "process"
        )

    def is_data_complete(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return True

    def is_abort(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return False


class _BlissScanWatcherProcess(_DataWatcherProcess):
    def __init__(self, dataDir, srcPattern=None, destPattern=None):
        super().__init__(dataDir, srcPattern, destPattern)
        if h5py.is_hdf5(dataDir):
            self._blissScanFile = dataDir

    def _removeAcquisition(self, scanID, reason):
        _logger.warning(
            "remoing acquisition is not done for hdf5 data watcher " "process"
        )

    def is_data_complete(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return True

    def is_abort(self):
        # For now data complete and is abort_is not handled for hdf5 and Nxtomo
        return False
