import gc
import logging
import os
import pickle
import shutil
import tempfile
import time
from glob import glob

import h5py
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt
from nxtomo.nxobject.nxdetector import FOV

from orangecontrib.tomwer.widgets.reconstruction.NabuOW import NabuOW
from tomwer.core.process.reconstruction.nabu.utils import _NabuMode
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.settings import mock_lsbram
from tomwer.core.utils.lbsram import mock_low_memory
from tomwer.synctools.darkref import QDKRFRP
from tomwer.tests.datasets import TomwerCIDatasets

logging.disable(logging.INFO)


class TestNabuWidget(TestCaseQt):
    """class testing the NabuOW"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self._recons_params = QDKRFRP()
        self.widget = NabuOW(parent=None)
        self.scan_dir = tempfile.mkdtemp()
        # create dataset
        self.master_file = os.path.join(self.scan_dir, "frm_edftomomill_twoentries.nx")
        shutil.copyfile(
            TomwerCIDatasets.get_dataset(
                "h5_datasets/frm_edftomomill_twoentries.nx",
            ),
            self.master_file,
        )
        self.scan = NXtomoScan(scan=self.master_file, entry="entry0000")
        # create listener for the nabu widget
        self.signal_listener = SignalListener()

        # connect signal / slot
        self.widget.sigScanReady.connect(self.signal_listener)

        # set up
        mock_low_memory(True)
        mock_lsbram(True)
        self.widget.setDryRun(dry_run=True)

    def tearDown(self):
        mock_low_memory(False)
        mock_lsbram(False)
        self.widget.sigScanReady.disconnect(self.signal_listener)
        self._recons_params = None
        self.scan = None
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        gc.collect()

    def test_serializing(self):
        pickle.dumps(self.widget.getConfiguration())

    def test_literal_dumps(self):
        literal_dumps(self.widget.getConfiguration())

    def testLowMemory(self):
        """Make sure no reconstruction is started if we are low in memory in
        lbsram"""
        self.assertEqual(len(glob(os.path.join(self.scan_dir, "*.cfg"))), 0)
        self.widget.process(self.scan)
        self.wait_processing()
        self.assertEqual(len(glob(os.path.join(self.scan_dir, "*.cfg"))), 0)

    def wait_processing(self):
        timeout = 10
        while timeout >= 0 and self.signal_listener.callCount() == 0:
            timeout -= 0.1
            time.sleep(0.1)
        if timeout <= 0.0:
            raise TimeoutError("nabu widget never end processing")

    def patch_fov(self, value: str):
        with h5py.File(self.scan.master_file, mode="a") as h5s:
            for entry in ("entry0000", "entry0001"):
                entry_node = h5s[entry]
                if "instrument/detector/field_of_view" in entry_node:
                    del entry_node["instrument/detector/field_of_view"]
                entry_node["instrument/detector/field_of_view"] = value

    def testSetConfiguration(self):
        """Make sure the configuration evolve from scan information"""
        self.assertEqual(self.widget.getMode(), _NabuMode.FULL_FIELD)
        self.patch_fov(value=FOV.HALF.value)
        self.widget.process(self.scan)
        self.wait_processing()
        self.assertEqual(self.widget.getMode(), _NabuMode.HALF_ACQ)
        self.patch_fov(value=FOV.FULL.value)
        self.scan.clear_cache()
        self.widget.process(self.scan)
        self.wait_processing()
        self.assertEqual(self.widget.getMode(), _NabuMode.FULL_FIELD)
