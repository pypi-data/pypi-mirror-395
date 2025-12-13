# coding: utf-8
from __future__ import annotations

import logging
import os
from fnmatch import fnmatch

import h5py
from silx.gui import qt

from tomwer.core.process.control.datawatcher import status as datawatcherstatus
from tomwer.core.process.control.datawatcher.datawatcherobserver import (
    _DataWatcherObserver_MixIn,
    _DataWatcherStaticObserverMixIn,
    _OngoingObservation,
)
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory

logger = logging.getLogger(__name__)


class _QDataWatcherObserver(_DataWatcherObserver_MixIn, qt.QThread):
    """
    DatWatcherObserver implementation with a qt.QThread

    We have two implementations in order to avoid hard dependancy on qt for
    tomwer.core package
    """

    sigScanReady = qt.Signal(object)
    """emit when scan ready"""

    def __init__(
        self,
        obsMethod,
        observationClass,
        headDir=None,
        startByOldest=False,
        srcPattern=None,
        destPattern=None,
        ignoredFolders=None,
        file_name_pattern=None,
    ):
        qt.QThread.__init__(self)
        _DataWatcherObserver_MixIn.__init__(
            self,
            obsMethod=obsMethod,
            observationClass=observationClass,
            headDir=headDir,
            startByOldest=startByOldest,
            srcPattern=srcPattern,
            destPattern=destPattern,
            ignoredFolders=ignoredFolders,
            time_between_loops=0.2,
            file_name_pattern=file_name_pattern,
        )
        self.observations.sigScanReady.connect(self._signalScanReady)

    def _signalScanReady(self, scan):
        assert isinstance(scan, (TomwerScanBase, BlissScan))
        self.sigScanReady.emit(scan)

    def _getObserver(self, scanID):
        return _QDataWatcherStaticObserver(
            scanID=scanID,
            obsMethod=self.obsMethod,
            srcPattern=self.srcPattern,
            destPattern=self.destPattern,
            patternObs=self._patternObs,
            observationRegistry=self.observations,
        )

    def run(self):
        look_for_hdf5_file = self.obsMethod in (
            datawatcherstatus.BLISS_SCAN_END,
            datawatcherstatus.NXtomo_END,
        )

        def process(file_path):
            do_observation = (
                self.observations.isObserving(file_path) is False
                and (
                    (look_for_hdf5_file and h5py.is_hdf5(file_path))
                    or (self.dataWatcherProcess._isScanDirectory(file_path))
                )
                and file_path not in self.observations.ignoredFolders
            )
            if (
                do_observation
                and self.file_name_pattern is not None
                and not fnmatch(os.path.basename(file_path), self.file_name_pattern)
            ):
                do_observation = False
            if do_observation is True:
                # do the observation
                self.observe(file_path)

            if os.path.isdir(file_path):
                try:
                    for f in os.listdir(file_path):
                        full_file_path = os.path.join(file_path, f)
                        if os.path.isdir(full_file_path) or (
                            look_for_hdf5_file and h5py.is_hdf5(full_file_path)
                        ):
                            process(full_file_path)
                except Exception:
                    pass

        if not os.path.isdir(self.headDir):
            logger.warning("can't observe %s, not a directory" % self.headDir)
            return
        self.dataWatcherProcess = self._getDataWatcherProcess()
        process(self.headDir)

        self._processObservation()

    def waitForObservationFinished(self, timeOut=10):
        threads = list(self.observations.dict.values())
        for thread in threads:
            thread.wait(timeOut)

    def wait(self, *args, **kwargs):
        self.waitForObservationFinished()
        super(_QDataWatcherObserver, self).wait(*args, **kwargs)


class _QOngoingObservation(_OngoingObservation, qt.QObject):
    """
    _OngoingObservation with a QObject and signals for each event
    """

    sigScanReady = qt.Signal(object)
    """Emitted when a finished acquisition is detected"""
    sigObsAdded = qt.Signal(str)
    """Signal emitted when an observation is added"""
    sigObsRemoved = qt.Signal(str)
    """Signal emitted when an observation is removed"""
    sigObsStatusReceived = qt.Signal(str, str)
    """Signal emitted when receiving a new observation status"""

    def __init__(self):
        qt.QObject.__init__(self)
        _OngoingObservation.__init__(self)

    def _acquisition_ended(self, scanID):
        _OngoingObservation._acquisition_ended(self, scanID=scanID)
        try:
            scans = ScanFactory.create_scan_objects(
                scan_path=scanID, accept_bliss_scan=True
            )
        except Exception as e:
            logger.error(f"Fail to create TomoBase instance from {scanID} Error is {e}")
        else:
            for scan in scans:
                self.sigScanReady.emit(scan)

    def add(self, observer):
        already_observing = self.isObserving(observer.path)
        _OngoingObservation.add(self, observer=observer)
        if not already_observing:
            observer.sigStatusChanged.connect(self._updateStatus)
            self.sigObsAdded.emit(observer.path)

    def remove(self, observer):
        observing = self.isObserving(observer.path)
        _OngoingObservation.remove(self, observer=observer)
        if observing is True:
            observer.sigStatusChanged.disconnect(self._updateStatus)
            self.sigObsRemoved.emit(observer.path)

    def _updateStatus(self, status, scan):
        if self.isObserving(scan) is True:
            self.sigObsStatusReceived.emit(
                scan, datawatcherstatus.DICT_OBS_STATUS[status]
            )
        _OngoingObservation._updateStatus(self, status=status, scan=scan)

    def reset(self):
        # self.ignoreFolders = []
        for scanID, observer in self.dict:
            observer.sigStatusChanged.disconnect(self._updateStatus)
            observer.quit()
        self.dict = {}


class _QDataWatcherStaticObserver(_DataWatcherStaticObserverMixIn, qt.QThread):
    """
    Implementation of the _DataWatcherFixObserverMixIn with a qt.QThread
    """

    sigStatusChanged = qt.Signal(int, str)
    """signal emitted when the status for a specific directory change
    """

    def __init__(
        self,
        scanID,
        obsMethod,
        srcPattern,
        destPattern,
        patternObs,
        observationRegistry,
    ):
        qt.QThread.__init__(self)
        _DataWatcherStaticObserverMixIn.__init__(
            self,
            scanID=scanID,
            obsMethod=obsMethod,
            srcPattern=srcPattern,
            destPattern=destPattern,
            patternObs=patternObs,
            observationRegistry=observationRegistry,
        )

    def run(self):
        look_for_hdf5_file = self.obsMethod in (
            datawatcherstatus.BLISS_SCAN_END,
            datawatcherstatus.NXtomo_END,
        )
        if not look_for_hdf5_file and not os.path.isdir(self.path):
            logger.info("can't observe %s, not a directory" % self.path)
            self.status = "failure"
            self.sigStatusChanged.emit(
                datawatcherstatus.OBSERVATION_STATUS[self.status], self.path
            )
            self.validation = -1
            return

        try:
            scans = ScanFactory.create_scan_objects(
                scan_path=self.path, accept_bliss_scan=True
            )
        except ValueError as e:
            logger.error(e)
        else:
            for scan in scans:
                if scan.is_abort(
                    src_pattern=self.srcPattern, dest_pattern=self.destPattern
                ):
                    if self.status != "aborted":
                        logger.info("Acquisition %s has been aborted" % self.path)
                        self.dataWatcherProcess._removeAcquisition(
                            scanID=self.path, reason="acquisition aborted by the user"
                        )

                        self.status = "aborted"
                    self.sigStatusChanged.emit(
                        datawatcherstatus.OBSERVATION_STATUS[self.status], self.path
                    )
                    self.validation = -2
                    return
                dataComplete = self.dataWatcherProcess.is_data_complete()

                if dataComplete is True:
                    self.status = "acquisition ended"
                    self.sigStatusChanged.emit(
                        datawatcherstatus.OBSERVATION_STATUS[self.status], self.path
                    )
                    self.validation = 1
                else:
                    self.status = "waiting for acquisition ending"
                    self.sigStatusChanged.emit(
                        datawatcherstatus.OBSERVATION_STATUS[self.status], self.path
                    )
                    self.validation = 0
        return
