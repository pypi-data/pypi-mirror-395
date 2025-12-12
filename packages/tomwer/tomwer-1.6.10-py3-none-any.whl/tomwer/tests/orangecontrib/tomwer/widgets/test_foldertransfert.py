# coding: utf-8
from __future__ import annotations


import gc
import logging
import os
import shutil
import tempfile
import time
from glob import glob

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.control.DataTransfertOW import DataTransfertOW
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.scanutils import MockEDF

logging.disable(logging.INFO)


class TestEDFFolderTransfertWidget(TestCaseQt):
    """class testing the DataTransfertOW within an EDF acquisition"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self.n_file = 10
        self.sourcedir = tempfile.mkdtemp()
        os.makedirs(self.sourcedir, exist_ok=True)
        self.targettedir = tempfile.mkdtemp()
        os.makedirs(self.targettedir, exist_ok=True)
        MockEDF.fastMockAcquisition(self.sourcedir, n_radio=self.n_file)
        self.scan = ScanFactory.create_scan_object(self.sourcedir)

        self.folderTransWidget = DataTransfertOW()
        self.folderTransWidget.turn_off_print = True
        self.folderTransWidget.setDestDir(self.targettedir)
        self.folderTransWidget._copying = False
        self.folderTransWidget.setForceSync(True)

    def tearDown(self):
        self.folderTransWidget.settingsHandler.removeCallback(
            self.folderTransWidget._updateSettingsVals
        )
        self.folderTransWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.folderTransWidget.close()
        self.folderTransWidget = None

        if os.path.isdir(self.sourcedir):
            shutil.rmtree(self.sourcedir)
        if os.path.isdir(self.targettedir):
            shutil.rmtree(self.targettedir)
        gc.collect()

    def testMoveFiles(self):
        """
        simple test that files are correctly moved
        """
        self.folderTransWidget._process(self.scan, move=True, noRsync=True)

        outputdir = os.path.join(self.targettedir, os.path.basename(self.sourcedir))
        timeout = 1
        while (
            (os.path.isdir(self.sourcedir))
            and timeout > 0
            or self.folderTransWidget.isCopying()
        ):
            timeout = timeout - 0.1
            time.sleep(0.1)
            self.qapp.processEvents()

        self.assertTrue(os.path.isdir(outputdir))
        self.assertTrue(self.checkDataCopied())

    def testCopyFiles(self):
        """
        Simple test that file are copy and deleted
        """
        self.folderTransWidget._process(self.scan, move=False, noRsync=True)

        timeout = 1
        outputdir = os.path.join(self.targettedir, os.path.basename(self.sourcedir))
        while (
            os.path.isdir(self.sourcedir) and timeout > 0
        ) or self.folderTransWidget.isCopying():
            timeout = timeout - 0.1
            time.sleep(0.1)
            self.qapp.processEvents()

        time.sleep(1)

        self.assertTrue(os.path.isdir(outputdir))
        self.assertTrue(self.checkDataCopied())

    def checkDataCopied(self):
        outputdir = os.path.join(self.targettedir, os.path.basename(self.sourcedir))
        outputFiles = os.listdir(outputdir)
        inputFile = glob(self.sourcedir)

        return (
            (len(inputFile) == 0)
            and (len(outputFiles) == (self.n_file + 2))
            and (not os.path.isdir(self.sourcedir))
        )
