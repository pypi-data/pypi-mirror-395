from tomwer.gui.reconstruction.nabu.nabuconfig.preprocessing import (
    SinoRingsOptions,
    TiltCorrection,
    RingCorrectionMethod,
)
from tomwer.tests.conftest import qtapp  # noqa F401


def test_tilt_correction_widget(qtapp):  # noqa F811
    """
    Test of TiltCorrection
    """
    widget = TiltCorrection(text="")
    assert not widget._tiltManualRB.isChecked()
    assert widget._autoManualRB.isChecked()
    assert widget.getTiltCorrection() == ("1d-correlation", "")
    widget.setTiltCorrection(0.0)
    assert widget.getTiltCorrection() == (0.0, "")
    assert widget._tiltManualRB.isChecked()
    assert not widget._autoManualRB.isChecked()
    widget.setTiltCorrection("fft-polar", auto_tilt_options="low_pass=10")
    assert widget.getTiltCorrection() == ("fft-polar", "low_pass=10")
    assert not widget._tiltManualRB.isChecked()
    assert widget._autoManualRB.isChecked()


def test_sino_rings_options(qtapp):  # noqa F811
    """
    Test of SinoRingsOptions
    """
    widget = SinoRingsOptions()
    # test munch options
    assert widget.getOptions() == {
        "sigma": 1.0,
        "levels": 10,
        "padding": False,
    }

    widget.setOptions(
        {
            "sigma": 3.25,
            "levels": 564,
            "padding": True,
        }
    )
    assert widget.getOptions() == {
        "sigma": 3.25,
        "levels": 564,
        "padding": True,
    }
    # test mean division
    widget.setMethod(method=RingCorrectionMethod.MEAN_DIVISION)
    assert widget.getOptions() == {
        "filter_cutoff": (0, 30),
    }

    # test VO deringer
    widget.setMethod(method=RingCorrectionMethod.VO.value)
    assert widget.getOptions() == {
        "dim": 1,
        "la_size": 51,
        "sm_size": 21,
        "snr": 3.0,
    }
    new_vo_options = {
        "dim": 2,
        "la_size": 42,
        "sm_size": 22,
        "snr": 6.3,
    }
    widget.setOptions(new_vo_options)
    assert widget.getOptions() == new_vo_options

    # test mean division
    new_mean_division_options = {
        "filter_cutoff": (10, 23),
    }

    widget.setMethod(method=RingCorrectionMethod.MEAN_DIVISION)
    widget.setOptions(new_mean_division_options)
    assert widget.getOptions() == new_mean_division_options
