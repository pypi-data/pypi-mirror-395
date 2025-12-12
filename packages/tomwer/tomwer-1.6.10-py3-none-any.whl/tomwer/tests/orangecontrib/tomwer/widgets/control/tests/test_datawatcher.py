# coding: utf-8
from __future__ import annotations

import gc
import logging
import os
import shutil
import tempfile
import time
from time import sleep

from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt

from orangecontrib.tomwer.tests.TestAcquisition import Simulation
from orangecontrib.tomwer.widgets.control.DataWatcherOW import DataWatcherOW
from tomwer.core.process.control.datawatcher import status as datawatcherstatus
from tomwer.core.utils.scanutils import MockBlissAcquisition, MockNXtomo

logging.disable(logging.INFO)


class DataWatcherWaiter(TestCaseQt):
    """Define a simple objecy able to wait for some state of the DataWatcher
    arrive"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset()
        self.lastStatus = []

    def tearDown(self):
        pass

    def reset(self):
        self.lastStatus = []

    def stateHasChanged(self, val):
        """Register all status"""
        if val not in self.lastStatus:
            self.lastStatus.append(val)

    def waitForState(self, state, maxWaiting):
        """simple function wich wait until the DataWatcherWidget reach the given
        state.
        If the widget doesn't reach this state after maxWaiting second. Then fail.

        :param state: the state we are waiting for
        :param maxWaiting: the maximal number of second to wait until failling.
        """
        while state not in self.lastStatus:
            time.sleep(1.0)
            self.qapp.processEvents()
            maxWaiting -= 1
            if maxWaiting <= 0:
                return False
        return state in self.lastStatus


class TestDataWatcherAcquisition(DataWatcherWaiter):
    """Functions testing the classical behavior of data watcher
    - signal acquisition is over only when all files are copied
    """

    def tearDown(self):
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        self.dataWatcherWidget.setObservation(False)
        self.dataWatcherWidget.close()
        del self.dataWatcherWidget
        self.dataWatcherWidget = None
        self.s.wait()
        del self.s
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)
        gc.collect()
        super().tearDown()

    def setUp(self):
        self.manipulationId = "test10"

        super().setUp()
        self.inputdir = tempfile.mkdtemp()
        DataWatcherWaiter.reset(self)
        self.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        self.dataWatcherWidget.srcPattern = ""
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)
        self.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)

        self.s = Simulation(
            self.inputdir,
            self.manipulationId,
            finalState=Simulation.advancement["acquisitionRunning"],
        )

    def testStartAcquisition(self):
        """Make sure the data watch detect the acquisition of started"""
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s.createFinalXML(True)
        self.dataWatcherWidget.setFolderObserved(observeDir)

        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.s.start()
        self.s.advanceTo("acquisitionDone")
        self.s.start()
        self.s.wait()
        self.dataWatcherWidget.startObservation()
        self.dataWatcherWidget._widget.observationThread.wait()
        self.dataWatcherWidget._widget.observationThread.observations.dict[
            observeDir
        ].wait()
        self.qapp.processEvents()
        finishedAcqui = (
            self.dataWatcherWidget._widget.observationThread.observations.ignoredFolders
        )
        self.qapp.processEvents()
        self.assertTrue(observeDir in finishedAcqui)


class TestDataWatcherInteraction(TestCaseQt):
    """Simple unit test to test the start/stop observation button action"""

    def setUp(self):
        super().setUp()
        self.inputdir = tempfile.mkdtemp()
        self.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        self.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.dataWatcherWidget.srcPattern = ""

    def tearDown(self):
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        self.dataWatcherWidget.close()
        del self.dataWatcherWidget
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)
        gc.collect()

    def testStartAndStopAcquisition(self):
        """test multiple start and stop action on the start observation to
        make sure no crash are appearing
        """
        try:
            self.dataWatcherWidget.setFolderObserved(self.inputdir)
            self.dataWatcherWidget.show()
            self.dataWatcherWidget.setObservation(True)
            for _ in range(5):
                self.dataWatcherWidget._widget._qpbstartstop.pressed.emit()
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)


class WaitForXMLOption(DataWatcherWaiter):
    """test the behavior of datawatcher when the option 'wait for xml copy'
    Basically in this case DataWatcherDirObserver will wait until an .xml
    arrived
    """

    @classmethod
    def setUpClass(cls):
        cls.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        cls.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        cls.dataWatcherWidget.obsMethod = datawatcherstatus.DET_END_XML
        cls.dataWatcherWidget.srcPattern = ""
        cls.manipulationId = "test10"
        super().setUpClass()

    def setUp(self):
        self.inputdir = tempfile.mkdtemp()
        self.reset()
        self.dataWatcherWidget.setObservation(False)
        self.dataWatcherWidget.resetStatus()
        super().setUp()

    def tearDown(self):
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        if os.path.isdir(self.inputdir):
            shutil.rmtree(self.inputdir)
        gc.collect()
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        cls.dataWatcherWidget.close()
        del cls.dataWatcherWidget
        if hasattr(cls, "s"):
            cls.s.quit()
            del cls.s
        super().tearDownClass()

    def testAcquistionNotEnding(self):
        """Check behavior if an acquisition never end"""
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(
            self.inputdir,
            self.manipulationId,
            finalState=Simulation.advancement["acquisitionRunning"],
        )
        self.dataWatcherWidget.setFolderObserved(observeDir)
        self.dataWatcherWidget.show()
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)

        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.s.start()
        self.s.wait()
        self.dataWatcherWidget.setObservation(True)
        self.dataWatcherWidget._widget.observationThread.wait()
        self.dataWatcherWidget._widget.observationThread.observations.dict[
            observeDir
        ].wait()
        finishedAcqui = (
            self.dataWatcherWidget._widget.observationThread.observations.ignoredFolders
        )
        self.qapp.processEvents()
        self.assertFalse(observeDir in finishedAcqui)

    def testAcquistionEnded(self):
        """Check behavior if an acquisition is ending"""
        manipulationId = "test10"
        observeDir = os.path.join(self.inputdir, self.manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(
            self.inputdir,
            manipulationId,
            finalState=Simulation.advancement["acquisitionDone"],
        )
        self.s.createFinalXML(True)
        self.dataWatcherWidget.setFolderObserved(observeDir)
        self.dataWatcherWidget.show()
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)

        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.s.start()
        self.s.wait()
        self.dataWatcherWidget.setObservation(True)
        self.dataWatcherWidget._widget.observationThread.wait()
        self.dataWatcherWidget._widget.observationThread.observations.dict[
            observeDir
        ].wait()
        finishedAcqui = (
            self.dataWatcherWidget._widget.observationThread.observations.ignoredFolders
        )
        self.qapp.processEvents()
        self.assertTrue(observeDir in finishedAcqui)


class TestRSync(DataWatcherWaiter):
    """test that the synchronization using RSyncManager is working"""

    def setUp(self):
        super().setUp()
        self.inputdir = tempfile.mkdtemp()
        self.outputdir = tempfile.mkdtemp()
        DataWatcherWaiter.reset(self)
        self.dataWatcherWidget = DataWatcherOW(displayAdvancement=False)
        self.dataWatcherWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.dataWatcherWidget._widget.setSrcAndDestPattern(
            self.inputdir, self.outputdir
        )

    def tearDown(self):
        while self.qapp.hasPendingEvents():
            self.qapp.processEvents()
        self.dataWatcherWidget.close()
        del self.dataWatcherWidget
        if hasattr(self, "s"):
            self.s.quit()
            del self.s
        super(TestRSync, self).tearDown()
        for d in (self.inputdir, self.outputdir):
            if os.path.isdir(d):
                shutil.rmtree(d, ignore_errors=True)
        gc.collect()

    def testStartAcquisition(self):
        """Test that rsync is launched when an acquisition is discovered"""
        manipulationId = "test10"
        observeDir = os.path.join(self.inputdir, manipulationId)
        for folder in (self.inputdir, observeDir):
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.assertTrue(os.path.isdir(observeDir))

        self.s = Simulation(
            self.inputdir,
            manipulationId,
            finalState=Simulation.advancement["acquisitionRunning"],
        )

        self.s.setSrcDestPatterns(self.inputdir, self.outputdir)
        self.s.createFinalXML(True)
        self.dataWatcherWidget.setFolderObserved(self.inputdir)
        self.dataWatcherWidget.show()
        self.dataWatcherWidget.sigTMStatusChanged.connect(self.stateHasChanged)
        self.assertTrue(self.dataWatcherWidget.currentStatus == "not processing")
        self.dataWatcherWidget.setObservation(True)
        self.s.start()
        # check state scanning
        time.sleep(0.5)

        self.dataWatcherWidget.stopObservation()

        # in this case the .info should be in the output dir also
        test10_output = os.path.join(self.outputdir, "test10")
        test10_input = os.path.join(self.inputdir, "test10")
        self.assertTrue(os.path.isfile(os.path.join(test10_output, "test10.info")))

        # make sure file transfert have been started (using rsync)
        # all file in outputdir should be in input dir
        time.sleep(2)
        # check that some .edf file have already been copied
        self.assertTrue(len(test10_output) > 5)

        # xml shouldn't be there because we are righting it at the end
        self.assertFalse(os.path.isfile(os.path.join(test10_output, "test10.xml")))
        self.assertFalse(os.path.isfile(os.path.join(test10_input, "test10.xml")))


class TestDataWatcherBlissScan(TestCaseQt):
    def setUp(self):
        self._widget = DataWatcherOW(self)
        self.tempdir = tempfile.mkdtemp()
        MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=3,
            n_darks=2,
            n_flats=2,
            output_dir=os.path.join(self.tempdir, "folder_1"),
        )

        MockBlissAcquisition(
            n_sample=2,
            n_sequence=1,
            n_scan_per_sequence=3,
            n_darks=2,
            n_flats=2,
            output_dir=os.path.join(self.tempdir, "test", "with", "some", "depth"),
        )
        self._listener = SignalListener()
        self._widget._widget.sigScanReady.connect(self._listener)

    def tearDown(self):
        self._widget._widget.sigScanReady.disconnect(self._listener)
        self._widget.stopObservation()
        self._listener = None
        shutil.rmtree(self.tempdir)
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        gc.collect()


class TestDataWatcherNXtomo(TestCaseQt):
    def setUp(self):
        self._widget = DataWatcherOW(self)
        self.tempdir = tempfile.mkdtemp()
        MockNXtomo(
            scan_path=os.path.join(self.tempdir, "folder_1"),
            n_proj=10,
        )

        MockNXtomo(
            scan_path=os.path.join(self.tempdir, "test", "with", "some", "depth"),
            n_proj=10,
        )
        self._listener = SignalListener()
        self._widget._widget.sigScanReady.connect(self._listener)

    def tearDown(self):
        self._widget._widget.sigScanReady.disconnect(self._listener)
        self._widget.stopObservation()
        self._listener = None
        shutil.rmtree(self.tempdir)
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        gc.collect()

    def test(self):
        self._widget.setFolderObserved(self.tempdir)
        self._widget._widget.getConfigWindow().setMode((datawatcherstatus.NXtomo_END,))
        self._widget.show()
        self._widget.startObservation()
        processing_time = 2
        sleep_time = 0.005
        while processing_time > 0:
            self.qapp.processEvents()
            sleep(sleep_time)
            processing_time -= sleep_time
        assert self._listener.callCount() == 2
