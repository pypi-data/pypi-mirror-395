# coding: utf-8
from __future__ import annotations

import os
import shutil
import tempfile
import unittest

from tomwer.core.process.script.python import PythonScript
from tomwer.core.utils.scanutils import MockNXtomo


class TestPythonScript(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        dim = 10
        mock = MockNXtomo(
            scan_path=os.path.join(self.tempdir, "scan1"),
            n_proj=10,
            n_ini_proj=10,
            scan_range=180,
            dim=dim,
        )
        self.scan = mock.scan

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test(self):
        process = PythonScript(inputs={"data": self.scan})
        process.definition()
        process.program_version()
        process.program_name()
        # TODO: configuration should be passed in inputs during construction
        process.set_configuration(
            {
                "scriptText": "print('toto')",
            }
        )

        process.run()
