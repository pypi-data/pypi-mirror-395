# coding: utf-8
from __future__ import annotations

import gc
import logging
import os
import shutil
import tempfile
import time

import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from orangecontrib.tomwer.widgets.reconstruction.DarkRefAndCopyOW import (
    DarkRefAndCopyOW,
)
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefsTask
from tomwer.core.process.reconstruction.darkref.params import ReduceMethod as DkrfMethod
from tomwer.core.process.reconstruction.darkref.settings import (
    DARKHST_PREFIX,
    REFHST_PREFIX,
)
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo
from tomwer.synctools.darkref import QDKRFRP

logging.disable(logging.INFO)


class TestEDFDarkRefWidget(TestCaseQt):
    """class testing the DarkRefWidget"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._recons_params = QDKRFRP()
        self.widget = DarkRefAndCopyOW(parent=None, reconsparams=self._recons_params)

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        self.qapp.processEvents()
        gc.collect()

    def testSyncRead(self):
        """Make sure any modification on the self._reconsParams is
        applied on the GUI"""
        rp = self._recons_params
        self.assertTrue(rp["REFSRMV"] is False)
        self.assertFalse(
            self.widget.widget.mainWidget.tabGeneral._rmOptionCB.isChecked()
        )
        rp["REFSRMV"] = True
        self.assertTrue(
            self.widget.widget.mainWidget.tabGeneral._rmOptionCB.isChecked()
        )

        pattern = self.widget.widget.mainWidget.tabExpert._refLE.text()
        newText = "popo.*"
        assert pattern != newText
        rp["RFFILE"] = newText
        self.assertTrue(
            self.widget.widget.mainWidget.tabExpert._refLE.text() == newText
        )

    def testSyncWrite(self):
        """Test that if we edit through the :class:`DarkRefWidget` then the
        modification are fall back into the self._reconsParams"""
        rp = self._recons_params

        # test patterns
        pattern = self.widget.widget.mainWidget.tabExpert._refLE.text()
        newText = "popo.*"
        assert pattern != newText
        self.widget.widget.mainWidget.tabExpert._refLE.setText(newText)
        self.widget.widget.mainWidget.tabExpert._refLE.editingFinished.emit()
        qt.QApplication.instance().processEvents()
        self.assertTrue(rp["RFFILE"] == newText)
        self.widget.widget.mainWidget.tabExpert._darkLE.setText(newText)
        self.widget.widget.mainWidget.tabExpert._darkLE.editingFinished.emit()
        qt.QApplication.instance().processEvents()
        self.assertTrue(rp["DKFILE"] == newText)

        # test calc mode
        self.widget.widget.mainWidget.tabGeneral._darkWCB.setMode(DkrfMethod.NONE)
        self.widget.widget.mainWidget.tabGeneral._refWCB.setMode(DkrfMethod.MEDIAN)
        self.assertTrue(rp["DARKCAL"] == DkrfMethod.NONE)
        self.assertTrue(rp["REFSCAL"] == DkrfMethod.MEDIAN)

        # test options
        cuRm = self.widget.widget.mainWidget.tabGeneral._rmOptionCB.isChecked()
        self.widget.widget.mainWidget.tabGeneral._rmOptionCB.setChecked(not cuRm)
        self.assertTrue(rp["REFSRMV"] == (not cuRm))
        self.assertTrue(rp["DARKRMV"] == (not cuRm))

        cuSkip = self.widget.widget.mainWidget.tabGeneral._skipOptionCB.isChecked()
        self.widget.widget.mainWidget.tabGeneral._skipOptionCB.setChecked(not cuSkip)
        # warning : here value of skip and overwrite are of course inverse
        self.assertTrue(rp["DARKOVE"] == cuSkip)
        self.assertTrue(rp["REFSOVE"] == cuSkip)


@pytest.mark.skip("Fail on CI")
class TestDarkRefCopyWithEDFAndHDF5(TestCaseQt):
    """Test the DarkRefCopy orange widget behaviour"""

    def setUp(self) -> None:
        TestCaseQt.setUp(self)
        self._folder = tempfile.mkdtemp()

        # define scans to be treated
        hdf5_mock_with_refs = MockNXtomo(
            scan_path=os.path.join(self._folder, "h5_with_refs"),
            n_proj=10,
            n_ini_proj=10,
            dim=20,
            create_ini_flat=True,
            create_ini_dark=True,
            create_final_flat=False,
        )
        self.hdf5_acquisition_with_refs = hdf5_mock_with_refs.scan

        hdf5_mock_without_refs = MockNXtomo(
            scan_path=os.path.join(self._folder, "h5_without_refs"),
            n_proj=10,
            n_ini_proj=10,
            dim=20,
            create_ini_flat=False,
            create_ini_dark=False,
        )
        self.hdf5_acquisition_without_refs = hdf5_mock_without_refs.scan

        hdf5_mock_without_refs_incoherent_dim = MockNXtomo(
            scan_path=os.path.join(self._folder, "h5_without_refs_different_dim"),
            n_proj=10,
            n_ini_proj=10,
            dim=21,
            create_ini_flat=False,
            create_ini_dark=False,
        )
        self.hdf5_acquisition_without_refs_incoherent_dim = (
            hdf5_mock_without_refs_incoherent_dim.scan
        )

        edf_mock_without_ref = MockEDF(
            scan_path=os.path.join(self._folder, "edf_without_refs"), dim=20, n_radio=20
        )
        self.edf_acquisition_without_ref = EDFTomoScan(
            scan=edf_mock_without_ref.scan_path
        )

        # processes set up
        self._recons_params = QDKRFRP()
        self.widget = DarkRefAndCopyOW(parent=None, reconsparams=self._recons_params)
        self.widget.setForceSync(True)
        self.widget.show()

    def tearDown(self) -> None:
        time.sleep(0.5)
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self._folder)
        gc.collect()

    def testCopyInactive(self):
        self.widget.setCopyActive(False)

        self.widget.process(self.hdf5_acquisition_with_refs)

        # make sure no dark or flats exists for the hdf5 without refs
        for scan in (
            self.hdf5_acquisition_without_refs_incoherent_dim,
            self.hdf5_acquisition_without_refs,
        ):
            self.widget.process(scan)

        # make sure no dark or flats exists for the edf one
        self.widget.process(self.edf_acquisition_without_ref)

    def testCopyActive(self):
        self.widget.setCopyActive(True)
        self.widget.setModeAuto(True)

        self.widget.process(self.hdf5_acquisition_with_refs)
        # 1. make sure dark has been processed for the one with ref
        self.assertTrue(self.widget.hasDarkStored())
        self.assertTrue(self.widget.hasFlatStored())

        # 2. make sure copy has been processed for the the 'compatible hdf5'
        self.widget.process(self.hdf5_acquisition_without_refs)

        # 3. make sure copy has been processed for the the 'compatible edf'
        self.widget.process(self.edf_acquisition_without_ref)
        self.assertEqual(
            len(
                DarkRefsTask.getRefHSTFiles(
                    self.edf_acquisition_without_ref.path, prefix=REFHST_PREFIX
                )
            ),
            2,
        )
        self.assertEqual(
            len(
                DarkRefsTask.getDarkHSTFiles(
                    self.edf_acquisition_without_ref.path, prefix=DARKHST_PREFIX
                )
            ),
            1,
        )

        # 4. make sure process but no copy made if incompatible size
        self.widget.process(self.hdf5_acquisition_without_refs_incoherent_dim)
