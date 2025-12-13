import gc
import os
import shutil
import tempfile

import numpy
from silx.gui import qt
from silx.gui.utils.testutils import SignalListener, TestCaseQt

from orangecontrib.tomwer.widgets.control.TomoObjSeriesOW import TomoObjSeriesOW
from tomwer.core.utils.scanutils import HDF5MockContext
from tomwer.core.volume.hdf5volume import HDF5Volume


class TestTomoObjSeriesOW(TestCaseQt):
    """
    Test the TomoObjSeriesOW orange widget
    """

    def setUp(self):
        super().setUp()
        self.window = TomoObjSeriesOW()
        self.folder = tempfile.mkdtemp()

        # connect to the series created signal
        self._listener = SignalListener()
        self.window._widget.sigSeriesSelected.connect(self._listener)

    def tearDown(self):
        self.window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.window.close()
        self.window = None
        self._listener = None
        shutil.rmtree(self.folder)
        gc.collect()

    def test_with_volumes(self):
        """test the TomoObjSeriesOW with volumes"""
        volume_1 = HDF5Volume(
            file_path=os.path.join(self.folder, "vol_file.hdf5"),
            data_path="entry0000",
            data=numpy.linspace(0, 10, 100 * 100 * 3).reshape(3, 100, 100),
        )
        volume_1.save()
        volume_2 = HDF5Volume(
            file_path=os.path.join(self.folder, "vol_file2.hdf5"),
            data_path="entry0001",
            data=numpy.linspace(60, 120, 100 * 100 * 5).reshape(5, 100, 100),
        )
        volume_2.save()

        assert self._listener.callCount() == 0
        assert len(self.window._widget._widget.getSelectedSeries()) == 0
        # add the volume to the possible objects to be added
        self.window.addTomoObj(volume_1)
        self.window.addTomoObj(volume_2)
        assert len(self.window._widget._widget.getSelectedSeries()) == 0

        # add volume to the series defined
        newSerieWidget = (
            self.window._widget._widget._seriesDefinitionWidget._manualDefWidget._newSeriesWidget
        )
        newSerieWidget.addTomoObjToCurrentSeries(volume_1)
        assert len(self.window._widget._widget.getSelectedSeries()) == 1
        newSerieWidget.addTomoObjToCurrentSeries(
            volume_1
        )  # try adding twice the same object
        assert len(self.window._widget._widget.getSelectedSeries()) == 1
        newSerieWidget.addTomoObjToCurrentSeries(volume_2)
        assert len(self.window._widget._widget.getSelectedSeries()) == 2
        assert self._listener.callCount() == 0
        self.window._widget._selectButton.released.emit()
        self.qapp.processEvents()
        assert self._listener.callCount() == 1

    def test_with_scans(self):
        """test the TomoObjSeriesOW with scans"""
        with HDF5MockContext(
            scan_path=os.path.join(self.folder, "test", "scan"), n_proj=100
        ) as scan:
            assert self._listener.callCount() == 0

            # add the scan to possible objects to be added
            self.window.addTomoObj(scan)
            assert len(self.window._widget._widget.getSelectedSeries()) == 0

            # add scan to the series defined
            newSerieWidget = (
                self.window._widget._widget._seriesDefinitionWidget._manualDefWidget._newSeriesWidget
            )
            newSerieWidget.addTomoObjToCurrentSeries(scan)

            assert len(self.window._widget._widget.getSelectedSeries()) == 1
            self.window._widget._selectButton.released.emit()
            self.qapp.processEvents()
            assert self._listener.callCount() == 1
