# coding: utf-8
from __future__ import annotations

import logging

from ewokscore.task import Task as EwoksTask

from tomwer.core import settings
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.core.process.task import BaseProcessInfo
from tomwer.core.scan.scanbase import TomwerScanBase, _TomwerBaseDock
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.signal import Signal
from tomwer.core.utils import logconfig
from tomwer.core.utils.scanutils import data_identifier_to_scan

logger = logging.getLogger(__name__)


class _ScanValidatorPlaceHolder(EwoksTask, input_names=["data"], output_names=["data"]):
    def run(self):
        self.outputs.data = data_identifier_to_scan(self.inputs.data)


class ScanValidator(BaseProcessInfo):
    """
    Simple workflow locker until the use validate scans

    :param memReleaserWaitLoop: the time to wait in second between two
                                    memory overload if we are in lbsram.
    """

    def __init__(self, memoryReleaser):
        super().__init__()
        self._manualValidation = True
        self._hasToLimitScanBlock = settings.isOnLbsram()
        self._memoryReleaser = memoryReleaser
        self._scans = {}
        """associate scanId (keys) to :class:`.TomoBase` object (value)"""

        # add callback _loopMemoryReleaserto free memory if necessary on lbsram
        if self._hasToLimitScanBlock:
            self._memoryReleaser.finished.connect(self._loopMemoryReleaser)
            self._memoryReleaser.start()

    def __del__(self):
        self._clearMemoryReleaser()

    def _clearMemoryReleaser(self):
        if self._memoryReleaser is not None:
            self._memoryReleaser.should_be_stopped = True
            self._memoryReleaser.wait(4000)
            self._memoryReleaser = None

    def addScan(self, scan):
        """
        Return the index on the current orderred dict

        :param scan:
        :return:
        """
        _ftserie = scan
        if type(scan) is str:
            _ftserie = ScanFactory.create_scan_object(_ftserie)
        logger.info(f"Scan {_ftserie} has been added by the Scan validator")

        self._scans[str(_ftserie)] = _ftserie

        index = len(self._scans) - 1

        self._freeStackIfNeeded()
        return index

    def _freeStackIfNeeded(self):
        # if we are low in memory in lbsram: we will automatically validate the current scan
        isLowMemoryLbs = is_low_on_memory(settings.get_lbsram_path()) is True
        if not self.isValidationManual():
            self._validateStack()
        elif isLowMemoryLbs:
            mess = "low memory, free ScanValidator stack "
            logger.processSkipped(mess)
            self._validateStack(filter_="lbsram")

    def _loopMemoryReleaser(self):
        """
        simple loop using the _memoryReleaser and calling the
        _freeStackIfNeeded function
        """
        self._freeStackIfNeeded()
        if self._memoryReleaser and not hasattr(
            self._memoryReleaser, "should_be_stopped"
        ):
            self._memoryReleaser.start()

    def _validateStack(self, filter_=None):
        """
        :param filter: can be None or 'lbsram' if lbsram will only free scan
                       located on lbsram.
        Validate all the scans in the stack.
        """
        for scanID in list(self._scans.keys()):
            scan = self._scans[scanID]
            if filter_ is None or settings.isOnLbsram(scan):
                self._validated(scan)

    def _validateScan(self, scan):
        """This will validate the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scan is not None:
            assert isinstance(scan, TomwerScanBase)
            self._validated(scan)

    def _cancelScan(self, scan):
        """This will cancel the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scan is not None:
            assert isinstance(scan, TomwerScanBase)
            self._canceled(scan)

    def _redoAcquisitionScan(self, scan):
        """This will emit a signal to request am acquisition for the current
        ftSerieReconstruction

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate.
            Execution order in this case is not insured.
        """
        if scan is not None:
            assert isinstance(scan, TomwerScanBase)
            self._redoacquisition(scan)

    # ------ callbacks -------
    def _validated(self, scan):
        """Callback when the validate button is pushed"""
        if scan is not None:
            assert isinstance(scan, TomwerScanBase)
            info = f"{str(scan)} has been validated"
            logger.processEnded(
                info,
                extra={
                    logconfig.DOC_TITLE: self._scheme_title,
                    logconfig.SCAN_ID: str(scan),
                },
            )
            self._sendScanReady(scan)
            # in some case the scan can not be in the _scans
            # (if the signal) come from an other window that 'scan to treat'
            if str(scan) in self._scans:
                del self._scans[str(scan)]

    def _canceled(self, scan):
        """Callback when the cancel button is pushed"""
        if scan is not None:
            assert isinstance(scan, TomwerScanBase)
            info = "%s has been canceled" % str(scan)
            logger.processEnded(
                info,
                extra={
                    logconfig.DOC_TITLE: self._scheme_title,
                    logconfig.SCAN_ID: str(scan),
                },
            )
            self._sendScanCanceledAt(scan)
            # in some case the scan can not be in the _scans
            # (if the signal) come from an other window that 'scan to treat'
            if str(scan) in self._scans:
                del self._scans[str(scan)]
            self.clear()

    def _redoacquisition(self, ftserie):
        """Callback when the redo acquisition button is pushed"""
        raise NotImplementedError("_redoacquisition not implemented yet")

    def _changeReconsParam(self, ftserie):
        """Callback when the change reconstruction button is pushed"""
        if ftserie is None:
            return

        _ftserie = ftserie
        if type(ftserie) is str:
            _ftserie = ScanFactory.create_scan_object(_ftserie)

        if _ftserie.path in self._scans:
            del self._scans[str(_ftserie)]
        self._sendUpdateReconsParam(_TomwerBaseDock(tomo_instance=_ftserie))

    def setManualValidation(self, b):
        """if the validation mode is setted to manual then we will wait for
        user approval before validating. Otherwise each previous and next scan
        will be validated

        :paramean b: False if we want an automatic validation
        """
        self._manualValidation = b
        if not self.isValidationManual():
            self._validateStack()

    def isValidationManual(self):
        """

        :return: True if the validation is waiting for user interaction,
                 otherwise False
        """
        return self._manualValidation

    def _sendScanReady(self, scan):
        raise RuntimeError("ScanValidator is a pure virtual class.")

    def _sendScanCanceledAt(self, scan):
        raise RuntimeError("ScanValidator is a pure virtual class.")

    def _sendUpdateReconsParam(self, scan):
        raise RuntimeError("ScanValidator is a pure virtual class.")

    def clear(self):
        scans = list(self._scans.values())
        # need to be copy because cancel will update self._scans
        for scan in scans:
            self._cancelScan(scan=scan)


class ScanValidatorP(ScanValidator):
    """
    For now to avoid multiple inheritance from QObject with the process widgets
    we have to define two classes. One only for the QObject inheritance.

    :param memReleaserWaitLoop: the time to wait in second between two
                                    memory overload if we are in lbsram.
    """

    scanReady = Signal(TomwerScanBase)
    """Signal emitted when a scan is ready"""
    scanCanceledAt = Signal(str)
    """Signal emitted when a scan has been canceled"""
    updateReconsParam = Signal(TomwerScanBase)
    """Signal emitted when a scan need to be reconstructed back with new
    parameters"""

    def __init__(self, memoryReleaser=None):
        ScanValidator.__init__(self, memoryReleaser)

    def _sendScanReady(self, scan):
        self.scanReady.emit(scan)

    def _sendScanCanceledAt(self, scan):
        self.scanCanceledAt.emit(scan)

    def _sendUpdateReconsParam(self, scan):
        self.updateReconsParam.emit(scan)
