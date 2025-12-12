import os

import numpy
import pint
from nxtomo.application.nxtomo import NXtomo
from silx.gui import qt
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui.visualization.nxtomometadata import NXtomoMetadataViewer
from tomwer.tests.conftest import qtapp  # noqa F401

_ureg = pint.get_application_registry()


def test_nx_editor(
    tmp_path,
    qtapp,  # noqa F811
):
    # 1.0 create nx tomo with raw data
    nx_tomo = NXtomo()
    nx_tomo.instrument.detector.x_pixel_size = 2.6e-6 * _ureg.meter
    nx_tomo.instrument.detector.y_pixel_size = 2.5e-6 * _ureg.meter
    nx_tomo.instrument.detector.field_of_view = "Half"
    nx_tomo.instrument.detector.distance = 59.0 * _ureg.meter
    nx_tomo.instrument.detector.set_transformation_from_x_flipped(True)
    nx_tomo.instrument.detector.set_transformation_from_y_flipped(False)
    nx_tomo.energy = 12.8 * _ureg.keV
    # warning: NXtomo uses McStas coordinate system
    nx_tomo.sample.z_translation = numpy.arange(12) * _ureg.meter
    nx_tomo.sample.y_translation = numpy.arange(2, 14) * _ureg.meter
    nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo.sample.rotation_angle = numpy.linspace(0, 180, num=12) * _ureg.degree

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo.save(
        file_path=file_path,
        data_path=entry,
    )

    scan = NXtomoScan(file_path, entry)

    # 2.0 create the widget and do the edition
    widget = NXtomoMetadataViewer()
    widget.setScan(scan=scan)
    widget.show()

    # 3.0 check data have been corrcetly loaded
    def check_metric(expected_value, current_value):
        if expected_value is None:
            return current_value is None
        return expected_value == current_value

    assert check_metric(
        2.6e-6,
        widget._xDetectorPixelSizeMetricEntry.getValue().to(_ureg.meter).magnitude,
    )
    assert widget._xDetectorPixelSizeMetricEntry._qcbUnit.currentText() == "m"
    assert check_metric(
        2.5e-6,
        widget._yDetectorPixelSizeMetricEntry.getValue().to(_ureg.meter).magnitude,
    )
    assert widget._yDetectorPixelSizeMetricEntry._qcbUnit.currentText() == "m"

    assert check_metric(
        59,
        widget._sampleDetectorDistanceMetricEntry.getValue().to(_ureg.meter).magnitude,
    )
    assert widget._sampleDetectorDistanceMetricEntry._qcbUnit.currentText() == "m"

    assert "Half" == widget._fieldOfViewCB.currentText()
    assert widget._lrFlippedCB.isChecked()
    assert not widget._udFlippedCB.isChecked()

    assert "12.8" == widget._energyEntry.text()

    # end
    widget.setAttribute(qt.Qt.WA_DeleteOnClose)
    widget.close()
    widget = None
