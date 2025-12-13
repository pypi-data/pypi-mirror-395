import pytest
import numpy

from tomwer.gui.reconstruction.axis.AxisSettingsWidget import AxisSettingsTabWidget
from tomwer.synctools.axis import QAxisRP
from tomwer.tests.utils import skip_gui_test
from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_get_nabu_cor_opts(qtapp):  # noqa F811
    axis_params = QAxisRP()
    widget = AxisSettingsTabWidget(recons_params=axis_params)
    assert axis_params.get_nabu_cor_options_as_dict() == {
        "side": "right",
        "radio_angles": (0.0, numpy.pi),
        "slice_idx": "middle",
    }
    widget._optionsWidget._corOpts.setText("low_pass=2.0")
    widget._optionsWidget._corOpts.editingFinished.emit()
    assert axis_params.get_nabu_cor_options_as_dict() == {
        "side": "right",
        "radio_angles": (0.0, numpy.pi),
        "slice_idx": "middle",
        "low_pass": 2.0,
    }
    widget._optionsWidget._corOpts.setText("low_pass=2 ; high_pass=10")
    widget._optionsWidget._corOpts.editingFinished.emit()
    assert axis_params.get_nabu_cor_options_as_dict() == {
        "side": "right",
        "radio_angles": (0.0, numpy.pi),
        "slice_idx": "middle",
        "low_pass": 2.0,
        "high_pass": 10.0,
    }
    widget._calculationWidget.setEstimatedCorValue("left")
    assert axis_params.get_nabu_cor_options_as_dict() == {
        "side": "left",
        "radio_angles": (0.0, numpy.pi),
        "slice_idx": "middle",
        "low_pass": 2.0,
        "high_pass": 10.0,
    }
