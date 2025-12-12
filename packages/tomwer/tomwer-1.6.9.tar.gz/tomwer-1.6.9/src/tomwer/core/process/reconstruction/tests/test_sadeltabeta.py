# coding: utf-8
from __future__ import annotations


import os
import shutil
import tempfile
import unittest

from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
    SADeltaBetaParams,
    SADeltaBetaTask,
)
from tomwer.core.utils.scanutils import MockNXtomo


class TestSADeltaBetaProcess(unittest.TestCase):
    """Test the SAAxisProcess class"""

    def setUp(self) -> None:
        super().setUp()
        self.tempdir = tempfile.mkdtemp()
        dim = 10
        mock = MockNXtomo(
            scan_path=self.tempdir, n_proj=10, n_ini_proj=10, scan_range=180, dim=dim
        )
        self.scan = mock.scan

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)
        super().tearDown()

    def test(self):
        process = SADeltaBetaTask(
            inputs={
                "data": self.scan,
                "sa_delta_beta_params": SADeltaBetaParams().to_dict(),
                "serialize_output_data": False,
            }
        )

        default_sadelta_beta_params = SADeltaBetaParams()
        default_sadelta_beta_params.output_dir = os.path.join(
            self.tempdir, "output_dir"
        )
        default_sadelta_beta_params.dry_run = True

        process.run()
