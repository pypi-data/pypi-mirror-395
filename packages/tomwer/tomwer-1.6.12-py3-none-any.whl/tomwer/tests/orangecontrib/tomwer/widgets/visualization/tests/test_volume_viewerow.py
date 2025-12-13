# coding: utf-8
from __future__ import annotations

import os
import numpy
from silx.gui import qt
from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.core.volume.hdf5volume import HDF5Volume

from orangecontrib.tomwer.widgets.visualization.VolumeViewerOW import VolumeViewerOW


def test_VolumeViewerOW(qtapp, tmp_path):  # noqa F811
    """Test VolumeViewerOW"""

    volume = HDF5Volume(
        file_path=os.path.join(tmp_path, "my_volume.hdf5"),
        data_path="my_vol",
    )
    volume.data = numpy.random.random((100, 100, 100))
    volume.save()
    volume.metadata = {}

    window = VolumeViewerOW()
    window.show()

    # test setting a volume (already loaded in memory)
    window.set_dynamic_input("volume", volume)
    window.handleNewSignals()
    qt.QApplication.instance().processEvents()
    volumeViewerWindow = window._window._window
    assert (
        volumeViewerWindow._geometryOrMetadataWidget._metadataWidget._volumeIdentifierQLE.text()
        == volume.get_identifier().to_str()
    )
    assert len(volumeViewerWindow._XYPlot2D.getPlot().getAllImages()) == 1
    # note: according to underlying threads other plot might have 0 or 1 image

    # test setting a volume not existing
    not_existing_volume = HDF5Volume(
        file_path="/does/not/exists.h5",
        data_path="my_vol",
    )
    window.set_dynamic_input("volume", not_existing_volume)
    window.handleNewSignals()
    assert (
        volumeViewerWindow._geometryOrMetadataWidget._metadataWidget._volumeIdentifierQLE.text()
        == not_existing_volume.get_identifier().to_str()
    )
    for plot in volumeViewerWindow.getPlots().values():
        assert len(plot.getAllImages()) == 0
