# coding: utf-8
from __future__ import annotations

import gc
import os
import shutil
import tempfile
import time

from orangecanvas.scheme.readwrite import literal_dumps
from processview.core.manager.manager import DatasetState, ProcessManager
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomoscan.esrf.scan.mock import MockEDF

from orangecontrib.tomwer.widgets.control.EDF2NXTomomillOW import EDF2NXOW
from orangecontrib.tomwer.widgets.control.NXTomomillOW import NXTomomillOW
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import MockBlissAcquisition


class TestNXTomomillOw(TestCaseQt):
    """
    Test the NXTomomillOW widget
    """

    def setUp(self):
        super().setUp()
        self.tempdir = tempfile.mkdtemp()
        mock = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=3,
            n_darks=2,
            n_flats=2,
            output_dir=self.tempdir,
        )
        self.scan = BlissScan(
            master_file=mock.samples[0].sample_file,
            proposal_file=mock.proposal_file,
            entry="1.1",
        )
        self.widget = NXTomomillOW()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.tempdir)
        gc.collect()

    def test(self):
        self.widget.add(self.scan.master_file)
        self.widget._sendAll()

    def test_literal_dumps(self):
        self.widget._saveNXTomoCfgFile(cfg_file="")
        literal_dumps(self.widget._ewoks_default_inputs)


class TestEDF2NXOW(TestCaseQt):
    """
    Test the EDF2NXOW widget
    """

    def setUp(self):
        super().setUp()
        self.tempdir = tempfile.mkdtemp()
        self._edf_folder_1 = os.path.join(self.tempdir, "edf_scan_1")
        self._edf_folder_2 = os.path.join(self.tempdir, "edf_scan_2_")
        MockEDF(
            scan_path=self._edf_folder_1,
            n_radio=10,
            n_ini_radio=10,
            n_extra_radio=0,
            dim=128,
            dark_n=1,
            flat_n=1,
        )
        MockEDF(
            scan_path=self._edf_folder_2,
            n_radio=10,
            n_ini_radio=10,
            n_extra_radio=0,
            dim=128,
            dark_n=1,
            flat_n=1,
        )
        self.widget = EDF2NXOW()
        self._process_manager = ProcessManager()

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self.tempdir)
        gc.collect()

    def test(self):
        self.widget.add(self._edf_folder_1)
        self.widget.add(self._edf_folder_2)
        self.widget._sendAll()
        self.qapp.processEvents()
        timeout = 10
        processing_queue = self.widget.task_executor_queue
        while not processing_queue.is_available and not processing_queue.empty():
            self.qapp.processEvents()
            time.sleep(0.1)
            timeout -= 0.1
            if timeout <= 0:
                raise TimeoutError
        # need to call one more time the processEvents tpo call callbacks and status notification
        for i in range(3):
            self.qapp.processEvents()
            time.sleep(0.1)

        # check the two output files exists and status of the processing is done...
        for folder in (self._edf_folder_1, self._edf_folder_2):
            scan = NXtomoScan(scan=folder + ".nx", entry="entry")
            self.assertTrue(os.path.exists(scan.master_file))

            self.assertEqual(
                self._process_manager.get_dataset_state(
                    dataset_id=scan.get_identifier(),
                    process=self.widget,
                ),
                DatasetState.SUCCEED,
            )

    def test_literal_dumps(self):
        self.widget._saveNXTomoCfgFile(cfg_file="")
        literal_dumps(self.widget._ewoks_default_inputs)
