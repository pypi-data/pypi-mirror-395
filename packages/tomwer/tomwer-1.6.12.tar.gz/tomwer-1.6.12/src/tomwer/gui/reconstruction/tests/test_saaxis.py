# coding: utf-8
from __future__ import annotations


import os
import pint
import shutil
import tempfile

import h5py
import numpy
import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from silx.io.url import DataUrl

from tomwer.core.process.reconstruction.saaxis.params import (
    ReconstructionMode,
    SAAxisParams,
)
from tomwer.core.process.reconstruction.scores import ComputedScore
from tomwer.core.process.reconstruction.scores.params import ScoreMethod
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.gui.reconstruction.saaxis.dimensionwidget import DimensionWidget
from tomwer.gui.reconstruction.saaxis.saaxis import SAAxisWindow
from tomwer.tests.utils import skip_gui_test


_ureg = pint.get_application_registry()


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestDimensionWidget(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        self._window = DimensionWidget(title="test window")

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()

    def testDimension(self):
        """Insure setting dimensions values and unit are correct"""
        # check initial values
        self.assertEqual(
            self._window.getQuantities(),
            (1.0 * _ureg.millimeter, 1.0 * _ureg.millimeter, 1.0 * _ureg.millimeter),
        )
        # set dim 0 to 20 mm
        self._window._dim0ValueQLE.setValue(20)
        self._window._dim0ValueQLE.editingFinished.emit()
        self.qapp.processEvents()
        self.assertEqual(
            self._window.getQuantities(cast_unit_to=_ureg.meter),
            (0.02 * _ureg.meter, 0.001 * _ureg.meter, 0.001 * _ureg.meter),
        )
        # set dim 1 to 0.6 millimeter
        self._window._dim1ValueQLE.setValue(0.6)
        self._window._dim1ValueQLE.editingFinished.emit()
        self.qapp.processEvents()
        self.assertEqual(
            self._window.getQuantities(cast_unit_to=_ureg.meter),
            (0.02 * _ureg.meter, 0.0006 * _ureg.meter, 0.001 * _ureg.meter),
        )
        # change display to micrometer
        self._window.setUnit(_ureg.millimeter)
        self.assertEqual(
            self._window.getQuantities(cast_unit_to=_ureg.meter),
            (0.02 * _ureg.meter, 0.0006 * _ureg.meter, 0.001 * _ureg.meter),
        )
        self.assertEqual(
            self._window._dim0Value,
            20 * _ureg.millimeter,
        )
        self._window._dim2ValueQLE.setValue(500)
        self._window._dim2ValueQLE.editingFinished.emit()
        self.qapp.processEvents()
        self.assertEqual(
            self._window.getQuantities(cast_unit_to=_ureg.meter),
            (0.02 * _ureg.meter, 0.0006 * _ureg.meter, 0.5 * _ureg.meter),
        )

    def testConstructorWithColors(self):
        """Insure passing colors works"""
        DimensionWidget(title="title", dims_colors=("#ffff5a", "#62efff", "#ff5bff"))

    def testConstructorWithDimNames(self):
        """Insure passing colors works"""
        DimensionWidget(title="title", dims_name=("x", "y", "z"))


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSAAxisWindow(TestCaseQt):
    """Test the SAAxisWindow interface"""

    _N_OUTPUT_URLS = 10

    def setUp(self):
        super().setUp()
        self._window = SAAxisWindow()
        self.folder = tempfile.mkdtemp()
        self._output_urls = []
        self._cor_scores = {}

        for i in range(self._N_OUTPUT_URLS):
            output_file = os.path.join(self.folder, f"recons_{i}.h5")
            with h5py.File(output_file, mode="a") as h5f:
                h5f["data"] = numpy.random.random(100 * 100).reshape(100, 100)
                url = DataUrl(file_path=output_file, data_path="data", scheme="silx")
                assert url.is_valid()
            self._output_urls.append(url)
            score = ComputedScore(
                tv=numpy.random.randint(10),
                std=numpy.random.randint(100),
            )
            self._cor_scores[i] = (url, score)

        # create a scan
        self.folder = tempfile.mkdtemp()
        dim = 10
        mock = MockNXtomo(
            scan_path=self.folder, n_proj=10, n_ini_proj=10, scan_range=180, dim=dim
        )
        mock.add_alignment_radio(index=10, angle=90)
        mock.add_alignment_radio(index=10, angle=0)
        self.scan = mock.scan

        self._window.setScan(self.scan)

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()
        self._window = None
        shutil.rmtree(self.folder)
        super().tearDown()

    def testGetConfiguration(self):
        """Insure configuration getter works"""
        conf = self._window.getConfiguration()
        # the configuration should be convertible to
        conf = SAAxisParams.from_dict(conf)
        self.assertEqual(conf.slice_indexes, "middle")
        self.assertEqual(conf.file_format, "hdf5")
        self.assertTrue(isinstance(conf.nabu_recons_params, dict))
        for key in (
            "preproc",
            "reconstruction",
            "dataset",
            "tomwer_slices",
            "output",
            "phase",
        ):
            with self.subTest(key=key):
                self.assertTrue(key in conf.nabu_recons_params)
        self.assertEqual(conf._dry_run, False)
        self.assertEqual(conf.mode, ReconstructionMode.VERTICAL)
        self.assertEqual(conf.score_method, ScoreMethod.TV_INVERSE)
        self.assertEqual(conf.output_dir, None)
        self.assertEqual(conf.scores, None)

    def testSetConfiguration(self):
        """Insure configuration setter works"""
        self._window.setSlicesRange(0, 20)
        configuration = {
            "slice_index": {"Slice": 2},
            "estimated_cor": 0.24,
            "research_width": 0.8,
            "n_reconstruction": 5,
        }
        self._window.setConfiguration(configuration)
        res_conf = self._window.getConfiguration()
        for key in (
            "slice_index",
            "estimated_cor",
            "research_width",
            "n_reconstruction",
        ):
            self.assertEqual(configuration[key], res_conf[key])

    def testSetResults(self):
        """Test setting results and saving result to a folder"""
        self._window.setCorScores(self._cor_scores, score_method="standard deviation")
        # test saving snapshots
        with tempfile.TemporaryDirectory() as output_png_imgs:
            final_dir = os.path.join(output_png_imgs, "test/create/it")
            self._window.saveReconstructedSlicesTo(final_dir)
            assert os.path.exists(final_dir)
            assert len(os.listdir(final_dir)) == len(self._cor_scores)
