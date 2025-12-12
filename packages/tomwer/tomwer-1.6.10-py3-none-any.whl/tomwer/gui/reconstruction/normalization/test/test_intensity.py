# coding: utf-8
from __future__ import annotations

import os
import shutil
import tempfile

from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.process.reconstruction.normalization.params import (
    Method as NormalizationMethod,
)
from tomwer.core.process.reconstruction.normalization.params import (
    _ValueSource as NormalizationSource,
)
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.gui.reconstruction.normalization.intensity import SinoNormWindow


class TestNormIntensityWindow(TestCaseQt):
    def setUp(self):
        super(TestNormIntensityWindow, self).setUp()
        self._widget = SinoNormWindow(parent=None)
        self._tmp_dir = tempfile.mkdtemp()
        scan_path = os.path.join(self._tmp_dir, "my_scan_2")
        self.scan = MockNXtomo(
            scan_path=scan_path,
            n_ini_proj=10,
            n_proj=10,
            n_alignement_proj=2,
            create_final_flat=False,
            create_ini_dark=True,
            create_ini_flat=True,
            n_refs=1,
        ).scan

    def tearDown(self):
        self._widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._widget.close()
        self.qapp.processEvents()
        self._widget = None
        shutil.rmtree(self._tmp_dir)
        super(TestNormIntensityWindow, self).tearDown()

    def test(self):
        self._widget.setScan(self.scan)
        self._widget.show()
        self.qWaitForWindowExposed(self._widget)
        self._widget.setCurrentMethod(NormalizationMethod.NONE)
        self.qapp.processEvents()
        assert self._widget.getConfiguration() == {"source": "none", "method": "none"}

        self._widget.setCurrentMethod(NormalizationMethod.CHEBYSHEV)
        self.qapp.processEvents()
        assert self._widget.getConfiguration() == {
            "method": "chebyshev",
            "source": "none",
        }

        self._widget.setCurrentMethod(NormalizationMethod.SUBTRACTION)
        self.qapp.processEvents()
        self._widget.setCurrentSource(NormalizationSource.MANUAL_ROI)
        self.qapp.processEvents()
        output_configuration = self._widget.getConfiguration()
        assert output_configuration["method"] == "subtraction"
        assert output_configuration["source"] == "manual ROI"
        assert "start_x" in output_configuration
        assert "end_x" in output_configuration
        assert "start_y" in output_configuration
        assert "end_y" in output_configuration
        assert "calc_fct" in output_configuration
        self._widget.setCurrentMethod(NormalizationMethod.DIVISION)
        self.qapp.processEvents()
        self._widget.setCurrentSource(NormalizationSource.DATASET)
        self.qapp.processEvents()
        output_configuration = self._widget.getConfiguration()
        assert output_configuration["method"] == "division"
        assert output_configuration["source"] == "from dataset"
        assert "dataset_url" in output_configuration

        self._widget.setCurrentMethod(NormalizationMethod.DIVISION)
        self.qapp.processEvents()
        self._widget.setCurrentSource(NormalizationSource.MANUAL_SCALAR)
        self.qapp.processEvents()
        output_configuration = self._widget.getConfiguration()
        assert output_configuration["method"] == "division"
        assert output_configuration["source"] == "scalar"
        assert "value" in output_configuration
