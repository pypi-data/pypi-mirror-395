import os
import pickle

import numpy
import pytest
import pint
from nxtomomill.nexus.nxtomo import NXtomo
from orangecanvas.scheme.readwrite import literal_dumps
from silx.gui.utils.testutils import SignalListener
from nxtomo.nxobject.nxdetector import ImageKey
from orangecontrib.tomwer.widgets.edit.NXtomoEditorOW import NXtomoEditorOW
from tomwer.core.process.edit.nxtomoeditor import NXtomoEditorKeys
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.tests.utils import skip_gui_test
from tomwer.gui.utils.qt_utils import QSignalSpy
from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.tests.test_utils import is_lr_flip, is_ud_flip

_ureg = pint.get_application_registry()


def getDefaultConfig() -> dict:
    """return the configuration of the NXtomo editor. First value is the value of the field, second is: is the associated lock button locked or not"""
    return {
        NXtomoEditorKeys.ENERGY: (5.9, False),
        NXtomoEditorKeys.SAMPLE_SOURCE_DISTANCE: (-55.2, False),
        NXtomoEditorKeys.PROPAGATION_DISTANCE: (10.1, True),
        NXtomoEditorKeys.SAMPLE_DETECTOR_DISTANCE: (2.4, True),
        NXtomoEditorKeys.FIELD_OF_VIEW: ("Full", False),
        NXtomoEditorKeys.DETECTOR_X_PIXEL_SIZE: (0.023, True),
        NXtomoEditorKeys.DETECTOR_Y_PIXEL_SIZE: (0.025, True),
        NXtomoEditorKeys.SAMPLE_X_PIXEL_SIZE: (0.24, True),
        NXtomoEditorKeys.SAMPLE_Y_PIXEL_SIZE: (0.26, True),
        NXtomoEditorKeys.LR_FLIPPED: (True, True),
        NXtomoEditorKeys.UD_FLIPPED: (False, False),
        NXtomoEditorKeys.X_TRANSLATION: (0.0,),
        NXtomoEditorKeys.Z_TRANSLATION: (0.0,),
    }


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_NXtomoEditorOW(
    qtapp,  # noqa F811
    tmp_path,
):
    window = NXtomoEditorOW()
    # test serialization
    window.setConfiguration(getDefaultConfig())
    assert window.getConfiguration() == getDefaultConfig()
    pickle.dumps(window.getConfiguration())

    # test literal dumps
    literal_dumps(window.getConfiguration())

    # test widget automation
    signal_listener = SignalListener()
    window.sigScanReady.connect(signal_listener)
    # set up the widget to define and lock distance, energy and x pixel size
    distance_widget = window.widget.mainWidget._sampleDetectorDistanceMetricEntry
    distance_widget.setValue(value_m=0.6)
    distance_widget.setUnit(_ureg.millimeter)
    distance_locker = window.widget.mainWidget._sampleDetectorDistanceLB
    distance_locker.setLock(True)
    energy_widget = window.widget.mainWidget._energyEntry
    energy_widget.setValue(88.058)
    energy_locker = window.widget.mainWidget._energyLockerLB
    energy_locker.setLock(True)
    x_pixel_widget = window.widget.mainWidget._xDetectorPixelSizeMetricEntry
    x_pixel_widget.setValue(value_m=45)
    x_pixel_widget.setUnit(_ureg.nanometer)
    x_pixel_locker = window.widget.mainWidget._xDetectorPixelSizeLB
    x_pixel_locker.setLock(True)

    # 1.0 create nx tomos with raw data
    nx_tomo = NXtomo()
    nx_tomo.instrument.detector.x_pixel_size = (
        0.023 * _ureg.meter  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.y_pixel_size = (
        0.025 * _ureg.meter  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.field_of_view = "full"
    nx_tomo.instrument.detector.distance = (
        2.4 * _ureg.meter  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.set_transformation_from_x_flipped(
        False  # should be overwrite by the configuration / lock buttons
    )
    nx_tomo.instrument.detector.set_transformation_from_y_flipped(True)
    nx_tomo.energy = 5.9 * _ureg.keV
    nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo.sample.rotation_angle = numpy.linspace(0, 20, num=12) * _ureg.degree

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo.save(
        file_path=file_path,
        data_path=entry,
    )
    # 2.0 set scan to the nxtomo-editor
    scan = NXtomoScan(file_path, entry)
    waiter = QSignalSpy(window.sigScanReady)
    window.setScan(scan=scan)
    # warning: avoid executing the ewoks task as this will be done
    # automatically (has some field lock). This would create concurrency task
    # and could bring some HDF5 concurrency error
    waiter.wait(5000)
    # 3.0 check results are as expected
    # make sure the scan has been re-emitted
    assert signal_listener.callCount() == 1
    # make sure the edition of the parameters have been done and only those
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
        detector_data_as="as_numpy_array",
    )
    numpy.testing.assert_almost_equal(
        overwrite_nx_tomo.instrument.detector.x_pixel_size.to_base_units().magnitude,
        (45e-9 * _ureg.meter).to_base_units().magnitude,
    )
    assert (
        overwrite_nx_tomo.instrument.detector.y_pixel_size
        == nx_tomo.instrument.detector.y_pixel_size
    )
    assert (
        overwrite_nx_tomo.instrument.detector.field_of_view
        == nx_tomo.instrument.detector.field_of_view
    )
    numpy.testing.assert_almost_equal(
        overwrite_nx_tomo.instrument.detector.distance.to_base_units().magnitude,
        (6.0e-4 * _ureg.meter).to_base_units().magnitude,
    )

    assert (
        is_lr_flip(
            overwrite_nx_tomo.instrument.detector.transformations.transformations
        )
        is True
    )
    assert (
        is_ud_flip(
            overwrite_nx_tomo.instrument.detector.transformations.transformations
        )
        is True
    )

    numpy.testing.assert_almost_equal(
        overwrite_nx_tomo.energy.to_base_units().magnitude,
        (88.058 * _ureg.keV).to_base_units().magnitude,
    )
    numpy.testing.assert_array_almost_equal(
        overwrite_nx_tomo.instrument.detector.data,
        nx_tomo.instrument.detector.data,
    )
