# coding: utf-8
from __future__ import annotations


import os
import shutil
import tempfile

import h5py
import numpy
import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from silx.io.url import DataUrl

from tomwer.core.process.reconstruction.sadeltabeta.params import SADeltaBetaParams
from tomwer.core.process.reconstruction.scores import ComputedScore
from tomwer.core.process.reconstruction.scores.params import ScoreMethod
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.gui.reconstruction.sadeltabeta import SADeltaBetaWindow
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSADeltaBetaWindow(TestCaseQt):
    """Test the SAAxisWindow interface"""

    _N_OUTPUT_URLS = 10

    def setUp(self):
        super().setUp()
        self._window = SADeltaBetaWindow()
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
        conf = SADeltaBetaParams.from_dict(conf)
        self.assertEqual(conf.slice_indexes, "middle")
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
        self.assertEqual(conf.score_method, ScoreMethod.TV_INVERSE)
        self.assertEqual(conf.output_dir, None)
        self.assertEqual(conf.scores, None)

    def testSetConfiguration(self):
        """Insure configuration setter works"""
        nabu_specific_params = {
            "phase": {
                "padding_type": "zeros",
                "unsharp_coeff": 5.36,
                "unsharp_sigma": 4.1,
            },
        }
        self._window.setSlicesRange(0, 20)
        configuration = {
            "slice_index": {"Slice": 2},
            "delta_beta_values": (50, 100, 200),
            "score_method": "standard deviation",
            "nabu_params": nabu_specific_params,
        }
        self._window.setConfiguration(configuration)
        res_conf = self._window.getConfiguration()
        for key in (
            "slice_index",
            "delta_beta_values",
            "score_method",
        ):
            self.assertEqual(configuration[key], res_conf[key])
        for key, value in nabu_specific_params["phase"].items():
            assert value == res_conf["nabu_params"]["phase"][key]

    def testSetResults(self):
        """Test setting results"""
        self._window.setDBScores(self._cor_scores, score_method="total variation")
        # test saving snapshots
        with tempfile.TemporaryDirectory() as output_png_imgs:
            final_dir = os.path.join(output_png_imgs, "test/create/it")
            self._window.saveReconstructedSlicesTo(final_dir)
            assert os.path.exists(final_dir)
            assert len(os.listdir(final_dir)) == len(self._cor_scores)
