import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.reconstruction.nabu.nabuconfig.ctf import CTFConfig
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestFutureSupervisorOW(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._widget = CTFConfig()

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self._widget = None
        return super().tearDown()

    def test_configuration(self):
        """
        test configuration setter and getter
        """
        self._widget.show()
        config = self._widget.getConfiguration()
        assert isinstance(config, dict)

        assert config == {
            "ctf_geometry": " z1_v=None; z1_h=None; detec_pixel_size=None; magnification=True",
            "ctf_advanced_params": " length_scale=1e-05; lim1=1e-05; lim2=0.2; normalize_by_mean=True",
            "beam_shape": "parallel",
        }

        config["beam_shape"] = "cone"
        config["ctf_geometry"] = (
            " z1_v=10.2; z1_h=3.6; detec_pixel_size=1e-05; magnification=False"
        )
        config["ctf_advanced_params"] = (
            " length_scale=2e-05; lim1=1e-08; lim2=0.1; normalize_by_mean=False"
        )

        self._widget.setConfiguration(config)
        assert self._widget.getConfiguration() == config
