from __future__ import annotations

import os
import h5py

import numpy
import pytest
import pint
from silx.gui import qt

from nxtomo.application.nxtomo import NXtomo
from nxtomo.nxobject.nxdetector import ImageKey, FOV
from nxtomo.utils.transformation import (
    build_matrix,
    DetXFlipTransformation,
    DetYFlipTransformation,
)

from tomwer.core.process.edit.nxtomoeditor import NXtomoEditorTask
from nxtomo.nxobject.nxtransformations import (
    NXtransformations,
    get_lr_flip,
    get_ud_flip,
)
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui.edit.nxtomoeditor import NXtomoEditor, _TranslationMetricEntry
from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.tests.test_utils import is_lr_flip, is_ud_flip

_ureg = pint.get_application_registry()


@pytest.mark.parametrize("detector_x_pixel_size", (0.12 * _ureg.millimeter,))
@pytest.mark.parametrize("detector_y_pixel_size", (None,))
@pytest.mark.parametrize("sample_x_pixel_size", (None,))
@pytest.mark.parametrize("sample_y_pixel_size", (None, 0.0066 * _ureg.meter))
@pytest.mark.parametrize("field_of_view", [item.value for item in FOV])
@pytest.mark.parametrize("sample_detector_distance", (1.2 * _ureg.meter,))
@pytest.mark.parametrize("sample_source_distance", (-10.2 * _ureg.meter,))
@pytest.mark.parametrize("propagation_distance", (1.01 * _ureg.meter,))
@pytest.mark.parametrize("energy", (None, 23.5 * _ureg.keV))
@pytest.mark.parametrize("lr_flipped", (False,))
@pytest.mark.parametrize("ud_flipped", (True, False))
@pytest.mark.parametrize(
    "x_translation",
    (None, numpy.ones(12) * _ureg.meter, numpy.arange(12) * _ureg.meter),
)
@pytest.mark.parametrize(
    "z_translation",
    (None, numpy.zeros(12) * _ureg.meter, numpy.arange(12, 24) * _ureg.meter),
)
def test_nx_editor(
    tmp_path,
    qtapp,  # noqa F811
    detector_x_pixel_size: pint.Quantity | None,
    detector_y_pixel_size: pint.Quantity | None,
    sample_x_pixel_size: pint.Quantity | None,
    sample_y_pixel_size: pint.Quantity | None,
    propagation_distance: pint.Quantity | None,
    sample_source_distance: pint.Quantity | None,
    field_of_view,
    sample_detector_distance: pint.Quantity,
    energy: pint.Quantity,
    lr_flipped,
    ud_flipped,
    x_translation: pint.Quantity,
    z_translation: pint.Quantity,
):
    """
    :param x_translation: x translation on the ESRF coordinate system (will be converted to McStas coordinate when saved)
    :param z_translation: z translation on the ESRF coordinate system (will be converted to McStas coordinate when saved)
    """
    # 1.0 create nx tomo with raw data
    nx_tomo = NXtomo()
    nx_tomo.energy = energy
    nx_tomo.instrument.detector.x_pixel_size = detector_x_pixel_size
    nx_tomo.instrument.detector.y_pixel_size = detector_y_pixel_size
    nx_tomo.instrument.detector.field_of_view = field_of_view
    nx_tomo.instrument.detector.distance = sample_detector_distance
    nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))

    nx_tomo.sample.rotation_angle = numpy.linspace(0, 20, num=12) * _ureg.degree
    # warning: mapping from ESRF coordinate to McStas
    nx_tomo.sample.z_translation = x_translation
    nx_tomo.sample.y_translation = z_translation
    nx_tomo.sample.x_pixel_size = sample_x_pixel_size
    nx_tomo.sample.y_pixel_size = sample_y_pixel_size
    nx_tomo.sample.propagation_distance = propagation_distance

    nx_tomo.instrument.source.distance = sample_source_distance

    nx_tomo.instrument.detector.set_transformation_from_lr_flipped(flipped=lr_flipped)
    nx_tomo.instrument.detector.set_transformation_from_ud_flipped(flipped=ud_flipped)

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo.save(
        file_path=file_path,
        data_path=entry,
    )

    scan = NXtomoScan(file_path, entry)

    # 2.0 create the widget and do the edition
    widget = NXtomoEditor()
    widget.setScan(scan=scan)

    # 3.0 check data have been correctly loaded
    def check_metric(expected_value, current_value):
        if expected_value is None:
            return current_value is None
        return numpy.isclose(expected_value, current_value)

    assert check_metric(
        detector_x_pixel_size, widget._xDetectorPixelSizeMetricEntry.getValue()
    )
    assert widget._xDetectorPixelSizeMetricEntry._qcbUnit.currentText() == "m"
    assert check_metric(
        detector_y_pixel_size, widget._yDetectorPixelSizeMetricEntry.getValue()
    )
    assert widget._yDetectorPixelSizeMetricEntry._qcbUnit.currentText() == "m"
    assert check_metric(
        sample_detector_distance, widget._sampleDetectorDistanceMetricEntry.getValue()
    )
    assert widget._sampleDetectorDistanceMetricEntry._qcbUnit.currentText() == "m"
    assert check_metric(
        sample_x_pixel_size, widget._xSamplePixelSizeMetricEntry.getValue()
    )
    assert check_metric(
        sample_y_pixel_size, widget._ySamplePixelSizeMetricEntry.getValue()
    )
    assert check_metric(
        sample_source_distance, widget._sampleSourceDistanceMetricEntry.getValue()
    )
    assert check_metric(
        propagation_distance, widget._propagationDistanceMetricEntry.getValue()
    )
    assert field_of_view == widget._fieldOfViewCB.currentText()
    assert lr_flipped == widget._lrFlippedCB.isChecked()
    assert ud_flipped == widget._udFlippedCB.isChecked()

    if energy is None:
        assert widget._energyEntry.getValue() is None
    else:
        assert numpy.isclose(
            energy.to(_ureg.keV).magnitude, widget._energyEntry.getValue()
        )

    def check_translation(expected_value, current_value):
        if expected_value is None:
            return current_value is None
        else:
            expected_value = expected_value.to_base_units().magnitude
            assert current_value is not None
            if isinstance(current_value, pint.Quantity):
                current_value = current_value.to_base_units().magnitude
            u_values = numpy.unique(expected_value)
            if u_values.size == 1:
                return float(current_value) == u_values[0]
            else:
                return current_value is _TranslationMetricEntry.LOADED_ARRAY

    assert check_translation(x_translation, widget._xTranslationQLE.getValue())
    assert widget._xTranslationQLE._qcbUnit.currentText() == "m"
    assert check_translation(z_translation, widget._zTranslationQLE.getValue())
    assert widget._zTranslationQLE._qcbUnit.currentText() == "m"

    # 4.0 edit some parameters
    widget._energyEntry.setText("23.789")
    widget._xDetectorPixelSizeMetricEntry.setUnit(_ureg.nanometer)
    widget._yDetectorPixelSizeMetricEntry.setValue(2.1e-7)
    widget._xSamplePixelSizeMetricEntry.setValue(value_m=5.6e-6)
    widget._sampleDetectorDistanceMetricEntry.setValue("unknown")
    widget._sampleSourceDistanceMetricEntry.setValue(-99)
    widget._propagationDistanceMetricEntry.setValue(88)
    widget._fieldOfViewCB.setCurrentText(FOV.HALF.value)
    widget._lrFlippedCB.setChecked(not lr_flipped)
    widget._xTranslationQLE.setValue(1.8)
    widget._xTranslationQLE.setUnit(_ureg.millimeter)
    widget._zTranslationQLE.setValue(2.8)
    widget._zTranslationQLE.setUnit(_ureg.meter)

    # 5.0
    task = NXtomoEditorTask(
        inputs={
            "data": scan,
            "configuration": widget.getConfigurationForTask(),
        }
    )
    task.run()

    # 6.0 make sure data have been overwrite
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
    )

    assert overwrite_nx_tomo.energy == 23.789 * _ureg.keV

    if detector_x_pixel_size is None:
        assert overwrite_nx_tomo.instrument.detector.x_pixel_size is None
    else:
        assert numpy.isclose(
            overwrite_nx_tomo.instrument.detector.x_pixel_size,
            0.12 * _ureg.nanometer,
        )
    assert overwrite_nx_tomo.instrument.detector.y_pixel_size == 2.1e-7 * _ureg.meter

    assert overwrite_nx_tomo.instrument.detector.distance is None
    assert overwrite_nx_tomo.instrument.detector.field_of_view is FOV.HALF

    final_transformation = NXtransformations()

    final_transformation.add_transformation(DetXFlipTransformation(flip=ud_flipped))
    final_transformation.add_transformation(DetYFlipTransformation(flip=not lr_flipped))
    # note: the 'not' comes from inversion done with the _xFlippedCB combobox

    numpy.testing.assert_allclose(
        build_matrix(
            overwrite_nx_tomo.instrument.detector.transformations.transformations
        ),
        build_matrix(final_transformation.transformations),
    )

    numpy.testing.assert_array_almost_equal(
        overwrite_nx_tomo.sample.x_translation,
        (numpy.array([1.8] * 12) * _ureg.millimeter).to_base_units(),
    )
    numpy.testing.assert_array_almost_equal(
        overwrite_nx_tomo.sample.z_translation,
        numpy.array([2.8] * 12) * _ureg.meter,
    )
    # end
    widget.setAttribute(qt.Qt.WA_DeleteOnClose)
    widget.close()
    widget = None


def test_nx_editor_lock(
    tmp_path,
    qtapp,  # noqa F811
):
    """test the pad lock buttons of the NXtomo editor"""
    # 1.0 create nx tomos with raw data
    nx_tomo_1 = NXtomo()
    nx_tomo_1.instrument.source.distance = 54.8 * _ureg.meter
    nx_tomo_1.instrument.detector.x_pixel_size = 0.023 * _ureg.meter
    nx_tomo_1.instrument.detector.y_pixel_size = 0.025 * _ureg.meter
    nx_tomo_1.instrument.detector.field_of_view = "full"
    nx_tomo_1.instrument.detector.distance = 2.4 * _ureg.meter
    nx_tomo_1.instrument.detector.set_transformation_from_x_flipped(False)
    nx_tomo_1.instrument.detector.set_transformation_from_y_flipped(True)
    nx_tomo_1.energy = 5.9 * _ureg.keV
    nx_tomo_1.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo_1.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo_1.sample.rotation_angle = numpy.linspace(0, 20, num=12) * _ureg.degree
    nx_tomo_1.sample.propagation_distance = 22.0 * _ureg.meter
    nx_tomo_1.sample.x_pixel_size = 0.023 * _ureg.millimeter
    nx_tomo_1.sample.y_pixel_size = 0.025 * _ureg.millimeter

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo_1.save(
        file_path=file_path,
        data_path=entry,
    )

    scan_1 = NXtomoScan(file_path, entry)

    nx_tomo_2 = NXtomo()
    nx_tomo_2.instrument.source.distance = 8 * _ureg.meter
    nx_tomo_2.instrument.detector.x_pixel_size = 4.023 * _ureg.meter
    nx_tomo_2.instrument.detector.y_pixel_size = 6.025 * _ureg.meter
    nx_tomo_2.instrument.detector.field_of_view = "full"
    nx_tomo_2.instrument.detector.distance = 2.89 * _ureg.meter
    lr_flip_sum = [
        trans.transformation_values
        for trans in get_lr_flip(
            nx_tomo_1.instrument.detector.transformations.transformations
        )
    ]
    lr_flip = numpy.isclose(lr_flip_sum, 180.0)
    nx_tomo_2.instrument.detector.set_transformation_from_x_flipped(not lr_flip)
    ud_flip_sum = [
        trans.transformation_values
        for trans in get_ud_flip(
            nx_tomo_1.instrument.detector.transformations.transformations
        )
    ]
    ud_flip = numpy.isclose(ud_flip_sum, 180.0)
    nx_tomo_2.instrument.detector.set_transformation_from_y_flipped(not ud_flip)
    nx_tomo_2.energy = 5.754 * _ureg.keV
    nx_tomo_2.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo_2.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo_2.sample.rotation_angle = numpy.linspace(0, 20, num=12) * _ureg.degree

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0001"
    nx_tomo_2.save(
        file_path=file_path,
        data_path=entry,
    )

    scan_2 = NXtomoScan(file_path, entry)

    # 2.0 create the widget and do the edition
    widget = NXtomoEditor()
    widget.setScan(scan=scan_1)

    for lockerButton in widget._lockerPBs:
        lockerButton.setLock(True)

    widget.setScan(scan=scan_2)
    # widget values must be the same (NXtomo field value not loaded if the lockers are active)
    assert widget._energyEntry.getValue() == 5.9
    assert widget._xDetectorPixelSizeMetricEntry.getValue() == 0.023 * _ureg.meter
    assert widget._yDetectorPixelSizeMetricEntry.getValue() == 0.025 * _ureg.meter
    assert widget._sampleDetectorDistanceMetricEntry.getValue() == 2.4 * _ureg.meter
    assert widget._propagationDistanceMetricEntry.getValue() == 22.0 * _ureg.meter
    assert widget._fieldOfViewCB.currentText() == "Full"
    assert not widget._lrFlippedCB.isChecked()
    assert widget._udFlippedCB.isChecked()
    assert widget._xSamplePixelSizeMetricEntry.getValue() == 0.023 * _ureg.millimeter
    assert widget._ySamplePixelSizeMetricEntry.getValue() == 0.025 * _ureg.millimeter
    assert widget._sampleSourceDistanceMetricEntry.getValue() == 54.8 * _ureg.meter

    # 3.0 save the nxtomo
    task = NXtomoEditorTask(
        inputs={
            "data": scan_2,
            "configuration": widget.getConfigurationForTask(),
        }
    )
    task.run()

    # 4.0 check save went well
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
    )
    assert (
        overwrite_nx_tomo.instrument.detector.x_pixel_size
        == nx_tomo_1.instrument.detector.x_pixel_size
    )
    assert (
        overwrite_nx_tomo.instrument.detector.y_pixel_size
        == nx_tomo_1.instrument.detector.y_pixel_size
    )
    assert (
        overwrite_nx_tomo.instrument.detector.field_of_view
        == nx_tomo_1.instrument.detector.field_of_view
    )
    assert (
        overwrite_nx_tomo.instrument.detector.distance
        == nx_tomo_1.instrument.detector.distance
    )
    assert is_lr_flip(
        overwrite_nx_tomo.instrument.detector.transformations.transformations
    ) == is_lr_flip(nx_tomo_1.instrument.detector.transformations.transformations)
    assert is_ud_flip(
        overwrite_nx_tomo.instrument.detector.transformations.transformations
    ) == is_ud_flip(nx_tomo_1.instrument.detector.transformations.transformations)

    assert overwrite_nx_tomo.energy == nx_tomo_1.energy
    assert (
        overwrite_nx_tomo.sample.propagation_distance
        == nx_tomo_1.sample.propagation_distance
    )
    assert overwrite_nx_tomo.sample.x_pixel_size == nx_tomo_1.sample.x_pixel_size
    assert overwrite_nx_tomo.sample.y_pixel_size == nx_tomo_1.sample.y_pixel_size
    assert (
        overwrite_nx_tomo.instrument.source.distance
        == nx_tomo_1.instrument.source.distance
    )
    assert widget.getConfiguration() == {
        "instrument.beam.energy": (5.9, True),
        "instrument.detector.distance": (2.4, True),
        "instrument.detector.field_of_view": ("Full", True),
        "instrument.detector.x_pixel_size": (0.023, True),
        "instrument.detector.y_pixel_size": (0.025, True),
        "instrument.detector.lr_flipped": (False, True),
        "instrument.detector.ud_flipped": (True, True),
        "instrument.source.distance": (54.8, True),
        "sample.propagation_distance": (22.0, True),
        "sample.x_pixel_size": (2.3e-5, True),
        "sample.y_pixel_size": (2.5e-5, True),
        "sample.x_translation": (None,),
        "sample.z_translation": (None,),
    }

    for lockerButton in widget._lockerPBs:
        lockerButton.setLock(False)

    assert widget.getConfiguration() == {
        "instrument.beam.energy": (5.9, False),
        "instrument.detector.distance": (2.4, False),
        "instrument.detector.field_of_view": ("Full", False),
        "instrument.detector.x_pixel_size": (0.023, False),
        "instrument.detector.y_pixel_size": (0.025, False),
        "instrument.detector.lr_flipped": (False, False),
        "instrument.detector.ud_flipped": (True, False),
        "instrument.source.distance": (54.8, False),
        "sample.x_translation": (None,),
        "sample.z_translation": (None,),
        "sample.propagation_distance": (22.0, False),
        "sample.x_pixel_size": (2.3e-5, False),
        "sample.y_pixel_size": (2.5e-5, False),
        "sample.x_translation": (None,),
        "sample.z_translation": (None,),
    }


def test_nxtomo_editor_with_missing_paths(
    tmp_path,
    qtapp,  # noqa F811
):
    """
    test widget behavior in the case some nxtomo path don't exist
    """

    # create nx tomo with raw data
    nx_tomo = NXtomo()
    nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo.sample.rotation_angle = numpy.linspace(0, 20, num=12) * _ureg.degree

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo.save(
        file_path=file_path,
        data_path=entry,
    )
    # delete some path that can be missing in some case
    with h5py.File(file_path, mode="a") as h5f:
        assert "entry0000" in h5f
        assert "entry0000/beam" not in h5f
        assert "entry0000/instrument/beam" not in h5f
        assert "entry0000/instrument/detector/distance" not in h5f
        assert "entry0000/instrument/detector/x_pixel_size" not in h5f
        assert "entry0000/instrument/detector/y_pixel_size" not in h5f
        assert "entry0000/instrument/detector/transformations" not in h5f

    scan = NXtomoScan(file_path, entry)

    # create the widget and do the edition
    widget = NXtomoEditor()

    widget.setScan(scan=scan)

    widget._sampleDetectorDistanceMetricEntry.setValue(0.05)
    widget._energyEntry.setValue(50.0)
    widget._xDetectorPixelSizeMetricEntry.setValue(0.02)
    widget._yDetectorPixelSizeMetricEntry.setValue(0.03)

    # overwrite the NXtomo
    task = NXtomoEditorTask(
        inputs={
            "data": scan,
            "configuration": widget.getConfigurationForTask(),
        }
    )
    task.run()

    # check save went well
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
    )
    assert overwrite_nx_tomo.instrument.detector.x_pixel_size == 0.02 * _ureg.meter
    assert overwrite_nx_tomo.instrument.detector.y_pixel_size == 0.03 * _ureg.meter
    assert overwrite_nx_tomo.energy == 50 * _ureg.keV
    assert overwrite_nx_tomo.instrument.detector.distance == 0.05 * _ureg.meter
