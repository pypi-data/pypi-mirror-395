# coding: utf-8
from __future__ import annotations

import asyncio
import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.gui.cluster.supervisor import FutureTomwerScanObserverWidget


class TestSupervisor(TestCaseQt):
    """Test the supervisor GUI"""

    def setUp(self):
        super().setUp()
        self.tempdir = tempfile.mkdtemp()

        # set up scans
        self._scans = []
        self._future_tomo_objs = []
        for i in range(5):
            # create scan
            scan = MockNXtomo(
                scan_path=os.path.join(self.tempdir, f"scan_test{i}"),
                n_proj=10,
                n_ini_proj=10,
                create_ini_dark=False,
                create_ini_flat=False,
                dim=10,
            ).scan
            self._scans.append(scan)

            # create future
            future = asyncio.Future()
            if i == 1:
                future.set_result(None)
            self._future_tomo_objs.append(
                FutureTomwerObject(
                    tomo_obj=scan,
                    futures=(future,),
                )
            )
        # set up gui
        self._supervisor = FutureTomwerScanObserverWidget()
        self._supervisor.setConvertWhenFinished(False)

    def tearDown(self):
        self._supervisor.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._supervisor.close()
        self._supervisor = None
        shutil.rmtree(self.tempdir)
        self._scans.clear()
        self._future_tomo_objs.clear()
        super().tearDown()

    def test(self):
        for future_tomo_obj in self._future_tomo_objs:
            self._supervisor.addFutureTomoObj(future_tomo_obj=future_tomo_obj)
        self._supervisor.show()
