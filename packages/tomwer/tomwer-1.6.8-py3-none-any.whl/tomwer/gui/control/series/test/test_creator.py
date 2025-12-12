# coding: utf-8
from __future__ import annotations

import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt
from tomoscan.series import Series

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.gui.control.series.seriescreator import (
    SeriesDefinition,
    SeriesHistoryDialog,
    SeriesManualControlDialog,
    SeriesManualFromTomoObj,
    SeriesTree,
    SeriesWidget,
)


class _MockScanBase:
    def init(self):
        n_hdf5_scan = 11
        self._scans = []
        self._root_dir = tempfile.mkdtemp()
        for i_scan in range(n_hdf5_scan):
            scan_path = os.path.join(self._root_dir, f"scan_{i_scan}")
            scan = MockNXtomo(scan_path=scan_path, n_proj=10, n_ini_proj=0).scan
            self._scans.append(scan)
        n_edf_scan = 4
        for i_scan in range(n_edf_scan):
            scan_path = os.path.join(self._root_dir, f"scan_{i_scan}")
            scan = MockEDF.mockScan(
                scanID=scan_path,
                nRadio=10,
                dim=10,
            )
            self._scans.append(scan)

    def close(self):
        shutil.rmtree(self._root_dir)


class _MockSeriesBase(_MockScanBase):
    def init(self):
        super().init()
        self._seriesList = [
            Series("series1", self._scans[0:1], use_identifiers=True),
            Series("series2", self._scans[1:5], use_identifiers=False),
            Series("series3", self._scans[5:11], use_identifiers=True),
            Series("series4", self._scans[8:11], use_identifiers=True),
            Series("series5", self._scans[-2:-1], use_identifiers=False),
            Series("series6", self._scans[-5:], use_identifiers=True),
        ]

    def close(self):
        self._seriesList.clear()
        super().close()


class TestSeriesTree(TestCaseQt, _MockSeriesBase):
    """Test the SeriesTree widget"""

    def setUp(self):
        super().setUp()
        super().init()
        self._widget = SeriesTree()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test_add_remove(self):
        """Test adding and removing series"""
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        for series in self._seriesList:
            self._widget.addSeries(series)
        assert self._widget.n_series == 6
        self._widget.removeSeries(self._seriesList[3])
        assert self._widget.n_series == 5
        self._widget.removeSeries(self._seriesList[2])
        self._widget.removeSeries(self._seriesList[1])
        self._widget.removeSeries(self._seriesList[0])
        # make sure no error is raised if we try to remove twine the same serie
        self._widget.removeSeries(self._seriesList[0])
        assert self._widget.n_series == 2
        self._widget.addSeries(self._seriesList[1])
        self._widget.addSeries(self._seriesList[2])
        assert self._widget.n_series == 4

    def test_selection(self):
        """Test selection of the SerieTree"""
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        for series in self._seriesList:
            self._widget.addSeries(series)

        selection = (self._seriesList[2], self._seriesList[3])
        self._widget.setSelectedSeries(selection)
        assert self._widget.getSelectedSeries() == selection
        self._widget.clearSelection()
        assert self._widget.getSelectedSeries() == ()


class TestSeriesHistoryDialog(TestCaseQt, _MockSeriesBase):
    """Test the SeriesHistoryDialog"""

    def setUp(self):
        super().setUp()
        super().init()
        self._widget = SeriesHistoryDialog()

        # create listener for the nabu widget
        self.signal_listener = SignalListener()

        # connect signal / slot
        self._widget.sigSeriesSend.connect(self.signal_listener)

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test(self):
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        for series in self._seriesList:
            self._widget.addSeries(series)

        selection = (self._seriesList[0], self._seriesList[4])
        self._widget.setSelectedSeries(selection)
        assert self._widget.getSelectedSeries() == selection
        assert self.signal_listener.callCount() == 0
        self._widget._sendButton.clicked.emit()
        self.qapp.processEvents()
        assert self.signal_listener.callCount() == 2
        assert self._widget.getSelectedSeries() == selection
        self.signal_listener.clear()
        self._widget._clearButton.clicked.emit()
        assert self._widget.getSelectedSeries() == ()
        assert self.signal_listener.callCount() == 0
        self._widget._sendButton.clicked.emit()
        assert self.signal_listener.callCount() == 0


class TestSeriesDefinition(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._widget = SeriesDefinition()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().tearDown()

    def test_manual_selection(self):
        self._widget.setMode("manual")
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        assert not self._widget._automaticDefWidget.isVisible()
        assert self._widget._manualDefWidget.isVisible()

    def test_automatic_selection(self):
        self._widget.setMode("auto")
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        assert self._widget._automaticDefWidget.isVisible()
        assert not self._widget._manualDefWidget.isVisible()


class TestSeriesManualDefinitionDialog(TestCaseQt, _MockScanBase):
    """Test interaction with the series manual definition"""

    def setUp(self):
        self._widget = SeriesManualControlDialog()
        super().setUp()
        super().init()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test(self):
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)

        self._widget.setSeriesName("series test")
        self.qapp.processEvents()
        assert self._widget.getSeriesName() == "series test"

        self._widget._mainWidget._newSeriesWidget._serieTree.rootItem.setText(
            0, "new series"
        )
        self.qapp.processEvents()
        assert self._widget.getSeriesName() == "new series"

        for scan in self._scans[:5]:
            self._widget.addScan(scan)

        self.assertEqual(self._widget.n_tomo_objs, len(self._scans[:5]))
        self._widget.removeScan(self._scans[0])
        self.assertEqual(self._widget.n_tomo_objs, len(self._scans[:5]) - 1)

        series_scan = tuple(self._scans[1:5])
        assert isinstance(series_scan, tuple)

        current_series = self._widget.getSeries(use_identifiers=True)
        assert isinstance(current_series, Series)
        series_test_1 = Series(
            name="new series", iterable=series_scan, use_identifiers=True
        )

        self.assertEqual(series_test_1, current_series)
        series_test_2 = Series(name="test", iterable=series_scan, use_identifiers=True)
        assert series_test_2.name == "test"
        assert current_series.name == "new series"
        self.assertNotEqual(series_test_2, current_series)

        self._widget.setSelectedScans([self._scans[2]])
        self._widget.getSelectedScans() == (self._scans[2],)
        self._widget.removeSelectedScans()
        self.assertEqual(self._widget.n_tomo_objs, len(self._scans[:5]) - 2)
        self._widget.getSelectedScans() == tuple()

        self._widget.clearSeries()
        self.assertEqual(self._widget.n_tomo_objs, 0)
        self.assertEqual(Series(name="new series"), self._widget.getSeries())

        # test adding an nx file
        hdf5_scan = self._scans[0]
        assert isinstance(hdf5_scan, NXtomoScan)
        self._widget.addScanFromNxFile(hdf5_scan.master_file)
        self.assertEqual(self._widget.n_tomo_objs, 1)


class TestSeriesWidget(TestCaseQt, _MockSeriesBase):
    """
    Test the SeriesWidget
    """

    def setUp(self):
        super().setUp()
        super().init()
        self._widget = SeriesWidget()
        # create listeners
        self.signal_send_series_listener = SignalListener()
        self.signal_serie_changed_listener = SignalListener()
        self.signal_history_changed_listener = SignalListener()

        # connect signal / slot
        self._widget.sigSeriesSend.connect(self.signal_send_series_listener)
        self._widget.sigCurrentSeriesChanged.connect(self.signal_serie_changed_listener)
        self._widget.sigHistoryChanged.connect(self.signal_history_changed_listener)

    def tearDown(self):
        self._widget.sigSeriesSend.disconnect(self.signal_send_series_listener)
        self._widget.sigCurrentSeriesChanged.disconnect(
            self.signal_serie_changed_listener
        )
        self._widget.sigHistoryChanged.disconnect(self.signal_history_changed_listener)

        self.signal_send_series_listener = None
        self.signal_serie_changed_listener = None
        self.signal_history_changed_listener = None

        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        super().close()
        super().tearDown()

    def test(self):
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        self._seriesList[3].name = "toto series"
        for series in self._seriesList[2:5]:
            self._widget.getHistoryWidget().addSeries(series)
        self._widget.setMode("history")
        self._widget.setMode("series definition", "manual")
        self._widget.getDefinitionWidget().getManualDefinitionWidget().setSeriesName(
            "new series"
        )

        self.assertEqual(
            len(
                self._widget.getDefinitionWidget()
                .getManualDefinitionWidget()
                .getSeries()
            ),
            0,
        )

        self._widget.getHistoryWidget().setSelectedSeries(
            [
                self._seriesList[3],
            ]
        )
        assert len(self._widget.getHistoryWidget().getSelectedSeries()) == 1

        self.signal_serie_changed_listener.clear()
        self._widget.getHistoryWidget().editSelected()
        self.qapp.processEvents()
        assert self.signal_serie_changed_listener.callCount() == 1

        self.assertEqual(
            self._widget.getDefinitionWidget()
            .getManualDefinitionWidget()
            .getSeries()
            .name,
            "toto series",
        )

        self.assertEqual(
            self._widget.getDefinitionWidget()
            .getManualDefinitionWidget()
            .getSeries(use_identifiers=True),
            self._seriesList[3],
        )

        self.signal_serie_changed_listener.clear()
        self._widget.getDefinitionWidget().getManualDefinitionWidget().addToCurrentSeries(
            self._scans[0]
        )
        self.qapp.processEvents()
        assert self.signal_serie_changed_listener.callCount() == 1

        expected_scans = self._scans[8:11]
        expected_scans.append(self._scans[0])
        expected_series = Series("toto series", expected_scans, use_identifiers=True)

        self.assertEqual(
            self._widget.getDefinitionWidget()
            .getManualDefinitionWidget()
            .getSeries(use_identifiers=True),
            expected_series,
        )

        # check send edited serie
        self.signal_history_changed_listener.clear()
        self.signal_send_series_listener.clear()
        self.qapp.processEvents()

        # check send selected from the history
        self.signal_send_series_listener.clear()
        self._widget.getHistoryWidget().setSelectedSeries(
            [
                self._seriesList[4],
            ]
        )
        assert len(self._widget.getHistoryWidget().getSelectedSeries()) == 1
        self._widget.getHistoryWidget().sendSelected()
        assert self.signal_send_series_listener.callCount() == 1


class TestSerieManualFromTomoObj(TestCaseQt):
    """
    test the SerieManualFromTomoObj widget
    """

    def setUp(self):
        super().setUp()
        self._tmp_dir = tempfile.mkdtemp()
        self._widget = SeriesManualFromTomoObj()
        self._volume_1 = HDF5Volume(
            file_path=os.path.join(self._tmp_dir, "vol1.hdf5"),
            data_path="data",
        )
        self._volume_2 = HDF5Volume(
            file_path=os.path.join(self._tmp_dir, "vol2.hdf"),
            data_path="data",
        )
        self._volume_3 = HDF5Volume(
            file_path=os.path.join(self._tmp_dir, "vol3.nx"),
            data_path="data",
        )
        self._scan_1 = MockNXtomo(
            scan_path=os.path.join(self._tmp_dir, "scan_1"), n_proj=10, n_ini_proj=10
        ).scan
        self._scan_2 = MockNXtomo(
            scan_path=os.path.join(self._tmp_dir, "scan_2"), n_proj=10, n_ini_proj=10
        ).scan

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        return super().tearDown()

    def test(self):
        self._widget.show()
        for tomo_obj in (
            self._volume_1,
            self._volume_2,
            self._volume_3,
            self._scan_1,
            self._scan_2,
        ):
            self._widget.addTomoObj(tomo_obj)

        current_serie = self._widget.getSeries()
        assert isinstance(current_serie, Series)
        assert len(current_serie) == 0

        for tomo_obj in (self._volume_1, self._volume_2):
            self._widget.addToCurrentSeries(tomo_obj)

        current_serie = self._widget.getSeries()
        assert isinstance(current_serie, Series)
        assert len(current_serie) == 2
